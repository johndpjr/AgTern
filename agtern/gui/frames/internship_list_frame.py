import tkinter as tk

from ...models import Internship
from ...pipelines import api_get_all_internships
from .vertical_scrolled_frame import VerticalScrolledFrame


class InternshipListFrame(tk.Frame):
    """A frame containing all internship results, as well as
    a search and sort by feature.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

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
        self._bttn_search = tk.Button(
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

        internships = api_get_all_internships()

        for i in internships:
            text = f"{i.company}\n{i.title}"
            if i.period is not None or i.year is not None:
                text += f"\n{i.period} {i.year}"

            tk.Button(
                self._frm_iship_list_container.interior,
                text=text,
                command=lambda i=i: self._on_iship_list_item_bttn_click(i),
            ).pack(side=tk.TOP, fill=tk.X, padx=(0, 3))

    def _on_search_bttn_click(self):
        """Responds to the event when the "Search"
        button is clicked.
        """
        # You can get the value of what's in the search box by calling get()
        #   on its corresponding StringVar variable

        print(
            '"Search" was clicked and the search is '
            f'"{self._var_search_result.get()}"'
        )

    def _on_iship_list_item_bttn_click(self, iship: Internship):
        """Displays internship information in the InternshipDetailFrame."""
        self.master.frm_internship_detail.show_internship_detail(iship)
