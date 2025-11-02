"""Stock list fetcher from Kiwoom API."""

from typing import Optional

import pandas as pd
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import DomesticStockInfoSummary, DomesticStockInfoSummaryItem
from cluefin_openapi.kiwoom._model import KiwoomHttpResponse
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


class StockListFetcher:
    """Fetch stock lists from Kiwoom API."""

    def __init__(self, client: Client, db_manager: DuckDBManager):
        """Initialize stock list fetcher.

        Args:
            client: Kiwoom API client
            db_manager: DuckDB manager instance
        """
        self.client = client
        self.db_manager = db_manager

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
                if not item.code or len(item.code) != 6 or not item.code.isdigit() and int(item.code) % 10 != 0:
                    continue
                if item.marketName == "거래소" or item.marketName == "코스닥":
                    stocks.append(item)
        except Exception as e:
            logger.error(f"Error parsing stock response: {e}")

        return stocks

    def fetch_stock_metadata_extended(self, stock_info: DomesticStockInfoSummaryItem) -> Optional[dict]:
        """Fetch extended stock metadata by combining two APIs.

        Fetches data from both get_stock_info_v1 and get_stock_info APIs,
        combining them into a single metadata dictionary.

        Args:
            stock_info: Stock info to fetch metadata for

        Returns:
            Dictionary with combined metadata fields, or None if either API fails.
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

            if metadata is None:
                logger.warning(f"Failed to fetch extended metadata for {stock_info} - skipping enrichment")
                return

            # Convert metadata dict to DataFrame
            df = pd.DataFrame([metadata])

            # Upsert to database
            count = self.db_manager.upsert_stock_metadata_extended(df)
            logger.info(f"Successfully enriched metadata for {stock_info.code} ({count} record)")
            return metadata

        except Exception as e:
            logger.error(f"Error fetching extended metadata for {stock_info}: {e}")
            return None

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
