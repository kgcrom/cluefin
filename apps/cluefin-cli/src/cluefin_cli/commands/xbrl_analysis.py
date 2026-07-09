"""XBRL disclosure analysis command.

Parses and displays *everything* ``cluefin-xbrl`` can extract from a DART XBRL
filing: a document overview, the structured financial statements (연결/별도),
and the disclosure notes (주석).
"""

import asyncio

import click
from loguru import logger
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cluefin_cli.data.fundamentals import DomesticFundamentalDataFetcher, default_business_year
from cluefin_cli.data.xbrl import REPORT_CODE_MAP, XbrlBundle, XbrlStatementFetcher
from cluefin_cli.utils.formatters import format_number

console = Console()

STATEMENT_TYPE_LABELS: dict[str, str] = {
    "BS": "Statement of Financial Position (재무상태표)",
    "IS": "Income Statement (손익계산서)",
    "CIS": "Comprehensive Income Statement (포괄손익계산서)",
    "CF": "Cash Flow Statement (현금흐름표)",
    "SCE": "Statement of Changes in Equity (자본변동표)",
}

SECTION_CHOICES = ["all", "overview", "statements", "notes"]


@click.command(name="xbrl")
@click.argument("stock_code")
@click.option(
    "--year",
    default=default_business_year(),
    show_default=True,
    help="Business year (YYYY) to analyse.",
)
@click.option(
    "--report",
    type=click.Choice(list(REPORT_CODE_MAP.keys()), case_sensitive=False),
    default="annual",
    show_default=True,
    help="DART report period.",
)
@click.option(
    "--section",
    type=click.Choice(SECTION_CHOICES, case_sensitive=False),
    default="all",
    show_default=True,
    help="Which section(s) to display.",
)
@click.option(
    "--statement-type",
    type=click.Choice(["BS", "IS", "CIS", "CF", "SCE"], case_sensitive=False),
    default=None,
    help="Filter statements to a specific type. Show all if not set.",
)
@click.option(
    "--note",
    "note_filter",
    default=None,
    help="Filter notes to a specific role code (e.g. D810000) or a title substring.",
)
@click.option(
    "--consolidated/--separate",
    "consolidated",
    default=True,
    show_default=True,
    help="Show consolidated (연결) or separate (별도) data.",
)
@click.option(
    "--max-rows",
    type=int,
    default=60,
    show_default=True,
    help="Max line items rendered per note (0 = unlimited).",
)
def xbrl_analysis(
    stock_code: str,
    year: str,
    report: str,
    section: str,
    statement_type: str | None,
    note_filter: str | None,
    consolidated: bool,
    max_rows: int,
) -> None:
    """Parse and display all XBRL data (statements + notes) for a stock code."""
    reprt_code = REPORT_CODE_MAP[report.lower()]

    basis = "consolidated" if consolidated else "separate"
    console.print(f"[bold blue]XBRL Analysis for {stock_code} ({year}, {report}, {basis})[/bold blue]")

    try:
        asyncio.run(
            _perform_xbrl_analysis(
                stock_code=stock_code,
                year=year,
                reprt_code=reprt_code,
                section=section.lower(),
                statement_type=statement_type,
                note_filter=note_filter,
                consolidated=consolidated,
                max_rows=max_rows,
            )
        )
    except Exception as exc:
        console.print(f"[red]Error during XBRL analysis: {exc}[/red]")
        logger.exception(f"XBRL analysis failed for {stock_code}")


async def _perform_xbrl_analysis(
    stock_code: str,
    year: str,
    reprt_code: str,
    section: str,
    statement_type: str | None,
    note_filter: str | None,
    consolidated: bool,
    max_rows: int,
) -> None:
    fundamental_fetcher = DomesticFundamentalDataFetcher()
    corp_code = await fundamental_fetcher.get_corp_code(stock_code)

    xbrl_fetcher = XbrlStatementFetcher()

    console.print("[dim]Searching for report filing...[/dim]")
    rcept_no = xbrl_fetcher.find_rcept_no(corp_code, year, reprt_code)
    if rcept_no is None:
        console.print(f"[red]No report filing found for {stock_code} ({year}).[/red]")
        return

    console.print(f"[dim]Downloading & parsing XBRL (rcept_no={rcept_no})...[/dim]")
    bundle = xbrl_fetcher.fetch(corp_code, rcept_no, reprt_code)

    show_overview = section in ("all", "overview")
    show_statements = section in ("all", "statements")
    show_notes = section in ("all", "notes")

    if show_overview:
        _display_overview(bundle, consolidated)

    if show_statements:
        _display_statements(bundle, statement_type, consolidated)

    if show_notes:
        _display_notes(bundle, note_filter, consolidated, max_rows)


