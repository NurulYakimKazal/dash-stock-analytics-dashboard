import logging
import yfinance as yf

from src.db.company_database import (
    create_companies_table,
    upsert_company_info
)

from utils.config import TICKERS


def run_company_etl():

    logger = logging.getLogger(__name__)

    create_companies_table()

    records = []

    for ticker in TICKERS:
        try:
            info = yf.Ticker(ticker).info

            records.append({
                "ticker": ticker,
                "name": info.get("shortName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "trailing_pe": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
            })

        except Exception as e:
            logger.warning(
                "Failed fetching %s: %s",
                ticker,
                e
            )

    if not records:
        logger.warning("No company records fetched")
        return

    updated = upsert_company_info(records)

    logger.info(
        "Company records upserted: %d",
        updated
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_company_etl()