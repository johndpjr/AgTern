import tkinter as tk
import webbrowser

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
        self._var_internship_company = tk.StringVar(self, value='Company placeholder')
        self._lbl_internship_company = tk.Label(
            self._lblfrm_internship_details,
            textvariable=self._var_internship_company
        )
        # Title (e.g. Software Engineering Intern)
        self._var_internship_title = tk.StringVar(self, value='Title placeholder')
        self._lbl_internship_title = tk.Label(
            self._lblfrm_internship_details,
            textvariable=self._var_internship_title
        )
        # Year (e.g. 2023)
        self._var_internship_year = tk.IntVar(self, value=2023)
        self._lbl_internship_year = tk.Label(
            self._lblfrm_internship_details,
            textvariable=self._var_internship_year
        )
        # Period (e.g. Summer)
        self._var_internship_period = tk.StringVar(self, value='Period placeholder')
        self._lbl_internship_period = tk.Label(
            self._lblfrm_internship_details,
            textvariable=self._var_internship_period
        )
        
        # "Apply now" button
        self._var_internship_link = tk.StringVar(self)
        self._bttn_apply_now = tk.Button(
            self,
            text='Apply now',
            command=self._on_apply_now_bttn_click
        )

        # Description (e.g. "At Lockheed Martin we are...")
        self._var_internship_txtbox = tk.StringVar(self)
        self._txtbx_internship_description = tk.Text(
            self,s
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
              f'"{self._var_internship_link.get()}"')

        link = self._var_internship_link.get()
        if link:  # Ensure not empty 
            webbrowser.open_new_tab(link)
