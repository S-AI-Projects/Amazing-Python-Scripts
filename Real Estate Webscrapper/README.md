## Real Estate Webscrapper
- It will take information from the real estate site and store it in the form of csv file making the data more organised and locally accessible.

___

## Requirements
- BeautifulSoup
- Pandas
---
## How To install
> pip install pandas

> pip install beautifulsoup
---
- Now run the real_estate_webscrapper.py file to create the output2.csv file.
- Then output2.csv will be created in the same folder as real_estate_webscrapper.py file and it can be opened using Microsoft Excel.
---
### Step 1
- Load the website https://www.magicbricks.com/ready-to-move-flats-in-new-delhi-pppfs in your code using requests.

### Step 2
- Use inspect in website to know which div contains the information that we need
- Use beautiful soup to load the information in program and store it into a dictionary for each property

### Step 3
- Use pandas to convert the list of dictionaries to csv file

## Supported result boundaries

The scraper requests the configured MagicBricks page with the `User-Agent` in `headers` (source lines 6–11), collects matching property cards (lines 16–21), and writes the resulting rows to CSV (lines 79–80).

| Case | Supported behavior | Source contract |
| --- | --- | --- |
| No matching cards | Empty dataset `[]`, then an empty DataFrame is written | `complete_dataset = []` at line 16; append is inside the card loop at line 76 |
| Standard card | Standard price and carpet-area selectors populate the corresponding fields | Lines 23–27 and 69–71 |
| Luxury card | Luxury price, per-square-foot and carpet-area selectors are fallbacks | Lines 29–33, 41–48, and 72–74 |
| Missing optional size | `Size` is `None` | Lines 50–54 |
| Missing both optional price-per-square-foot selectors | `Pricepersqft` is `None` | Lines 35–48 |

Each card needs a parseable price, title containing a sale marker, and carpet-area text from one of the supported selectors. The source does not define a stable rejection result when these required fields are missing, when the network request fails, or when the page markup changes; those cases are outside the supported contract. The boundary checks mock the request, parser results, and CSV writer, so no live site access or file write occurs.

Run `python3 work/R29-T042/check.py` for empty, minimal-card, and luxury-card checks.
---

## Author
[Himanshi2997](https://github.com/Himanshi2997)
---

## Output
![output2](https://user-images.githubusercontent.com/67272318/118381259-b8b71f80-b606-11eb-983d-5d8094d05f06.PNG)
