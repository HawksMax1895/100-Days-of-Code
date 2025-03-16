from turtle import Turtle, Screen

max = Turtle()
screen = Screen()

def move_forward():
    max.forward(10)

def move_backward():
    max.backward(10)

def counter_clockwise():
    heading = max.heading()
    heading -= 5
    max.setheading(heading)

def clockwise():
    heading = max.heading()
    heading += 5
    max.setheading(heading)

def clear():
    screen.resetscreen()

screen.listen()
screen.onkey(key='w', fun=move_forward)
screen.onkey(key='a', fun=move_backward)
screen.onkey(key='s', fun=counter_clockwise)
screen.onkey(key='d', fun=clockwise)
screen.onkey(key='c', fun=clear)

screen.exitonclick()