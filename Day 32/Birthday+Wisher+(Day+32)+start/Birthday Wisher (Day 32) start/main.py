# import smtplib
#
# my_email = "max084842@gmail.com"
# password = ""
#
# connection = smtplib.SMTP("smtp.gmail.com")
# connection.starttls()
# connection.login(user=my_email, password=password)
# connection.sendmail(from_addr=my_email, to_addrs="radimax@web.de", msg="Hello")
# connection.close()
#
# import datetime as dt
#
# now = dt.datetime.now()
# year = now.year
# print(year)
#
# date_of_birth = dt.datetime(year=1997, month=10, day=8)
# print(date_of_birth)

import smtplib
import datetime as dt
import random

my_email = "max084842@gmail.com"
password = ""

day_of_week = dt.datetime.now().weekday()

with open("quotes.txt") as f:
    quotes = f.read().splitlines()

quote_of_day = random.choice(quotes)

if day_of_week == 0:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="radimax@web.de",
                            msg=f"Subject: Quote of the Day\n\n{quote_of_day}")