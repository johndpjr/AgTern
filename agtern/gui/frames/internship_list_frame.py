import tkinter as tk

from ...models import Internship
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
            # textvariable is special tkinter variable of type str
            # Setting the textvariable here binds the value of search_result
            #   to whatever is currently in _entry_search
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

        self._entry_search.grid(row=0, column=0, sticky=tk.NS, pady=(0, 2))
        self._bttn_search.grid(row=0, column=1, sticky=tk.NS, padx=(2, 0), pady=(0, 2))
        self._frm_iship_list_container.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW,
        )
        # Let the internship container expand vertically
        self.grid_rowconfigure(1, weight=1)

        internships = [
            Internship(
                "Google",
                "Software Engineering Intern",
                2023,
                "Summer",
                "https://careers.google.com/jobs/results/80503484702433990-software-engineering-intern-summer-2023/",
            ),
            Internship(
                "BNSF",
                "Technology Services Intern",
                2023,
                "Summer",
                "https://jobs.bnsf.com/job/Fort-Worth-Technology-Services-Summer-Intern-2023-%28Paid%29-%28Fort-Worth%2C-TX%29-TX-76131/931724600/",
            ),
            Internship(
                "FBI",
                "FBI Honors Internship Program",
                2023,
                "Summer",
                "https://www.fbi.gov/contact-us/field-offices/neworleans/news/press-releases/fbi-honors-internship-program",
            ),
            Internship(
                "Dell",
                "Software Engineer Intern",
                2023,
                "Summer",
                "https://jobs.dell.com/internships",
            ),
            Internship(
                "Apple",
                "App Developer Intern",
                2023,
                "Summer",
                "https://www.apple.com/careers/us/students.html",
            ),
        ]

        for i in internships:
            tk.Button(
                self._frm_iship_list_container.interior,
                text=f"{i.company}\n{i.title}\n{i.period} {i.year}",
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
