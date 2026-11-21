import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from main import compute_watermark_geometry, apply_watermark_and_resize, FolderSelectAndRun, basewidth


class TestImageWatermarkerRefactoring(unittest.TestCase):
    """
    Characterisation and unit tests for extracted geometry helper in imageWatermarker/main.py.
    Anchors cited:
      - Line 36: image_files = []
      - Line 42: output_path = join(outfolder, ('with-watermark_' + name))
    """

    def test_smallest_valid_input_geometry(self):
        """
        Smallest valid input: Image (100, 100), watermark (20, 20).
        """
        im_size = (100, 100)
        mark_size = (20, 20)
        geom = compute_watermark_geometry(im_size, mark_size, base_width=2048)

        # Expected position: (100 - (20 + 50), 100 - (20 + 50)) = (30, 30)
        expected_position = (30, 30)
        self.assertEqual(geom["position"], expected_position)

        # Expected target size: (2048, 2048)
        expected_size = (2048, 2048)
        self.assertEqual(geom["target_size"], expected_size)

    def test_ordinary_input_geometry(self):
        """
        Ordinary input: High-resolution photo (4000, 3000), watermark (400, 200).
        """
        im_size = (4000, 3000)
        mark_size = (400, 200)
        geom = compute_watermark_geometry(im_size, mark_size, base_width=2048)

        expected_position = (4000 - 450, 3000 - 250)
        self.assertEqual(geom["position"], (3550, 2750))

        expected_hsize = int(3000 * (2048 / 4000.0))
        self.assertEqual(geom["target_size"], (2048, expected_hsize))

    def test_characterisation_before_and_after_equivalence(self):
        """
        Characterisation test asserting exact equivalence between original formula and extracted helper.
        Original:
          position = (im.size[0] - (mark.size[0] + 50), im.size[1] - (mark.size[1] + 50))
          wpercent = (basewidth / float(im.size[0]))
          hsize = int((float(im.size[1]) * float(wpercent)))
        """
        sizes_to_test = [
            ((800, 600), (100, 50)),
            ((1920, 1080), (250, 80)),
            ((3000, 2000), (300, 150))
        ]

        for im_size, mark_size in sizes_to_test:
            # Baseline calculation
            orig_position = (im_size[0] - (mark_size[0] + 50), im_size[1] - (mark_size[1] + 50))
            orig_wpercent = (basewidth / float(im_size[0]))
            orig_hsize = int((float(im_size[1]) * float(orig_wpercent)))

            # Refactored helper
            refactored = compute_watermark_geometry(im_size, mark_size, basewidth)

            self.assertEqual(refactored["position"], orig_position)
            self.assertEqual(refactored["target_size"], (basewidth, orig_hsize))
            self.assertAlmostEqual(refactored["wpercent"], orig_wpercent)

    def test_apply_watermark_and_resize_output_shape(self):
        """
        Unit test verifying resized composite image dimensions.
        """
        im = Image.new('RGB', (1000, 500), color='white')
        mark = Image.new('RGBA', (100, 50), color='blue')

        result_im = apply_watermark_and_resize(im, mark, base_width=1000)
        self.assertEqual(result_im.size, (1000, 500))

    def test_folder_select_and_run_default_call(self):
        """
        Verifies FolderSelectAndRun invokes batch with default signature gracefully.
        """
        with patch('main.batch', return_value=[]) as mock_batch:
            res = FolderSelectAndRun()
            mock_batch.assert_called_once_with("<input folder>", "<output folder>", "<watermark image>")
            self.assertEqual(res, [])


if __name__ == '__main__':
    unittest.main()
