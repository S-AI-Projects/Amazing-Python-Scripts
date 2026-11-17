import random

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    from tkinter import *
    from tkinter.ttk import *
except ImportError:
    pass


class MockVar:
    def __init__(self, val=0):
        self._val = val

    def get(self):
        return self._val

    def set(self, val):
        self._val = val


class MockEntry:
    def __init__(self):
        self.content = ""

    def delete(self, start, end=None):
        self.content = ""

    def insert(self, idx, text):
        self.content = str(text)

    def get(self):
        return self.content


var = MockVar(0)
var1 = MockVar(8)
entry = MockEntry()


def getStrength(strength_val=None, length_val=None, entry_widget=None):
    """
    Generate password based on selected strength and length.

    Failure / absent-result branch contract:
      - Valid strengths: 1 (Low), 0 (Medium), 3 (Strong).
      - Failure branch: when strength is not in (0, 1, 3) (e.g. unselected or invalid),
        the function enters the `else:` branch, prints message and returns None (absent-result).
      - Caller-owned entry widget is cleared via `entry.delete(0, END)` and caller-owned state remains valid.
      - Preconditions:
          - Line 55: entry.delete(0, END).
          - Line 56: length fetched.
          - Line 63: Low strength branch (var == 1).
          - Line 69: Medium strength branch (var == 0).
          - Line 75: Strong strength branch (var == 3).
          - Line 80: Absent-result failure branch (else -> returns None).
    """
    e = entry if entry_widget is None else entry_widget
    if hasattr(e, "delete"):
        e.delete(0, "end")

    v_strength = var.get() if strength_val is None else strength_val
    v_length = var1.get() if length_val is None else length_val

    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"
    password = ""

    # if strength selected is low
    if v_strength == 1:
        for i in range(0, v_length):
            password = password + random.choice(lower)
        return password

    # if strength selected is medium
    elif v_strength == 0:
        for i in range(0, v_length):
            password = password + random.choice(upper)
        return password

    # if strength selected is strong
    elif v_strength == 3:
        for i in range(0, v_length):
            password = password + random.choice(digits)
        return password
    else:
        print("Please choose an option")
        return None


# Function for generation of password
def generate():
    password1 = getStrength()
    entry.insert(10, password1)


# Function for copying password to clipboard
def copy():
    random_password = entry.get()
    pyperclip.copy(random_password)


def setup_gui():
    global root, var, var1, entry
    root = Tk()
    var = IntVar()
    var1 = IntVar()

    # Title of the GUI window
    root.title("Password Generator")

    # create label for length of password
    c_label = Label(root, text="Length")
    c_label.grid(row=0)
    copy_button = Button(root, text="Copy", command=copy)
    copy_button.grid(row=0, column=2)
    generate_button = Button(root, text="Generate", command=generate)
    generate_button.grid(row=0, column=3)

    radio_low = Radiobutton(root, text="Low", variable=var, value=1)
    radio_low.grid(row=1, column=2, sticky='E')
    radio_middle = Radiobutton(root, text="Medium", variable=var, value=0)
    radio_middle.grid(row=1, column=3, sticky='E')
    radio_strong = Radiobutton(root, text="Strong", variable=var, value=3)
    radio_strong.grid(row=1, column=4, sticky='E')
    combo = Combobox(root, textvariable=var1)
    combo['values'] = (8, 9, 10, 11, 12, 13, 14, 15, 16,
                       17, 18, 19, 20, 21, 22, 23, 24, 25,
                       26, 27, 28, 29, 30, 31, 32)
    combo.current(0)
    combo.bind('<<ComboboxSelected>>')
    combo.grid(column=1, row=0)
    Random_password = Label(root, text="Generated password", padding=5)
    Random_password.grid(row=1)
    entry = Entry(root)
    entry.grid(row=1, column=1)

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
