from cluefin_openapi.nhplug._exceptions import NHPlugAPIError

# 실측(2026-08-22, moapi): 모의투자 환경은 성공 시 rsp_cd="XA102"
# ("모의투자 조회가 완료되었습니다")를 내려준다. 문서에는 00000 만 성공으로
# 기재돼 있으므로 둘 다 성공으로 취급한다. 실패는 HTTP 200 + 그 외 rsp_cd
# (예: 14070 "모의투자 매매불가 종목입니다."), 요청 자체 오류는 HTTP 4xx.
SUCCESS_RSP_CODES = frozenset({"00000", "XA102"})


def check_response_error(response_data: dict) -> None:
    """HTTP 200 이어도 body rsp_cd 가 실패일 수 있으므로 여기서 확인한다."""
    rsp_cd = response_data.get("rsp_cd")
    if rsp_cd is not None and rsp_cd not in SUCCESS_RSP_CODES:
        raise NHPlugAPIError(
            f"API error {rsp_cd}: {response_data.get('rsp_msg', '')}",
            status_code=200,
            response_data=response_data,
        )
