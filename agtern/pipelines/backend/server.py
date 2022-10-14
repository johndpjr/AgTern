import pandas as pd
from math import nan

from ..data import DataFile
from ...models import Internship
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
                iship["company"],
                iship["title"],
                iship["year"],
                iship["period"],
                iship["link"],
                iship["location"],
                iship["description"],
            )
        ) for iship in internships_df.to_dict(orient="records")
    ]
