import tkinter as tk


class GameFrame(tk.Tk):

    def __init__(self):
        super().__init__()

        # Component initialization
        self.contentFrame = tk.Label(self)
        self.contentFrame.pack(fill=tk.BOTH, expand=True)
        # Center the window on the screen
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        # Bind the closing event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.contentFrame.destroy()
        self.destroy()


