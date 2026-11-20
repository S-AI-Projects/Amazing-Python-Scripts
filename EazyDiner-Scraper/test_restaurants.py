import unittest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from restaurants import EazyDiner
from bs4 import BeautifulSoup


def generate_restaurant_html(n):
    """
    Generates synthetic HTML containing N .restaurant elements.
    """
    cards = []
    for i in range(1, n + 1):
        card = f"""
        <div class="restaurant">
            <h3 class="res_name">Bistro {i}</h3>
            <h3 class="res_loc">Sector {i}</h3>
            <span class="critic">4.{i % 9}</span>
            <div class="res_cuisine">Italian,Cafe</div>
            <span class="cost_for_two">{500 + i * 50}</span>
        </div>
        """
        cards.append(card)
    return "<html><body>" + "\n".join(cards) + "</body></html>"


class TestEazyDinerComplexity(unittest.TestCase):
    """
    Complexity experiment and unit tests for EazyDiner in restaurants.py.
    Anchor cited:
      - Line 46: restaurant_data = {"restaurants": []}
    """

    def setUp(self):
        self.scraper = EazyDiner("Delhi NCR")

    def test_smallest_valid_input(self):
        """
        Smallest valid input: N = 1 restaurant card.
        Precondition: Line 46 (restaurant_data = {"restaurants": []}).
        """
        html = generate_restaurant_html(1)
        res_json = self.scraper.getRestaurants(html_source=html)
        data = json.loads(res_json)

        self.assertEqual(len(data["restaurants"]), 1)
        expected_first = {
            "restaurant": "Bistro 1",
            "location": "Sector 1",
            "rating": "4.1",
            "cuisine": "Italian, Cafe",
            "price": "Rs. 550 for two"
        }
        self.assertEqual(data["restaurants"][0], expected_first)

    def test_ordinary_input(self):
        """
        Ordinary input: N = 5 restaurant cards.
        """
        html = generate_restaurant_html(5)
        res_json = self.scraper.getRestaurants(html_source=html)
        data = json.loads(res_json)

        self.assertEqual(len(data["restaurants"]), 5)
        self.assertEqual(data["restaurants"][4]["restaurant"], "Bistro 5")

    def test_complexity_linear_scaling_three_sizes(self):
        """
        Measures scaling of operations across 3 distinct sizes: N = 1, N = 5, N = 20.
        Complexity claim: O(N) where work = 5 * N operations.
        Ensures work / N is constant (5.0) and all sizes produce correct outputs.
        """
        sizes = [1, 5, 20]
        results = []

        for n in sizes:
            html = generate_restaurant_html(n)
            soup = BeautifulSoup(html, "html.parser")
            data, ops = self.scraper.parse_restaurants(soup)

            # Correctness assertion
            self.assertEqual(len(data["restaurants"]), n)

            # Operations work assertion: exactly 5 extraction operations per restaurant card
            self.assertEqual(ops, 5 * n)
            ratio = ops / float(n)
            self.assertEqual(ratio, 5.0)

            results.append({
                "N": n,
                "operations": ops,
                "work_per_item": ratio
            })

        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
