# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-06-04  
**Generated:** 2026-06-04T01:11:44  
**Repos audited:** 5  
**Checks:** 60 total — 59 pass, 1 fail, 0 warn, 0 unavailable

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-06-04

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (17960 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | 5 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `handoff_tag_canonicity` | PASS | §3.1 canonical: four canonical tags enumerated |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-06-04

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (9159 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-06-04

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (8922 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): ARCHITECTURE.md: last_reviewed 2026-06-02 predates last edit 2026-06-03 - edited but not re-reviewed |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-06-04

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-06-04

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6662 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## Summary

- 5 repo(s) audited
- 59/60 checks passed
- **1 failure(s)** — route findings to repo owners

*Report generated by `scripts/audit.py`. Do not edit manually.*
