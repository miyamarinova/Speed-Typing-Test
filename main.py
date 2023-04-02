import random
from tkinter import *
from tkinter import messagebox
import threading
import time

BACKGROUND_COLOR = '#4D4D4D'
words = []

class Screen():
    def __init__(self):

        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry('800x500')
        self.words = []
        with open("words") as f:
            self.words = [line.rstrip() for line in f]

        self.entered_words = []
        self.displayed_words = []
        self.on_screen_words = []
        self.sec_var = 60
        self.running = False
        self.random_word = ''
        self.window.config(background=BACKGROUND_COLOR)

        self.title_label_0 = Label(text="MI|YA", bg=BACKGROUND_COLOR, font=('Arial', 15, "bold"), fg="white")
        self.title_label_01 = Label(text="Simplicity is beauty, functionality is strength", bg=BACKGROUND_COLOR,
                               font=('Arial', 10), fg="white")

        self.title_label_0.place(x=10, y=10)
        self.title_label_01.place(x=10, y=30)

        self.title_label_1 = Label(text='Typing Speed Test', bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 50, 'bold'), fg='white')
        self.title_label_1.place(x=50, y=50)

        self.info_wpm = Label(text=f'Speed: 0.00 CPS  0.00 WPS', bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 14),
                              fg='white')
        self.info_wpm.place(x=50, y=200)

        self.sec_var = 60

        self.timer = Label(text='TIME LEFT:', bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 14),
                           fg='white')
        self.timer.place(x=350, y=200)

        self.timer = Label(text=str(self.sec_var), bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 14),
                              fg='white')
        self.timer.place(x=440, y=200)

        self.reset_button = Button(self.window, text="Reset", command=self.reset, bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 14, 'bold'), fg=BACKGROUND_COLOR,width=5)
        self.reset_button.place(x=500,y=200)

        self.quit_button = Button(self.window, text="Quit", command=self.quit_game, bg=BACKGROUND_COLOR,
                                   font=('Roboto Mono.ttf', 14, 'bold'), fg=BACKGROUND_COLOR,width=5)
        self.quit_button.place(x=570, y=200)

        self.words_label = Label(self.window)
        self.words_label.config(text='Press Start to Begin', bg=BACKGROUND_COLOR, font=('Roboto Mono.ttf', 20, 'bold'), fg='white')
        self.words_label.place(x=50,y=250)

        self.words_entry = Entry(self.window, bg='white',fg=BACKGROUND_COLOR,font=('Roboto Mono.ttf', 20),width=55)
        self.words_entry.place(x=50, y=300)

        self.start_button = Button(self.window, text="Start", command=lambda: [self.start_timer(), threading.Thread(target=self.countdown_timer).start()], bg=BACKGROUND_COLOR,font=('Roboto Mono.ttf', 50, 'bold'), fg=BACKGROUND_COLOR)
        self.start_button.place(x=50, y=350)

        self.counter = 0
        self.running = False
        self.window.mainloop()

    def random_words(self):
        for _ in range(5):
            self.random_word = random.choice(self.words)
            self.displayed_words.append(self.random_word)
            self.on_screen_words.append(self.random_word)
            self.words.remove(self.random_word)
        self.words_label["text"] = " ".join(self.displayed_words)

    def next_words(self):
        self.displayed_words = []
        self.on_screen_words = []
        self.words_entry.delete(0, END)
        self.start_timer()

    def start_timer(self):
        self.start_button['state'] = 'disabled'
        self.running = True
        self.random_words()
        self.window.bind('<Return>', self.equal_words)

    def equal_words(self,e):
        displayed_words_str = ''.join(self.displayed_words)
        words_entry_str = ''.join(list(self.words_entry.get())).replace(" ", "")
        words_entry_str_no_spaces = words_entry_str.replace(" ", "")

        if displayed_words_str == words_entry_str:
            self.words_entry.config(fg='green')
            self.next_words()
        else:
            self.words_entry.config(fg='red')

    def countdown_timer(self):
        while self.sec_var > -1:
            self.sec_var -= 1
            self.timer.config(text=self.sec_var)
            time.sleep(1)
            self.counter += 0.1
            self.cps = len(self.words_entry.get()) / self.counter
            self.wps = len(self.words_entry.get().split(" ")) / self.counter
            self.info_wpm.config(text=f'Speed: {self.cps:.2f} CPS  {self.wps:.2f} WPS')
            if self.sec_var == 0:
                self.stop_app()
                break

    def stop_app(self):
        messagebox.askokcancel("New Try?", f"Your result: {self.cps:.2f} CPS  {self.wps:.2f} WPS")

    def reset(self):
        self.start_button['state'] = "normal"
        self.running = False
        self.sec_var = 61
        self.counter = 0
        self.info_wpm.config(text='Speed: 0.00 CPS  0.00 WPS')
        self.displayed_words = []
        self.on_screen_words = []
        self.words_entry.delete(0,END)
        self.completed_words = []
        self.start_timer()
        self.random_words()
        self.words_entry.delete(0, END)

    def quit_game(self):
        self.window.quit()

Screen()
