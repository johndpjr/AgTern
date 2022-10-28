import tkinter as tk
from tkinter.ttk import *


def set_styles(style: Style):
    style.configure(
        "White.TButton",
        bd=0,
        relief="solid",
        justify=tk.CENTER,
        background="white",
        foreground="black",
    )
    style.configure(
        "Red.TButton",
        bd=0,
        relief="solid",
        justify=tk.CENTER,
        background="#CC2222",
        foreground="black",
    )
    style.configure(
        "DetailFrame.TLabel",
        background="white",
        foreground="black",
        font=("MS Reference Sans Serif", 14),
    )
    style.configure(
        "DetailFrameHighlight.TLabel",
        background="#CC2222",
        foreground="white",
        font=("MS Reference Sans Serif", 14),
    )
    style.configure(
        "EntryFrame.TLabel",
        background="white",
        foreground="black",
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "EntryFrameHighlight.TLabel",
        background="#CC2222",
        foreground="white",
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "Settings.TLabel",
        background="#CC2222",
        foreground="white",
        font=("MS Reference Sans Serif", 10),
    )
    style.configure(
        "TFrame",
        background="white",
    )
    style.configure(
        "TMenubutton",
        background="white",
    )
    style.configure(
        "TSeparator",
        background="white",
    )
    style.configure(
        "Vertical.TScrollbar",
        troughcolor="white",
        bordercolor="white",
        background="#CC2222",
        gripcount=0,
        arrowcolor="white",
    )
    style.map("Vertical.TScrollbar", background=[("active", "#AA1111")])
