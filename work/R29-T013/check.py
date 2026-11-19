"""
Focused reference cross-check for Car in Drag Racing Game
"""
import sys
import io
import contextlib
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Drag Racing Game" / "Drag.py"

import importlib.util
spec = importlib.util.spec_from_file_location("drag_racing", str(SOURCE_PATH))
drag_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drag_module)


def reference_oracle_car(top_speed, acceleration):
    """
    Independent reference simulation for drag racing.
    Does not use the Car class.
    """
    speed = 0.0
    gear = 1
    steps = 0
    while speed < top_speed:
        steps += 1
        speed += acceleration * gear
        if speed >= top_speed * 0.8:
            if gear < 5:
                gear += 1
    return {
        "steps": steps,
        "final_speed": speed,
        "final_gear": gear
    }


class CarCrossCheckTests(unittest.TestCase):

    def test_smallest_valid_input(self):
        # Preconditions established at source lines:
        # Car.__init__ at line 5: current_speed = 0, gear = 1
        # accelerate at lines 16-17: current_speed += acceleration * gear
        # race at lines 28-32: while current_speed < top_speed
        top_speed = 10
        acceleration = 10

        expected = reference_oracle_car(top_speed, acceleration)
        self.assertEqual(expected["steps"], 1)
        self.assertEqual(expected["final_speed"], 10)
        self.assertEqual(expected["final_gear"], 2)

        car = drag_module.Car("SmallCar", top_speed=top_speed, acceleration=acceleration)
        with patch("time.sleep"), patch("builtins.print"):
            car.race()

        self.assertEqual(car.current_speed, expected["final_speed"])
        self.assertEqual(car.gear, expected["final_gear"])

    def test_ordinary_input(self):
        # Preconditions at lines 35:
        # top_speed = 200, acceleration = 20
        top_speed = 200
        acceleration = 20

        expected = reference_oracle_car(top_speed, acceleration)
        self.assertEqual(expected["steps"], 9)
        self.assertEqual(expected["final_speed"], 200)
        self.assertEqual(expected["final_gear"], 3)

        car = drag_module.Car("Player Car", top_speed=top_speed, acceleration=acceleration)
        with patch("time.sleep"), patch("builtins.print"):
            car.race()

        self.assertEqual(car.current_speed, expected["final_speed"])
        self.assertEqual(car.gear, expected["final_gear"])

    def test_boundary_high_acceleration(self):
        # Precondition at line 31:
        # if current_speed >= top_speed * 0.8: shift_gear()
        top_speed = 100
        acceleration = 85

        expected = reference_oracle_car(top_speed, acceleration)
        self.assertEqual(expected["steps"], 2)
        self.assertEqual(expected["final_speed"], 255)
        self.assertEqual(expected["final_gear"], 3)

        car = drag_module.Car("FastCar", top_speed=top_speed, acceleration=acceleration)
        with patch("time.sleep"), patch("builtins.print"):
            car.race()

        self.assertEqual(car.current_speed, expected["final_speed"])
        self.assertEqual(car.gear, expected["final_gear"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(CarCrossCheckTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T013/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
