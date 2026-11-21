"""
Differential cross-check tests for Auto-Fill-Google-Forms comparing
against an independent reference oracle.

Source Preconditions and Anchors:
- Lines 6-8: inputName, inputEmailID, inputPhone XPaths
- Line 11: Submit button XPath
- Line 27: csv_input = csv.DictReader(f_input)
- Lines 28-31: row['name'], row['email'], row['phone_number']
- Lines 36-45: Submission loop over records
"""

import copy
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

SOURCE = Path(__file__).resolve().parents[1] / "test.py"
CSV_PATH = Path(__file__).resolve().parents[1] / "input.csv"

# Mock selenium modules
mock_selenium = types.ModuleType("selenium")
mock_selenium.__path__ = []
mock_webdriver = types.ModuleType("selenium.webdriver")
mock_webdriver.__path__ = []
mock_keys = types.ModuleType("selenium.webdriver.common.keys")
mock_keys.Keys = MagicMock(name="Keys")
mock_webdriver.common = types.ModuleType("selenium.webdriver.common")
mock_webdriver.common.keys = mock_keys

mock_selenium.webdriver = mock_webdriver
mock_webdriver.Firefox = MagicMock(name="Firefox")

modules = {
    "selenium": mock_selenium,
    "selenium.webdriver": mock_webdriver,
    "selenium.webdriver.common": mock_webdriver.common,
    "selenium.webdriver.common.keys": mock_keys,
}

# Load module under test
spec = importlib.util.spec_from_file_location("auto_fill_module", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load auto-fill module from {SOURCE}")
auto_fill_module = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, modules):
    spec.loader.exec_module(auto_fill_module)


class IndependentReferenceOracle:
    """
    Independent reference oracle for CSV record parsing and form submission.
    Does not call the functions under test. Uses manual line tokenization and column indices.
    """

    @staticmethod
    def parse_csv_lines(raw_csv_text):
        lines = [line.strip() for line in raw_csv_text.strip().splitlines() if line.strip()]
        if not lines:
            return []
        header = [col.strip() for col in lines[0].split(",")]
        name_idx = header.index("name")
        email_idx = header.index("email")
        phone_idx = header.index("phone_number")

        results = []
        for line in lines[1:]:
            parts = [p.strip() for p in line.split(",")]
            results.append({
                "name": parts[name_idx],
                "email": parts[email_idx],
                "phone_number": parts[phone_idx]
            })
        return results


