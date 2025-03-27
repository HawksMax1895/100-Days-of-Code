from bs4 import BeautifulSoup
import requests
import os
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv()

SPOTIPY_CLIENT_ID = os.environ.get("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

url = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url=f"{url}{date}", headers=header)
billboard = response.text

soup = BeautifulSoup(billboard, "html.parser")

titles = [song.getText().strip() for song in soup.select("li ul li h3")]

scope = "playlist-modify-private"
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, show_dialog=True)
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id =sp.me()["id"]

year = date.split("-")[0]
song_uris = []
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

title = f"Billboard Top 100 {date}"
playlist = sp.user_playlist_create(user_id, title, False, False, f"Playlist with the 100 Top songs from the Billboard Charts on {date}")

playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id, song_uris)

