Description
This pull request defines the supported boundaries of InstaBot in Unfollowers Insta and adds focused unit tests covering smallest inputs and boundary conditions.

Related Issue
Fixes: #16

Type of Change
- Tests
- Documentation

Changes Made
- Added documentation of supported boundaries in Unfollowers-Insta/insta_bot_bb8.py
- Added work/R29-T012/check.py with focused boundary unit tests
- Added work/R29-T012/README.md with boundary explanations and line references
- Added work/R29-T012/results.txt containing test execution output

Screenshots / Recordings
Not applicable because these changes are automated tests and documentation.

Testing
Tested locally using the following command:
python3 work/R29-T012/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
All external browser and user interactions were mocked so the suite executes fast and offline.
