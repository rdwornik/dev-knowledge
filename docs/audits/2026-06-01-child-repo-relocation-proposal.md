<!-- scope: meta -->

# Child-repo relocation queue (ADR-64 Q3-A)

> **Live queue.** These 18 child-repo *execution* items were **moved out of `.dev-knowledge/BACKLOG.md` `## Coordination` on 2026-06-01** (readability pass, step 3) and are tracked here until their target-repo sessions relocate them into each child repo's own `BACKLOG.md` (ADR-41). **No file in any other repo has been touched** — relocation executes in the target repo, then the item leaves this queue. Genuine cross-repo governance pointers (BACKLOG ids 45-47) stay in `BACKLOG.md ## Coordination`, not here. This file is a record, not parsed by `validate_backlog.py`.

## Triage rule
- **Relocate** — work executes in a child repo → moves to that repo's `BACKLOG.md`; then leaves this queue.
- **Keep in `.dev-knowledge`** — genuine cross-repo governance (BACKLOG ids 45/46/47) — not in this queue.

## Relocation mechanics (pins ADR-64 §"Open implementation questions" #1)
1. **Move, don't copy** — a child-repo session adds the item to `<repo>/BACKLOG.md` (its own local id); a follow-on `.dev-knowledge` session removes it from this queue. The two commits cross-reference by message.
2. **Split-brain avoidance** — an item is active in exactly one place; it leaves this queue only once it lands in the child repo.
3. **Backlink** — the child entry cites the originating `.dev-knowledge` context (audit/ADR) so provenance survives.
4. **Re-triage at move-time** — if an item turns out to carry a genuine `.dev-knowledge` governance obligation, keep a one-line Coordination pointer there and move only the execution part.

## Queue (18 items; original BACKLOG ids retained for traceability)

### [P1][M] Apply tier-deprecation to corp-monorepo
`id:48 · repo:corp-monorepo · status:open`
Remove tier:/scale: from VISION/ARCHITECTURE frontmatter; add status/last_reviewed per the amended ADR-33 schema.

### [P1][M] Apply tier-deprecation to ai-council
`id:49 · repo:ai-council · status:open`
Remove tier:/scale:; add the missing status key (vision_md WARN); verify last_reviewed.

### [P1][L] Execute the ai-council universalization execution plan
`id:50 · repo:ai-council · status:open`
Run the 2026-05-25 plan (Actions 1-8): README delete, tier-residue, naming, codemap, workspace dot-prefix, BACKLOG header. Subsumes #49/#57.

### [P2][M] Handoff folder-format adoption (corp-monorepo)
`id:51 · repo:corp-monorepo · status:open`
Convert flat `docs/HANDOFF.md` to folder format, or deprecate (after the A4 legacy-format decision).

### [P2][S] P1-2 path-traversal branch unmerged
`id:52 · repo:corp-monorepo · status:open`
Merge `chore/extract-p1-2-to-backlog-2026-05-28` → main; resolve the pre-delete gate (security-finding tracking stranded).

### [P2][M] Root hygiene application — corp-monorepo
`id:53 · repo:corp-monorepo · status:open`
Consolidate tool configs into pyproject.toml; dot-prefix the workspace; verify tach.toml movability.

### [P2][M] Root hygiene application — ai-council
`id:54 · repo:ai-council · status:open`
Consolidate tool configs into pyproject.toml where present; dot-prefix the workspace; confirm clean root.

### [P2][S] README disposition decision (corp-monorepo)
`id:55 · repo:corp-monorepo · status:open`
Decide keep-or-delete corp-monorepo's root README (external audience?); README optional since ADR-38 A5.

### [P2][M] corp-monorepo hyphen migration + ADR-38
`id:56 · repo:corp-monorepo · status:open`
Hyphen-rename ADR files + reclassify docs/archive/ content (ADR-38 Scale-L gaps already closed).

### [P2][M] ai-council hyphen migration + ADR-38
`id:57 · repo:ai-council · status:open`
Verify + hyphen-migrate; ADR-38 gaps (ARCHITECTURE to root, add LESSONS/BACKLOG). Largely subsumed by #50.

### [P2][M] Prevent auto-debate of stray Council-keyed files
`id:58 · repo:ai-council · status:open`
Guard against stray Council-frontmatter files auto-running (allow-list / required marker / inbox-only scoping).

### [P2][L] ADR-59 visual-pattern child-repo retrofits (4×)
`id:59 · repo:ecosystem · status:open`
Apply ADR-59 to the 4 child repos (plans authored 2026-05-27); corp-monorepo blocked on its ruff-strictness decision.

### [P2][M] corp-sca dev-tooling install + run.py → scripts/
`id:60 · repo:corp-sca-time-automation · status:open`
Install pytest+ruff in the venv, then move run.py → scripts/run.py and update its 6 refs; verify with pytest.

### [P3][S] ai-council LESSONS scope-tag backfill
`id:61 · repo:ai-council · status:open`
Add `[scope: X]` to each LESSONS entry's 6-field schema position (ADR-46 advisory WARN).

### [P3][S] UPPERCASE TYPE legacy-archive rename
`id:62 · repo:corp-monorepo · status:open`
Rename `YYYY-MM-DD_TYPE_topic.md` → `YYYY-MM-DD-topic.md` in docs/archive/ opportunistically (corp-monorepo + corp-sca).

### [P3][S] docs/HANDOFF.md flat-file deprecation
`id:63 · repo:corp-monorepo · status:open`
Retire flat `docs/HANDOFF.md` (corp-monorepo + ai-council) or designate legacy; tied to #51.

### [P3][M] Per-repo deeper cleanup (post-retrofit)
`id:64 · repo:ecosystem · status:open`
Decide per repo whether to address retrofit leftovers (ruff errors, stray __pycache__, .env content).

### [P3][M] Cross-repo low-severity cleanups (child subset)
`id:65 · repo:ecosystem · status:open`
Child-owned items from the 2026-05-29 audit (verify-script layout SK-4, corp-monorepo flat-handoff CM-2, hook floors HK-4).

## History
- **2026-06-01** — moved here from `BACKLOG.md ## Coordination` (readability pass step 3). Originated as the 2026-05-31 migration's relocation proposal; triage verdicts unchanged. Items leave this queue as their target-repo sessions relocate them.
