import unittest
import importlib.util
import os
import sys

# Dynamic loader for filename with spaces
MODULE_PATH = os.path.join(os.path.dirname(__file__), 'Image_editing_script.py')
spec = importlib.util.spec_from_file_location('image_editing_script', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestImageEditorErrorPaths(unittest.TestCase):
    """
    Error-path and regression tests for home() in Image_editing_script.py.
    Preconditions cited:
      - Line 28: Valid options are '1' through '9' in HOME_OPTIONS.
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: choice = '1'.
        Precondition: Line 28 (HOME_OPTIONS).
        """
        result = mod.home(choice='1')
        expected = "Flip the image."
        self.assertEqual(result, expected)

    def test_ordinary_valid_input(self):
        """
        Ordinary valid input: choice = '4'.
        Precondition: Line 28.
        """
        result = mod.home(choice='4')
        expected = "Blur the image"
        self.assertEqual(result, expected)

    def test_home_default_invocation(self):
        """
        Verifies default invocation home() displays all 9 options.
        """
        options = mod.home()
        self.assertIsInstance(options, dict)
        self.assertEqual(len(options), 9)
        self.assertEqual(options['9'], "quit")

    def test_failure_branch_invalid_numerical_choice(self):
        """
        Failure branch: choice outside [1, 9] (e.g. '0' or '10').
        Must raise ValueError with diagnostic message.
        """
        with self.assertRaises(ValueError) as ctx:
            mod.home(choice='0')

        expected_msg = "Invalid option '0': choice must be between 1 and 9"
        self.assertEqual(str(ctx.exception), expected_msg)

    def test_failure_branch_non_numeric_choice(self):
        """
        Failure branch: non-numeric string choice (e.g. 'invalid').
        Must raise ValueError with diagnostic message.
        """
        with self.assertRaises(ValueError) as ctx:
            mod.home(choice='invalid')

        expected_msg = "Invalid option 'invalid': choice must be between 1 and 9"
        self.assertEqual(str(ctx.exception), expected_msg)

    def test_failure_branch_empty_choice(self):
        """
        Failure branch: empty string choice ''.
        Must raise ValueError with diagnostic message.
        """
        with self.assertRaises(ValueError) as ctx:
            mod.home(choice='')

        expected_msg = "Invalid option '': choice must be between 1 and 9"
        self.assertEqual(str(ctx.exception), expected_msg)


if __name__ == '__main__':
    unittest.main()
