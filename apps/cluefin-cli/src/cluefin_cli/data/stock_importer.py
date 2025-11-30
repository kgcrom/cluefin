"""Stock chart data importer from KIS API."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Optional

import pandas as pd
import requests
from cluefin_openapi import TokenBucket
from cluefin_openapi.kis._client import Client
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


@dataclass
class StockFetchResult:
    """Result container for a single stock fetch operation."""

    stock_code: str
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


class DomesticStockChartImporter:
    """Import domestic stock chart data from KIS API to DuckDB."""

    def __init__(
        self,
        client: Client,
        db_manager: DuckDBManager,
        rate_limit: float = 20.0,
        max_workers: int = 3,
    ):
        """Initialize chart data importer.

        Args:
            client: KIS API client
            db_manager: DuckDB manager instance
            rate_limit: API requests per second (default: 20)
            max_workers: Number of parallel workers (default: 3, max: 10)
        """
        self.client = client
        self.db_manager = db_manager
        self.rate_limit = rate_limit
        self.max_workers = min(max_workers, 10)
        self.rate_limiter = TokenBucket(
            capacity=int(rate_limit),
            refill_rate=rate_limit,
        )

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
            if skip_existing and self.db_manager.check_domestic_stock_data_exists(stock_code, start_date, end_date):
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
                count = self.db_manager.insert_domestic_stock_daily_chart(stock_code, df)
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

    def _create_worker_client(self) -> Client:
        """Create a new KIS client instance for worker thread.

        Each worker needs its own client because requests.Session is not thread-safe.

        Returns:
            New Client instance with same credentials
        """
        return Client(
            token=self.client.token,
            app_key=self.client.app_key,
            secret_key=self.client.secret_key,
            env=self.client.env,
            debug=self.client.debug,
        )

    def _fetch_single_stock_worker(
        self,
        worker_client: Client,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> StockFetchResult:
        """Worker function to fetch a single stock's data (thread-safe).

        Args:
            worker_client: KIS client for this worker
            stock_code: Stock code to fetch
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            StockFetchResult with fetched data or error
        """
        try:
            # Wait for rate limit token (thread-safe)
            if not self.rate_limiter.wait_for_tokens(1, timeout=30.0):
                return StockFetchResult(
                    stock_code=stock_code,
                    success=False,
                    error="Rate limit timeout",
                )

            # Make API call using worker's own client
            response = worker_client.domestic_basic_quote.get_stock_period_quote(
                fid_cond_mrkt_div_code="J",
                fid_input_iscd=stock_code,
                fid_input_date_1=start_date,
                fid_input_date_2=end_date,
                fid_period_div_code="D",
                fid_org_adj_prc="1",
            )

            output1 = response.output1 if hasattr(response, "output1") else None
            output2 = response.output2 if hasattr(response, "output2") else []

            return StockFetchResult(
                stock_code=stock_code,
                success=True,
                data={"output1": output1, "output2": output2},
            )

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
        ) as e:
            logger.warning(f"Network error fetching {stock_code}: {e}")
            return StockFetchResult(
                stock_code=stock_code,
                success=False,
                error=f"Network error: {e}",
            )
        except Exception as e:
            logger.error(f"Error fetching {stock_code}: {e}")
            return StockFetchResult(
                stock_code=stock_code,
                success=False,
                error=str(e),
            )

    def _process_chunk_parallel(
        self,
        stock_codes: list[str],
        start_date: str,
        end_date: str,
    ) -> list[StockFetchResult]:
        """Process a chunk of stocks in parallel using ThreadPoolExecutor.

        Args:
            stock_codes: List of stock codes to fetch
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            List of StockFetchResult for each stock
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for stock_code in stock_codes:
                worker_client = self._create_worker_client()
                future = executor.submit(
                    self._fetch_single_stock_worker,
                    worker_client,
                    stock_code,
                    start_date,
                    end_date,
                )
                futures[future] = stock_code

            for future in as_completed(futures):
                stock_code = futures[future]
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Worker error for {stock_code}: {e}")
                    results.append(
                        StockFetchResult(
                            stock_code=stock_code,
                            success=False,
                            error=str(e),
                        )
                    )

        return results

    def _save_chunk_results(self, results: list[StockFetchResult]) -> dict[str, int]:
        """Save all results from a chunk to database (main thread only).

        Args:
            results: List of fetch results

        Returns:
            Dictionary with {stock_code: record_count} (-1 for errors)
        """
        counts = {}

        for result in results:
            if not result.success:
                counts[result.stock_code] = -1
                continue

            if result.data is None or not result.data.get("output2"):
                counts[result.stock_code] = 0
                continue

            try:
                df = self._prepare_stock_chart_data(result.stock_code, result.data)
                count = self.db_manager.insert_domestic_stock_daily_chart(result.stock_code, df)
                counts[result.stock_code] = count
            except Exception as e:
                logger.error(f"Error saving {result.stock_code}: {e}")
                counts[result.stock_code] = -1

        return counts

    def import_batch(
        self,
        stock_codes: list[str],
        start_date: str,
        end_date: str,
        progress_callback: Optional[Callable] = None,
        skip_existing: bool = True,
        chunk_size: int = 10,
    ) -> dict:
        """Import data for multiple stocks using parallel fetching.

        Args:
            stock_codes: List of stock codes
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            progress_callback: Optional callback for progress updates
            skip_existing: Skip imports if data exists
            chunk_size: Number of stocks per chunk (default: 10)

        Returns:
            Dictionary with results {stock_code: count}
        """
        results = {}
        total = len(stock_codes)

        for chunk_start in range(0, len(stock_codes), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(stock_codes))
            chunk = stock_codes[chunk_start:chunk_end]

            # Batch check existence for this chunk
            if skip_existing:
                exists_map = self.db_manager.check_domestic_stock_data_exists_batch(chunk, start_date, end_date)
                existing_codes = [code for code, exists in exists_map.items() if exists]
                if existing_codes:
                    logger.info(f"Skipping {len(existing_codes)} existing stocks: {existing_codes}")
                    for code in existing_codes:
                        results[code] = 0
            else:
                exists_map = {}

            # Filter out existing codes
            codes_to_fetch = [code for code in chunk if not exists_map.get(code, False)]

            if codes_to_fetch:
                logger.info(
                    f"Stock charts import for stocks {chunk_start + 1} to {chunk_end} of {total}, "
                    f"fetching {len(codes_to_fetch)} stocks, start_date={start_date}, end_date={end_date}"
                )

                # Parallel fetch for this chunk
                fetch_results = self._process_chunk_parallel(codes_to_fetch, start_date, end_date)

                # Save all results to DB (main thread)
                chunk_results = self._save_chunk_results(fetch_results)
                results.update(chunk_results)

            # Update progress
            if progress_callback:
                progress_callback(chunk_end, total, chunk[-1])

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


