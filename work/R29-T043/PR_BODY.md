## Summary

Extract the normalized-landmark to pixel-coordinate calculation into `landmark_to_pixel` and compare it against an independent `math.floor` reference for bounded in-frame coordinates. The camera loop calls the helper with the same landmark and frame dimensions.

## Verification

- `python3 work/R29-T043/check.py` — 3 tests passed across the smallest fixture, an ordinary fixture, and a 25-input grid on Python 3.9.6.
- The checks assert tuple type, pair shape, exact coordinates, and unchanged landmark inputs without opening a webcam.
- Inputs and expected reference results are in [`result-table.txt`](work/R29-T043/result-table.txt).
