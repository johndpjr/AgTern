import tkinter as tk
from datetime import datetime
from tkinter import ttk

from agtern.common import Internship
from agtern.gui.styles import *


class InternshipEntryFrame(tk.Frame):
    """A frame containing internship entry button."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(width=360, height=120, bg=BACKGROUND)

        # Variables that the parent (and thus all children)
        #   have access to
        self.internship = None
        self._var_name = tk.StringVar()
        self._var_title = tk.StringVar()
        self._var_period = tk.StringVar()
        self._var_year = tk.StringVar()
        self._var_icon = tk.StringVar()

        self.card_entry = tk.Frame(
            self,
            background=BACKGROUND,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.lb_name = ttk.Label(
            self, textvariable=self._var_name, style="EntryFrame.TLabel"
        )
        self.lb_title = ttk.Label(
            self, textvariable=self._var_title, style="EntryFrame.TLabel"
        )
        self.lb_period = ttk.Label(
            self, textvariable=self._var_period, style="EntryFrame.TLabel"
        )
        self.lb_year = ttk.Label(
            self, textvariable=self._var_year, style="EntryFrame.TLabel"
        )
        self.lb_icon = tk.Label(
            self,
            textvariable=self._var_icon,
            bg=BACKGROUND,
            font=("Helvetica", 36),
            anchor=tk.CENTER,
        )

        self.card_entry.place_configure(
            relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9
        )
        self.lb_icon.place_configure(relx=0.1, rely=0.2, relwidth=0.25, relheight=0.6)
        self.lb_name.place_configure(relx=0.4, rely=0.2, relwidth=0.5, relheight=0.2)
        self.lb_title.place_configure(relx=0.4, rely=0.4, relwidth=0.5, relheight=0.2)
        self.lb_period.place_configure(relx=0.4, rely=0.6, relwidth=0.3, relheight=0.2)
        self.lb_year.place_configure(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.2)

        # bind mouse click input
        def _bound_to_mouseclick(event):
            self.bind_all("<Button-1>", self.populate_detail_frame)
            self.card_entry.config(bg=HIGHLIGHT)
            self.lb_icon.config(bg=HIGHLIGHT, fg=TEXT_LIGHT)
            self.lb_name.config(style="EntryFrameHighlight.TLabel")
            self.lb_title.config(style="EntryFrameHighlight.TLabel")
            self.lb_period.config(style="EntryFrameHighlight.TLabel")
            self.lb_year.config(style="EntryFrameHighlight.TLabel")

        self.bind("<Enter>", _bound_to_mouseclick)

        # unbind mouse click input
        def _unbound_to_mouseclick(event):
            self.unbind_all("<Button-1>")
            self.card_entry.config(bg=BACKGROUND)
            self.lb_icon.config(bg=BACKGROUND, fg=TEXT_DARK)
            self.lb_name.config(style="EntryFrame.TLabel")
            self.lb_title.config(style="EntryFrame.TLabel")
            self.lb_period.config(style="EntryFrame.TLabel")
            self.lb_year.config(style="EntryFrame.TLabel")

        self.bind("<Leave>", _unbound_to_mouseclick)

    def populate_entry(self, i: Internship):
        self.internship = i
        self._var_name.set(i.company)
        self._var_title.set(f"{i.title[:20]}{'...' if len(i.title) > 20 else ''}")
        self._var_period.set(i.period)
        if i.year != 0:
            self._var_year.set(str(i.year))
        self._var_icon.set(i.company[0] if i.company else " ")

    def populate_detail_frame(self, event):
        self.master.master.master.master._on_iship_list_item_bttn_click(self.internship)
