from textwrap import fill
import tkinter as tk
import tkinter.ttk as ttk
from ...models import Internship
from ...logger import LOG

from .profile_frame import ProfileFrame

# A dict, keyed by association
class DoubleDict(dict):
    def __init__(self, initDict: dict = {}):
        super().__init__()
        for key, value in initDict.items():
            self.__setitem__(key, value)
    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        super().__setitem__(value, key)
    def __delitem__(self, key) -> None:
        del self[self[key]]
        del self[key]

class InternshipSearchFrame(tk.Frame):
    """A Frame containing search bar, sort option, and various filters"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        #constants
        self.PAD_OPTIONS = {'padx': 4, 'pady': 4}
        self.SORT_OPTIONS = ('Alphabetical ⬇️', 'Alphabetical ⬆️', 'Date ⬇️', 'Date ⬆️')
        self.MAJOR_OPTIONS = ProfileFrame.MAJOR_OPTIONS
        self.SEMESTER_OPTIONS = ('Spring', 'Summer', 'Fall')
        self.SEMESTER_CONVERT = DoubleDict({'Spring':0, 'Summer':1, 'Fall':2})
        self.YEAR_OPTIONS = tuple(range(2022, 2031))
        
        # 1 setup items!
        # 1.1 Give search bar a frame of its own...
        self._frame_search = tk.Frame(self)
        self.searchInput = tk.StringVar() #represents current input
        self._search_input = ttk.Entry(self._frame_search, textvariable=self.searchInput, width=25) #text box, updates searchInput
        self.search_icon = tk.PhotoImage(file='agtern/gui/assets/search-icon.png').subsample(3,3) #search button image
        self._search_button = ttk.Button(self._frame_search, image=self.search_icon, command=self._onclick_search) #the actual button
        # 1.2 Sort?
        self.sortInput = tk.StringVar()
        self._sortby = ttk.OptionMenu(self, self.sortInput, self.SORT_OPTIONS[0], *self.SORT_OPTIONS, command=self._onselect_sort)
        # 1.3 Separator/Labels
        self._line = ttk.Separator(self)
        self._label_filter = tk.Label(self, text='Filters', anchor=tk.W) #text
        # 1.4 Major?
        self.majorInput = tk.StringVar()
        self._major = ttk.OptionMenu(self, self.majorInput, self.MAJOR_OPTIONS[5], *self.MAJOR_OPTIONS, command=self._onselect_major)
        self._major.config(width=25)
        # 1.5 Semester?
        self.semesterInput = tk.StringVar()
        self._semester = ttk.OptionMenu(self, self.semesterInput, self.SEMESTER_OPTIONS[1], *self.SEMESTER_OPTIONS, command=self._onselect_semester)
        # 1.6 Year?
        self.yearInput = tk.StringVar()
        self._year = ttk.OptionMenu(self, self.yearInput, self.YEAR_OPTIONS[0], *self.YEAR_OPTIONS, command=self._onselect_year)
        # 1.7 Filter Button on the bottom
        self._filter_button = ttk.Button(self, text='Filter', command=self._onclick_filter)

        # 2 now display them!
        self._frame_search.grid(row=0)
        self._search_input.grid(row=0, column=0, stick='EW', padx=2, ipady=3)
        self._search_button.grid(row=0, column=1, **self.PAD_OPTIONS)
        self._search_button.focus()
        self._sortby.grid(row=1, columnspan=2, sticky='EW', **self.PAD_OPTIONS)
        self._line.grid(row=2, columnspan=2, sticky='EW', **self.PAD_OPTIONS)
        self._label_filter.grid(row=3, sticky='EW', **self.PAD_OPTIONS)
        self._major.grid(row=4, sticky='EW', **self.PAD_OPTIONS)
        self._semester.grid(row=5, sticky='EW', **self.PAD_OPTIONS)
        self._year.grid(row=6, stick='EW', **self.PAD_OPTIONS)
        self._filter_button.grid(row=7, sticky='EW', **self.PAD_OPTIONS)

    def _onclick_search(self):
        """called when self._search_button is clicked"""
        print(f'You wrote {self.searchInput.get()} and clicked the search button')
    
    def _onselect_sort(self, sortInput: str):
        """called when self._sortby is updated"""
        print(f'You selected to sort {sortInput}')

    def _onselect_major(self, majorInput: str):
        """called when self._major is updated"""
        print(f'You selected the major {majorInput}')

    def _onselect_semester(self, semesterInput: str):
        """called when self._semester is updated"""
        print(f'You selected the {semesterInput} semester')
    
    def _onselect_year(self, yearInput: str):
        """called when self._year is updated"""
        print(f'You selected year {yearInput}')
    
    def _onclick_filter(self):
        """called when self._filter_button is clicked
        Relevant information (StringVar):
        - self.majorInput
        - self.semesterInput
        - self.yearInput
        """
        print(f'You clicked the filter button! 🍀')