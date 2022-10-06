import pandas as pd
import json
from agtern.data import DataFile


def import_companies():
    """Imports all company names and links from companies.csv into scraping_config.json."""

    # Gets paths of companies CSV and scraping config JSON
    companies_csv = DataFile("companies.csv", default_data="name,link")
    scraping_config_json = DataFile("scraping_config.json", default_data="[]")

    # Converts readable JSON into object read in by DataFrame
    with open(scraping_config_json.path, "r") as f:
        readable_json = json.load(f)

    # Reads in and converts CSV/JSON into Pandas DataFrames
    company_df = pd.read_csv(companies_csv.path)
    original_df = pd.DataFrame(readable_json)

    # Creates new JSON object with companies from CSV
    print("INFO: Generating company info...")
    new_df = pd.DataFrame()
    new_df["name"] = company_df["name"]
    new_df["link"] = company_df["link"]
    new_df["scrape"] = "{}"

    # Tries to set existing scrape configs to new JSON object.
    # Keeps default scrape '{}' for all internships if scraping_config.json
    # 'name' and 'scrape' do not exist (will occur if the file hasn't been created)
    try:
        new_df.loc[new_df["name"].isin(original_df["name"]), "scrape"] = \
            original_df.loc[original_df["name"] == new_df["name"], "scrape"]
    except:
        print("WARNING: Setting scrape configurations to '{}'")

    # Rewrites JSON file using new DataFrame (in readable format)
    print("INFO: Writing info to scraping_config.json...")
    with open(scraping_config_json.path, "w") as f:
        json.dump(readable_json, f, indent=2)
