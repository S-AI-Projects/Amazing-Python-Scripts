## Description
This PR strengthens the tests for `automated_backup` in `Automated Script/Script.py` to prove mutation resistance — demonstrating that the test suite catches a plausible one-line fault (flattening subdirectory paths) while the original implementation passes cleanly.

## Related Issue
Fixes: #33

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Fixed syntax error in original `Script.py` (misplaced triple-quoted string causing `IndentationError`).
- Added explicit contract docstring citing precondition anchors (Line 24: existence check, Line 28: `makedirs`, Line 34: `relpath`, Line 37: `shutil.copy2`).
- Made `automated_backup` return a sorted list of relative paths copied for testability.
- Implemented mutation-resistant regression suite in `Automated Script/test_script.py` with tests for:
  - Smallest valid input (single file, single-level directory)
  - Ordinary input (multi-level nested directory hierarchy)
  - **Mutation proof**: original preserves `docs/manual.pdf` hierarchy; mutant using `os.path.basename` instead of `os.path.relpath` fails the same named assertion for a semantic reason
  - Nonexistent source → returns `None` gracefully
- Automated check runner `work/R29-T030/check.py` with mutation proof evidence in `work/R29-T030/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Mutation Testing)

## Testing
- Executed `python3 work/R29-T030/check.py`:
  - 4 tests passed with 0 failures and 0 errors.
  - Mutation detection confirmed: original PASS, mutant FAIL on the same `assertFalse(mutant_nested_exists)` assertion.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T030/check.py` exits with status code 0.
No mutation or test-only branch remains in the final source code.
