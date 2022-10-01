import tkinter as tk
import webbrowser

import appvars


class InternshipDetailFrame(tk.Frame):
    """A frame containing all specific internship details."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a LabelFrame (a container for labels) to contain
        #   basic internship details like Company, Title, and Year & Period
        self._lblfrm_internship_details = tk.LabelFrame(
            self,
            text='Internship details'
        )
        # Company (e.g. Google)
        self._lbl_internship_company = tk.Label(
            self._lblfrm_internship_details,
            textvariable=tk.StringVar(parent, name=appvars.INTERNSHIP_COMPANY)
        )
        # Title (e.g. Software Engineering Intern)
        self._lbl_internship_title = tk.Label(
            self._lblfrm_internship_details,
            textvariable=tk.StringVar(parent, name=appvars.INTERNSHIP_TITLE)
        )
        # Container for Period and Year (e.g. Summer 2023)
        self._frm_internship_period_year = tk.Frame(
            self._lblfrm_internship_details
        )
        # Period (e.g. Summer)
        self._lbl_internship_period = tk.Label(
            self._frm_internship_period_year,
            textvariable=tk.StringVar(parent, name=appvars.INTERNSHIP_PERIOD)
        )
        # Year (e.g. 2023)
        self._lbl_internship_year = tk.Label(
            self._frm_internship_period_year,
            textvariable=tk.StringVar(parent, name=appvars.INTERNSHIP_YEAR)
        )
        
        # "Apply now" button
        self._var_internship_link = tk.StringVar(parent, name=appvars.INTERNSHIP_LINK)
        self._bttn_apply_now = tk.Button(
            self,
            text='Apply now',
            command=self._on_apply_now_bttn_click
        )

        # Description (e.g. "At Lockheed Martin we are...")
        self._var_internship_txtbox = tk.StringVar(self)
        self._txtbx_internship_description = tk.Text(
            self,
            wrap=tk.WORD,
            state=tk.DISABLED
        )

        self._lblfrm_internship_details.grid(row=0, sticky=tk.EW)
        self._lbl_internship_company.grid(row=0, sticky=tk.W)
        self._lbl_internship_title.grid(row=1, sticky=tk.W)
        self._frm_internship_period_year.grid(row=2, sticky=tk.W)
        self._lbl_internship_period.pack(side=tk.LEFT)
        self._lbl_internship_year.pack(side=tk.LEFT)

        self._bttn_apply_now.grid(row=1, sticky=tk.W, pady=3)

        self._txtbx_internship_description.grid(row=2, sticky=tk.NSEW)

        self.grid_rowconfigure(2, weight=1)     # allow row 2 to expand vertically
        self.grid_columnconfigure(0, weight=1)  # allow column 0 to expand horizontally
    
    def _on_apply_now_bttn_click(self):
        """Open url of internship when the "Apply now"
        button is clicked."""

        link = self.getvar(appvars.INTERNSHIP_LINK)
        print(f'"Apply now" was clicked and the link is {link}')
        if link:  # Ensure not empty 
            webbrowser.open_new_tab(link)
