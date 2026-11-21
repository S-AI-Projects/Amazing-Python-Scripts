## Description
This pull request defines and locks down the input/output contract for `get_problems` in `Codechef Scrapper/codechef.py`. It adds focused regression tests covering the smallest valid input, ordinary input, repeated-value domain boundary, zero-count boundary, and observable mutation isolation with all external I/O and dependencies mocked.

## Related Issue
Fixes: S-AI-Projects/Amazing-Python-Scripts#6

## Type of Change
- [x] Tests
- [x] Documentation

## Changes Made
- Documented concise input/output contract docstring in `Codechef Scrapper/codechef.py` beside `get_problems` citing source precondition lines.
- Added regression test suite in `Codechef Scrapper/tests/test_codechef.py` with mocked Selenium WebDriver and FPDF dependencies.
- Added standalone automated check runner in `work/R29-T051/check.py` saving execution report to `work/R29-T051/results.txt`.
- Added contract documentation and fixture specifications in `work/R29-T051/README.md`.

## Screenshots / Recordings
Not applicable (automated unit tests / backend scraper).

## Testing
Tested locally using:
```bash
python3 work/R29-T051/check.py
```
All 5 tests passed successfully with 0 errors and 0 failures.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
All checks run using standard Python library mocks without requiring live Chrome browser or external network connections.
