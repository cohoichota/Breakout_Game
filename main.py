import time
from turtle import Screen
from turtle import Turtle

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
ALIGNMENT = "center"
FONT = ("Arial", 18, "normal")

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Breakout_Game")
screen.tracer(0)


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)

    def go_left(self):
        new_x = self.xcor() - 20
        self.goto(new_x, self.ycor())

    def go_right(self):
        new_x = self.xcor() + 20
        self.goto(new_x, self.ycor())


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("white")
        self.x_move = 10
        self.y_move = 10

    def ball_move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, 0)
        self.bounce_y()


class Brick(Turtle):
    def __init__(self):
        super().__init__()
        self.brick = None
        self.brick_list = []

    def create_brick(self):
        for n in range(6):
            select_color = COLORS[n]
            for i in range(6):
                self.brick = Turtle()
                self.brick.shape("square")
                self.brick.color(select_color)
                self.brick.shapesize(stretch_wid=1, stretch_len=5)
                self.brick.penup()
                self.brick.goto(-330 + 130 * i, 250 - 30 * n)
                self.brick_list.append(self.brick)


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.clear()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(0, 270)
        self.score = 0
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        try:
            with open("data.txt") as data:
                self.high_score = int(data.read())
        except FileNotFoundError:
            with open("data.txt", mode="w") as file:
                file.write("0")
            with open("data.txt", mode="r") as data:
                self.high_score = int(data.read())

    def increase_score(self):
        self.score += 1

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Arial", 18, "normal"))

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", mode="w") as data:
                a = str(self.high_score)
                data.write(a)
        self.score = 0
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)


paddle = Paddle((0, -260))
ball = Ball()
brick = Brick()
create_brick = brick.create_brick()
brick_list = brick.brick_list
score = Scoreboard()


screen.listen()
screen.onkey(key="Left", fun=paddle.go_left)
screen.onkey(key="Right", fun=paddle.go_right)


game_is_on = True
while game_is_on:

    screen.update()
    time.sleep(0.1)
    ball.ball_move()

    # Detect collision with wall
    if ball.ycor() > 280:
        ball.bounce_y()

    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    # Detect collision with paddle
    if ball.distance(paddle) < 50 and ball.ycor() < -240:
        ball.bounce_y()

    # Detect paddle missed
    if ball.distance(paddle) > 50 and ball.ycor() < -300:
        ball.reset_position()

    # Game over
    if len(brick_list) < 0:
        game_is_on = False
        score.game_over()

    # Block collision check
    for i in brick_list:
        if (i.ycor()-10 <= ball.ycor() <= i.ycor()+10) and (i.xcor()-50 < ball.xcor() < i.xcor()+50):
            i.goto(1000, 1000)
            ball.bounce_y()
            brick_list.remove(i)
            score.increase_score()
            score.update_scoreboard()


screen.exitonclick()
