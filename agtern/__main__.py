from agtern.gui import Application
from agtern.backend import start_server

HEADLESS_SCRAPER = True


def main(headless_scraper=None):
    if headless_scraper is None:
        start_server(HEADLESS_SCRAPER)
    else:
        start_server(headless_scraper)
    app = Application()
    try:
        app.mainloop()
    except KeyboardInterrupt:  # Ctrl+C
        pass  # Do nothing and hide Traceback


if __name__ == '__main__':
    main()
