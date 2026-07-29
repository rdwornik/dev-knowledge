# `.vscode` W1 visibility — execution record

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-30 · **Slug:** vscode-w1-execution-record
- **Arc:** RULING-W consumer write-through, branch `docs/vscode-w1-execution-record`.
- **Executes:** `docs/audits/2026-07-29-technical-vscode-w1-visibility-ruling.md` — ruled
  2026-07-29, executed nowhere until this arc. That file is **immutable**; this is its execution
  record, not an amendment to it (CLAUDE.md §5 rule 3).
- **Status of execution:** all three ruled legs **COMMITTED ON BRANCHES, NOT MERGED.** RULING-W:
  worktree/branch → report, never a direct push to a consumer's main. The operator is each
  repo's merge gate.

---

## What landed

| # | Leg | Repo | Branch | Commit |
|---|---|---|---|---|
| 1 | `.vscode` decoration copy + `extensions.json` + `DECLARED-UNTIL-MECHANISM` entry | corp-monorepo | `chore/vscode-w1-visibility` | `65a8a35` |
| 2 | `review_date: 2026-08-13 → 2026-08-26` | corp-monorepo | same branch as leg 1 | `65a8a35` |
| 3 | `review_date: 2026-08-13 → 2026-08-26` | ai-council | `chore/vscode-e1-redate` | `e4f002e` |
| — | this record + hub re-date + R4 filings | .dev-knowledge | `docs/vscode-w1-execution-record` | (this commit) |

Leg 1 followed `ai-council/.methodology.yaml:97-109` as the named verbatim precedent. The
`.vscode/settings.json` write was an **ADR-93 merge, not a clobber**: corp's pre-existing
`files.watcherExclude` block survives byte-identical (verified — the diff contains no `+`/`-`
line touching it), and hub repo-personal keys were deliberately not copied. The
`editor-config` carrier remains `implemented: false`; [#371] is not partially closed by this.

## Two departures from the ruling's literal text, both recorded rather than silent

**1. Architect-authorized extension of part 4 — the hub row re-dates too.** The ruling's part 4
names both *consumer* declarations. But both consumer reason blocks assert "the hub's own
`.vscode` entry carries the same `2026-08-13` review_date" — so re-dating consumers alone would
make that sentence false and leave the hub row lapsing on 2026-08-13, defeating the very e1
alignment part 4 exists to buy. Ruled by the architect this session: re-date
`.dev-knowledge/.methodology.yaml`'s `.vscode` row to **2026-08-26** in this arc, and move the
date inside all three reason blocks so the cross-reference stays true.

**2. `.gitignore` negation in corp — unanticipated by the ruling, required for leg 1 to exist.**
corp's `.gitignore:16` is `.vscode/*` with a single un-ignore at `!.vscode/settings.json`. The
ruled `extensions.json` was therefore **untrackable**: it could be written and never committed,
and the decoration would have shipped inert (the highlight keys do nothing without the
recommended extension). ai-council tracks both files. A second negation line
`!.vscode/extensions.json` was added as the minimal means of making the ruled artifact
committable. Flagged here rather than absorbed as a silent sub-edit.

## The frozen C-0 witness

Authored and proven RED **before any edit**, then frozen; re-run verbatim at close-out. The
in-scope set is the **mutable declaration surfaces**, not every mention of the date — the
immutable and historical surfaces (`JOURNAL.md`, prior `docs/audits/*`, `docs/handoffs/**`,
`logs/PROPOSALS-*`) record a date that *was* true, and editing them would violate §5 rules 1-3.

| # | Surface | C-0 | C-3 |
|---|---|---|---|
| 1 | `ai-council/.methodology.yaml:93` prose | RED | GREEN-on-branch |
| 2 | `ai-council/.methodology.yaml:94` scalar | RED | GREEN-on-branch |
| 3 | `corp-monorepo/.methodology.yaml:99` prose | RED | GREEN-on-branch |
| 4 | `corp-monorepo/.methodology.yaml:100` scalar | RED | GREEN-on-branch |
| 5 | `.dev-knowledge/.methodology.yaml:99` scalar | RED | GREEN-on-branch |

No in-scope witness was already GREEN at freeze → the premise was well-formed, no STOP.

**Discrepancy line (reported, table not edited):** the executing plan anticipated **six** in-scope
stamps, assuming the hub `.vscode` reason prose also carried the date. It does not — the hub
prose reads "SHORT shelf-life deliberately set", dateless. The in-scope set is **five**. No hub
prose date edit was owed.

**Recorded, not fixed:** `ecosystem/disposition-register.yaml:223` and `tasks/manifest.json`
mirror the declarations and still carry `2026-08-13`. They are derived/registry surfaces outside
this arc's ruled scope; named here so the residue is not silent.

GREEN-on-main for every row requires the operator's three merges.

## R4 filings

- **[#447]** (new) — the ratchet-raise ↔ local-hook bootstrap deadlock, mechanism-scoped: a
  commit that raises a ratchet is judged by the pre-raise threshold, because `pre-commit install`
  arms hooks at install time. `kill-candidates: none` with the reason stated on the row.
- **[#446]** annotated — the 6-question SUPPLEMENT residual at `.claude/commands/handoff.md:117`
  is now named in its write set. The row sat at **1178 of the 1200-char `doc_rot` cap**, so the
  annotation was only possible by compressing redundant text elsewhere in the row
  (info-preserving; it now sits at 1197). This is the **[#364]** defect in its natural habitat
  again — the same one the ruling this record executes called out for [#371]/[#352]. Recorded as
  a fresh instance rather than resolved by dropping the annotation.
