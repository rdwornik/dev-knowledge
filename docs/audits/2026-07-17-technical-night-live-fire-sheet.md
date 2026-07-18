# LIVE-FIRE SHEET — P4 dynamic trigger verification (2026-07-17 night)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-17
- **Source:** 2026-07-17 night-run scratchpad (`LIVE-FIRE-SHEET.md`), content unchanged below this block.
- **Night rule:** the run was READ-ONLY / zero-commit — no writes to any real repo tree; all
  outputs went to scratchpad. This docs-only arc (branch `docs/2026-07-17-night-audit`, filed
  2026-07-18) is its first commit.
- **Companion night-run audits (same arc):** `2026-07-17-technical-night-verdict-sheet.md`, `2026-07-17-technical-night-divergence-ledger.md`, `2026-07-17-technical-night-live-fire-sheet.md`, `2026-07-17-technical-night-handoff-evidence-pack.md`.

**Method:** all mutations ran in **throwaway local clones** under the scratchpad
(`sandbox/sandbox-{hub,corp,ai}`, hardlinked local clones — hub re-cloned with
`core.longpaths=true` after a MAX_PATH checkout failure). NEVER the real checkouts.
Each scenario: mutate → run the organ → capture the verbatim trigger → revert. Sandbox
deleted at teardown; real trees verified (see bottom).

**Grading:** FIRED = the organ produced its expected trigger, witnessed live. SILENT = defect.
Parity scenarios graded by **delta against the sandbox baseline** (fresh clones have unarmed
hooks + missing gitignored state, so absolute counts differ from the real fleet — that is
expected and not a defect). Sandbox fleet_parity baseline: `155 at-parity · 20 pass-declared ·
1 gate-ahead-declared · 4 warn-undeclared · 2 must-absent · 0 stale · 0 refused`.

| # | Scenario | Result | Verbatim trigger |
|---|---|---|---|
| S1 | delete corp `gate_rev_ahead` decl | **FIRED** | gate-ahead `1→0`, warn-undeclared `4→5`; `corp-monorepo precommit-hub-block WARN-undeclared: present but not carried faithfully: rev 'v1.3.1' != recorded deploy source_tag 'v1.2.0'` |
| S2 | corp pin drifts v1.3.1→v1.4.0 (undeclared) | **FIRED** | gate-ahead `1→0`, warn-undeclared `4→5`; `corp-monorepo precommit-hub-block WARN-undeclared: rev 'v1.4.0' != recorded deploy source_tag 'v1.2.0'` — bless failed, not blessed as gate-ahead |
| S3 | inject `waivable: true` on a MUST row | **FIRED** | refused `0→1`; `- canonical-doc-architecture refused: waivable: true on a MUST/INVERSE row -- a necessary condition is never waivable (ADR-102 loader refusal)` |
| S4a | remove a row's `ownership:` block | **FIRED** | refused `0→1`, ownership tally `52→51`; `- precommit-hub-block refused: ownership block is mandatory (ADR-103) -- needs value in {methodology-generic/project/conditional}` |
| S4b | blank a row's `reason:` | **FIRED** | refused `0→1`; `- canonical-doc-vision refused: ownership malformed -- declaration needs a non-blank reason (ADR-103; shares the ADR-102 grammar)` |
| S5 | corpus catch-up (source_tag == pin, decl present) | **FIRED** | stale `0→1`, gate-ahead `1→0`; `corp-monorepo precommit-hub-block stale-declaration: gate-ahead declaration inert: corpus caught up (pin v1.3.1 == corpus v1.3.1) -- PRUNE the gate_rev_ahead` |
| S6 | direct-to-main non-merge push (hooks installed first) | **FIRED** | hooks armed+verified (`pre-push` EXISTS, pre-commit-managed: YES); `hook id: block-ff-push / exit code: 1 / block_ff_push: REFUSED — non-merge commit(s) would land on main's first-parent spine ... fix: redo as a --no-ff merge` → `error: failed to push some refs` |
| S7 | remove one disposition → undispositioned WARN | **FIRED** | `[disp] warn-doc-rot-backlog-262` line disappears, undispositioned count `1→2`; `ship-gate: RED — not shipped-ready (2 new/undispositioned WARN(s))` |

## SILENT defects: NONE. All seven organs fired.

## Honest nuances (reported, not hidden)

- **S3/S4a/S4b exit 0, not 2.** The loader surfaces a bad row as a **row-level `refused`**
  (counted in the `refused` tally, WARN-only posture, process exits 0), not a process-level
  exit-2. Exit-2 is reserved for a **structurally unusable** manifest (unparseable YAML), not a
  single bad row. The scenario intent — *refuse the row + name it* — is fully met; this is the
  designed graceful posture (Layer-2 WARN-only), not a miss.
- **S6 also refused the *baseline* push** (empty remote): `block_ff_push` reconstructed main's
  range and found the 3 pre-existing operator-ratified FF/direct commits (533109f20 / 3a894eeb5
  / d0f9ead67). So the prevent organ is live and aggressive even before my test commit — the
  offending push then failed unambiguously (`exit code 1`). (Contra my prior "empty-initial
  skips" note — here reconstruction caught the standing violations.)
- **S7 sandbox baseline was already RED (1 undispositioned WARN)** = `deployed_methodology_version:
  sandbox-hub not listed in deployed-versions.yaml (ADR-91)` — the **known clone/worktree
  dir-name artifact** (a fresh clone's dir `sandbox-hub` is not a registry key; the real hub
  `.dev-knowledge` IS a key and skips as `[--]`). Environmental — must NOT be dispositioned or
  faked into the registry. My mutation added exactly its expected **+1** undispositioned WARN
  (the now-unsuppressed `#262` doc_rot), taking the count `1→2`; the RED verdict path was
  witnessed live. S7's mechanism (disposition removal un-suppresses exactly that WARN, gate
  reports RED) is cleanly proven.

## Teardown verification

- `rm -rf scratchpad/sandbox` → sandbox dir absent (verified). **Zero sandbox leftovers.**
- Real trees after teardown:
  - **hub** `e0cbffdb` main — **CLEAN, byte-identical to P0.**
  - **corp** HEAD **560a38d → 2454a6f** (advanced 3 commits on branch `docs/2026-07-17-night-process-audit`), tree clean — **EXTERNAL** (a parallel night session committing; I only ever cloned corp read-only).
  - **ai-council** `3862749` main — `M config/settings.yaml` + `?? docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` — **EXTERNAL** concurrent churn (this file + mod appeared/changed across the run: absent at 22:37 P0, present 22:52, config mod toggled clean→dirty during the run).
- **My run's own teardown criterion PASSES:** zero writes/commits by me to any real tree, zero
  sandbox leftovers. The corp/ai-council real-tree changes are attributable to a **concurrent
  night session** (distinct "night-process/batch-audit" workstream), NOT this run — evidenced by
  timing (all post-P0) and that I used only read-only reads + local clones on those repos.

## FLEET-NOT-QUIESCENT finding (for the morning)

A **second night session is running against the fleet** tonight: corp-monorepo is on branch
`docs/2026-07-17-night-process-audit` and advanced 3 commits during this run; ai-council received
`docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` + a live `config/settings.yaml` edit.
Implication: **cross-consumer witnessed state for corp/ai-council is a moving target tonight** —
the divergence ledger's corp/ai rows were witnessed at a point-in-time (~22:40–23:00) and corp's
content may have shifted by morning. Re-witness corp/ai before executing any alignment arc.
