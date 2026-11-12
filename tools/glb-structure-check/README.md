# glb-structure-check

Validates the binary structure of a GLB (glTF Binary) file.

## What it does

Reads a `.glb` file and checks:
- Magic bytes are `glTF` (correct for all glTF Binary files)
- Version field is 2
- File length in header matches actual file size
- At least one JSON chunk (type `0x4E4F534A`) is present
- Chunk lengths are positive integers

## Usage

```bash
python3 glb_check.py file.glb
```

Exit codes:
- **0**: valid
- **1**: invalid structure (bad magic, missing JSON, etc.)
- **2**: I/O error (file not found, permission, etc.)

## Self-test

Run from inside the tool folder:

```bash
cd tools/glb-structure-check && python3 self_test.py; echo exit=$?
```

This generates sample files (`make_samples.py`) if they are missing, then tests both a valid and an invalid GLB. Exits 0 only when both checks pass.

## Files

| File | Purpose |
|---|---|
| `glb_check.py` | Main tool |
| `self_test.py` | Offline self-test |
| `make_samples.py` | Generates binary sample files |
| `sample/valid_minimal.glb` | Pre-generated valid minimal GLB |
| `sample/bad_magic.glb` | Pre-generated invalid magic file |
| `README.md` | This file |

## Untested

- Only tests magic, version, file length, and JSON chunk presence. Does not validate JSON payload or BIN chunk.
- Does not check for multiple JSON chunks (spec allows one).
- Does not check that chunk data is properly aligned (padding is assumed).
- Generated samples use a minimal valid JSON; real-world files may have more complex structures.
- No network access; files must be local.
