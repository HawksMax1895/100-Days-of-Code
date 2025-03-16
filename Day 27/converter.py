from tkinter import *

def convert():
    miles = float(entry.get())
    new_result = miles*1.609
    result_label.config(text=new_result)

window = Tk()
window.title("Mile to Kilometer Converter")
#window.minsize(width=300, height=300)
window.config(padx=20, pady=20)

#Label
text_label = Label(text="is equal to")
text_label.grid(column=0, row=1)

miles_label = Label(text="miles")
miles_label.grid(column=2, row=0)

km_label = Label(text="km")
km_label.grid(column=2, row=1)

result_label = Label(text="0")
result_label.grid(column=1, row=1)

#Button
button= Button(text="Convert", command=convert)
button.grid(column=1, row=2)

#Entry
entry = Entry(width=30)
entry.grid(column=1,row=0)

window.mainloop()