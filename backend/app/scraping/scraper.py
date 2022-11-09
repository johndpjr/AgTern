from __future__ import annotations  # Allow type annotations before the type is defined

import json
import signal
import time
import traceback
from argparse import Namespace
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests
import selenium.webdriver.support.expected_conditions as condition
from pydantic import ValidationError
from selenium.common import InvalidArgumentException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome

from backend.app.crud import crud
from backend.app.database import DatabaseSession
from backend.app.models import Internship as InternshipModel
from backend.app.utils import LOG, DataFile

from .actions import ScrapingContext, parse_config

# from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    """Manages a Chrome instance. Provides convenience methods for web scraping."""

    # Suppress warning for assigning None to class variables:
    # noinspection PyTypeChecker
    def __init__(self, save_internships: bool):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None
        self.crawl_delay: float = 0
        self.last_request_time: datetime = None
        self.save_internships = save_internships

    def start(
        self, headless: bool, options: Options = None, auto_download: bool = True
    ):
        """Starts a new Chrome instance."""
        if options is None:
            options = Options()
        options.headless = headless
        options.add_argument("--start-maximized")
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
        self.last_request_time = datetime.now()
        try:
            self.driver.get(link)
        except InvalidArgumentException as e:
            LOG.exception(f"Could not navigate to link: {link}", e)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def js(self, code: str, *args: Any) -> Any:
        return self.driver.execute_script(code, *args)

    def scrape_xpath(self, xpath: str) -> list[WebElement]:
        return self.wait.until(
            condition.presence_of_all_elements_located(
                (By.XPATH, xpath)
            )
        )

    def scrape_css(self, xpath: str, property_value: str) -> list[dict]:
        return [
            self.js(
                "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1])",
                element,
                property_value
            )
            for element in self.scrape_xpath(xpath)
        ]

    def commit_internships(self, ctx: ScrapingContext) -> bool:
        if not self.save_internships:
            return True
        LOG.info("Writing to database...")
        success = True
        internships_to_add = []
        internships_to_update = (
            []
        )  # TODO: Update internships instead of ignoring duplicates
        column_names = InternshipModel.__table__.columns.keys()
        for idx, internship in ctx.data.iterrows():
            try:
                internship_exists = False
                for unique_prop in ctx.unique_properties:
                    if (
                        unique_prop in column_names
                        and hasattr(InternshipModel, unique_prop)
                        and hasattr(internship, unique_prop)
                    ):
                        # noinspection PyTypeChecker
                        if (
                            ctx.db.query(getattr(InternshipModel, unique_prop))
                            .filter(
                                InternshipModel.company == ctx.company
                                and getattr(InternshipModel, unique_prop)
                                == getattr(internship, unique_prop)
                            )
                            .count()
                            > 0
                        ):
                            internship_exists = (
                                True  # Skip this internship because it already exists
                            )
                if not internship_exists:
                    internships_to_add.append(
                        InternshipModel(
                            **{
                                k: v
                                for k, v in internship.items()
                                if k in column_names and v is not None
                            }
                        )
                    )
            except ValidationError as errors:
                LOG.error("Unable to create internship!")
                LOG.error(f"Internship: {internship.to_dict()}")
                LOG.error(errors)
                success = False
        try:
            crud.create_internships(ctx.db, *internships_to_add)
            LOG.info("Saving to database succeeded!")
        except Exception as e:
            LOG.error("Saving to database FAILED!")
            LOG.error(e)
        return success

    def scrape_company(self, link: str, config: pd.Series):
        db = DatabaseSession()
        if "company" not in config:
            LOG.warning(
                'One of the companies in the scraping config does not have a "company" property. Skipping!'
            )
            return
        company_name = config["company"]
        self.last_request_time = None
        self.crawl_delay = 0
        parsed_link = urlparse(link)
        robots_txt_response = requests.get(
            f"{parsed_link.scheme if len(parsed_link.scheme) > 0 else 'http'}://{parsed_link.netloc}/robots.txt"
        )
        robots_txt = None if robots_txt_response.status_code != 200 else robots_txt_response.text
        context = ScrapingContext(
            scraper=self,
            company=company_name,
            db=db,
            data=pd.DataFrame(),
            robots_txt=robots_txt
        )
        crawl_delay = None
        if robots_txt is not None:
            for line in context.robots_txt.splitlines():
                line = line.strip()
                while line.find("#") != -1:
                    line = line[:line.find("#")]
                if line.lower().startswith("crawl-delay:"):
                    new_crawl_delay = float(line[12:].strip())
                    if crawl_delay is None or new_crawl_delay < crawl_delay:
                        crawl_delay = new_crawl_delay
        if crawl_delay is None:
            crawl_delay = 1
        LOG.info(f"Crawl-delay: {crawl_delay}")
        self.goto(link)
        time.sleep(3)  # Make sure page is fully loaded
        self.crawl_delay = crawl_delay
        procedure = parse_config(context, config["scrape"])
        action_num = 0
        for action in procedure:
            action_num += 1
            try:
                # noinspection PyUnresolvedReferences
                LOG.info(
                    f"Running Action {company_name}:{action_num} ({action.action.name})..."
                )
                action()
            except Exception as e:
                LOG.error(f"ERROR: Could not execute {company_name}:{action_num}!")
                LOG.error(traceback.format_exc())
        self.commit_internships(context)


ScrapingContext.update_forward_refs(
    WebScraper=WebScraper
)  # Allow ScrapingContext to reference WebScraper


# dump_schemas()  # Export schemas as json files (currently broken)


def scrape(args: Namespace):
    """Scrapes all companies in scraping config if actions are defined there.
    Scraped internships are stored in a database."""
    scraper = None

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
        scraper = WebScraper(args.save_internships)
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

        # Iterate through valid sources to be scraped
        company_scrape_df: pd.DataFrame = company_scrape_df.loc[
            company_scrape_df["scrape"].notna()
        ]
        for idx, entry in company_scrape_df.iterrows():
            # Uncomment below to just scrape Amazon
            # TODO: Add a command-line argument to select which company/companies to scrape
            if entry["company"] != "Dell":
                continue
            LOG.info(f"Scraping {entry['company']}...")
            scraper.scrape_company(entry["link"], entry)
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
    scraper = worker(target=scrape, daemon=True, args=(args,))
    scraper.start()
