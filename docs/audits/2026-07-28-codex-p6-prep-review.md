# Terra review — P6 dated-pressure prep artifacts (Parts 1–4)

- **Class:** codex (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** p6-prep-review
- **Lane:** `codex exec review -m gpt-5.6-terra` (codex-cli 0.145.0), prompt-mode DOC profile (the
  `--base`-XOR-prompt contract; adversarial brief: "forgetting dressed as retiring" in the drain prep,
  underpriced options in the sizing/matrix artifacts, boundary blur + unanchored claims in all four).
- **Subject:** the four prep artifacts at `b35c9090` (Part 5, the D-queue list, was declared out of scope in
  the brief — it is a derivation list, not a proposal surface).
- **Producer ≠ reviewer:** artifacts authored by the CC session; review by terra; session id
  `019faa6b-3443-7780-aed2-50bd332a049c`.

## Verdict

**0 P1 · 3 P2 · 1 P3 — ALL FOUR ADOPTED AND FIXED in the follow-up commit on this branch; none dispositioned
away.**

## Findings + dispositions

1. **[P2] drain-slice-prep — the [#360] retire recommendation lacked ADR-85's required evidence.** "Its ADR-85
   stabilization purpose was served" was unsupported: ADR-85 §Decision item 6 froze the doc set to *gather
   reliability/override-rate data first* (`DEFINITION_OF_DONE.md:107-109` still states the condition); reaching
   the date does not show the purpose met. **FIXED:** the disposition is now two-step and conditional — check
   the override-log/gate-reliability record first; retire only on that data; renew-with-owner if the data was
   never collected. The exact "forgetting dressed as retiring" class the brief targeted — caught in the one
   place it appeared.
2. **[P2] 382-charter — the dependency map drew [#387] as an unconditional predecessor.** The live row
   (`tasks/387-*.md`) binds only "before any ADR cites it", and the charter's own ordering note said so — the
   diagram contradicted its own text. **FIXED:** the edge is now drawn conditional (binds only if the [#382]
   ADR cites intake #2), matching the note.
3. **[P2] vscode-sizing — option (c) priced "~0".** Its outcome edits `review_date`s in BOTH consumers'
   `.methodology.yaml` — consumer writes under RULING-W + merge delegation — plus the hub W1 deadline;
   near-zero pricing skewed the comparison. **FIXED:** re-priced **S (cross-repo, no build)** with the
   mechanics named.
4. **[P3] 364-cap-option-matrix — option 4(a) omitted the per-incident artifact cost.** The linked
   `incident-evidence` file must be created, reviewed, indexed and retained (immutable class) per accumulating
   incident; the validator's scope (`validate_doc_rot.py:91-107`, BACKLOG task lines only) makes it exempt but
   not free. **FIXED:** the recurring overhead is now in the row; the recommendation stands with the honest
   price attached.

## Boundary note

The review itself executed nothing: read-only lane over committed artifacts; all fixes landed as ordinary
edits on the prep branch before merge (contract D).
