
import agtern
from agtern.scripts import *
from argparse import ArgumentParser

def run_cli( args = None ):
    parser = ArgumentParser( prog = "AgTern" )
    parser.add_argument(
            "script",
            choices = [ "import-companies", "sort-companies" ],
            action = "store",
            default = None,
            nargs = "?" # Might or might not exist
    )
    parser.add_argument( "--show-scraper", action = "store_true" )
    parser.add_argument( "--noscrape", action="store_true" )
    args = parser.parse_args( args )

    run_main = True
    if args.script == "import-companies":
        import_companies()
        run_main = False
    elif args.script == "sort-companies":
        sort_companies()
        run_main = False


    if run_main:
        agtern.main( noscrape = args.noscrape, headless_scraper = not args.show_scraper )