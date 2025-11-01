"""DuckDB management for stock chart data storage."""

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
            db_path: Path to DuckDB database file. Defaults to <project_root>/data/data.duckdb
        """
        if db_path is None:
            # Use project root directory instead of home directory
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            db_path = str(project_root / "data" / "data.duckdb")

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
            CREATE TABLE IF NOT EXISTS daily_charts (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- From API response (for reference)
                pred_signal VARCHAR,
                pred_diff_close_pric BIGINT,
                turnover_rate DOUBLE,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Weekly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS weekly_charts (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- From API response (for reference)
                pred_signal VARCHAR,
                pred_diff_close_pric BIGINT,
                turnover_rate DOUBLE,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Monthly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS monthly_charts (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- From API response (for reference)
                pred_signal VARCHAR,
                pred_diff_close_pric BIGINT,
                turnover_rate DOUBLE,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        # Industry daily chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS industry_daily_charts (
                industry_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (industry_code, date)
            )
        """)

        # Industry weekly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS industry_weekly_charts (
                industry_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (industry_code, date)
            )
        """)

        # Industry monthly chart table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS industry_monthly_charts (
                industry_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (industry_code, date)
            )
        """)

        # Stock metadata table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS stock_metadata (
                stock_code VARCHAR PRIMARY KEY,
                stock_name VARCHAR,
                -- get_stock_info_v1 fields
                listing_date DATE,
                market_name VARCHAR,
                market_code VARCHAR,
                industry_name VARCHAR,
                company_size VARCHAR,
                company_class VARCHAR,
                audit_info VARCHAR,
                stock_state VARCHAR,
                investment_warning INTEGER,
                -- get_stock_info fields
                settlement_month VARCHAR,
                face_value INTEGER,
                capital BIGINT,
                float_stock BIGINT,
                per DECIMAL,
                eps DECIMAL,
                roe DECIMAL,
                pbr DECIMAL,
                bps DECIMAL,
                sales_amount BIGINT,
                business_profit BIGINT,
                net_income BIGINT,
                market_cap BIGINT,
                foreign_ownership_rate DECIMAL,
                distribution_rate DECIMAL,
                distribution_stock BIGINT
            )
        """)

        # Industry codes table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS industry_codes (
                code VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                group_code INT NOT NULL,
                market VARCHAR,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
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
        insert_df = self._prepare_chart_data(stock_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO daily_charts
                (stock_code, date, open, high, low, close, volume, trading_amount,
                 pred_signal, pred_diff_close_pric, turnover_rate)
                SELECT stock_code, date, open, high, low, close, volume, trading_amount,
                       pred_signal, pred_diff_close_pric, turnover_rate
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
            df: DataFrame with columns matching weekly_charts schema

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
                """INSERT INTO weekly_charts
                (stock_code, date, open, high, low, close, volume, trading_amount,
                 pred_signal, pred_diff_close_pric, turnover_rate)
                SELECT stock_code, date, open, high, low, close, volume, trading_amount,
                       pred_signal, pred_diff_close_pric, turnover_rate
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
            df: DataFrame with columns matching monthly_charts schema

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
                """INSERT INTO monthly_charts
                (stock_code, date, open, high, low, close, volume, trading_amount,
                 pred_signal, pred_diff_close_pric, turnover_rate)
                SELECT stock_code, date, open, high, low, close, volume, trading_amount,
                       pred_signal, pred_diff_close_pric, turnover_rate
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

    def insert_industry_daily_chart(self, industry_code: str, df: pd.DataFrame) -> int:
        """Insert industry daily chart data.

        Args:
            industry_code: Industry code
            df: DataFrame with columns matching industry_daily_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for industry daily chart: {industry_code}")
            return 0

        # Prepare data
        insert_df = self._prepare_industry_chart_data(industry_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO industry_daily_charts
                (industry_code, date, open, high, low, close, volume, trading_amount)
                SELECT industry_code, date, open, high, low, close, volume, trading_amount
                FROM insert_df
                ON CONFLICT (industry_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} industry daily chart records for {industry_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting industry daily chart for {industry_code}: {e}")
            raise

    def insert_industry_weekly_chart(self, industry_code: str, df: pd.DataFrame) -> int:
        """Insert industry weekly chart data.

        Args:
            industry_code: Industry code
            df: DataFrame with columns matching industry_weekly_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for industry weekly chart: {industry_code}")
            return 0

        insert_df = self._prepare_industry_chart_data(industry_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO industry_weekly_charts
                (industry_code, date, open, high, low, close, volume, trading_amount)
                SELECT industry_code, date, open, high, low, close, volume, trading_amount
                FROM insert_df
                ON CONFLICT (industry_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} industry weekly chart records for {industry_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting industry weekly chart for {industry_code}: {e}")
            raise

    def insert_industry_monthly_chart(self, industry_code: str, df: pd.DataFrame) -> int:
        """Insert industry monthly chart data.

        Args:
            industry_code: Industry code
            df: DataFrame with columns matching industry_monthly_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for industry monthly chart: {industry_code}")
            return 0

        insert_df = self._prepare_industry_chart_data(industry_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO industry_monthly_charts
                (industry_code, date, open, high, low, close, volume, trading_amount)
                SELECT industry_code, date, open, high, low, close, volume, trading_amount
                FROM insert_df
                ON CONFLICT (industry_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} industry monthly chart records for {industry_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting industry monthly chart for {industry_code}: {e}")
            raise

    def _prepare_chart_data(self, stock_code: str, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare chart data for insertion.

        Args:
            stock_code: Stock code to add to data
            df: Raw DataFrame from API

        Returns:
            Prepared DataFrame
        """
        result = pd.DataFrame()

        # Map date field
        if "dt" in df.columns:
            result["date"] = pd.to_datetime(df["dt"], format="%Y%m%d")
        else:
            result["date"] = pd.to_datetime(df.index)

        result["stock_code"] = stock_code

        # Map OHLCV fields
        field_mapping = {
            "cur_prc": "close",
            "open_pric": "open",
            "high_pric": "high",
            "low_pric": "low",
            "trde_qty": "volume",
            "trde_prica": "trading_amount",
        }

        for api_field, db_field in field_mapping.items():
            if api_field in df.columns:
                # Convert to numeric, handling empty strings
                result[db_field] = pd.to_numeric(df[api_field], errors="coerce")

        # Map optional fields
        optional_fields = {
            "pred_pre": "pred_diff_close_pric",
            "pred_pre_sig": "pred_signal",
            "trde_tern_rt": "turnover_rate",
        }
        for api_field, db_field in optional_fields.items():
            if api_field in df.columns:
                if api_field == "pred_pre_sig":
                    result[db_field] = df[api_field].astype(str)
                else:
                    # Remove leading '+' sign before converting to numeric
                    result[db_field] = pd.to_numeric(
                        df[api_field].astype(str).str.replace(r"^\+", "", regex=True), errors="coerce"
                    )
            else:
                result[db_field] = None

        return result

    def _prepare_industry_chart_data(self, industry_code: str, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare industry chart data for insertion.

        Args:
            industry_code: Industry code to add to data
            df: Raw DataFrame from API

        Returns:
            Prepared DataFrame
        """
        result = pd.DataFrame()

        # Map date field
        if "dt" in df.columns:
            result["date"] = pd.to_datetime(df["dt"], format="%Y%m%d")
        else:
            result["date"] = pd.to_datetime(df.index)

        result["industry_code"] = industry_code

        # Map OHLCV fields (same as stock charts)
        field_mapping = {
            "cur_prc": "close",
            "open_pric": "open",
            "high_pric": "high",
            "low_pric": "low",
            "trde_qty": "volume",
            "trde_prica": "trading_amount",
        }

        for api_field, db_field in field_mapping.items():
            if api_field in df.columns:
                # Convert to numeric, handling empty strings
                result[db_field] = pd.to_numeric(df[api_field], errors="coerce")

        return result

    def update_stock_metadata(
        self,
        stock_code: str,
        stock_name: Optional[str] = None,
    ) -> None:
        """Update stock metadata.

        Args:
            stock_code: Stock code
            stock_name: Stock name (optional)
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
                None,
                next_import_date,
                today,
                None,
                next_import_date,
            ],
        )
        logger.debug(f"Updated metadata for {stock_code}")

    def upsert_stock_metadata_extended(self, df: pd.DataFrame) -> int:
        """Upsert extended stock metadata from combined API responses.

        Args:
            df: DataFrame with all stock metadata columns including:
                stock_code, stock_name, listing_date, market_name, market_code,
                industry_name, company_size, company_class, audit_info, stock_state,
                investment_warning, settlement_month, face_value, capital, float_stock,
                per, eps, roe, pbr, bps, sales_amount, business_profit, net_income,
                market_cap, foreign_ownership_rate, distribution_rate, distribution_stock

        Returns:
            Number of records upserted
        """
        if df.empty:
            logger.warning("Empty DataFrame for stock metadata")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO stock_metadata
                (stock_code, stock_name, listing_date, market_name, market_code,
                 industry_name, company_size, company_class, audit_info, stock_state,
                 investment_warning, settlement_month, face_value, capital, float_stock,
                 per, eps, roe, pbr, bps, sales_amount, business_profit, net_income,
                 market_cap, foreign_ownership_rate, distribution_rate, distribution_stock)
                SELECT stock_code, stock_name, listing_date, market_name, market_code,
                       industry_name, company_size, company_class, audit_info, stock_state,
                       investment_warning, settlement_month, face_value, capital, float_stock,
                       per, eps, roe, pbr, bps, sales_amount, business_profit, net_income,
                       market_cap, foreign_ownership_rate, distribution_rate, distribution_stock
                FROM insert_df
                ON CONFLICT (stock_code) DO UPDATE SET
                    stock_name = EXCLUDED.stock_name,
                    listing_date = EXCLUDED.listing_date,
                    market_name = EXCLUDED.market_name,
                    market_code = EXCLUDED.market_code,
                    industry_name = EXCLUDED.industry_name,
                    company_size = EXCLUDED.company_size,
                    company_class = EXCLUDED.company_class,
                    audit_info = EXCLUDED.audit_info,
                    stock_state = EXCLUDED.stock_state,
                    investment_warning = EXCLUDED.investment_warning,
                    settlement_month = EXCLUDED.settlement_month,
                    face_value = EXCLUDED.face_value,
                    capital = EXCLUDED.capital,
                    float_stock = EXCLUDED.float_stock,
                    per = EXCLUDED.per,
                    eps = EXCLUDED.eps,
                    roe = EXCLUDED.roe,
                    pbr = EXCLUDED.pbr,
                    bps = EXCLUDED.bps,
                    sales_amount = EXCLUDED.sales_amount,
                    business_profit = EXCLUDED.business_profit,
                    net_income = EXCLUDED.net_income,
                    market_cap = EXCLUDED.market_cap,
                    foreign_ownership_rate = EXCLUDED.foreign_ownership_rate,
                    distribution_rate = EXCLUDED.distribution_rate,
                    distribution_stock = EXCLUDED.distribution_stock"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.info(f"Upserted {count} stock metadata records")
            return count
        except Exception as e:
            logger.error(f"Error upserting stock metadata: {e}")
            raise

    def insert_industry_codes(self, df: pd.DataFrame) -> int:
        """Insert industry codes.

        Args:
            df: DataFrame with columns: code, name, group_name, market

        Returns:
            Number of records inserted/updated
        """
        if df.empty:
            logger.warning("Empty DataFrame for industry codes")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO industry_codes
                (code, name, group_code, market)
                SELECT code, name, group_code, market
                FROM insert_df
                ON CONFLICT (code) DO UPDATE SET
                    name = EXCLUDED.name,
                    group_code = EXCLUDED.group_code,
                    market = EXCLUDED.market,
                    updated_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.info(f"Inserted/updated {count} industry code records")
            return count
        except Exception as e:
            logger.error(f"Error inserting industry codes: {e}")
            raise

    def get_industry_codes(self, market_type: Optional[str] = None) -> pd.DataFrame:
        """Get industry codes from database.

        Args:
            market_type: Filter by market type (0=KOSPI, 1=KOSDAQ, etc.)

        Returns:
            DataFrame with industry code data
        """
        if market_type:
            result = self.connection.execute(
                "SELECT * FROM industry_codes WHERE market_type = ? ORDER BY code", [market_type]
            ).df()
        else:
            result = self.connection.execute("SELECT * FROM industry_codes ORDER BY code").df()

        return result

    def get_database_stats(self) -> dict:
        """Get database statistics.

        Returns:
            Dictionary with table statistics
        """
        stats = {}

        # Count records per table
        for table in ["daily_charts", "weekly_charts", "monthly_charts"]:
            result = self.connection.execute(f"SELECT COUNT(*) as count FROM {table}").fetchall()
            stats[f"{table}_count"] = result[0][0] if result else 0

            result = self.connection.execute(f"SELECT COUNT(DISTINCT stock_code) as count FROM {table}").fetchall()
            stats[f"{table}_stocks"] = result[0][0] if result else 0

        # Count industry chart records per table
        for table in ["industry_daily_charts", "industry_weekly_charts", "industry_monthly_charts"]:
            result = self.connection.execute(f"SELECT COUNT(*) as count FROM {table}").fetchall()
            stats[f"{table}_count"] = result[0][0] if result else 0

            result = self.connection.execute(
                f"SELECT COUNT(DISTINCT industry_code) as count FROM {table}"
            ).fetchall()
            stats[f"{table}_industries"] = result[0][0] if result else 0

        # Count metadata
        result = self.connection.execute("SELECT COUNT(*) as count FROM stock_metadata").fetchall()
        stats["tracked_stocks"] = result[0][0] if result else 0

        # Count industry codes
        result = self.connection.execute("SELECT COUNT(*) as count FROM industry_codes").fetchall()
        stats["industry_codes_count"] = result[0][0] if result else 0

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
                SELECT stock_code FROM daily_charts
                UNION
                SELECT stock_code FROM weekly_charts
                UNION
                SELECT stock_code FROM monthly_charts
            ) ORDER BY stock_code
            """
        ).fetchall()

        return [row[0] for row in result]

    def get_stock_date_range(self, stock_code: str, table: str = "daily_charts") -> Optional[tuple]:
        """Get date range for a stock in a table.

        Args:
            stock_code: Stock code
            table: Table name (daily_charts, weekly_charts, monthly_charts)

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
        table = f"{frequency}_charts"
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            f"""
            SELECT COUNT(*) as count FROM {table}
            WHERE stock_code = ? AND date BETWEEN ? AND ?
            """,
            [stock_code, start, end],
        ).fetchall()

        actual_count = result[0][0] if result else 0

        # If no data exists, return False
        if actual_count == 0:
            return False

        return True

    def check_industry_data_exists(
        self, industry_code: str, frequency: str, start_date: str, end_date: str
    ) -> bool:
        """Check if data already exists for an industry/frequency/date range.

        Args:
            industry_code: Industry code
            frequency: daily/weekly/monthly
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            True if all data exists, False otherwise
        """
        table = f"industry_{frequency}_charts"
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            f"""
            SELECT COUNT(*) as count FROM {table}
            WHERE industry_code = ? AND date BETWEEN ? AND ?
            """,
            [industry_code, start, end],
        ).fetchall()

        actual_count = result[0][0] if result else 0

        # If no data exists, return False
        if actual_count == 0:
            return False

        return True

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

        self.connection.execute("DELETE FROM daily_charts")
        self.connection.execute("DELETE FROM weekly_charts")
        self.connection.execute("DELETE FROM monthly_charts")
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
