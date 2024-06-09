import random
import json

"""file = open('songs.json')
tracklist = []
for x in json.load(file)["message"]["body"]["track_list"]:
    if x["track"]["has_lyrics"] == 1:
        tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))
print(tracklist)
"""

artist = "Stephanie Beatriz feat. Olga Merediz & Encanto - Cast"
artist.split("feat.")
print(artist.split(" feat.")[0])