# SongGuesser

This is a basic Python app that prompts a user with a song lyric and they guess which song the lyric comes from.

After guessing, there is an option to play the song on Spotify. 

When a user selects a year for the songs to come from, an API is utilized to get the billboard hot 100 list from a random day in that year.

Four songs are selected from the list and one is chosen as the correct one. Another API is used to get the lyrics for this correct song and a random line is chosen.

If the user selects random, each new lyric is taken from a different year.

The years go back to 1958 because this was the first full year that the hot 100 list was implemented.


## Running the Program

To run the SongGuesser application, follow these steps:

1. **Prerequisites**: Ensure you have Python 3.x installed on your system.
2. **Install Dependencies**: Open a terminal and navigate to the project directory. Run the following command to install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. **Spotify Playback** (optional):
   - To enable Spotify playback, ensure you have an active Spotify application running on your device. No Spotify Developer account or API setup is required.
   
4. **Run the Program**: In the terminal, execute the following command:
   ```
   python SongGuesser.py
   ```
5. **Interact with the GUI**: A window will appear where you can select the game mode (e.g., guess the song, lyric, or band), choose a year or "Random," and click "Play!" to start the game.
