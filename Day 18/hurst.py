import random
import colorgram
import turtle as turtle_import

rgb_colors = []
colors = colorgram.extract('image.jpg', 30)
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    new_color = (r, g, b)
    rgb_colors.append(new_color)

hurst = turtle_import.Turtle()
hurst.speed(0)
turtle_import.colormode(255)
hurst.penup()

x_1= 0
y_1= 0
for y in range(0, 10):
    for x in range(0, 10):
        hurst.dot(20, random.choice(rgb_colors))
        x_1 += 50
        hurst.setx(x_1)
    y_1 += 50
    hurst.sety(y_1)
    x_1 =0
    hurst.setx(x_1)

screen = turtle_import.Screen()
screen.exitonclick()