> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-cc/DECLARE-ADR-122-RULINGS-2026-09-24.md` (a Drive transport path, not retained in
> this repo — verifiable against the bytes landed below by their hash,
> `sha256:bd11f9d59c524a1406c2f3cb4567693dd4f06ed14e6a503ace4eac613eda7fe1`, 2,570 B, computed by
> this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-declare-adr-122-rulings.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: ADR-122 step 0 (the view budget) in the next window's first lane; the operator's answers to Q2 and Q3 into RATIFICATION-2026-09-24 at the cut
date: 2026-09-24
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)
basis: SESSION-lane-adr-backlog (ADR-122 Proposed @ a97d3088, matrix 410/390/386, 20-row trial, 6 disagreements, sol check 12/5/0)

# DECLARE — ADR-122: the architect's ruling on the view ceiling, and recommendations on the two operator questions

## Ruling (technical): the view ceiling becomes a render budget

- **Truth has no byte ceiling.** `tasks/` records are never limited by size.
- **One budget, one source.** The 72,000 B test bar and the 100,000 B `--check` bar are two truths;
  they collapse into one configuration value that both read.
- **Interim, to unblock filing today:** the budget is 150,000 B for the generated view, with the named
  cause "ADR-122 step 0; the view is uncommitted and field-only at step 2" and `manual_until:
  2026-10-15`.
- **Target (step 2):** the default view renders fields — id, title, status, wave, links — never
  clauses; closed rows render in a separate view; views are not committed.

## Recommendations (functional; the operator decides)

- **Q2 — the browser's view.** The browser reads at events, never monitors (the equilibrium
  ruling). The batch-close organ and the handoff cut write a small view to the transport: the open
  rows of the current wave plus counts; the full listing on demand through CC. Freshness: every
  wave merge and every handoff. No committed `BACKLOG.md`.
- **Q3 — the untyped prose (26 of 116 clauses).** A rule, not 26 decisions: a clause that any script
  reads becomes a field; a clause no script reads goes to a `notes` field that governs nothing.
  Migration classifies mechanically from the research record's reader list. Codex's point stands:
  narrative may stay narrative, provided nothing machine-reads it.

## Consequences recorded

- O-6 (auto-close on a green verifier) is ADR-122's criterion-with-check; O-6a (new rows need a
  verifier or an explicit "not yet decided") becomes the schema.
- The closure-proposal organ's heuristics are superseded by criteria checks (D35).
- D36: the transport folder holds files of other projects (a CV amendment broke decision coverage);
  the transport registry scopes by repository.
- A YAML merge driver was not trialled; the first adjacent-line conflicts decide whether one is needed.
- ADR-122's reversal condition (pilot the hybrid, then events) stands as written.
