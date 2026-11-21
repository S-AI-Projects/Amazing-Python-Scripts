## Description
This pull request adds an executable worked example and contract tests for `FacebookLogin` in `Automate Facebook bot/script.py`. It documents the complete execution flow from input through intermediate states to the final result, clearly identifying the decisive state transitions (authentication session submission and group broadcast loop dispatch), and locks down behavior on the smallest valid input (`groupid = []`) and ordinary input (`groupid = ['123456789']`).

## Related Issue
Fixes: S-AI-Projects/Amazing-Python-Scripts#57

## Type of Change
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance

## Changes Made
- Added comprehensive executable documentation and doctest examples to `FacebookLogin` docstring in `Automate Facebook bot/script.py` and updated `Automate Facebook bot/Readme.md`.
- Identified and explained the two decisive state transitions: (1) authentication session dispatch via login form submission, and (2) group broadcast loop dispatch across target `groupid` elements.
- Introduced lightweight, in-memory `MockWebDriver` and `MockWebElement` helpers and optional `driver` / `sleep_fn` injection in `FacebookLogin` to enable fast, deterministic, offline execution of examples and tests without live credentials.
- Guarded interactive `input()` prompts behind `prompt_user_inputs()` under `if __name__ == '__main__':` to allow clean importing in test runners while maintaining full backward-compatibility for CLI execution.
- Added contract and regression test suite `Automate Facebook bot/tests/test_script.py` verifying smallest valid input (`groupid = []`), ordinary input (`groupid = ['123456789']`), multiple group iteration, doctest execution, and decisive state transitions.
- Created standalone automated runner `work/R29-T057/check.py` saving evidence in `work/R29-T057/results.txt` and `work/R29-T057/results.json`.
- Added detailed task documentation in `work/R29-T057/README.md`.

## Screenshots / Recordings
Not applicable (automated unit tests / backend script).

## Testing
Tested locally using:
```bash
python3 work/R29-T057/check.py
```
And via unittest discovery:
```bash
python3 -m unittest discover -s "Automate Facebook bot/tests" -p "test_script.py" -v
```
All 6 tests passed successfully with 0 errors and 0 failures.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
All checks run fast and offline using the Python standard library without requiring external dependencies, browser drivers, or live Facebook credentials.
