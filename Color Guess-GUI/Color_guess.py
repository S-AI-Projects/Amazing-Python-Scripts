import random
import tkinter

colors_name = ['Red', 'White', 'Yellow', 'Pink',
               'Blue', 'Black', 'Brown', 'Purple', 'Green', 'Cyan']
score = 0
time_left = 60


def start_game(play=None):
    """Start or advance the color guessing game.

    Contract & Branch Coverage:
    - Precondition Anchor: `colors_name` defined at lines 4-5.
    - Precondition Anchor: `score = 0` (line 6), `time_left = 60` (line 7).
    - Active Branch (Line 11): `if time_left == 60:` triggers `countdown()` (Line 12).
    - Absent-Result / Expired Branch (Line 19 in change_color):
      When `time_left <= 0` (e.g. 0), `if (time_left > 0):` evaluates to False.
      The absent-result fallback is taken: returns None without mutating score,
      entry text, labels, or color sequence.
    - Rejection / Incorrect Guess Branch (Line 21 in change_color):
      When `e.get().lower() != colors_name[1].lower()`, score does not increment.
    """
    if time_left == 60:
        countdown()
    change_color()


def change_color():
    global score
    global time_left
    if (time_left > 0):
        e.focus_set()
        if e.get().lower() == colors_name[1].lower():
            score += 1

        e.delete(0, tkinter.END)
        random.shuffle(colors_name)
        label.config(fg=str(colors_name[1]), text=str(colors_name[0]))
        scoreLabel.config(text="Score: "+str(score))


def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        timeLabel.config(text='Time Left: '+str(time_left))
        timeLabel.after(1000, countdown)


class DummyWidget:
    """Lightweight widget interface for headless test isolation and mock execution."""

    def __init__(self, text=""):
        self.text = text
        self.fg = ""
        self.focused = False
        self.after_calls = []

    def config(self, **kwargs):
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'fg' in kwargs:
            self.fg = kwargs['fg']

    def after(self, ms, func):
        self.after_calls.append((ms, func))

    def focus_set(self):
        self.focused = True

    def get(self):
        return self.text

    def delete(self, start, end):
        self.text = ""


# Fallback widget instances for headless environments and module imports
root = None
instruct = DummyWidget("Which Color?")
scoreLabel = DummyWidget("Press Enter to Start")
timeLabel = DummyWidget("Time Left: 60")
label = DummyWidget()
e = DummyWidget()


def init_gui(tk_root=None):
    """Initialize real Tkinter GUI widgets."""
    global root, instruct, scoreLabel, timeLabel, label, e
    if tk_root is not None:
        root = tk_root
    else:
        root = tkinter.Tk()
    root.title("The ColorGuess")
    root.geometry("600x400")

    instruct = tkinter.Label(root, text="Which Color?", font=("san-serif", 30))
    instruct.pack()

    scoreLabel = tkinter.Label(
        root, text="Press Enter to Start", font=("san-serif", 24))
    scoreLabel.pack()

    timeLabel = tkinter.Label(root, text="Time Left: " +
                              str(time_left), font=("san-serif", 18))
    timeLabel.pack()

    label = tkinter.Label(root, font=("san-serif", 60))
    label.pack()

    e = tkinter.Entry(root)
    root.bind('<Return>', start_game)
    e.pack()
    e.focus_set()
    return root


if __name__ == '__main__':
    root = init_gui()
    root.mainloop()
