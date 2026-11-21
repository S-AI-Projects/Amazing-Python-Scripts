"""
Focused regression tests for Codechef Scrapper/codechef.py get_problems.

Anchors and Preconditions from Codechef Scrapper/codechef.py:
- Line 18: baseurl = "https://www.codechef.com/problems"
- Line 19: wait = WebDriverWait(driver, 15)
- Lines 22-23: problem_difficulty = {"Beginner": "school", "Easy": "easy",
  "Medium": "medium", "Hard": "hard", "Challenge": "challenge"}
- Line 31 (original) / Line 53: problem_info = {}
- Lines 55-58: driver.get(baseurl + '/' + category); wait.until(...)
- Lines 63-71: loop over range(1, no_of_problems + 1), xpath element lookups, and assignment into problem_info
"""

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

SOURCE = Path(__file__).resolve().parents[1] / "codechef.py"


def load_codechef_module():
    """Load codechef.py with external dependencies and I/O mocked."""
    fpdf_mod = types.ModuleType("fpdf")
    fpdf_mod.FPDF = MagicMock(name="FPDF")

    selenium_mod = types.ModuleType("selenium")
    selenium_mod.__path__ = []

    selenium_common = types.ModuleType("selenium.common")
    selenium_common.__path__ = []
    selenium_common_exc = types.ModuleType("selenium.common.exceptions")

    class TimeoutException(Exception):
        pass

    class NoSuchElementException(Exception):
        pass

    selenium_common_exc.TimeoutException = TimeoutException
    selenium_common_exc.NoSuchElementException = NoSuchElementException

    selenium_webdriver = types.ModuleType("selenium.webdriver")
    selenium_webdriver.__path__ = []

    mock_driver_instance = MagicMock(name="driver_instance")
    mock_chrome = MagicMock(name="Chrome", return_value=mock_driver_instance)
    mock_chrome_options = MagicMock(name="ChromeOptions")
    selenium_webdriver.Chrome = mock_chrome
    selenium_webdriver.ChromeOptions = mock_chrome_options

    selenium_webdriver_common = types.ModuleType("selenium.webdriver.common")
    selenium_webdriver_common.__path__ = []

    selenium_webdriver_common_by = types.ModuleType("selenium.webdriver.common.by")
    selenium_webdriver_common_by.By = types.SimpleNamespace(XPATH="xpath")

    selenium_webdriver_common_dc = types.ModuleType(
        "selenium.webdriver.common.desired_capabilities"
    )
    selenium_webdriver_common_dc.DesiredCapabilities = types.SimpleNamespace(CHROME={})

    selenium_webdriver_support = types.ModuleType("selenium.webdriver.support")
    selenium_webdriver_support.__path__ = []

    selenium_webdriver_support_ec = types.ModuleType(
        "selenium.webdriver.support.expected_conditions"
    )
    selenium_webdriver_support_ec.element_to_be_clickable = MagicMock(
        name="element_to_be_clickable"
    )

    selenium_webdriver_support_ui = types.ModuleType("selenium.webdriver.support.ui")
    selenium_webdriver_support_ui.WebDriverWait = MagicMock(name="WebDriverWait")

    modules = {
        "fpdf": fpdf_mod,
        "selenium": selenium_mod,
        "selenium.common": selenium_common,
        "selenium.common.exceptions": selenium_common_exc,
        "selenium.webdriver": selenium_webdriver,
        "selenium.webdriver.common": selenium_webdriver_common,
        "selenium.webdriver.common.by": selenium_webdriver_common_by,
        "selenium.webdriver.common.desired_capabilities": selenium_webdriver_common_dc,
        "selenium.webdriver.support": selenium_webdriver_support,
        "selenium.webdriver.support.expected_conditions": selenium_webdriver_support_ec,
        "selenium.webdriver.support.ui": selenium_webdriver_support_ui,
    }

    spec = importlib.util.spec_from_file_location("codechef_scrapper", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load codechef module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


CODECHEF = load_codechef_module()


class TestGetProblemsContract(unittest.TestCase):
    """
    Focused regression tests for get_problems in Codechef Scrapper/codechef.py.
    """

    def setUp(self):
        # Fresh mocks for driver and wait before each test
        self.mock_driver = MagicMock()
        self.mock_wait = MagicMock()
        CODECHEF.driver = self.mock_driver
        CODECHEF.wait = self.mock_wait

    def _setup_dom_mock(self, rows):
        """Helper to mock find_element_by_xpath for a list of (name, url) tuples."""

        def fake_find(xpath):
            for idx, (name, url) in enumerate(rows, start=1):
                name_xpath = f"//*[@id='primary-content']/div/div[2]/div/div[2]/table/tbody/tr[{idx}]/td[1]/div/a/b"
                url_xpath = f"//*[@id='primary-content']/div/div[2]/div/div[2]/table/tbody/tr[{idx}]/td[1]/div/a"
                if xpath == name_xpath:
                    el = MagicMock()
                    el.text = name
                    return el
                elif xpath == url_xpath:
                    el = MagicMock()
                    el.get_attribute.return_value = url
                    return el
            raise Exception(f"Unexpected XPath in test: {xpath}")

        self.mock_driver.find_element_by_xpath.side_effect = fake_find

    def test_smallest_valid_input(self):
        """
        Smallest valid input: category='school' (Beginner), no_of_problems=1.
        Source preconditions:
          - Line 18: baseurl = 'https://www.codechef.com/problems'
          - Lines 22-23: problem_difficulty['Beginner'] == 'school'
          - Line 31 (original) / 53: problem_info = {}
        """
        category_input = CODECHEF.problem_difficulty["Beginner"]
        count_input = 1

        mock_rows = [("ATM", "https://www.codechef.com/problems/HS08TEST")]
        self._setup_dom_mock(mock_rows)

        expected_return = {"ATM": "https://www.codechef.com/problems/HS08TEST"}
        expected_url = "https://www.codechef.com/problems/school"

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            actual_return = CODECHEF.get_problems(category_input, count_input)

        print(
            f"smallest_valid: input=({category_input!r}, {count_input}), "
            f"expected={expected_return!r}, actual={actual_return!r}"
        )

        self.assertEqual(actual_return, expected_return)
        self.mock_driver.get.assert_called_once_with(expected_url)
        self.mock_wait.until.assert_called_once()

    def test_ordinary_input(self):
        """
        Ordinary input: category='easy' (Easy), no_of_problems=2.
        Source preconditions:
          - Line 18: baseurl = 'https://www.codechef.com/problems'
          - Lines 22-23: problem_difficulty['Easy'] == 'easy'
          - Lines 63-71: loop over 2 problems
        """
        category_input = CODECHEF.problem_difficulty["Easy"]
        count_input = 2

        mock_rows = [
            ("CIELAB", "https://www.codechef.com/problems/CIELAB"),
            ("HORSES", "https://www.codechef.com/problems/HORSES"),
        ]
        self._setup_dom_mock(mock_rows)

        expected_return = {
            "CIELAB": "https://www.codechef.com/problems/CIELAB",
            "HORSES": "https://www.codechef.com/problems/HORSES",
        }
        expected_url = "https://www.codechef.com/problems/easy"

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            actual_return = CODECHEF.get_problems(category_input, count_input)

        print(
            f"ordinary_input: input=({category_input!r}, {count_input}), "
            f"expected={expected_return!r}, actual={actual_return!r}"
        )

        self.assertEqual(actual_return, expected_return)
        self.mock_driver.get.assert_called_once_with(expected_url)
        self.mock_wait.until.assert_called_once()

    def test_repeated_value_domain_boundary(self):
        """
        Repeated-value domain boundary: duplicate problem names in table rows.
        Source preconditions:
          - Lines 22-23: problem_difficulty['Medium'] == 'medium'
          - Line 70 (original 47): problem_info[problem_name] = problem_url overwrites duplicate keys.
        """
        category_input = CODECHEF.problem_difficulty["Medium"]
        count_input = 2

        mock_rows = [
            ("DUPLICATE_NAME", "https://www.codechef.com/problems/VER1"),
            ("DUPLICATE_NAME", "https://www.codechef.com/problems/VER2"),
        ]
        self._setup_dom_mock(mock_rows)

        # Dictionary key collision means the latest URL is preserved and size is 1
        expected_return = {
            "DUPLICATE_NAME": "https://www.codechef.com/problems/VER2",
        }

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            actual_return = CODECHEF.get_problems(category_input, count_input)

        print(
            f"repeated_value_boundary: input=({category_input!r}, {count_input}), "
            f"expected={expected_return!r}, actual={actual_return!r}"
        )

        self.assertEqual(actual_return, expected_return)
        self.assertEqual(len(actual_return), 1)

    def test_zero_problems_boundary(self):
        """
        Boundary condition: no_of_problems=0.
        Source preconditions:
          - Line 31 (original) / 53: problem_info = {}
          - Line 63 (original 41): range(1, 1) produces empty loop.
        """
        category_input = CODECHEF.problem_difficulty["Beginner"]
        count_input = 0

        self._setup_dom_mock([])
        expected_return = {}

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            actual_return = CODECHEF.get_problems(category_input, count_input)

        print(
            f"zero_problems_boundary: input=({category_input!r}, {count_input}), "
            f"expected={expected_return!r}, actual={actual_return!r}"
        )

        self.assertEqual(actual_return, expected_return)
        self.mock_driver.find_element_by_xpath.assert_not_called()

    def test_observable_mutation_and_state_isolation(self):
        """
        Mutation test:
        Asserts that calling get_problems does not mutate global problem_difficulty,
        and mutating the returned dictionary does not mutate module state.
        Source preconditions:
          - Lines 22-23: problem_difficulty anchor
          - Line 31 (original) / 53: problem_info is local
        """
        expected_difficulty = {
            "Beginner": "school",
            "Easy": "easy",
            "Medium": "medium",
            "Hard": "hard",
            "Challenge": "challenge",
        }
        self.assertEqual(CODECHEF.problem_difficulty, expected_difficulty)

        mock_rows = [("ATM", "https://www.codechef.com/problems/HS08TEST")]
        self._setup_dom_mock(mock_rows)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = CODECHEF.get_problems("school", 1)

        # Global anchor remained unmutated
        self.assertEqual(CODECHEF.problem_difficulty, expected_difficulty)

        # Mutate the returned dictionary
        result["MUTATED_KEY"] = "MUTATED_VALUE"

        # Subsequent call receives isolated fresh dict
        with contextlib.redirect_stdout(output):
            fresh_result = CODECHEF.get_problems("school", 0)

        self.assertEqual(fresh_result, {})
        self.assertNotIn("MUTATED_KEY", fresh_result)
        self.assertEqual(CODECHEF.problem_difficulty, expected_difficulty)


if __name__ == "__main__":
    unittest.main(verbosity=2)
