import platform
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
RESULTS = Path(__file__).resolve().parent / "results.txt"
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "Pdf2Video_Converter/tests",
    "-p",
    "test_pdf2text.py",
    "-v",
]


def main():
    result = subprocess.run(
        TEST_COMMAND,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    test_output = result.stdout + result.stderr
    test_count_match = re.search(r"Ran (\d+) tests?", test_output)
    test_count = int(test_count_match.group(1)) if test_count_match else 0
    report = "\n".join(
        [
            "Focused Pdf2Video pdf2text boundary checks",
            "Requested check command: python3 work/R29-T002/check.py",
            "Native test command: "
            + " ".join(["python3", "-m", "unittest", *TEST_COMMAND[3:]]),
            "No repository-wide pytest/unittest configuration was found; "
            "the focused tests use standard-library unittest.",
            "Baseline result: before adding the docstring, the same two tests "
            "passed against the original implementation.",
            "Source boundary contract, from script.py lines 15-47: PDF_file "
            "is passed to convert_from_path at 500 DPI; the returned pages are "
            "iterated and each OCR string is appended, with '-\\n' replaced "
            "by ''. Zero pages therefore return the initialized empty string; "
            "one page returns its OCR text after normalization. The source "
            "does not define invalid-input exception behavior.",
            "Boundary table (page sequence returned by convert_from_path):",
            "| Page count | Source contract | Expected return | Test |",
            "| 0 | No page loop iterations; initialized text is returned | '' | test_zero_pages_returns_empty_text |",
            "| 1 | Save and OCR one page, then normalize '-\\n' | 'Boundarytext\\n' | test_one_page_returns_ocr_text_with_existing_hyphen_normalization |",
            "External dependencies, PDF conversion, OCR, image I/O, and file "
            "deletion are mocked; import only loads the target module.",
            f"Python version: {sys.version.replace(chr(10), ' ')}",
            "Unittest version: standard library bundled with this Python version",
            f"Platform: {platform.platform()}",
            f"Nonzero test count: {test_count}",
            f"Test process exit code: {result.returncode}",
            "",
            "Literal fixture inputs, expected values, actual values, and test output:",
            test_output.rstrip(),
            "",
        ]
    )
    RESULTS.write_text(report, encoding="utf-8")
    sys.stdout.write(test_output)
    sys.stdout.write(f"\nSaved evidence to {RESULTS.relative_to(ROOT)}.\n")
    if test_count == 0:
        sys.stderr.write("The focused unittest command did not run any tests.\n")
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
