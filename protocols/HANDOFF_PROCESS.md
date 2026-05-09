# HANDOFF_PROCESS v3.1

<!-- version: 3.1 — 2026-05-09 (afternoon rewrite per amended ADR-42) -->
<!-- scope: meta -->

Version: 3.1
Effective: 2026-05-09 (afternoon)
Supersedes: v3.0 (2026-05-09 morning), v2.0 (ADR-32 §4 deprecated; ADR-32 §1-§3 extended)
Authority: ADR-42 (amended 2026-05-09 afternoon)

> **Authoritative source:** `docs/decisions/ADR-42_handoff_format_v3.md`. This protocol
> is the operational counterpart of ADR-42: structural decisions live in the ADR;
> operational mechanics (triggers, state tracking, generation workflow, roles,
> validation checkpoints) live here. If they conflict, ADR-42 wins.

---

## Purpose
<!-- scope: meta -->

Operational protocol for generating handoffs in the `.dev-knowledge` ecosystem.
Implements ADR-42 three-stage flow with full Stage 2 mandate — ALL handoff types
(audit-sync, session-sync, feature-X-sync) execute all three stages. No shortcuts.

A handoff transfers session state across browser chats or Claude Code sessions. All
handoff artifacts live in `.dev-knowledge/docs/handoffs/{date}-{slug}/` — ADR-36
read-only contract preserved (no writes to target repos).

---

## Trigger phrases
<!-- scope: meta -->

Rob in Claude Code (.dev-knowledge) says one of:

| Phrase | Effect |
|---|---|
| "Make handoff for {repo}" | Stage 1 (default type: session-sync) |
| "Make handoff for {repo}, type {type}" | Stage 1 with explicit type |
| "Complete handoff for {repo}" | Stage 3 (requires stage2-response.md present) |
| "Stage 3 for {slug}" | Stage 3 by exact slug |
| "Save this response as stage 2 for {slug}" | Write stage2-response.md from current chat |

Explicit types: `audit-sync`, `session-sync`, `feature-X-sync` (where X is descriptive).
Handoffs are explicitly triggered by Rob. Claude Code does not propose handoff generation
unprompted.

---

## State tracking
<!-- scope: meta -->

`docs/handoffs/_in_progress/{slug}/` directory tracks in-progress handoffs.

`{slug}` = `{YYYY-MM-DD}-{repo}-{type}` where date is from Stage 1 trigger.

| Files present in `_in_progress/{slug}/` | Detected stage | Action |
|---|---|---|
| (directory absent or empty) | Stage 0 | Run Stage 1 |
| `stage1-question.md` only | Stage 1 done, awaiting Stage 2 | Show Rob "paste browser-2 response into `stage2-response.md`" |
| `stage1-question.md` + `stage2-response.md` | Stage 2 done, ready for Stage 3 | Run Stage 3 |

If state is ambiguous (e.g., both files exist but Rob says "make handoff" again),
FLAG and ask Rob: delete and restart, or proceed to Stage 3?

---

## Stage 1 — Question generation
<!-- scope: hybrid -->

**Trigger:** "Make handoff for {repo}" or "Make handoff for {repo}, type {type}"

**Procedure:**

1. Determine slug: `{YYYY-MM-DD}-{repo}-{type}` (use today's date)
2. Verify target repo path exists and is a git repository
3. Capture target repo state:
   - HEAD SHA (`git rev-parse HEAD`)
   - Branch (`git branch --show-current`)
   - Working tree status (`git status --porcelain`)
4. Read `.dev-knowledge/BACKLOG.md`, identify items relevant to {repo}
5. If `audit-sync` type: read `.dev-knowledge/docs/audits/` for relevant audit
   reports; load findings as Stage 1 context — they inform question generation
   but do NOT substitute for Stage 2
6. Read `templates/HANDOFF_QUESTION_TEMPLATE.md`
7. Create directory `docs/handoffs/_in_progress/{slug}/`
8. Generate `docs/handoffs/_in_progress/{slug}/stage1-question.md`:
   - Header: target repo, HEAD SHA, branch, working tree state, timestamp, type, slug
   - Rob's instructions: how to use this file (open browser-2, paste, get response,
     save as stage2-response.md, return to Claude Code for Stage 3)
   - Customized 5-question template (OBJECTIVE / REALITY / RATIONALE / DIRECTIVES /
     BOUNDARIES) with repo-specific context pre-filled
   - For audit-sync: include audit findings summary as RATIONALE context, prompt
     browser-2 to extend or correct
   - Receiver synthesis prompt at end
9. Append JOURNAL entry under today's date:
   `- Handoff Stage 1 generated for {slug}: HEAD {SHA} captured; awaiting browser-2 response`
