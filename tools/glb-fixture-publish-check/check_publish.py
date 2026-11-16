#!/usr/bin/env python3
"""check_publish.py - offline pre-publish checker for GLB fixtures.
No network, no upload. Usage: python3 check_publish.py [folder]
Exit 0 pass, 1 fail, 2 usage error. Stdlib only.
"""
import csv, hashlib, json, sys
from pathlib import Path

EXPECTED_HEADER = ["case_id", "rule", "expected_bytes", "source", "read_back"]
ALIGNMENT = "(len+3) AND NOT 3"
EXPECTED_ROWS = 10

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def check_folder(root):
    root = Path(root)
    checks = []
    def add(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})
    csv_path = root / "data" / "data.csv"
    readme_path = root / "README.md"
    add("data/data.csv exists", csv_path.is_file())
    add("README.md exists", readme_path.is_file())
    files = {}
    if csv_path.is_file():
        b = csv_path.read_bytes()
        files["data/data.csv"] = {"bytes": len(b), "sha256_local_only": sha256_bytes(b), "lines": b.count(b"\n")}
    if readme_path.is_file():
        b = readme_path.read_bytes()
        files["README.md"] = {"bytes": len(b), "sha256_local_only": sha256_bytes(b), "lines": b.count(b"\n")}
    rows = []
    if csv_path.is_file():
        try:
            with csv_path.open(newline="", encoding="utf-8") as fh:
                reader = csv.reader(fh)
                header = next(reader, None)
                rows = list(reader)
            add("csv header matches", header == EXPECTED_HEADER, str(header))
        except Exception as exc:
            add("csv parses", False, str(exc))
        add("csv has 10 data rows", len(rows) == EXPECTED_ROWS, str(len(rows)))
        flat = "\n".join(",".join(r) for r in rows)
        add("alignment expression preserved as text", ALIGNMENT in flat)
    if readme_path.is_file():
        text = readme_path.read_text(encoding="utf-8", errors="replace")
        add("README mentions 10 rows", "10" in text)
        add("README mentions data/data.csv", "data/data.csv" in text)
        add("README mentions README.md", "README.md" in text)
        add("README states no dataset URL", "https://" not in text)
    passed = all(c["ok"] for c in checks) and len(checks) >= 8
    return {"folder": str(root), "passed": passed, "checks": checks, "files_local_only": files,
            "note": "hashes are local file hashes only, not published hashes; no live URL known"}

def main(argv):
    args = argv[1:]
    if len(args) > 1 or (args and args[0] in ("-h", "--help")):
        if args and args[0] in ("-h", "--help") and len(args) == 1:
            print(__doc__); return 0
        print("usage: python3 check_publish.py [folder]", file=sys.stderr); return 2
    result = check_folder(args[0] if args else ".")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
