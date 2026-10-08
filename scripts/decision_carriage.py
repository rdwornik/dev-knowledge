#!/usr/bin/env python
"""decision_carriage.py -- a decision's true carriage, derived from evidence; the seed of the
batch-close dispositions gate.

WHY THIS EXISTS (R90, `to-browser/RATIFICATION-2026-10-08.md`). The 2026-10-07 handoff readiness
dry run (`to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`) found twelve accepted decisions
that P13 (`decision_coverage.onboarding_findings`) refused: the B2-W1 integrator had ruled a
disposition for every one of them (seat ruling 3, 2026-10-05) and none reached
`decision_coverage.DECISION_DISPOSITIONS`. A ruling that lives only in a session file is the
same as no ruling to every gate. This module derives each decision's carriage from evidence
and RENDERS the register entries, so the entry is generated rather than retyped. The gate that
REQUIRES it at batch close is still owed (its row is filed with this module); this is its seed.

WHAT IT READS, per decision file (`to-cc/AMEND-*` / `DECLARE-*` on the transport):
  * the lanes the file names that have a LANE contract on the transport (a name with no
    contract is prose, not a lane);
  * per lane: a merge commit REACHABLE from `--ref` whose subject names the lane's branch --
    every merge, not only the first-parent spine, because a lane can land inside another
    lane's merge (FOUNDATION lane 4 landed inside b2-merge-gate, 1546090c); and any
    `archive/*` tag carrying the lane's name, with whether that tag is on `--ref`;
  * the GREEN `SIGNAL-*.md` files the decision names, and whether each exists;
  * for a `-vN-superseded` file, its successor and whether the successor exists;
  * the render-record lines that name the decision (an AMEND applied at render).

WHAT IT DOES NOT DO. It never judges that a decision is done: a merged lane can still leave a
Done-when unmet (AMEND-B2-W1-4: W1-12 merged close-out-only). `propose()` returns a PROPOSAL --
SUPERSEDED / ALL-LANES-MERGED / SOME-LANES-MERGED / NO-LANE-MERGED / NO-LANES -- and `render`
writes a register entry ONLY for a decision the seat ruled ESTABLISHED (`--accept`). A partly
executed decision is carried by an implementing row (`· implements: <stem> ·`), never by a
whole-file Disposition, because `decision_coverage._state` reads any Disposition as `done`.

Read-only: git and the transport are read; `render` prints. Layer 2 holds (ADR-28).
LIBRARY-FIRST: stdlib (argparse, json, re, subprocess) and git; `gen_handoff.transport_root`
for the transport; no new dependency.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

#: A lane name as decision files write it: `foundation-<n>-<slug>` or `b2-<slug>`.
LANE_RE = re.compile(r"\b(foundation-\d+-[a-z0-9-]+|b2-[a-z][a-z0-9-]+)\b")
SIGNAL_RE = re.compile(r"to-browser/(SIGNAL-[A-Za-z0-9._-]+\.md)")
SUPERSEDED_RE = re.compile(r"-v\d+-superseded$")

PROPOSE_SUPERSEDED = "SUPERSEDED"
PROPOSE_ALL = "ALL-LANES-MERGED"
PROPOSE_SOME = "SOME-LANES-MERGED"
PROPOSE_NONE = "NO-LANE-MERGED"
PROPOSE_NO_LANES = "NO-LANES"


def _git(repo: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.stdout


def _is_ancestor(repo: Path, commit: str, ref: str) -> bool:
    return subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", commit, ref],
                          capture_output=True).returncode == 0


def name_pattern(stem: str) -> re.Pattern:
    """The decision's name as prose writes it: the full stem, or the stem without its date --
    `AMEND-BATCH-FOUNDATION-3 applied` -- bounded so `AMEND-BATCH-FOUNDATION` never matches
    `AMEND-BATCH-FOUNDATION-3`."""
    short = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)
    return re.compile(rf"{re.escape(stem)}|{re.escape(short)}(?![-\w])")


def _lines_naming(path: Path, needle: "re.Pattern", limit: int = 3) -> list[str]:
    if not path.exists():
        return []
    out = []
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if needle.search(ln):
            out.append(f"{path.parent.name}/{path.name}:{i}")
            if len(out) >= limit:
                break
    return out


def lane_merges(lane: str, merges: list[tuple[str, str]]) -> list[str]:
    """Short shas of the merges whose subject names `lane`'s branch, oldest last as git lists."""
    keys = (f"'worktree-{lane}'", f"/{lane}'", f"'{lane}'")
    return [sha for sha, subject in merges if any(k in subject for k in keys)]


_SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


def state_tips(transport: Path, lane: str) -> list[str]:
    """Shas the batch STATE files record for `lane` -- its branch tip -- inside the lane's own
    clause: after its name and before the next `,` or `;`, so a fates line listing several
    lanes (`foundation-4-merge-gate (from its branch 2dd2067d), foundation-7-ci-poll, ...`)
    never lends one lane's sha to the next."""
    clause = re.compile(rf"{re.escape(lane)}(?![-\w])([^,;]*)")
    shas: list[str] = []
    for state in sorted((transport / "to-browser").glob("STATE-BATCH-*.md")):
        for m in clause.finditer(state.read_text(encoding="utf-8", errors="replace")):
            shas += [s for s in _SHA_RE.findall(m.group(1)) if not s.isdigit()]
    return list(dict.fromkeys(shas))


def gather(repo: Path, transport: Path, decision_rels: list[str], *,
           ref: str = "origin/main") -> list[dict]:
    """The evidence record per decision file. Reads git and the transport; writes nothing."""
    merges = [tuple(ln.split(" ", 1)) for ln in
              _git(repo, "log", "--merges", "--format=%h %s", ref).splitlines() if " " in ln]
    tags = _git(repo, "tag", "-l", "archive/*").split()
    contracts = {p.name for p in transport.glob("LANE-*.md")}
    records = sorted((transport / "to-browser").glob("SESSION-gen-*-record-*.md"))
    out = []
    for rel in decision_rels:
        path = transport / rel
        body = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        stem = Path(rel).stem
        lanes = sorted({ln for ln in LANE_RE.findall(body)
                        if any(c.endswith(f"-{ln}.md") for c in contracts)})
        ev = {"decision": rel, "stem": stem, "exists": path.exists(), "lanes": {}}
        for lane in lanes:
            lane_tags = [t for t in tags if t.endswith(lane.split("-", 1)[-1]) or lane in t]
            found = lane_merges(lane, merges)
            ev["lanes"][lane] = {
                "merges": found,
                "tags": {t: _is_ancestor(repo, t, ref) for t in lane_tags},
                # No merge of its own: the lane's recorded tip, proven an ancestor of `ref`
                # (it landed inside another lane's merge).
                "tips_on_ref": [] if found else [
                    sha for sha in state_tips(transport, lane) if _is_ancestor(repo, sha, ref)],
            }
        ev["signals"] = {s: (transport / "to-browser" / s).exists()
                         for s in sorted(set(SIGNAL_RE.findall(body)))}
        base = SUPERSEDED_RE.sub("", stem)
        if base != stem:
            succ = transport / Path(rel).parent / f"{base}.md"
            ev["successor"] = {"file": f"{Path(rel).parent.as_posix()}/{succ.name}",
                               "exists": succ.exists()}
        ev["render_record"] = [hit for rec in records
                               for hit in _lines_naming(rec, name_pattern(base))][:3]
        out.append(ev)
    return out


