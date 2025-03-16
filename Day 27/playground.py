def add(*args):
    print(args[2])
    sum=0
    for n in args:
        sum=sum+n
    print(sum)

add(3, 5, 6, 2, 17)

def calculate(n, **kwargs):
    print(kwargs)
    #for key, value in kwargs.items():
    #    print(key)
    #    print(value)
    #print(kwargs["add"])
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)


calculate(2, add=3, multiply=5)

class Car:
    def __init__(self, **kw):
        self.make = kw["make"]
        self.model = kw.get("model")

my_car = Car(make="hynudai")
print(my_car.make)
print(my_car.model)