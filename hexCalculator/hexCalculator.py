import tkinter as tk

"""
hexCalculator Invariant Specification:
Function: calculate_hex_add(s1: str, s2: str) -> str
Contract:
  - Line 25: num1 = int(entry1.get(), 16)
  - Line 27: result = hex(num1 + num2)
  - Result formatted as 'Result: ' + result.upper()
Invariants:
  1. Commutativity: calculate_hex_add(a, b) == calculate_hex_add(b, a) for all valid hex strings.
  2. Identity: calculate_hex_add(a, "0") produces numerical equivalent of int(a, 16).
  3. Rejection: Non-hex strings return "Invalid Input".
"""


def calculate_hex_add(val1_str, val2_str):
    try:
        num1 = int(val1_str, 16)
        num2 = int(val2_str, 16)
        result = hex(num1 + num2)
        return "Result: " + result.upper()
    except ValueError:
        return "Invalid Input"


def hex_add():
    res = calculate_hex_add(entry1.get(), entry2.get())
    output.config(text=res)


def hex_subtract():
    try:
        num1 = int(entry1.get(), 16)
        num2 = int(entry2.get(), 16)
        result = hex(num1 - num2)
        output.config(text="Result: " + result.upper())
    except ValueError:
        output.config(text="Invalid Input")


def hex_multiply():
    try:
        num1 = int(entry1.get(), 16)
        num2 = int(entry2.get(), 16)
        result = hex(num1 * num2)
        output.config(text="Result: " + result.upper())
    except ValueError:
        output.config(text="Invalid Input")


def hex_divide():
    try:
        num1 = int(entry1.get(), 16)
        num2 = int(entry2.get(), 16)
        result = hex(num1 // num2)
        output.config(text="Result: " + result.upper())
    except (ValueError, ZeroDivisionError):
        output.config(text="Invalid Input")


def create_app():
    root = tk.Tk()
    root.title("Hex Calculator")

    global entry1, entry2, output
    entry1 = tk.Entry(root, width=15)
    entry1.grid(row=0, column=0, padx=10, pady=5)
    entry2 = tk.Entry(root, width=15)
    entry2.grid(row=0, column=1, padx=10, pady=5)

    add_button = tk.Button(root, text="Add", command=hex_add)
    add_button.grid(row=1, column=0, padx=10, pady=5)
    subtract_button = tk.Button(root, text="Subtract", command=hex_subtract)
    subtract_button.grid(row=1, column=1, padx=10, pady=5)
    multiply_button = tk.Button(root, text="Multiply", command=hex_multiply)
    multiply_button.grid(row=2, column=0, padx=10, pady=5)
    divide_button = tk.Button(root, text="Divide", command=hex_divide)
    divide_button.grid(row=2, column=1, padx=10, pady=5)

    output = tk.Label(root, text="Result: ")
    output.grid(row=3, columnspan=2)

    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
