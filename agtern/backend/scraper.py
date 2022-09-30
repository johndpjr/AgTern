
"""Pre-MVP: This file reads from a config file to scrape websites and save them in a json file.
Post-MVP: This file will read configs from a database to scrape websites and save the results back into the database."""

from multiprocessing import Process
import json
import dataclasses

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as condition
from selenium.webdriver.common.by import By

from agtern.core import Internship

def scrape():
    """Pre-MVP: This function scrapes all websites in the config and stores them in a file.
    Post-MVP: This function will take arguments to specify how and where to scrape. The results will be stored in a database."""
    driver = None
    try:
        options = Options()
        # options.headless = True
        driver = webdriver.Chrome( options = options )
        wait = WebDriverWait( driver, 5 )
        driver.get( "https://www.tesla.com/careers/search/?query=Internship&site=US" )
        tbody: WebElement = wait.until(
            condition.presence_of_element_located( ( By.CLASS_NAME, "tds-table-body" ) )
        )
        internships = []
        for tr in tbody.find_elements( By.CLASS_NAME, "tds-table-row" ):
            res = tr.find_elements( By.TAG_NAME, "td" )
            info = res[0].find_element( By.TAG_NAME, "a" )
            title = info.text
            link = info.get_attribute( "href" )
            category = res[1].text
            location = res[2].text
            internship = Internship( title, link, category, location )
            internships.append( dataclasses.asdict( internship ) )
            print( f"{internship}\n" )
        print( "Writing to database..." )
        with open( "db.json", "w" ) as db:
            db.write( json.dumps( internships ) )
        print( "Done!" )
    finally:
        # Ensure driver is closed if an exception occurs
        if driver is not None:
            driver.close()

def start_scraper():
    open( "db.json", "w+" ) # Create json file if it doesn't exist
    scraper = Process( target = scrape )
    scraper.daemon = True # Run in background, so it doesn't block the GUI (if shown)
    scraper.start()