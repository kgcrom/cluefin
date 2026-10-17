"""워커 스레드에서 UI 를 만지는 공통 도우미 — 실패는 화면에 남기고, 화면 전환은 취소로 본다."""

from rich.markup import escape
from textual.message_pump import NoActiveAppError
from textual.widgets import Static


def _closed(screen) -> bool:
    """화면이 내려갔거나 내려가는 중이다.

    pop 된 화면은 몇 틱 동안 `is_attached` 가 True 인 채로 자식 위젯부터 지워진다 —
    이 사이의 `query_one` 은 `NoMatches` 를 낸다. 그 구간엔 메시지 펌프가 이미 멈춰
    `is_running` 이 False 다(2026-10-17, textual 8.0 에서 틱마다 찍어 확인)."""
    return not screen.is_attached or not screen.is_running


def screen_gone(screen, exc: BaseException) -> bool:
    """로딩 도중 다른 화면으로 갈아타면 내려간 화면의 워커가 `self.app` 을 만지는
    순간 `NoActiveAppError`(메시지가 빈 예외)가 나고, 화면이 지워지는 도중이면 패널
    `query_one` 이 `NoMatches` 를 낸다. 실패가 아니라 취소이므로 로그도 패널 갱신도
    하지 않고 조용히 끝내야 한다 — 2026-09-02 실측에서 "Failed to load KIS 투자자별
    순매수: ", 2026-10-17 에 "Failed to load top movers: No nodes match
    '#top-gainers-panel'" 처럼 ERROR 로 보였다."""
    return isinstance(exc, NoActiveAppError) or _closed(screen)


def set_text(screen, selector: str, text: str) -> None:
    """워커 스레드에서 Static 하나를 갱신한다. 화면이 이미 내려갔으면 조용히 버린다."""

    def _apply():
        # 워커 쪽 검사와 이 콜백 실행 사이에 화면이 내려갈 수 있다. 여기서 NoMatches 가
        # 나면 워커의 except 안에서 다시 터져 워커가 죽는다(Textual 은 그때 앱을 끈다).
        if _closed(screen):
            return
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
            # 예외 메시지에는 pydantic 의 "[type=...]" 처럼 태그로 읽히는 대괄호가 흔하다.
            set_text(screen, selector, f"{label} 로딩 실패: {escape(str(e))}")
