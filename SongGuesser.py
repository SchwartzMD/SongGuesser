# NEW STUFF

from tkinter import *
from tkinter import ttk
import random
import requests as r
import json
from tkmacosx import Button


class SongGuesser:
    def __init__(self, master):
        self.score = 0
        self.attempts = 0
        self.guess = False
        self.menuPage = Frame(root)
        self.menuPage.pack()
        self.label = Label(self.menuPage, text="Song Guesser")
        self.label.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        genres = ('Hip Hop', 'Country', 'Pop', 'R&B', 'Rock', 'Any')
        genres_var = StringVar(value=genres)
        self.genreBox = Listbox(self.options, height=6, listvariable=genres_var, exportselection=0)
        decades = ('60\'s', '70\'s', '80\'s', '90\'s', '2000\'s', '2010\'s', '2020\'s', 'Any')
        decades_var = StringVar(value=decades)
        self.decadeBox = Listbox(self.options, height=8, listvariable=decades_var, exportselection=0)
        self.genre_label = Label(self.options, text="Select a Genre:")
        self.decade_label = Label(self.options, text="Select a Decade:")
        self.genre_label.grid(column=0, row=0)
        self.decade_label.grid(column=1, row=0)
        self.genreBox.grid(column=0, row=1)
        self.decadeBox.grid(column=1, row=1)
        self.button = Button(self.menuPage, text="Play!",
                             command=lambda: [self.guessPager()]
                             )
        # guessPage(parent, controller).pickSongs(), controller.show_frame(guessPage)
        self.button.pack()

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

    def menuPager(self):
        self.score = 0
        self.attempts = 0
        self.guessPage.destroy()
        self.menuPage = Frame(root)
        self.menuPage.pack()
        self.label = Label(self.menuPage, text="Song Guesser")
        self.label.pack()
        self.options = Frame(self.menuPage)
        self.options.pack()
        genres = ('Hip Hop', 'Country', 'Pop', 'R&B', 'Rock', 'Any')
        genres_var = StringVar(value=genres)
        self.genreBox = Listbox(self.options, height=6, listvariable=genres_var, exportselection=0)
        decades = ('60\'s', '70\'s', '80\'s', '90\'s', '2000\'s', '2010\'s', '2020\'s', 'Any')
        decades_var = StringVar(value=decades)
        self.decadeBox = Listbox(self.options, height=8, listvariable=decades_var, exportselection=0)
        self.genre_label = Label(self.options, text="Select a Genre:")
        self.decade_label = Label(self.options, text="Select a Decade:")
        self.genre_label.grid(column=0, row=0)
        self.decade_label.grid(column=1, row=0)
        self.genreBox.grid(column=0, row=1)
        self.decadeBox.grid(column=1, row=1)
        self.button = Button(self.menuPage, text="Play!",
                             command=lambda: [self.guessPager()]
                             )
        # guessPage(parent, controller).pickSongs(), controller.show_frame(guessPage)
        self.button.pack()

    def pickSongs(self):
        file = open('songs.json')
        tracklist = []
        for x in json.load(file)["message"]["body"]["track_list"]:
            if x["track"]["has_lyrics"] == 1:
                tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))

        rands = []
        for x in range(0, len(tracklist)):
            rands.append(x)
        random.shuffle(rands)
        rands = rands[:4]
        correct = random.randint(0, 3)

        answers = []
        for x in rands:
            track = tracklist[x][0]
            artist = tracklist[x][1]
            answers.append((track, artist))

        track = answers[correct][0]
        artist = answers[correct][1]
        api_track = track.replace(" ", "%20").lower()
        api_artist = artist.replace(" ", "%20").lower()
        print(track, artist)
        api_key = "&apikey=51abcf5782652100f10c6c2da5f3dae2"

        track_call = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?" \
                     "q_track=" + api_track + "&q_artist=" + api_artist + api_key

        response = r.get(track_call)
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
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
            else:
                self.answer1.config(bg="red")
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        self.guess = True

    def check2(self, event=None):
        if not self.guess:
            if self.correct == 1:
                self.answer2.config(bg="green")
                self.score += 1
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
            else:
                self.answer2.config(bg="red")
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        self.guess = True

    def check3(self, event=None):
        if not self.guess:
            if self.correct == 2:
                self.answer3.config(bg="green")
                self.score += 1
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
            else:
                self.answer3.config(bg="red")
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        self.guess = True

    def check4(self, event=None):
        if not self.guess:
            if self.correct == 3:
                self.answer4.config(bg="green")
                self.score += 1
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
            else:
                self.answer4.config(bg="red")
                self.attempts += 1
                self.score_display.config(text="Score: " + str(self.score) + "/" + str(self.attempts))
        self.guess = True


def getCorrect():
    file = open('songs.json')
    song = json.load(file)["message"]["body"]["lyrics"]["lyrics_body"]
    tracklist = []
    for x in json.load(file)["message"]["body"]["track_list"]:
        tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))
    print(tracklist)


# Radio Button??
# COMBOBOX
# MESSAGE WIDGET for warning

# Tkinter event loop
if __name__ == "__main__":
    root = Tk()
    root.title('Song Guesser')
    root.eval('tk::PlaceWindow . center')
    mainWindow = SongGuesser(root)
    root.mainloop()
