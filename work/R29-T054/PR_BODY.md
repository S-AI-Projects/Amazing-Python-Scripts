## Description
This pull request adds invariant and property-based regression tests for `Number-Guess-Game/numberguess.py`. It defines and locks down core mathematical invariants (target boundedness, directional comparison monotonicity, and guess count preservation) across 100 deterministic seeded property test cases, while validating mutation sensitivity with a deliberate mutant failure test.

## Related Issue
Fixes: S-AI-Projects/Amazing-Python-Scripts#54

## Type of Change
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance

## Changes Made
- Documented invariant definitions and contract in `Number-Guess-Game/numberguess.py` citing source precondition lines.
- Extracted modular helpers `validate_range`, `evaluate_guess`, and `run_game` while keeping `main()` interactive execution 100% backward-compatible under `if __name__ == '__main__':`.
- Added property test suite in `Number-Guess-Game/tests/test_number_guess.py` testing smallest valid input, ordinary input, 100 deterministic seeded cases (seed 42), and deliberate mutant failure.
- Created standalone automated runner `work/R29-T054/check.py` saving evidence to `work/R29-T054/results.txt` and `work/R29-T054/results.json`.
- Added contract documentation in `work/R29-T054/README.md`.

## Screenshots / Recordings
Not applicable (automated unit tests / CLI game).

## Testing
Tested locally using:
```bash
python3 work/R29-T054/check.py
```
And via unittest discovery:
```bash
python3 -m unittest discover -s "Number-Guess-Game/tests" -p "test_number_guess.py" -v
```
All 5 tests passed successfully with 0 errors and 0 failures across 100 property cases.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
All checks execute fast and offline using Python standard library without external dependencies.
