from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application import Application
from models.internship import Internship
import appvars


class Controller:
    """Implements the Controller in the MVC (Model View Controller)
    pattern.
    """

    def __init__(self, model: Application):
        self.model = model

    def show_internship_detail(self, internship: Internship):
        self.model.setvar(appvars.INTERNSHIP_COMPANY, internship.company)
        self.model.setvar(appvars.INTERNSHIP_TITLE, internship.title)
        self.model.setvar(appvars.INTERNSHIP_YEAR, internship.year)
        self.model.setvar(appvars.INTERNSHIP_PERIOD, internship.period)
        self.model.setvar(appvars.INTERNSHIP_LINK, internship.link)
