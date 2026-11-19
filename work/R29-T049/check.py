"""Correctness and scaling checks for Search_File.search_files."""
from __future__ import annotations

import importlib.util
import os
import platform
import random
import statistics
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO / "Search_File" / "searching_specific_files.py"
REPORT_PATH = Path(__file__).resolve().parent / "measurements.txt"


def load_search_module():
    spec = importlib.util.spec_from_file_location("searching_specific_files", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load_search_module()


class SearchFileTests(unittest.TestCase):
    def test_smallest_valid_directory(self):
        # Public precondition: searching_specific_files.py:10 accepts a root;
        # line 12 walks it and line 13 applies the literal '*.mp4' pattern.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "clip.mp4").write_bytes(b"")
            actual = list(SEARCH.search_files(str(root), "*.mp4"))
            expected = [str(root / "clip.mp4")]
            self.assertEqual(actual, expected, f"expected {expected!r}; actual {actual!r}")

    def test_ordinary_directory_filters_and_orders_matches(self):
        # The same public precondition is exercised over a nested directory.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "a.mp4").write_bytes(b"")
            (root / "b.txt").write_bytes(b"")
            nested = root / "nested"
            nested.mkdir()
            (nested / "c.mp4").write_bytes(b"")
            expected = [str(root / "a.mp4"), str(nested / "c.mp4")]
            actual = list(SEARCH.search_files(str(root), "*.mp4"))
            self.assertEqual(actual, expected, f"expected {expected!r}; actual {actual!r}")


def make_tree(base: Path, size: int, seed: int):
    rng = random.Random(seed)
    root = base / f"case-{size}-{seed}"
    root.mkdir()
    expected = []
    for index in range(size):
        directory = root / f"d{index % 5}"
        directory.mkdir(exist_ok=True)
        ext = ".mp4" if index % 4 == 0 else ".txt"
        # Fixed-seed suffix keeps generated names reproducible and unique.
        name = f"{index:05d}-{rng.randrange(1_000_000):06d}{ext}"
        (directory / name).write_bytes(b"")
        if ext == ".mp4":
            expected.append(str(directory / name))
    return root, expected


def run_measurements():
    rows = []
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        for size in (20, 200, 1000):
            durations = []
            for repetition in range(5):
                root, expected = make_tree(base, size, seed=29049 + repetition)
                start = time.perf_counter_ns()
                actual_raw = list(SEARCH.search_files(str(root), "*.mp4"))
                elapsed = time.perf_counter_ns() - start
                # Correctness checks are deliberately outside the timed interval.
                actual = sorted(actual_raw)
                if actual != sorted(expected):
                    raise AssertionError(
                        f"size={size} repetition={repetition}: "
                        f"expected {expected!r}; actual {actual!r}"
                    )
                durations.append(elapsed / 1_000_000)
            ordered = sorted(durations)
            median = statistics.median(durations)
            rows.append((size, median, min(durations), max(durations), ordered))

    report = [
        "Search_File scaling observations",
        f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})",
        "Input size n: number of files in five temporary directories; 1 in 4 names ends in .mp4.",
        "Timed region: list(search_files(root, '*.mp4')); tree creation and output comparison excluded.",
        "Each repetition uses a fresh tree and fixed seed 29049 + repetition; 5 repetitions per size.",
        "Times are observations only; correctness has no speed threshold.",
        "n files | median ms | min ms | max ms | all five ms",
    ]
    for size, median, low, high, ordered in rows:
        report.append(
            f"{size} | {median:.3f} | {low:.3f} | {high:.3f} | "
            + ", ".join(f"{value:.3f}" for value in ordered)
        )
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SearchFileTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T049/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    if not result.wasSuccessful():
        return 1
    run_measurements()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
