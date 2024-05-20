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
        self.canvas.pack()
        self.p1 = Paddle(self.canvas, "p1", "yellow", 30, 250, 30, 420, 30, 470)
        self.p2 = Paddle(self.canvas, "p2", "blue", 870, 250, 480, 870, 30, 470)

    def start(self):
        self.root.mainloop()

class Paddle:
    def __init__(self, canvas, tag, color, x=0, y=0, left_boundary=0, right_boundary=900, top_boundary=0, bottom_boundary=500):
        self.canvas = canvas
        self.tag = tag
        self.x = x
        self.y = y
        self.color = color
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.top_boundary = top_boundary
        self.bottom_boundary = bottom_boundary
        self.redraw()

    def redraw(self):
        x0 = self.x - 30
        x1 = self.x + 30
        y0 = self.y - 30
        y1 = self.y + 30
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)


if __name__ == '__main__':
    p = Playfield()
    p.start()