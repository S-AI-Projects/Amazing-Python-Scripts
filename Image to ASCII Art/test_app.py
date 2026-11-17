import os
import sys
import unittest
from unittest.mock import MagicMock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import app


class MockImage:
    """Mock Image providing isolated repeatable behavior for unit testing without external PIL dependencies."""

    def __init__(self, size):
        self.size = size
        self.resized_size = None

    def resize(self, new_dimensions):
        new_img = MockImage(new_dimensions)
        new_img.resized_size = new_dimensions
        return new_img


class TestResizeImageRepeatable(unittest.TestCase):
    """
    Focused repeatable verification of resize_image in Image to ASCII Art/app.py.
    Preconditions cited:
      - Line 24: width, height = image.size.
      - Line 25: ratio = height / width.
      - Line 26: new_height = int(new_width * ratio).
      - Line 27: resized_image = image.resize((new_width, new_height)).
    """

    def test_smallest_valid_input(self):
        """
        Smallest valid input:
        1x1 pixel image with new_width=1.
        Preconditions: app.py lines 24, 25, 26, 27.
        """
        img = MockImage((1, 1))
        new_width = 1
        expected_size = (1, 1)

        result = app.resize_image(img, new_width=new_width)

        self.assertEqual(result.size, expected_size)
        self.assertEqual(img.size, (1, 1))  # Preserves input isolation / non-mutation

    def test_ordinary_input(self):
        """
        Ordinary input:
        800x600 image with default new_width=100.
        Aspect ratio: 600 / 800 = 0.75.
        Expected new height: int(100 * 0.75) = 75.
        Preconditions: app.py lines 24, 25, 26, 27.
        """
        img = MockImage((800, 600))
        expected_size = (100, 75)

        result = app.resize_image(img, new_width=100)

        self.assertEqual(result.size, expected_size)
        self.assertEqual(img.size, (800, 600))  # Input preserved

    def test_repeatable_idempotency_and_isolation(self):
        """
        Repeated calls with controlled input return identical deterministic results
        without leaking or mutating state across repeated invocations.
        """
        img = MockImage((400, 200))
        res1 = app.resize_image(img, 50)
        res2 = app.resize_image(img, 50)
        res3 = app.resize_image(img, 50)

        self.assertEqual(res1.size, (50, 25))
        self.assertEqual(res2.size, (50, 25))
        self.assertEqual(res3.size, (50, 25))
        self.assertEqual(img.size, (400, 200))


if __name__ == "__main__":
    unittest.main()
