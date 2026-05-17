# Manifest — ai-council (session-sync)

<!-- scope: meta -->

## Handoff metadata

| Field | Value |
|---|---|
| Slug | `2026-05-17-ai-council-session-sync` |
| Type | session-sync |
| Target repo | `ai-council` |
| Repo path | `C:\Users\1028120\Documents\Dev\ai-council` |
| Generated | 2026-05-17 |
| Generator | Claude Code in `.dev-knowledge` |
| HANDOFF_PROCESS version | v3.3.3 |

## HEAD pin

| Field | Value |
|---|---|
| Stage 1 SHA | `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` |
| Stage 3 SHA (verified) | `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` |
| Branch | `main` |
| Ancestor check | PASS — no drift between Stage 1 and Stage 3 |

**Receiving session:** verify `git rev-parse HEAD` in ai-council matches the Stage 3 SHA above before acting. If it differs, stop and report to the operator.

## File index

| # | File | Description |
|---|---|---|
| 00a | `00_README.md` | Rob's upload instructions (do not upload to new chat) |
| 00b | `00_first-message.md` | Paste as first message in new chat (do not upload as attachment) |
| 01a | `01_MANIFEST.md` | This file — entry point, metadata, index |
| 01b | `01_manifest.json` | Machine-readable checksums (SHA-256) |
| 02 | `02_VISION.md` | ai-council VISION (full copy) |
| 02b | `02b_ECOSYSTEM_VISION.md` | .dev-knowledge VISION (full copy — cross-repo) |
| 03 | `03_PLAYBOOK.md` | .dev-knowledge PLAYBOOK (full copy) |
| 04 | `04_ESSENTIALS.md` | .dev-knowledge ESSENTIALS (full copy) |
| 05 | `05_GOVERNANCE_ESSENCES.md` | ADR essences for this handoff |
| 06 | `06_STATE_OF_PLAY.md` | Current state — reality + verified findings |
| 07 | `07_ACTION_PLAN.md` | Objective, directives, boundaries |
| 08 | `08_TREE.txt` | ai-council tracked file tree at HEAD |
| 09 | `09_EXECUTION_EVIDENCE.md` | Return-trip template |

## Stage 2 source

Stage 2 architect response provided by the existing (old) ai-council browser chat from its lived session knowledge. Response covers: research-mode question-formulation failure (witnessed, primary directive), AGENTS.md creation (governance gap, second priority), pre-commit hook verification, ADR-38 compliance, docs/HANDOFF.md status (verified absent at Stage 3), LESSONS.md scope-tag backfill (advisory).

Architect epistemic note: the architect chat's knowledge predates the docs-simplification session by at least one session. REALITY and RATIONALE in `06_STATE_OF_PLAY.md` are marked accordingly.

## Stage 3 verifications performed

- `git merge-base --is-ancestor 1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8 HEAD` → exit 0 (no drift)
- `git ls-files` confirmed: `AGENTS.md` absent, `docs/HANDOFF.md` absent
- ai-council Scale M files present: README.md ✓, VISION.md ✓, BACKLOG.md ✓, LESSONS.md ✓, JOURNAL.md ✓, CLAUDE.md ✓
- `CHANGELOG.md` absent ✓ (correctly removed per ADR-49)
