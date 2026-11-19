"""Compare landmark pixel conversion to an independent floor-based oracle."""
from __future__ import annotations

import ast
import math
import platform
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "Pose_Estimation_Using_OpenCV" / "PoseEstimation.py"
TABLE = Path(__file__).resolve().parent / "result-table.txt"


def load_converter():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "landmark_to_pixel")
    namespace = {}
    isolated = ast.Module(body=[function], type_ignores=[])
    exec(compile(ast.fix_missing_locations(isolated), str(SOURCE), "exec"), namespace)
    return namespace["landmark_to_pixel"]


CONVERT = load_converter()


class LandmarkPixelTests(unittest.TestCase):
    def test_smallest_image_origin(self):
        # Source precondition: the frame loop reads h,w at source line 27 and
        # passes them to landmark_to_pixel at source line 29.
        landmark = SimpleNamespace(x=0.0, y=0.0)
        actual = CONVERT(landmark, 1, 1)
        expected = (0, 0)
        self.assertEqual(actual, expected,
                         f"expected {expected!r}; actual {actual!r}")
        self.assertEqual((landmark.x, landmark.y), (0.0, 0.0),
                         "expected landmark input unchanged")

    def test_ordinary_landmark(self):
        landmark = SimpleNamespace(x=0.25, y=0.5)
        actual = CONVERT(landmark, 640, 480)
        expected = (160, 240)
        self.assertEqual(actual, expected,
                         f"expected {expected!r}; actual {actual!r}")

    def test_25_small_normalized_inputs_against_floor_oracle(self):
        # Domain: positive image dimensions and MediaPipe normalized x,y in
        # [0, 1). math.floor is an independent oracle for integer pixel bins.
        fractions = (0.0, 0.125, 0.25, 0.5, 0.875)
        width, height = 7, 5
        rows = []
        for x in fractions:
            for y in fractions:
                landmark = SimpleNamespace(x=x, y=y)
                before = (landmark.x, landmark.y)
                expected = (math.floor(x * width), math.floor(y * height))
                actual = CONVERT(landmark, width, height)
                self.assertEqual(type(actual), tuple,
                                 f"expected tuple; actual {type(actual).__name__}")
                self.assertEqual(len(actual), 2,
                                 f"expected coordinate pair; actual {actual!r}")
                self.assertEqual(actual, expected,
                                 f"input {(x, y, width, height)!r}: expected {expected!r}; actual {actual!r}")
                self.assertEqual((landmark.x, landmark.y), before,
                                 f"expected input unchanged {before!r}; actual {(landmark.x, landmark.y)!r}")
                rows.append(f"{x},{y},{width},{height} -> {expected[0]},{expected[1]}")
        TABLE.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LandmarkPixelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T043/check.py")
    print("Independent oracle: math.floor(x * width), math.floor(y * height)")
    print("Cases: 25 grid inputs plus smallest and ordinary fixtures")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
