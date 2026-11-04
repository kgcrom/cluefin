from typing import Any

from textual.app import ComposeResult
from textual.widgets import Static


class MarketOverviewBar(Static):
    """KOSPI/KOSDAQ index summary bar.

    장세(KOSPI200 60일선 대비) 칸은 지수 칸과 별도 워커에서 비동기로 채워지므로,
    각자 상태를 들고 있다가 `_refresh_text` 에서 합친다 — 먼저 끝난 쪽이 나중 쪽을 지우지 않는다.
    """

    DEFAULT_CSS = """
    MarketOverviewBar {
        height: 1;
        background: $surface;
        color: $text;
        padding: 0 1;
    }
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._index_parts: list[str] = []
        self._regime_text: str = ""

    def update_indices(self, kospi: list[dict[str, Any]], kosdaq: list[dict[str, Any]]) -> None:
        parts = []
        for item in kospi:
            rate = item.get("fluctuation_rate", 0.0)
            color = "red" if rate >= 0 else "blue"
            sign = "+" if rate >= 0 else ""
            parts.append(f"[bold]{item['name']}[/bold] {item['close_price']:,.2f} [{color}]{sign}{rate:.2f}%[/{color}]")

        for item in kosdaq:
            rate = item.get("fluctuation_rate", 0.0)
            color = "red" if rate >= 0 else "blue"
            sign = "+" if rate >= 0 else ""
            parts.append(f"[bold]{item['name']}[/bold] {item['close_price']:,.2f} [{color}]{sign}{rate:.2f}%[/{color}]")

        self._index_parts = parts
        self._refresh_text()

    def update_regime(self, text: str) -> None:
        """장세 칸 하나만 갱신한다 (KIS 호출이 지수 칸과 별도로 끝난다)."""
        self._regime_text = text
        self._refresh_text()

    def _refresh_text(self) -> None:
        parts = list(self._index_parts)
        if self._regime_text:
            parts.append(self._regime_text)
        self.update("  |  ".join(parts) if parts else "Market data loading...")

    @staticmethod
    def format_regime_cell(closes: list[float], window: int = 60, label: str = "KOSPI200") -> str:
        """마지막 종가와 최근 `window` 영업일 종가 평균의 괴리(%)·위/아래.

        정보 표시용이다(장세 필터는 3그룹 성과를 개선하지 못했다 — 메모리). `closes` 는 날짜
        오름차순이어야 한다. `window` 개 미만이거나 평균이 0이면 계산할 수 없으므로 "—" 를 보인다 —
        KIS 호출이 실패했을 때도 호출부가 같은 값을 넘긴다.
        """
        if len(closes) < window:
            return f"{label} —"
        last = closes[-1]
        moving_average = sum(closes[-window:]) / window
        if moving_average == 0:
            return f"{label} —"
        pct = (last - moving_average) / moving_average * 100
        sign = "+" if pct >= 0 else ""
        direction = "위" if pct >= 0 else "아래"
        return f"{label} {last:,.0f} · {window}일선 {sign}{pct:.1f}% {direction}"

    def compose(self) -> ComposeResult:
        yield from []
