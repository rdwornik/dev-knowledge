"""Measure the start-up token cost of one `claude -p` call in a clean repo.

A dirty tree makes the Stop hook continue the turn, so a dirty-tree sum is not a
start-up cost ([#1705]); the probe refuses to run on one.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROLE = "seat-orchestrator"  # the model a lane-head seat runs on
TIMEOUT_S = 180
_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def default_model():
    try:
        from scripts import provider_registry
    except ImportError:
        import provider_registry
    return provider_registry.anthropic_role_model(ROLE)


def dirty_files(repo):
    r = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln[3:].strip().strip('"') for ln in r.stdout.splitlines() if ln.strip()]


def _total(usage):
    return sum(usage.get(k, 0) for k in _KEYS)


def calls_from_usage(usage):
    iterations = usage.get("iterations")
    if not iterations:
        raise ValueError("usage has no iterations")
    return round(_total(usage) / _total(iterations[0]))


def run_claude(repo, model):
    exe = shutil.which("claude") or "claude"
    r = subprocess.run(
        [exe, "-p", "Reply with OK.", "--output-format", "json", "--model", model],
        cwd=repo,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_S,
        check=True,
    )
    return r.stdout


def main(argv, runner=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--model", default=None)
    args = ap.parse_args(argv)
    repo = Path(args.repo)

    dirty = dirty_files(repo)
    if dirty:
        print("refusing dirty tree: " + ", ".join(dirty), file=sys.stderr)
        return 2

    usage = json.loads((runner or run_claude)(repo, args.model or default_model()))["usage"]
    calls = calls_from_usage(usage)
    print(f"calls={calls} tokens={_total(usage)}")
    return 0 if calls <= 1 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
