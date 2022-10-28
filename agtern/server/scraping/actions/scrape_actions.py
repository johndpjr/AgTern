from __future__ import annotations

import time
from typing import Callable, List

import pandas as pd
from pydantic import AnyUrl

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


@scrape_action("scrape")
def scrape(ctx: ScrapingContext, properties: List[ScrapePropertyModel]):
    for prop in properties:
        if prop.value is not None:
            ctx.data[prop.name] = prop.value
            continue
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
        ctx.data[prop.name] = pd.Series(contents)
    ctx.data["company"] = ctx.company
