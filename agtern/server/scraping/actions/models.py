from __future__ import annotations

import re
from inspect import Parameter
from types import MappingProxyType
from typing import Callable, Optional, List, Pattern, Union

import pandas as pd
from pydantic import BaseModel, conint, validator, root_validator, ValidationError


# See https://pydantic-docs.helpmanual.io/usage/types/ for a complete list of Pydantic built-in type annotations


class ScrapingContext(BaseModel):
    # noinspection PyUnresolvedReferences
    scraper: "WebScraper"  # ForwardRef to prevent circular reference
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


class RegexConfigModel(BaseModel):
    pattern: Pattern  # Automatically compiles regex
    group: Union[conint(ge=0, lt=100), str] = 0  # Can be 0 (whole match), 1-99 (group number), or str (group name)
    format: str = None  # Specify either format or group
    default: str = None  # String to use if the match fails

    # Regex flags
    # See https://docs.python.org/3/howto/regex.html#compilation-flags
    ascii: bool = False
    dotall: bool = False
    ignorecase: bool = False
    locale: bool = False
    multiline: bool = False
    verbose: bool = False

    flags: int = 0

    @root_validator(pre=True)
    def validate_format(cls, values):
        if "group" in values and "format" in values:
            raise ValueError("Both \"group\" and \"format\" were specified. "
                             "Either specify a group id or a format string!")
        return values

    @root_validator(skip_on_failure=True)
    def validate(cls, values):
        if "pattern" in values:
            # Recompile regex with specified flags
            flags = 0
            all_flags = {
                "ascii": re.ASCII,
                "dot_all": re.DOTALL,
                "ignore_case": re.IGNORECASE,
                "locale": re.LOCALE,
                "multiline": re.MULTILINE,
                "verbose": re.VERBOSE
            }
            for flag in all_flags:
                if flag in values:
                    flags |= all_flags[flag]
            values["flags"] = flags
            values["pattern"] = re.compile(values["pattern"], flags)
            return RegexConfigModel.construct(**values)


class ScrapePropertyModel(ScrapeActionModel):
    xpath: str = None
    value: str = None  # Constant string to use as a column value
    html_property: str = "innerText"
    regex: Optional[RegexConfigModel] = None

    @root_validator(pre=True)
    def validate_value(cls, values):
        if "value" in values and len(values.keys()) > 1:
            raise ValueError("Property \"value\" cannot be used with additional properties!")
        return values


class CompanyScrapeConfigModel(BaseModel):
    company: str
    link: str
    scrape: List[ScrapeActionModel]
