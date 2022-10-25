from argparse import ArgumentParser

from .gui import Application
from .server import import_companies, sort_companies, start_server


def main(noscrape: bool = True, headless_scraper: bool = True, scrape_only: bool = False):
    if not noscrape:
        start_server(headless_scraper, scrape_only)

    if not scrape_only:
        app = Application()
        try:
            app.mainloop()
        except KeyboardInterrupt:  # Ctrl+C
            pass  # Do nothing and hide Traceback


def run_cli():
    parser = ArgumentParser(prog="AgTern")
    parser.add_argument("--update-companies", action="store_true")
    parser.add_argument("--show-scraper", action="store_true")
    parser.add_argument("--noscrape", action="store_true")
    parser.add_argument("--scrape-only", action="store_true")
    args = parser.parse_args()

    if args.update_companies:
        print("INFO: Updating company info...")
        sort_companies()
        import_companies()
    else:
        print("INFO: Starting program...")
        main(
            noscrape=args.noscrape,
            headless_scraper=not args.show_scraper and not args.scrape_only,
            scrape_only=args.scrape_only
        )


if __name__ == "__main__":
    run_cli()
