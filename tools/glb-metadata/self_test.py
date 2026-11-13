#!/usr/bin/env python3
"""self_test.py — offline tests for glb_metadata.py.

Run from inside this folder with no arguments, no network:

    python3 self_test.py

Writes three tiny GLB fixture files into a temp directory, then imports
glb_metadata from the same folder (via sys.path) and calls its check_glb
function on a real open file object, asserting both the printed lines and
the returned True/False. No subprocess, no network, nothing written outside
a temp dir. Exits 0 only when every check passes. Standard library only.

Fixture layout (all little-endian):

  header     12 bytes : uint32 magic, uint32 version, uint32 declared length
  chunk      8 bytes  : uint32 chunkLength, uint32 chunkType
  data       N bytes  : chunk payload

so the declared length must equal 12 + 8 + N of the bytes actually written.
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

import glb_metadata as gm  # noqa: E402  (import after sys.path tweak)

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

    magic:   uint32 little-endian
    version: uint32
    length:  uint32 written into the 12-byte header (the declared length)
    chunks:  list of (chunk_type_int, chunk_data_bytes)
    """
    header = struct.pack("<III", magic, version, length)
    body = b""
    for chunk_type, chunk_data in chunks:
        body += struct.pack("<II", len(chunk_data), chunk_type) + chunk_data
    return header + body


def capture_check_glb(data):
    """Write `data` to a temp file, run check_glb on it.

    Returns (printed_stdout, returned_ok). A real file object is used so
    that check_glb sees the same file size and file name it would see in
    normal use.
    """
    tmpdir = tempfile.mkdtemp(prefix="glb-metadata-self-test-")
    path = os.path.join(tmpdir, "fixture.glb")
    with open(path, "wb") as fh:
        fh.write(data)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        with open(path, "rb") as fh:
            ok = gm.check_glb(fh)
        printed = sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout
    return printed, ok


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def main():
    valid_magic = 0x46546C67      # "glTF"
    valid_version = 2
    chunk_type_json = 0x4E4F534A  # "JSON"

    # --- valid fixture: declared length must equal the real byte count ---
    json_payload = b"{}" + b"\x00" * 2        # 4 bytes, 4-byte aligned
    real_length = 12 + 8 + len(json_payload)   # 12 + 8 + 4 = 24
    valid_bytes = make_glb(
        valid_magic, valid_version, real_length,
        [(chunk_type_json, json_payload)],
    )
    check(len(valid_bytes) == real_length,
          "valid: declared length equals real byte count (%d)" % real_length)

    output, ok = capture_check_glb(valid_bytes)
    check("magic: glTF" in output, "valid: magic is printed")
    check("version: 2" in output, "valid: version 2 is printed")
    check("type=JSON" in output, "valid: chunk type JSON is printed")
    check("length=%d" % len(json_payload) in output,
          "valid: chunk length is printed")
    check(str(real_length) in output, "valid: total length is printed")
    check(ok is True, "valid: check_glb returns True")

    # --- bad magic: kept at 12 bytes, no chunks ---
    bad_magic = 0xDEADBEAF
    bad_bytes = make_glb(bad_magic, valid_version, 12, [])
    check(len(bad_bytes) == 12, "bad magic: fixture is 12 bytes")
    output, ok = capture_check_glb(bad_bytes)
    check("wrong magic" in output, "bad magic: tool reports wrong magic")
    check(ok is False, "bad magic: check_glb returns False")

    # --- declared length that does not match the real byte count ---
    # Same 24 real bytes as the valid fixture, but the header claims 20.
    mismatch_bytes = make_glb(
        valid_magic, valid_version, real_length - 4,
        [(chunk_type_json, json_payload)],
    )
    check(len(mismatch_bytes) == real_length and real_length != real_length - 4,
          "length mismatch: fixture still writes %d bytes" % real_length)
    output, ok = capture_check_glb(mismatch_bytes)
    check("does NOT match file size" in output,
          "length mismatch: tool reports the mismatch")
    check(ok is False, "length mismatch: check_glb returns False")

    # --- summary ---
    print("\nResults: %d/%d checks passed" % (PASSED, CHECKS))
    return 0 if PASSED == CHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
