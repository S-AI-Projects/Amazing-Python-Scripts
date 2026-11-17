import os
import sys
import unittest
from unittest.mock import MagicMock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

tts_module = __import__("text-to-speech")


class TestTextToSpeechScaling(unittest.TestCase):
    """
    Focused test suite measuring work done and scaling of Text_to_speech in Text-To-Speech/text-to-speech.py.
    Preconditions cited:
      - Line 36: Message = entry_field.get().
      - Line 37: speech = gTTS(text=Message).
      - Line 38: speech.save('Data.mp3').
      - Line 39: playsound('Data.mp3').
      - Line 40: os.remove('Data.mp3').
    """

    def setUp(self):
        self.mock_speech = MagicMock()
        self.mock_gtts = MagicMock(return_value=self.mock_speech)
        self.mock_player = MagicMock()
        self.mock_cleaner = MagicMock()

    def test_smallest_valid_input_measurement(self):
        """
        Smallest valid input:
        1-character string "a".
        Preconditions: text-to-speech.py lines 36-40.
        """
        input_text = "a"
        result = tts_module.Text_to_speech(
            message=input_text,
            gtts_cls=self.mock_gtts,
            player_fn=self.mock_player,
            cleaner_fn=self.mock_cleaner
        )

        self.mock_gtts.assert_called_once_with(text=input_text)
        self.assertEqual(result["text_length"], 1)
        self.assertEqual(result["char_operations"], 1)
        self.assertEqual(result["word_count"], 1)

    def test_ordinary_input_measurement(self):
        """
        Ordinary input:
        Standard sentence "Convert your Text into Voice".
        Preconditions: text-to-speech.py lines 36-40.
        """
        input_text = "Convert your Text into Voice"
        result = tts_module.Text_to_speech(
            message=input_text,
            gtts_cls=self.mock_gtts,
            player_fn=self.mock_player,
            cleaner_fn=self.mock_cleaner
        )

        self.mock_gtts.assert_called_once_with(text=input_text)
        self.assertEqual(result["text_length"], len(input_text))
        self.assertEqual(result["char_operations"], len(input_text))
        self.assertEqual(result["word_count"], 5)

    def test_linear_scaling_measurement(self):
        """
        Measures work scaling across multiple input sizes (10, 100, 1000 chars)
        verifying operations scale linearly with text length O(N) isolated from external I/O.
        """
        sizes = [10, 100, 500, 1000]
        for s in sizes:
            text = "x" * s
            res = tts_module.Text_to_speech(
                message=text,
                gtts_cls=self.mock_gtts,
                player_fn=self.mock_player,
                cleaner_fn=self.mock_cleaner
            )
            self.assertEqual(res["char_operations"], s)


if __name__ == "__main__":
    unittest.main()
