"""
Focused runnable example checks for resize_image in Image Manipulation Script
"""
import sys
import io
import contextlib
import tempfile
import unittest
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Image Manipulation Script" / "image_manipulation.py"

import importlib.util
spec = importlib.util.spec_from_file_location("img_manip", str(SOURCE_PATH))
img_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(img_mod)


class ResizeImageExampleTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)
        # Create a fresh sample source image (100x100)
        self.input_file = self.dir_path / "test_input.png"
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(self.input_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_smallest_valid_input(self):
        # Preconditions established at source lines 16 to 18:
        # image.resize(new_size) where smallest valid size is (1, 1)
        output_file = self.dir_path / "smallest_out.png"
        new_size = (1, 1)

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            img_mod.resize_image(str(self.input_file), str(output_file), new_size)
            output = buf.getvalue().strip()

        expected_msg = "Image resized and saved successfully."
        self.assertEqual(output, expected_msg)

        # Verify intermediate to saved state transition
        with Image.open(output_file) as saved:
            self.assertEqual(saved.size, (1, 1))

    def test_ordinary_input(self):
        # Precondition established at source line 43:
        # new_size = (800, 600)
        output_file = self.dir_path / "ordinary_out.png"
        new_size = (800, 600)

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            img_mod.resize_image(str(self.input_file), str(output_file), new_size)
            output = buf.getvalue().strip()

        expected_msg = "Image resized and saved successfully."
        self.assertEqual(output, expected_msg)

        with Image.open(output_file) as saved:
            self.assertEqual(saved.size, (800, 600))

    def test_docstring_example_execution(self):
        # Executes the example from the docstring
        output_file = self.dir_path / "example_out.png"
        new_size = (800, 600)

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            img_mod.resize_image(str(self.input_file), str(output_file), new_size)
            output = buf.getvalue().strip()

        self.assertEqual(output, "Image resized and saved successfully.")
        self.assertTrue(output_file.exists())


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ResizeImageExampleTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T017/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
