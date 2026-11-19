## Summary

Add focused regression checks for `Calendar GUI/Calendar_gui.py::showCal` using mocked Tkinter objects and literal year fixtures for the smallest supported year (`1`) and an ordinary year (`2024`). The checks cover the rendered calendar text, output type and layout, and field input behavior.

## Verification

- `python3 work/R29-T050/check.py` — 2 tests passed on Python 3.9.6.
- A temporary one-line mutation from `calendar.calendar(find_year)` to `calendar.calendar(find_year + 1)` caused both named tests to fail at the calendar text assertion. See [`mutation-result.txt`](work/R29-T050/mutation-result.txt).
- Test runner, literal expected outputs, and task notes are in [`work/R29-T050/`](work/R29-T050/).

No production behavior was changed.
