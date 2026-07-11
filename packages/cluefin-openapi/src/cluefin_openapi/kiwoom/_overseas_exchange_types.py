from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasExchangeEstimatedAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환전 예상 금액 조회 응답")

    sell_aplc_exrt: str = Field(default="", description="매도적용환율. 소수점 둘째 자리까지 포맷된 숫자")
    buy_aplc_exrt: str = Field(default="", description="매수적용환율. 소수점 둘째 자리까지 포맷된 숫자")
    aplc_exrt: str = Field(default="", description="적용환율. 소수점 여섯째 자리까지 포맷된 숫자")
    sell_crnc_entra_nowrm: str = Field(default="", description="매도통화예수금금잔. 소수점 둘째 자리까지 포맷된 숫자")
    sell_crnc_ch_uncla_nowrm: str = Field(
        default="", description="매도통화현금미수금금잔. 소수점 둘째 자리까지 포맷된 숫자"
    )
    sell_crnc_etc_loana_nowrm: str = Field(
        default="", description="매도통화기타대여금금잔. 소수점 둘째 자리까지 포맷된 숫자"
    )
    sell_crnc_exmn_alow_amt: str = Field(
        default="", description="매도통화환전가능금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    buy_crnc_entra_nowrm: str = Field(default="", description="매수통화예수금금잔. 소수점 둘째 자리까지 포맷된 숫자")
    buy_crnc_ch_uncla_nowrm: str = Field(
        default="", description="매수통화현금미수금금잔. 소수점 둘째 자리까지 포맷된 숫자"
    )
    buy_crnc_etc_loana_nowrm: str = Field(
        default="", description="매수통화기타대여금금잔. 소수점 둘째 자리까지 포맷된 숫자"
    )
    buy_crnc_exmn_alow_amt: str = Field(
        default="", description="매수통화환전가능금액. 소수점 둘째 자리까지 포맷된 숫자"
    )
    krw_uncl_amt: str = Field(default="", description="원화미수금액. 단위: 원, 좌측 0-padding 처리된 15자리 숫자")
    sell_expc_amt: str = Field(default="", description="매도예상금액. 소수점 둘째 자리까지 포맷된 숫자")
    buy_expc_amt: str = Field(default="", description="매수예상금액. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasExchangeRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환율 조회 응답")

    sell_aplc_exrt: str = Field(default="", description="매도적용환율. 소수점 둘째 자리까지 포맷된 숫자")
    buy_aplc_exrt: str = Field(default="", description="매수적용환율. 소수점 둘째 자리까지 포맷된 숫자")
    aplc_exrt: str = Field(
        default="",
        description="적용환율. 실제 환전에 적용되는 환율입니다. 다만, 환전시점 시 환율 변동으로 인해 조회 환율과 적용 환율이 다를 수 있으며 환전 신청 전 꼭 환율을 확인해주시기 바랍니다",
    )
    exrt_tp_nm: str = Field(default="", description="환율구분명")
    spcl_bf_exrt: str = Field(
        default="",
        description="우대율 적용 전 환율. 환율 우대율을 적용하기 전 환율 입니다. 실제 환전은 aplc_exrt (적용환율)로 진행됩니다",
    )
    exrt_spcl_rt: str = Field(default="", description="환율우대율")


class OverseasExchangeRequest(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환전 신청 응답")

    sell_aplc_exrt: str = Field(default="", description="매도적용환율")
    buy_aplc_exrt: str = Field(default="", description="매수적용환율")
    aplc_exrt: str = Field(default="", description="적용환율")
    entra_prerm: str = Field(default="", description="예수금전잔")
    ch_uncla_prerm: str = Field(default="", description="현금미수금전잔")
    etc_loana_prerm: str = Field(default="", description="기타대여금전잔")
    entra_nowrm: str = Field(default="", description="예수금금잔")
    ch_uncla_nowrm: str = Field(default="", description="현금미수금금잔")
    etc_loana_nowrm: str = Field(default="", description="기타대여금금잔")
    krw_exmn_alow_amt: str = Field(default="", description="원화환전가능금액")
    ch_uncl_rpym_amt: str = Field(default="", description="현금미수변제금")
    ch_uncl_dlfe: str = Field(default="", description="현금미수연체료")
    etc_loan_npay_rpym_amt: str = Field(default="", description="기타대여미납변제금")
    etc_loan_npay_dlfe: str = Field(default="", description="기타대여미납연체료")
    fc_entra_prerm: str = Field(default="", description="외화예수금전잔")
    fc_ch_uncla_prerm: str = Field(default="", description="외화현금미수금전잔")
    fc_etc_loana_prerm: str = Field(default="", description="외화기타대여금전잔")
    fc_entra_nowrm: str = Field(default="", description="외화예수금금잔")
    fc_ch_uncla_nowrm: str = Field(default="", description="외화현금미수금금잔")
    fc_etc_loana_nowrm: str = Field(default="", description="외화기타대여금금잔")
    fc_exmn_alow_amt: str = Field(default="", description="외화환전가능금액")
    fc_ch_uncl_rpym_amt: str = Field(default="", description="외화현금미수변제금")
    fc_ch_uncl_dlfe: str = Field(default="", description="외화현금미수연체료")
    fc_etc_loan_npay_rpym_amt: str = Field(default="", description="외화기타대여미납변제금")
    fc_etc_loan_npay_dlfe: str = Field(default="", description="외화기타대여미납연체료")
    krw_exmn_amt: str = Field(default="", description="원화환전금액")
    sell_fc_amt: str = Field(default="", description="매도외화금액")
    buy_fc_amt: str = Field(default="", description="매수외화금액")
