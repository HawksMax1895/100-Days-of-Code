import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
score = Scoreboard()
car_manager = CarManager()

screen.listen()
screen.onkey(player.move, 'w')

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move()

    #Turle reaches end
    if player.ycor() > 260:
        player.reset_pos()
        score.point()
        car_manager.level_up()

    #Detect Turtle Collision resulting in Turtle soup
    for car in car_manager.all_cars:
        if player.distance(car) < 20:
            score.game_over()
            game_is_on = False

screen.exitonclick()