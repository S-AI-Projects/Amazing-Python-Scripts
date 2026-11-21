import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))
from exchange_rates import parse_currencies, select_currency, parse_exchange_table


class TestExchangeRatesBoundaries(unittest.TestCase):
    """
    Focused boundary tests for Currency-Exchange-Rates/exchange_rates.py.
    Anchors cited:
      - Line 25: currencies = []
      - Line 33: current_element = {'name': currency_name, 'short': currency_short}
      - Line 42: currency selection boundary 1 <= position <= len(currencies)
    """

    def setUp(self):
        self.sample_html = """
        <html>
            <select>
                <option>USD - US Dollar</option>
                <option>EUR - Euro</option>
                <option>GBP - British Pound</option>
            </select>
        </html>
        """
        self.currencies = [
            {'name': 'US Dollar', 'short': 'USD'},
            {'name': 'Euro', 'short': 'EUR'},
            {'name': 'British Pound', 'short': 'GBP'}
        ]

    def test_smallest_valid_input(self):
        """
        Smallest valid boundary: position = 1 (1-based indexing).
        Precondition: Line 42 (currency = currencies[currency_index]).
        """
        result = select_currency(self.currencies, position=1)
        expected = {'name': 'US Dollar', 'short': 'USD'}
        self.assertEqual(result, expected)

    def test_ordinary_input(self):
        """
        Ordinary input: position = 2.
        Precondition: Line 42 (currency = currencies[currency_index]).
        """
        result = select_currency(self.currencies, position=2)
        expected = {'name': 'Euro', 'short': 'EUR'}
        self.assertEqual(result, expected)

    def test_upper_boundary_input(self):
        """
        Upper valid boundary: position = len(currencies).
        """
        position = len(self.currencies)
        result = select_currency(self.currencies, position=position)
        expected = {'name': 'British Pound', 'short': 'GBP'}
        self.assertEqual(result, expected)

    def test_boundary_below_lower_limit_rejected(self):
        """
        Rejected boundary: position = 0 (below valid 1-based range).
        Must raise IndexError.
        """
        with self.assertRaises(IndexError):
            select_currency(self.currencies, position=0)

    def test_boundary_above_upper_limit_rejected(self):
        """
        Rejected boundary: position = len(currencies) + 1.
        Must raise IndexError.
        """
        with self.assertRaises(IndexError):
            select_currency(self.currencies, position=len(self.currencies) + 1)

    def test_negative_position_rejected(self):
        """
        Rejected boundary: negative position (e.g. -1).
        Must raise IndexError.
        """
        with self.assertRaises(IndexError):
            select_currency(self.currencies, position=-1)

    def test_html_parsing_anchor_current_element(self):
        """
        Tests parsing of options into currencies list.
        Anchor: Line 25 (currencies = []), Line 33 (current_element).
        """
        html = "<select><option>INR - Indian Rupee</option></select>"
        parsed = parse_currencies(html)
        expected = [{'name': 'Indian Rupee', 'short': 'INR'}]
        self.assertEqual(parsed, expected)

    def test_parse_exchange_table(self):
        """
        Tests parsing exchange rate table data.
        """
        table_html = """
        <table class="tablesorter">
            <tr><th>Currency</th><th>Rate</th></tr>
            <tr><td>Euro</td><td>0.85</td></tr>
            <tr><td>British Pound</td><td>0.75</td></tr>
        </table>
        """
        rates = parse_exchange_table(table_html)
        expected = [
            {'currency': 'Euro', 'amount': 0.85},
            {'currency': 'British Pound', 'amount': 0.75}
        ]
        self.assertEqual(rates, expected)


if __name__ == '__main__':
    unittest.main()
