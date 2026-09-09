#!/usr/bin/env python3
"""Assemble PASTE_THIS.md from a v5 handoff bundle's canonical sources.

Usage: python scripts/assemble_paste.py <bundle_dir>

Manifest (in order):
  0. <bundle>/HANDOFF_BOOT.md session-header (optional; extracted from the bundle's
     own HANDOFF_BOOT.md up to the first '##' heading — slug/mode/purpose/generated-at)
  1. ROLE PIN  (required — a 3-line pin naming the role file's version + sha256, NOT the
     role file itself; the role is RESIDENT in the browser project instructions since
     HANDOFF_PROCESS v6.3.0 / census R1. See _role_pin below.)
  2. <bundle>/RESIDUAL.md       (required — drift-flags + planning why + task-graph)
  3. <bundle>/PROBES.md         (required — orientation + teeth probes)
  4. <bundle>/SUPPLEMENT.md     (architect strategic supplement — an always-generated
     fillable file; only its filled-in ANSWERS region folds in, and only when non-empty,
     since the QUESTIONS are for the OUTGOING browser, not the incoming session)

Output: <bundle>/PASTE_THIS.md  (UTF-8, LF, never hand-edited)
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import click

_SECTION_SEP = "\n\n---\n\n"

# CUT-3 ([#611], lane-g-611-bundle-thinning, 2026-09-02): the REAL, immutable ceiling on an
# assembled PASTE_THIS.md — 20,000 bytes. This constant is now the SOLE declared PASTE_THIS
# byte budget in the repo; PUBLIC (no leading underscore) because scripts/window_metrics.py
# imports it rather than re-declaring its own number.
#
# RETIRED HERE, IN THE SAME COMMIT: `_SIZE_WARN_BYTES = 48_000` (this constant, prior value)
# and `window_metrics.collect`'s `paste_budget: int = 65_000` default — two numbers claiming
# to be the same budget, computed independently and never reconciled (65,000 − the since-retired
# ~17,196 B inline role file ≈ 47,800 ≈ the "independently re-derived" 48,000 here — the same
# arithmetic, done twice, drifting apart only because nothing forced the two sites to agree).
# One number now; window_metrics imports THIS one rather than declaring its own.
#
# A WARN, not a gate — assembly still succeeds, mirroring check_boot_byte_budget's split-by-site
# pattern (WARN at generation, a FAIL-class gate — if the operator wants one — belongs in
# audit.py, out of this lane's write-scope).
PASTE_BYTE_CEILING = 20_000

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


# --- the ROLE PIN (HANDOFF_PROCESS v6.3.0; census R1 mechanism, operator ruling D-R1) ----
#
# WHAT CHANGED AND WHY. Through v6.2.0 the assembler INLINED the whole of
# `protocols/HANDOFF_BOOT.md` into every paste — ~17 KB of role text re-transmitted on
# every handoff, to a browser that could simply HOLD it. v6.3.0 makes the role
# RESIDENT: the operator installs `protocols/HANDOFF_BOOT.md` once as the browser
# project's instructions, and the paste ships a three-line PIN instead.
#
# The "role MUST reach the browser" requirement of HANDOFF_PROCESS is UNCHANGED. What
# changes is the mechanism that satisfies it: residency, guarded by a refusal. The pin
# names the version and the sha256 of the exact role file this bundle was cut against,
# and instructs the seat to REFUSE rather than proceed if what it holds does not match.
# That is why the third line is not decoration — without it, residency degrades silently
# when the resident copy drifts, and a silent mismatch is strictly worse than a heavy
# paste. A pin without teeth would be a size optimisation bought with a correctness hole.
_ROLE_REFUSAL = ("If your project instructions do not carry this contract at this "
                 "version+sha, say so before answering.")


def _role_pin(role_path: Path, version: str) -> str:
    """The 3-line role PIN: identity, integrity, refusal.

    sha256 is computed over the file's RAW BYTES, so it is insensitive to how the
    reader's platform would render newlines and matches what `sha256sum` reports.
    """
    digest = hashlib.sha256(role_path.read_bytes()).hexdigest()
    return "\n".join((
        f"ROLE PIN — {role_path.name} @ handoff-process v{version}",
        f"sha256: {digest}",
        _ROLE_REFUSAL,
    ))


_VERSION_RE = re.compile(r"^Version:\s+v?(\d+\.\d+(?:\.\d+)?)", re.MULTILINE)


def _spec_version(repo_root: Path) -> str:
    """The live HANDOFF_PROCESS version — read, never hard-coded.

    A hard-coded constant here is exactly the coupled-version surface the
    `reconciled_versions` / `handoff_version_stamp` organs exist to police, so the
    assembler reads the spec instead of carrying a copy to go stale (the
    de-hardcode-first doctrine, PLAYBOOK amendment_coherence honest limits).
    """
    spec = repo_root / "protocols" / "HANDOFF_PROCESS.md"
    # Fail CLOSED, and cleanly. Both arms exit 1 with a named reason rather than a
    # traceback: the pin's whole value is that it vouches for an identity, so an
    # unknown version must refuse loudly instead of shipping an unverifiable pin.
    if not spec.exists():
        click.echo("[error] protocols/HANDOFF_PROCESS.md is missing — the ROLE PIN needs its "
                   "Version line; refusing rather than pinning an unknown version", err=True)
        sys.exit(1)
    m = _VERSION_RE.search(spec.read_text(encoding="utf-8"))
    if not m:
        click.echo("[error] protocols/HANDOFF_PROCESS.md: no parseable 'Version:' line — "
                   "the ROLE PIN cannot be built without it", err=True)
        sys.exit(1)
    return m.group(1)


# --- the window-specific ratio ([#611]; derivation: docs/audits/2026-09-02-technical- ---
# --- lane-g-611-bundle-thinning.md §1.2) ------------------------------------------------
#
# DEFINITION. A byte is window-specific iff it lands inside content this repo's own
# generator already marks as hand-authored: a FILL-IN region body (gen_handoff.FILL_IN_RE
# -- RF-6's own hand-authored/generator-output boundary, reused rather than re-declared),
# or the folded SUPPLEMENT ANSWERS section (100% operator/architect-typed by construction,
# already isolated by _extract_answers above). Everything else -- headings, table
# scaffolding, static callouts, {{TOKEN}} substitutions, and all of PROBES.md (zero
# FILL-IN regions in any mode) -- is generator output and reads 0.
#
# An UNFILLED FILL-IN region's body is the generator's own `_(fill: ...)_` placeholder
# prompt (uniform across every template in templates/handoff/v5/*.tmpl) -- generic
# boilerplate the operator has not yet replaced, excluded rather than counted.
_PLACEHOLDER_RE = re.compile(r"\A\s*_\(fill:.*\)_\s*\Z", re.DOTALL)


def _fill_in_bytes(text: str) -> int:
    """Window-specific bytes in TEXT: the summed UTF-8 length of every FILL-IN region's
    BODY (never the `<!-- FILL-IN:... -->` marker comments themselves -- those are
    generator instructions, not window content), excluding an unfilled placeholder body."""
    from gen_handoff import FILL_IN_RE  # noqa: PLC0415 (sibling CLI; deferred import)
    total = 0
    for m in FILL_IN_RE.finditer(text):
        body = m.group("body")
        if _PLACEHOLDER_RE.match(body):
            continue
        total += len(body.encode("utf-8"))
    return total


def window_specific_bytes(sections: list[tuple[str, str]], answers_label: str = "SUPPLEMENT.md") -> int:
    """Window-specific bytes summed across every FOLDED section. The SUPPLEMENT ANSWERS
    section is not FILL-IN-tagged but is counted whole, by the same construction (see
    module note above); every other section is scanned for FILL-IN region bodies."""
    total = 0
    for label, text in sections:
        total += len(text.encode("utf-8")) if label == answers_label else _fill_in_bytes(text)
    return total


# --- P11 leg 2: an OPEN carrier is discharged by the RESIDUAL, and only here ([#643]) -----
#
# WHY THIS GATE IS AT ASSEMBLY AND NOT AT PREFLIGHT. P11 has two legs and they do not become
# checkable at the same moment. Leg 1 — a flush-left `carried-by:` whose value resolves on
# `main` — reads only the transport and `main`, so it refuses BEFORE the cut, as preflight row
# `p11_carriage` in gen_handoff.py. Leg 2 is the other arm of the same disjunction: a value
# that is the literal `OPEN` discharges P11 *only* by being NAMED in this bundle's residual —
# and the residual does not exist when preflight runs. It is written by the generator as a
# fillable file and filled by the operator afterwards. ASSEMBLY IS THE FIRST MOMENT BOTH
# OPERANDS EXIST, which is what makes it the first moment the conjunct can be tested at all.
# One preflight row claiming to cover both legs would be the false completeness P11 exists to
# catch — the shape row 1 already documents for its own second conjunct.
#
# WHAT IT COST TO NOT HAVE THIS. Measured 2026-09-08: `2026-09-08-dev-knowledge-architect` and
# its `-2` successor failed P11 on the SAME 25-file transport, five files each time, because
# nothing between them tested carriage before the bundle was written. A committed handoff is
# immutable, so each discovery cost a superseding cut.
#
# ONLY THE `OPEN` KIND IS JUDGED HERE. A file whose value names a home was leg 1's subject and
# was already refused-or-passed before the cut; re-judging it would put one predicate in two
# places, free to disagree about the same file. The shortfall itself comes from
# `gen_handoff.carriage_shortfall`, which BOTH stages call — there is one predicate, not two.
#
# Family precedent for a handoff refusing debt, cited in the refusal the operator reads:
# `DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08` / `DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08`.
# A window may hand off with debt only when the debt is explicit and owned.

#: The bundle home a real cut lands in. HONEST LIMIT, and it is why the gate is scoped rather
#: than universal: `assemble_paste.py` also runs over ad-hoc directories (fixtures, one-off
#: assemblies) that are not a window's handoff and carry no residual duty. A gate that refused
#: those would be measuring something it was never given.
_BUNDLE_HOME_PARTS = ("docs", "handoffs")


def _is_window_bundle(bundle_dir: Path, repo_root: Path) -> bool:
    """True when `bundle_dir` is `<repo_root>/docs/handoffs/<slug>` — a real cut's home."""
    try:
        rel = bundle_dir.resolve().relative_to(repo_root.resolve())
    except (ValueError, OSError):
        return False
    return len(rel.parts) >= 3 and rel.parts[:2] == _BUNDLE_HOME_PARTS


