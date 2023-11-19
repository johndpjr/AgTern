import traceback
from json import JSONDecodeError
from typing import Union

from pydantic import ValidationError

from backend.app.utils import LOG, DataFile, DataFolder

from .models import CompanyScrapeConfigModel

registry: dict[str, CompanyScrapeConfigModel] = {}
configs_loaded: bool = False


def register_config(config: CompanyScrapeConfigModel):
    """Adds a scrape config to the registry. Raises an exception if the config already exists."""
    company_name = config.company_name
    if company_name.lower() in registry.keys():
        raise Exception(
            f"The scrape configuration for {company_name} has already been loaded! Call remove_config before loading again."
        )
    registry[company_name.lower()] = config


def get_config(company_name: str) -> Union[CompanyScrapeConfigModel, None]:
    """Retrieves a scrape config by company name. Returns None if the config hasn't been loaded."""
    try:
        return registry[company_name.lower()]
    except KeyError:
        return None


def remove_config(company_name: str):
    """Attempts to remove a scrape config by company name. Raises an exception if the config hasn't been loaded."""
    try:
        del registry[company_name.lower()]
    except KeyError:
        raise Exception(
            f"The scrape configuration for {company_name} has not been loaded!"
        )


def load_config(file: DataFile) -> dict:
    """Loads the json from the given file and preprocesses it. Raises JSONDecodeError on failure."""
    json = file.load_json()
    if isinstance(json, list):
        raise JSONDecodeError("Expected JSON object, not list", file.name, 0)
    for required_prop in ["$schema", "company", "unique"]:
        if required_prop not in json:
            LOG.warn(f'{file.name} does not have a "{required_prop}" property!')
    if "company" in json and isinstance(json["company"], str):
        json["company"] = {"name": json["company"]}
    if "regex" in json and isinstance(json["regex"], dict):
        for name, value in json["regex"].items():
            if isinstance(value, str):
                json["regex"][name] = {"pattern": value}


def load_configs():
    """Attempts to load all scrape configuration json files from data/companies and store them in the config registry. Logs errors for invalid configs. Returns all of the configs that have been loaded."""
    global configs_loaded
    if configs_loaded:
        raise Exception(
            "Scrape configurations have already been loaded! Call reset_configs before loading again."
        )
    LOG.info("Loading scrape configuration files...")
    configs_loaded = True
    for file in DataFolder("companies").files():
        if (
            not file.extension == ".json"
            or file.name_without_extension.lower().endswith("schema")
            or file.name.startswith("_")
        ):
            continue
        # noinspection PyBroadException
        try:
            json = load_config(file)
            register_config(CompanyScrapeConfigModel(**json))
        except (ValidationError, JSONDecodeError) as e:
            LOG.error(
                f"Validation of {file.name} failed! {file.name_without_extension} will not be scraped."
            )
            LOG.error(e)
        except Exception:
            LOG.error(
                f"Error loading {file.name}! {file.name_without_extension} will not be scraped."
            )
            LOG.error(traceback.format_exc())
    return get_configs()


def get_configs() -> list[CompanyScrapeConfigModel]:
    """Retrieves a sorted list of all the scrape configs that have been loaded successfully."""
    return sorted(list(registry.values()), key=lambda config: config.company_name)


def get_company_names() -> list[str]:
    """Retrieves a list of the names of the companies whose configs have been loaded successfully."""
    # Need list comprehension since keys of registry are all lowercase
    return [config.company_name for config in registry.values()]


def reset_configs():
    global registry, configs_loaded
    registry = {}
    configs_loaded = False


# Requires:
# jsonschema[format]==4.19.1
# rfc3987==1.3.8
#
# schema_json = companies_folder.file("AgTernScrapeConfigSchema.json")
# schema_validator = None
# if schema_json.exists():
#     try:
#         schema = schema_json.load_json()
#         jsonschema.Draft202012Validator.check_schema(schema)
#         schema_validator = jsonschema.Validator(schema, format_checker=jsonschema.draft202012_format_checker)
#     except jsonschema.exceptions.ValidationError:
#         schema_validator = None
#         LOG.error(f"Unable to load {schema_json.name}! Company scrape configurations will not be validated.")
#         traceback.format_exc()
# if schema_validator is not None:
#     try:
#         schema_validator.validate(config)
#     except jsonschema.exceptions.ValidationError:
#         LOG.error(f"Validation of {file.name} failed! {company} will not be scraped.")
#         for err in schema_validator.iter_errors(config):
#             LOG.error(err.message)
#         continue
