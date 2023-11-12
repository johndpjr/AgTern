import time
from random import randint
from typing import Callable, Union

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys

from backend.app.utils import LOG
from backend.data_processing import get_keywords
from backend.scraping.context import ctx

from .models import ActionFailure, ScrapeString


def raise_on_failure(action: Callable):
    def modified_action(*args, **kwargs):
        try:
            return action(*args, **kwargs)
        except ActionFailure as cause:
            raise cause from None
        except Exception as cause:
            try:
                cause_str = str(cause)
                if len(cause_str) > 0:
                    cause_str = f": {cause_str}"
                cause_description = f"{type(cause).__name__}{cause_str}"
                new_cause = ActionFailure(cause_description).with_traceback(
                    cause.__traceback__
                )
            except Exception:
                # Fallback if an error occurs while printing
                raise ActionFailure() from cause
            # from None prevents exception chaining:
            raise new_cause from None

    return modified_action


@raise_on_failure
def column(column_id: str):
    """Alias for ctx.data[column_id]."""
    return ctx.data[column_id]


@raise_on_failure
def goto(link_id: str):
    """Navigates to a URL."""
    link = ctx.config.link(link_id)
    try:
        ctx.scraper.goto(link)
    except TimeoutException:
        id_hint = f" (id={link_id})" if ctx.config.is_id(link_id) else ""
        raise ActionFailure(f'Navigation to "{link}"{id_hint} timed out!') from None


@raise_on_failure
def goto_default():
    """Navigates to the default URL."""
    goto(ctx.config.default_link)


@raise_on_failure
def sleep(ms: float):
    """Waits for a period of time."""
    time.sleep(ms / 1000)


@raise_on_failure
def wait_until_true(predicate: Union[str, Callable[[], bool]]):
    """Waits until a JavaScript code string or Python function returns true.
    Times out after a few seconds."""
    if isinstance(predicate, str):
        return ctx.scraper.wait_until_true(predicate)
    return ctx.scraper.wait.until(lambda d: predicate())


@raise_on_failure
def is_clickable(*xpath_ids: str) -> Union[bool, list[bool]]:
    """Returns True if all of the elements matched by the specified XPath are clickable.
    Waits for at least one element to exist, but doesn't wait for an element to be clickable.
    Times out after a few seconds."""
    if len(xpath_ids) != 1:
        bools = []
        for xpath_id in xpath_ids:
            bools += is_clickable(xpath_id)
        return bools
    xpath_id = xpath_ids[0]
    xpath = ctx.config.xpath(xpath_id)
    try:
        elements = ctx.scraper.get_elements_by_xpath(xpath)
        # TODO: Fix this race condition caused by fetching the elements twice
        cursors = ctx.scraper.scrape_css(xpath, "cursor")
        if len(elements) == 0:
            return False
        for element, cursor in zip(elements, cursors):
            if (
                not element.is_enabled()
                or not element.is_displayed()
                or element.get_attribute("aria-disabled") == "true"
                or cursor == "default"
            ):
                return False
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False
    return True


@raise_on_failure
def click(xpath_id: str, must_exist: bool = True):
    """Clicks on one or more elements.
    Raises an exception if the element(s) cannot be located unless must_exist is False.
    """
    elements = ctx.scraper.get_elements_by_xpath(ctx.config.xpath(xpath_id))
    i = 0
    for element in elements:
        i += 1
        LOG.info(f"Clicking element {i}/{len(elements)}...")
        if must_exist:
            ctx.scraper.js("arguments[0].click()", element)
            time.sleep(0.25)
        else:
            try:
                ctx.scraper.js("arguments[0].click()", element)
                time.sleep(0.25)
            except TimeoutException:
                continue
    time.sleep(1)  # TODO: Is this necessary?


@raise_on_failure
def type_text(xpath_id: str, text: str):
    """Types text into a text input."""
    # TODO: Delay in between keystrokes
    ActionChains(ctx.scraper.driver).send_keys_to_element(
        ctx.scraper.get_elements_by_xpath(ctx.config.xpath(xpath_id))[0],
        *text,
        Keys.ENTER,
    ).perform()


@raise_on_failure
def scroll_to_bottom():
    """Scrolls to the bottom of the current page."""
    LOG.info("Scrolling to the bottom of the page...")
    scroll_amount = 1080
    at_bottom = False
    num_scrolls = 0
    while not at_bottom:
        num_scrolls += 1
        time.sleep(randint(100, 250) / 1000)
        ctx.scraper.js(f"window.scrollBy(0,{scroll_amount},{{behavior:'smooth'}})")
        # ActionChains(ctx.scraper.driver).scroll_by_amount(0, screen_height).perform()
        time.sleep(0.75)  # Time to scroll, complete request, and show more elements
        scroll_height = ctx.scraper.js("return document.body.scrollHeight")
        if scroll_amount * num_scrolls > scroll_height:
            at_bottom = True


