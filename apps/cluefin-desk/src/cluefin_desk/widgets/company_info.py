import pandas as pd
from textual.widgets import Static


class CompanyInfoWidget(Static):
    """Company basic info panel."""

    DEFAULT_CSS = """
    CompanyInfoWidget {
        height: 1fr;
        padding: 1;
    }
    """

    @staticmethod
    def _has(row: pd.Series, key: str) -> bool:
        value = row.get(key)
        return value is not None and not pd.isna(value) and str(value) != ""

    @classmethod
    def format_lines(cls, row: pd.Series) -> list[str]:
        """Render the info panel lines. KIS-only fields are shown only when present,
        so the same widget serves both the Kiwoom and KIS basic-data shapes."""
        lines = [
            f"[bold]{row.get('stock_name', 'N/A')}[/bold]",
            f"Code: {row.get('stock_code', 'N/A')}",
            f"Market: {row.get('market_name', 'N/A')}",
            f"Sector: {row.get('sector_name', 'N/A')}",
        ]
        if cls._has(row, "state") and row.get("state") != "정상":
            lines.append(f"[red]State: {row.get('state')}[/red]")

        if cls._has(row, "current_price"):
            lines += [
                "",
                "[bold]Price[/bold]",
                f"현재가: {row.get('current_price')} ({row.get('price_change_rate', '-')}%)",
                f"52주: {row.get('52_week_low', '-')} ~ {row.get('52_week_high', '-')}",
            ]

        lines += [
            "",
            "[bold]Fundamentals[/bold]",
            f"Market Cap: {row.get('market_cap', 'N/A')}",
            f"PER: {row.get('per', 'N/A')}",
            f"PBR: {row.get('pbr', 'N/A')}",
            f"ROE: {row.get('roe', 'N/A')}",
            f"EPS: {row.get('eps', 'N/A')}",
            f"BPS: {row.get('bps', 'N/A')}",
        ]

        if cls._has(row, "financial_period"):
            lines += [
                "",
                f"[bold]Financials ({row.get('financial_period')})[/bold]",
                f"매출액: {row.get('revenue', '-')}",
                f"영업이익: {row.get('operating_profit', '-')}",
                f"당기순이익: {row.get('net_profit', '-')}",
                f"부채비율: {row.get('debt_ratio', '-')}%",
            ]

        if cls._has(row, "foreign_exhaustion_rate"):
            lines += [
                "",
                "[bold]Supply/Demand[/bold]",
                f"외인소진율: {row.get('foreign_exhaustion_rate')}%",
                f"신용비율: {row.get('credit_ratio', '-')}%",
            ]

        return lines

    def update_info(self, df: pd.DataFrame) -> None:
        if df is None or df.empty:
            self.update("No company data available")
            return

        self.update("\n".join(self.format_lines(df.iloc[0])))
