Description
This pull request adds independent reference cross-check tests for the Car class in Drag Racing Game and adds source comments explaining representative race behavior.

Related Issue
Fixes: #17

Type of Change
- Tests
- Documentation

Changes Made
- Added source documentation in Drag Racing Game/Drag.py describing step progression
- Added work/R29-T013/check.py with independent oracle simulation tests
- Added work/R29-T013/README.md with fixture explanations and source lines
- Added work/R29-T013/results.txt with test runner output

Screenshots / Recordings
Not applicable because these changes are automated tests and documentation.

Testing
Tested locally using the following command:
python3 work/R29-T013/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The oracle model does not call Car methods directly, ensuring independent verification.
