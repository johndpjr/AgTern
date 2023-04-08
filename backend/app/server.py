from argparse import Namespace
from os import makedirs, system
from threading import Thread
from time import sleep

import uvicorn
from fastapi import FastAPI

from .api import api_router
from .core import settings
from .database import DatabaseModel, engine
from .scraping import start_scraper
from .spa import SinglePageApplication
from .utils import LOG, import_companies, sort_companies

DatabaseModel.metadata.create_all(bind=engine)

app = FastAPI(title="AgTern", generate_unique_id_function=lambda route: route.name)

app.include_router(api_router, prefix=settings.API_V1_STR)

client_dir = "./frontend/dist/agtern-client"
makedirs(client_dir, exist_ok=True)
app.mount(
    "/",
    SinglePageApplication(directory=client_dir, html=True),
    name="AgTern",
)


def run_server():
    uvicorn.run(
        "backend.app.server:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
    )


def generate_client():
    sleep(1)
    # The rmtree is not needed (openapi-typescript-codegen does it automatically)
    # rmtree("./frontend/src/_generated", ignore_errors=True)
    system("cd frontend && npm run update-api-client")


def start_server(args: Namespace):
    if not args.save_jobs:
        LOG.warning("Jobs won't be stored to db; use --save-jobs to store to db")

    if args.scrape_only:
        args.headless = False
        start_scraper(args)
        return

    if args.dev:
        Thread(target=generate_client, daemon=True).start()
    Thread(target=run_server).start()

    if args.update_companies:
        LOG.info("Updating company info...")
        try:
            # deprecated because we are no longer using companies.csv
            # sort_companies()
            # import_companies()
            print(
                "NOTE: THIS IS DEPRECATED. WE ARE NO LONGER SORTING USING COMPANIES.CSV"
            )
        except Exception as e:
            LOG.error(f"An exception occurred: {e}", exc_info=True)

    if not args.no_scrape:
        start_scraper(args)
