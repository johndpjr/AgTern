import tkinter as tk

from .vertical_scrolled_frame import VerticalScrolledFrame


class InternshipListFrame(tk.Frame):
    """A frame containing all internship results, as well as
    a search and sort by feature.
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Special tkinter variable that is a type str
        self._var_search_result = tk.StringVar(self)
        # Setting the textvariable here binds the value of _var_search_result
        #   to whatever is currently in _entry_search
        self._entry_search = tk.Entry(
            self,
            textvariable=self._var_search_result,
        )
        self.photoimage = tk.PhotoImage(
            file='agtern/gui/assets/search-icon.png'
        ).subsample(3, 3)
        # self.photoimage = self.photo.subsample(3, 3)
        self._bttn_search = tk.Button(
            self,
            text='Search',
            image=self.photoimage,
            compound=tk.LEFT,
            command=self._on_search_bttn_click
        )
        # Contains the actual internships (uses a scrolled frame for overflow)
        self._frm_internship_list_container = VerticalScrolledFrame(self)

        self._entry_search.grid(row=0, column=0, sticky=tk.NS, pady=(0,2))
        self._bttn_search.grid(row=0, column=1, sticky=tk.NS, padx=(2,0), pady=(0,2))
        self._frm_internship_list_container.grid(
            row=1, column=0,
            columnspan=2, sticky=tk.NSEW,
        )
        # Let the internship container expand vertically
        self.grid_rowconfigure(1, weight=1)

        for i in range(20):
            tk.Button(
                self._frm_internship_list_container.interior,
                text='Some fake internship item'
            ).pack(side=tk.TOP, fill=tk.X, padx=(0,3))
    
    def _on_search_bttn_click(self):
        """Responds to the event when the "Search"
        button is clicked.
        """
        # You can get the value of what's in the search box by calling get()
        #   on its corresponding StringVar variable
        print('"Search" was clicked and the search is ' \
              f'"{self._var_search_result.get()}"')