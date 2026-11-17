import os
import sys
import random
import unittest
import importlib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

rms = importlib.import_module("Restaurant-Management-System")


class TestBtnclickInvariant(unittest.TestCase):
    """
    Focused invariant/property tests for btnclick in Restaurant-Management-System.py.
    Invariant:
      For any sequence of inputs S = [x_1, x_2, ..., x_n],
      successive calls to btnclick(x_i) satisfy:
        1. operator == old_operator + str(x_i)
        2. text_input.get() == operator
        3. length of operator increases exactly by len(str(x_i))
    Precondition source lines:
      - Line 25: global operator referenced.
      - Line 26: operator = operator + str(numbers).
      - Line 28: text_input.set(operator).
    """

    def setUp(self):
        # Reset module state
        rms.operator = ""
        rms.text_input.set("")

    def test_smallest_valid_input(self):
        """
        Smallest valid input:
        Single character/digit '0'.
        Preconditions: lines 25, 26, 28.
        """
        initial_op = rms.operator
        btn_input = 0
        expected_op = initial_op + "0"

        rms.btnclick(btn_input)

        self.assertEqual(rms.operator, expected_op)
        self.assertEqual(rms.text_input.get(), expected_op)

    def test_ordinary_input(self):
        """
        Ordinary input:
        Operator string like '+' or multi-digit sequence like '45'.
        Preconditions: lines 25, 26, 28.
        """
        rms.operator = "12"
        rms.text_input.set("12")
        btn_input = "+"
        expected_op = "12+"

        rms.btnclick(btn_input)

        self.assertEqual(rms.operator, expected_op)
        self.assertEqual(rms.text_input.get(), expected_op)

    def test_property_invariant_100_random_cases(self):
        """
        Generates at least 100 bounded valid inputs with a fixed seed
        and verifies the preservation of the concatenation invariant.
        """
        rng = random.Random(42)  # Fixed deterministic seed
        valid_tokens = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+", "-", "*", "/", "."]

        for _ in range(100):
            token = rng.choice(valid_tokens)
            prev_op = rms.operator
            expected_op = prev_op + str(token)

            rms.btnclick(token)

            self.assertEqual(rms.operator, expected_op)
            self.assertEqual(rms.text_input.get(), expected_op)
            self.assertEqual(len(rms.operator), len(prev_op) + len(str(token)))


if __name__ == "__main__":
    unittest.main()
