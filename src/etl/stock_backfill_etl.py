import logging
import yfinance as yf
import pandas as pd

from src.db.stock_database import (
    create_stock_tables,
    insert_stock_prices
)

from utils.config import TICKERS, DEFAULT_START


def run_stock_backfill():

    create_stock_tables()

    logger = logging.getLogger(__name__)
    logger.info("Downloading all tickers...")

    df = yf.download(
        TICKERS,
        start=DEFAULT_START,
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

    try:
        # Convert MultiIndex columns (ticker -> OHLCV) into rows
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

        # Single bulk insert for all tickers
        inserted = insert_stock_prices(records)

        logger.info(
            "Backfill complete: sent=%d inserted=%d skipped=%d",
            len(records),
            inserted,
            len(records) - inserted,
        )

    except Exception:
        logger.exception("Backfill failed")