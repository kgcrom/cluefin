from typing import Literal

from cluefin_openapi.kiwoom._domestic_stock_info_types import (
    DomesticStockInfoBasic,
    DomesticStockInfoBasicV1,
    DomesticStockInfoChangeRateFromOpen,
    DomesticStockInfoDailyPreviousDayConclusion,
    DomesticStockInfoDailyPreviousDayExecutionVolume,
    DomesticStockInfoDailyTradingDetails,
    DomesticStockInfoDailyTradingItemsByInvestor,
    DomesticStockInfoExecution,
    DomesticStockInfoHighLowPriceApproach,
    DomesticStockInfoHighPer,
    DomesticStockInfoIndustryCode,
    DomesticStockInfoInstitutionalInvestorByStock,
    DomesticStockInfoInterestStockInfo,
    DomesticStockInfoMarginTradingTrend,
    DomesticStockInfoMemberCompany,
    DomesticStockInfoNewHighLowPrice,
    DomesticStockInfoPriceVolatility,
    DomesticStockInfoProgramTradingStatusByStock,
    DomesticStockInfoSummary,
    DomesticStockInfoSupplyDemandConcentration,
    DomesticStockInfoTop50ProgramNetBuy,
    DomesticStockInfoTotalInstitutionalInvestorByStock,
    DomesticStockInfoTradingMember,
    DomesticStockInfoTradingMemberInstantVolume,
    DomesticStockInfoTradingMemberSupplyDemandAnalysis,
    DomesticStockInfoTradingVolumeRenewal,
    DomesticStockInfoUpperLowerLimitPrice,
    DomesticStockInfoVolatilityControlEvent,
)
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)


