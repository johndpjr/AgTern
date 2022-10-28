import tkinter as tk
from datetime import datetime
from tkinter import ttk

from ....common import LOG
from ...styles import *


class SettingsFrame(tk.Frame):
    """A frame containing profile details and validation."""

    WINDOW_SIZE_OPTIONS = [
        "1280x720",
        "1920x1080",
    ]

    MAJOR_OPTIONS = [
        "Aerospace Engineering",
        "Biological and Agricultural Engineering",
        "Biomedical Engineering",
        "Chemical Engineering",
        "Civil and Environmental Engineering",
        "Computer Science and Engineering",
        "Electrical and Computer Engineering",
        "Engineering Technology and Industrial Distribution",
        "Industrial and Systems Engineering",
        "Materials Science and Engineering",
        "Mechanical Engineering",
        "Multidisciplinary Engineering",
        "Nuclear Engineering",
        "Ocean Engineering",
        "Petroleum Engineering",
    ]

    GRAD_YEAR_OPTIONS = [datetime.now().year + i for i in range(4, -3, -1)]

    GRAD_MONTH_OPTIONS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            background=HIGHLIGHT, highlightthickness=2, highlightbackground=BORDER
        )

        # Variables that the parent (and thus all children)
        #   have access to

        self._var_win_size = tk.StringVar(value="1280x720")
        self._var_name = tk.StringVar(value="Enter here.")
        self._var_major = tk.StringVar(value="Computer Science and Engineering")
        self._var_grad_year = tk.StringVar(value=datetime.now().year)
        self._var_grad_month = tk.StringVar(value="January")
        self._var_error_msg = tk.StringVar()

        # Set default OptionMenu values if a config exists
        if self.master.config["StudentProfile"]["name"]:
            self._var_win_size.set(
                f'{self.master.config["AgTern"]["window_width"]}x{self.master.config["AgTern"]["window_height"]}'
            )
            self._var_name.set(self.master.config["StudentProfile"]["name"])
            self._var_major.set(self.master.config["StudentProfile"]["major"])
            self._var_grad_year.set(
                self.master.config["StudentProfile"]["graduation_year"]
            )
            self._var_grad_month.set(
                self.master.config["StudentProfile"]["graduation_month"]
            )

        self._option_window_size = ttk.OptionMenu(
            self,
            self._var_win_size,
            self._var_win_size.get(),
            *self.WINDOW_SIZE_OPTIONS,
        )
        self._entry_name = ttk.Entry(
            self,
            textvariable=self._var_name,
        )
        self._option_major = ttk.OptionMenu(
            self,
            self._var_major,
            self._var_major.get(),
            *self.MAJOR_OPTIONS,
        )
        self._option_grad_year = ttk.OptionMenu(
            self,
            self._var_grad_year,
            self._var_grad_year.get(),
            *self.GRAD_YEAR_OPTIONS,
        )
        self._option_grad_month = ttk.OptionMenu(
            self,
            self._var_grad_month,
            self._var_grad_month.get(),
            *self.GRAD_MONTH_OPTIONS,
        )
        self._lbl_error_msg = ttk.Label(
            self, textvariable=self._var_error_msg, style="Settings.TLabel"
        )
        self._bttn_save_profile = ttk.Button(
            self,
            text="Save Profile Information",
            command=self._on_save_profile_bttn_click,
            style="White.TButton",
        )

        # Display window information (currently hand-picked options)
        ttk.Label(self, text="Window Information:", style="Settings.TLabel").grid(
            row=0, column=0, sticky=tk.E, padx=(0, 60), pady=15
        )

        labels = [
            ttk.Label(self, text=label, style="Settings.TLabel") for label in ["Size"]
        ]
        values = [self._option_window_size]

        for i in range(len(labels)):
            labels[i].grid(row=i + 1, column=0, sticky=tk.E, padx=(0, 30), pady=(0, 2))
            values[i].grid(
                row=i + 1, column=1, sticky=tk.NSEW, padx=(0, 3), pady=(0, 2)
            )
            if values[i].__class__ == ttk.OptionMenu:
                values[i]["menu"].config(bg=BACKGROUND)

        # Display user information (name can be set, all others are hand-picked options)
        ttk.Label(self, text="Profile Information:", style="Settings.TLabel").grid(
            row=2, column=0, sticky=tk.E, padx=(0, 60), pady=15
        )

        labels = [
            ttk.Label(self, text=label, style="Settings.TLabel")
            for label in ["Name", "Major", "Graduation Year", "Graduation Month"]
        ]
        values = [
            self._entry_name,
            self._option_major,
            self._option_grad_year,
            self._option_grad_month,
        ]

        for i in range(len(labels)):
            labels[i].grid(row=i + 3, column=0, sticky=tk.E, padx=(0, 30), pady=(0, 2))
            values[i].grid(
                row=i + 3, column=1, sticky=tk.NSEW, padx=(0, 3), pady=(0, 2)
            )
            if values[i].__class__ == ttk.OptionMenu:
                values[i]["menu"].config(bg=BACKGROUND)

        # Display error message and button to write information to config

        self._lbl_error_msg.grid(
            row=8, column=0, sticky=tk.E, padx=(0, 30), pady=(0, 2)
        )
        self._bttn_save_profile.grid(
            row=8, column=1, sticky=tk.NSEW, padx=(0, 3), pady=30
        )

        # Configure column and row weights (rows are all the same weight)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        for r in range(9):
            self.grid_rowconfigure(r, weight=1)

    def _on_save_profile_bttn_click(self):
        """Responds to the event when the 'Save Profile Information'
        button is clicked.
        """
        LOG.info('"Save Profile Information" was clicked')

        # Validate user-entered values
        if self._var_name.get() == "":
            self._var_error_msg.set("Name cannot be empty.")
        else:
            # Set config values
            winw, winh = self._var_win_size.get().split("x")
            self.master.config.read_dict(
                {
                    "AgTern": {
                        "window_width": winw,
                        "window_height": winh,
                    },
                    "StudentProfile": {
                        "name": self._var_name.get(),
                        "major": self._var_major.get(),
                        "graduation_year": self._var_grad_year.get(),
                        "graduation_month": self._var_grad_month.get(),
                    },
                }
            )

            # Write config values to file and notify user
            with open(self.master.dfile_config.path, "w") as configfile:
                self.master.config.write(configfile)

            # Resize window
            self.master.set_window_size()

            self._var_error_msg.set("Done!")
