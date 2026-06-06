"""Verify skill script — compact 3-line check cadence.

Runs pytest, ruff, and git-status. Prints PASS/FAIL per check.
Full output only on failure. Exits 1 if any check fails.
"""
import subprocess
import sys


def run(cmd):
    r = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode, r.stdout + r.stderr


results = {}

rc, out = run("pytest -x --tb=short")
results["pytest"] = ("PASS" if rc == 0 else "FAIL", out if rc != 0 else "")

rc, out = run("ruff check")
results["ruff"] = ("PASS" if rc == 0 else "FAIL", out if rc != 0 else "")

rc, out = run("git status --porcelain")
dirty = out.strip()
results["git"] = ("FAIL" if dirty else "PASS", dirty if dirty else "")

print(f"pytest : {results['pytest'][0]}")
print(f"ruff   : {results['ruff'][0]}")
print(f"git    : {results['git'][0]}")

if any(v[0] == "FAIL" for v in results.values()):
    print("\n--- Full output ---")
    for k, (status, detail) in results.items():
        if detail:
            print(f"\n[{k}]\n{detail}")
    sys.exit(1)
