from argparse import ArgumentParser

import agtern
from agtern.pipelines import import_companies, sort_companies


def run_cli(args=None):
    parser = ArgumentParser(prog="AgTern")
    parser.add_argument("--update-companies", action="store_true")
    parser.add_argument("--show-scraper", action="store_true")
    parser.add_argument("--noscrape", action="store_true")
    args = parser.parse_args(args)

    if args.update_companies:
        print("INFO: Updating company info...")
        sort_companies()
        import_companies()
    else:
        print("INFO: Starting program...")
        agtern.main(noscrape=args.noscrape, headless_scraper=not args.show_scraper)
