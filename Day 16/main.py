# # import another_module
# #
# # print(another_module.another_variable)
#
# import turtle
#
# timmy = turtle.Turtle()
# timmy.shape("turtle")
# timmy.color("blue")
# timmy.forward(100)
# my_screen = turtle.Screen()
# print(my_screen.canvwidth)
# my_screen.exitonclick()


import prettytable

table = prettytable.PrettyTable()
table.add_column("Pokemon Name", ["Pikachu", "Squirtle", "Charmander"])
table.add_column("Type", ["Electric", "Water", "Fire"])
table.align = "l"
print(table)