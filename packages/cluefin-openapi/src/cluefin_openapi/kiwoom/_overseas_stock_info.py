from typing import Literal

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._model import (
    KiwoomHttpHeader,
    KiwoomHttpResponse,
)
from cluefin_openapi.kiwoom._overseas_stock_info_types import (
    OverseasStockInfoEtfCategoryList,
    OverseasStockInfoEtfEtnList,
    OverseasStockInfoExchangeList,
    OverseasStockInfoGapUpDownEtf,
    OverseasStockInfoGapUpDownStock,
    OverseasStockInfoHighLowApproachEtf,
    OverseasStockInfoHighLowApproachStock,
    OverseasStockInfoHighLowApproachWatchlist,
    OverseasStockInfoIndexList,
    OverseasStockInfoNewHighLowEtf,
    OverseasStockInfoNewHighLowStock,
    OverseasStockInfoPriceByRangeEtf,
    OverseasStockInfoPriceByRangeStock,
    OverseasStockInfoPriceSurgeEtf,
    OverseasStockInfoPriceSurgeStock,
    OverseasStockInfoPriceSurgeWatchlist,
    OverseasStockInfoRemainingRatioSurgeEtf,
    OverseasStockInfoRemainingRatioSurgeStock,
    OverseasStockInfoSectorList,
    OverseasStockInfoStock,
    OverseasStockInfoStockList,
    OverseasStockInfoStockMemo,
    OverseasStockInfoVolumeConcentrationEtf,
    OverseasStockInfoVolumeConcentrationStock,
    OverseasStockInfoVolumeRenewalEtf,
    OverseasStockInfoVolumeRenewalStock,
    OverseasStockInfoVolumeRenewalWatchlist,
    OverseasStockInfoVolumeSurgeEtf,
    OverseasStockInfoVolumeSurgeStock,
    OverseasStockInfoYearlyFluctuationRateByEtfCategory,
    OverseasStockInfoYearlyFluctuationRateBySector,
    OverseasStockInfoYearlyFluctuationRateEtf,
    OverseasStockInfoYearlyFluctuationRateSector,
    OverseasStockInfoYearlyFluctuationRateStock,
)

