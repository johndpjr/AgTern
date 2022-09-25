import tkinter as tk


class TopBarFrame(tk.Frame):
    """A persistent frame for common actions."""
    
    def __init__(self, parent, *args, **kwargs):
        # Initialize a Frame (since we inherit from tk.Frame)
        super().__init__(parent, *args, **kwargs)

        # Create all widgets of this frame
        self._bttn_my_profile = tk.Button(
            self,
            text='My Profile',
            command=self._on_my_profile_bttn_click
        )
        self._bttn_my_internships = tk.Button(
            self,
            text='My Internships',
            command=self._on_my_internships_bttn_click
        )
        self._bttn_search_internships = tk.Button(
            self,
            text='Search Internships',
            command=self._on_search_internships_bttn_click
        )

        # Pack all widgets into this frame
        self._bttn_my_profile.pack(side=tk.LEFT, anchor=tk.W, padx=3, pady=2)
        self._bttn_my_internships.pack(side=tk.LEFT, anchor=tk.W, padx=3, pady=2)
        self._bttn_search_internships.pack(side=tk.RIGHT, anchor=tk.E, padx=3, pady=2)
    
    def _on_my_profile_bttn_click(self):
        """Responds to the event when the "My Profile" button is clicked."""
        print('"My Profile" was clicked')

    def _on_my_internships_bttn_click(self):
        """Responds to the event when the "My Internships"
        button is clicked.
        """
        print('"My Internships" was clicked')

    def _on_search_internships_bttn_click(self):
        """Responds to the event when the "Search Internships"
        button is clicked.
        """
        print('"Search Internships" was clicked')