# --------------------------------------------------------------------------- #
# Overview
# --------------------------------------------------------------------------- #
def _display_overview(bundle: XbrlBundle, consolidated: bool) -> None:
    """Render a high-level summary of the parsed document."""
    doc = bundle.document
    stmts = bundle.statements
    notes = bundle.notes

    n_note_cons = sum(1 for n in notes.notes.values() if n.is_consolidated)
    n_note_sep = len(notes.notes) - n_note_cons

    table = Table(box=box.SIMPLE, show_header=False)
    table.add_column("Field", style="bold", min_width=24)
    table.add_column("Value")

    table.add_row("Source file", doc.source_file)
    table.add_row("Entity ID", doc.entity_id or "-")
    table.add_row("Reporting period end", str(doc.reporting_period_end) if doc.reporting_period_end else "-")
    table.add_row("Total facts", format_number(len(doc.facts)))
    table.add_row("Consolidated statements", ", ".join(stmts.statements.keys()) or "-")
    table.add_row("Separate statements", ", ".join(stmts.separate_statements.keys()) or "-")
    table.add_row("Notes (연결/별도)", f"{n_note_cons} / {n_note_sep}")

    console.print(Panel(table, title="[bold]Document Overview[/bold]", expand=False))


# --------------------------------------------------------------------------- #
# Financial statements
# --------------------------------------------------------------------------- #
def _display_statements(bundle: XbrlBundle, statement_type: str | None, consolidated: bool) -> None:
    basis = "consolidated" if consolidated else "separate"
    statements = bundle.statements.statements if consolidated else bundle.statements.separate_statements

    console.print(f"\n[bold underline]Financial Statements ({basis})[/bold underline]")

    if not statements:
        console.print(f"[yellow]No {basis} financial statements found in the XBRL data.[/yellow]")
        return

    target_type = statement_type.upper() if statement_type else None
    displayed = False

    for stmt_key, stmt in statements.items():
        if target_type and stmt_key != target_type:
            continue
        _display_statement(stmt_key, stmt)
        displayed = True

    if not displayed and target_type:
        available = ", ".join(statements.keys())
        console.print(f"[yellow]Statement type '{target_type}' not found. Available: {available}[/yellow]")


def _display_statement(stmt_key: str, stmt) -> None:
    """Render a single financial statement as a Rich table."""
    title = STATEMENT_TYPE_LABELS.get(stmt_key, stmt_key)
    console.print(f"\n[bold cyan]{title}[/bold cyan]")

    # Statement-intrinsic dimensions (e.g. equity components on the SCE) need
    # their own column; plain statements (BS/IS/...) have none.
    has_dimensions = any(item.dimensions for item in stmt.line_items)

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("Account", min_width=30)
    table.add_column("Label (KO)", min_width=20)
    table.add_column("Value", justify="right", min_width=15)
    table.add_column("Unit", min_width=6)
    table.add_column("Period", min_width=12)
    if has_dimensions:
        table.add_column("Dimensions", min_width=16)

    for item in stmt.line_items:
        indent = "  " * item.depth
        concept = f"{indent}{item.concept_local_name}"

        label_ko = item.label_ko or ""
        if item.is_abstract:
            concept = f"[bold]{concept}[/bold]"
            label_ko = f"[bold]{label_ko}[/bold]" if label_ko else ""

        value_str = _format_value(item.value)
        unit_str = item.unit or ""
        period_str = _format_period(item.period)

        row = [concept, label_ko, value_str, unit_str, period_str]
        if has_dimensions:
            row.append(_format_dimensions(item.dimensions))
        table.add_row(*row)

    console.print(Panel(table, expand=False))


