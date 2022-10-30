import requests
from requests.adapters import HTTPAdapter, Retry

from .schemas import InternshipBase
from .logger import LOG


class AgTernAPI:
    """Wrapper for all communication to AgTern's services."""
    env = "dev"
    LOCALHOST_URL = "http://127.0.0.1:5000"
    SERVER_URL = "http://our-public-agtern-api.com"

    def __init__(self):
        # TODO: make this env dynamic based off arguments
        if self.env == "dev":
            self.base_url = self.LOCALHOST_URL
        else:
            # NOTE: update this when we are cloud-hosted
            self.base_url = self.SERVER_URL
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=1)
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def get_all_internships(self):
        """Retrieve all internships."""

        LOG.info("Retrieving internships...")
        resp = self.session.get(self.base_url + "/internships/")
        if resp.ok:
            data = resp.json()
            return [InternshipBase(**iship) for iship in data]
        return []
