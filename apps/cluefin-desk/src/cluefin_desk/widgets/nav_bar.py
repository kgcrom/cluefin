from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static


class NavButton(Static):
    """Single navigation button in the nav bar."""

    DEFAULT_CSS = """
    NavButton {
        width: auto;
        height: 1;
        padding: 0 1;
        color: $text;
    }
    NavButton.active {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    NavButton.help-btn {
        color: $warning;
    }
    """

    def __init__(self, label: str, key: str, *, is_help: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._label = label
        self._key = key
        self._is_help = is_help
        if is_help:
            self.add_class("help-btn")

    def on_mount(self) -> None:
        self.update(f"[{self._key}\u00b7{self._label}]")


class NavBar(Widget):
    """Bloomberg-style top navigation bar."""

    DEFAULT_CSS = """
    NavBar {
        dock: top;
        height: 1;
        background: $surface;
        layout: horizontal;
    }
    NavBar > .nav-title {
        width: auto;
        padding: 0 1;
        color: $success;
        text-style: bold;
    }
    NavBar > .nav-buttons {
        width: 1fr;
        height: 1;
        align: left middle;
    }
    """

    BUTTONS = [
        ("MKT", "1"),
        ("RANK", "2"),
        ("THEME", "3"),
        ("ETF", "4"),
        ("INV", "5"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._active_key = "1"

    def compose(self) -> ComposeResult:
        yield Static("CLUEFIN DESK", classes="nav-title")
        with Horizontal(classes="nav-buttons"):
            for label, key in self.BUTTONS:
                yield NavButton(label, key, id=f"nav-btn-{key}")
            yield NavButton("HELP", "?", is_help=True, id="nav-btn-help")

    def set_active(self, key: str) -> None:
        self._active_key = key
        for btn in self.query(NavButton):
            btn.remove_class("active")
        try:
            active_btn = self.query_one(f"#nav-btn-{key}", NavButton)
            active_btn.add_class("active")
        except Exception:
            pass