# --------------------------------------------------------------------------- #
# Notes (주석)
# --------------------------------------------------------------------------- #
def _display_notes(bundle: XbrlBundle, note_filter: str | None, consolidated: bool, max_rows: int) -> None:
    basis = "consolidated" if consolidated else "separate"
    console.print(f"\n[bold underline]Disclosure Notes / 주석 ({basis})[/bold underline]")

    all_notes = [n for n in bundle.notes.notes.values() if n.is_consolidated == consolidated]

    if not all_notes:
        console.print(f"[yellow]No {basis} disclosure notes found in the XBRL data.[/yellow]")
        return

    # Sort by role code for a stable, readable order.
    all_notes.sort(key=lambda n: n.role_code)

    selected = _filter_notes(all_notes, note_filter)
    if not selected:
        console.print(f"[yellow]No notes matched filter '{note_filter}'.[/yellow]")
        return

    _display_notes_summary(selected)

    for note in selected:
        _display_note_section(note, max_rows)


def _filter_notes(notes: list, note_filter: str | None) -> list:
    if not note_filter:
        return notes
    needle = note_filter.lower()
    return [n for n in notes if needle in n.role_code.lower() or (n.title and needle in n.title.lower())]


def _display_notes_summary(notes: list) -> None:
    """Render an index of the note sections before diving into details."""
    table = Table(box=box.SIMPLE, title="Notes Index")
    table.add_column("Role", style="bold cyan")
    table.add_column("Title")
    table.add_column("Items", justify="right")
    table.add_column("With values", justify="right")

    for note in notes:
        n_items = len(note.line_items)
        n_valued = sum(1 for it in note.line_items if it.value is not None or it.text_value is not None)
        table.add_row(note.role_code, note.title or "-", str(n_items), str(n_valued))

    console.print(table)


def _display_note_section(note, max_rows: int) -> None:
    """Render a single note section as a Rich table."""
    title = f"[{note.role_code}] {note.title or '(untitled)'}"
    console.print(f"\n[bold magenta]{title}[/bold magenta]")

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("Concept", min_width=26)
    table.add_column("Label (KO)", min_width=18)
    table.add_column("Value", justify="right", min_width=12)
    table.add_column("Text", min_width=16)
    table.add_column("Period", min_width=12)
    table.add_column("Dimensions", min_width=16)

    items = note.line_items
    truncated = 0
    if max_rows and len(items) > max_rows:
        truncated = len(items) - max_rows
        items = items[:max_rows]

    for item in items:
        indent = "  " * item.depth
        concept = f"{indent}{item.concept_local_name}"
        label_ko = item.label_ko or ""
        if item.is_abstract:
            concept = f"[bold]{concept}[/bold]"
            label_ko = f"[bold]{label_ko}[/bold]" if label_ko else ""

        value_str = _format_value(item.value)
        text_str = _truncate(item.text_value, 40)
        period_str = _format_period(item.period)
        dim_str = _format_dimensions(item.dimensions)

        table.add_row(concept, label_ko, value_str, text_str, period_str, dim_str)

    console.print(Panel(table, expand=False))
    if truncated:
        console.print(f"[dim]... {truncated} more line item(s) hidden (use --max-rows 0 to show all).[/dim]")


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def _format_value(value) -> str:
    if value is None:
        return "-"
    try:
        return format_number(int(value))
    except (ValueError, OverflowError, TypeError):
        return str(value)


def _format_period(period) -> str:
    """Format an XbrlPeriod for display."""
    if period is None:
        return "-"
    if period.instant is not None:
        return str(period.instant)
    if period.start_date is not None and period.end_date is not None:
        return f"{period.start_date}~{period.end_date}"
    return "-"


def _format_dimensions(dimensions: dict[str, str]) -> str:
    """Compactly format a fact's dimensional context."""
    if not dimensions:
        return "-"
    parts = [f"{_local(axis)}={_local(member)}" for axis, member in dimensions.items()]
    return "; ".join(parts)


def _local(qname: str) -> str:
    """Reduce a qname / URI to its readable local segment."""
    for sep in ("#", ":", "/"):
        if sep in qname:
            qname = qname.rsplit(sep, 1)[-1]
    return qname


def _truncate(text: str | None, limit: int) -> str:
    if not text:
        return ""
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"
