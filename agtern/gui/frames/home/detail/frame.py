import tkinter as tk

from agtern.common import Internship
from agtern.gui.styles import *

from .card import InternshipDetailCard


class InternshipDetailFrame(tk.Frame):
    """A frame containing all specific internship details."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(background=BACKGROUND)

        self._card_iship_details = InternshipDetailCard(self)

        # Stores the value of the current internship link
        self._var_iship_link = tk.StringVar()

        # Textbox storing internship description
        self._txtbx_iship_description = tk.Text(
            self,
            wrap=tk.WORD,
            state=tk.DISABLED,
            highlightthickness=1,
            highlightbackground=BORDER,
        )

        self.grid_rowconfigure(0, weight=1, uniform="detailframe")
        self.grid_rowconfigure(1, weight=2, uniform="detailframe")
        self.grid_columnconfigure(0, weight=1)

    def show_internship_detail(self, iship: Internship):
        """Sets all of the internship detail variables to whatever
        internship was clicked."""
        if not self._card_iship_details.grid_info():
            self._card_iship_details.grid(row=0, sticky=tk.NSEW)
        if not self._txtbx_iship_description.grid_info():
            self._txtbx_iship_description.grid(row=1, sticky=tk.NSEW)

        self._card_iship_details.show_internship_detail(iship)
        self._insert_description(iship.description)
        self._var_iship_link.set(iship.link)

    def _insert_description(self, description: str):
        """Clears the internship description textbox, inserts the description,
        and disables the textbox from modification."""
        self._txtbx_iship_description.config(state=tk.NORMAL)
        self._txtbx_iship_description.delete(1.0, tk.END)
        self._txtbx_iship_description.insert(tk.END, description)
        self._txtbx_iship_description.config(state=tk.DISABLED)
