## Summary

Add focused CLI regression checks for the TODO app's missing/empty-list branch and its ordinary display flow. The empty deletion path is followed by a successful display and exit in the same isolated run.

The runner uses only a temporary working directory, mocked menu input, and captured output. It verifies the exact empty-list response, header, ordinary item, and persisted file contents.

## Verification

- `python3 work/R29-T048/check.py` — 2 tests passed on Python 3.9.6.
- Source anchors and literal fixture details are documented in [`README.md`](work/R29-T048/README.md).
