"""gen_north_star.py -- the NORTH STAR view: the arc set, in dependency order.

WHY THIS IS GENERATED AND NEVER HAND-WRITTEN. It answers "what is this repo working towards, and
in what order" -- a question whose answer changes every time a row lands. A hand-written answer is
stale at the next commit, which is the failure this repo already refuses everywhere else ("never
restate a count or roster in prose -- cite the surface that computes it"). So the arc DECLARATION
lives here as data, and every status, count and member list is read from `tasks/` at generation
time.

WHAT IS DECLARED vs WHAT IS DERIVED, stated because the split is the whole design:
  * DECLARED (in ARCS below): which arcs exist, their order, their done-when, and the contract
    each would start from. These are architect judgments and cannot be derived.
  * DERIVED (from tasks/): every member row, its status, its priority, and every count. These are
    facts and must never be typed.

An arc's members are selected by PREDICATE rather than by a hand-listed id set, so a row filed
into an arc's theme tomorrow appears here without editing this file -- the same reason `[#383]`
was re-scoped onto a `kind:` selector instead of line ranges.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

_REPO_ROOT = _SCRIPTS.parent
# HOME: `ecosystem/`, not `docs/`. ADR-101's home allowlist admits docs GENRE TREES only --
# `docs` itself is absent BY DESIGN -- while `ecosystem/` is the admitted home for "generated /
# declared ecosystem state", which is exactly what this view is (`organ-index.md` and
# `doc-counts.md` are its neighbours). The gate refused `docs/NORTH-STAR.md` on first commit
# and it was right to: a new home is an operator ruling, not a drive-by add.
OUT_RELPATH = "ecosystem/north-star.md"

#: The arc set, in DEPENDENCY ORDER. `blocked_by` is prose because it names a condition, not a row.
ARCS: tuple[dict, ...] = (
    dict(
        key="metric",
        name="THE METRIC - a reward function, before anything that would consume one",
        themes=("[E7] Tooling & evaluation",),
        blocked_by="Nothing. This is the head of the sequence.",
        done_when=("A rule-adherence harness scores the instruction corpus, and a deliberately "
                   "weakened instruction set FAILS while the intact set passes. Until that "
                   "discriminates, every downstream arc is optimising against no signal."),
        contract=("intake #35 PROPOSED ROW R3 (promptfoo) - decided in principle, NOT born; "
                  "blocked on one ruling about its fold target, since both [#491] and [#492] "
                  "are deferred today"),
    ),
    dict(
        key="autonomy",
        name="AUTONOMY ORGANS - what fired, how often, and did it help",
        themes=("[E3] Lessons feedback loop", "[E4] Decision management"),
        blocked_by=("THE METRIC. Every absent property here is downstream of a measurement that "
                    "does not yet exist - four AUT lanes reached that conclusion independently, "
                    "from subjects that never touch."),
        done_when=("One surface answers what has actually fired, how often, and whether it "
                   "helped - for organs, for landed rules, and for the LESSONS to rules to "
                   "gates conversion."),
        contract=("docs/audits/2026-08-30-technical-autonomy-decision-tree.md - ten parked "
                  "items, each carrying the trigger that releases it"),
    ),
    dict(
        key="doctrine",
        name="DOCTRINE CONSOLIDATION - one audience, one owner, budgeted in bytes",
        themes=("[E5] Canonical-file integrity", "[E1] Handoff continuity"),
        blocked_by=("Nothing - batch D landed its first wave: README recreated, CLAUDE.md "
                    "re-genred, codex/ universalised."),
        done_when=("Every boot-time surface is budgeted in BYTES with a gate, and every canonical "
                   "doc has exactly one owner and one audience."),
        contract=("docs/audits/2026-08-29-technical-batchd-launch-contracts/ - the seven frozen "
                  "contracts; lanes b, c and h landed"),
    ),
    dict(
        key="deployment",
        name="DEPLOYMENT WAVE - the fleet carries what the hub rules",
        themes=("[E6] Cross-repo universalization", "[E9] Fleet Desired-State System (North Star)"),
        blocked_by=("DOCTRINE CONSOLIDATION - shipping a corpus mid-re-genre ships the churn "
                    "rather than the doctrine."),
        done_when=("Every ADR-104 member carries the ruled corpus at a declared version, and "
                   "fleet_parity reports zero undeclared divergence across them."),
        # THE MIGRATION ORDER. Operator-ruled 2026-08-31 (batch E, CUT-1), SUPERSEDING the
        # "CONFLICT NAMED, NOT RESOLVED" text this field carried between b3f489b5 and the cut.
        # The arc's members are selected by theme, as everywhere else in this file; what is
        # DECLARED here is the ORDER the wave ships in. A rival sixth arc was deliberately NOT
        # created: arc membership is a theme selector, so a second arc sharing [E6]/[E9] would
        # double-count every row in both and make both counts wrong.
        #
        # THE TWO SEQUENCES WERE NEVER RIVALS, and the ruling dissolves rather than adjudicates
        # them: INSTANTIATION order and MIGRATION order are different things. win-tooling is
        # FIRST instantiated (it carries the engine; DC-5 uses its template as the precedent for
        # consumer #2) and LAST migrated (most mature, so best able to wait, and the member where
        # a mid-re-genre ship would cost most). Recorded because the field previously read as a
        # contradiction, and a sequence that reads as a contradiction gets resolved silently by
        # whoever ships first.
        sequence=("hub -> monorepo -> ai-council -> win-tooling (operator-ruled 2026-08-31, "
                  "batch E CUT-1: this is the MIGRATION order, for the consolidated-doctrine "
                  "corpus). win-tooling being LAST here does NOT roll back its status as the "
                  "FIRST INSTANTIATED consumer - the floor stays, and DC-5 instantiates "
                  "ai-council from win-tooling's template. SUPERSEDES the HERMETIZATION order "
                  "recorded on this field 2026-08-31 (batch E -> engine ratification -> "
                  "win-tooling full cycle -> monorepo -> ai-council), which stated the "
                  "INSTANTIATION sequence, not the migration one. Full ruling: "
                  "docs/audits/2026-08-31-technical-batche-launch-contracts/CUT.md CUT-1."),
        contract=("intake #38 (the root-contract) - amended 2026-08-30; R18 stays parked on "
                  "tested conditions rather than on silence"),
    ),
    dict(
        key="learning",
        name="LEARNING LOOP - the repo as its own training signal",
        themes=("[E2] Enforced governance",),
        blocked_by=("THE METRIC, then AUTONOMY ORGANS. A loop with no reward optimises nothing - "
                    "WRONG ORDER, not wrong tool."),
        done_when=("A per-repo layer turns the repo's own events into a boot-surface signal that "
                   "changes what the next session does, with the hub shipping the MECHANISM and "
                   "never the managed state."),
        contract="intake #63 (universal per-repo learning loop) - DRAFT, evidence-gated on AUT-R3",
    ),
)


def read_rows(repo_root: Path) -> list[dict]:
    """Every MANIFEST-REFERENCED `tasks/` row as its frontmatter. DERIVED -- never typed.

    Referenced, not merely present. `tasks/` also holds RETIRED ALLOCATION RECORDS -- files kept
    so a closed id is never re-issued (ADR-107 6.3) -- and a bare `glob("*.md")` counts them,
    which produced a denominator of 354 against `validate_backlog`'s 217. A generated view whose
    total disagrees with the repo's own validator is worse than no view, so the manifest is the
    roster and the glob is not.
    """
    import json

    import yaml

    manifest = Path(repo_root) / "tasks" / "manifest.json"
    referenced = {n["file"] for n in json.loads(manifest.read_text(encoding="utf-8"))["nodes"]
                  if "task" in n}
    out: list[dict] = []
    for p in sorted((Path(repo_root) / "tasks").glob("*.md")):
        if p.name not in referenced:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[3:end]) or {}
        except Exception:                      # noqa: BLE001 - a malformed row is validate_backlog's
            continue                           # finding to report, not this reporter's
        if isinstance(fm, dict) and fm.get("id"):
            fm["_file"] = p.name
            out.append(fm)
    return out


def render(repo_root: Path) -> str:
    rows = read_rows(repo_root)
    open_rows = [r for r in rows if str(r.get("status", "")).lower() == "open"]
    deferred = [r for r in rows if str(r.get("status", "")).lower() == "deferred"]
    lines: list[str] = []
    add = lines.append
    add("# NORTH STAR - the arc set, in dependency order")
    add("")
    add("> **GENERATED - do not hand-edit.** Regenerate:")
    add("> `uv run --locked python scripts/gen_north_star.py --write`")
    add(">")
    add("> The arc names, their order, their done-when and their starting contract are DECLARED in")
    add("> `scripts/gen_north_star.py` - architect judgments, not derivable. Every member row,")
    add("> status and count below is DERIVED from `tasks/` at generation time, so this file cannot")
    add("> drift from the backlog the way a hand-written roadmap does.")
    add("")
    add(f"Open rows: **{len(open_rows)}** of {len(rows)} manifest-referenced "
        f"(**{len(deferred)} deferred**).")
    add("")
    add("**Deferred is shown deliberately.** On 2026-08-30 an intake's fold target was found to")
    add("have gone deferred underneath the instruction that cited it, unnoticed, because nothing")
    add("watches a blocker's status (`[#624]`). A deferred row is not a closed row and a plan")
    add("resting on one is a plan resting on nothing.")
    add("")
    add("**Read the ORDER as binding.** Each arc names what blocks it, and the blocks are not")
    add("preferences: an arc worked ahead of its blocker is work optimising against no signal.")
    add("")
    for i, arc in enumerate(ARCS, 1):
        members = [r for r in open_rows if r.get("theme") in arc["themes"]]
        by_pri: dict[str, int] = {}
        for r in members:
            key = str(r.get("priority", "?"))
            by_pri[key] = by_pri.get(key, 0) + 1
        add(f"## {i}. {arc['name']}")
        add("")
        add(f"- **Blocked by:** {arc['blocked_by']}")
        add(f"- **Done when:** {arc['done_when']}")
        # `sequence` is OPTIONAL and declared per arc: the order the arc ships in, where that
        # order is itself an architect judgment rather than a consequence of the row set.
        if arc.get("sequence"):
            add(f"- **Ships in this order:** {arc['sequence']}")
        add(f"- **First frozen-contract candidate:** {arc['contract']}")
        add(f"- **Themes (the selector):** {', '.join('`' + t + '`' for t in arc['themes'])}")
        pri = " / ".join(f"{k} {v}" for k, v in sorted(by_pri.items())) or "none"
        defs_ = [r for r in deferred if r.get("theme") in arc["themes"]]
        add(f"- **Open rows in scope:** {len(members)} ({pri})")
        add(f"- **Deferred in scope:** {len(defs_)}")
        add("")
    add("## What this view deliberately does NOT do")
    add("")
    add("It does not rank rows inside an arc, and it does not promise that every open row belongs")
    add("to an arc. A row outside every theme selector above is not lost - it is simply not part of")
    add("the North Star sequence, and `BACKLOG.md` remains the complete list. Claiming otherwise")
    add("would make this file a second backlog, which is the duplication this repo spends most of")
    add("its enforcement budget preventing.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gen_north_star",
                                 description="Generate the NORTH STAR arc view from tasks/.")
    ap.add_argument("--write", action="store_true", help="write the file instead of printing it")
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed file is stale")
    ap.add_argument("--repo-root", default=str(_REPO_ROOT))
    args = ap.parse_args(argv)
    root = Path(args.repo_root)
    body = render(root)
    out = root / OUT_RELPATH
    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != body:
            print(f"gen_north_star: {OUT_RELPATH} is STALE -- regenerate with --write")
            return 1
        print(f"gen_north_star: {OUT_RELPATH} current")
        return 0
    if args.write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8", newline="\n")
        print(f"gen_north_star: wrote {OUT_RELPATH}")
        return 0
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
