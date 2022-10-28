import configparser
import tkinter as tk
import tkinter.ttk as ttk

from ..common import DataFile
from .frames import HomeFrame, SettingsFrame, TopBarFrame
from .styles import *


class Application(tk.Tk):
    """GUI for AgTern."""

    def __init__(self):
        super().__init__()

        # Initialize config parser
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.dfile_config = DataFile("config.ini")
        self.config.read(self.dfile_config.path)

        self.title("AgTern")
        self.set_window_size()

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(background=BACKGROUND)
        set_styles(self.style)

        # Create global frames
        self.frm_top_bar = TopBarFrame(self, relief=tk.RAISED, bd=2)
        self.frm_body = HomeFrame(self)
        self.frm_settings = SettingsFrame(self)

        # Pack TopBarFrame at the top and fill the frame in the X direction
        self.frm_top_bar.place_configure(relx=0, rely=0, relwidth=1, relheight=0.075)
        self.frm_body.place_configure(relx=0, rely=0.075, relwidth=1, relheight=0.925)

    def view_settings(self):
        """Show the My Profile view, where window and profile information
        can be modified."""
        self.frm_settings.place_configure(
            relx=0.025, rely=0.09, relwidth=0.4, relheight=0.5
        )

    def remove_settings(self):
        """Remove the My Profile view, where window and profile information
        can be modified."""
        self.frm_settings.place_forget()

    def view_clear(self):
        # Unpack all current widgets except for top bar
        for widget in self.place_slaves():
            if self.frm_top_bar is not widget:
                widget.place_forget()

    def set_window_size(self):
        # Set geometry to size stored in config file
        win_w = self.config["AgTern"]["window_width"]
        win_h = self.config["AgTern"]["window_height"]
        self.geometry(f"{win_w}x{win_h}")
