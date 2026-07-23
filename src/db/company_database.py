import os
from typing import Callable
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from functools import lru_cache

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD_RAW = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT", "5432")
DBNAME = os.getenv("DB_NAME")

if not all([USER, PASSWORD_RAW, HOST, PORT, DBNAME]):
    raise ValueError("Missing one or more DB environment variables")

PASSWORD = quote_plus(PASSWORD_RAW)

DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    future=True,
)

# -----------------------------
# SCHEMA INIT
# -----------------------------
def create_companies_table():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS company_info (
            ticker VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(100),
            industry VARCHAR(150),
            market_cap BIGINT,
            trailing_pe NUMERIC(10, 2),
            dividend_yield NUMERIC(10, 4),
            beta NUMERIC(10, 4),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """))


# -----------------------------
# BULK UPSERT
# -----------------------------
def upsert_company_info(records: list[dict]) -> int | Callable[[], int]:

    if not records:
        return 0

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                INSERT INTO company_info
                (
                    ticker,
                    name,
                    sector,
                    industry,
                    market_cap,
                    trailing_pe,
                    dividend_yield,
                    beta
                )
                VALUES
                (
                    :ticker,
                    :name,
                    :sector,
                    :industry,
                    :market_cap,
                    :trailing_pe,
                    :dividend_yield,
                    :beta
                )
                ON CONFLICT (ticker)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    sector = EXCLUDED.sector,
                    industry = EXCLUDED.industry,
                    market_cap = EXCLUDED.market_cap,
                    trailing_pe = EXCLUDED.trailing_pe,
                    dividend_yield = EXCLUDED.dividend_yield,
                    beta = EXCLUDED.beta,
                    updated_at = CURRENT_TIMESTAMP
            """),
            records
        )

        return result.rowcount


@lru_cache(maxsize=20)
def fetch_company_data(ticker: str):

    df = pd.read_sql_query(
        text("""
            SELECT *
            FROM company_info
            WHERE ticker = :ticker
        """),
        engine,
        params={"ticker": ticker},
    )

    if not df.empty:
        df["updated_at"] = pd.to_datetime(
            df["updated_at"]
        )

    return df