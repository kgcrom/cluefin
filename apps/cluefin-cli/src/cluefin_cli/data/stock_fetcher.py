"""Stock list fetcher from Kiwoom API and KIS API."""

import os
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd
from cluefin_openapi.kis._client import Client as KisClient
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import DomesticStockInfoSummary, DomesticStockInfoSummaryItem
from cluefin_openapi.kiwoom._model import KiwoomHttpResponse
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


class StockListFetcher:
    """Fetch stock lists from Kiwoom API and overseas stocks from KIS API."""

    def __init__(self, client: Client, db_manager: DuckDBManager, kis_client: Optional[KisClient] = None):
        """Initialize stock list fetcher.

        Args:
            client: Kiwoom API client
            db_manager: DuckDB manager instance
            kis_client: KIS API client (optional, required for overseas stocks)
        """
        self.client = client
        self.db_manager = db_manager
        self.kis_client = kis_client

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

    def fetch_and_save_metadata_batch(
        self, stock_infos: list[DomesticStockInfoSummaryItem], chunk_size: int = 100
    ) -> tuple[int, int]:
        """Fetch metadata for multiple stocks and save to database in chunks.

        Processes stocks in chunks to balance memory usage and incremental progress.
        Each chunk is fetched and saved to database before moving to the next chunk.

        Args:
            stock_infos: List of stock info objects to fetch metadata for
            chunk_size: Number of stocks to process per chunk (default: 100)

        Returns:
            Tuple of (success_count, failed_count)
        """
        total_stocks = len(stock_infos)
        total_success = 0
        total_failed = 0

        # Calculate number of chunks
        num_chunks = (total_stocks + chunk_size - 1) // chunk_size  # Ceiling division

        logger.info(f"Processing {total_stocks} stocks in {num_chunks} chunks of {chunk_size}...")

        # Process stocks in chunks
        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * chunk_size
            chunk_end = min(chunk_start + chunk_size, total_stocks)
            chunk = stock_infos[chunk_start:chunk_end]

            logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Processing stocks {chunk_start + 1}-{chunk_end}...")

            chunk_metadata = []
            chunk_failed = 0

            # Fetch metadata for all stocks in this chunk
            for stock_info in chunk:
                global_idx = stock_infos.index(stock_info) + 1
                logger.info(
                    f"  [{global_idx}/{total_stocks}] Fetching metadata for {stock_info.code} ({stock_info.name})"
                )
                metadata = self.fetch_domestic_stock_metadata_extended(stock_info)

                if metadata:
                    chunk_metadata.append(metadata)
                else:
                    chunk_failed += 1
                    logger.warning(f"  Failed to fetch metadata for {stock_info.code}")

            # Save this chunk to database
            if chunk_metadata:
                logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Saving {len(chunk_metadata)} records to database...")
                df = pd.DataFrame(chunk_metadata)
                count = self.db_manager.upsert_domestic_stock_metadata_extended(df)
                logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Successfully saved {count} records")
                total_success += count
            else:
                logger.warning(f"[Chunk {chunk_idx + 1}/{num_chunks}] No metadata to save")

            total_failed += chunk_failed
            logger.info(
                f"[Chunk {chunk_idx + 1}/{num_chunks}] Complete - Success: {len(chunk_metadata)}, Failed: {chunk_failed}"
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

                if hasattr(product_info, "ovrs_stck_etf_risk_drtp_cd"):
                    return None

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

    def fetch_and_save_overseas_metadata_batch(self, stocks_df: pd.DataFrame, chunk_size: int = 50) -> tuple[int, int]:
        """Fetch metadata for multiple overseas stocks and save to database in chunks.

        Args:
            stocks_df: DataFrame of stocks from master file
            chunk_size: Number of stocks to process per chunk (default: 50)

        Returns:
            Tuple of (success_count, failed_count)
        """
        total_stocks = len(stocks_df)
        total_success = 0
        total_failed = 0

        # Calculate number of chunks
        num_chunks = (total_stocks + chunk_size - 1) // chunk_size

        logger.info(f"Processing {total_stocks} overseas stocks in {num_chunks} chunks of {chunk_size}...")

        # Process stocks in chunks
        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * chunk_size
            chunk_end = min(chunk_start + chunk_size, total_stocks)
            chunk = stocks_df.iloc[chunk_start:chunk_end]

            logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Processing stocks {chunk_start + 1}-{chunk_end}...")

            chunk_metadata = []
            chunk_failed = 0

            # Fetch metadata for all stocks in this chunk
            for idx, (_, stock_row) in enumerate(chunk.iterrows()):
                global_idx = chunk_start + idx + 1
                symbol = stock_row["Symbol"]
                logger.info(
                    f"  [{global_idx}/{total_stocks}] Fetching metadata for {symbol} ({stock_row['English name']})"
                )
                metadata = self.fetch_overseas_stock_metadata_extended(stock_row)

                if metadata:
                    chunk_metadata.append(metadata)
                else:
                    chunk_failed += 1
                    logger.warning(f"  Failed to fetch metadata for {symbol}")

            # Save this chunk to database
            if chunk_metadata:
                logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Saving {len(chunk_metadata)} records to database...")
                df = pd.DataFrame(chunk_metadata)
                count = self.db_manager.upsert_overseas_stock_metadata(df)
                logger.info(f"[Chunk {chunk_idx + 1}/{num_chunks}] Successfully saved {count} records")
                total_success += count
            else:
                logger.warning(f"[Chunk {chunk_idx + 1}/{num_chunks}] No metadata to save")

            total_failed += chunk_failed
            logger.info(
                f"[Chunk {chunk_idx + 1}/{num_chunks}] Complete - Success: {len(chunk_metadata)}, Failed: {chunk_failed}"
            )

        logger.info(f"Batch processing complete - Total success: {total_success}, Total failed: {total_failed}")
        return total_success, total_failed
