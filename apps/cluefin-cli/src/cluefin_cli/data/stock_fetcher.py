"""Stock list fetcher from Kiwoom API."""

from typing import Optional

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import DomesticStockInfoSummary
from cluefin_openapi.kiwoom._model import KiwoomHttpResponse
from loguru import logger


class StockListFetcher:
    """Fetch stock lists from Kiwoom API."""

    def __init__(self, client: Client):
        """Initialize stock list fetcher.

        Args:
            client: Kiwoom API client
        """
        self.client = client

    def get_all_stocks(self, market: Optional[str] = None) -> list[str]:
        """Get all listed stocks from Kiwoom API.

        Args:
            market: Filter by market ('kospi', 'kosdaq', or None for all)

        Returns:
            List of stock codes
        """
        stocks = []

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

        # Remove duplicates and sort
        stocks = sorted(set(stocks))
        logger.info(f"Total unique stocks: {len(stocks)}")

        return stocks

    def _parse_stocks_from_response(self, response: KiwoomHttpResponse[DomesticStockInfoSummary]) -> list[str]:
        """Parse stock codes from API response.

        Args:
            response: Kiwoom API response object

        Returns:
            List of stock codes
        """
        stocks = []

        try:
            for item in response.body.list:
                if item.marketName == "거래소" or item.marketName == "코스닥":
                    stocks.append(item.code.strip())
        except Exception as e:
            logger.error(f"Error parsing stock response: {e}")

        return stocks

    def validate_stock_code(self, stock_code: str) -> bool:
        """Validate if stock code exists in Kiwoom API.

        Args:
            stock_code: Stock code to validate

        Returns:
            True if stock code is valid, False otherwise
        """
        stock_code = stock_code.strip()

        if not stock_code or len(stock_code) != 6 or not stock_code.isdigit():
            return False

        try:
            # Try to fetch basic info for the stock
            self.client.stock_info.get_stock_info_v1(stk_cd=f"KRX:{stock_code}")
            return True
        except Exception as e:
            logger.debug(f"Stock code validation failed for {stock_code}: {e}")
            return False
