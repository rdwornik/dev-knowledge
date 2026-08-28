"""Verify skill script -- compact 3-line check cadence with an ACTIONABLE failure block.

Runs pytest, ruff, and git-status. Success is exactly three lines. Failure adds a
structured file / expected / received / directive block per failing check, and exits
with a semantic bitmask code so an iterate-until-green loop can tell WHICH check is
still red without re-parsing prose ([#127]; refs #104, #126).

Exit codes ([#127] enrichment -- machine-distinguishable, composable):

    0   everything passed
    2   pytest failed          (EXIT_PYTEST)
    4   ruff failed            (EXIT_RUFF)
    8   git working tree dirty (EXIT_GIT)

A bitmask rather than a first-failure code, deliberately: a loop that sees 6 knows
pytest AND ruff are red, and a loop that sees the SAME code twice in a row knows it
made no progress -- which is the anti-retry-loop signal the row asks for. A
first-failure code cannot express either.
"""
import re
import subprocess
import sys

EXIT_PYTEST = 2
EXIT_RUFF = 4
EXIT_GIT = 8


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


# --- failure-block extraction (pure; tested without running the real tools) ----

_PYTEST_LOC = re.compile(r"^(?:FAILED|ERROR)\s+([^\s:]+\.py)(?:::(\S+))?", re.M)
_PYTEST_FILE_LINE = re.compile(r"^([^\s:]+\.py):(\d+):", re.M)
_PYTEST_ASSERT = re.compile(r"^E\s+(.+)$", re.M)
_RUFF_VIOLATION = re.compile(r"^(\S+?):(\d+):(\d+):\s+(\S+)\s+(.*)$", re.M)


def _first(pattern, text, default=""):
    m = pattern.search(text)
    return m if m else default


def pytest_failure(out: str) -> dict:
    """file / expected / received / directive for a pytest failure."""
    loc = _PYTEST_LOC.search(out)
    if loc:
        where = loc.group(1) + (f"::{loc.group(2)}" if loc.group(2) else "")
    else:
        fl = _PYTEST_FILE_LINE.search(out)
        where = f"{fl.group(1)}:{fl.group(2)}" if fl else "(unattributed - see full output)"
    assertion = _PYTEST_ASSERT.search(out)
    received = assertion.group(1).strip() if assertion else "non-zero exit; no assertion line parsed"
    return {
        "file": where,
        "expected": "exit 0 - every test passes",
        "received": received,
        "directive": ("fix the failing test or the code under it, then re-run this skill; "
                      "do NOT proceed to the next step"),
    }


def ruff_failure(out: str) -> dict:
    """file / expected / received / directive for a ruff failure."""
    v = _RUFF_VIOLATION.search(out)
    if v:
        where = f"{v.group(1)}:{v.group(2)}:{v.group(3)}"
        received = f"{v.group(4)} {v.group(5).strip()}"
    else:
        where = "(unattributed - see full output)"
        received = "ruff exited non-zero; no violation line parsed"
    return {
        "file": where,
        "expected": "no lint violations",
        "received": received,
        "directive": "run `uv run --locked ruff check --fix`, then re-run this skill",
    }


def git_failure(dirty: str) -> dict:
    """file / expected / received / directive for a dirty working tree."""
    paths = [ln[3:].strip() for ln in dirty.splitlines() if len(ln) > 3]
    head = paths[0] if paths else "(unattributed)"
    more = f" (+{len(paths) - 1} more)" if len(paths) > 1 else ""
    return {
        "file": head + more,
        "expected": "clean working tree",
        "received": f"{len(paths)} uncommitted path(s)",
        "directive": "commit the intended changes (or stash the rest), then re-run this skill",
    }


def render_block(name: str, fields: dict) -> str:
    """The actionable block, one shape for every check ([#127] Done-when)."""
    return (f"[{name}]\n"
            f"  file      : {fields['file']}\n"
            f"  expected  : {fields['expected']}\n"
            f"  received  : {fields['received']}\n"
            f"  directive : {fields['directive']}")


def exit_code(failed: list) -> int:
    """Bitmask of the failing checks; 0 when everything passed."""
    bits = {"pytest": EXIT_PYTEST, "ruff": EXIT_RUFF, "git": EXIT_GIT}
    return sum(bits[n] for n in failed)


def main() -> int:
    results = {}
    blocks = {}

    # [#528] leg 1 -- the xdist flags are spelled out here rather than inherited. `-n auto` is
    # already the `addopts` default (pyproject.toml, adopted 2026-08-06 on a measured 5.2x), so
    # repeating it changes nothing today and keeps this call site checkable against the row's
    # Done-when if that default ever moves. `--dist worksteal` replaces xdist's default `load`
    # scheduler: the night-2 lane-latency measurement
    # (docs/audits/2026-08-14-technical-night2-latency.md §2b) attributes ~204 s of the 473 s
    # parallel wall to two heavy files landing on one worker while the others drained early, and
    # worksteal is the scheduler that rebalances a drained queue. `--max-worker-restart=0` is the
    # gate-context flag: xdist's default restart budget is numprocesses x 4, so a crashed worker
    # is silently replaced up to 4N times (night-2 research
    # docs/audits/2026-08-14-technical-night2-research.md §2.2 -- the witnessed 19 strays sit
    # inside that default). A gate that quietly restarts workers reports a verdict it did not
    # earn; 0 turns that into a loud, bounded failure. PLAYBOOK Ch5 "Tiered suite" carries the
    # doctrine.
    rc, out = run(
        "uv run --locked pytest -n auto --dist worksteal --max-worker-restart=0 -x --tb=short"
    )
    results["pytest"] = "PASS" if rc == 0 else "FAIL"
    if rc != 0:
        blocks["pytest"] = (pytest_failure(out), out)

    rc, out = run("uv run --locked ruff check")
    results["ruff"] = "PASS" if rc == 0 else "FAIL"
    if rc != 0:
        blocks["ruff"] = (ruff_failure(out), out)

    rc, out = run("git status --porcelain")
    dirty = out.strip()
    results["git"] = "FAIL" if dirty else "PASS"
    if dirty:
        blocks["git"] = (git_failure(dirty), dirty)

    # Success stays EXACTLY three lines ([#127] Done-when, second half).
    print(f"pytest : {results['pytest']}")
    print(f"ruff   : {results['ruff']}")
    print(f"git    : {results['git']}")

    if not blocks:
        return 0

    failed = [n for n in ("pytest", "ruff", "git") if results[n] == "FAIL"]
    code = exit_code(failed)
    print("\n--- Actionable ---")
    for name in failed:
        print(render_block(name, blocks[name][0]))
    print(f"\nexit {code} = " + " + ".join(f"{n}({exit_code([n])})" for n in failed))
    print("\n--- Full output ---")
    for name in failed:
        print(f"\n[{name}]\n{blocks[name][1]}")
    return code


if __name__ == "__main__":
    sys.exit(main())
