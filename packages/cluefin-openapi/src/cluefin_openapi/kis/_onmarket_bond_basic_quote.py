"""장내채권 기본 시세"""

from typing_extensions import Literal

from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpHeader, KisHttpResponse
from cluefin_openapi.kis._onmarket_bond_basic_quote_types import (
    OnmarketBondAskingPrice,
    OnmarketBondAvgUnitPrice,
    OnmarketBondDailyChartPrice,
    OnmarketBondDailyPrice,
    OnmarketBondExecution,
    OnmarketBondIssueInfo,
    OnmarketBondPrice,
)


class OnmarketBondBasicQuote:
    """장내채권 기본시세"""

    def __init__(self, client: HttpClient):
        self.client = client

    def _check_response_error(self, response_data: dict) -> None:
        """Check if API response contains an error and raise if so."""
        rt_cd = response_data.get("rt_cd")
        if rt_cd != "0":
            msg_cd = response_data.get("msg_cd", "")
            msg1 = response_data.get("msg1", "Unknown error")
            raise ValueError(f"KIS API Error [{msg_cd}]: {msg1} (rt_cd={rt_cd})")

    def get_bond_asking_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["B"] = "B"
    ) -> KisHttpResponse[OnmarketBondAskingPrice]:
        """
        장내채권현재가(호가) [국내주식-132]

        Args:
            fid_input_iscd (str): 채권종목코드 (ex. KR2088012A16)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, B: 장내채권

        Returns:
            KisHttpResponse[OnmarketBondAskingPrice]: 장내채권현재가(호가)
        """
        headers = {
            "tr_id": "FHKBJ773401C0",
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-bond/v1/quotations/inquire-asking-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondAskingPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["B"] = "B"
    ) -> KisHttpResponse[OnmarketBondPrice]:
        """
        장내채권현재가(시세) [국내주식-200]

        Args:
            fid_input_iscd (str): 채권종목코드 (ex. KR2033022D33)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, B: 장내채권

        Returns:
            KisHttpResponse[OnmarketBondPrice]: 장내채권현재가(시세)
        """
        headers = {"tr_id": "FHKBJ773400C0"}
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-bond/v1/quotations/inquire-price", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_execution(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["B"] = "B"
    ) -> KisHttpResponse[OnmarketBondExecution]:
        """
        장내채권현재가(체결) [국내주식-201]

        Args:
            fid_input_iscd (str): 채권종목코드 (ex. KR2033022D33)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, B: 장내채권

        Returns:
            KisHttpResponse[OnmarketBondExecution]: 장내채권현재가(체결)
        """
        headers = {"tr_id": "FHKBJ773403C0"}
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get("/uapi/domestic-bond/v1/quotations/inquire-ccnl", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondExecution.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_daily_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["B"] = "B"
    ) -> KisHttpResponse[OnmarketBondDailyPrice]:
        """
        장내채권현재가(일별) [국내주식-202]

        Args:
            fid_input_iscd (str): 채권종목코드 (ex. KR2033022D33)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, B: 장내채권

        Returns:
            KisHttpResponse[OnmarketBondDailyPrice]: 장내채권현재가(일별)
        """
        headers = {"tr_id": "FHKBJ773404C0"}
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-bond/v1/quotations/inquire-daily-price", headers=headers, params=params
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondDailyPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_daily_chart_price(
        self, fid_input_iscd: str, fid_cond_mrkt_div_code: Literal["B"] = "B"
    ) -> KisHttpResponse[OnmarketBondDailyChartPrice]:
        """
        장내채권 기간별시세(일) [국내주식-159]

        Args:
            fid_input_iscd (str): 채권종목코드 (ex. KR2033022D33)
            fid_cond_mrkt_div_code (str): 조건 시장 분류 코드, B: 장내채권

        Returns:
            KisHttpResponse[OnmarketBondDailyChartPrice]: 장내채권 기간별시세(일) (최근 30건)
        """
        headers = {"tr_id": "FHKBJ773701C0"}
        params = {
            "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
            "FID_INPUT_ISCD": fid_input_iscd,
        }
        response = self.client._get(
            "/uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondDailyChartPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_avg_unit_price(
        self,
        inqr_strt_dt: str,
        inqr_end_dt: str,
        pdno: str = "",
        prdt_type_cd: str = "302",
        vrfc_kind_cd: str = "00",
        custtype: Literal["B", "P"] = "P",
    ) -> KisHttpResponse[OnmarketBondAvgUnitPrice]:
        """
        장내채권 평균단가조회 [국내주식-158]

        Args:
            inqr_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inqr_end_dt (str): 조회종료일자 (YYYYMMDD)
            pdno (str): 상품번호 (채권종목코드)
            prdt_type_cd (str): 상품유형코드 (302: 채권)
            vrfc_kind_cd (str): 검증종류코드 (00)
            custtype (str): 고객타입 (B: 법인, P: 개인)

        Returns:
            KisHttpResponse[OnmarketBondAvgUnitPrice]: 장내채권 평균단가조회
        """
        headers = {"tr_id": "CTPF2005R", "custtype": custtype}
        params = {
            "INQR_STRT_DT": inqr_strt_dt,
            "INQR_END_DT": inqr_end_dt,
            "PDNO": pdno,
            "PRDT_TYPE_CD": prdt_type_cd,
            "VRFC_KIND_CD": vrfc_kind_cd,
            "CTX_AREA_NK30": "",
            "CTX_AREA_FK100": "",
        }
        response = self.client._get(
            "/uapi/domestic-bond/v1/quotations/avg-unit",
            headers=headers,
            params=params,
        )
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondAvgUnitPrice.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)

    def get_bond_issue_info(self, pdno: str, prdt_type_cd: str = "302") -> KisHttpResponse[OnmarketBondIssueInfo]:
        """
        장내채권 발행정보 [국내주식-156]

        Args:
            pdno (str): 채권 종목번호 (ex. KR6449111CB8)
            prdt_type_cd (str): 상품유형코드 (302: 채권)

        Returns:
            KisHttpResponse[OnmarketBondIssueInfo]: 장내채권 발행정보
        """
        headers = {"tr_id": "CTPF1101R"}
        params = {"PDNO": pdno, "PRDT_TYPE_CD": prdt_type_cd}
        response = self.client._get("/uapi/domestic-bond/v1/quotations/issue-info", headers=headers, params=params)
        response_data = response.json()
        self._check_response_error(response_data)
        header = KisHttpHeader.model_validate(response.headers)
        body = OnmarketBondIssueInfo.model_validate(response_data)
        return KisHttpResponse(header=header, body=body)
