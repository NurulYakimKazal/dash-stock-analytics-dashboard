import logging
import yfinance as yf
import pandas as pd
from datetime import timedelta, datetime

from src.db.stock_database import (
    create_stock_tables,
    insert_stock_prices,
    get_all_latest_stock_dates
)

from utils.config import TICKERS, DEFAULT_START

def run_stock_etl():

    create_stock_tables()
    logger = logging.getLogger(__name__)

    latest_dates = get_all_latest_stock_dates()

    if latest_dates.empty:
        start = DEFAULT_START
    else:
        start = latest_dates["latest_date"].min() + timedelta(days=1)

    today = datetime.today().date()

    if start >= today:
        logger.info("Stock data already up to date.")
        return

    df = yf.download(
        TICKERS,
        start=start,
        interval="1d",
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        threads=True,
    )

    if df is None or df.empty:
        logger.warning("Empty dataframe")
        return

    if not isinstance(df.columns, pd.MultiIndex):
        logger.error("Unexpected yfinance format")
        return

    # =========================================================
    # 🔥 VECTORIZE EVERYTHING (NO LOOP)
    # =========================================================

    # Stack ticker level into rows
    stock_df = (
        df.stack(level=0, future_stack=True)
        .reset_index()
        .rename(columns={
            "Date": "date",
            "Ticker": "ticker",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })
    )

    if "date" not in stock_df.columns:
        logger.error("Missing Date column")
        return

    # Convert datetime to Python date for PostgreSQL DATE column
    # Convert pandas datetime to Python date for PostgreSQL DATE
    stock_df["date"] = pd.to_datetime(
        stock_df["date"]
    ).dt.date

    # Prepare database records
    records_df = (
        stock_df[
            [
                "ticker",
                "date",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]
        .dropna(subset=["close"])
        .drop_duplicates(
            subset=["ticker", "date"]
        )
    )

    records = records_df.to_dict("records")

    if not records:
        logger.warning("No valid records to insert")
        return

    inserted = insert_stock_prices(records)

    logger.info("Inserted rows: %d", inserted)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_stock_etl()