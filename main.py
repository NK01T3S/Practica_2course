from tkinter import *

def setup_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 900
    window_height = 500
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

class MeinMenu:
    def __init__(self):
        self.root = Tk()
        self.root.title("MeinMenu")
        self.play_button = Button(self.root, text="ИГРАТЬ", command=self.start_game, padx=80, pady=20)
        self.play_button.pack(pady=50)
        self.control_button = Button(self.root, text="УПРАВЛЕНИЕ", command=self.show_controls, padx=60, pady=20)
        self.control_button.pack(pady=50)
        self.exit_button = Button(self.root, text="ВЫХОД", command=self.exit_program, padx=80, pady=20)
        self.exit_button.pack(pady=50)
        setup_window(self.root)
        self.root.resizable(width=False, height=False)
        self.root.mainloop()

    def start_game(self):
        self.root.destroy()
        p = Playfield()
        p.root.focus_force()
        p.start()

    def show_controls(self):
        controls_window = Toplevel(self.root)
        setup_window(controls_window)
        controls_window.resizable(width=False, height=False)
        controls_window.title("Управление")

        controls_text = "Управление:\n\nИгрок 1:\nW - вверх\nS - вниз\nA - влево\nD - вправо\n\nИгрок 2:\nI - вверх\nK - вниз\nJ - влево\nL - вправо"
        controls_label = Label(controls_window, text=controls_text, font=("Arial", 14))
        controls_label.pack(padx=20, pady=20)

        controls_close_button = Button(controls_window, text="Закрыть",
                                       command=lambda: [controls_window.destroy(), self.root.deiconify()])
        controls_close_button.pack(pady=60)

        self.root.withdraw()

    def exit_program(self):
        self.root.destroy()

class Playfield:
    def __init__(self):
        self.pressed = {}
        self.p1_score = 0
        self.p2_score = 0
        self._create_ui()
        self.winner_window = None

    def start(self):
        self._animate()
        setup_window(self.root)
        self.root.mainloop()

    def _create_ui(self):
        self.root = Tk()
        self.canvas = Canvas(width=900, height=500, bg="black")
        self.root.resizable(width=False, height=False)
        self.canvas.pack()
        self.menu_button = Button(self.root, text="<-", command=self.go_to_main_menu, padx=20, pady=10)
        self.menu_button.place(x=20, y=20)
        self.p1 = Paddle(self.canvas, "p1", "yellow", 30, 250, 30, 420, 30, 470)
        self.p2 = Paddle(self.canvas, "p2", "blue", 870, 250, 480, 870, 30, 470)
        self.ball = Ball(self.canvas, "ball", self.p1_score, self.p2_score, "red", 450, 250)
        self.gate_left = Gate(self.canvas, "gate_left", "white", 5, 250, 100, 300, 100, 450)
        self.gate_right = Gate(self.canvas, "gate_right", "white", 895, 250, 750, 300, 750, 450)

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

        if self.ball.check_horizontal_collision(self.p1) or self.ball.check_horizontal_collision(self.p2):
            self.ball.bounce_horizontal()
        if self.ball.check_vertical_collision(self.p1) or self.ball.check_vertical_collision(self.p2):
            self.ball.bounce_vertical()
        self.ball.check_paddle_collision(self.p1)
        self.ball.check_paddle_collision(self.p2)

        self.ball.move()

        self.p1.redraw()
        self.p2.redraw()
        self.ball.redraw()
        self.gate_left.redraw()
        self.gate_right.redraw()
        self.canvas.delete("score")
        self.canvas.create_text(450, 50, text=f"{self.ball.p1_score}     {self.ball.p2_score}", tags="score",
                                fill="white", font=("Arial", 20))

        if self.ball.p1_score >= 10 or self.ball.p2_score >= 10:
            self.show_winner()
        else:
            self.root.after(10, self._animate)

    def show_winner(self):
        self.winner_window = Toplevel(self.root)
        self.winner_window.title("Победа!")

        screen_width = self.winner_window.winfo_screenwidth()
        screen_height = self.winner_window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.winner_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.winner_window.resizable(width=False, height=False)
        if self.ball.p1_score >= 10:
            winner_text = "Игрок 1 победил!"
        else:
            winner_text = "Игрок 2 победил!"
        winner_label = Label(self.winner_window, text=winner_text, font=("Arial", 20))
        winner_label.pack(padx=20, pady=20)
        restart_button = Button(self.winner_window, text="Перезапуск", command=self.restart_game)
        restart_button.pack(pady=10)
        main_menu_button = Button(self.winner_window, text="Главное меню", command=self.go_to_main_menu)
        main_menu_button.pack(pady=10)

    def restart_game(self):
        self.root.destroy()
        p = Playfield()
        p.root.focus_force()
        p.start()

    def _set_bindings(self):
        for char in ["w", "s", "a", "d", "i", "k", "j", "l"]:
            self.root.bind(f"<KeyPress-{char}>", self._pressed)
            self.root.bind(f"<KeyRelease-{char}>", self._released)
            self.pressed[char] = False

    def _pressed(self, event):
        self.pressed[event.char] = True

    def _released(self, event):
        self.pressed[event.char] = False

    def go_to_main_menu(self):
        self.root.destroy()
        MeinMenu()

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

    def move_up(self):
        self.y = max(self.y - 3, self.top_boundary)

    def move_down(self):
        self.y = min(self.y + 3, self.bottom_boundary)

    def move_left(self):
        self.x = max(self.x - 3, self.left_boundary)

    def move_right(self):
        self.x = min(self.x + 3, self.right_boundary)

    def redraw(self):
        x0 = self.x - 30
        x1 = self.x + 30
        y0 = self.y - 30
        y1 = self.y + 30
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)

