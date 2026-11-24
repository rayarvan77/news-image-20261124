#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 make.fun bounty.

Copies the pre-rendered entry.png (built by draw_poster.py) into the
output directory and verifies it meets the competition rules: a whole
PNG, 1024x1024 pixels, at most 1 MiB. Pure Python 3 standard library,
no network, fully deterministic: two runs write byte-identical files.
"""

import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def png_dimensions(path):
    """Read width/height from the PNG IHDR chunk (bytes 16..24)."""
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def png_is_whole(path):
    """A whole PNG ends with the 12-byte IEND chunk."""
    with open(path, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    return tail == b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)

    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = png_dimensions(dest)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    if not png_is_whole(dest):
        raise SystemExit("entry.png is truncated: missing IEND chunk")

    with open(dest, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"entry.png: {width}x{height}, {size} bytes, sha256={digest}")
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
