from __future__ import annotations

import re
from abc import ABCMeta
from enum import Enum
from inspect import Parameter
from types import MappingProxyType
from typing import *

import pandas as pd
from pydantic import *
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from backend.app.scraping import WebScraper


# See https://pydantic-docs.helpmanual.io/usage/types/ for a complete list of Pydantic built-in type annotations


class ScrapingContext(BaseModel):
    scraper: WebScraper
    company: str
    db: Session = None
    data: pd.DataFrame = None
    scraping_progress: Dict[str, int] = {}
    unique_properties: List[str] = []
    robots_txt: str = None

    class Config:
        arbitrary_types_allowed = True  # Allow pd.DataFrame annotation


class ScrapeAction(BaseModel):
    name: str
    parameters: MappingProxyType[str, Parameter]
    model: Union[BaseModel, ABCMeta]  # Hack to make IntelliSense work
    execute: Callable

    class Config:
        arbitrary_types_allowed = True

    @validator("model", pre=True)
    def validate_model(cls, value):
        if (
            isinstance(value, BaseModel)
            or str(type(value)).find("pydantic.main.ModelMetaclass") != -1
        ):  # Need this because we can't import it
            return value
        raise ValueError('"model" is not a Pydantic model!')


class ScrapeActionModel(BaseModel):
    name: str  # TODO: Validate against scraping action names


class RegexConfigModel(BaseModel):
    pattern: Pattern  # Automatically compiles regex
    group: Union[
        conint(ge=0, lt=100), str
    ] = 0  # Can be 0 (whole match), 1-99 (group number), or str (group name)
    format: str = None  # Specify either format or group
    default: str = None  # String to use if the match fails
    _use_default_on_failure: bool = False

    # Regex flags
    # See https://docs.python.org/3/howto/regex.html#compilation-flags
    ascii: bool = False
    dot_all: bool = False
    ignore_case: bool = False
    locale: bool = False
    multiline: bool = False
    verbose: bool = False

    _flags: int = 0

    @root_validator(pre=True)
    def validate_format(cls, values):
        if "group" in values and "format" in values:
            raise ValueError(
                'Both "group" and "format" were specified. '
                "Either specify a group id or a format string!"
            )
        return values

    @root_validator(pre=True)
    def validate_default(cls, values):
        values["_use_default_on_failure"] = "default" in values
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
                "verbose": re.VERBOSE,
            }
            for flag in all_flags:
                if flag in values:
                    flags |= all_flags[flag]
            values["_flags"] = flags
            values["pattern"] = re.compile(values["pattern"], flags)
            return RegexConfigModel.construct(**values)

    @property
    def flags(self):
        return self._flags

    @property
    def use_default_on_failure(self):
        return self._use_default_on_failure


class DataType(str, Enum):
    int = "int"
    float = "float"
    str = "str"
    bool = "bool"


class ScrapePropertyModel(ScrapeActionModel):
    xpath: str = None
    value: str = None  # Constant string to use as a column value
    html_property: str = "innerText"
    regex: RegexConfigModel = None
    store_as: DataType = DataType.str
    unique: bool = False

    @root_validator(pre=True)
    def validate_value(cls, values):
        if "value" in values and len(values.keys()) > 1:
            raise ValueError(
                'Property "value" cannot be used with additional properties!'
            )
        return values


class CompanyScrapeConfigModel(BaseModel):
    company: str
    link: str
    scrape: List[ScrapeActionModel]
