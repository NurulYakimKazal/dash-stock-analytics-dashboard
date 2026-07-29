from src.db.company_database import fetch_company_data
from src.db.stock_database import fetch_stock_data


_db_initialized = False


def init_db_and_sync(create_companies_table, create_stock_table, run_company_etl, run_stock_etl):
    global _db_initialized

    # Create tables once
    if not _db_initialized:
        create_companies_table()
        create_stock_table()
        _db_initialized = True

    try:
        run_company_etl()
        fetch_company_data.cache_clear()

        run_stock_etl()
        fetch_stock_data.cache_clear()

        print("Company and stock data sync completed.")

    except Exception as e:
        print(f"ETL failed: {e}")