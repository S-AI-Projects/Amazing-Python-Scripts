"""Focused regression runner for Calendar GUI.showCal."""
from __future__ import annotations

import importlib.util
import platform
import sys
import os
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(os.environ.get("SHOWCAL_SOURCE", ROOT / "Calendar GUI" / "Calendar_gui.py"))
FIXTURES = Path(__file__).resolve().parent


class FakeWindow:
    def __init__(self):
        self.title_value = None
        self.geometry_value = None
        self.config_values = []
        self.mainloop_calls = 0

    def title(self, value):
        self.title_value = value

    def geometry(self, value):
        self.geometry_value = value

    def config(self, **kwargs):
        self.config_values.append(kwargs)

    def mainloop(self):
        self.mainloop_calls += 1


class FakeLabel:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.options = kwargs
        self.grid_calls = []

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)


class FakeYearField:
    def __init__(self, text):
        self.text = text
        self.get_calls = 0

    def get(self):
        self.get_calls += 1
        return self.text


def load_module(source: Path, year_field: FakeYearField):
    window = FakeWindow()
    labels = []
    tkinter = types.ModuleType("tkinter")
    tkinter.Tk = lambda: window
    tkinter.Label = lambda parent, **kwargs: labels.append(
        FakeLabel(parent, **kwargs)
    ) or labels[-1]
    tkinter.LEFT = "left"
    previous_tk = sys.modules.get("tkinter")
    sys.modules["tkinter"] = tkinter
    try:
        name = f"calendar_gui_under_test_{id(year_field)}"
        spec = importlib.util.spec_from_file_location(name, source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if previous_tk is None:
            sys.modules.pop("tkinter", None)
        else:
            sys.modules["tkinter"] = previous_tk
    module.year_field = year_field
    return module, window, labels


class ShowCalContractTests(unittest.TestCase):
    def assert_calendar_case(self, text: str, year: int, line_count: int):
        field = FakeYearField(text)
        module, window, labels = load_module(SOURCE, field)

        # Source precondition: Calendar_gui.py:14 converts the field text to int;
        # years 1 and 2024 are valid inputs accepted by calendar.calendar.
        module.showCal()

        expected = (FIXTURES / f"expected-{year}.txt").read_text(encoding="utf-8")
        self.assertEqual(field.get_calls, 1, "year field reads: expected 1, actual %r" % field.get_calls)
        self.assertEqual(field.text, text, "input after call: expected %r, actual %r" % (text, field.text))
        self.assertEqual(window.title_value, "Calendar For The Year")
        self.assertEqual(window.geometry_value, "550x600")
        self.assertEqual(window.config_values, [{"background": "white"}])
        self.assertEqual(window.mainloop_calls, 1)
        self.assertEqual(len(labels), 2, "labels: expected 2, actual %r" % len(labels))
        output_label = labels[1]
        self.assertEqual(type(output_label.options["text"]), str)
        self.assertEqual(output_label.options["text"], expected,
                         "calendar text expected from expected-%s.txt; actual shown in unittest diff" % year)
        self.assertEqual(len(expected.splitlines()), line_count)
        self.assertEqual(output_label.options["justify"], "left")
        self.assertEqual(output_label.grid_calls, [{"row": 2, "column": 1, "padx": 20}])

    def test_smallest_supported_year_one(self):
        self.assert_calendar_case("1", 1, 36)

    def test_ordinary_year_2024(self):
        self.assert_calendar_case("2024", 2024, 35)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ShowCalContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T050/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
