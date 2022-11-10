from __future__ import annotations

import time
from random import randint
from typing import Callable, List

import pandas as pd
from pydantic import AnyUrl
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys

from backend.app.utils import LOG

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
def click(ctx: ScrapingContext, xpath: str, must_exist: bool = True):
    elements = ctx.scraper.scrape_xpath(xpath)
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
    time.sleep(1)


@scrape_action("type")
def type(ctx: ScrapingContext, xpath: str, text: str):
    # TODO: Delay in between keystrokes
    ActionChains(ctx.scraper.driver)\
        .send_keys_to_element(ctx.scraper.scrape_xpath(xpath)[0], *text, Keys.ENTER)\
        .perform()


@scrape_action("scroll_to_bottom")
def scroll_to_bottom(ctx: ScrapingContext):
    LOG.info("Scrolling to the bottom of the page...")
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
    try:
        elements = ctx.scraper.scrape_xpath(prop.xpath)
    except TimeoutException:
        LOG.error(f"Unable to find {prop.name}! ({prop.xpath})")
        LOG.error(f"Assuming 1 element wasn't found.")
        ctx.scraping_progress[prop.name] += 1
        return
    # Create column with found elements and add to DataFrame
    contents = []
    for element in elements:
        # Scrape off of current page
        text = element.get_attribute(prop.html_property)
        if prop.loading_text is not None and text == prop.loading_text:
            LOG.info("Element is loading...")
            time.sleep(1)
            scrape_property(ctx, prop)
            return
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
        # See https://stackoverflow.com/a/74250413/11827673
        # I don't really know what this pandas code is doing
        # But hey, it works!
        ctx.data = pd.concat([
            ctx.data.drop(columns=prop.name),
            pd.concat([
                previous_data,
                new_data
            ], ignore_index=True).to_frame(prop.name)
        ], axis=1)
        ctx.scraping_progress[prop.name] += len(new_data)
    else:
        ctx.data[prop.name] = pd.Series(contents, dtype=prop.store_as)
        ctx.scraping_progress[prop.name] = len(new_data)


def goto_next_page(ctx: ScrapingContext, next_page: str = None):
    if next_page is None:
        return False
    try:
        elements = ctx.scraper.scrape_xpath(next_page)
        cursors = ctx.scraper.scrape_css(next_page, "cursor")
        if len(elements) > 0:
            valid = False
            for element, cursor in zip(elements, cursors):
                if element.is_enabled() and \
                   element.is_displayed() and \
                   element.get_attribute("aria-disabled") != "true" and \
                   cursor != "default":
                    valid = True
            if valid:
                click(ctx, next_page)
                return True
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass
    return False

@scrape_action("scrape")
def scrape(
        ctx: ScrapingContext,
        link: AnyUrl = None,
        link_property: str = None,
        prop: ScrapePropertyModel = None,
        properties: List[ScrapePropertyModel] = None,
        next_page: str = None,
        scroll: bool = False
):
    if prop is not None and properties is not None:
        raise ValueError('Both "prop" and "properties" were specified!')
    if link is not None and link_property is not None:
        raise ValueError('Both "link" and "link_property" were specified!')

    if link is not None:
        ctx.scraper.goto(link)
    if scroll:
        scroll_to_bottom(ctx)
    if link_property is not None:
        links = ctx.data[link_property]
        i = 1
        num_links = len(links)
        for link in links:
            LOG.info(f"Scraping link {i}/{num_links} ({link})...")
            scrape(ctx, link=link, prop=prop, properties=properties, next_page=next_page, scroll=scroll)
            # Uncomment below to just scrape 3 links
            # TODO: Add a command-line argument to limit how many internships we scrape for testing
            # Need to coordinate with scrape_property or all of the info on the first page for the other internships
            # will be scraped
            if i == 3:
                return
            i += 1
        return

    if properties is not None:
        i = 1
        num_props = len(properties)
        for _prop in properties:
            LOG.info(f"Scraping property {i}/{num_props} ({_prop.name})...")
            scrape(ctx, prop=_prop)
            i += 1
        if next_page is not None:
            LOG.info("Going to the next page...")
            if goto_next_page(ctx, next_page):
                scrape(ctx, properties=properties, next_page=next_page, scroll=scroll)
            else:
                LOG.info("No more pages!")
    if prop is not None:
        if prop.value is not None:
            ctx.data[prop.name] = prop.value
        else:
            scrape_property(ctx, prop)
        ctx.data["company"] = ctx.company
