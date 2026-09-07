"""워커 스레드에서 UI 를 만지는 공통 도우미 — 실패는 화면에 남기고, 화면 전환은 취소로 본다."""

from textual.message_pump import NoActiveAppError
from textual.widgets import Static


def screen_gone(screen, exc: BaseException) -> bool:
    """로딩 도중 다른 화면으로 갈아타면 내려간 화면의 워커가 `self.app` 을 만지는
    순간 `NoActiveAppError`(메시지가 빈 예외)가 난다. 실패가 아니라 취소이므로
    로그도 패널 갱신도 하지 않고 조용히 끝내야 한다 — 2026-09-02 실측에서
    "Failed to load KIS 투자자별 순매수: " 처럼 원인 없는 ERROR 로 보였다."""
    return isinstance(exc, NoActiveAppError) or not screen.is_attached


def set_text(screen, selector: str, text: str) -> None:
    """워커 스레드에서 Static 하나를 갱신한다. 화면이 이미 내려갔으면 조용히 버린다."""

    def _apply():
        screen.query_one(selector, Static).update(text)

    try:
        screen.app.call_from_thread(_apply)
    except NoActiveAppError:
        pass


def guarded(screen, selector: str | None, label: str, fn, *args) -> None:
    """로더 하나를 돌리고, 실패하면 로그와 함께 `selector` 패널에 남긴다.

    실패를 로그에만 남기면 표가 빈 채로 멈춰 있어 사용자는 원인을 알 수 없다.
    한 로더의 실패가 같은 워커의 뒤 로더를 막지 않는다. `selector` 가 None 이면
    (표만 있는 탭) 로그만 남긴다."""
    try:
        fn(*args)
    except Exception as e:
        if screen_gone(screen, e):
            return
        from loguru import logger

        logger.error(f"Failed to load {label}: {e}")
        if selector is not None:
            set_text(screen, selector, f"{label} 로딩 실패: {e}")
