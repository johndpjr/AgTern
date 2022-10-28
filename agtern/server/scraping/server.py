from dataclasses import fields
import pandas as pd
from math import nan

from ...common import DataFile, Internship
from .scraper import start_scraper

"""Pre-MVP: This file provides functions that read the json file that the backend writes to.
Post-MVP: This file will manage a web server that will provide an API to access the database."""


def start_server(headless_scraper=True, scrape_only=False):
    start_scraper(headless_scraper, scrape_only)


# Transform CSV into list of Internship objects
def get_all_internships() -> list:
    try:
        internships_csv = DataFile("internships.csv", is_temp=True, create_on_init=False)
        internships_df = pd.read_csv(internships_csv.path).replace({nan: None})
        internships = []
        for iship in internships_df.to_dict(orient="records"):
            data = {}
            for key, value in iship.items():
                if value is not None:
                    data[key] = value
            internships.append(Internship.parse_obj(data))
    except pd.errors.EmptyDataError:
        return []
    return internships
