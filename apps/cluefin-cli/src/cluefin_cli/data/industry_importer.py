"""Industry code import functionality from idxcode.mst file.

업종코드 파일 다운로드:
https://apiportal.koreainvestment.com/apiservice-category
"""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from loguru import logger

from .duckdb_manager import DuckDBManager


class DomesticIndustryCodeImporter:
    """Importer for domestic industry code data from idxcode.mst file.

    MST 파일은 고정폭 텍스트 파일로 cp949 인코딩됨:
    - Position 0: market code (idx_div) - 1 character
    - Position 1-4: industry code (idx_code) - 4 characters
    - Position 5-44: industry name (idx_name) - 40 characters

    업종코드 파일은 한국투자증권 API Portal에서 다운로드 가능:
    https://apiportal.koreainvestment.com/apiservice-category
    """

    FILE_ENCODING = "cp949"

    def __init__(self, db_manager: DuckDBManager):
        """Initialize industry code importer.

        Args:
            db_manager: DuckDB manager instance
        """
        self.db_manager = db_manager

    def import_industry_codes(self, mst_file_path: str) -> Dict[str, int]:
        """Import industry codes from idxcode.mst file.

        Args:
            mst_file_path: Path to idxcode.mst file

        Returns:
            Dictionary with import statistics
        """
        mst_path = Path(mst_file_path)

        if not mst_path.exists():
            logger.error(f"MST file not found: {mst_path}")
            raise FileNotFoundError(f"MST file not found: {mst_path}")

        logger.info(f"Importing industry codes from {mst_path}")

        try:
            df = self._parse_mst_file(mst_path)

            if df.empty:
                logger.warning("No records found in MST file")
                return {"total": 0}

            # Insert into database
            count = self.db_manager.insert_domestic_industry_codes(df)
            logger.info(f"Successfully imported {count} domestic industry codes")

            return {"total": count}
        except Exception as e:
            logger.error(f"Error importing industry codes: {e}")
            raise

    def _parse_mst_file(self, file_path: Path) -> pd.DataFrame:
        """Parse idxcode.mst file.

        File structure (고정폭 텍스트 파일):
        - Position 1-5: industry code (idx_code) - 4 characters
        - Position 5-45: industry name (idx_name) - 40 characters

        Args:
            file_path: Path to MST file

        Returns:
            DataFrame with market, code, name columns
        """
        records = []

        try:
            with open(file_path, "r", encoding="cp949") as f:
                for row in f:
                    # Extract fields from fixed-width format
                    code = row[1:5].strip()  # Position 1-5: industry code
                    name = row[5:45].rstrip()  # Position 5-45: industry name

                    # Skip empty records
                    if not code:
                        continue

                    records.append({"code": code, "name": name})

            logger.info(f"Parsed {len(records)} records from {file_path.name}")
            return pd.DataFrame(records)

        except Exception as e:
            logger.error(f"Error parsing MST file: {e}")
            raise

    def get_industry_codes_summary(self) -> pd.DataFrame:
        """Get summary of domestic industry codes in database.

        Returns:
            DataFrame with industry code counts by market
        """
        df = self.db_manager.get_domestic_industry_codes()

        if df.empty:
            logger.warning("No domestic industry codes found in database")
            return pd.DataFrame()

        # Group by market and count
        summary = df.groupby("market").size().reset_index(name="count")
        summary = summary.rename(columns={"market": "market_code"})

        return summary[["market_code", "count"]]
