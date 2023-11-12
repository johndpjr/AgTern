from __future__ import annotations

import contextvars
from typing import TYPE_CHECKING, Any, Callable, Union

from backend.app.database import DatabaseSession

from .robots_txt import RobotsTxt

if TYPE_CHECKING:
    from backend.scraping import WebScraper
    from backend.scraping.config import CompanyScrapeConfigModel

ctxvar = contextvars.ContextVar("ctx")


class ScrapeSettings:
    # noinspection PyTypeChecker
    def __init__(self):
        # Set the number of seconds that the web scraper waits for elements to exist before raising an error
        self.timeout: float = 5

        # Limit the number of links visited, jobs processed, etc
        self.max_internships: int = 3

        # Override the crawl_delay specified in robots.txt
        # WARNING! Setting this too low WILL get you blocked on certain websites!
        self.crawl_delay_override: float = None

        # Prints the processed Job objects as JSON to the console before writing to the database
        # It is recommended to also set max_internships to avoid flooding the console
        self.print_result: bool = False

        # Enables printing tracebacks in addition to error messages when errors are encountered during scraping
        # Can sometimes be useful when debugging, but most of the time it is too much information
        self.print_tracebacks: bool = False
        # TODO: Add more variables that change how scraping is performed


class ScrapeContext:
    # Allow initializing class variables to None:
    # noinspection PyTypeChecker
    def __init__(self):
        self.scraper: WebScraper = None
        self.config: CompanyScrapeConfigModel = None
        self.settings: ScrapeSettings = ScrapeSettings()
        self.db: DatabaseSession = DatabaseSession()
        self.data: dict[str, Union[list[str], str]] = {}
        self.unique: list[str] = []
        self.robots_txt: RobotsTxt = RobotsTxt()

    def execute(self, function: Callable, *args, **kwargs) -> Any:
        return call_with_context(function, self, *args, **kwargs)

    def valid(self):
        """Returns true if all context variables have been properly set."""
        return (
            self.scraper is not None
            and self.config is not None
            and self.settings is not None
            and self.db is not None
            and self.data is not None
            and self.unique is not None
            and self.robots_txt is not None
        )

    def savemap_lookup(self, some_id: str, savemap: dict[str, str]) -> str:
        """Maps an ID to a column string.
        If savemap is None or doesn't contain the ID, the ID is returned."""
        if savemap is None:
            return some_id
        if some_id not in savemap:
            if "*" in savemap:
                return savemap["*"]
            else:
                return some_id
        return savemap[some_id]

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, item):
        return item in self.data

    def __repr__(self):
        return f"ScrapeContext({self.config.company_name})"

    # TODO: Add __enter__ and __exit__ to make this a context manager usable with the 'with' statement


class ScrapeContextProxy(ScrapeContext):
    """Defines a fake ScrapeContext that proxies attribute access to the currently active context."""

    # noinspection PyMissingConstructor
    def __init__(self):
        """Redefine the constructor to do nothing."""
        pass

    def __getattr__(self, item):
        """Proxies attribute access to the currently active context."""
        try:
            return getattr(ctxvar.get(), item)
        except LookupError:
            raise LookupError("There is no active ScrapeContext!")

    def __setattr__(self, key, value):
        """Proxies attribute assignment to the currently active context."""
        try:
            setattr(ctxvar.get(), key, value)
        except LookupError:
            raise LookupError("There is no active ScrapeContext!")


# Show ctx as a variable in IDEs, even if it doesn't technically exist
ctx: ScrapeContext = ScrapeContextProxy()


def get_active_context() -> ScrapeContext:
    """Gets the current context. Should be semantically equal to ctx."""
    return ctxvar.get()


def wrap_with_context(function: Callable, context: ScrapeContext) -> Callable:
    """Wraps a function so that it is aware of the ScrapeContext for this company."""

    def wrapper(*args, **kwargs):
        local_ctx = contextvars.Context()

        def modified_function():
            ctxvar.set(context)
            return function(*args, **kwargs)

        return local_ctx.run(modified_function)

    return wrapper


def call_with_context(
    function: Callable, context: ScrapeContext, *args, **kwargs
) -> Any:
    """Calls a function with a ScrapeContext."""
    local_ctx = contextvars.Context()

    def modified_function():
        ctxvar.set(context)
        return function(*args, **kwargs)

    return local_ctx.run(modified_function)