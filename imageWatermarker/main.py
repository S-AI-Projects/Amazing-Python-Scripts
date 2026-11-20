import os
import sys
from os.path import join
from PIL import Image, ImageEnhance

# Resampling filter compatibility (PIL 10+)
RESAMPLE_FILTER = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS', getattr(Image, 'ANTIALIAS', 1))

basewidth = 2048

"""
Contract & Refactoring Specification:
Extracted Helper: compute_watermark_geometry(im_size: tuple[int, int], mark_size: tuple[int, int], base_width: int = 2048) -> dict
Preconditions:
  - Source anchor Line 36: image_files = []
  - Source anchor Line 42: output_path = join(outfolder, ('with-watermark_' + name))
  - im_size[0] > 0, im_size[1] > 0, mark_size[0] > 0, mark_size[1] > 0
Invariants:
  - Preserves exact watermark placement (bottom-right offset by 50px).
  - Preserves exact aspect ratio during perspective resize to base_width.
"""


def compute_watermark_geometry(im_size, mark_size, base_width=basewidth):
    """
    Extracted helper calculating watermark placement coordinates and target resize dimensions.
    Single Responsibility: Pure geometric calculation for watermarking and resizing.
    """
    position = (
        im_size[0] - (mark_size[0] + 50),
        im_size[1] - (mark_size[1] + 50)
    )
    wpercent = base_width / float(im_size[0])
    hsize = int(float(im_size[1]) * float(wpercent))
    return {
        "position": position,
        "target_size": (base_width, hsize),
        "wpercent": wpercent
    }


def apply_watermark_and_resize(im, mark, base_width=basewidth):
    """
    Applies watermark composite and resizes image according to compute_watermark_geometry.
    """
    geom = compute_watermark_geometry(im.size, mark.size, base_width)

    # Composite watermark layer
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, geom["position"])
    new_image = Image.composite(layer, im, layer)

    # Resize in perspective
    smaller_new_image = new_image.resize(geom["target_size"], RESAMPLE_FILTER)
    return smaller_new_image


def batch(infolder, outfolder, watermark, base_width=basewidth):
    if not os.path.exists(watermark):
        return []

    mark = Image.open(watermark)
    image_files = []
    output_records = []

    for root, dirs, files in os.walk(infolder):
        for name in files:
            image_files.append((root, name))

    for root, name in image_files:
        try:
            im = Image.open(join(root, name))
            smaller_new_image = apply_watermark_and_resize(im, mark, base_width)

            output_path = join(outfolder, ('with-watermark_' + name))
            os.makedirs(outfolder, exist_ok=True)
            smaller_new_image.save(output_path, 'jpeg')
            output_records.append(output_path)
        except Exception as error:
            print('Caught this error: ' + repr(error))

    return output_records


def FolderSelectAndRun(infolder="<input folder>", outfolder="<output folder>", watermark="<watermark image>"):
    return batch(infolder, outfolder, watermark)


if __name__ == '__main__':
    FolderSelectAndRun()
