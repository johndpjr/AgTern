from argparse import Namespace
from threading import Thread
from typing import List

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from agtern.common import LOG, Internship, InternshipCreateSchema
from agtern.server.database import get_db
from agtern.server.scraping import start_scraper

from .database import DatabaseInternship, crud, engine, models
from .utils import import_companies, sort_companies

models.DatabaseModel.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/internships/", response_model=List[Internship])
async def get_all_internships(db: Session = Depends(get_db)):
    """Returns all internships from the database"""
    return crud.get_all_internships(db)


@app.post("/api/internships/", response_model=Internship)
async def create_internship(
    internship: InternshipCreateSchema, db: Session = Depends(get_db)
):
    """Adds an Internship object to the database."""
    db_internship = DatabaseInternship(
        **{
            k: v
            for k, v in internship.dict().items()
            if k in DatabaseInternship.__table__.columns.keys() and v is not None
        }
    )
    return crud.create_internship(db, db_internship)


def run():
    uvicorn.run("agtern.server:app", host="0.0.0.0", port=5000, log_level="info")


def start_server(args: Namespace):
    if not args.save_internships:
        LOG.warning(
            "Internships won't be stored to db; use --save-internships to store to db"
        )

    if args.scrape_only:
        args.headless = False
        start_scraper(args)
        return

    Thread(target=run, daemon=True).start()

    if args.update_companies:
        LOG.info("Updating company info...")
        try:
            sort_companies()
            import_companies()
        except Exception as e:
            LOG.error(f"An exception occurred: {e}", exc_info=True)

    if not args.no_scrape:
        start_scraper(args)
