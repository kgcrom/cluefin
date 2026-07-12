from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasOrderBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매수 주문 응답")

    stk_nm: str = Field(default="", description="종목명")
    ord_no: str = Field(default="", description="주문번호. 취소 혹은 정정 주문 시 사용")
    fc_entra: str = Field(default="", description="외화예수금")
    tdy_rebuy_useda: str = Field(default="", description="금일재매수사용금액")
    pred_rebuy_useda: str = Field(default="", description="전일재매수사용금액")
    trst_prof_ch: str = Field(default="", description="사용증거금")


class OverseasOrderSell(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매도 주문 응답")

    stk_nm: str = Field(default="", description="종목명")
    ord_no: str = Field(default="", description="주문번호. 취소 혹은 정정 주문 시 사용")
    poss_qty: str = Field(default="", description="보유수량")
    tdy_resel_usedq: str = Field(default="", description="금일재매도사용수량")
    pred_resel_usedq: str = Field(default="", description="전일재매도사용수량")


class OverseasOrderModify(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 정정 주문 응답")

    stk_nm: str = Field(default="", description="종목명")
    ord_no: str = Field(default="", description="주문번호. 취소 혹은 정정 주문 시 사용")
    fc_entra: str = Field(default="", description="외화예수금")
    tdy_rebuy_useda: str = Field(default="", description="금일재매수사용금액")
    pred_rebuy_useda: str = Field(default="", description="전일재매수사용금액")
    trst_prof_ch: str = Field(default="", description="사용증거금")
    mdfy_ord_qty: str = Field(default="", description="정정주문수량")


class OverseasOrderCancel(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 취소 주문 응답")

    stk_nm: str = Field(default="", description="종목명")
    ord_no: str = Field(default="", description="주문번호")
    cncl_ord_qty: str = Field(default="", description="취소주문수량")


class OverseasOrderOrderableQuantity(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주문가능수량(종목/증거금률별) 응답")

    stk_profa_rt: str = Field(default="", description="종목증거금율")
    profa_rt: str = Field(default="", description="계좌증거금율")
    aplc_rt: str = Field(default="", description="적용증거금율")
    krw_ord_rqst_yn: str = Field(default="", description="원화주문신청여부. Y, N")
    krw_ord_alowa_50: str = Field(
        default="", description="증거금50%종목 원화주문가능금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    krw_ord_alowq_50: str = Field(
        default="", description="증거금50%종목 원화주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    ord_alowa_50: str = Field(default="", description="증거금50%종목 주문가능금액. 소수점 둘째 자리까지 포맷된 숫자")
    ord_alowq_50: str = Field(
        default="", description="증거금50%종목 주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    pred_rebuy_alowa_50: str = Field(
        default="", description="증거금50%종목 전일재사용금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    tdy_rebuy_alowa_50: str = Field(
        default="", description="증거금50%종목 금일재사용금액. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    krw_ord_alowa_100: str = Field(
        default="", description="증거금100%종목원화주문가능금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    krw_ord_alowq_100: str = Field(
        default="", description="증거금100%종목원화주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    ord_alowa_100: str = Field(default="", description="증거금100%종목 주문가능금액. 소수점 둘째 자리까지 포맷된 숫자")
    ord_alowq_100: str = Field(
        default="", description="증거금100%종목 주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    pred_rebuy_alowa_100: str = Field(
        default="", description="증거금100%종목 전일재사용금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    tdy_rebuy_alowa_100: str = Field(
        default="", description="증거금100%종목 금일재사용금액. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    min_krw_ord_alowa: str = Field(
        default="", description="미수불가 원화주문가능금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    min_krw_ord_alowq: str = Field(
        default="", description="미수불가 원화주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    min_ord_alowa: str = Field(default="", description="미수불가 주문가능금액. 소수점 둘째 자리까지 포맷된 숫자")
    min_ord_alowq: str = Field(
        default="", description="미수불가 주문가능수량. 단위: 1주, 좌측 0-padding 처리된 12자리 숫자"
    )
    min_pred_rebuy_alowa: str = Field(
        default="", description="미수불가 전일재사용금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    min_tdy_rebuy_alowa: str = Field(
        default="", description="미수불가 금일재사용금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    krw_entra: str = Field(default="", description="원화예수금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자")
    fc_entra: str = Field(default="", description="외화예수금. 소수점 둘째 자리까지 포맷된 숫자")
    fc_uncl_amt: str = Field(default="", description="외화미수금. 소수점 둘째 자리까지 포맷된 숫자")
    ord_alowa: str = Field(default="", description="주문가능현금. 소수점 둘째 자리까지 포맷된 숫자")
    krw_ord_set_amt: str = Field(
        default="", description="해외원화주문설정금. 단위: 원, 좌측 0-padding 처리된 12자리 숫자"
    )
    krw_ord_evlt_amt: str = Field(default="", description="해외원화주문평가금. 소수점 둘째 자리까지 포맷된 숫자")
    crnc_code: str = Field(default="", description="통화")
