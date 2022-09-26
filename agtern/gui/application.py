import tkinter as tk
import tkinter.ttk as ttk
import configparser

from gui.frames.top_bar_frame import TopBarFrame
from gui.frames.internship_list_frame import InternshipListFrame
from gui.frames.internship_detail_frame import InternshipDetailFrame
from gui.frames.profile_frame import ProfileFrame


class Application(tk.Tk):
    """GUI for AgTern."""

    def __init__(self):
        super().__init__()

        self.title('AgTern')
        self.geometry('640x480')

        # Initialize config parser
        self._config_parser = configparser.ConfigParser(allow_no_value=True)
        self._config_parser.read("agtern/config.ini")

        # Create global frames
        self.frm_top_bar = TopBarFrame(self, relief=tk.RAISED, bd=2)

        # Pack TopBarFrame at the top and fill the frame in the X direction
        self.frm_top_bar.pack(side=tk.TOP, fill=tk.X, pady=(0,3))

        # Send user to profile if config.ini not set
        # Otherwise go to internship search 
        if not self._config_parser['AgTern']['window_width']:
            self.view_profile()
        else:
            self.view_search()

    def view_profile(self):
        
        # Clear previous view frames
        self.view_clear()

        # Create profile view frames
        self.frm_profile_detail = ProfileFrame(self)

        self.frm_profile_detail.pack(side=tk.TOP, fill=tk.BOTH, padx=(0,3), pady=3)


    def view_search(self):
        # Restrict access to internship search before config creation
        if not self._config_parser['AgTern']['window_width']:
            return
        
        # Clear previous view frames
        self.view_clear()

        # Create search view frames
        self.frm_internship_list = InternshipListFrame(self)
        self.frm_internship_detail = InternshipDetailFrame(self)

        # Pack InternshipListFrame on the left and fill the frame
        #   in both directions
        self.frm_internship_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=(3,0), pady=3)
        # Add a Separator widget to divide the previous and next frames
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=3)
        # Pack InternshipDetailFrame on the right side and fill the frame
        #   in both directions
        self.frm_internship_detail.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,3), pady=3)

    def view_clear(self):
        # Unpack all current widgets except for top bar
        for widget in self.pack_slaves():
            if self.frm_top_bar is not widget:
                widget.pack_forget()