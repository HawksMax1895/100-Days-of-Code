from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def gen_password():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    pass_entry.insert(END, string=password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    if len(website_entry.get()) == 0 or len(pass_entry.get()) == 0:
        messagebox.showwarning(title="Missing Information", message="Please fill out all the fields")
        return None

    is_ok = messagebox.askokcancel(title=website_entry.get(),
                                   message=f"These are the details entered: \nEmail: {mail_entry.get()}\nPassword: {pass_entry.get()}\nIs it ok to save?")
    if is_ok:
        password_file = open("passwords.txt", "a")
        password_file.write(f"{website_entry.get()} | {mail_entry.get()} | {pass_entry.get()}\n")
        password_file.close()
        website_entry.delete(0, END)
        pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
pass_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pass_image)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
website.grid(column=0, row=1)
mail = Label(text="Email/Username:")
mail.grid(column=0, row=2)
password = Label(text="Password:")
password.grid(column=0, row=3)

gen_pass = Button(text="Generate Password", command=gen_password)
gen_pass.grid(column=2, row=3)
add = Button(text="Add", width=45, command=save_password)
add.grid(column=1, row=4, columnspan=2)

website_entry = Entry(width=45)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()
mail_entry = Entry(width=45)
mail_entry.grid(column=1, row=2, columnspan=2)
mail_entry.insert(END, string="maxradmacher@gmail.com")
pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3)

window.mainloop()
