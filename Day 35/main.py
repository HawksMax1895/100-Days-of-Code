import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
print(api_key)

lat = 50.76693006338142
lon = 6.094452156110828

weather = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={'lat': lat, 'lon': lon, 'cnt': 4, 'appid': api_key})
weather.raise_for_status()
forecast = weather.json()['list']

forecast_weather = []

for entry in forecast:
    if entry['weather'][0]['id'] < 600:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body="It's going to rain today. Remember to bring an umbrella today",
            from_="+12315946472",
            to="+4917645999428",
        )

        print(message.body)
        break


