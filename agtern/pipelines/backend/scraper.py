"""Pre-MVP: This file reads from a config file to scrape websites and save them in a json file.
Post-MVP: This file will read configs from a database to scrape websites and save the results back into the database."""

import csv
import json
import logging
import traceback
from dataclasses import fields
from multiprocessing import Process

import pandas as pd
import selenium.webdriver.support.expected_conditions as condition
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ...logger import LOG
from ...models import Internship
from ..data import DataFile


def scrape(headless: bool = True):
    """Pre-MVP: This function scrapes all websites in the config and stores them in a file.
    Post-MVP: This function will take arguments to specify how and where to scrape. The results will be stored in a database."""
    driver = None

    # Close driver when work is finished
    def close_driver(signal_number=None, frame=None):
        # Make sure driver exists
        if driver is not None:
            driver.close()
        LOG.info("Closing driver...")
        # Close Process
        exit(0)

    # Ensure driver is closed if interrupted:
    # signal.signal( signal.SIGINT, close_driver )

    try:
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        LOG.info("INFO: Waiting...")
        wait = WebDriverWait(driver, 5)

        # Get JSON data from scraping_config.json (empty DataFrame if not exists)
        scraping_config_json = DataFile(
            "scraping_config.json",
            default_data='[{"name":null,"link":null,"scrape":null}]',
        )
        with open(scraping_config_json.path, "r") as f:
            config = json.load(f)

        # Transform JSON data into DataFrame
        # Create new internship DataFrame to be written to database
        company_scrape_df = pd.DataFrame(config)
        internship_df = pd.DataFrame()

        # Iterate through valid sources to be scraped
        company_scrape_df = company_scrape_df.loc[company_scrape_df["scrape"].notna()]
        for idx, entry in company_scrape_df.iterrows():
            LOG.info(f"INFO: Scraping {entry['name']}...")

            # Go to the page that should be scraped
            driver.get(entry["link"])

            # Create temp DataFrame with scraped info
            data = pd.DataFrame()

            # Find scrape info for fields in Internship model
            for field in fields(Internship):
                # If scrape info not given for field, fill column with NaN
                if field.name not in entry["scrape"]:
                    data[field.name] = None
                    continue
                # Otherwise wait until element is found via XPATH
                elements = wait.until(
                    condition.presence_of_all_elements_located(
                        (By.XPATH, entry["scrape"][field.name])
                    )
                )
                # Create column with found elements and add to temp DataFrame
                contents = []
                for element in elements:
                    # Account for differing element types
                    if element.tag_name == "a":
                        contents.append(element.get_attribute("href"))
                    else:
                        contents.append(element.text)
                data[field.name] = pd.Series(contents)
            # Fill 'company' column with company being searched
            data["company"] = entry["name"]

            # Append company data to database DataFrame
            internship_df = pd.concat([internship_df, data])
        LOG.info("INFO: Writing to database...")

        # Write DataFrame info to temp data CSV
        # TODO: Write to actual database (AWS?)
        internships_csv = DataFile("internships.csv", is_temp=True)
        internship_df.to_csv(internships_csv.path, index=False, quoting=csv.QUOTE_ALL)

        LOG.info("Done!")
    except Exception as e:
        # Log any errors to stdout
        logging.error(traceback.format_exc())
    finally:
        # Ensure driver is closed if an exception occurs
        close_driver()


def start_scraper(headless=True):
    scraper = Process(target=scrape, args=(headless,))  # DO NOT REMOVE COMMA!!
    # Run in background, so it doesn't block the GUI (if shown)
    scraper.daemon = True
    LOG.info("Starting driver...")
    scraper.start()
