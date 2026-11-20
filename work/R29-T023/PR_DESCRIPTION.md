## Description
This PR defines the explicit contract of `setup_teams` in `Zoombinis/Zoombinis.py` and implements differential cross-check tests comparing `setup_teams` against an independent reference implementation across various inputs, structured shapes, and controlled random seeds.

## Related Issue
Fixes: #26

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Added explicit docstring contract for `setup_teams` citing preconditions (Line 25: `teams = []`, Line 27: `team = []`, Line 29: values in range `[1, 4]`).
- Supported deterministic random stream injection while keeping default zero-argument `setup_teams()` signature fully intact and backwards-compatible.
- Implemented `reference_setup_teams` within `Zoombinis/test_zoombinis.py` and established differential tests verifying structured equivalence (type, shape, ordering, range).
- Implemented automated check runner `work/R29-T023/check.py` with structured evidence saved to `work/R29-T023/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Differential Testing)

## Testing
- Executed `python3 work/R29-T023/check.py`:
  - 4 differential tests passed with 0 failures and 0 errors.
  - Verified across multiple distinct seeds and default invocation.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T023/check.py` exits with status code 0.
