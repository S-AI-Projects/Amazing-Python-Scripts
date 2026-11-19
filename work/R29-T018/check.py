"""
Focused failure behavior checks for Neon Effect Filter
"""
import sys
import io
import contextlib
import unittest
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = REPO_ROOT / "Neon Effect Filter" / "Code.py"

# Mock cv2, numpy, and matplotlib before importing
mock_cv2 = MagicMock()
mock_np = MagicMock()
mock_plt = MagicMock()
sys.modules["cv2"] = mock_cv2
sys.modules["numpy"] = mock_np
sys.modules["matplotlib"] = MagicMock()
sys.modules["matplotlib.pyplot"] = mock_plt

import importlib.util
spec = importlib.util.spec_from_file_location("neon_code", str(SOURCE_PATH))
neon_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neon_mod)


class NeonEffectFailureBehaviorTests(unittest.TestCase):

    def setUp(self):
        mock_cv2.reset_mock()

    def test_failure_branch_missing_image(self):
        # Precondition established at source line 9:
        # img = cv2.imread(img_path)
        # When image path does not exist, cv2.imread returns None
        mock_cv2.imread.return_value = None

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = neon_mod.apply_neon_effect("non_existent_path.jpg")
            stdout_text = buf.getvalue().strip()

        # Explicit expected return value is None
        self.assertIsNone(result, "Expected None when image cannot be loaded")
        expected_msg = "Error: Unable to load image at non_existent_path.jpg"
        self.assertEqual(stdout_text, expected_msg)

    def test_ordinary_valid_call_succeeds_after_failure(self):
        # First trigger failure
        mock_cv2.imread.return_value = None
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            fail_result = neon_mod.apply_neon_effect("invalid.jpg")
        self.assertIsNone(fail_result)

        # Precondition established at source lines 9 to 25:
        # Ordinary valid image succeeds immediately after failure
        mock_image = MagicMock()
        mock_cv2.imread.return_value = mock_image
        mock_cv2.cvtColor.return_value = mock_image
        mock_cv2.pyrDown.return_value = mock_image
        mock_cv2.bilateralFilter.return_value = mock_image
        mock_cv2.pyrUp.return_value = mock_image
        mock_cv2.medianBlur.return_value = mock_image
        mock_cv2.adaptiveThreshold.return_value = mock_image
        mock_cv2.bitwise_and.return_value = mock_image
        mock_cv2.bitwise_xor.return_value = "neon_filtered_array"

        valid_result = neon_mod.apply_neon_effect("valid_photo.jpg")
        self.assertEqual(valid_result, "neon_filtered_array")

    def test_smallest_valid_input(self):
        # Smallest supported image array
        mock_small_image = MagicMock()
        mock_cv2.imread.return_value = mock_small_image
        mock_cv2.cvtColor.return_value = mock_small_image
        mock_cv2.pyrDown.return_value = mock_small_image
        mock_cv2.bilateralFilter.return_value = mock_small_image
        mock_cv2.pyrUp.return_value = mock_small_image
        mock_cv2.medianBlur.return_value = mock_small_image
        mock_cv2.adaptiveThreshold.return_value = mock_small_image
        mock_cv2.bitwise_and.return_value = mock_small_image
        mock_cv2.bitwise_xor.return_value = "small_neon_array"

        result = neon_mod.apply_neon_effect("smallest.jpg")
        self.assertEqual(result, "small_neon_array")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(NeonEffectFailureBehaviorTests)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print(f"Python: {sys.version}")
    print("Command: python3 work/R29-T018/check.py")
    print(f"Nonzero tests: {test_result.testsRun}")
    if not test_result.wasSuccessful():
        sys.exit(1)
