"""
Utilities for retrieving fundamental analysis data via the DART OpenAPI.

This module wraps the lower-level REST clients in ``cluefin_openapi`` and exposes
helpers that return Python-native structures ready to feed into the CLI views.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional

from cluefin_openapi.dart._client import Client as DartClient
from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement
from cluefin_openapi.dart._periodic_report_financial_statement_types import (
    SingleCompanyMajorAccount,
    SingleCompanyMajorAccountItem,
    SingleCompanyMajorIndicator,
    SingleCompanyMajorIndicatorItem,
)
from cluefin_openapi.dart._periodic_report_key_information import PeriodicReportKeyInformation
from cluefin_openapi.dart._periodic_report_key_information_types import (
    DividendInformation,
    MajorShareholderStatus,
)
from cluefin_openapi.dart._public_disclosure import PublicDisclosure
from cluefin_openapi.dart._public_disclosure_types import CompanyOverview, UniqueNumber, UniqueNumberItem

from cluefin_cli.config.settings import settings

TARGET_ACCOUNTS: Dict[str, str] = {
    "매출액": "Revenue",
    "영업이익": "Operating Profit",
    "당기순이익": "Net Profit",
    "자산총계": "Total Assets",
    "부채총계": "Total Liabilities",
    "자본총계": "Total Equity",
}

INDICATOR_CATEGORIES: Dict[str, str] = {
    "M210000": "Profitability",
    "M220000": "Stability",
    "M230000": "Growth",
    "M240000": "Efficiency",
}


@dataclass(slots=True)
class AccountSnapshot:
    """Normalised snapshot for a single financial account."""

    name: str
    label: str
    current_label: str
    current_amount: Optional[Decimal]
    previous_label: Optional[str]
    previous_amount: Optional[Decimal]
    currency: Optional[str]


@dataclass(slots=True)
class IndicatorSnapshot:
    """Normalised representation of a financial indicator."""

    category: str
    name: str
    value: Optional[Decimal]
    unit_hint: Optional[str]


@dataclass(slots=True)
class DividendSnapshot:
    """Dividend data for the current and prior periods."""

    category: str
    current: Optional[str]
    previous: Optional[str]
    two_years_ago: Optional[str]
    stock_kind: Optional[str]


@dataclass(slots=True)
class ShareholderSnapshot:
    """Largest shareholder ownership details."""

    name: str
    relation: Optional[str]
    shares_current: Optional[str]
    holding_ratio_current: Optional[str]
    shares_previous: Optional[str]
    holding_ratio_previous: Optional[str]


class DomesticFundamentalDataFetcher:
    """Fetches and normalises domestic stock fundamental data via DART OpenAPI."""

    def __init__(self):
        if not settings.dart_auth_key:
            raise ValueError("DART_AUTH_KEY environment variable is required for fundamental analysis.")

        self._client = DartClient(auth_key=settings.dart_auth_key)
        self._public_disclosure = PublicDisclosure(self._client)
        self._financial_statement = PeriodicReportFinancialStatement(self._client)
        self._key_information = PeriodicReportKeyInformation(self._client)

        self._corp_index: Dict[str, UniqueNumberItem] = {}
        self._corp_index_loaded: bool = False

    async def get_corp_code(self, stock_code: str) -> str:
        """Resolve a 6-digit stock code to its DART corporate code."""
        normalised = stock_code.strip()
        if not normalised:
            raise ValueError("Stock code must not be empty.")

        if not normalised.isdigit():
            raise ValueError(f"Stock code must be numeric. Received: {stock_code}")

        normalised = normalised.zfill(6)
        await self._ensure_corp_index()

        item = self._corp_index.get(normalised)
        if item is None:
            raise ValueError(f"No corp code mapping found for stock code {normalised}.")

        return item.corp_code

    async def get_company_overview(self, corp_code: str) -> CompanyOverview:
        """Retrieve company overview details from DART."""
        overview = self._public_disclosure.company_overview(corp_code)
        if overview.status != "000":
            raise ValueError(f"DART company overview error ({overview.status}): {overview.message}")
        return overview

    async def get_key_accounts(
        self,
        corp_code: str,
        *,
        business_year: str,
        report_code: str,
    ) -> List[AccountSnapshot]:
        """Fetch key financial accounts for the provided period."""
        response = self._financial_statement.get_single_company_major_accounts(
            corp_code=corp_code,
            bsns_year=business_year,
            reprt_code=report_code,
        )
        self._ensure_success(response)

        items = response.result.list or []
        deduped: Dict[str, SingleCompanyMajorAccountItem] = {}

        for item in items:
            deduped.setdefault(item.account_nm, item)

        snapshots: List[AccountSnapshot] = []
        for account_name, friendly_name in TARGET_ACCOUNTS.items():
            source = deduped.get(account_name)
            if source is None:
                continue

            snapshots.append(
                AccountSnapshot(
                    name=friendly_name,
                    label=account_name,
                    current_label=source.thstrm_nm,
                    current_amount=self._parse_decimal(source.thstrm_amount),
                    previous_label=source.frmtrm_nm,
                    previous_amount=self._parse_decimal(source.frmtrm_amount),
                    currency=source.currency,
                )
            )

        if not snapshots:
            for item in items[:6]:
                snapshots.append(
                    AccountSnapshot(
                        name=item.account_nm,
                        label=item.account_nm,
                        current_label=item.thstrm_nm,
                        current_amount=self._parse_decimal(item.thstrm_amount),
                        previous_label=item.frmtrm_nm,
                        previous_amount=self._parse_decimal(item.frmtrm_amount),
                        currency=item.currency,
                    )
                )

        return snapshots

    async def get_indicators(
        self,
        corp_code: str,
        *,
        business_year: str,
        report_code: str,
    ) -> List[IndicatorSnapshot]:
        """Retrieve major financial indicators across the core categories."""
        snapshots: List[IndicatorSnapshot] = []
        for idx_cl_code, category in INDICATOR_CATEGORIES.items():
            response = self._financial_statement.get_single_company_major_indicators(
                corp_code=corp_code,
                bsns_year=business_year,
                reprt_code=report_code,
                idx_cl_code=idx_cl_code,
            )
            self._ensure_success(response)

            items: List[SingleCompanyMajorIndicatorItem] = response.result.list or []
            for item in items[:6]:
                snapshots.append(
                    IndicatorSnapshot(
                        category=category,
                        name=item.idx_nm,
                        value=self._parse_decimal(item.idx_val),
                        unit_hint=self._guess_indicator_unit(item.idx_nm),
                    )
                )

        return snapshots

    async def get_dividend_information(
        self,
        corp_code: str,
        *,
        business_year: str,
        report_code: str,
    ) -> List[DividendSnapshot]:
        """Fetch dividend distribution details."""
        response = self._key_information.get_dividend_information(
            corp_code=corp_code,
            bsns_year=business_year,
            reprt_code=report_code,
        )
        self._ensure_success(response)

        records: List[DividendSnapshot] = []
        for item in response.result.list or []:
            records.append(
                DividendSnapshot(
                    category=item.se,
                    current=self._normalise_text(item.thstrm),
                    previous=self._normalise_text(item.frmtrm),
                    two_years_ago=self._normalise_text(item.lwfr),
                    stock_kind=item.stock_knd,
                )
            )

        return records

    async def get_major_shareholders(
        self,
        corp_code: str,
        *,
        business_year: str,
        report_code: str,
    ) -> List[ShareholderSnapshot]:
        """Fetch largest shareholder holdings."""
        response = self._key_information.get_major_shareholder_status(
            corp_code=corp_code,
            bsns_year=business_year,
            reprt_code=report_code,
        )
        self._ensure_success(response)

        shareholders: List[ShareholderSnapshot] = []
        for item in response.result.list or []:
            shareholders.append(
                ShareholderSnapshot(
                    name=item.nm,
                    relation=item.relate or "",
                    shares_previous=item.bsis_posesn_stock_co,
                    holding_ratio_previous=item.bsis_posesn_stock_qota_rt,
                    shares_current=item.trmend_posesn_stock_co,
                    holding_ratio_current=item.trmend_posesn_stock_qota_rt,
                )
            )

        return shareholders

    async def _ensure_corp_index(self) -> None:
        """Load the corp code index if it has not been initialised yet."""
        if self._corp_index_loaded:
            return

        response: UniqueNumber = self._public_disclosure.corp_code()
        result = response.result
        if result.status != "000":
            raise ValueError(f"DART corp code fetch failed ({result.status}): {result.message}")

        self._corp_index = {item.stock_code: item for item in (result.list or []) if item.stock_code}
        self._corp_index_loaded = True

    @staticmethod
    def _ensure_success(
        response: SingleCompanyMajorAccount
        | SingleCompanyMajorIndicator
        | DividendInformation
        | MajorShareholderStatus,
    ) -> None:
        """Verify that a DART response completed successfully."""
        if response.result.status != "000":
            raise ValueError(f"DART API error ({response.result.status}): {response.result.message}")

    @staticmethod
    def _parse_decimal(value: Optional[str]) -> Optional[Decimal]:
        """Safely parse DART numeric strings into Decimal values."""
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned or cleaned == "-":
            return None
        cleaned = cleaned.replace(",", "")
        if cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = f"-{cleaned[1:-1]}"
        try:
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def _normalise_text(value: Optional[str]) -> Optional[str]:
        """Collapse blank strings into ``None``."""
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @staticmethod
    def _guess_indicator_unit(name: str) -> Optional[str]:
        """Infer a human friendly unit hint for the indicator value."""
        lowered = name.lower()
        if "률" in name or "율" in name or "%" in name or "return" in lowered:
            return "%"
        if "회전" in name or "배" in name or "turnover" in lowered or "ratio" in lowered:
            return None
        return None


def default_business_year() -> str:
    """Return the most recent completed business year."""
    current_year = datetime.now().year
    return str(current_year - 1)
