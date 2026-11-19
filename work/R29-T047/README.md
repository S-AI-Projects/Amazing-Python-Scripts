# R29-T047: `NeuralNetwork` worked example

The example in `FlappyBird/README.md` uses the real public function from `Flappy.py:20`. The source defines an input shape, then Dense widths 512, 256, and 64, then the requested output width at lines 22–32. With input shape `(4,)` and output size `2`, a single state has shape `(1, 4)` and the model's two action scores have shape `(1, 2)`.

The function constructs and compiles a model; it does not train it. Numeric predictions vary with initialized or trained weights, so the asserted output is the prediction shape. The check executes the exact marked README block with Keras and Gym imports mocked; the fake prediction is only used to verify the returned shape and is not presented as a real Q-value.

Smallest supported shape checked: `(1,)` to one output. Ordinary example checked: `(4,)` to two outputs. Command: `python3 work/R29-T047/check.py` (Python 3.9.6; 2 tests passed).
