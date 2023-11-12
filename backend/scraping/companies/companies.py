from backend.scraping.actions import *
from backend.scraping.pipelines import *


def default_scrape():
    pass


def default_process():
    get_tags("title", "description")


@scrape_internships("Allstate")
def scrape_allstate():
    scrape_text("title", "category", "location", "post_date")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("company_job_id", "description")
        scrape_links("apply_link")


@process_internship("Allstate")
def process_allstate():
    default_process()


@scrape_internships("Amazon")
def scrape_amazon():
    while True:
        scrape_text("title", "location", "post_date")
        scrape_links("posting_link")
        if not is_clickable("next_page"):
            break
        click("next_page")
    for link in column("posting_link"):
        goto(link)
        scrape_text("company_job_id", "description")
        scrape_links("apply_link")


@process_internship("Amazon")
def process_amazon():
    default_process()


@scrape_internships("Tesla")
def scrape_tesla():
    # scroll_to_bottom()
    scrape_text("title", "year", "period", "category", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "company_job_id", "job_type")
        scrape_links("apply_link")


@process_internship("Tesla")
def process_tesla():
    match("title", "year", "period")
    default_process()