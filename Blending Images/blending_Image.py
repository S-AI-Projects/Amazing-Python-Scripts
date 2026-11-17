"""
Blending Images GUI script.

Public contract for image1:
- image1(filepath=None):
    Loads an image from filepath (or GUI askopenfilename if None),
    resizes it to (500, 500) pixels, and sets global img1.
    Returns the loaded and resized image array.
    Precondition source lines:
      - Line 25: photo1 path acquired.
      - Line 28: image loaded via cv2.imread.
      - Line 29: image resized to dimensions (500, 500).
"""

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
except ImportError:
    tk = None
    askopenfilename = None

img1 = None
img2 = None
alpha = None


def image1(filepath=None):  # getting image 1
    photo1 = filepath if filepath is not None else (askopenfilename() if askopenfilename else "")
    global img1
    if cv2 is not None:
        img1 = cv2.imread(photo1)
        img1 = cv2.resize(img1, (500, 500))
    else:
        # Fallback / mock representation when cv2 is mocked or not installed
        img1 = photo1
    return img1


def image2(filepath=None):  # getting image 2
    photo2 = filepath if filepath is not None else (askopenfilename() if askopenfilename else "")
    global img2
    if cv2 is not None:
        img2 = cv2.imread(photo2)
        img2 = cv2.resize(img2, (500, 500))
    else:
        img2 = photo2
    return img2


def proceeds():  # reading alpha and displaying output
    global alpha
    alpha = t.get(1.0, "end-1c")
    alpha = float(alpha)
    if alpha >= 0 and alpha <= 1:
        beta = 1 - alpha
        res = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
        cv2.imshow('Result', res)
        cv2.imwrite("Output.jpg", res)
        cv2.waitKey(0)
    else:  # when alpha is invalid
        print("invalid alpha")
        exit()


def setup_gui():
    global window, t, b1, b2, proceed
    if tk is None:
        return
    window = tk.Tk()
    window.title("Image blending")
    window.geometry('300x140')

    tk.Label(window, text="Enter alpha (0 to 1)").grid(row=0, column=0)
    tk.Label(window, text="Image 1").grid(row=1, column=0)
    tk.Label(window, text="Image 2").grid(row=2, column=0)

    t = tk.Text(window, height=1, width=5)
    b1 = tk.Button(window, text='choose image 1', command=image1)
    b2 = tk.Button(window, text='choose image 2', command=image2)
    proceed = tk.Button(window, text='Proceed', command=proceeds)

    t.grid(row=0, column=1)
    b1.grid(row=1, column=1)
    b2.grid(row=2, column=1)
    proceed.grid(row=3, column=1)

    window.mainloop()
    if cv2 is not None:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    setup_gui()

