import requests
import os
from twilio.rest import Client

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

lat = 50.76693006338142
lon = 6.094452156110828
print(api_key)

weather = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={'lat': lat, 'lon': lon, 'cnt': 4, 'appid': api_key})
weather.raise_for_status()
forecast = weather.json()['list']

forecast_weather = []

for entry in forecast:
    if entry['weather'][0]['id'] < 600:
        #print("Rain")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="It's going to rain today. Remember to bring an umbrella today",
            from_=os.environ.get("FROM_NUMBER"),
            to=os.environ.get("TO_NUMBER"),
        )

        print(message.body)
        break


