import json

import pytest

from cluefin_openapi.kiwoom._domestic_account_types import (
    DomesticAccountDailyRealizedProfitLossDetails,
    DomesticAccountExecuted,
    DomesticAccountProfitRate,
)
from cluefin_openapi.kiwoom._model import KiwoomHttpHeader, KiwoomHttpResponse


def test_account_daily_realized_profit_loss_details_json_serialization():
    """
    계좌 당일 실현손익 상세 응답 모델의 JSON 직렬화 테스트
    """
    # 테스트 샘플 데이터 생성
    data = DomesticAccountDailyRealizedProfitLossDetails(
        return_code=0,
        return_msg="조회가 완료되었습니다.",
        tdy_rlzt_pl="179439",
        tdy_rlzt_pl_dtl=[
            {
                "stk_nm": "삼성전자",
                "cntr_qty": "1",
                "buy_uv": "97602.9573459",
                "cntr_pric": "158200",
                "tdy_sel_pl": "59813.0426541",
                "pl_rt": "+61.28",
                "tdy_trde_cmsn": "500",
                "tdy_trde_tax": "284",
                "stk_cd": "A005930",
            },
            {
                "stk_nm": "카카오",
                "cntr_qty": "10",
                "buy_uv": "45000.0",
                "cntr_pric": "48000",
                "tdy_sel_pl": "30000.0",
                "pl_rt": "+6.67",
                "tdy_trde_cmsn": "1200",
                "tdy_trde_tax": "864",
                "stk_cd": "A035720",
            },
        ],
    )
    
    # 응답 객체 생성
    headers = KiwoomHttpHeader(**{
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10077",
    })
    response = KiwoomHttpResponse(headers=headers, body=data)
    
    # JSON 직렬화 테스트
    serialized = json.dumps(response.body.model_dump(), ensure_ascii=False)
    deserialized = json.loads(serialized)
    
    # 검증
    assert deserialized["tdy_rlzt_pl"] == "179439"
    assert len(deserialized["tdy_rlzt_pl_dtl"]) == 2
    assert deserialized["tdy_rlzt_pl_dtl"][0]["stk_nm"] == "삼성전자"
    assert deserialized["tdy_rlzt_pl_dtl"][0]["stk_cd"] == "A005930"
    assert deserialized["tdy_rlzt_pl_dtl"][0]["tdy_sel_pl"] == "59813.0426541"
    assert deserialized["tdy_rlzt_pl_dtl"][1]["stk_nm"] == "카카오"


def test_account_executed_json_serialization():
    """
    계좌 체결내역 응답 모델의 JSON 직렬화 테스트
    """
    # 테스트 샘플 데이터 생성
    data = DomesticAccountExecuted(
        return_code=0,
        return_msg="조회가 완료되었습니다.",
        cntr=[
            {
                "ord_no": "0000037",
                "stk_nm": "삼성전자",
                "io_tp_nm": "-매도",
                "ord_pric": "158200",
                "ord_qty": "1",
                "cntr_pric": "158200",
                "cntr_qty": "1",
                "oso_qty": "0",
                "tdy_trde_cmsn": "310",
                "tdy_trde_tax": "284",
                "ord_stt": "체결",
                "trde_tp": "보통",
                "orig_ord_no": "0000000",
                "ord_tm": "153815",
                "stk_cd": "005930",
                "stex_tp": "0",
                "stex_tp_txt": "SOR",
                "sor_yn": "Y",
            },
            {
                "ord_no": "0000036",
                "stk_nm": "SK하이닉스",
                "io_tp_nm": "-매도",
                "ord_pric": "175000",
                "ord_qty": "2",
                "cntr_pric": "175000",
                "cntr_qty": "2",
                "oso_qty": "0",
                "tdy_trde_cmsn": "620",
                "tdy_trde_tax": "630",
                "ord_stt": "체결",
                "trde_tp": "보통",
                "orig_ord_no": "0000000",
                "ord_tm": "153806",
                "stk_cd": "000660",
                "stex_tp": "0",
                "stex_tp_txt": "SOR",
                "sor_yn": "Y",
            },
        ]
    )
    
    # 응답 객체 생성
    headers = KiwoomHttpHeader(**{
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10076",
    })
    response = KiwoomHttpResponse(headers=headers, body=data)
    
    # JSON 직렬화 테스트
    serialized = json.dumps(response.body.model_dump(), ensure_ascii=False)
    deserialized = json.loads(serialized)
    
    # 검증
    assert len(deserialized["cntr"]) == 2
    assert deserialized["cntr"][0]["ord_no"] == "0000037"
    assert deserialized["cntr"][0]["stk_nm"] == "삼성전자"
    assert deserialized["cntr"][0]["cntr_pric"] == "158200"
    assert deserialized["cntr"][1]["stk_nm"] == "SK하이닉스"
    assert deserialized["cntr"][1]["cntr_qty"] == "2"


