from turtle import Turtle


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.speed('fastest')
        self.hideturtle()
        self.goto(0, 280)
        with open('data.txt') as file:
            self.high_score = file.read()
        self.score = 0
        self.update()

    def update(self):
        self.clear()
        self.write(f'Score: {self.score}, High Score: {self.high_score}', move=False, align='center',
                   font=('Arial', 10, 'bold'))

    def add(self):
        self.score += 1
        self.update()

    def reset(self):
        if self.score > int(self.high_score):
            with open('data.txt', mode='w') as file:
                file.write(f"{self.score}")
                self.high_score = self.score
        self.score = 0
        self.update()
