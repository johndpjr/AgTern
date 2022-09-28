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
            textvariable=tk.StringVar(parent, value='Company placeholder', name=appvars.INTERNSHIP_COMPANY)
        )
        # Title (e.g. Software Engineering Intern)
        self._lbl_internship_title = tk.Label(
            self._lblfrm_internship_details,
            textvariable=tk.StringVar(parent, value='Title placeholder', name=appvars.INTERNSHIP_TITLE)
        )
        # Year (e.g. 2023)
        self._var_internship_year = tk.IntVar(self, value=2023)
        self._lbl_internship_year = tk.Label(
            self._lblfrm_internship_details,
            textvariable=tk.StringVar(parent, value='Year placeholder', name=appvars.INTERNSHIP_YEAR)
        )
        # Period (e.g. Summer)
        self._lbl_internship_period = tk.Label(
            self._lblfrm_internship_details,
            textvariable=tk.StringVar(parent, value='Period placeholder', name=appvars.INTERNSHIP_PERIOD)
        )
        
        # "Apply now" button
        tk.StringVar(parent, name='internship.link')
        self._bttn_apply_now = tk.Button(
            self,
            text='Apply now',
            command=self._on_apply_now_bttn_click
        )

        # Description (e.g. "At Lockheed Martin we are...")
        self._var_internship_txtbox = tk.StringVar(self)
        self._txtbx_internship_description = tk.Text(
            self,
            wrap=tk.WORD
        )

        self._lblfrm_internship_details.grid(row=0, column=0, sticky=tk.EW)
        self._lbl_internship_company.pack(side=tk.TOP, anchor=tk.NW)
        self._lbl_internship_title.pack(side=tk.TOP, anchor=tk.NW)
        self._lbl_internship_year.pack(side=tk.TOP, anchor=tk.NW)
        self._lbl_internship_period.pack(side=tk.TOP, anchor=tk.NW)

        self._bttn_apply_now.grid(row=1, column=0, sticky=tk.W, pady=3)

        self._txtbx_internship_description.grid(row=2, column=0, sticky=tk.NSEW)

        self.grid_rowconfigure(2, weight=1)     # allow row 2 to expand vertically
        self.grid_columnconfigure(0, weight=1)  # allow column 0 to expand horizontally
    
    def _on_apply_now_bttn_click(self):
        """Open url of internship when the "Apply now"
        button is clicked."""

        print('"Apply now" was clicked and the link is ' \
              f'"{self.getvar("internship.link")}"')

        link = self.getvar('internship.link')
        if link:  # Ensure not empty 
            webbrowser.open_new_tab(link)
