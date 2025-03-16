from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
random_card = {}
to_learn = {}

#---------------Read CSV---------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french_df = pandas.read_csv("data/french_words.csv")
    to_learn = french_df.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

#---------------Random French Word---------------#
def random_french():
    global random_card, task_id
    window.after_cancel(task_id)
    random_card = random.choice(to_learn)
    random_french_word = random_card["French"]
    canvas.itemconfig(current_language, text="French", fill="black")
    canvas.itemconfig(current_french_word, text=random_french_word, fill="black")
    canvas.itemconfig(current_card, image=card_front)
    task_id = window.after(3000, flip_card)


#---------------Card Flip---------------#
def flip_card():
    random_english_word = random_card["English"]
    canvas.itemconfig(current_french_word, text=random_english_word, fill="white")
    canvas.itemconfig(current_language, text="English", fill="white")
    canvas.itemconfig(current_card, image=card_back)

#---------------Known Word---------------#
def known_word():
    to_learn.remove(random_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    random_french()

#---------------UI---------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

task_id = window.after(3000, flip_card)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
current_card = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
current_language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
current_french_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

button_right = Button(image=right, highlightthickness=0, bg=BACKGROUND_COLOR, command=known_word)
button_right.grid(column=1, row=1)
button_wrong = Button(image=wrong, highlightthickness=0, bg=BACKGROUND_COLOR, command=random_french)
button_wrong.grid(column=0, row=1)

random_french()

window.mainloop()