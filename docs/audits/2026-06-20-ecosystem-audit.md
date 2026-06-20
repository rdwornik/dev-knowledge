# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-06-20  
**Generated:** 2026-06-20T14:15:56  
**Repos audited:** 5  
**Checks:** 110 total — 95 pass, 2 fail, 0 warn, 0 unavailable, 13 n/a

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-06-20

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22314 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `handoff_tag_canonicity` | N/A | §3.1 section not found (consolidated?) — nothing to lint |
| `canonical_freshness` | PASS | 6 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v5.2 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | 10 probe(s) bind to live state (2026-06-19-dev-knowledge-architect) |
| `reconciled_versions` | PASS | 1 reconciled_with edge(s) match live spec version(s) |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-06-20

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (9159 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 6 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-06-20

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (8831 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-06 - edited but not re-reviewed |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-06-20

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 6 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-06-20

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `mermaid_theme_directive` | PASS | All mermaid blocks use base+themeVariables; all classDef fill: have color: |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## Summary

- 5 repo(s) audited
- 95/110 checks passed
- **2 failure(s)** — route findings to repo owners
- 13 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
