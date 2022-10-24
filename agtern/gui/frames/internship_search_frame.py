from textwrap import fill
import tkinter as tk
from ...models import Internship
from ...logger import LOG

class InternshipSearchFrame(tk.Frame):
    """A Frame containing search bar, sort option, and various filters"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.PAD_OPTIONS = {'padx': 4, 'pady': 4}
        
        # 1 setup items!
        ## 1.1 we got our client-side filters ...
        self.searchInput = tk.StringVar() #represents current input
        self._search_input = tk.Entry(self,textvariable=self.searchInput) #text box, updates searchInput
        self._search_button = tk.Button(self, text="SRCH", command=self._onclick_search_button) #the button.
        self.SORT_OPTIONS = ('Alphabetical ⬇️', 'Alphabetical ⬆️', 'Date ⬇️', 'Date ⬆️')
        self.sortInput = tk.StringVar(value=self.SORT_OPTIONS[0]) #string of chosen sort option, defaulted
        self._sortby = tk.OptionMenu(self, self.sortInput, *self.SORT_OPTIONS, command=self._onselect_sort_input) #updates sortInput

        ## 1.2 ... and our server-side filters!

        # 2 now display them!
        self._search_input.grid(row=0, column=0, **self.PAD_OPTIONS)
        self._search_button.grid(row=0, column=1, **self.PAD_OPTIONS)
        self._sortby.grid(row=1, columnspan=2, sticky='EW', **self.PAD_OPTIONS)

    def _onclick_search_button(self):
        """called when self._search_button is clicked"""
        print('You clicked the search button, searching:', self.searchInput.get())
    
    def _onselect_sort_input(self, sortInput: str):
        """called when self._sortby is updated"""
        print('You selected the sort option:', sortInput)