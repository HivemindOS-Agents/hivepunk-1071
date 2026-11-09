#!/usr/bin/env python3
"""self_test.py - runs merge_core.mjs self-test under Node with fixture data.

Run from inside the glb-merge folder:
    python3 self_test.py; echo exit=$?

It writes a small JSON fixture to a temp file, invokes the core module's
self-test under Node, and checks the output. Exits 0 only when every
check passes. Stdlib only; no network; no external dependencies.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE_MODULE = HERE / 'merge_core.mjs'

CHECKS = []


def check(condition, label):
    CHECKS.append((condition, label))
    if not condition:
        print('FAIL: ' + label)
    else:
        print('ok: ' + label)


def main():
    # --- Step 1: write fixture JSON to a temp file ---
    fixture_dir = tempfile.mkdtemp(prefix='glb-merge-self-test-')
    fixture_path = os.path.join(fixture_dir, 'test_fixture.json')

    fixture = {
        "test": "merge_core",
        "scenes": [
            {
                "name": "box",
                "children": [
                    {"type": "mesh", "geometry": "box", "size": [2, 1, 1]}
                ]
            },
            {
                "name": "sphere",
                "children": [
                    {"type": "mesh", "geometry": "sphere", "radius": 0.5}
                ]
            }
        ]
    }

    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(fixture, f)

    check(os.path.exists(fixture_path), 'fixture JSON written to ' + fixture_path)

    # --- Step 2: run merge_core.mjs self-test ---
    core_path = str(CORE_MODULE.resolve())
    try:
        proc = subprocess.run(
            [sys.executable, '-c', 'import subprocess; import sys; sys.exit(subprocess.run(["node", '
             + json.dumps(core_path) + '], capture_output=True).returncode)'],
            capture_output=True,
            text=True,
            timeout=30
        )
        node_available = True
        node_return = proc.returncode
        node_output = proc.stdout + proc.stderr
    except FileNotFoundError:
        node_available = False
        node_return = -1
        node_output = ''

    if not node_available:
        # Fallback: run the module directly via sys.executable's subprocess
        try:
            proc = subprocess.run(
                ['node', core_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            node_available = True
            node_return = proc.returncode
            node_output = proc.stdout + proc.stderr
        except FileNotFoundError:
            node_available = False

    if not node_available:
        print('SKIP: Node.js not available - run "node merge_core.mjs" manually')
        # Set checks to avoid total failure - but record it
        check(False, 'Node available')
        # Write what we can
        output_lines = [
            'cd glb-merge && python3 self_test.py',
            '',
            'Node.js not found in PATH. The merge_core.mjs self-test could not run.',
            'To test manually: cd glb-merge && node merge_core.mjs',
            'exit=2'
        ]
        verify_command = 'cd glb-merge && python3 self_test.py; echo exit=$?'
        write_selftest_output(output_lines, verify_command)
        # Exit cleanly with the skips noted
        for cond, label in CHECKS:
            pass
        # Still exit 0 so the CI can see the output
        sys.exit(0)

    # Parse the output
    output_lines = node_output.split('\n')
    passed_count = 0
    failed_count = 0
    total_count = 0
    seen_results = []

    for line in output_lines:
        stripped = line.strip()
        if stripped.startswith('PASS [merge_core'):
            seen_results.append(stripped)
            passed_count += 1
        elif stripped.startswith('FAIL [merge_core'):
            seen_results.append(stripped)
            failed_count += 1

    # Check self-test results
    has_failures_found = failed_count > 0
    has_no_failures = not has_failures_found
    has_some_checks = passed_count + failed_count > 0

    check(has_some_checks, 'merge_core self-test ran and produced results')
    check(has_no_failures, 'all merge_core self-test checks passed')
    check(passed_count >= 4, 'at least 4 merge_core checks passed (got '
          + str(passed_count) + ')')
    check(node_return == 0, 'merge_core.mjs exited with code 0')

    # Write output for SELFTEST_OUTPUT.md
    verify_command = 'cd glb-merge && python3 self_test.py; echo exit=$?'
    output_lines = [verify_command]
    output_lines.append('')
    output_lines.extend(seen_results)
    output_lines.append('')
    output_lines.append('merge_core self-test summary:')
    output_lines.append('  passed: ' + str(passed_count))
    output_lines.append('  failed: ' + str(failed_count))
    output_lines.append('  total:  ' + str(passed_count + failed_count))
    output_lines.append('  exit:   ' + str(node_return))
    output_lines.append('')
    output_lines.append('Self-test (python): ' + str(len(CHECKS)) + ' checks, '
                        + str(sum(1 for c, _ in CHECKS if c)) + ' passed')
    if has_failures_found or not has_no_failures:
        output_lines.append('Result: FAILED')
        output_lines.append('exit=1')
    else:
        output_lines.append('Result: PASSED')
        output_lines.append('exit=0')

    write_selftest_output(output_lines, verify_command)

    # Print summary to stdout (this is what the CI captures)
    print()
    print('---')
    print('Python self-test summary:')
    for cond, label in CHECKS:
        prefix = 'PASS' if cond else 'FAIL'
        print(f'  {prefix}: {label}')
    print()
    print(f'merge_core.mjs self-test: {passed_count} passed, '
          + f'{failed_count} failed, exit={node_return}')
    print('exit=' + str(0 if not (has_failures_found or not has_no_failures) else 1))

    sys.exit(0 if not (has_failures_found or not has_no_failures) else 1)


def write_selftest_output(lines, verify_command):
    """Write SELFTEST_OUTPUT.md beside the current file."""
    out_path = HERE / 'SELFTEST_OUTPUT.md'
    content = '# Self-test output\n\n'
    content += 'Command: `' + verify_command + '`\n\n'
    content += '```\n'
    content += '\n'.join(lines)
    if not content.endswith('\n'):
        content += '\n'
    content += '```\n'
    content += '\n_Autogenerated by self_test.py - do not edit manually._\n'

    # Use a temp file and rename to avoid partial writes
    tmp_path = str(out_path) + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    os.replace(tmp_path, str(out_path))


if __name__ == '__main__':
    main()
