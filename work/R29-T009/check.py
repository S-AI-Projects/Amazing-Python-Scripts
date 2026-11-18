import contextlib
import hashlib
import importlib.util
import io
import platform
from pathlib import Path
import random
import re
import string
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Speak-like-Yoda" / "Speak_Like_yoda.py"
RESULTS = Path(__file__).resolve().parent / "results.txt"
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "Speak-like-Yoda/tests",
    "-p",
    "test_speak_like_yoda.py",
    "-v",
]
INPUT_SEED = 1729
SHUFFLE_SEED = 7100
SIZES = (256, 16_384, 262_144)
REPETITIONS = 5
VOCABULARY = ("Yoda,", "Jedi!", "wise", "force.")
PUNCTUATION_TO_REMOVE = string.punctuation.replace("'", "")


class DiscardOutput:
    def write(self, text):
        return len(text)

    def flush(self):
        pass


def load_module():
    spec = importlib.util.spec_from_file_location("speak_like_yoda", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Yoda module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_input(size, repetition):
    generator = random.Random(INPUT_SEED + size + repetition)
    words = generator.choices(VOCABULARY, k=size // 4 + 2)
    sentence = " ".join(words)[:size]
    return (" " + sentence)[1:]


def expected_output(sentence, seed):
    normalized = sentence.lower().translate(str.maketrans("", "", PUNCTUATION_TO_REMOVE))
    words = normalized.split()
    random.Random(seed).shuffle(words)
    return "\nYour Yodenglish sentence: \n" + " ".join(words).capitalize() + "\n"


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def benchmark(module):
    lines = [
        "Complexity experiment",
        "Input-size variable: n = number of characters in the input sentence.",
        "Sizes are exact input character counts; each repetition gets a newly "
        "generated sentence from a deterministic local seed.",
        f"Input generation seed base: {INPUT_SEED}",
        f"Shuffle seed base: {SHUFFLE_SEED}",
        f"Repetitions per size: {REPETITIONS}",
        "Timed interval: one speak_like_yoda call, after import, input creation, "
        "and random seeding; stdout is redirected to a no-op stream. Output "
        "verification occurs in a separate untimed call. This excludes process "
        "startup, input construction, terminal I/O, and compilation.",
        "Each timed call is followed by a fresh deterministic verification call; "
        "expected output is independently computed with translate/split/join.",
        "",
        "n characters | repetition ns (5) | median ns | range ns | input SHA-256s | "
        "expected/actual output SHA-256s",
    ]

    for size in SIZES:
        times = []
        input_hashes = []
        output_hashes = []
        for repetition in range(REPETITIONS):
            sentence = make_input(size, repetition)
            seed = SHUFFLE_SEED + repetition
            expected = expected_output(sentence, seed)
            input_hashes.append(digest(sentence))

            module.random.seed(seed)
            with contextlib.redirect_stdout(DiscardOutput()):
                start = time.perf_counter_ns()
                timed_result = module.speak_like_yoda(sentence)
                elapsed = time.perf_counter_ns() - start
            if timed_result is not None:
                raise AssertionError(
                    f"n={size}, repetition={repetition}: expected return None, "
                    f"actual {timed_result!r}"
                )
            times.append(elapsed)

            verification_input = make_input(size, repetition)
            verification_seed = SHUFFLE_SEED + repetition
            actual_output = io.StringIO()
            module.random.seed(verification_seed)
            with contextlib.redirect_stdout(actual_output):
                verification_result = module.speak_like_yoda(verification_input)
            actual = actual_output.getvalue()
            if verification_result is not None or actual != expected:
                raise AssertionError(
                    f"n={size}, repetition={repetition}: expected "
                    f"(None, {expected[:120]!r}..., sha256={digest(expected)}), "
                    f"actual ({verification_result!r}, {actual[:120]!r}..., "
                    f"sha256={digest(actual)})"
                )
            output_hashes.append((digest(expected), digest(actual)))

        median = sorted(times)[len(times) // 2]
        lines.append(
            f"{size:>12} | {times!r} | {median:>9} | "
            f"{min(times)}-{max(times)} | {input_hashes!r} | "
            f"{output_hashes!r}"
        )
    lines.extend(
        [
            "",
            "All observed cases passed correctness; timings are observations, "
            "not a pass/fail threshold.",
            "Code-based complexity: string processing and the shuffle loop "
            "perform O(n) work and use O(n) auxiliary space in the worst case, "
            "where n is input characters. The punctuation loop scans the string "
            "for a fixed 31 punctuation characters. Counting each random index "
            "selection as O(1) gives a worst-case O(n) bound; Python's "
            "rejection-based random selection makes total runtime expected "
            "O(n), not a strict worst-case claim. Timings are observations, "
            "not proof of the bound.",
        ]
    )
    return "\n".join(lines)


def main():
    test_result = subprocess.run(
        TEST_COMMAND,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    test_output = test_result.stdout + test_result.stderr
    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0

    report = "\n".join(
        [
            "Focused speak_like_yoda contract and complexity checks",
            "Requested check command: python3 work/R29-T009/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "Test configuration: no root Python test configuration exists; "
            "the project has no test runner for this item, so standard-library "
            "unittest is used.",
            "Source facts recorded before edits: the function takes one string, "
            "returns None, does not mutate its immutable input, shuffles a local "
            "word list using random, and prints to stdout. Import is side-effect "
            "free; direct script execution reads stdin. It uses only Python's "
            "standard-library random and string modules.",
            "Baseline before the complexity docstring change: 2 tests passed "
            "against the original source with no expected/actual mismatches.",
            f"Python version: {sys.version.replace(chr(10), ' ')}",
            "Unittest version: standard library bundled with this Python version",
            f"Platform: {platform.platform()}",
            f"Nonzero test count: {test_count}",
            f"Test process exit code: {test_result.returncode}",
            "",
            "Contract test inputs and expected versus actual results:",
            test_output.rstrip(),
            "",
        ]
    )
    if test_count == 0:
        RESULTS.write_text(report, encoding="utf-8")
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1
    if test_result.returncode:
        RESULTS.write_text(report, encoding="utf-8")
        sys.stdout.write(test_output)
        return test_result.returncode

    experiment = benchmark(load_module())
    report += experiment + "\n"
    RESULTS.write_text(report, encoding="utf-8")
    sys.stdout.write(test_output)
    sys.stdout.write(experiment + "\n")
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
