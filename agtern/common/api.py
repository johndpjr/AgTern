import requests

from .schemas import InternshipBase
from .logger import LOG


class AgTernAPI:
    """Wrapper for all communication to AgTern's services."""
    env = "dev"

    def __init__(self):
        if self.env == "dev":
            self.base_url = "http://127.0.0.1:5000"
        else:
            # TODO: update this when we are cloud-hosted
            self.base_url = "http://our-public-agtern-api.com"

    def get_all_internships(self):
        """Retrieve all internships."""

        LOG.info("Retrieving internships...")
        resp = requests.get(self.base_url + "/internships/")
        if resp.ok:
            data = resp.json()
            LOG.info(data)
            return [InternshipBase(**iship) for iship in data]
        return []
