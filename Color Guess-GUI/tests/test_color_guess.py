"""Contract and failure-path coverage tests for start_game in Color Guess-GUI.

Issue: R29-T058
Target: Color Guess-GUI/Color_guess.py (start_game, change_color, countdown)
Anchors:
- Precondition 1: Source fixture / data anchor at lines 4-5:
  `colors_name = ['Red', 'White', 'Yellow', 'Pink', 'Blue', 'Black', 'Brown', 'Purple', 'Green', 'Cyan']`
- Precondition 2: Initial game state at lines 6-7:
  `score = 0`, `time_left = 60`
- Precondition 3: Active game branch at line 11:
  `if time_left == 60: countdown()`
- Precondition 4: Absent-result / game-over fallback branch at line 19 in change_color:
  `if (time_left > 0):` (evaluates False when time_left <= 0)
- Precondition 5: Rejection / wrong-guess branch at line 21:
  `if e.get().lower() == colors_name[1].lower():`
"""

import sys
import unittest
from pathlib import Path

# Add project root and module directory to path for clean import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_DIR = REPO_ROOT / "Color Guess-GUI"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import Color_guess


class TestColorGuessFailureBehavior(unittest.TestCase):
    """Failure-behavior and contract test suite for start_game."""

    def setUp(self):
        # Anchor from lines 4-5 in Color Guess-GUI/Color_guess.py
        self.initial_colors = [
            'Red', 'White', 'Yellow', 'Pink', 'Blue',
            'Black', 'Brown', 'Purple', 'Green', 'Cyan'
        ]
        Color_guess.colors_name = list(self.initial_colors)
        Color_guess.score = 0
        Color_guess.time_left = 60
        Color_guess.scoreLabel = Color_guess.DummyWidget("Press Enter to Start")
        Color_guess.timeLabel = Color_guess.DummyWidget("Time Left: 60")
        Color_guess.label = Color_guess.DummyWidget()
        Color_guess.e = Color_guess.DummyWidget()

    def test_data_anchor_integrity(self):
        """Verify the data anchor colors_name defined at lines 4-5."""
        expected_anchor = [
            'Red', 'White', 'Yellow', 'Pink', 'Blue',
            'Black', 'Brown', 'Purple', 'Green', 'Cyan'
        ]
        self.assertEqual(Color_guess.colors_name, expected_anchor)

    def test_smallest_valid_input_absent_result_branch(self):
        """Precondition: Line 7 initializes time_left = 60; countdown (line 33) decrements
        it until time_left reaches 0 (expired game state).
        Precondition: Line 11 `if time_left == 60:` is False.
        Precondition: Line 19 in change_color() `if (time_left > 0):` evaluates False.

        Literal inputs:
        - play: None
        - time_left: 0
        - score: 0
        - colors_name: ['Red', 'White', 'Yellow', 'Pink', 'Blue', 'Black', 'Brown', 'Purple', 'Green', 'Cyan']
        - e.text: 'White'

        Independently calculated expected outputs:
        - Return value of start_game(None): None
        - time_left remains 0 (no countdown decrement or rescheduling)
        - score remains 0 (no increment)
        - scoreLabel.text remains 'Press Enter to Start' (unchanged)
        - e.text remains 'White' (not deleted)
        - colors_name remains unshuffled
        """
        Color_guess.time_left = 0
        Color_guess.score = 0
        Color_guess.e.text = "White"
        expected_colors_before = list(Color_guess.colors_name)

        result = Color_guess.start_game(None)

        # Assert intended sentinel/return
        self.assertIsNone(result)

        # Assert caller-owned state remains valid and unmodified
        self.assertEqual(Color_guess.time_left, 0)
        self.assertEqual(Color_guess.score, 0)
        self.assertEqual(Color_guess.scoreLabel.text, "Press Enter to Start")
        self.assertEqual(Color_guess.e.text, "White")
        self.assertEqual(Color_guess.colors_name, expected_colors_before)

    def test_ordinary_valid_input_active_branch(self):
        """Precondition: Lines 6-7 initialize score = 0, time_left = 60.
        Precondition: Line 11 `if time_left == 60:` evaluates True, invoking countdown().
        Precondition: Line 33 decrements time_left from 60 to 59.
        Precondition: Line 19 `if (time_left > 0):` evaluates True.
        Precondition: Line 21 matches e.get().lower() == colors_name[1].lower().

        Literal inputs:
        - play: None
        - time_left: 60
        - score: 0
        - e.text: 'White' (matches colors_name[1])

        Independently calculated expected outputs:
        - Return value: None
        - time_left: 59 (decremented by countdown)
        - score: 1 (incremented)
        - scoreLabel.text: 'Score: 1'
        - e.text: '' (cleared by e.delete)
        - timeLabel.after called with (1000, countdown)
        """
        Color_guess.time_left = 60
        Color_guess.score = 0
        Color_guess.e.text = Color_guess.colors_name[1]  # 'White'

        result = Color_guess.start_game(None)

        self.assertIsNone(result)
        self.assertEqual(Color_guess.time_left, 59)
        self.assertEqual(Color_guess.score, 1)
        self.assertEqual(Color_guess.scoreLabel.text, "Score: 1")
        self.assertEqual(Color_guess.e.text, "")
        self.assertEqual(len(Color_guess.timeLabel.after_calls), 1)
        self.assertEqual(Color_guess.timeLabel.after_calls[0][0], 1000)

    def test_ordinary_call_succeeds_after_failure_case(self):
        """Assert that an ordinary valid call still succeeds after the failure/absent-result case.
        1. Call start_game with time_left = 0 (failure/absent-result branch reached).
        2. Verify failure state is cleanly handled.
        3. Reset state to valid initial game: time_left = 60, score = 0, e.text = colors_name[1].
        4. Call start_game(None) and assert ordinary success.
        """
        # Step 1: Failure / absent-result case
        Color_guess.time_left = 0
        Color_guess.score = 0
        Color_guess.e.text = "IncorrectGuess"
        result_failure = Color_guess.start_game(None)
        self.assertIsNone(result_failure)
        self.assertEqual(Color_guess.score, 0)
        self.assertEqual(Color_guess.time_left, 0)

        # Step 2: Reset for valid game
        Color_guess.time_left = 60
        Color_guess.score = 0
        Color_guess.colors_name = list(self.initial_colors)
        Color_guess.e.text = Color_guess.colors_name[1]

        # Step 3: Ordinary call after failure
        result_success = Color_guess.start_game(None)
        self.assertIsNone(result_success)
        self.assertEqual(Color_guess.time_left, 59)
        self.assertEqual(Color_guess.score, 1)
        self.assertEqual(Color_guess.scoreLabel.text, "Score: 1")
        self.assertEqual(Color_guess.e.text, "")

    def test_incorrect_guess_rejection_branch(self):
        """Test rejection branch at line 21 when e.get().lower() != colors_name[1].lower().
        Score is not incremented (stays 0), but entry is cleared and colors are shuffled.
        """
        Color_guess.time_left = 60
        Color_guess.score = 0
        Color_guess.e.text = "CompletelyWrongColor"

        Color_guess.start_game(None)

        # Score remains 0 because guess was incorrect
        self.assertEqual(Color_guess.score, 0)
        self.assertEqual(Color_guess.scoreLabel.text, "Score: 0")
        self.assertEqual(Color_guess.e.text, "")
        self.assertEqual(Color_guess.time_left, 59)

    def test_countdown_absent_branch_when_zero(self):
        """Test countdown() fallback branch at line 32: if time_left > 0.
        When time_left <= 0, countdown does nothing (does not decrement below 0,
        does not schedule after() tick).
        """
        Color_guess.time_left = 0
        Color_guess.timeLabel.after_calls = []

        Color_guess.countdown()

        self.assertEqual(Color_guess.time_left, 0)
        self.assertEqual(Color_guess.timeLabel.after_calls, [])


if __name__ == '__main__':
    unittest.main()
