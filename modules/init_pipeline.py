import time
from src.db.stock_database import fetch_stock_data

SYNC_INTERVAL = 3600  # 1 hour

_last_etl_run = None
_db_initialized = False


def init_db_and_sync(create_tables, run_etl):
    global _last_etl_run, _db_initialized

    # Create tables once
    if not _db_initialized:
        create_tables()
        _db_initialized = True

    # Check ETL interval
    now = time.time()

    if (
        _last_etl_run is None
        or (now - _last_etl_run) > SYNC_INTERVAL
    ):
        try:
            run_etl()

            # Clear stale in-memory data
            fetch_stock_data.cache_clear()

            _last_etl_run = now

            print("Stock data synced")

        except Exception as e:
            _last_etl_run = now
            print(f"ETL failed: {e}")