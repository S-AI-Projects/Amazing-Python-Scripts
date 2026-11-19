# R29-T041: `gen` contract checks

`gen` is defined at `Password-Generator/passowrd_gen.py:5`. It reads one integer length at line 12, builds a local candidate list from uppercase, lowercase, digits, and punctuation at lines 6–19, shuffles that list at line 21, then prints the requested prefix at lines 22–23. It returns `None`; there is no caller-owned input collection to mutate. The only observable mutation is the local list passed to `random.shuffle`.

## Literal fixtures

The checker replaces shuffle with a deterministic in-place reversal and controls `input()`:

- Smallest positive length: input `"1"`, expected printed password `~`.
- Ordinary length: input `"12"`, expected printed password `~}|{`_^]\\[@?`.
- Full candidate boundary: input `"94"`, expected output is the full reversed candidate alphabet, recorded literally as `EXPECTED_MAX` in `check.py`; all 94 characters appear exactly once.

Each case separately asserts the `None` return, exact printed output, prompt, pre-shuffle list, and mutation of that local list. Command: `python3 work/R29-T041/check.py` (Python 3.9.6; 3 tests passed).
