from argparse import Namespace

from celery import Celery
from celery.schedules import crontab

from backend.scraping.scraper import start_scraper

celery_app = Celery("tasks", broker="redis://localhost:6379/0")
args = Namespace(
    headless=True,
    no_scrape=False,
    scrape_only=True,
    save_jobs=True,
    multiprocessing=False,
    dev=True,
    include_companies=None,
    exclude_companies=None,
)

# Scrapes every day at 6 AM UTC, 12 AM CST
celery_app.conf.beat_schedule = {
    "scrape-every-day": {
        "task": "background.run",
        "schedule": crontab(hour=6, minute=0),
    }
}


@celery_app.task
def run():
    start_scraper(args)
