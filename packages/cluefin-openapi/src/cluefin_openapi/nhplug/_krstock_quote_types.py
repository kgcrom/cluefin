from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugAssetHttpBody


class KrStockQuoteCurrentPriceOutput(BaseModel):
    """주식현재가 시세 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 41")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 10")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    askp: int | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 10")
    acml_vol: int | None = Field(default=None, description="거래량 / 길이 12")
    vol_rate: float | None = Field(default=None, description="거래비율 / 길이 6.2")
    move_rate: float | None = Field(default=None, description="유동주회전율 / 길이 6.2")
    acml_tr_pbmn: int | None = Field(default=None, description="거래대금 / 길이 18")
    stck_mxpr: int | None = Field(default=None, description="상한가 / 길이 10")
    stck_hgpr: int | None = Field(default=None, description="고가 / 길이 10")
    stck_oprc: int | None = Field(default=None, description="시가 / 길이 10")
    stck_oprc_sign: str | None = Field(default=None, description="시가대비부호 / 길이 1")
    stck_oprc_vrss: int | None = Field(default=None, description="시가대비등락폭 / 길이 10")
    stck_lwpr: int | None = Field(default=None, description="저가 / 길이 10")
    stck_llam: int | None = Field(default=None, description="하한가 / 길이 10")
    hoga_bsop_hour: str | None = Field(default=None, description="호가시간 / 길이 8")
    askp1: int | None = Field(default=None, description="매도호가1 / 길이 10")
    askp2: int | None = Field(default=None, description="매도호가2 / 길이 10")
    askp3: int | None = Field(default=None, description="매도호가3 / 길이 10")
    askp4: int | None = Field(default=None, description="매도호가4 / 길이 10")
    askp5: int | None = Field(default=None, description="매도호가5 / 길이 10")
    askp6: int | None = Field(default=None, description="매도호가6 / 길이 10")
    askp7: int | None = Field(default=None, description="매도호가7 / 길이 10")
    askp8: int | None = Field(default=None, description="매도호가8 / 길이 10")
    askp9: int | None = Field(default=None, description="매도호가9 / 길이 10")
    askp10: int | None = Field(default=None, description="매도호가10 / 길이 10")
    bidp1: int | None = Field(default=None, description="매수호가1 / 길이 10")
    bidp2: int | None = Field(default=None, description="매수호가2 / 길이 10")
    bidp3: int | None = Field(default=None, description="매수호가3 / 길이 10")
    bidp4: int | None = Field(default=None, description="매수호가4 / 길이 10")
    bidp5: int | None = Field(default=None, description="매수호가5 / 길이 10")
    bidp6: int | None = Field(default=None, description="매수호가6 / 길이 10")
    bidp7: int | None = Field(default=None, description="매수호가7 / 길이 10")
    bidp8: int | None = Field(default=None, description="매수호가8 / 길이 10")
    bidp9: int | None = Field(default=None, description="매수호가9 / 길이 10")
    bidp10: int | None = Field(default=None, description="매수호가10 / 길이 10")
    askp_rsqn1: int | None = Field(default=None, description="매도호가잔량1 / 길이 12")
    askp_rsqn2: int | None = Field(default=None, description="매도호가잔량2 / 길이 12")
    askp_rsqn3: int | None = Field(default=None, description="매도호가잔량3 / 길이 12")
    askp_rsqn4: int | None = Field(default=None, description="매도호가잔량4 / 길이 12")
    askp_rsqn5: int | None = Field(default=None, description="매도호가잔량5 / 길이 12")
    askp_rsqn6: int | None = Field(default=None, description="매도호가잔량6 / 길이 12")
    askp_rsqn7: int | None = Field(default=None, description="매도호가잔량7 / 길이 12")
    askp_rsqn8: int | None = Field(default=None, description="매도호가잔량8 / 길이 12")
    askp_rsqn9: int | None = Field(default=None, description="매도호가잔량9 / 길이 12")
    askp_rsqn10: int | None = Field(default=None, description="매도호가잔량10 / 길이 12")
    bidp_rsqn1: int | None = Field(default=None, description="매수호가잔량1 / 길이 12")
    bidp_rsqn2: int | None = Field(default=None, description="매수호가잔량2 / 길이 12")
    bidp_rsqn3: int | None = Field(default=None, description="매수호가잔량3 / 길이 12")
    bidp_rsqn4: int | None = Field(default=None, description="매수호가잔량4 / 길이 12")
    bidp_rsqn5: int | None = Field(default=None, description="매수호가잔량5 / 길이 12")
    bidp_rsqn6: int | None = Field(default=None, description="매수호가잔량6 / 길이 12")
    bidp_rsqn7: int | None = Field(default=None, description="매수호가잔량7 / 길이 12")
    bidp_rsqn8: int | None = Field(default=None, description="매수호가잔량8 / 길이 12")
    bidp_rsqn9: int | None = Field(default=None, description="매수호가잔량9 / 길이 12")
    bidp_rsqn10: int | None = Field(default=None, description="매수호가잔량10 / 길이 12")
    total_askp_rsqn: int | None = Field(default=None, description="총매도잔량 / 길이 12")
    total_bidp_rsqn: int | None = Field(default=None, description="총매수잔량 / 길이 12")
    ovtm_askp_rsqn: int | None = Field(default=None, description="시간외매도잔량 / 길이 12")
    ovtm_bidp_rsqn: int | None = Field(default=None, description="시간외매수잔량 / 길이 12")
    pvt_scnd_dmrs: int | None = Field(default=None, description="피봇2차저항 / 길이 10")
    pvt_frst_dmrs: int | None = Field(default=None, description="피봇1차저항 / 길이 10")
    pvt_pont_val: int | None = Field(default=None, description="피봇가 / 길이 10")
    pvt_frst_dmsp: int | None = Field(default=None, description="피봇1차지지 / 길이 10")
    pvt_scnd_dmsp: int | None = Field(default=None, description="피봇2차지지 / 길이 10")
    mrkt_div_isnm: str | None = Field(default=None, description="코스피코스닥구분 / 길이 6")
    bstp_kor_isnm: str | None = Field(default=None, description="업종명 / 길이 40")
    bstp_cls_code: str | None = Field(default=None, description="업종코드 / 길이 6")
    avls_scal_isnm: str | None = Field(default=None, description="자본금규모 / 길이 6")
    stac_month: str | None = Field(default=None, description="결산월 / 길이 16")
    market1: str | None = Field(default=None, description="시장조치1 / 길이 16")
    market2: str | None = Field(default=None, description="시장조치2 / 길이 16")
    market3: str | None = Field(default=None, description="시장조치3 / 길이 16")
    market4: str | None = Field(default=None, description="시장조치4 / 길이 16")
    market5: str | None = Field(default=None, description="시장조치5 / 길이 16")
    market6: str | None = Field(default=None, description="시장조치6 / 길이 16")
    cb_text: str | None = Field(default=None, description="CB구분 / 길이 6")
    stck_fcam: int | None = Field(default=None, description="액면가 / 길이 10")
    prdy_clpr_title: str | None = Field(default=None, description="전일종가타이틀 / 길이 12")
    stck_prdy_clpr: int | None = Field(default=None, description="전일종가 / 길이 10")
    stck_sspr: int | None = Field(default=None, description="대용가 / 길이 10")
    gongprice: int | None = Field(default=None, description="공모가 / 길이 7")
    d5_hgpr: int | None = Field(default=None, description="5일고가 / 길이 10")
    d5_lwpr: int | None = Field(default=None, description="5일저가 / 길이 10")
    d20_hgpr: int | None = Field(default=None, description="20일고가 / 길이 10")
    d20_lwpr: int | None = Field(default=None, description="20일저가 / 길이 10")
    w52_hgpr: int | None = Field(default=None, description="52주최고가 / 길이 10")
    w52_hgpr_date: str | None = Field(default=None, description="52주최고가일 / 길이 4")
    w52_lwpr: int | None = Field(default=None, description="52주최저가 / 길이 10")
    w52_lwpr_date: str | None = Field(default=None, description="52주최저가일 / 길이 4")
    move_stcn: int | None = Field(default=None, description="유동주식수 / 길이 12")
    lstn_stcn_unit3: int | None = Field(default=None, description="상장주식수 / 길이 12")
    hts_avls: int | None = Field(default=None, description="시가총액 / 길이 12")
    memb_bsop_hour: str | None = Field(default=None, description="시간 / 길이 5")
    seln_mbcr_name1: str | None = Field(default=None, description="매도거래원1 / 길이 6")
    shnu_mbcr_name1: str | None = Field(default=None, description="매수거래원1 / 길이 6")
    seln_qty1: int | None = Field(default=None, description="매도거래량1 / 길이 12")
    shnu_qty1: int | None = Field(default=None, description="매수거래량1 / 길이 12")
    seln_mbcr_name2: str | None = Field(default=None, description="매도거래원2 / 길이 6")
    shnu_mbcr_name2: str | None = Field(default=None, description="매수거래원2 / 길이 6")
    seln_qty2: int | None = Field(default=None, description="매도거래량2 / 길이 12")
    shnu_qty2: int | None = Field(default=None, description="매수거래량2 / 길이 12")
    seln_mbcr_name3: str | None = Field(default=None, description="매도거래원3 / 길이 6")
    shnu_mbcr_name3: str | None = Field(default=None, description="매수거래원3 / 길이 6")
    seln_qty3: int | None = Field(default=None, description="매도거래량3 / 길이 12")
    shnu_qty3: int | None = Field(default=None, description="매수거래량3 / 길이 12")
    seln_mbcr_name4: str | None = Field(default=None, description="매도거래원4 / 길이 6")
    shnu_mbcr_name4: str | None = Field(default=None, description="매수거래원4 / 길이 6")
    seln_qty4: int | None = Field(default=None, description="매도거래량4 / 길이 12")
    shnu_qty4: int | None = Field(default=None, description="매수거래량4 / 길이 12")
    seln_mbcr_name5: str | None = Field(default=None, description="매도거래원5 / 길이 6")
    shnu_mbcr_name5: str | None = Field(default=None, description="매수거래원5 / 길이 6")
    seln_qty5: int | None = Field(default=None, description="매도거래량5 / 길이 12")
    shnu_qty5: int | None = Field(default=None, description="매수거래량5 / 길이 12")
    glob_seln_qty: int | None = Field(default=None, description="매도외국인거래량 / 길이 12")
    glob_shnu_qty: int | None = Field(default=None, description="매수외국인거래량 / 길이 12")
    for_hour: str | None = Field(default=None, description="외국인시간 / 길이 6")
    for_rate: float | None = Field(default=None, description="외국인지분율 / 길이 5.2")
    crdt_stlm_date: str | None = Field(default=None, description="결제일 / 길이 4")
    crdt_rmnd_rate: float | None = Field(default=None, description="잔고비율(%) / 길이 5.2")
    yu_date: str | None = Field(default=None, description="유상기준일 / 길이 4")
    mu_date: str | None = Field(default=None, description="무상기준일 / 길이 4")
    yu_rate: float | None = Field(default=None, description="유상배정비율 / 길이 5.2")
    mu_rate: float | None = Field(default=None, description="무상배정비율 / 길이 5.2")
    frgn_ntby_vol: float | None = Field(default=None, description="외국인변동주수 / 길이 10.0")
    jasa: str | None = Field(default=None, description="자사주 / 길이 1")
    stck_lstn_date: str | None = Field(default=None, description="상장일 / 길이 8")
    dae_rate: float | None = Field(default=None, description="대주주지분율 / 길이 5.2")
    dae_date: str | None = Field(default=None, description="대주주지분일자 / 길이 6")
    filler: str | None = Field(default=None, description="FILLER / 길이 1")
    deposit_gb: str | None = Field(default=None, description="증거금율 / 길이 1")
    cpfn: int | None = Field(default=None, description="자본금 / 길이 12")
    total_seln_qty: int | None = Field(default=None, description="전체거래원매도합 / 길이 12")
    total_shnu_qty: int | None = Field(default=None, description="전체거래원매수합 / 길이 12")
    detour_gb: str | None = Field(default=None, description="우회상장여부 / 길이 1")
    scrt_grp_isnm: str | None = Field(default=None, description="증권구분 / 길이 6")
    crdt_deal_date: str | None = Field(default=None, description="공여율기준일 / 길이 4")
    crdt_loan_gvrt: float | None = Field(default=None, description="공여율(%) / 길이 5.2")
    per: float | None = Field(default=None, description="PER / 길이 5.2")
    hando_gb: str | None = Field(default=None, description="종목별신용한도 / 길이 1")
    wghn_avrg_prc: int | None = Field(default=None, description="가중가 / 길이 10")
    lstn_stcn_unit0: int | None = Field(default=None, description="상장주식수_주 / 길이 12")
    add_lstn_stcn: int | None = Field(default=None, description="추가상장주수 / 길이 12")
    gicomment: str | None = Field(default=None, description="종목comment / 길이 100")
    prdy_vol: int | None = Field(default=None, description="전일거래량 / 길이 12")
    pre_prdy_sign: str | None = Field(default=None, description="전일대비등락부호 / 길이 1")
    pre_prdy_vrss: int | None = Field(default=None, description="전일대비등락폭 / 길이 10")
    stck_dryy_hgpr: int | None = Field(default=None, description="연종최고가 / 길이 10")
    dryy_hgpr_date: str | None = Field(default=None, description="연중최고가일 / 길이 4")
    stck_dryy_lwpr: int | None = Field(default=None, description="연중최저가 / 길이 10")
    dryy_lwpr_date: str | None = Field(default=None, description="연중최저가일 / 길이 4")
    frgn_hldn_qty: float | None = Field(default=None, description="외국인보유주식수 / 길이 15")
    issu_limt_rate: float | None = Field(default=None, description="외국인한도율(%) / 길이 5.2")
    frml_mrkt_unit: float | None = Field(default=None, description="매매수량단위 / 길이 5")
    comp_cls_code: str | None = Field(default=None, description="경쟁대량방향구분 / 길이 1")
    largem_gb: str | None = Field(default=None, description="대량매매구분 / 길이 1")
    pbr: float | None = Field(default=None, description="PBR / 길이 5.2")
    dmrs_val: int | None = Field(default=None, description="디저항값 / 길이 7")
    dmsp_val: int | None = Field(default=None, description="디지지값 / 길이 7")
    prdy_tr_pbmn: int | None = Field(default=None, description="전일거래대금 / 길이 12")
    vi_antc_sdpr: int | None = Field(default=None, description="VI기준가 / 길이 10")
    vi_antc_mxpr: int | None = Field(default=None, description="VI상승발동가 / 길이 10")
    vi_antc_llam: int | None = Field(default=None, description="VI하락발동가 / 길이 10")
    invt_epmd_yn: str | None = Field(default=None, description="투자유의종목여부 / 길이 1")
    uplm_qty: int | None = Field(default=None, description="상한수량 / 길이 12")
    short_over_code: str | None = Field(
        default=None, description="단기과열구분코드 / 길이 1 / 1.단기과열예고 2.단기과열지정 3.단기과열연장"
    )
    mrkt_alrm_code: str | None = Field(
        default=None,
        description="투자주의경고구분코드 / 길이 1 / 1.투자주의 2.투자경고 3.투자주의>투자위험예고 4.투자경고투자위험예고 5.투자위험",
    )
    sltr_yn: str | None = Field(default=None, description="정리매매여부 / 길이 1 / Y.정리매매종목")
    crd_rt_grd_nm: str | None = Field(default=None, description="담보유지비율(%) / 길이 6")
    mid_prc: int | None = Field(default=None, description="중간가 / 길이 10")
    midp_total_askp_rsqn: int | None = Field(default=None, description="매도중간가잔량합계수량 / 길이 12")
    midp_total_bidp_rsqn: int | None = Field(default=None, description="매수중간가잔량합계수량 / 길이 12")
    nxt_mid_prc: int | None = Field(default=None, description="nxt중간가 / 길이 10")
    nxt_midp_total_askp_rsqn: int | None = Field(default=None, description="nxt매도중간가잔량합계수량 / 길이 12")
    nxt_midp_total_bidp_rsqn: int | None = Field(default=None, description="nxt매수중간가잔량합계수량 / 길이 12")
    marg_grad_cls_code: str | None = Field(default=None, description="증거금등급구분코드 / 길이 1")


class KrStockQuoteCurrentPriceTickOutput(BaseModel):
    """주식현재가 시세 시간대별 체결 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    bsop_hour: str | None = Field(default=None, description="시간 / 길이 8")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 10")
    askp: int | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 10")
    # 스펙은 string 으로 명세하지만 실측(2026-08-22)에는 int 로 온다 — balance/dailyPnl
    # 의 "합계"류 필드와 같은 divergence. int|str Union 으로 완화한다.
    cntg_vol: int | str | None = Field(default=None, description="변동거래량 / 길이 12")
    acml_vol: int | None = Field(default=None, description="거래량 / 길이 12")