class DomesticStockInfo:
    def __init__(self, client):
        self.client = client
        self.path = "/api/dostk/stkinfo"

    def get_stock_info(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoBasic]:
        """
        주식기본정보 요청

        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)

        Returns:
            KiwoomHttpResponse[DomesticStockInfoBasic]: 주식 기본 정보
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10001",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock basic info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoBasic.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_trading_member(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoTradingMember]:
        """
        주식거래원요청

        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTradingMember]: 주식 거래원 정보
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10002",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock trading member: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTradingMember.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_execution(
        self, stk_cd: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoExecution]:
        """체결정보요청
        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoExecution]: 체결 정보 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10003",
        }
        body = {"stk_cd": stk_cd}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching execution info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoExecution.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_margin_trading_trend(
        self, stk_cd: str, dt: str, qry_tp: Literal["1", "2"], cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoMarginTradingTrend]:
        """신용매매동향요청

        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            dt (str): 일자 (YYYYMMDD)
            qry_tp (Literal["1", "2"]): 조회구분 (1:융자, 2:대주)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoMarginTradingTrend]: 신용 매매 동향 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10013",
        }
        body = {"stk_cd": stk_cd, "dt": dt, "qry_tp": qry_tp}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching margin trading trend: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoMarginTradingTrend.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_trading_details(
        self, stk_cd: str, strt_dt: str, cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoDailyTradingDetails]:
        """일별거래상세요청

        Args:
            stk_cd (str): 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoDailyTradingDetails]: 일별 거래 상세 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10015",
        }
        body = {"stk_cd": stk_cd, "strt_dt": strt_dt}

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily trading details: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoDailyTradingDetails.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_new_high_low_price(
        self,
        mrkt_tp: str,
        ntl_tp: str,
        high_low_close_tp: str,
        stk_cnd: str,
        trde_qty_tp: str,
        crd_cnd: str,
        updown_incls: str,
        dt: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoNewHighLowPrice]:
        """신고저가요청

        Args:
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            ntl_tp (str): 신고저구분 (1:신고가, 2:신저가)
            high_low_close_tp (str): 고저종구분 (1:고저기준, 2:종가기준)
            stk_cnd (str): 종목조건 (0:전체조회, 1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기)
            trde_qty_tp (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            crd_cnd (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            updown_incls (str): 상하한포함 (0:미포함, 1:포함)
            dt (str): 기간 (5:5일, 10:10일, 20:20일, 60:60일, 250:250일)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoNewHighLowPrice]: 신고 저가 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10016",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "ntl_tp": ntl_tp,
            "high_low_close_tp": high_low_close_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "crd_cnd": crd_cnd,
            "updown_incls": updown_incls,
            "dt": dt,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching new high low price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoNewHighLowPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_upper_lower_limit_price(
        self,
        mrkt_tp: str,
        updown_tp: str,
        sort_tp: str,
        stk_cnd: str,
        trde_qty_tp: str,
        crd_cnd: str,
        trde_gold_tp: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoUpperLowerLimitPrice]:
        """상하한가요청

        Args:
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            updown_tp (str): 상하한구분 (1:상한, 2:상승, 3:보합, 4:하한, 5:하락, 6:전일상한, 7:전일하한)
            sort_tp (str): 정렬구분 (1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순)
            stk_cnd (str): 종목조건 (0:전체조회, 1:관리종목제외, 3:우선주제외, 4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기, 9:증20만 보기, 10:우선주+관리종목+환기종목제외)
            trde_qty_tp (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            crd_cnd (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            trde_gold_tp (str): 매매금구분 (0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT 3.통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoUpperLowerLimitPrice]: 상하한가 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10017",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "updown_tp": updown_tp,
            "sort_tp": sort_tp,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "crd_cnd": crd_cnd,
            "trde_gold_tp": trde_gold_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching upper lower limit price: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoUpperLowerLimitPrice.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_high_low_price_approach(
        self,
        high_low_tp: str,
        alacc_rt: str,
        mrkt_tp: str,
        trde_qty_tp: str,
        stk_cnd: str,
        crd_cnd: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoHighLowPriceApproach]:
        """고저가접근요청

        Args:
            high_low_tp (str): 고저구분 (1:고가, 2:저가)
            alacc_rt (str): 근접율 (05:0.5, 10:1.0, 15:1.5, 20:2.0, 25:2.5, 30:3.0)
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            trde_qty_tp (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            stk_cnd (str): 종목조건 (0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기)
            crd_cnd (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoHighLowPriceApproach]: 고저가 접근 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10018",
        }

        body = {
            "high_low_tp": high_low_tp,
            "alacc_rt": alacc_rt,
            "mrkt_tp": mrkt_tp,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching high low price approach: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoHighLowPriceApproach.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_price_volatility(
        self,
        mrkt_tp: str,
        flu_tp: str,
        tm_tp: str,
        tm: str,
        trde_qty_tp: str,
        stk_cnd: str,
        crd_cnd: str,
        pric_cnd: str,
        updown_incls: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoPriceVolatility]:
        """가격급등락요청

        Args:
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥, 201:코스피200)
            flu_tp (str): 등락구분 (1:급등, 2:급락)
            tm_tp (str): 시간구분 (1:분전, 2:일전)
            tm (str): 시간 (분 혹은 일 입력)
            trde_qty_tp (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            stk_cnd (str): 종목조건 (0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기)
            crd_cnd (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            pric_cnd (str): 가격조건 (0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상)
            updown_incls (str): 상하한포함 (0:미포함, 1:포함)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoPriceVolatility]: 가격 급등락 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10019",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "flu_tp": flu_tp,
            "tm_tp": tm_tp,
            "tm": tm,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "pric_cnd": pric_cnd,
            "updown_incls": updown_incls,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching price volatility: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoPriceVolatility.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_trading_volume_renewal(
        self,
        mrkt_tp: str,
        cycle_tp: str,
        trde_qty_tp: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoTradingVolumeRenewal]:
        """거래량갱신요청

        Args:
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            cycle_tp (str): 주기구분 (5:5일, 10:10일, 20:20일, 60:60일, 250:250일)
            trde_qty_tp (str): 거래량구분 (5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTradingVolumeRenewal]: 거래량 갱신 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10024",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "cycle_tp": cycle_tp,
            "trde_qty_tp": trde_qty_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching trading volume renewal: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTradingVolumeRenewal.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_supply_demand_concentration(
        self,
        mrkt_tp: str,
        prps_cnctr_rt: str,
        cur_prc_entry: str,
        prpscnt: str,
        cycle_tp: str,
        stex_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoSupplyDemandConcentration]:
        """매물대집중요청

        Args:
            mrkt_tp (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            prps_cnctr_rt (str): 매물집중비율 (0~100 입력)
            cur_prc_entry (str): 현재가진입 (0:현재가 매물대 진입 포함안함, 1:현재가 매물대 진입포함)
            prpscnt (str): 매물대수 (숫자입력)
            cycle_tp (str): 주기구분 (50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoSupplyDemandConcentration]: 매물대 집중 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10025",
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "prps_cnctr_rt": prps_cnctr_rt,
            "cur_prc_entry": cur_prc_entry,
            "prpscnt": prpscnt,
            "cycle_tp": cycle_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching supply demand concentration: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoSupplyDemandConcentration.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_high_per(
        self,
        pertp: Literal["1", "2", "3", "4", "5", "6"],
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoHighPer]:
        """고저PER요청

        Args:
            pertp (Literal["1", "2", "3", "4", "5", "6"]): PER구분 (1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE)
            stex_tp (Literal["1", "2", "3"]): 거래소구분 (1:KRX, 2:NXT 3.통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoHighPer]: 고PER 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10026",
        }

        body = {
            "pertp": pertp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching high PER: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoHighPer.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_change_rate_from_open(
        self,
        sort_tp: Literal["1", "2", "3", "4"],
        trde_qty_cnd: Literal["0000", "0010", "0050", "0100", "0500", "1000"],
        mrkt_tp: Literal["000", "001", "101"],
        updown_incls: Literal["0", "1"],
        stk_cnd: Literal["0", "1", "4", "3", "5", "6", "7", "8", "9"],
        crd_cnd: Literal["0", "1", "2", "3", "4", "9"],
        trde_prica_cnd: Literal["0", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"],
        flu_cnd: Literal["1", "2"],
        stex_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoChangeRateFromOpen]:
        """시가대비등락률요청

        Args:
            sort_tp (Literal["1", "2", "3", "4"]): 정렬구분 (1:시가, 2:고가, 3:저가, 4:기준가)
            trde_qty_cnd (Literal["0000", "0010", "0050", "0100", "0500", "1000"]): 거래량조건 (0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0500:50만주이상, 1000:백만주이상)
            mrkt_tp (Literal["000", "001", "101"]): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            updown_incls (Literal["0", "1"]): 상하한포함 (0:불 포함, 1:포함)
            stk_cnd (Literal["0", "1", "4", "3", "5", "6", "7", "8", "9"]): 종목조건 (0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기)
            crd_cnd (Literal["0", "1", "2", "3", "4", "9"]): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            trde_prica_cnd (Literal["0", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"]): 거래대금조건 (0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상)
            flu_cnd (Literal["1", "2"]): 등락조건 (1:상위, 2:하위)
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoChangeRateFromOpen]: 시가 대비 등락률 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10028",
        }

        body = {
            "sort_tp": sort_tp,
            "trde_qty_cnd": trde_qty_cnd,
            "mrkt_tp": mrkt_tp,
            "updown_incls": updown_incls,
            "stk_cnd": stk_cnd,
            "crd_cnd": crd_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "flu_cnd": flu_cnd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching change rate from open: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoChangeRateFromOpen.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_trading_member_supply_demand_analysis(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        qry_dt_tp: Literal["0", "1"],
        pot_tp: Literal["0", "1"],
        dt: Literal["5", "10", "20", "40", "60", "120"],
        sort_base: Literal["1", "2"],
        mmcm_cd: str,
        stex_tp: Literal["1", "2", "3"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoTradingMemberSupplyDemandAnalysis]:
        """거래원매물대분석요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD)
            end_dt (str): 종료일자 (YYYYMMDD)
            qry_dt_tp (str): 조회기간구분 (0:기간으로 조회, 1:시작일자, 종료일자로 조회)
            pot_tp (str): 시점구분 (0:당일, 1:전일)
            dt (str): 기간 (5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일)
            sort_base (str): 정렬기준 (1:종가순, 2:날짜순)
            mmcm_cd (str): 회원사코드, 회원사코드는 ka10102 API를 통해 조회 가능(get_member_list)
            stex_tp (str): 거래소구분 (1:KRX, 2:NXT 3.통합)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTradingMemberSupplyDemandAnalysis]: 거래원 매물대 분석 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10043",
        }

        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "qry_dt_tp": qry_dt_tp,
            "pot_tp": pot_tp,
            "dt": dt,
            "sort_base": sort_base,
            "mmcm_cd": mmcm_cd,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching trading member supply demand analysis: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTradingMemberSupplyDemandAnalysis.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_trading_member_instant_volume(
        self,
        stk_cd: str,
        mmcm_cd: str,
        mrkt_tp: Literal["0", "1", "2", "3"],
        qty_tp: Literal["0", "1", "2", "3", "5", "10", "30", "50", "100"],
        pric_tp: Literal["0", "1", "8", "2", "3", "4", "5"],
        stex_tp: Literal["1", "2"],
    ) -> KiwoomHttpResponse[DomesticStockInfoTradingMemberInstantVolume]:
        """거래원순간거래량요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            mmcm_cd (str): 회원사코드 (3자리)
            mrkt_tp (Literal["0", "1", "2", "3"]): 시장구분 (1:코스피, 2:코스닥, 3:종목). Defaults to "0".
            qty_tp (Literal["0", "1", "2", "3", "5", "10", "30", "50", "100"]): 수량구분 (0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30:30000주, 50:50000주, 100:100000주). Defaults to "0".
            pric_tp (Literal["0", "1", "8", "2", "3", "4", "5"]): 가격구분 (0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원 ~ 2천원, 3:2천원 ~ 5천원, 4:5천원 ~ 1만원, 5:1만원 이상). Defaults to "0".
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT). Defaults to "1".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTradingMemberInstantVolume]: 거래원 순간 거래량 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10052",
        }

        body = {
            "stk_cd": stk_cd,
            "mmcm_cd": mmcm_cd,
            "mrkt_tp": mrkt_tp,
            "qty_tp": qty_tp,
            "pric_tp": pric_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching trading member instant volume: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTradingMemberInstantVolume.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_volatility_control_event(
        self,
        mrkt_tp: Literal["000", "001", "101"],
        bf_mkrt_tp: Literal["0", "1", "2"],
        motn_tp: Literal["0", "1", "2", "3"],
        skip_stk: str,
        trde_qty_tp: Literal["0", "1"],
        trde_prica_tp: Literal["0", "1"],
        motn_drc: Literal["0", "1", "2"],
        stex_tp: Literal["1", "2"],
        min_trde_qty: str = "",
        max_trde_qty: str = "",
        min_trde_prica: str = "",
        max_trde_prica: str = "",
        stk_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoVolatilityControlEvent]:
        """변동성완화장치발동목록요청

        Args:
            mrkt_tp (str): 시장구분 (3자리, 000:전체, 001:코스피, 101:코스닥)
            bf_mkrt_tp (str): 장전구분 (1자리, 0:전체, 1:정규시장, 2:시간외단일가)
            motn_tp (str): 발동구분 (1자리, 0:전체, 1:정적VI, 2:동적VI, 3:동적VI + 정적VI)
            skip_stk (str): 제외종목 (9자리, 전종목포함 조회시 9개 0으로 설정(000000000),전종목제외 조회시 9개 1으로 설정(111111111),9개 종목조회여부를 조회포함(0), 조회제외(1)로 설정하며 종목순서는 우선주,관리종목,투자경고/위험,투자주의,환기종목,단기과열종목,증거금100%,ETF,ETN가 됨.우선주만 조회시"011111111"", 관리종목만 조회시 ""101111111"" 설정).
            trde_qty_tp (Literal["0", "1"]): 거래량구분 (0:사용안함, 1:사용)
            trde_price_tp (Literal["0", "1"]): 거래대금구분 (0:사용안함, 1:사용)
            motn_drc (Literal["0", "1", "2"]): 발동방향 (0:전체, 1:상승, 2:하락)
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT 3.통합)
            min_trde_qty (str): 최소거래량 (12자리, 0 주 이상, 거래량구분이 1일때만 입력(공백허용))
            max_trde_qty (str): 최대거래량 (12자리, 100000000 주 이하, 거래량구분이 1일때만 입력(공백허용))
            min_trde_prica (str): 최소거래대금 (10자리, 0 백만원 이상, 거래대금구분 1일때만 입력(공백허용))
            max_trde_prica (str): 최대거래대금 (10자리, 100000000 백만원 이하, 거래대금구분 1일때만 입력(공백허용))
            stk_cd (str, optional): 종목코드 (20자리, 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 공백입력시 시장구분으로 설정한 전체종목조회)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoVolatilityControlEvent]: 변동성완화장치 발동 목록 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "api-id": "ka10054",
            "con-yn": cont_yn,
            "next-key": next_key,
        }

        body = {
            "mrkt_tp": mrkt_tp,
            "bf_mkrt_tp": bf_mkrt_tp,
            "stk_cd": stk_cd,
            "motn_tp": motn_tp,
            "skip_stk": skip_stk,
            "trde_qty_tp": trde_qty_tp,
            "min_trde_qty": min_trde_qty,
            "max_trde_qty": max_trde_qty,
            "trde_prica_tp": trde_prica_tp,
            "min_trde_prica": min_trde_prica,
            "max_trde_prica": max_trde_prica,
            "motn_drc": motn_drc,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching volatility control event list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoVolatilityControlEvent.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_previous_day_execution_volume(
        self, stk_cd: str, tdy_pred: Literal["1", "2"], cont_yn: Literal["Y", "N"] = "N", next_key: str = ""
    ) -> KiwoomHttpResponse[DomesticStockInfoDailyPreviousDayExecutionVolume]:
        """당일전일체결량요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tdy_pred (Literal["1", "2"]): 당일전일 (1:당일, 2:전일)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoDailyPreviousDayExecutionVolume]: 당일 전일 체결량 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10055",
        }

        body = {
            "tdy_pred": tdy_pred,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily previous day execution volume: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoDailyPreviousDayExecutionVolume.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_trading_items_by_investor(
        self,
        strt_dt: str,
        end_dt: str,
        trde_tp: Literal["1", "2"],
        mrkt_tp: Literal["001", "101"],
        invsr_tp: Literal["8000", "9000", "1000", "3000", "5000", "4000", "2000", "6000", "7000", "7100", "9999"],
        stex_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoDailyTradingItemsByInvestor]:
        """투자자별일별매매종목요청

        Args:
            strt_dt (str): 시작일자 (YYYYMMDD)
            end_dt (str): 종료일자 (YYYYMMDD)
            trde_tp (Literal["1", "2"]): 매매구분 (1:순매도, 2:순매수)
            mrkt_tp (Literal["001", "101"]): 시장구분 (001:코스피, 101:코스닥)
            invsr_tp (str): 투자자구분 (8000:개인, 9000:외국인, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계)
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoDailyTradingItemsByInvestor]: 투자자별 일별 매매 종목 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10058",
        }

        body = {
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "trde_tp": trde_tp,
            "mrkt_tp": mrkt_tp,
            "invsr_tp": invsr_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching daily trading items by investor: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoDailyTradingItemsByInvestor.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_institutional_investor_by_stock(
        self,
        dt: str,
        stk_cd: str,
        amt_qty_tp: Literal["1", "2"],
        trde_tp: Literal["0", "1", "2"],
        unit_tp: Literal["1000", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoInstitutionalInvestorByStock]:
        """종목별투자자기관별요청

        Args:
            dt (str): 일자 (YYYYMMDD)
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분 (1:금액, 2:수량)
            trde_tp (Literal["0", "1", "2"]): 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_tp (Literal["1000", "1"]): 단위구분 (1000:천주, 1:단주)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoInstitutionalInvestorByStock]: 종목별 투자자 기관 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10059",
        }

        body = {
            "dt": dt,
            "stk_cd": stk_cd,
            "amt_qty_tp": amt_qty_tp,
            "trde_tp": trde_tp,
            "unit_tp": unit_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching institutional investor by stock: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoInstitutionalInvestorByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_total_institutional_investor_by_stock(
        self,
        stk_cd: str,
        strt_dt: str,
        end_dt: str,
        amt_qty_tp: Literal["1", "2"],
        trde_tp: Literal["0", "1", "2"],
        unit_tp: Literal["1000", "1"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoTotalInstitutionalInvestorByStock]:
        """종목별투자자기관합계요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt (str): 시작일자 (YYYYMMDD)
            end_dt (str): 종료일자 (YYYYMMDD)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분 (1:금액, 2:수량)
            trde_tp (Literal["0", "1", "2"]): 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_tp (Literal["1000", "1"]): 단위구분 (1000:천주, 1:단주)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTotalInstitutionalInvestorByStock]: 종목별 투자자 기관 합계 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10061",
        }

        body = {
            "stk_cd": stk_cd,
            "strt_dt": strt_dt,
            "end_dt": end_dt,
            "amt_qty_tp": amt_qty_tp,
            "trde_tp": trde_tp,
            "unit_tp": unit_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching total institutional investor by stock: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTotalInstitutionalInvestorByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_daily_previous_day_conclusion(
        self,
        stk_cd: str,
        tdy_pred: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoDailyPreviousDayConclusion]:
        """당일전일체결요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tdy_pred (Literal["1", "2"]): 당일전일 (1:당일, 2:전일)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoDailyPreviousDayConclusion]: 당일 전일 체결 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10084",
        }

        body = {
            "stk_cd": stk_cd,
            "tdy_pred": tdy_pred,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching daily previous day conclusion: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoDailyPreviousDayConclusion.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_interest_stock_info(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoInterestStockInfo]:
        """관심종목정보요청

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 여러개의 종목코드 입력시 | 로 구분
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoInterestStockInfo]: 관심 종목 정보 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10095",
        }

        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching interest stock info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoInterestStockInfo.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_info_summary(
        self,
        mrkt_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoSummary]:
        """종목정보 리스트

        Args:
            mrkt_tp (str): 시장구분 (2자리, 0:코스피, 10:코스닥, 3:ELW, 8:ETF, 30:K-OTC, 50:코넥스, 5:신주인수권, 4:뮤추얼펀드, 6:리츠, 9:하이일드)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoSummary]: 종목 정보 요약 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10099",
        }

        body = {
            "mrkt_tp": mrkt_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching stock info list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoSummary.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_stock_info_v1(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoBasicV1]:
        """종목정보 조회

        Args:
            stk_cd (str): 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoBasicV1]: 종목 정보 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10100",
        }

        body = {
            "stk_cd": stk_cd,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching stock info: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoBasicV1.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_industry_code(
        self,
        mrkt_tp: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoIndustryCode]:
        """업종코드 리스트

        Args:
            mrkt_tp (str): 시장구분 (1자리, 0:코스피(거래소), 1:코스닥, 2:KOSPI200, 4:KOSPI100, 7:KRX100(통합지수))
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoIndustryCode]: 업종 코드 리스트 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10101",
        }

        body = {
            "mrkt_tp": mrkt_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching industry code list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoIndustryCode.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_member_company(
        self,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoMemberCompany]:
        """회원사 리스트 요청

        Args:
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoMemberCompany]: 회원사 리스트 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10102",
        }

        body = {}
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching member company list: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoMemberCompany.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_top_50_program_net_buy(
        self,
        trde_upper_tp: Literal["1", "2"],
        amt_qty_tp: Literal["1", "2"],
        mrkt_tp: str,
        stex_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoTop50ProgramNetBuy]:
        """프로그램순매수상위50요청

        Args:
            trde_upper_tp (Literal["1", "2"]): 매매상위구분 (1:순매도상위, 2:순매수상위)
            amt_qty_tp (Literal["1", "2"]): 금액수량구분 (1:금액, 2:수량)
            mrkt_tp (str): 시장구분 (10자리, P00101:코스피, P10102:코스닥)
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT 3.통합). Defaults to "1".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoTop50ProgramNetBuy]: 프로그램 순매수 상위 50 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90003",
        }

        body = {
            "trde_upper_tp": trde_upper_tp,
            "amt_qty_tp": amt_qty_tp,
            "mrkt_tp": mrkt_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching top 50 program net buy: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoTop50ProgramNetBuy.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)

    def get_program_trading_status_by_stock(
        self,
        dt: str,
        mrkt_tp: str,
        stex_tp: Literal["1", "2"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[DomesticStockInfoProgramTradingStatusByStock]:
        """종목별프로그램매매현황요청

        Args:
            dt (str): 일자 (YYYYMMDD)
            mrkt_tp (str): 시장구분 (10자리, P00101:코스피, P10102:코스닥)
            stex_tp (Literal["1", "2"]): 거래소구분 (1:KRX, 2:NXT 3.통합). Defaults to "1".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[DomesticStockInfoProgramTradingStatusByStock]: 종목별 프로그램 매매 현황 응답
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka90004",
        }

        body = {
            "dt": dt,
            "mrkt_tp": mrkt_tp,
            "stex_tp": stex_tp,
        }
        response = self.client._post(self.path, headers, body)

        if response.status_code != 200:
            raise Exception(f"Error fetching program trading status by stock: {response.text}")
        headers = KiwoomHttpHeader.model_validate(response.headers)
        body = DomesticStockInfoProgramTradingStatusByStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=headers, body=body)
