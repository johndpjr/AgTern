from argparse import Namespace
from os import makedirs
from threading import Thread

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from backend.scraping import start_scraper

from .api import api_router
from .core import settings
from .database import DatabaseModel, engine
from .spa import SinglePageApplication
from .utils import LOG

load_dotenv()

DatabaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME, generate_unique_id_function=lambda route: route.name
)

app.include_router(api_router, prefix=settings.API_V1_STR)

client_dir = "./frontend/dist/agtern-client"
makedirs(client_dir, exist_ok=True)
app.mount(
    "/",
    SinglePageApplication(directory=client_dir, html=True),
    name=settings.APP_NAME,
)


def run_server():
    uvicorn.run(
        "backend.app.server:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
    )


def start_server(args: Namespace):
    if not args.save_jobs:
        LOG.warning("Jobs won't be stored to db; use --save-jobs to store to db")

    if args.scrape_only:
        args.headless = False
        start_scraper(args)
        return

    Thread(target=run_server).start()

    if not args.no_scrape:
        start_scraper(args)
