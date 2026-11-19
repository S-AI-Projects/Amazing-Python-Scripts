Description
This pull request adds mutation resistant regression tests for generate_doors in Door Puzzle AI, proving that contract checks detect plausible off by one allocation errors.

Related Issue
Fixes: #24

Type of Change
- Tests
- Documentation

Changes Made
- Added documentation of protected condition in Door Puzzle AI/Puzzle.py
- Added work/R29-T020/check.py verifying the contract and asserting failure on deliberate mutant
- Added work/R29-T020/README.md with fixture definitions and line references
- Added work/R29-T020/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are automated tests and documentation.

Testing
Tested locally using the following command:
python3 work/R29-T020/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The deliberate mutant is kept entirely inside the test file and does not touch the production script.
