import requests
import datetime

MY_LAT = 50.775345
MY_LNG = 6.083887
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()
#
# longitude = response.json()["iss_position"]["longitude"]
# latitude = response.json()["iss_position"]["latitude"]
#
# iss_position = (longitude, latitude)
# print(iss_position)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

response = requests.get(url=" https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
time_now = datetime.datetime.now()
print(response.json())
print(time_now)

print(sunrise.split("T")[1].split(":"))