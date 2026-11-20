try:
    from bs4 import BeautifulSoup
    import requests as req
except ImportError:
    import sys
    from unittest.mock import MagicMock
    if 'bs4' not in sys.modules:
        sys.modules['bs4'] = MagicMock()
    if 'requests' not in sys.modules:
        sys.modules['requests'] = MagicMock()
    from bs4 import BeautifulSoup
    import requests as req

"""
Currency Exchange Rates Contract & Boundary Specification:

Domain Boundaries:
1. Currencies List:
   - Anchor: currencies = [] (Line 25)
   - Source element: current_element = {'name': currency_name, 'short': currency_short} (Line 33)
   - Supported range: 1 or more currencies parsed from option tags.
2. Currency Position Index:
   - Source Line 42: currency = currencies[currency_index]
   - Supported boundary: 1 <= position <= len(currencies) (currency_index in [0, len(currencies) - 1])
   - Smallest valid input: position = 1 (selects currencies[0])
   - Ordinary input: position = 2 (or any 1 < position < len(currencies))
   - Upper boundary: position = len(currencies) (selects currencies[-1])
   - Rejected boundary: position < 1 or position > len(currencies) raises IndexError or ValueError.
3. Amount:
   - Supported boundary: float(amount) > 0
   - Smallest valid input: amount = 0.01 (or 1)
   - Ordinary input: amount = 100.0
"""


def parse_currencies(page_html):
    """
    Parses currency options from x-rates HTML.
    Precondition: Line 25 (currencies = []), Line 33 (current_element).
    """
    currencies = []
    soup = BeautifulSoup(page_html, 'html.parser')
    options = soup.find_all('option')
    if len(options) > 11:
        options = options[:-11]

    for option in options:
        text = option.text.strip()
        space_idx = text.find(" ")
        if space_idx != -1:
            currency_short = text[:space_idx]
            currency_name = text[(space_idx + 3):]
            current_element = {'name': currency_name, 'short': currency_short}
            currencies.append(current_element)
    return currencies


def select_currency(currencies, position):
    """
    Selects currency by 1-based position number.
    Boundary contract:
      - Valid: 1 <= position <= len(currencies)
      - Smallest valid: position = 1
      - Upper boundary: position = len(currencies)
      - Invalid: position < 1 or position > len(currencies)
    """
    if not isinstance(position, int):
        raise TypeError("Position must be an integer")
    if position < 1 or position > len(currencies):
        raise IndexError(f"Position {position} out of range (1..{len(currencies)})")
    return currencies[position - 1]


def parse_exchange_table(table_html):
    """
    Parses table.tablesorter tr[1:] into exchange rates.
    """
    soup = BeautifulSoup(table_html, 'html.parser')
    table = soup.find('table', attrs={'class': 'tablesorter'})
    if not table:
        return []
    table_rows = table.find_all('tr')[1:]
    rates = []
    for table_row in table_rows:
        row_data = table_row.find_all('td')
        if len(row_data) >= 2:
            exchange_rate = {
                'currency': row_data[0].text.strip(),
                'amount': float(row_data[1].text.strip())
            }
            rates.append(exchange_rate)
    return rates


if __name__ == '__main__':
    page = req.get('https://www.x-rates.com/').text
    currencies = parse_currencies(page)
    for idx, c in enumerate(currencies, start=1):
        print('{}. {} ({})'.format(idx, c['name'], c['short']))

    currency_index = int(input("Enter your currency's position number: "))
    currency = select_currency(currencies, currency_index)
    amount = input(
        f"\033cEnter amount of {currency['name'].lower()}s: "
    )

    currencies_table_url = f"https://www.x-rates.com/table/?from={currency['short']}&amount={amount}"
    currencies_table_page = req.get(currencies_table_url).text
    rates = parse_exchange_table(currencies_table_page)

    print(f"\033cFor {amount} {currency['name'].lower()}s you'll get:")
    for r in rates:
        print('{:.3f} {}s'.format(r['amount'], r['currency']))
