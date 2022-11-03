from __future__ import annotations  # Allow type annotations before the type is defined

import signal
from argparse import Namespace
import json
import time
import traceback
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import selenium.webdriver.support.expected_conditions as condition
from pydantic import ValidationError
from undetected_chromedriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .actions import ScrapingContext, parse_config, dump_schemas
from agtern.common import LOG, DataFile, InternshipCreateSchema, AgTernAPI
from agtern.server.database import get_db


class WebScraper:
    """Manages a Chrome instance. Provides convenience methods for web scraping."""

    # Suppress warning for assigning None to class variables:
    # noinspection PyTypeChecker
    def __init__(self):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None
        self.crawl_delay: float = 0
        self.last_request_time: datetime = None

    def start(self, headless: bool, options: Options = None, auto_download: bool = True):
        """Starts a new Chrome instance."""
        if options is None:
            options = Options()
        options.headless = headless
        # if auto_download:
        #     driver_manager = ChromeDriverManager()
        #     driver_exists = driver_manager.driver_cache.find_driver(driver_manager.driver)
        #     if not driver_exists:
        #         LOG.info("Chrome WebDriver does not exist! Downloading...")
        #     driver_path = ChromeDriverManager().install()
        #     if not driver_exists:
        #         LOG.info("Done downloading Chrome WebDriver!")
        #     LOG.info("Starting Chrome WebDriver...")
        #     self.driver = Chrome(driver_path, options=options)
        # else:
        #     self.driver = Chrome(options=options)
        self.driver = Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    def goto(self, link: str):
        if self.last_request_time is not None and self.crawl_delay > 0:
            time_passed = (datetime.now() - self.last_request_time).total_seconds()
            if self.crawl_delay > time_passed:
                delay_amount = self.crawl_delay - time_passed
                LOG.info(f"Delaying for {delay_amount:.2f} seconds...")
                time.sleep(delay_amount)
        self.driver.get(link)
        self.last_request_time = datetime.now()
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def js(self, code: str, *args: Any) -> Any:
        return self.driver.execute_script(code, *args)

    def scrape_xpath(self, xpath: str) -> list:
        return self.wait.until(
            condition.presence_of_all_elements_located(
                (By.XPATH, xpath)
            )
        )

    def scrape_company(self, link: str, config: pd.Series) -> pd.DataFrame:
        data = pd.DataFrame()
        db = get_db()
        if "company" not in config:
            LOG.warning(
                "One of the companies in the scraping config does not have a \"company\" property. Skipping!"
            )
            return data
        company_name = config["company"]
        self.last_request_time = None
        self.crawl_delay = 0
        parsed_link = urlparse(link)
        self.goto(f"{parsed_link.scheme if len(parsed_link.scheme) > 0 else 'http'}://{parsed_link.netloc}/robots.txt")
        context = ScrapingContext(
            scraper=self,
            company=company_name,
            db=db,
            data=data,
            robots_txt=self.driver.page_source
        )
        crawl_delay = None
        for line in context.robots_txt.splitlines():
            line = line.strip()
            while line.find("#") != -1:
                line = line[:line.find("#")]
            if line.lower().startswith("crawl-delay:"):
                new_crawl_delay = float(line[12:].strip())
                if crawl_delay is None or new_crawl_delay < crawl_delay:
                    crawl_delay = new_crawl_delay
        if crawl_delay is None:
            crawl_delay = 0
        LOG.info(f"Crawl-delay: {crawl_delay}")
        self.goto(link)
        time.sleep(3)  # Make sure page is fully loaded
        self.crawl_delay = crawl_delay
        procedure = parse_config(context, config["scrape"])
        action_num = 0
        for action in procedure:
            action_num += 1
            try:
                LOG.info(f"Running Action {company_name}:{action_num} ({action.action.name})...")
                action()
            except Exception as e:
                LOG.error(f"ERROR: Could not execute {company_name}:{action_num}!")
                LOG.error(traceback.format_exc())
        return data


ScrapingContext.update_forward_refs(WebScraper=WebScraper)  # Allow ScrapingContext to reference WebScraper


# dump_schemas()  # Export schemas as json files (currently broken)


def scrape(args: Namespace):
    """Scrapes all companies in scraping config if actions are defined there.
     Scraped internships are stored in a database."""
    scraper = None
    api = AgTernAPI()

    # Close driver when work is finished
    def close_driver(signal_number=None, frame=None):
        # Make sure driver exists
        if scraper is not None and scraper.driver is not None:
            LOG.info("Closing driver...")
            scraper.driver.close()
            LOG.info("Done!")
        # Close Process
        exit(0)

    # Ensure driver is closed if interrupted:
    signal.signal(signal.SIGINT, close_driver)

    try:
        scraper = WebScraper()
        scraper.start(args.headless)

        LOG.info("Loading scraping config...")
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
            LOG.info(f"Scraping {entry['company']}...")
            data = scraper.scrape_company(entry["link"], entry)
            # Append company data to database DataFrame
            internship_df = pd.concat([internship_df, data])
        LOG.info("Writing to database...")

        for idx, internship in internship_df.iterrows():
            if args.save_internships:
                try:
                    internship = InternshipCreateSchema(
                        **{k: v for k, v in internship.items() if v is not None}
                    )
                    api.create_internship(internship)
                except ValidationError as errors:
                    LOG.error("Unable to create internship!")
                    LOG.error(errors)

        LOG.info("Done!")
    except Exception as e:
        # Log any errors to stdout
        LOG.error(traceback.format_exc())
    finally:
        # Ensure driver is closed if an exception occurs
        close_driver()


def start_scraper(args: Namespace):
    LOG.info("Starting scraper...")
    if args.scrape_only:
        scrape(args)
        return

    worker = Process if args.multiprocessing else Thread
    scraper = worker(target=scrape,
                     daemon=True,
                     args=(args,))
    scraper.start()
