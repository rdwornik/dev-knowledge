#!/usr/bin/env python
"""ship_gate_diff.py -- ONE comparator for "what hard-fails/undispositioned WARNs did this
branch introduce vs a baseline" (DECLARE-WINDOW-DEFECTS-2026-09-23 D11).

THE FALSE NEGATIVE THIS CLOSES. `SESSION-integrator-wave4b-2026-09-22.md`, 22:15Z-22:24Z: the
handback organ's own ship-gate leg reported "RED against origin/main too ... none introduced by
this branch", while the integrator's own side-by-side diff, computed separately, found
"hard-fail organs 0 -> 1: + organ_truth: ... scripts/handback.py -- INTRODUCED by this merge".
Root cause: the organ's leg diffed by `Finding.check_name` ALONE --

    {f.check_name for f in findings if f.status == "fail"
     or (f.status == "warn" and undispositioned)}

`check_organ_truth` (and any check like it) emits MULTIPLE findings under the SAME check_name
for different legs -- a `warn` naming dated `manual_until` debt already on `origin/main`, and a
SEPARATE `fail` naming a brand-new unfated organ the lane's own merge introduced. Because both
sat under the one string `"organ_truth"`, `head_names - base_names` read EMPTY: the check_name
was already "in" the baseline set (via the pre-existing warn), so the new fail's arrival was
invisible to a set built only from names.

THE FIX: diff by the PAIR `(check_name, status)`, not the bare name. A `(check_name, status)`
head carries that the baseline does not is introduced, whatever OTHER status of the same
check_name already sat on the baseline. This is coarse enough to ignore evidence-text-only
drift under an status that already existed (a WARN's row count moving, a staleness counter
advancing a day is the SAME failure mode restated with a new number, not a new one) and fine
enough to catch a check that gains a NEW status it did not carry before -- which is a new
failure mode wearing an old check's name, exactly the wave-4B instance.

ONE COMPARATOR, TWO CALLERS (D11's own mechanism, "the organ and the integrator call one
comparator"): `scripts/handback.py`'s `ship-gate` self-check leg imports `blocking_at_head` /
`blocking_at_ref` from here instead of computing its own set, and the integrator (or anyone
doing the same check by hand, the way the wave-4B receipts describe doing it "line by line")
runs `python scripts/ship_gate_diff.py diff [--base origin/main]` for the identical
computation -- one implementation, never two that can silently disagree again.

LIBRARY-FIRST: `audit.run_checks`, `audit._load_dispositions` and `audit._match_disposition`
compute the findings and the disposition register exactly as `audit.py ship-gate` does; this
module holds no second copy of either, only the `(check_name, status)` comparator and the
worktree-baseline plumbing needed to run that computation against a ref other than the working
tree.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

DEFAULT_BASE = "origin/main"
TIMEOUT_S = 1800
_ROOT = Path(__file__).resolve().parents[1]

#: `(check_name, status)` -- the identity a Finding is compared by. See the module docstring
#: for why the pair, not the bare `check_name`, is what makes this comparator correct.
Identity = tuple[str, str]


def _run(argv: list[str], cwd: Path, timeout: Optional[float] = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, f"could not start {argv[0] if argv else '<empty>'}: {exc!r}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def findings_at_head(repo: Path) -> list:
    """Every `Finding` `audit.py ship-gate` would print for `repo`'s CURRENT working tree --
    called exactly as `audit.cmd_ship_gate` computes them, so this can never drift from what
    `audit.py ship-gate` itself would report."""
    import audit  # noqa: PLC0415 -- heavy; only a CLI/organ path pays for it
    return audit.run_checks(Path(repo))


def blocking_identities(findings, dispositions) -> frozenset:
    """The `(check_name, status)` pairs that would RED `audit.py ship-gate`: every FAIL, and
    every undispositioned WARN. `dispositions` is `audit._load_dispositions()`'s own return."""
    import audit  # noqa: PLC0415
    out: set[Identity] = set()
    for f in findings:
        if f.status == "fail":
            out.add((f.check_name, f.status))
        elif f.status == "warn" and audit._match_disposition(f, dispositions) is None:
            out.add((f.check_name, f.status))
    return frozenset(out)


