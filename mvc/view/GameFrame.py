import tkinter as tk

from mvc.model.prime.Constants import DIM


class GameFrame(tk.Tk):

    def __init__(self):
        super().__init__()
        self.running = True

        # Create your content
        self.contentFrame = tk.Label(self, text="Game Window Loaded")
        self.contentFrame.pack(fill=tk.BOTH, expand=True)

        # Force window placement AFTER it's created
        self.after(0, self.force_placement)

        # Bind close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def force_placement(self):
        """Guaranteed macOS-safe placement after Tk finishes initializing."""
        width = DIM.width
        height = DIM.height

        # Make sure the window has a known size first
        self.geometry(f"{width}x{height}")

        # Move it to the top-left corner
        self.geometry(f"{width}x{height}+40+40")

        # Bring the window to the front
        self.lift()
        self.focus_force()

    def on_close(self):
        self.running = False  # tell game loop to stop ASAP

        try:
            self.contentFrame.config(image='')
            self.contentFrame.image = None
        except:
            pass

        self.destroy()


