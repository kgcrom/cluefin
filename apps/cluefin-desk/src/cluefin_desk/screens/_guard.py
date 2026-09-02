"""워커 스레드가 UI 를 만질 때 "화면이 이미 내려간" 경우를 실패와 구분한다."""

from textual.message_pump import NoActiveAppError


def screen_gone(screen, exc: BaseException) -> bool:
    """로딩 도중 다른 화면으로 갈아타면 내려간 화면의 워커가 `self.app` 을 만지는
    순간 `NoActiveAppError`(메시지가 빈 예외)가 난다. 실패가 아니라 취소이므로
    로그도 패널 갱신도 하지 않고 조용히 끝내야 한다 — 2026-09-02 실측에서
    "Failed to load KIS 투자자별 순매수: " 처럼 원인 없는 ERROR 로 보였다."""
    return isinstance(exc, NoActiveAppError) or not screen.is_attached
