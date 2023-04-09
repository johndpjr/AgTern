import logging
from argparse import ArgumentParser, Namespace

from .app.server import start_server
from .app.utils import LOG


def main(args: Namespace):
    if args.dev:
        start_server(args)
    else:
        LOG.warning("--dev not set; server is not running locally")


def run_cli():
    parser = ArgumentParser(prog="AgTern")
    parser.add_argument("--show-scraper", dest="headless", action="store_false")
    parser.add_argument("--no-scrape", action="store_true")
    parser.add_argument("--scrape-only", action="store_true")
    parser.add_argument("--save-jobs", action="store_true")
    parser.add_argument("--run-as-proc", dest="multiprocessing", action="store_true")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    if args.dev:
        LOG.setLevel(logging.INFO)
    else:
        LOG.warning("Running in production (set --dev for INFO messages)...")

    try:
        LOG.info("Starting program...")
        main(args)
        LOG.info("Closing program...")
    except Exception as e:
        LOG.error(f"An exception occurred: {e}", exc_info=True)


if __name__ == "__main__":
    run_cli()
