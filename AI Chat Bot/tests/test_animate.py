import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "main.py"


def load_chatbot_module():
    requests = types.ModuleType("requests")
    requests.post = lambda *args, **kwargs: None
    pyfiglet = types.ModuleType("pyfiglet")
    pyfiglet.figlet_format = lambda text: text
    modules = {"requests": requests, "pyfiglet": pyfiglet}
    spec = importlib.util.spec_from_file_location("ai_chat_bot_main", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load AI Chat Bot module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


CHATBOT = load_chatbot_module()


class AnimateTests(unittest.TestCase):
    def run_animate(self, frame_count):
        output = io.StringIO()
        sleep_calls = 0

        def finish_after_frames(_seconds):
            nonlocal sleep_calls
            sleep_calls += 1
            if sleep_calls == frame_count:
                CHATBOT.done = True

        CHATBOT.done = False
        with (
            patch.object(CHATBOT.sys, "stdout", output),
            patch.object(CHATBOT.time, "sleep", side_effect=finish_after_frames) as sleep,
        ):
            result = CHATBOT.animate()

        return result, output.getvalue(), sleep.call_count

    def test_completion_flag_starts_false(self):
        # main.py lines 18-19 provide the completion state before main runs.
        expected = False
        actual = CHATBOT.done
        print(f"initial done expected={expected!r}, actual={actual!r}")
        self.assertIs(actual, expected, f"expected={expected!r}; actual={actual!r}")

    def test_smallest_run_repeats_identically_and_isolated_from_later_run(self):
        # main.py lines 22-29 take no arguments and advance the spinner until
        # the caller's done flag is set; line 32 emits the final carriage return.
        # One frame is the smallest controlled valid run.
        expected = (None, "\r|\r", 1)
        first = self.run_animate(frame_count=1)
        print(f"smallest animate run expected={expected!r}, actual={first!r}")
        self.assertEqual(first, expected, f"expected={expected!r}; actual={first!r}")

        repeated = self.run_animate(frame_count=1)
        print(f"repeated smallest run expected={expected!r}, actual={repeated!r}")
        self.assertEqual(
            repeated,
            expected,
            f"expected={expected!r}; actual={repeated!r}",
        )

        ordinary_expected = (None, "\r|\r/\r-\r", 3)
        ordinary = self.run_animate(frame_count=3)
        print(
            f"ordinary animate run expected={ordinary_expected!r}, "
            f"actual={ordinary!r}"
        )
        self.assertEqual(
            ordinary,
            ordinary_expected,
            f"expected={ordinary_expected!r}; actual={ordinary!r}",
        )

        after_ordinary = self.run_animate(frame_count=1)
        print(
            f"smallest after ordinary expected={expected!r}, "
            f"actual={after_ordinary!r}"
        )
        self.assertEqual(
            after_ordinary,
            expected,
            f"expected={expected!r}; actual={after_ordinary!r}",
        )


if __name__ == "__main__":
    unittest.main()
