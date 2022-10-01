
import csv, json

data = []
with open( "companies.csv", "r" ) as f:
    reader = csv.DictReader( f, fieldnames = [ "company_id", "url" ] )
    for entry in reader:
        data.append( {
            "company": entry["company_id"],
            "link": entry["url"].strip().strip( "\"" )
        } )

with open( "../scraping_config.json", "w" ) as f:
    json.dump( data, f, indent = 2 )