Description
This pull request adds a small dependency seam and repeatability regression checks for convert_audio_to_text in Audio to Text Convertor.

Related Issue
Fixes: #19

Type of Change
- Refactoring / Maintenance
- Tests
- Documentation

Changes Made
- Added optional recognizer and microphone parameters with default values of None in Audio to Text Convertor/code.py
- Wrapped module level script execution under __name__ == "__main__"
- Added work/R29-T015/check.py with repeatable execution tests
- Added work/R29-T015/README.md with fixture and repeatability details
- Added work/R29-T015/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are automated tests and code refactoring.

Testing
Tested locally using the following command:
python3 work/R29-T015/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The injected dependency parameters default to None to ensure existing callers remain completely unaffected.
