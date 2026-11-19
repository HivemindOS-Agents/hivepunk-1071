#!/usr/bin/env python3
"""publish_manifest.py - describe the exact upload set for this artifact.

This tool does no network at all. It never uploads, never talks to Hugging
Face, and never writes a URL. It reads this folder as raw bytes and reports
the two entries that the platform's own publish play must upload:

    data/        -> data/      (the whole folder, same tree, same names)
    README.md    -> README.md  (the dataset card, byte for byte)

For each file it reports the byte count and the sha256 of the bytes it
actually read. Nothing else is added, renamed or invented. Values in the
manifest are a local read-back of this folder, never a read of a published
page, and must not be quoted as published values.

Usage:
    python3 publish_manifest.py            print the manifest
    python3 publish_manifest.py --write    write MANIFEST.txt
    python3 publish_manifest.py --check    compare disk with MANIFEST.txt

Exit 0 when the upload set is exactly the two entries above; 2 on a usage
error, on a traversal path, or (with --check) on any drift.

Stdlib only, no network, no subprocess.
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPLOAD_SET = (("data", "data"), ("README.md", "README.md"))
CHUNK = 1 << 16


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def _safe_child(root, rel):
    if rel.startswith("/") or ".." in Path(rel).parts:
        raise ValueError("refusing traversal path %r" % rel)
    return Path(root) / rel


def collect(root=None):
    root = Path(root) if root is not None else HERE
    entries = []
    for source, dest in UPLOAD_SET:
        path = _safe_child(root, source)
        if not path.exists():
            entries.append((source, dest, None, None))
            continue
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                rel = child.relative_to(path).as_posix()
                entries.append((source + "/" + rel, dest + "/" + rel, child.stat().st_size, sha256_file(child)))
        else:
            entries.append((source, dest, path.stat().st_size, sha256_file(path)))
    return entries


def manifest_text(entries):
    lines = [
        "# upload set for glb-fixture-byte-layouts",
        "# local read-back of this folder only; NOT a read of any published page",
        "# columns: bytes  sha256  source  ->  destination",
    ]
    for source, dest, size, digest in entries:
        if size is None:
            lines.append("MISSING  -  %s  ->  %s" % (source, dest))
        else:
            lines.append("%d  %s  %s  ->  %s" % (size, digest, source, dest))
    return "\n".join(lines) + "\n"


def check_two_entries(entries):
    if not entries:
        raise ValueError("upload set is empty")
    for source, dest, size, digest in entries:
        if size is None:
            raise ValueError("missing source %r" % source)
        if not (source.startswith("data/") or source == "README.md"):
            raise ValueError("entry outside the upload set: %r" % source)
        if source == "README.md" and dest != "README.md":
            raise ValueError("README.md must land as README.md")
        if source.startswith("data/") and dest != "data/" + source[len("data/"):]:
            raise ValueError("data/ tree must keep its names")
    if not any(s == "README.md" for s, _, _, _ in entries):
        raise ValueError("README.md is missing from the upload set")
    if not any(s.startswith("data/") for s, _, _, _ in entries):
        raise ValueError("data/ is missing from the upload set")
    return True


def write_manifest(root=None, target=None):
    root = Path(root) if root is not None else HERE
    target = Path(target) if target is not None else (root / "MANIFEST.txt")
    entries = collect(root)
    check_two_entries(entries)
    text = manifest_text(entries)
    Path(target).write_text(text, encoding="utf-8")
    return text


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    mode = "print"
    if argv:
        if len(argv) != 1 or argv[0] not in ("--write", "--check"):
            print("error: only --write or --check", file=sys.stderr)
            return 2
        mode = argv[0][2:]
    try:
        entries = collect(HERE)
        check_two_entries(entries)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    text = manifest_text(entries)
    if mode == "print":
        sys.stdout.write(text)
        return 0
    target = HERE / "MANIFEST.txt"
    if mode == "write":
        write_manifest(HERE, target)
        print("wrote %s" % target)
        return 0
    if not target.exists():
        print("error: MANIFEST.txt is missing", file=sys.stderr)
        return 2
    if target.read_text(encoding="utf-8") != text:
        print("error: upload set drifted from MANIFEST.txt", file=sys.stderr)
        return 2
    print("ok: upload set matches MANIFEST.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
