import spotipy
from spotipy.oauth2 import SpotifyOAuth

song = "Calling America"
artist = 'Electric Light Orchestra'

scope = 'user-modify-playback-state'
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
if "B**ch!" in song:
    song = song.replace("**", "it")
track = spotify.search(song + " " + artist, type="track", limit=10)["tracks"]["items"]
if not track:
    track = spotify.search(song, type="track", limit=10)["tracks"]["items"]
uri = track[0]["uri"]
print(track[0]['artists'][0]['name'])
#spotify.start_playback(uris=[uri])
#for x in spotify.search("track:Everyday", type="track",limit=10)["tracks"]["items"]["uri"][0]:
 #   print(x)
