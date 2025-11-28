import tkinter as tk

from pythonic.mvc.model.prime.Constants import DIM


class GameFrame(tk.Tk):

    def __init__(self):
        super().__init__()

        # Create your content
        self.contentFrame = tk.Label(self, text="Game Window Loaded")
        self.contentFrame.pack(fill=tk.BOTH, expand=True)

        # Force window placement AFTER it's created
        self.after(50, self.force_placement)

        # Bind close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def force_placement(self):
        """Guaranteed macOS-safe placement after Tk finishes initializing."""
        width = DIM.width
        height = DIM.height

        # Debug printing so we see what DIM actually contains
        print("Placing window:")
        print("Width:", width, " Height:", height)

        # Make sure the window has a known size first
        self.geometry(f"{width}x{height}")

        # Move it to the top-left corner
        self.geometry(f"{width}x{height}+0+0")

        # Bring the window to the front
        self.lift()
        self.focus_force()

    def on_close(self):
        self.destroy()
