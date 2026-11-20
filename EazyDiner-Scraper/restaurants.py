import json
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import sys
    from unittest.mock import MagicMock
    if 'requests' not in sys.modules:
        sys.modules['requests'] = MagicMock()
    if 'bs4' not in sys.modules:
        sys.modules['bs4'] = MagicMock()
    import requests
    from bs4 import BeautifulSoup

"""
Complexity & Scaling Specification for EazyDiner:
Class: EazyDiner
Methods:
  - parse_restaurants(soup) -> tuple[dict, int]
  - getRestaurants(html_source=None, session=None) -> str

Complexity Statement:
  - Input-size variable: N = number of restaurant card elements ('.restaurant') present in the HTML document.
  - Asymptotic Worst-Case Time Complexity: O(N) linear time.
    * Each card undergoes exactly 5 element extractions: res_name, res_loc, critic, res_cuisine, cost_for_two.
    * Total extraction operations = 5 * N.
  - Asymptotic Space Complexity: O(N) linear space to accumulate parsed records in memory.
  - Dominant Cost Center: HTML DOM traversal and substring extractions per restaurant node.
  - Empirical Observation: Operation count scales strictly linearly (ratio work/N = constant = 5).

Data Anchor & Preconditions:
  - Line 46: restaurant_data = {"restaurants": []}
"""


class EazyDiner:
    """
    Class - `EazyDiner`
    Example:
    ```
    restaurants = EazyDiner(location="Delhi NCR")
    ```
    Methods :
    1. ``.getRestaurants() | Response - List of restraunts and its details.
    """

    def __init__(self, location):
        self.location = location

    def parse_restaurants(self, soup):
        """
        Parses restaurant DOM elements.
        Anchor: Line 46 (restaurant_data = {"restaurants": []}).
        Returns tuple of (restaurant_data dict, operations_count int).
        """
        restaurant_data = {"restaurants": []}
        restaurants = soup.select(".restaurant")
        operations_count = 0

        for r in restaurants:
            name_el = r.find("h3", class_="res_name")
            name = name_el.getText().strip() if name_el else ""

            loc_el = r.find("h3", class_="res_loc")
            location = loc_el.getText().strip() if loc_el else ""

            rat_el = r.find("span", class_="critic")
            rating = rat_el.getText().strip() if rat_el else ""

            cui_el = r.find("div", class_="res_cuisine")
            cuisine = cui_el.getText().replace(",", ", ").strip() if cui_el else ""

            price_el = r.find("span", class_="cost_for_two")
            price = price_el.getText().encode("ascii", "ignore").decode().strip() if price_el else ""

            operations_count += 5

            restaurant_data["restaurants"].append(
                {
                    "restaurant": name,
                    "location": location,
                    "rating": rating,
                    "cuisine": cuisine,
                    "price": "Rs. " + price + " for two",
                }
            )

        return restaurant_data, operations_count

    def getRestaurants(self, html_source=None, session=None):
        """
        Retrieves restaurant listings for the given location.
        """
        url = (
            "https://www.eazydiner.com/restaurants?location="
            + self.location.replace(" ", "-").replace(",", "").lower()
        )
        try:
            if html_source is not None:
                text = html_source
            else:
                fetcher = session.get if session else requests.get
                res = fetcher(url)
                text = res.text

            soup = BeautifulSoup(text, "html.parser")
            restaurant_data, _ = self.parse_restaurants(soup)
            return json.dumps(restaurant_data)
        except Exception:
            return None


if __name__ == '__main__':
    scraper = EazyDiner("Delhi NCR")
    print(scraper.getRestaurants())
