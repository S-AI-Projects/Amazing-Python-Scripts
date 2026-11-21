import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from Scrap import parse_flipkart_html, scrape_flipkart


class TestFlipkartRepeatableVerification(unittest.TestCase):
    """
    Repeatable verification tests for Flipkart webscraping.
    Preconditions cited:
      - Line 31: Product_name = []
      - Line 32: Prices = []
      - Line 33: Description = []
      - Line 34: Reviews = []
    """

    def setUp(self):
        # Smallest valid input fixture (1 product)
        self.smallest_html = """
        <div class="_1YokD2 _3Mn1Gg">
            <div class="_4rR01T">BrandX Phone 64GB</div>
            <div class="_30jeq3 _1_WHN1">₹12,499</div>
            <ul class="_1xgFaf">4 GB RAM | 64 GB ROM</ul>
            <div class="_3LWZlK">4.1</div>
        </div>
        """

        # Ordinary input fixture (2 products)
        self.ordinary_html = """
        <div class="_1YokD2 _3Mn1Gg">
            <div class="_4rR01T">Phone Alpha 128GB</div>
            <div class="_30jeq3 _1_WHN1">₹24,999</div>
            <ul class="_1xgFaf">6 GB RAM | 128 GB ROM</ul>
            <div class="_3LWZlK">4.5</div>

            <div class="_4rR01T">Phone Beta 256GB</div>
            <div class="_30jeq3 _1_WHN1">₹39,999</div>
            <ul class="_1xgFaf">8 GB RAM | 256 GB ROM</ul>
            <div class="_3LWZlK">4.7</div>
        </div>
        """

    def test_smallest_valid_input(self):
        """
        Smallest valid input: Single product parsing.
        Preconditions: Lines 31-34 (Product_name = [], Prices = [], Description = [], Reviews = []).
        """
        result = parse_flipkart_html(self.smallest_html)
        expected = {
            "Product Name": ["BrandX Phone 64GB"],
            "Prices": ["₹12,499"],
            "Description": ["4 GB RAM | 64 GB ROM"],
            "Reviews": ["4.1"]
        }
        self.assertEqual(result, expected)

    def test_ordinary_input(self):
        """
        Ordinary input: Multi-product catalog page parsing.
        """
        result = parse_flipkart_html(self.ordinary_html)
        expected = {
            "Product Name": ["Phone Alpha 128GB", "Phone Beta 256GB"],
            "Prices": ["₹24,999", "₹39,999"],
            "Description": ["6 GB RAM | 128 GB ROM", "8 GB RAM | 256 GB ROM"],
            "Reviews": ["4.5", "4.7"]
        }
        self.assertEqual(result, expected)

    def test_repeatable_consecutive_runs_deterministic(self):
        """
        Verification of reproducibility:
        Two consecutive runs with identical inputs produce identical outputs.
        """
        run_1 = parse_flipkart_html(self.ordinary_html)
        run_2 = parse_flipkart_html(self.ordinary_html)
        self.assertEqual(run_1, run_2)
        self.assertIsNot(run_1, run_2)

    def test_mocked_scrape_no_network(self):
        """
        Verifies scrape_flipkart works with zero live network calls.
        """
        mock_response = MagicMock()
        mock_response.text = self.ordinary_html
        mock_fetcher = MagicMock(return_value=mock_response)

        data = scrape_flipkart(pages=1, fetcher=mock_fetcher, save_csv=False)

        self.assertEqual(mock_fetcher.call_count, 1)
        self.assertEqual(len(data["Product Name"]), 2)
        self.assertEqual(data["Product Name"][0], "Phone Alpha 128GB")
        self.assertEqual(data["Prices"][0], "₹24,999")


if __name__ == '__main__':
    unittest.main()
