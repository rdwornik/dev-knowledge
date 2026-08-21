# LANE-ARCH — lifecycle archival: ADRs + audits (batch 1, lane C)

| Model | Mode | Effort |
|---|---|---|
| opus (default) | execute — no plan mode | high |

**Worktree ⇄ file:** slug `lane-arch-adr-audits` → branch `worktree-lane-arch-adr-audits` →
`LANE-ARCH-adr-audits.md`. **Repo:** `.dev-knowledge`. **Purpose:** execute the
lifecycle-archival row (operator demand: archival EXECUTED). Measured start state: ADRs 2/88
archived, audits 0. Governance pointer: `protocols/PLAYBOOK.md`, `STANDING_RULINGS.md` §Q
read-only — **Q3 push-before-delete binds every move.**

**SCOPE SPLIT (binding):** this lane archives **ADRs + docs/audits ONLY**. The intake class
(0/34) is EXPLICITLY DEFERRED to after the ratification lane merges — docs/intake/** belongs
to lane D this batch; touching it here is a contract violation.

**Done-contract (immutable):**
1. Read the lifecycle-archival row first (repo is the record) and follow its criteria; where
   the row is silent: an ADR is archival-eligible per existing archived-ADR precedent (2
   exist — quote how they were archived and mirror it); an audit is eligible ONLY if its
   findings are transcribed into rows (verify the transcription, cite the row ids in the
   move commit).
2. Archive destinations follow EXISTING convention per class. If no convention exists for a
   class: do NOT invent a path — list the candidates with quoted governance basis in
   `ARTIFACT-lane-arch.md` (worktree root), mark them `PROPOSED-PATH`, archive NOTHING of
   that class, and STOP that leg. Zero invented paths.
3. Every move = git mv (history preserved), push-before-delete honored (nothing is removed
   that isn't already on the pushed branch), one **COMMIT** per class batch.
4. Any index/reference to a moved file is updated in the SAME commit — no dangling links
   (grep for the old path before committing; show the grep in the artifact).
5. Artifact: per-class counts before/after · eligibility evidence · PROPOSED-PATH items ·
   nothing-touched list. pytest + `python scripts/audit.py` green (no new WARNs of your
   making). **COMMIT, then STOP.**

**What NOT to do:** no docs/intake/** touches · no deletions (archival is MOVE) · no tasks/,
BACKLOG, §Q, PLAYBOOK edits · no pre-commit or .gitignore edits · no audits-index
regeneration (integrator, once) · no merges · docs-only lane: no terra (no code impact).
**Decision budget:** zero questions; PROPOSED-PATH + report instead.
