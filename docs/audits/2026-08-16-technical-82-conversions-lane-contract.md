# CONTRACT W2E — Done-when conversions, #82 group · worktree `worktree-lane-e-82-conversions`

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** 82-conversions
- **Ids:** `[#82]` `[#145]` `[#239]` `[#263]` (`[#82]` home per A1). **OWNED-FILES manifest:** `tasks/82-define-per-repository-agentic-review-profiles.md`, `tasks/145-codification-completeness-pass.md`, `tasks/239-follow-up.md`, `tasks/263-protocols-edge-map-reconciliation-residuals.md` (+ `BACKLOG.md` / `tasks/manifest.json` regen at close — regen surfaces excluded from the footprint).

## Common law (COMMON, verbatim per the contract of record)
Auto mode; own worktree/branch only; `uv sync --locked --group analytics` first; `PYTHONUTF8=1` on console errors; T_start = packet line 1; step 0 commits contract-of-record + prints OWNED-FILES manifest; edit nothing outside it (regen surfaces excluded); `tasks/` edits at SOURCE then `gen_task_tree.py --emit-source`; targeted tests only (full suite = integration, once); no merges, no pushes to main, no births, no register edits unless the contract names them; decision budget: STOP only for curated-baseline touch, rule-vs-ruling conflict, or unruled fork — else decide-and-report in ONE packet; commit-and-STOP.

## Purpose
These four ids were part of the 2026-08-13 W4a conversion wave (17-row group A) but were **SKIPPED there** for lack of a census P1/P2 draft (`a4fc652d`, "11 SKIPPED (no census draft)"). The 2026-08-14 wave-2 draft artifact `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` (landed on `main` by CONTRACT W2-0, `29501b39`) drafted all four — this lane applies those drafts verbatim to the four rows' Done-when clauses, closing the gap W4a left open.

## Referents verified live before applying (step 0 diligence)
- `[#82]` draft cites the ADR-104 `adr104-fleet-members` anchor (`docs/decisions/ADR-104-fleet-repository-shape.md:149-161`) and `scripts/audit.py::check_membership_agreement` (`scripts/audit.py:3793`) — both present. Per the drafts doc §"Open substitution", `[#82]`'s home is a **textual substitution** if the operator later names another candidate — not re-litigated here.
- `[#145]` draft's home is a `docs/audits/<date>-technical-*` artifact convention — no additional referent to verify.
- `[#239]` draft cites `scripts/enforcement_coverage.py` (present) and a `protocols/STANDING_RULINGS.md` per-element deferral home (section pattern already in use elsewhere in that file).
- `[#263]` draft cites `ecosystem/doc-code-edge.yaml`'s `mermaid_theme_directive` exempt entry (present, `ecosystem/doc-code-edge.yaml:115`), the two `protocols/PLAYBOOK.md` "per ESSENTIALS...English-only" refs (present, `protocols/PLAYBOOK.md:641,704`), the `protocols/AI_COUNCIL_PROCESS.md` "ESSENTIALS § Repo artifacts" ref (present, `protocols/AI_COUNCIL_PROCESS.md:325,413`), and `doc_code_coverage_drift` — all live.

## Steps
1. **Step 0** — commit this contract of record; print OWNED-FILES manifest (above). → COMMIT
2. Apply each id's wave-2 draft verbatim to its row's Done-when clause (frontmatter `status` untouched; no births, no closes). → COMMIT
3. Regenerate `BACKLOG.md` + `tasks/manifest.json` via `gen_task_tree.py --emit-source`; verify `validate_backlog` OK. → COMMIT
4. JOURNAL on the lane branch. → COMMIT

## What NOT to do
No merges · no pushes to main · no new ids · no closes/status changes · no edits outside the four owned task files (+ regen surfaces) · no full-suite runs · no `STANDING_RULINGS.md`/register edits (the drafts *reference* future homes there; this lane does not create those sections) · no answering stop-hooks with new scope.

## Done-when (frozen)
(1) Each of `[#82]` `[#145]` `[#239]` `[#263]`'s Done-when clause reads its wave-2 draft verbatim; (2) `BACKLOG.md`/manifest regenerated clean, `validate_backlog` OK; (3) lane packet: T_start · manifest as executed · per-step commit shas · targeted-test evidence · deviations self-reported · final "STOPPED" line.
