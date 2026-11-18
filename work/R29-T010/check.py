import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Snake-Water-Game" / "Snake-Water Game.py"
TEST_FILE = "test_game.GameContractTests.test_ordinary_input_water_beaten_by_snake"
TEST_DIRECTORY = "Snake-Water-Game/tests"
RESULTS = Path(__file__).resolve().parent / "results.txt"
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    TEST_DIRECTORY,
    "-p",
    "test_game.py",
    "-v",
]


def run_tests(environment=None, test_name=None):
    command = TEST_COMMAND
    if test_name:
        command = [
            sys.executable,
            "-m",
            "unittest",
            test_name,
            "-v",
        ]
    return subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def main():
    baseline = run_tests()
    baseline_output = baseline.stdout + baseline.stderr
    baseline_match = re.search(r"Ran (\d+) tests?", baseline_output)
    baseline_count = int(baseline_match.group(1)) if baseline_match else 0
    report_lines = [
        "Focused Snake-Water game contract and mutation checks",
        "Requested check command: python3 work/R29-T010/check.py",
        "Native test command: "
        + " ".join(["python3", "-m", "unittest", "discover", "-s", TEST_DIRECTORY, "-p", "test_game.py", "-v"]),
        "No root test configuration exists; the focused tests use standard-library unittest.",
        "Source facts recorded before edits: game(comp, mine) takes two strings, "
        "returns None on a tie, True when the player wins, and False otherwise. "
        "The choice tuple is defined at source line 24. The function does not "
        "mutate its string arguments. It relies on random only in top-level game "
        "startup; import-time input/output and that random choice are mocked.",
        f"Python version: {sys.version.replace(chr(10), ' ')}",
        "Unittest version: standard library bundled with this Python version",
        f"Platform: {platform.platform()}",
        f"Baseline test count: {baseline_count}",
        f"Baseline exit code: {baseline.returncode}",
        "Baseline input/output transcript:",
        baseline_output.rstrip(),
        "",
    ]

    if baseline_count == 0 or baseline.returncode:
        RESULTS.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        sys.stdout.write(baseline_output)
        return baseline.returncode or 1

    original = SOURCE.read_text(encoding="utf-8")
    original_line = "elif (comp == 'water' and mine == 'snake'):"
    mutant_line = "elif (comp == 'water' and mine == 'water'):"
    if original.count(original_line) != 1:
        raise RuntimeError("Could not uniquely locate intended comparison to mutate")
    with tempfile.TemporaryDirectory(prefix="r29-t010-mutant-") as directory:
        mutant_source = Path(directory) / SOURCE.name
        mutant_source.write_text(original.replace(original_line, mutant_line), encoding="utf-8")
        environment = os.environ.copy()
        environment["SNAKE_WATER_SOURCE"] = str(mutant_source)
        test_path = str(ROOT / TEST_DIRECTORY)
        existing_pythonpath = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            test_path
            if not existing_pythonpath
            else test_path + os.pathsep + existing_pythonpath
        )
        mutant = run_tests(environment, TEST_FILE)
        mutant_output = mutant.stdout + mutant.stderr

    detected = (
        mutant.returncode != 0
        and "test_ordinary_input_water_beaten_by_snake" in mutant_output
        and "expected=True" in mutant_output
        and "actual=False" in mutant_output
    )
    report_lines.extend(
        [
            "Mutation experiment: temporary copy changed the water-versus-snake "
            "comparison from mine == 'snake' to mine == 'water'.",
            f"Mutant test command: python3 -m unittest {TEST_FILE} -v",
            f"Mutant exit code: {mutant.returncode}",
            f"Mutant detected by same named assertion: {detected}",
            "Mutant input: comp='water', mine='snake'; independently expected=True; "
            "mutant actual=False.",
            "Mutant output:",
            mutant_output.rstrip(),
            "The mutant exists only in a temporary directory and is not included "
            "in the final source.",
        ]
    )
    RESULTS.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    sys.stdout.write(baseline_output)
    sys.stdout.write("\n" + "\n".join(report_lines[-8:]) + "\n")
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    return 0 if detected else 1


if __name__ == "__main__":
    raise SystemExit(main())
