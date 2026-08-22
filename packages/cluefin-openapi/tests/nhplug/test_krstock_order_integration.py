"""NH PLUG 국내주식 주문 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 주문을 접수한다 — kiwoom 주문 통합테스트와
같은 방식. 운영(prod)으로 돌리면 실제 체결되므로 절대 prod 로 실행하지 말 것.
장 운영시간(평일 09:00–15:30 KST)이 아니면 접수 거부 코드로 skip 된다.
"""

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

from ._integration_helpers import real_account_only, skip_if_env_blocked

TEST_IEM_CD = "005930"  # 삼성전자


def _unfillable_buy_price(client: HttpClient, iem_cd: str) -> int:
    """체결되지 않을 만큼 낮으면서 1,000원 배수로 내림한 매수 지정가를 계산한다.

    시세(krstock/quote) 카테고리가 아직 정식 메서드로 구현되지 않아 raw `client.post`
    로 현재가(`/krstock/quote/v1/currentPrice`)를 직접 호출한다 — 시세 카테고리 구현 후
    정식 메서드(예: `client.krstock_quote.current_price(...)`)로 교체할 것.
    """
    response = client.post(
        "/krstock/quote/v1/currentPrice",
        body={"market_cd": "KRX", "iem_cd": iem_cd},
    )
    data = response.json()
    output_0 = data.get("Output_0") or {}
    stck_prpr = output_0.get("stck_prpr")
    if not stck_prpr:
        pytest.skip(f"현재가 조회 실패로 미체결 지정가를 만들 수 없다: [{data.get('rsp_cd')}] {data.get('rsp_msg')}")
    base = abs(int(stck_prpr))
    price = (int(base * 0.8) // 1000) * 1000
    if price <= 0:
        pytest.skip(f"기준가가 너무 낮아 미체결 지정가를 만들 수 없다: {stck_prpr}")
    return price


@pytest.fixture
def krstock_pending_buy_order(client: HttpClient, krstock_account: str) -> dict:
    """정정 대상이 될 미체결 매수주문을 실제로 접수하고 원주문 식별자를 반환한다.

    modify 입력이 요구하는 원주문 식별자는 `org_mkt_orr_no`(원시장주문번호) 하나뿐이며,
    신규주문 응답의 `mkt_orr_no` 를 그대로 사용한다.
    """
    price = _unfillable_buy_price(client, TEST_IEM_CD)
    try:
        response = client.krstock_order.cash_buy(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="01",  # 보통가(지정가) — 시장가는 즉시 체결되어 정정 대상이 될 수 없다
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
            orr_pr=price,
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    output_0 = response.body.output_0
    if output_0 is None or not output_0.mkt_orr_no:
        pytest.skip("매수주문 응답에 시장주문번호가 없다")
    return {"mkt_orr_no": output_0.mkt_orr_no, "orr_pr": price}


@pytest.mark.integration
def test_cash_buy_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 매수 접수. 모의투자 계좌라 실손실은 없다."""
    try:
        response = client.krstock_order.cash_buy(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
@real_account_only("/krstock/order/v1/creditBuy", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_credit_buy_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 신용 매수 접수. 운영에서만 검증 가능 — 실제 신용주문이 체결된다.

    cfd_lon_cd="01"(유통융자)을 사용한다 — 스펙 설명의 신용대출코드 목록(01.유통융자
    02.자기융자 03.유통대주 04.자기대주 10.매입자금대출) 중 신규 매수 신용거래의
    가장 기본 형태(융자·유통물)이고, lon_dt(대출일자)는 스펙상 03·04(대주)일 때만
    필수라 01을 쓰면 추가 입력 없이 호출할 수 있다.
    """
    try:
        response = client.krstock_order.credit_buy(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            cfd_lon_cd="01",  # 유통융자 — lon_dt 불필요
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
@real_account_only("/krstock/order/v1/creditSell", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_credit_sell_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 신용 매도 접수. 운영에서만 검증 가능 — 실제 신용주문이 체결된다.

    creditSell 스펙은 creditBuy 와 필드·required 구성이 완전히 동일하다(설명 문구의
    쉼표 하나 차이뿐). creditBuy 실측(19999: 모의투자에서는 해당업무가 제공되지 않습니다)을
    신용 계열 API 전체의 공통 제약으로 보고 동일한 skip 을 붙였지만, creditSell 자체는
    아직 실측하지 않은 추정이다 — 운영 검증 시 이 marker 를 다시 확인할 것.

    cfd_lon_cd="01"(유통융자)을 사용한다 — lon_dt(대출일자)는 스펙상 03·04(대주)일
    때만 필수라 01을 쓰면 추가 입력 없이 호출할 수 있다.
    """
    try:
        response = client.krstock_order.credit_sell(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            cfd_lon_cd="01",  # 유통융자 — lon_dt 불필요
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
def test_cash_sell_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 매도 접수. 보유 잔고가 없으면 거부 코드가 나올 수 있다 —
    그 코드도 환경 제약이므로 실측 후 ENV_BLOCKED_CODES 에 등록한다."""
    try:
        response = client.krstock_order.cash_sell(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
def test_modify_order(client: HttpClient, krstock_account: str, krstock_pending_buy_order: dict):
    """미체결 매수주문(krstock_pending_buy_order)을 다른 미체결 가격으로 정정한다."""
    new_price = max(krstock_pending_buy_order["orr_pr"] - 1000, 1000)
    try:
        response = client.krstock_order.modify(
            act_no=krstock_account,
            org_mkt_orr_no=krstock_pending_buy_order["mkt_orr_no"],
            all_pat_dit_cd="1",  # 전체(전량)
            iem_cd=TEST_IEM_CD,
            cor_qty=1,
            cor_pr=new_price,
            sop_cnd_pr=0,  # 원주문이 스톱지정가(16)가 아니므로 사용되지 않음 — required 라 0 전송
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
@real_account_only("/krstock/order/v1/reservedOrder", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_reserved_order(client: HttpClient, krstock_account: str):
    """지정가 예약주문(다음 영업일 매수) 접수.

    이 테스트는 접수된 예약주문을 취소하지 않는다 — 성공하면 다음 작업(reservedCancel)의
    통합테스트가 이 주문을 취소 대상으로 재사용할 수 있게 남겨둔다.
    """
    price = _unfillable_buy_price(client, TEST_IEM_CD)
    try:
        response = client.krstock_order.reserved_order(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            sby_dit_cd="2",  # 매수
            frs_sba_orr_yn="N",
            nmn_pr_tp_cd="01",  # 지정가
            cfd_lon_cd="00",  # 일반거래(현금)
            orr_qty=1,
            orr_uit_pr=price,
            bkg_orr_tp_cd="1",  # 일반예약
            bkg_orr_enf_tp_cd="1",  # 일반
            rmt_mkt_cd="KRX",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.bkg_orr_no is not None


@pytest.mark.integration
def test_cancel_order(client: HttpClient, krstock_account: str, krstock_pending_buy_order: dict):
    """미체결 매수주문(krstock_pending_buy_order)을 취소한다.

    cancel 입력은 modify 와 달리 `cor_pr`·`sop_cnd_pr`·`rmt_mkt_cd`·`sor_mkt_sli_yn` 이
    없다 — 취소에는 가격·시장 정보가 필요 없다.
    """
    try:
        response = client.krstock_order.cancel(
            act_no=krstock_account,
            org_mkt_orr_no=krstock_pending_buy_order["mkt_orr_no"],
            all_pat_dit_cd="1",  # 전체(전량)
            iem_cd=TEST_IEM_CD,
            cor_qty=1,
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None
