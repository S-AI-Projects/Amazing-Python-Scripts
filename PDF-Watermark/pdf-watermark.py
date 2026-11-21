from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader

"""
PDF Watermark Contract:
Function: pdf_watermark(input_file: str, watermark_file: str, output_file: str = 'watermarked.pdf') -> int
Inputs:
  - input_file (str): Path to input PDF file to watermark.
  - watermark_file (str): Path to PDF file containing the watermark page.
  - output_file (str): Path where the watermarked PDF will be saved (default: 'watermarked.pdf').
Preconditions:
  - Line 24: input_file must be a readable valid PDF source.
  - Line 25: watermark_file must be a readable valid PDF source.
  - Line 27: watermark_file must have at least one page accessible via getPage(0).
Outputs:
  - int: Number of watermarked pages written to output_file.
Observable Mutation / Side Effects:
  - Line 36: Writes output_file to disk containing each input page merged with watermark page 0.
"""


def pdf_watermark(input_file, watermark_file, output_file='watermarked.pdf'):
    ori_pdf = PdfFileReader(input_file)
    mark = PdfFileReader(watermark_file)

    watermark_page = mark.getPage(0)
    ori_page_count = ori_pdf.getNumPages()

    final = PdfFileWriter()
    for i in range(ori_page_count):
        each_page = ori_pdf.getPage(i)
        each_page.mergePage(watermark_page)
        final.addPage(each_page)

    with open(output_file, 'wb') as output:
        final.write(output)

    return ori_page_count


if __name__ == '__main__':
    input_File = input(
        "Enter File Name You want to add Watermark too[Include .pdf extension]: ")
    watermark = input("Enter Watermark File Name [Include .pdf extension]: ")
    pdf_watermark(input_File, watermark)
