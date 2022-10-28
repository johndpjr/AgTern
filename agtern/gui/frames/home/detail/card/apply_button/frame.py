import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

from .......common import LOG


class InternshipApplyButton(tk.Frame):
    """A frame containing all specific internship details."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            width=350,
            height=100,
            bg="white",
            highlightthickness=1,
            highlightbackground="black",
        )

        self._var_link = tk.StringVar()
        self._var_img = tk.PhotoImage(file="agtern/gui/assets/link-icon.png").subsample(
            70, 70
        )

        self._lbl_apply = ttk.Label(self, text="Apply now", style="DetailFrame.TLabel")
        self._photo_img = ttk.Label(
            self, image=self._var_img, style="DetailFrame.TLabel"
        )

        self._lbl_apply.place_configure(relx=0.3, rely=0.1, relwidth=0.6, relheight=0.8)
        self._photo_img.place_configure(relx=0.9, rely=0.6)

        # bind mouse click input
        def _bound_to_mouseclick(event):
            self.bind_all("<Button-1>", self._on_apply_now_bttn_click)
            self.configure(bg="#CC2222")
            self._lbl_apply.config(style="DetailFrameHighlight.TLabel")
            self._photo_img.config(style="DetailFrameHighlight.TLabel")

        self.bind("<Enter>", _bound_to_mouseclick)

        # unbind mouse click input
        def _unbound_to_mouseclick(event):
            self.unbind_all("<Button-1>")
            self.configure(bg="white")
            self._lbl_apply.config(style="DetailFrame.TLabel")
            self._photo_img.config(style="DetailFrame.TLabel")

        self.bind("<Leave>", _unbound_to_mouseclick)

    def _on_apply_now_bttn_click(self, event):
        """Open url of internship when the "Apply now"
        button is clicked."""

        link = self._var_link.get()
        LOG.info(f'"Apply now" was clicked and the link is {link}')
        if link:  # Ensure not empty
            webbrowser.open_new_tab(link)

    def set_apply_link(self, link: str):
        """Sets all of the internship link variables to whatever
        internship was clicked."""
        self._var_link.set(link)
