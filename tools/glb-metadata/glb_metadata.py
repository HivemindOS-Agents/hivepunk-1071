#!/usr/bin/env python3
"""glb_metadata.py

Read a .glb (GLTF Binary) file's header metadata and print:
- magic bytes
- version
- declared length
- each chunk's type and length

Usage:  python3 glb_metadata.py model.glb

Stdlib only, no network.
"""

import os
import struct
import sys

# Constants
GLTF_MAGIC = 0x46546C67  # 'glTF' in little-endian ASCII
GLTF_VERSION = 2
CHUNK_JSON = 0x4E4F534A  # 'JSON' in little-endian ASCII
CHUNK_BIN = 0x004E4942   # 'BIN\0' in little-endian ASCII

CHUNK_NAMES = {
    CHUNK_JSON: 'JSON',
    CHUNK_BIN: 'BIN',
}

HEADER_FORMAT = '<III'  # three uint32 little-endian: magic, version, length
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CHUNK_HEADER_FORMAT = '<II'  # uint32 chunkLength, uint32 chunkType
CHUNK_HEADER_SIZE = struct.calcsize(CHUNK_HEADER_FORMAT)


def check_glb(fh):
    """Read a GLB file from an open binary file-like object and print metadata.

    Returns True if the file is structurally valid, False otherwise.
    """
    # Get file size (if possible)
    try:
        fh.seek(0, os.SEEK_END)
        file_size = fh.tell()
        fh.seek(0)
    except (OSError, AttributeError):
        file_size = None

    raw_header = fh.read(HEADER_SIZE)
    if len(raw_header) < HEADER_SIZE:
        print(f"error: file too small for GLB header ({len(raw_header)} bytes)", file=sys.stderr)
        return False

    magic, version, declared_length = struct.unpack(HEADER_FORMAT, raw_header)

    # Print file info first
    if file_size is not None:
        print(f"File: {getattr(fh, 'name', 'stdin')} ({file_size} bytes)")
    else:
        print(f"File: {getattr(fh, 'name', 'stdin')}")

    # Magic check
    if magic != GLTF_MAGIC:
        raw_magic_bytes = struct.pack('<I', magic)
        as_str = raw_magic_bytes.decode('latin-1', errors='replace')
        print(f"magic: 0x{magic:08X} ({as_str!r}) — wrong magic")
        return False

    # If we got this far, magic is correct
    raw_magic_bytes = struct.pack('<I', magic)
    as_str = raw_magic_bytes.decode('latin-1', errors='replace')
    print(f"magic: {as_str} (0x{magic:08X})")
    print(f"version: {version}")
    print(f"declared length: {declared_length}", end='')

    if file_size is not None:
        if declared_length == file_size:
            print(f" (matches file size)")
        else:
            print(f" (does NOT match file size, which is {file_size})")
            return False
    else:
        print()

    if version != GLTF_VERSION:
        print(f"wrong version — expected {GLTF_VERSION}", file=sys.stderr)
        return False

    # Read chunks
    chunk_index = 0
    while True:
        chunk_header_bytes = fh.read(CHUNK_HEADER_SIZE)
        if len(chunk_header_bytes) < CHUNK_HEADER_SIZE:
            if len(chunk_header_bytes) == 0:
                break  # normal end
            print(f"warning: truncated chunk header at offset", file=sys.stderr)
            return False

        chunk_length, chunk_type = struct.unpack(CHUNK_HEADER_FORMAT, chunk_header_bytes)
        type_name = CHUNK_NAMES.get(chunk_type, f"unknown (0x{chunk_type:08X})")
        print(f"chunk {chunk_index}: type={type_name} length={chunk_length}")

        # Skip over the chunk data
        fh.seek(chunk_length, os.SEEK_CUR)
        chunk_index += 1

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 glb_metadata.py <file.glb>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        with open(path, 'rb') as fh:
            ok = check_glb(fh)
        return 0 if ok else 1
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"error: permission denied: {path}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