# rule: handoff-open-carrier-named
def assert_open_carriers_named(bundle_dir: Path, repo_root: Path) -> None:
    """Refuse assembly while an `OPEN` decision file is unnamed in the filled residual.

    Exits 1 before `PASTE_THIS.md` is written, which is the whole point: the refusal has to
    land while the bundle is still repairable.

    HONEST LIMIT, stated rather than left to be discovered. `gen_handoff.generate(assemble=True)`
    spawns this script with `check=False`, so a refusal here does NOT propagate as a non-zero
    `generate()`. What it produces is the thing that actually stops the handoff: **no
    `PASTE_THIS.md`**, plus this block on stderr. A bundle with no assembled paste cannot be
    pasted, and `/handoff` runs the assembler in the operator's own terminal where the refusal
    is read. Making `generate` propagate the code is a change to the generate path, which is
    outside this gate's scope; the guarantee it needs — the paste is not produced — holds
    either way, and this note exists so nobody reads the swallowed exit code as a hole nobody
    noticed.
    """
    # Deferred, sibling-CLI import — the same idiom `reflow_framing` / `FILL_IN_RE` already use.
    from gen_handoff import (  # noqa: PLC0415
        CARRIAGE_OPEN,
        carriage_shortfall,
        transport_root,
    )
    if not _is_window_bundle(bundle_dir, repo_root):
        return
    residual = bundle_dir / "RESIDUAL.md"
    if not residual.exists():
        return              # the required-source check below reports the absence itself
    transport = transport_root()
    if transport is None:
        click.echo("[error] P11 leg 2 could not be measured: CLAUDE_PROMPTS_DIR is UNRESOLVED "
                   "and ~/Downloads is not a directory either, so the decision files this "
                   "bundle must carry cannot be read. An unknown boundary is not a clean one "
                   "(DEFECT E-29) — refusing rather than assembling on an unmeasured window.",
                   err=True)
        sys.exit(1)
    text = residual.read_text(encoding="utf-8", errors="replace")
    unnamed = [v for v in carriage_shortfall(transport, repo_root, residual=text)
               if v.kind == CARRIAGE_OPEN]
    if not unnamed:
        return
    click.echo(f"[error] P11 leg 2: {len(unnamed)} decision file(s) state `carried-by: OPEN` "
               f"and are named nowhere in {residual.name}. An OPEN carrier discharges P11 only "
               "by being named in this bundle's residual — a window may hand off with debt, "
               "never with debt that is silent (DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / "
               "DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08). Refusing to assemble; a committed "
               "bundle is immutable and the only later repair is a superseding cut.", err=True)
    for v in unnamed:
        click.echo(f"  | {v.path.parent.name}/{v.path.name}", err=True)
    sys.exit(1)


