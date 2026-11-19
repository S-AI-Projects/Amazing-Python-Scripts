Description
This pull request adds complexity analysis and empirical scaling measurements for HeartRate Detection, along with regression tests verifying buffer management and pixel averaging.

Related Issue
Fixes: #23

Type of Change
- Performance Improvement
- Tests
- Documentation

Changes Made
- Added complexity documentation and process_heartrate_frame helper function in HeartRate-Detection-OpenC-py/HeartRate.py
- Wrapped camera loop under __name__ == "__main__"
- Added work/R29-T019/check.py measuring scaling on different input sizes
- Added work/R29-T019/timings.txt with timing measurements across input dimensions
- Added work/R29-T019/README.md with complexity analysis and source line references
- Added work/R29-T019/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are complexity analysis and automated tests.

Testing
Tested locally using the following command:
python3 work/R29-T019/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The pass criteria do not depend on wall clock speed thresholds, ensuring deterministic and portable testing.
