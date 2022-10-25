"""Pre-MVP: This file reads from a config file to scrape websites and save them in a json file.
Post-MVP: This file will read configs from a database to scrape websites and save the results back into the database."""
from __future__ import annotations  # Allow type annotations before the type is defined

import csv
import json
import logging
import traceback
from multiprocessing import Process
from threading import Thread

import pandas as pd
import selenium.webdriver.support.expected_conditions as condition
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .actions import ScrapingContext, parse_config
from ...common import DataFile


class WebScraper:
    """Manages a Chrome instance. Provides convenience methods for web scraping."""

    # Suppress warning for assigning None to class variables:
    # noinspection PyTypeChecker
    def __init__(self):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None

    def start(self, headless: bool, options: Options = None, auto_download: bool = True):
        """Starts a new Chrome instance."""
        if options is None:
            options = Options()
        options.headless = headless
        if auto_download:
            driver_manager = ChromeDriverManager()
            driver_exists = driver_manager.driver_cache.find_driver(driver_manager.driver)
            if not driver_exists:
                print("Chrome WebDriver does not exist! Downloading...")
            driver_path = ChromeDriverManager().install()
            if not driver_exists:
                print("Done downloading Chrome WebDriver!")
            print("Starting Chrome WebDriver...")
            self.driver = Chrome(driver_path, options=options)
        else:
            self.driver = Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    def goto(self, link: str):
        self.driver.get(link)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def scrape_xpath(self, xpath: str) -> list:
        return self.wait.until(
            condition.presence_of_all_elements_located(
                (By.XPATH, xpath)
            )
        )

    def scrape_company(self, link: str, config: pd.Series) -> pd.DataFrame:
        data = pd.DataFrame()
        if "company" not in config:
            print("One of the companies in the scraping config does not have a \"company\" property. Skipping!")
            return data
        company_name = config["company"]
        context = ScrapingContext(scraper=self, company=company_name, data=data)
        self.goto(link)
        procedure = parse_config(context, config["scrape"])
        action_num = 0
        for action in procedure:
            action_num += 1
            try:
                print(f"Running Action {action_num}:")
                action()
            except Exception as e:
                print(f"ERROR: Could not execute {company_name}:{action_num}!")
                print(traceback.format_exc())
        return data


ScrapingContext.update_forward_refs(WebScraper=WebScraper)  # Allow ScrapingContext to reference WebScraper


def scrape(headless: bool = True):
    """Pre-MVP: This function scrapes all websites in the config and stores them in a file.
    Post-MVP: This function will take arguments to specify how and where to scrape.
    The results will be stored in a database."""
    scraper = None

    # Close driver when work is finished
    def close_driver(signal_number=None, frame=None):
        # Make sure driver exists
        if scraper is not None:
            print("INFO: Closing driver...")
            scraper.driver.close()
            print("Done!")
        # Close Process
        exit(0)

    # Ensure driver is closed if interrupted:
    # signal.signal( signal.SIGINT, close_driver )

    try:
        scraper = WebScraper()
        scraper.start(headless)

        print("Loading scraping config...")
        # Get JSON data from scraping_config.json (empty DataFrame if not exists)
        scraping_config_json = DataFile(
            "scraping_config.json",
            default_data='[{"company":null,"link":null,"scrape":null}]',
        )
        with open(scraping_config_json.path, "r") as f:
            config = json.load(f)

        # Transform JSON data into DataFrame
        # Create new internship DataFrame to be written to database
        company_scrape_df = pd.DataFrame(config)
        internship_df = pd.DataFrame()

        # Iterate through valid sources to be scraped
        company_scrape_df: pd.DataFrame = company_scrape_df.loc[company_scrape_df["scrape"].notna()]
        for idx, entry in company_scrape_df.iterrows():
            print(f"INFO: Scraping {entry['company']}...")
            data = scraper.scrape_company(entry["link"], entry)
            # Append company data to database DataFrame
            internship_df = pd.concat([internship_df, data])
        print("INFO: Writing to database...")

        # Write DataFrame info to temp data CSV
        # TODO: Write to actual database (AWS?)
        internships_csv = DataFile("internships.csv", is_temp=True)
        internship_df.to_csv(internships_csv.path, index=False, quoting=csv.QUOTE_ALL)

        print("Done!")
    except Exception as e:
        # Log any errors to stdout
        logging.error(traceback.format_exc())
    finally:
        # Ensure driver is closed if an exception occurs
        close_driver()


def start_scraper(headless=True, scrape_only=False, multiprocessing=True):
    print("INFO: Starting scraper...")
    if scrape_only:
        scrape(headless)
    else:
        worker = Process if multiprocessing else Thread
        scraper = worker(target=scrape, args=(headless,))  # DO NOT REMOVE COMMA!!
        # Run in background, so it doesn't block the GUI (if shown)
        scraper.daemon = True
        scraper.start()
