import requests
import os
import dotenv
from datetime import datetime

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

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.put(url=graph_endpoint, json=graph_params, headers=headers)
# print(response.text)

pixel_endpoint = f"{graph_endpoint}/graph1"

today = datetime.today().strftime("%Y%m%d")
print(today)

pixel_params = {
    "date": today,
    "quantity": "10",
}
# response = requests.post(pixel_endpoint, json=pixel_params, headers=headers)
# print(response.text)

graph_params_update = {
    "unit": "min",
    "color": "momiji",
}

# response = requests.put(pixel_endpoint, json=graph_params_update, headers=headers)
# print(response.text)

delete_endpoint = f"{pixel_endpoint}/{today}"

response = requests.delete(delete_endpoint, headers=headers)
print(response.text)



