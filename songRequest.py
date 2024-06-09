import requests as r
import json

track = "my nigga"
artist = "yg"
print(track)
print(track.replace(" ", "%20").lower())
api_track = track.replace(" ", "%20").lower()
api_artist = artist.replace(" ", "%20").lower()

api_key = "&apikey=51abcf5782652100f10c6c2da5f3dae2"

track_call = "http://api.musixmatch.com/ws/1.1/chart.tracks.get?" \
             "chart_name=top" + "&page=1&page_size=500" + "&country=us" + "&f_has_lyrics=1" + api_key

response = r.get(track_call)
print(response.json())

jake = response.json()
with open('songs.json', 'w') as outfile:
    json.dump(response.json(), outfile)