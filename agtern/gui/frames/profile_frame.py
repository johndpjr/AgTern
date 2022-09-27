import tkinter as tk
from datetime import datetime


class ProfileFrame(tk.Frame):
    """A frame containing profile details and validation."""

    WINDOW_SIZE_OPTIONS = [
        '640x480',
        '1280x720',
        '1920x1080',
    ]
    
    MAJOR_OPTIONS = [
        'Aerospace Engineering',
        'Biological and Agricultural Engineering',
        'Biomedical Engineering',
        'Chemical Engineering',
        'Civil and Environmental Engineering',
        'Computer Science and Engineering',
        'Electrical and Computer Engineering',
        'Engineering Technology and Industrial Distribution',
        'Industrial and Systems Engineering',
        'Materials Science and Engineering',
        'Mechanical Engineering',
        'Multidisciplinary Engineering',
        'Nuclear Engineering',
        'Ocean Engineering',
        'Petroleum Engineering',
    ]

    GRAD_YEAR_OPTIONS = [
        datetime.now().year + i
        for i in range(4, -3, -1)
    ]

    GRAD_MONTH_OPTIONS = [
        'January', 
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July',
        'August', 
        'September', 
        'October', 
        'November', 
        'December',
    ]
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Variables that the parent (and thus all children)
        #   have access to
        self._var_window_size = tk.StringVar(parent)
        self._var_name = tk.StringVar(parent)
        self._var_major = tk.StringVar(parent)
        self._var_grad_year = tk.StringVar(parent)
        self._var_grad_month = tk.StringVar(parent)
        self._var_error_message = tk.StringVar(parent)

        # Set default OptionMenu values
        if not self.master._config_parser['StudentProfile']['name']:
            self._var_window_size.set('640x480')
            self._var_name.set('Enter here.')
            self._var_major.set('Computer Science and Engineering')
            self._var_grad_year.set(datetime.now().year)
            self._var_grad_month.set('January')
        else:
            self._var_window_size.set(f'{self.master._config_parser["AgTern"]["window_width"]}x{self.master._config_parser["AgTern"]["window_height"]}')
            self._var_name.set(self.master._config_parser['StudentProfile']['name'])
            self._var_major.set(self.master._config_parser['StudentProfile']['major'])
            self._var_grad_year.set(self.master._config_parser['StudentProfile']['graduation_year'])
            self._var_grad_month.set(self.master._config_parser['StudentProfile']['graduation_month'])
        self._var_error_message.set('')

        self._option_window_size = tk.OptionMenu(
            self,
            self._var_window_size,
            *self.WINDOW_SIZE_OPTIONS,
        )
        self._entry_name = tk.Entry(
            self,
            textvariable=self._var_name,
        )
        self._option_major = tk.OptionMenu(
            self,
            self._var_major,
            *self.MAJOR_OPTIONS,
        )
        self._option_grad_year = tk.OptionMenu(
            self,
            self._var_grad_year,
            *self.GRAD_YEAR_OPTIONS,
        )
        self._option_grad_month = tk.OptionMenu(
            self,
            self._var_grad_month,
            *self.GRAD_MONTH_OPTIONS,
        )
        self._label_error_message = tk.Label(
            self,
            textvariable=self._var_error_message,
        )
        self._bttn_save_profile = tk.Button(
            self,
            text='Save Profile Information',
            command=self._on_save_profile_bttn_click
        )

        # Display window information (currently hand-picked options)
        tk.Label(self, text='Window Information:').grid(row=0, column=0, sticky=tk.E, padx=(0,60), pady=15)

        labels = [tk.Label(self, text=label) for label in ['Size']]
        values = [self._option_window_size]

        for i in range(len(labels)):
            labels[i].grid(row=i+1, column=0, sticky=tk.E, padx=(0,30), pady=(0,2))
            values[i].grid(row=i+1, column=1, sticky=tk.NSEW, padx=(0,3), pady=(0,2))

        # Display user information (name can be set, all others are hand-picked options)
        tk.Label(self, text='Profile Information:').grid(row=2, column=0, sticky=tk.E, padx=(0,60), pady=15)

        labels = [tk.Label(self, text=label) for label in ['Name', 'Major', 'Graduation Year', 'Graduation Month']]
        values = [self._entry_name, self._option_major, self._option_grad_year, self._option_grad_month]

        for i in range(len(labels)):
            labels[i].grid(row=i+3, column=0, sticky=tk.E, padx=(0,30), pady=(0,2))
            values[i].grid(row=i+3, column=1, sticky=tk.NSEW, padx=(0,3), pady=(0,2))

        # Display error message and button to write information to config
        self._label_error_message.grid(row=8, column=0, sticky=tk.E, padx=(0,30), pady=(0,2))
        self._bttn_save_profile.grid(row=8, column=1, sticky=tk.NSEW, padx=(0,3), pady=30)
        
        # Configure column and row weights (rows are all the same weight)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        for r in range(9):
            self.grid_rowconfigure(r, weight=1)

    def _on_save_profile_bttn_click(self):
        """Responds to the event when the 'Save Profile Information'
        button is clicked.
        """
        print('"Save Profile Information" was clicked')

        # Validate user-entered values
        if self._var_name.get() == '':
            self._var_error_message.set('Name cannot be empty.')
        else:
            # Set config values
            self.master._config_parser.read_dict({
                'AgTern': {
                    'window_width': self._var_window_size.get().split('x')[0],
                    'window_height': self._var_window_size.get().split('x')[1],
                },
                'StudentProfile': {
                    'name': self._var_name.get(),
                    'major': self._var_major.get(),
                    'graduation_year': self._var_grad_year.get(),
                    'graduation_month': self._var_grad_month.get(),
                }
            })

            # Write config values to file and notify user
            with open('agtern/config.ini', 'w') as configfile:
                self.master._config_parser.write(configfile)

            # Resize window
            self.master.set_window_size()
            self._var_error_message.set('Done!')
            