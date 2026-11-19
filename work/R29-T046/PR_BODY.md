## Summary

Extract the notebook's elapsed-minutes/remainder calculation into the named `format_elapsed(seconds)` helper and document it in the README. The helper keeps the existing output wording and numerical behavior for non-negative elapsed seconds.

## Verification

- `python3 work/R29-T046/check.py` — 3 tests passed on Python 3.9.6.
- Tests cover 0 and 125.9 seconds and compare the new helper with the previous inline formula.
- The runner executes only the helper, without Drive or torrent I/O. Run output is in [`results.txt`](work/R29-T046/results.txt).
