# R29-T053: Auto Fill Google Forms Reference Comparison

## Overview
This task implements independent reference comparison for `Auto-Fill-Google-Forms/readme.md` and `test.py` against an independent tokenizing reference oracle.

## Preconditions and Source Anchors
Preconditions established in `Auto-Fill-Google-Forms/test.py` and `readme.md`:
- **Lines 6-8**: `inputName`, `inputEmailID`, `inputPhone` XPaths for Google Form fields.
- **Line 11**: `Submit` button XPath.
- **Line 26**: `with open("input.csv", "r") as f_input` opens the input CSV file.
- **Line 27**: `csv_input = csv.DictReader(f_input)` initializes CSV dictionary reader.
- **Lines 28-31**: `row['name']`, `row['email']`, `row['phone_number']` extracts ordered field attributes.
- **Lines 36-45**: `while i < len(name)` sends keys, clicks submit, and navigates back.

## Independent Reference Oracle
The independent oracle (`IndependentReferenceOracle.parse_csv_lines`) uses raw string line splitting, trimming, and column index lookup rather than `csv.DictReader` and does not invoke the functions under test (`read_records`, `fill_form_records`).

## Fixtures and Differential Tests
1. **Smallest Valid Input**:
   - 1 header row + 1 data record: `"Alice,alice@example.com,1234"`
   - Output: `[{"name": "Alice", "email": "alice@example.com", "phone_number": "1234"}]`
   - Verified against oracle.

2. **Ordinary Input**:
   - Standard `input.csv` containing 6 records (Constance, Homer, John, Moe, Sai Harsha Vardhan, sreddhar).
   - Preserves 6-element list in exact file order.

3. **25 Domain Samples Cross-Check**:
   - 25 diverse valid records covering various string formats, international phone numbers, special characters in emails, and whitespace.
   - All 25 outputs match the independent oracle with 100% equivalence in type, shape, and ordering.

4. **Input Immutability**:
   - Verifies input lists (`names`, `emails`, `phones`) are not mutated by `fill_form_records`.

5. **Browser Automation Mocks**:
   - Verifies `send_keys`, `click`, and `back` calls on mocked Selenium browser.

## Running the Checks
```bash
python3 work/R29-T053/check.py
```
Or via native unittest discovery:
```bash
python3 -m unittest discover -s "Auto-Fill-Google-Forms/tests" -p "test_auto_fill.py" -v
```
