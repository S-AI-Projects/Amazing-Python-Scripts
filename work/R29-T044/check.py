"""Property checks for the Rock-paper-scissors winner invariant."""
from __future__ import annotations

import contextlib
import io
import os
import platform
import random
import runpy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
SOURCE = Path(os.environ.get("RPS_SOURCE", REPO / "Rock-paper-scissors" / "game.py"))
WINNING_PAIRS = {(1, 3), (2, 1), (3, 2)}  # user, computer; rules in README.md


def run_round(user_choice, computer_draws):
    answers = iter([str(user_choice), "n"])
    output = io.StringIO()
    with patch("builtins.input", side_effect=lambda *args: next(answers)), \
         patch("random.randint", side_effect=computer_draws), \
         contextlib.redirect_stdout(output):
        runpy.run_path(str(SOURCE), run_name="__main__")
    return output.getvalue()


def assert_round(test, user_choice, computer_choice, draws=None):
    if draws is None:
        draws = [computer_choice]
    output = run_round(user_choice, draws)
    expected_winner = "User" if (user_choice, computer_choice) in WINNING_PAIRS else "Computer"
    marker = "<== You win ==>" if expected_winner == "User" else "<== Computer wins ==>"
    other = "<== Computer wins ==>" if expected_winner == "User" else "<== You win ==>"
    test.assertEqual(output.count(marker), 1,
                     f"choices ({user_choice}, {computer_choice}) expected {expected_winner}; output {output!r}")
    test.assertEqual(output.count(other), 0,
                     f"choices ({user_choice}, {computer_choice}) must have one winner; output {output!r}")
    test.assertNotIn("<== It's a tie ==>", output,
                     f"draws are rerolled before resolution; output {output!r}")


class WinnerInvariantTests(unittest.TestCase):
    def test_entire_three_by_three_initial_choice_domain(self):
        # Source preconditions: game.py:11 accepts integer choices; lines 32-37
        # redraw a tie; lines 57-64 establish the winner mapping.
        for user_choice in (1, 2, 3):
            for first_computer_draw in (1, 2, 3):
                if first_computer_draw == user_choice:
                    actual_computer = user_choice % 3 + 1
                    draws = [first_computer_draw, actual_computer]
                else:
                    actual_computer = first_computer_draw
                    draws = [first_computer_draw]
                with self.subTest(user=user_choice, first_draw=first_computer_draw):
                    assert_round(self, user_choice, actual_computer, draws)

    def test_fixed_seed_one_hundred_bounded_valid_rounds(self):
        rng = random.Random(29044)
        choices = (1, 2, 3)
        for case in range(100):
            user_choice = rng.choice(choices)
            computer_choice = rng.choice(tuple(choice for choice in choices
                                               if choice != user_choice))
            with self.subTest(case=case, user=user_choice, computer=computer_choice):
                assert_round(self, user_choice, computer_choice)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WinnerInvariantTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T044/check.py")
    print("Cases: all 9 initial choice pairs plus 100 fixed-seed valid rounds")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
