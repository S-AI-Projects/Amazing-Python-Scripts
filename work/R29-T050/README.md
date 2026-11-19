# R29-T050: `showCal` regression checks

The checks exercise only `Calendar GUI/Calendar_gui.py` and replace Tkinter's window and label objects with small fakes, so no display or external I/O is needed.

## Contract fixtures

- Smallest accepted year: input `"1"`; expected calendar text is the checked-in `expected-1.txt` fixture (36 lines).
- Ordinary year: input `"2024"`; expected calendar text is the checked-in `expected-2024.txt` fixture (35 lines).
- The precondition is established at `Calendar GUI/Calendar_gui.py:14`, where the field value is converted to `int`; each test passes a literal numeric string.
- Checks also cover result type and exact text, field-read count and unchanged input, window title/size/background, calendar label placement, left justification, and one main-loop call.
- Expected text fixtures were recorded before editing any implementation. No production code was changed.

## Verification

Command: `python3 work/R29-T050/check.py`

Result: 2 tests passed on Python 3.9.6. The focused runner is the project test configuration for this isolated task because the repository has no project-wide Python test configuration for this module.

Mutation: changing `calendar.calendar(find_year)` to `calendar.calendar(find_year + 1)` made both named tests fail at the exact calendar-text assertion. The full output is in `mutation-result.txt`.
