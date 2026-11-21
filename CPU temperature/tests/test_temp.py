"""
Deterministic repeatability tests for get_cpu_temperature in CPU temperature/temp.py.

Source Precondition Anchors:
- Line 15 (original) / 29: temperature = psutil.sensors_temperatures()['coretemp'][0].current
- Lines 17-19 (original) / 31-33: exception handler returning 'NA'
- Lines 9-33: get_cpu_temperature with optional sensors_fn dependency seam
"""

from collections import namedtuple
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock

SOURCE = Path(__file__).resolve().parents[1] / "temp.py"

spec = importlib.util.spec_from_file_location("temp_module", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load temp module from {SOURCE}")
temp_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(temp_module)

ShwTemp = namedtuple("shwtemp", ["current"])


class TestGetCpuTemperatureRepeatability(unittest.TestCase):
    """
    Repeatability and deterministic execution test suite for get_cpu_temperature.
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: Single sensor reading at 0.0 C.
        Precondition: coretemp list containing 1 reading at line 15/29.
        """
        sensors_fixture = {"coretemp": [ShwTemp(current=0.0)]}
        expected_temp = 0.0

        actual_temp = temp_module.get_cpu_temperature(sensors_fn=lambda: sensors_fixture)

        print(
            f"smallest_valid: fixture={sensors_fixture!r}, "
            f"expected={expected_temp}, actual={actual_temp}"
        )

        self.assertEqual(actual_temp, expected_temp)
        self.assertIsInstance(actual_temp, float)

    def test_ordinary_input(self):
        """
        Ordinary input: Multi-core sensor readings (55.5 C, 58.0 C).
        First sensor value selected at index [0].
        """
        sensors_fixture = {
            "coretemp": [ShwTemp(current=55.5), ShwTemp(current=58.0)]
        }
        expected_temp = 55.5

        actual_temp = temp_module.get_cpu_temperature(sensors_fn=lambda: sensors_fixture)

        print(
            f"ordinary_input: fixture={sensors_fixture!r}, "
            f"expected={expected_temp}, actual={actual_temp}"
        )

        self.assertEqual(actual_temp, expected_temp)
        self.assertIsInstance(actual_temp, float)

    def test_sensors_unavailable_returns_na_sentinel(self):
        """
        Fallback boundary: empty sensor dict returns 'NA'.
        Precondition: KeyError caught at lines 17-19/31-33.
        """
        sensors_fixture = {}
        expected_temp = "NA"

        actual_temp = temp_module.get_cpu_temperature(sensors_fn=lambda: sensors_fixture)

        print(
            f"unavailable_sensors: fixture={sensors_fixture!r}, expected='NA', actual={actual_temp!r}"
        )

        self.assertEqual(actual_temp, expected_temp)

    def test_repeatability_and_state_isolation(self):
        """
        Step 3 Requirement:
        Run the same fixture twice in fresh isolated state and once after another valid input;
        assert that earlier runs cannot alter the later result.
        """
        ordinary_fixture = {"coretemp": [ShwTemp(current=62.5)]}
        smallest_fixture = {"coretemp": [ShwTemp(current=1.0)]}

        # Run 1: Fresh isolated run
        result_run1 = temp_module.get_cpu_temperature(sensors_fn=lambda: ordinary_fixture)
        self.assertEqual(result_run1, 62.5)

        # Run 2: Second run with identical fixture in fresh state
        result_run2 = temp_module.get_cpu_temperature(sensors_fn=lambda: ordinary_fixture)
        self.assertEqual(result_run2, 62.5)
        self.assertEqual(result_run1, result_run2)

        # Intermediate run with a different valid fixture
        result_inter = temp_module.get_cpu_temperature(sensors_fn=lambda: smallest_fixture)
        self.assertEqual(result_inter, 1.0)

        # Run 3: Same fixture run immediately after another valid input
        result_run3 = temp_module.get_cpu_temperature(sensors_fn=lambda: ordinary_fixture)
        self.assertEqual(result_run3, 62.5)

        # Assert earlier runs cannot alter later results
        self.assertEqual(result_run3, result_run1)

        print("repeatability_check: verified 3 runs with perfect result consistency and isolation!")

    def test_default_dependency_seam_preserves_callers(self):
        """
        Verify that get_cpu_temperature() called without arguments defaults gracefully
        without breaking callers.
        """
        mock_psutil = MagicMock()
        mock_psutil.sensors_temperatures.return_value = {
            "coretemp": [ShwTemp(current=42.0)]
        }

        orig_psutil = temp_module.psutil
        temp_module.psutil = mock_psutil
        try:
            # Call with zero arguments using default seam
            default_result = temp_module.get_cpu_temperature()
            self.assertEqual(default_result, 42.0)
            mock_psutil.sensors_temperatures.assert_called_once()
        finally:
            temp_module.psutil = orig_psutil


if __name__ == "__main__":
    unittest.main(verbosity=2)
