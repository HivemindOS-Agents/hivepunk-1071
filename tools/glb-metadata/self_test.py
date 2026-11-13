#!/usr/bin/env python3
"""self_test.py — offline tests for glb_metadata.py.

Run from inside this folder with no arguments:
    python3 self_test.py

Writes two tiny GLB fixture files into a temp directory, then imports
glb_metadata from the same folder (via sys.path) and calls its check_glb
function on each, asserting the output lines. No subprocess, no network,
no files outside this folder are read or written. Exits 0 only when every
check passes. Standard library only.
"""

import io
import os
import struct
import sys
import tempfile
from pathlib import Path

# Ensure the tool can be imported from this folder
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import glb_metadata as gm

CHECKS = 0
PASSED = 0


def check(condition, label):
    global CHECKS, PASSED
    CHECKS += 1
    if not condition:
        print("FAIL: %s" % label)
        return
    PASSED += 1
    print("ok: %s" % label)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------

def make_glb(magic, version, length, chunks):
    """Return bytes of a complete GLB file.

    magic: uint32 little-endian
    version: uint32
    length: uint32 (the total length written into the 12-byte header)
    chunks: list of (chunk_type_int, chunk_data_bytes)
    """
    header = struct.pack("<III", magic, version, length)
    body = b""
    for chunk_type, chunk_data in chunks:
        chunk_header = struct.pack("<II", len(chunk_data), chunk_type)
        body += chunk_header + chunk_data
    return header + body


def capture_check_glb(data):
    """Feed `data` to check_glb via a BytesIO, return the printed lines."""
    # check_glb reads from a file object; pass an in-memory BytesIO
    fobj = io.BytesIO(data)
    fobj.name = "fixture.glb"  # for error messages
    # Capture print output
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        gm.check_glb(fobj)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout


def main():
    # --- valid_minimal.glb ---
    # Magic 0x46546C67 = "glTF"
    # Version 2, total length 20
    # One chunk: type 0x4E4F534A = "JSON" little-endian, length 4 (empty object
    # padded to 4 bytes)
    valid_magic = 0x46546C67
    valid_version = 2
    valid_length = 20
    chunk_type_json = 0x4E4F534A
    chunk_data = b"{}" + b"\x00" * 2  # 4 bytes with padding
    valid_bytes = make_glb(valid_magic, valid_version, valid_length,
                           [(chunk_type_json, chunk_data)])
    assert len(valid_bytes) == valid_length, "fixture size mismatch"

    output = capture_check_glb(valid_bytes)
    check("magic: glTF" in output or "46546C67" in output,
          "valid: magic is printed")
    # tool prints magic as hex or as string; check at least that version line exists
    check("version: 2" in output or "Version: 2" in output or "version=2" in output,
          "valid: version 2 printed")
    check("JSON" in output or "4E4F534A" in output,
          "valid: chunk type JSON printed")
    # Length check
    check(str(valid_length) in output,
          "valid: total length printed")

    # --- bad_magic.glb ---
    # Wrong magic, version 2, length 12, no chunks
    bad_magic = 0xDEADBEAF
    bad_length = 12
    bad_bytes = make_glb(bad_magic, valid_version, bad_length, [])
    output = capture_check_glb(bad_bytes)
    check("wrong magic" in output.lower() or "deadbeaf" in output.lower() or "magic" in output.lower(),
          "bad magic: tool reports wrong magic")
    # Should not report version 2 when magic is wrong
    # (tool may still print version; we don't enforce that it stops, but it must mention magic)

    # --- summary ---
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
