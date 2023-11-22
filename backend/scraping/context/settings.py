from __future__ import annotations


class ScrapeSettings:
    # noinspection PyTypeChecker
    def __init__(self):
        # Set the number of seconds that the web scraper waits for elements to exist before raising an error
        # A long delay will reduce errors due to slow connection speed,
        # but increases scraping time if websites don't load properly
        self.timeout: float = 5

        # Limit the number of links visited, jobs processed, etc
        # If None, all internships are scraped
        self.max_jobs: int = 3

        # Override the crawl_delay specified in robots.txt
        # WARNING! Setting this too low WILL get you blocked on some websites!
        # If None, the crawl delay in robots.txt is used
        # If 0, scraping is performed as fast as your connection speed allows
        self.crawl_delay_override: float = None

        # Prints the processed Job objects as JSON to the console before writing to the database
        # It is recommended to also set max_internships to avoid flooding the console
        self.print_result: bool = False

        # Enables printing tracebacks in addition to error messages when errors are encountered during scraping
        # Can sometimes be useful when debugging, but most of the time it is too much information
        self.print_tracebacks: bool = False

        # This is a case-insensitive list of the names of the companies that should be scraped
        # If None, everything is scraped
        # If [], nothing is scraped
        self.scrape_companies: list[str] = None


default_settings = ScrapeSettings()
