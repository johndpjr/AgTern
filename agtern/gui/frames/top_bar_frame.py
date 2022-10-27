import tkinter as tk
import tkinter.ttk as ttk

from ...common import LOG


class TopBarFrame(tk.Frame):
    """A persistent frame for common actions."""

    def __init__(self, parent, *args, **kwargs):
        # Initialize a Frame (since we inherit from tk.Frame)
        super().__init__(parent, *args, **kwargs)
        self.PAD_OPTIONS = {"padx": 4, "pady": 4, "ipadx": 2, "ipady": 2}

        # Create all widgets of this frame
        self._bttn_my_profile = ttk.Button(
            self, text="My Profile", command=self._on_my_profile_bttn_click
        )
        self._bttn_search_internships = ttk.Button(
            self,
            text="Search Internships",
            command=self._on_search_internships_bttn_click,
        )

        # Pack all widgets into this frame
        self._bttn_my_profile.pack(side=tk.LEFT, anchor=tk.W, **self.PAD_OPTIONS)
        self._bttn_search_internships.pack(
            side=tk.RIGHT, anchor=tk.E, **self.PAD_OPTIONS
        )

    def _on_my_profile_bttn_click(self):
        """Responds to the event when the "My Profile" button is clicked."""
        LOG.info('"My Profile" was clicked')
        self.master.view_profile()

    def _on_search_internships_bttn_click(self):
        """Responds to the event when the "Search Internships"
        button is clicked.
        """
        LOG.info('"Search Internships" was clicked')
        self.master.view_search()
