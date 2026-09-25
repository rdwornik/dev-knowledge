"""lane_digest.py -- one operator-facing digest from the receipts of a batch (lane-l8-lane-end).

The `digest` organ of the `lane-end` moment (`ecosystem/harness.yaml`; command
`lane_digest.py --lane {lane}`), and the batch view. The operator reads ONE digest, not merges:
per lane, what it did, its merge sha, its verdict, its cost if one was recorded, and what is left
open.

Plain language on purpose. A receipt is machine text (`SKIPPED-NOT-BUILT`, `exit_code`, an input
hash); the digest says "not built yet", "did not pass" and names the organ in words. Nothing here
prints a hash, a receipt file name or a status token.

  * verdict: `finished clean` (every organ passed) / `needs attention` (an organ failed or could not
    run) / `incomplete` (nothing failed, but an organ was skipped or no receipts exist yet).
  * open items: every organ that is not `ok`, and a lane with no receipts at all.
  * cost: the newest `usd` row for the lane in `logs/LANE-COSTS.jsonl`; otherwise "not recorded".

TWO BATCH VIEWS, one live and one dead (R-W4-3, lane-batch-digest). `--root` reads each lane's own
worktree checkout (`<root>/<lane>/logs/receipts`) and its `git log main..HEAD` -- correct only
while that worktree still exists. By batch-close it does not: `teardown` has already removed it,
and a merge fast-forwards HEAD onto main, so `main..HEAD` reads empty by construction ("1 lane,
finished clean, Did: no commits recorded" -- wave 3's own batch-close, reproduced in
`tests/test_connection_loop.py`). The reports view is the fix: it reads each lane's
`LANE-END-<lane>.md` off the transport (`transport_report.py`, written from inside the lane's own
worktree at lane-end, while `main..HEAD` was still right) plus the merge sha `merge_receipt.py`
recorded on the integrator's own ledger (`logs/MERGE-RECEIPTS.jsonl`) -- never git, and never the
integrator's checkout. The lane roster is named explicitly (`--lanes`, or `$HARNESS_LANES`) rather
than discovered by listing what happens to be on the transport: the whole point is that a lane can
be MISSING its report (its worktree predates the transport-report mechanism, or the Stop hook was
never armed in it) and still needs to be named, not silently dropped. With no roster named either
way, every `LANE-END-*.md` found under the reports root is read instead -- a best-effort listing,
not a substitute for a named roster.

THE REPORTS VIEW ARMS ITSELF FROM THE ENVIRONMENT, ON PURPOSE -- `ecosystem/harness.yaml` is out of
this lane's reach (the contract: "do not edit harness.yaml ... the trigger exists"; DECLARE-WAVE4A
hard precondition 5 confines every harness.yaml edit this wave to lane W4-2's `merge` moment). The
`batch-close` row's declared command stays exactly `lane_digest.py --lane {batch} --receipts-dir
{receipts}` -- unedited, untouched. So the reports view triggers itself: naming a lane roster,
either `--lanes` on the command line or `$HARNESS_LANES` in the environment, is what selects it,
because a roster is the one signal that distinguishes "digest this batch" from "digest the one real
lane `--lane` and `--receipts-dir` already name". `--reports-root` is there too, for a caller that
wants to point at an explicit (or synthetic, in a test) transport root rather than the ambient
`CLAUDE_PROMPTS_DIR` `transport_report.py` itself resolves from -- but naming it is never required:
`HARNESS_LANES=<comma-separated lanes>` alongside the declared row's own `HARNESS_BATCH=<batch>` is
enough, and it is the same env-var-carries-batch-context convention `HARNESS_BATCH` already is.

Reads only. It never stops a session (DECLARE-NIGHT N3): an unexpected failure is a printed reason
and exit 4; the argument-error code 2 -- a Stop hook's "block and continue" -- is never returned.

FLOOR: hub-only. One-line reason: it reads the hub's lane receipts and cost ledger.
"""
from __future__ import annotations

