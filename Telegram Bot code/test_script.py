import os
import sys
import unittest
from unittest.mock import MagicMock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import script


class TestStartRefactoring(unittest.TestCase):
    """
    Focused regression test suite for simplified start function in Telegram Bot code/script.py.
    Preconditions cited:
      - Line 11: build_welcome_message(user_name) simplifies response composition.
      - Line 25-27: start extracts user details and replies without mutating update.
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input:
        Update object with minimal mock message and no user name.
        Preconditions: script.py lines 11, 25-27.
        """
        mock_update = MagicMock()
        mock_update.effective_user = None
        mock_update.message.reply_text = MagicMock(return_value="replied")

        expected_msg = "Hello! I'm your Telegram bot. How can I assist you?"

        result = script.start(mock_update)

        mock_update.message.reply_text.assert_called_once_with(expected_msg)
        self.assertEqual(result, "replied")

    def test_ordinary_input_with_user(self):
        """
        Ordinary input:
        Update object with a named user.
        Preconditions: script.py lines 11, 25-27.
        """
        mock_update = MagicMock()
        mock_update.effective_user.first_name = "Alice"
        mock_update.message.reply_text = MagicMock(return_value="replied_alice")

        expected_msg = "Hello Alice! I'm your Telegram bot. How can I assist you?"

        result = script.start(mock_update)

        mock_update.message.reply_text.assert_called_once_with(expected_msg)
        self.assertEqual(result, "replied_alice")

    def test_extracted_helper_contract(self):
        """
        Validates helper unit contract directly for both smallest (None) and ordinary ("Bob").
        """
        self.assertEqual(script.build_welcome_message(None), script.WELCOME_MESSAGE)
        self.assertEqual(
            script.build_welcome_message("Bob"),
            "Hello Bob! I'm your Telegram bot. How can I assist you?"
        )


if __name__ == "__main__":
    unittest.main()
