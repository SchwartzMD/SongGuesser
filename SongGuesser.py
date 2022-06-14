from tkinter import *
from tkinter import ttk
import random
import requests as r
import json
from tkmacosx import Button
from microservice import randomize_client
import billboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk

class SongGuesser:
    def __init__(self, master):
        self.year = None
        self.score = 0
        self.attempts = 0
        self.guess = False
        self.menuPage = Frame(root)
        self.menuPage.pack()
        self.label = Label(self.menuPage, text="Song Guesser")
        self.label.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        self.years = list(range(1959,2022))
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
                               command=lambda: [self.getDecade(), self.guessPager()]
                               )
        # guessPage(parent, controller).pickSongs(), controller.show_frame(guessPage)
        self.new_game.pack()

    def menuPager(self):
        self.guessPage.destroy()
        self.menuPage = Frame(root)
        self.menuPage.pack()
        self.label = Label(self.menuPage, text="Song Guesser")
        self.label.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        years = list(range(1958,2022))
        years.append("Random")
        years.reverse()
        self.decadeBox = ttk.Combobox(self.options, values = years)
        self.decadeBox.current(years.index(self.year))
        self.decade_label = Label(self.options, text="Select a Year:")
        self.decade_label.grid(column=1, row=0)
        self.decadeBox.grid(column=1, row=1)
        self.buttons = Frame(root)
        self.new_game = Button(self.menuPage, text="New Game",
                               command=lambda: [self.getDecade(), self.resetScore(), self.guessPager()]
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
        self.guess = False
        self.answers = key[0]
        self.correct = key[1]
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
                              command=lambda: [self.check1(),
                                               self.next_prompt()])
        self.answer1.pack()
        self.answer2 = Button(self.question, bd=0,
                              text=self.answers[1][0] + " - " + self.answers[1][1].split(" feat.")[0],
                              command=lambda: [self.check2(),
                                               self.next_prompt()])
        self.answer2.pack()
        self.answer3 = Button(self.question, bd=0,
                              text=self.answers[2][0] + " - " + self.answers[2][1].split(" feat.")[0],
                              command=lambda: [self.check3(),
                                               self.next_prompt()])
        self.answer3.pack()
        self.answer4 = Button(self.question, bd=0,
                              text=self.answers[3][0] + " - " + self.answers[3][1].split(" feat.")[0],
                              command=lambda: [self.check4(),
                                               self.next_prompt()])
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

    def getDecade(self):
        self.year = (self.years[self.decadeBox.current()])

    def getSongs(self):
        month= ["01","02",'03','04','05','06','07','08','09','10','11','12']
        day = ['01', '02', '03', '04', '05', '06', '07','08','09']
        for x in range(10,29):
            day.append(str(x))
        if self.year == "Random":
            self.date = str(random.choice(self.years)) + '-' + str(
                random.choice(month)) + '-' + str(
                random.choice(day))
        else:
            self.date = str(self.year) + '-' + str(random.choice(month)) + '-' + str(
                random.choice(day))
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

    def check1(self, event=None):
        if not self.guess:
            if self.correct == 0:
                self.answer1.config(bg="green")
                self.score += 1
            else:
                self.answer1.config(bg="red")
                self.guess = True
                self.check2()
                self.check3()
                self.check4()
            self.attempts += 1
            self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        if self.correct == 0:
            self.answer1.config(bg="green")
        self.guess = True

    def check2(self, event=None):
        if not self.guess:
            if self.correct == 1:
                self.answer2.config(bg="green")
                self.score += 1
                self.guess = True
            else:
                self.answer2.config(bg="red")
                self.guess = True
                self.check1()
                self.check3()
                self.check4()
            self.attempts += 1
            self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        if self.correct == 1:
            self.answer2.config(bg="green")

    def check3(self, event=None):
        if not self.guess:
            if self.correct == 2:
                self.answer3.config(bg="green")
                self.score += 1
                self.guess = True
            else:
                self.answer3.config(bg="red")
                self.guess = True
                self.check1()
                self.check2()
                self.check4()
            self.attempts += 1
            self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        if self.correct == 2:
            self.answer3.config(bg="green")

    def check4(self, event=None):
        if not self.guess:
            if self.correct == 3:
                self.answer4.config(bg="green")
                self.score += 1
                self.guess = True
            else:
                self.answer4.config(bg="red")
                self.guess = True
                self.check1()
                self.check2()
                self.check3()
            self.attempts += 1
            self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        if self.correct == 3:
            self.answer4.config(bg="green")

    def playSong(self):
        scope = 'user-modify-playback-state'
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        track = spotify.search(self.track + " " + self.artist, type="track", limit=10)["tracks"]["items"]
        if not track:
            track = spotify.search(self.track, type="track", limit=10)["tracks"]["items"]
        uri = track[0]["uri"]
        spotify.start_playback(uris=[uri])


# Tkinter event loop
if __name__ == "__main__":
    root = Tk()
    root.title('Song Guesser')
    root.eval('tk::PlaceWindow . center')
    mainWindow = SongGuesser(root)
    root.mainloop()
