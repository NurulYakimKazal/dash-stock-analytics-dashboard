import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from modules.init_pipeline import init_db_and_sync
from src.db.company_database import create_companies_table
from src.db.stock_database import create_stock_table
from src.etl.company_etl import run_company_etl
from src.etl.stock_incremental_etl import run_stock_etl


def sync():
    print(f"Starting company and stock sync: {datetime.now(timezone.utc)}")

    init_db_and_sync(
        create_companies_table,
        create_stock_table,
        run_company_etl,
        run_stock_etl
    )

    print("Company and stock data sync complete")


if __name__ == "__main__":
    sync()