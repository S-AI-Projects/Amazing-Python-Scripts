## Description
This pull request measures and documents the work done and complexity scaling of heat map generation in `Data-Visualization/HeatMap/heat_maps.py`. It defines the input-size variable ($N = R \times C$ where $R=\text{rows}$ and $C=\text{columns}$), distinguishes theoretical worst-case claims ($\mathcal{O}(R \cdot C)$ time and space) from empirical observations, isolates algorithmic computation from process startup and Plotly display I/O, and adds contract regression tests across the smallest valid input ($1 \times 1$) and ordinary input ($5 \times 3$).

## Related Issue
Fixes: S-AI-Projects/Amazing-Python-Scripts#59

## Type of Change
- [x] Tests
- [x] Documentation
- [x] Refactoring / Maintenance

## Changes Made
- Added comprehensive complexity analysis comment in `Data-Visualization/HeatMap/heat_maps.py` explicitly naming the input-size variable $N = R \times C$ and distinguishing theoretical worst-case complexity ($\mathcal{O}(R \cdot C)$ time and space) from empirical benchmark observations.
- Refactored `heat_maps.py` into testable modular functions `generate_heatmap_data` and `build_heatmap_figure` while preserving all original module-level attributes (`rows=5`, `columns=3`, `data`, `fig`).
- Wrapped `fig.show()` inside `main()` under `if __name__ == '__main__':` to allow clean headless importing in test environments without opening browser windows.
- Added standard-library fallbacks for `numpy` and `plotly` ensuring offline test execution without external dependencies.
- Added regression test suite in `Data-Visualization/tests/test_heat_maps.py` covering smallest valid input ($1 \times 1$), ordinary input ($5 \times 3$), module attribute preservation, seed reproducibility, and multi-size correctness scaling.
- Implemented automated benchmark runner `work/R29-T059/check.py` testing 3 increasing sizes ($N=25, 400, 2500$) over 5 repetitions with fixed seeds, measuring operation counts and reporting median and range metrics outside the correctness checks.
- Recorded empirical benchmark results in `work/R29-T059/results.txt` and `work/R29-T059/results.json`.
- Added detailed task documentation in `work/R29-T059/README.md`.

## Screenshots / Recordings
Not applicable (automated complexity benchmark / unit tests).

## Testing
Tested locally using:
```bash
python3 work/R29-T059/check.py
```
And via unittest discovery:
```bash
python3 -m unittest discover -s "Data-Visualization/tests" -p "test_heat_maps.py" -v
```
All 5 tests and benchmark scaling passes succeeded with 0 errors and 0 failures.

## Checklist
- [x] I have tested my changes locally.
- [x] I have added or updated tests, if needed.
- [x] I have updated documentation, if needed.
- [x] I have followed the project's coding guidelines.
- [x] I have run the relevant tests and checks.
- [x] I have addressed previous review feedback, if applicable.

## Additional Notes
No pass/fail threshold depends on wall-clock speed; all measured benchmark cases pass strict correctness checks.
