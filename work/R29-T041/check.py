"""Focused contract checks for Password-Generator.gen."""
from __future__ import annotations

import ast
import contextlib
import io
import platform
import string
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "Password-Generator" / "passowrd_gen.py"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
EXPECTED_MAX = "~}|{`_^]\\[@?>=<;:/.-,+*)('&%$#\"!9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"


def load_gen():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "gen")
    namespace = {"string": string, "random": None}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])),
                 str(SOURCE), "exec"), namespace)
    return namespace["gen"]


class PasswordGeneratorTests(unittest.TestCase):
    def run_case(self, input_text, expected_password):
        calls = []

        class DeterministicRandom:
            @staticmethod
            def shuffle(chars):
                calls.append({"before": "".join(chars), "length": len(chars)})
                chars.reverse()
                calls[-1]["after"] = "".join(chars)

        gen = load_gen()
        output = io.StringIO()
        with patch("builtins.input", return_value=input_text) as input_mock, \
             contextlib.redirect_stdout(output):
            gen.__globals__["random"] = DeterministicRandom
            returned = gen()

        actual_output = output.getvalue()
        expected_output = expected_password + "\n"
        # Source precondition: passowrd_gen.py:12 reads a length; lines 14-19
        # assemble the local candidate list from the four character classes.
        self.assertEqual(input_mock.call_args.args[0], "Enter the Password Length: ",
                         f"expected length prompt; actual {input_mock.call_args!r}")
        self.assertEqual(returned, None,
                         f"expected gen() return None; actual {returned!r}")
        self.assertEqual(actual_output, expected_output,
                         f"input {input_text!r}: expected {expected_output!r}; actual {actual_output!r}")
        self.assertEqual(len(calls), 1, f"expected one shuffle; actual {calls!r}")
        self.assertEqual(calls[0]["before"], ALPHABET,
                         f"expected candidate list {ALPHABET!r}; actual {calls[0]['before']!r}")
        self.assertEqual(calls[0]["length"], 94,
                         f"expected 94 unique candidates; actual {calls[0]['length']!r}")
        self.assertEqual(calls[0]["after"], ALPHABET[::-1],
                         f"expected in-place reverse mutation; actual {calls[0]['after']!r}")

    def test_smallest_valid_length(self):
        self.run_case("1", "~")

    def test_ordinary_length(self):
        self.run_case("12", "~}|{`_^]\\[@?")

    def test_full_candidate_set_boundary(self):
        self.run_case("94", EXPECTED_MAX)
        self.assertEqual(len(EXPECTED_MAX), 94,
                         f"expected 94-character boundary result; actual {len(EXPECTED_MAX)}")
        self.assertEqual(len(set(EXPECTED_MAX)), 94,
                         f"expected every candidate exactly once; actual unique count {len(set(EXPECTED_MAX))}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PasswordGeneratorTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T041/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
