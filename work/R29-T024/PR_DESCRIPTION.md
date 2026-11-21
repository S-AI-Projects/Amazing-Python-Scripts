## Description
This PR establishes invariant and property-based testing around `hex_add` in `hexCalculator/hexCalculator.py`, testing algebraic invariants (commutativity and identity) across randomly generated inputs, documenting preconditions, and isolating GUI dependencies for clean headless execution.

## Related Issue
Fixes: #27

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Documented invariants and preconditions citing source lines (Line 25: `num1 = int(entry1.get(), 16)`, Line 27: `result = hex(num1 + num2)`).
- Factored out core computation into `calculate_hex_add(val1, val2)` while preserving Tkinter UI behavior in `create_app()`.
- Implemented comprehensive property tests in `hexCalculator/test_hex_calculator.py` validating commutativity across 100 random pairs and identity across 50 values, alongside boundary inputs ("0", "0" and "A", "F").
- Added automated check runner `work/R29-T024/check.py` with results captured in `work/R29-T024/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Property Testing)

## Testing
- Executed `python3 work/R29-T024/check.py`:
  - 6 tests passed with 0 failures and 0 errors.
  - Confirmed invariant preservation and error handling on invalid non-hex inputs.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T024/check.py` exits with status code 0.
