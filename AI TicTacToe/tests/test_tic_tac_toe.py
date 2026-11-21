"""Contract and regression tests for display_board and format_row in AI TicTacToe.

Issue: R29-T056
Target: AI TicTacToe/TicTacToe.py (display_board and extracted format_row)
Anchors:
- Precondition 1: Board representation established at line 63:
  `the_board = [' '] * 10` where index 0 is unused and indices 1-9 represent cells.
- Precondition 2: Display structure established at lines 4-11:
  Alternating '-------------' separators with row triplets formatted '| c1 | c2 | c3 |'.
- Data Anchor: winning_combinations established at lines 28-32:
  winning_combinations = [
      [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
      [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
      [1, 5, 9], [3, 5, 7]  # diagonals
  ]
"""

import io
import sys
import unittest
from pathlib import Path

# Add project root and module directory to path for clean import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_DIR = REPO_ROOT / "AI TicTacToe"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import TicTacToe


class TestDisplayBoard(unittest.TestCase):
    """Regression and refactoring tests for display_board and format_row."""

    def setUp(self):
        # Anchor from lines 28-32 in AI TicTacToe/TicTacToe.py
        self.winning_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
            [1, 5, 9], [3, 5, 7]  # diagonals
        ]

    def _capture_display(self, board):
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            TicTacToe.display_board(board)
        finally:
            sys.stdout = old_stdout
        return captured_output.getvalue()

    def test_smallest_valid_input(self):
        """Precondition: Line 63 establishes the smallest valid board representation:
        `the_board = [' '] * 10` with 10 empty string elements.

        Precondition: Lines 4-11 define display_board rendering rows [7, 8, 9],
        [4, 5, 6], and [1, 2, 3] separated by '-------------'.
        """
        smallest_valid_board = [' '] * 10
        expected_output = (
            "-------------\n"
            "|   |   |   |\n"
            "-------------\n"
            "|   |   |   |\n"
            "-------------\n"
            "|   |   |   |\n"
            "-------------\n"
        )
        actual_output = self._capture_display(smallest_valid_board)
        self.assertEqual(actual_output, expected_output)

    def test_ordinary_input(self):
        """Precondition: Board with in-progress gameplay markers placed via place_marker (lines 23-24).
        board = [' ', 'X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']
        Positions:
        Top row (7, 8, 9): board[7]='O', board[8]=' ', board[9]='X' -> '| O |   | X |'
        Middle row (4, 5, 6): board[4]=' ', board[5]='X', board[6]='O' -> '|   | X | O |'
        Bottom row (1, 2, 3): board[1]='X', board[2]='O', board[3]='X' -> '| X | O | X |'
        """
        ordinary_board = [' ', 'X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']
        expected_output = (
            "-------------\n"
            "| O |   | X |\n"
            "-------------\n"
            "|   | X | O |\n"
            "-------------\n"
            "| X | O | X |\n"
            "-------------\n"
        )
        actual_output = self._capture_display(ordinary_board)
        self.assertEqual(actual_output, expected_output)

    def test_row_triplets_match_winning_combinations(self):
        """Data Anchor: Verify that the 3 rows printed by display_board correspond to
        winning_combinations row triplets from lines 28-29:
        Row 3: [7, 8, 9] (winning_combinations[2])
        Row 2: [4, 5, 6] (winning_combinations[1])
        Row 1: [1, 2, 3] (winning_combinations[0])
        """
        # Board with distinct values for all 9 cells
        board = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        actual_lines = self._capture_display(board).splitlines()

        # Lines 0, 2, 4, 6 are separators
        self.assertEqual(actual_lines[0], '-------------')
        self.assertEqual(actual_lines[2], '-------------')
        self.assertEqual(actual_lines[4], '-------------')
        self.assertEqual(actual_lines[6], '-------------')

        # Check row 3 (combinations [7, 8, 9])
        r3 = self.winning_combinations[2]
        self.assertEqual(actual_lines[1], f'| {board[r3[0]]} | {board[r3[1]]} | {board[r3[2]]} |')

        # Check row 2 (combinations [4, 5, 6])
        r2 = self.winning_combinations[1]
        self.assertEqual(actual_lines[3], f'| {board[r2[0]]} | {board[r2[1]]} | {board[r2[2]]} |')

        # Check row 1 (combinations [1, 2, 3])
        r1 = self.winning_combinations[0]
        self.assertEqual(actual_lines[5], f'| {board[r1[0]]} | {board[r1[1]]} | {board[r1[2]]} |')

    def test_format_row_extracted_calculation(self):
        """Test the extracted responsibility: format_row(board, c1, c2, c3).
        Verifies formatting a 3-cell row with vertical bar delimiters.
        """
        board = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.assertEqual(TicTacToe.format_row(board, 1, 2, 3), '| A | B | C |')
        self.assertEqual(TicTacToe.format_row(board, 4, 5, 6), '| D | E | F |')
        self.assertEqual(TicTacToe.format_row(board, 7, 8, 9), '| G | H | I |')

    def test_before_after_behavioral_equivalence(self):
        """Verify that extracted format_row produces byte-for-byte identical output
        to the original inline string concatenation ('| ' + board[c1] + ' | ' + board[c2] + ' | ' + board[c3] + '|').
        """
        sample_boards = [
            [' '] * 10,
            [' ', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'],
            [' ', 'O', ' ', 'X', ' ', 'O', ' ', 'X', ' ', 'O'],
            [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ]
        row_triplets = [(7, 8, 9), (4, 5, 6), (1, 2, 3)]

        for board in sample_boards:
            for c1, c2, c3 in row_triplets:
                original_calc = '| ' + str(board[c1]) + ' | ' + str(board[c2]) + ' | ' + str(board[c3]) + ' |'
                refactored_calc = TicTacToe.format_row(board, c1, c2, c3)
                self.assertEqual(refactored_calc, original_calc)

    def test_display_board_does_not_mutate_board(self):
        """Verify display_board is a pure read-only operation and does not mutate the board."""
        board = [' ', 'X', 'O', ' ', 'X', 'O', ' ', 'X', 'O', ' ']
        original_copy = list(board)
        self._capture_display(board)
        self.assertEqual(board, original_copy)


if __name__ == '__main__':
    unittest.main()