@click.command()
@click.option("--pin-only", is_flag=True,
             help="Print only the 3-line ROLE PIN and exit (v7 /boot-session use — "
                  "HANDOFF_PROCESS.md §17.4: the same pin mechanism §4 uses, reused rather "
                  "than duplicated, so a boot-session paste and a v5/v6 bundle paste never "
                  "carry two independently-computed pins).")
@click.argument("bundle_dir", required=False,
                type=click.Path(exists=True, file_okay=False, path_type=Path))
def main(pin_only: bool, bundle_dir: Path | None) -> None:
    """Assemble PASTE_THIS.md for BUNDLE_DIR from canonical sources, or (--pin-only) print
    just the ROLE PIN."""
    repo_root = Path(__file__).parent.parent

    if pin_only:
        role_path = repo_root / "protocols" / "HANDOFF_BOOT.md"
        if not role_path.exists():
            click.echo(f"[error] Required source missing: {role_path}", err=True)
            sys.exit(1)
        click.echo(_role_pin(role_path, _spec_version(repo_root)))
        return
    if bundle_dir is None:
        raise click.UsageError("BUNDLE_DIR is required unless --pin-only is given.")

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

    # P11 leg 2, and it runs FIRST — after the fill-state flip (so the residual read here is
    # the FILLED one) and before a single byte of PASTE_THIS.md is composed. A refusal is only
    # worth having while the bundle is still repairable.
    assert_open_carriers_named(bundle_dir, repo_root)

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

    # 1. ROLE PIN — the role file is RESIDENT, not inlined (v6.3.0; census R1, ruling D-R1).
    role_path = repo_root / "protocols" / "HANDOFF_BOOT.md"
    if not role_path.exists():
        click.echo(f"[error] Required source missing: {role_path}", err=True)
        sys.exit(1)
    role_text = role_path.read_text(encoding="utf-8")
    # rule: handoff-boot-budget
    # A10 item 2 / R4: the browser role file carries a stated numeric byte budget. The budget
    # SURVIVES the residency flip and is deliberately unchanged: the role file still has to fit
    # a browser project-instructions field, and it is now read by EVERY session of that project
    # rather than once per paste, so its size matters more, not less. WARN here (assembly
    # proceeds); audit.py::check_boot_byte_budget is the FAIL-class organ that blocks the merge.
    boot_bytes = len(role_text.encode("utf-8"))
    if boot_bytes > HANDOFF_BOOT_BYTE_BUDGET:
        click.echo(f"[warn] protocols/HANDOFF_BOOT.md is {boot_bytes} bytes "
                   f"(> budget {HANDOFF_BOOT_BYTE_BUDGET}) — trim the browser role file; "
                   "audit.py check_boot_byte_budget FAILs the ship-gate on this "
                   "(A10 item 2 / R4)", err=True)
    sections.append(("ROLE PIN (protocols/HANDOFF_BOOT.md — RESIDENT, not inlined)",
                     _role_pin(role_path, _spec_version(repo_root))))
    click.echo(f"[pin] role file NOT inlined: {boot_bytes} bytes replaced by a 3-line pin "
               "(v6.3.0 residency; install protocols/HANDOFF_BOOT.md as the browser project's "
               "instructions once — protocols/OPERATOR-INTERFACE.md)", err=True)

    # 2-3. Required sources (inlined verbatim — the file-less browser must RECEIVE these).
    required: list[tuple[str, Path]] = [
        ("RESIDUAL.md", bundle_dir / "RESIDUAL.md"),
        ("PROBES.md", bundle_dir / "PROBES.md"),
    ]
    for label, path in required:
        if not path.exists():
            click.echo(f"[error] Required source missing: {path}", err=True)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
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
    # CUT-3 / [#611]: the ratio is measured over the SAME sections list, against the SAME
    # content_bytes denominator already computed above for the END sentinel -- one span,
    # never two disagreeing measurements.
    ws_bytes = window_specific_bytes(sections)
    ws_pct = round(ws_bytes * 100 / content_bytes) if content_bytes else 0
    click.echo(f"Written: {paste_path} ({size} bytes; window-specific {ws_bytes}/{content_bytes} "
               f"B = {ws_pct}%)")
    if size > PASTE_BYTE_CEILING:
        click.echo(f"[warn] PASTE_THIS.md is {size} bytes (> {PASTE_BYTE_CEILING}) — heavy boot; "
                   "check for re-narration creep (RF-2/RF-6) before shipping; artifacts other "
                   "than PASTE_THIS must not be pasted at all (intake #18 A2)", err=True)


if __name__ == "__main__":
    main()
