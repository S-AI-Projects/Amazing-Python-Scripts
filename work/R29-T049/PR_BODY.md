## Summary

Make the Search File example importable and runnable by extracting `search_files(root_path, pattern)` and guarding the default CLI. Add focused correctness checks and repeatable scaling observations for 20, 200, and 1,000 files.

The measured work is a top-down directory traversal plus filename filtering. For `N` filesystem entries across visited directories, the worst-case work is O(N); the `F` filename filtering operations are included in that bound. The iterator streams paths.

## Verification

- `python3 work/R29-T049/check.py` — 2 correctness tests passed on Python 3.9.6.
- Five fresh, fixed-seed temporary trees per size; expected matched paths checked outside each timed interval. Results and ranges are in [`measurements.txt`](work/R29-T049/measurements.txt).
- The check has no wall-clock pass/fail threshold.