def propose(ev: dict) -> str:
    """A PROPOSAL from the evidence -- never a verdict that the decision is done (module doc)."""
    if ev.get("successor", {}).get("exists"):
        return PROPOSE_SUPERSEDED
    lanes = ev.get("lanes", {})
    if not lanes:
        return PROPOSE_NO_LANES
    merged = [lane for lane, e in lanes.items() if e["merges"] or e.get("tips_on_ref")]
    if len(merged) == len(lanes):
        return PROPOSE_ALL
    return PROPOSE_SOME if merged else PROPOSE_NONE


def reason_for(ev: dict, ruling: str) -> str:
    """The register entry's reason: the evidence, then the ruling that accepted it."""
    if propose(ev) == PROPOSE_SUPERSEDED:
        return (f"SUPERSEDED, never pasted; successor {ev['successor']['file']}. {ruling}")
    parts = []
    for lane, e in sorted(ev.get("lanes", {}).items()):
        if e["merges"]:
            parts.append(f"lane {lane} merged {', '.join(e['merges'])} (reachable from main)")
        elif e.get("tips_on_ref"):
            parts.append(f"lane {lane} tip {', '.join(e['tips_on_ref'])} is an ancestor of "
                         "main (landed inside another merge)")
        else:
            parts.append(f"lane {lane}: no merge found by subject")
    for sig, ok in sorted(ev.get("signals", {}).items()):
        parts.append(f"{sig} {'present' if ok else 'ABSENT'}")
    if ev.get("render_record"):
        parts.append(f"applied at render ({', '.join(ev['render_record'])})")
    return f"EXECUTED: {'; '.join(parts) or 'no lane evidence'}. {ruling}"


def render(evidence: list[dict], accept: dict[str, str], *, ruling: str, owner: str) -> str:
    """`DECISION_DISPOSITIONS` entries for the ACCEPTED stems only, as Python source text.

    `accept` maps a stem to extra evidence text the seat accepted (empty for none) -- the one
    place a decision with no lane (a review route, say) gets its evidence into the entry.
    """
    lines = []
    for ev in evidence:
        if ev["stem"] not in accept:
            continue
        reason = reason_for(ev, ruling)
        if accept[ev["stem"]]:
            reason = reason.replace(f". {ruling}", f"; {accept[ev['stem']]}. {ruling}", 1)
        lines.append(f"    {json.dumps('declare:' + ev['stem'])}: Disposition(\n"
                     f"        reason={json.dumps(reason, ensure_ascii=False)},\n"
                     f"        owner={json.dumps(owner, ensure_ascii=False)}),")
    return "\n".join(lines)


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("evidence", help="print the evidence + proposal per decision, as JSON")
    g.add_argument("decisions", nargs="+", help="transport-relative decision files")
    g.add_argument("--ref", default="origin/main")
    g.add_argument("--transport")
    r = sub.add_parser("render", help="print DECISION_DISPOSITIONS entries for accepted stems")
    r.add_argument("evidence_json", help="the JSON `evidence` printed")
    r.add_argument("--accept", action="append", default=[], metavar="STEM[=EXTRA]",
                   help="a stem the seat ruled ESTABLISHED, with optional accepted evidence")
    r.add_argument("--ruling", required=True, help="the ruling that accepted the carriage")
    r.add_argument("--owner", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "evidence":
        import gen_handoff  # noqa: PLC0415 -- deferred: only the evidence leg needs the transport
        transport = Path(args.transport) if args.transport else gen_handoff.transport_root()
        if transport is None:
            print("decision_carriage: no transport (set CLAUDE_PROMPTS_DIR)", file=sys.stderr)
            return 2
        evs = gather(Path.cwd(), transport, args.decisions, ref=args.ref)
        for ev in evs:
            ev["proposal"] = propose(ev)
        print(json.dumps(evs, indent=1, ensure_ascii=False))
        return 0
    evs = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    accept = dict((a.split("=", 1) + [""])[:2] for a in args.accept)
    print(render(evs, accept, ruling=args.ruling, owner=args.owner))
    return 0


if __name__ == "__main__":
    sys.exit(main())
