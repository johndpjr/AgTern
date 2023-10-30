import time
from random import randint
from typing import Callable

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys

from backend.app.utils import LOG
from backend.scraping.context.context import ctx


class ActionFailure(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def raise_on_failure(action: Callable):
    def modified_action(*args, **kwargs):
        try:
            return action(*args, **kwargs)
        except Exception as cause:
            raise ActionFailure() from cause

    return modified_action


@raise_on_failure
def goto(url: str):
    """Navigates to a URL."""
    ctx.scraper.goto(url)


@raise_on_failure
def goto_default():
    """Navigates to the default URL."""
    goto(ctx.config.default_link)


@raise_on_failure
def sleep(ms: float):
    """Waits for a period of time."""
    time.sleep(ms / 1000)


@raise_on_failure
def click(xpath_id: str, must_exist: bool = True):
    """Clicks on one or more elements.
    Raises an exception if the element(s) cannot be located unless must_exist is False.
    """
    elements = ctx.scraper.scrape_xpath(ctx.config.xpath(xpath_id))
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
def type(xpath_id: str, text: str):
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
def scrape(*xpath_ids: str) -> list[str]:
    """Looks up a series of XPaths by ID, gets the text from each of the elements, and stores them in ctx.data."""
    if len(xpath_ids) != 1:
        elements = []
        for xpath_id in xpath_ids:
            elements += scrape(xpath_id)
        return elements
    xpath_id = xpath_ids[0]
    xpath = ctx.config.xpath(xpath_id)
    LOG.info(f"Scraping {xpath_id}...")
    if xpath_id not in ctx.data:
        ctx.data[xpath_id] = []
    if len(ctx.data[xpath_id]) > ctx.settings.max_internships:
        ctx.data[xpath_id] = ctx.data[xpath_id][: ctx.settings.max_internships]
        return []
    result = ctx.scraper.scrape_xpath(xpath)
    if len(result) == 0:
        raise ActionFailure(
            f'XPath "{xpath}" (id={xpath_id}) did not match any elements!'
        )
    if len(ctx.data[xpath_id]) + len(result) > ctx.settings.max_internships:
        result = result[: ctx.settings.max_internships - len(ctx.data[xpath_id])]
    ctx.data[xpath_id] += result
    return result


@raise_on_failure
def match(*regex_ids: str) -> list[str]:
    """Looks up a series of RegExes by ID and filters each column in ctx.data according to those IDs."""
    if len(regex_ids) != 1:
        strings = []
        for regex_id in regex_ids:
            strings += match(regex_id)
        return strings
    regex_id = regex_ids[0]
    regex = ctx.config.regex(regex_id)
    column = ctx.data[regex_id]
    strings = []
    for string in column:
        result = regex.pattern.search(string)
        if result is not None:
            # Replace text with either group or format string
            if regex.format is not None:
                string = regex.format.format(result.groupdict())
            else:
                string = result.group(regex.group)  # Group 0 is the whole match
        elif regex.use_default_on_failure:
            string = regex.default
        strings.append(string)
    ctx.data[regex_id] = strings
    return strings


@raise_on_failure
def get_tags(*column_ids):
    """Performs NLP to collect tags from the given column IDs and stores them in ctx.data['tags']."""
    if len(column_ids) > 1:
        for column_id in column_ids:
            get_tags(column_id)
    LOG.error("get_tags is not implemented yet!")
