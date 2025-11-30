"""Stock list fetcher from Kiwoom API and KIS API."""

import logging
import os
import shutil
import tempfile
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from cluefin_openapi import TokenBucket
from cluefin_openapi.kis._client import Client as KisClient
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import DomesticStockInfoSummary, DomesticStockInfoSummaryItem
from cluefin_openapi.kiwoom._model import KiwoomHttpResponse

from cluefin_cli.data.duckdb_manager import DuckDBManager

logger = logging.getLogger(__name__)


@dataclass
class MetadataFetchResult:
    """Result container for metadata fetch operation."""

    stock_code: str
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    skipped: bool = False  # For ETF skip case


class StockListFetcher:
    """Fetch stock lists from Kiwoom API and overseas stocks from KIS API."""

    def __init__(
        self,
        client: Client,
        db_manager: DuckDBManager,
        kis_client: Optional[KisClient] = None,
        rate_limit: float = 20.0,
        max_workers: int = 3,
    ):
        """Initialize stock list fetcher.

        Args:
            client: Kiwoom API client
            db_manager: DuckDB manager instance
            kis_client: KIS API client (optional, required for overseas stocks)
            rate_limit: API requests per second (default: 20)
            max_workers: Number of parallel workers (default: 3, max: 10)
        """
        self.client = client
        self.db_manager = db_manager
        self.kis_client = kis_client
        self.rate_limit = rate_limit
        self.max_workers = min(max_workers, 10)
        self.rate_limiter = TokenBucket(
            capacity=int(rate_limit),
            refill_rate=rate_limit,
        )

    def get_all_stocks(self, market: Optional[str] = None) -> list[DomesticStockInfoSummaryItem]:
        """Get all listed stocks from Kiwoom API.

        Args:
            market: Filter by market ('kospi', 'kosdaq', or None for all)

        Returns:
            List of stock codes
        """
        stocks: list[DomesticStockInfoSummaryItem] = []

        # Get KOSPI stocks (mrkt_tp = '0')
        if market is None or market.lower() == "kospi":
            try:
                logger.info("Fetching KOSPI stocks from Kiwoom API...")
                response = self.client.stock_info.get_stock_info_summary(mrkt_tp="0")
                kospi_stocks = self._parse_stocks_from_response(response)
                stocks.extend(kospi_stocks)
                logger.info(f"Found {len(kospi_stocks)} KOSPI stocks")
            except Exception as e:
                logger.error(f"Error fetching KOSPI stocks: {e}")

        # Get KOSDAQ stocks (mrkt_tp = '10')
        if market is None or market.lower() == "kosdaq":
            try:
                logger.info("Fetching KOSDAQ stocks from Kiwoom API...")
                response = self.client.stock_info.get_stock_info_summary(mrkt_tp="10")
                kosdaq_stocks = self._parse_stocks_from_response(response)
                stocks.extend(kosdaq_stocks)
                logger.info(f"Found {len(kosdaq_stocks)} KOSDAQ stocks")
            except Exception as e:
                logger.error(f"Error fetching KOSDAQ stocks: {e}")

        stocks = sorted(stocks, key=lambda x: x.code)
        logger.info(f"Total unique stocks: {len(stocks)}")

        return stocks

    def _parse_stocks_from_response(
        self, response: KiwoomHttpResponse[DomesticStockInfoSummary]
    ) -> list[DomesticStockInfoSummaryItem]:
        """Parse stock codes from API response.

        Args:
            response: Kiwoom API response object

        Returns:
            List of stock codes
        """
        stocks = []

        try:
            for item in response.body.list:
                # 6자리 숫자 코드이고 1의 자리가 0이 아닌 경우에는 우선주이므로 제외
                if not item.code or len(item.code) != 6 or not item.code.isdigit() or int(item.code) % 10 != 0:
                    continue
                if item.marketName == "거래소" or item.marketName == "코스닥":
                    stocks.append(item)
        except Exception as e:
            logger.error(f"Error parsing stock response: {e}")

        return stocks

    def fetch_domestic_stock_metadata_extended(self, stock_info: DomesticStockInfoSummaryItem) -> Optional[dict]:
        """Fetch extended domestic stock metadata by combining two APIs.

        Fetches data from both get_stock_info_v1 and get_stock_info APIs,
        combining them into a single metadata dictionary.

        Note: This method does NOT save to database. Use fetch_and_save_metadata_batch
        for batch processing with automatic DB saving.

        Args:
            stock_info: Stock info to fetch metadata for

        Returns:
            Dictionary with combined metadata fields, or None if API fails.
            Fields include both v1 API fields and get_stock_info fields.
        """

        try:
            v1_data = stock_info

            # Fetch from get_stock_info API
            logger.debug(f"Fetching metadata from get_stock_info for {stock_info.code}...")
            response_basic = self.client.stock_info.get_stock_info(stock_info.code)
            basic_data = response_basic.body

            # Combine data from both APIs
            metadata = {
                "stock_code": v1_data.code,
                # From get_stock_info_v1
                "stock_name": v1_data.name,
                "listing_date": self._parse_date(v1_data.regDay),
                "market_name": v1_data.marketName,
                "market_code": v1_data.marketCode,
                "industry_name": v1_data.upName,
                "company_size": v1_data.upSizeName,
                "company_class": v1_data.companyClassName,
                "audit_info": v1_data.auditInfo,
                "stock_state": v1_data.state,
                "investment_warning": v1_data.orderWarning if v1_data.orderWarning else None,
                # From get_stock_info
                "settlement_month": basic_data.setl_mm,
                "face_value": self._parse_decimal(basic_data.fav),
                "capital": self._parse_int(basic_data.cap),
                "float_stock": self._parse_int(basic_data.flo_stk),
                "per": self._parse_decimal(basic_data.per),
                "eps": self._parse_decimal(basic_data.eps),
                "roe": self._parse_decimal(basic_data.roe),
                "pbr": self._parse_decimal(basic_data.pbr),
                "bps": self._parse_decimal(basic_data.bps),
                "sales_amount": self._parse_int(basic_data.sale_amt),
                "business_profit": self._parse_int(basic_data.bus_pro),
                "net_income": self._parse_int(basic_data.cup_nga),
                "market_cap": self._parse_int(basic_data.mac),
                "foreign_ownership_rate": self._parse_decimal(basic_data.for_exh_rt),
                "distribution_rate": self._parse_decimal(basic_data.dstr_rt),
                "distribution_stock": self._parse_int(basic_data.dstr_stk),
            }

            return metadata

        except Exception as e:
            logger.error(f"Error fetching extended metadata for {stock_info}: {e}")
            return None

    def _create_kiwoom_worker_client(self) -> Client:
        """Create a new Kiwoom client instance for worker thread."""
        # Determine env from URL
        env = "dev" if "mockapi" in self.client.url else "prod"
        return Client(
            token=self.client.token,
            env=env,
            timeout=self.client.timeout,
            max_retries=self.client.max_retries,
            debug=self.client.debug,
        )

    def _create_kis_worker_client(self) -> Optional[KisClient]:
        """Create a new KIS client instance for worker thread."""
        if self.kis_client is None:
            return None
        return KisClient(
            token=self.kis_client.token,
            app_key=self.kis_client.app_key,
            secret_key=self.kis_client.secret_key,
            env=self.kis_client.env,
            debug=self.kis_client.debug,
        )

    def _fetch_domestic_metadata_worker(
        self,
        worker_client: Client,
        stock_info: DomesticStockInfoSummaryItem,
    ) -> MetadataFetchResult:
        """Worker function to fetch domestic stock metadata (thread-safe)."""
        try:
            if not self.rate_limiter.wait_for_tokens(1, timeout=30.0):
                return MetadataFetchResult(
                    stock_code=stock_info.code,
                    success=False,
                    error="Rate limit timeout",
                )

            # Fetch from get_stock_info API using worker client
            response_basic = worker_client.stock_info.get_stock_info(stock_info.code)
            basic_data = response_basic.body

            metadata = {
                "stock_code": stock_info.code,
                "stock_name": stock_info.name,
                "listing_date": self._parse_date(stock_info.regDay),
                "market_name": stock_info.marketName,
                "market_code": stock_info.marketCode,
                "industry_name": stock_info.upName,
                "company_size": stock_info.upSizeName,
                "company_class": stock_info.companyClassName,
                "audit_info": stock_info.auditInfo,
                "stock_state": stock_info.state,
                "investment_warning": stock_info.orderWarning if stock_info.orderWarning else None,
                "settlement_month": basic_data.setl_mm,
                "face_value": self._parse_decimal(basic_data.fav),
                "capital": self._parse_int(basic_data.cap),
                "float_stock": self._parse_int(basic_data.flo_stk),
                "per": self._parse_decimal(basic_data.per),
                "eps": self._parse_decimal(basic_data.eps),
                "roe": self._parse_decimal(basic_data.roe),
                "pbr": self._parse_decimal(basic_data.pbr),
                "bps": self._parse_decimal(basic_data.bps),
                "sales_amount": self._parse_int(basic_data.sale_amt),
                "business_profit": self._parse_int(basic_data.bus_pro),
                "net_income": self._parse_int(basic_data.cup_nga),
                "market_cap": self._parse_int(basic_data.mac),
                "foreign_ownership_rate": self._parse_decimal(basic_data.for_exh_rt),
                "distribution_rate": self._parse_decimal(basic_data.dstr_rt),
                "distribution_stock": self._parse_int(basic_data.dstr_stk),
            }

            return MetadataFetchResult(
                stock_code=stock_info.code,
                success=True,
                data=metadata,
            )

        except Exception as e:
            logger.error(f"Error fetching metadata for {stock_info.code}: {e}")
            return MetadataFetchResult(
                stock_code=stock_info.code,
                success=False,
                error=str(e),
            )

    def _process_domestic_chunk_parallel(
        self,
        stock_infos: list[DomesticStockInfoSummaryItem],
    ) -> list[MetadataFetchResult]:
        """Process a chunk of domestic stocks in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for stock_info in stock_infos:
                worker_client = self._create_kiwoom_worker_client()
                future = executor.submit(
                    self._fetch_domestic_metadata_worker,
                    worker_client,
                    stock_info,
                )
                futures[future] = stock_info.code

            for future in as_completed(futures):
                stock_code = futures[future]
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Worker error for {stock_code}: {e}")
                    results.append(
                        MetadataFetchResult(
                            stock_code=stock_code,
                            success=False,
                            error=str(e),
                        )
                    )

        return results

    def _save_domestic_chunk_results(self, results: list[MetadataFetchResult]) -> tuple[int, int]:
        """Save domestic metadata results to database."""
        metadata_list = []
        failed = 0

        for result in results:
            if not result.success:
                failed += 1
                continue
            if result.data:
                metadata_list.append(result.data)

        if metadata_list:
            df = pd.DataFrame(metadata_list)
            count = self.db_manager.upsert_domestic_stock_metadata_extended(df)
            return count, failed
        return 0, failed

    def fetch_and_save_domestic_metadata_batch(
        self, stock_infos: list[DomesticStockInfoSummaryItem], chunk_size: int = 100
    ) -> tuple[int, int]:
        """Fetch metadata for multiple stocks and save to database in chunks using parallel processing.

        Args:
            stock_infos: List of stock info objects to fetch metadata for
            chunk_size: Number of stocks to process per chunk (default: 100)

        Returns:
            Tuple of (success_count, failed_count)
        """
        total_stocks = len(stock_infos)
        total_success = 0
        total_failed = 0

        num_chunks = (total_stocks + chunk_size - 1) // chunk_size
        logger.info(f"Processing {total_stocks} stocks in {num_chunks} chunks of {chunk_size} (parallel)...")

        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * chunk_size
            chunk_end = min(chunk_start + chunk_size, total_stocks)
            chunk = stock_infos[chunk_start:chunk_end]

            logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Processing stocks {chunk_start + 1}-{chunk_end}...")

            # Parallel fetch for this chunk
            fetch_results = self._process_domestic_chunk_parallel(chunk)

            # Save results to DB (main thread)
            chunk_success, chunk_failed = self._save_domestic_chunk_results(fetch_results)
            total_success += chunk_success
            total_failed += chunk_failed

            logger.info(
                f"[Chunk {chunk_idx + 1}/{num_chunks}] Complete - Success: {chunk_success}, Failed: {chunk_failed}"
            )

        logger.info(f"Batch processing complete - Total success: {total_success}, Total failed: {total_failed}")
        return total_success, total_failed

    def _parse_date(self, value: Optional[str]) -> Optional[str]:
        """Parse date string to YYYY-MM-DD format.

        Args:
            value: Date string (may be in YYYYMMDD or other format)

        Returns:
            Date string in YYYY-MM-DD format, or None
        """
        if not value:
            return None
        try:
            # Try parsing as YYYYMMDD format
            if isinstance(value, str) and len(value) == 8 and value.isdigit():
                return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"
            return str(value)
        except Exception:
            return None

    def _parse_decimal(self, value: Optional[str]) -> Optional[float]:
        """Parse decimal value safely.

        Args:
            value: Value to parse

        Returns:
            Float value, or None if conversion fails
        """
        if value is None or value == "":
            return None
        try:
            # Remove any whitespace and convert
            cleaned = str(value).strip()
            return float(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    def _parse_int(self, value: Optional[str]) -> Optional[int]:
        """Parse integer value safely.

        Args:
            value: Value to parse

        Returns:
            Integer value, or None if conversion fails
        """
        if value is None or value == "":
            return None
        try:
            # Remove any whitespace, commas, and convert
            cleaned = str(value).strip().replace(",", "")
            return int(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None

    def _download_overseas_master(self, exchange: str) -> pd.DataFrame:
        """Download overseas stock master file from Kiwoom.

        Args:
            exchange: Exchange code ('nas' for NASDAQ, 'nys' for NYSE)

        Returns:
            DataFrame with overseas stock master data

        Raises:
            Exception: If download or parsing fails
        """
        try:
            import ssl

            # Disable SSL verification for master file download
            ssl._create_default_https_context = ssl._create_unverified_context

            # Download master file zip
            url = f"https://new.real.download.dws.co.kr/common/master/{exchange}mst.cod.zip"
            temp_dir = tempfile.mkdtemp()

            zip_path = os.path.join(temp_dir, f"{exchange}mst.cod.zip")
            logger.debug(f"Downloading master file from {url}...")
            urllib.request.urlretrieve(url, zip_path)

            # Extract zip file
            with zipfile.ZipFile(zip_path) as zip_ref:
                zip_ref.extractall(temp_dir)

            # Read the master file
            master_path = os.path.join(temp_dir, f"{exchange}mst.cod")
            columns = [
                "National code",
                "Exchange id",
                "Exchange code",
                "Exchange name",
                "Symbol",
                "realtime symbol",
                "Korea name",
                "English name",
                "Security type",
                "currency",
                "float position",
                "data type",
                "base price",
                "Bid order size",
                "Ask order size",
                "market start time",
                "market end time",
                "DR 여부",
                "DR 국가코드",
                "업종분류코드",
                "지수구성종목 존재 여부",
                "Tick size Type",
                "구분코드",
                "Tick size type 상세",
            ]

            logger.info(f"Reading master file from {master_path}...")
            df = pd.read_table(master_path, sep="\t", encoding="cp949")
            df.columns = columns

            # Clean up temp directory
            shutil.rmtree(temp_dir)

            logger.info(f"Downloaded {len(df)} stocks from {exchange} master file")
            return df

        except Exception as e:
            logger.error(f"Error downloading overseas master file for {exchange}: {e}")
            raise

    def get_all_overseas_stocks(self, market: Optional[str] = None) -> pd.DataFrame:
        """Get all overseas stocks from master file.

        Args:
            market: Filter by market ('nasdaq', 'nyse', or None for all)

        Returns:
            DataFrame with overseas stocks
        """
        stocks: list[pd.DataFrame] = []

        # Get NASDAQ stocks
        if market is None or market.lower() == "nasdaq":
            try:
                logger.info("Fetching NASDAQ stocks from master file...")
                nasdaq_stocks = self._download_overseas_master("nas")
                stocks.append(nasdaq_stocks)
                logger.info(f"Found {len(nasdaq_stocks)} NASDAQ stocks")
            except Exception as e:
                logger.error(f"Error fetching NASDAQ stocks: {e}")

        # Get NYSE stocks
        if market is None or market.lower() == "nyse":
            try:
                logger.info("Fetching NYSE stocks from master file...")
                nyse_stocks = self._download_overseas_master("nys")
                stocks.append(nyse_stocks)
                logger.info(f"Found {len(nyse_stocks)} NYSE stocks")
            except Exception as e:
                logger.error(f"Error fetching NYSE stocks: {e}")

        if not stocks:
            logger.warning("No overseas stocks fetched")
            return pd.DataFrame()

        result = pd.concat(stocks, ignore_index=True)

        # Filter by Security type 2 (Stock only)
        before_filter = len(result)
        result = result[result["Security type"] == 2]
        logger.info(f"Filtered {before_filter - len(result)} non-stock items (ETF, etc.)")

        result = result.sort_values("Symbol").reset_index(drop=True)
        logger.info(f"Total unique overseas stocks: {len(result)}")

        return result

    def fetch_overseas_stock_metadata_extended(self, stock_row: pd.Series) -> Optional[dict]:
        """Fetch extended overseas stock metadata by calling KIS API.

        Args:
            stock_row: Row from master file DataFrame with stock information

        Returns:
            Dictionary with combined metadata fields, or None if API fails
        """
        if self.kis_client is None:
            logger.warning("KIS client not initialized, skipping metadata fetch")
            return None

        try:
            symbol = stock_row["Symbol"]
            exchange_code = stock_row["Exchange code"]

            # Map exchange code to prdt_type_cd for ProductBaseInfo API
            # 512: NASDAQ, 513: NYSE
            prdt_type_cd_map = {"NAS": "512", "NYS": "513"}
            prdt_type_cd = prdt_type_cd_map.get(exchange_code)

            if not prdt_type_cd:
                logger.warning(f"Unknown exchange code {exchange_code}, skipping {symbol}")
                return None

            logger.debug(f"Fetching product info for {symbol} ({exchange_code})...")
            response = self.kis_client.overseas_basic_quote.get_product_base_info(
                prdt_type_cd=prdt_type_cd, pdno=symbol
            )

            # Extract data from response
            if response.output:
                product_info = response.output

                etf_risk_code = getattr(product_info, "ovrs_stck_etf_risk_drtp_cd", None)
                if etf_risk_code and etf_risk_code.strip():
                    logger.info(f"  Skipping ETF: {symbol} (etf_risk_code={etf_risk_code})")
                    return "ETF_SKIPPED"

                metadata = {
                    "stock_code": symbol,
                    # From master file
                    "stock_name_en": stock_row["English name"],
                    "stock_name_kr": stock_row["Korea name"],
                    # From ProductBaseInfo API (ProductBaseInfoItem fields)
                    "std_pdno": product_info.std_pdno if hasattr(product_info, "std_pdno") else None,
                    "prdt_eng_name": product_info.prdt_eng_name if hasattr(product_info, "prdt_eng_name") else None,
                    "natn_cd": product_info.natn_cd if hasattr(product_info, "natn_cd") else None,
                    "natn_name": product_info.natn_name if hasattr(product_info, "natn_name") else None,
                    "tr_mket_cd": product_info.tr_mket_cd if hasattr(product_info, "tr_mket_cd") else None,
                    "tr_mket_name": product_info.tr_mket_name if hasattr(product_info, "tr_mket_name") else None,
                    "ovrs_excg_cd": product_info.ovrs_excg_cd if hasattr(product_info, "ovrs_excg_cd") else None,
                    "ovrs_excg_name": product_info.ovrs_excg_name if hasattr(product_info, "ovrs_excg_name") else None,
                    "tr_crcy_cd": product_info.tr_crcy_cd if hasattr(product_info, "tr_crcy_cd") else None,
                    "ovrs_papr": product_info.ovrs_papr if hasattr(product_info, "ovrs_papr") else None,
                    "crcy_name": product_info.crcy_name if hasattr(product_info, "crcy_name") else None,
                    "ovrs_stck_dvsn_cd": product_info.ovrs_stck_dvsn_cd
                    if hasattr(product_info, "ovrs_stck_dvsn_cd")
                    else None,
                    "prdt_clsf_cd": product_info.prdt_clsf_cd if hasattr(product_info, "prdt_clsf_cd") else None,
                    "prdt_clsf_name": product_info.prdt_clsf_name if hasattr(product_info, "prdt_clsf_name") else None,
                    "lstg_stck_num": product_info.lstg_stck_num if hasattr(product_info, "lstg_stck_num") else None,
                    "lstg_dt": product_info.lstg_dt if hasattr(product_info, "lstg_dt") else None,
                    "ovrs_stck_tr_stop_dvsn_cd": product_info.ovrs_stck_tr_stop_dvsn_cd
                    if hasattr(product_info, "ovrs_stck_tr_stop_dvsn_cd")
                    else None,
                    "lstg_abol_item_yn": product_info.lstg_abol_item_yn
                    if hasattr(product_info, "lstg_abol_item_yn")
                    else None,
                    "lstg_yn": product_info.lstg_yn if hasattr(product_info, "lstg_yn") else None,
                    "tax_levy_yn": product_info.tax_levy_yn if hasattr(product_info, "tax_levy_yn") else None,
                    "ovrs_item_name": product_info.ovrs_item_name if hasattr(product_info, "ovrs_item_name") else None,
                    "sedol_no": product_info.sedol_no if hasattr(product_info, "sedol_no") else None,
                    "prdt_name": product_info.prdt_name if hasattr(product_info, "prdt_name") else None,
                    "lstg_abol_dt": product_info.lstg_abol_dt if hasattr(product_info, "lstg_abol_dt") else None,
                    "ptp_item_yn": product_info.ptp_item_yn if hasattr(product_info, "ptp_item_yn") else None,
                    "dtm_tr_psbl_yn": product_info.dtm_tr_psbl_yn if hasattr(product_info, "dtm_tr_psbl_yn") else None,
                    "ovrs_stck_etf_risk_drtp_cd": product_info.ovrs_stck_etf_risk_drtp_cd
                    if hasattr(product_info, "ovrs_stck_etf_risk_drtp_cd")
                    else None,
                }

                return metadata
            else:
                logger.warning(f"No product info returned for {symbol}")
                return None

        except Exception as e:
            logger.error(f"Error fetching metadata for {stock_row.get('Symbol', 'unknown')}: {e}")
            return None

    def _fetch_overseas_metadata_worker(
        self,
        worker_client: KisClient,
        stock_row: pd.Series,
    ) -> MetadataFetchResult:
        """Worker function to fetch overseas stock metadata (thread-safe)."""
        symbol = stock_row["Symbol"]
        exchange_code = stock_row["Exchange code"]

        try:
            if not self.rate_limiter.wait_for_tokens(1, timeout=30.0):
                return MetadataFetchResult(
                    stock_code=symbol,
                    success=False,
                    error="Rate limit timeout",
                )

            prdt_type_cd_map = {"NAS": "512", "NYS": "513"}
            prdt_type_cd = prdt_type_cd_map.get(exchange_code)

            if not prdt_type_cd:
                return MetadataFetchResult(
                    stock_code=symbol,
                    success=False,
                    error=f"Unknown exchange code {exchange_code}",
                )

            response = worker_client.overseas_basic_quote.get_product_base_info(
                prdt_type_cd=prdt_type_cd, pdno=symbol
            )

            if response.output:
                product_info = response.output

                etf_risk_code = getattr(product_info, "ovrs_stck_etf_risk_drtp_cd", None)
                if etf_risk_code and etf_risk_code.strip():
                    return MetadataFetchResult(
                        stock_code=symbol,
                        success=True,
                        skipped=True,
                    )

                metadata = {
                    "stock_code": symbol,
                    "stock_name_en": stock_row["English name"],
                    "stock_name_kr": stock_row["Korea name"],
                    "std_pdno": getattr(product_info, "std_pdno", None),
                    "prdt_eng_name": getattr(product_info, "prdt_eng_name", None),
                    "natn_cd": getattr(product_info, "natn_cd", None),
                    "natn_name": getattr(product_info, "natn_name", None),
                    "tr_mket_cd": getattr(product_info, "tr_mket_cd", None),
                    "tr_mket_name": getattr(product_info, "tr_mket_name", None),
                    "ovrs_excg_cd": getattr(product_info, "ovrs_excg_cd", None),
                    "ovrs_excg_name": getattr(product_info, "ovrs_excg_name", None),
                    "tr_crcy_cd": getattr(product_info, "tr_crcy_cd", None),
                    "ovrs_papr": getattr(product_info, "ovrs_papr", None),
                    "crcy_name": getattr(product_info, "crcy_name", None),
                    "ovrs_stck_dvsn_cd": getattr(product_info, "ovrs_stck_dvsn_cd", None),
                    "prdt_clsf_cd": getattr(product_info, "prdt_clsf_cd", None),
                    "prdt_clsf_name": getattr(product_info, "prdt_clsf_name", None),
                    "lstg_stck_num": getattr(product_info, "lstg_stck_num", None),
                    "lstg_dt": getattr(product_info, "lstg_dt", None),
                    "ovrs_stck_tr_stop_dvsn_cd": getattr(product_info, "ovrs_stck_tr_stop_dvsn_cd", None),
                    "lstg_abol_item_yn": getattr(product_info, "lstg_abol_item_yn", None),
                    "lstg_yn": getattr(product_info, "lstg_yn", None),
                    "tax_levy_yn": getattr(product_info, "tax_levy_yn", None),
                    "ovrs_item_name": getattr(product_info, "ovrs_item_name", None),
                    "sedol_no": getattr(product_info, "sedol_no", None),
                    "prdt_name": getattr(product_info, "prdt_name", None),
                    "lstg_abol_dt": getattr(product_info, "lstg_abol_dt", None),
                    "ptp_item_yn": getattr(product_info, "ptp_item_yn", None),
                    "dtm_tr_psbl_yn": getattr(product_info, "dtm_tr_psbl_yn", None),
                    "ovrs_stck_etf_risk_drtp_cd": getattr(product_info, "ovrs_stck_etf_risk_drtp_cd", None),
                }

                return MetadataFetchResult(
                    stock_code=symbol,
                    success=True,
                    data=metadata,
                )
            else:
                return MetadataFetchResult(
                    stock_code=symbol,
                    success=False,
                    error="No product info returned",
                )

        except Exception as e:
            logger.error(f"Error fetching metadata for {symbol}: {e}")
            return MetadataFetchResult(
                stock_code=symbol,
                success=False,
                error=str(e),
            )

    def _process_overseas_chunk_parallel(
        self,
        stocks_df: pd.DataFrame,
    ) -> list[MetadataFetchResult]:
        """Process a chunk of overseas stocks in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for _, stock_row in stocks_df.iterrows():
                worker_client = self._create_kis_worker_client()
                if worker_client is None:
                    results.append(
                        MetadataFetchResult(
                            stock_code=stock_row["Symbol"],
                            success=False,
                            error="KIS client not initialized",
                        )
                    )
                    continue

                future = executor.submit(
                    self._fetch_overseas_metadata_worker,
                    worker_client,
                    stock_row,
                )
                futures[future] = stock_row["Symbol"]

            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Worker error for {symbol}: {e}")
                    results.append(
                        MetadataFetchResult(
                            stock_code=symbol,
                            success=False,
                            error=str(e),
                        )
                    )

        return results

    def _save_overseas_chunk_results(self, results: list[MetadataFetchResult]) -> tuple[int, int, int]:
        """Save overseas metadata results to database."""
        metadata_list = []
        failed = 0
        skipped = 0

        for result in results:
            if not result.success:
                failed += 1
                continue
            if result.skipped:
                skipped += 1
                continue
            if result.data:
                metadata_list.append(result.data)

        if metadata_list:
            df = pd.DataFrame(metadata_list)
            count = self.db_manager.upsert_overseas_stock_metadata(df)
            return count, failed, skipped
        return 0, failed, skipped

    def fetch_and_save_overseas_metadata_batch(self, stocks_df: pd.DataFrame, chunk_size: int = 50) -> tuple[int, int]:
        """Fetch metadata for multiple overseas stocks and save to database using parallel processing.

        Args:
            stocks_df: DataFrame of stocks from master file
            chunk_size: Number of stocks to process per chunk (default: 50)

        Returns:
            Tuple of (success_count, failed_count)
        """
        total_stocks = len(stocks_df)
        total_success = 0
        total_failed = 0
        total_skipped = 0

        num_chunks = (total_stocks + chunk_size - 1) // chunk_size
        logger.info(f"Processing {total_stocks} overseas stocks in {num_chunks} chunks of {chunk_size} (parallel)...")

        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * chunk_size
            chunk_end = min(chunk_start + chunk_size, total_stocks)
            chunk = stocks_df.iloc[chunk_start:chunk_end]

            logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Processing stocks {chunk_start + 1}-{chunk_end}...")

            # Parallel fetch for this chunk
            fetch_results = self._process_overseas_chunk_parallel(chunk)

            # Save results to DB (main thread)
            chunk_success, chunk_failed, chunk_skipped = self._save_overseas_chunk_results(fetch_results)
            total_success += chunk_success
            total_failed += chunk_failed
            total_skipped += chunk_skipped

            logger.info(
                f"[Chunk {chunk_idx + 1}/{num_chunks}] Complete - Success: {chunk_success}, Skipped(ETF): {chunk_skipped}, Failed: {chunk_failed}"
            )

        logger.info(
            f"Batch processing complete - Total success: {total_success}, Total skipped(ETF): {total_skipped}, Total failed: {total_failed}"
        )
        return total_success, total_failed
