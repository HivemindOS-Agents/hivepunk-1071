# GLB Structure Check Tool

A single-file Python tool to validate the structural integrity of a binary `.glb` (GLTF Binary) file. It reads only the 12-byte header and the JSON chunk — it does **not** parse the binary mesh data.

## Checks performed

1. **Magic bytes** — first 4 bytes must be `glTF` (binary `67 6C 54 46`).
2. **Declared length vs file size** — the 8–11 bytes (uint32) must equal the actual file length.
3. **Chunk layout** — the JSON chunk must appear first; chunk lengths must be aligned to 4 bytes.
4. **Required top-level glTF keys** — the JSON chunk must contain `asset.version` (a valid string).

## Usage

```bash
python3 glb_check.py <path-to-file.glb>
```

Exit code `0` if all checks pass, `1` otherwise. Progress and results printed to stdout.

### Examples

```bash
# Against a valid GLB:
python3 glb_check.py glb_check.py  # (no, this is Python code)
python3 glb_check.py sample/valid_minimal.glb

# Expected output:
# PASS: valid_minimal.glb: magic check passed (glTF)
# PASS: valid_minimal.glb: total length check passed (56 bytes)
# PASS: valid_minimal.glb: chunk layout check passed (JSON first, lengths aligned)
# PASS: valid_minimal.glb: required keys check passed (asset.version present)
# PASS: valid_minimal.glb: all checks passed
# exit code 0
```

```bash
# Against a file with bad magic:
python3 glb_check.py sample/bad_magic.glb

# Expected output:
# FAIL: bad_magic.glb: magic check failed (got b'NOTglTF')
# (and possibly other failures)
# exit code 1
```

## Sample files

`sample/valid_minimal.glb` — 56-byte valid GLB with a `{ "asset": { "version": "2.0" } }` JSON chunk.

`sample/bad_magic.glb` — starts with `NOTglTF` instead of `glTF`, all other bytes same as valid file.

## What is untested
- Chunks beyond the first two (JSON + BIN) — spec allows more, but checking multiple extra chunks is not implemented.
- Zero-length or empty chunks (unusual but spec-legal).
- Files with no BIN chunk (spec requires at least one JSON chunk, BIN is optional).
- Large files (>2 GB) — Python's `struct.unpack` works with uint32 up to 4 GB, but reading the whole file may hit memory limits.
- Files on network filesystems or from stdin.
- Files with extraneous trailing bytes after the last chunk.

## Self-test

```bash
cd tools/glb-structure-check && python3 self_test.py; echo exit=$?
```

The self-test calls `glb_check.py` on both sample files, verifies pass/fail counts match expected, and exits 0 only when all pass. Written output goes to `SELFTEST_OUTPUT.md`.
