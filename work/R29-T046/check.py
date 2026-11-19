"""Isolated checks for the elapsed-time calculation in the Colab notebook."""
from __future__ import annotations

import ast
import json
import platform
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NOTEBOOK = REPO / "Torrent to Drive Downloader" / "leech.ipynb"
README = REPO / "Torrent to Drive Downloader" / "readme.md"


def load_formatter():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    source = next(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code" and "def format_elapsed" in "".join(cell["source"])
    )
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "format_elapsed")
    isolated = ast.Module(body=[function], type_ignores=[])
    namespace = {}
    exec(compile(ast.fix_missing_locations(isolated), str(NOTEBOOK), "exec"), namespace)
    return namespace["format_elapsed"]


FORMAT_ELAPSED = load_formatter()


class ElapsedTimeTests(unittest.TestCase):
    def assert_format(self, seconds, expected):
        # The README fixture and notebook calculation use elapsed seconds;
        # the notebook's original begin/end values are seconds from time.time().
        actual = FORMAT_ELAPSED(seconds)
        original = "{} min : {} sec".format(int(seconds // 60), int(seconds % 60))
        self.assertEqual(actual, expected,
                         f"expected {expected!r} for {seconds!r}; actual {actual!r}")
        self.assertEqual(actual, original,
                         f"expected behavior preserved as {original!r}; actual {actual!r}")

    def test_smallest_elapsed_duration(self):
        self.assert_format(0.0, "0 min : 0 sec")

    def test_ordinary_elapsed_duration(self):
        self.assert_format(125.9, "2 min : 5 sec")

    def test_readme_documents_same_examples(self):
        text = README.read_text(encoding="utf-8")
        for expected in ("0 min : 0 sec", "2 min : 5 sec"):
            self.assertIn(expected, text, f"expected README to document {expected!r}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ElapsedTimeTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T046/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
