"""Pre-MVP: This file calls functions in agtern.backend.server to retrieve data.
Post-MVP: This file will provide functions that will query the AgTern web server."""

from typing import List

from .models import Internship
from ..server import get_all_internships


def api_get_all_internships() -> List[Internship]:
    return get_all_internships()
