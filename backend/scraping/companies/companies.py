from backend.scraping.actions import *
from backend.scraping.context import ctx
from backend.scraping.pipelines import *


def default_scrape():
    pass


def default_process():
    get_tags("title", "description")
    # Strip whitespace from either side of all columns
    ctx.data = {key: value.strip() for key, value in ctx.data.items()}


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
    scroll_to_bottom()
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
    match("location", "company_job_id", "post_date", "description")
    default_process()


@scrape_internships("Apple")
def scrape_apple():
    while True:
        scrape_text("title", "post_date")
        scrape_links("posting_link")
        if not is_clickable("next_page"):
            break
        click("next_page")
    for link in column("posting_link"):
        goto(link)
        scrape_text("category", "location", "company_job_id", "description")
        scrape_links("apply_link")


@process_internship("Apple")
def process_apple():
    match("description")
    default_process()


@scrape_internships("AT&T")
def scrape_att():
    click("category_tab")
    click("internships_category_button")
    click("show_all_button", must_exist=False)
    scrape_text("title", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "company_job_id", "post_date")
        scrape_links("apply_link")


@process_internship("AT&T")
def process_att():
    match("description", "company_job_id", "post_date")
    default_process()


@scrape_internships("Boeing")
def scrape_boeing():
    scrape_text("title", "company_job_id", "location", "post_date")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "category")
        scrape_links("apply_link")


@process_internship("Boeing")
def process_boeing():
    match("category", "description")
    default_process()


@scrape_internships("JPMorgan")
def scrape_jpmorgan():
    scroll_to_bottom()
    scrape_text("title", "category", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "job_type")
        scrape_links("apply_link")


@process_internship("JPMorgan")
def process_jpmorgan():
    match("title")
    default_process()


@scrape_internships("Cigna")
def scrape_cigna():
    while True:
        scrape_text("title")
        scrape_links("posting_link")
        if not is_clickable("next_page"):
            break
        click("next_page")
    for link in column("posting_link"):
        goto(link)
        scrape_text("category", "post_date", "company_job_id", "description")
        scrape_links("apply_link")


@process_internship("Cigna")
def process_cigna():
    match("category", "post_date", "company_job_id", "description")
    default_process()


@scrape_internships("Tesla")
def scrape_tesla():
    scroll_to_bottom()
    scrape_text("title", "year", "period", "category", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "company_job_id", "job_type")
        scrape_links("apply_link")


@process_internship("Tesla")
def process_tesla():
    match("title", "year", "period")
    default_process()


@scrape_internships("Texas Instruments")
def scrape_ti():
    scroll_to_bottom()
    scrape_text("title", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "company_job_id")
        scrape_links("apply_link")


@process_internship("Texas Instruments")
def process_ti():
    match("title")
    default_process()


@scrape_internships("Verizon")
def scrape_verizon():
    scroll_to_bottom()
    scrape_text("title", "category", "location")
    for link in scrape_links("posting_link"):
        goto(link)
        scrape_text("description", "company_job_id")
        scrape_links("apply_link")


@process_internship("Verizon")
def process_verizon():
    match("title")
    default_process()