def test_account_profit_rate_json_serialization():
    """
    계좌 수익률 응답 모델의 JSON 직렬화 테스트
    """
    # 테스트 샘플 데이터 생성
    data = DomesticAccountProfitRate(
        return_code=0,
        return_msg="조회가 완료되었습니다.",
        acnt_prft_rt=[
            {
                "dt": "",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-63000",
                "pur_pric": "124500",
                "pur_amt": "373500",
                "rmnd_qty": "3",
                "tdy_sel_pl": "0",
                "tdy_trde_cmsn": "0",
                "tdy_trde_tax": "0",
                "crd_tp": "00",
                "loan_dt": "00000000",
                "setl_remn": "3",
                "clrn_alow_qty": "3",
                "crd_amt": "0",
                "crd_int": "0",
                "expr_dt": "00000000",
            },
            {
                "dt": "",
                "stk_cd": "035720",
                "stk_nm": "카카오",
                "cur_prc": "+47200",
                "pur_pric": "45000",
                "pur_amt": "450000",
                "rmnd_qty": "10",
                "tdy_sel_pl": "0",
                "tdy_trde_cmsn": "0",
                "tdy_trde_tax": "0",
                "crd_tp": "00",
                "loan_dt": "00000000",
                "setl_remn": "10",
                "clrn_alow_qty": "10",
                "crd_amt": "0",
                "crd_int": "0",
                "expr_dt": "00000000",
            },
        ]
    )
    
    # 응답 객체 생성
    headers = KiwoomHttpHeader(**{
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10085",
    })
    response = KiwoomHttpResponse(headers=headers, body=data)
    
    # JSON 직렬화 테스트
    serialized = json.dumps(response.body.model_dump(), ensure_ascii=False)
    deserialized = json.loads(serialized)
    
    # 검증
    assert len(deserialized["acnt_prft_rt"]) == 2
    assert deserialized["acnt_prft_rt"][0]["stk_cd"] == "005930"
    assert deserialized["acnt_prft_rt"][0]["stk_nm"] == "삼성전자"
    assert deserialized["acnt_prft_rt"][0]["pur_pric"] == "124500"
    assert deserialized["acnt_prft_rt"][1]["stk_nm"] == "카카오"
    assert deserialized["acnt_prft_rt"][1]["cur_prc"] == "+47200"


def test_response_full_serialization():
    """
    전체 응답 객체(헤더+바디)의 JSON 직렬화 테스트
    """
    # 테스트 샘플 데이터 생성
    data = DomesticAccountExecuted(
        return_code=0,
        return_msg="조회가 완료되었습니다.",
        cntr=[
            {
                "ord_no": "0000037",
                "stk_nm": "삼성전자",
                "io_tp_nm": "-매도",
                "ord_pric": "158200",
                "ord_qty": "1",
                "cntr_pric": "158200",
                "cntr_qty": "1",
                "oso_qty": "0",
                "tdy_trde_cmsn": "310",
                "tdy_trde_tax": "284",
                "ord_stt": "체결",
                "trde_tp": "보통",
                "orig_ord_no": "0000000",
                "ord_tm": "153815",
                "stk_cd": "005930",
                "stex_tp": "0",
                "stex_tp_txt": "SOR",
                "sor_yn": "Y",
            }
        ]
    )
    
    # 응답 객체 생성
    headers = KiwoomHttpHeader(**{
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10076",
    })
    response = KiwoomHttpResponse(headers=headers, body=data)
    
    # 전체 응답 객체(헤더+바디) 직렬화 테스트
    response_dict = {
        "headers": headers.model_dump(by_alias=True),
        "body": data.model_dump()
    }
    serialized = json.dumps(response_dict, ensure_ascii=False)
    deserialized = json.loads(serialized)
    
    # 검증
    assert deserialized["headers"]["cont-yn"] == "N"
    assert deserialized["headers"]["api-id"] == "ka10076"
    assert len(deserialized["body"]["cntr"]) == 1
    assert deserialized["body"]["cntr"][0]["stk_nm"] == "삼성전자"
    assert deserialized["body"]["cntr"][0]["ord_no"] == "0000037"
    
    # 전체 응답 객체(헤더+바디) 직렬화 테스트
    response_dict = {
        "headers": response.headers.model_dump(),
        "body": response.body.model_dump()
    }
    serialized = json.dumps(response_dict, ensure_ascii=False)
    deserialized = json.loads(serialized)
    
    # 검증
    assert deserialized["headers"]["cont_yn"] == "N"
    assert deserialized["headers"]["api_id"] == "ka10076"
    assert len(deserialized["body"]["cntr"]) == 1
    assert deserialized["body"]["cntr"][0]["stk_nm"] == "삼성전자"
    assert deserialized["body"]["cntr"][0]["ord_no"] == "0000037"
