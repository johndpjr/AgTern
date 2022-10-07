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

from ..utils import DataFile, Internship


def scrape(headless: bool = True):
    """Pre-MVP: This function scrapes all websites in the config and stores them in a file.
    Post-MVP: This function will take arguments to specify how and where to scrape. The results will be stored in a database."""
    driver = None

    def close_driver(signal_number=None, frame=None):
        if driver is not None:
            driver.close()
        print("INFO: Closing driver...")
        exit(0)

    # Ensure driver is closed if interrupted:
    # signal.signal( signal.SIGINT, close_driver )

    try:
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print("INFO: Waiting...")
        wait = WebDriverWait(driver, 5)

        scraping_config_json = DataFile(
            "scraping_config.json",
            default_data='[{"name":null,"link":null,"scrape":null}]',
        )
        with open(scraping_config_json.path, "r") as f:
            config = json.load(f)

        company_scrape_df = pd.DataFrame(config)
        internship_df = pd.DataFrame()

        company_scrape_df = company_scrape_df.loc[company_scrape_df["scrape"].notna()]
        print(company_scrape_df)
        for idx, entry in company_scrape_df.iterrows():
            print(f"INFO: Scraping {entry['name']}...")

            # Go to the page that should be scraped
            driver.get(entry["link"])

            data = pd.DataFrame()
            for field in fields(Internship):
                if field.name not in entry["scrape"]:
                    data[field.name] = None
                    continue
                elements = wait.until(
                    condition.presence_of_all_elements_located(
                        (By.XPATH, entry["scrape"][field.name])
                    )
                )
                contents = []
                for element in elements:
                    if element.tag_name == "a":
                        contents.append(element.get_attribute("href"))
                    else:
                        contents.append(element.text)
                data[field.name] = pd.Series(contents)
            data["company"] = entry["name"]
            internship_df = internship_df.append(data)
        print("INFO: Writing to database...")
        internship_df.to_csv("internships.csv", index=False, quoting=csv.QUOTE_ALL)

        print("Done!")
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
    print("INFO: Starting driver...")
    scraper.start()
