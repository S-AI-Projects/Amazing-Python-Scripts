# R29-T043: pose landmark coordinate reference

`PoseEstimation.py:27` obtains frame height and width, and line 29 converts each normalized landmark. The new `landmark_to_pixel(lm, width, height)` helper isolates that calculation without importing the camera loop. Its output contract is a two-integer `(x, y)` tuple; the landmark input remains unchanged.

## Fixtures and oracle

- Smallest frame/origin: `(width, height) = (1, 1)`, landmark `(0.0, 0.0)`, expected `(0, 0)`.
- Ordinary frame: `(640, 480)`, landmark `(0.25, 0.5)`, expected `(160, 240)`.
- A 25-case grid covers x and y from `{0, 0.125, 0.25, 0.5, 0.875}` on a `7 × 5` frame. The independent reference uses `math.floor` for the bounded non-negative in-frame domain. Input values are recorded with expected coordinates in `result-table.txt`.

The runner extracts only the named helper from the target module. It does not initialize OpenCV, MediaPipe, or a webcam.

Command: `python3 work/R29-T043/check.py` (Python 3.9.6; 3 tests passed, covering 27 inputs).
