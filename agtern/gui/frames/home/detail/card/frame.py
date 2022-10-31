import tkinter as tk
from tkinter import ttk

from ......common import Internship
from .....styles import *
from .apply_button import InternshipApplyButton


class InternshipDetailCard(tk.Frame):
    """A frame containing all specific internship details."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            width=700,
            height=250,
            bg=BACKGROUND,
            highlightthickness=1,
            highlightbackground=BORDER,
        )

        self._var_company = tk.StringVar()
        self._var_title = tk.StringVar()
        self._var_period = tk.StringVar()
        self._var_year = tk.StringVar()

        self._lbl_company = ttk.Label(
            self, textvariable=self._var_company, style="DetailFrame.TLabel"
        )
        self._lbl_title = ttk.Label(
            self, textvariable=self._var_title, style="DetailFrame.TLabel"
        )
        self._lbl_period = ttk.Label(
            self, textvariable=self._var_period, style="DetailFrame.TLabel"
        )
        self._lbl_year = ttk.Label(
            self, textvariable=self._var_year, style="DetailFrame.TLabel"
        )
        self._btn_apply = InternshipApplyButton(self)

        self._lbl_company.place_configure(
            relx=0.05, rely=0.05, relwidth=0.9, relheight=0.15
        )
        self._lbl_title.place_configure(
            relx=0.05, rely=0.2, relwidth=0.9, relheight=0.15
        )
        self._lbl_period.place_configure(
            relx=0.05, rely=0.35, relwidth=0.45, relheight=0.15
        )
        self._lbl_year.place_configure(
            relx=0.35, rely=0.35, relwidth=0.45, relheight=0.15
        )
        self._btn_apply.place_configure(
            relx=0.05, rely=0.6, relwidth=0.45, relheight=0.3
        )

    def show_internship_detail(self, iship: Internship):
        """Sets all of the internship detail variables to whatever
        internship was clicked."""

        self._var_company.set(iship.company)
        self._var_title.set(iship.title)
        self._var_period.set(iship.period)
        self._var_year.set(iship.year)
        self._btn_apply.set_apply_link(iship.link)
