from argparse import ArgumentParser, Namespace
from threading import Thread
import logging

from .common import LOG
from .gui import Application
from .server import start_server


def main(args: Namespace):
    if args.dev:
        if args.scrape_only:
            start_server(args)
            return
        else:
            Thread(
                target=start_server,
                daemon=True,
                args=(args,)
            ).start()
    else:
        LOG.warning("--dev not set; server is not running locally")

    app = Application()
    try:
        app.mainloop()
    except KeyboardInterrupt:  # Ctrl+C
        pass  # Do nothing and hide Traceback


def run_cli():
    parser = ArgumentParser(prog="AgTern")
    parser.add_argument("--update-companies", action="store_true")
    parser.add_argument("--show-scraper", dest="headless", action="store_false")
    parser.add_argument("--no-scrape", action="store_true")
    parser.add_argument("--scrape-only", action="store_true")
    parser.add_argument("--save-internships", action="store_true")
    parser.add_argument("--run-as-proc", dest="multiprocessing",
                        action="store_true")
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