class Ball:
    def __init__(self, canvas, tag, p1_score, p2_score, color="green", x=0, y=0):
        self.canvas = canvas
        self.tag = tag
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.x = x
        self.y = y
        self.color = color
        self.vx = 5
        self.vy = 5
        self.radius = 10
        self.redraw()
        self.friction = 0.98

    def move(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= self.friction
        self.vy *= self.friction

        if self.x < -10 or self.x > 870:
            self.vx = -self.vx

        if self.y < -10 or self.y > 470:
            self.vy = -self.vy

        if self.x < 30:
            self.p2_score += 1
            self.reset_position()
        elif self.x > 870:
            self.p1_score += 1
            self.reset_position()

    def check_horizontal_collision(self, paddle):
        x0_paddle = paddle.x - 30
        x1_paddle = paddle.x + 30
        y0_paddle = paddle.y - 20
        y1_paddle = paddle.y + 20

        if (x0_paddle < self.x + self.radius < x1_paddle or
            x0_paddle < self.x - self.radius < x1_paddle) and \
                (y0_paddle < self.y + self.radius < y1_paddle or
                 y0_paddle < self.y - self.radius < y1_paddle):
            return True

        return False

    def check_vertical_collision(self, paddle):
        x0_paddle = paddle.x - 30
        x1_paddle = paddle.x + 30
        y0_paddle = paddle.y - 20
        y1_paddle = paddle.y + 20

        if (x0_paddle < self.x < x1_paddle) and \
                ((y0_paddle < self.y + self.radius < y1_paddle) or
                 (y0_paddle < self.y - self.radius < y1_paddle)):
            return True

        return False

    def bounce_horizontal(self):
        self.vx = -self.vx
        if abs(self.vx) < 10:
            if self.vx > 0:
                self.vx = 10
            else:
                self.vx = -10
        self.vy *= 1.05

    def bounce_vertical(self):
        self.vy = -self.vy
        if abs(self.vy) < 10:
            if self.vy > 0:
                self.vy = 10
            else:
                self.vy = -10
        self.vx *= 1.05

    def check_paddle_collision(self, paddle):
        x0_paddle = paddle.x - 30
        x1_paddle = paddle.x + 30
        y0_paddle = paddle.y - 20
        y1_paddle = paddle.y + 20

        if (x0_paddle < self.x < x1_paddle) and (y0_paddle < self.y < y1_paddle):
            if self.x < paddle.x:
                self.x = x0_paddle - self.radius
            elif self.x > paddle.x:
                self.x = x1_paddle + self.radius
            if self.y < paddle.y:
                self.y = y0_paddle - self.radius
            elif self.y > paddle.y:
                self.y = y1_paddle + self.radius

            if self.x < paddle.x:
                self.bounce_horizontal()
            elif self.x > paddle.x:
                self.bounce_horizontal()

            if self.y < paddle.y:
                self.bounce_vertical()
            elif self.y > paddle.y:
                self.bounce_vertical()

    def reset_position(self):
        if self.x < 30:
            self.x = 350
            self.y = 250
        elif self.x > 870:
            self.x = 550
            self.y = 250
        self.vx = -self.vx
        self.vy = -self.vy

        self.canvas.delete("score")
        self.canvas.create_text(450, 50, text=f"{self.p1_score}     {self.p2_score}", tags="score",
                                fill="white", font=("Arial", 20))

    def redraw(self):
        x0 = self.x - self.radius
        x1 = self.x + self.radius
        y0 = self.y - self.radius
        y1 = self.y + self.radius
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)

class Gate:
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
        x0 = self.x - 5
        x1 = self.x + 5
        y0 = self.y - 100
        y1 = self.y + 100
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(x0, y0, x1, y1, tags=self.tag, fill=self.color)


if __name__ == '__main__':
    MeinMenu()