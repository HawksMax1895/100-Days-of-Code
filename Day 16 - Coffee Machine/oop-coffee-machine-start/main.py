from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_machine = CoffeeMaker()
bank = MoneyMachine()

is_on = True
while is_on:
    choice = input(f"What would you like? ({menu.get_items()}) ")
    if choice == "off":
        is_on = False
    elif choice == "report":
        coffee_machine.report()
        bank.report()
    else:
        drink = menu.find_drink(choice)
        if coffee_machine.is_resource_sufficient(drink):
            #zwei ifs nacheinander auch zusammenfassbar mit einem if und dem Operator "and"
            if bank.make_payment(drink.cost):
                coffee_machine.make_coffee(drink)