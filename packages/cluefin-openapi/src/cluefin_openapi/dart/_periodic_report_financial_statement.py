import io
import zipfile
from pathlib import Path
from typing import Literal, Mapping
from xml.etree import ElementTree

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._exceptions import DartAPIError
from cluefin_openapi.dart._model import DartStatusCode
from cluefin_openapi.dart._periodic_report_financial_statement_types import (
    MultiCompanyMajorAccount,
    MultiCompanyMajorAccountItem,
    MultiCompanyMajorIndicator,
    MultiCompanyMajorIndicatorItem,
    SingleCompanyFullStatement,
    SingleCompanyFullStatementItem,
    SingleCompanyMajorAccount,
    SingleCompanyMajorAccountItem,
    SingleCompanyMajorIndicator,
    SingleCompanyMajorIndicatorItem,
    XbrlTaxonomy,
    XbrlTaxonomyItem,
)


class PeriodicReportFinancialStatement:
    """DART 정기보고서 재무정보 조회 API"""

    def __init__(self, client: Client):
        self.client = client

    def get_single_company_major_accounts(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> SingleCompanyMajorAccount:
        """
        단일회사 주요계정

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bsns_year (str): 사업연도 (YYYY)
            reprt_code (str): 보고서코드 (1분기:11013, 반기:11012, 3분기:11014, 사업보고서:11011)

        Returns:
            # SingleCompanyMajorAccount: 단일회사 주요계정 데이터 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/fnlttSinglAcnt.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"단일회사 주요계정 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return SingleCompanyMajorAccount.parse(
            payload,
            list_model=SingleCompanyMajorAccountItem,
        )

    def get_multi_company_major_accounts(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
    ) -> MultiCompanyMajorAccount:
        """다중회사 주요계정

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bsns_year (str): 사업연도 (YYYY)
            reprt_code (str): 보고서코드 (1분기:11013, 반기:11012, 3분기:11014, 사업보고서:11011

        Returns:
            MultiCompanyMajorAccount: 다중회사 주요계정 데이터 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
        }
        payload = self.client._get("/api/fnlttMultiAcnt.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"다중회사 주요계정 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return MultiCompanyMajorAccount.parse(
            payload,
            list_model=MultiCompanyMajorAccountItem,
        )

    def get_single_company_full_statements(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: Literal["CFS", "OFS"] = "CFS",
    ) -> SingleCompanyFullStatement:
        """단일회사 전체 재무제표

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bsns_year (str): 사업연도 (YYYY)
            reprt_code (str): 보고서코드 (1분기:11013, 반기:11012, 3분기:11014, 사업보고서:11011)
            fs_div (Literal["CFS", "OFS"], optional): 개별/연결구분. Defaults to "CFS".

        Returns:
            SingleCompanyFullStatement: 단일회사 전체 재무제표 데이터 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
            "fs_div": fs_div,
        }
        payload = self.client._get("/api/fnlttSinglAcntAll.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"단일회사 전체 재무제표 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return SingleCompanyFullStatement.parse(
            payload,
            list_model=SingleCompanyFullStatementItem,
        )

    def get_single_company_major_indicators(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        idx_cl_code: str,
    ) -> SingleCompanyMajorIndicator:
        """단일회사 주요 재무지표

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bsns_year (str): 사업연도 (YYYY)
            reprt_code (str): 보고서코드 (1분기:11013, 반기:11012, 3분기:11014, 사업보고서:11011)
            idx_cl_code (str): 지표구분코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000)

        Returns:
            SingleCompanyMajorIndicator: 단일회사 주요 재무지표 데이터 응답 객체
        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
            "idx_cl_code": idx_cl_code,
        }
        payload = self.client._get("/api/fnlttSinglIndx.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"단일회사 주요 재무지표 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return SingleCompanyMajorIndicator.parse(
            payload,
            list_model=SingleCompanyMajorIndicatorItem,
        )

    def get_multi_company_major_indicators(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        idx_cl_code: str,
    ) -> MultiCompanyMajorIndicator:
        """
        다중회사 주요 재무지표

        Args:
            corp_code (str): 공시대상회사의 고유번호 (8자리)
            bsns_year (str): 사업연도 (YYYY)
            reprt_code (str): 보고서코드 (1분기:11013, 반기:11012, 3분기:11014, 사업보고서:11011)
            # idx_cl_code (str): 지표구분코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000)

        """
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
            "idx_cl_code": idx_cl_code,
        }
        payload = self.client._get("/api/fnlttCmpnyIndx.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"다중회사 주요 재무지표 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")
        return MultiCompanyMajorIndicator.parse(payload, list_model=MultiCompanyMajorIndicatorItem)

    def get_xbrl_taxonomy(
        self,
        sj_div: Literal[
            "BS1",
            "BS2",
            "BS3",
            "BS4",
            "IS1",
            "IS2",
            "IS3",
            "IS4",
            "CIS1",
            "CIS2",
            "CIS3",
            "CIS4",
            "DCIS1",
            "DCIS2",
            "DCIS3",
            "DCIS4",
            "DCIS5",
            "DCIS6",
            "DCIS7",
            "DCIS8",
            "CF1",
            "CF2",
            "CF3",
            "CF4",
            "SCE1",
            "SCE2",
        ],
    ) -> XbrlTaxonomy:
        """
        XBRL 택사노미 재무제표 양식
        금융감독원 회계포털에서 제공하는 IFRS 기반 XBRL 재무제표 공식 표준 계정과목체계를 제공합니다.

        Args:
            sj_div (Literal): 재무제표구분
                - BS1: 재무상태표 연결 유동/비유동법
                - BS2: 재무상태표 개별 유동/비유동법
                - BS3: 재무상태표 연결 유동성배열법
                - BS4: 재무상태표 개별 유동성배열법
                - IS1: 별개의 손익계산서 연결 기능별분류
                - IS2: 별개의 손익계산서 개별 기능별분류
                - IS3: 별개의 손익계산서 연결 성격별분류
                - IS4: 별개의 손익계산서 개별 성격별분류
                - CIS1: 포괄손익계산서 연결 세후
                - CIS2: 포괄손익계산서 개별 세후
                - CIS3: 포괄손익계산서 연결 세전
                - CIS4: 포괄손익계산서 개별 세전
                - DCIS1: 단일 포괄손익계산서 연결 기능별분류 세후포괄손익
                - DCIS2: 단일 포괄손익계산서 개별 기능별분류 세후포괄손익
                - DCIS3: 단일 포괄손익계산서 연결 기능별분류 세전
                - DCIS4: 단일 포괄손익계산서 개별 기능별분류 세전
                - DCIS5: 단일 포괄손익계산서 연결 성격별분류 세후포괄손익
                - DCIS6: 단일 포괄손익계산서 개별 성격별분류 세후포괄손익
                - DCIS7: 단일 포괄손익계산서 연결 성격별분류 세전
                - DCIS8: 단일 포괄손익계산서 개별 성격별분류 세전
                - CF1: 현금흐름표 연결 직접법
                - CF2: 현금흐름표 개별 직접법
                - CF3: 현금흐름표 연결 간접법
                - CF4: 현금흐름표 개별 간접법
                - SCE1: 자본변동표 연결
                - SCE2: 자본변동표 개별

        Returns:
            XbrlTaxonomy: XBRL 택사노미 재무제표 양식 데이터 응답 객체
        """
        params = {
            "sj_div": sj_div,
        }
        payload = self.client._get("/api/xbrlTaxonomy.json", params=params)
        if not isinstance(payload, Mapping):
            raise TypeError(
                f"XBRL 택사노미 재무제표 양식 API 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}"
            )

        return XbrlTaxonomy.parse(payload, list_model=XbrlTaxonomyItem)

    def download_financial_statement_xbrl(
        self,
        rcept_no: str,
        reprt_code: Literal["11011", "11012", "11013", "11014"],
        *,
        destination: Path | str = Path("."),
        overwrite: bool = False,
    ) -> Path:
        """
        재무제표 원본파일(XBRL) - 정기보고서에 첨부된 XBRL 재무제표 원본파일을 다운로드합니다.

        DART API는 XBRL 패키지를 ZIP 형식으로 반환합니다. ZIP 파일에는 다음 파일들이 포함됩니다:
        - .xbrl: XBRL instance document (실제 재무 데이터)
        - .xsd: Taxonomy schema (확장 스키마)
        - _def.xml: Definition linkbase
        - _cal.xml: Calculation linkbase
        - _pre.xml: Presentation linkbase
        - _lab-ko.xml: Korean label linkbase
        - _lab-en.xml: English label linkbase

        Args:
            rcept_no (str): 접수번호 (14자리)
            reprt_code (Literal): 보고서코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)
            destination (Path | str): 압축 해제할 폴더 경로. Defaults to current directory.
            overwrite (bool): 기존 파일 덮어쓰기 여부. Defaults to False.

        Returns:
            Path: XBRL 파일들이 압축 해제된 폴더 경로
        """
        params = {
            "rcept_no": rcept_no,
            "reprt_code": reprt_code,
        }
        payload = self.client._get_bytes("/api/fnlttXbrl.xml", params=params)

        stripped = payload.lstrip()
        if stripped.startswith(b"<"):
            try:
                root = ElementTree.fromstring(payload)
            except ElementTree.ParseError:
                root = None
            if root is not None:
                status = (root.findtext("status") or "").strip()
                if status and status != DartStatusCode.SUCCESS:
                    message = (root.findtext("message") or "").strip()
                    raise DartAPIError(
                        message or "재무제표 원본파일(XBRL) 조회에 실패했습니다.",
                        response_data={"status": status, "message": message},
                    )

        destination_path = Path(destination).expanduser()
        destination_path.mkdir(parents=True, exist_ok=True)

        buffer = io.BytesIO(payload)
        if zipfile.is_zipfile(buffer):
            buffer.seek(0)
            try:
                with zipfile.ZipFile(buffer) as archive:
                    if not overwrite:
                        for name in archive.namelist():
                            file_path = destination_path / name
                            if file_path.exists():
                                raise FileExistsError(f"이미 존재하는 파일을 덮어쓸 수 없습니다: {file_path}")
                    archive.extractall(destination_path)
            except zipfile.BadZipFile as exc:  # pragma: no cover - defensive guard
                raise DartAPIError("ZIP 파일이 손상되었습니다.") from exc
        else:
            raise DartAPIError("응답이 ZIP 파일 형식이 아닙니다.")

        return destination_path
