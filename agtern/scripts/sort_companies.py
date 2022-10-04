
import json
from agtern.data import DataFile

def sort_companies():
    """Sorts both companies.csv and scraping_config.json by company name."""
    companies_csv = DataFile( "companies.csv", default_data = "" ) # Create if it doesn't exist

    # Read the csv
    with open( companies_csv.path, "r" ) as f:
        data = f.read()

    # Map name -> line of csv
    companies = {}

    # List of names
    company_names = []

    # Load and process csv data
    for line in data.split( "\n" ):
        if "," not in line:
            continue
        company_name = line.split( "," )[0]
        company_names.append( company_name )
        companies[company_name] = line

    # Sort the names
    company_names = sorted( company_names )

    # Construct new csv
    final_entries = []
    for company_name in company_names:
        final_entries.append( companies[company_name] )

    # Write the csv
    with open( companies_csv.path, "w" ) as f:
        f.write( "\n".join( final_entries ) )



    scraping_config_json = DataFile( "scraping_config.json", default_data = "[]" )

    # Read the json
    with open( scraping_config_json.path, "r" ) as f:
        data = json.load( f )

    # Map name -> entry of json
    companies = {}

    # List of names
    company_names = []

    # Load and process json data
    for entry in data:
        company_name = entry["company"]
        company_names.append( company_name )
        companies[company_name] = entry

    # Sort the names
    company_names = sorted( company_names )

    # Construct new json
    final_entries = []
    for company_name in company_names:
        final_entries.append( companies[company_name] )

    # Write the json
    with open( scraping_config_json.path, "w" ) as f:
        json.dump( final_entries, f, indent = 2 )