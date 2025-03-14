from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import requests as r
import json
from tkmacosx import Button
import billboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk
from datetime import datetime

class SongGuesser:
    def __init__(self, master):
        self.answerGuessed = False
        self.year = None
        self.score, self.attempts = 0,0
        self.remainingScore = 1
        self.menuPage = Frame(root)
        self.menuPage.pack()
        self.answerLabel = Label(self.menuPage, text="I want to guess the:")
        self.answerLabel.pack()
        self.answerBox = ttk.Combobox(self.menuPage, values=["Song", "Lyric", "Band"])
        self.answerBox.current(0)
        self.answerBox.pack()
        self.gameSelection = Frame(self.menuPage)
        self.gameSelection.pack()
        self.questionLabel = Label(self.gameSelection, text="Based on the:")
        self.questionLabel.pack()
        self.questionBox = ttk.Combobox(self.menuPage, values=["Song", "Lyric", "Band"])
        self.questionBox.current(1)
        self.questionBox.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        self.years = list(range(1959,datetime.now().year+1))
        self.years.append("Random")
        self.years.reverse()
        decades = ('Any','60\'s', '70\'s', '80\'s', '90\'s', '2000\'s', '2010\'s', '2020\'s')
        decades_var = StringVar(value=self.years)
        self.decadeBox = ttk.Combobox(self.options, values=self.years)
        self.decadeBox.current(0)
        self.decade_label = Label(self.options, text="Select a year:")
        self.decade_label.grid(column=1, row=0)
        self.decadeBox.grid(column=1, row=1)
        self.new_game = Button(self.menuPage, text="Play!",
                               command=lambda: [self.getDecade(), self.getQuestionAnswer(), self.guessPager()]
                               )
        # guessPage(parent, controller).pickSongs(), controller.show_frame(guessPage)
        self.new_game.pack()

    def menuPager(self):
        self.guessPage.destroy()
        self.menuPage = Frame(root)
        self.menuPage.pack()
        # self.label = Label(self.menuPage, text="Song Guesser")
        # self.label.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        years = list(range(1958,datetime.now().year+1))
        years.append("Random")
        years.reverse()
        self.decadeBox = ttk.Combobox(self.options, values = years)
        self.decadeBox.current(years.index(self.year))
        self.decade_label = Label(self.options, text="Select a Year:")
        self.decade_label.grid(column=1, row=0)
        self.decadeBox.grid(column=1, row=1)
        self.buttons = Frame(root)
        self.new_game = Button(self.menuPage, text="New Game",
                               command=lambda: [self.getDecade(), self.resetScore(), self.getQuestionAnswer(), self.guessPager()]
                               )
        self.new_game.pack()
        self.resume = Button(self.menuPage, text="Resume",
                               command=lambda: [self.guessPager()]
                               )

        self.resume.pack()

    def resetScore(self):
        self.score = 0
        self.attempts = 0

    def guessPager(self):
        key = self.pickSongs()
        self.answers = key[0]
        self.correct = key[1]
        self.answerGuessed = False
        self.menuPage.destroy()
        self.guessPage = Frame(root)
        self.guessPage.pack()
        self.nav = Frame(self.guessPage)
        self.nav.pack()
        self.spotButt = Frame(self.guessPage)
        self.spotButt.pack()
        self.question = Frame(self.guessPage)
        self.question.pack()
        back_button = Button(self.nav, text="Back to Menu",
                             command=lambda: [self.menuPager()]
                             )
        back_button.grid(column=0, row=0)
        self.prompt = Label(self.question, text=self.getLyric())
        self.prompt.pack()
        self.answer1 = Button(self.question, bd=0,
                              text=self.answers[0][0] + " - " + self.answers[0][1].split(" feat.")[0],
                              command=lambda: [self._handle_guess(0, self.answer1)])
        self.answer1.pack()
        self.answer2 = Button(self.question, bd=0,
                              text=self.answers[1][0] + " - " + self.answers[1][1].split(" feat.")[0],
                              command=lambda: [self._handle_guess(1, self.answer2)])
        self.answer2.pack()
        self.answer3 = Button(self.question, bd=0,
                              text=self.answers[2][0] + " - " + self.answers[2][1].split(" feat.")[0],
                              command=lambda: [self._handle_guess(2, self.answer3)])
        self.answer3.pack()
        self.answer4 = Button(self.question, bd=0,
                              text=self.answers[3][0] + " - " + self.answers[3][1].split(" feat.")[0],
                              command=lambda: [self._handle_guess(3, self.answer4)])
        self.answer4.pack()
        self.score_display = Label(self.guessPage,
                                   text="Score: " + str(self.score) + "/" + str(self.attempts))
        self.score_display.pack()

    def next_prompt(self):
        next_button = Button(self.nav, text="Next",
                             command=lambda: [self.guessPage.destroy(), self.guessPager()])
        next_button.grid(column=1, row=0)
        logoimage = Image.open("spotify-logo-png-7057.png")
        logoimage = logoimage.resize((21,21))
        logoimage = ImageTk.PhotoImage(logoimage)
        play_button = Button(self.spotButt, text = 'Play on Spotify', image = logoimage, compound = LEFT,
                             command=lambda: [self.playSong()])
        play_button.pack()

    def getQuestionAnswer(self):
        self.questionChoice = self.questionBox.current()
        self.answerChoice = self.answerBox.current()

    def getDecade(self):
        self.year = (self.years[self.decadeBox.current()])

    def getSongs(self):
        month = []
        day = []
        monthRange = 12
        dayRange = 28


        if self.year == "Random":
            self.year = random.choice(self.years)

        if self.year == datetime.now().year:
            monthRange = datetime.now().month
            dayRange = datetime.now().day

        for x in range(1,monthRange+1):
            if x < 10:
                month.append("0" + str(x))
            else:
                month.append(str(x))
        for x in range(1,dayRange+1):
            if x < 10:
                day.append("0" + str(x))
            else:
                day.append(str(x))

        self.date = str(self.year) + '-' + str(random.choice(month)) + '-' + str(random.choice(day))
        self.chart = billboard.ChartData('hot-100', self.date)
        return self.chart

    def pickSongs(self):
        tracklist = self.getSongs()
        rands = []
        for x in range(0, len(tracklist)):
            rands.append(x)
        random.shuffle(rands)
        rands = rands[:4]
        choices = [0,1,2,3]
        correct = random.choice(choices)
        choices.remove(correct)
        answers = []
        for x in rands:
            track = tracklist[x].title
            artist = tracklist[x].artist
            answers.append((track, artist))
        self.track = answers[correct][0]
        self.artist = answers[correct][1]
        api_track = self.track.replace(" ", "%20").lower()
        api_artist = self.artist.replace(" ", "%20").lower()
        api_key = "&apikey=51abcf5782652100f10c6c2da5f3dae2"

        track_call = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?" \
                     "q_track=" + api_track + "&q_artist=" + api_artist + api_key

        response = r.get(track_call)
        if response.json()["message"]["header"]["status_code"] != 404:
            lyrics = response.json()["message"]["body"]["lyrics"]["lyrics_body"]

        while (response.json()["message"]["header"]["status_code"] != 200) or (lyrics == ""):
            correct = random.choice(choices)
            choices.remove(correct)
            self.track = answers[correct][0]
            self.artist = answers[correct][1]
            api_track = self.track.replace(" ", "%20").lower()
            api_artist = self.artist.replace(" ", "%20").lower()
            print(self.track, self.artist)
            api_key = "&apikey=51abcf5782652100f10c6c2da5f3dae2"

            track_call = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?" \
                         "q_track=" + api_track + "&q_artist=" + api_artist + api_key
            response = r.get(track_call)
            if response.json()["message"]["header"]["status_code"] != 404:
                lyrics = response.json()["message"]["body"]["lyrics"]["lyrics_body"]
        with open('lyrics.json', 'w') as outfile:
            json.dump(response.json(), outfile)
        return answers, correct

    def getLyric(self):
        file = open('lyrics.json')
        lyrics = json.load(file)["message"]["body"]["lyrics"]["lyrics_body"]
        lyrics = lyrics[:-74]
        line = ""
        line_pick = random.randint(0, len(lyrics) - 2)
        while lyrics[line_pick] != "\n":
            line_pick -= 1
        line_pick += 1
        while lyrics[line_pick] != "\n":
            line = line + lyrics[line_pick]
            line_pick += 1
        return line
    
    def wrongGuess(self):
        if not self.answerGuessed:
            lowerScore = {1:0.5, 0.50:0.25, 0.25:0}
            self.remainingScore = lowerScore[self.remainingScore]
            
    def correctGuess(self):
        self.score += self.remainingScore
        self.remainingScore = 1
        self.attempts += 1
        self.answerGuessed = True

    def _handle_guess(self, button_index, button_widget):
        if self.answerGuessed:
            return
        
        self.answer_buttons = [self.answer1, self.answer2, self.answer3, self.answer4]
        
        is_correct = self.correct == button_index
        button_color = "green" if is_correct else "red"
        button_widget.config(bg=button_color)
        
        if is_correct:
            self.correctGuess()
            self.next_prompt()
        else:
            self.wrongGuess()
            if self.remainingScore == 0:
                self.correctGuess()
                self.next_prompt()
                self.answer_buttons[self.correct].config(bg="green")
                
        self.score_display.config(text=f"Score: {self.score}/{self.attempts}")


    def playSong(self):
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-modify-playback-state'))
        track = spotify.search(self.track + " " + self.artist, type="track", limit=10)["tracks"]["items"]
        if not track:
            track = spotify.search(self.track, type="track", limit=10)["tracks"]["items"]
        uri = track[0]["uri"]
        try:
            spotify.start_playback(uris=[uri])
        except:
            messagebox.showerror("Spotify Not Active", "Your Spotify player is not active. Please interact with your Spotify app to enable song playing.")


# Tkinter event loop
if __name__ == "__main__":
    root = Tk()
    root.title('Song Guesser')
    root.eval('tk::PlaceWindow . center')
    mainWindow = SongGuesser(root)
    root.mainloop()
