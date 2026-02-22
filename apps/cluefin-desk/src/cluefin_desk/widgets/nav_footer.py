from textual.reactive import reactive
from textual.widgets import Footer
from textual.widgets._footer import FooterKey


class NavFooter(Footer):
    DEFAULT_CSS = """
    NavFooter FooterKey.-active-screen {
        background: $primary;
        .footer-key--key { color: $text; background: $primary-darken-2; text-style: bold; }
        .footer-key--description { color: $text; background: $primary; text-style: bold; }
    }
    """
    active_screen_key: reactive[str] = reactive("")

    def __init__(self, *, active_screen_key: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.active_screen_key = active_screen_key

    async def recompose(self) -> None:
        await super().recompose()
        self._apply_active_class()

    def watch_active_screen_key(self, value: str) -> None:
        self._apply_active_class()

    def _apply_active_class(self) -> None:
        for fk in self.query(FooterKey):
            fk.set_class(fk.key == self.active_screen_key, "-active-screen")
