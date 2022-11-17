from argparse import Namespace
from os import makedirs, system
from shutil import rmtree
from threading import Thread
from time import sleep

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

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
makedirs(client_dir)
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
    rmtree("./frontend/src/_generated", ignore_errors=True)
    system("cd frontend && npm run update-api-client")


def start_server(args: Namespace):
    if not args.save_internships:
        LOG.warning(
            "Internships won't be stored to db; use --save-internships to store to db"
        )

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
            sort_companies()
            import_companies()
        except Exception as e:
            LOG.error(f"An exception occurred: {e}", exc_info=True)

    if not args.no_scrape:
        start_scraper(args)
