"""Industry chart data importer from KIS API."""

import time
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Sequence, TypedDict

import pandas as pd
import requests
from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_issue_other_types import SectorPeriodQuoteItem1, SectorPeriodQuoteItem2
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


class SectorPeriodData(TypedDict):
    """Type definition for sector period data response."""

    output1: SectorPeriodQuoteItem1
    output2: Sequence[SectorPeriodQuoteItem2]


class DomesticIndustryChartImporter:
    """Import domestic industry chart data from KIS API to DuckDB."""

    def __init__(self, client: Client, db_manager: DuckDBManager):
        """Initialize domestic industry chart data importer.

        Args:
            client: KIS API client
            db_manager: DuckDB manager instance
        """
        self.client = client
        self.db_manager = db_manager

    def import_industry_data(
        self,
        industry_code: str,
        start_date: str,
        end_date: str,
    ) -> int:
        """Import daily chart data for a single industry.

        Args:
            industry_code: Industry code (e.g., '001' for KOSPI)
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format

        Returns:
            Number of records imported
        """
        industry_code = industry_code.strip()

        if not self._validate_date_format(start_date):
            raise ValueError(f"Invalid start date format: {start_date}")
        if not self._validate_date_format(end_date):
            raise ValueError(f"Invalid end date format: {end_date}")

        try:
            # Fetch and store data
            count = self._import_period_data(industry_code, start_date, end_date)
            return count

        except Exception as e:
            logger.error(f"Error importing data for industry {industry_code}: {e}")
            return -1

    def _import_period_data(self, industry_code: str, start_date: str, end_date: str) -> int:
        """Import period chart data for a specific industry.

        Args:
            industry_code: Industry code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Number of records imported
        """
        logger.info(f"Importing data for industry {industry_code} from {start_date} to {end_date}")

        try:
            # Split date range into chunks (max 50 weekdays per chunk)
            date_chunks = self._split_date_range_into_chunks(start_date, end_date, max_weekdays=50)
            logger.info(f"Split date range into {len(date_chunks)} chunk(s)")

            all_rows = []

            # Fetch data for each chunk
            for chunk_idx, (chunk_start, chunk_end) in enumerate(date_chunks, 1):
                logger.debug(f"Fetching chunk {chunk_idx}/{len(date_chunks)}: {chunk_start} to {chunk_end}")

                data = self._fetch_sector_period_data(industry_code, chunk_start, chunk_end)

                if data and data.get("output2"):
                    # Convert output2 items to rows, including output1 metadata
                    output1 = data.get("output1")
                    rows = self._prepare_industry_chart_rows(industry_code, data.get("output2", []), output1)
                    all_rows.extend(rows)
                    logger.debug(f"Got {len(rows)} records from chunk {chunk_idx}")

                # Rate limit: 10 requests per second (0.1s sleep)
                time.sleep(0.1)

            if all_rows:
                df = pd.DataFrame(all_rows)
                count = self.db_manager.insert_industry_daily_chart(industry_code, df)
                logger.info(f"Imported {count} records for industry {industry_code}")
                return count
            else:
                logger.warning(f"No data returned from API for industry {industry_code}")
                return 0

        except Exception as e:
            logger.error(f"Error importing period data for industry {industry_code}: {e}")
            raise

    def _fetch_sector_period_data(self, industry_code: str, start_date: str, end_date: str) -> SectorPeriodData:
        """Fetch sector period data from KIS API with retry logic.

        Args:
            industry_code: Industry code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Dictionary with output1 and output2 data
        """
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.domestic_issue_other.get_sector_period_quote(
                    fid_cond_mrkt_div_code="U",  # Sector
                    fid_input_iscd=industry_code,
                    fid_input_date_1=start_date,
                    fid_input_date_2=end_date,
                    fid_period_div_code="D",  # Daily
                )

                # Extract output1 and output2
                if not hasattr(response, "output1"):
                    raise ValueError("Response missing required 'output1' attribute")
                if not hasattr(response, "output2"):
                    raise ValueError("Response missing required 'output2' attribute")

                return SectorPeriodData(output1=response.output1, output2=response.output2)

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
            ) as e:
                # Network errors - retry with exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(
                        f"Network error fetching industry {industry_code}, retry {attempt + 1}/{max_retries} "
                        f"in {wait_time}s: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"Failed to fetch industry {industry_code} after {max_retries} network error retries: {e}"
                    )
                    raise

            except Exception as e:
                # API business logic errors (invalid token, bad params, etc) - fail immediately
                logger.error(f"API error fetching industry {industry_code} (no retry): {e}")
                raise

        # This should never be reached, but needed for type checking
        raise RuntimeError(f"Failed to fetch data for industry {industry_code} after {max_retries} attempts")

    def _prepare_industry_chart_rows(self, industry_code: str, output2: list, output1=None) -> list[dict]:
        """Prepare industry chart rows for insertion.

        Args:
            industry_code: Industry code
            output2: List of SectorPeriodQuoteItem2 objects
            output1: SectorPeriodQuoteItem1 object (metadata, optional)

        Returns:
            List of dictionaries to insert
        """
        rows = []

        # Extract fields from output1 (constant for all rows)
        prdy_vrss_sign = None
        bstp_nmix_prdy_ctrt = None
        prdy_nmix = None
        hts_kor_isnm = None
        bstp_cls_code = None
        prdy_vol = None

        if output1:
            prdy_vrss_sign = getattr(output1, "prdy_vrss_sign", None)
            bstp_nmix_prdy_ctrt_val: Any = getattr(output1, "bstp_nmix_prdy_ctrt", None)
            bstp_nmix_prdy_ctrt = pd.to_numeric(bstp_nmix_prdy_ctrt_val, errors="coerce")
            prdy_nmix_val: Any = getattr(output1, "prdy_nmix", None)
            prdy_nmix = pd.to_numeric(prdy_nmix_val, errors="coerce")
            hts_kor_isnm = getattr(output1, "hts_kor_isnm", None)
            bstp_cls_code = getattr(output1, "bstp_cls_code", None)
            prdy_vol_val: Any = getattr(output1, "prdy_vol", None)
            prdy_vol = pd.to_numeric(prdy_vol_val, errors="coerce")

        for item in output2:
            open_val: Any = item.bstp_nmix_oprc
            high_val: Any = item.bstp_nmix_hgpr
            low_val: Any = item.bstp_nmix_lwpr
            close_val: Any = item.bstp_nmix_prpr
            volume_val: Any = item.acml_vol
            trading_amount_val: Any = item.acml_tr_pbmn

            row = {
                "industry_code": industry_code,
                "date": pd.to_datetime(item.stck_bsop_date, format="%Y%m%d"),
                "open": pd.to_numeric(open_val, errors="coerce"),
                "high": pd.to_numeric(high_val, errors="coerce"),
                "low": pd.to_numeric(low_val, errors="coerce"),
                "close": pd.to_numeric(close_val, errors="coerce"),
                "volume": pd.to_numeric(volume_val, errors="coerce"),
                "trading_amount": pd.to_numeric(trading_amount_val, errors="coerce"),
                "mod_yn": getattr(item, "mod_yn", None),
                # From output1
                "prdy_vrss_sign": prdy_vrss_sign,
                "bstp_nmix_prdy_ctrt": bstp_nmix_prdy_ctrt,
                "prdy_nmix": prdy_nmix,
                "hts_kor_isnm": hts_kor_isnm,
                "bstp_cls_code": bstp_cls_code,
                "prdy_vol": prdy_vol,
            }
            rows.append(row)

        return rows

    def _split_date_range_into_chunks(
        self, start_date: str, end_date: str, max_weekdays: int = 50
    ) -> list[tuple[str, str]]:
        """Split date range into chunks not exceeding max weekdays.

        Args:
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            max_weekdays: Maximum weekdays per chunk (default: 50)

        Returns:
            List of (chunk_start, chunk_end) tuples
        """
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")

        chunks = []
        current_start = start

        while current_start <= end:
            # Find the end date for this chunk (not exceeding max_weekdays)
            current_date = current_start
            weekday_count = 0

            while current_date <= end and weekday_count < max_weekdays:
                if current_date.weekday() < 5:  # Monday=0 to Friday=4
                    weekday_count += 1
                if weekday_count < max_weekdays:
                    current_date += timedelta(days=1)

            # current_date is now the last date within max_weekdays or end date
            chunk_end = min(current_date, end)
            chunks.append((current_start.strftime("%Y%m%d"), chunk_end.strftime("%Y%m%d")))

            # Move to next day after chunk end
            current_start = chunk_end + timedelta(days=1)

        return chunks

    def _count_weekdays(self, start_date: str, end_date: str) -> int:
        """Count weekdays (Monday-Friday) between two dates.

        Args:
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Number of weekdays
        """
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")

        weekday_count = 0
        current = start
        while current <= end:
            if current.weekday() < 5:  # Monday=0, Friday=4
                weekday_count += 1
            current += timedelta(days=1)

        return weekday_count

    def import_batch(
        self,
        industry_codes: list[str],
        start_date: str,
        end_date: str,
        progress_callback: Optional[Callable] = None,
    ) -> dict:
        """Import data for multiple industries.

        Args:
            industry_codes: List of industry codes
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with results {industry_code: count}
        """
        results = {}
        total = len(industry_codes)

        for idx, industry_code in enumerate(industry_codes, 1):
            if progress_callback:
                progress_callback(idx, total, industry_code)

            try:
                results[industry_code] = self.import_industry_data(
                    industry_code,
                    start_date,
                    end_date,
                )
            except Exception as e:
                logger.error(f"Error importing industry {industry_code}: {e}")
                results[industry_code] = -1

        return results

    @staticmethod
    def _validate_date_format(date_str: str) -> bool:
        """Validate date format (YYYYMMDD).

        Args:
            date_str: Date string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def get_default_date_range(days_back: int = 1095) -> tuple[str, str]:
        """Get default date range (n days back from today).

        Args:
            days_back: Number of days to go back (default: 3 years = 1095 days)

        Returns:
            Tuple of (start_date, end_date) in YYYYMMDD format
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        return (start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))
