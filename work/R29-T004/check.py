import platform
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Last Access" / "Last Access.py"
RESULTS = Path(__file__).resolve().parent / "results.txt"
TEST_DIRECTORY = "Last Access/tests"
MUTATION_TEST = (
    "test_last_access.LastAccessInvariantTests.test_ordinary_folder_preserves_file_order"
)
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    TEST_DIRECTORY,
    "-p",
    "test_last_access.py",
    "-v",
]


def run_tests(environment=None, test_name=None):
    command = TEST_COMMAND
    if test_name:
        command = [sys.executable, "-m", "unittest", test_name, "-v"]
    return subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def main():
    result = run_tests()
    test_output = result.stdout + result.stderr
    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0
    report_lines = [
        "Focused Last Access invariant/property checks",
        "Requested check command: python3 work/R29-T004/check.py",
        "Native test command: "
        + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
        "No root test configuration exists; the focused tests use standard-library unittest.",
        "Source facts recorded before refactoring: the script prompts for a "
        "folder, filters listdir results through isfile, then prints each "
        "filename and local access time in listing order. The script had no "
        "function and returned None. listdir/isfile/getatime/ctime, input, "
        "and stdout are controlled by fixtures.",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        "Baseline on original script before refactoring: smallest valid empty "
        "folder (path='.') printed 'ENTER THE PATH TO FOLDER\\\\n'; ordinary "
        "folder entries=['first.txt', 'notes', 'second.txt'] printed first.txt "
        "then time-101, followed by second.txt then time-202. Both baseline "
        "tests passed.",
        "Invariant: output contains only regular files in listdir order, "
        "each filename precedes its time line, and fresh equivalent input "
        "listings produce the same output without mutation.",
        "Property generation: 100 bounded cases with seed 20261118; each "
        "case has 0-8 files and 0-5 directories.",
        "",
    ]
    report_lines.extend(
        [
            f"Nonzero test count: {test_count}",
            f"Test process exit code: {result.returncode}",
            "",
            "Literal fixture inputs, expected values, actual values, and test output:",
            test_output.rstrip(),
            "",
        ]
    )
    if test_count == 0:
        RESULTS.write_text("\n".join(report_lines), encoding="utf-8")
        sys.stdout.write(test_output)
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1
    if result.returncode:
        RESULTS.write_text("\n".join(report_lines), encoding="utf-8")
        sys.stdout.write(test_output)
        return result.returncode

    original = SOURCE.read_text(encoding="utf-8")
    original_loop = "for k in files_list:"
    mutant_loop = "for k in reversed(files_list):"
    if original.count(original_loop) != 1:
        raise RuntimeError("Could not uniquely locate Last Access output loop")
    with tempfile.TemporaryDirectory(prefix="r29-t004-mutant-") as directory:
        mutant_source = Path(directory) / SOURCE.name
        mutant_source.write_text(
            original.replace(original_loop, mutant_loop), encoding="utf-8"
        )
        environment = os.environ.copy()
        environment["LAST_ACCESS_SOURCE"] = str(mutant_source)
        test_path = str(ROOT / TEST_DIRECTORY)
        existing_pythonpath = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            test_path
            if not existing_pythonpath
            else test_path + os.pathsep + existing_pythonpath
        )
        mutant = run_tests(environment, MUTATION_TEST)
        mutant_output = mutant.stdout + mutant.stderr

    detected = (
        mutant.returncode != 0
        and "test_ordinary_folder_preserves_file_order" in mutant_output
        and "expected ordered output=" in mutant_output
        and "actual output=" in mutant_output
    )
    report_lines.extend(
        [
            "Mutation experiment: temporary copy reverses the filtered file list "
            "before printing.",
            f"Mutant test command: python3 -m unittest {MUTATION_TEST} -v",
            f"Mutant exit code: {mutant.returncode}",
            f"Mutant detected by same named assertion: {detected}",
            "Readable mutant fixture: entries=['first.txt', 'notes', "
            "'second.txt']; regular files=['first.txt', 'second.txt']; "
            "expected file order=['first.txt', 'second.txt']; mutant order="
            "['second.txt', 'first.txt'].",
            "Mutant output:",
            mutant_output.rstrip(),
            "The mutant exists only in a temporary directory and is not included "
            "in the final source.",
        ]
    )
    RESULTS.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    sys.stdout.write(test_output)
    sys.stdout.write("\n" + "\n".join(report_lines[-8:]) + "\n")
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    return 0 if detected else 1


if __name__ == "__main__":
    raise SystemExit(main())
