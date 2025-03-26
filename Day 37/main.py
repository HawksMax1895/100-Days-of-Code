import requests
import os
import dotenv

dotenv.load_dotenv()

USERNAME = "radimax"
TOKEN = os.environ.get("PIXELA_TOKEN")

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}


# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_params = {
    "id": "graph1",
    "name": "Workout Graph",
    "unit": "Km",
    "type": "float",
    "color": "sora",
}

requests.post(url=graph_endpoint, json=graph_params)
