# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-05-16  
**Generated:** 2026-05-16T18:08:41  
**Repos audited:** 2  
**Checks:** 40 total — 8 pass, 28 fail, 4 warn, 0 unavailable

---

## .dev-knowledge — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-05-16

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'scale', 'status', 'tier', 'version'] |
| `adr38_baseline` | FAIL | Missing required: ['src', 'pyproject.toml'] |
| `claude_md` | PASS | CLAUDE.md present (9343 chars) |
| `dated_entries_lessons` | FAIL | LESSONS.md: non-ISO-date H2 heading found: '## Entries' |
| `dated_entries_journal` | PASS | JOURNAL.md: envelope OK (56 dated entries, reverse-chrono) |
| `dated_entries_changelog` | FAIL | CHANGELOG.md: ordering violation — '2026-04-24' before '2026-04-25' (not reverse-chrono) |
| `backlog_organization` | FAIL | BACKLOG_ARCHIVE.md missing (required alongside BACKLOG.md per ADR-47) |
| `backlog_organization` | FAIL | [done] token found in BACKLOG.md at line(s): [33, 42, 49, 61, 68] (extract to BACKLOG_ARCHIVE.md) |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] v3.3.2 — HANDOFF_FOLDER_TEMPLATE parameterization for cross-repo' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] PLAYBOOK content additions for ADRs 36/37/40/41' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] Audit tool P1 implementation' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] Cross-repo dated-entries format standard (Entry 1)' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] Cross-repo BACKLOG organization standard (Entry 2)' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P2] [done] Audit tool extension — ADR-46 + ADR-47 checks + extraction scrip' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] Phase 1 validation — audit + handoff dry-run on ai-council' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] AI Council cross-project transcript routing' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P2] [done] Structure and universalize scrum-master review propagation proce' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] ADR naming convention reconciliation (underscore vs hyphen)' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P1] [done] ADR naming convention reconciliation (unders' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P2] [done] ARCHITECTURE.md root placement enforcement' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P2] [done] ARCHITECTURE.md root placement enforcement' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P2] [open] Handoff folder format adoption (corp-monorep' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P2] [done] `_archive/` convention — standardize (drop underscore prefix per' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P2] [done] `_archive/` convention — standardize (drop u' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P3] [open] UPPERCASE TYPE tag in legacy archive filenam' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P3] [open] docs/HANDOFF.md flat file deprecation (corp-' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P3] [open] Undiscovered repos confirmation' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] .dev-knowledge atomic migration to hyphen convention (Prompt K s' |
| `backlog_organization` | FAIL | Entry heading does not match [P{N}] [open|superseded] pattern: '### [P1] [done] Cross-repo handshake: ADR-34 amendment propagation to ai-council' |
| `backlog_organization` | FAIL | Entry missing required fields ['Why']: '### [P3] [open] A5 Phase 2: retire UPPERCASE TYPE tag in leg' |
| `backlog_organization` | WARN | BACKLOG.md exceeds 300-line kill criterion (408 lines) — review ADR-47 |
| `backlog_organization` | WARN | Cross-stream section is 40% of open items (kill criterion: 33%) — review ADR-47 |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-05-16

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'scale', 'tier', 'version'] |
| `adr38_baseline` | WARN | Missing optional (ARCHITECTURE.md — required at tier L): ['ARCHITECTURE.md'] |
| `claude_md` | PASS | CLAUDE.md present (16736 chars) |
| `dated_entries_lessons` | WARN | LESSONS.md: no [scope: X] tag found in entries (ADR-46 sniff test) |
| `dated_entries_journal` | PASS | JOURNAL.md: envelope OK (19 dated entries, reverse-chrono) |
| `dated_entries_changelog` | PASS | CHANGELOG.md: envelope OK (4 dated entries, reverse-chrono) |
| `backlog_organization` | PASS | BACKLOG.md organization OK (11 open items, 8 streams) |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## Summary

- 2 repo(s) audited
- 8/40 checks passed
- **28 failure(s)** — route findings to repo owners
- 4 warning(s)

*Report generated by `scripts/audit.py`. Do not edit manually.*
