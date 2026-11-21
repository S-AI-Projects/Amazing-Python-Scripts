"""
Focused check runner for Task R29-T052: MazeSolver boundary checks.
"""
from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = Path(__file__).resolve().parent
TEST_DIR = ROOT / "AI-based AI Maze Solver" / "tests"
RESULTS_TXT = WORK_DIR / "results.txt"
RESULTS_JSON = WORK_DIR / "results.json"

TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    str(TEST_DIR),
    "-p",
    "test_maze.py",
    "-v",
]


def main() -> int:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)

    result = subprocess.run(
        TEST_COMMAND,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    test_output = (result.stdout or "") + (result.stderr or "")

    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0

    report_lines = [
        "Focused AI-based AI Maze Solver MazeSolver boundary checks",
        "Requested check command: python3 work/R29-T052/check.py",
        "Native test command: "
        + " ".join([sys.executable, "-m", "unittest", "discover", "-s", "AI-based AI Maze Solver/tests", "-p", "test_maze.py", "-v"]),
        "Test configuration: Standard-library unittest discovery runner.",
        "Target: AI-based AI Maze Solver/maze.py (MazeSolver)",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Nonzero test count: {test_count}",
        f"Test process exit code: {result.returncode}",
        "",
        "Source Preconditions and Boundary Anchors:",
        "- Line 7 (original) / 33: self.maze = maze",
        "- Line 8 (original) / 34: self.rows = len(maze)",
        "- Line 9 (original) / 35: self.cols = len(maze[0]) (IndexError on empty input)",
        "- Line 10 (original) / 36: self.start = (0, 0)",
        "- Line 11 (original) / 37: self.goal = (self.rows - 1, self.cols - 1)",
        "- Lines 16-23 (original) / 42-49: obstacle bounds checking in get_neighbors",
        "- Line 59 (original) / 85: returns sentinel None when goal unreachable",
        "",
        "Boundary Table and Test Cases Summary:",
        "1. test_smallest_valid_boundary_1x1: 1x1 grid [[0]], start=(0,0), goal=(0,0) -> returns [(0,0)]",
        "2. test_ordinary_interior_input_2x2: 2x2 grid [[0,0],[0,0]], start=(0,0), goal=(1,1) -> path reached",
        "3. test_single_row_boundary_1x3: 1x3 grid [[0,0,0]], start=(0,0), goal=(0,2) -> 1 neighbor (0,1)",
        "4. test_single_column_boundary_3x1: 3x1 grid [[0],[0],[0]], start=(0,0), goal=(2,0) -> 1 neighbor (1,0)",
        "5. test_unsolvable_maze_returns_none_sentinel: 2x2 blocked grid [[0,1],[1,0]] -> returns None sentinel",
        "6. test_unsupported_empty_maze_raises_index_error: [] -> raises IndexError at line 9",
        "7. test_maze_input_immutability: verifies input maze grid is not mutated by solver",
        "",
        "Test Runner Output:",
        test_output.rstrip(),
        "",
    ]

    report = "\n".join(report_lines)
    RESULTS_TXT.write_text(report, encoding="utf-8")

    evidence_data = {
        "task": "R29-T052",
        "item": "AI-based AI Maze Solver",
        "target_file": "AI-based AI Maze Solver/maze.py",
        "target_class": "MazeSolver",
        "tool_versions": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "tests_run": test_count,
        "exit_code": result.returncode,
        "success": (result.returncode == 0 and test_count > 0),
        "boundary_table": [
            {
                "partition": "valid_boundary_smallest",
                "input": "[[0]]",
                "dimensions": "1x1",
                "expected": "start=(0,0), goal=(0,0), path=[(0,0)]",
                "test": "test_smallest_valid_boundary_1x1",
            },
            {
                "partition": "valid_interior_ordinary",
                "input": "[[0, 0], [0, 0]]",
                "dimensions": "2x2",
                "expected": "start=(0,0), goal=(1,1), path reached",
                "test": "test_ordinary_interior_input_2x2",
            },
            {
                "partition": "valid_boundary_single_row",
                "input": "[[0, 0, 0]]",
                "dimensions": "1x3",
                "expected": "start=(0,0), goal=(0,2), neighbors=[(0,1)]",
                "test": "test_single_row_boundary_1x3",
            },
            {
                "partition": "valid_boundary_single_col",
                "input": "[[0], [0], [0]]",
                "dimensions": "3x1",
                "expected": "start=(0,0), goal=(2,0), neighbors=[(1,0)]",
                "test": "test_single_column_boundary_3x1",
            },
            {
                "partition": "valid_boundary_unsolvable",
                "input": "[[0, 1], [1, 0]]",
                "dimensions": "2x2",
                "expected": "sentinel None",
                "test": "test_unsolvable_maze_returns_none_sentinel",
            },
            {
                "partition": "explicitly_unsupported",
                "input": "[]",
                "dimensions": "0 rows",
                "expected": "IndexError at line 9",
                "test": "test_unsupported_empty_maze_raises_index_error",
            },
            {
                "partition": "immutability",
                "input": "[[0, 1], [0, 0]]",
                "dimensions": "2x2",
                "expected": "input maze unmutated",
                "test": "test_maze_input_immutability",
            },
        ],
    }
    RESULTS_JSON.write_text(json.dumps(evidence_data, indent=2), encoding="utf-8")

    sys.stdout.write(test_output)
    sys.stdout.write(f"\nSaved evidence to {RESULTS_TXT.relative_to(ROOT)}.\n")

    if test_count == 0:
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
