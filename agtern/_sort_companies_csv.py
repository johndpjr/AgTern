
# Read the csv
with open( "companies.csv", "r" ) as f:
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
final_lines = []
for company_name in company_names:
    final_lines.append( companies[company_name] )

# Write the csv
with open( "companies.csv", "w" ) as f:
    f.write( "\n".join( final_lines ) )