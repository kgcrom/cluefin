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


class OverseasStockInfo:
    def __init__(self, client: Client):
        self.client = client
        self.path = "/api/us/stkinfo"

    def get_exchange_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoExchangeList]:
        """미국주식 거래소구분 조회 (usa10098)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching exchange list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoExchangeList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_stock_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoStockList]:
        """미국주식 종목리스트 (usa10099)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoStockList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoStock]:
        """미국주식 종목 조회 (usa10100)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_sector_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoSectorList]:
        """미국주식 업종리스트 (usa10101)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching sector list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoSectorList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_index_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoIndexList]:
        """미국지수 리스트 (usa10102)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching index list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoIndexList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_etf_etn_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoEtfEtnList]:
        """미국 ETF,ETN 리스트 (usa10104)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching etf etn list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoEtfEtnList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_etf_category_list(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoEtfCategoryList]:
        """미국 ETF 카테고리 리스트 (usa10105)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching etf category list: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoEtfCategoryList.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_surge_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeSurgeStock]:
        """미국주식 거래량급등락(주식/업종) (usa20520)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_surge_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeSurgeEtf]:
        """미국주식 거래량급등락(ETF) (usa20521)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_by_range_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceByRangeStock]:
        """미국주식 가격대별주가(주식/업종) (usa20570)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price by range stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceByRangeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_by_range_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceByRangeEtf]:
        """미국주식 가격대별주가(ETF) (usa20571)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price by range etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceByRangeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeStock]:
        """미국주식 가격급등락(주식/업종) (usa20930)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeEtf]:
        """미국주식 가격급등락(ETF) (usa20931)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_price_surge_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoPriceSurgeWatchlist]:
        """미국주식 가격급등락(관심종목) (usa20932)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching price surge watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoPriceSurgeWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachStock]:
        """미국주식 고가/저가 접근(주식/업종) (usa20970)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachEtf]:
        """미국주식 고가/저가 접근(ETF) (usa20971)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_high_low_approach_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoHighLowApproachWatchlist]:
        """미국주식 고가/저가 접근(관심종목) (usa20972)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching high low approach watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoHighLowApproachWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalStock]:
        """미국주식 거래량갱신(주식/업종) (usa23400)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalEtf]:
        """미국주식 거래량갱신(ETF) (usa23401)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_renewal_watchlist(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeRenewalWatchlist]:
        """미국주식 거래량갱신(관심종목) (usa23402)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume renewal watchlist: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeRenewalWatchlist.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_new_high_low_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoNewHighLowStock]:
        """미국주식 신고가/신저가(주식/업종) (usa24100)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching new high low stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoNewHighLowStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_new_high_low_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoNewHighLowEtf]:
        """미국주식 신고가/신저가(ETF) (usa24101)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching new high low etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoNewHighLowEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_gap_up_down_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoGapUpDownStock]:
        """미국주식 갭상승/갭하락(주식/업종) (usa24140)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching gap up down stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoGapUpDownStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_gap_up_down_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoGapUpDownEtf]:
        """미국주식 갭상승/갭하락(ETF) (usa24141)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching gap up down etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoGapUpDownEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_remaining_ratio_surge_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeStock]:
        """미국주식 잔량률급증(주식/업종) (usa24210)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching remaining ratio surge stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoRemainingRatioSurgeStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_remaining_ratio_surge_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoRemainingRatioSurgeEtf]:
        """미국주식 잔량률급증(ETF) (usa24211)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching remaining ratio surge etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoRemainingRatioSurgeEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_concentration_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationStock]:
        """미국주식 매물대집중(주식/업종) (usa24220)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume concentration stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeConcentrationStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_volume_concentration_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoVolumeConcentrationEtf]:
        """미국주식 매물대집중(ETF) (usa24221)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching volume concentration etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoVolumeConcentrationEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_stock(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateStock]:
        """미국주식 연도별 등락률(종목) (usa26410)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate stock: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateStock.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_by_sector(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateBySector]:
        """미국주식 연도별 업종별 종목등락률 (usa26411)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate by sector: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateBySector.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_by_etf_category(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateByEtfCategory]:
        """미국주식 연도별 ETF 카테고리별 종목등락률 (usa26412)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate by etf category: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateByEtfCategory.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_sector(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateSector]:
        """미국주식 연도별 등락률(업종) (usa26413)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate sector: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateSector.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)

    def get_yearly_fluctuation_rate_etf(
        self,
        body: dict[str, str],
        cont_yn: Literal["Y", "N"] = "N",
        next_key: str = "",
    ) -> KiwoomHttpResponse[OverseasStockInfoYearlyFluctuationRateEtf]:
        """미국주식 연도별 등락률(ETF) (usa26414)

        Args:
            body (dict[str, str]): 요청 파라미터. TODO: API 문서 확정 후 개별 인자로 교체
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

        response = self.client._post(self.path, headers, body)
        if response.status_code != 200:
            raise Exception(f"Error fetching yearly fluctuation rate etf: {response.text}")

        res_headers = KiwoomHttpHeader.model_validate(response.headers)
        res_body = OverseasStockInfoYearlyFluctuationRateEtf.model_validate(response.json())
        return KiwoomHttpResponse(headers=res_headers, body=res_body)
