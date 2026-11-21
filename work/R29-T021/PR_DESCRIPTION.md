## Description
This PR defines and locks down the input/output contract for `PDF Watermark` in `PDF-Watermark/pdf-watermark.py` and adds comprehensive focused regression tests covering smallest valid input (1 page), ordinary input (3 pages), and multi-page boundary cases with all external I/O mocked.

## Related Issue
Fixes: #3

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Documented concise I/O contract in docstring citing source lines establishing preconditions (Lines 24, 25, 27).
- Encapsulated core watermarking logic in `pdf_watermark(input_file, watermark_file, output_file)` preserving backward-compatible CLI execution under `if __name__ == '__main__':`.
- Added unit tests in `PDF-Watermark/test_watermark.py` asserting explicit expected values, return values, and observable mutations separately.
- Created standalone check runner `work/R29-T021/check.py` and generated execution evidence in `work/R29-T021/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Unit Testing)

## Testing
- Executed `python3 work/R29-T021/check.py`:
  - 3 tests passed with 0 failures and 0 errors.
  - Verified on Python 3.9+ with mocked I/O.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T021/check.py` exits with status code 0.
