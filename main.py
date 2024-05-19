from tkinter import *

def setup_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 900
    window_height = 500
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

class Playfield:
    def __init__(self):
        self._create_ui()
        setup_window(self.root)

    def _create_ui(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=900, height=500, bg="black")
        self.root.resizable(width=False, height=False)
        self.root.update_idletasks()

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    p = Playfield()
    p.start()