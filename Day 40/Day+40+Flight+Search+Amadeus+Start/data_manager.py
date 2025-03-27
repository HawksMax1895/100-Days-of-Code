import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DataManager:

    def __init__(self):
        self.prices_endpoint = os.environ.get("SHEETY_URL")
        self.users_endpoint = os.environ.get("SHEETY_USER_URL")
        self.token = SHEETY_TOKEN= os.environ.get("SHEETY_TOKEN")
        self.destination_data = {}
        self.customer_data ={}
        self.header ={"Authorization": f"Bearer {SHEETY_TOKEN}"}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=self.prices_endpoint, headers=self.header)
        data = response.json()
        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{self.prices_endpoint}/{city['id']}", json=new_data, headers=self.header)
            print(response.text)

    def get_customer_email(self):
        response = requests.get(url=self.users_endpoint, headers=self.header)
        self.customer_data = response.json()["users"]
        return self.customer_data
