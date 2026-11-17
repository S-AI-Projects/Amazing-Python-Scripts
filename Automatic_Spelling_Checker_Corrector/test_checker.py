import os
import sys
import unittest
import tempfile

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import automatic_spelling_checker_corrector as checker


class TestReadTextFileMutation(unittest.TestCase):
    """
    Focused regression test proving detection of a plausible one-line mutant in readTextFile.
    Plausible mutant:
      `words = [word for word in tokens if word.isalnum()]` (allows numbers/digits into words list)
      instead of `word.isalpha()`.
    Preconditions cited:
      - Line 35: tokens = word_tokenize(inputFile.read()).
      - Line 38: words = [word for word in tokens if word.isalpha()].
    """

    def setUp(self):
        checker.tokens = []

    def test_smallest_valid_input(self):
        """
        Smallest valid input:
        File with single alphabetic word "hello".
        Preconditions: lines 35, 38.
        """
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write("hello")
            f_path = f.name

        try:
            words = checker.readTextFile(f_path)
            self.assertEqual(words, ["hello"])
            self.assertEqual(checker.tokens, ["hello"])
        finally:
            os.remove(f_path)

    def test_ordinary_input_with_punctuation_and_numbers(self):
        """
        Ordinary input:
        Sentence with words, numbers, and punctuation: "Hello world 123 ! Python 2026".
        Expected output strictly filters non-alpha: ['Hello', 'world', 'Python'].
        Preconditions: lines 35, 38.
        """
        content = "Hello world 123 ! Python 2026"
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write(content)
            f_path = f.name

        try:
            expected_words = ["Hello", "world", "Python"]
            actual_words = checker.readTextFile(f_path)
            self.assertEqual(actual_words, expected_words)
        finally:
            os.remove(f_path)

    def test_mutant_fails_assertion(self):
        """
        Simulates the plausible mutant `word.isalnum()` on the test input
        and proves that the mutant fails the regression assertion for semantic reasons.
        """
        content = "Test 999 word"
        tokens = checker.word_tokenize(content)

        # Original implementation
        original_words = [w for w in tokens if w.isalpha()]
        self.assertEqual(original_words, ["Test", "word"])

        # Mutant implementation (plausible mistake: isalnum() instead of isalpha())
        mutant_words = [w for w in tokens if w.isalnum()]

        # The test fails when run against mutant because '999' is included
        self.assertNotEqual(mutant_words, original_words)
        self.assertIn("999", mutant_words)


if __name__ == "__main__":
    unittest.main()
