import unittest
from unittest.mock import MagicMock
import random
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hexCalculator as hc


class TestHexAddProperty(unittest.TestCase):
    """
    Property tests and contract regression for hex_add in hexCalculator/hexCalculator.py.
    Anchors cited:
      - Line 25: num1 = int(entry1.get(), 16)
      - Line 27: result = hex(num1 + num2)
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: "0" and "0".
        Precondition: Line 25 (num1), Line 27 (result).
        """
        result = hc.calculate_hex_add("0", "0")
        expected = "Result: 0X0"
        self.assertEqual(result, expected)

    def test_ordinary_input(self):
        """
        Ordinary input: "A" (10) and "F" (15). Sum = 25 -> 0x19 -> "0X19".
        Precondition: Line 25 (num1), Line 27 (result).
        """
        result = hc.calculate_hex_add("A", "F")
        expected = "Result: 0X19"
        self.assertEqual(result, expected)

    def test_invariant_commutativity_property(self):
        """
        Algebraic invariant: Commutativity.
        For all valid hex pairs (a, b), calculate_hex_add(a, b) == calculate_hex_add(b, a).
        Tested across 100 randomly generated hex values.
        """
        rng = random.Random(42)
        test_pairs = []
        for _ in range(100):
            val1 = hex(rng.randint(0, 0xFFFFF))[2:]
            val2 = hex(rng.randint(0, 0xFFFFF))[2:]
            test_pairs.append((val1, val2))

        for a, b in test_pairs:
            res_ab = hc.calculate_hex_add(a, b)
            res_ba = hc.calculate_hex_add(b, a)
            self.assertEqual(res_ab, res_ba, f"Commutativity violated for {a}, {b}")

    def test_invariant_identity_property(self):
        """
        Algebraic invariant: Identity element "0".
        calculate_hex_add(a, "0") produces integer value equal to int(a, 16).
        """
        rng = random.Random(99)
        for _ in range(50):
            val = rng.randint(0, 0xFFFFFF)
            hex_str = hex(val)[2:]
            res = hc.calculate_hex_add(hex_str, "0")
            parsed_val = int(res.split(": ")[1], 16)
            self.assertEqual(parsed_val, val)

    def test_rejection_invalid_inputs(self):
        """
        Negative domain boundary: non-hex strings return 'Invalid Input'.
        """
        self.assertEqual(hc.calculate_hex_add("G12", "5"), "Invalid Input")
        self.assertEqual(hc.calculate_hex_add("ABC", "XYZ"), "Invalid Input")
        self.assertEqual(hc.calculate_hex_add("", "1"), "Invalid Input")

    def test_gui_hex_add_integration_mocked(self):
        """
        Mocks tkinter entry widgets and verifies hex_add updates output label.
        """
        hc.entry1 = MagicMock()
        hc.entry2 = MagicMock()
        hc.output = MagicMock()

        hc.entry1.get.return_value = "10"
        hc.entry2.get.return_value = "20"
        hc.hex_add()

        hc.output.config.assert_called_once_with(text="Result: 0X30")


if __name__ == '__main__':
    unittest.main()