10. Run validators (`python scripts/validate_scope_tags.py`, `pre-commit run --all-files`)
11. Single commit on feature branch
12. Report to Rob:
    - Stage 1 complete
    - File created: `docs/handoffs/_in_progress/{slug}/stage1-question.md`
    - Next: paste content into browser-2 chat for {repo}; receive response;
      save as `docs/handoffs/_in_progress/{slug}/stage2-response.md`
    - Then: say "complete handoff for {repo}" to trigger Stage 3

**Output:** `_in_progress/{slug}/stage1-question.md`, JOURNAL entry, commit

---

## Stage 2 — Architect response (Rob's manual step)
<!-- scope: llm -->

**Input:** Content of `_in_progress/{slug}/stage1-question.md`

**Procedure (Rob does this manually):**

1. Open a NEW claude.ai chat for {repo} (browser-2)
2. Paste the "Context for browser-2 architect" section through end of `stage1-question.md`
   as first message
3. Browser-2 architect answers all 5 pipeline questions (OBJECTIVE / REALITY /
   RATIONALE / DIRECTIVES / BOUNDARIES) with project-level intelligence
4. Save response as `docs/handoffs/_in_progress/{slug}/stage2-response.md`:
   - Option A: Rob writes file directly (copy-paste response)
   - Option B: In Claude Code — "save this response as stage 2 for {slug}";
     Claude Code writes the file from chat content

**Output:** `docs/handoffs/_in_progress/{slug}/stage2-response.md`

No commit at this step — file is created/uncommitted until Stage 3 picks it up.

---

## Stage 3 — Reconciliation + folder generation
<!-- scope: hybrid -->

**Trigger:** "Complete handoff for {repo}" or "Stage 3 for {slug}"

**Procedure:**

1. Verify `_in_progress/{slug}/stage1-question.md` exists — if missing, FLAG and STOP
2. Verify `_in_progress/{slug}/stage2-response.md` exists — if missing, FLAG and STOP
   with message: "Stage 2 not complete. Paste browser-2 response as stage2-response.md first."
3. Re-capture target repo state:
   - Current HEAD SHA
   - Compare to Stage 1 SHA (from `stage1-question.md` header)
   - If drifted: FLAG to Rob with both SHAs, ask whether to proceed or abort and
     re-generate Stage 1 (do NOT silently proceed)
4. Read `templates/HANDOFF_FOLDER_TEMPLATE.md`
5. Read `.dev-knowledge` VISION.md, protocols/PLAYBOOK.md, protocols/ESSENTIALS.md
6. Read `_in_progress/{slug}/stage2-response.md`
7. Identify ADRs cited in DIRECTIVES (07_ACTION_PLAN content)
8. Generate folder `docs/handoffs/{slug}/` with 11 files (all flat, no subdirectories):
   - `00_README.md` — Rob's upload instructions
   - `00_first-message.md` — browser-2 first message + receiver synthesis prompt
   - `01_MANIFEST.md` — entry, file index, drift verification, HEAD SHA
   - `01_manifest.json` — machine-readable metadata + SHA-256 of all files (generated last)
   - `02_VISION.md` — full copy of `.dev-knowledge/VISION.md`
   - `03_PLAYBOOK.md` — full copy of `.dev-knowledge/protocols/PLAYBOOK.md`
   - `04_ESSENTIALS.md` — full copy of `.dev-knowledge/protocols/ESSENTIALS.md`
   - `05_GOVERNANCE_ESSENCES.md` — 2-4 sentence essences for ADRs cited in directives
   - `06_STATE_OF_PLAY.md` — REALITY + RATIONALE answers from Stage 2; audit findings
     if audit-sync; deferred items as BACKLOG references (do not duplicate queue)
   - `07_ACTION_PLAN.md` — OBJECTIVE + DIRECTIVES + BOUNDARIES from Stage 2
   - `08_TREE.txt` — `git ls-files` output in target repo at Stage 3 time
   - `09_EXECUTION_EVIDENCE.md` — empty return-trip template
9. Compute SHA-256 of every file in folder, populate `01_manifest.json`
10. Move `_in_progress/{slug}/` to `docs/handoffs/_archive/{slug}/`:
    - `_archive/{slug}/stage1-question.md`
    - `_archive/{slug}/stage2-response.md`
    This preserves Stage 1+2 inputs for traceability without violating flat structure
    of the final handoff folder.
11. Append JOURNAL entry under today's date:
    `- Handoff Stage 3 complete for {slug}: folder at docs/handoffs/{slug}/`
12. Append CHANGELOG entry under today's date (Changed or Added section)
13. Review BACKLOG.md: if any P1 items were closed by this handoff, update Status
14. Run validators (`python scripts/validate_scope_tags.py`, `pre-commit run --all-files`)
15. Single commit on feature branch
16. Report to Rob:
    - Stage 3 complete
    - Folder: `docs/handoffs/{slug}/`
    - Next: zip folder contents + upload to new browser-2 chat; paste `00_first-message.md`
    - Browser-2 executes directives, fills `09_EXECUTION_EVIDENCE.md`
    - Return that file to `.dev-knowledge` for next session reference

