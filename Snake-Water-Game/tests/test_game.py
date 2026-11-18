import contextlib
import importlib.util
import io
import os
from pathlib import Path
import random
import sys
import types
import unittest
from unittest.mock import patch


DEFAULT_SOURCE = Path(__file__).resolve().parents[1] / "Snake-Water Game.py"
SOURCE = Path(os.environ.get("SNAKE_WATER_SOURCE", DEFAULT_SOURCE))


def load_game_module():
    tkinter = types.ModuleType("tkinter")
    tkinter.__path__ = []
    tkinter_tix = types.ModuleType("tkinter.tix")
    tkinter_tix.Tree = object
    with patch.dict(sys.modules, {"tkinter": tkinter, "tkinter.tix": tkinter_tix}):
        spec = importlib.util.spec_from_file_location("snake_water_game", SOURCE)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load game module from {SOURCE}")
        module = importlib.util.module_from_spec(spec)
        with patch("builtins.input", return_value="snake"):
            with patch("random.randint", return_value=0):
                with contextlib.redirect_stdout(io.StringIO()):
                    spec.loader.exec_module(module)
    return module


GAME_MODULE = load_game_module()


class GameContractTests(unittest.TestCase):
    def assert_game_result(self, comp, mine, expected):
        original_inputs = (comp, mine)
        first_inputs = tuple(original_inputs)
        second_inputs = tuple(original_inputs)
        first_actual = GAME_MODULE.game(*first_inputs)
        second_actual = GAME_MODULE.game(*second_inputs)
        print(
            f"input={original_inputs!r}, expected={expected!r}, "
            f"actual_first={first_actual!r}, actual_second={second_actual!r}"
        )
        self.assertIs(type(first_actual), type(expected))
        self.assertEqual(
            first_actual,
            expected,
            f"input={original_inputs!r}; expected={expected!r}; "
            f"actual={first_actual!r}",
        )
        self.assertEqual(second_actual, expected)
        self.assertEqual(first_inputs, original_inputs)
        self.assertEqual(second_inputs, original_inputs)
        self.assertEqual(original_inputs, (comp, mine))

    def test_smallest_valid_draw_returns_none(self):
        # Source line 24 defines the domain and includes the shortest option,
        # "gun"; source line 9 establishes equal inputs as a draw.
        comp = "gun"
        mine = "gun"
        expected = None
        self.assert_game_result(comp, mine, expected)

    def test_ordinary_input_water_beaten_by_snake(self):
        # Source line 24 establishes both values in the choice domain;
        # source lines 14-15 establish water versus snake as a win.
        comp = "water"
        mine = "snake"
        expected = True
        self.assert_game_result(comp, mine, expected)


if __name__ == "__main__":
    unittest.main()
