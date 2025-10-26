"""DuckDB management for stock chart data storage."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd
from loguru import logger


class DuckDBManager:
    """Manager for DuckDB database operations."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize DuckDB manager.

        Args:
            db_path: Path to DuckDB database file. Defaults to ~/.cluefin/data.duckdb
        """
        if db_path is None:
            db_path = os.path.expanduser("~/.cluefin/data.duckdb")

        # Create directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path
        self.connection = duckdb.connect(db_path)
        self._create_tables()
        logger.info(f"Connected to DuckDB at {db_path}")

    def _create_tables(self):
        """Create tables if they don't exist."""
        # Daily chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS daily_chart (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                trading_value DOUBLE,
                adjusted_close DOUBLE,

                -- From API response (for reference)
                bic_inds_tp VARCHAR,
                sm_inds_tp VARCHAR,
                stk_infr VARCHAR,
                upd_stkpc_tp VARCHAR,
                upd_stkpc_event VARCHAR,
                pred_close_pric VARCHAR,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Weekly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS weekly_chart (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                trading_value DOUBLE,
                adjusted_close DOUBLE,

                -- From API response (for reference)
                bic_inds_tp VARCHAR,
                sm_inds_tp VARCHAR,
                stk_infr VARCHAR,
                upd_stkpc_tp VARCHAR,
                upd_stkpc_event VARCHAR,
                pred_close_pric VARCHAR,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Monthly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS monthly_chart (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                trading_value DOUBLE,
                adjusted_close DOUBLE,

                -- From API response (for reference)
                bic_inds_tp VARCHAR,
                sm_inds_tp VARCHAR,
                stk_infr VARCHAR,
                upd_stkpc_tp VARCHAR,
                upd_stkpc_event VARCHAR,
                pred_close_pric VARCHAR,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Stock metadata table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS stock_metadata (
                stock_code VARCHAR PRIMARY KEY,
                stock_name VARCHAR,
                last_imported_date DATE,
                import_frequency VARCHAR,
                next_import_date DATE,
                last_updated_at TIMESTAMP DEFAULT NOW()
            )
        """)

        logger.debug("DuckDB tables created/verified")

    def insert_daily_chart(self, stock_code: str, df: pd.DataFrame) -> int:
        """Insert daily chart data.

        Args:
            stock_code: Stock code
            df: DataFrame with columns matching daily_chart schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for daily chart: {stock_code}")
            return 0

        # Prepare data
        print(f"Stock: {stock_code}")
        insert_df = self._prepare_chart_data(stock_code, df)
        print(f"Insert DataFrame:\n{insert_df.head()}")

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO daily_chart
                (stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                 bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric)
                SELECT stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                       bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric
                FROM insert_df
                ON CONFLICT (stock_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} daily chart records for {stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting daily chart for {stock_code}: {e}")
            raise

    def insert_weekly_chart(self, stock_code: str, df: pd.DataFrame) -> int:
        """Insert weekly chart data.

        Args:
            stock_code: Stock code
            df: DataFrame with columns matching weekly_chart schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for weekly chart: {stock_code}")
            return 0

        insert_df = self._prepare_chart_data(stock_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO weekly_chart
                (stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                 bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric)
                SELECT stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                       bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric
                FROM insert_df
                ON CONFLICT (stock_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} weekly chart records for {stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting weekly chart for {stock_code}: {e}")
            raise

    def insert_monthly_chart(self, stock_code: str, df: pd.DataFrame) -> int:
        """Insert monthly chart data.

        Args:
            stock_code: Stock code
            df: DataFrame with columns matching monthly_chart schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for monthly chart: {stock_code}")
            return 0

        insert_df = self._prepare_chart_data(stock_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO monthly_chart
                (stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                 bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric)
                SELECT stock_code, date, open, high, low, close, volume, trading_value, adjusted_close,
                       bic_inds_tp, sm_inds_tp, stk_infr, upd_stkpc_tp, upd_stkpc_event, pred_close_pric
                FROM insert_df
                ON CONFLICT (stock_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} monthly chart records for {stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting monthly chart for {stock_code}: {e}")
            raise

    def _prepare_chart_data(self, stock_code: str, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare chart data for insertion.

        Args:
            stock_code: Stock code to add to data
            df: Raw DataFrame from API

        Returns:
            Prepared DataFrame
        """
        # Create DataFrame with same length as input
        result = pd.DataFrame(index=df.index)
        result["stock_code"] = stock_code

        # Map date field
        if "dt" in df.columns:
            result["date"] = pd.to_datetime(df["dt"], format="%Y%m%d")
        else:
            result["date"] = pd.to_datetime(df.index)

        # Map OHLCV fields
        field_mapping = {
            "cur_prc": "close",
            "open_pric": "open",
            "high_pric": "high",
            "low_pric": "low",
            "trde_qty": "volume",
            "trde_prica": "trading_value",
            "pred_close_pric": "adjusted_close",
        }

        for api_field, db_field in field_mapping.items():
            if api_field in df.columns:
                # Convert to numeric, handling empty strings
                result[db_field] = pd.to_numeric(df[api_field], errors="coerce")

        # Map optional fields
        optional_fields = [
            "bic_inds_tp",
            "sm_inds_tp",
            "stk_infr",
            "upd_stkpc_tp",
            "upd_stkpc_event",
            "pred_close_pric",
        ]
        for field in optional_fields:
            if field in df.columns:
                result[field] = df[field].astype(str)
            else:
                result[field] = None
        return result

    def update_stock_metadata(
        self,
        stock_code: str,
        stock_name: Optional[str] = None,
        import_frequency: Optional[str] = None,
    ) -> None:
        """Update stock metadata.

        Args:
            stock_code: Stock code
            stock_name: Stock name (optional)
            import_frequency: Import frequency (daily/weekly/monthly/all)
        """
        today = datetime.now().date()
        next_import_date = today + timedelta(days=1)

        self.connection.execute(
            """
            INSERT INTO stock_metadata
            (stock_code, stock_name, last_imported_date, import_frequency, next_import_date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(stock_code) DO UPDATE SET
                last_imported_date = ?,
                import_frequency = ?,
                next_import_date = ?,
                last_updated_at = NOW()
            """,
            [
                stock_code,
                stock_name,
                today,
                import_frequency,
                next_import_date,
                today,
                import_frequency,
                next_import_date,
            ],
        )
        logger.debug(f"Updated metadata for {stock_code}")

    def get_database_stats(self) -> dict:
        """Get database statistics.

        Returns:
            Dictionary with table statistics
        """
        stats = {}

        # Count records per table
        for table in ["daily_chart", "weekly_chart", "monthly_chart"]:
            result = self.connection.execute(f"SELECT COUNT(*) as count FROM {table}").fetchall()
            stats[f"{table}_count"] = result[0][0] if result else 0

            result = self.connection.execute(f"SELECT COUNT(DISTINCT stock_code) as count FROM {table}").fetchall()
            stats[f"{table}_stocks"] = result[0][0] if result else 0

        # Count metadata
        result = self.connection.execute("SELECT COUNT(*) as count FROM stock_metadata").fetchall()
        stats["tracked_stocks"] = result[0][0] if result else 0

        # Database size
        db_size = os.path.getsize(self.db_path)
        stats["database_size_mb"] = round(db_size / (1024 * 1024), 2)

        return stats

    def get_imported_stocks(self) -> list[str]:
        """Get list of all imported stock codes.

        Returns:
            List of stock codes with data in database
        """
        result = self.connection.execute(
            """
            SELECT DISTINCT stock_code FROM (
                SELECT stock_code FROM daily_chart
                UNION
                SELECT stock_code FROM weekly_chart
                UNION
                SELECT stock_code FROM monthly_chart
            ) ORDER BY stock_code
            """
        ).fetchall()

        return [row[0] for row in result]

    def get_stock_date_range(self, stock_code: str, table: str = "daily_chart") -> Optional[tuple]:
        """Get date range for a stock in a table.

        Args:
            stock_code: Stock code
            table: Table name (daily_chart, weekly_chart, monthly_chart)

        Returns:
            Tuple of (min_date, max_date) or None if no data
        """
        result = self.connection.execute(
            f"SELECT MIN(date), MAX(date) FROM {table} WHERE stock_code = ?", [stock_code]
        ).fetchall()

        if result and result[0][0] is not None:
            return (result[0][0], result[0][1])
        return None

    def check_data_exists(self, stock_code: str, frequency: str, start_date: str, end_date: str) -> bool:
        """Check if data already exists for a stock/frequency/date range.

        Args:
            stock_code: Stock code
            frequency: daily/weekly/monthly
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            True if all data exists, False otherwise
        """
        table = f"{frequency}_chart"
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            f"""
            SELECT COUNT(*) as count FROM {table}
            WHERE stock_code = ? AND date BETWEEN ? AND ?
            """,
            [stock_code, start, end],
        ).fetchall()

        expected_trading_days = self._estimate_trading_days(start, end, frequency)
        actual_count = result[0][0] if result else 0

        # Allow 10% tolerance for missing data (holidays, etc.)
        tolerance = max(1, int(expected_trading_days * 0.1))
        return actual_count >= (expected_trading_days - tolerance)

    def _estimate_trading_days(self, start_date, end_date, frequency: str) -> int:
        """Estimate number of trading days in date range.

        Args:
            start_date: Start date
            end_date: End date
            frequency: daily/weekly/monthly

        Returns:
            Estimated number of trading periods
        """
        delta = end_date - start_date

        if frequency == "daily":
            # Korea has ~252 trading days per year, roughly 5 per week
            return max(1, int(delta.days * 0.72))
        elif frequency == "weekly":
            return max(1, delta.days // 7)
        elif frequency == "monthly":
            return max(1, (delta.days // 30) + 1)

        return 1

    def clear_all_tables(self, confirm: bool = True) -> None:
        """Clear all data from tables.

        Args:
            confirm: Require confirmation before clearing
        """
        if confirm:
            response = input("Are you sure you want to clear all chart data? (yes/no): ")
            if response.lower() != "yes":
                logger.info("Clear operation cancelled")
                return

        self.connection.execute("DELETE FROM daily_chart")
        self.connection.execute("DELETE FROM weekly_chart")
        self.connection.execute("DELETE FROM monthly_chart")
        self.connection.execute("DELETE FROM stock_metadata")
        logger.info("All tables cleared")

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("DuckDB connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
