"""
Focused scaling measurements and regression checks for HeartRate Detection
"""
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "HeartRate-Detection-OpenC-py" / "HeartRate.py"

# Mock numpy, cv2, and matplotlib before importing source
mock_np = MagicMock()


def mock_average(a):
    if hasattr(a, "data"):
        vals = a.data
    elif isinstance(a, (list, tuple)):
        vals = a
    else:
        vals = [a]
    return sum(vals) / len(vals)


mock_np.average.side_effect = mock_average
mock_cv2 = MagicMock()
mock_plt = MagicMock()

sys.modules["numpy"] = mock_np
sys.modules["cv2"] = mock_cv2
sys.modules["matplotlib"] = MagicMock()
sys.modules["matplotlib.pyplot"] = mock_plt

import importlib.util
spec = importlib.util.spec_from_file_location("heartrate_mod", str(SOURCE_PATH))
heart_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heart_mod)


class MockArray:
    def __init__(self, data):
        self.data = data
        self.size = len(data)


class HeartRateScalingTests(unittest.TestCase):

    def test_smallest_valid_input(self):
        # Preconditions established at source lines:
        # x, y, w, h = 800, 500, 100, 100 at line 21
        # heartbeat_count = 128 at line 23
        # Smallest valid input has w = 1 and h = 1 (N = 1 pixel)
        crop_img = MockArray([100.0])
        initial_values = [0.0] * 128
        initial_times = [1000.0] * 128

        new_vals, new_times, avg = heart_mod.process_heartrate_frame(
            crop_img, initial_values, initial_times, current_time=1001.0
        )

        expected_avg = 100.0
        self.assertEqual(avg, expected_avg)
        self.assertEqual(len(new_vals), 128)
        self.assertEqual(new_vals[-1], expected_avg)
        self.assertEqual(new_times[-1], 1001.0)

    def test_ordinary_input(self):
        # Ordinary input with w=100, h=100 (N = 10,000 pixels) from lines 21 and 22
        pixel_count = 10000
        crop_img = MockArray([150.0] * pixel_count)
        initial_values = [0.0] * 128
        initial_times = [1000.0] * 128

        new_vals, new_times, avg = heart_mod.process_heartrate_frame(
            crop_img, initial_values, initial_times, current_time=1002.0
        )

        expected_avg = 150.0
        self.assertEqual(avg, expected_avg)
        self.assertEqual(len(new_vals), 128)
        self.assertEqual(new_vals[-1], expected_avg)

    def test_scaling_experiment(self):
        # Measure operations and elapsed time across input sizes N
        sizes = [100, 400, 1600, 10000]
        timings_file = Path(__file__).resolve().parent / "timings.txt"
        records = []

        initial_values = [0.0] * 128
        initial_times = [1000.0] * 128

        for n in sizes:
            crop_img = MockArray([120.0] * n)
            start_t = time.perf_counter()
            # Run 50 iterations to smooth timing
            for _ in range(50):
                heart_mod.process_heartrate_frame(
                    crop_img, initial_values, initial_times, current_time=1003.0
                )
            elapsed = time.perf_counter() - start_t
            records.append(f"N = {n:5d} pixels | 50 iterations took {elapsed:.6f} seconds")

        with open(timings_file, "w") as f:
            f.write("\n".join(records) + "\n")

        self.assertEqual(len(records), len(sizes))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(HeartRateScalingTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T019/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
