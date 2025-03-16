import tkinter
from tkinter import *

def button_clicked():
    my_label.config(text=input.get())

window = tkinter.Tk()
window.title("My first GUI Program")
window.minsize(width=500, height=300)
window.config(padx=100, pady=35)

#Label

my_label = tkinter.Label(text="I Am a Label", font=("Arial", 24, "bold"))
my_label["text"] = "New Text"
my_label.config(text="New Text")
#my_label.pack(side="bottom")
#my_label.place(x=5,y=5)
my_label.grid(column=0, row=0)
my_label.config(pady=100, padx=25)

#Entry

input = Entry(width=10)
#print(input.get())
#input.pack()
input.grid(column=3, row=2)

#Button

button = Button(text="Click Me", command=button_clicked)
#button.pack()
button.grid(column=1, row=1)

button2 = Button(text="Click Me 2x", command=button_clicked)
#button.pack()
button2.grid(column=2, row=0)

window.mainloop()