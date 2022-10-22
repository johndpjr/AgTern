import json

import pandas as pd

from ...logger import LOG
from ..data import DataFile


def import_companies():
    """Imports all company names and links from companies.csv into scraping_config.json."""

    # Gets paths of companies CSV and scraping config JSON
    companies_csv = DataFile("companies.csv", default_data="name,link")
    scraping_config_json = DataFile(
        "scraping_config.json", default_data='[{"name":null,"link":null,"scrape":null}]'
    )

    # Converts readable JSON into object read in by DataFrame
    with open(scraping_config_json.path, "r") as f:
        readable_json = json.load(f)

    # Reads in and converts CSV/JSON into Pandas DataFrames
    company_df = pd.read_csv(companies_csv.path)
    original_df = pd.DataFrame(readable_json)

    # Creates new JSON object with companies from CSV
    LOG.info("Generating company info...")
    new_df = pd.DataFrame()
    new_df["name"] = company_df["name"]
    new_df["link"] = company_df["link"]

    # Merge DataFrames to retain scrape values
    new_df = new_df.merge(original_df.drop("link", axis=1), how="left", on=["name"])

    # Rewrites JSON file using new DataFrame (in readable format)
    log.INFO("Writing info to scraping_config.json...")
    with open(scraping_config_json.path, "w") as f:
        json.dump(json.loads(new_df.to_json(orient="records")), f, indent=2)
