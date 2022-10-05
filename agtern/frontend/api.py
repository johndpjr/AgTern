
"""Pre-MVP: This file calls functions in agtern.backend.server to retrieve data.
Post-MVP: This file will provide functions that will query the AgTern web server."""

import agtern.backend as backend


def get_all_internships():
    return backend.get_all_internships()
