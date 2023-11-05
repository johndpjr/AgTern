class ActionFailure(Exception):
    """Raised when something goes wrong when executing an action in a pipeline."""

    def __init__(self, *args):
        super().__init__(*args)


class ScrapeString(str):
    """Represents a string that has been scraped off of a website.
    This string should be interpreted literally, not as a link id, xpath id, etc."""

    # No extra functionality, just used for subclass checks
    pass
