"""Stock chart data importer from KIS API."""

import time
from datetime import datetime, timedelta
from typing import Callable, Optional

import pandas as pd
import requests
from cluefin_openapi.kis._client import Client
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


class StockChartImporter:
    """Import stock chart data from KIS API to DuckDB."""

    def __init__(self, client: Client, db_manager: DuckDBManager):
        """Initialize chart data importer.

        Args:
            client: KIS API client
            db_manager: DuckDB manager instance
        """
        self.client = client
        self.db_manager = db_manager

    def import_stock_data(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        skip_existing: bool = True,
    ) -> int:
        """Import daily chart data for a single stock.

        Args:
            stock_code: Stock code (e.g., '005930')
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            skip_existing: Skip import if data already exists

        Returns:
            Number of records imported
        """
        stock_code = stock_code.strip()

        if not self._validate_date_format(start_date):
            raise ValueError(f"Invalid start date format: {start_date}")
        if not self._validate_date_format(end_date):
            raise ValueError(f"Invalid end date format: {end_date}")

        # Validate date range (max 100 weekdays)
        self._validate_date_range(start_date, end_date)

        try:
            # Check if data already exists
            if skip_existing and self.db_manager.check_stock_data_exists(stock_code, start_date, end_date):
                logger.info(f"Data already exists for {stock_code}, skipping...")
                return 0

            # Fetch and store data
            count = self._import_period_data(stock_code, start_date, end_date)
            return count

        except Exception as e:
            logger.error(f"Error importing data for {stock_code}: {e}")
            return -1

    def _import_period_data(self, stock_code: str, start_date: str, end_date: str) -> int:
        """Import period chart data for a specific stock.

        Args:
            stock_code: Stock code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Number of records imported
        """

        try:
            all_data = self._fetch_period_data(stock_code, start_date, end_date)

            if all_data:
                df = self._prepare_stock_chart_data(stock_code, all_data)
                count = self.db_manager.insert_stock_daily_chart(stock_code, df)
                return count
            else:
                logger.warning(f"No data returned from API for {stock_code}")
                return 0

        except Exception as e:
            logger.error(f"Error importing period data for {stock_code}: {e}")
            raise

    def _fetch_period_data(self, stock_code: str, start_date: str, end_date: str) -> dict:
        """Fetch period chart data from KIS API with retry logic.

        Args:
            stock_code: Stock code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Dictionary with output1 and output2 data
        """
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.domestic_basic_quote.get_stock_period_quote(
                    fid_cond_mrkt_div_code="J",  # KRX market
                    fid_input_iscd=stock_code,
                    fid_input_date_1=start_date,
                    fid_input_date_2=end_date,
                    fid_period_div_code="D",  # Daily
                    fid_org_adj_prc="1",  # Adjusted price
                )

                # Extract output1 and output2
                output1 = response.output1 if hasattr(response, "output1") else None
                output2 = response.output2 if hasattr(response, "output2") else []

                return {"output1": output1, "output2": output2}

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
            ) as e:
                # Network errors - retry with exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(
                        f"Network error fetching {stock_code}, retry {attempt + 1}/{max_retries} in {wait_time}s: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to fetch {stock_code} after {max_retries} network error retries: {e}")
                    raise

            except Exception as e:
                # API business logic errors (invalid token, bad params, etc) - fail immediately
                logger.error(f"API error fetching {stock_code} (no retry): {e}")
                raise

    def _prepare_stock_chart_data(self, stock_code: str, data: dict) -> pd.DataFrame:
        """Prepare stock chart data for insertion.

        Args:
            stock_code: Stock code
            data: Dictionary containing output1 and output2

        Returns:
            Prepared DataFrame
        """
        output1 = data.get("output1")
        output2 = data.get("output2", [])

        if not output2:
            return pd.DataFrame()

        # Extract fields from output1 (these are constant for all rows)
        vol_tnrt = getattr(output1, "vol_tnrt", None) if output1 else None
        lstn_stcn = getattr(output1, "lstn_stcn", None) if output1 else None
        hts_avls = getattr(output1, "hts_avls", None) if output1 else None
        per = getattr(output1, "per", None) if output1 else None
        eps = getattr(output1, "eps", None) if output1 else None
        pbr = getattr(output1, "pbr", None) if output1 else None

        # Convert output2 items to dict
        rows = []
        for item in output2:
            row = {
                "stock_code": stock_code,
                "date": pd.to_datetime(item.stck_bsop_date, format="%Y%m%d"),
                "open": pd.to_numeric(item.stck_oprc, errors="coerce"),
                "high": pd.to_numeric(item.stck_hgpr, errors="coerce"),
                "low": pd.to_numeric(item.stck_lwpr, errors="coerce"),
                "close": pd.to_numeric(item.stck_clpr, errors="coerce"),
                "volume": pd.to_numeric(item.acml_vol, errors="coerce"),
                "trading_amount": pd.to_numeric(item.acml_tr_pbmn, errors="coerce"),
                "flng_cls_code": item.flng_cls_code,
                "prtt_rate": pd.to_numeric(item.prtt_rate, errors="coerce"),
                "mod_yn": item.mod_yn,
                "prdy_vrss_sign": item.prdy_vrss_sign,
                "prdy_vrss": pd.to_numeric(item.prdy_vrss, errors="coerce"),
                "revl_issu_reas": item.revl_issu_reas,
                # From output1
                "vol_tnrt": pd.to_numeric(vol_tnrt, errors="coerce") if vol_tnrt is not None else None,
                "lstn_stcn": pd.to_numeric(lstn_stcn, errors="coerce") if lstn_stcn is not None else None,
                "hts_avls": pd.to_numeric(hts_avls, errors="coerce") if hts_avls is not None else None,
                "per": pd.to_numeric(per, errors="coerce") if per is not None else None,
                "eps": pd.to_numeric(eps, errors="coerce") if eps is not None else None,
                "pbr": pd.to_numeric(pbr, errors="coerce") if pbr is not None else None,
            }
            rows.append(row)

        return pd.DataFrame(rows)

    def _validate_date_range(self, start_date: str, end_date: str) -> None:
        """Validate that date range does not exceed 100 weekdays.

        Args:
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Raises:
            ValueError: If date range exceeds 100 weekdays
        """
        weekday_count = self._count_weekdays(start_date, end_date)
        if weekday_count > 100:
            raise ValueError(
                f"Date range exceeds 100 trading days (weekdays): {weekday_count} weekdays found. "
                f"Please use a smaller date range."
            )

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
        stock_codes: list[str],
        start_date: str,
        end_date: str,
        progress_callback: Optional[Callable] = None,
        skip_existing: bool = True,
    ) -> dict:
        """Import data for multiple stocks.

        Args:
            stock_codes: List of stock codes
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            progress_callback: Optional callback for progress updates
            skip_existing: Skip imports if data exists

        Returns:
            Dictionary with results {stock_code: count}
        """
        results = {}
        total = len(stock_codes)
        chunk_size = 10

        # Process in chunks of 10
        for chunk_start in range(0, len(stock_codes), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(stock_codes))
            chunk = stock_codes[chunk_start:chunk_end]

            # Batch check existence for this chunk
            if skip_existing:
                exists_map = self.db_manager.check_stock_data_exists_batch(chunk, start_date, end_date)
                existing_codes = [code for code, exists in exists_map.items() if exists]
                if existing_codes:
                    logger.info(f"Skipping {len(existing_codes)} existing stocks: {existing_codes}")
                    for code in existing_codes:
                        results[code] = 0  # Mark as skipped
            else:
                exists_map = {}

            # Process each stock in chunk sequentially
            logger.info(
                f"Stock charts import for stocks {chunk_start + 1} to {chunk_end} of {total}, start_date={start_date}, end_date={end_date}"
            )
            for stock_code in chunk:
                idx = stock_codes.index(stock_code) + 1

                if progress_callback:
                    progress_callback(idx, total, stock_code)

                # Skip if already exists (checked in batch above)
                if skip_existing and exists_map.get(stock_code, False):
                    continue

                try:
                    results[stock_code] = self.import_stock_data(
                        stock_code,
                        start_date,
                        end_date,
                        skip_existing=False,  # Already checked
                    )
                    # Rate limit: 10 requests per second (0.1s sleep)
                    # If use dev token, consider increasing delay (2 requests/sec)
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error importing {stock_code}: {e}")
                    results[stock_code] = -1

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
