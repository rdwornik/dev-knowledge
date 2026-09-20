"""lane_digest.py -- one operator-facing digest from the receipts of a batch (lane-l8-lane-end).

The `digest` organ of the `lane-end` moment (`ecosystem/harness.yaml`; command
`lane_digest.py --lane {lane}`), and the batch view (`--root`). The operator reads ONE digest, not
merges: per lane, what it did, its verdict, its cost if one was recorded, and what is left open.

Plain language on purpose. A receipt is machine text (`SKIPPED-NOT-BUILT`, `exit_code`, an input
hash); the digest says "not built yet", "did not pass" and names the organ in words. Nothing here
prints a hash, a receipt file name or a status token.

  * verdict: `finished clean` (every organ passed) / `needs attention` (an organ failed or could not
    run) / `incomplete` (nothing failed, but an organ was skipped or no receipts exist yet).
  * open items: every organ that is not `ok`, and a lane with no receipts at all.
  * cost: the newest `usd` row for the lane in `logs/LANE-COSTS.jsonl`; otherwise "not recorded".

Reads only. It never stops a session (DECLARE-NIGHT N3): an unexpected failure is a printed reason
and exit 4; the argument-error code 2 -- a Stop hook's "block and continue" -- is never returned.

FLOOR: hub-only. One-line reason: it reads the hub's lane receipts and cost ledger.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

try:  # pragma: no cover -- whichever entry point the caller uses (package mode vs script)
    from scripts import transport_report as _tr
except ImportError:  # pragma: no cover
    import transport_report as _tr

EXIT_OK = 0
EXIT_FAILED = 4

VERDICT_CLEAN = "finished clean"
VERDICT_ATTENTION = "needs attention"
VERDICT_INCOMPLETE = "incomplete"

_ROOT = Path(__file__).resolve().parents[1]
_PLAIN_STATUS = {
    "failed": "did not pass",
    "error": "could not run",
    "SKIPPED-NOT-BUILT": "not built yet",
    "SKIPPED-NO-INPUT": "skipped, an input was missing",
    "unreadable": "its receipt could not be read",
}


@dataclass
class LaneInput:
    name: str
    receipts: list[dict] = field(default_factory=list)
    did: list[str] = field(default_factory=list)
    cost_usd: Optional[float] = None


def _words(organ: str) -> str:
    """`fleet_health.seat_health_line` -> `seat health line`; `no_leftovers` -> `no leftovers`."""
    return organ.rsplit(".", 1)[-1].replace("_", " ").replace("-", " ").strip() or "an organ"


def _status(receipt: dict) -> str:
    return str(receipt.get("status") or "")


def open_items(lane: LaneInput) -> list[str]:
    if not lane.receipts:
        return ["no receipts yet -- nothing has reported for this lane"]
    items = []
    for r in lane.receipts:
        status = _status(r)
        if status == "ok":
            continue
        phrase = _PLAIN_STATUS.get(status, "status unclear")
        code = r.get("exit_code")
        if status == "failed" and isinstance(code, int) and code:
            phrase += f" (exit {code})"
        items.append(f"{_words(str(r.get('organ') or ''))}: {phrase}")
    return items


def verdict(lane: LaneInput) -> str:
    if not lane.receipts:
        return VERDICT_INCOMPLETE
    statuses = {_status(r) for r in lane.receipts}
    if statuses & {"failed", "error", "unreadable"}:
        return VERDICT_ATTENTION
    if statuses - {"ok"}:
        return VERDICT_INCOMPLETE
    return VERDICT_CLEAN


def verdicts(lanes: Sequence[LaneInput]) -> dict[str, str]:
    return {lane.name: verdict(lane) for lane in lanes}


def render_digest(lanes: Sequence[LaneInput]) -> str:
    tally = verdicts(lanes)
    counts = {v: sum(1 for x in tally.values() if x == v)
              for v in (VERDICT_CLEAN, VERDICT_ATTENTION, VERDICT_INCOMPLETE)}
    out = [f"# Lane digest -- {len(lanes)} lane{'s' if len(lanes) != 1 else ''}", "",
           f"{counts[VERDICT_CLEAN]} finished clean, {counts[VERDICT_ATTENTION]} need attention, "
           f"{counts[VERDICT_INCOMPLETE]} incomplete.", ""]
    for lane in lanes:
        items = open_items(lane)
        out += [f"## {lane.name} -- {tally[lane.name]}", ""]
        if lane.did:
            out += ["Did:"] + [f"- {line}" for line in lane.did] + [""]
        else:
            out += ["Did: no commits recorded.", ""]
        out += [f"Cost: ${lane.cost_usd:,.2f}" if lane.cost_usd is not None else "Cost: not recorded", ""]
        if items:
            out += ["Left open:"] + [f"- {item}" for item in items]
        else:
            out += ["Left open: nothing."]
        out += [""]
    return "\n".join(out).rstrip() + "\n"


# --- reading the inputs --------------------------------------------------------------------------

def load_receipts(receipts_dir: Path) -> list[dict]:
    if not receipts_dir.is_dir():
        return []
    rows = []
    for path in sorted(receipts_dir.glob("*.json")):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            rows.append({"organ": path.stem, "status": "unreadable"})
            continue
        if isinstance(row, dict) and row.get("organ"):
            rows.append(row)
        else:   # any shape we do not recognise is an open item, never a silent omission
            rows.append({"organ": path.stem, "status": "unreadable"})
    return rows


def load_costs(costs_file: Path) -> dict[str, float]:
    """slug -> the newest `usd` recorded for it (a later row supersedes an earlier one)."""
    costs: dict[str, float] = {}
    try:
        text = costs_file.read_text(encoding="utf-8")
    except OSError:
        return costs
    for line in text.splitlines():
        try:
            row = json.loads(line)
            costs[str(row["slug"])] = float(row["usd"])
        except (ValueError, KeyError, TypeError):
            continue
    return costs


def _lane_from(name: str, receipts_dir: Path, repo: Path, costs: dict[str, float]) -> LaneInput:
    return LaneInput(name=name, receipts=load_receipts(receipts_dir),
                     did=_tr.commit_subjects(repo), cost_usd=costs.get(name))


def batch_lanes(root: Path, costs: dict[str, float]) -> list[LaneInput]:
    """One lane per sub-directory of `root`: its `logs/receipts` when present, else its own JSON."""
    lanes = []
    for sub in sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []:
        nested = sub / "logs" / "receipts"
        lanes.append(_lane_from(sub.name, nested if nested.is_dir() else sub, sub, costs))
    return lanes


# --- entry point ---------------------------------------------------------------------------------

class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # argparse would exit 2 -- the blocking code
        raise ValueError(message)


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="lane_digest.py", description=__doc__.splitlines()[0])
    p.add_argument("--lane", default=None, help="digest this one lane (the moment command)")
    p.add_argument("--root", default=None,
                   help="digest a batch: a folder with one sub-folder (a lane checkout) per lane")
    p.add_argument("--receipts-dir", default=None,
                   help="with --lane: the lane's receipts (default $HARNESS_RECEIPTS_DIR or <repo>/logs/receipts)")
    p.add_argument("--repo", default=None, help="the checkout to read commits from (default: this repo)")
    p.add_argument("--costs-file", default=None, help="default <repo>/logs/LANE-COSTS.jsonl")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    try:
        try:
            args = _parser().parse_args(argv)
        except ValueError as exc:
            print(f"lane_digest: bad arguments: {exc}", file=sys.stderr)
            return EXIT_FAILED
        repo = Path(args.repo) if args.repo else _ROOT
        costs = load_costs(Path(args.costs_file) if args.costs_file else repo / "logs" / "LANE-COSTS.jsonl")
        if args.root:
            lanes = batch_lanes(Path(args.root), costs)
        else:
            name = args.lane or repo.resolve().name
            receipts = Path(args.receipts_dir or os.environ.get("HARNESS_RECEIPTS_DIR")
                            or repo / "logs" / "receipts")
            lanes = [_lane_from(name, receipts, repo, costs)]
        sys.stdout.write(render_digest(lanes))
        return EXIT_OK
    except BaseException as exc:  # noqa: BLE001 -- a digest must never raise out of a Stop hook
        print(f"lane_digest: {type(exc).__name__}: {exc}", file=sys.stderr)
        return EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
