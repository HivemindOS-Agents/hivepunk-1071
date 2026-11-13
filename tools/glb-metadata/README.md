# glb-metadata

Read the binary header of any GLB (gLTF Binary) file and print:
- Magic bytes (the 4-byte `glTF` signature, shown as hex)
- Version (uint32, must be 2)
- Declared total length (uint32, must equal actual file size)
- Each chunk type and its length

## What is a GLB file?

A GLB file (Khronos gLTF Binary) starts with a 12-byte header:

```
offset 0:  uint32 magic      = 0x46546C67 ("glTF" in ASCII)
offset 4:  uint32 version    = 2 (for gLTF 2.0)
offset 8:  uint32 length     = total file size in bytes
```

After the header come zero or more chunks. Each chunk is:

```
offset 0:  uint32 chunkLength
offset 4:  uint32 chunkType     JSON chunk = 0x4E4F534A
                                 BIN  chunk = 0x004E4942
offset 8:  chunkLength bytes of data
```

## Usage

```bash
python3 glb_metadata.py path/to/model.glb
```

Stdlib only. No network, no subprocess.

Exit codes:
| code | meaning |
|---|---|
| 0 | file read and validated |
| 1 | file not found, unreadable, or structural error (bad magic, bad version, declared length mismatch) |

## Output example (valid file)

```
File: model.glb (24576 bytes)
magic: glTF (0x46546C67)
version: 2
declared length: 24576 (matches file size)
chunk 0: type=JSON (0x4E4F534A) length=2156
chunk 1: type=BIN  (0x004E4942) length=22416
```

## Output example (bad magic)

```
File: not_a_glb.bin (1024 bytes)
magic: 0xDEADBEAF (wrong magic)
```

## Self-test

```bash
cd tools/glb-metadata && python3 self_test.py
```

Builds two GLB fixture files in a temp directory using `struct.pack`, imports
`glb_metadata` from its own folder, and calls `check_glb` on each. Checks that:
- valid magic, version 2, and chunk types are printed.
- a file with bad magic causes the tool to report it.

No arguments, no network, no files outside the folder. Exits 0 only when
every check passes.

## Untested

- **No run against a real GLB file from the web or from Blender.** All
  fixtures are synthetic.
- The tool does **not** validate the JSON content of the JSON chunk or check
  that the BIN chunk is referenced correctly.
- No test for truncated chunks (file ends mid-chunk). The tool reads the
  chunk header but will fail with `struct.error` if the file is too short;
  that is an unhandled exception rather than a graceful message.
- The tool expects the whole file to fit in memory.
- Extremely large files (multiple gigabytes) may cause memory issues.

## Files

| file | what it is |
|---|---|
| `glb_metadata.py` | the tool (reads a GLB binary file, prints header info) |
| `self_test.py` | offline checks, run with no arguments |
| `README.md` | this file |
