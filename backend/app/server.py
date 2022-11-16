from argparse import Namespace
from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api import api_router
from .core import settings
from .database import DatabaseModel, engine
from .scraping import start_scraper
from .spa.spa import SinglePageApplication
from .utils import LOG, import_companies, sort_companies

DatabaseModel.metadata.create_all(bind=engine)

app = FastAPI(title="AgTern")

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount(
    "/",
    SinglePageApplication(directory="./frontend/dist/agtern-client", html=True),
    name="AgTern",
)


def run():
    uvicorn.run(
        "backend.app.server:app", host="0.0.0.0", port=settings.PORT, log_level="info"
    )


def start_server(args: Namespace):
    if not args.save_internships:
        LOG.warning(
            "Internships won't be stored to db; use --save-internships to store to db"
        )

    if args.scrape_only:
        args.headless = False
        start_scraper(args)
        return

    Thread(target=run).start()

    if args.update_companies:
        LOG.info("Updating company info...")
        try:
            sort_companies()
            import_companies()
        except Exception as e:
            LOG.error(f"An exception occurred: {e}", exc_info=True)

    if not args.no_scrape:
        start_scraper(args)
