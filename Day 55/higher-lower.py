from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemZidzM3aDc5cHFjZHU3ZGlyM256MGZocWxiaTF1dGZsdXF1dGx5YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KuPZknky1LGKocimth/giphy.gif" width=600>')

random_number = random.randint(0, 9)

@app.route("/<int:number>")
def guess(number):
    if number > random_number:
        return "<h1 style='color: purple'>Too high, try again!</h1>" \
               "<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWN5cHhrMWJxdHhxZXl4MXZrY20zdTloZW5rOTB2enh2eWN4cDhjeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jgNDd7JfzZU5l3KU1h/giphy.gif'/>"
    if number < random_number:
        return "<h1 style='color: red'>Too low, try again!</h1>" \
               "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGpid3IxbGFzbzlndjFyaGtxc2p5d241M2JlcXBiMml2OHc1dzA0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vIyWHMigvN993Fx7dJ/giphy.gif'/>"
    if number == random_number:
        return "<h1 style='color: green'>TOUCHDOWN!</h1>" \
               "<img src='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW9oYnBpY3oyNnQ2YXBxb2gxcHNlNHZiYXl3bWNzam5nNTl6OXFyYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HFdxdcBCVPIndztZaR/giphy.gif'/>"

if __name__ == "__main__":
    app.run(debug=True)


