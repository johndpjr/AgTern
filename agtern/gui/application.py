import tkinter as tk


class Application(tk.Tk):
    """GUI for AgTern."""

    def __init__(self):
        super().__init__()

        self.title('AgTern')
        self.geometry('640x480')
        
        hello_world_label = tk.Label(self, text='Hello, World!')
        hello_world_label.pack(side=tk.TOP)