#!/usr/bin/env python3
"""make_samples.py — Write the two sample .glb files used by glb_check.py self-test.

Run once before the self-test:
    python3 make_samples.py

Creates in sample/:
    valid_minimal.glb  — a minimal valid GLB file
    bad_magic.glb      — same structure but with invalid magic bytes

Both files are 56 bytes.
"""

import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE_DIR = HERE / "sample"

def build_glb(json_obj, magic=b"glTF"):
    """Build a minimal valid two-chunk GLB (JSON only, no BIN chunk)."""
    # JSON chunk content
    json_bytes = json.dumps(json_obj, separators=(",", ":")).encode("utf-8")
    # Pad to 4 bytes
    padding = (4 - len(json_bytes) % 4) % 4
    json_bytes_padded = json_bytes + b" " * padding

    # Chunk header: length (uint32), type (uint32, JSON = 0x4E4F534A)
    chunk_header = struct.pack("<II", len(json_bytes_padded), 0x4E4F534A)

    # Total file: 12-byte header + 8-byte chunk header + padded chunk
    total_length = 12 + 8 + len(json_bytes_padded)

    # File header: magic (4 bytes), version (uint32, =2), total length (uint32)
    header = magic + struct.pack("<II", 2, total_length)

    return header + chunk_header + json_bytes_padded


def write_sample(filename, glb_bytes):
    out_path = SAMPLE_DIR / filename
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(glb_bytes)
    print(f"Wrote {out_path} ({len(glb_bytes)} bytes)")


def main():
    json_content = {"asset": {"version": "2.0"}}

    # Valid file
    valid = build_glb(json_content, magic=b"glTF")
    write_sample("valid_minimal.glb", valid)

    # Bad magic file
    bad = build_glb(json_content, magic=b"NOTglTF")
    write_sample("bad_magic.glb", bad)


if __name__ == "__main__":
    main()