class KrStockQuoteCurrentPriceExpectedOutput(BaseModel):
    """주식현재가 시세 예상체결/ECN 정보 (Output_2).

    스펙은 Output_2 를 Array 로 선언하지만 스펙 자체의 x-schema-warning 이 예시
    응답은 Object 라고 명시한다 — `KrStockQuoteCurrentPrice.output_2` 에서
    object/array 둘 다 허용하는 Union 으로 받는다.
    """

    model_config = ConfigDict(extra="allow")

    # 아래 수치류 필드는 스펙상 모두 string 이지만 실측(2026-08-22)에는 int/float 로
    # 온다 — Output_2 가 스펙 선언(Array)과 달리 Object 로 오는 것과 같은 종류의
    # 명세 오차다. int|float|str Union 으로 완화한다.
    cncc_aspr_code: str | None = Field(default=None, description="동시호가구분 / 길이 1 / 1.동시호가 이외 정규시장")
    antc_cnpr: int | float | str | None = Field(default=None, description="예상체결가 / 길이 10")
    antc_cntg_sign: str | None = Field(
        default=None,
        description="예상체결부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    antc_cntg_vrss: int | float | str | None = Field(default=None, description="예상체결등락폭 / 길이 10")
    antc_prdy_ctrt: int | float | str | None = Field(default=None, description="예상체결등락률 / 길이 5.2")
    antc_vol: int | float | str | None = Field(default=None, description="예상체결수량 / 길이 12")
    chkdata: str | None = Field(default=None, description="ECN정보유무구분 / 길이 1")
    ovtm_untp_prpr: int | float | str | None = Field(default=None, description="ECN전일종가 / 길이 10")
    ovtm_untp_sign: str | None = Field(default=None, description="ECN부호 / 길이 1")
    ovtm_untp_vrss: int | float | str | None = Field(default=None, description="ECN등락폭 / 길이 10")
    ovtm_untp_ctrt: int | float | str | None = Field(default=None, description="ECN등락률 / 길이 5.2")
    ovtm_untp_vol: int | float | str | None = Field(default=None, description="ECN체결수량 / 길이 12")
    ovtm_antc_sign: str | None = Field(
        default=None,
        description="ECN대비예상체결부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    ovtm_antc_vrss: int | float | str | None = Field(default=None, description="ECN대비예상체결등락폭 / 길이 10")
    ovtm_antc_ctrt: int | float | str | None = Field(default=None, description="ECN대비예상체결등락률 / 길이 5.2")
    scoring: int | float | str | None = Field(default=None, description="종합스코어링 / 길이 6.2")
    vi_type_code: str | None = Field(default=None, description="VI거래중지여부 / 길이 1 / 1.VI발동 N.그외")


class KrStockQuoteCurrentPrice(NHPlugAssetHttpBody):
    """주식현재가 시세 (`POST /krstock/quote/v1/currentPrice`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회).
    """

    output_0: KrStockQuoteCurrentPriceOutput | None = Field(
        default=None, alias="Output_0", description="현재가 종합 정보"
    )
    output_1: list[KrStockQuoteCurrentPriceTickOutput] | None = Field(
        default=None, alias="Output_1", description="시간대별 체결 목록"
    )
    output_2: list[KrStockQuoteCurrentPriceExpectedOutput] | KrStockQuoteCurrentPriceExpectedOutput | None = Field(
        default=None,
        alias="Output_2",
        description="예상체결/ECN 정보 (스펙은 Array, 실제 예시는 Object — 둘 다 허용)",
    )


class KrStockQuoteCurrentExecutionTickOutput(BaseModel):
    """주식현재가 체결 시간대별 체결 상세 (Output_0 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    bsop_hour: str | None = Field(default=None, description="시간 / 길이 8")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 8")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 8")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    cntg_vol: int | None = Field(default=None, description="변동거래량 / 길이 12")
    shnu_cntg_smtn: int | None = Field(default=None, description="누적매수체결량 / 길이 12")
    bidrate: float | None = Field(default=None, description="당일매수비중 / 길이 5.2")
    seln_cntg_smtn: int | None = Field(default=None, description="누적매도체결량 / 길이 12")
    askrate: float | None = Field(default=None, description="당일매도비중 / 길이 5.2")
    stnr_cntg_smtn: int | None = Field(default=None, description="누적보합체결량 / 길이 12")
    uncrate: float | None = Field(default=None, description="당일보합비중 / 길이 5.2")
    cttr: float | None = Field(default=None, description="체결강도 / 길이 6.2")
    askp: int | None = Field(default=None, description="매도호가 / 길이 8")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 8")
    acml_vol: int | None = Field(default=None, description="전체거래량 / 길이 12")
    filler: str | None = Field(default=None, description="filler / 길이 30")


class KrStockQuoteCurrentExecutionSummaryOutput(BaseModel):
    """주식현재가 체결 종목 종합 정보 (Output_1)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    iem_nm: str | None = Field(default=None, description="KOR_종목명 / 길이 40")
    # 아래 수치류 필드는 스펙상 string 이지만, currentPrice(balance/dailyPnl 포함)에서
    # 반복 확인된 "합계/가격류가 string 으로 명세되지만 실서버는 int 로 응답" 패턴과
    # 동일한 이름 규칙(vol/su/prc 계열)이라 선제적으로 int|str 로 완화한다.
    toffervol: int | str | None = Field(default=None, description="누적매도가체결량 / 길이 12")
    tbidvol: int | str | None = Field(default=None, description="누적매수가체결량 / 길이 12")
    tbovol: int | str | None = Field(default=None, description="누적보합가체결량 / 길이 12")
    toffersu: int | str | None = Field(default=None, description="누적매도가체결건수 / 길이 10")
    tbidsu: int | str | None = Field(default=None, description="누적매수가체결건수 / 길이 10")
    tbosu: int | str | None = Field(default=None, description="누적보합가체결건수 / 길이 10")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 8")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 8")
    acml_vol: int | None = Field(default=None, description="전체거래량 / 길이 12")
    stck_oprc: int | str | None = Field(default=None, description="시가 / 길이 8")
    stck_hgpr: int | str | None = Field(default=None, description="고가 / 길이 8")
    stck_lwpr: int | str | None = Field(default=None, description="저가 / 길이 8")
    askp: int | None = Field(default=None, description="매도호가 / 길이 8")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 8")
    cttr: float | None = Field(default=None, description="체결강도 / 길이 6.2")
    new_volume: int | str | None = Field(default=None, description="신규거래량 / 길이 12")
    stck_prdy_clpr: int | str | None = Field(
        default=None, description="전일종가 / 길이 8 / 기준가 혹은 전일종가 기준가 우선 셋팅"
    )
    filler: str | None = Field(default=None, description="filler / 길이 30")
    ctsz20: str | None = Field(default=None, description="CTSz20 / 길이 20")
    nextbutton: str | None = Field(default=None, description="NEXTBUTTON / 길이 1")


class KrStockQuoteCurrentExecution(NHPlugAssetHttpBody):
    """주식현재가 체결 (`POST /krstock/quote/v1/currentExecution`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). currentPrice 와 달리 `Output_0` 이 곧바로
    배열이고 `Output_1` 이 단일 종합 객체다(반대로 뒤집힌 구조).
    """

    output_0: list[KrStockQuoteCurrentExecutionTickOutput] | None = Field(
        default=None, alias="Output_0", description="시간대별 체결 상세 목록"
    )
    output_1: KrStockQuoteCurrentExecutionSummaryOutput | None = Field(
        default=None, alias="Output_1", description="종목 종합 정보"
    )


class KrStockQuoteCurrentDailyOutput(BaseModel):
    """주식현재가 일자별 일별 시세 상세 (Output_0 배열의 각 항목).

    스펙은 이 블록의 모든 필드를 string 으로 선언한다. currentPrice/currentExecution
    에서 반복 확인된 "수치류 필드가 string 으로 명세되지만 실서버는 int/float 로
    응답" 패턴이 여기서도 실측 확인됐다(2026-08-22, 005930) — 확인된 필드만
    int|float|str 로 완화했다(날짜·코드·filler 류는 실제로도 string 이라 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    bsop_date: str | None = Field(default=None, description="일자 / 길이 8 / YY/MM/DD")
    stck_oprc: int | str | None = Field(default=None, description="시가 / 길이 9")
    stck_hgpr: int | str | None = Field(default=None, description="고가 / 길이 9")
    stck_lwpr: int | str | None = Field(default=None, description="저가 / 길이 9")
    stck_clpr: int | str | None = Field(default=None, description="종가 / 길이 9")
    prdy_vrss_sign: str | None = Field(default=None, description="FILLER / 길이 1")
    prdy_vrss: int | str | None = Field(default=None, description="등락폭 / 길이 9")
    prdy_ctrt: float | str | None = Field(default=None, description="등락률 / 길이 5.2")
    acml_vol: int | str | None = Field(default=None, description="거래량 / 길이 12")
    acml_tr_pbmn: int | str | None = Field(default=None, description="거래대금 / 길이 18")
    high_date: str | None = Field(default=None, description="고가일 / 길이 8")
    low_date: str | None = Field(default=None, description="저가일 / 길이 8")
    vol_prdy_rt: float | str | None = Field(default=None, description="거래량전일비 / 길이 6.2")
    cttr: float | str | None = Field(default=None, description="체결강도 / 길이 6.2")
    filler: str | None = Field(default=None, description="FILLER / 길이 43")
    next_key: str | None = Field(default=None, description="NEXT_KEY / 길이 12")
    nextbutton: str | None = Field(default=None, description="NEXTBUTTON / 길이 1")


class KrStockQuoteCurrentDaily(NHPlugAssetHttpBody):
    """주식현재가 일자별 (`POST /krstock/quote/v1/currentDaily`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 응답 블록은 `Output_0` 하나뿐이고
    그 자체가 배열이다(currentExecution 의 `Output_0` 과 같은 모양).
    """

    output_0: list[KrStockQuoteCurrentDailyOutput] | None = Field(
        default=None, alias="Output_0", description="일별 시세 상세 목록"
    )


class KrStockQuoteCurrentInvestorOutput(BaseModel):
    """주식현재가 투자자 투자자별 거래현황 상세 (Output_0 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    bsop_date1: str | None = Field(default=None, description="거래일자 / 길이 8 / YYYYMMDD")
    bsop_date2: str | None = Field(default=None, description="거래일자 / 길이 8 / YYMMDD00")
    stck_prpr: int | None = Field(default=None, description="종가 / 길이 7")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 6")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    acml_vol: float | None = Field(default=None, description="거래량 / 길이 10")
    for_rate: float | None = Field(default=None, description="외국인지분율 / 길이 5.2")
    frgn_ntby_qty: float | None = Field(default=None, description="외국인순매수량 / 길이 10")
    person: float | None = Field(default=None, description="개인투자자순매수량 / 길이 10")
    gigwan: float | None = Field(default=None, description="기관계투자자순매수량 / 길이 10")
    invest: float | None = Field(default=None, description="외국인투자자순매수량 / 길이 10")
    account: float | None = Field(default=None, description="거래원순매수량 / 길이 10")
    program: float | None = Field(default=None, description="프로그램 / 길이 10")
    jasaz10: str | None = Field(default=None, description="자사주 / 길이 10")
    filler: str | None = Field(default=None, description="FILLER / 길이 30")


class KrStockQuoteCurrentInvestor(NHPlugAssetHttpBody):
    """주식현재가 투자자 (`POST /krstock/quote/v1/currentInvestor`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 응답 블록은 `Output_0` 하나뿐이고
    그 자체가 배열이다.
    """

    output_0: list[KrStockQuoteCurrentInvestorOutput] | None = Field(
        default=None, alias="Output_0", description="투자자별 거래현황 상세 목록"
    )


class KrStockQuotePeriodOutput(BaseModel):
    """국내주식기간별시세(일/주/월/년) 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    qry_date: str | None = Field(default=None, description="조회날짜 / 길이 8 / YYYYMMDD")
    qry_time: str | None = Field(default=None, description="조회시간 / 길이 6 / HHmmSS")
    iem_cd: str | None = Field(default=None, description="단축종목코드 / 길이 9")
    iem_nm: str | None = Field(default=None, description="한글종목명 / 길이 41")
    stck_prpr: str | None = Field(default=None, description="현재가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="전일대비부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    prdy_vrss: str | None = Field(default=None, description="전일대비 / 길이 10")
    prdy_ctrt: str | None = Field(default=None, description="전일대비율 / 길이 5 / float 5.2")
    acml_vol: str | None = Field(default=None, description="누적거래량 / 길이 12")
    acml_tr_pbmn: str | None = Field(default=None, description="누적거래대금 / 길이 18")
    prdy_vol: str | None = Field(default=None, description="전일거래량 / 길이 12")
    prdy_vol_rate: str | None = Field(default=None, description="거래량전일비 / 길이 15 / float 15.2")
    vol_rate: str | None = Field(default=None, description="거래량회전율 / 길이 10 / float 10.5")
    cttr: str | None = Field(default=None, description="체결강도 / 길이 6 / float 6.2")
    prdy_cttr: str | None = Field(default=None, description="전일체결강도 / 길이 6 / float 6.2")
    askp: str | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: str | None = Field(default=None, description="매수호가 / 길이 10")
    askp_rsqn1: str | None = Field(default=None, description="매도1호가잔량 / 길이 12")
    bidp_rsqn1: str | None = Field(default=None, description="매수1호가잔량 / 길이 12")
    stck_mxpr: str | None = Field(default=None, description="상한가 / 길이 10")
    stck_llam: str | None = Field(default=None, description="하한가 / 길이 10")
    stck_oprc: str | None = Field(default=None, description="시가 / 길이 10")
    stck_hgpr: str | None = Field(default=None, description="고가 / 길이 10")
    stck_lwpr: str | None = Field(default=None, description="저가 / 길이 10")
    lstn_stcn: str | None = Field(default=None, description="상장주수 / 길이 12")
    hts_avls: str | None = Field(default=None, description="시가총액 / 길이 10 / 억단위")
    dae_rate: str | None = Field(default=None, description="대주주지분율 / 길이 5 / float 5.2")
    per: str | None = Field(default=None, description="PER / 길이 5 / float 5.2")
    pbr: str | None = Field(default=None, description="PBR / 길이 5 / float 5.2")
    eps: str | None = Field(default=None, description="EPS / 길이 9")
    bps: str | None = Field(default=None, description="BPS / 길이 10")
    prdy_oprc: str | None = Field(default=None, description="전일시가 / 길이 10")
    prdy_high: str | None = Field(default=None, description="전일고가 / 길이 10")
    prdy_low: str | None = Field(default=None, description="전일저가 / 길이 10")
    prdy_clpr: str | None = Field(default=None, description="전일종가 / 길이 10")
    tdw_oprc: str | None = Field(default=None, description="이번주시가 / 길이 10")
    tdw_high: str | None = Field(default=None, description="이번주고가 / 길이 10")
    tdw_low: str | None = Field(default=None, description="이번주저가 / 길이 10")
    tdm_oprc: str | None = Field(default=None, description="이번달시가 / 길이 10")
    tdm_high: str | None = Field(default=None, description="이번달고가 / 길이 10")
    tdm_low: str | None = Field(default=None, description="이번달저가 / 길이 10")
    vi_sttc_mxpr: str | None = Field(default=None, description="VI정적발동상승 / 길이 10")
    vi_sttc_llam: str | None = Field(default=None, description="VI정적발동하락 / 길이 10")
    start_time: str | None = Field(default=None, description="장시작시간 / 길이 6 / HHmmSS")
    end_time: str | None = Field(default=None, description="장마감시간 / 길이 6 / HHmmSS")
    bsop_date: str | None = Field(default=None, description="영업일 / 길이 8")
    stck_sdpr: str | None = Field(default=None, description="주식기준가 / 길이 10")
    stck_fcam: str | None = Field(default=None, description="주식액면가 / 길이 10")
    bstp_kor_isnm: str | None = Field(default=None, description="업종한글명 / 길이 40")
    bstp_cls_code: str | None = Field(default=None, description="업종코드 / 길이 6")
    exchange_prpr: str | None = Field(default=None, description="달러환율 / 길이 8")
    ctsz30: str | None = Field(default=None, description="연속조회키 / 길이 30")
    lasttickcount: str | None = Field(default=None, description="마지막N틱봉의틱묶음갯수 / 길이 5 / 최근봉마지막틱갯수")
    send_cnt: str | None = Field(default=None, description="전송레코드건수 / 길이 5")
    pre_tr_sta_hour: str | None = Field(default=None, description="프리마켓시작시간 / 길이 6 / NXT/UNT프리마켓시작시간")
    pre_tr_fin_hour: str | None = Field(default=None, description="프리마켓종료시간 / 길이 6 / NXT/UNT프리마켓종료시간")
    main_tr_sta_hour: str | None = Field(
        default=None, description="메인마겟시작시간 / 길이 6 / NXT/UNT메인마켓시작시간"
    )
    main_tr_fin_hour: str | None = Field(
        default=None, description="메인마겟종료시간 / 길이 6 / NXT/UNT메인마켓종료시간"
    )
    aft_tr_sta_hour: str | None = Field(
        default=None, description="에프터마겟시작시간 / 길이 6 / NXT/UNT에프터마켓시작시간"
    )
    aft_tr_fin_hour: str | None = Field(
        default=None, description="에프터마겟종료시간 / 길이 6 / NXT/UNT에프터마켓종료시간"
    )
    cncc_aspr_sta_hour: str | None = Field(
        default=None, description="정규장마감전동시호가 / 길이 6 / KRX/UNT종료전동시호가시작시간"
    )


class KrStockQuotePeriodBarOutput(BaseModel):
    """국내주식기간별시세(일/주/월/년) 주기별 봉 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    bsop_date: str | None = Field(default=None, description="영업일 / 길이 8")
    bsop_time: str | None = Field(default=None, description="시간 / 길이 6 / HHmmSS")
    stck_sdpr: str | None = Field(default=None, description="주식기준가 / 길이 10")
    stck_oprc: str | None = Field(default=None, description="시가 / 길이 10")
    stck_hgpr: str | None = Field(default=None, description="고가 / 길이 10")
    stck_lwpr: str | None = Field(default=None, description="저가 / 길이 10")
    stck_prpr: str | None = Field(default=None, description="현재가 / 길이 10")
    vol: str | None = Field(default=None, description="거래량 / 길이 15")
    tr_pbmn: str | None = Field(default=None, description="거래대금 / 길이 18")
    flng_cls_code: str | None = Field(
        default=None,
        description="락구분코드 / 길이 2 / 01.권리락 02.배당락 03.분배락 04.권배락 05.중간배당락 06.권리중간배당락 07.권리분기배당락 99.기타",
    )
    prtt_rate: str | None = Field(default=None, description="락비율 / 길이 8 / float 8.2")
    news_cnt: str | None = Field(default=None, description="뉴스건수 / 길이 3 / 일간일때만처리")
    updownmark: str | None = Field(default=None, description="상하한가표시 / 길이 1 / 0.기본 1.상한 4.하한")
    fcam_mod_cls_code: str | None = Field(
        default=None,
        description="액면가변경구분코드 / 길이 2 / 00.해당없음 01.액면분할 02.액면병합 03.주식분할 04.주식병합 99.기타",
    )
    vol_prtt_rate: str | None = Field(default=None, description="거래량수정비율 / 길이 2")


class KrStockQuotePeriod(NHPlugAssetHttpBody):
    """국내주식기간별시세(일/주/월/년) (`POST /krstock/quote/v1/period`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 스펙은 `Output_0` 을 Array 로 선언하지만
    스펙 자체의 x-schema-warning 이 예시 응답은 Object 라고 명시한다 —
    object/array 둘 다 허용하는 Union 으로 받는다. `Output_1` 은 주기별(일/주/월/년)
    봉 상세 배열이다.
    """

    output_0: list[KrStockQuotePeriodOutput] | KrStockQuotePeriodOutput | None = Field(
        default=None,
        alias="Output_0",
        description="종합 정보 (스펙은 Array, 실제 예시는 Object — 둘 다 허용)",
    )
    output_1: list[KrStockQuotePeriodBarOutput] | None = Field(
        default=None, alias="Output_1", description="주기별 봉 상세 목록"
    )


class KrStockQuoteAfterHoursCurrentOutput(BaseModel):
    """국내주식 시간외현재가 시간외 단일가 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 41")
    mrkt_cls_code: str | None = Field(default=None, description="시장구분 / 길이 1")
    trht_yn: str | None = Field(default=None, description="거래구분 / 길이 1")
    mkop_cls_code: str | None = Field(default=None, description="장구분 / 길이 1")
    stck_prpr: int | None = Field(default=None, description="정규장종가 / 길이 10")
    ovtm_untp_sdpr: int | None = Field(default=None, description="기준가 / 길이 10")
    ovtm_untp_mxpr: int | None = Field(default=None, description="상한가 / 길이 10")
    ovtm_untp_llam: int | None = Field(default=None, description="하한가 / 길이 10")
    ovtm_cntg_hour: str | None = Field(default=None, description="체결시간 / 길이 8")
    ovtm_untp_prpr: int | None = Field(default=None, description="체결가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="체결등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    ovtm_prdy_vrss: int | None = Field(default=None, description="체결등락폭 / 길이 10")
    ovtm_prdy_ctrt: float | None = Field(default=None, description="체결등락률 / 길이 5.2")
    ovtm_untp_oprc: int | None = Field(default=None, description="시가 / 길이 10")
    ovtm_untp_hgpr: int | None = Field(default=None, description="고가 / 길이 10")
    ovtm_untp_lwpr: int | None = Field(default=None, description="저가 / 길이 10")
    ovtm_untp_vol: int | None = Field(default=None, description="거래량 / 길이 12")
    ovtm_tr_pbmn: int | None = Field(default=None, description="거래대금 / 길이 12")
    ovtm_untp_askp: int | None = Field(default=None, description="매도호가 / 길이 10")
    ovtm_untp_bidp: int | None = Field(default=None, description="매수호가 / 길이 10")
    ovtm_bsop_hour: str | None = Field(default=None, description="호가시간 / 길이 8")
    ovtm_untp_askp1: int | None = Field(default=None, description="매도1차선호가 / 길이 10")
    ovtm_untp_askp2: int | None = Field(default=None, description="매도2차선호가 / 길이 10")
    ovtm_untp_askp3: int | None = Field(default=None, description="매도3차선호가 / 길이 10")
    ovtm_untp_askp4: int | None = Field(default=None, description="매도4차선호가 / 길이 10")
    ovtm_untp_askp5: int | None = Field(default=None, description="매도5차선호가 / 길이 10")
    ovtm_untp_askp6: int | None = Field(default=None, description="매도6차선호가 / 길이 10")
    ovtm_untp_askp7: int | None = Field(default=None, description="매도7차선호가 / 길이 10")
    ovtm_untp_askp8: int | None = Field(default=None, description="매도8차선호가 / 길이 10")
    ovtm_untp_askp9: int | None = Field(default=None, description="매도9차선호가 / 길이 10")
    ovtm_untp_askp10: int | None = Field(default=None, description="매도10차선호가 / 길이 10")
    ovtm_untp_bidp1: int | None = Field(default=None, description="매수1차선호가 / 길이 10")
    ovtm_untp_bidp2: int | None = Field(default=None, description="매수2차선호가 / 길이 10")
    ovtm_untp_bidp3: int | None = Field(default=None, description="매수3차선호가 / 길이 10")
    ovtm_untp_bidp4: int | None = Field(default=None, description="매수4차선호가 / 길이 10")
    ovtm_untp_bidp5: int | None = Field(default=None, description="매수5차선호가 / 길이 10")
    ovtm_untp_bidp6: int | None = Field(default=None, description="매수6차선호가 / 길이 10")
    ovtm_untp_bidp7: int | None = Field(default=None, description="매수7차선호가 / 길이 10")
    ovtm_untp_bidp8: int | None = Field(default=None, description="매수8차선호가 / 길이 10")
    ovtm_untp_bidp9: int | None = Field(default=None, description="매수9차선호가 / 길이 10")
    ovtm_untp_bidp10: int | None = Field(default=None, description="매수10차선호가 / 길이 10")
    ovtm_askp_rsqn1: int | None = Field(default=None, description="매도1차선잔량 / 길이 12")
    ovtm_askp_rsqn2: int | None = Field(default=None, description="매도2차선잔량 / 길이 12")
    ovtm_askp_rsqn3: int | None = Field(default=None, description="매도3차선잔량 / 길이 12")
    ovtm_askp_rsqn4: int | None = Field(default=None, description="매도4차선잔량 / 길이 12")
    ovtm_askp_rsqn5: int | None = Field(default=None, description="매도5차선잔량 / 길이 12")
    ovtm_askp_rsqn6: int | None = Field(default=None, description="매도6차선잔량 / 길이 12")
    ovtm_askp_rsqn7: int | None = Field(default=None, description="매도7차선잔량 / 길이 12")
    ovtm_askp_rsqn8: int | None = Field(default=None, description="매도8차선잔량 / 길이 12")
    ovtm_askp_rsqn9: int | None = Field(default=None, description="매도9차선잔량 / 길이 12")
    ovtm_askp_rsqn10: int | None = Field(default=None, description="매도10차선잔량 / 길이 12")
    ovtm_bidp_rsqn1: int | None = Field(default=None, description="매수1차선잔량 / 길이 12")
    ovtm_bidp_rsqn2: int | None = Field(default=None, description="매수2차선잔량 / 길이 12")
    ovtm_bidp_rsqn3: int | None = Field(default=None, description="매수3차선잔량 / 길이 12")
    ovtm_bidp_rsqn4: int | None = Field(default=None, description="매수4차선잔량 / 길이 12")
    ovtm_bidp_rsqn5: int | None = Field(default=None, description="매수5차선잔량 / 길이 12")
    ovtm_bidp_rsqn6: int | None = Field(default=None, description="매수6차선잔량 / 길이 12")
    ovtm_bidp_rsqn7: int | None = Field(default=None, description="매수7차선잔량 / 길이 12")
    ovtm_bidp_rsqn8: int | None = Field(default=None, description="매수8차선잔량 / 길이 12")
    ovtm_bidp_rsqn9: int | None = Field(default=None, description="매수9차선잔량 / 길이 12")
    ovtm_bidp_rsqn10: int | None = Field(default=None, description="매수10차선잔량 / 길이 12")
    total_askp_rsqn: int | None = Field(default=None, description="매도잔량합 / 길이 12")
    total_bidp_rsqn: int | None = Field(default=None, description="매수잔량합 / 길이 12")
    ecn_dongsi: str | None = Field(default=None, description="동시구분 / 길이 1 / 1.동시호가 이외 정규시장")
    ovtm_antc_cnpr: int | None = Field(default=None, description="예상체결가 / 길이 10")
    antc_vrss_sign: str | None = Field(
        default=None,
        description="예상체결부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    antc_cntg_vrss: int | None = Field(default=None, description="예상체결등락폭 / 길이 10")
    antc_cntg_ctrt: float | None = Field(default=None, description="예상체결등락률 / 길이 5.2")
    antc_vol: int | None = Field(default=None, description="예상체결수량 / 길이 12")
    antc_tr_pbmn: int | None = Field(default=None, description="예상대금 / 길이 12")
    item_info: str | None = Field(default=None, description="종목정보 / 길이 28")
    ivs_hed_yn: str | None = Field(default=None, description="투자유의종목여부 / 길이 1 / Y.투자유의종목")
    short_ovh_gb: str | None = Field(
        default=None, description="단기과열구분코드 / 길이 1 / 1.단기과열예고 2.단기과열지정 3.단기과열연장"
    )
    alert_gb: str | None = Field(
        default=None,
        description="투자주의경고구분코드 / 길이 1 / 1.투자주의 2.투자경고 3.투자주의>투자위험예고 4.투자경고투자위험예고 5.투자위험",
    )
    jungri_yn: str | None = Field(default=None, description="정리매매여부 / 길이 1 / Y.정리매매종목")


class KrStockQuoteAfterHoursCurrentRegularOutput(BaseModel):
    """국내주식 시간외현재가 정규장 종합 정보 (Output_1).

    스펙은 대부분 필드를 string 으로 선언하지만, 2026-08-22 실측(005930)에서
    아래 19개 필드가 실제로는 int/float 로 내려오는 것을 확인해 `int|float|str`
    로 완화했다(다른 필드는 실측에서도 문자열로 와서 스펙 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    bsop_date: str | None = Field(default=None, description="일자 / 길이 8")
    acml_vol: int | str | None = Field(default=None, description="거래량 / 길이 12")
    vol_rate: float | str | None = Field(default=None, description="거래량전일비 / 길이 6.2")
    acml_tr_pbmn: int | str | None = Field(default=None, description="거래대금 / 길이 12")
    stck_oprc: int | str | None = Field(default=None, description="시가 / 길이 10")
    stck_hgpr: int | str | None = Field(default=None, description="고가 / 길이 10")
    stck_lwpr: int | str | None = Field(default=None, description="저가 / 길이 10")
    stck_prpr: int | None = Field(default=None, description="정규장종가 / 길이 10")
    stck_mxpr: int | str | None = Field(default=None, description="상한가 / 길이 10")
    stck_llam: int | str | None = Field(default=None, description="하한가 / 길이 10")
    stck_fcam: int | str | None = Field(default=None, description="액면가 / 길이 10")
    askp: int | str | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: int | str | None = Field(default=None, description="매수호가 / 길이 10")
    askp_rsqn: int | str | None = Field(default=None, description="매도잔량 / 길이 12")
    bidp_rsqn: int | str | None = Field(default=None, description="매수잔량 / 길이 12")
    total_askp_rsqn: int | None = Field(default=None, description="매도잔량합 / 길이 12")
    total_bidp_rsqn: int | None = Field(default=None, description="매수잔량합 / 길이 12")
    ovtm_askp_rsqn: int | str | None = Field(default=None, description="시간외매도잔량 / 길이 12")
    ovtm_bidp_rsqn: int | str | None = Field(default=None, description="시간외매수잔량 / 길이 12")
    frgn_hour: str | None = Field(default=None, description="외국인시간 / 길이 6")
    for_rate: float | str | None = Field(default=None, description="외국인지분율 / 길이 5.2")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="체결등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | str | None = Field(default=None, description="등락폭 / 길이 10")
    prdy_ctrt: float | str | None = Field(default=None, description="등락률 / 길이 5.2")
    sosokz6: str | None = Field(default=None, description="코스피구분 / 길이 6")
    bstp_kor_isnm: str | None = Field(default=None, description="업종명 / 길이 40")
    bstp_cls_code: str | None = Field(default=None, description="업종코드 / 길이 6")
    cap_size: str | None = Field(default=None, description="자본금규모 / 길이 6")
    new_volume: int | str | None = Field(default=None, description="신규거래량 / 길이 12")


class KrStockQuoteAfterHoursCurrent(NHPlugAssetHttpBody):
    """국내주식 시간외현재가 (`POST /krstock/quote/v1/afterHoursCurrent`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `iem_cd` 하나뿐이다(market_cd
    없음 — 다른 quote API 와 다르다). `Output_0` 은 시간외 단일가 종합 정보,
    `Output_1` 은 정규장 종합 정보로 둘 다 단일 객체다(배열 아님).
    """

    output_0: KrStockQuoteAfterHoursCurrentOutput | None = Field(
        default=None, alias="Output_0", description="시간외 단일가 종합 정보"
    )
    output_1: KrStockQuoteAfterHoursCurrentRegularOutput | None = Field(
        default=None, alias="Output_1", description="정규장 종합 정보"
    )


class KrStockQuoteCurrentAfterHoursDailyTickOutput(BaseModel):
    """주식현재가 시간외일자별주가 시간외 체결 상세 (Output_0 배열의 각 항목).

    스펙의 필드명과 description 이 서로 어긋나 있다(예: `shrn_iscd` 설명이
    "고가"). 원문 description 을 그대로 보존한다.
    """

    model_config = ConfigDict(extra="allow")

    qry_date: str | None = Field(default=None, description="일자 / 길이 8")
    qry_time: str | None = Field(default=None, description="시가 / 길이 6")
    shrn_iscd: str | None = Field(default=None, description="고가 / 길이 9")
    hts_kor_isnm: str | None = Field(default=None, description="저가 / 길이 41")
    stck_prpr: str | None = Field(default=None, description="락구분 / 길이 10")
    prdy_vrss_sign: str | None = Field(default=None, description="Filler / 길이 1")


class KrStockQuoteCurrentAfterHoursDailyOutput(BaseModel):
    """주식현재가 시간외일자별주가 종합 상세 (Output_1 배열의 각 항목).

    스펙은 4개 필드 모두 string 으로 선언하지만, 2026-08-22 실측(005930)에서
    `acml_vol`/`acml_tr_pbmn` 이 실제로는 int 로 내려오는 것을 확인해
    `int|str` 로 완화했다(`prdy_ctrt`/`prdy_vol` 은 실측에서도 문자열이라
    스펙 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    prdy_ctrt: str | None = Field(default=None, description="현재가 / 길이 5")
    acml_vol: int | str | None = Field(default=None, description="거래량 / 길이 12")
    acml_tr_pbmn: int | str | None = Field(default=None, description="거래대금 / 길이 18")
    prdy_vol: str | None = Field(default=None, description="Filler / 길이 12")


class KrStockQuoteCurrentAfterHoursDaily(NHPlugAssetHttpBody):
    """주식현재가 시간외일자별주가 (`POST /krstock/quote/v1/currentAfterHoursDaily`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `market_cd` 없이 `iem_cd` 외
    `date`/`array_cnt`/`maxavg`/`gubun` 이 전부 required 다(다른 quote API 와
    달리 선택 필드가 없다). `Output_0`/`Output_1` 모두 배열이다.
    """

    output_0: list[KrStockQuoteCurrentAfterHoursDailyTickOutput] | None = Field(
        default=None, alias="Output_0", description="시간외 체결 상세 목록"
    )
    output_1: list[KrStockQuoteCurrentAfterHoursDailyOutput] | None = Field(
        default=None, alias="Output_1", description="종합 상세 목록"
    )


class KrStockQuoteCurrentAfterHoursExecutionOutput(BaseModel):
    """주식현재가 시간외시간별체결 상세 (Output_0 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    bsop_hour: str | None = Field(default=None, description="시간 / 길이 8")
    open: int | None = Field(default=None, description="시가 / 길이 9")
    high: int | None = Field(default=None, description="고가 / 길이 9")
    low: int | None = Field(default=None, description="저가 / 길이 9")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 9")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 9")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    acml_vol: float | None = Field(default=None, description="거래량 / 길이 10")
    cntg_vol: float | None = Field(default=None, description="변동거래량 / 길이 10")
    cntg_tr_pbmn: float | None = Field(default=None, description="거래대금 / 길이 14")
    askp1: int | None = Field(default=None, description="매도호가 / 길이 9")
    bidp1: int | None = Field(default=None, description="매수호가 / 길이 9")
    filler: str | None = Field(default=None, description="Filler / 길이 30")


class KrStockQuoteCurrentAfterHoursExecution(NHPlugAssetHttpBody):
    """주식현재가 시간외시간별체결 (`POST /krstock/quote/v1/currentAfterHoursExecution`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `iem_cd` 하나뿐이다(market_cd
    없음 — afterHoursCurrent/currentAfterHoursDaily 와 같은 패턴). `Output_0`
    하나만 있고 배열이다.
    """

    output_0: list[KrStockQuoteCurrentAfterHoursExecutionOutput] | None = Field(
        default=None, alias="Output_0", description="시간외 시간별 체결 상세 목록"
    )


class KrStockQuoteAfterHoursExpectedOutput(BaseModel):
    """주식현재가 시간외시간별예상 상세 (Output_0 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    bsop_hour: str | None = Field(default=None, description="시간 / 길이 8")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 9")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보함+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 9")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    cntg_vol: float | None = Field(default=None, description="거래량 / 길이 10")
    askp1: int | None = Field(default=None, description="매도호가 / 길이 9")
    bidp1: int | None = Field(default=None, description="매수호가 / 길이 9")
    askp_rsqn1: float | None = Field(default=None, description="매도잔량 / 길이 10")
    bidp_rsqn1: float | None = Field(default=None, description="매수잔량 / 길이 10")
    filler: str | None = Field(default=None, description="Filler / 길이 30")


class KrStockQuoteAfterHoursExpected(NHPlugAssetHttpBody):
    """주식현재가 시간외시간별예상 (`POST /krstock/quote/v1/afterHoursExpected`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `iem_cd` 하나뿐이다(market_cd
    없음 — afterHoursCurrent/currentAfterHoursDaily/currentAfterHoursExecution
    과 같은 패턴). `Output_0` 하나만 있고 배열이다. currentAfterHoursExecution
    과 구조가 거의 같다(예상체결가 버전).
    """

    output_0: list[KrStockQuoteAfterHoursExpectedOutput] | None = Field(
        default=None, alias="Output_0", description="시간외 시간별 예상체결 상세 목록"
    )


class KrStockQuoteEtfCurrentOutput(BaseModel):
    """ETF/ETN 현재가 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 6")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 41")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 10")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 5.2")
    askp: int | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 10")
    acml_vol: int | None = Field(default=None, description="거래량 / 길이 12")
    acml_rate: float | None = Field(default=None, description="거래비율 / 길이 6.2")
    yu_rate: float | None = Field(default=None, description="유동주회전율 / 길이 5.2")
    acml_tr_pbmn: int | None = Field(default=None, description="거래대금 / 길이 12")
    stck_mxpr: int | None = Field(default=None, description="상한가 / 길이 10")
    stck_hgpr: int | None = Field(default=None, description="고가 / 길이 10")
    stck_oprc: int | None = Field(default=None, description="시가 / 길이 10")
    oprc_sign: str | None = Field(
        default=None,
        description="시가대비부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    oprc_vrss: int | None = Field(default=None, description="시가대비등락폭 / 길이 10")
    stck_lwpr: int | None = Field(default=None, description="저가 / 길이 10")
    stck_llam: int | None = Field(default=None, description="하한가 / 길이 10")
    bsop_hour: str | None = Field(default=None, description="호가시간 / 길이 8")
    askp1: int | None = Field(default=None, description="매도1호가 / 길이 10")
    askp2: int | None = Field(default=None, description="매도2호가 / 길이 10")
    askp3: int | None = Field(default=None, description="매도3호가 / 길이 10")
    askp4: int | None = Field(default=None, description="매도4호가 / 길이 10")
    askp5: int | None = Field(default=None, description="매도5호가 / 길이 10")
    askp6: int | None = Field(default=None, description="매도6호가 / 길이 10")
    askp7: int | None = Field(default=None, description="매도7호가 / 길이 10")
    askp8: int | None = Field(default=None, description="매도8호가 / 길이 10")
    askp9: int | None = Field(default=None, description="매도9호가 / 길이 10")
    askp10: int | None = Field(default=None, description="매도10호가 / 길이 10")
    bidp1: int | None = Field(default=None, description="매수1호가 / 길이 10")
    bidp2: int | None = Field(default=None, description="매수2호가 / 길이 10")
    bidp3: int | None = Field(default=None, description="매수3호가 / 길이 10")
    bidp4: int | None = Field(default=None, description="매수4호가 / 길이 10")
    bidp5: int | None = Field(default=None, description="매수5호가 / 길이 10")
    bidp6: int | None = Field(default=None, description="매수6호가 / 길이 10")
    bidp7: int | None = Field(default=None, description="매수7호가 / 길이 10")
    bidp8: int | None = Field(default=None, description="매수8호가 / 길이 10")
    bidp9: int | None = Field(default=None, description="매수9호가 / 길이 10")
    bidp10: int | None = Field(default=None, description="매수10호가 / 길이 10")
    askp_rsqn1: int | None = Field(default=None, description="매도1호가잔량 / 길이 12")
    askp_rsqn2: int | None = Field(default=None, description="매도2호가잔량 / 길이 12")
    askp_rsqn3: int | None = Field(default=None, description="매도3호가잔량 / 길이 12")
    askp_rsqn4: int | None = Field(default=None, description="매도4호가잔량 / 길이 12")
    askp_rsqn5: int | None = Field(default=None, description="매도5호가잔량 / 길이 12")
    askp_rsqn6: int | None = Field(default=None, description="매도6호가잔량 / 길이 12")
    askp_rsqn7: int | None = Field(default=None, description="매도7호가잔량 / 길이 12")
    askp_rsqn8: int | None = Field(default=None, description="매도8호가잔량 / 길이 12")
    askp_rsqn9: int | None = Field(default=None, description="매도9호가잔량 / 길이 12")
    askp_rsqn10: int | None = Field(default=None, description="매도10호가잔량 / 길이 12")
    bidp_rsqn1: int | None = Field(default=None, description="매수1호가잔량 / 길이 12")
    bidp_rsqn2: int | None = Field(default=None, description="매수2호가잔량 / 길이 12")
    bidp_rsqn3: int | None = Field(default=None, description="매수3호가잔량 / 길이 12")
    bidp_rsqn4: int | None = Field(default=None, description="매수4호가잔량 / 길이 12")
    bidp_rsqn5: int | None = Field(default=None, description="매수5호가잔량 / 길이 12")
    bidp_rsqn6: int | None = Field(default=None, description="매수6호가잔량 / 길이 12")
    bidp_rsqn7: int | None = Field(default=None, description="매수7호가잔량 / 길이 12")
    bidp_rsqn8: int | None = Field(default=None, description="매수8호가잔량 / 길이 12")
    bidp_rsqn9: int | None = Field(default=None, description="매수9호가잔량 / 길이 12")
    bidp_rsqn10: int | None = Field(default=None, description="매수10호가잔량 / 길이 12")
    total_askp_rsqn: int | None = Field(default=None, description="총매도호가잔량 / 길이 12")
    total_bidp_rsqn: int | None = Field(default=None, description="총매수호가잔량 / 길이 12")
    ovtm_askp_rsqn: int | None = Field(default=None, description="시간외매도잔량 / 길이 12")
    ovtm_bidp_rsqn: int | None = Field(default=None, description="시간외매수잔량 / 길이 12")
    pvt_scnd_dmrs: int | None = Field(default=None, description="피벗2차저항 / 길이 10")
    pvt_frst_dmrs: int | None = Field(default=None, description="피벗1차저항 / 길이 10")
    pvt_pont_val: int | None = Field(default=None, description="피벗가 / 길이 10")
    pvt_frst_dmsp: int | None = Field(default=None, description="피벗1차지지 / 길이 10")
    pvt_scnd_dmsp: int | None = Field(default=None, description="피벗2차지지 / 길이 10")
    mrkt_div_code: str | None = Field(default=None, description="코스닥코스피구분 / 길이 6")
    bstp_cls_code: str | None = Field(default=None, description="지수코드 / 길이 6")
    bstp_kor_isnm: str | None = Field(default=None, description="업종명 / 길이 40")
    cap_size: str | None = Field(default=None, description="자본금규모 / 길이 6")
    stac_month: str | None = Field(default=None, description="결산월 / 길이 16")
    market1: str | None = Field(default=None, description="시장조치1 / 길이 16")
    market2: str | None = Field(default=None, description="시장조치2 / 길이 16")
    market3: str | None = Field(default=None, description="시장조치3 / 길이 16")
    market4: str | None = Field(default=None, description="시장조치4 / 길이 16")
    market5: str | None = Field(default=None, description="시장조치5 / 길이 16")
    market6: str | None = Field(default=None, description="시장조치6 / 길이 16")
    cb_text: str | None = Field(default=None, description="CB구분 / 길이 6")
    stck_fcam: int | None = Field(default=None, description="액면가 / 길이 10")
    prdy_clpr_title: str | None = Field(default=None, description="전일종가타이틀 / 길이 12")
    prdy_clpr: int | None = Field(default=None, description="전일종가 / 길이 10")
    stck_sspr: int | None = Field(default=None, description="대용가 / 길이 10")
    gongprice: int | None = Field(default=None, description="공모가 / 길이 10")
    d5_hgpr: int | None = Field(default=None, description="5일고가 / 길이 10")
    d5_lwpr: int | None = Field(default=None, description="5일저가 / 길이 10")
    d20_hgpr: int | None = Field(default=None, description="20일고가 / 길이 10")
    d20_lwpr: int | None = Field(default=None, description="20일저가 / 길이 10")
    w52_hgpr: int | None = Field(default=None, description="52주최고가 / 길이 10")
    w52_lwpr: int | None = Field(default=None, description="52주최저가 / 길이 10")
    move_stcn: int | None = Field(default=None, description="유동주식수 / 길이 12")
    lstn_stcn1: int | None = Field(default=None, description="상장주식수_천주 / 길이 12")
    hts_avls: int | None = Field(default=None, description="시가총액 / 길이 12")
    cntg_hour: str | None = Field(default=None, description="시간 / 길이 5")
    seln_mbcr_no1: str | None = Field(default=None, description="매도거래원1 / 길이 6")
    shnu_mbcr_no1: str | None = Field(default=None, description="매수거래원1 / 길이 6")
    seln_acml_vol1: int | None = Field(default=None, description="매도거래량1 / 길이 12")
    shnu_acml_vol1: int | None = Field(default=None, description="매수거래량1 / 길이 12")
    seln_mbcr_no2: str | None = Field(default=None, description="매도거래원2 / 길이 6")
    shnu_mbcr_no2: str | None = Field(default=None, description="매수거래원2 / 길이 6")
    seln_acml_vol2: int | None = Field(default=None, description="매도거래량2 / 길이 12")
    shnu_acml_vol2: int | None = Field(default=None, description="매수거래량2 / 길이 12")
    seln_mbcr_no3: str | None = Field(default=None, description="매도거래원3 / 길이 6")
    shnu_mbcr_no3: str | None = Field(default=None, description="매수거래원3 / 길이 6")
    seln_acml_vol3: int | None = Field(default=None, description="매도거래량3 / 길이 12")
    shnu_acml_vol3: int | None = Field(default=None, description="매수거래량3 / 길이 12")
    seln_mbcr_no4: str | None = Field(default=None, description="매도거래원4 / 길이 6")
    shnu_mbcr_no4: str | None = Field(default=None, description="매수거래원4 / 길이 6")
    seln_acml_vol4: int | None = Field(default=None, description="매도거래량4 / 길이 12")
    shnu_acml_vol4: int | None = Field(default=None, description="매수거래량4 / 길이 12")
    seln_mbcr_no5: str | None = Field(default=None, description="매도거래원5 / 길이 6")
    shnu_mbcr_no5: str | None = Field(default=None, description="매수거래원5 / 길이 6")
    seln_acml_vol5: int | None = Field(default=None, description="매도거래량5 / 길이 12")
    shnu_acml_vol5: int | None = Field(default=None, description="매수거래량5 / 길이 12")
    seln_frgn_vol: int | None = Field(default=None, description="매도외국인거래량 / 길이 12")
    shnu_frgn_vol: int | None = Field(default=None, description="매수외국인거래량 / 길이 12")
    frgn_hour: str | None = Field(default=None, description="외국인시간 / 길이 6")
    for_rate: float | None = Field(default=None, description="외국인지분율 / 길이 5.2")
    settdate: str | None = Field(default=None, description="결제일 / 길이 4")
    crate: float | None = Field(default=None, description="잔고비율(%) / 길이 5.2")
    yudate: str | None = Field(default=None, description="유상기준일 / 길이 4")
    mudate: str | None = Field(default=None, description="무상기준일 / 길이 4")
    yurate: float | None = Field(default=None, description="유상배정비율 / 길이 5.2")
    murate: float | None = Field(default=None, description="무상배정비율 / 길이 5.2")
    lstn_date: str | None = Field(default=None, description="상장일 / 길이 8")
    lstn_stcn: int | None = Field(default=None, description="상장주식수_주 / 길이 12")
    total_seln_qty: int | None = Field(default=None, description="전체거래원매도합 / 길이 12")
    total_shnu_qty: int | None = Field(default=None, description="전체거래원매수합 / 길이 12")
    new_volume: int | None = Field(default=None, description="신규거래량 / 길이 12")


class KrStockQuoteEtfCurrentTickOutput(BaseModel):
    """ETF/ETN 시간대별 체결 상세 (Output_1 배열의 각 항목).

    스펙은 `cntg_vol` 을 string 으로 선언하지만, 2026-08-22 실측(069500)에서
    실제로는 int 로 내려오는 것을 확인해 `int|str` 로 완화했다.
    """

    model_config = ConfigDict(extra="allow")

    bsop_hour: str | None = Field(default=None, description="호가시간 / 길이 8")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 10")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 10")
    askp: int | None = Field(default=None, description="매도호가 / 길이 10")
    bidp: int | None = Field(default=None, description="매수호가 / 길이 10")
    cntg_vol: int | str | None = Field(default=None, description="변동거래량 / 길이 12")
    acml_vol: int | None = Field(default=None, description="거래량 / 길이 12")


class KrStockQuoteEtfCurrentExpectedOutput(BaseModel):
    """ETF/ETN 예상체결 정보 (Output_2).

    스펙은 6개 필드 모두 string 으로 선언하지만, 2026-08-22 실측(069500)에서
    `antc_cnpr`/`antc_vrss`/`antc_ctrt`/`antc_vol` 이 실제로는 int/float 로
    내려오는 것을 확인해 완화했다(`aspr_cls_code`/`antc_sign` 은 실측에서도
    문자열이라 스펙 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    aspr_cls_code: str | None = Field(default=None, description="동시호가구분 / 길이 1 / 1.동시호가 이외 정규시장")
    antc_cnpr: int | str | None = Field(default=None, description="예상체결가 / 길이 10")
    antc_sign: str | None = Field(
        default=None,
        description="예상체결부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    antc_vrss: int | str | None = Field(default=None, description="예상체결등락폭 / 길이 10")
    antc_ctrt: float | str | None = Field(default=None, description="예상체결등락률 / 길이 5.2")
    antc_vol: int | str | None = Field(default=None, description="예상체결수량 / 길이 12")


class KrStockQuoteEtfCurrentNavOutput(BaseModel):
    """ETF/ETN NAV·괴리율·LP 잔량 상세 (Output_3, 공식 스펙 문서에는 없고 예시 응답에만 존재).

    스펙은 32개 필드 모두 string 으로 선언하지만, 2026-08-22 실측(069500)에서
    아래 27개 필드가 실제로는 int/float 로 내려오는 것을 확인해 완화했다
    (`bu12`/`nav_sign`/`dprt_sign`/`clon_cls_code`/`txtn_type_code` 는 실측에서도
    문자열이라 스펙 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    bu12: str | None = Field(default=None, description="ETF구분 / 길이 1")
    itmt_last_nav: float | str | None = Field(default=None, description="장중/최종NAV / 길이 10.2")
    nav_sign: str | None = Field(
        default=None,
        description="NAV등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    nav_vrss: float | str | None = Field(default=None, description="NAV등락폭 / 길이 10.2")
    prdy_last_nav: float | str | None = Field(default=None, description="전일NAV / 길이 10.2")
    dprt: float | str | None = Field(default=None, description="괴리율 / 길이 10.2")
    dprt_sign: str | None = Field(
        default=None,
        description="괴리율부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    cnfg_cnt: int | str | None = Field(default=None, description="구성종목수 / 길이 10")
    totvalue: int | str | None = Field(default=None, description="순자산총액(억원) / 길이 12")
    trc_errt: float | str | None = Field(default=None, description="추적오차율 / 길이 10.2")
    lp_askp_rsqn1: int | str | None = Field(default=None, description="LP매도호가잔량1 / 길이 12")
    lp_askp_rsqn2: int | str | None = Field(default=None, description="LP매도호가잔량2 / 길이 12")
    lp_askp_rsqn3: int | str | None = Field(default=None, description="LP매도호가잔량3 / 길이 12")
    lp_askp_rsqn4: int | str | None = Field(default=None, description="LP매도호가잔량4 / 길이 12")
    lp_askp_rsqn5: int | str | None = Field(default=None, description="LP매도호가잔량5 / 길이 12")
    lp_askp_rsqn6: int | str | None = Field(default=None, description="LP매도호가잔량6 / 길이 12")
    lp_askp_rsqn7: int | str | None = Field(default=None, description="LP매도호가잔량7 / 길이 12")
    lp_askp_rsqn8: int | str | None = Field(default=None, description="LP매도호가잔량8 / 길이 12")
    lp_askp_rsqn9: int | str | None = Field(default=None, description="LP매도호가잔량9 / 길이 12")
    lp_askp_rsqn10: int | str | None = Field(default=None, description="LP매도호가잔량10 / 길이 12")
    lp_bidp_rsqn1: int | str | None = Field(default=None, description="LP매수호가잔량1 / 길이 12")
    lp_bidp_rsqn2: int | str | None = Field(default=None, description="LP매수호가잔량2 / 길이 12")
    lp_bidp_rsqn3: int | str | None = Field(default=None, description="LP매수호가잔량3 / 길이 12")
    lp_bidp_rsqn4: int | str | None = Field(default=None, description="LP매수호가잔량4 / 길이 12")
    lp_bidp_rsqn5: int | str | None = Field(default=None, description="LP매수호가잔량5 / 길이 12")
    lp_bidp_rsqn6: int | str | None = Field(default=None, description="LP매수호가잔량6 / 길이 12")
    lp_bidp_rsqn7: int | str | None = Field(default=None, description="LP매수호가잔량7 / 길이 12")
    lp_bidp_rsqn8: int | str | None = Field(default=None, description="LP매수호가잔량8 / 길이 12")
    lp_bidp_rsqn9: int | str | None = Field(default=None, description="LP매수호가잔량9 / 길이 12")
    lp_bidp_rsqn10: int | str | None = Field(default=None, description="LP매수호가잔량10 / 길이 12")
    clon_cls_code: str | None = Field(default=None, description="ETF복제방법구분코드 / 길이 12")
    txtn_type_code: str | None = Field(default=None, description="ETF과세유형코드 / 길이 18")


class KrStockQuoteEtfCurrentIndexOutput(BaseModel):
    """ETF/ETN 기초지수 상세 (Output_4, 공식 스펙 문서에는 없고 예시 응답에만 존재).

    스펙은 `prdy_vrss` 를 int(등락폭)로 선언하지만 2026-08-22 실측(069500)에서
    소수부가 있는 float(15.27)로 내려와 `float` 로 정정했다. `prpr_nmix`·
    `ubjisu`·`ubchange`·`ovrs_nmix`·`ovrs_vrss` 는 스펙상 string 이지만 실제로는
    int/float 로 내려와 `int|float|str` 로 완화했다(나머지 필드는 실측에서도
    문자열이라 스펙 그대로 둠).
    """

    model_config = ConfigDict(extra="allow")

    bstp_cls_code: str | None = Field(default=None, description="지수코드 / 길이 6")
    bstp_kor_isnm: str | None = Field(default=None, description="업종명 / 길이 40")
    prpr_nmix: float | str | None = Field(default=None, description="지수 / 길이 10.2")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    prdy_vrss: float | None = Field(
        default=None, description="등락폭 / 길이 10 (스펙은 int 지만 실측은 소수부 있는 float)"
    )
    ubjiid: str | None = Field(default=None, description="채권지수코드 / 길이 6")
    ubjiid2: str | None = Field(default=None, description="채권지수세부코드 / 길이 1")
    ubjisu: int | float | str | None = Field(default=None, description="채권지수 / 길이 10.4")
    ubsign: str | None = Field(
        default=None,
        description="채권등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    ubchange: int | float | str | None = Field(default=None, description="채권등락폭 / 길이 10.4")
    symbol: str | None = Field(default=None, description="해외지수심볼 / 길이 12")
    ovrs_nmix: int | float | str | None = Field(default=None, description="해외지수 / 길이 10.2")
    ovrs_sign: str | None = Field(
        default=None,
        description="해외지수등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    ovrs_vrss: int | float | str | None = Field(default=None, description="해외지수등락폭 / 길이 10.2")
    jisukpgubun: str | None = Field(default=None, description="지수거래소구분 / 길이 1 / 1.코스피 2.코스닥")


class KrStockQuoteEtfCurrent(NHPlugAssetHttpBody):
    """ETF/ETN 현재가 (`POST /krstock/quote/v1/etfCurrent`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `iem_cd` 하나뿐이다(market_cd
    없음). `Output_3`/`Output_4` 는 스펙 문서에는 없고 예시 응답에만 존재한다
    (spec 의 x-schema-warning 이 명시) — 두 블록 모두 필드가 전부 string 으로
    선언돼 있어 그대로 반영했다.
    """

    output_0: KrStockQuoteEtfCurrentOutput | None = Field(
        default=None, alias="Output_0", description="ETF/ETN 현재가 종합 정보"
    )
    output_1: list[KrStockQuoteEtfCurrentTickOutput] | None = Field(
        default=None, alias="Output_1", description="시간대별 체결 상세 목록"
    )
    output_2: KrStockQuoteEtfCurrentExpectedOutput | None = Field(
        default=None, alias="Output_2", description="예상체결 정보"
    )
    output_3: KrStockQuoteEtfCurrentNavOutput | None = Field(
        default=None, alias="Output_3", description="NAV·괴리율·LP 잔량 상세 (스펙 문서 미기재, 예시 응답에만 존재)"
    )
    output_4: KrStockQuoteEtfCurrentIndexOutput | None = Field(
        default=None, alias="Output_4", description="기초지수 상세 (스펙 문서 미기재, 예시 응답에만 존재)"
    )


class KrStockQuoteEtfComponentsOutput(BaseModel):
    """ETF 구성종목시세 상세 (Output_0 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 40")
    stck_prpr: int | None = Field(default=None, description="현재가 / 길이 7")
    prdy_vrss_sign: str | None = Field(
        default=None,
        description="등락부호 / 길이 1 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)",
    )
    prdy_vrss: int | None = Field(default=None, description="등락폭 / 길이 6")
    prdy_ctrt: float | None = Field(default=None, description="등락률 / 길이 6.2")
    cu_unit: float | None = Field(default=None, description="1CU단위증권수(주) / 길이 18.2")
    totprice: int | None = Field(default=None, description="평가금액2 / 길이 12")
    vol: float | None = Field(default=None, description="비중 / 길이 6.2")
    vltn_amt: float | None = Field(default=None, description="평가금액 / 길이 18.0")
    filler: str | None = Field(default=None, description="Filler / 길이 30")


class KrStockQuoteEtfComponents(NHPlugAssetHttpBody):
    """ETF 구성종목시세 (`POST /krstock/quote/v1/etfComponents`) 응답.

    시세 조회 API 라 계좌번호가 필요 없다. 스펙에 `CtsHeader` 파라미터가 없어
    연속조회를 지원하지 않는다(단건 조회). 입력은 `iem_cd` 하나뿐이다(market_cd
    없음). `Output_0` 하나만 있고 배열이다(구성종목 목록).
    """

    output_0: list[KrStockQuoteEtfComponentsOutput] | None = Field(
        default=None, alias="Output_0", description="구성종목 상세 목록"
    )