import argparse
import json
import os
import re
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
    "missing": "no report reached the transport",
}


@dataclass
class LaneInput:
    name: str
    receipts: list[dict] = field(default_factory=list)
    did: list[str] = field(default_factory=list)
    cost_usd: Optional[float] = None
    #: The merge commit the integrator's own ledger (`logs/MERGE-RECEIPTS.jsonl`) recorded for
    #: this lane -- R-W4-3's "integrator's receipt" half. `None` when the ledger names none.
    merge_sha: Optional[str] = None


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
        out += [f"Merge: {lane.merge_sha}" if lane.merge_sha else "Merge: not recorded", ""]
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
    """One lane per sub-directory of `root`: its `logs/receipts` when present, else its own JSON.

    LIVE-WORKTREE ONLY. Correct while `<root>/<lane>` is still a checkout -- its own
    `git log main..HEAD` is right there. `teardown` removes that checkout, so this view is
    unusable at batch-close; `reports_root_lanes` below is what batch-close reads (R-W4-3)."""
    lanes = []
    for sub in sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []:
        nested = sub / "logs" / "receipts"
        lanes.append(_lane_from(sub.name, nested if nested.is_dir() else sub, sub, costs))
    return lanes


# --- the transport-reports batch view (R-W4-3) ----------------------------------------------------

def load_merge_shas(ledger_file: Path, batch: Optional[str] = None) -> dict[str, str]:
    """slug -> the newest merge sha `merge_receipt.py` recorded for it in the append-only ledger
    (a later row for the same slug wins). Missing or unreadable: empty, never raised -- a digest
    must never stop on a ledger it cannot read.

    FILTERED BY BATCH WHEN ONE IS NAMED (codex terra HIGH, 2026-09-22): a lane slug is not unique
    across the ledger's whole history -- a later batch can reuse an earlier one's slug -- and
    selecting "the newest row for this slug" with no batch filter would then hand an earlier
    batch's digest a LATER batch's merge sha, silently misattributing whose merge it was. With no
    `batch` given (an ad hoc, batch-unaware invocation) every row is still considered, which is
    the pre-fix behaviour and the only thing possible without knowing which batch to prefer."""
    shas: dict[str, str] = {}
    try:
        text = ledger_file.read_text(encoding="utf-8")
    except OSError:
        return shas
    for line in text.splitlines():
        try:
            row = json.loads(line)
            sha = row.get("merge_sha")
        except (ValueError, AttributeError):
            continue
        if not sha:
            continue
        if batch and str(row.get("batch") or "") != batch:
            continue
        try:
            shas[str(row["slug"])] = str(sha)
        except KeyError:
            continue
    return shas


def lane_roster(reports_dir: Path, lanes_arg: Optional[str]) -> list[str]:
    """The batch's lane names, named explicitly rather than discovered.

    `lanes_arg` (the `--lanes` flag) wins; then `$HARNESS_LANES` -- the same env-var-carries-the-
    batch-context convention `HARNESS_BATCH`/`HARNESS_LANE` already use, so the integrator names
    the roster it already knows without a new harness.yaml placeholder. With NEITHER set, every
    `LANE-END-*.md` actually found under `reports_dir` is read -- a best-effort listing, never a
    silent empty batch, but it can under-name a lane whose report never reached the transport."""
    raw = lanes_arg if lanes_arg is not None else os.environ.get("HARNESS_LANES", "")
    names = [n for n in re.split(r"[,\s]+", raw or "") if n]
    if names:
        return names
    if not reports_dir.is_dir():
        return []
    prefix, suffix = _tr.ARTIFACT_PREFIX, ".md"
    return sorted(p.name[len(prefix):-len(suffix)] for p in reports_dir.glob(f"{prefix}*.md"))