def blocking_at_head(repo: Path) -> frozenset:
    """`blocking_identities` over `repo`'s current working tree."""
    import audit  # noqa: PLC0415
    findings = findings_at_head(repo)
    dispositions = audit._load_dispositions()
    return blocking_identities(findings, dispositions)


#: The script run inside a detached baseline worktree -- a separate interpreter, so it reads
#: THAT tree's `audit.py`, never the caller's already-imported copy.
_BASELINE_SCRIPT = (
    "import sys, json\n"
    "sys.path.insert(0, 'scripts')\n"
    "import audit\n"
    "from pathlib import Path\n"
    "findings = audit.run_checks(Path('.'))\n"
    "disp = audit._load_dispositions()\n"
    "out = set()\n"
    "for f in findings:\n"
    "    if f.status == 'fail':\n"
    "        out.add((f.check_name, f.status))\n"
    "    elif f.status == 'warn' and audit._match_disposition(f, disp) is None:\n"
    "        out.add((f.check_name, f.status))\n"
    "print(json.dumps(sorted(out)))\n"
)


def blocking_at_ref(repo: Path, ref: str,
                    runner: Callable[..., tuple[int, str]] = _run) -> frozenset:
    """`blocking_identities`, computed against `ref` in a disposable detached worktree -- so a
    finding already present at `ref` is a baseline fact, not this branch's introduction. Shares
    the calling interpreter's already-loaded dependencies (`sys.executable`); only `audit.py`'s
    CONTENT at `ref` differs, so no `uv sync` is needed in the throwaway tree."""
    with tempfile.TemporaryDirectory(prefix="ship-gate-diff-baseline-") as tmp:
        worktree = Path(tmp) / "wt"
        code, out = runner(
            ["git", "-C", str(repo), "worktree", "add", "--detach", str(worktree), ref], repo)
        if code != 0:
            raise RuntimeError(f"could not create a baseline worktree at {ref}: {out.strip()[-500:]}")
        try:
            proc_code, proc_out = runner([sys.executable, "-c", _BASELINE_SCRIPT], worktree,
                                         TIMEOUT_S)
            if proc_code != 0:
                raise RuntimeError(f"baseline ship-gate at {ref} could not run: "
                                  f"{proc_out.strip()[-2000:]}")
            line = [ln for ln in proc_out.splitlines() if ln.strip()][-1]
            return frozenset(tuple(pair) for pair in json.loads(line))
        finally:
            runner(["git", "-C", str(repo), "worktree", "remove", "--force", str(worktree)], repo)


def diff(repo: Path, base: str = DEFAULT_BASE,
         head: Optional[frozenset] = None,
         base_ids: Optional[frozenset] = None) -> tuple[frozenset, frozenset]:
    """`(introduced, resolved)` -- what HEAD adds vs `base` that it did not carry, and what
    `base` carried that HEAD no longer does. `head`/`base_ids` are seams for a caller that has
    already computed one side (tests; a caller re-using a `base` run across several heads)."""
    head_ids = blocking_at_head(repo) if head is None else head
    baseline = blocking_at_ref(repo, base) if base_ids is None else base_ids
    return head_ids - baseline, baseline - head_ids


def _fmt(identities) -> str:
    return ", ".join(f"{name} ({status})" for name, status in sorted(identities))


def cmd_diff(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="ship_gate_diff.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diff", help="what HEAD introduces vs a baseline ref -- exit 1 if anything")
    d.add_argument("--base", default=DEFAULT_BASE)
    d.add_argument("--repo", default=None)
    d.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd != "diff":
        return 2  # pragma: no cover -- argparse `required=True` makes this unreachable

    repo = Path(args.repo) if args.repo else _ROOT
    introduced, resolved = diff(repo, args.base)

    if args.json:
        print(json.dumps({"base": args.base, "introduced": sorted(introduced),
                          "resolved": sorted(resolved)}, indent=2, sort_keys=True))
    else:
        print(f"ship-gate-diff: HEAD vs {args.base}")
        if introduced:
            print(f"  INTRODUCED ({len(introduced)}): {_fmt(introduced)}")
        else:
            print("  introduced: none")
        if resolved:
            print(f"  resolved ({len(resolved)}): {_fmt(resolved)}")
    return 1 if introduced else 0


def main(argv: Optional[list[str]] = None) -> int:
    return cmd_diff(argv)


if __name__ == "__main__":
    sys.exit(main())
