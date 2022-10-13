from argparse import ArgumentParser

from .gui import Application
from .pipelines import import_companies, sort_companies, start_server

HEADLESS_SCRAPER = True


def main(noscrape: bool = True, headless_scraper=None):
    if not noscrape:
        if headless_scraper is None:
            start_server(HEADLESS_SCRAPER)
        else:
            start_server(headless_scraper)

    app = Application()
    try:
        app.mainloop()
    except KeyboardInterrupt:  # Ctrl+C
        pass  # Do nothing and hide Traceback


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
        main(noscrape=args.noscrape, headless_scraper=not args.show_scraper)


if __name__ == "__main__":
    run_cli()
