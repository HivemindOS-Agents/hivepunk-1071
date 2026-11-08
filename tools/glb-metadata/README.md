# GLB Metadata Tool

This repository contains a tiny stdlib-only script that reads a GLB file and prints
a simple JSON summary of key metadata such as asset version, generator, and
counts of scenes, nodes, meshes, and materials.

## Usage

```bash
python3 parse_glb.py <input.glb> -o summary.json
```

If you prefer to write directly to stdout:

```bash
python3 parse_glb.py <input.glb> -o -
```

## Self‑test

The self‑test simply attempts to run `self_test.py` (which is not present in
this repo).  The output of that attempt is recorded in
`SELFTEST_RUN.txt`.

```bash
cd tools/glb-metadata && python3 self_test.py; echo exit=$?
```

See `SELFTEST_RUN.txt` for the actual test run output.
