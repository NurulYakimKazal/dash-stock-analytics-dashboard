import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from modules.init_pipeline import init_db_and_sync
from src.db.stock_database import create_stock_table
from src.etl.stock_incremental_etl import run_stock_etl
from src.etl.company_etl import run_company_etl


def sync():
    print(f"Starting stock sync: {datetime.now(timezone.utc)}")

    init_db_and_sync(
        create_stock_table,
        run_stock_etl,
        run_company_etl
    )

    print("Data sync complete")


if __name__ == "__main__":
    sync()