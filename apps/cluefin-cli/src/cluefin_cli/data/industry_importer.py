"""Industry code import functionality from idxcode.mst file.

업종코드 파일 다운로드:
https://apiportal.koreainvestment.com/apiservice-category
"""

import logging
import os
import shutil
import ssl
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict

import pandas as pd

from .duckdb_manager import DuckDBManager

logger = logging.getLogger(__name__)


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

    def import_industry_codes(self) -> Dict[str, int]:
        """Import industry codes from idxcode.mst file.

        Downloads idxcode.mst.zip from DWS, extracts it, and imports industry codes.

        Returns:
            Dictionary with import statistics
        """
        temp_dir = None
        try:
            # Disable SSL verification for master file download
            ssl._create_default_https_context = ssl._create_unverified_context

            # Download master file zip
            url = "https://new.real.download.dws.co.kr/common/master/idxcode.mst.zip"
            temp_dir = tempfile.mkdtemp()

            zip_path = os.path.join(temp_dir, "idxcode.mst.zip")
            logger.debug(f"Downloading industry code file from {url}...")
            urllib.request.urlretrieve(url, zip_path)

            # Extract zip file
            logger.debug(f"Extracting zip file from {zip_path}...")
            with zipfile.ZipFile(zip_path) as zip_ref:
                zip_ref.extractall(temp_dir)

            # Read the master file
            mst_path = Path(os.path.join(temp_dir, "idxcode.mst"))
            if not mst_path.exists():
                logger.error(f"MST file not found after extraction: {mst_path}")
                raise FileNotFoundError("idxcode.mst not found in zip file")

            logger.info(f"Importing industry codes from {mst_path}")
            df = self._parse_mst_file(mst_path)

            if df.empty:
                logger.warning("No records found in MST file")
                return {"total": 0}

            # Insert into database
            count = self.db_manager.insert_industry_codes(df)
            logger.info(f"Successfully imported {count} industry codes")

            return {"total": count}
        except Exception as e:
            logger.error(f"Error importing industry codes: {e}")
            raise
        finally:
            # Clean up temp directory
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.debug(f"Cleaned up temp directory: {temp_dir}")

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
        """Get summary of industry codes in database.

        Returns:
            DataFrame with industry code counts by market
        """
        df = self.db_manager.get_industry_codes()

        if df.empty:
            logger.warning("No domestic industry codes found in database")
            return pd.DataFrame()

        # Group by market and count
        summary = df.groupby("market").size().reset_index(name="count")
        summary = summary.rename(columns={"market": "market_code"})

        return summary[["market_code", "count"]]


