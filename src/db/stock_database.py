import os
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
def create_stock_table():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            ticker TEXT NOT NULL,
            date DATE NOT NULL,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            volume BIGINT,
            PRIMARY KEY (ticker, date)
        );
        """))

# -----------------------------
# BULK INSERT
# -----------------------------
def insert_stock_prices(records: list[dict]) -> int:
    if not records:
        return 0

    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO stock_prices (
                    ticker,
                    date,
                    open,
                    high,
                    low,
                    close,
                    volume
                )
                VALUES (
                    :ticker,
                    :date,
                    :open,
                    :high,
                    :low,
                    :close,
                    :volume
                )
                ON CONFLICT (ticker, date) DO NOTHING
            """),
            records
        )

        return result.rowcount

# -----------------------------
# WATERMARK
# -----------------------------
def get_all_latest_stock_dates():
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT ticker, MAX(date) AS latest_date
            FROM stock_prices
            GROUP BY ticker
        """))

        rows = result.mappings().all()

    if not rows:
        return pd.DataFrame(columns=["ticker", "latest_date"])

    return pd.DataFrame(rows)

@lru_cache(maxsize=20)
def fetch_stock_data(ticker: str):
    df = pd.read_sql_query(
        text("""
            SELECT *
            FROM stock_prices            
            WHERE ticker = :ticker
            ORDER BY date DESC
        """),
        engine,
        params={"ticker": ticker},
    )

    df["date"] = pd.to_datetime(df["date"])

    return df