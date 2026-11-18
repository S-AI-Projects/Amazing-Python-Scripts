import contextlib
import io
import os
from pathlib import Path
import posixpath
import random
import runpy
import types
import unittest
from unittest.mock import patch


DEFAULT_SOURCE = Path(__file__).resolve().parents[1] / "Last Access.py"
SOURCE = Path(os.environ.get("LAST_ACCESS_SOURCE", DEFAULT_SOURCE))
MODULE = runpy.run_path(str(SOURCE))
LAST_ACCESS = MODULE["last_access"]


class LastAccessInvariantTests(unittest.TestCase):
    def run_listing(self, path, entries, file_names, timestamps):
        entries_before = entries.copy()
        timestamp_map = dict(timestamps)
        namespace = LAST_ACCESS.__globals__
        fixtures = {
            "listdir": lambda _path: entries.copy(),
            "isfile": lambda candidate: candidate.replace("\\", "/").rsplit(
                "/", 1
            )[-1]
            in file_names,
            "join": posixpath.join,
            "os": types.SimpleNamespace(
                path=types.SimpleNamespace(
                    getatime=lambda candidate: timestamp_map[
                        candidate.replace("\\", "/").rsplit("/", 1)[-1]
                    ]
                )
            ),
            "time": types.SimpleNamespace(
                ctime=lambda timestamp: f"time-{timestamp}"
            ),
        }
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with patch.dict(namespace, fixtures):
                actual_result = LAST_ACCESS(path)
        actual_output = output.getvalue()
        self.assertEqual(entries, entries_before, "input entries must not mutate")
        return actual_result, actual_output, entries_before

    def test_smallest_valid_empty_folder(self):
        # README.md line 11 establishes a folder path input; source line 9
        # lists folder entries. An empty folder is the smallest valid case.
        path = "."
        entries = []
        expected_result = None
        expected_output = ""
        actual_result, actual_output, _ = self.run_listing(path, entries, set(), {})
        print(
            f"path={path!r}, entries={entries!r}, expected="
            f"{(expected_result, expected_output)!r}, actual="
            f"{(actual_result, actual_output)!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(actual_output, expected_output)

    def test_ordinary_folder_preserves_file_order(self):
        # README.md lines 3 and 5 promise file access times; source line 9
        # keeps listdir order while filtering, lines 10-14 print each file.
        path = "fixture-folder"
        entries = ["first.txt", "notes", "second.txt"]
        file_names = {"first.txt", "second.txt"}
        timestamps = {"first.txt": 101, "second.txt": 202}
        expected_result = None
        expected_output = (
            "first.txt\n"
            "Last access time(Local time): time-101\n"
            "second.txt\n"
            "Last access time(Local time): time-202\n"
        )
        actual_result, actual_output, before = self.run_listing(
            path, entries, file_names, timestamps
        )
        repeated_result, repeated_output, repeated_before = self.run_listing(
            path, entries.copy(), file_names, timestamps
        )
        print(
            f"path={path!r}, entries={entries!r}, expected="
            f"{(expected_result, expected_output)!r}, actual="
            f"{(actual_result, actual_output)!r}"
        )
        self.assertIsNone(actual_result)
        self.assertEqual(
            actual_output,
            expected_output,
            f"expected ordered output={expected_output!r}; "
            f"actual output={actual_output!r}",
        )
        self.assertEqual(before, entries)
        self.assertIsNone(repeated_result)
        self.assertEqual(repeated_output, expected_output)
        self.assertEqual(repeated_before, entries)

    def test_cli_keeps_prompt_for_empty_folder(self):
        # README.md line 11 establishes interactive folder input; source
        # lines 18-20 retain that prompt and invoke last_access.
        output = io.StringIO()
        with patch("builtins.input", return_value="."):
            with patch("os.listdir", return_value=[]):
                with contextlib.redirect_stdout(output):
                    runpy.run_path(str(SOURCE), run_name="__main__")
        expected = "ENTER THE PATH TO FOLDER\n"
        actual = output.getvalue()
        print(f"CLI expected={expected!r}, actual={actual!r}")
        self.assertEqual(actual, expected)

    def test_generated_folders_preserve_order_and_input(self):
        # Source line 9 filters listdir results without sorting; source
        # lines 12-15 print each remaining file and timestamp in that order.
        generator = random.Random(20261118)
        for case_number in range(100):
            file_count = generator.randint(0, 8)
            directory_count = generator.randint(0, 5)
            files = [f"file-{case_number}-{index}.txt" for index in range(file_count)]
            directories = [
                f"directory-{case_number}-{index}"
                for index in range(directory_count)
            ]
            entries = files + directories
            generator.shuffle(entries)
            file_names = set(files)
            timestamps = {
                name: generator.randint(1, 1_000_000) for name in files
            }
            expected_result = None
            expected_rows = []
            for name in entries:
                if name in file_names:
                    expected_rows.append(
                        (
                            name,
                            f"Last access time(Local time): time-{timestamps[name]}",
                        )
                    )
            expected_lines = [
                line for row in expected_rows for line in row
            ]
            expected_output = (
                "\n".join(expected_lines) + "\n" if expected_lines else ""
            )
            fresh_entries = entries.copy()
            actual_result, actual_output, before = self.run_listing(
                "generated-folder", fresh_entries, file_names, timestamps
            )
            repeated_result, repeated_output, repeated_before = self.run_listing(
                "generated-folder", entries.copy(), file_names, timestamps
            )
            actual_rows = list(
                zip(
                    actual_output.splitlines()[::2],
                    actual_output.splitlines()[1::2],
                )
            )
            print(
                f"property case={case_number}, entries={entries!r}, "
                f"expected={(expected_result, expected_rows)!r}, actual="
                f"{(actual_result, actual_rows)!r}"
            )
            self.assertIsNone(
                actual_result,
                f"case={case_number}; expected result=None; actual={actual_result!r}",
            )
            self.assertEqual(
                actual_output,
                expected_output,
                f"case={case_number}; entries={entries!r}; "
                f"expected={expected_output!r}; actual={actual_output!r}",
            )
            self.assertEqual(
                actual_rows,
                expected_rows,
                f"case={case_number}; expected rows={expected_rows!r}; "
                f"actual rows={actual_rows!r}",
            )
            self.assertEqual(
                before,
                entries,
                f"case={case_number}; expected unchanged entries={entries!r}; "
                f"actual={before!r}",
            )
            self.assertIsNone(
                repeated_result,
                f"case={case_number}; expected result=None; "
                f"actual={repeated_result!r}",
            )
            self.assertEqual(
                repeated_output,
                expected_output,
                f"case={case_number}; fresh equivalent input changed output; "
                f"expected={expected_output!r}; actual={repeated_output!r}",
            )
            self.assertEqual(
                repeated_before,
                entries,
                f"case={case_number}; expected unchanged second input={entries!r}; "
                f"actual={repeated_before!r}",
            )


if __name__ == "__main__":
    unittest.main()
