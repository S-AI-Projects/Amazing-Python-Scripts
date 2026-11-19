Description
This pull request simplifies find_lyrics in Lyrics_Finder by extracting the URL formatting calculation into a dedicated helper function build_lyrics_url and adding focused regression tests.

Related Issue
Fixes: #20

Type of Change
- Refactoring / Maintenance
- Tests
- Documentation

Changes Made
- Extracted build_lyrics_url function in Lyrics_Finder/script.py to isolate URL creation
- Added work/R29-T016/check.py with before and after regression tests
- Added work/R29-T016/README.md explaining the extracted responsibility and test cases
- Added work/R29-T016/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are code refactoring and automated tests.

Testing
Tested locally using the following command:
python3 work/R29-T016/check.py
All 4 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The existing public interface of find_lyrics remains completely unchanged and backward compatible.
