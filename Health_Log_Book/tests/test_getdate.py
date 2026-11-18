import contextlib
import datetime
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


SOURCE = Path(__file__).resolve().parents[1] / "main.py"
DATETIME_TYPE = datetime.datetime


def load_health_log_module():
    tkinter = types.ModuleType("tkinter")
    tkinter.__path__ = []
    tkinter.Tk = MagicMock()
    tkinter.Label = MagicMock()
    tkinter.Text = MagicMock()
    tkinter.Button = MagicMock()
    tkinter.Frame = MagicMock()
    tkinter.LEFT = "left"
    messagebox = types.ModuleType("tkinter.messagebox")
    messagebox.showinfo = MagicMock()
    messagebox.showerror = MagicMock()
    ttk = types.ModuleType("tkinter.ttk")
    ttk.Treeview = MagicMock()
    ttk.Scrollbar = MagicMock()
    tkinter.messagebox = messagebox
    tkinter.ttk = ttk
    database = types.ModuleType("database")
    database.connect = MagicMock(return_value=MagicMock(name="connection"))
    database.create_table1 = MagicMock()
    database.create_table2 = MagicMock()
    modules = {
        "tkinter": tkinter,
        "tkinter.messagebox": messagebox,
        "tkinter.ttk": ttk,
        "database": database,
    }
    spec = importlib.util.spec_from_file_location("health_log_main", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load health log module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)
    return module


HEALTH_LOG = load_health_log_module()


class GetDateTests(unittest.TestCase):
    def assert_getdate_returns(self, clock_value, expected):
        clock = MagicMock()
        clock.now.return_value = clock_value
        with patch.object(HEALTH_LOG.datetime, "datetime", clock):
            actual = HEALTH_LOG.getdate()
        print(
            f"getdate() clock_input={clock_value!r}, expected={expected!r}, "
            f"actual={actual!r}, "
            f"type={type(actual).__name__}"
        )
        self.assertIs(type(actual), DATETIME_TYPE)
        self.assertEqual(
            actual,
            expected,
            f"expected datetime={expected!r}; actual={actual!r}",
        )
        clock.now.assert_called_once_with()

    def test_1_smallest_valid_datetime(self):
        # main.py line 12 returns datetime.datetime.now(); getdate has no
        # arguments, so the smallest valid fixture is the smallest clock value.
        clock_value = DATETIME_TYPE(1, 1, 1, 0, 0, 0, 0)
        expected = DATETIME_TYPE(1, 1, 1, 0, 0, 0, 0)
        self.assert_getdate_returns(clock_value, expected)

    def test_2_ordinary_datetime_after_smallest_value(self):
        # main.py lines 10-12 accept no arguments and return the clock value.
        clock_value = DATETIME_TYPE(2024, 6, 15, 12, 34, 56, 789123)
        expected = DATETIME_TYPE(2024, 6, 15, 12, 34, 56, 789123)
        self.assert_getdate_returns(clock_value, expected)


if __name__ == "__main__":
    unittest.main()
