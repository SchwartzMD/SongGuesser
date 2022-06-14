# SongGuesser

This is a basic Python app that prompts a user with a song lyric and they guess which song the lyric comes from.
After guessing, there is an option to play the song on Spotify. 
When a user selects a year for the songs to come from, an API is utilized to get the billboard hot 100 list from a random day in that year.
Four songs are selected from the list and one is chosen as the correct one. Another API is used to get the lyrics for this correct song and a random line is chosen.
If the user selects random, each new lyric is taken from a different year.
The years go back to 1958 because this was the first full year that the hot 100 list was implemented.
