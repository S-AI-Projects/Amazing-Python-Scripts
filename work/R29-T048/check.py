"""Focused CLI checks for empty and ordinary TODO list behavior."""
from __future__ import annotations

import contextlib
import io
import platform
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "TODO (CLI-VER)" / "todolist.py"
HEADER = "_________TODO LIST__________\n    TIME                   WORK"


def run_todo(inputs):
    with tempfile.TemporaryDirectory() as temp:
        workdir = Path(temp)
        todo_dir = workdir / "TODO (CLI-VER)"
        todo_dir.mkdir()
        path = todo_dir / "todolist.txt"
        if inputs.get("initial_file") is not None:
            path.write_text(inputs["initial_file"], encoding="utf-8")
        answers = iter(inputs["answers"])
        output = io.StringIO()
        with patch("builtins.input", side_effect=lambda: next(answers)), \
             contextlib.redirect_stdout(output):
            old_cwd = Path.cwd()
            try:
                import os
                os.chdir(workdir)
                runpy.run_path(str(SCRIPT), run_name="__main__")
            finally:
                os.chdir(old_cwd)
        return output.getvalue(), path.read_text(encoding="utf-8")


class TodoFailurePathTests(unittest.TestCase):
    def test_missing_empty_list_then_display_succeeds(self):
        # Source precondition: todolist.py:2 initializes no_of_items to 0;
        # lines 4-12 create the missing file with the empty-list header.
        # Literal choices 2, 4, 5 reach the empty delete path (lines 28-29),
        # then exercise a successful display call (lines 76-87) before exit.
        actual_output, actual_file = run_todo({
            "initial_file": None,
            "answers": ["2", "4", "5"],
        })
        expected_file = HEADER
        self.assertEqual(actual_file, expected_file,
                         f"expected file {expected_file!r}; actual {actual_file!r}")
        message = "There is no item in the list kindly add some items"
        self.assertIn(message, actual_output,
                      f"expected empty-list message {message!r}; actual output {actual_output!r}")
        expected_display = "_________TODO LIST__________\n\n    TIME                   WORK"
        self.assertIn(expected_display, actual_output,
                      f"expected displayed header {expected_display!r}; actual output {actual_output!r}")
        self.assertIn("Thank you for using our application", actual_output,
                      f"expected normal exit after display; actual output {actual_output!r}")

    def test_ordinary_list_still_displays_normally(self):
        # Literal fixture creates one item: three lines minus the two header
        # lines at todolist.py:5-10 gives no_of_items=1 (line 13).
        initial = HEADER + "\n1    09:30                   Read"
        actual_output, actual_file = run_todo({
            "initial_file": initial,
            "answers": ["4", "5"],
        })
        self.assertEqual(actual_file, initial,
                         f"expected file unchanged {initial!r}; actual {actual_file!r}")
        expected_item = "1    09:30                   Read"
        self.assertIn(expected_item, actual_output,
                      f"expected item {expected_item!r}; actual output {actual_output!r}")
        self.assertIn("Thank you for using our application", actual_output,
                      f"expected normal exit; actual output {actual_output!r}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TodoFailurePathTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T048/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
