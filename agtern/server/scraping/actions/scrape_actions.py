from __future__ import annotations

import time
from random import randint
from typing import Callable, List

import pandas as pd
from pydantic import AnyUrl
from selenium.webdriver import ActionChains

from .models import ScrapingContext, ScrapePropertyModel
from .scrape_action_registry import register_action


def scrape_action(name: str):
    """Returns a decorator that registers this function as a scraping action."""

    def decorator(function: Callable):
        """Register the scrape action and return the function unchanged."""
        register_action(name, function)
        return function

    return decorator


# See https://pydantic-docs.helpmanual.io/usage/types for a list of built-in type annotations


@scrape_action("goto")
def goto(ctx: ScrapingContext, url: AnyUrl):
    ctx.scraper.goto(url)


@scrape_action("sleep")
def sleep(ms: float):
    time.sleep(ms / 1000)


@scrape_action("click")
def click(ctx: ScrapingContext, xpath: str):
    ActionChains(ctx.scraper.driver).click(ctx.scraper.scrape_xpath(xpath)[0]).perform()


@scrape_action("scroll_to_bottom")
def scroll_to_bottom(ctx: ScrapingContext):
    screen_height = ctx.scraper.js("return window.screen.height")
    at_bottom = False
    num_scrolls = 0
    while not at_bottom:
        num_scrolls += 1
        time.sleep(randint(100, 250) / 1000)
        ActionChains(ctx.scraper.driver).scroll_by_amount(0, screen_height).perform()
        time.sleep(0.2)  # Time to complete request and show more elements
        scroll_height = ctx.scraper.js("return document.body.scrollHeight")
        if screen_height * num_scrolls > scroll_height:
            at_bottom = True


@scrape_action("scrape")
def scrape(ctx: ScrapingContext, prop: ScrapePropertyModel):
    if prop.value is not None:
        ctx.data[prop.name] = prop.value
        return
    elements = ctx.scraper.scrape_xpath(prop.xpath)
    # Create column with found elements and add to DataFrame
    contents = []
    for element in elements:
        # Scrape off of current page
        text = element.get_attribute(prop.html_property)
        if prop.regex is not None:
            # Match against regex in config
            match = prop.regex.pattern.search(text)
            if match is not None:
                # Replace text with either group or format string
                if prop.regex.format is not None:
                    text = prop.regex.format.format(match.groupdict())
                else:
                    text = match.group(prop.regex.group)  # Group 0 is the whole match
            else:
                text = prop.regex.default
        contents.append(text)
    ctx.data[prop.name] = pd.Series(contents, dtype=prop.store_as)
    ctx.data["company"] = ctx.company
