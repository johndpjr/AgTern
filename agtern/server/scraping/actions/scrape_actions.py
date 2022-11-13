from __future__ import annotations

import time
from random import randint
from typing import Callable, List

import pandas as pd
from pydantic import AnyUrl
from selenium.webdriver import ActionChains

from agtern.common import LOG

from .models import ScrapePropertyModel, ScrapingContext
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


@scrape_action("type")
def type(ctx: ScrapingContext, xpath: str, text: str):
    # TODO: Delay in between keystrokes
    ActionChains(ctx.scraper.driver).send_keys_to_element(
        ctx.scraper.scrape_xpath(xpath)[0], *text
    ).perform()


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


def scrape_property(ctx: ScrapingContext, prop: ScrapePropertyModel):
    if prop.unique and prop.name not in ctx.unique_properties:
        ctx.unique_properties.append(prop.name)
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
            elif prop.regex.use_default_on_failure:
                text = prop.regex.default
        contents.append(text)
    new_data = pd.Series(contents, dtype=prop.store_as)
    if prop.name in ctx.data:
        # Append new data to the end of the column
        previous_data_length = ctx.scraping_progress[prop.name]
        previous_data = ctx.data[prop.name][:previous_data_length]
        ctx.data.drop(columns=prop.name)
        ctx.data[prop.name] = pd.concat([previous_data, new_data], ignore_index=True)
        ctx.scraping_progress[prop.name] += len(new_data)
    else:
        ctx.data[prop.name] = pd.Series(contents, dtype=prop.store_as)
        ctx.scraping_progress[prop.name] = len(new_data)


@scrape_action("scrape")
def scrape(
    ctx: ScrapingContext,
    link: AnyUrl = None,
    link_property: str = None,
    prop: ScrapePropertyModel = None,
    properties: List[ScrapePropertyModel] = None,
):
    if prop is not None and properties is not None:
        raise ValueError('Both "prop" and "properties" were specified!')
    if link is not None and link_property is not None:
        raise ValueError('Both "link" and "link_property" were specified!')

    if link is not None:
        ctx.scraper.goto(link)
    elif link_property is not None:
        links = ctx.data[link_property]
        i = 1
        num_links = len(links)
        for link in links:
            LOG.info(f"Scraping link {i}/{num_links} ({link})...")
            scrape(ctx, link=link, prop=prop, properties=properties)
            # Uncomment below to just scrape 3 links
            # TODO: Add a command-line argument to limit how many internships we scrape for testing
            # if i == 2:
            #     return
            i += 1
        return

    if properties is not None:
        i = 1
        num_props = len(properties)
        for prop in properties:
            LOG.info(f"Scraping property {i}/{num_props} ({prop.name})...")
            scrape(ctx, prop=prop)
            i += 1
        return
    elif prop is not None:  # If both are None, nothing executes
        if prop.value is not None:
            ctx.data[prop.name] = prop.value
        scrape_property(ctx, prop)
        ctx.data["company"] = ctx.company
