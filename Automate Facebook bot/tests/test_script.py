"""Contract, regression, and executable documentation tests for FacebookLogin.

Issue: R29-T057
Target: Automate Facebook bot/script.py (FacebookLogin)
Anchors:
- Precondition 1: LOGIN_URL established at line 10:
  `LOGIN_URL = 'https://www.facebook.com/login.php'`
- Precondition 2: Source fixture/data anchor at line 13:
  `groupid = []`
- Precondition 3: FacebookLogin.__init__ credentials & navigation at lines 22-31
- Precondition 4: FacebookLogin.login authentication submission at lines 34-44
- Precondition 5: Group broadcast loop at lines 45-60
"""

import doctest
import io
import sys
import unittest
from pathlib import Path

# Add project root and module directory to path for clean import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_DIR = REPO_ROOT / "Automate Facebook bot"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import script
from script import FacebookLogin, MockWebDriver, LOGIN_URL


class TestFacebookLogin(unittest.TestCase):
    """Executable documentation and contract tests for FacebookLogin."""

    def setUp(self):
        # Reset groupid before each test
        script.groupid = []
        script.message = ""

    def _capture_output(self, fn, *args, **kwargs):
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            result = fn(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return captured.getvalue(), result

    def test_smallest_valid_input(self):
        """Precondition: Line 10 establishes LOGIN_URL = 'https://www.facebook.com/login.php'.
        Precondition: Line 13 establishes data anchor `groupid = []` (0 target groups).
        Precondition: Lines 22-31 initialize credentials and navigate to LOGIN_URL.
        Precondition: Line 45 loop `for i in range(len(groupid)):` runs 0 times when groupid is empty.

        Literal inputs:
        - email: 'test_user@example.com'
        - password: 'password123'
        - groupid: []

        Independently calculated expected outputs:
        - Displayed output: "" (no groups visited, so no waiting message printed)
        - Final driver URL: 'https://www.facebook.com/login.php'
        - Visited URLs: ['https://www.facebook.com/login.php']
        - Email element received: ['test_user@example.com']
        - Password element received: ['password123']
        - Login button clicked: True
        """
        driver = MockWebDriver()
        bot = FacebookLogin('test_user@example.com', 'password123', driver=driver, sleep_fn=lambda s: None)

        # Initial state assertion
        self.assertEqual(driver.current_url, 'https://www.facebook.com/login.php')
        self.assertEqual(driver.visited_urls, ['https://www.facebook.com/login.php'])

        # Data anchor: groupid = []
        script.groupid = []

        # Execute login with smallest valid input
        output, _ = self._capture_output(bot.login)

        # Output assertion
        self.assertEqual(output, "")

        # State assertions
        email_elem = driver.find_element_by_id('email')
        pass_elem = driver.find_element_by_id('pass')
        btn_elem = driver.find_element_by_id('loginbutton')

        self.assertEqual(email_elem.keys, ['test_user@example.com'])
        self.assertEqual(pass_elem.keys, ['password123'])
        self.assertTrue(btn_elem.clicked)
        self.assertEqual(driver.current_url, 'https://www.facebook.com/login.php')
        self.assertEqual(driver.visited_urls, ['https://www.facebook.com/login.php'])

    def test_ordinary_input(self):
        """Precondition: Line 10 LOGIN_URL = 'https://www.facebook.com/login.php'.
        Precondition: Line 13 groupid populated with one group ID ['123456789'].
        Precondition: Line 46 link = 'https://facebook.com/groups/' + groupid[i].
        Precondition: Line 48 print("Waiting for few seconds .......").
        Precondition: Lines 50-59 post box click, message dispatch, submit button click.

        Literal inputs:
        - email: 'ordinary_user@example.com'
        - password: 'secure_password_456'
        - groupid: ['123456789']

        Independently calculated expected outputs:
        - Displayed output: "Waiting for few seconds .......\n"
        - Final driver URL: 'https://facebook.com/groups/123456789'
        - Visited URLs: ['https://www.facebook.com/login.php', 'https://facebook.com/groups/123456789']
        - Post box clicked: True
        - Active element received: ['message']
        - Submit button clicked: True
        """
        driver = MockWebDriver()
        bot = FacebookLogin('ordinary_user@example.com', 'secure_password_456', driver=driver, sleep_fn=lambda s: None)

        # Data anchor with ordinary input
        script.groupid = ['123456789']

        output, _ = self._capture_output(bot.login)

        # Displayed output assertion
        self.assertEqual(output, "Waiting for few seconds .......\n")

        # Driver URL progression
        self.assertEqual(driver.current_url, 'https://facebook.com/groups/123456789')
        self.assertEqual(driver.visited_urls, [
            'https://www.facebook.com/login.php',
            'https://facebook.com/groups/123456789'
        ])

        # Element interaction assertions
        post_box = driver.find_element_by_class_name('a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7')
        submit_btn = driver.find_element_by_class_name('a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5')

        self.assertTrue(post_box.clicked)
        self.assertEqual(driver.active_element.keys, ['message'])
        self.assertTrue(submit_btn.clicked)

    def test_multiple_groups_iteration(self):
        """Precondition: Line 45 loop executes for multiple groups in groupid.
        Literal input: groupid = ['101', '102']
        Expected output: 2 lines of "Waiting for few seconds .......\n"
        """
        driver = MockWebDriver()
        bot = FacebookLogin('multi_user@example.com', 'multi_pass', driver=driver, sleep_fn=lambda s: None)

        script.groupid = ['101', '102']

        output, _ = self._capture_output(bot.login)

        expected_output = "Waiting for few seconds .......\nWaiting for few seconds .......\n"
        self.assertEqual(output, expected_output)
        self.assertEqual(driver.current_url, 'https://facebook.com/groups/102')
        self.assertEqual(driver.visited_urls, [
            'https://www.facebook.com/login.php',
            'https://facebook.com/groups/101',
            'https://facebook.com/groups/102'
        ])

    def test_executable_documentation_worked_example(self):
        """Execute the exact worked example documented in script.FacebookLogin docstring
        and assert its displayed output and end state.
        """
        driver = MockWebDriver()
        bot = FacebookLogin('user@example.com', 'secret123', driver=driver, sleep_fn=lambda s: None)

        # Verify initial state documented in docstring
        self.assertEqual(bot.driver.current_url, 'https://www.facebook.com/login.php')

        # Set target group
        script.groupid = ['123456789']

        # Execute login and capture displayed output
        output, _ = self._capture_output(bot.login)

        # Assert displayed output matches documented output
        self.assertEqual(output, "Waiting for few seconds .......\n")

        # Assert final driver URL matches documented URL
        self.assertEqual(driver.current_url, 'https://facebook.com/groups/123456789')

    def test_doctest_execution(self):
        """Run doctest on script module to verify the documentation example runs cleanly."""
        suite = doctest.DocTestSuite(script)
        runner = unittest.TextTestRunner(stream=io.StringIO())
        result = runner.run(suite)
        self.assertEqual(result.failures, [])
        self.assertEqual(result.errors, [])
        self.assertGreater(result.testsRun, 0)

    def test_decisive_state_transitions(self):
        """Validate the two decisive state transitions identified in the documentation:
        1. Authentication submission transition
        2. Group broadcast loop dispatch transition
        """
        driver = MockWebDriver()
        bot = FacebookLogin('alice@example.com', 'wonderland', driver=driver, sleep_fn=lambda s: None)

        # Initial state before login()
        self.assertEqual(driver.current_url, LOGIN_URL)
        btn = driver.find_element_by_id('loginbutton')
        self.assertFalse(btn.clicked)

        # Execute login with ordinary input
        script.groupid = ['grp_alpha']
        output, _ = self._capture_output(bot.login)

        # Decisive Transition 1: Authentication submitted
        self.assertTrue(btn.clicked)

        # Decisive Transition 2: Group broadcast dispatched
        self.assertEqual(driver.current_url, 'https://facebook.com/groups/grp_alpha')
        self.assertEqual(output, "Waiting for few seconds .......\n")


if __name__ == '__main__':
    unittest.main()
