from dataclasses import fields
import pandas as pd
from math import nan

from ...common import Internship, DataFile
from .extractor import update_internship
from .scraper import start_scraper

"""Pre-MVP: This file provides functions that read the json file that the backend writes to.
Post-MVP: This file will manage a web server that will provide an API to access the database."""


def start_server(headless_scraper=True):
    start_scraper(headless_scraper)

# Transform CSV into list of Internship objects
def get_all_internships() -> list:
    internships_csv = DataFile("internships.csv", is_temp=True, create_on_init=False)
    internships_df = pd.read_csv(internships_csv.path).replace({nan: None})
    return [
        update_internship(
            Internship(
                *[iship[field.name] or '' for field in fields(Internship)]
            )
        ) for iship in internships_df.to_dict(orient="records")
    ]
