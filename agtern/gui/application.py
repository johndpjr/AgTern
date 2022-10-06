import tkinter as tk
import tkinter.ttk as ttk
import configparser

from .frames.top_bar_frame import TopBarFrame
from .frames.internship_list_frame import InternshipListFrame
from .frames.internship_detail_frame import InternshipDetailFrame
from .frames.profile_frame import ProfileFrame
from ..data import DataFile

class Application(tk.Tk):
    """GUI for AgTern."""

    def __init__(self):
        super().__init__()

        # Initialize config parser
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.dfile_config = DataFile( "config.ini" )
        self.config.read( self.dfile_config.path )

        self.title('AgTern')
        self.set_window_size()

        # Create global frames
        self.frm_top_bar = TopBarFrame(self, relief=tk.RAISED, bd=2)
        self.frm_profile_detail = ProfileFrame(self)
        self.frm_internship_list = InternshipListFrame(self)
        self._separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.frm_internship_detail = InternshipDetailFrame(self)

        # Pack TopBarFrame at the top and fill the frame in the X direction
        self.frm_top_bar.pack(side=tk.TOP, fill=tk.X, pady=(0,3))

        # Send user to profile if config.ini not set
        # Otherwise go to internship search 
        if not self.config['StudentProfile']['name']:
            self.view_profile()
        else:
            self.view_search()

    def view_profile(self):
        """Show the My Profile view, where window and profile information
        can be modified."""
        # Clear previous view frames
        self.view_clear()

        self.frm_profile_detail.pack(side=tk.TOP, fill=tk.BOTH, padx=(0,3), pady=3)

    def view_search(self):
        """Display InternshipListFrame and InternshipDetailFrame."""
        # Restrict access to internship search before config creation
        if not self.config['StudentProfile']['name']:
            return
        
        # Clear previous view frames
        self.view_clear()

        # Pack InternshipListFrame on the left and fill the frame
        #   in both directions
        self.frm_internship_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=(3,0), pady=3)
        # Add a Separator widget to divide the previous and next frames
        self._separator.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=3)
        # Pack InternshipDetailFrame on the right side and fill the frame
        #   in both directions
        self.frm_internship_detail.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,3), pady=3)

    def view_clear(self):
        # Unpack all current widgets except for top bar
        for widget in self.pack_slaves():
            if self.frm_top_bar is not widget:
                widget.pack_forget()

    def set_window_size(self):
        # Set geometry to size stored in config file
        win_w = self.config['AgTern']['window_width']
        win_h = self.config['AgTern']['window_height']
        self.geometry(f'{win_w}x{win_h}')
