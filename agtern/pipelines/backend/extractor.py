import re

from ...models import Internship


def update_internship(internship: Internship) -> Internship:
    """Extracts additional information from an internship title."""

    full_title = internship.title
    # Match everything before intern(ship)
    title = re.search('.+?(intern|internship)', full_title, re.IGNORECASE)
    if title is not None: internship.title = title.group(0)
    # Match a 4 digit year
    year = re.search('\d{4}', full_title)
    if year is not None: internship.year = int(year.group())
    # Match summer or spring
    period = re.search('summer|spring', full_title, re.IGNORECASE)
    if period is not None: internship.period = period.group()

    return internship
