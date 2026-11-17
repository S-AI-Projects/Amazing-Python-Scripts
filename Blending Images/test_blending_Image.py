import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure Blending Images directory is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import blending_Image


class ReferenceOracle:
    """
    Independent reference oracle for image1.
    Given an input shape (H, W, C) and path, computes the expected resized shape,
    dimensions (500, 500, C), and tracks calls without calling blending_Image.image1.
    """

    TARGET_WIDTH = 500
    TARGET_HEIGHT = 500

    @classmethod
    def compute_expected(cls, filepath, raw_shape=(100, 100, 3)):
        channels = raw_shape[2] if len(raw_shape) > 2 else 1
        expected_shape = (cls.TARGET_HEIGHT, cls.TARGET_WIDTH, channels)
        return {
            "source_path": filepath,
            "expected_shape": expected_shape,
            "target_dimensions": (cls.TARGET_WIDTH, cls.TARGET_HEIGHT)
        }


class TestImage1ReferenceComparison(unittest.TestCase):
    """
    Regression tests comparing image1 against an independent reference oracle.
    Preconditions cited:
      - Line 25: filepath acquisition.
      - Line 28: image reading via cv2.imread.
      - Line 29: image resizing to (500, 500) via cv2.resize.
    """

    def setUp(self):
        # Reset module state
        blending_Image.img1 = None

    def test_smallest_valid_input(self):
        """
        Smallest valid input:
        1x1 pixel image file path.
        Precondition lines: blending_Image.py lines 25, 28, 29.
        """
        smallest_input_path = "test_data/smallest_1x1.png"
        raw_shape = (1, 1, 3)

        oracle_result = ReferenceOracle.compute_expected(smallest_input_path, raw_shape)

        mock_cv2 = MagicMock()
        mock_raw_img = MagicMock()
        mock_raw_img.shape = raw_shape
        mock_resized_img = MagicMock()
        mock_resized_img.shape = oracle_result["expected_shape"]

        mock_cv2.imread.return_value = mock_raw_img
        mock_cv2.resize.return_value = mock_resized_img

        with patch.object(blending_Image, "cv2", mock_cv2):
            result = blending_Image.image1(filepath=smallest_input_path)

            mock_cv2.imread.assert_called_once_with(smallest_input_path)
            mock_cv2.resize.assert_called_once_with(mock_raw_img, oracle_result["target_dimensions"])

            self.assertEqual(result.shape, oracle_result["expected_shape"])
            self.assertEqual(blending_Image.img1.shape, oracle_result["expected_shape"])

    def test_ordinary_input(self):
        """
        Ordinary input:
        Standard photo file 'lake.jpg' (or 800x600 ordinary image).
        Precondition lines: blending_Image.py lines 25, 28, 29.
        """
        ordinary_input_path = "lake.jpg"
        raw_shape = (600, 800, 3)

        oracle_result = ReferenceOracle.compute_expected(ordinary_input_path, raw_shape)

        mock_cv2 = MagicMock()
        mock_raw_img = MagicMock()
        mock_raw_img.shape = raw_shape
        mock_resized_img = MagicMock()
        mock_resized_img.shape = oracle_result["expected_shape"]

        mock_cv2.imread.return_value = mock_raw_img
        mock_cv2.resize.return_value = mock_resized_img

        with patch.object(blending_Image, "cv2", mock_cv2):
            result = blending_Image.image1(filepath=ordinary_input_path)

            mock_cv2.imread.assert_called_once_with(ordinary_input_path)
            mock_cv2.resize.assert_called_once_with(mock_raw_img, oracle_result["target_dimensions"])

            self.assertEqual(result.shape, oracle_result["expected_shape"])
            self.assertEqual(blending_Image.img1.shape, oracle_result["expected_shape"])

    def test_twenty_domain_inputs_against_oracle(self):
        """
        Enumerates at least 20 small valid inputs across the domain and compares with oracle.
        Precondition lines: blending_Image.py lines 25, 28, 29.
        """
        domain_inputs = [
            (f"sample_images/img_{idx}.jpg", (10 * (idx + 1), 10 * (idx + 1), 3))
            for idx in range(25)
        ]

        self.assertGreaterEqual(len(domain_inputs), 20)

        for path, raw_shape in domain_inputs:
            expected = ReferenceOracle.compute_expected(path, raw_shape)

            mock_cv2 = MagicMock()
            mock_raw_img = MagicMock()
            mock_raw_img.shape = raw_shape
            mock_resized_img = MagicMock()
            mock_resized_img.shape = expected["expected_shape"]

            mock_cv2.imread.return_value = mock_raw_img
            mock_cv2.resize.return_value = mock_resized_img

            with patch.object(blending_Image, "cv2", mock_cv2):
                actual = blending_Image.image1(filepath=path)
                self.assertEqual(actual.shape, expected["expected_shape"])
                self.assertEqual(blending_Image.img1.shape, expected["expected_shape"])


if __name__ == "__main__":
    unittest.main()
