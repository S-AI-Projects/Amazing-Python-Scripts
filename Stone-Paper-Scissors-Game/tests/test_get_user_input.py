import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "Rock-Paper-Scissors Game.py"
SPEC = importlib.util.spec_from_file_location("rock_paper_scissors_game", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load game module from {SOURCE}")
GAME = importlib.util.module_from_spec(SPEC)

# The script starts a game at import time; mock its two top-level prompts so
# only the named module is imported and no game interaction reaches a user.
with patch("builtins.input", side_effect=["0", "N"]), contextlib.redirect_stdout(
    io.StringIO()
):
    SPEC.loader.exec_module(GAME)


class GetUserInputContractTests(unittest.TestCase):
    def run_input_case(self, inputs):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(
            output
        ):
            actual = GAME.get_user_input()
        return actual, output.getvalue()

    def test_smallest_valid_input_returns_one(self):
        # Source line 10 accepts exactly 1, 2, or 3; "1" is the smallest.
        inputs = ["1"]
        expected = 1
        actual, actual_output = self.run_input_case(inputs)
        expected_output = ""
        print(
            f"smallest valid: input={inputs!r}, "
            f"expected={(expected, expected_output)!r}, "
            f"actual={(actual, actual_output)!r}"
        )
        self.assertEqual(
            actual, expected, f"input={inputs!r}; expected={expected!r}; actual={actual!r}"
        )
        self.assertEqual(
            actual_output,
            expected_output,
            f"expected output={expected_output!r}; actual output={actual_output!r}",
        )

    def test_ordinary_input_returns_two(self):
        # Source lines 9-11 map the ordinary menu entry "2" to the returned 2.
        inputs = ["2"]
        expected = 2
        actual, actual_output = self.run_input_case(inputs)
        expected_output = ""
        print(
            f"ordinary: input={inputs!r}, "
            f"expected={(expected, expected_output)!r}, "
            f"actual={(actual, actual_output)!r}"
        )
        self.assertEqual(
            actual, expected, f"input={inputs!r}; expected={expected!r}; actual={actual!r}"
        )
        self.assertEqual(
            actual_output,
            expected_output,
            f"expected output={expected_output!r}; actual output={actual_output!r}",
        )

    def test_out_of_range_input_retries_at_domain_boundary(self):
        # Source line 10 rejects 4; the subsequent "1" is the smallest accepted value.
        inputs = ["4", "1"]
        expected = 1
        expected_output = "Invalid input. Please enter a number between 1 and 3.\n"
        actual, actual_output = self.run_input_case(inputs)
        print(
            f"out-of-range retry: input={inputs!r}, "
            f"expected={(expected, expected_output)!r}, "
            f"actual={(actual, actual_output)!r}"
        )
        self.assertEqual(
            actual, expected, f"input={inputs!r}; expected={expected!r}; actual={actual!r}"
        )
        self.assertEqual(
            actual_output,
            expected_output,
            f"expected output={expected_output!r}; actual output={actual_output!r}",
        )

    def test_input_does_not_mutate_choice_fixture(self):
        # Source line 50 defines the exact choice fixture used for this check.
        inputs = ["3"]
        expected_result = 3
        expected_choices = ["stone", "paper", "scissors"]
        choices_before = GAME.a.copy()
        actual, actual_output = self.run_input_case(inputs)
        actual_choices = GAME.a.copy()
        print(
            f"choice mutation: input={inputs!r}, "
            f"expected={(expected_result, expected_choices)!r}, "
            f"actual={(actual, actual_choices)!r}"
        )
        self.assertEqual(
            actual,
            expected_result,
            f"input={inputs!r}; expected={expected_result!r}; actual={actual!r}",
        )
        self.assertEqual(
            choices_before,
            expected_choices,
            f"expected initial choices={expected_choices!r}; actual={choices_before!r}",
        )
        self.assertEqual(
            actual_choices,
            expected_choices,
            f"expected unchanged choices={expected_choices!r}; actual={actual_choices!r}",
        )
        self.assertEqual(
            actual_output,
            "",
            f"expected output=''; actual output={actual_output!r}",
        )


if __name__ == "__main__":
    unittest.main()
