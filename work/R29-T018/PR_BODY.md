Description
This pull request adds error handling for missing or unreadable images in Neon Effect Filter and adds focused tests covering the failure branch and post failure recovery.

Related Issue
Fixes: #22

Type of Change
- Bug Fix
- Tests
- Documentation

Changes Made
- Added failure check in Neon Effect Filter/Code.py when cv2.imread returns None to return cleanly rather than crashing
- Encapsulated processing logic into apply_neon_effect under __name__ == "__main__"
- Added work/R29-T018/check.py testing failure paths and subsequent valid calls
- Added work/R29-T018/README.md with failure branch line references
- Added work/R29-T018/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are automated error handling and tests.

Testing
Tested locally using the following command:
python3 work/R29-T018/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
External GUI and image libraries are mocked so tests run deterministically in any environment.
