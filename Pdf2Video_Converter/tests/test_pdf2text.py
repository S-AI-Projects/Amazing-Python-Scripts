import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


SOURCE = Path(__file__).resolve().parents[1] / "script.py"


def load_converter_module():
    pil = types.ModuleType("PIL")
    pil.__path__ = []
    pil.Image = types.SimpleNamespace(open=MagicMock(name="Image.open"))

    pytesseract = types.ModuleType("pytesseract")
    pytesseract.image_to_string = MagicMock(name="image_to_string")

    mutagen = types.ModuleType("mutagen")
    mutagen.__path__ = []
    mutagen_mp3 = types.ModuleType("mutagen.mp3")
    mutagen_mp3.MP3 = MagicMock(name="MP3")

    moviepy = types.ModuleType("moviepy")
    moviepy.__path__ = []
    moviepy_editor = types.ModuleType("moviepy.editor")
    moviepy_editor.VideoFileClip = MagicMock(name="VideoFileClip")
    moviepy_editor.AudioFileClip = MagicMock(name="AudioFileClip")

    gtts = types.ModuleType("gtts")
    gtts.gTTS = MagicMock(name="gTTS")

    pdf2image = types.ModuleType("pdf2image")
    pdf2image.convert_from_path = MagicMock(name="convert_from_path")

    modules = {
        "PIL": pil,
        "pytesseract": pytesseract,
        "mutagen": mutagen,
        "mutagen.mp3": mutagen_mp3,
        "moviepy": moviepy,
        "moviepy.editor": moviepy_editor,
        "gtts": gtts,
        "pdf2image": pdf2image,
    }
    spec = importlib.util.spec_from_file_location("pdf2video_script", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load converter module from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module


CONVERTER = load_converter_module()


class Pdf2TextBoundaryTests(unittest.TestCase):
    def test_zero_pages_returns_empty_text(self):
        # script.py line 15 establishes that conversion supplies the pages;
        # with zero pages, lines 20 and 33-37 execute no page operations.
        pdf_input = "empty.pdf"
        expected = ""
        with (
            patch.object(CONVERTER, "convert_from_path", return_value=[]) as convert,
            patch.object(CONVERTER.Image, "open") as image_open,
            patch.object(CONVERTER.pytesseract, "image_to_string") as recognize,
            patch.object(CONVERTER.os, "remove") as remove,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            actual = CONVERTER.pdf2text(pdf_input)

        print(
            f"pdf2text({pdf_input!r}) expected={expected!r}, actual={actual!r}"
        )
        self.assertIs(type(actual), str)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")
        convert.assert_called_once_with(pdf_input, 500)
        image_open.assert_not_called()
        recognize.assert_not_called()
        remove.assert_not_called()

    def test_one_page_returns_ocr_text_with_existing_hyphen_normalization(self):
        # script.py lines 20-26 save each supplied page; lines 33-40 OCR and
        # normalize each result, and lines 43-47 remove page images and return.
        pdf_input = "ordinary.pdf"
        page = MagicMock(name="single page")
        image = object()
        ocr_text = "Boundary-\ntext\n"
        expected = "Boundarytext\n"
        with (
            patch.object(
                CONVERTER, "convert_from_path", return_value=[page]
            ) as convert,
            patch.object(CONVERTER.Image, "open", return_value=image) as image_open,
            patch.object(
                CONVERTER.pytesseract,
                "image_to_string",
                return_value=ocr_text,
            ) as recognize,
            patch.object(CONVERTER.os, "remove") as remove,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            actual = CONVERTER.pdf2text(pdf_input)

        print(
            f"pdf2text({pdf_input!r}), OCR={ocr_text!r}, "
            f"expected={expected!r}, actual={actual!r}"
        )
        self.assertIs(type(actual), str)
        self.assertEqual(actual, expected, f"expected={expected!r}; actual={actual!r}")
        convert.assert_called_once_with(pdf_input, 500)
        page.save.assert_called_once_with("page_1.jpg", "JPEG")
        image_open.assert_called_once_with("page_1.jpg")
        recognize.assert_called_once_with(image)
        remove.assert_called_once_with("page_1.jpg")


if __name__ == "__main__":
    unittest.main()
