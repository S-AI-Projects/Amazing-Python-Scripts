"""
Focused regression and refactoring checks for find_lyrics in Lyrics_Finder
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Lyrics_Finder" / "script.py"

# Mock requests before importing source
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

import importlib.util
spec = importlib.util.spec_from_file_location("lyrics_script", str(SOURCE_PATH))
lyrics_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lyrics_mod)


class LyricsFinderTests(unittest.TestCase):

    def setUp(self):
        mock_requests.reset_mock()

    def test_smallest_valid_input(self):
        # Preconditions established at source lines 4 to 12:
        # build_lyrics_url formats URL: https://api.lyrics.ovh/v1/{}/{}
        artist = "a"
        title = "b"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"lyrics": "la"}
        mock_requests.get.return_value = mock_resp

        result = lyrics_mod.find_lyrics(artist, title)

        expected_url = "https://api.lyrics.ovh/v1/a/b"
        mock_requests.get.assert_called_once_with(expected_url)
        self.assertEqual(result, "la")

    def test_ordinary_input(self):
        # Preconditions established at source lines 4 to 16
        artist = "Coldplay"
        title = "Yellow"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"lyrics": "Look at the stars"}
        mock_requests.get.return_value = mock_resp

        result = lyrics_mod.find_lyrics(artist, title)

        expected_url = "https://api.lyrics.ovh/v1/Coldplay/Yellow"
        mock_requests.get.assert_called_once_with(expected_url)
        self.assertEqual(result, "Look at the stars")

    def test_error_status_response(self):
        # Status code 404 error path at line 17
        artist = "Unknown"
        title = "Unknown"

        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_requests.get.return_value = mock_resp

        result = lyrics_mod.find_lyrics(artist, title)

        expected_error = "Error fetching lyrics. Please check the artist and title and try again."
        self.assertEqual(result, expected_error)

    def test_missing_lyrics_key(self):
        # Status code 200 with missing lyrics key at line 14
        artist = "Instrumental"
        title = "Song"

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        mock_requests.get.return_value = mock_resp

        result = lyrics_mod.find_lyrics(artist, title)

        expected_msg = "Lyrics not found for this song."
        self.assertEqual(result, expected_msg)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LyricsFinderTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T016/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
