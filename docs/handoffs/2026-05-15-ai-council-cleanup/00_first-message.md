# Prompt — ai-council ADR-46+47 Compliance Cleanup

| Field  | Value                                    |
|--------|------------------------------------------|
| Model  | Sonnet                                   |
| Mode   | Auto-accept                              |
| Effort | medium                                   |

**Repo:** `ai-council` (`C:\Users\1028120\Documents\Dev\ai-council`)
**Branch:** `main` (work directly on main; changes are documentation only)
**Purpose:** Bring ai-council into compliance with ADR-46 (dated-entries format)
and ADR-47 (BACKLOG organization). Driven by the 2026-05-15 ecosystem audit.
**This prompt does NOT make code changes** — documentation files only.

---

## Read first

This bundle lives at:
`C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\handoffs\2026-05-15-ai-council-cleanup\`

Read in this order:
1. `01_MANIFEST.md` — entry point, HEAD pin
2. `06_STATE_OF_PLAY.md` — audit findings + migration decisions locked
3. `05_GOVERNANCE_ESSENCES.md` — ADR-46 + ADR-47 rules (the binding standards)
4. `07_ACTION_PLAN.md` — directives (7 steps)
5. `08_TREE.txt` — ai-council file inventory + in-scope files

Also read `CLAUDE.md` in this repo (ai-council) for local conventions.

---

## Git workflow

```
git rev-parse HEAD        # must match 0f069554b894802504aa4e5ce140b1d481ae9ec8
git status --porcelain    # must be empty
```

If HEAD mismatch: **STOP**. Report to operator before any work.

Work directly on `main` — this is documentation-only cleanup (no code, no tests).
Per-directive commits per `07_ACTION_PLAN.md`.

**Do NOT push to remote. Do NOT merge anything.**

---

## UNDERSTAND

**Problem.** The 2026-05-15 ecosystem audit flagged 5 FAIL checks in ai-council:
1. LESSONS.md: `## Session: Phase 1 Foundation (2026-02-21)` — non-ISO H2 envelope
2. JOURNAL.md: `2026-03-15` entry appears before `2026-05-12` — ordering violation
3. BACKLOG.md: BACKLOG_ARCHIVE.md missing
4. BACKLOG.md: `[blocked]` heading — not in ADR-47 vocabulary
5. BACKLOG.md: 11 entries missing `**Status:**` field

**Scope.** Fix all 5 FAIL checks. Touch only: LESSONS.md, JOURNAL.md, BACKLOG.md,
BACKLOG_ARCHIVE.md (new), CHANGELOG.md, JOURNAL.md (close-out entry).

**Migration decisions are locked** (universalization principle — ai-council conforms
to the standard; the standard is not amended for ai-council):
- A: `[blocked]` → `[open]` + `**Blocked:** <reason>` body annotation
- B: `## Session: Phase 1 Foundation (2026-02-21)` → `## 2026-02-21` + session
  label moves to body as `**Session:** Phase 1 Foundation` prose line

**Risks this prompt prevents:**
- Re-debating locked migration decisions — they are decided, implement them
- Content changes inside entry bodies — only structural edits (headings, ordering,
  status fields, body annotations)
- Writing to .dev-knowledge — read-only access to bundle files only
- Pushing to remote — stays local until operator review

---

## Steps (execute in order per `07_ACTION_PLAN.md`)

### Step 1 — Pre-flight
```
git rev-parse HEAD
git status --porcelain
```
Read LESSONS.md, JOURNAL.md, BACKLOG.md before editing.

### Step 2 — LESSONS.md: migrate session envelope to ISO
- Find `## Session: Phase 1 Foundation (2026-02-21)`
- Rename to `## 2026-02-21`
- Add `**Session:** Phase 1 Foundation` line under heading
- Verify `## Session:` no longer appears

**COMMIT:** `docs(lessons): migrate session envelope to ISO format per ADR-46 [cleanup]`

### Step 3 — JOURNAL.md: restore reverse-chrono ordering
- Locate `2026-03-15` entry block
- Move to correct position (after 2026-05-12 entries, before anything earlier)
- Verify dates descend from top to bottom

**COMMIT:** `docs(journal): restore reverse-chrono ordering per ADR-46 [cleanup]`

### Step 4 — BACKLOG.md: create BACKLOG_ARCHIVE.md
- Create `BACKLOG_ARCHIVE.md` at repo root (empty scaffold with scope tag)
- No items to archive (no `[done]` entries in current BACKLOG.md)

**COMMIT:** `chore(backlog): create BACKLOG_ARCHIVE.md scaffold per ADR-47 [cleanup]`

### Step 5 — BACKLOG.md: migrate `[blocked]` + add `Status:` to all 11 entries
- Change `[blocked]` heading to `[open]` + add `**Blocked:**` body bullet
- Add `- **Status:** open` to all 11 entries

**COMMIT:** `chore(backlog): migrate [blocked] → [open] + add Status fields per ADR-47 [cleanup]`

### Step 6 — CHANGELOG + JOURNAL close-out entries
- CHANGELOG: prepend `## 2026-05-15` entry with `### Changed` group
- JOURNAL: prepend `## 2026-05-15 — ADR-46+47 compliance cleanup (cross-repo handoff)` entry

**COMMIT:** `docs(changelog): ADR-46+47 compliance cleanup [cleanup]`
**COMMIT:** `docs(journal): 2026-05-15 ADR-46+47 compliance cleanup [cleanup]`

### Step 7 — Fill 09_EXECUTION_EVIDENCE.md and signal completion
Fill:
`C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\handoffs\2026-05-15-ai-council-cleanup\09_EXECUTION_EVIDENCE.md`

Run `git rev-parse HEAD` in ai-council and record the final SHA.
Run `git status --porcelain` — must be clean.

Signal: "Execution complete. Return to .dev-knowledge and run `python scripts/audit.py run`."

---

## What NOT to do

- Do NOT modify any `.dev-knowledge` file. Bundle files are read-only context.
- Do NOT re-debate `[blocked]` vs ADR-47 amendment. Decision is locked.
- Do NOT re-debate session-numbered envelope vs ISO. Decision is locked.
- Do NOT change content inside LESSONS.md entry bodies (only the `## Session:` heading changes).
- Do NOT change JOURNAL.md entry body text (only block position changes).
- Do NOT create ARCHITECTURE.md — that's a separate tracked item (P3 Governance in BACKLOG).
- Do NOT touch source code, tests, or config files.
- Do NOT push to remote.
- Do NOT use `[blocked]` status anywhere (not in ADR-47 vocabulary).

---

## Final

Post-execution state:
- All 5 audit FAIL checks fixed in ai-council
- Working tree clean
- 09_EXECUTION_EVIDENCE.md filled

**Next:** Operator runs `python scripts/audit.py run` from `.dev-knowledge`.
Expected: ai-council `dated_entries_lessons`, `dated_entries_journal`,
`backlog_organization` all PASS. Stream B P1 items flip to `[done]` on clean audit.
