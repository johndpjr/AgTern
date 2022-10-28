import tkinter as tk
import tkinter.ttk as ttk

from ....common import LOG
from ...styles import *


class TopBarFrame(tk.Frame):
    """A persistent frame for common actions."""

    def __init__(self, parent, *args, **kwargs):
        # Initialize a Frame (since we inherit from tk.Frame)
        super().__init__(parent, *args, **kwargs)
        self.configure(background=HIGHLIGHT)
        self.PAD_OPTIONS = {"padx": 4, "pady": 4, "ipadx": 2, "ipady": 2}
        self.var_img = tk.PhotoImage(
            file="agtern/gui/assets/settings-icon.png"
        ).subsample(3, 3)
        self.settings_open = False

        # Create all widgets of this frame
        self._bttn_my_profile = ttk.Button(
            self,
            image=self.var_img,
            command=self._on_my_profile_bttn_click,
            padding="5 5 5 5",
            style="White.TButton",
        )

        # Pack all widgets into this frame
        self._bttn_my_profile.pack(side=tk.LEFT, anchor=tk.W, **self.PAD_OPTIONS)

    def _on_my_profile_bttn_click(self):
        """Responds to the event when the "My Profile" button is clicked."""
        LOG.info('"My Profile" was clicked')
        if not self.settings_open:
            self.master.view_settings()
        else:
            self.master.remove_settings()
        self.settings_open = not self.settings_open
