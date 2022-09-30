
from .scraper import start_scraper

"""Pre-MVP: This file provides functions that read the json file that the backend writes to.
Post-MVP: This file will manage a web server that will provide an API to access the database."""

def start_server():
    start_scraper()

def get_all_internships():
    with open( "db.json", "r" ) as f: # IMPORTANT: Open as read-only! Scraper could be writing at the same time!
        pass