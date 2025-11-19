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

        # Stock daily charts table (KIS API)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS stock_daily_charts (
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open BIGINT NOT NULL,
                high BIGINT NOT NULL,
                low BIGINT NOT NULL,
                close BIGINT NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,
                
                -- Additional fields from KIS API
                flng_cls_code VARCHAR,
                prtt_rate DECIMAL,
                mod_yn VARCHAR,
                prdy_vrss_sign VARCHAR,
                prdy_vrss BIGINT,
                revl_issu_reas VARCHAR,
                
                -- Fields from output1
                vol_tnrt DECIMAL,
                lstn_stcn BIGINT,
                hts_avls BIGINT,
                per DECIMAL,
                eps DECIMAL,
                pbr DECIMAL,
                
                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (stock_code, date)
            )
        """)

        logger.debug("DuckDB tables created/verified")

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

    def insert_stock_daily_chart(self, stock_code: str, df: pd.DataFrame) -> int:
        """Insert stock daily chart data from KIS API.

        Args:
            stock_code: Stock code
            df: DataFrame with columns matching stock_daily_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for stock daily chart: {stock_code}")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO stock_daily_charts
                (stock_code, date, open, high, low, close, volume, trading_amount,
                 flng_cls_code, prtt_rate, mod_yn, prdy_vrss_sign, prdy_vrss, revl_issu_reas,
                 vol_tnrt, lstn_stcn, hts_avls, per, eps, pbr)
                SELECT stock_code, date, open, high, low, close, volume, trading_amount,
                       flng_cls_code, prtt_rate, mod_yn, prdy_vrss_sign, prdy_vrss, revl_issu_reas,
                       vol_tnrt, lstn_stcn, hts_avls, per, eps, pbr
                FROM insert_df
                ON CONFLICT (stock_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.debug(f"Inserted {count} stock daily chart records for {stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting stock daily chart for {stock_code}: {e}")
            raise

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

        # Count stock daily chart records (new KIS data)
        result = self.connection.execute("SELECT COUNT(*) as count FROM stock_daily_charts").fetchall()
        stats["stock_daily_charts_count"] = result[0][0] if result else 0

        result = self.connection.execute("SELECT COUNT(DISTINCT stock_code) as count FROM stock_daily_charts").fetchall()
        stats["stock_daily_charts_stocks"] = result[0][0] if result else 0

        # Count industry daily chart records
        result = self.connection.execute("SELECT COUNT(*) as count FROM industry_daily_charts").fetchall()
        stats["industry_daily_charts_count"] = result[0][0] if result else 0

        result = self.connection.execute("SELECT COUNT(DISTINCT industry_code) as count FROM industry_daily_charts").fetchall()
        stats["industry_daily_charts_industries"] = result[0][0] if result else 0

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

    def get_stock_date_range(self, stock_code: str, table: str = "stock_daily_charts") -> Optional[tuple]:
        """Get date range for a stock in a table.

        Args:
            stock_code: Stock code
            table: Table name (stock_daily_charts, industry_daily_charts)

        Returns:
            Tuple of (min_date, max_date) or None if no data
        """
        result = self.connection.execute(
            f"SELECT MIN(date), MAX(date) FROM {table} WHERE stock_code = ?", [stock_code]
        ).fetchall()

        if result and result[0][0] is not None:
            return (result[0][0], result[0][1])
        return None

    def check_stock_data_exists(self, stock_code: str, start_date: str, end_date: str) -> bool:
        """Check if stock daily data already exists for a stock/date range.

        Args:
            stock_code: Stock code
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            True if all data exists, False otherwise
        """
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            """
            SELECT COUNT(*) as count FROM stock_daily_charts
            WHERE stock_code = ? AND date BETWEEN ? AND ?
            """,
            [stock_code, start, end],
        ).fetchall()

        actual_count = result[0][0] if result else 0
        return actual_count > 0

    def check_stock_data_exists_batch(
        self, stock_codes: list[str], start_date: str, end_date: str
    ) -> dict[str, bool]:
        """Check if stock daily data exists for multiple stocks in batch.

        Args:
            stock_codes: List of stock codes
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            Dictionary mapping stock_code to existence status (True if data exists)
        """
        if not stock_codes:
            return {}

        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        placeholders = ",".join("?" * len(stock_codes))
        query = f"""
            SELECT stock_code, COUNT(*) as count
            FROM stock_daily_charts
            WHERE stock_code IN ({placeholders})
              AND date BETWEEN ? AND ?
            GROUP BY stock_code
        """

        result = self.connection.execute(
            query, [*stock_codes, start, end]
        ).fetchall()

        exists_map = {row[0]: row[1] > 0 for row in result}

        for stock_code in stock_codes:
            if stock_code not in exists_map:
                exists_map[stock_code] = False

        return exists_map

    def check_industry_data_exists(self, industry_code: str, start_date: str, end_date: str) -> bool:
        """Check if daily data already exists for an industry/date range.

        Args:
            industry_code: Industry code
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            True if all data exists, False otherwise
        """
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            """
            SELECT COUNT(*) as count FROM industry_daily_charts
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

        self.connection.execute("DELETE FROM industry_daily_charts")
        self.connection.execute("DELETE FROM stock_metadata")
        self.connection.execute("DELETE FROM industry_codes")
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
