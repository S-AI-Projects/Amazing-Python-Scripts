## Description
This PR specifies and implements failure-path and error-handling behavior for `home` in `Image editor python script/Image_editing_script.py`, validating menu options and asserting clear diagnostic error messages for out-of-bounds or non-numeric selections, with CLI execution isolated under `if __name__ == '__main__':`.

## Related Issue
Fixes: #31

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Documented explicit input/output contract for `home(choice=None)` and defined `HOME_OPTIONS` mapping citing preconditions (Line 28).
- Implemented input validation raising `ValueError` with clear diagnostic messages for invalid options (e.g., `'0'`, `'invalid'`, `''`).
- Preserved default zero-argument `home()` behavior printing the CLI menu options and returning the option dictionary.
- Created unit tests in `Image editor python script/test_image_editor.py` asserting smallest valid input (`'1'`), ordinary input (`'4'`), and testing multiple failure paths for both exception type and diagnostic message contents.
- Added automated check runner `work/R29-T028/check.py` with execution evidence stored in `work/R29-T028/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Error-Path Unit Testing)

## Testing
- Executed `python3 work/R29-T028/check.py`:
  - 6 tests passed with 0 failures and 0 errors.
  - Verified exception raising and message matching on invalid options.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T028/check.py` exits with status code 0.
