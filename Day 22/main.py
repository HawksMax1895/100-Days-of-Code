from turtle import Screen
from paddle import Paddle
from scoreboard import Scoreboard
from ball import Ball
import time

screen = Screen()
screen.bgcolor('black')
screen.setup(width=800, height=600)
screen.title('Pong')
screen.tracer(0)

paddle_l = Paddle((-350, 0))
paddle_r = Paddle((350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(paddle_l.go_up, 'w')
screen.onkey(paddle_l.go_down, 's')
screen.onkey(paddle_r.go_up, 'i')
screen.onkey(paddle_r.go_down, 'k')

game_is_on = True
while game_is_on:
    time.sleep(ball.velo)
    screen.update()
    ball.move()

    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    if ball.xcor() > 320 and paddle_r.distance(ball) < 50 or ball.xcor() < -320 and paddle_l.distance(ball) < 50:
        ball.bounce_x()

    if ball.xcor() > 380:
        ball.reset_pos()
        scoreboard.l_point()

    if ball.xcor() < -380:
        ball.reset_pos()
        scoreboard.r_point()



screen.exitonclick()
