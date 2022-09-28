
from agtern.data import DataFile
import csv, json

def import_companies():
    """Imports all company names and links from companies.csv into scraping_config.json."""

    companies_csv = DataFile( "companies.csv" )

    if not companies_csv.exists():
        raise FileNotFoundError( "companies.csv does not exist!" )

    scraping_config_json = DataFile( "scraping_config.json", default_data = "[]" )

    original_config = []
    with open( scraping_config_json.path, "r" ) as f:
        original_config = json.load( f )

    data = []
    with open( companies_csv.path, "r" ) as f:
        reader = csv.DictReader( f, fieldnames = [ "company", "link" ] )
        for entry in reader:
            found_existing_entry = False
            for original_entry in original_config: # Just update link if entry already exists
                if original_entry["company"] == entry["company"]:
                    original_entry["link"] = entry["link"].strip().strip( "\"" )
                    data.append( original_entry )
                    found_existing_entry = True
            if not found_existing_entry:
                data.append( {
                    "company": entry["company"],
                    "link": entry["link"].strip().strip( "\"" ),
                    "scrape": {}
                } )

    with open( scraping_config_json.path, "w" ) as f:
        json.dump( data, f, indent = 2 )