import logging
from src.etl.stock_backfill_etl import run_stock_backfill


if __name__ == "__main__":
    try:
        run_stock_backfill()
    except Exception as e:
        logging.exception(f"Backfill failed: {e}")
        raise