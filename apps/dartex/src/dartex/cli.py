import typer
from rich.console import Console

app = typer.Typer(help="dartex: DART 재무제표 주석 파싱 도구")
console = Console()


@app.command()
def search(name: str = typer.Argument(..., help="기업명 검색어")):
    """기업 검색"""
    console.print(f"[yellow]검색 기능 구현 예정: {name}[/yellow]")


@app.command()
def collect(
    corp_code: str = typer.Option(..., "--corp-code", "-c", help="기업 코드"),
    years: int = typer.Option(5, "--years", "-y", help="수집 연도 수"),
):
    """특정 기업의 주석 데이터 수집"""
    console.print(f"[yellow]수집 기능 구현 예정: {corp_code}, {years}년[/yellow]")


@app.command()
def show(
    corp_code: str = typer.Option(..., "--corp-code", "-c"),
    section: str = typer.Option(None, "--section", "-s", help="주석 섹션명"),
    year: int = typer.Option(None, "--year", help="조회 연도"),
):
    """저장된 주석 데이터 조회"""
    console.print("[yellow]조회 기능 구현 예정[/yellow]")


@app.command()
def timeseries(
    corp_code: str = typer.Option(..., "--corp-code", "-c"),
    section: str = typer.Option(..., "--section", "-s"),
    format: str = typer.Option("table", "--format", "-f", help="출력 형식 (table, csv, json)"),
):
    """시계열 데이터 조회"""
    console.print("[yellow]시계열 기능 구현 예정[/yellow]")


@app.command()
def export(
    corp_code: str = typer.Option(..., "--corp-code", "-c"),
    output: str = typer.Option("./export", "--output", "-o"),
    format: str = typer.Option("excel", "--format", "-f", help="excel, csv"),
):
    """데이터 내보내기"""
    console.print("[yellow]내보내기 기능 구현 예정[/yellow]")


if __name__ == "__main__":
    app()
