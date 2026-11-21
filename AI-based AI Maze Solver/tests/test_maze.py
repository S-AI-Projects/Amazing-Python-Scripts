"""
Focused boundary regression tests for MazeSolver in AI-based AI Maze Solver/maze.py.

Source Preconditions and Data Anchors:
- Line 7 (original) / 33: self.maze = maze
- Line 8 (original) / 34: self.rows = len(maze)
- Line 9 (original) / 35: self.cols = len(maze[0])
- Line 10 (original) / 36: self.start = (0, 0)
- Line 11 (original) / 37: self.goal = (self.rows - 1, self.cols - 1)
- Lines 13-24 (original) / 39-50: get_neighbors bounds checking
- Lines 26-27 (original) / 52-53: Manhattan distance heuristic
- Lines 29-59 (original) / 55-85: A* search solve() implementation and sentinel return None
"""

import copy
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "maze.py"

spec = importlib.util.spec_from_file_location("maze_module", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load maze module from {SOURCE}")
maze_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maze_module)
MazeSolver = maze_module.MazeSolver


class TestMazeSolverBoundaries(unittest.TestCase):
    """
    Boundary test suite locking down supported domain boundaries of MazeSolver.
    """

    def test_smallest_valid_boundary_1x1(self):
        """
        Smallest valid boundary input: 1x1 grid [[0]].
        Source preconditions:
          - Line 8/34: self.rows = len(maze) -> 1
          - Line 9/35: self.cols = len(maze[0]) -> 1
          - Line 10/36: self.start = (0, 0)
          - Line 11/37: self.goal = (self.rows - 1, self.cols - 1) -> (0, 0)
        """
        maze_input = [[0]]
        solver = MazeSolver(maze_input)

        expected_rows = 1
        expected_cols = 1
        expected_start = (0, 0)
        expected_goal = (0, 0)
        expected_heuristic = 0
        expected_neighbors = []
        expected_path = [(0, 0)]

        actual_rows = solver.rows
        actual_cols = solver.cols
        actual_start = solver.start
        actual_goal = solver.goal
        actual_heuristic = solver.heuristic((0, 0))
        actual_neighbors = solver.get_neighbors((0, 0))
        actual_path = solver.solve()

        print(
            f"smallest_valid_1x1: input={maze_input!r}, "
            f"expected_path={expected_path!r}, actual_path={actual_path!r}"
        )

        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_cols, expected_cols)
        self.assertEqual(actual_start, expected_start)
        self.assertEqual(actual_goal, expected_goal)
        self.assertEqual(actual_heuristic, expected_heuristic)
        self.assertEqual(actual_neighbors, expected_neighbors)
        self.assertEqual(actual_path, expected_path)

    def test_ordinary_interior_input_2x2(self):
        """
        Ordinary interior input: 2x2 grid [[0, 0], [0, 0]].
        Source preconditions:
          - Line 8/34: self.rows = len(maze) -> 2
          - Line 9/35: self.cols = len(maze[0]) -> 2
          - Line 10/36: self.start = (0, 0)
          - Line 11/37: self.goal = (2 - 1, 2 - 1) -> (1, 1)
        """
        maze_input = [[0, 0], [0, 0]]
        solver = MazeSolver(maze_input)

        expected_rows = 2
        expected_cols = 2
        expected_start = (0, 0)
        expected_goal = (1, 1)
        expected_start_heuristic = 2
        expected_goal_heuristic = 0
        expected_start_neighbors = [(1, 0), (0, 1)]

        actual_rows = solver.rows
        actual_cols = solver.cols
        actual_start = solver.start
        actual_goal = solver.goal
        actual_start_heuristic = solver.heuristic(actual_start)
        actual_goal_heuristic = solver.heuristic(actual_goal)
        actual_start_neighbors = solver.get_neighbors(actual_start)
        actual_path = solver.solve()

        print(
            f"ordinary_interior_2x2: input={maze_input!r}, "
            f"start={actual_start}, goal={actual_goal}, path={actual_path!r}"
        )

        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_cols, expected_cols)
        self.assertEqual(actual_start, expected_start)
        self.assertEqual(actual_goal, expected_goal)
        self.assertEqual(actual_start_heuristic, expected_start_heuristic)
        self.assertEqual(actual_goal_heuristic, expected_goal_heuristic)
        self.assertEqual(actual_start_neighbors, expected_start_neighbors)
        self.assertIsNotNone(actual_path)
        self.assertEqual(actual_path[-1], expected_goal)

    def test_single_row_boundary_1x3(self):
        """
        Dimensional boundary: single-row 1x3 maze [[0, 0, 0]].
        Source preconditions:
          - Line 8/34: self.rows = 1
          - Line 9/35: self.cols = 3
          - Line 10/36: self.start = (0, 0)
          - Line 11/37: self.goal = (0, 2)
        """
        maze_input = [[0, 0, 0]]
        solver = MazeSolver(maze_input)

        expected_rows = 1
        expected_cols = 3
        expected_start = (0, 0)
        expected_goal = (0, 2)
        expected_neighbors = [(0, 1)]

        actual_rows = solver.rows
        actual_cols = solver.cols
        actual_start = solver.start
        actual_goal = solver.goal
        actual_neighbors = solver.get_neighbors((0, 0))

        print(
            f"single_row_1x3: input={maze_input!r}, "
            f"expected_goal={expected_goal}, actual_goal={actual_goal}"
        )

        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_cols, expected_cols)
        self.assertEqual(actual_start, expected_start)
        self.assertEqual(actual_goal, expected_goal)
        self.assertEqual(actual_neighbors, expected_neighbors)

    def test_single_column_boundary_3x1(self):
        """
        Dimensional boundary: single-column 3x1 maze [[0], [0], [0]].
        Source preconditions:
          - Line 8/34: self.rows = 3
          - Line 9/35: self.cols = 1
          - Line 10/36: self.start = (0, 0)
          - Line 11/37: self.goal = (2, 0)
        """
        maze_input = [[0], [0], [0]]
        solver = MazeSolver(maze_input)

        expected_rows = 3
        expected_cols = 1
        expected_start = (0, 0)
        expected_goal = (2, 0)
        expected_neighbors = [(1, 0)]

        actual_rows = solver.rows
        actual_cols = solver.cols
        actual_start = solver.start
        actual_goal = solver.goal
        actual_neighbors = solver.get_neighbors((0, 0))

        print(
            f"single_column_3x1: input={maze_input!r}, "
            f"expected_goal={expected_goal}, actual_goal={actual_goal}"
        )

        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_cols, expected_cols)
        self.assertEqual(actual_start, expected_start)
        self.assertEqual(actual_goal, expected_goal)
        self.assertEqual(actual_neighbors, expected_neighbors)

    def test_unsolvable_maze_returns_none_sentinel(self):
        """
        Solution boundary: completely blocked maze [[0, 1], [1, 0]].
        Source preconditions:
          - Lines 16-23/42-49: obstacles (truthy values) are excluded from neighbors
          - Line 59/85: returns sentinel None when open_set is exhausted
        """
        maze_input = [[0, 1], [1, 0]]
        solver = MazeSolver(maze_input)

        expected_neighbors = []
        expected_result = None

        actual_neighbors = solver.get_neighbors((0, 0))
        actual_result = solver.solve()

        print(
            f"unsolvable_maze: input={maze_input!r}, "
            f"expected={expected_result!r}, actual={actual_result!r}"
        )

        self.assertEqual(actual_neighbors, expected_neighbors)
        self.assertIsNone(actual_result)

    def test_unsupported_empty_maze_raises_index_error(self):
        """
        Unsupported boundary: empty list [] on outer boundary.
        Source precondition:
          - Line 9/35: self.cols = len(maze[0]) raises IndexError when maze is empty.
        """
        empty_input = []
        print(f"unsupported_empty: input={empty_input!r}, expected_exception=IndexError")

        with self.assertRaises(IndexError):
            MazeSolver(empty_input)

    def test_maze_input_immutability(self):
        """
        Mutation boundary: ensures solver initialization and solve() do not mutate
        the caller-provided maze input grid.
        Source preconditions:
          - Line 7/33: self.maze = maze
        """
        original_maze = [[0, 1], [0, 0]]
        maze_copy = copy.deepcopy(original_maze)

        solver = MazeSolver(maze_copy)
        solver.solve()

        print(
            f"immutability: original={original_maze!r}, actual={maze_copy!r}"
        )

        self.assertEqual(maze_copy, original_maze)


if __name__ == "__main__":
    unittest.main(verbosity=2)
