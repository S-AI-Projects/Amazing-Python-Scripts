# R29-T042: scraper supported boundaries

The supported field behavior and unsupported cases are documented in `Real Estate Webscrapper/README.md`, citing the source lines that establish the request headers, empty dataset, selectors, defaults, and CSV write.

## Fixtures and expected rows

- Smallest supported page result: `complete_dataset = []`; expected DataFrame input `[]` and output path `./Real Estate Webscrapper/scraped.csv`.
- Smallest valid card: standard price `₹ 50,00,000`, title `Flat sale in Green Park`, carpet-area text `900 sq ft`, with the optional size and price-per-square-foot selectors absent. Expected row: `{"Price": "50,00,000", "Pricepersqft": None, "Size": None, "Address": "Green Park ", "Carpet Area": "900 sq ft"}`.
- Luxury boundary: luxury price/price-per-square-foot/carpet selectors plus `2 BHK`. Expected row has price `1.2Cr`, price-per-square-foot `12,000persqft`, size `2 BHK`, address `City `, and carpet area `1200 sq ft`.

Requests, parser card results, and DataFrame output are stubbed. Required-field omissions and network/markup failures remain unspecified by the source and are not assigned invented exception rules.

Command: `python3 work/R29-T042/check.py` (Python 3.9.6; 3 tests passed).
