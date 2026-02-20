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

    def update_info(self, df: pd.DataFrame) -> None:
        if df is None or df.empty:
            self.update("No company data available")
            return

        row = df.iloc[0]
        lines = [
            f"[bold]{row.get('stock_name', 'N/A')}[/bold]",
            f"Code: {row.get('stock_code', 'N/A')}",
            f"Market: {row.get('market_name', 'N/A')}",
            f"Sector: {row.get('sector_name', 'N/A')}",
            "",
            "[bold]Fundamentals[/bold]",
            f"Market Cap: {row.get('market_cap', 'N/A')}",
            f"PER: {row.get('per', 'N/A')}",
            f"PBR: {row.get('pbr', 'N/A')}",
            f"ROE: {row.get('roe', 'N/A')}",
            f"EPS: {row.get('eps', 'N/A')}",
            f"BPS: {row.get('bps', 'N/A')}",
        ]

        self.update("\n".join(lines))
