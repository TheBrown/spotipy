from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(URL)

response.raise_for_status()

billboard_website = response.text
soup = BeautifulSoup(billboard_website, "html.parser")

songs = [song.text.strip() for song in soup.select(selector="li h3[id=title-of-a-story]")]

top_100 = [f"{song}" for song in songs]
print(top_100)

scope = "playlist-modify-private"

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        cache_path="token.txt",
        scope=scope))

user_id = sp.current_user()["id"]

year = date.split("-")[0]
song_uris = []
for song in top_100:
    result = sp.search(q=f"track:{song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

