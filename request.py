"""from musixmatch import Musixmatch

musixmatch = Musixmatch('51abcf5782652100f10c6c2da5f3dae2')

print(musixmatch.track_search('Snow','Red Hot Chili Peppers', 10, 1, 'dec'))"""

import requests as r
import json
import random

file = open('songs.json')
tracklist = []
for x in json.load(file)["message"]["body"]["track_list"]:
    tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))
print(tracklist)

selection = random.randint(0, len(tracklist)-1)
track = tracklist[selection][0]
artist = tracklist[selection][1]
print(track.replace(" ", "%20").lower())
api_track = track.replace(" ", "%20").lower()
api_artist = artist.replace(" ", "%20").lower()

api_key = "&apikey=51abcf5782652100f10c6c2da5f3dae2"

track_call = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?" \
             "q_track=" + api_track + "&q_artist=" + api_artist + api_key

response = r.get(track_call)
print(response.json())

jake = response.json()
with open('lyrics.json', 'w') as outfile:
    json.dump(response.json(), outfile)
