import logging
from src.etl.financial_backfill_etl import run_financial_backfill


if __name__ == "__main__":
    try:
        run_financial_backfill()
    except Exception as e:
        logging.exception(f"Backfill failed: {e}")
        raise