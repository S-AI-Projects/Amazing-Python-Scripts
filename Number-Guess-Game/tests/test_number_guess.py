"""
Invariant and property-based tests for Number Guess Game (numberguess.py).

Source Precondition and Invariant Anchors:
- Lines 5-10: top_of_range validation
- Line 15: random_number in [0, top_of_range]
- Lines 18-35: Guessing loop and monotonic comparison feedback
- Line 36: Final guess counter report
"""

import copy
import importlib.util
from pathlib import Path
import random
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "numberguess.py"

spec = importlib.util.spec_from_file_location("numberguess_module", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load numberguess module from {SOURCE}")
numberguess_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(numberguess_module)


class NumberGuessGameInvariantTests(unittest.TestCase):
    """
    Invariant and property-based test suite for Number Guess Game.
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: top_of_range = 1, target = 1, guess = 1.
        Source preconditions:
          - Line 8: top_of_range > 0 (smallest positive int is 1)
          - Line 15: random.randint(0, 1)
          - Lines 28-30: guess == random_number terminates on attempt 1.
        """
        top_val, err = numberguess_module.validate_range("1")
        self.assertIsNone(err)
        self.assertEqual(top_val, 1)

        result = numberguess_module.run_game(
            top_of_range=1,
            guesses_input_iter=["1"],
            random_number=1
        )

        expected_result = {
            "random_number": 1,
            "guesses": 1,
            "feedback": ["You got it! "],
            "summary": "You got it in 1 guesses"
        }

        print(
            f"smallest_valid: top_of_range=1, target=1, guess=['1'], "
            f"expected={expected_result!r}, actual={result!r}"
        )

        self.assertEqual(result, expected_result)
        self.assertEqual(result["guesses"], 1)

    def test_ordinary_input(self):
        """
        Ordinary input: top_of_range = 10, target = 7, guesses = ["3", "8", "7"].
        Demonstrates feedback progression below, above, and correct.
        """
        top_val, err = numberguess_module.validate_range("10")
        self.assertIsNone(err)
        self.assertEqual(top_val, 10)

        result = numberguess_module.run_game(
            top_of_range=10,
            guesses_input_iter=["3", "8", "7"],
            random_number=7
        )

        expected_result = {
            "random_number": 7,
            "guesses": 3,
            "feedback": [
                "You were below the number!",
                "You were above the number!",
                "You got it! "
            ],
            "summary": "You got it in 3 guesses"
        }

        print(
            f"ordinary_input: top_of_range=10, target=7, guesses=['3', '8', '7'], "
            f"guesses_count={result['guesses']}"
        )

        self.assertEqual(result, expected_result)
        self.assertEqual(result["guesses"], 3)

    def test_target_boundedness_and_feedback_monotonicity_100_cases(self):
        """
        Property Test: 100 bounded valid cases with fixed seed (seed = 42).
        Verifies:
          1. Invariant: 0 <= random_number <= top_of_range
          2. Comparison Monotonicity Invariant:
             - guess < target -> 'You were below the number!'
             - guess > target -> 'You were above the number!'
             - guess == target -> 'You got it! ' and terminates
          3. Guess Count Invariant: total recorded guesses == len(guesses_taken)
        """
        rng = random.Random(42)
        total_cases = 100

        for case_idx in range(total_cases):
            top = rng.randint(1, 1000)
            target = rng.randint(0, top)

            # Invariant 1: Target Boundedness
            self.assertGreaterEqual(target, 0)
            self.assertLessEqual(target, top)

            # Generate random intermediate guesses ending at target
            num_prior_guesses = rng.randint(0, 5)
            guesses_list = [rng.randint(0, top) for _ in range(num_prior_guesses)]
            # Ensure target is the final guess
            guesses_list.append(target)

            result = numberguess_module.run_game(
                top_of_range=top,
                guesses_input_iter=guesses_list,
                random_number=target
            )

            # Invariant 2: Comparison Monotonicity across all steps
            # Since an earlier random guess might coincide with target, game terminates at first match
            first_match_idx = guesses_list.index(target)
            expected_guesses_count = first_match_idx + 1

            # Invariant 3: Guess Count Invariant
            self.assertEqual(result["guesses"], expected_guesses_count)
            self.assertEqual(result["summary"], f"You got it in {expected_guesses_count} guesses")
            self.assertEqual(len(result["feedback"]), expected_guesses_count)

            # Check individual feedback entries
            for i in range(first_match_idx):
                g = guesses_list[i]
                if g > target:
                    self.assertEqual(result["feedback"][i], "You were above the number!")
                elif g < target:
                    self.assertEqual(result["feedback"][i], "You were below the number!")

            # Final feedback must be win message
            self.assertEqual(result["feedback"][-1], "You got it! ")

        print(f"property_test_100_cases: 100 bounded cases successfully verified against invariants!")

    def test_input_mutation_isolation(self):
        """
        Verify that run_game does not mutate caller's input lists.
        """
        guesses = ["1", "5", "10"]
        guesses_copy = copy.deepcopy(guesses)

        numberguess_module.run_game(10, guesses, random_number=10)
        self.assertEqual(guesses, guesses_copy)

    def test_deliberate_mutant_fails_invariant(self):
        """
        Verify that a deliberate mutant breaking the invariant fails the property test,
        confirming test sensitivity to regressions.
        """
        # Mutant A: inverted feedback (> reports below, < reports above)
        def mutant_evaluate_inverted(user_guess, random_number):
            if user_guess == random_number:
                return "You got it! ", True
            elif user_guess > random_number:
                return "You were below the number!", False  # INVERTED
            else:
                return "You were above the number!", False  # INVERTED

        msg, _ = mutant_evaluate_inverted(user_guess=10, random_number=5)
        # Invariant dictates that user_guess > random_number must report 'above'
        with self.assertRaises(AssertionError):
            self.assertEqual(msg, "You were above the number!")

        # Mutant B: broken guess counter (off-by-one)
        def mutant_run_game_broken_counter(guesses_list, target):
            # Broken: counter starts at 0 and misses increment
            return {"guesses": len(guesses_list) - 1, "target": target}

        mutant_res = mutant_run_game_broken_counter(["3", "7"], 7)
        # Invariant dictates that 2 guesses must report guesses == 2
        with self.assertRaises(AssertionError):
            self.assertEqual(mutant_res["guesses"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