class OverseasStockChartImporter:
    """Import overseas stock chart data from KIS API to DuckDB."""

    def __init__(
        self,
        client: Client,
        db_manager: DuckDBManager,
        rate_limit: float = 20.0,
        max_workers: int = 3,
    ):
        """Initialize overseas chart data importer.

        Args:
            client: KIS API client
            db_manager: DuckDB manager instance
            rate_limit: API requests per second (default: 20)
            max_workers: Number of parallel workers (default: 3, max: 10)
        """
        self.client = client
        self.db_manager = db_manager
        self.rate_limit = rate_limit
        self.max_workers = min(max_workers, 10)
        self.rate_limiter = TokenBucket(
            capacity=int(rate_limit),
            refill_rate=rate_limit,
        )

    def import_stock_data(
        self,
        exchange_code: str,
        stock_code: str,
        start_date: str,
        end_date: str,
        skip_existing: bool = True,
    ) -> int:
        """Import daily chart data for a single overseas stock.

        Args:
            exchange_code: Exchange code (NYS, NAS, AMS, HKS, TSE, etc.)
            stock_code: Stock code/symbol (e.g., TSLA)
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            skip_existing: Skip import if data already exists

        Returns:
            Number of records imported
        """
        exchange_code = exchange_code.strip().upper()
        stock_code = stock_code.strip().upper()

        if not self._validate_date_format(start_date):
            raise ValueError(f"Invalid start date format: {start_date}")
        if not self._validate_date_format(end_date):
            raise ValueError(f"Invalid end date format: {end_date}")

        try:
            # Check if data already exists
            if skip_existing and self.db_manager.check_overseas_stock_data_exists(
                exchange_code, stock_code, start_date, end_date
            ):
                logger.info(f"Data already exists for {exchange_code}:{stock_code}, skipping...")
                return 0

            # Fetch and store data
            count = self._fetch_and_store_data(exchange_code, stock_code, start_date, end_date)
            return count

        except Exception as e:
            logger.error(f"Error importing data for {exchange_code}:{stock_code}: {e}")
            return -1

    def _fetch_and_store_data(self, exchange_code: str, stock_code: str, start_date: str, end_date: str) -> int:
        """Fetch overseas stock data and store in database.

        Args:
            exchange_code: Exchange code
            stock_code: Stock code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Number of records imported
        """
        try:
            # Convert exchange code to API format (NYSE -> NYS, NASDAQ -> NAS)
            api_exchange_code = "NYS" if exchange_code == "NYSE" else "NAS"
            all_data = self._fetch_period_data(api_exchange_code, stock_code, end_date)

            if all_data:
                df = self._prepare_stock_chart_data(exchange_code, stock_code, all_data, start_date)
                count = self.db_manager.insert_overseas_stock_daily_chart(exchange_code, stock_code, df)
                return count
            else:
                logger.warning(f"No data returned from API for {exchange_code}:{stock_code}")
                return 0

        except Exception as e:
            logger.error(f"Error fetching data for {exchange_code}:{stock_code}: {e}")
            raise

    def _fetch_period_data(self, exchange_code: str, stock_code: str, base_date: str) -> dict:
        """Fetch period chart data from overseas KIS API with retry logic and pagination.

        Args:
            exchange_code: Exchange code
            stock_code: Stock code
            base_date: Based date (YYYYMMDD)

        Returns:
            Dictionary with output1 and output2 data
        """
        max_retries = 3
        keyb = ""  # Start with empty key for first request
        all_output2 = []
        output1 = None

        while True:
            for attempt in range(max_retries):
                try:
                    response = self.client.overseas_basic_quote.get_stock_period_quote(
                        auth="",
                        excd=exchange_code,
                        symb=stock_code,
                        gubn="0",  # Daily
                        bymd=base_date,  # Base date
                        modp="1",  # Adjusted price
                        keyb=keyb,
                    )

                    # Extract output1 and output2
                    output1 = response.output1 if hasattr(response, "output1") else None
                    output2 = response.output2 if hasattr(response, "output2") else []

                    all_output2.extend(output2)

                    # Check if there's more data to fetch (pagination)
                    # Note: Check if response has more data indicator
                    # For now, we assume single response contains all data
                    break

                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError,
                ) as e:
                    # Network errors - retry with exponential backoff
                    if attempt < max_retries - 1:
                        wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                        logger.warning(
                            f"Network error fetching {exchange_code}:{stock_code}, retry {attempt + 1}/{max_retries} in {wait_time}s: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"Failed to fetch {exchange_code}:{stock_code} after {max_retries} network error retries: {e}"
                        )
                        raise

                except Exception as e:
                    # API business logic errors (invalid token, bad params, etc) - fail immediately
                    logger.error(f"API error fetching {exchange_code}:{stock_code} (no retry): {e}")
                    raise

            # If no more data, break the loop
            if not all_output2 or not keyb:
                break

            time.sleep(0.1)  # Rate limit

        return {"output1": output1, "output2": all_output2}

    def _prepare_stock_chart_data(
        self, exchange_code: str, stock_code: str, data: dict, start_date: str = None
    ) -> pd.DataFrame:
        """Prepare overseas stock chart data for insertion.

        Args:
            exchange_code: Exchange code
            stock_code: Stock code
            data: Dictionary containing output1 and output2
            start_date: Start date (YYYYMMDD) for filtering data

        Returns:
            Prepared DataFrame
        """
        output1 = data.get("output1")
        output2 = data.get("output2", [])

        if not output2:
            return pd.DataFrame()

        # Extract fields from output1
        zdiv = getattr(output1, "zdiv", None) if output1 else None

        # Convert output2 items to dict
        rows = []
        for item in output2:
            item_date = pd.to_datetime(item.xymd, format="%Y%m%d")

            # Filter by start_date if provided
            if start_date:
                start_datetime = pd.to_datetime(start_date, format="%Y%m%d")
                if item_date < start_datetime:
                    continue

            row = {
                "exchange_code": exchange_code,
                "stock_code": stock_code,
                "date": item_date,
                "open": pd.to_numeric(item.open, errors="coerce"),
                "high": pd.to_numeric(item.high, errors="coerce"),
                "low": pd.to_numeric(item.low, errors="coerce"),
                "close": pd.to_numeric(item.clos, errors="coerce"),
                "volume": pd.to_numeric(item.tvol, errors="coerce"),
                "trading_amount": pd.to_numeric(item.tamt, errors="coerce"),
                "sign": item.sign,
                "diff": pd.to_numeric(item.diff, errors="coerce"),
                "rate": pd.to_numeric(item.rate, errors="coerce"),
                "zdiv": zdiv,
            }
            rows.append(row)

        return pd.DataFrame(rows)

    def _create_worker_client(self) -> Client:
        """Create a new KIS client instance for worker thread.

        Returns:
            New Client instance with same credentials
        """
        return Client(
            token=self.client.token,
            app_key=self.client.app_key,
            secret_key=self.client.secret_key,
            env=self.client.env,
            debug=self.client.debug,
        )

    def _fetch_single_stock_worker(
        self,
        worker_client: Client,
        exchange_code: str,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> StockFetchResult:
        """Worker function to fetch a single overseas stock's data (thread-safe).

        Args:
            worker_client: KIS client for this worker
            exchange_code: Exchange code (NYS, NAS, etc.)
            stock_code: Stock code to fetch
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            StockFetchResult with fetched data or error
        """
        try:
            # Wait for rate limit token (thread-safe)
            if not self.rate_limiter.wait_for_tokens(1, timeout=30.0):
                return StockFetchResult(
                    stock_code=stock_code,
                    success=False,
                    error="Rate limit timeout",
                )

            # Convert exchange code to API format
            api_exchange_code = "NYS" if exchange_code == "NYSE" else "NAS"

            # Make API call using worker's own client
            response = worker_client.overseas_basic_quote.get_stock_period_quote(
                auth="",
                excd=api_exchange_code,
                symb=stock_code,
                gubn="0",
                bymd=end_date,
                modp="1",
                keyb="",
            )

            output1 = response.output1 if hasattr(response, "output1") else None
            output2 = response.output2 if hasattr(response, "output2") else []

            return StockFetchResult(
                stock_code=stock_code,
                success=True,
                data={"output1": output1, "output2": output2, "start_date": start_date},
            )

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
        ) as e:
            logger.warning(f"Network error fetching {exchange_code}:{stock_code}: {e}")
            return StockFetchResult(
                stock_code=stock_code,
                success=False,
                error=f"Network error: {e}",
            )
        except Exception as e:
            logger.error(f"Error fetching {exchange_code}:{stock_code}: {e}")
            return StockFetchResult(
                stock_code=stock_code,
                success=False,
                error=str(e),
            )

    def _process_chunk_parallel(
        self,
        exchange_code: str,
        stock_codes: list[str],
        start_date: str,
        end_date: str,
    ) -> list[StockFetchResult]:
        """Process a chunk of overseas stocks in parallel.

        Args:
            exchange_code: Exchange code
            stock_codes: List of stock codes to fetch
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            List of StockFetchResult for each stock
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for stock_code in stock_codes:
                worker_client = self._create_worker_client()
                future = executor.submit(
                    self._fetch_single_stock_worker,
                    worker_client,
                    exchange_code,
                    stock_code,
                    start_date,
                    end_date,
                )
                futures[future] = stock_code

            for future in as_completed(futures):
                stock_code = futures[future]
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Worker error for {stock_code}: {e}")
                    results.append(
                        StockFetchResult(
                            stock_code=stock_code,
                            success=False,
                            error=str(e),
                        )
                    )

        return results

    def _save_chunk_results(
        self,
        exchange_code: str,
        results: list[StockFetchResult],
    ) -> dict[str, int]:
        """Save all results from a chunk to database (main thread only).

        Args:
            exchange_code: Exchange code
            results: List of fetch results

        Returns:
            Dictionary with {stock_code: record_count} (-1 for errors)
        """
        counts = {}

        for result in results:
            if not result.success:
                counts[result.stock_code] = -1
                continue

            if result.data is None or not result.data.get("output2"):
                counts[result.stock_code] = 0
                continue

            try:
                start_date = result.data.get("start_date")
                df = self._prepare_stock_chart_data(
                    exchange_code,
                    result.stock_code,
                    result.data,
                    start_date,
                )
                count = self.db_manager.insert_overseas_stock_daily_chart(exchange_code, result.stock_code, df)
                counts[result.stock_code] = count
            except Exception as e:
                logger.error(f"Error saving {exchange_code}:{result.stock_code}: {e}")
                counts[result.stock_code] = -1

        return counts

    def import_batch(
        self,
        exchange_code: str,
        stock_codes: list[str],
        start_date: str,
        end_date: str,
        progress_callback: Optional[Callable] = None,
        skip_existing: bool = True,
        chunk_size: int = 10,
    ) -> dict:
        """Import data for multiple overseas stocks using parallel fetching.

        Args:
            exchange_code: Exchange code (NYS, NAS, AMS, HKS, TSE, etc.)
            stock_codes: List of stock codes/symbols
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            progress_callback: Optional callback for progress updates
            skip_existing: Skip imports if data exists
            chunk_size: Number of stocks per chunk (default: 10)

        Returns:
            Dictionary with results {stock_code: count}
        """
        results = {}
        total = len(stock_codes)

        for chunk_start in range(0, len(stock_codes), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(stock_codes))
            chunk = stock_codes[chunk_start:chunk_end]

            # Batch check existence for this chunk
            if skip_existing:
                exists_map = self.db_manager.check_overseas_stock_data_exists_batch(
                    exchange_code, chunk, start_date, end_date
                )
                existing_codes = [code for code, exists in exists_map.items() if exists]
                if existing_codes:
                    logger.info(f"Skipping {len(existing_codes)} existing stocks: {existing_codes}")
                    for code in existing_codes:
                        results[code] = 0
            else:
                exists_map = {}

            # Filter out existing codes
            codes_to_fetch = [code for code in chunk if not exists_map.get(code, False)]

            if codes_to_fetch:
                logger.info(
                    f"Overseas stock charts import for {exchange_code} stocks {chunk_start + 1} to {chunk_end} of {total}, "
                    f"fetching {len(codes_to_fetch)} stocks, start_date={start_date}, end_date={end_date}"
                )

                # Parallel fetch for this chunk
                fetch_results = self._process_chunk_parallel(exchange_code, codes_to_fetch, start_date, end_date)

                # Save all results to DB (main thread)
                chunk_results = self._save_chunk_results(exchange_code, fetch_results)
                results.update(chunk_results)

            # Update progress
            if progress_callback:
                progress_callback(chunk_end, total, chunk[-1])

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
