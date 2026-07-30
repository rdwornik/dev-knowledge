#!/usr/bin/env python3
"""Assemble PASTE_THIS.md from a v5 handoff bundle's canonical sources.

Usage: python scripts/assemble_paste.py <bundle_dir>

Manifest (in order):
  0. <bundle>/HANDOFF_BOOT.md session-header (optional; extracted from the bundle's
     own HANDOFF_BOOT.md up to the first '##' heading — slug/mode/purpose/generated-at)
  1. protocols/HANDOFF_BOOT.md  (required — browser role file + boot line)
  2. <bundle>/RESIDUAL.md       (required — drift-flags + planning why + task-graph)
  3. <bundle>/PROBES.md         (required — orientation + teeth probes)
  4. <bundle>/SUPPLEMENT.md     (architect strategic supplement — an always-generated
     fillable file; only its filled-in ANSWERS region folds in, and only when non-empty,
     since the QUESTIONS are for the OUTGOING browser, not the incoming session)

Output: <bundle>/PASTE_THIS.md  (UTF-8, LF, never hand-edited)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import click

_SECTION_SEP = "\n\n---\n\n"

# RF-2 item 2: surface paste growth so it stops creeping unchecked (36.5 KB -> 59 KB across
# 06-15..07-03 with no budget). The healthy filled paste is ~59 KB; warn just past that so
# genuine bloat (re-narration creep, RF-6) trips a visible [warn] without nagging on a normal
# bundle. A WARN, not a gate — assembly still succeeds. Tunable.
_SIZE_WARN_BYTES = 65_000

# A10 item 2 / R4 ([#446]): the stated numeric byte budget for the browser role file
# `protocols/HANDOFF_BOOT.md` — 18,000 bytes, ruled 2026-07-31 (architect technical lane;
# recorded as amendment A1 on docs/audits/2026-07-31-technical-v6-open-rulings.md). Live boot
# was 16,156 B when the number was ruled, so the budget is ~11% headroom over a MEASURED file,
# not an invented ceiling. The per-bundle session header is NOT governed by it.
#
# ENFORCEMENT IS SPLIT BY SITE (operator ruling 2026-07-31): this emitter WARNs and assembly
# still succeeds; `audit.py::check_boot_byte_budget` FAILs, so the ship-gate REDs and the merge
# blocks. The guarantee lives in the gate that blocks the merge, not in the emitter — a
# blocking assembler would make an over-long boot un-generatable rather than un-shippable.
HANDOFF_BOOT_BYTE_BUDGET = 18_000

# Intake #18 A8: ruling-bearing markers in a folded ANSWERS region. A ruling stranded in a
# consumed transient is promotion debt (BW-h) — surfaced at the exact beat the transient is
# consumed. Advisory only; never blocks the fold.
_PROMOTION_DEBT_RE = re.compile(r"(?i)\b(?:BINDING|do not relitigate|MUST NOT|ruling)\b")


def _report_promotion_debt(answers: str) -> None:
    """Print the PROMOTION DEBT block for ruling-bearing ANSWERS lines (intake #18 A8).

    Each matched line is echoed verbatim with the ADR-87-item-7 ladder prompt. Stdout/stderr
    advisory only — assembly always proceeds.
    """
    hits = [ln.strip() for ln in answers.splitlines() if _PROMOTION_DEBT_RE.search(ln)]
    if not hits:
        return
    click.echo(f"[promotion-debt] {len(hits)} ruling-bearing line(s) in the folded ANSWERS — "
               "durable home: ADR / PLAYBOOK / ESSENTIALS one-liner / carrier? (intake #18 A8)",
               err=True)
    for ln in hits:
        click.echo(f"  | {ln}", err=True)


def _extract_session_header(text: str) -> str:
    """Return the session-header block from a bundle HANDOFF_BOOT.md.

    Extracts everything up to (but not including) the first '## ' heading —
    the title line, scope comment, and the Field/Value table. Strips trailing
    whitespace so the block ends cleanly.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        if re.match(r"^## ", line):
            break
        out.append(line)
    return "".join(out).rstrip()


_MODE_RE = re.compile(
    r"(?im)^\|\s*\*{0,2}mode\*{0,2}\s*\|\s*\*{0,2}(architect|execution)\b")


def _extract_mode(text: str) -> str | None:
    """Return the handoff mode ('architect' | 'execution') from a bundle HANDOFF_BOOT.md.

    Parses the `| **Mode** | **architect** ... |` row of the session-header Field/Value
    table (the row v5 §13 bundles emit). Returns the lowercased mode, or None when no
    parseable Mode row is present — the caller then treats the bundle as non-architect
    (the supplement stays a silent [skip], the pre-v5.1 behaviour).
    """
    m = _MODE_RE.search(text)
    return m.group(1).lower() if m else None


_ANSWERS_MARKER_RE = re.compile(r"^.*PASTE CHAT ANSWERS BELOW THIS LINE.*$", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _extract_answers(text: str) -> str | None:
    """Return the filled-in ANSWERS region of a SUPPLEMENT.md, or None if unfilled.

    The supplement is generated with a fixed divider line containing
    'PASTE CHAT ANSWERS BELOW THIS LINE'; the operator pastes the outgoing chat's
    answers below it. Everything after that divider is the ANSWERS region. The operator
    scaffolding (HTML comments) and surrounding whitespace are stripped; if nothing
    substantive remains the supplement is unfilled (cold handoff or not-yet-filled) and
    None is returned, so the caller does not fold it. Only the ANSWERS region is ever
    folded — the QUESTIONS are for the OUTGOING browser, not the incoming session.

    No divider present (a legacy / hand-written supplement) -> treat the whole file as
    answers, preserving the pre-v5.2 whole-file fold for non-conformant inputs.
    """
    m = _ANSWERS_MARKER_RE.search(text)
    region = text[m.end():] if m else text
    stripped = _HTML_COMMENT_RE.sub("", region).strip()
    return stripped or None


@click.command()
@click.argument("bundle_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def main(bundle_dir: Path) -> None:
    """Assemble PASTE_THIS.md for BUNDLE_DIR from canonical sources."""
    repo_root = Path(__file__).parent.parent

    # Fill-step flip (§13 "the cold->FILLED flip is mechanized via the assembler's shared
    # fill-state"): when the SUPPLEMENT was FILLED after a cold generation, flip the cold
    # framing banners to FILLED in the SOURCE files first, so PASTE_THIS and its sources agree
    # with the folded ANSWERS instead of still announcing "generated EMPTY". No-op on a cold /
    # unfilled bundle; surgical (never clobbers hand-authored FILL-IN narrative).
    from gen_handoff import reflow_framing  # noqa: PLC0415 (sibling CLI; deferred import)
    flipped = reflow_framing(bundle_dir)
    if flipped:
        click.echo("[reflow] SUPPLEMENT filled -> flipped cold framing to FILLED in: "
                   f"{', '.join(flipped)}", err=True)

    sections: list[tuple[str, str]] = []

    # 0. Optional: bundle session-header (slug/mode/purpose/generated-at). The Mode row
    #    also drives the architect-mode supplement expectation in the manifest loop below.
    mode: str | None = None
    bundle_boot = bundle_dir / "HANDOFF_BOOT.md"
    if bundle_boot.exists():
        boot_text = bundle_boot.read_text(encoding="utf-8")
        mode = _extract_mode(boot_text)
        header = _extract_session_header(boot_text)
        if header:
            sections.append(("HANDOFF_BOOT.md (session header)", header))

    # 1-3. Required sources (inlined verbatim — the file-less browser must RECEIVE them).
    required: list[tuple[str, Path]] = [
        ("protocols/HANDOFF_BOOT.md", repo_root / "protocols" / "HANDOFF_BOOT.md"),
        ("RESIDUAL.md", bundle_dir / "RESIDUAL.md"),
        ("PROBES.md", bundle_dir / "PROBES.md"),
    ]
    for label, path in required:
        if not path.exists():
            click.echo(f"[error] Required source missing: {path}", err=True)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        # rule: handoff-boot-budget
        # A10 item 2 / R4: the browser role file carries a stated numeric byte budget. WARN
        # here (assembly proceeds); audit.py::check_boot_byte_budget is the FAIL-class organ
        # that actually blocks the merge. Measured on the SOURCE file, not the assembled
        # paste — PASTE_THIS has its own separate _SIZE_WARN_BYTES budget above.
        if label == "protocols/HANDOFF_BOOT.md":
            boot_bytes = len(text.encode("utf-8"))
            if boot_bytes > HANDOFF_BOOT_BYTE_BUDGET:
                click.echo(f"[warn] protocols/HANDOFF_BOOT.md is {boot_bytes} bytes "
                           f"(> budget {HANDOFF_BOOT_BYTE_BUDGET}) — trim the browser role file; "
                           "audit.py check_boot_byte_budget FAILs the ship-gate on this "
                           "(A10 item 2 / R4)", err=True)
        sections.append((label, text.rstrip()))

    # 4. SUPPLEMENT.md — the architect strategic supplement (an always-generated fillable
    #    file). Fold ONLY its filled-in ANSWERS region, and ONLY when non-empty: the
    #    QUESTIONS are for the OUTGOING browser, and an empty ANSWERS section (a cold or
    #    not-yet-filled handoff) is the defined N/A disposition, not folded. CC never
    #    fabricates answers, so an unfilled supplement folds nothing — by design.
    supplement = bundle_dir / "SUPPLEMENT.md"
    if supplement.exists():
        answers = _extract_answers(supplement.read_text(encoding="utf-8"))
        if answers:
            sections.append(("SUPPLEMENT.md", answers))
            _report_promotion_debt(answers)
        else:
            click.echo(
                "[skip] SUPPLEMENT.md present but ANSWERS empty (cold handoff or "
                "not-yet-filled) -> not folded; next session uses the section 13(d) beat",
                err=True)
    elif mode == "architect":
        click.echo(
            "[skip] SUPPLEMENT.md not found — expected generated in architect mode; "
            "assembling without it", err=True)
    else:
        click.echo("[skip] SUPPLEMENT.md not found — no supplement section", err=True)

    body = _SECTION_SEP.join(f"=== {label} ===\n\n{content}" for label, content in sections)
    # Terminal END sentinel (intake #18 A1): makes paste truncation VISIBLE to the browser —
    # a paste not ending in this line is partial (BW-a). n counts the sections actually
    # folded (the sentinel is not a section); bytes measure the body BEFORE the sentinel so
    # the value is deterministic, never self-referential.
    content_bytes = len(body.encode("utf-8"))
    body = (body + _SECTION_SEP
            + f"=== END OF PASTE — {len(sections)} sections · {content_bytes} bytes ===")
    paste_path = bundle_dir / "PASTE_THIS.md"
    paste_path.write_text(body + "\n", encoding="utf-8", newline="\n")
    size = len(body.encode("utf-8"))
    click.echo(f"Written: {paste_path} ({size} bytes)")
    if size > _SIZE_WARN_BYTES:
        click.echo(f"[warn] PASTE_THIS.md is {size} bytes (> {_SIZE_WARN_BYTES}) — heavy boot; "
                   "check for re-narration creep (RF-2/RF-6) before shipping; artifacts other "
                   "than PASTE_THIS must not be pasted at all (intake #18 A2)", err=True)


if __name__ == "__main__":
    main()
