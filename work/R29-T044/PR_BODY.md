## Summary

Document the game's one-winner invariant and add focused checks of the winner mapping. The test runner controls choices and captures output, checks all nine initial choice pairs including the equal-choice redraw, and generates 100 additional fixed-seed valid rounds.

## Verification

- `python3 work/R29-T044/check.py` — 2 tests passed across 109 rounds on Python 3.9.6.
- A temporary one-line mutation to the winner comparison fails the same named invariant test. See [`mutation-result.txt`](work/R29-T044/mutation-result.txt).
- Fixtures and rule justification are in [`README.md`](work/R29-T044/README.md).
