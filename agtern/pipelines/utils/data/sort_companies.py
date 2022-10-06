import pandas as pd
import csv
from . import DataFile


def sort_companies():
    """Sorts both companies.csv and scraping_config.json by company name."""

    # Create or read in companies.csv
    companies_csv = DataFile("companies.csv", default_data="name,link")

    # Initialize company info containers
    company_df = pd.read_csv(companies_csv.path)

    # Validate CSV contents if manually given
    assert company_df["name"].is_unique

    # Reformat CSV
    company_df["link"] = company_df["link"].str.strip()
    company_df = company_df.sort_values("name")

    # Write back data sorted by company name
    company_df.to_csv(companies_csv.path, index=False, quoting=csv.QUOTE_ALL)
