from __future__ import annotations

import json
import signal
import traceback
from argparse import Namespace
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from time import time
from typing import Any
from urllib.parse import urlparse

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

    @property
    def current_url(self):
        return self.driver.current_url

    def generate_context(self, company_name: str):
        """Generates a ScrapeContext bound to this WebScraper and the CompanyScrapeConfigModel for the given company.
        Returns None if scraping cannot be performed."""
        config = get_config(company_name)
        if config.default_link is None:
            return None  # The company cannot be scraped
        context = ScrapeContext()
        context.config = config
        context.scraper = self
        context.robots_txt.set_url(config.default_link)
        # noinspection PyBroadException
        try:
            self.goto(context.robots_txt.url, ignore_robots_txt=True)
        except Exception:
            LOG.error(
                f"Request for robots.txt located at {context.robots_txt.url} timed out!"
            )
        # noinspection PyBroadException
        try:
            LOG.info(f"Parsing {context.robots_txt.url}")
            context.robots_txt.parse(self.scrape_xpath("//body")[0])
        except Exception:
            LOG.error(f"robots.txt parsing failed!")
            LOG.error(traceback.format_exc())
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

    def make_link_absolute(self, link: str):
        """Makes a link absolute relative to the current URL.
        If link is already an absolute URL, it is returned unchanged."""
        relative_url = urlparse(link)
        current_url = urlparse(self.driver.current_url)
        scheme = relative_url.scheme if relative_url.scheme else current_url.scheme
        netloc = relative_url.netloc if relative_url.netloc else current_url.netloc
        path = relative_url.path if relative_url.path else current_url.path
        params = relative_url.params if relative_url.params else current_url.params
        query = relative_url.query if relative_url.query else current_url.query
        fragment = (
            relative_url.fragment if relative_url.fragment else current_url.fragment
        )
        absolute_link = ""
        if scheme:
            absolute_link += scheme + "://"
        absolute_link += netloc
        absolute_link += path
        if not relative_url.path:
            # The following are page-specific, so don't use them if the path changed
            if params:
                absolute_link += ";" + params
            if query:
                absolute_link += "?" + query
            if fragment:
                absolute_link += "#" + query
        return absolute_link

    def goto(self, link: str, ignore_robots_txt: bool = False):
        """Navigates to a link.
        Waits until the crawl delay specified in robots.txt has passed.
        Waits until the page is loaded."""
        link = self.make_link_absolute(link)
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

    def wait_until_true(self, code: str, *args: Any):
        """Waits until a JavaScript code string returns true.
        Times out after a few seconds."""
        return self.wait.until(lambda d: d.execute_script(code, *args))

    def scrape_xpath(self, xpath: str) -> list[str]:
        """Retrieves a list of strings from elements on the current page.
        Waits until there is at least one element that matches the XPath.
        Times out after a few seconds."""
        # Loosely based on https://stackoverflow.com/a/68216786/11827673
        xpath = xpath.replace('"', '\\"')
        script = (
            f"return (x=>{{"
            f"const s=document.evaluate(x,document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);"
            f"return [...Array(s.snapshotLength)].map((_,i)=>{{"
            f"n=s.snapshotItem(i);"
            f"return n.nodeType===Node.ATTRIBUTE_NODE?n.value:n.textContent"
            f'}})}})("{xpath}")'
        )
        # (x=>{
        #     const s=document.evaluate(x,document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);
        #     return [...Array(s.snapshotLength)].map((_,i)=>{
        #         n=s.snapshotItem(i);
        #         return n.nodeType===Node.ATTRIBUTE_NODE?n.value:n.textContent
        #     })
        # })("")
        self.wait_until_true(f"{script}.length!=0")
        return self.js(script)

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
            for element in self.get_elements_by_xpath(xpath)
        ]

    def commit_jobs(self) -> bool:
        """Saves the jobs added to the ScrapeContext to the database.
        Returns True if successful.
        Logs validation errors."""
        # TODO: Clean up this function so it's easier to read and possibly more performant
        if not self.save_jobs:
            return True
        success = True
        jobs_to_add = []
        num_skipped = 0
        column_names = JobModel.__table__.columns.keys()
        for job in ctx.data:
            try:
                job_exists = False
                for unique_prop in ctx.unique:
                    if (
                        unique_prop in column_names
                        and hasattr(JobModel, unique_prop)
                        and unique_prop in job
                    ):
                        # noinspection PyTypeChecker
                        if (
                            ctx.db.query(getattr(JobModel, unique_prop))
                            .filter(
                                JobModel.company == ctx.config.company_name
                                and getattr(JobModel, unique_prop) == job[unique_prop]
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
                else:
                    num_skipped += 1
            except ValidationError as errors:
                LOG.error("Unable to create job!")
                LOG.error(f"Job: {json.dumps(job, indent=2)}")
                LOG.error(errors)
                success = False
        LOG.info(f"{num_skipped} jobs were skipped.")
        if len(jobs_to_add) > 0:
            try:
                LOG.info("Writing to database...")
                crud.create_jobs(ctx.db, *jobs_to_add)
                LOG.info(f"Saved {len(jobs_to_add)} jobs to the database!")
            except Exception as e:
                LOG.error("Saving to database FAILED!")
                LOG.error(e)
        else:
            LOG.info("Nothing to save!")
        return success

    def scrape_company(self, company_name: str):
        """Navigates to the given link and starts scraping based on the scrape config.
        Returns the final context or None if scraping could not be performed."""
        start_time = time()
        # noinspection PyShadowingNames
        ctx = self.generate_context(company_name)
        if ctx is None:
            return None
        if ctx.settings.scrape_companies is not None:
            found = False
            for name in ctx.settings.scrape_companies:
                if name.lower() == company_name.lower():
                    found = True
                    break
            if not found:
                return None
        self.wait = WebDriverWait(self.driver, ctx.settings.timeout)
        pipelines = get_pipelines_for_company(company_name)
        try:
            if "scrape" not in pipelines:
                return None
            LOG.info(f"Scraping {company_name}...")
            ctx.execute(pipelines["scrape"])
        except ActionFailure as cause:
            LOG.error(f"Error scraping {company_name}:")
            if ctx.settings.print_tracebacks or len(cause.args) == 0:
                # If there's no message, print the traceback
                LOG.error(traceback.format_exc())
            else:
                # If the ActionFailure has a message, just print it
                for arg in cause.args:
                    LOG.error(arg)
            LOG.error(f"Scraping {company_name} aborted!")
            return None
        if "process" in pipelines:
            # TODO: Execute processing in parallel
            original_data = ctx.data
            final_data = []
            for i, row in enumerate(original_data):
                LOG.info(f"Processing job {i+1}/{len(original_data)}...")
                try:
                    ctx.data = row
                    ctx.execute(pipelines["process"])
                    final_data.append(ctx.data)
                except ActionFailure:
                    LOG.error("Error processing job:")
                    LOG.error(json.dumps(row, indent=2))
                    LOG.error(traceback.format_exc())
                    LOG.error("Saving job aborted!")
            ctx.data = final_data
        if ctx.settings.print_result:
            LOG.info(json.dumps(ctx.data, indent=2))
        end_time = time()
        delta_time = int(end_time - start_time)
        minutes = delta_time // 60
        seconds = delta_time % 60
        LOG.info(f"Scraping and processing for {company_name} took {minutes}:{seconds}")
        return ctx

    def __enter__(self):
        """Called when a WebScraper is created in a 'with' statement."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when a WebScraper that has been created with a 'with' statement either
        goes out of scope or raises an error."""
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
    start_time = time()
    with WebScraper(args.save_jobs, args.headless) as scraper:
        # Ensure driver is closed if interrupted:
        signal.signal(signal.SIGINT, scraper.signal_handler)
        configs = get_configs()
        something_succeeded = False
        skipped = []
        for config in configs:
            company_name = config.company_name
            try:
                # noinspection PyShadowingNames
                ctx = scraper.scrape_company(company_name)
                if ctx is None:  # No config for company or no "scrape" pipeline
                    skipped.append(company_name)
                    continue
                ctx.execute(scraper.commit_jobs)
                something_succeeded = True
            except ActionFailure as e:
                LOG.error(f"Error scraping {company_name}:")
                LOG.error(traceback.format_exc())
                LOG.error(f"Scraping {company_name} aborted!")
            if len(skipped) > 0:
                skipped_company_names = ", ".join(skipped)
                LOG.error(
                    f"The following companies were skipped: {skipped_company_names}"
                )
        if something_succeeded:
            end_time = time()
            delta_time = int(end_time - start_time)
            minutes = delta_time // 60
            seconds = delta_time % 60
            LOG.info("SCRAPING COMPLETE!")
            LOG.info(f"Scraping ALL companies took {minutes}:{seconds}")


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
