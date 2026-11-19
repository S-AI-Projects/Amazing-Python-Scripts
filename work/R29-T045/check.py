"""Isolated state and dependency checks for change_wall."""
from __future__ import annotations

import ast
import platform
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "Changing_Wall_Paper_using_python" / "Changing_Wall_Paper.py"


def load_change_wall(setter, path_var, result_var):
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "change_wall")
    namespace = {"set_wallpaper": setter, "path": path_var, "result": result_var}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])),
                 str(SOURCE), "exec"), namespace)
    return namespace["change_wall"]


class FakeVar:
    def __init__(self, value=""):
        self.value = value
        self.history = []

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.history.append(value)


class ChangeWallTests(unittest.TestCase):
    def test_empty_path_failure_sets_expected_status(self):
        # Source precondition: Changing_Wall_Paper.py:13 passes str(path.get())
        # to the external setter; line 17 maps its exception to this status.
        calls = []
        def failing_setter(value):
            calls.append(value)
            raise OSError("mocked missing image")
        path = FakeVar("")
        result = FakeVar()
        load_change_wall(failing_setter, path, result)()
        self.assertEqual(calls, [""], f"expected setter calls ['']; actual {calls!r}")
        self.assertEqual(path.get(), "", f"expected input unchanged ''; actual {path.get()!r}")
        self.assertEqual(result.value, "Wallpaper not found !",
                         f"expected failure status; actual {result.value!r}")

    def test_smallest_valid_path_succeeds(self):
        # Minimal non-empty relative path accepted by the public path variable.
        calls = []
        path = FakeVar("a.jpg")
        result = FakeVar()
        load_change_wall(calls.append, path, result)()
        self.assertEqual(calls, ["a.jpg"], f"expected setter calls ['a.jpg']; actual {calls!r}")
        self.assertEqual(result.value, "success",
                         f"expected success status; actual {result.value!r}")

    def test_ordinary_path_succeeds(self):
        # Valid ordinary fixture reaches the same call at source line 13.
        calls = []
        path_text = "Pictures/sunset.jpg"
        path = FakeVar(path_text)
        result = FakeVar()
        load_change_wall(calls.append, path, result)()
        self.assertEqual(calls, [path_text],
                         f"expected setter calls {[path_text]!r}; actual {calls!r}")
        self.assertEqual(path.get(), path_text,
                         f"expected input unchanged {path_text!r}; actual {path.get()!r}")
        self.assertEqual(result.value, "success",
                         f"expected success status; actual {result.value!r}")

    def test_failure_then_success_does_not_leak_external_state(self):
        outcomes = [OSError("first call fails"), None]
        calls = []
        def controlled_setter(value):
            calls.append(value)
            outcome = outcomes.pop(0)
            if outcome is not None:
                raise outcome
        path = FakeVar("/tmp/missing.jpg")
        result = FakeVar()
        change_wall = load_change_wall(controlled_setter, path, result)

        change_wall()
        first_expected = "Wallpaper not found !"
        self.assertEqual(result.value, first_expected,
                         f"expected first result {first_expected!r}; actual {result.value!r}")
        path.set("/tmp/ordinary.jpg")
        change_wall()
        second_expected = "success"
        self.assertEqual(result.value, second_expected,
                         f"expected second result {second_expected!r}; actual {result.value!r}")
        self.assertEqual(calls, ["/tmp/missing.jpg", "/tmp/ordinary.jpg"],
                         f"expected isolated setter inputs; actual {calls!r}")
        self.assertEqual(result.history, [first_expected, second_expected],
                         f"expected fresh statuses; actual {result.history!r}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ChangeWallTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T045/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
