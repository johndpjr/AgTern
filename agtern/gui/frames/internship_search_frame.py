import tkinter as tk
from ...models import Internship
from ...logger import LOG

class InternshipSearchFrame(tk.Frame):
    """A Frame containing search bar, sort option, and various filters"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        #setup items!
        ##we got our client-side filters ...
        self.searchInput = tk.StringVar() #string that updates with the search input
        self._search_input = tk.Entry(self,textvariable=self.searchInput) #entry box, updates searchInput
        self._search_button = tk.Button(self, text="SRCH")

        ##... and our server-side filters!

        #now display them!
        self._search_input.grid(row=0, column=0)
        self._search_button.grid(row=0, column=1)

    def _onclick_search_button():
        """called when the search button is clicked.
        self.searchInput -> the entered keywords"""
        pass