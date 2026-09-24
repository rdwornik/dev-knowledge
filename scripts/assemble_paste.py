#!/usr/bin/env python3
"""Assemble PASTE_THIS.md from a v5 handoff bundle's canonical sources.

Usage: python scripts/assemble_paste.py <bundle_dir>

Manifest (in order):
  0. <bundle>/HANDOFF_BOOT.md session-header (optional; extracted from the bundle's
     own HANDOFF_BOOT.md up to the first '##' heading — slug/mode/purpose/generated-at;
     its `>` pointer blocks are SHED to one forms line, see _shed_header)
  1. ROLE PIN  (required — a 3-line pin naming the role file's version + sha256, NOT the
     role file itself; the role is RESIDENT in the browser project instructions since
     HANDOFF_PROCESS v6.3.0 / census R1. See _role_pin below.)
  2. <bundle>/RESIDUAL.md       (required — SHED to drift-flags + the OPEN list + a pointer
     to the rest and to the live ledger, see shed_residual)
  3. <bundle>/PROBES.md         (required — orientation + teeth probes)
  4. <bundle>/SUPPLEMENT.md     (architect strategic supplement — when its ANSWERS region is
     filled, a POINTER section names it; the answers themselves are pulled JIT, not inlined)

DECISION_LEDGER.md is never folded: the live ledger on the transport supersedes the snapshot.

THE PASTE GATE (LANE-5A-9): an assembled paste above PASTE_BYTE_CEILING is REFUSED — exit 1,
no PASTE_THIS.md written, a stale one replaced by a refusal notice.

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
# A GATE since LANE-5A-9 (2026-09-24), no longer a WARN. The WARN let the live paste reach
# 34,998 B — 75 % over — with nothing stopping it (DIGEST-HANDOFF-READINESS-2026-09-23 §4 item 3).
# The shed below brought the same bundle under it, so the ceiling can refuse without refusing
# the documented flow. Unlike the boot budget, the refusal sits HERE: the paste has no later
# merge gate to catch it — it is handed to a browser, not shipped through the ship-gate.
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


# --- the SHED (LANE-5A-9; DIGEST-HANDOFF-READINESS-2026-09-23 §4 "SHED") ------------------
#
# WHAT THE PASTE IS FOR. The browser re-reads the whole paste on every turn of the window, so a
# byte in it is billed per turn, and prose the seat reads once belongs one hop away. The live
# 2026-09-19 paste measured 34,998 B: the SUPPLEMENT answers (11.5 KB) and the RESIDUAL's
# narrative sections were inlined whole, and the header carried three pointer paragraphs — one
# of them naming PLAYBOOK Ch8 as the launch authority, which ruling O-5 (RATIFICATION
# 2026-09-23-playbook) withdrew. The shed keeps what a seat needs on turn one and POINTS at the
# rest; nothing is lost, because CC holds every file and pulls it on request.

#: The ONE forms line the session header's pointer blocks collapse into. Code and data describe
#: themselves (O-5): the launcher's own --help, the four seat templates, the routing registry.
FORMS_LINE = (
    "> **Forms by pointer — code and data describe themselves (O-5).** Launch: "
    "`uv run --locked python scripts/dispatch.py launch --help` · seat orders + lane contract: "
    "`templates/dispatcher-order-template.md`, `templates/integrator-order-template.md`, "
    "`templates/batch-common-rules-template.md`, `templates/lane-contract-template.md` · "
    "routing: `ecosystem/provider-registry.yaml` · rules: `protocols/STANDING_RULINGS.md` · "
    "runbook: `docs/handoffs/README.md`. Ask CC to pull any of them.")


def _shed_header(header: str) -> str:
    """The session header with every `>` pointer block replaced by the ONE forms line.

    The title and the Field/Value table (slug, mode, purpose, destination) stay verbatim: they
    are this window's own facts. The `>` blocks are the generator's doctrine pointers, and one
    of them — the fill-state banner — says the ANSWERS "fold into PASTE_THIS.md", a claim the
    supplement pointer below made false. A header with no `>` block gains no line."""
    lines = header.splitlines()
    if not any(ln.startswith(">") for ln in lines):
        return header
    kept = [ln for ln in lines if not ln.startswith(">")]
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).rstrip()
    return f"{body}\n\n{FORMS_LINE}"


_H2_SPLIT_RE = re.compile(r"^(?=## )", re.MULTILINE)
_DRIFT_HEADING_RE = re.compile(r"(?i)^## [^\n]*drift")
#: A transport-qualified decision-file path as a residual writes it — the same `to-cc/NAME.md`
#: form `gen_handoff._residual_names` reads (either separator; a Windows paste writes `\`).
_QUALIFIED_RE = re.compile(r"\bto-(?:cc|browser)[/\\][\w.\-]+\.md\b")


def _bundle_ref(bundle_dir: Path, repo_root: Path, name: str) -> str:
    """`docs/handoffs/<slug>/<name>` when the bundle is in the repo, else `<dir>/<name>`."""
    try:
        rel = bundle_dir.resolve().relative_to(repo_root.resolve())
    except (ValueError, OSError):
        rel = Path(bundle_dir.name)
    return f"{rel.as_posix()}/{name}"


def open_list(bundle_dir: Path, repo_root: Path, residual: str) -> list[str]:
    """The OPEN decision files this handoff carries, transport-qualified.

    In a real bundle home the set is READ OFF THE TRANSPORT with P11's own helpers
    (`gen_handoff.decision_files` + `carried_by_value` + its anchored OPEN predicate), so it is
    complete by construction and cannot shrink with the shed: a residual that named a file in a
    section the shed drops still hands that file on. Anywhere else — a fixture, an ad-hoc
    directory, no transport — it is the qualified paths the residual itself names."""
    if _is_window_bundle(bundle_dir, repo_root):
        from gen_handoff import (  # noqa: PLC0415 (sibling CLI; deferred import)
            _OPEN_VALUE_RE,
            carried_by_value,
            decision_files,
            transport_root,
        )
        transport = transport_root()
        if transport is not None:
            return [f"{p.parent.name}/{p.name}" for p in decision_files(transport)
                    if _OPEN_VALUE_RE.match(carried_by_value(p) or "")]
    return list(dict.fromkeys(m.replace("\\", "/") for m in _QUALIFIED_RE.findall(residual)))


def shed_residual(text: str, opens: list[str], residual_ref: str) -> str:
    """RESIDUAL shed to: its title, the drift-flags section(s), the OPEN list, and a pointer.

    A residual with no `## ` sections is a hand residual with nothing to shed and is returned
    whole. The pointer names the full residual (shipped map, next-frontier "why", task-state)
    and the LIVE ledger — `to-browser/LEDGER-<repo>.md` — rather than the bundle's
    DECISION_LEDGER.md snapshot, which the digest found presenting itself as the ledger."""
    parts = _H2_SPLIT_RE.split(text)
    preamble, sections = parts[0], parts[1:]
    if not sections:
        return text.rstrip()
    title = next((ln for ln in preamble.splitlines() if ln.startswith("# ")), "# Residual")
    kept = [re.sub(r"\n-{3,}\s*\Z", "", s.rstrip()).rstrip()
            for s in sections if _DRIFT_HEADING_RE.match(s)]
    if not kept:
        kept = ["_(this residual has no drift-flags section — ask CC to pull it)_"]
    listing = "\n".join(f"- `{p}`" for p in opens) if opens else "- _(none)_"
    open_block = ("**OPEN decision files this handoff carries** (`carried-by: OPEN` — work, "
                  f"not filing; P11):\n{listing}")
    pointer = (f"**The rest of this residual is not inlined** (the paste gate): the shipped map, "
               f"the next-frontier decisions and task-state are in `{residual_ref}` — ask CC to "
               "pull it. The live decision ledger is `to-browser/LEDGER-<repo>.md` on the "
               "transport; the bundle's `DECISION_LEDGER.md` is a snapshot, never pasted.")
    return "\n\n".join([title, *kept, open_block, pointer])


def supplement_pointer(supplement_ref: str) -> str:
    """The SUPPLEMENT section: the ANSWERS are filled and live at `supplement_ref`.

    The section keeps its `=== SUPPLEMENT.md ===` label so `audit.py::supplement_folded` still
    sees the answers REACH the paste — by a pointer the seat acts on, rather than 11 KB it is
    billed for on every turn."""
    return (f"The outgoing architect's ANSWERS are FILLED, in `{supplement_ref}` below its "
            "divider — not inlined (the paste gate). Ask CC to pull them before the §13(d) "
            "operator-context beat, which then NARROWS to *\"anything changed since the "
            "supplement was written?\"*.")


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


def _invalidate_stale_paste(bundle_dir: Path, unnamed) -> None:
    """Overwrite an EXISTING PASTE_THIS.md with a refusal stub naming what is owed.

    THE ARTEFACT A REFUSAL LEAVES BEHIND, and it only became a hole once the cold pass was
    allowed to write a paste. The cold cut assembles PASTE_THIS.md and defers; the operator
    fills the bundle, names no carrier, re-runs; this function's caller refuses and exits
    BEFORE rewriting the paste. Without this, that complete, pasteable cold artifact is still
    on disk and the operator ships the very thing the gate refused (terra, 2026-09-09).

    INVALIDATED, NOT DELETED, and both halves of that are deliberate. This script owns
    PASTE_THIS.md outright — its own header says the file is never hand-edited — so replacing
    its contents is within its remit where deleting an operator's file would not be. And a stub
    that says REFUSED is louder than an absence: a missing file reads as "the tool did not
    run", while this one carries its own repair instructions to whoever opens it.

    ONLY WHEN ONE ALREADY EXISTS. A refusal on a bundle that never had a paste still leaves
    none, which is the guarantee the cold-cut tests assert and it is not weakened here.
    """
    paste = bundle_dir / "PASTE_THIS.md"
    if not paste.exists():
        return
    owed = "\n".join(f"  - {v.path.parent.name}/{v.path.name}" for v in unnamed)
    paste.write_text(
        "=== THIS HANDOFF WAS REFUSED — DO NOT PASTE ===\n\n"
        "P11 leg 2 refused this bundle, and the assembled paste that used to be here has been\n"
        "replaced by this notice. It was written by an earlier COLD pass, before the residual\n"
        "was filled, and pasting it would ship the handoff the gate just refused.\n\n"
        "These decision files state `carried-by: OPEN` and are named nowhere in RESIDUAL.md:\n"
        f"{owed}\n\n"
        "Name each one in this bundle's RESIDUAL.md — the transport-qualified path, e.g.\n"
        "`to-cc/<file>.md` — then re-run scripts/assemble_paste.py on this directory. A window\n"
        "may hand off with debt; it may never hand off with debt that is silent.\n",
        encoding="utf-8", newline="\n")
    click.echo(f"  -> the stale PASTE_THIS.md from the cold pass was REPLACED with a refusal "
               f"notice; {paste} is not pasteable", err=True)


def _invalidate_oversized_paste(bundle_dir: Path, size: int) -> None:
    """The paste-gate twin of `_invalidate_stale_paste`: same remit, same only-if-it-exists
    rule, so an over-ceiling refusal never leaves an earlier pasteable file behind."""
    paste = bundle_dir / "PASTE_THIS.md"
    if not paste.exists():
        return
    paste.write_text(
        "=== THIS HANDOFF WAS REFUSED — DO NOT PASTE ===\n\n"
        f"The assembled paste measured {size} bytes, over the {PASTE_BYTE_CEILING}-byte ceiling\n"
        "(scripts/assemble_paste.py PASTE_BYTE_CEILING), and the paste that used to be here was\n"
        "replaced by this notice. Shed the largest section — move prose behind a pointer — then\n"
        "re-run scripts/assemble_paste.py on this directory.\n",
        encoding="utf-8", newline="\n")
    click.echo(f"  -> the stale PASTE_THIS.md was REPLACED with a refusal notice; {paste} is "
               "not pasteable", err=True)


# rule: handoff-open-carrier-named
def _residual_is_an_untouched_render(text: str) -> bool:
    """True when EVERY FILL-IN region in `text` still holds the generator's own placeholder.

    This is what "the cold pass" actually means, DERIVED from the artifact rather than taken
    on trust from a caller. A template render satisfies it by construction; the moment the
    operator writes into any region it stops holding, so a PARTIALLY filled residual is judged
    rather than exempt -- strictly tighter than the flag this replaced.

    A residual with NO FILL-IN regions is not an untouched render and returns False: absence of
    regions is not evidence of innocence, and this predicate gates a refusal.
    """
    from gen_handoff import FILL_IN_RE  # noqa: PLC0415 (sibling CLI; deferred import)
    bodies = [m.group("body") for m in FILL_IN_RE.finditer(text)]
    return bool(bodies) and all(_PLACEHOLDER_RE.match(b) for b in bodies)


def assert_open_carriers_named(bundle_dir: Path, repo_root: Path) -> None:
    """Refuse assembly while an `OPEN` decision file is unnamed in the filled residual.

    Exits 1 before `PASTE_THIS.md` is written, which is the whole point: the refusal has to
    land while the bundle is still repairable.

    TWO PASSES, and only the second is judged. The assembler runs once inside the cut
    (spawned by `gen_handoff._run_assembler`) and again when the operator
    re-runs it after filling. On the first pass `RESIDUAL.md` is a template render from seconds
    earlier and can name nothing, so the gate DEFERS -- printing what is owed rather than
    refusing. Judging there would refuse every cut on a window carrying any `OPEN` debt, which
    is the documented default flow, not an edge case. This is leg 2's own reasoning applied one
    stage further in: a conjunct is judged where both operands exist, and nowhere earlier.

    THE EXIT CODE NOW PROPAGATES, and the correction is recorded because this docstring
    previously argued it did not need to. `gen_handoff.generate(assemble=True)` spawned this
    script with `check=False` and returned a GenResult regardless, so the standard cut command
    printed `Generated bundle` and exited 0 on a bundle this function had just refused. The
    old note reasoned that no `PASTE_THIS.md` was guarantee enough — a bundle with no
    assembled paste cannot be pasted. That reasoning was wrong in the way understated risks
    usually are: it priced the missing FILE and ignored the false RECEIPT beside it, and a
    receipt saying the cut is clean is acted on, while an absent one is not. Terra HIGH,
    2026-09-09. `gen_handoff._run_assembler` returns this exit code and `generate()` raises
    `AssemblyRefusedError` on any non-zero, which `main` renders as one `[error]` line and a
    non-zero exit.
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
    # BOTH LEGS, and the second closes the bypass the first one left. A residual-only test
    # defers whenever the residual is untouched -- including on the POST-FILL run, when the
    # operator has filled SUPPLEMENT.md and simply left every RESIDUAL.md placeholder alone.
    # That is the documented assembly step, so the gate would be skipped exactly where it is
    # supposed to bite (terra, 2026-09-09). The bundle's own fill state is the discriminator,
    # read through `detect_fill_state` -- the ONE definition, which itself reuses
    # `_extract_answers` above so the framing flip and this gate cannot disagree about what
    # "filled" means.
    #
    # Deferral therefore needs the bundle to be cold ALL THE WAY: nothing folded, and no region
    # written. Anything else is judged.
    from gen_handoff import detect_fill_state  # noqa: PLC0415 (sibling CLI; deferred import)
    if not detect_fill_state(bundle_dir) and _residual_is_an_untouched_render(text):
        # THE FIRST OF TWO PASSES, and the residual it would judge is a template render from
        # seconds ago. `.claude/commands/handoff.md` states the flow: the operator fills the
        # supplement, "then commit the filled file and re-run scripts/assemble_paste.py". Only
        # that second run has both operands. Refusing here refuses every cut on a window
        # carrying ANY `OPEN` debt -- eight files on the live transport today -- which is the
        # documented default flow, not an edge case.
        #
        # This is the same reasoning that put leg 2 at assemble time rather than at preflight,
        # applied one stage further in: judge a conjunct where both of its operands exist, and
        # nowhere earlier. It is a DEFERRAL, not an exemption -- the post-fill run below is
        # unchanged, and `test_the_post_fill_pass_still_refuses_the_same_bundle` pins that the
        # identical bundle still refuses there.
        #
        # LOUD, because a silent skip is the failure mode this lane was sent to fix. The
        # operator is told which files they owe while the bundle is still repairable.
        click.echo(f"[defer] P11 leg 2: {len(unnamed)} decision file(s) state `carried-by: "
                   "OPEN` and are named nowhere in this bundle's RESIDUAL.md yet. NOT a pass "
                   "-- the residual was rendered moments ago and cannot name anything. Name "
                   "each of these in RESIDUAL.md before you re-run this assembler after "
                   "filling; that run REFUSES on what is still missing.", err=True)
        for v in unnamed:
            click.echo(f"  | {v.path.parent.name}/{v.path.name}", err=True)
        return
    click.echo(f"[error] P11 leg 2: {len(unnamed)} decision file(s) state `carried-by: OPEN` "
               f"and are named nowhere in {residual.name}. An OPEN carrier discharges P11 only "
               "by being named in this bundle's residual — a window may hand off with debt, "
               "never with debt that is silent (DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / "
               "DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08). Refusing to assemble; a committed "
               "bundle is immutable and the only later repair is a superseding cut.", err=True)
    for v in unnamed:
        click.echo(f"  | {v.path.parent.name}/{v.path.name}", err=True)
    _invalidate_stale_paste(bundle_dir, unnamed)
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
            sections.append(("HANDOFF_BOOT.md (session header)", _shed_header(header)))

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

    # 2-3. Required sources. PROBES.md is inlined verbatim (the file-less browser must RECEIVE
    #      its rows); RESIDUAL.md is SHED — drift-flags + the OPEN list + a pointer (LANE-5A-9).
    required: list[tuple[str, Path]] = [
        ("RESIDUAL.md", bundle_dir / "RESIDUAL.md"),
        ("PROBES.md", bundle_dir / "PROBES.md"),
    ]
    for label, path in required:
        if not path.exists():
            click.echo(f"[error] Required source missing: {path}", err=True)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        if label == "RESIDUAL.md":
            text = shed_residual(text, open_list(bundle_dir, repo_root, text),
                                 _bundle_ref(bundle_dir, repo_root, "RESIDUAL.md"))
        sections.append((label, text.rstrip()))

    # 4. SUPPLEMENT.md — the architect strategic supplement (an always-generated fillable
    #    file). Only a filled-in ANSWERS region earns a section, and since LANE-5A-9 that
    #    section is a POINTER to the answers, not the answers: the QUESTIONS are for the
    #    OUTGOING browser, and an empty ANSWERS section (a cold or not-yet-filled handoff) is
    #    the defined N/A disposition. CC never fabricates answers — by design.
    supplement = bundle_dir / "SUPPLEMENT.md"
    if supplement.exists():
        answers = _extract_answers(supplement.read_text(encoding="utf-8"))
        if answers:
            sections.append(("SUPPLEMENT.md", supplement_pointer(
                _bundle_ref(bundle_dir, repo_root, "SUPPLEMENT.md"))))
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
    size = len(body.encode("utf-8"))
    # THE PASTE GATE (LANE-5A-9): measured before a byte is written, so a refused paste never
    # exists as a file. Each section's size is printed so the repair names its largest term.
    if size > PASTE_BYTE_CEILING:
        click.echo(f"[error] the assembled paste is {size} bytes, over the {PASTE_BYTE_CEILING}-"
                   "byte ceiling (PASTE_BYTE_CEILING). Refusing to write PASTE_THIS.md — shed "
                   "the largest section behind a pointer (RF-2/RF-6) and re-run. Sections:",
                   err=True)
        for label, content in sections:
            click.echo(f"  | {len(content.encode('utf-8'))} B  {label}", err=True)
        _invalidate_oversized_paste(bundle_dir, size)
        sys.exit(1)
    paste_path.write_text(body + "\n", encoding="utf-8", newline="\n")
    # CUT-3 / [#611]: the ratio is measured over the SAME sections list, against the SAME
    # content_bytes denominator already computed above for the END sentinel -- one span,
    # never two disagreeing measurements. The SUPPLEMENT section is a generated pointer since
    # LANE-5A-9, so no section is counted whole any more (`answers_label=""`).
    ws_bytes = window_specific_bytes(sections, answers_label="")
    ws_pct = round(ws_bytes * 100 / content_bytes) if content_bytes else 0
    click.echo(f"Written: {paste_path} ({size} bytes; window-specific {ws_bytes}/{content_bytes} "
               f"B = {ws_pct}%)")


if __name__ == "__main__":
    main()
