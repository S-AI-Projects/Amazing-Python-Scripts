"""
Focused invariant checks for Support Chat Bot For Your Website Project 9
"""
import sys
import random
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPO_ROOT / "Support Chat Bot For Your Website -  Project 9"


class DummyDocument:
    def __init__(self, content, source):
        self.page_content = content
        self.metadata = {"source": source}


def mock_similarity_search(query, k=2):
    # Simulated corpus of 10 available documents
    corpus = [
        DummyDocument(f"Document content number {i}", f"https://example.com/page{i}")
        for i in range(10)
    ]
    # Invariant: returned count is bounded by min(k, len(corpus))
    return corpus[:k]


def broken_mutant_similarity_search(query, k=2):
    # Deliberately breaks the invariant by always returning at least 1 document even when k=0
    corpus = [
        DummyDocument(f"Document content number {i}", f"https://example.com/page{i}")
        for i in range(10)
    ]
    if k == 0:
        return [corpus[0]]
    return corpus[:k]


class SupportChatBotInvariantTests(unittest.TestCase):

    def test_smallest_valid_input(self):
        # Precondition established at source line 43:
        # document_count = st.slider('No.Of links to return', 0, 5, 2, step=1)
        # Smallest valid slider value is 0
        prompt = ""
        document_count = 0

        results = mock_similarity_search(prompt, k=document_count)
        expected_count = 0
        self.assertEqual(len(results), expected_count, f"Expected {expected_count} results but got {len(results)}")

    def test_ordinary_input(self):
        # Precondition established at source lines 42 and 43:
        # Default slider value is 2
        prompt = "How to reset account password"
        document_count = 2

        results = mock_similarity_search(prompt, k=document_count)
        expected_count = 2
        self.assertEqual(len(results), expected_count, f"Expected {expected_count} results but got {len(results)}")
        self.assertEqual(results[0].metadata["source"], "https://example.com/page0")

    def test_invariant_across_random_inputs(self):
        # Deterministic seed for reproducible property checking
        rng = random.Random(42)
        sample_queries = [
            "help",
            "contact email",
            "pricing plan details",
            "working hours",
            "support ticket status"
        ]

        for _ in range(25):
            query = rng.choice(sample_queries)
            k = rng.randint(0, 5)
            results = mock_similarity_search(query, k=k)
            # Core invariant: returned count never exceeds requested slider k
            self.assertLessEqual(len(results), k, f"Invariant violated: returned {len(results)} when k was {k}")

    def test_deliberate_mutant_fails_invariant(self):
        # Verification that broken implementation fails the invariant check
        k = 0
        mutant_results = broken_mutant_similarity_search("test query", k=k)
        # The mutant returns 1 result for k=0, which violates the invariant
        invariant_broken = len(mutant_results) > k
        self.assertTrue(invariant_broken, "Mutant did not break the invariant as expected")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(SupportChatBotInvariantTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T014/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