**Output:** `docs/handoffs/{slug}/` (11 files flat) + `docs/handoffs/_archive/{slug}/`
(stage1 + stage2 inputs), JOURNAL + CHANGELOG entries, commit

---

## Folder structure (per ADR-42)
<!-- scope: meta -->

```
docs/handoffs/{date}-{slug}/
├── 00_README.md                 (Rob's upload instructions)
├── 00_first-message.md          (browser-2 first message, copy-paste)
├── 01_MANIFEST.md               (entry point, file index, HEAD pin)
├── 01_manifest.json             (machine-readable, SHA-256 checksums)
├── 02_VISION.md                 (FULL .dev-knowledge VISION copy)
├── 03_PLAYBOOK.md               (FULL .dev-knowledge PLAYBOOK copy)
├── 04_ESSENTIALS.md             (FULL .dev-knowledge ESSENTIALS copy)
├── 05_GOVERNANCE_ESSENCES.md    (ADR essences relevant to actions)
├── 06_STATE_OF_PLAY.md          (current state, audit findings)
├── 07_ACTION_PLAN.md            (goals, directives, boundaries)
├── 08_TREE.txt                  (target repo file inventory)
└── 09_EXECUTION_EVIDENCE.md     (return trip template)
```

Stage 1+2 inputs archived separately at:
```
docs/handoffs/_archive/{slug}/
├── stage1-question.md
└── stage2-response.md
```

Slug format: `{YYYY-MM-DD}-{repo}-{type}`. Final folder immutable post-close.

---

## File responsibilities
<!-- scope: meta -->

| File | Purpose | Content origin |
|---|---|---|
| `00_README.md` | Rob's instructions: how to use this handoff | Generated by Claude Code |
| `00_first-message.md` | Copy-paste for browser-2 first message | Generated by Claude Code |
| `01_MANIFEST.md` | Entry point, file index, HEAD pin, receiver synthesis prompt | Generated by Claude Code |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums | Generated by Claude Code (last) |
| `02_VISION.md` | Ecosystem context | Full copy of `.dev-knowledge/VISION.md` |
| `03_PLAYBOOK.md` | HOW we work — methodology preserved across sessions | Full copy of `.dev-knowledge/protocols/PLAYBOOK.md` |
| `04_ESSENTIALS.md` | High-leverage cheat-sheet rules | Full copy of `.dev-knowledge/protocols/ESSENTIALS.md` |
| `05_GOVERNANCE_ESSENCES.md` | ADR rules driving specific actions in this handoff | Curated by Claude Code from relevant ADRs |
| `06_STATE_OF_PLAY.md` | Current State per ADR-37 | Stage 2 REALITY/RATIONALE answers + audit findings if audit-sync |
| `07_ACTION_PLAN.md` | Future State per ADR-37 | Stage 2 OBJECTIVE/DIRECTIVES/BOUNDARIES answers |
| `08_TREE.txt` | Target repo file inventory at Stage 3 | `git ls-files` in target repo |
| `09_EXECUTION_EVIDENCE.md` | Return trip: browser-2 fills post-work | Empty template, filled by next session |

**Invariant rule:** `02_VISION.md`, `03_PLAYBOOK.md`, `04_ESSENTIALS.md` are FULL
copies — never curated. They are the methodology anchors that prevent browser-2 from
hallucinating norms.

**ADR essence rule:** `05_GOVERNANCE_ESSENCES.md` includes ONLY ADRs cited in
`07_ACTION_PLAN.md` directives. Format per essence: title + 2-3 operational
sentences + reference path to full ADR.

---

## Drift mitigation
<!-- scope: dev -->

Stage 1 captures target repo HEAD SHA in `stage1-question.md` header. Stage 3
re-verifies before generation:

- **Match:** proceed
- **Mismatch:** Claude Code STOPS, flags to Rob with both SHAs, asks whether to
  proceed (Rob may abort and re-generate Stage 1 from current HEAD)

`01_manifest.json` SHA-256 checksums prevent post-generation file tampering.

Browser-2 first action upon opening handoff: verify HEAD SHA via `git rev-parse HEAD`
in target repo. Mismatch → STOP, report drift, do not proceed.

---

## Return trip
<!-- scope: hybrid -->

`09_EXECUTION_EVIDENCE.md` is filled by browser-2 or Claude Code in target repo after
completing handoff work. Provides:
- Commands run (raw stdout)
- Test results (pytest output)
- Git diffs of changes made
- Final HEAD SHA after work
- Failures or partial completions (explicit, not omitted)
- Handoff for next session if applicable

