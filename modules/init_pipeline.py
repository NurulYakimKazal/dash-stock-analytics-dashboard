from src.db.stock_database import fetch_stock_data

_db_initialized = False


def init_db_and_sync(create_tables, run_etl):
    global _db_initialized

    # Create tables once
    if not _db_initialized:
        create_tables()
        _db_initialized = True

    try:
        run_etl()

        fetch_stock_data.cache_clear()

        print("Stock data synced")

    except Exception as e:
        print(f"ETL failed: {e}")