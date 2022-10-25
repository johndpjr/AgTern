from __future__ import annotations

from inspect import Parameter
from types import MappingProxyType
from typing import Callable, Optional, List

import pandas as pd
from pydantic import BaseModel


class ScrapingContext(BaseModel):
    scraper: "WebScraper"
    company: str
    data: pd.DataFrame = None

    class Config:
        arbitrary_types_allowed = True  # Allow pd.DataFrame annotation


class ScrapeAction(BaseModel):
    name: str
    parameters: MappingProxyType[str, Parameter]
    execute: Callable

    class Config:
        arbitrary_types_allowed = True


class ScrapeActionModel(BaseModel):
    name: str  # TODO: Validate against scraping action names


class ScrapePropertyModel(ScrapeActionModel):
    xpath: str
    html_property: str = "innerText"
    regex: Optional[str] = None


class CompanyScrapeConfigModel(BaseModel):
    company: str
    link: str
    scrape: List[ScrapeActionModel]
