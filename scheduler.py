from apscheduler.schedulers.blocking import BlockingScheduler

from modules.init_pipeline import init_db_and_sync
from src.db.stock_database import create_stock_table
from src.etl.stock_incremental_etl import run_stock_etl

scheduler = BlockingScheduler()

scheduler.add_job(
    lambda: init_db_and_sync(
        create_stock_table,
        run_stock_etl,
    ),
    trigger="interval",
    minutes=60,
)

print("Scheduler started...")

scheduler.start()