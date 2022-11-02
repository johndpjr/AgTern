from argparse import Namespace
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List
from threading import Thread
import uvicorn

from ..common import LOG, schemas
from .database import (
    crud,
    models,
    engine,
    SessionLocal
)
from ..server import start_scraper
from .utils import sort_companies, import_companies


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/internships/", response_model=List[schemas.Internship])
async def get_all_internships(db: Session = Depends(get_db)):
    """Returns all internships from the database"""
    return crud.get_all_internships(db)

@app.post("/api/internships/", response_model=schemas.Internship)
async def create_internship(internship: schemas.InternshipCreate, db: Session = Depends(get_db)):
    """Adds an Internship object to the database."""
    return crud.create_internship(db, internship)


def run():
    uvicorn.run("agtern:app", host="0.0.0.0", port=5000, log_level="info")

def start_server(args: Namespace):
    if args.scrape_only:
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
        if not args.save_internships:
            LOG.warning("Internships won't be stored to db; use --save-internships to store to db")
        start_scraper(args)
