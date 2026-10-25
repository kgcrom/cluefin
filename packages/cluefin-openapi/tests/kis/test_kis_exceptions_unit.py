import pytest

from cluefin_openapi.kis import KISAPIError, KISResponseError
from cluefin_openapi.kis._exceptions import raise_for_rt_cd


def test_raise_for_rt_cd_accepts_success():
    raise_for_rt_cd({"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상처리 되었습니다.", "output": []})


def test_raise_for_rt_cd_raises_with_codes_only():
    body = {"rt_cd": "2", "msg_cd": "OPSQ2001", "msg1": "ERROR WRONG VALUE SIZE [SYMB]:[17]", "output": {"x": "1"}}

    with pytest.raises(KISResponseError, match=r"KIS API Error \[OPSQ2001\]: .* \(rt_cd=2\)") as exc_info:
        raise_for_rt_cd(body)

    # Only the codes travel with the exception — account responses can carry account numbers.
    assert exc_info.value.response_data == {"rt_cd": "2", "msg_cd": "OPSQ2001", "msg1": body["msg1"]}


def test_kis_response_error_is_both_kis_api_error_and_value_error():
    # ValueError base keeps callers written against the old plain ValueError working.
    assert issubclass(KISResponseError, KISAPIError)
    assert issubclass(KISResponseError, ValueError)
