import logging
from argparse import ArgumentParser

from .common import LOG
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
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    if args.dev:
        LOG.setLevel(logging.INFO)
    else:
        LOG.warning("Running in production (set --dev for INFO messages)...")

    if args.update_companies:
        LOG.info("Updating company info...")
        try:
            sort_companies()
            import_companies()
        except Exception:
            LOG.error("An exception occurred...", exc_info=True)
        LOG.info("Closing program...")
    else:
        LOG.info("Starting program...")
        try:
            main(
                noscrape=args.noscrape,
                headless_scraper=not args.show_scraper and not args.scrape_only,
                scrape_only=args.scrape_only
            )
        except Exception:
            LOG.error("An exception occurred...", exc_info=True)
        LOG.info("Closing program...")


if __name__ == "__main__":
    run_cli()
