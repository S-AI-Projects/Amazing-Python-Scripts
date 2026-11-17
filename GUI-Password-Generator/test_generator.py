import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import generator


class TestGetStrengthFailureBehavior(unittest.TestCase):
    """
    Focused test suite covering failure / absent-result behavior of getStrength.
    Precondition source lines:
      - Line 55: entry widget cleared with entry.delete(0, 'end').
      - Line 63: Low strength (var == 1).
      - Line 69: Medium strength (var == 0).
      - Line 75: Strong strength (var == 3).
      - Line 80: Absent-result failure branch (else -> returns None).
    """

    def setUp(self):
        generator.entry.delete(0)
        generator.var.set(0)
        generator.var1.set(8)

    def test_absent_result_failure_branch_smallest_input(self):
        """
        Exercises the failure / absent-result branch with smallest invalid input (-1, length 0).
        Verifies that function returns None, entry is cleared, and caller-owned state remains valid.
        Preconditions: generator.py lines 55, 80.
        """
        entry_mock = generator.MockEntry()
        entry_mock.insert(0, "old_password")

        # Call with invalid strength value (reaching else branch)
        result = generator.getStrength(strength_val=-1, length_val=0, entry_widget=entry_mock)

        # Assert intended sentinel None
        self.assertIsNone(result)
        # Verify entry was cleared
        self.assertEqual(entry_mock.get(), "")

    def test_ordinary_valid_input_succeeds_after_failure(self):
        """
        Verifies that after exercising the failure branch, an ordinary valid call (Medium strength, len 10)
        succeeds normally and preserves caller-owned state.
        Preconditions: generator.py lines 69, 80.
        """
        entry_mock = generator.MockEntry()

        # Step 1: Failure branch
        res_fail = generator.getStrength(strength_val=99, length_val=5, entry_widget=entry_mock)
        self.assertIsNone(res_fail)

        # Step 2: Ordinary call immediately following failure
        res_success = generator.getStrength(strength_val=0, length_val=10, entry_widget=entry_mock)
        self.assertIsNotNone(res_success)
        self.assertEqual(len(res_success), 10)
        self.assertTrue(res_success.isalpha())


if __name__ == "__main__":
    unittest.main()
