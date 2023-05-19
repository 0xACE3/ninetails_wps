from tkinter import ttk
import tkinter as tk


class CaptureGui(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        # main controller
        self.controller = controller

        # configs
        self.title("Fast WPS")
        self.attributes("-transparentcolor", "red")
        self.button_captions = ["Capture Screen", "Stop Program"]

        # frames
        self.frm: ttk.Frame | None = None
        self.capture_frm: ttk.Frame | None = None

        # ui components
        self._make_main_frame()
        self._make_buttons()
        self._make_capture_frame()

    def main(self):
        print("Launching GUI...")
        self.mainloop()

    def _make_main_frame(self):
        self.frm = ttk.Frame(self)
        self.frm.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def _make_buttons(self):
        # outer frame
        outer_frm = ttk.Frame(self.frm)
        outer_frm.pack()

        for caption in self.button_captions:
            btn = ttk.Button(outer_frm,
                             text=caption,
                             command=(lambda button=caption: self.controller.on_button_click(button)))
            btn.pack(side="left")

    def _make_capture_frame(self):
        # transparent style
        style = ttk.Style()
        style.element_create("Transparent.Frame", "from", "clam")
        style.layout("Transparent.TFrame", [("Transparent.Frame", {"sticky": "nswe"})])
        style.configure("Transparent.TFrame", background="red")

        # outer frame
        outer_frm = ttk.Frame(self.frm)
        outer_frm.pack(fill=tk.BOTH, expand=True)

        # capture frame
        self.capture_frm = ttk.Frame(outer_frm, width=1090, height=420, borderwidth=30, style="Transparent.TFrame")
        self.capture_frm.pack(fill=tk.BOTH, expand=True)

    def shutdown(self):
        print("Shutting down GUI...")
        self.destroy()
