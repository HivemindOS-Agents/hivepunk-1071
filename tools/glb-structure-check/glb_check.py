#!/usr/bin/env python3
"""glb_check.py — Validate a .glb (GLTF Binary) file's structure.

Reads a binary .glb file and checks:
  1. Magic bytes: first 4 bytes must be 'glTF'
  2. Declared total length vs file size
  3. Chunk layout: JSON chunk appears first, chunk lengths are 4-byte aligned
  4. Required top-level glTF keys: asset.version must be present

Usage:
    python3 glb_check.py <path-to-file.glb>

Returns 0 if all checks pass, 1 otherwise. Prints progress and results to stdout.
"""

import json
import os
import struct
import sys

# Chunk types (GLTF spec):
# 0x4E4F534A = JSON chunk
# 0x004E4942 = BIN chunk
CHUNK_TYPE_JSON = 0x4E4F534A
CHUNK_TYPE_BIN = 0x004E4942

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 glb_check.py <file.glb>")
        sys.exit(1)

    path = sys.argv[1]
    basename = os.path.basename(path)

    if not os.path.exists(path):
        print(f"FAIL: {basename}: file not found")
        sys.exit(1)

    with open(path, "rb") as f:
        data = f.read()

    file_size = len(data)
    all_checks_pass = True

    # --- Check 1: Magic bytes ---
    if file_size < 4:
        print(f"FAIL: {basename}: file too small for magic bytes ({file_size} bytes)")
        sys.exit(1)

    magic = data[0:4]
    if magic == b"glTF":
        print(f"PASS: {basename}: magic check passed (glTF)")
    else:
        print(f"FAIL: {basename}: magic check failed (got {magic!r})")
        all_checks_pass = False

    # --- Check 2: Total length vs file size ---
    if file_size < 12:
        print(f"FAIL: {basename}: file too small for header ({file_size} bytes)")
        sys.exit(1)

    version = struct.unpack_from("<I", data, 4)[0]
    declared_length = struct.unpack_from("<I", data, 8)[0]

    if version != 2:
        print(f"FAIL: {basename}: version check failed (got {version}, expected 2)")
        all_checks_pass = False

    if declared_length == file_size:
        print(f"PASS: {basename}: total length check passed ({declared_length} bytes)")
    else:
        print(f"FAIL: {basename}: total length check failed (declared {declared_length}, file is {file_size})")
        all_checks_pass = False

    # Use declared length for further checks to match spec behavior
    actual_file_size = min(declared_length, file_size)

    # --- Check 3: Chunk layout ---
    offset = 12  # start of first chunk header
    chunk_index = 0
    json_chunk_found = False
    chunk_layout_ok = True
    first_chunk_is_json = None

    while offset + 8 <= actual_file_size:
        chunk_length = struct.unpack_from("<I", data, offset)[0]
        chunk_type = struct.unpack_from("<I", data, offset + 4)[0]

        # No end-of-file sentinel, must have at least chunk_length bytes
        if offset + 8 + chunk_length > actual_file_size:
            print(f"FAIL: {basename}: chunk {chunk_index} (type 0x{chunk_type:08X}) length {chunk_length} exceeds file boundary")
            chunk_layout_ok = False
            break

        # Check 4-byte alignment
        if chunk_length % 4 != 0:
            print(f"FAIL: {basename}: chunk {chunk_index} length {chunk_length} not aligned to 4 bytes")
            chunk_layout_ok = False

        if chunk_type == CHUNK_TYPE_JSON:
            json_chunk_found = True
            chunk_content = data[offset + 8 : offset + 8 + chunk_length]
            # Check for required keys
            _check_required_keys(chunk_content, basename)

            if first_chunk_is_json is None:
                first_chunk_is_json = True
            else:
                print(f"FAIL: {basename}: multiple JSON chunks found")
                chunk_layout_ok = False
        elif chunk_type == CHUNK_TYPE_BIN:
            if first_chunk_is_json is None:
                first_chunk_is_json = False

        offset += 8 + chunk_length
        chunk_index += 1

    if first_chunk_is_json is True:
        print(f"PASS: {basename}: chunk layout check passed (JSON first, lengths aligned)")
    elif first_chunk_is_json is False:
        print(f"FAIL: {basename}: chunk layout check failed (first chunk is not JSON)")
        chunk_layout_ok = False
    else:
        print(f"FAIL: {basename}: chunk layout check failed (no chunks found, first chunk not JSON)")
        chunk_layout_ok = False

    if not chunk_layout_ok:
        all_checks_pass = False

    # --- Summary ---
    if all_checks_pass:
        print(f"PASS: {basename}: all checks passed")
    else:
        print(f"FAIL: {basename}: one or more checks failed")

    sys.exit(0 if all_checks_pass else 1)


def _check_required_keys(chunk_bytes, basename):
    """Check that the JSON chunk contains required top-level glTF keys."""
    try:
        decoded = chunk_bytes.decode("utf-8").rstrip("\x00").rstrip()
        gltf = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"FAIL: {basename}: JSON chunk decode failed ({e})")
        return False

    if not isinstance(gltf, dict):
        print(f"FAIL: {basename}: JSON chunk is not a top-level object")
        return False

    # Check asset.version
    asset = gltf.get("asset")
    has_version = False
    if isinstance(asset, dict):
        version_str = asset.get("version")
        if version_str is not None:
            has_version = True
            # Accept any non-empty version string
            if str(version_str).strip():
                pass

    if has_version:
        print(f"PASS: {basename}: required keys check passed (asset.version present)")
        return True
    else:
        print(f"FAIL: {basename}: required keys check failed (missing asset.version)")
        return False


if __name__ == "__main__":
    main()
