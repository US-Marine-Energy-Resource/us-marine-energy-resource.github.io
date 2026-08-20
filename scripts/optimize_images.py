#!/usr/bin/env python3
"""One-time/on-demand image optimizer for docs/assets/.

Walks every raster image under ``docs/assets/`` (PNG/JPEG; the one SVG,
favicon.svg, is skipped) and, in place:

1. Downscales (longest edge > MAX_DIMENSION only) with Lanczos resampling.
2. Flattens RGBA to RGB when the image has no actual transparent pixels
   (true of every plot/screenshot/map in this repo today).
3. Quantizes via ``imagequant`` (the libimagequant engine also used by the
   ``pngquant`` CLI, but pip-installable with no system binary required).
   Falls back to a truecolor save if the requested quality floor can't be
   met, and prints a warning so that case gets manual review rather than
   silent quality loss.
4. Re-saves as PNG with ``optimize=True``.

This script is NOT run during ``mkdocs build`` -- run it by hand (or via a
pre-commit hook you set up locally) whenever you add or replace an image,
then commit the result. See hooks/check_image_sizes.py for the cheap,
dependency-free build-time guard that flags images this script hasn't been
run on.

Usage
-----
    pip install -r docs/requirements.txt
    python scripts/optimize_images.py [--docs-dir <path>]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MAX_DIMENSION = 2400
MAX_COLORS = 256
DITHERING_LEVEL = 1.0
MIN_QUALITY = 70
MAX_QUALITY = 95

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_DOCS_DIR = _SCRIPT_DIR.parent / "docs"

_RASTER_SUFFIXES = {".png", ".jpg", ".jpeg"}


def _find_images(assets_dir: Path) -> list[Path]:
    return sorted(
        p for p in assets_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in _RASTER_SUFFIXES
    )


def _resize_if_needed(im, path: Path):
    from PIL import Image

    longest = max(im.size)
    if longest <= MAX_DIMENSION:
        return im
    scale = MAX_DIMENSION / longest
    new_size = (round(im.width * scale), round(im.height * scale))
    print(f"  resize: {im.size} -> {new_size}")
    return im.resize(new_size, Image.LANCZOS)


def _flatten_if_opaque(im):
    if im.mode not in ("RGBA", "LA"):
        return im.convert("RGB") if im.mode != "RGB" else im
    alpha = im.getchannel("A")
    if alpha.getextrema() == (255, 255):
        return im.convert("RGB")
    return im.convert("RGBA")


def _quantize(im, path: Path):
    import imagequant

    try:
        return imagequant.quantize_pil_image(
            im,
            dithering_level=DITHERING_LEVEL,
            max_colors=MAX_COLORS,
            min_quality=MIN_QUALITY,
            max_quality=MAX_QUALITY,
        )
    except RuntimeError as exc:
        print(
            f"  WARNING: {path.name} could not be quantized within the "
            f"quality floor ({exc}) -- saved as truecolor; review manually."
        )
        return im


def optimize_one(path: Path) -> tuple[int, int]:
    from PIL import Image

    before = path.stat().st_size
    with Image.open(path) as im:
        im = _flatten_if_opaque(im)
        im = _resize_if_needed(im, path)
        if path.suffix.lower() == ".png":
            im = _quantize(im, path)
        im.save(path, optimize=True)
    after = path.stat().st_size
    return before, after


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-dir", type=Path, default=_DEFAULT_DOCS_DIR)
    args = parser.parse_args()

    assets_dir = args.docs_dir.resolve() / "assets"
    images = _find_images(assets_dir)
    if not images:
        print(f"No raster images found under {assets_dir}")
        return

    total_before = total_after = 0
    rows: list[tuple[str, int, int]] = []

    for path in images:
        print(f"{path.relative_to(assets_dir.parent)}:")
        before, after = optimize_one(path)
        total_before += before
        total_after += after
        rows.append((str(path.relative_to(assets_dir.parent)), before, after))

    print("\n--- summary ---")
    for name, before, after in rows:
        pct = (after / before * 100) if before else 0
        print(f"{name:70s} {before:>9,d} -> {after:>9,d} bytes ({pct:5.1f}%)")

    if total_before:
        pct = total_after / total_before * 100
        print(
            f"\nTotal: {total_before:,d} -> {total_after:,d} bytes "
            f"({pct:.1f}%, {100 - pct:.1f}% reduction)"
        )

    print("\nattr_list snippets (paste width/height into markdown):")
    from PIL import Image

    for path in images:
        with Image.open(path) as im:
            print(f'  {path.name}: {{ width="{im.width}" height="{im.height}" loading="lazy" }}')


if __name__ == "__main__":
    sys.exit(main())
