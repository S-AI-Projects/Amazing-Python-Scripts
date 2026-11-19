Description
This pull request adds invariant property tests for Support Chat Bot For Your Website and adds source documentation describing the result count invariant.

Related Issue
Fixes: #18

Type of Change
- Tests
- Documentation

Changes Made
- Added invariant documentation in Support Chat Bot For Your Website -  Project 9/app.py
- Added work/R29-T014/check.py with invariant checks, seeded random testing, and deliberate mutation failure checks
- Added work/R29-T014/README.md with invariant definitions and source line references
- Added work/R29-T014/results.txt with test runner output

Screenshots / Recordings
Not applicable because these changes are automated tests and documentation.

Testing
Tested locally using the following command:
python3 work/R29-T014/check.py
All 4 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The test runner includes a test demonstrating that a deliberate mutant breaking the invariant fails as required.
