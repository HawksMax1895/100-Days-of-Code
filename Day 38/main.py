import os
import dotenv
import requests
from datetime import datetime

dotenv.load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_URL = os.environ.get("SHEETY_URL")
TOKEN = os.environ.get("TOKEN")

activity = input("Tell me which exercises you did: ")

url = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

params = {
    "query": activity,
    "weight_kg": 94,
    "height_cm": 190,
    "age": 27,
    "gender": "male"
}

response = requests.post(url=url, json=params, headers=headers)
response.raise_for_status()

exercises_data = response.json()["exercises"]

today = datetime.today()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

for exercise_item in exercises_data:
    exercise = exercise_item["name"]
    duration = exercise_item["duration_min"]
    calories = exercise_item["nf_calories"]

    sheety_header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    workout_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise.title(),
            "duration": duration,
            "calories": calories,
        }
    }

    google_response = requests.post(url=SHEETY_URL, json=workout_params, headers=sheety_header)
    google_response.raise_for_status()
    print(google_response.text)