def reports_root_lanes(reports_dir: Path, lane_names: Sequence[str], costs: dict[str, float],
                       merge_shas: dict[str, str]) -> list[LaneInput]:
    """One `LaneInput` per named lane, read from its `LANE-END-<lane>.md` on the transport
    (`transport_report.py`'s `parse_report`) -- never git, and never the integrator's checkout.

    A lane named in the roster with no report on the transport is NAMED AS MISSING (a synthetic
    `status: missing` receipt, which reads as an open item in plain language and an `incomplete`
    verdict), never dropped from the digest: the whole reason `--reports-root` exists is that a
    lane can merge cleanly and still leave no report (its worktree predates the transport-report
    mechanism, or never had the Stop hook armed), and that gap has to be visible, not silent."""
    lanes = []
    for name in lane_names:
        path = reports_dir / f"{_tr.ARTIFACT_PREFIX}{name}.md"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            lanes.append(LaneInput(name=name,
                                   receipts=[{"organ": "transport report", "status": "missing"}],
                                   cost_usd=costs.get(name), merge_sha=merge_shas.get(name)))
            continue
        facts = _tr.parse_report(text)
        lanes.append(LaneInput(name=name, receipts=facts.receipts, did=facts.commits,
                               cost_usd=costs.get(name), merge_sha=merge_shas.get(name)))
    return lanes


# --- entry point ---------------------------------------------------------------------------------

class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # argparse would exit 2 -- the blocking code
        raise ValueError(message)


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="lane_digest.py", description=__doc__.splitlines()[0])
    p.add_argument("--lane", default=None, help="digest this one lane (the moment command)")
    p.add_argument("--root", default=None,
                   help="digest a batch from live worktree checkouts (one sub-folder per lane); "
                        "unusable once teardown has run -- see --reports-root")
    p.add_argument("--reports-root", nargs="?", default=None, const="",
                   help="digest a batch from the transport's LANE-END-<lane>.md reports (R-W4-3), "
                        "never git. A value is the transport root; the bare flag resolves it the "
                        "way transport_report.py does (CLAUDE_PROMPTS_DIR, User scope first)")
    p.add_argument("--lanes", default=None,
                   help="with --reports-root: the batch's lane roster, comma/whitespace-separated "
                        "(default: $HARNESS_LANES, else every LANE-END-*.md found)")
    p.add_argument("--batch", default=None,
                   help="with --reports-root: the batch a merge sha is looked up under (default: "
                        "--lane, else $HARNESS_BATCH) -- a lane slug is not unique across the "
                        "ledger's whole history, so an unnamed batch reads every row for the slug")
    p.add_argument("--merge-ledger", default=None,
                   help="with --reports-root: default <repo>/logs/MERGE-RECEIPTS.jsonl")
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
        # A named roster (`--lanes`, or `$HARNESS_LANES` -- see the module docstring) selects the
        # reports view even through the UNEDITED harness.yaml row, whose `--lane {batch}
        # --receipts-dir {receipts}` never changes: a roster is what distinguishes "digest this
        # batch" from "digest the one real lane those two flags already name".
        wants_reports = (args.reports_root is not None or args.lanes
                        or os.environ.get("HARNESS_LANES"))
        if args.root:
            lanes = batch_lanes(Path(args.root), costs)
        elif wants_reports:
            folder = _tr.resolve_transport(args.reports_root or None)
            # The batch identity a merge-sha lookup filters on: `--batch` first, then whatever
            # `--lane` carries (the unedited harness.yaml row's `{batch}` substitution lands
            # there), then `$HARNESS_BATCH` directly.
            batch = args.batch or args.lane or os.environ.get("HARNESS_BATCH")
            merge_shas = load_merge_shas(
                Path(args.merge_ledger) if args.merge_ledger else repo / "logs" / "MERGE-RECEIPTS.jsonl",
                batch=batch)
            lanes = reports_root_lanes(folder, lane_roster(folder, args.lanes), costs, merge_shas)
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