Next `.dev-knowledge` session reads `09_EXECUTION_EVIDENCE.md` to verify what actually
happened — eliminates "Self-Correction Theatre."

---

## Validation checkpoints
<!-- scope: meta -->

| Stage | Validator | Expected result |
|---|---|---|
| Stage 1 | `python scripts/validate_scope_tags.py` | passes, hybrid ≤25% |
| Stage 1 | `pre-commit run --all-files` | passes |
| Stage 1 | `git status` | single new file (`_in_progress/{slug}/stage1-question.md`) + JOURNAL modified |
| Stage 3 | `python scripts/validate_scope_tags.py` | passes |
| Stage 3 | `pre-commit run --all-files` | passes |
| Stage 3 | folder structure | 11 files flat in `docs/handoffs/{slug}/`, no subdirectories |
| Stage 3 | `01_manifest.json` | SHA-256 entries for all 11 files present |

---

## Roles
<!-- scope: meta -->

- **Rob.** Triggers handoff (never browser-2 unprompted), reviews Stage 1 question
  prompt, carries browser-2 response back (Stage 2), accepts handoff folder.
- **Claude Code (.dev-knowledge).** Executes Stage 1 and Stage 3: reads target repo
  state, generates question prompt, generates folder, computes checksums, runs
  validators, commits.
- **Browser-2 (target project chat).** Executes Stage 2: answers 5 pipeline questions
  with project-level intelligence. Also consumes the handoff: opens it, verifies HEAD
  SHA, provides receiver synthesis, executes directives, fills `09_EXECUTION_EVIDENCE.md`.

Browser-2 does NOT generate folders or run git in target repo (unless Rob explicitly
directs it to). Claude Code does NOT redesign architecture or invent session content.

---

## What changed v3.0 → v3.1
<!-- scope: meta -->

| Dimension | v3.0 (morning) | v3.1 (afternoon) |
|---|---|---|
| Stage 2 mandate | Skipped for audit-sync | Mandatory for ALL handoff types |
| State tracking | None | `_in_progress/{slug}/` directory with stage detection |
| Trigger phrases | Loose ("Make handoff...") | Table with exact phrases and effects |
| Archive | Not specified | Stage 1+2 inputs archived at `docs/handoffs/_archive/{slug}/` |
| Validation checkpoints | Implicit | Explicit per-stage table |
| JOURNAL hook | Not specified | Stage 1 + Stage 3 append entries |
| CHANGELOG hook | Not specified | Stage 3 appends entry |
| BACKLOG integration | Read at Stage 1 | Read at Stage 1; update at Stage 3 if items closed |
| Drift detection | Stage 3 re-verifies | Stage 3 re-verifies AND flags both SHAs on mismatch |

---

## References
<!-- scope: meta -->

- `docs/decisions/ADR-42_handoff_format_v3.md` — authoritative source (amended 2026-05-09 afternoon)
- `docs/decisions/ADR-32_handoff_format.md` — v2.0 (§4 deprecated by ADR-42; §1-§3 extended)
- `docs/decisions/ADR-37_session_boundary_protocol.md` — two-phase Current/Future overlay
- `docs/decisions/ADR-41_cross_session_backlog_architecture.md` — BACKLOG as pending items source
- `docs/decisions/ADR-36_audit_tool_architecture.md` — read-only contract
- `templates/HANDOFF_QUESTION_TEMPLATE.md` — Stage 1 output skeleton
- `templates/HANDOFF_FOLDER_TEMPLATE.md` — Stage 3 folder structure spec
- Council #24 — "wygeneruj handoff" trigger phrase

---

## Section history
<!-- scope: meta -->

- v3.1 (2026-05-09 afternoon) — Stage 2 mandatory for ALL handoff types (audit-sync
  shortcut removed per amended ADR-42). Operational state tracking via
  `_in_progress/{slug}/` directory. Trigger phrase table. Per-stage validation
  checkpoints. JOURNAL hook per Stage 1 + Stage 3. CHANGELOG hook per Stage 3.
  BACKLOG update at Stage 3. Archive pattern: Stage 1+2 inputs at
  `docs/handoffs/_archive/{slug}/`. Drift flag reports both SHAs.
- v3.0 (2026-05-09 morning) — full rewrite per ADR-42. Three-stage flow, flat 11-file
  structure, VISION/PLAYBOOK/ESSENTIALS as mandatory invariants, standardized 5-question
  pipeline, `09_EXECUTION_EVIDENCE.md` return trip. ADR-32 §4 deprecated in favor of
  BACKLOG.md.
- v2.0 (2026-04-28) — full rewrite per ADR-32. 9-section HANDOFF.md, folder convention,
  point-in-time copies, charter + step-verification controls, extract-to-task mechanics.
- v1.x — superseded. Single-file Type A/B framing.
