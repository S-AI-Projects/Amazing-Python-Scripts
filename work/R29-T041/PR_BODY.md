## Summary

Add focused `gen` regression checks for the smallest positive length, an ordinary length, and the maximum 94-character candidate-set boundary. The runner controls input and uses a deterministic in-place shuffle to make exact output fixtures reproducible.

Each case checks the printed password, `None` return, prompt, initial candidate list, and local shuffle mutation separately. The existing public `gen()` interface and output behavior are unchanged.

## Verification

- `python3 work/R29-T041/check.py` — 3 tests passed on Python 3.9.6.
- Literal fixtures and source line anchors are in [`README.md`](work/R29-T041/README.md).
