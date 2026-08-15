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

# [#528] leg 1 — the xdist flags are spelled out here rather than inherited. `-n auto` is
# already the `addopts` default (pyproject.toml, adopted 2026-08-06 on a measured 5.2x), so
# repeating it changes nothing today and keeps this call site checkable against the row's
# Done-when if that default ever moves. `--dist worksteal` replaces xdist's default `load`
# scheduler: the night-2 lane-latency measurement (8387ff2a §2b) attributes ~204 s of the
# 473 s parallel wall to two heavy files landing on one worker while the others drained
# early, and worksteal is the scheduler that rebalances a drained queue.
# `--max-worker-restart=0` is the gate-context flag: xdist's default restart budget is
# numprocesses x 4, so a crashed worker is silently replaced up to 4N times (night-2
# research 757077f2 §2.2 — the witnessed 19 strays sit inside that default). A gate that
# quietly restarts workers reports a verdict it did not earn; 0 turns that into a loud,
# bounded failure. PLAYBOOK Ch5 "Tiered suite" carries the doctrine.
rc, out = run(
    "uv run --locked pytest -n auto --dist worksteal --max-worker-restart=0 -x --tb=short"
)
results["pytest"] = ("PASS" if rc == 0 else "FAIL", out if rc != 0 else "")

rc, out = run("uv run --locked ruff check")
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
