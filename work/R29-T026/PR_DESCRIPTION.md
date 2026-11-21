## Description
This PR refactors `FolderSelectAndRun` / `batch` in `imageWatermarker/main.py` by extracting the watermark positioning and perspective resize computation into a dedicated single-responsibility helper function `compute_watermark_geometry`, backed by characterisation tests confirming exact equivalence before and after refactoring.

## Related Issue
Fixes: #29

## Type of Change
- [x] Tests
- [x] Refactoring / Maintenance
- [x] Documentation

## Changes Made
- Extracted `compute_watermark_geometry(im_size, mark_size, base_width)` to encapsulate watermark placement offset and perspective aspect-ratio resize calculation.
- Modularized image composite creation and resize in `apply_watermark_and_resize`.
- Preserved public interface of `FolderSelectAndRun` and `batch`, documenting precondition anchors (Line 36: `image_files = []`, Line 42: `output_path = ...`).
- Added characterisation and unit tests in `imageWatermarker/test_main.py` covering smallest valid input (100x100), ordinary input (4000x3000), and verifying exact identity to the original inline formulas.
- Added automated check runner `work/R29-T026/check.py` with verification evidence recorded in `work/R29-T026/evidence.json`.

## Screenshots / Recordings
N/A (CLI / Refactoring & Unit Tests)

## Testing
- Executed `python3 work/R29-T026/check.py`:
  - 5 tests passed with 0 failures and 0 errors.
  - Characterisation equivalence confirmed across multiple aspect ratios.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
Automated check runner `python3 work/R29-T026/check.py` exits with status code 0.
