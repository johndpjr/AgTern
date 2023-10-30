import re
from typing import *

from pydantic import *
from pydantic import AnyUrl


class ConfigLookupError(KeyError):
    def __init__(self, *args):
        super().__init__(*args)


# TODO: Update these validators for Pydantic 2 (should be less buggy)
class RegexConfigModel(BaseModel):
    pattern: re.Pattern  # Automatically compiles regex
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
            values["_use_default_on_failure"] = "default" in values
            values["pattern"] = re.compile(values["pattern"], flags)
            return RegexConfigModel.construct(**values)

    @property
    def flags(self):
        return self._flags

    @property
    def use_default_on_failure(self):
        return self._use_default_on_failure


class CompanyConfigModel(BaseModel):
    name: str
    # TODO: Add company metadata here (category, tags, etc)


class CompanyScrapeConfigModel(BaseModel):
    company: CompanyConfigModel
    links: dict[str, AnyUrl] = {}
    xpaths: dict[str, str] = {}
    regexes: dict[str, RegexConfigModel] = {}
    unique: list[str] = []

    @root_validator(pre=True)
    def validate(cls, values):
        """Transforms string aliases into config objects."""
        if "company" in values and isinstance(values["company"], str):
            values["company"] = CompanyConfigModel(name=values["company"])
        if "regexes" in values and isinstance(values["regexes"], dict):
            for key, value in values["regexes"].items():
                if isinstance(value, str):
                    # noinspection PyTypeChecker
                    values["regexes"][key] = RegexConfigModel(pattern=value)
        return values

    @property
    def company_name(self):
        return self.company.name

    @property
    def default_link(self) -> Union[AnyUrl, None]:
        if len(self.links.values()) == 0:
            return None
        if "internships" in self.links:
            return self.links["internships"]
        if "home" in self.links:
            return self.links["home"]
        return next(
            iter(self.links.values())
        )  # First value in dict (at least for CPython 3.6+)

    def lookup(self, source_name: str, name: str):
        source = getattr(self, source_name)
        if name in source:
            return source[name]
        raise ConfigLookupError(f"{self.company_name.lower()}:{source_name}:{name}")

    def link(self, name: str):
        return self.lookup("links", name)

    def xpath(self, name: str):
        return self.lookup("xpaths", name)

    def regex(self, name: str):
        return self.lookup("regexes", name)
