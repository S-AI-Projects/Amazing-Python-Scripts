"""
Focused mutation resistant regression checks for generate_doors in Door Puzzle AI
"""
import sys
import random
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Door Puzzle AI" / "Puzzle.py"

import importlib.util
spec = importlib.util.spec_from_file_location("door_puzzle", str(SOURCE_PATH))
puzzle_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(puzzle_mod)


def mutant_generate_doors_off_by_one(num_doors):
    # Plausible one line mistake: Allocates num_doors - 1 doors
    doors = [False] * (num_doors - 1)
    prize_door = random.randint(0, num_doors - 2) if num_doors > 1 else 0
    if doors:
        doors[prize_door] = True
    return doors


def mutant_generate_doors_multiple_prizes(num_doors):
    # Plausible one line mistake: Initialized with True so multiple doors have prizes
    doors = [True] * num_doors
    prize_door = random.randint(0, num_doors - 1)
    doors[prize_door] = True
    return doors


class GenerateDoorsMutationTests(unittest.TestCase):

    def assert_valid_door_contract(self, doors, num_doors):
        # Named assertion: Verifies door count and single prize invariant
        self.assertEqual(len(doors), num_doors, f"Expected {num_doors} doors but got {len(doors)}")
        self.assertEqual(doors.count(True), 1, f"Expected exactly 1 prize door but found {doors.count(True)}")
        self.assertEqual(doors.count(False), num_doors - 1, f"Expected {num_doors - 1} empty doors")

    def test_smallest_valid_input(self):
        # Preconditions established at source lines:
        # doors = [False] * num_doors at line 9
        # prize_door = random.randint(0, num_doors - 1) at line 10
        # doors[prize_door] = True at line 11
        # Smallest valid input is num_doors = 1
        num_doors = 1
        with patch("random.randint", return_value=0):
            doors = puzzle_mod.generate_doors(num_doors)

        expected_doors = [True]
        self.assertEqual(doors, expected_doors)
        self.assert_valid_door_contract(doors, num_doors)

    def test_ordinary_input(self):
        # Precondition from source line 27: num_doors = 3
        num_doors = 3
        with patch("random.randint", return_value=1):
            doors = puzzle_mod.generate_doors(num_doors)

        expected_doors = [False, True, False]
        self.assertEqual(doors, expected_doors)
        self.assert_valid_door_contract(doors, num_doors)

    def test_mutant_fails_contract_assertion(self):
        # Proves that the regression test detects a plausible mistake
        num_doors = 3
        mutant_doors = mutant_generate_doors_off_by_one(num_doors)

        # The original passes assert_valid_door_contract
        with patch("random.randint", return_value=1):
            original_doors = puzzle_mod.generate_doors(num_doors)
        self.assert_valid_door_contract(original_doors, num_doors)

        # The mutant must fail the exact same named assertion
        with self.assertRaises(AssertionError):
            self.assert_valid_door_contract(mutant_doors, num_doors)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(GenerateDoorsMutationTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T020/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
