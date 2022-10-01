
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

import signal

from agtern.models import Internship

def scrape( headless: bool = True ):
    """Pre-MVP: This function scrapes all websites in the config and stores them in a file.
    Post-MVP: This function will take arguments to specify how and where to scrape. The results will be stored in a database."""
    driver = None

    def close_driver( signal_number = None, frame = None ):
        if driver is not None:
            driver.close()
        exit( 0 )

    # Ensure driver is closed if interrupted:
    # signal.signal( signal.SIGINT, close_driver )

    try:
        options = Options()
        options.headless = headless
        driver = webdriver.Chrome( options = options )
        wait = WebDriverWait( driver, 5 )

        with open( "scraping_config.json", "r" ) as f:
            config = json.load( f )

        internships = []
        for company_config_entry in config:
            company_name = company_config_entry["company"]
            if "scrape" not in company_config_entry.keys() or len( company_config_entry["scrape"].keys() ) == 0:
                print( f"{company_name} does not have any scrapeable properties. Skipping!" )
                continue

            print( f"Scraping {company_name}..." ) # Company name

            driver.get( company_config_entry["link"] )

            data = {}
            for property in company_config_entry["scrape"].keys():
                elements = wait.until(
                        condition.presence_of_all_elements_located(
                                ( By.XPATH, company_config_entry["scrape"][property] )
                        )
                )
                data[property] = [ element.text for element in elements ]

            for i in range( len( data[list( data.keys() )[0]] ) ):
                internship = {
                    "company": company_name
                }
                for property in data.keys():
                    internship[property] = data[property][i]
                internships.append( internship )

        print( "Writing to database..." )
        with open( "db.json", "w" ) as f:
            json.dump( internships, f, indent = 2 )
        print( "Done!" )
    finally:
        # Ensure driver is closed if an exception occurs
        close_driver()

def start_scraper( headless = True ):
    scraper = Process( target = scrape, args = ( headless, ) ) # DO NOT REMOVE COMMA!!
    scraper.daemon = True # Run in background, so it doesn't block the GUI (if shown)
    scraper.start()