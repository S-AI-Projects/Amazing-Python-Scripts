import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from converter_script import Definations, Converter, trace_decimal_to_binary


class TestDefinationsWorkedExample(unittest.TestCase):
    """
    Unit tests and verified executable worked example for Definations in converter_script.py.
    Anchors cited:
      - Line 28: decimal_number = 0
      - Line 33: binary_number = []
    """

    def test_smallest_valid_input_worked_example(self):
        """
        Smallest valid input: decimal 0.
        Precondition anchors: Line 28 (decimal_number = 0), Line 33 (binary_number = []).
        """
        trace = trace_decimal_to_binary(0)

        # Assert intermediate steps and final result
        self.assertEqual(trace["decimal"], 0)
        self.assertEqual(trace["binary_bits"], [0])
        self.assertEqual(trace["binary_str"], "0")
        self.assertEqual(len(trace["intermediate_steps"]), 1)
        self.assertEqual(trace["intermediate_steps"][0], {"dividend": 0, "quotient": 0, "remainder": 0})

        # Consistency with Definations class
        defn = Definations(0)
        self.assertEqual(defn.Decimal_to_Binary(), "0")

    def test_ordinary_input_worked_example(self):
        """
        Ordinary input: decimal 13.
        Steps:
          1. 13 // 2 = 6 rem 1
          2. 6 // 2 = 3 rem 0
          3. 3 // 2 = 1 rem 1
          4. 1 // 2 = 0 rem 1
          Collected remainders: [1, 0, 1, 1] -> reversed: [1, 1, 0, 1] -> '1101'
        """
        trace = trace_decimal_to_binary(13)

        expected_steps = [
            {"dividend": 13, "quotient": 6, "remainder": 1},
            {"dividend": 6, "quotient": 3, "remainder": 0},
            {"dividend": 3, "quotient": 1, "remainder": 1},
            {"dividend": 1, "quotient": 0, "remainder": 1}
        ]
        self.assertEqual(trace["intermediate_steps"], expected_steps)
        self.assertEqual(trace["binary_bits"], [1, 1, 0, 1])
        self.assertEqual(trace["binary_str"], "1101")

        # Consistency with Definations class
        defn = Definations(13)
        self.assertEqual(defn.Decimal_to_Binary(), "1101")

    def test_definations_all_conversions_consistent(self):
        """
        Verifies standard conversions for base 2, 8, 10, 16.
        """
        defn = Definations(42)
        self.assertEqual(defn.Decimal_to_Binary(), "101010")
        self.assertEqual(defn.Decimal_to_Octal(), "52")
        self.assertEqual(defn.Decimal_to_Hexadecimal(), "2a")

        defn_hex = Definations("2a")
        self.assertEqual(defn_hex.Hexadecimal_to_Decimal(), 42)
        self.assertEqual(defn_hex.Hexadecimal_to_Binary(), "101010")

    def test_converter_formatting(self):
        """
        Verifies Converter wrapper output string.
        """
        conv = Converter("13")
        res = conv.convert(FROM="d", TO="b")
        self.assertIn("13 in Decimal = 1101 in Binary", res)


if __name__ == '__main__':
    unittest.main()
