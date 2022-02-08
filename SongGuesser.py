from tkinter import *
from tkinter import ttk
import random
answers = [("Who Let the Dogs Out", "Who Let the Dogs Out"),
           ("Ain't Nothin' but a Heartache", "I Want it That Way"),
           ("We've been spending most our lives", "Gangsta's Paradise"),
            ("One and One and One is three", "Come Together"),
           ("Lyric2", "Song2"),
           ("Lyric3", "Song3")]
for x in range(100):
    answers.append(("Lyric"+str(x), "Song"+str(x)))
random.shuffle(answers)
correct = random.randint(0,3)

# create root window
class myWindow:
    def __init__(self, master):
        self.top = Frame(root)
        self.top.pack()
        self.question = Label(self.top, text=answers[correct][0])
        self.question.pack()
        self.bottom = Frame(root, width=300)
        self.answer1 = Button(self.bottom, text=answers[0][1], wraplength=150, command=self.check1)
        self.answer1.grid(row=0, column=0)
        self.answer2 = Button(self.bottom, text=answers[1][1], wraplength=150, command=self.check2)
        self.answer2.grid(row=0, column=1)
        self.answer3 = Button(self.bottom, text=answers[2][1], wraplength=150, command=self.check3)
        self.answer3.grid(row=1, column=0)
        self.answer4 = Button(self.bottom, text=answers[3][1], wraplength=150, command=self.check4)
        self.answer4.grid(row=1, column=1)
        self.bottom.pack()

    def check1(self, event=None):
        if correct == 0:
            self.question.config(text='Correct!')
    def check2(self, event=None):
        if correct == 1:
            self.question.config(text='Correct!')
    def check3(self, event=None):
        if correct == 2:
            self.question.config(text='Correct!')
    def check4(self, event=None):
        if correct == 3:
            self.question.config(text='Correct!')


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


if __name__ == "__main__":
    root = Tk()
    root.title('Song Guesser')
    root.eval('tk::PlaceWindow . center')
    mainWindow = myWindow(root)
    root.mainloop()
