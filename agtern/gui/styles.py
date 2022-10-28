import tkinter as tk
from tkinter.ttk import *

BACKGROUND = "#FFFFFF"
HIGHLIGHT = "#500000"
THUMB = "#AA1111"
BORDER = "#000000"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#FFFFFF"


def set_styles(style: Style):
    style.configure(
        "White.TButton",
        bd=0,
        relief="solid",
        justify=tk.CENTER,
        background=BACKGROUND,
        foreground=TEXT_DARK,
    )
    style.configure(
        "Red.TButton",
        bd=0,
        relief="solid",
        justify=tk.CENTER,
        background=HIGHLIGHT,
        foreground=TEXT_DARK,
    )
    style.configure(
        "DetailFrame.TLabel",
        background=BACKGROUND,
        foreground=TEXT_DARK,
        font=("MS Reference Sans Serif", 14),
    )
    style.configure(
        "DetailFrameHighlight.TLabel",
        background=HIGHLIGHT,
        foreground=TEXT_LIGHT,
        font=("MS Reference Sans Serif", 14),
    )
    style.configure(
        "EntryFrame.TLabel",
        background=BACKGROUND,
        foreground=TEXT_DARK,
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "EntryFrameHighlight.TLabel",
        background=HIGHLIGHT,
        foreground=TEXT_LIGHT,
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "Settings.TLabel",
        background=HIGHLIGHT,
        foreground=TEXT_LIGHT,
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "TFrame",
        background=BACKGROUND,
    )
    style.configure(
        "TMenubutton",
        background=BACKGROUND,
    )
    style.configure(
        "TSeparator",
        background=BACKGROUND,
    )
    style.configure(
        "Vertical.TScrollbar",
        troughcolor=BACKGROUND,
        bordercolor=BACKGROUND,
        background=HIGHLIGHT,
        gripcount=0,
        arrowcolor=BACKGROUND,
    )
    style.map("Vertical.TScrollbar", background=[("active", THUMB)])
