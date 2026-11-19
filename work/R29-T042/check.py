"""Boundary checks for the scraper with network/parser/CSV boundaries stubbed."""
from __future__ import annotations

import platform
import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "Real Estate Webscrapper" / "real_estate_webscrapper.py"
EXPECTED_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
}
URL = "https://www.magicbricks.com/ready-to-move-flats-in-new-delhi-pppfs"


class Tag:
    def __init__(self, text):
        self.text = text


class Card:
    def __init__(self, fields):
        self.fields = fields

    def find(self, _tag, attrs):
        return self.fields.get(attrs["class"])


class Soup:
    def __init__(self, _content, _parser, cards):
        self.cards = cards

    def find_all(self, _tag, attrs):
        return self.cards


def run_scraper(cards):
    network_calls = []
    dataframe_calls = []
    csv_calls = []

    class Response:
        content = b"mocked response"

    requests = types.ModuleType("requests")
    requests.get = lambda url, headers: network_calls.append((url, headers)) or Response()
    bs4 = types.ModuleType("bs4")
    bs4.BeautifulSoup = lambda content, parser: Soup(content, parser, cards)

    class FakeDataFrame:
        def __init__(self, data):
            self.data = data
            dataframe_calls.append(data)

        def to_csv(self, path):
            csv_calls.append(path)

    pandas = types.ModuleType("pandas")
    pandas.DataFrame = FakeDataFrame
    modules = {"requests": requests, "bs4": bs4, "pandas": pandas}
    with patch.dict(sys.modules, modules):
        namespace = runpy.run_path(str(SCRIPT), run_name="__main__")
    return namespace["complete_dataset"], network_calls, dataframe_calls, csv_calls


class ScraperBoundaryTests(unittest.TestCase):
    def test_empty_result_is_supported(self):
        # Source anchors: headers are declared at lines 6-8; complete_dataset
        # starts at line 16 and remains empty when find_all returns no cards.
        actual, network, frames, csv = run_scraper([])
        self.assertEqual(actual, [], f"expected empty dataset []; actual {actual!r}")
        self.assertEqual(network, [(URL, EXPECTED_HEADERS)],
                         f"expected one request with declared headers; actual {network!r}")
        self.assertEqual(frames, [[]], f"expected DataFrame input []; actual {frames!r}")
        self.assertEqual(csv, ["./Real Estate Webscrapper/scraped.csv"],
                         f"expected CSV output path; actual {csv!r}")

    def test_smallest_valid_card_defaults_optional_fields(self):
        fields = {
            "m-srp-card__price": Tag("₹ 50,00,000"),
            "m-srp-card__title": Tag("Flat sale in Green Park"),
            "m-srp-card__summary__info": Tag("900 sq ft"),
        }
        expected_record = {
            "Price": "50,00,000",
            "Pricepersqft": None,
            "Size": None,
            "Address": "Green Park ",
            "Carpet Area": "900 sq ft",
        }
        actual, _network, frames, _csv = run_scraper([Card(fields)])
        self.assertEqual(actual, [expected_record],
                         f"expected record {expected_record!r}; actual {actual!r}")
        self.assertEqual(frames, [[expected_record]],
                         f"expected DataFrame rows {[[expected_record]]!r}; actual {frames!r}")

    def test_luxury_fallback_fields_and_size_boundary(self):
        fields = {
            "luxury-srp-card__price": Tag("₹ 1.2 Cr"),
            "luxury-srp-card__sqft": Tag("₹ 12,000 per sqft"),
            "m-srp-card__title__bhk": Tag("2 BHK"),
            "m-srp-card__title": Tag("2 BHK apartment for sale in City"),
            "luxury-srp-card__area__value": Tag("1200 sq ft"),
        }
        expected_record = {
            "Price": "1.2Cr",
            "Pricepersqft": "12,000persqft",
            "Size": "2 BHK",
            "Address": "City ",
            "Carpet Area": "1200 sq ft",
        }
        actual, _network, _frames, _csv = run_scraper([Card(fields)])
        self.assertEqual(actual, [expected_record],
                         f"expected fallback record {expected_record!r}; actual {actual!r}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ScraperBoundaryTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T042/check.py")
    print("External I/O: requests, BeautifulSoup, and pandas boundary stubs")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
