# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-06-02  
**Generated:** 2026-06-02T10:44:26  
**Repos audited:** 5  
**Checks:** 60 total — 47 pass, 12 fail, 1 warn, 0 unavailable

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-06-02

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (12094 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | 4 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `handoff_tag_canonicity` | PASS | §3.1 canonical: four canonical tags enumerated |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-06-02

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | FAIL | Missing required: ['CONTRIBUTING.md'] |
| `claude_md` | PASS | CLAUDE.md present (8758 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | FAIL | Missing mandatory canonical files: ['CONTRIBUTING.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | FAIL | Canonical file(s) missing required spine heading(s): ["VISION.md: '## Vision'", "VISION.md: '## Values'", "VISION.md: '## References'", "ARCHITECTURE.md: '## Key conventions'", "ARCHITECTURE.md: '## Authority and governance'", "ARCHITECTURE.md: '## Validators and enforcement'", "BACKLOG.md: '## Big picture'", "LESSONS.md: '# Lessons Learned'"] |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-06-02

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | FAIL | Missing required: ['LESSONS.md'] |
| `claude_md` | PASS | CLAUDE.md present (8922 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | FAIL | Missing mandatory canonical files: ['LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | FAIL | Canonical file(s) missing required spine heading(s): ["ARCHITECTURE.md: '## Key conventions'", "ARCHITECTURE.md: '## Authority and governance'", "ARCHITECTURE.md: '## Validators and enforcement'", "BACKLOG.md: '## Big picture'", "CONTRIBUTING.md: '## Branch naming'", "CONTRIBUTING.md: '## Commit style'", "CONTRIBUTING.md: '## Handoff process'", "JOURNAL.md: '# Journal'"] |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-06-02

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | FAIL | Missing required: ['CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `claude_md` | PASS | CLAUDE.md present (6399 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | FAIL | Missing mandatory canonical files: ['CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 4 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | FAIL | Canonical file(s) missing required spine heading(s): ["VISION.md: '## Values'", "ARCHITECTURE.md: '## Key conventions'", "ARCHITECTURE.md: '## Authority and governance'", "ARCHITECTURE.md: '## Validators and enforcement'", "BACKLOG.md: '## Big picture'"] |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-06-02

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | FAIL | Missing required: ['CONTRIBUTING.md', 'LESSONS.md'] |
| `claude_md` | PASS | CLAUDE.md present (6671 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | FAIL | Missing mandatory canonical files: ['CONTRIBUTING.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | WARN | CLAUDE.md: no parseable last_reviewed frontmatter |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | FAIL | Canonical file(s) missing required spine heading(s): ["VISION.md: '## Values'", "ARCHITECTURE.md: '## Key conventions'", "ARCHITECTURE.md: '## Authority and governance'", "ARCHITECTURE.md: '## Validators and enforcement'", "CLAUDE.md: '## 5. Critical rules'", "CLAUDE.md: '## 6. Session start protocol'", "BACKLOG.md: '## Big picture'", "JOURNAL.md: '# Journal'"] |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## Summary

- 5 repo(s) audited
- 47/60 checks passed
- **12 failure(s)** — route findings to repo owners
- 1 warning(s)

*Report generated by `scripts/audit.py`. Do not edit manually.*
