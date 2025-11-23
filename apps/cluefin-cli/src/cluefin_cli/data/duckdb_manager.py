"""DuckDB management for stock chart data storage."""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd
from loguru import logger


# Exchange code mapping: Full name (NYSE, NASDAQ) → API code (NYS, NAS)
EXCHANGE_CODE_TO_API = {
    "NYSE": "NYS",
    "NASDAQ": "NAS",
}


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
        # Domestic industry daily charts table (KIS API)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS domestic_industry_daily_charts (
                industry_code VARCHAR NOT NULL,
                date DATE NOT NULL,

                -- OHLCV from output2 (daily data)
                open DECIMAL NOT NULL,
                high DECIMAL NOT NULL,
                low DECIMAL NOT NULL,
                close DECIMAL NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,
                mod_yn VARCHAR,

                -- Fields from output1 (metadata, constant per API call)
                prdy_vrss_sign VARCHAR,
                bstp_nmix_prdy_ctrt DECIMAL,
                prdy_nmix DECIMAL,
                hts_kor_isnm VARCHAR,
                bstp_cls_code VARCHAR,
                prdy_vol BIGINT,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (industry_code, date)
            )
        """)

        # Domestic stock metadata table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS domestic_stock_metadata (
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

        # Domestic industry codes table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS domestic_industry_codes (
                code VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)

        # Domestic stock daily charts table (KIS API)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS domestic_stock_daily_charts (
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

        # Overseas stock metadata table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS overseas_stock_metadata (
                stock_code VARCHAR PRIMARY KEY,
                -- Master file fields
                stock_name_en VARCHAR,
                stock_name_kr VARCHAR,
                -- ProductBaseInfoItem API fields
                std_pdno VARCHAR,
                prdt_eng_name VARCHAR,
                natn_cd VARCHAR,
                natn_name VARCHAR,
                tr_mket_cd VARCHAR,
                tr_mket_name VARCHAR,
                ovrs_excg_cd VARCHAR,
                ovrs_excg_name VARCHAR,
                tr_crcy_cd VARCHAR,
                ovrs_papr VARCHAR,
                crcy_name VARCHAR,
                ovrs_stck_dvsn_cd VARCHAR,
                prdt_clsf_cd VARCHAR,
                prdt_clsf_name VARCHAR,
                lstg_stck_num VARCHAR,
                lstg_dt VARCHAR,
                ovrs_stck_tr_stop_dvsn_cd VARCHAR,
                lstg_abol_item_yn VARCHAR,
                lstg_yn VARCHAR,
                tax_levy_yn VARCHAR,
                ovrs_item_name VARCHAR,
                sedol_no VARCHAR,
                prdt_name VARCHAR,
                lstg_abol_dt VARCHAR,
                ptp_item_yn VARCHAR,
                dtm_tr_psbl_yn VARCHAR,
                ovrs_stck_etf_risk_drtp_cd VARCHAR
            )
        """)

        # Overseas stock daily charts table (KIS API)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS overseas_stock_daily_charts (
                exchange_code VARCHAR NOT NULL,
                stock_code VARCHAR NOT NULL,
                date DATE NOT NULL,
                open DECIMAL NOT NULL,
                high DECIMAL NOT NULL,
                low DECIMAL NOT NULL,
                close DECIMAL NOT NULL,
                volume BIGINT NOT NULL,
                trading_amount BIGINT NOT NULL,

                -- Additional fields from KIS API
                sign VARCHAR,
                diff DECIMAL,
                rate DECIMAL,

                -- Fields from output1
                zdiv VARCHAR,

                -- Metadata
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (exchange_code, stock_code, date)
            )
        """)

        logger.debug("DuckDB tables created/verified")

    def insert_domestic_industry_daily_chart(self, industry_code: str, df: pd.DataFrame) -> int:
        """Insert domestic industry daily chart data.

        Args:
            industry_code: Industry code
            df: DataFrame with columns matching domestic_industry_daily_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for domestic industry daily chart: {industry_code}")
            return 0

        # Prepare data
        insert_df = self._prepare_industry_chart_data(industry_code, df)

        try:
            self.connection.register("insert_df", insert_df)
            self.connection.execute(
                """INSERT INTO domestic_industry_daily_charts
                (industry_code, date, open, high, low, close, volume, trading_amount,
                 mod_yn, prdy_vrss_sign, bstp_nmix_prdy_ctrt, prdy_nmix, hts_kor_isnm, bstp_cls_code, prdy_vol)
                SELECT industry_code, date, open, high, low, close, volume, trading_amount,
                       mod_yn, prdy_vrss_sign, bstp_nmix_prdy_ctrt, prdy_nmix, hts_kor_isnm, bstp_cls_code, prdy_vol
                FROM insert_df
                ON CONFLICT (industry_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(insert_df)
            logger.info(f"Inserted {count} domestic industry daily chart records for {industry_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting domestic industry daily chart for {industry_code}: {e}")
            raise

    def insert_domestic_stock_daily_chart(self, stock_code: str, df: pd.DataFrame) -> int:
        """Insert domestic stock daily chart data from KIS API.

        Args:
            stock_code: Stock code
            df: DataFrame with columns matching domestic_stock_daily_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for domestic stock daily chart: {stock_code}")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO domestic_stock_daily_charts
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
            logger.debug(f"Inserted {count} domestic stock daily chart records for {stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting domestic stock daily chart for {stock_code}: {e}")
            raise

    def insert_overseas_stock_daily_chart(self, exchange_code: str, stock_code: str, df: pd.DataFrame) -> int:
        """Insert overseas stock daily chart data from KIS API.

        Args:
            exchange_code: Exchange code (NYS, NAS, AMS, HKS, TSE, etc.)
            stock_code: Stock code/symbol (e.g., TSLA)
            df: DataFrame with columns matching overseas_stock_daily_charts schema

        Returns:
            Number of records inserted
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for overseas stock {exchange_code}:{stock_code}")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO overseas_stock_daily_charts
                (exchange_code, stock_code, date, open, high, low, close, volume, trading_amount,
                 sign, diff, rate, zdiv)
                SELECT exchange_code, stock_code, date, open, high, low, close, volume, trading_amount,
                       sign, diff, rate, zdiv
                FROM insert_df
                ON CONFLICT (exchange_code, stock_code, date) DO UPDATE SET created_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.debug(f"Inserted {count} overseas stock daily chart records for {exchange_code}:{stock_code}")
            return count
        except Exception as e:
            logger.error(f"Error inserting overseas stock daily chart for {exchange_code}:{stock_code}: {e}")
            raise

    def _prepare_industry_chart_data(self, industry_code: str, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare industry chart data for insertion.

        For KIS API data, the DataFrame is already prepared by IndustryChartImporter
        with all required columns. This method just ensures data types are correct.

        Args:
            industry_code: Industry code (for reference)
            df: DataFrame from IndustryChartImporter with correct schema

        Returns:
            Prepared DataFrame (passed through with minor type conversions)
        """
        # DataFrame is already properly formatted by IndustryChartImporter
        # Just ensure numeric columns are correct type
        result = df.copy()

        # Ensure key columns have correct types
        numeric_cols = ["open", "high", "low", "close", "bstp_nmix_prdy_ctrt", "prdy_nmix"]
        for col in numeric_cols:
            if col in result.columns:
                result[col] = pd.to_numeric(result[col], errors="coerce")

        return result

    def update_domestic_stock_metadata(
        self,
        stock_code: str,
        stock_name: Optional[str] = None,
    ) -> None:
        """Update domestic stock metadata.

        Args:
            stock_code: Stock code
            stock_name: Stock name (optional)
        """
        today = datetime.now().date()
        next_import_date = today + timedelta(days=1)

        self.connection.execute(
            """
            INSERT INTO domestic_stock_metadata
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

    def upsert_domestic_stock_metadata_extended(self, df: pd.DataFrame) -> int:
        """Upsert extended domestic stock metadata from combined API responses.

        Args:
            df: DataFrame with all domestic stock metadata columns including:
                stock_code, stock_name, listing_date, market_name, market_code,
                industry_name, company_size, company_class, audit_info, stock_state,
                investment_warning, settlement_month, face_value, capital, float_stock,
                per, eps, roe, pbr, bps, sales_amount, business_profit, net_income,
                market_cap, foreign_ownership_rate, distribution_rate, distribution_stock

        Returns:
            Number of records upserted
        """
        if df.empty:
            logger.warning("Empty DataFrame for domestic stock metadata")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO domestic_stock_metadata
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
            logger.info(f"Upserted {count} domestic stock metadata records")
            return count
        except Exception as e:
            logger.error(f"Error upserting domestic stock metadata: {e}")
            raise

    def upsert_overseas_stock_metadata(self, df: pd.DataFrame) -> int:
        """Upsert overseas stock metadata from master file and ProductBaseInfo API.

        Args:
            df: DataFrame with overseas stock metadata columns including:
                stock_code, stock_name_en, stock_name_kr, std_pdno, prdt_eng_name,
                natn_cd, natn_name, tr_mket_cd, tr_mket_name, ovrs_excg_cd,
                ovrs_excg_name, tr_crcy_cd, ovrs_papr, crcy_name, ovrs_stck_dvsn_cd,
                prdt_clsf_cd, prdt_clsf_name, lstg_stck_num, lstg_dt,
                ovrs_stck_tr_stop_dvsn_cd, lstg_abol_item_yn, lstg_yn, tax_levy_yn,
                ovrs_item_name, sedol_no, prdt_name, lstg_abol_dt, ptp_item_yn,
                dtm_tr_psbl_yn, ovrs_stck_etf_risk_drtp_cd

        Returns:
            Number of records upserted
        """
        if df.empty:
            logger.warning("Empty DataFrame for overseas stock metadata")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO overseas_stock_metadata
                (stock_code, stock_name_en, stock_name_kr, std_pdno, prdt_eng_name,
                 natn_cd, natn_name, tr_mket_cd, tr_mket_name, ovrs_excg_cd,
                 ovrs_excg_name, tr_crcy_cd, ovrs_papr, crcy_name, ovrs_stck_dvsn_cd,
                 prdt_clsf_cd, prdt_clsf_name, lstg_stck_num, lstg_dt,
                 ovrs_stck_tr_stop_dvsn_cd, lstg_abol_item_yn, lstg_yn, tax_levy_yn,
                 ovrs_item_name, sedol_no, prdt_name, lstg_abol_dt, ptp_item_yn,
                 dtm_tr_psbl_yn, ovrs_stck_etf_risk_drtp_cd)
                SELECT stock_code, stock_name_en, stock_name_kr, std_pdno, prdt_eng_name,
                       natn_cd, natn_name, tr_mket_cd, tr_mket_name, ovrs_excg_cd,
                       ovrs_excg_name, tr_crcy_cd, ovrs_papr, crcy_name, ovrs_stck_dvsn_cd,
                       prdt_clsf_cd, prdt_clsf_name, lstg_stck_num, lstg_dt,
                       ovrs_stck_tr_stop_dvsn_cd, lstg_abol_item_yn, lstg_yn, tax_levy_yn,
                       ovrs_item_name, sedol_no, prdt_name, lstg_abol_dt, ptp_item_yn,
                       dtm_tr_psbl_yn, ovrs_stck_etf_risk_drtp_cd
                FROM insert_df
                ON CONFLICT (stock_code) DO UPDATE SET
                    stock_name_en = EXCLUDED.stock_name_en,
                    stock_name_kr = EXCLUDED.stock_name_kr,
                    std_pdno = EXCLUDED.std_pdno,
                    prdt_eng_name = EXCLUDED.prdt_eng_name,
                    natn_cd = EXCLUDED.natn_cd,
                    natn_name = EXCLUDED.natn_name,
                    tr_mket_cd = EXCLUDED.tr_mket_cd,
                    tr_mket_name = EXCLUDED.tr_mket_name,
                    ovrs_excg_cd = EXCLUDED.ovrs_excg_cd,
                    ovrs_excg_name = EXCLUDED.ovrs_excg_name,
                    tr_crcy_cd = EXCLUDED.tr_crcy_cd,
                    ovrs_papr = EXCLUDED.ovrs_papr,
                    crcy_name = EXCLUDED.crcy_name,
                    ovrs_stck_dvsn_cd = EXCLUDED.ovrs_stck_dvsn_cd,
                    prdt_clsf_cd = EXCLUDED.prdt_clsf_cd,
                    prdt_clsf_name = EXCLUDED.prdt_clsf_name,
                    lstg_stck_num = EXCLUDED.lstg_stck_num,
                    lstg_dt = EXCLUDED.lstg_dt,
                    ovrs_stck_tr_stop_dvsn_cd = EXCLUDED.ovrs_stck_tr_stop_dvsn_cd,
                    lstg_abol_item_yn = EXCLUDED.lstg_abol_item_yn,
                    lstg_yn = EXCLUDED.lstg_yn,
                    tax_levy_yn = EXCLUDED.tax_levy_yn,
                    ovrs_item_name = EXCLUDED.ovrs_item_name,
                    sedol_no = EXCLUDED.sedol_no,
                    prdt_name = EXCLUDED.prdt_name,
                    lstg_abol_dt = EXCLUDED.lstg_abol_dt,
                    ptp_item_yn = EXCLUDED.ptp_item_yn,
                    dtm_tr_psbl_yn = EXCLUDED.dtm_tr_psbl_yn,
                    ovrs_stck_etf_risk_drtp_cd = EXCLUDED.ovrs_stck_etf_risk_drtp_cd"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.info(f"Upserted {count} overseas stock metadata records")
            return count
        except Exception as e:
            logger.error(f"Error upserting overseas stock metadata: {e}")
            raise

    def insert_domestic_industry_codes(self, df: pd.DataFrame) -> int:
        """Insert domestic industry codes.

        Args:
            df: DataFrame with columns: code, name

        Returns:
            Number of records inserted/updated
        """
        if df.empty:
            logger.warning("Empty DataFrame for domestic industry codes")
            return 0

        try:
            self.connection.register("insert_df", df)
            self.connection.execute(
                """INSERT INTO domestic_industry_codes
                (code, name)
                SELECT code, name
                FROM insert_df
                ON CONFLICT (code) DO UPDATE SET
                    name = EXCLUDED.name,
                    updated_at = NOW()"""
            )
            self.connection.unregister("insert_df")
            count = len(df)
            logger.info(f"Inserted/updated {count} domestic industry code records")
            return count
        except Exception as e:
            logger.error(f"Error inserting domestic industry codes: {e}")
            raise

    def get_domestic_industry_codes(self) -> pd.DataFrame:
        """Get domestic industry codes from database.

        Returns:
            DataFrame with domestic industry code data
        """
        result = self.connection.execute("SELECT * FROM domestic_industry_codes ORDER BY code").df()
        return result

    def get_overseas_stock_codes(self, exchange_code: str) -> list[str]:
        """Get overseas stock codes from database by exchange.

        Args:
            exchange_code: Exchange code (NYSE for NYSE, NASD for NASDAQ)

        Returns:
            List of stock codes
        """
        result = self.connection.execute(
            "SELECT stock_code FROM overseas_stock_metadata WHERE ovrs_excg_cd = ? ORDER BY stock_code",
            [exchange_code],
        ).fetchall()
        return [row[0] for row in result]

    def get_database_stats(self) -> dict:
        """Get database statistics.

        Returns:
            Dictionary with table statistics
        """
        stats = {}

        # Count domestic stock daily chart records (new KIS data)
        result = self.connection.execute("SELECT COUNT(*) as count FROM domestic_stock_daily_charts").fetchall()
        stats["domestic_stock_daily_charts_count"] = result[0][0] if result else 0

        result = self.connection.execute(
            "SELECT COUNT(DISTINCT stock_code) as count FROM domestic_stock_daily_charts"
        ).fetchall()
        stats["domestic_stock_daily_charts_stocks"] = result[0][0] if result else 0

        # Count domestic industry daily chart records
        result = self.connection.execute("SELECT COUNT(*) as count FROM domestic_industry_daily_charts").fetchall()
        stats["domestic_industry_daily_charts_count"] = result[0][0] if result else 0

        result = self.connection.execute(
            "SELECT COUNT(DISTINCT industry_code) as count FROM domestic_industry_daily_charts"
        ).fetchall()
        stats["domestic_industry_daily_charts_industries"] = result[0][0] if result else 0

        # Count metadata
        result = self.connection.execute("SELECT COUNT(*) as count FROM domestic_stock_metadata").fetchall()
        stats["domestic_tracked_stocks"] = result[0][0] if result else 0

        # Count domestic industry codes
        result = self.connection.execute("SELECT COUNT(*) as count FROM domestic_industry_codes").fetchall()
        stats["domestic_industry_codes_count"] = result[0][0] if result else 0

        # Count overseas stock daily chart records
        result = self.connection.execute("SELECT COUNT(*) as count FROM overseas_stock_daily_charts").fetchall()
        stats["overseas_stock_daily_charts_count"] = result[0][0] if result else 0

        result = self.connection.execute(
            "SELECT COUNT(DISTINCT CONCAT(exchange_code, ':', stock_code)) as count FROM overseas_stock_daily_charts"
        ).fetchall()
        stats["overseas_stock_daily_charts_stocks"] = result[0][0] if result else 0

        # Count overseas stock metadata
        result = self.connection.execute("SELECT COUNT(*) as count FROM overseas_stock_metadata").fetchall()
        stats["overseas_stock_metadata_count"] = result[0][0] if result else 0

        # Database size
        db_size = os.path.getsize(self.db_path)
        stats["database_size_mb"] = round(db_size / (1024 * 1024), 2)

        return stats

    def get_stock_date_range(self, stock_code: str, table: str = "domestic_stock_daily_charts") -> Optional[tuple]:
        """Get date range for a stock in a table.

        Args:
            stock_code: Stock code
            table: Table name (domestic_stock_daily_charts, industry_daily_charts)

        Returns:
            Tuple of (min_date, max_date) or None if no data
        """
        result = self.connection.execute(
            f"SELECT MIN(date), MAX(date) FROM {table} WHERE stock_code = ?", [stock_code]
        ).fetchall()

        if result and result[0][0] is not None:
            return (result[0][0], result[0][1])
        return None

    def check_domestic_stock_data_exists(self, stock_code: str, start_date: str, end_date: str) -> bool:
        """Check if domestic stock daily data already exists for a stock/date range.

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
            SELECT COUNT(*) as count FROM domestic_stock_daily_charts
            WHERE stock_code = ? AND date BETWEEN ? AND ?
            """,
            [stock_code, start, end],
        ).fetchall()

        actual_count = result[0][0] if result else 0
        return actual_count > 0

    def check_domestic_stock_data_exists_batch(
        self, stock_codes: list[str], start_date: str, end_date: str
    ) -> dict[str, bool]:
        """Check if domestic stock daily data exists for multiple stocks in batch.

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
            FROM domestic_stock_daily_charts
            WHERE stock_code IN ({placeholders})
              AND date BETWEEN ? AND ?
            GROUP BY stock_code
        """

        result = self.connection.execute(query, [*stock_codes, start, end]).fetchall()

        exists_map = {row[0]: row[1] > 0 for row in result}

        for stock_code in stock_codes:
            if stock_code not in exists_map:
                exists_map[stock_code] = False

        return exists_map

    def check_overseas_stock_data_exists(
        self, exchange_code: str, stock_code: str, start_date: str, end_date: str
    ) -> bool:
        """Check if overseas stock daily data already exists for a stock/date range.

        Args:
            exchange_code: Exchange code (NYS, NAS, AMS, HKS, TSE, etc.)
            stock_code: Stock code/symbol
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)

        Returns:
            True if any data exists, False otherwise
        """
        start = pd.to_datetime(start_date, format="%Y%m%d").date()
        end = pd.to_datetime(end_date, format="%Y%m%d").date()

        result = self.connection.execute(
            """
            SELECT COUNT(*) as count FROM overseas_stock_daily_charts
            WHERE exchange_code = ? AND stock_code = ? AND date BETWEEN ? AND ?
            """,
            [exchange_code, stock_code, start, end],
        ).fetchall()

        actual_count = result[0][0] if result else 0
        return actual_count > 0

    def check_overseas_stock_data_exists_batch(
        self, exchange_code: str, stock_codes: list[str], start_date: str, end_date: str
    ) -> dict[str, bool]:
        """Check if overseas stock daily data exists for multiple stocks in batch.

        Args:
            exchange_code: Exchange code (NYS, NAS, AMS, HKS, TSE, etc.)
            stock_codes: List of stock codes/symbols
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
            FROM overseas_stock_daily_charts
            WHERE exchange_code = ? AND stock_code IN ({placeholders})
              AND date BETWEEN ? AND ?
            GROUP BY stock_code
        """

        result = self.connection.execute(query, [exchange_code, *stock_codes, start, end]).fetchall()

        exists_map = {row[0]: row[1] > 0 for row in result}

        for stock_code in stock_codes:
            if stock_code not in exists_map:
                exists_map[stock_code] = False

        return exists_map

    def check_domestic_industry_data_exists(self, industry_code: str, start_date: str, end_date: str) -> bool:
        """Check if daily data already exists for a domestic industry/date range.

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
            SELECT COUNT(*) as count FROM domestic_industry_daily_charts
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

        self.connection.execute("DELETE FROM domestic_industry_daily_charts")
        self.connection.execute("DELETE FROM domestic_stock_metadata")
        self.connection.execute("DELETE FROM domestic_industry_codes")
        self.connection.execute("DELETE FROM overseas_stock_daily_charts")
        self.connection.execute("DELETE FROM overseas_stock_metadata")
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
