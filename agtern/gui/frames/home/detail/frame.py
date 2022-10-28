import tkinter as tk
import tkinter.ttk as ttk

from .....common import Internship
from ....styles import *
from .card import InternshipDetailCard


class InternshipDetailFrame(tk.Frame):
    """A frame containing all specific internship details."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(background=BACKGROUND)

        self._card_iship_details = InternshipDetailCard(self)

        # "Apply now" button
        self._var_iship_link = tk.StringVar()

        # Description (e.g. "At Lockheed Martin we are...")
        self._var_iship_txtbox = tk.StringVar(self)
        self._txtbx_iship_description = tk.Text(
            self,
            wrap=tk.WORD,
            state=tk.DISABLED,
            highlightthickness=1,
            highlightbackground=BORDER,
        )

        self._txtbx_iship_description.grid(row=1, sticky=tk.NSEW)

        self.grid_rowconfigure(0, weight=1, uniform="detailframe")
        self.grid_rowconfigure(1, weight=2, uniform="detailframe")
        self.grid_columnconfigure(0, weight=1)

    def show_internship_detail(self, iship: Internship):
        """Sets all of the internship detail variables to whatever
        internship was clicked."""
        self._card_iship_details.grid(row=0, sticky=tk.NSEW)
        self._card_iship_details.show_internship_detail(iship)
        self._var_iship_link.set(iship.link)
