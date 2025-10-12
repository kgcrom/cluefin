"""공시정보 (Public Disclosure Information) API client."""

from __future__ import annotations

import io
import zipfile
from datetime import date, timedelta
from pathlib import Path
from typing import List, Literal, Mapping, Optional
from xml.etree.ElementTree import Element

from defusedxml.ElementTree import ParseError, fromstring

from ._client import Client
from ._exceptions import (
    DartAPIError,
)
from ._public_disclosure_types import (
    CompanyOverview,
    PublicDisclosureSearch,
    PublicDisclosureSearchItem,
    UniqueNumber,
    UniqueNumberItem,
)


class PublicDisclosure:
    """DART 공시정보 API"""

    def __init__(self, client: Client):
        self.client = client

    def public_disclosure_search(
        self,
        *,
        corp_code: Optional[str] = None,
        bgn_de: Optional[str] = None,
        end_de: Optional[str] = None,
        last_reprt_at: Literal["Y", "N"] = "N",
        pblntf_ty: Optional[Literal["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]] = None,
        pblntf_detail_ty: Optional[str] = None,
        corp_cls: Optional[Literal["Y", "K", "N", "E"]] = None,
        sort: Optional[Literal["date", "crp", "rpt"]] = None,
        sort_mth: Optional[Literal["asc", "desc"]] = None,
        page_no: Optional[int] = None,
        page_count: Optional[int] = None,
    ) -> PublicDisclosureSearch:
        """공시검색

        Args:
            corp_code (str, optional): 고유번호 (선택). 공시대상회사의 고유번호(8자리).
            bgn_de (str, optional): 시작일 (선택). 검색시작 접수일자(YYYYMMDD).
            end_de (str, optional): 종료일 (선택). 검색종료 접수일자(YYYYMMDD).
            last_reprt_at (Literal["Y", "N"], optional): 최종보고서 검색 여부. 기본값 "N".
            pblntf_ty (Literal["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], optional): 공시유형.
            pblntf_detail_ty (str, optional): 공시상세유형. ※ 상세요청 시 공시유형과 동시에 제공.
            corp_cls (Literal["Y", "K", "N", "E"], optional): 법인구분. Y(유가), K(코스닥), N(코넥스), E(기타).
            sort (Literal["date", "crp", "rpt"], optional): 정렬기준. date(접수일자), crp(회사명), rpt(보고서명).
            sort_mth (Literal["asc", "desc"], optional): 정렬방식. asc(오름차순), desc(내림차순).
            page_no (int, optional): 페이지 번호(1~N). 기본값 1.
            page_count (int, optional): 페이지 별 건수(1~100). 기본값 10.

        Returns:
            PublicDisclosureSearch: 공시검색 결과
        """
        if bgn_de is None and end_de is None:
            # DART defaults to an empty result when no date range is provided.
            today = date.today()
            bgn_de = (today - timedelta(days=90)).strftime("%Y%m%d")
            end_de = today.strftime("%Y%m%d")

        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
            "last_reprt_at": last_reprt_at,
            "pblntf_ty": pblntf_ty,
            "pblntf_detail_ty": pblntf_detail_ty,
            "corp_cls": corp_cls,
            "sort": sort,
            "sort_mth": sort_mth,
            "page_no": page_no,
            "page_count": page_count,
        }

        query_params = {key: value for key, value in params.items() if value is not None}

        payload = self.client._get("/api/list.json", params=query_params)
        if not isinstance(payload, Mapping):
            raise TypeError(f"DART 공시검색 응답은 매핑 타입이어야 합니다. 수신한 타입: {type(payload)!r}")

        return PublicDisclosureSearch.parse(
            payload,
            list_model=PublicDisclosureSearchItem,
        )

    def company_overview(self, corp_code: str) -> CompanyOverview:
        """기업개황요청

        Args:
            corp_code (str): 공시대상회사의 고유번호(8자리)

        Returns:
            CompanyOverview: 기업개황 데이터
        """
        # DART 공시정보 > 기업개황 API는 corp_code가 필수 파라미터입니다.
        payload = self.client._get("/api/company.json", params={"corp_code": corp_code})
        if not isinstance(payload, dict):  # pragma: no cover - defensive guard
            raise TypeError("기업개황 응답이 JSON 형식이 아닙니다.")
        return CompanyOverview.model_validate(payload)

    def disclosure_document_file(
        self,
        rcept_no: str,
        *,
        destination: Path | str = Path("document.xml"),
        overwrite: bool = False,
    ) -> Path:
        """
        공시서류원본파일 - 공시보고서 원본파일을 제공합니다.

        Args:
            rcept_no (str): 접수번호(14자리)
            destination (Path | str, optional): 저장할 파일 경로. 기본값 Path("document.xml").
            overwrite (bool, optional): 이미 존재하는 파일을 덮어쓸지 여부. 기본값 False.

        Returns:
            Path: 저장된 파일 경로
        """
        params = {"rcept_no": rcept_no}
        payload = self.client._get_bytes("/api/document.xml", params=params)
        stripped = payload.lstrip()
        # DART returns error details as small XML bodies even on binary endpoints.
        if stripped.startswith(b"<"):
            try:
                root = fromstring(payload)
            except ParseError:
                root = None
            if root is not None:
                status = (root.findtext("status") or "").strip()
                message = (root.findtext("message") or "").strip()
                if status and status != "000":
                    raise DartAPIError(
                        message or "공시서류 원본파일 조회에 실패했습니다.",
                        response_data={"status": status, "message": message},
                    )

        xml_bytes = payload
        buffer = io.BytesIO(payload)
        if zipfile.is_zipfile(buffer):
            buffer.seek(0)
            try:
                with zipfile.ZipFile(buffer) as archive:
                    xml_name = next(
                        (name for name in archive.namelist() if name.lower().endswith(".xml")),
                        None,
                    )
                    if xml_name is None:
                        raise DartAPIError("공시서류 ZIP 파일에 XML 데이터가 포함되어있지 않습니다.")
                    xml_bytes = archive.read(xml_name)
            except zipfile.BadZipFile as exc:  # pragma: no cover - defensive guard
                raise DartAPIError("공시서류 ZIP 파일이 손상되었습니다.") from exc

        destination_path = Path(destination).expanduser()
        if destination_path.is_dir():
            destination_path = destination_path / "document.xml"

        if destination_path.exists() and not overwrite:
            raise FileExistsError(f"이미 존재하는 파일을 덮어쓸 수 없습니다: {destination_path}")

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_bytes(xml_bytes)
        return destination_path

    def corp_code(self) -> UniqueNumber:
        """고유번호 - DART에 등록되어있는 공시대상회사의 고유번호,회사명,종목코드, 최근변경일자를 파일로 제공합니다."""
        params = {"crtfc_key": self.client.auth_key}
        response = self.client._get_bytes("/api/corpCode.xml", params=params)
        xml_bytes = None
        try:
            with zipfile.ZipFile(io.BytesIO(response)) as archive:
                xml_name = next(
                    (name for name in archive.namelist() if name.lower().endswith(".xml")),
                    None,
                )
                if xml_name is None:
                    raise DartAPIError("고유번호 ZIP 파일에 XML 데이터가 포함되어있지 않습니다.")
                xml_bytes = archive.read(xml_name)
        except zipfile.BadZipFile as exc:  # pragma: no cover - defensive guard
            raise DartAPIError("고유번호 ZIP 파일이 손상되었습니다.") from exc

        try:
            root = fromstring(xml_bytes)
        except ParseError as exc:  # pragma: no cover - defensive guard
            raise DartAPIError("고유번호 XML 파싱에 실패했습니다.") from exc

        status = "000"
        message = "정상"

        items: List[UniqueNumberItem] = []
        for element in root.findall("list"):
            corp_code = self._xml_text(element, "corp_code")
            corp_name = self._xml_text(element, "corp_name")

            if not corp_code or not corp_name:
                continue  # pragma: no cover - skip malformed entries defensively

            corp_eng_name = self._xml_text(element, "corp_eng_name") or self._xml_text(element, "corp_name_eng")

            items.append(
                UniqueNumberItem(
                    corp_code=corp_code,
                    corp_name=corp_name,
                    corp_eng_name=corp_eng_name or None,
                    corp_cls=self._optional_xml_text(element, "corp_cls"),
                    stock_code=self._optional_xml_text(element, "stock_code"),
                    modify_date=self._xml_text(element, "modify_date"),
                )
            )

        payload = {
            "result": {
                "status": status,
                "message": message,
                "list": items,
            }
        }

        return UniqueNumber.parse(payload, list_model=UniqueNumberItem)

    @staticmethod
    def _xml_text(node: Element, tag: str) -> str:
        value = node.findtext(tag)
        return value.strip() if value else ""

    def _optional_xml_text(self, node: Element, tag: str) -> Optional[str]:
        value = self._xml_text(node, tag)
        return value or None
