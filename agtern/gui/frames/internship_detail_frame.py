import tkinter as tk
import webbrowser

from ...common import LOG, InternshipBase


class InternshipDetailFrame(tk.Frame):
    """A frame containing all specific internship details."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a LabelFrame (a container for labels) to contain
        #   basic internship details like Company, Title, and Year & Period
        self._lblfrm_iship_details = tk.LabelFrame(self, text="Internship details")
        # Company (e.g. Google)
        self._var_iship_company = tk.StringVar()
        self._lbl_iship_company = tk.Label(
            self._lblfrm_iship_details, textvariable=self._var_iship_company
        )
        # Title (e.g. Software Engineering Intern)
        self._var_iship_title = tk.StringVar()
        self._lbl_iship_title = tk.Label(
            self._lblfrm_iship_details, textvariable=self._var_iship_title
        )
        # Container for Period and Year (e.g. Summer 2023)
        self._frm_iship_period_year = tk.Frame(self._lblfrm_iship_details)
        # Period (e.g. Summer)
        self._var_iship_period = tk.StringVar()
        self._lbl_iship_period = tk.Label(
            self._frm_iship_period_year, textvariable=self._var_iship_period
        )
        # Year (e.g. 2023)
        self._var_iship_year = tk.StringVar()
        self._lbl_iship_year = tk.Label(
            self._frm_iship_period_year, textvariable=self._var_iship_year
        )

        # "Apply now" button
        self._var_iship_link = tk.StringVar()
        self._bttn_apply_now = tk.Button(
            self, text="Apply now", command=self._on_apply_now_bttn_click
        )

        # Description (e.g. "At Lockheed Martin we are...")
        self._var_iship_txtbox = tk.StringVar(self)
        self._txtbx_iship_description = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)

        self._lblfrm_iship_details.grid(row=0, sticky=tk.EW)
        self._lbl_iship_company.grid(row=0, sticky=tk.W)
        self._lbl_iship_title.grid(row=1, sticky=tk.W)
        self._frm_iship_period_year.grid(row=2, sticky=tk.W)
        self._lbl_iship_period.pack(side=tk.LEFT)
        self._lbl_iship_year.pack(side=tk.LEFT)

        self._bttn_apply_now.grid(row=1, sticky=tk.W, pady=3)

        self._txtbx_iship_description.grid(row=2, sticky=tk.NSEW)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_apply_now_bttn_click(self):
        """Open url of internship when the "Apply now"
        button is clicked."""

        link = self._var_iship_link.get()
        LOG.info(f'"Apply now" was clicked and the link is {link}')
        if link:  # Ensure not empty
            webbrowser.open_new_tab(link)

    def show_internship_detail(self, iship: InternshipBase):
        """Sets all of the internship detail variables to whatever
        internship was clicked."""

        self._var_iship_company.set(iship.company)
        self._var_iship_title.set(iship.title)
        self._var_iship_period.set(iship.period)
        self._var_iship_year.set(iship.year)
        self._var_iship_link.set(iship.link)
