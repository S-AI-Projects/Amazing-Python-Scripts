# R29-T052: `MazeSolver` Domain Boundary Checks

## Overview
This task identifies the supported domain boundaries around `MazeSolver` in `AI-based AI Maze Solver/maze.py` and establishes explicit boundary verification.

## Preconditions and Source Anchors
Preconditions established in `AI-based AI Maze Solver/maze.py`:
- **Line 7 (original) / 33**: `self.maze = maze` stores reference to the 2D grid.
- **Line 8 (original) / 34**: `self.rows = len(maze)` calculates total rows.
- **Line 9 (original) / 35**: `self.cols = len(maze[0])` calculates column width from the first row. Raises `IndexError` when `maze` is an empty list (`[]`).
- **Line 10 (original) / 36**: `self.start = (0, 0)` sets fixed starting coordinate.
- **Line 11 (original) / 37**: `self.goal = (self.rows - 1, self.cols - 1)` sets goal at the bottom-right corner.
- **Lines 16-23 (original) / 42-49**: `get_neighbors(node)` verifies boundary checks (`row > 0`, `row < self.rows - 1`, `col > 0`, `col < self.cols - 1`) and obstacle avoidance (`not self.maze[...]`).
- **Line 59 (original) / 85**: `return None` sentinel returned when `open_set` is exhausted without reaching `self.goal`.

## Boundary Table

| Partition | Input `maze` | Dimensions | Contract Preconditions | Expected Output / Behavior | Test Name |
|---|---|---|---|---|---|
| Valid Boundary (Smallest valid input) | `[[0]]` | 1x1 | Lines 8-11: `rows=1, cols=1, start=(0,0), goal=(0,0)` | `solve()` returns `[(0, 0)]`, `heuristic=0`, `neighbors=[]` | `test_smallest_valid_boundary_1x1` |
| Valid Interior (Ordinary input) | `[[0, 0], [0, 0]]` | 2x2 | Lines 8-11: `rows=2, cols=2, start=(0,0), goal=(1,1)` | `start=(0,0), goal=(1,1)`, `heuristic=2`, `solve()` succeeds | `test_ordinary_interior_input_2x2` |
| Valid Boundary (Single-row / 1xN) | `[[0, 0, 0]]` | 1x3 | Lines 8-11: `rows=1, cols=3, start=(0,0), goal=(0,2)` | `rows=1, cols=3`, `get_neighbors((0,0))` returns `[(0, 1)]` | `test_single_row_boundary_1x3` |
| Valid Boundary (Single-column / Nx1) | `[[0], [0], [0]]` | 3x1 | Lines 8-11: `rows=3, cols=1, start=(0,0), goal=(2,0)` | `rows=3, cols=1`, `get_neighbors((0,0))` returns `[(1, 0)]` | `test_single_column_boundary_3x1` |
| Valid Boundary (Unsolvable / Blocked) | `[[0, 1], [1, 0]]` | 2x2 | Lines 16-23 (walls), Line 59 (`return None`) | `get_neighbors((0,0)) == []`, `solve()` returns sentinel `None` | `test_unsolvable_maze_returns_none_sentinel` |
| Explicitly Unsupported (Empty outer list) | `[]` | 0 rows | Line 9: `self.cols = len(maze[0])` | Raises `IndexError` | `test_unsupported_empty_maze_raises_index_error` |
| Immutability / Mutation Check | `[[0, 1], [0, 0]]` | 2x2 | Line 7: `self.maze = maze` | Input list is not modified during initialization or search | `test_maze_input_immutability` |

## Verification
Execute the automated check runner:
```bash
python3 work/R29-T052/check.py
```
Or via native unittest discovery:
```bash
python3 -m unittest discover -s "AI-based AI Maze Solver/tests" -p "test_maze.py" -v
```
All 7 tests pass with zero failures and zero errors.
