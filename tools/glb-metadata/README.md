# glb-metadata

Read the binary header of any GLB (gLTF Binary) file and print:
- Magic bytes (the 4-byte `glTF` signature, shown as hex)
- Version (uint32, must be 2)
- Declared total length (uint32, must equal actual file size)
- Each chunk type and its length

## What is a GLB file?

A GLB file (Khronos gLTF Binary) starts with a 12-byte header:

~~~
offset 0:  uint32 magic      = 0x46546C67 ("glTF" in ASCII)
offset 4:  uint32 version    = 2 (for gLTF 2.0)
offset 8:  uint32 length     = total file size in bytes
~~~

After the header come zero or more chunks. Each chunk is:

~~~
offset 0:  uint32 chunkLength
offset 4:  uint32 chunkType     JSON chunk = 0x4E4F534A
                                 BIN  chunk = 0x004E4942
offset 8:  chunkLength bytes of data
~~~

## Usage

~~~bash
python3 glb_metadata.py path/to/model.glb
~~~

Stdlib only. No network, no subprocess.

Exit codes:
| code | meaning |
|---|---|
| 0 | file read and validated |
| 1 | file not found, unreadable, or structural error (bad magic, bad version, declared length mismatch) |

## Output example (valid file)

~~~
File: model.glb (24576 bytes)
magic: glTF (0x46546C67)
version: 2
declared length: 24576 (matches file size)
chunk 0: type=JSON (0x4E4F534A) length=2156
chunk 1: type=BIN  (0x004E4942) length=22416
~~~

## Output example (bad magic)

~~~
File: not_a_glb.bin (1024 bytes)
magic: 0xDEADBEAF (wrong magic)
~~~

## Self-test

~~~bash
cd tools/glb-metadata && python3 self_test.py
~~~

Builds tiny GLB fixture files in a temp directory using `struct.pack`, imports
`glb_metadata` from its own folder, opens each fixture as a real file and calls
`check_glb` on it. It asserts both the printed lines and the returned
True/False. No arguments, no network, no files outside a temp dir. Exits 0
only when every check passes.

The fixtures, and the invariant each one pins:

| fixture | real bytes | header declares | expected |
|---|---|---|---|
| valid | 24 | 24 | prints magic `glTF`, version 2, `type=JSON length=4`, and returns `True` |
| bad_magic | 12 | 12 (magic `0xDEADBEAF`) | prints `wrong magic` and returns `False` |
| mismatch | 24 | 20 | prints `does NOT match file size` and returns `False` |

The valid fixture is exactly 24 bytes: a 12-byte header, an 8-byte chunk header
(`chunkLength` 4, `chunkType` JSON) and a 4-byte chunk payload (`{}` plus two
padding NULs). The JSON payload is padded to a 4-byte boundary so no chunk
offset is fractional.

**Invariant to keep when editing this test:** the declared length in the header
must equal `12 + 8 + len(payload)` for however many chunks are written. A
hardcoded length that does not match the bytes actually written makes the
fixture contradict itself and the assertion fires before the tool is exercised.
The test computes the length from the payload rather than hardcoding it, and
`bad_magic` is asserted to be 12 bytes so it cannot drift silently.

## Untested

- **No run against a real GLB file from the web or from Blender.** All
  fixtures are synthetic.
- The tool does **not** validate the JSON content of the JSON chunk or check
  that the BIN chunk is referenced correctly. The fixtures' JSON payload is
  `{}` and is never parsed.
- No test for truncated chunks (file ends mid-chunk). The tool reads the
  chunk header but will fail with `struct.error` if the file is too short;
  that is an unhandled exception rather than a graceful message.
- No test for a file shorter than the 12-byte header.
- No test for `version != 2`, and no test for an unknown chunk type (the tool
  prints `unknown (0x...)` rather than failing).
- The tool expects the whole file to fit in memory; very large files may
  cause memory issues.

## Files

| file | what it is |
|---|---|
| `glb_metadata.py` | the tool (reads a GLB binary file, prints header info) |
| `self_test.py` | offline checks, run with no arguments |
| `README.md` | this file |
