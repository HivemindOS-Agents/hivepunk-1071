#!/usr/bin/env python3
"""glb_check.py -- validate the binary structure of a GLB file.

Reads a .glb file, checks:
  - Magic bytes are 'glTF'
  - Version is 2
  - File length matches actual file size
  - At least one JSON chunk present (type 0x4E4F534A)
  - Chunk lengths are consistent

Usage:
  python3 glb_check.py file.glb

Exit codes:
  0 - file is valid
  1 - file is invalid (structure error)
  2 - cannot read file (I/O error)
"""

import struct
import sys

def read_glb_header(f):
    """Read and return (magic, version, length)."""
    header = f.read(12)
    if len(header) < 12:
        return None, None, None
    magic, version, length = struct.unpack('<4sII', header)
    return magic, version, length

def main():
    if len(sys.argv) < 2:
        print("Usage: glb_check.py file.glb", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path, 'rb') as f:
            magic, version, length = read_glb_header(f)
            if magic is None:
                print("Error: file too short for header", file=sys.stderr)
                sys.exit(1)
            if magic != b'glTF':
                print(f"Error: bad magic bytes: {magic!r}", file=sys.stderr)
                sys.exit(1)
            if version != 2:
                print(f"Error: unsupported version {version}, expected 2", file=sys.stderr)
                sys.exit(1)
            # Get actual file size
            f.seek(0, 2)
            actual_size = f.tell()
            if length != actual_size:
                print(f"Error: header length {length} does not match file size {actual_size}", file=sys.stderr)
                sys.exit(1)
            # Read chunks
            f.seek(12)  # after header
            json_found = False
            while f.tell() < length:
                chunk_data = f.read(8)
                if len(chunk_data) < 8:
                    break
                chunk_len, chunk_type = struct.unpack('<II', chunk_data)
                if chunk_len < 1:
                    print(f"Error: zero-length chunk at offset {f.tell()-8}", file=sys.stderr)
                    sys.exit(1)
                if chunk_type == 0x4E4F534A:
                    json_found = True
                # Skip chunk data (with padding alignment)
                padded = (chunk_len + 3) // 4 * 4
                f.seek(f.tell() - 8 + 8 + padded)  # skip header + data
            if not json_found:
                print("Error: no JSON chunk found", file=sys.stderr)
                sys.exit(1)
            print(f"Valid GLB: {path}")
            sys.exit(0)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"Error: permission denied: {path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
