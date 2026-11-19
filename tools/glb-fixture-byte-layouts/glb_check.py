#!/usr/bin/env python3
"""glb_check.py - standalone GLB header/chunk checker and case builder.
Stdlib only, no network. GLB layout checked: 12-byte header (magic
0x46546C67, version 2, total length == file size), then chunks with
8-byte headers; JSON chunk (0x4E4F534A) first, optional BIN chunk
(0x004E4942) second, each chunk length a multiple of 4, JSON padded
with 0x20 spaces, BIN padded with 0x00 to 4-byte alignment.
Usage: python3 glb_check.py data/data.csv
"""
import csv, json, struct, sys
from pathlib import Path
MAGIC = 0x46546C67
JSON_TYPE = 0x4E4F534A
BIN_TYPE = 0x004E4942
DEFECTS = {"none","bad-magic","bad-version","bad-total-length","chunk-order","json-bad-padding","bin-unpadded"}
def _pad(data, byte):
    return data + byte * ((-len(data)) % 4)
def _chunk(ctype, data):
    return struct.pack("<II", len(data), ctype) + data
def build_glb(json_text, bin_bytes=None, defect="none"):
    if defect not in DEFECTS:
        raise ValueError("unknown defect %r" % defect)
    raw = json_text.encode("utf-8")
    json_data = _pad(raw, b"\x00" if defect == "json-bad-padding" else b" ")
    json_chunk = _chunk(JSON_TYPE, json_data)
    bin_chunk = b""
    if bin_bytes is not None:
        data = bytes(bin_bytes) if defect == "bin-unpadded" else _pad(bytes(bin_bytes), b"\x00")
        bin_chunk = _chunk(BIN_TYPE, data)
    body = (bin_chunk + json_chunk) if defect == "chunk-order" else (json_chunk + bin_chunk)
    magic = 0x0BADF00D if defect == "bad-magic" else MAGIC
    version = 1 if defect == "bad-version" else 2
    total = 12 + len(body) + (4 if defect == "bad-total-length" else 0)
    return struct.pack("<III", magic, version, total) + body
def check_glb(data):
    errors = []
    if len(data) < 12:
        return False, ["file shorter than 12-byte header"]
    magic, version, total = struct.unpack("<III", data[:12])
    if magic != MAGIC:
        errors.append("bad magic 0x%08X" % magic)
    if version != 2:
        errors.append("bad version %d" % version)
    if total != len(data):
        errors.append("bad total length %d != file size %d" % (total, len(data)))
    pos, seen = 12, []
    while pos < len(data):
        if pos + 8 > len(data):
            errors.append("truncated chunk header at %d" % pos); break
        clen, ctype = struct.unpack("<II", data[pos:pos+8])
        if clen % 4:
            errors.append("chunk at %d length %d not 4-byte aligned" % (pos, clen))
        if pos + 8 + clen > len(data):
            errors.append("chunk at %d overruns file" % pos); break
        seen.append(ctype)
        payload = data[pos+8:pos+8+clen]
        if ctype == JSON_TYPE:
            stripped = payload.rstrip(b" ")
            pad = payload[len(stripped):]
            if any(b != 0x20 for b in pad):
                errors.append("JSON padding is not 0x20")
            try:
                json.loads(stripped.decode("utf-8"))
            except Exception:
                errors.append("JSON chunk does not parse after 0x20 padding")
        pos += 8 + clen
    if pos != len(data):
        errors.append("trailing bytes after last chunk")
    if not seen or seen[0] != JSON_TYPE:
        errors.append("first chunk is not JSON (chunk order)")
    if len(seen) > 2 or (len(seen) == 2 and seen[1] != BIN_TYPE):
        errors.append("unexpected chunk types %r" % (seen,))
    return (not errors), errors
def row_to_bytes(row):
    bin_bytes = bytes.fromhex(row["bin_hex"]) if row["bin_hex"].strip() else None
    return build_glb(row["json_text"], bin_bytes, row["defect"])
def load_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return reader.fieldnames, rows
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    path = Path(argv[0]) if argv else Path(__file__).resolve().parent / "data" / "data.csv"
    _, rows = load_rows(path)
    bad = 0
    for row in rows:
        ok, errs = check_glb(row_to_bytes(row))
        want = row["expected"] == "valid"
        status = "ok" if ok == want else "MISMATCH"
        if ok != want: bad += 1
        print("%s: %s expected=%s got=%s %s" % (status, row["case_id"], row["expected"], "valid" if ok else "invalid", "; ".join(errs)))
    print("rows: %d mismatches: %d" % (len(rows), bad))
    return 1 if bad else 0
if __name__ == "__main__":
    sys.exit(main())
