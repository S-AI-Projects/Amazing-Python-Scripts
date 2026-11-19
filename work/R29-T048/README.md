# R29-T048: TODO empty and missing-list behavior

The script has no reusable function API and performs relative file I/O at import time, so the focused runner invokes only `TODO (CLI-VER)/todolist.py` with a temporary working directory, a controlled input sequence, and captured stdout.

## Fixtures and expected outcomes

- Smallest supported empty case: no `todolist.txt` exists; source lines 2–14 initialize the item count and create the two-line header. Literal menu input is `2, 4, 5`: deleting from the empty list prints `There is no item in the list kindly add some items` (lines 29–31), then displaying the list succeeds (lines 76–87), and the app exits normally.
- Ordinary case: a literal one-item file (`09:30`, `Read`) produces an item count of one from the three lines minus two header lines at source line 8. Menu input `4, 5` displays the item and leaves the file unchanged.
- Both tests assert explicit expected text and file state. `check.py` isolates all file I/O in a temporary directory.

Run with `python3 work/R29-T048/check.py` (Python 3.9.6; 2 tests).
