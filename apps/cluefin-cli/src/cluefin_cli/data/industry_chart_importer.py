"""Industry chart data importer from Kiwoom API."""

from datetime import datetime, timedelta
from typing import Callable, Optional

import pandas as pd
from cluefin_openapi.kiwoom._client import Client
from loguru import logger

from cluefin_cli.data.duckdb_manager import DuckDBManager


class IndustryChartImporter:
    """Import industry chart data from Kiwoom API to DuckDB."""

    def __init__(self, client: Client, db_manager: DuckDBManager):
        """Initialize industry chart data importer.

        Args:
            client: Kiwoom API client
            db_manager: DuckDB manager instance
        """
        self.client = client
        self.db_manager = db_manager

    def import_industry_data(
        self,
        industry_code: str,
        start_date: str,
        end_date: str,
        frequencies: list[str],
        skip_existing: bool = True,
    ) -> dict:
        """Import chart data for a single industry.

        Args:
            industry_code: Industry code (e.g., '001' for KOSPI)
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            frequencies: List of frequencies to import ('daily', 'weekly', 'monthly')
            skip_existing: Skip import if data already exists

        Returns:
            Dictionary with import results {frequency: record_count}
        """
        results = {}
        industry_code = industry_code.strip()

        if not self._validate_date_format(start_date):
            raise ValueError(f"Invalid start date format: {start_date}")
        if not self._validate_date_format(end_date):
            raise ValueError(f"Invalid end date format: {end_date}")

        for frequency in frequencies:
            try:
                # Check if data already exists
                if skip_existing and self.db_manager.check_industry_data_exists(
                    industry_code, frequency, start_date, end_date
                ):
                    logger.info(f"Data already exists for industry {industry_code} ({frequency}), skipping...")
                    results[frequency] = 0
                    continue

                # Fetch and store data
                count = self._import_frequency(industry_code, start_date, end_date, frequency)
                results[frequency] = count

            except Exception as e:
                logger.error(f"Error importing {frequency} data for industry {industry_code}: {e}")
                results[frequency] = -1

        return results

    def _import_frequency(self, industry_code: str, start_date: str, end_date: str, frequency: str) -> int:
        """Import chart data for a specific frequency.

        Args:
            industry_code: Industry code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            frequency: Frequency type ('daily', 'weekly', 'monthly')

        Returns:
            Number of records imported
        """
        logger.info(f"Importing {frequency} data for industry {industry_code}")

        # Convert dates
        end_datetime = datetime.strptime(end_date, "%Y%m%d")
        all_data = []

        try:
            if frequency == "daily":
                all_data = self._fetch_daily_data(industry_code, end_datetime)
            elif frequency == "weekly":
                all_data = self._fetch_weekly_data(industry_code, end_datetime)
            elif frequency == "monthly":
                all_data = self._fetch_monthly_data(industry_code, end_datetime)
            else:
                raise ValueError(f"Unknown frequency: {frequency}")

            # Filter by date range
            if all_data:
                df = pd.DataFrame(all_data)
                df = self._filter_date_range(df, start_date, end_date)

                # Store in database
                if frequency == "daily":
                    count = self.db_manager.insert_industry_daily_chart(industry_code, df)
                elif frequency == "weekly":
                    count = self.db_manager.insert_industry_weekly_chart(industry_code, df)
                elif frequency == "monthly":
                    count = self.db_manager.insert_industry_monthly_chart(industry_code, df)

                return count
            else:
                logger.warning(f"No {frequency} data returned from API for industry {industry_code}")
                return 0

        except Exception as e:
            logger.error(f"Error importing {frequency} data for industry {industry_code}: {e}")
            raise

    def _fetch_daily_data(self, industry_code: str, base_date: datetime) -> list[dict]:
        """Fetch daily chart data.

        Args:
            industry_code: Industry code
            base_date: Base date to fetch from

        Returns:
            List of data records
        """
        all_data = []
        base_dt = base_date.strftime("%Y%m%d")

        try:
            response = self.client.chart.get_industry_daily(
                inds_cd=industry_code,
                base_dt=base_dt,
            )

            if response.body and hasattr(response.body, "inds_dt_pole_qry"):
                for item in response.body.inds_dt_pole_qry:
                    all_data.append(self._item_to_dict(item))

        except Exception as e:
            logger.error(f"Error fetching daily data for industry {industry_code}: {e}")

        return all_data

    def _fetch_weekly_data(self, industry_code: str, base_date: datetime) -> list[dict]:
        """Fetch weekly chart data.

        Args:
            industry_code: Industry code
            base_date: Base date to fetch from

        Returns:
            List of data records
        """
        all_data = []
        base_dt = base_date.strftime("%Y%m%d")

        try:
            response = self.client.chart.get_industry_weekly(
                inds_cd=industry_code,
                base_dt=base_dt,
            )

            if response.body and hasattr(response.body, "inds_stk_pole_qry"):
                for item in response.body.inds_stk_pole_qry:
                    all_data.append(self._item_to_dict(item))

        except Exception as e:
            logger.error(f"Error fetching weekly data for industry {industry_code}: {e}")

        return all_data

    def _fetch_monthly_data(self, industry_code: str, base_date: datetime) -> list[dict]:
        """Fetch monthly chart data.

        Args:
            industry_code: Industry code
            base_date: Base date to fetch from

        Returns:
            List of data records
        """
        all_data = []
        base_dt = base_date.strftime("%Y%m%d")

        try:
            response = self.client.chart.get_industry_monthly(
                inds_cd=industry_code,
                base_dt=base_dt,
            )

            if response.body and hasattr(response.body, "inds_mth_pole_qry"):
                for item in response.body.inds_mth_pole_qry:
                    all_data.append(self._item_to_dict(item))

        except Exception as e:
            logger.error(f"Error fetching monthly data for industry {industry_code}: {e}")

        return all_data

    def _item_to_dict(self, item) -> dict:
        """Convert API item to dictionary.

        Args:
            item: API response item (Pydantic BaseModel)

        Returns:
            Dictionary representation with only model_fields
        """
        result = {}

        # Extract only fields defined in model_fields
        if hasattr(item, "model_fields"):
            for field_name in item.model_fields.keys():
                result[field_name] = getattr(item, field_name)
        elif isinstance(item, dict):
            result = item.copy()

        return result

    def _filter_date_range(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter DataFrame by date range.

        Args:
            df: DataFrame with 'dt' or 'date' column
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)

        Returns:
            Filtered DataFrame
        """
        # Ensure date column exists
        if "dt" in df.columns:
            df["date"] = pd.to_datetime(df["dt"], format="%Y%m%d")
        elif "date" not in df.columns:
            return df

        start = pd.to_datetime(start_date, format="%Y%m%d")
        end = pd.to_datetime(end_date, format="%Y%m%d")

        return df[(df["date"] >= start) & (df["date"] <= end)].copy()

    def import_batch(
        self,
        industry_codes: list[str],
        start_date: str,
        end_date: str,
        frequencies: list[str],
        progress_callback: Optional[Callable] = None,
        skip_existing: bool = True,
    ) -> dict:
        """Import data for multiple industries.

        Args:
            industry_codes: List of industry codes
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            frequencies: List of frequencies
            progress_callback: Optional callback for progress updates
            skip_existing: Skip imports if data exists

        Returns:
            Dictionary with results {industry_code: {frequency: count}}
        """
        results = {}
        total = len(industry_codes)

        for idx, industry_code in enumerate(industry_codes, 1):
            if progress_callback:
                progress_callback(idx, total, industry_code)

            try:
                results[industry_code] = self.import_industry_data(
                    industry_code, start_date, end_date, frequencies, skip_existing=skip_existing
                )
            except Exception as e:
                logger.error(f"Error importing industry {industry_code}: {e}")
                results[industry_code] = {freq: -1 for freq in frequencies}

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
