from apscheduler.schedulers.blocking import BlockingScheduler

from modules.init_pipeline import init_db_and_sync
from src.db.stock_database import create_stock_table
from src.etl.stock_incremental_etl import run_stock_etl
from datetime import datetime, timezone


scheduler = BlockingScheduler()


def sync():
    print(
        f"Starting stock sync: {datetime.now(timezone.utc)}"
    )

    init_db_and_sync(
        create_stock_table,
        run_stock_etl,
    )


scheduler.add_job(
    sync,
    trigger="cron",
    day_of_week="mon-fri",
    hour=23,
    minute=0,
    timezone="UTC",
)

scheduler.start()