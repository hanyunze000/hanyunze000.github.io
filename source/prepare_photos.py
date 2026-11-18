"""Prepare the published JPEGs and small gallery previews from the photographer's files."""

import argparse
from io import BytesIO
from math import sqrt
from pathlib import Path
from shutil import copyfile
import warnings

from PIL import Image, ImageCms, ImageOps

from photographs import ROWS


GALLERY = Path(__file__).resolve().parent.parent / "assets" / "photography"
LIMIT = 5_000_000
PREVIEW_SIZE = (1120, 840)


def encode_jpeg(image, quality, metadata):
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True,
               progressive=True, subsampling=2, **metadata)
    return buffer.getvalue()


def full_jpeg(image, metadata):
    data = encode_jpeg(image, 88, metadata)
    while len(data) > LIMIT:
        scale = min(0.95, 0.97 * sqrt(LIMIT / len(data)))
        size = tuple(max(1, round(value * scale)) for value in image.size)
        image = image.resize(size, Image.Resampling.LANCZOS)
        data = encode_jpeg(image, 88, metadata)
    low, high = 89, 98
    while low <= high:
        quality = (low + high) // 2
        candidate = encode_jpeg(image, quality, metadata)
        if len(candidate) <= LIMIT:
            data = candidate
            low = quality + 1
        else:
            high = quality - 1
    return data


def prepare(original, slug):
    destination = GALLERY / f"{slug}.jpg"
    keep_original = original.stat().st_size <= LIMIT
    with warnings.catch_warnings():
        # The supplied medium-format JPEGs are up to 102 megapixels.
        warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)
        with Image.open(original) as source:
            if source.format != "JPEG":
                raise ValueError(f"Expected a JPEG photograph: {original.name}")
            icc = source.info.get("icc_profile")
            exif = source.getexif()
            metadata = {"icc_profile": icc} if icc else {}
            credit = Image.Exif()
            for tag in (315, 33432):  # Artist and Copyright
                if tag in exif:
                    credit[tag] = exif[tag]
            if credit:
                metadata["exif"] = credit.tobytes()
            if keep_original:
                copyfile(original, destination)
                source.draft("RGB", PREVIEW_SIZE)
            else:
                width, height = source.size
                factor = 1
                while width * height // (factor * factor) > 36_000_000:
                    factor *= 2
                source.draft("RGB", (width // factor, height // factor))
            image = ImageOps.exif_transpose(source)
            if image.mode != "RGB":
                image = image.convert("RGB")
    if not keep_original:
        destination.write_bytes(full_jpeg(image, metadata))
    image.thumbnail(PREVIEW_SIZE, Image.Resampling.LANCZOS)
    if icc:
        image = ImageCms.profileToProfile(image, BytesIO(icc), ImageCms.createProfile("sRGB"), outputMode="RGB")
    image.save(GALLERY / "previews" / f"{slug}.webp", quality=84, method=4)
    return destination.stat().st_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("originals", type=Path)
    args = parser.parse_args()
    (GALLERY / "previews").mkdir(parents=True, exist_ok=True)
    for row in ROWS:
        for photo in row:
            source_file = args.originals / photo.source
            size = prepare(source_file, photo.slug)
            print(f"{photo.slug}: {source_file.stat().st_size:,} -> {size:,} bytes", flush=True)
