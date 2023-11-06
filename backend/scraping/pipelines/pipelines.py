from backend.scraping.actions.actions import ActionFailure, goto_default, sleep
from backend.scraping.context.context import ctx

from .pipeline_registry import pipeline_decorator


def before_scrape():
    ctx.unique = ctx.config.unique
    goto_default()
    sleep(3000)


def after_scrape():
    column_lengths = [len(ctx.data[column]) for column in ctx.data.keys()]
    if min(column_lengths) != max(column_lengths):
        column_length_dict = {
            column: len(ctx.data[column]) for column in ctx.data.keys()
        }
        # TODO: Save this data so that the pipeline can be resumed?
        raise ActionFailure(
            f"Internship data length mismatch! SCRAPE DATA LOST! {column_length_dict}"
        )
    company_name = ctx.config.company_name
    ctx.data["company"] = [company_name for i in range(column_lengths[0])]
    # Rotate dict of column names mapped to lists into list of dicts mapped to single values:
    ctx.data = [
        dict(zip(ctx.data.keys(), internship)) for internship in zip(*ctx.data.values())
    ]
    # TODO: Warn when xpaths, regexes, etc. are unused in the pipeline


scrape_internships = pipeline_decorator("scrape", before_scrape, after_scrape)
process_internship = pipeline_decorator("process")
