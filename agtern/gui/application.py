import tkinter as tk
import tkinter.ttk as ttk

from gui.frames.top_bar_frame import TopBarFrame
from gui.frames.internship_list_frame import InternshipListFrame
from gui.frames.internship_detail_frame import InternshipDetailFrame


class Application(tk.Tk):
    """GUI for AgTern."""

    def __init__(self):
        super().__init__()

        self.title('AgTern')
        self.geometry('640x480')
        
        # Create all the frames
        self.frm_top_bar = TopBarFrame(self, relief=tk.RAISED, bd=2)
        self.frm_internship_list = InternshipListFrame(self)
        self.frm_internship_detail = InternshipDetailFrame(self)

        # Pack all frames into the window
        # Pack TopBarFrame at the top and fill the frame in the X direction
        self.frm_top_bar.pack(side=tk.TOP, fill=tk.X, pady=(0,3))
        # Pack InternshipListFrame on the left and fill the frame
        #   in both directions
        self.frm_internship_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=(3,0), pady=3)
        # Add a Separator widget to divide the previous and next frames
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=3)
        # Pack InternshipDetailFrame on the right side and fill the frame
        #   in both directions
        self.frm_internship_detail.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,3), pady=3)
