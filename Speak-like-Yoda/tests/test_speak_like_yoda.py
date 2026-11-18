import contextlib
import importlib.util
import io
from pathlib import Path
import random
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "Speak_Like_yoda.py"
SPEC = importlib.util.spec_from_file_location("speak_like_yoda", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load Yoda module from {SOURCE}")
YODA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(YODA)


class SpeakLikeYodaContractTests(unittest.TestCase):
    def test_smallest_valid_input(self):
        # Source line 18 lowercases a string; the empty string is its smallest valid input.
        sentence = ""
        expected_result = None
        expected_output = "\nYour Yodenglish sentence: \n\n"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            actual_result = YODA.speak_like_yoda(sentence)
        actual_output = output.getvalue()
        print(
            f"smallest input={sentence!r}, expected="
            f"{(expected_result, expected_output)!r}, actual="
            f"{(actual_result, actual_output)!r}"
        )
        self.assertIsNone(
            actual_result,
            f"input={sentence!r}; expected={expected_result!r}; "
            f"actual={actual_result!r}",
        )
        self.assertEqual(
            actual_output,
            expected_output,
            f"input={sentence!r}; expected output={expected_output!r}; "
            f"actual output={actual_output!r}",
        )

    def test_ordinary_input_with_fixed_shuffle_seed(self):
        # Source lines 21-25 split, shuffle, join, and print the transformed words.
        sentence = "Hello, brave Jedi!"
        seed = 7
        expected_result = None
        expected_output = "\nYour Yodenglish sentence: \nJedi hello brave\n"
        output = io.StringIO()
        random_state = YODA.random.getstate()
        try:
            YODA.random.seed(seed)
            with contextlib.redirect_stdout(output):
                actual_result = YODA.speak_like_yoda(sentence)
        finally:
            YODA.random.setstate(random_state)
        actual_output = output.getvalue()
        print(
            f"ordinary input={sentence!r}, seed={seed}, expected="
            f"{(expected_result, expected_output)!r}, actual="
            f"{(actual_result, actual_output)!r}"
        )
        self.assertIsNone(
            actual_result,
            f"input={sentence!r}; expected={expected_result!r}; "
            f"actual={actual_result!r}",
        )
        self.assertEqual(
            actual_output,
            expected_output,
            f"input={sentence!r}; expected output={expected_output!r}; "
            f"actual output={actual_output!r}",
        )
        self.assertEqual(
            sentence,
            "Hello, brave Jedi!",
            "expected the immutable input string to remain unchanged",
        )


if __name__ == "__main__":
    unittest.main()
