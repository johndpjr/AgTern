from dataclasses import dataclass


# TODO: Refactor this dataclass into a pydantic Model or dataclass


@dataclass
class Internship:
    """Models internship details."""

    company: str
    title: str
    year: str
    period: str
    link: str
    location: str = ""
    description: str = ""
