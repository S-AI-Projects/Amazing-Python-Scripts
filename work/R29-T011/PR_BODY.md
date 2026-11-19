Description
This pull request adds contract tests for welcomeScreen in Flappy Bird Game. It verifies the return value and checks that global sprites and sounds are not mutated.

Related Issue
Fixes: #2

Type of Change
- Tests
- Documentation

Changes Made
- Added docstring contract above welcomeScreen in Flappy-Bird-Game/main.py
- Added work/R29-T011/check.py with smallest, ordinary, and boundary test cases
- Added work/R29-T011/README.md documenting inputs and expected values
- Added work/R29-T011/results.txt with test runner output

Screenshots / Recordings
Not applicable because these changes are automated tests and documentation.

Testing
Tested locally using the following command:
python3 work/R29-T011/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
Everything was tested using Python mock objects so it runs cleanly without needing external GUI windows.
