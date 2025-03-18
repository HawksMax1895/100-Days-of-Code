import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 50.775345 # Your latitude
MY_LONG = 6.083887 # Your longitude

my_email = "max084842@gmail.com"
password = ""

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

latitude_close = (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5)
longitude_close = (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5)
night_time = time_now.hour >= sunset or time_now.hour <= sunrise

def check_iss():
    if latitude_close and longitude_close and night_time:
        print("hello")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Subject: Look Up\n\nISS is visible!")

while True:
    check_iss()
    time.sleep(60)