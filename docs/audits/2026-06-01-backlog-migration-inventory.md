<!-- scope: meta -->

# BACKLOG migration — Step 0 inventory + git cross-check (ADR-64/65)

> **Measure-first, report-only — no BACKLOG edits in this step.** Branch
> `docs/backlog-migration-adr64-2026-06-01` off `main` @ `b487a35`. Basis for the
> destructive Step 5 (purge done items) and Step 7 (child-repo relocation proposal).

## Counts (verified live)

| Metric | Value |
|---|---|
| Total entries | **107** |
| Open / in-progress | **66** (all `[open]`; none use `in-progress`) |
| Done (closed/superseded/resolved) | **41** |
| H2 sections | 9 (Streams A–D + Cross-stream + 4 session-arc sections) |
| Entries with a stable `id:` | **0** (the schema has no id field yet) |
| Status vocabulary in file | `open/closed/superseded/resolved` (schema says `open/in-progress/blocked/done` — drift) |

## Done-set — git verification (all 41 verifiable → all removable in Step 5)

**A. Embedded closing SHA, verified in `git log` (13 entries):**

| Line | Entry (short) | Closing SHA(s) — verified |
|---|---|---|
| 115 | backlog_extract.py retired | `a5ed940` |
| 122 | migrate_links SKIP_NAMES | `dc46565` |
| 129 | README ADR index 45-50/54 | `dc46565` |
| 150 | Codemap generator spec | `b2296ff` (merge) |
| 217 | v4 first real test | `93b7b1c` |
| 448 | v3.4 Stage-1 template | `b4afff3` |
| 456 | v3.4 skill rewrite | `e2f85f4` |
| 464 | v3.4 self-consistency | `581c3cb` `60df5b6` `4e3cc3e` |
| 472 | v3.4 ADR-42 Q5 addendum | `581c3cb` |
| 480 | v3.4 FOLDER_TEMPLATE drift | `b696474` |
| 488 | v3.4 broken citations | `256e26b` `a86c18d` |
| 496 | v3.4 ADR-45 stale refs | `4e3cc3e` |
| 732 | workspace ADRs folder alias | `f5322837` |

**B. Closed-by-ADR, verified via the ADR's introducing commit (6 entries):**

| Line | Entry | Closing ADR → commit |
|---|---|---|
| 83 | AI Council cross-project routing | ADR-43 → `f6c616f` |
| 672 | Draft 5 handoff ADRs | ADR-55..58 → `aa41258` |
| 202 | v4 handoff ratification | ADR-62 → `986d350` |
| 384 | Codify scrum-master authority | ADR-63 → `986d350` |
| 694 | Folder taxonomy ADR | ADR-60 → `be92f55` |
| 702 | Codify git worktree pattern | ADR-61 → `42f2be1` |

**C. Artifact/state-verified — closing artifact named in the entry is present/absent in git HEAD (22 entries):**
Lines 20, 35, 55, 63, 77, 171, 179, 194, 210, 224, 231, 238, 245, 332, 347, 430, 597, 605, 679, 751, 808, 815.
Verification basis per entry is the artifact it cites — e.g. 210/815 → checks #8/#7 present in `scripts/audit.py` (`a7576dd`); 751 → `protocols/AI_COUNCIL_PROCESS.md` present (`7ef4fe8`); 63 → `check_backlog_organization` absent at HEAD; 605 → test absent + suite green; 430/597 → ADR-62/ADR-60 (`986d350`/`be92f55`); 171/179/347 → tier system deprecated (ADR-33/40 amendments); 224/238/245 → handoff bundles present under `docs/handoffs/`.

**Flag-don't-delete (Step 5):** **none.** Every done entry has a verifiable closing anchor (embedded SHA, ADR commit, or artifact/state at HEAD). Two (63, 605) are *verified-by-absence* rather than by a closing SHA — their JOURNAL-map line will state the verification method explicitly rather than a single SHA.

## Child-repo execution set (Step 7 relocation candidates — ~21 open items)

Owner is a child repo; work executes there (ADR-41 → relocate, not direct from `.dev-knowledge`):

| Line | Entry | Target repo |
|---|---|---|
| 27 | ai-council LESSONS scope-tag backfill | ai-council |
| 418 | Handoff folder format adoption | corp-monorepo |
| 424 / 612 | UPPERCASE TYPE legacy-archive rename | corp-monorepo, corp-sca |
| 438 | docs/HANDOFF.md flat-file deprecation | corp-monorepo, ai-council |
| 542 | P1-2 path-traversal branch unmerged | corp-monorepo |
| 582 | hyphen migration + ADR-38 | corp-monorepo |
| 590 | hyphen migration + ADR-38 | ai-council |
| 629 | apply tier-deprecation | corp-monorepo |
| 636 | apply tier-deprecation | ai-council |
| 643 | root hygiene application | corp-monorepo |
| 649 | root hygiene application | ai-council |
| 687 | execute ai-council universalization plan | ai-council |
| 717 | prevent auto-debate of stray Council files | ai-council |
| 739 | ADR-59 visual-pattern retrofits (4×) | 4 child repos |
| 794 | per-repo deeper cleanup (post-retrofit) | child repos |
| 856 | corp-sca dev-tooling + run.py move | corp-sca |

**Stay-in-`.dev-knowledge` as `## Coordination` pointers (governance, not execution):** 164 (Phase-2 universalization rollout — disseminator), 296 (cross-repo audit Phase 3 — auditor tool), 403 (apply scrum-master pattern — review-authority trigger), 565 (undiscovered-repos confirmation — discovery), 655 (README disposition decision — per-repo decision). **Keep ≤10** (ADR-64 carveout); current candidate count ≈5 → within budget.

## Anomalies / drift (for the restructure)

- **All 107 entries lack `id:`** — Step 6 assigns monotonic ids.
- **Status vocabulary drift** — file uses `closed/superseded/resolved`; schema (ADR-41/47, PLAYBOOK §10) says `done`. Step 4 fixes the schema; Step 5 removes all done; remaining are `open` (a few are really in-progress/blocked — Step 6 reclassifies).
- **Taxonomy** — named streams route only 10/66 open; 4 session-arc H2 sections hold 37/66. Step 6 retires all stream/arc headers → `repo:` field + status sections.
- **Multi-note dilution** — many entries stack 2–4 dated `Status update`/`Scope update` bullets; removed on close (Step 5) or collapsed to current-state on restructure (Step 6).
- **Schema mutation** — non-schema fields proliferate (`Order`, `Sub-items`, `Escalated`, `Effort`, `Acceptance criteria`, `Trigger`). Step 6 normalizes to the Step-4 schema; rich detail that is still load-bearing moves to the entry's `What`/`Why`.

## In-progress / blocked reclassification candidates (Step 6)

No entry is tagged `in-progress`/`blocked` today (vocabulary gap). Candidates for `## Now` (in-progress) on restructure: items the operator is actively driving — to be confirmed at Step 6 (e.g. the migration-adjacent items). Candidates for `## Blocked`: 739/744 sub-item (corp-monorepo retrofit blocked on ruff-strictness decision). Most of the 66 are genuinely `open`.
