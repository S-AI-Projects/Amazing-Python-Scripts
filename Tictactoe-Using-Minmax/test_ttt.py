import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import main as ttt


class TestInsertLetterWorkedExample(unittest.TestCase):
    """
    Focused test suite with runnable worked examples for insertLetter in Tictactoe-Using-Minmax/main.py.
    Precondition source lines:
      - Line 35: b = board if target_board is None else target_board.
      - Line 36: b[pos] = letter assigns character into board array index.
    """

    def setUp(self):
        # Reset module global board
        ttt.board = [' ' for _ in range(10)]

    def test_smallest_valid_input_worked_example(self):
        """
        Smallest valid input:
        Board index 1 with letter 'X'.
        Preconditions: main.py lines 35, 36.

        Worked Example Walkthrough:
          - Initial state: board[1] is ' '.
          - Invocation: insertLetter('X', 1).
          - Intermediate mutation: slot 1 mutated to 'X'.
          - Final state: board[1] == 'X', all other indices remain ' '.
        """
        self.assertEqual(ttt.board[1], ' ')
        ttt.insertLetter('X', 1)
        self.assertEqual(ttt.board[1], 'X')
        self.assertEqual(ttt.board[2:], [' ' for _ in range(8)])

    def test_ordinary_input_worked_example(self):
        """
        Ordinary input:
        Board index 5 (center) with letter 'O'.
        Preconditions: main.py lines 35, 36.

        Worked Example Walkthrough:
          - Initial state: custom fresh board.
          - Invocation: insertLetter('O', 5, test_board).
          - Final state: test_board[5] == 'O'.
        """
        test_board = [' ' for _ in range(10)]
        self.assertEqual(test_board[5], ' ')
        ttt.insertLetter('O', 5, test_board)
        self.assertEqual(test_board[5], 'O')
        self.assertEqual(test_board[1:5], [' ', ' ', ' ', ' '])
        self.assertEqual(test_board[6:], [' ', ' ', ' ', ' '])

    def test_multiple_sequential_moves_worked_example(self):
        """
        Step-by-step intermediate state verification across sequential moves.
        """
        board_seq = [' ' for _ in range(10)]
        # Step 1: Human places 'X' at position 1
        ttt.insertLetter('X', 1, board_seq)
        self.assertEqual(board_seq[1], 'X')

        # Step 2: Computer places 'O' at position 5
        ttt.insertLetter('O', 5, board_seq)
        self.assertEqual(board_seq[5], 'O')

        # Step 3: Human places 'X' at position 9
        ttt.insertLetter('X', 9, board_seq)
        self.assertEqual(board_seq[9], 'X')


if __name__ == "__main__":
    unittest.main()
