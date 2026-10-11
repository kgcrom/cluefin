"""공시 원문 파일 (www.sec.gov/Archives/edgar/data)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from ._archives_types import FilingIndex
from ._client import WWW_BASE_URL, Client
from ._exceptions import SecAPIError
from ._ids import accession_plain, cik_digits, path_segment

# XBRL 제출물에서 파서가 쓰는 파일은 인스턴스, 회사 스키마(.xsd), 링크베이스(_cal/_def/_lab/_pre.xml)다.
# 인라인 XBRL 공시(2019년~)는 SEC가 본문 .htm에서 뽑은 인스턴스를 `<이름>_htm.xml`로 함께 둔다.
# 폴더의 .xml 중 XBRL 입력이 아닌 것은 SEC 렌더링 결과(2009~2012년의 R1.xml)와 요약 파일뿐이다.
_NOT_XBRL_INPUT = re.compile(r"^(R\d+|FilingSummary)\.xml$", re.IGNORECASE)


class Archives:
    """SEC 공시 원문 파일"""

    def __init__(self, client: Client):
        self.client = client

    def filing_index(self, cik: int | str, accession_number: str) -> FilingIndex:
        """공시 폴더의 파일 목록.

        Args:
            cik (int | str): 제출 회사의 CIK
            accession_number (str): 접수번호 (대시는 있어도 없어도 된다)
        """
        payload = self.client._get_json(f"{_folder_url(cik, accession_number)}/index.json")
        if not isinstance(payload, dict) or not isinstance(payload.get("directory"), dict):
            raise SecAPIError(f"공시 폴더 목록 응답에 directory가 없습니다: {accession_number}")
        return FilingIndex.model_validate(payload["directory"])

    def download_filing_document(
        self,
        cik: int | str,
        accession_number: str,
        name: str,
        *,
        destination: Path | str = Path("."),
        overwrite: bool = False,
    ) -> Path:
        """공시 폴더의 파일 하나를 저장한다 (예: 주 문서 `aapl-20230930.htm`).

        Args:
            cik (int | str): 제출 회사의 CIK
            accession_number (str): 접수번호
            name (str): 파일명. `FilingEntry.primary_document` 또는 `filing_index()`의 항목 이름.
            destination (Path | str): 저장할 폴더. 기본값 현재 폴더.
            overwrite (bool): 이미 있는 파일을 덮어쓸지. 기본값 False.

        Returns:
            Path: 저장된 파일 경로
        """
        name = path_segment(name, what="파일명")
        path = Path(destination).expanduser() / name
        if path.exists() and not overwrite:
            raise FileExistsError(f"이미 존재하는 파일을 덮어쓸 수 없습니다: {path}")

        data = self.client._get_bytes(f"{_folder_url(cik, accession_number)}/{name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def download_xbrl_files(
        self,
        cik: int | str,
        accession_number: str,
        *,
        destination: Path | str,
        overwrite: bool = False,
    ) -> List[Path]:
        """XBRL 인스턴스·스키마·링크베이스를 한 폴더에 저장한다. `cluefin-xbrl`이 그 폴더를 파싱한다.

        인라인 XBRL 공시(2019년~)는 SEC가 뽑아 둔 인스턴스(`*_htm.xml`)를 받는다. 본문 .htm은 받지 않는다.

        Args:
            cik (int | str): 제출 회사의 CIK
            accession_number (str): 접수번호
            destination (Path | str): 저장할 폴더
            overwrite (bool): 이미 있는 파일을 덮어쓸지. 기본값 False. 하나라도 있으면 아무것도 받지 않는다.

        Returns:
            List[Path]: 저장된 파일 경로 (이름순)

        Raises:
            SecAPIError: 폴더에 XBRL 파일(스키마 .xsd)이 없을 때
        """
        index = self.filing_index(cik, accession_number)
        # Validate every name before the first download so a bad one cannot leave a half-written folder.
        names = sorted(path_segment(item.name, what="파일명") for item in index.items if _is_xbrl_input(item.name))
        if not any(name.lower().endswith(".xsd") for name in names):
            raise SecAPIError(f"XBRL 파일이 없는 공시입니다: {accession_number}")

        folder = Path(destination).expanduser()
        if not overwrite:
            existing = next((folder / name for name in names if (folder / name).exists()), None)
            if existing is not None:
                raise FileExistsError(f"이미 존재하는 파일을 덮어쓸 수 없습니다: {existing}")

        return [
            self.download_filing_document(cik, accession_number, name, destination=folder, overwrite=True)
            for name in names
        ]


def _folder_url(cik: int | str, accession_number: str) -> str:
    return f"{WWW_BASE_URL}/Archives/edgar/data/{cik_digits(cik)}/{accession_plain(accession_number)}"


def _is_xbrl_input(name: str) -> bool:
    lowered = name.lower()
    return lowered.endswith((".xsd", ".xml")) and not _NOT_XBRL_INPUT.match(name)
