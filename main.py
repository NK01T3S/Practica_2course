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
        self.pressed = {}
        self._create_ui()

    def start(self):
        self._animate()
        setup_window(self.root)
        self.root.mainloop()

    def _create_ui(self):
        self.root = Tk()
        self.canvas = Canvas(width=900, height=500, bg="black")
        self.root.resizable(width=False, height=False)
        self.canvas.pack()
        self.p1 = Paddle(self.canvas, "p1", "yellow", 30, 250, 30, 420, 30, 470)
        self.p2 = Paddle(self.canvas, "p2", "blue", 870, 250, 480, 870, 30, 470)
        self.ball = Ball(self.canvas, "ball", "red", 450, 250)

        self._set_bindings()

    def _animate(self):
        if self.pressed["w"]:
            self.p1.move_up()
        if self.pressed["s"]:
            self.p1.move_down()
        if self.pressed["a"]:
            self.p1.move_left()
        if self.pressed["d"]:
            self.p1.move_right()
        if self.pressed["i"]:
            self.p2.move_up()
        if self.pressed["k"]:
            self.p2.move_down()
        if self.pressed["j"]:
            self.p2.move_left()
        if self.pressed["l"]:
            self.p2.move_right()

        self.ball.move()

        self.p1.redraw()
        self.p2.redraw()
        self.ball.redraw()
        self.root.after(10, self._animate)

    def _set_bindings(self):
        for char in ["w", "s", "a", "d", "i", "k", "j", "l"]:
            self.root.bind(f"<KeyPress-{char}>", self._pressed)
            self.root.bind(f"<KeyRelease-{char}>", self._released)
            self.pressed[char] = False

    def _pressed(self, event):
        self.pressed[event.char] = True

    def _released(self, event):
        self.pressed[event.char] = False

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

    def move_left(self):
        self.x = max(self.x - 4, self.left_boundary)

    def move_right(self):
        self.x = min(self.x + 4, self.right_boundary)

    def move_up(self):
        self.y = max(self.y - 4, self.top_boundary)

    def move_down(self):
        self.y = min(self.y + 4, self.bottom_boundary)

    def redraw(self):
        x0 = self.x - 30
        x1 = self.x + 30
        y0 = self.y - 30
        y1 = self.y + 30
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)

class Ball:
    def __init__(self, canvas, tag, color="green", x=0, y=0):
        self.canvas = canvas
        self.tag = tag
        self.x = x
        self.y = y
        self.color = color
        self.vx = 3
        self.vy = 3
        self.radius = 10
        self.redraw()

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < -10 or self.x > 870:
            self.vx = -self.vx

        if self.y < -10 or self.y > 470:
            self.vy = -self.vy

    def bounce_horizontal(self):
        self.vx = -self.vx

    def reset_position(self):
        self.x = 450
        self.y = 250
        self.vx = 3
        self.vy = 3

    def redraw(self):
        x0 = self.x - self.radius
        x1 = self.x + self.radius
        y0 = self.y - self.radius
        y1 = self.y + self.radius
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)


if __name__ == '__main__':
    p = Playfield()
    p.start()