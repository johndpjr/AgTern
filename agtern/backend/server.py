
from .scraper import start_scraper

import json

from ..data import DataFile

"""Pre-MVP: This file provides functions that read the json file that the backend writes to.
Post-MVP: This file will manage a web server that will provide an API to access the database."""


def start_server(headless_scraper=True):
    start_scraper(headless_scraper)


def get_all_internships() -> list:
    data = []
    db_json = DataFile("db.json", default_data="[]")
    # IMPORTANT: Open as read-only! Scraper could be writing at the same time!
    with open(db_json.path, "r") as f:
        data = json.load(f)
    return data
