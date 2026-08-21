# LANE-554 — cloud provisioning (batch 1, lane B)

| Model | Mode | Effort |
|---|---|---|
| opus (default) | execute — no plan mode | high |

**Worktree ⇄ file pairing:** slug `lane-554-cloud-provisioning` → branch
`worktree-lane-554-cloud-provisioning` → this contract `LANE-554-cloud-provisioning.md`.
**Repo:** `.dev-knowledge` · **Purpose:** execute [#554]'s provisioning legs AS WRITTEN IN ITS
ROW (repo is the record — read the row first), so the NEXT cloud dispatch is the first live
test of Q4/Q5 with provisioning already proven, plus the two review amendments below.
Governance pointer: `protocols/PLAYBOOK.md`, `STANDING_RULINGS.md` §Q read-only (Q4/Q5
especially).

**Done-contract (immutable):**
1. Every provisioning leg in [#554]'s row executed or explicitly reported blocked-with-reason.
2. **A3 (baked):** devcontainer prebuild leg — on-config-change trigger, region EuropeWest,
   history depth 1 — PLUS a measured warm-start acceptance check: resume-vs-create time
   recorded in the end artifact (two timed runs minimum). Budget note in artifact: Actions
   minutes 30% consumed (source: codespaces audit RULING block).
3. **B1 (baked, blocking):** depth-1 prebuild breaks spine-walking instruments
   (validate_git_backlog runs the full first-parent spine — 1517 entries). The provisioning
   MUST include either a gated `git fetch --unshallow` (or `--deepen`) step that runs BEFORE
   any spine-walking instrument in a cloud lane, or an explicit documented exclusion of those
   instruments from cloud lanes. State which, and why, in the artifact.
4. Env refuse-gate leg per the row (bespoke — library-first line: name what stdlib/devcontainer
   feature was checked first, one line).
5. pytest green; scripts follow repo standards (English, logging, config in YAML not
   hardcoded).

**Pre-commit:** same rule as lane A — no `.pre-commit-config.yaml` edits; hook entries as
fenced proposed-diffs in the artifact; no audits-index regeneration.

**Git workflow:** all work on `worktree-lane-554-cloud-provisioning`; **COMMIT** per leg;
pytest before final; **commit-and-STOP — never merge, never push main.**

**Steps**
1. Read `CLAUDE.md`, [#554]'s row + any docs it cites, §Q4/Q5. UNDERSTAND: list the legs and
   their acceptance in your first commit's artifact stub. **COMMIT**
2. Execute legs in row order; one **COMMIT** per leg.
3. A3 prebuild + warm-start measurement. **COMMIT**
4. B1 unshallow/exclusion clause implemented + documented. **COMMIT**
5. Terra review (`/codex-review`), severity tally INTO the artifact, fix P1/P2. **COMMIT**
6. Final artifact `ARTIFACT-lane-554.md` at the worktree root (legs done/blocked ·
   measurements · proposed diffs · tally), pytest green, **COMMIT, then STOP.** Do NOT write
   under docs/audits/ (archival lane owns it this batch).

**Decision budget:** zero interactive questions; defaults + end-artifact reporting. The ssh
BOM defect is OPERATOR-owned — do not attempt to fix it; note interactions only.
**What NOT to do:** no merges · no tasks/BACKLOG/§Q edits · no new folders without quoted
basis (PROPOSED-PATH rule) · no deletions · no cloud dispatches from inside this lane · no
pre-commit edits.
