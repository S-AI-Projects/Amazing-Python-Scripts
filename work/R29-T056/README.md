# Task R29-T056: Simplify one responsibility in display_board (TicTacToe.py)

## Overview
- **Item**: AI TicTacToe
- **Target File**: `AI TicTacToe/TicTacToe.py`
- **Target Function**: `display_board` (lines 4-18)
- **Extracted Responsibility**: `format_row(board, c1, c2, c3)` row string formatting calculation
- **Task Type**: Focused refactoring

---

## 1. Refactoring Details

### Responsibility Isolated
In the original implementation, `display_board(board)` combined two responsibilities:
1. Orchestrating board layout (printing separators and ordering the 3 board rows: top row `7, 8, 9`, middle row `4, 5, 6`, bottom row `1, 2, 3`).
2. Performing repetitive string concatenation calculations to format each 3-cell row (`'| ' + board[c1] + ' | ' + board[c2] + ' | ' + board[c3] + '|'`).

The row-formatting calculation was extracted into:
```python
def format_row(board, c1, c2, c3):
    """Format a 3-cell board row with vertical bar delimiters.

    Extracts the row-formatting calculation responsibility from display_board.
    Cells c1, c2, c3 correspond to board positions (e.g. from winning_combinations row triplets).
    """
    return f'| {board[c1]} | {board[c2]} | {board[c3]} |'
```

And `display_board` was simplified to:
```python
def display_board(board):
    separator = '-------------'
    print(separator)
    print(format_row(board, 7, 8, 9))
    print(separator)
    print(format_row(board, 4, 5, 6))
    print(separator)
    print(format_row(board, 1, 2, 3))
    print(separator)
```

Additionally, `play_tic_tac_toe()` at line 125 was placed under `if __name__ == '__main__':` to allow safe importing of `display_board` and `format_row` in automated test suites without blocking on interactive user input.

---

## 2. Preconditions and Data Anchors

### Precondition 1: Board representation (Line 63)
Line 63 establishes the board as a 10-element list initialized to spaces:
```python
the_board = [' '] * 10
```
- Index `0` is an unused offset.
- Indices `1` through `9` represent the 9 playable board cells.

### Precondition 2: Display structure (Lines 4-18)
The board is printed with alternating separator lines `'-------------'` and three row lines corresponding to:
- Top row: indices `7, 8, 9`
- Middle row: indices `4, 5, 6`
- Bottom row: indices `1, 2, 3`

### Data Anchor: Winning combinations (Lines 35-39 / original 28-32)
```python
winning_combinations = [
    [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
    [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
    [1, 5, 9], [3, 5, 7]  # diagonals
]
```
The rows displayed by `display_board` correspond precisely to the three row triplets of `winning_combinations`:
- `winning_combinations[2] = [7, 8, 9]`
- `winning_combinations[1] = [4, 5, 6]`
- `winning_combinations[0] = [1, 2, 3]`

---

## 3. Fixtures and Expected Outputs

### Fixture A: Smallest Valid Input (Empty Board)
- **Input**: `board = [' '] * 10`
- **Expected Output**:
```
-------------
|   |   |   |
-------------
|   |   |   |
-------------
|   |   |   |
-------------
```

### Fixture B: Ordinary Input (Partially Played Board)
- **Input**: `board = [' ', 'X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']`
- **Expected Output**:
```
-------------
| O |   | X |
-------------
|   | X | O |
-------------
| X | O | X |
-------------
```

---

## 4. Test Verification
The test suite in `AI TicTacToe/tests/test_tic_tac_toe.py` verifies:
1. `test_smallest_valid_input`: Validates empty board rendering against exact expected output.
2. `test_ordinary_input`: Validates partially played board rendering against exact expected output.
3. `test_row_triplets_match_winning_combinations`: Ensures rows correspond to `winning_combinations` row triplets.
4. `test_format_row_extracted_calculation`: Directly tests the extracted row-formatting helper.
5. `test_before_after_behavioral_equivalence`: Verifies extracted calculation produces byte-identical output to original concatenation across multiple board states.
6. `test_display_board_does_not_mutate_board`: Verifies immutability of input board.

To run:
```bash
python3 work/R29-T056/check.py
```