@raise_on_failure
def scrape_text(*xpath_ids: str, savemap: dict[str, str] = None) -> list[str]:
    """Looks up a series of XPaths by ID, gets the text from each of the elements, and stores them in ctx.data."""
    if len(xpath_ids) != 1:
        elements = []
        for xpath_id in xpath_ids:
            elements += scrape_text(xpath_id, savemap=savemap)
        return elements
    xpath_id = xpath_ids[0]
    xpath = ctx.config.xpath(xpath_id)
    if xpath_id not in ctx.data:
        ctx.data[xpath_id] = []
    if ctx.settings.max_internships is not None:
        if len(ctx.data[xpath_id]) > ctx.settings.max_internships:
            ctx.data[xpath_id] = ctx.data[xpath_id][: ctx.settings.max_internships]
            return []
    try:
        result = ctx.scraper.scrape_xpath(xpath)
        if len(result) == 0:
            raise TimeoutException()
    except TimeoutException:
        id_hint = f" (id={xpath_id})" if ctx.config.is_id(xpath_id) else ""
        raise ActionFailure(
            f'XPath "{xpath}"{id_hint} did not match any elements on '
            f"{ctx.scraper.current_url}"
        ) from None
    LOG.info(f"Found {len(result)}x {xpath_id}")
    if ctx.settings.max_internships is not None:
        if len(ctx.data[xpath_id]) + len(result) > ctx.settings.max_internships:
            result = result[: ctx.settings.max_internships - len(ctx.data[xpath_id])]
    result = [ScrapeString(value) for value in result]
    ctx.data[ctx.savemap_lookup(xpath_id, savemap)] += result
    return result


@raise_on_failure
def scrape_links(*xpath_ids, savemap: dict[str, str] = None) -> list[str]:
    """Looks up a series of XPaths by ID, gets the text from each of the elements, and stores them in ctx.data.
    Transforms relative links to absolute links."""
    if len(xpath_ids) != 1:
        elements = []
        for xpath_id in xpath_ids:
            elements += scrape_links(xpath_id, savemap=savemap)
        return elements
    xpath_id = xpath_ids[0]
    column_id = ctx.savemap_lookup(xpath_id, savemap)
    links = scrape_text(xpath_id, savemap=savemap)
    ctx.data[column_id] = [
        ScrapeString(ctx.scraper.make_link_absolute(link))
        for link in ctx.data[column_id]
    ]
    return [ScrapeString(ctx.scraper.make_link_absolute(link)) for link in links]


@raise_on_failure
def match(*regex_ids: str, savemap: dict[str, str] = None) -> str:
    """Looks up a series of RegExes by ID and filters each column in ctx.data according to those IDs."""
    if len(regex_ids) != 1:
        strings = []
        for regex_id in regex_ids:
            strings += match(regex_id, savemap=savemap)
        return strings
    regex_id = regex_ids[0]
    regex = ctx.config.regex(regex_id)
    string = ctx.data[regex_id]
    LOG.info(f"Matching {regex_id} regex")
    result = regex.pattern.search(string)
    if result is not None:
        # Replace text with either group or format string
        if regex.format is not None:
            string = regex.format.format(result.groupdict())
            replacement = "FormatString"
        else:
            string = result.group(regex.group)  # Group 0 is the whole match
            replacement = "RegExGroup"
    elif regex.use_default_on_failure:
        string = regex.default
        replacement = "Default"
    else:
        replacement = "NoChange"
    string = ScrapeString(string)
    LOG.info(f"Match: {result is not None}")
    LOG.info(f"Replacement: {replacement}")
    ctx.data[ctx.savemap_lookup(regex_id, savemap)] = string
    return string


@raise_on_failure
def get_tags(*column_ids, savemap: dict[str, str] = None):
    """Performs NLP to collect tags from the given column IDs and stores them in ctx.data['tags'] by default."""
    # TODO: Move nlt.download into backend.data_processing.nlp
    import nltk

    nltk.download("popular", quiet=True)
    if len(column_ids) > 1:
        tags = []
        for column_id in column_ids:
            tags += get_tags(column_id, savemap=savemap)
        return tags
    if savemap is None:
        savemap = {"*": "tags"}
    column_id = column_ids[0]
    tags_column_id = ctx.savemap_lookup(column_id, savemap)
    LOG.info(f"Extracting keywords from {column_id}...")
    # TODO: Sort keywords and remove duplicates
    keywords = get_keywords(ctx.data[column_id]).lower()
    if tags_column_id in ctx.data:
        ctx.data[tags_column_id] = ScrapeString(
            ",".join(ctx.data[tags_column_id].split(",") + keywords.split(","))
        )
    else:
        ctx.data[tags_column_id] = ScrapeString(keywords)
    return keywords.split(",")
