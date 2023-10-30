from __future__ import annotations

import json
import signal
import traceback
from argparse import Namespace
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from typing import Any

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
from backend.app.models import Job as JobModel
from backend.app.utils import LOG

from .actions import ActionFailure
from .companies import *  # Do not remove!
from .config import get_config, get_configs, load_configs
from .context import ScrapeContext, ctx
from .pipelines import get_pipelines_for_company


class WebScraper:
    """Manages a Chrome instance. Provides convenience methods for web scraping."""

    # Suppress warning for assigning None to class variables:
    # noinspection PyTypeChecker
    def __init__(self, save_jobs: bool, headless: bool, driver_options: Options = None):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None
        self.save_jobs: bool = save_jobs
        self.headless: bool = headless
        self.driver_options: Options = (
            driver_options if driver_options is not None else Options()
        )
        self.driver_options.headless = headless
        self.driver_options.add_argument("--start-maximized")

    def start(self):
        """Starts a new Chrome instance."""
        # TODO: Support multiple drivers?
        driver_path = ChromeDriverManager().install()
        self.driver = Chrome(
            driver_executable_path=driver_path, options=self.driver_options
        )
        self.wait = WebDriverWait(self.driver, 5)

    def generate_context(self, company_name: str):
        """Generates a ScrapeContext bound to this WebScraper and the CompanyScrapeConfigModel for the given company."""
        config = get_config(company_name)
        context = ScrapeContext()
        context.config = config
        context.scraper = self
        context.robots_txt.set_url(config.default_link)
        # noinspection PyBroadException
        try:
            self.goto(context.robots_txt.url, ignore_robots_txt=True)
            LOG.info(f"Parsing {context.robots_txt.url}")
            context.robots_txt.parse(self.scrape_xpath("//body/@innerText")[0])
        except Exception:
            LOG.error(
                f"Request for robots.txt located at {context.robots_txt.url} timed out!"
            )
        LOG.info(f"Crawl-Delay: {context.robots_txt.crawl_delay}")
        if not context.valid():
            raise Exception("The generated ScrapeContext is invalid!")
        return context

    def signal_handler(self, signal_id=None, frame=None):
        LOG.error("Interrupt detected. Aborting!")
        self.quit()

    def quit(self):
        """Closes the driver if it has been started."""
        if self.driver is not None:
            LOG.info("Closing driver...")
            self.driver.quit()
            self.driver = None
            self.wait = None
            LOG.info("Driver closed.")

    def goto(self, link: str, ignore_robots_txt: bool = False):
        """Navigates to a link.
        Waits until the crawl delay specified in robots.txt has passed.
        Waits until the page is loaded."""
        LOG.info(f"Navigating to {link}")
        if not ignore_robots_txt and not ctx.robots_txt.crawl_allowed(link):
            LOG.warning(f"Warning: Crawling is disallowed for {link}")
        if not ignore_robots_txt:
            ctx.robots_txt.delay_if_needed()
        try:
            self.driver.get(link)
        except InvalidArgumentException as e:
            LOG.exception(f"Could not navigate to link: {link}", e)
        if not ignore_robots_txt:
            ctx.robots_txt.last_request_time = datetime.now()
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def js(self, code: str, *args: Any) -> Any:
        """Executes a JavaScript code string. Waits for and returns the result."""
        return self.driver.execute_script(code, *args)

    def scrape_xpath(self, xpath: str) -> list[str]:
        """Retrieves a list of strings from elements on the current page.
        Waits until there is at least one element that matches the XPath.
        Times out after a few seconds."""
        html_property = "innerText"
        last_segment = xpath.split("/")[-1]
        if last_segment.startswith("@") and len(last_segment) > 1:
            xpath = xpath[: -len(last_segment) - 1]
            html_property = last_segment[1:]
        elements = self.get_elements_by_xpath(xpath)
        # TODO: Optimize this list comprehension, use one JS call for retrieving the elements and their attributes?
        return [element.get_attribute(html_property) for element in elements]

    def get_elements_by_xpath(self, xpath: str) -> list[WebElement]:
        """Retrieves a list of elements on the current page.
        Waits until there is at least one element that matches the XPath.
        Times out after a few seconds."""
        return self.wait.until(
            condition.presence_of_all_elements_located((By.XPATH, xpath))
        )

    def scrape_css(
        self, xpath: str, property_value: str
    ) -> list[dict]:  # TODO: Check if this really returns list[dict]
        """Retrieves a list of CSS property values based on an XPath.
        Waits until there is at least one element that matches the XPath.
        Times out after a few seconds."""
        return [
            self.js(
                "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1])",
                element,
                property_value,
            )
            for element in self.scrape_xpath(xpath)
        ]

    def commit_jobs(self) -> bool:
        """Saves the jobs added to the ScrapeContext to the database.
        Returns True if successful.
        Logs validation errors."""
        # TODO: Clean up this function so it's easier to read and possibly more performant
        if not self.save_jobs:
            return True
        LOG.info("Writing to database...")
        success = True
        jobs_to_add = []
        column_names = JobModel.__table__.columns.keys()
        for job in ctx.data:
            try:
                job_exists = False
                for unique_prop in ctx.unique:
                    if (
                        unique_prop in column_names
                        and hasattr(JobModel, unique_prop)
                        and hasattr(job, unique_prop)
                    ):
                        # noinspection PyTypeChecker
                        if (
                            ctx.db.query(getattr(JobModel, unique_prop))
                            .filter(
                                JobModel.company == ctx.config.company_name
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
            LOG.info(f"Saved {len(jobs_to_add)} jobs to the database.")
        except Exception as e:
            LOG.error("Saving to database FAILED!")
            LOG.error(e)
        return success

    def scrape_company(self, company_name: str):
        """Navigates to the given link and starts scraping based on the scrape config.
        Returns the final context."""
        LOG.info(f"Scraping {company_name}...")
        try:
            pipelines = get_pipelines_for_company(company_name)
            if "scrape" not in pipelines:
                LOG.error(
                    f'"scrape" pipeline does not exist for {company_name}. Skipping!'
                )
                return None
            # noinspection PyShadowingNames
            ctx = self.generate_context(company_name)
            ctx.execute(pipelines["scrape"])
            return ctx
        except ActionFailure:
            LOG.error(f"Error scraping {company_name}:")
            LOG.error(traceback.format_exc())
            LOG.error(f"Scraping {company_name} aborted!")
        # self.commit_jobs(context)
        return None

    def __enter__(self):
        """Called when a WebScraper is created in a 'with' statement."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when a WebScraper that has been created with a 'with' statement either goes out of scope or raises an error."""
        if exc_type is not None:
            LOG.error("A fatal error occurred. Aborting!")
            LOG.error(traceback.format_exc())
        # noinspection PyBroadException
        try:
            self.quit()
        except Exception:
            LOG.error("Error closing driver:")
            LOG.error(traceback.format_exc())


def scrape_all(args: Namespace):
    """Scrapes all companies in scraping config if actions are defined there.
    Scraped jobs are stored in a database."""
    with WebScraper(args.save_jobs, args.headless) as scraper:
        # Ensure driver is closed if interrupted:
        signal.signal(signal.SIGINT, scraper.signal_handler)
        configs = get_configs()
        something_succeeded = False
        for config in configs:
            company_name = config.company_name
            try:
                # noinspection PyShadowingNames
                ctx = scraper.scrape_company(company_name)
                if ctx is None:  # No config for company or no "scrape" pipeline
                    continue
                LOG.info(json.dumps(ctx.data, indent=2))
                ctx.execute(scraper.commit_jobs)
                something_succeeded = True
            except ActionFailure as e:
                LOG.error(f"Error scraping {company_name}:")
                LOG.error(traceback.format_exc())
                LOG.error(f"Scraping {company_name} aborted!")
        if something_succeeded:
            LOG.info("SCRAPING COMPLETE!")


def start_scraper(args: Namespace):
    load_configs()
    LOG.info("Starting scraper...")
    if args.scrape_only:
        scrape_all(args)  # Run in main thread
        return

    worker = Process if args.multiprocessing else Thread
    scraper = worker(target=scrape_all, daemon=True, args=(args,))
    scraper.start()  # Run in background thread/process
    # TODO: Dispatch multiple scrapers to execute different pipelines at the same time
