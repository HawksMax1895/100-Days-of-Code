import os
import dotenv
import requests

dotenv.load_dotenv()

SHEETY_ENDPOINT=os.environ.get("SHEETY_URL")
SHEETY_TOKEN= os.environ.get("SHEETY_TOKEN")

headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=headers)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for cities in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": cities["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{cities['id']}", json=new_data, headers=headers)


