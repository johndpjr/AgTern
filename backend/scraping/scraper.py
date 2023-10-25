from __future__ import annotations

import json
import signal
import time
import traceback
from argparse import Namespace
from datetime import datetime
from multiprocessing import Process
from os import fsdecode, listdir, pardir
from os.path import abspath, join
from threading import Thread
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests
import selenium.webdriver.support.expected_conditions as condition
from pydantic import ValidationError
from selenium.common import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from backend.app.crud import crud
from backend.app.database import DatabaseSession
from backend.app.models import Job as JobModel
from backend.app.utils import LOG, DataFile

from .actions import ScrapingContext, parse_config


class WebScraper:
    """Manages a Chrome instance. Provides convenience methods for web scraping."""

    # Suppress warning for assigning None to class variables:
    # noinspection PyTypeChecker
    def __init__(self, save_jobs: bool):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None
        self.crawl_delay: float = 0
        self.last_request_time: datetime = None
        self.save_jobs = save_jobs

    def start(self, headless: bool, options: Options = None):
        """Starts a new Chrome instance."""
        if options is None:
            options = Options()
        options.headless = headless
        options.add_argument("--start-maximized")
        driver_path = ChromeDriverManager().install()
        self.driver = Chrome(driver_executable_path=driver_path, options=options)

        self.wait = WebDriverWait(self.driver, 5)

    def goto(self, link: str):
        if self.last_request_time is not None and self.crawl_delay > 0:
            time_passed = (datetime.now() - self.last_request_time).total_seconds()
            if self.crawl_delay > time_passed:
                delay_amount = self.crawl_delay - time_passed
                LOG.info(f"Delaying for {delay_amount:.2f} seconds...")
                time.sleep(delay_amount)
        try:
            self.driver.get(link)
        except InvalidArgumentException as e:
            LOG.exception(f"Could not navigate to link: {link}", e)
        self.last_request_time = datetime.now()
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def js(self, code: str, *args: Any) -> Any:
        return self.driver.execute_script(code, *args)

    def scrape_xpath(self, xpath: str) -> list[WebElement]:
        return self.wait.until(
            condition.presence_of_all_elements_located((By.XPATH, xpath))
        )

    def scrape_css(self, xpath: str, property_value: str) -> list[dict]:
        return [
            self.js(
                "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1])",
                element,
                property_value,
            )
            for element in self.scrape_xpath(xpath)
        ]

    def commit_jobs(self, ctx: ScrapingContext) -> bool:
        if not self.save_jobs:
            return True
        LOG.info("Writing to database...")
        success = True
        jobs_to_add = []
        column_names = JobModel.__table__.columns.keys()
        for idx, job in ctx.data.iterrows():
            try:
                job_exists = False
                for unique_prop in ctx.unique_properties:
                    if (
                        unique_prop in column_names
                        and hasattr(JobModel, unique_prop)
                        and hasattr(job, unique_prop)
                    ):
                        # noinspection PyTypeChecker
                        if (
                            ctx.db.query(getattr(JobModel, unique_prop))
                            .filter(
                                JobModel.company == ctx.company
                                and getattr(JobModel, unique_prop)
                                == getattr(job, unique_prop)
                            )
                            .count()
                            > 0
                        ):
                            job_exists = True  # Skip this job because it already exists
                if not job_exists:
                    jobs_to_add.append(
                        JobModel(
                            **{
                                k: v
                                for k, v in job.items()
                                if k in column_names and v is not None
                            }
                        )
                    )
            except ValidationError as errors:
                LOG.error("Unable to create job!")
                LOG.error(f"Job: {job.to_dict()}")
                LOG.error(errors)
                success = False
        try:
            crud.create_jobs(ctx.db, *jobs_to_add)
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
        robots_txt = (
            None if robots_txt_response.status_code != 200 else robots_txt_response.text
        )
        context = ScrapingContext(
            scraper=self,
            company=company_name,
            db=db,
            data=pd.DataFrame(),
            robots_txt=robots_txt,
        )
        crawl_delay = None
        if robots_txt is not None:
            for line in context.robots_txt.splitlines():
                line = line.strip()
                while line.find("#") != -1:
                    line = line[: line.find("#")]
                if line.lower().startswith("crawl-delay:"):
                    new_crawl_delay = float(line[12:].strip())
                    if crawl_delay is None or new_crawl_delay < crawl_delay:
                        crawl_delay = new_crawl_delay
        else:
            LOG.info("No robots.txt was found!")
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
        self.commit_jobs(context)


ScrapingContext.update_forward_refs(
    WebScraper=WebScraper
)  # Allow ScrapingContext to reference WebScraper


def scrape(args: Namespace):
    """Scrapes all companies in scraping config if actions are defined there.
    Scraped jobs are stored in a database."""
    scraper = None

    # Close driver when work is finished
    def close_driver(signal_number=None, frame=None):
        # Make sure driver exists
        if scraper is not None and scraper.driver is not None:
            LOG.info("Closing driver...")
            scraper.driver.quit()
        # Close process
        exit(0)

    # Ensure driver is closed if interrupted:
    signal.signal(signal.SIGINT, close_driver)

    try:
        scraper = WebScraper(args.save_jobs)
        scraper.start(args.headless)

        LOG.info("Loading scraping config...")
        company_scrape = []
        directory = abspath(join(__file__, pardir)) + "/../../data/companies"
        for file in listdir(directory):
            filename = fsdecode(file)
            # Include/exclude companies
            company = filename.removesuffix(".json")
            if (args.include_companies and company not in args.include_companies) or (
                args.exclude_companies and company in args.exclude_companies
            ):
                continue
            file_dir_path = join(directory, filename)
            file_scrape_config_json = DataFile(
                file_dir_path,
                default_data='{"company":null,"link":null,"scrape":null}',
            )

            print(file_scrape_config_json.path)
            with open(file_scrape_config_json.path, "r") as f:
                company_scrape.append(json.load(f))

        # Transform JSON data into DataFrame (model that holds scrape data)
        company_scrape_df = pd.DataFrame.from_records(company_scrape)
        # Iterate through valid sources to be scraped
        company_scrape_df: pd.DataFrame = company_scrape_df.loc[
            company_scrape_df["scrape"].notna()
        ]
        LOG.info("Scraping specified companies...")
        company_scrape_df = company_scrape_df.sort_values(
            by=["company"], ascending=True
        )
        for idx, entry in company_scrape_df.iterrows():
            # TODO: Add a command-line argument to select which company/companies to scrape
            # if entry["company"] != "Allstate":
            #     continue
            LOG.info(f"Scraping {entry['company']}...")
            try:
                scraper.scrape_company(entry["link"], entry)
            except Exception as ex:
                LOG.info(ex)

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