class AutoFillGoogleFormsCrossCheckTests(unittest.TestCase):
    """
    Independent reference comparison test suite for Auto-Fill-Google-Forms.
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: CSV with 1 header and 1 record.
        Source preconditions:
          - Line 27: DictReader header mapping
          - Lines 28-31: field extraction
          - Lines 36-45: 1 iteration of submission loop
        """
        csv_text = "name,email,phone_number\nAlice,alice@example.com,1234\n"
        f_input = io.StringIO(csv_text)

        names, emails, phones = auto_fill_module.read_records(f_input)
        actual_submissions = auto_fill_module.fill_form_records(
            names, emails, phones, sleep_fn=lambda: None
        )

        # Expected output from independent oracle
        expected_submissions = IndependentReferenceOracle.parse_csv_lines(csv_text)

        print(
            f"smallest_valid: input=1 row, "
            f"expected={expected_submissions!r}, actual={actual_submissions!r}"
        )

        self.assertEqual(len(actual_submissions), 1)
        self.assertEqual(actual_submissions, expected_submissions)

    def test_ordinary_input(self):
        """
        Ordinary input: input.csv file containing 6 student records.
        Source preconditions:
          - Line 26: with open('input.csv', 'r') as f_input
          - Line 27: csv_input = csv.DictReader(f_input)
        """
        raw_text = CSV_PATH.read_text(encoding="utf-8")
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            names, emails, phones = auto_fill_module.read_records(f)

        actual_submissions = auto_fill_module.fill_form_records(
            names, emails, phones, sleep_fn=lambda: None
        )

        expected_submissions = IndependentReferenceOracle.parse_csv_lines(raw_text)

        print(
            f"ordinary_input: rows={len(actual_submissions)}, "
            f"first_actual={actual_submissions[0]!r}, "
            f"first_expected={expected_submissions[0]!r}"
        )

        self.assertEqual(len(actual_submissions), 6)
        self.assertEqual(actual_submissions, expected_submissions)

    def test_differential_twenty_domain_inputs(self):
        """
        Cross-check against independent oracle across 25 diverse valid inputs.
        Domain includes various names, email domains, phone formats, hyphens, and whitespace.
        """
        sample_records = [
            ("User01", "user01@test.com", "100-001"),
            ("User02", "user02@domain.org", "100-002"),
            ("User03", "user03@company.co", "100-003"),
            ("User04", "user04@school.edu", "100-004"),
            ("User05", "user05@mail.net", "100-005"),
            ("Mary Jane", "mary.jane@email.com", "+1-555-0101"),
            ("Bob Smith", "bob_smith@provider.com", "5550102"),
            ("Charlie", "charlie+tag@sample.com", "123-456-7890"),
            ("Dr. Watson", "watson@baker.st", "020-7946-0911"),
            ("Sherlock", "holmes@baker.st", "020-7946-0912"),
            ("Grace Hopper", "grace@navy.mil", "703-555-0199"),
            ("Ada Lovelace", "ada@analytical.org", "44-20-7946"),
            ("Alan Turing", "alan@bletchley.uk", "44-1908-654"),
            ("Margaret Hamilton", "margaret@mit.edu", "617-253-1000"),
            ("Katherine Johnson", "katherine@nasa.gov", "757-864-1000"),
            ("Dennis Ritchie", "dmr@bell-labs.com", "908-582-3000"),
            ("Ken Thompson", "ken@bell-labs.com", "908-582-3001"),
            ("Linus Torvalds", "torvalds@kernel.org", "503-555-0145"),
            ("Guido van Rossum", "guido@python.org", "31-20-555-0100"),
            ("Tim Berners-Lee", "timbl@w3.org", "617-253-2613"),
            ("Radia Perlman", "radia@spanningtree.net", "425-555-0188"),
            ("Vint Cerf", "vint@internetsociety.org", "703-555-0177"),
            ("Donald Knuth", "knuth@stanford.edu", "650-723-2300"),
            ("Barbara Liskov", "liskov@csail.mit.edu", "617-253-5860"),
            ("Leslie Lamport", "lamport@microsoft.com", "425-703-0000"),
        ]

        csv_lines = ["name,email,phone_number"]
        for n, e, p in sample_records:
            csv_lines.append(f"{n},{e},{p}")
        csv_payload = "\n".join(csv_lines) + "\n"

        f_input = io.StringIO(csv_payload)
        names, emails, phones = auto_fill_module.read_records(f_input)
        actual_submissions = auto_fill_module.fill_form_records(
            names, emails, phones, sleep_fn=lambda: None
        )

        expected_submissions = IndependentReferenceOracle.parse_csv_lines(csv_payload)

        print(
            f"differential_twenty_domain_inputs: tested {len(actual_submissions)} inputs, "
            f"all match independent oracle!"
        )

        self.assertEqual(len(actual_submissions), 25)
        self.assertEqual(len(actual_submissions), len(expected_submissions))
        self.assertEqual(actual_submissions, expected_submissions)

    def test_input_mutation_isolation(self):
        """
        Verify that fill_form_records does not mutate input lists.
        """
        names = ["Alice", "Bob"]
        emails = ["alice@test.com", "bob@test.com"]
        phones = ["111", "222"]

        names_copy = copy.deepcopy(names)
        emails_copy = copy.deepcopy(emails)
        phones_copy = copy.deepcopy(phones)

        auto_fill_module.fill_form_records(names, emails, phones, sleep_fn=lambda: None)

        self.assertEqual(names, names_copy)
        self.assertEqual(emails, emails_copy)
        self.assertEqual(phones, phones_copy)

    def test_browser_automation_interactions(self):
        """
        Verify browser automation interactions (send_keys, click, back) with mocked browser.
        Precondition anchors:
          - Lines 6-8: XPath constants
          - Line 11: Submit XPath
          - Lines 37-44: send_keys, submit click, browser back
        """
        mock_browser = MagicMock()
        mock_element = MagicMock()
        mock_browser.find_element_by_xpath.return_value = mock_element

        names = ["TestUser"]
        emails = ["test@example.com"]
        phones = ["999-0000"]

        auto_fill_module.fill_form_records(
            names, emails, phones, browser=mock_browser, sleep_fn=lambda: None
        )

        # 3 input fields + 1 submit button = 4 xpath calls per record
        self.assertEqual(mock_browser.find_element_by_xpath.call_count, 4)
        self.assertEqual(mock_element.send_keys.call_count, 3)
        self.assertEqual(mock_element.click.call_count, 1)
        self.assertEqual(mock_browser.back.call_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
