from backend.scraping.actions import *
from backend.scraping.pipelines import *


@scrape_internships("Tesla")
def scrape_tesla():
    # scroll_to_bottom()
    scrape("title", "year", "period", "category", "location")
    match("title", "year", "period")
    for link in scrape("posting_link"):
        goto(link)
        scrape("description", "company_job_id", "job_type", "apply_link")


@process_internship("Tesla")
def process_tesla():
    get_tags("title", "description")
