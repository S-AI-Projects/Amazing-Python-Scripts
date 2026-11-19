"""
Focused boundary checks for InstaBot in Unfollowers-Insta
"""
import sys
import io
import contextlib
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Unfollowers-Insta" / "insta_bot_bb8.py"

# Mock selenium and getpass before loading source
mock_selenium = MagicMock()
mock_webdriver = MagicMock()
mock_selenium.webdriver = mock_webdriver
sys.modules["selenium"] = mock_selenium
sys.modules["selenium.webdriver"] = mock_webdriver

import importlib.util
spec = importlib.util.spec_from_file_location("insta_bot_bb8", str(SOURCE_PATH))
insta_module = importlib.util.module_from_spec(spec)
sys.modules["insta_bot_bb8"] = insta_module
spec.loader.exec_module(insta_module)


class InstaBotBoundaryTests(unittest.TestCase):

    def setUp(self):
        # Create an InstaBot instance without interactive input
        with patch("builtins.input", return_value="testuser"), \
             patch("insta_bot_bb8.getpass", return_value="secretpw"):
            self.bot = insta_module.InstaBot()
        self.bot.driver.execute_script.side_effect = None

    def test_smallest_valid_input(self):
        # Precondition established at source line 83:
        # last_ht, ht = 0, 1
        # Smallest scroll: execute_script returns height 1 on first scroll
        mock_box = MagicMock()
        mock_box.find_elements_by_tag_name.return_value = []
        self.bot.driver.find_element_by_xpath.return_value = mock_box
        self.bot.driver.execute_script.return_value = 1

        with patch("time.sleep"):
            names = self.bot.scroll_list("/html/body/div[4]/div/div/div[2]")

        expected_names = []
        self.assertEqual(names, expected_names, f"Expected {expected_names} but got {names}")

        # Smallest input for unfollowers computation: empty lists
        self.bot.following = []
        self.bot.followers = []
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.bot.get_unfollowers()

        expected_unfollowers = []
        self.assertEqual(self.bot.unfollowers, expected_unfollowers)

    def test_ordinary_input(self):
        # Precondition at line 83: last_ht, ht = 0, 1
        # Ordinary scroll: height grows to 200, then repeats 200 so loop terminates
        mock_link1 = MagicMock()
        mock_link1.text = "friend1"
        mock_link2 = MagicMock()
        mock_link2.text = "friend2"

        mock_box = MagicMock()
        mock_box.find_elements_by_tag_name.return_value = [mock_link1, mock_link2]
        self.bot.driver.find_element_by_xpath.return_value = mock_box
        self.bot.driver.execute_script.side_effect = [200, 200]

        with patch("time.sleep"):
            names = self.bot.scroll_list("/html/body/div[4]/div/div/div[2]")

        expected_names = ["friend1", "friend2"]
        self.assertEqual(names, expected_names)

        # Ordinary input for unfollowers
        self.bot.following = ["alice", "bob", "charlie"]
        self.bot.followers = ["alice"]
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.bot.get_unfollowers()

        expected_unfollowers = ["bob", "charlie"]
        self.assertEqual(self.bot.unfollowers, expected_unfollowers)

    def test_boundary_conditions(self):
        # Preconditions at lines 102 to 105:
        # self.unfollowers = [x for x in self.following if x not in self.followers]
        # Boundary 1: Complete overlap, everyone follows back
        self.bot.following = ["alice", "bob"]
        self.bot.followers = ["alice", "bob", "charlie"]
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.bot.get_unfollowers()
        self.assertEqual(self.bot.unfollowers, [])

        # Boundary 2: Disjoint sets, nobody follows back
        self.bot.following = ["user1", "user2"]
        self.bot.followers = ["user3", "user4"]
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.bot.get_unfollowers()
        self.assertEqual(self.bot.unfollowers, ["user1", "user2"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(InstaBotBoundaryTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T012/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
