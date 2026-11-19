# R29-T046: isolate the elapsed-time formatter

The Colab notebook originally split the elapsed seconds into minutes and remainder inline. The download cell now uses `format_elapsed(seconds)` for that one calculation; the helper uses `divmod(int(seconds), 60)` and keeps the displayed text unchanged (`Elapsed Time:  2 min : 5 sec`). The README documents the input domain and examples.

## Fixtures

- Smallest elapsed duration: `seconds = 0.0`; expected `0 min : 0 sec`.
- Ordinary duration: `seconds = 125.9`; expected `2 min : 5 sec`.

The notebook measures `begin` and `end` with `time.time()` in download cell 3; elapsed seconds are non-negative. The check extracts and runs only the helper AST, so it does not mount Drive, install packages, connect to a torrent, or execute notebook side effects. It compares each expected result to both the helper and the original inline calculation.

Command: `python3 work/R29-T046/check.py` (Python 3.9.6; 3 tests passed). See `results.txt` for the run summary.
