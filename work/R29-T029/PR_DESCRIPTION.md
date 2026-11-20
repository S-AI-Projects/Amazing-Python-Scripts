## Description
This PR characterizes and experimentally validates the algorithmic scaling complexity of `EazyDiner` in `EazyDiner-Scraper/restaurants.py`, establishing explicit $O(N)$ linear time and space complexity with deterministic operation counting across 3 distinct input sizes ($N \in [1, 5, 20]$), supported by offline mock HTML fixtures.

## Related Issue
Fixes: #32

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Added detailed complexity specification defining input variable $N$ (number of `.restaurant` cards) with asymptotic worst-case $O(N)$ claim and empirical operation counting.
- Documented precondition anchors citing source lines (Line 46: `restaurant_data = {"restaurants": []}`).
- Modularized DOM parsing into `parse_restaurants(soup)` returning parsed records and operation counts.
- Implemented complexity scaling and regression tests in `EazyDiner-Scraper/test_restaurants.py` asserting exact expected values on smallest valid input ($N=1$), ordinary input ($N=5$), and linear scaling ($N=20$) without depending on flaky wall-clock timings.
- Added automated check runner `work/R29-T029/check.py` with experimental results captured in `work/R29-T029/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Complexity Experiment & Unit Testing)

## Testing
- Executed `python3 work/R29-T029/check.py`:
  - 3 tests passed with 0 failures and 0 errors.
  - Confirmed $O(N)$ linear scaling ($work / N = 5.0$) across all tested sizes.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T029/check.py` exits with status code 0.
