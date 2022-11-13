import requests
from pydantic import ValidationError
from requests.adapters import HTTPAdapter, Retry

from .logger import LOG
from .models import Internship
from .schemas import InternshipCreateSchema


class AgTernAPI:
    """Wrapper for all communication to AgTern's services."""

    env = "dev"
    LOCALHOST_URL = "http://127.0.0.1:5000/api"
    SERVER_URL = "http://our-public-agtern-api.com/api"

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
            return [Internship(**iship) for iship in data]
        return []

    def create_internship(self, internship: InternshipCreateSchema):
        """Create an internship."""

        LOG.info("Creating internship...")
        resp = self.session.post(
            self.base_url + "/internships/", data=internship.json()
        )
        if resp.ok:
            data = resp.json()
            try:
                return Internship(**data)
            except ValidationError as errors:
                LOG.error("Unable to create internship!")
                LOG.error(errors)
        return None
