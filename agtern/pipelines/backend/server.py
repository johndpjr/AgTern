import json

import pandas as pd

from ..utils import DataFile
from .scraper import start_scraper

"""Pre-MVP: This file provides functions that read the json file that the backend writes to.
Post-MVP: This file will manage a web server that will provide an API to access the database."""


def start_server(headless_scraper=True):
    start_scraper(headless_scraper)


def get_all_internships() -> list:
    internships_csv = DataFile("internships.csv")
    internships_df = pd.read_csv(internships_csv.path)
    return internships_df.to_dict(orient="records")
