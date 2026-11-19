# R29-T045: repeatable `change_wall` checks

`change_wall` is defined at source line 10. It reads the selected path at line 13, calls the external `set_wallpaper`, maps failure to `Wallpaper not found !` at line 17, and stores the result at line 19. The focused runner extracts only that function from the source, so importing the Tk window and entering a GUI loop are avoided.

## Inputs and outcomes

- Empty path `""`: mocked setter raises `OSError`; expected status `Wallpaper not found !`.
- Smallest valid path `"a.jpg"`: mocked setter returns normally; expected status `success`.
- Ordinary path `"Pictures/sunset.jpg"`: expected setter argument is unchanged and result is `success`.
- Isolation sequence: `"/tmp/missing.jpg"` raises, then `"/tmp/ordinary.jpg"` succeeds. Expected status history is [`Wallpaper not found !`, `success`].

The wallpaper dependency and Tk state are controlled fakes. No live desktop, network, account, or image file is used. Command: `python3 work/R29-T045/check.py` (Python 3.9.6; 4 tests passed).
