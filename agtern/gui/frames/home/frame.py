import configparser
import tkinter as tk
import tkinter.ttk as ttk

from .detail import InternshipDetailFrame
from .list import InternshipListFrame
from .search import InternshipSearchFrame


class HomeFrame(tk.Frame):
    """GUI for AgTern."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background="white")

        # Create global frames
        self.frm_internship_list = InternshipListFrame(self)
        self._separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.frm_internship_detail = InternshipDetailFrame(self)
        self.frm_internship_search = InternshipSearchFrame(self)

        self.frm_internship_search.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 3), pady=3)
        # Add a Separator widget to divide the previous and next frames
        self._separator.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=3)

        # Pack InternshipListFrame on the left and fill the frame
        #   in both directions
        self.frm_internship_list.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=3)
        # Pack InternshipDetailFrame on the right side and fill the frame
        #   in both directions
        self.frm_internship_detail.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 3), pady=3
        )
