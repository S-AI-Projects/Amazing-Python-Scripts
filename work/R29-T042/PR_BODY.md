## Summary

Document the scraper's supported card boundaries and empty-result behavior. Add focused checks for an empty page result, a minimal standard card with optional fields missing, and the luxury selector fallbacks.

The request, parser results, and CSV writer are stubbed. The boundary notes cite the exact source selectors and defaults, and leave behavior unspecified when required markup or network access is missing.

## Verification

- `python3 work/R29-T042/check.py` — 3 tests passed on Python 3.9.6.
- Expected rows, optional-field defaults, and source references are in [`README.md`](work/R29-T042/README.md).
