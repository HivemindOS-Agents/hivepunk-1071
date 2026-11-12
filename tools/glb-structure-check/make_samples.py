#!/usr/bin/env python3
"""make_samples.py -- generate binary sample GLB files for glb-structure-check.

Generates in the sample/ directory two files:
  valid_minimal.glb - a minimally valid GLB with JSON chunk containing asset version.
  bad_magic.glb - a file with incorrect magic bytes.

Run from the tool folder: python3 make_samples.py
"""

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"

def write_valid_minimal():
    """Create a minimal valid GLB: magic glTF, version 2, one JSON chunk."""
    # Minimal JSON: asset version 2.0
    json_str = '{"asset":{"version":"2.0"}}'
    json_bytes = json_str.encode('utf-8')
    # Pad JSON to 4-byte alignment (already aligned: length 27, aligned 28)
    padding = (4 - len(json_bytes) % 4) % 4
    padded_json = json_bytes + b' ' * padding
    # Chunk: JSON type 0x4E4F534A, length of chunk data (padded_json)
    chunk_length = len(padded_json)
    chunk_type = 0x4E4F534A  # JSON
    chunk_header = struct.pack('<II', chunk_length, chunk_type)
    # Total file length: 12 (header) + len(chunk_header) + chunk_length
    total_length = 12 + len(chunk_header) + chunk_length
    header = struct.pack('<4sII', b'glTF', 2, total_length)
    return header + chunk_header + padded_json

def write_bad_magic():
    """Create a file with wrong magic bytes (NOT 'glTF')."""
    json_str = '{"asset":{"version":"2.0"}}'
    json_bytes = json_str.encode('utf-8')
    padding = (4 - len(json_bytes) % 4) % 4
    padded_json = json_bytes + b' ' * padding
    chunk_length = len(padded_json)
    chunk_type = 0x4E4F534A
    chunk_header = struct.pack('<II', chunk_length, chunk_type)
    total_length = 12 + len(chunk_header) + chunk_length
    # Use "NOTg" as magic (should fail check)
    header = struct.pack('<4sII', b'NOTg', 2, total_length)
    return header + chunk_header + padded_json

def main():
    SAMPLE.mkdir(parents=True, exist_ok=True)
    valid_path = SAMPLE / "valid_minimal.glb"
    bad_path = SAMPLE / "bad_magic.glb"
    valid_path.write_bytes(write_valid_minimal())
    bad_path.write_bytes(write_bad_magic())
    print(f"Created {valid_path} ({valid_path.stat().st_size} bytes)")
    print(f"Created {bad_path} ({bad_path.stat().st_size} bytes)")
    sys.exit(0)

if __name__ == "__main__":
    main()
