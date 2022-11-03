import tkinter as tk
import tkinter.ttk as ttk

from .....common import LOG
from ..... import Internship
from ....styles import *
from .scrolled import InternshipEntryFrame, VerticalScrolledFrame


class InternshipListFrame(tk.Frame):
    """A frame containing all internship results"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background=BACKGROUND)

        self._var_search_result = tk.StringVar()
        self._entry_search = tk.Entry(
            self,
            textvariable=self._var_search_result
            # textvariable is special tkinter variable that binds
            # _var_search_result to the contents of this Entry widget
        )
        self.photoimage = tk.PhotoImage(
            file="agtern/gui/assets/search-icon.png"
        ).subsample(3, 3)
        self._bttn_search = ttk.Button(
            self,
            text="Search",
            image=self.photoimage,
            compound=tk.LEFT,
            command=self._on_search_bttn_click,
        )
        # Contains the actual internships (uses a scrolled frame for overflow)
        self._frm_iship_list_container = VerticalScrolledFrame(self)

        # Don't grid the search widgets since we won't implement them for MVP
        # self._entry_search.grid(row=0, column=0, sticky=tk.NS, pady=(0, 2))
        # self._bttn_search.grid(row=0, column=1, sticky=tk.NS, padx=(2, 0), pady=(0, 2))
        self._frm_iship_list_container.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW,
        )
        # Let the internship container expand vertically
        self.grid_rowconfigure(1, weight=1)

        self._populate_internships()

    def _populate_internships(self):
        # TODO: Access the frame 2 levels up more cleanly
        internships = self.master.master.api.get_all_internships()

        for i in internships:
            entry = InternshipEntryFrame(self._frm_iship_list_container.interior)
            entry.populate_entry(i)
            entry.pack(side=tk.TOP, fill=tk.X)

    def _on_search_bttn_click(self):
        """Responds to the event when the "Search"
        button is clicked.
        """
        # Get the contents of the search box by calling get()
        # on its corresponding StringVar variable

        LOG.info(
            '"Search" was clicked and the search is '
            f'"{self._var_search_result.get()}"'
        )

    def _on_iship_list_item_bttn_click(self, iship: Internship):
        """Displays internship information in the InternshipDetailFrame."""
        self.master.frm_internship_detail.show_internship_detail(iship)
