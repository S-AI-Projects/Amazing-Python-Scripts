## Summary

Add repeatable `change_wall` checks around its external wallpaper setter. The runner extracts only the named function, mocks the wallpaper dependency and result/path variables, and avoids launching Tk.

Checks cover empty-path failure, the smallest valid path, an ordinary path, and failure followed by success to confirm result state is overwritten correctly.

## Verification

- `python3 work/R29-T045/check.py` — 4 tests passed on Python 3.9.6.
- Inputs, expected statuses, source anchors, and isolation notes are in [`README.md`](work/R29-T045/README.md).
