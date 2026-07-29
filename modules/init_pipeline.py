from src.db.stock_database import fetch_stock_data
from src.db.company_database import fetch_company_data

_db_initialized = False


def init_db_and_sync(create_tables, run_stock_etl, run_company_etl):
    global _db_initialized

    # Create tables once
    if not _db_initialized:
        create_tables()
        _db_initialized = True

    try:
        run_stock_etl()
        fetch_stock_data.cache_clear()

        run_company_etl()
        fetch_company_data.cache_clear()

        print("Stock and company data sync completed.")

    except Exception as e:
        print(f"ETL failed: {e}")