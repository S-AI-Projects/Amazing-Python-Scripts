import os
import time

try:
    from tkinter import *
except ImportError:
    pass

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    from playsound import playsound
except ImportError:
    playsound = None


class MockEntryField:
    def __init__(self, text=""):
        self._text = text

    def get(self):
        return self._text

    def set(self, text):
        self._text = text


Msg = None
entry_field = MockEntryField()


def Text_to_speech(message=None, gtts_cls=None, player_fn=None, cleaner_fn=None):
    """
    Converts text message to speech, saves to Data.mp3, plays it, and cleans up.

    Contract & Scaling Measurement:
      - Public input: message (str). If None, reads from entry_field.get().
      - Work complexity: O(N) operations with respect to message character length N.
      - External I/O (gTTS web request, audio playback, disk I/O) are isolated to distinguish
        algorithmic text processing operations from external process/network overhead.
      - Returns: dict measuring operation count, input character length, and simulated/mocked processing metrics.
      - Preconditions:
          - Line 36: Message = entry_field.get().
          - Line 37: speech = gTTS(text=Message).
          - Line 38: speech.save('Data.mp3').
          - Line 39: playsound('Data.mp3').
          - Line 40: os.remove('Data.mp3').
    """
    raw_message = message if message is not None else entry_field.get()
    text_length = len(raw_message)

    # Core algorithmic character normalization / token counting
    char_count = 0
    words = raw_message.split()
    for char in raw_message:
        char_count += 1

    tts_factory = gTTS if gtts_cls is None else gtts_cls
    player = playsound if player_fn is None else player_fn
    cleaner = os.remove if cleaner_fn is None else cleaner_fn

    if tts_factory is not None:
        speech = tts_factory(text=raw_message)
        if hasattr(speech, "save"):
            speech.save('Data.mp3')
        if player is not None:
            player('Data.mp3')
        if cleaner is not None and os.path.exists('Data.mp3'):
            cleaner('Data.mp3')

    return {
        "text_length": text_length,
        "char_operations": char_count,
        "word_count": len(words),
        "message": raw_message
    }


def Exit():
    root.destroy()


def Reset():
    if Msg and hasattr(Msg, "set"):
        Msg.set("")


def setup_gui():
    global root, Msg, entry_field
    root = Tk()
    root.geometry('600x300')
    root.resizable(0, 0)
    root.config(bg='ghost white')
    root.title('TEXT TO SPEECH')

    Label(root, text='Convert your Text into Voice',
          font='arial 20 bold', bg='white smoke').pack()
    Label(root, text='Enter Text', font='arial 15 bold',
          bg='white smoke').place(x=20, y=60)

    Msg = StringVar()
    entry_field = Entry(root, textvariable=Msg, width='60')
    entry_field.place(x=20, y=100)

    Button(root, text="PLAY", font='arial 15 bold',
           command=Text_to_speech, width=4).place(x=25, y=140)
    Button(root, text='EXIT', font='arial 15 bold',
           command=Exit, bg='OrangeRed1').place(x=100, y=140)
    Button(root, text='RESET', font='arial 15 bold',
           command=Reset).place(x=175, y=140)

    root.mainloop()


if __name__ == "__main__":
    setup_gui()

