import time
import traceback
from datetime import datetime, timedelta
from urllib.parse import urlparse

from protego import Protego

from backend.app.utils import LOG


class RobotsTxt:
    # Allow initializing class variables to None:
    # noinspection PyTypeChecker
    def __init__(self, default_crawl_delay: float = 1, user_agent: str = "googlebot"):
        self.default_crawl_delay = default_crawl_delay
        self.user_agent = user_agent
        self.parser: Protego = Protego()
        self.url: str = None
        self.exists: bool = None
        self.last_request_time: datetime = None

    @property
    def crawl_delay(self) -> float:
        """Returns the crawl_delay"""
        crawl_delay = self.parser.crawl_delay(self.user_agent)
        if crawl_delay is not None:
            try:
                crawl_delay = int(crawl_delay)
            except ValueError:
                crawl_delay = None
        req_rate = self.parser.request_rate(self.user_agent)
        req_rate_delay = None
        if req_rate is not None:
            req_rate_delay = req_rate.seconds / req_rate.requests
        if crawl_delay is None and req_rate_delay is None:
            return self.default_crawl_delay
        if req_rate_delay is not None and crawl_delay is not None:
            return min(req_rate_delay, crawl_delay)
        return req_rate_delay if req_rate_delay is not None else crawl_delay

    def crawl_allowed(self, url_or_path: str) -> bool:
        return self.parser.can_fetch(self.user_agent, url_or_path)

    def set_url(self, url: str):
        """Sets the URL to the robots.txt at the root of the specified link."""
        parsed_url = urlparse(url)
        self.url = f"{parsed_url.scheme if len(parsed_url.scheme) > 0 else 'http'}://{parsed_url.netloc}/robots.txt"

    def parse(self, text: str) -> bool:
        """Attempts to parse the robots.txt file. Returns True if successful."""
        # noinspection PyBroadException
        try:
            self.parser = Protego.parse(text)
            self.exists = True
        except Exception:
            LOG.error(f"Unable to parse robots.txt located at {self.url}")
            LOG.error(traceback.format_exc())
            self.exists = False
        return self.exists

    def delay_if_needed(self):
        """Waits until enough time has passed after the last request to perform another request."""
        if self.last_request_time is None:
            self.last_request_time = datetime.now() - timedelta(
                seconds=self.crawl_delay
            )
        time_passed = (datetime.now() - self.last_request_time).total_seconds()
        from backend.scraping.context import ctx

        if ctx.settings.crawl_delay_override is not None:
            crawl_delay = ctx.settings.crawl_delay_override
        else:
            crawl_delay = self.crawl_delay
        delay_amount = crawl_delay - time_passed
        if delay_amount > 0:
            LOG.info(f"Delaying for {delay_amount:.2f} seconds...")
            time.sleep(delay_amount)
