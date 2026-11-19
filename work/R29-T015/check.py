"""
Focused repeatable verification checks for convert_audio_to_text in Audio to Text Convertor
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Audio to Text Convertor" / "code.py"

# Mock speech_recognition before loading source
mock_sr = MagicMock()


class MockUnknownValueError(Exception):
    pass


class MockRequestError(Exception):
    pass


mock_sr.UnknownValueError = MockUnknownValueError
mock_sr.RequestError = MockRequestError
sys.modules["speech_recognition"] = mock_sr

import importlib.util
spec = importlib.util.spec_from_file_location("audio_code", str(SOURCE_PATH))
audio_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_mod)


class AudioToTextRepeatabilityTests(unittest.TestCase):

    def setUp(self):
        self.mock_mic = MagicMock()
        self.mock_mic.__enter__.return_value = MagicMock()
        self.mock_mic.__exit__.return_value = None

    def test_smallest_valid_input_repeatability(self):
        # Preconditions established at source lines 4 to 17:
        # Dependency seam allows injecting recognizer and microphone
        mock_r = MagicMock()
        mock_r.listen.return_value = "audio_chunk"
        mock_r.recognize_google.return_value = "hi"

        expected_text = "hi"

        # Verify repeatability by calling multiple times with fresh equivalent inputs
        for i in range(5):
            result = audio_mod.convert_audio_to_text(recognizer=mock_r, microphone=self.mock_mic)
            self.assertEqual(result, expected_text, f"Run {i}: Expected {expected_text} but got {result}")

    def test_ordinary_input_repeatability(self):
        # Ordinary input with multiple words
        mock_r = MagicMock()
        mock_r.listen.return_value = "audio_chunk"
        mock_r.recognize_google.return_value = "python script audio test"

        expected_text = "python script audio test"

        for i in range(5):
            result = audio_mod.convert_audio_to_text(recognizer=mock_r, microphone=self.mock_mic)
            self.assertEqual(result, expected_text, f"Run {i}: Expected {expected_text} but got {result}")

    def test_unknown_value_error_handling(self):
        # Boundary case when audio cannot be transcribed
        mock_r = MagicMock()
        mock_r.listen.return_value = "audio_chunk"
        mock_r.recognize_google.side_effect = MockUnknownValueError("Could not understand")

        result = audio_mod.convert_audio_to_text(recognizer=mock_r, microphone=self.mock_mic)
        self.assertIsNone(result)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AudioToTextRepeatabilityTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T015/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
