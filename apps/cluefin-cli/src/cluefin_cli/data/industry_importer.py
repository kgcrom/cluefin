"""Industry code import functionality for Kiwoom API."""

from typing import Dict, List, Optional

import pandas as pd
from cluefin_openapi.kiwoom import Client
from loguru import logger

from .duckdb_manager import DuckDBManager


class IndustryCodeImporter:
    """Importer for industry code data from Kiwoom API."""

    # Market type mapping
    MARKET_TYPES = {
        "0": "KOSPI",
        "1": "KOSDAQ",
    }

    def __init__(self, client: Client, db_manager: DuckDBManager):
        """Initialize industry code importer.

        Args:
            client: Kiwoom API client
            db_manager: DuckDB manager instance
        """
        self.client = client
        self.db_manager = db_manager

    def import_industry_codes(self, market_type: Optional[List[str]] = None) -> Dict[str, int]:
        """Import industry codes for specified market types.

        Args:
            market_type: List of market type codes (0=KOSPI, 1=KOSDAQ)
                         If None, imports all market types.

        Returns:
            Dictionary with import statistics per market type
        """
        if market_type is None:
            market_types = list(self.MARKET_TYPES.keys())
        else:
            market_types = market_type

        results = {}
        total_imported = 0

        for market_code in market_types:
            market_name = self.MARKET_TYPES.get(market_code, f"UNKNOWN_{market_code}")
            logger.info(f"Importing industry codes for market: {market_name} ({market_code})")

            try:
                count = self._import_single_market(market_code)
                results[market_name] = count
                total_imported += count
                logger.info(f"Successfully imported {count} industry codes for {market_name}")
            except Exception as e:
                logger.error(f"Error importing industry codes for {market_name}: {e}")
                results[market_name] = 0

        results["total"] = total_imported
        return results

    def _import_single_market(self, market_type: str) -> int:
        """Import industry codes for a single market type.

        Args:
            market_type: Market type code (0, 1)

        Returns:
            Number of industry codes imported
        """
        all_items = []
        cont_yn = "N"
        next_key = ""

        # Handle pagination
        while True:
            response = self.client.stock_info.get_industry_code(mrkt_tp=market_type, cont_yn=cont_yn, next_key=next_key)

            if response.body.list:
                all_items.extend(response.body.list)

            # Check if there are more pages
            cont_yn = response.headers.cont_yn
            next_key = response.headers.next_key

            if cont_yn != "Y":
                break

        if not all_items:
            logger.warning(f"No industry codes found for market type: {market_type}")
            return 0

        # Convert to DataFrame
        df = self._convert_to_dataframe(all_items, self.MARKET_TYPES[market_type])

        # Insert into database
        count = self.db_manager.insert_industry_codes(df)

        return count

    def _convert_to_dataframe(self, items: List, market_name: str) -> pd.DataFrame:
        """Convert industry code items to DataFrame.

        Args:
            items: List of DomesticStockInfoIndustryCodeItem objects
            market_name: Market name

        Returns:
            DataFrame with industry code data
        """
        data = []
        for item in items:
            data.append({"code": item.code, "name": item.name, "group_code": int(item.group), "market": market_name})

        return pd.DataFrame(data)

    def get_industry_codes_summary(self) -> pd.DataFrame:
        """Get summary of industry codes in database.

        Returns:
            DataFrame with industry code counts by market type
        """
        df = self.db_manager.get_industry_codes()

        if df.empty:
            logger.warning("No industry codes found in database")
            return pd.DataFrame()

        # Group by market and count
        summary = df.groupby("market").agg({"code": "count", "name": "first"}).reset_index()
        summary = summary.rename(columns={"code": "count", "market": "market_name"})

        return summary[["market_name", "count"]]
