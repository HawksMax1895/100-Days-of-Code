##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import smtplib
import datetime as dt
import pandas as pd
import random
import os

my_email = "max084842@gmail.com"
password = ""

bday = pd.read_csv("birthdays.csv")
today_m = dt.datetime.now().month
today_d = dt.datetime.now().day

letters = [f for f in os.listdir("letter_templates")]
chosen_letter = random.choice(letters)

with open(f"letter_templates/{chosen_letter}") as x:
    content = x.read()

for row in bday.itertuples(index=False):
    if row.month == today_m and row.day == today_d:
        message = content.replace("[NAME]", row.name)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=row.email, msg=f"Subject: Happy Birthday\n\n{message}")



