## Summary

Add an executable `NeuralNetwork` example to the FlappyBird README. It traces a four-feature state through the defined hidden widths `[512, 256, 64]` to a two-action output shape `(1, 2)`, while explaining that numeric scores depend on model weights.

## Verification

- `python3 work/R29-T047/check.py` — 2 tests passed on Python 3.9.6.
- The runner executes the marked README code block with external ML and game dependencies mocked, checks its displayed output, and verifies one-feature and four-feature shapes.
- Fixture and source anchors are in [`README.md`](work/R29-T047/README.md).
