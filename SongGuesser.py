# NEW STUFF

from tkinter import *
from tkinter import ttk
import random
import requests as r
import json
from tkmacosx import Button


class SongGuesser(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (menuPage, guessPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(menuPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def getLyric():
    file = open('lyrics.json')
    lyrics = json.load(file)["message"]["body"]["lyrics"]["lyrics_body"]
    lyrics = lyrics[:-75]
    line = ""
    line_pick = random.randint(0, len(lyrics) - 12)

    while lyrics[line_pick] != "\n":
        line_pick -= 1
    line_pick += 1
    while lyrics[line_pick] != "\n":
        line = line + lyrics[line_pick]
        line_pick += 1
    return line


class guessPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        button = Button(self, text="Back to Menu",
                           command=lambda: [controller.show_frame(menuPage)]
                        )
        button.pack()
        self.answers = ["no", "no", "no", "no"]
        self.question = Label(self, text=getLyric())
        self.question.pack()
        self.answer1 = Button(self, bd=0,
                              text=self.answers[0][0] + " - " + self.answers[0][1].split(" feat.")[0],
                              command=self.check1)
        self.answer1.pack()
        self.answer2 = Button(self, bd=0,
                              text=self.answers[1][0] + " - " + self.answers[1][1].split(" feat.")[0],
                              command=self.check2)
        self.answer2.pack()
        self.answer3 = Button(self, bd=0,
                              text=self.answers[2][0] + " - " + self.answers[2][1].split(" feat.")[0],
                              command=self.check3)
        self.answer3.pack()
        self.answer4 = Button(self, bd=0,
                              text=self.answers[3][0] + " - " + self.answers[3][1].split(" feat.")[0],
                              command=self.check4)
        self.answer4.pack()

    def updateAnswers(self):
        self.answer1.config(text=self.answers[0][0] + " - " + self.answers[0][1].split(" feat.")[0],
                            bg="#F0F0F0"),
        self.answer2.config(text=self.answers[1][0] + " - " + self.answers[1][1].split(" feat.")[0],
                            bg="#F0F0F0"),
        self.answer3.config(text=self.answers[2][0] + " - " + self.answers[2][1].split(" feat.")[0],
                            bg="#F0F0F0"),
        self.answer4.config(text=self.answers[3][0] + " - " + self.answers[3][1].split(" feat.")[0],
                            bg="#F0F0F0")

    def check1(self, event=None):
        if self.correct == 0:
            self.answer1.config(bg="green")
        else:
            self.answer1.config(bg="red")

    def check2(self, event=None):
        if self.correct == 1:
            self.answer2.config(bg="green")
        else:
            self.answer2.config(bg="red")

    def check3(self, event=None):
        if self.correct == 2:
            self.answer3.config(bg="green")
        else:
            self.answer3.config(bg="red")

    def check4(self, event=None):
        if self.correct == 3:
            self.answer4.config(bg="green")
        else:
            self.answer4.config(bg="red")

    def pickCorrect(self):
        self.correct = random.randint(0,3)

    def updateLyric(self, event=None):
        self.question.config(text=getLyric())



    def pickSongs(self):
        file = open('songs.json')
        tracklist = []
        for x in json.load(file)["message"]["body"]["track_list"]:
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

        file = open('songs.json')
        tracklist = []
        for x in json.load(file)["message"]["body"]["track_list"]:
            if x["track"]["has_lyrics"] == 1:
                tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))

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
        self.answers = answers
        self.correct = correct
        print(self.answers)



class menuPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.label = Label(self, text="Song Guesser")
        self.label.pack()
        self.options = Frame(self)
        self.options.pack()
        genres = ('Hip Hop', 'Country', 'Pop', 'R&B', 'Rock', 'Any')
        genres_var = StringVar(value=genres)
        self.genreBox = Listbox(self.options, height=6, listvariable=genres_var, exportselection=0)
        decades = ('60\'s', '70\'s', '80\'s', '90\'s', '2000\'s', '2010\'s', '2020\'s', 'Any')
        decades_var = StringVar(value=decades)
        self.decadeBox = Listbox(self.options, height=8, listvariable=decades_var, exportselection=0)
        self.genre_label = Label(self.options, text = "Select a Genre:")
        self.decade_label = Label(self.options, text="Select a Decade:")
        self.genre_label.grid(column = 0, row = 0)
        self.decade_label.grid(column=1, row=0)
        self.genreBox.grid(column=0, row=1)
        self.decadeBox.grid(column=1, row=1)
        self.button = Button(self, text="Play!",
                        command=lambda: [self.guessPager()]
                        )
        #guessPage(parent, controller).pickSongs(), controller.show_frame(guessPage)
        self.button.pack()

    def guessPager(self):
        self.label.destroy()
        self.options.destroy()
        self.genreBox.destroy()
        self.decadeBox.destroy()
        self.genre_label.destroy()
        self.decade_label.destroy()
        self.button.destroy()


    def loadLyric(self):
        guessPage.updateLyric(self)




def getCorrect():
    file = open('songs.json')
    song = json.load(file)["message"]["body"]["lyrics"]["lyrics_body"]
    tracklist = []
    for x in json.load(file)["message"]["body"]["track_list"]:
        tracklist.append((x["track"]["track_name"], x["track"]["artist_name"]))
    print(tracklist)



"""random.shuffle(answers)
correct = random.randint(0, 3)"""

"""center_screen()
root.geometry('400x400')
# frame inside root window
top = Frame(root)
bottom = Frame(root, width=300)
top.pack()"""
# geometry method


# button inside frame which is
# inside root
"""question = Label(top, text="Ain't nothing but a heartache")
question.pack()"""

"""answer1 = Button(root, text='Who Let the Dogs Out', wraplength=150).place(x=25, y = 200)
answer2 = Button(root, text='I Want it That Way', wraplength=150).place(x=225, y = 200)
answer3 = Button(root, text="Gangsta's Paradise", wraplength=150).place(x=25, y = 300)
answer4 = Button(root, text='Jump', wraplength=150).place(x=225, y = 300)"""

"""answer1 = Button(bottom, text='Who Let the Dogs Out', wraplength=150)
answer2 = Button(bottom, text='I Want it That Way', wraplength=150, action=correct())
answer3 = Button(bottom, text="Gangsta's Paradise", wraplength=150)
answer4 = Button(bottom, text='Jump', wraplength=150)



bottom.pack()
answer1.grid(row=0, column=0)
answer2.grid(row=0, column=1)
answer3.grid(row=1, column=0)
answer4.grid(row=1, column=1)"""

# Radio Button??
# COMBOBOX
# MESSAGE WIDGET for warning
# Tkinter event loop

SongGuesser().mainloop()
