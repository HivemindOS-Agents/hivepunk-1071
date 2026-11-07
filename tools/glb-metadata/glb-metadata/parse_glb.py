#!/usr/bin/env python3
"""parse_glb.py – a tiny stdlib‑only parser for .glb files.

The script reads a GLB binary, extracts the JSON chunk, and prints a small JSON
summary containing:

* asset_version – the glTF asset version string
* asset_generator – the optional generator string
* asset_extras – any extras object present under "asset"
* scene_count – number of scene objects
* node_count – number of node objects
* mesh_count – number of mesh objects
* material_count – number of material objects
* mesh_names – list of mesh name strings
* material_names – list of material name strings

Usage
-----

```
# read a GLB file and write the summary to summary.json
python3 parse_glb.py example.glb -o summary.json

# write the summary to stdout
python3 parse_glb.py example.glb -o -
```

The default output format is compact JSON. The `-o -` option prints to standard output.

The implementation walks the GLB binary by hand: it looks for a chunk whose
type is `JSON` (0x4E4F534A) and parses that payload with the standard library
`json` module. No external dependencies are used.

The parser deliberately ignores any binary chunk or other GLB extensions.
It only guarantees the minimal structure required by the spec.

The functions below are useful if you want to import the logic in another
module.
"""

from __future__ import annotations

import json
import os
import struct
import sys
from pathlib import Path

# Chunk type constants (little‑endian 4‑byte words)
CHUNK_TYPE_JSON = 0x4E4F534A  # "JSON"
CHUNK_TYPE_BIN  = 0x004E4F53  # "BIN" (unused in this simple tool)


#------------
# Core logic
#------------

def _read_glb_header(f: os.PathLike | str) -> tuple[int, int, int]:
    """Read the GLB header and return (magic, version, total_length)."""
    with open(f, "rb") as h:
        data = h.read(12)
    if len(data) != 12:
        raise ValueError("GLB header too short")
    magic, version, total_len = struct.unpack("<III", data)
    if magic != 0x46546C67:  # "glTF"
        raise ValueError("Not a GLB file – missing magic stamp")
    return magic, version, total_len


def _find_json_chunk(f: os.PathLike | str) -> bytes:
    """Return the payload of the first JSON chunk.

    Raises ValueError if no JSON chunk is found.
    """
    with open(f, "rb") as h:
        # Skip header
        h.seek(12)
        while True:
            header = h.read(8)
            if len(header) < 8:
                break
            chunk_len, chunk_type = struct.unpack("<II", header)
            payload = h.read(chunk_len)
            if len(payload) < chunk_len:
                raise ValueError("Chunk truncated")
            if chunk_type == CHUNK_TYPE_JSON:
                return payload
    raise ValueError("No JSON chunk found")


def _parse_json_payload(payload: bytes) -> dict:
    """Parse JSON payload and return the decoded dict."""
    return json.loads(payload.decode("utf‑8"))


def _collect_metrics(gltf: dict) -> dict:
    """Given the top‑level GLTF dict compute the small summary dict."""
    asset = gltf.get("asset", {})
    scenes = gltf.get("scenes", [])
    nodes = gltf.get("nodes", [])
    meshes = gltf.get("meshes", [])
    mats = gltf.get("materials", [])

    return {
        "asset_version": asset.get("version", ""),
        "asset_generator": asset.get("generator", ""),
        "asset_extras": asset.get("extras", {}),
        "scene_count": len(scenes),
        "node_count": len(nodes),
        "mesh_count": len(meshes),
        "material_count": len(mats),
        "mesh_names": [m.get("name", "") for m in meshes],
        "material_names": [m.get("name", "") for m in mats],
    }


def parse_glb_file(path: os.PathLike | str) -> dict:
    """Return the summary dictionary for the GLB file at *path*.

    This function does all the heavy lifting and is useful when importing
    the module into another script.
    """
    json_payload = _find_json_chunk(path)
    gltf = _parse_json_payload(json_payload)
    return _collect_metrics(gltf)


#------------
# CLI wrapper
#------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    import argparse
    p = argparse.ArgumentParser(description="Extract simple metadata from a glTF2 GLB file")
    p.add_argument("input", help="Path to the .glb file to read")
    p.add_argument("-o", "--out", default=None,
                    help="Output JSON file; use '-' for stdout (default writes to %(default)s)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        summary = parse_glb_file(args.input)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json_data = json.dumps(summary, indent=2, sort_keys=True)
    output_path = args.out
    if output_path in (None, ""):
        output_path = "summary.json"
    if output_path == "-":
        print(json_data)
        return 0
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_data)
    except Exception as exc:
        print(f"error: could not write {output_path}: {exc}", file=sys.stderr)
        return 2
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

