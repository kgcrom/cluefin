"""제출 이력 (data.sec.gov/submissions)."""

from __future__ import annotations

import re
from typing import List, Optional, Sequence

from ._client import DATA_BASE_URL, Client
from ._ids import cik10
from ._submissions_types import CompanySubmissions, FilingEntry, columns_to_rows

_PAGE_NAME_PATTERN = re.compile(r"^CIK\d{10}-submissions-\d{3}\.json$")


class Submissions:
    """SEC 제출 이력 API"""

    def __init__(self, client: Client):
        self.client = client

    def submissions(self, cik: int | str) -> CompanySubmissions:
        """회사 정보와 최근 제출 이력.

        Args:
            cik (int | str): CIK. 앞자리 0과 `CIK` 접두사는 있어도 없어도 된다.

        Returns:
            CompanySubmissions: 회사 정보, 최근 제출 이력(`filings`), 오래된 이력 페이지 목록(`filing_files`)
        """
        payload = self.client._get_json(f"{DATA_BASE_URL}/submissions/CIK{cik10(cik)}.json")
        return CompanySubmissions.model_validate(payload)

    def submissions_page(self, name: str) -> List[FilingEntry]:
        """오래된 제출 이력 한 페이지.

        Args:
            name (str): `CompanySubmissions.filing_files[i].name` (예: `CIK0000320193-submissions-001.json`)

        Returns:
            List[FilingEntry]: 그 페이지의 제출 이력
        """
        if not _PAGE_NAME_PATTERN.match(name):
            raise ValueError(f"제출 이력 페이지 이름이 아닙니다: {name!r}")
        payload = self.client._get_json(f"{DATA_BASE_URL}/submissions/{name}")
        return [FilingEntry.model_validate(row) for row in columns_to_rows(payload)]

    def filings(
        self,
        cik: int | str,
        *,
        forms: Optional[Sequence[str]] = None,
        include_amendments: bool = True,
        include_older: bool = False,
    ) -> List[FilingEntry]:
        """제출 이력을 서식으로 걸러 돌려준다 (최신순).

        Args:
            cik (int | str): CIK
            forms (Sequence[str], optional): 남길 서식 (예: ["10-K", "10-Q"]). None이면 전부.
            include_amendments (bool): forms를 줬을 때 정정 서식(`10-K/A` 등)도 남길지. 기본 True.
            include_older (bool): 최근 이력 밖의 오래된 페이지까지 모두 받을지. 페이지마다 요청이 한 번씩 더 간다.

        Returns:
            List[FilingEntry]: 걸러진 제출 이력
        """
        company = self.submissions(cik)
        entries = list(company.filings)
        if include_older:
            for page in company.filing_files:
                entries.extend(self.submissions_page(page.name))
            entries.sort(key=lambda entry: entry.filing_date, reverse=True)
        if forms is None:
            return entries

        wanted = {form.upper() for form in forms}
        if include_amendments:
            wanted |= {f"{form}/A" for form in wanted}
        return [entry for entry in entries if entry.form.upper() in wanted]
