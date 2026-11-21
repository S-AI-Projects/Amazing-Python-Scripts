import unittest
from unittest.mock import MagicMock, patch, mock_open
import importlib.util
import os
import sys

# Provide mock PyPDF2 if not installed in the current environment
if 'PyPDF2' not in sys.modules:
    try:
        import PyPDF2
    except ImportError:
        mock_pypdf = MagicMock()
        sys.modules['PyPDF2'] = mock_pypdf

# Dynamic loader for hyphenated filename pdf-watermark.py
MODULE_PATH = os.path.join(os.path.dirname(__file__), 'pdf-watermark.py')
spec = importlib.util.spec_from_file_location('pdf_watermark_module', MODULE_PATH)
pdf_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pdf_mod)


class MockPage:
    def __init__(self, page_id):
        self.page_id = page_id
        self.merged_with = []

    def mergePage(self, other):
        self.merged_with.append(other.page_id)


class TestPDFWatermarkContract(unittest.TestCase):
    """
    Focused contract regression tests for PDF Watermark in PDF-Watermark/pdf-watermark.py.
    Preconditions cited:
      - Line 24: input_file must be loaded via PdfFileReader(input_file)
      - Line 25: watermark_file must be loaded via PdfFileReader(watermark_file)
      - Line 27: watermark_page must be extracted via mark.getPage(0)
    """

    def setUp(self):
        self.pdf_watermark = pdf_mod.pdf_watermark

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(pdf_mod, 'PdfFileWriter')
    @patch.object(pdf_mod, 'PdfFileReader')
    def test_smallest_valid_input(self, mock_reader_cls, mock_writer_cls, mock_file_open):
        """
        Smallest valid input: 1-page document with 1 watermark page.
        Precondition: Line 24 (input_file), Line 25 (watermark_file), Line 27 (mark.getPage(0)).
        """
        input_file = "single_page.pdf"
        watermark_file = "watermark.pdf"
        output_file = "watermarked.pdf"

        # Mocking reader for input PDF (1 page)
        mock_input_reader = MagicMock()
        mock_input_reader.getNumPages.return_value = 1
        page0 = MockPage("input_p0")
        mock_input_reader.getPage.side_effect = lambda idx: page0 if idx == 0 else None

        # Mocking reader for watermark PDF (1 page)
        mock_mark_reader = MagicMock()
        mark_page0 = MockPage("mark_p0")
        mock_mark_reader.getPage.side_effect = lambda idx: mark_page0 if idx == 0 else None

        def reader_factory(path):
            if path == input_file:
                return mock_input_reader
            elif path == watermark_file:
                return mock_mark_reader
            raise FileNotFoundError(path)

        mock_reader_cls.side_effect = reader_factory

        # Mocking writer
        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        # Execute
        result = self.pdf_watermark(input_file, watermark_file, output_file)

        # Assert returned value
        expected_result = 1
        self.assertEqual(result, expected_result)

        # Assert observable mutation: page 0 was merged with watermark page 0
        self.assertEqual(page0.merged_with, ["mark_p0"])

        # Assert output file writing
        mock_file_open.assert_called_once_with(output_file, 'wb')
        mock_writer.addPage.assert_called_once_with(page0)
        mock_writer.write.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(pdf_mod, 'PdfFileWriter')
    @patch.object(pdf_mod, 'PdfFileReader')
    def test_ordinary_input(self, mock_reader_cls, mock_writer_cls, mock_file_open):
        """
        Ordinary input: 3-page document with 1 watermark page.
        Precondition: Line 24 (input_file), Line 25 (watermark_file), Line 27 (mark.getPage(0)).
        """
        input_file = "document_3pages.pdf"
        watermark_file = "watermark.pdf"
        output_file = "output_doc.pdf"

        mock_input_reader = MagicMock()
        mock_input_reader.getNumPages.return_value = 3
        pages = [MockPage(f"input_p{i}") for i in range(3)]
        mock_input_reader.getPage.side_effect = lambda idx: pages[idx]

        mock_mark_reader = MagicMock()
        mark_page0 = MockPage("watermark_stamp")
        mock_mark_reader.getPage.side_effect = lambda idx: mark_page0 if idx == 0 else None

        def reader_factory(path):
            if path == input_file:
                return mock_input_reader
            elif path == watermark_file:
                return mock_mark_reader
            raise FileNotFoundError(path)

        mock_reader_cls.side_effect = reader_factory

        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        result = self.pdf_watermark(input_file, watermark_file, output_file)

        # Explicit expected return value
        expected_page_count = 3
        self.assertEqual(result, expected_page_count)

        # Assert observable mutations across all 3 pages
        for i, p in enumerate(pages):
            self.assertEqual(p.merged_with, ["watermark_stamp"])

        self.assertEqual(mock_writer.addPage.call_count, 3)
        mock_file_open.assert_called_once_with(output_file, 'wb')
        mock_writer.write.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(pdf_mod, 'PdfFileWriter')
    @patch.object(pdf_mod, 'PdfFileReader')
    def test_domain_boundary_multi_page_watermark_uses_page_zero(self, mock_reader_cls, mock_writer_cls, mock_file_open):
        """
        Boundary condition: Watermark PDF has multiple pages (e.g. 2 pages).
        Contract specifies only page 0 of watermark is merged onto all input pages.
        Precondition: Line 27 establishes watermark = mark.getPage(0).
        """
        input_file = "two_page_input.pdf"
        watermark_file = "multi_page_watermark.pdf"
        output_file = "boundary_output.pdf"

        mock_input_reader = MagicMock()
        mock_input_reader.getNumPages.return_value = 2
        pages = [MockPage(f"doc_p{i}") for i in range(2)]
        mock_input_reader.getPage.side_effect = lambda idx: pages[idx]

        mock_mark_reader = MagicMock()
        mark_p0 = MockPage("watermark_page_0")
        mark_p1 = MockPage("watermark_page_1")
        mock_mark_reader.getPage.side_effect = lambda idx: mark_p0 if idx == 0 else mark_p1

        def reader_factory(path):
            if path == input_file:
                return mock_input_reader
            elif path == watermark_file:
                return mock_mark_reader
            raise FileNotFoundError(path)

        mock_reader_cls.side_effect = reader_factory

        mock_writer = MagicMock()
        mock_writer_cls.return_value = mock_writer

        result = self.pdf_watermark(input_file, watermark_file, output_file)

        expected_count = 2
        self.assertEqual(result, expected_count)
        # Ensure page 0 was merged onto both pages, not page 1
        self.assertEqual(pages[0].merged_with, ["watermark_page_0"])
        self.assertEqual(pages[1].merged_with, ["watermark_page_0"])
        self.assertEqual(mock_writer.addPage.call_count, 2)


if __name__ == '__main__':
    unittest.main()
