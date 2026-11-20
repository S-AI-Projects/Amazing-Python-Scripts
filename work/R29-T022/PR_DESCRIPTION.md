## Description
This PR defines and documents the supported input domain and boundary cases for `Currency Exchange Rates` in `Currency-Exchange-Rates/exchange_rates.py`, introducing comprehensive unit tests covering smallest valid boundary, ordinary values, upper boundary, and rejected boundary conditions with mocked external dependencies.

## Related Issue
Fixes: #25

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Documented domain boundary specifications and boundary tables citing source code preconditions (Line 25: `currencies = []`, Line 33: `current_element = {'name': ..., 'short': ...}`, Line 42: `currency = currencies[currency_index]`).
- Modularized currency extraction (`parse_currencies`), 1-based index validation (`select_currency`), and table parsing (`parse_exchange_table`).
- Added boundary test suite `Currency-Exchange-Rates/test_exchange_rates.py` with 8 distinct test cases asserting both accepted boundaries (position 1, position 2, position `len`) and rejected out-of-range inputs (position 0, position `len + 1`, negative index).
- Implemented test runner `work/R29-T022/check.py` with verification evidence saved to `work/R29-T022/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Unit Testing)

## Testing
- Executed `python3 work/R29-T022/check.py`:
  - 8 tests passed with 0 failures and 0 errors.
  - Verified edge cases and error bounds.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T022/check.py` exits with status code 0.
