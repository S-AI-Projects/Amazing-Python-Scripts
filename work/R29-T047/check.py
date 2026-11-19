"""Run the NeuralNetwork documentation example with mocked Keras builders."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import platform
import re
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "FlappyBird" / "Flappy.py"
README = REPO / "FlappyBird" / "README.md"


class FakeLayer:
    def __init__(self, units=None, **kwargs):
        self.units = units
        self.kwargs = kwargs


class FakeSequential:
    def __init__(self):
        self.layers = []
        self.compile_args = None

    def add(self, layer):
        self.layers.append(layer)

    def compile(self, **kwargs):
        self.compile_args = kwargs
        self.loss = kwargs["loss"]

    def summary(self):
        pass

    def predict(self, state, verbose=0):
        return [[0.0] * self.layers[-1].units for _ in state]

    @property
    def output_shape(self):
        return (None, self.layers[-1].units)


def load_module():
    numpy = types.ModuleType("numpy")
    flappy_bird_gym = types.ModuleType("flappy_bird_gym")
    layers = types.ModuleType("tensorflow.keras.layers")
    layers.Input = lambda shape: FakeLayer(input_shape=shape)
    layers.Dense = lambda units, **kwargs: FakeLayer(units=units, **kwargs)
    models = types.ModuleType("tensorflow.keras.models")
    models.Sequential = FakeSequential
    models.load_model = lambda *args, **kwargs: None
    models.save_model = lambda *args, **kwargs: None
    optimizers = types.ModuleType("tensorflow.keras.optimizers")
    optimizers.RMSprop = lambda **kwargs: {"type": "RMSprop", **kwargs}
    keras = types.ModuleType("tensorflow.keras")
    tensorflow = types.ModuleType("tensorflow")
    modules = {
        "numpy": numpy,
        "flappy_bird_gym": flappy_bird_gym,
        "tensorflow": tensorflow,
        "tensorflow.keras": keras,
        "tensorflow.keras.layers": layers,
        "tensorflow.keras.models": models,
        "tensorflow.keras.optimizers": optimizers,
    }
    with patch.dict(sys.modules, modules):
        spec = importlib.util.spec_from_file_location("flappy_under_test", SOURCE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class NeuralNetworkExampleTests(unittest.TestCase):
    def test_documented_example_executes_and_shows_expected_shapes(self):
        # Public preconditions are established by Flappy.py:20 (shape args);
        # lines 23-28 define intermediate dense widths and output width.
        text = README.read_text(encoding="utf-8")
        match = re.search(r"<!-- runnable example -->\n```python\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(match, "expected a marked runnable Python example in README.md")
        module = load_module()
        import_shim = types.ModuleType("Flappy")
        import_shim.NeuralNetwork = module.NeuralNetwork
        output = io.StringIO()
        with patch.dict(sys.modules, {"Flappy": import_shim}), \
             contextlib.redirect_stdout(output):
            exec(compile(match.group(1), "README.md example", "exec"),
                 {"NeuralNetwork": module.NeuralNetwork})
        expected = (
            "state: [[0.25, 0.75, 0.5, 0.0]]\n"
            "dense widths: [512, 256, 64, 2]\n"
            "model output shape: (None, 2)\n"
            "Q-value shape: (1, 2)\n"
            "loss: mse\n"
        )
        self.assertEqual(output.getvalue(), expected,
                         f"expected example output {expected!r}; actual {output.getvalue()!r}")

    def test_smallest_shape_and_ordinary_shape_build_expected_architecture(self):
        module = load_module()
        for input_shape, output_size, expected_shape in [((1,), 1, (None, 1)),
                                                         ((4,), 2, (None, 2))]:
            model = module.NeuralNetwork(input_shape, output_size)
            widths = [layer.units for layer in model.layers if layer.units is not None]
            expected_widths = [512, 256, 64, output_size]
            self.assertEqual(widths, expected_widths,
                             f"expected dense widths {expected_widths!r}; actual {widths!r}")
            self.assertEqual(model.output_shape, expected_shape,
                             f"expected output shape {expected_shape!r}; actual {model.output_shape!r}")
            self.assertEqual(model.compile_args["loss"], "mse",
                             f"expected loss 'mse'; actual {model.compile_args['loss']!r}")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NeuralNetworkExampleTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Python: {platform.python_version()} ({sys.version.splitlines()[0]})")
    print("Command: python3 work/R29-T047/check.py")
    print(f"Nonzero tests: {result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
