#!/usr/bin/env python
"""windows_gate -- the known-reds-aware judgement behind the `windows-gate` required context
(ADR-127 AMENDMENT 2). Repair 1 of the integrator's refusal of 866d0925 (REFUSED-linux-first-ci).

THE DEFECT IT REPAIRS. The first `windows-gate` read the raw `pytest` matrix conclusion. The
Windows leg concludes `failure` on main whenever a known, FLAGGED red exists on it (a red on both
sides is not a refusal), so the gate was red on every Windows-sensitive merge. The merge verdict
(`actions_verdict.verdict_for`) judges a failing pytest leg TEST BY TEST against the base run;
this module applies that same comparison inside the run, with the same functions, so the gate and
the verdict cannot disagree:

  * the leg `success`                     -> pass;
  * the leg `failure`                     -> compare its failing node ids with the base run's
    Windows leg (`known_reds.compare_to_base`): any NEW red (red at the tip, green at the base), a
    non-test failure marker (INTERNALERROR, worker crash, collection error) or a red that names no
    test -> FAIL; reds present on both sides (flagged or registered) -> pass;
  * anything else (skipped, cancelled, timed_out, absent) -> FAIL;
  * an unreadable tip log, base log or registry -> FAIL (fail closed). Never advisory.

Needs `click` (via `actions_verdict`), so the workflow job runs `uv sync --locked` first.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from scripts import actions_verdict as av, known_reds as kr
except ImportError:                                               # pragma: no cover -- shim
    import actions_verdict as av
    import known_reds as kr

LEG_SUCCESS = ("success",)


def judge(leg_conclusion: str, tip_text: Optional[str], base_text: Optional[str],
          registry, *, os_key: str = "windows-latest") -> "tuple[bool, str]":
    """`(passes, reason)` for the Windows leg. Pure: logs and registry come from the caller."""
    if leg_conclusion in LEG_SUCCESS:
        return True, "the Windows leg succeeded"
    if leg_conclusion != "failure":
        return False, f"the Windows leg concluded {leg_conclusion or 'absent'}: it did not run to a verdict"
    if tip_text is None:
        return False, "the Windows leg is red and its pytest output could not be read (fail closed)"
    if registry is None:
        return False, "the known-reds registry at the base could not be read (fail closed)"
    if base_text is None:
        return False, "the base run's Windows pytest output could not be read (fail closed)"
    tip, base = av._leg_failures(tip_text), av._leg_failures(base_text)
    if tip["markers"]:
        return False, "non-test failure on the Windows leg: " + "; ".join(tip["markers"])
    if not tip["ids"]:
        return False, "the Windows leg is red and its output names no failing test (fail closed)"
    result = kr.compare_to_base(tip["ids"], base["ids"], registry, workers=registry.workers,
                                os_key=os_key, tip_signatures=tip["signatures"],
                                base_signatures=base["signatures"])
    if result["new"]:
        return False, "new red test(s) on the Windows leg: " + ", ".join(sorted(result["new"]))
    flagged = len(result["flagged"])
    return True, (f"the Windows leg is red only where the base is red too "
                  f"({len(tip['ids'])} test(s); {flagged} flagged, none new)")


def _read(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--leg-conclusion", required=True)
    ap.add_argument("--tip-out", default=None, help="the tip Windows leg's pytest.out")
    ap.add_argument("--base-out", default=None, help="the base run's Windows pytest.out")
    ap.add_argument("--base-sha", default=None)
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    registry = None
    if args.leg_conclusion == "failure" and args.base_sha:
        try:
            registry = av._load_registry_at(args.base_sha, repo_root=Path(args.root))
        except Exception as exc:                  # noqa: BLE001 -- reported, and fails closed
            print(f"windows-gate: registry at {args.base_sha} unreadable: {exc}")
    ok, reason = judge(args.leg_conclusion, _read(args.tip_out), _read(args.base_out), registry)
    print(f"windows-gate: {'PASS' if ok else 'FAIL'} -- {reason}")
    return 0 if ok else 1


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    sys.exit(main())
