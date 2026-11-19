Description
This pull request adds an executable worked example and docstring for resize_image in Image Manipulation Script along with automated regression checks.

Related Issue
Fixes: #21

Type of Change
- Documentation
- Tests

Changes Made
- Added runnable docstring example in Image Manipulation Script/image_manipulation.py explaining the decisive state transition
- Wrapped module level example execution inside __name__ == "__main__"
- Added work/R29-T017/check.py with executable tests verifying image dimensions and messages
- Added work/R29-T017/README.md with state transition explanations
- Added work/R29-T017/results.txt with test execution output

Screenshots / Recordings
Not applicable because these changes are documentation and automated tests.

Testing
Tested locally using the following command:
python3 work/R29-T017/check.py
All 3 tests passed successfully.

Checklist
- I have tested my changes locally.
- I have added or updated tests, if needed.
- I have updated documentation, if needed.
- I have followed the project's coding guidelines.
- I have run the relevant tests and checks.
- I have addressed previous review feedback, if applicable.

Additional Notes
The tests create temporary images on disk and clean them up automatically after execution.