_PRIC_CND = Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
_TRDE_QTY_TP = Literal["", "0", "10", "15", "20", "30", "50", "100", "300", "500"]
_TRDE_PRICA_CND = Literal["", "0", "1", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"]
_STK_CND = Literal["", "0", "1", "2"]
_STK_TP = Literal["", "0", "1"]
_STEX_TP = Literal["", "0", "1", "2", "3"]


class OverseasStockInfo:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/stkinfo"

    def get_exchange_list(
        self,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoExchangeList]:
        """미국주식 거래소구분 조회 (usa10098)

        Args:
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoExchangeList]: 미국주식 거래소구분 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10098",
        }
        body = {
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching exchange list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoExchangeList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_stock_list(
        self,
        stex_tp: Literal["%", "NA", "ND", "NY"],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoStockList]:
        """미국주식 종목리스트 (usa10099)

        Args:
            stex_tp (Literal["%", "NA", "ND", "NY"]): 거래소구분. %:전체,NA:AMEX,ND:NASDAQ,NY:NYSE
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoStockList]: 미국주식 종목리스트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10099",
        }
        body = {
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoStockList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_stock(
        self,
        stk_cd: str,
        stex_tp: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoStock]:
        """미국주식 종목 조회 (usa10100)

        Args:
            stk_cd (str): 종목코드
            stex_tp (str, optional): 거래소구분. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoStock]: 미국주식 종목 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10100",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_sector_list(
        self,
        gubun: Literal["", "%", "1"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoSectorList]:
        """미국주식 업종리스트 (usa10101)

        Args:
            gubun (Literal["", "%", "1"], optional): 구분. %:전체, 1:미국. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoSectorList]: 미국주식 업종리스트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10101",
        }
        body = {
            "gubun": gubun,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching sector list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoSectorList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_index_list(
        self,
        index_qry_tp: Literal["", "%", "NQ", "NS", "NW"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoIndexList]:
        """미국지수 리스트 (usa10102)

        Args:
            index_qry_tp (Literal["", "%", "NQ", "NS", "NW"], optional): 업종지수구분. %:전체,NQ:나스닥,NS:S&P500,NW:다우. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoIndexList]: 미국지수 리스트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10102",
        }
        body = {
            "index_qry_tp": index_qry_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching index list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoIndexList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_stock_memo(
        self,
        input_list: list[dict[str, str]] | None = None,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoStockMemo]:
        """미국주식 종목메모 조회 (usa10103)

        Args:
            input_list (list[dict[str, str]] | None, optional): 요청종목코드리스트.
                [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoStockMemo]: 미국주식 종목메모 조회 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10103",
        }
        body = {
            "input_list": input_list if input_list is not None else [],
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock memo: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoStockMemo.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_etf_etn_list(
        self,
        stex_tp: Literal["", "%", "NA", "ND", "NY"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoEtfEtnList]:
        """미국 ETF,ETN 리스트 (usa10104)

        Args:
            stex_tp (Literal["", "%", "NA", "ND", "NY"], optional): 거래소구분. %:전체,NA:AMEX,ND:NASDAQ,NY:NYSE. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoEtfEtnList]: 미국 ETF,ETN 리스트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10104",
        }
        body = {
            "stex_tp": stex_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching etf etn list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoEtfEtnList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_etf_category_list(
        self,
        gubun: Literal["", "%", "1", "2"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoEtfCategoryList]:
        """미국 ETF 카테고리 리스트 (usa10105)

        Args:
            gubun (Literal["", "%", "1", "2"], optional): 구분. %:전체,1:카테고리1차,2:카테고리2차. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoEtfCategoryList]: 미국 ETF 카테고리 리스트 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa10105",
        }
        body = {
            "gubun": gubun,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching etf category list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoEtfCategoryList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_surge_stock(
        self,
        stex_tp: _STEX_TP = "",
        inds_cd: str = "",
        tm: str = "",
        stk_tp: _STK_TP = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeSurgeStock]:
        """미국주식 거래량급등락(주식/업종) (usa20520)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            tm (str, optional): x일평균대비. 5일, 10일, 20일, 30일. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeSurgeStock]: 미국주식 거래량급등락(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20520",
        }
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "tm": tm,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_surge_etf(
        self,
        stex_tp: _STEX_TP = "",
        tm: str = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeSurgeEtf]:
        """미국주식 거래량급등락(ETF) (usa20521)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            tm (str, optional): x일평균대비. 5일, 10일, 20일, 30일. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeSurgeEtf]: 미국주식 거래량급등락(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20521",
        }
        body = {
            "stex_tp": stex_tp,
            "tm": tm,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_by_range_stock(
        self,
        stex_tp: _STEX_TP = "",
        stk_tp: _STK_TP = "",
        stk_cnd: _STK_CND = "",
        inds_cd: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd1: str = "",
        pric_cnd2: str = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceByRangeStock]:
        """미국주식 가격대별주가(주식/업종) (usa20570)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체, 1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd1 (str, optional): 가격조건1. 최대 999999.99. Defaults to "".
            pric_cnd2 (str, optional): 가격조건2. 최대 999999.99. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoPriceByRangeStock]: 미국주식 가격대별주가(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20570",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "inds_cd": inds_cd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd1": pric_cnd1,
            "pric_cnd2": pric_cnd2,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price by range stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceByRangeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_by_range_etf(
        self,
        stex_tp: _STEX_TP = "",
        stk_cnd: _STK_CND = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd1: str = "",
        pric_cnd2: str = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceByRangeEtf]:
        """미국주식 가격대별주가(ETF) (usa20571)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd1 (str, optional): 가격조건1. 최대 999999.99. Defaults to "".
            pric_cnd2 (str, optional): 가격조건2. 최대 999999.99. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoPriceByRangeEtf]: 미국주식 가격대별주가(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20571",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cnd": stk_cnd,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd1": pric_cnd1,
            "pric_cnd2": pric_cnd2,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price by range etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceByRangeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_stock(
        self,
        stex_tp: _STEX_TP = "",
        stk_tp: _STK_TP = "",
        inds_cd: str = "",
        stk_cnd: _STK_CND = "",
        flu_tp: Literal["", "1", "2"] = "",
        tm_tp: Literal["", "1", "2", "3"] = "",
        tm: str = "",
        pric_cnd: _PRIC_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeStock]:
        """미국주식 가격급등락(주식/업종) (usa20930)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            flu_tp (Literal["", "1", "2"], optional): 급등.급락 구분. 1:급등,2:급락. Defaults to "".
            tm_tp (Literal["", "1", "2", "3"], optional): 분전, 전일 구분. 1:분전,2:일전,3:지정일. Defaults to "".
            tm (str, optional): 분,일자 설정. XX분전(최대30) or XX일전(최대30) or tm_tp:3 입력 시 기간(1:1일전,2:5일전,3:1개월전,4:3개월전,5:6개월전,6:연중,7:1년전,8:3년전,9:5년전). Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoPriceSurgeStock]: 미국주식 가격급등락(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20930",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_tp": stk_tp,
            "inds_cd": inds_cd,
            "stk_cnd": stk_cnd,
            "flu_tp": flu_tp,
            "tm_tp": tm_tp,
            "tm": tm,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: _STK_CND = "",
        flu_tp: Literal["", "1", "2"] = "",
        tm_tp: Literal["", "1", "2", "3"] = "",
        tm: str = "",
        pric_cnd: _PRIC_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeEtf]:
        """미국주식 가격급등락(ETF) (usa20931)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            flu_tp (Literal["", "1", "2"], optional): 급등.급락 구분. 1:급등,2:급락. Defaults to "".
            tm_tp (Literal["", "1", "2", "3"], optional): 분전, 전일 구분. 1:분전,2:일전,3:지정일. Defaults to "".
            tm (str, optional): 분,일자 설정. XX분전(최대30) or XX일전(최대30) or tm_tp:3 입력 시 기간(1:1일전,2:5일전,3:1개월전,4:3개월전,5:6개월전,6:연중,7:1년전,8:3년전,9:5년전). Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoPriceSurgeEtf]: 미국주식 가격급등락(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20931",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "flu_tp": flu_tp,
            "tm_tp": tm_tp,
            "tm": tm,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_watchlist(
        self,
        stex_tp: _STEX_TP = "",
        stk_cd: list[dict[str, str]] | None = None,
        flu_tp: Literal["", "1", "2"] = "",
        tm_tp: Literal["", "1", "2", "3"] = "",
        tm: str = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeWatchlist]:
        """미국주식 가격급등락(관심종목) (usa20932)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 관심종목. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            flu_tp (Literal["", "1", "2"], optional): 정렬 구분. 1:급등(기본값),2:급락. Defaults to "".
            tm_tp (Literal["", "1", "2", "3"], optional): 기준 구분. 1:분전(기본값),2:일전,3:지정일. Defaults to "".
            tm (str, optional): 분전 값. XX분전(최대30) or XX일전(최대30) or tm_tp:3 입력 시 기간(1:1일전,2:5일전,3:1개월전,4:3개월전,5:6개월전,6:연중,7:1년전,8:3년전,9:5년전). Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoPriceSurgeWatchlist]: 미국주식 가격급등락(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20932",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "flu_tp": flu_tp,
            "tm_tp": tm_tp,
            "tm": tm,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_stock(
        self,
        stex_tp: _STEX_TP = "",
        inds_cd: str = "",
        stk_tp: _STK_TP = "",
        high_low_tp: Literal["", "1", "2"] = "",
        alacc_rt: Literal["", "0.5", "1.0", "1.5", "2.0", "2.5", "3.5"] = "",
        stk_cnd: _STK_CND = "",
        pric_cnd_st: str = "",
        pric_cnd_ed: str = "",
        trde_pric_cnd_st: _TRDE_PRICA_CND = "",
        trde_qty_cnd_fr: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachStock]:
        """미국주식 고가/저가 접근(주식/업종) (usa20970)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            high_low_tp (Literal["", "1", "2"], optional): 고가,저가구분. 1:고가,2:저가. Defaults to "".
            alacc_rt (Literal, optional): 근접률. 0.5:0.5%, 1.0:1.0%, 1.5:1.5%, 2.0:2.0%, 2.5:2.5%, 3.5:3.5%. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd_st (str, optional): 가격조건 시작. USD, 가격조건 끝으로만 조회할 경우 0. Defaults to "".
            pric_cnd_ed (str, optional): 가격조건 끝. USD, 가격조건 시작으로만 조회할 경우 0. Defaults to "".
            trde_pric_cnd_st (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_cnd_fr (Literal, optional): 거래량조건. 0:전체 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoHighLowApproachStock]: 미국주식 고가/저가 접근(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20970",
        }
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "high_low_tp": high_low_tp,
            "alacc_rt": alacc_rt,
            "stk_cnd": stk_cnd,
            "pric_cnd_st": pric_cnd_st,
            "pric_cnd_ed": pric_cnd_ed,
            "trde_pric_cnd_st": trde_pric_cnd_st,
            "trde_qty_cnd_fr": trde_qty_cnd_fr,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        high_low_tp: Literal["", "1", "2"] = "",
        alacc_rt: Literal["", "0.5", "1.0", "1.5", "2.0", "2.5", "3.5"] = "",
        stk_cnd: _STK_CND = "",
        pric_cnd_st: str = "",
        pric_cnd_ed: str = "",
        trde_pric_cnd_st: _TRDE_PRICA_CND = "",
        trde_qty_cnd_fr: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachEtf]:
        """미국주식 고가/저가 접근(ETF) (usa20971)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            high_low_tp (Literal["", "1", "2"], optional): 고가,저가구분. 1:고가,2:저가. Defaults to "".
            alacc_rt (Literal, optional): 근접률. 0.5:0.5%, 1.0:1.0%, 1.5:1.5%, 2.0:2.0%, 2.5:2.5%, 3.5:3.5%. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd_st (str, optional): 가격조건 시작. USD, 가격조건 끝으로만 조회할 경우 0. Defaults to "".
            pric_cnd_ed (str, optional): 가격조건 끝. USD, 가격조건 시작으로만 조회할 경우 0. Defaults to "".
            trde_pric_cnd_st (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_cnd_fr (Literal, optional): 거래량조건. 0:전체 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoHighLowApproachEtf]: 미국주식 고가/저가 접근(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20971",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "high_low_tp": high_low_tp,
            "alacc_rt": alacc_rt,
            "stk_cnd": stk_cnd,
            "pric_cnd_st": pric_cnd_st,
            "pric_cnd_ed": pric_cnd_ed,
            "trde_pric_cnd_st": trde_pric_cnd_st,
            "trde_qty_cnd_fr": trde_qty_cnd_fr,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_watchlist(
        self,
        stex_tp: _STEX_TP = "",
        stk_cd: list[dict[str, str]] | None = None,
        high_low_tp: Literal["", "1", "2"] = "",
        alacc_rt: Literal["", "0.5", "1.0", "1.5", "2.0", "2.5", "3.5"] = "",
        stk_cnd: _STK_CND = "",
        pric_cnd_st: str = "",
        pric_cnd_ed: str = "",
        trde_pric_cnd_st: _TRDE_PRICA_CND = "",
        trde_qty_cnd_fr: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachWatchlist]:
        """미국주식 고가/저가 접근(관심종목) (usa20972)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 관심종목코드. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            high_low_tp (Literal["", "1", "2"], optional): 고가,저가구분. 1:고가,2:저가. Defaults to "".
            alacc_rt (Literal, optional): 근접률. 0.5:0.5%, 1.0:1.0%, 1.5:1.5%, 2.0:2.0%, 2.5:2.5%, 3.5:3.5%. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd_st (str, optional): 가격조건 시작. USD, 가격조건 끝으로만 조회할 경우 0. Defaults to "".
            pric_cnd_ed (str, optional): 가격조건 끝. USD, 가격조건 시작으로만 조회할 경우 0. Defaults to "".
            trde_pric_cnd_st (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_cnd_fr (Literal, optional): 거래량조건. 0:전체 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoHighLowApproachWatchlist]: 미국주식 고가/저가 접근(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa20972",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "high_low_tp": high_low_tp,
            "alacc_rt": alacc_rt,
            "stk_cnd": stk_cnd,
            "pric_cnd_st": pric_cnd_st,
            "pric_cnd_ed": pric_cnd_ed,
            "trde_pric_cnd_st": trde_pric_cnd_st,
            "trde_qty_cnd_fr": trde_qty_cnd_fr,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_stock(
        self,
        stex_tp: _STEX_TP = "",
        stk_cd: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        stk_tp: _STK_TP = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        dt_tp: Literal["", "5", "10", "20", "60", "250"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalStock]:
        """미국주식 거래량갱신(주식/업종) (usa23400)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            stk_cd (str, optional): 업종검색. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            dt_tp (Literal["", "5", "10", "20", "60", "250"], optional): 일자구분. 5:5일,10:10일,20:20일,60:60일,250:250일. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeRenewalStock]: 미국주식 거래량갱신(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa23400",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
            "trde_qty_tp": trde_qty_tp,
            "stk_tp": stk_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "dt_tp": dt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        dt_tp: Literal["", "5", "10", "20", "60", "250"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalEtf]:
        """미국주식 거래량갱신(ETF) (usa23401)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            dt_tp (Literal["", "5", "10", "20", "60", "250"], optional): 일자구분. 5:5일,10:10일,20:20일,60:60일,250:250일. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeRenewalEtf]: 미국주식 거래량갱신(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa23401",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "dt_tp": dt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_watchlist(
        self,
        stex_tp: _STEX_TP = "",
        stk_cd: list[dict[str, str]] | None = None,
        trde_qty_tp: _TRDE_QTY_TP = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        dt_tp: Literal["", "5", "10", "20", "60", "250"] = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalWatchlist]:
        """미국주식 거래량갱신(관심종목) (usa23402)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_cd (list[dict[str, str]] | None, optional): 관심종목. [{'stex_tp':'거래소구분','stk_cd':'종목코드'},...]. Defaults to None.
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            dt_tp (Literal["", "5", "10", "20", "60", "250"], optional): 일자구분. 5:5일,10:10일,20:20일,60:60일,250:250일. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeRenewalWatchlist]: 미국주식 거래량갱신(관심종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa23402",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd if stk_cd is not None else [],
            "trde_qty_tp": trde_qty_tp,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "dt_tp": dt_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_new_high_low_stock(
        self,
        stex_tp: _STEX_TP = "",
        stk_tp: _STK_TP = "",
        inds_cd: str = "",
        stk_cnd: _STK_CND = "",
        ntl_tp: Literal["", "1", "2"] = "",
        high_low_tp: Literal["", "1", "2"] = "",
        dt: str = "",
        pric_cnd: _PRIC_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoNewHighLowStock]:
        """미국주식 신고가/신저가(주식/업종) (usa24100)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체, 1:주식. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            ntl_tp (Literal["", "1", "2"], optional): 신고가신저가구분. 1:신고가, 2:신저가. Defaults to "".
            high_low_tp (Literal["", "1", "2"], optional): 고저기준. 1:고가저가기준,2:종가기준. Defaults to "".
            dt (str, optional): 기간입력. n일 기간(최대250), 일자구분과 동시사용 안됨. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoNewHighLowStock]: 미국주식 신고가/신저가(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24100",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_tp": stk_tp,
            "inds_cd": inds_cd,
            "stk_cnd": stk_cnd,
            "ntl_tp": ntl_tp,
            "high_low_tp": high_low_tp,
            "dt": dt,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching new high low stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoNewHighLowStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_new_high_low_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        stk_cnd: _STK_CND = "",
        ntl_tp: Literal["", "1", "2"] = "",
        high_low_tp: Literal["", "1", "2"] = "",
        dt: str = "",
        pric_cnd: _PRIC_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoNewHighLowEtf]:
        """미국주식 신고가/신저가(ETF) (usa24101)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%,2:증50%. Defaults to "".
            ntl_tp (Literal["", "1", "2"], optional): 신고가신저가구분. 1:신고가, 2:신저가. Defaults to "".
            high_low_tp (Literal["", "1", "2"], optional): 고저기준. 1:고가저가기준,2:종가기준. Defaults to "".
            dt (str, optional): 기간입력. n일 기간(최대250), 일자구분과 동시사용 안됨. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoNewHighLowEtf]: 미국주식 신고가/신저가(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24101",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "stk_cnd": stk_cnd,
            "ntl_tp": ntl_tp,
            "high_low_tp": high_low_tp,
            "dt": dt,
            "pric_cnd": pric_cnd,
            "trde_qty_tp": trde_qty_tp,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching new high low etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoNewHighLowEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_gap_up_down_stock(
        self,
        stex_tp: _STEX_TP = "",
        inds_cd: str = "",
        stk_tp: _STK_TP = "",
        sort_tp: Literal["", "1", "2"] = "",
        updown_tp: Literal["", "1", "2"] = "",
        alacc_rt: str = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoGapUpDownStock]:
        """미국주식 갭상승/갭하락(주식/업종) (usa24140)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            sort_tp (Literal["", "1", "2"], optional): 정렬기준. 1:갭비율, 2:전일대비. Defaults to "".
            updown_tp (Literal["", "1", "2"], optional): 등락구분. 1:갭상승, 2:갭하락. Defaults to "".
            alacc_rt (str, optional): 비율1(근접율). 갭비율 값(3:3%이상,5:5%이상,10:10%이상,50:50%이상,100:100%이상,150:150%이상,200:200%이상). Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증거금100%,2:증거금50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. USD 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoGapUpDownStock]: 미국주식 갭상승/갭하락(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24140",
        }
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "sort_tp": sort_tp,
            "updown_tp": updown_tp,
            "alacc_rt": alacc_rt,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching gap up down stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoGapUpDownStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_gap_up_down_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        sort_tp: Literal["", "1", "2"] = "",
        updown_tp: Literal["", "1", "2"] = "",
        alacc_rt: str = "",
        stk_cnd: _STK_CND = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoGapUpDownEtf]:
        """미국주식 갭상승/갭하락(ETF) (usa24141)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            sort_tp (Literal["", "1", "2"], optional): 정렬기준. 1:갭비율, 2:전일대비. Defaults to "".
            updown_tp (Literal["", "1", "2"], optional): 등락구분. 1:갭상승, 2:갭하락. Defaults to "".
            alacc_rt (str, optional): 비율1(근접율). 갭비율 값(3:3%이상,5:5%이상,10:10%이상,50:50%이상,100:100%이상,150:150%이상,200:200%이상). Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증거금100%,2:증거금50%. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. USD 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoGapUpDownEtf]: 미국주식 갭상승/갭하락(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24141",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "sort_tp": sort_tp,
            "updown_tp": updown_tp,
            "alacc_rt": alacc_rt,
            "stk_cnd": stk_cnd,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
            "trde_qty_tp": trde_qty_tp,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching gap up down etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoGapUpDownEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_remaining_ratio_surge_stock(
        self,
        stex_tp: _STEX_TP = "",
        inds_cd: str = "",
        rt_tp: Literal["", "0", "1"] = "",
        stk_tp: _STK_TP = "",
        tm: str = "",
        stk_cnd: _STK_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeStock]:
        """미국주식 잔량률급증(주식/업종) (usa24210)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            rt_tp (Literal["", "0", "1"], optional): 비율 구분. 0:매수/매도 1:매도/매수. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목 구분. 0:전체,1:주식. Defaults to "".
            tm (str, optional): xxx분전 설정. 0-30분전 설정, 최대 30분. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. USD 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeStock]: 미국주식 잔량률급증(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24210",
        }
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "rt_tp": rt_tp,
            "stk_tp": stk_tp,
            "tm": tm,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching remaining ratio surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoRemainingRatioSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_remaining_ratio_surge_etf(
        self,
        stex_tp: _STEX_TP = "",
        rt_tp: Literal["", "0", "1"] = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        tm: str = "",
        stk_cnd: _STK_CND = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeEtf]:
        """미국주식 잔량률급증(ETF) (usa24211)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소 구분. 0:전체,1:NYSE,2:AMEX,3:NASDAQ. Defaults to "".
            rt_tp (Literal["", "0", "1"], optional): 비율 구분. 0:매수/매도 1:매도/매수. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            tm (str, optional): xxx분전 설정. 0-30분전 설정, 최대 30분. Defaults to "".
            stk_cnd (Literal["", "0", "1", "2"], optional): 종목조건. 0:전체,1:증100%만보기,2:증50%만보기. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. USD 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeEtf]: 미국주식 잔량률급증(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24211",
        }
        body = {
            "stex_tp": stex_tp,
            "rt_tp": rt_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "tm": tm,
            "stk_cnd": stk_cnd,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching remaining ratio surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoRemainingRatioSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_concentration_stock(
        self,
        stex_tp: _STEX_TP = "",
        inds_cd: str = "",
        stk_tp: _STK_TP = "",
        dt: str = "",
        prps_cnctr_rt: str = "",
        cond: Literal["", "0", "1", "2", "3"] = "",
        prpscnt: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationStock]:
        """미국주식 매물대집중(주식/업종) (usa24220)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 API 참고, stk_tp(종목구분) 1일 경우. Defaults to "".
            stk_tp (Literal["", "0", "1"], optional): 종목구분. 0:전체,1:주식. Defaults to "".
            dt (str, optional): 기간. n일, 최대 300일. Defaults to "".
            prps_cnctr_rt (str, optional): 매물대 집중비율. n%, 최대 100%. Defaults to "".
            cond (Literal["", "0", "1", "2", "3"], optional): 조건. 0:전체,1:현재가 매물대 진입,2:현재가 매물대 위,3:현재가 매물대 아래. Defaults to "".
            prpscnt (str, optional): 매물대수. n 매물대수, 최대 99. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationStock]: 미국주식 매물대집중(주식/업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24220",
        }
        body = {
            "stex_tp": stex_tp,
            "inds_cd": inds_cd,
            "stk_tp": stk_tp,
            "dt": dt,
            "prps_cnctr_rt": prps_cnctr_rt,
            "cond": cond,
            "prpscnt": prpscnt,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume concentration stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeConcentrationStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_concentration_etf(
        self,
        stex_tp: _STEX_TP = "",
        etf_cat1: str = "",
        etf_cat2: str = "",
        dt: str = "",
        prps_cnctr_rt: str = "",
        cond: Literal["", "0", "1", "2", "3"] = "",
        prpscnt: str = "",
        trde_qty_tp: _TRDE_QTY_TP = "",
        pric_cnd: _PRIC_CND = "",
        trde_prica_cnd: _TRDE_PRICA_CND = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationEtf]:
        """미국주식 매물대집중(ETF) (usa24221)

        Args:
            stex_tp (Literal["", "0", "1", "2", "3"], optional): 거래소구분. 0:전체,1:NYSE,2:NASDAQ,3:AMEX. Defaults to "".
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            dt (str, optional): 기간. n일, 최대 300일. Defaults to "".
            prps_cnctr_rt (str, optional): 매물대 집중비율. n%, 최대 100%. Defaults to "".
            cond (Literal["", "0", "1", "2", "3"], optional): 조건. 0:전체,1:현재가 매물대 진입,2:현재가 매물대 위,3:현재가 매물대 아래. Defaults to "".
            prpscnt (str, optional): 매물대수. n 매물대수, 최대 99. Defaults to "".
            trde_qty_tp (Literal, optional): 거래량조건. 0:전체, 10,15,20,30,50,100,300,500(1만단위) 이상. Defaults to "".
            pric_cnd (Literal, optional): 가격조건. 0:전체,1:5미만,2:10미만,3:10이상,4:10~20,5:20~50,6:50이상,7:50~100,8:100미만,9:100이상,10:500이상. Defaults to "".
            trde_prica_cnd (Literal, optional): 거래대금조건. 0:전체 1,3,5,10,30,50,100,300,500,1000,3000,5000(USD, 1만단위) 이상. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationEtf]: 미국주식 매물대집중(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa24221",
        }
        body = {
            "stex_tp": stex_tp,
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "dt": dt,
            "prps_cnctr_rt": prps_cnctr_rt,
            "cond": cond,
            "prpscnt": prpscnt,
            "trde_qty_tp": trde_qty_tp,
            "pric_cnd": pric_cnd,
            "trde_prica_cnd": trde_prica_cnd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume concentration etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeConcentrationEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_stock(
        self,
        stex_tp: str,
        stk_cd: str,
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateStock]:
        """미국주식 연도별 등락률(종목) (usa26410)

        Args:
            stex_tp (str): 거래소구분
            stk_cd (str): 종목코드
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateStock]: 미국주식 연도별 등락률(종목) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa26410",
        }
        body = {
            "stex_tp": stex_tp,
            "stk_cd": stk_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_by_sector(
        self,
        inds_cd: str = "",
        srch_yr: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateBySector]:
        """미국주식 연도별 업종별 종목등락률 (usa26411)

        Args:
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 참고. Defaults to "".
            srch_yr (str, optional): 조회연도. YYYY. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateBySector]: 미국주식 연도별 업종별 종목등락률 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa26411",
        }
        body = {
            "inds_cd": inds_cd,
            "srch_yr": srch_yr,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate by sector: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateBySector.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_by_etf_category(
        self,
        etf_cat1: str = "",
        etf_cat2: str = "",
        srch_yr: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateByEtfCategory]:
        """미국주식 연도별 ETF 카테고리별 종목등락률 (usa26412)

        Args:
            etf_cat1 (str, optional): ETF카테고리코드1. stk_tp(종목구분) 2일 경우 ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. stk_tp(종목구분) 2일 경우 ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            srch_yr (str, optional): 조회연도. YYYY. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateByEtfCategory]: 미국주식 연도별 ETF 카테고리별 종목등락률 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa26412",
        }
        body = {
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
            "srch_yr": srch_yr,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate by etf category: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateByEtfCategory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_sector(
        self,
        inds_cd: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateSector]:
        """미국주식 연도별 등락률(업종) (usa26413)

        Args:
            inds_cd (str, optional): 업종코드. 000:전체, usa10101 참고. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateSector]: 미국주식 연도별 등락률(업종) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa26413",
        }
        body = {
            "inds_cd": inds_cd,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate sector: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateSector.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_etf(
        self,
        etf_cat1: str = "",
        etf_cat2: str = "",
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateEtf]:
        """미국주식 연도별 등락률(ETF) (usa26414)

        Args:
            etf_cat1 (str, optional): ETF카테고리코드1. ETF 대카테고리코드, usa10105 cate1 속성 참고. Defaults to "".
            etf_cat2 (str, optional): ETF카테고리코드2. ETF 중카테고리코드, usa10105 cate2 속성 참고. Defaults to "".
            cont_yn (Literal["Y", "N"], optional): 연속조회 여부. Defaults to "N".
            next_key (str, optional): 다음키. Defaults to "".

        Returns:
            KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateEtf]: 미국주식 연도별 등락률(ETF) 응답
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.token}",
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "usa26414",
        }
        body = {
            "etf_cat1": etf_cat1,
            "etf_cat2": etf_cat2,
        }

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
