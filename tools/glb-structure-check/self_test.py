#!/usr/bin/env python3
"""self_test.py -- offline checks for glb-structure-check.

Run from inside the folder:
    cd tools/glb-structure-check && python3 self_test.py

It generates missing sample files via make_samples.py, then invokes glb_check.py
on both valid and invalid samples and expects correct exit codes. No arguments,
no network. Exits 0 only when every check passes.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"
MAKE_SAMPLES = HERE / "make_samples.py"
GLB_CHECK = HERE / "glb_check.py"
VALID_GLB = SAMPLE / "valid_minimal.glb"
BAD_MAGIC = SAMPLE / "bad_magic.glb"

def ensure_samples():
    """If sample files are missing, run make_samples.py to create them."""
    if not (SAMPLE.exists() and VALID_GLB.exists() and BAD_MAGIC.exists()):
        print("Generating missing sample files...")
        proc = subprocess.run(
            [sys.executable, str(MAKE_SAMPLES)],
            cwd=str(HERE),
            capture_output=True,
            text=True
        )
        if proc.returncode != 0:
            print(f"make_samples.py failed: {proc.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

CHECKS = 0
PASSES = 0

def test_valid():
    global CHECKS, PASSES
    CHECKS += 1
    print(f"Testing valid_minimal.glb...")
    proc = subprocess.run(
        [sys.executable, str(GLB_CHECK), str(VALID_GLB)],
        capture_output=True,
        text=True
    )
    if proc.returncode == 0:
        print("  PASS: valid_minimal.glb returned exit code 0")
        PASSES += 1
    else:
        print(f"  FAIL: valid_minimal.glb returned exit code {proc.returncode}, expected 0")
        print(f"  stdout: {proc.stdout.strip()}")
        print(f"  stderr: {proc.stderr.strip()}")

def test_bad_magic():
    global CHECKS, PASSES
    CHECKS += 1
    print(f"Testing bad_magic.glb...")
    proc = subprocess.run(
        [sys.executable, str(GLB_CHECK), str(BAD_MAGIC)],
        capture_output=True,
        text=True
    )
    # Expected exit code 1 (invalid file detected)
    if proc.returncode == 1:
        print("  PASS: bad_magic.glb reported magic failure")
        PASSES += 1
    else:
        print(f"  FAIL: bad_magic.glb returned exit code {proc.returncode}, expected 1")
        print(f"  stdout: {proc.stdout.strip()}")
        print(f"  stderr: {proc.stderr.strip()}")

def main():
    ensure_samples()
    test_valid()
    test_bad_magic()
    print(f"\nResults: {PASSES}/{CHECKS} checks passed")
    if PASSES == CHECKS:
        print("All self-tests passed.")
        sys.exit(0)
    else:
        print("Some self-tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
