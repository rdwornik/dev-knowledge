# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-07-10  
**Generated:** 2026-07-10T00:10:18  
**Repos audited:** 5  
**Checks:** 153 total — 120 pass, 1 fail, 13 warn, 0 unavailable, 19 n/a

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-07-10

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (26832 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `handoff_tag_canonicity` | N/A | §3.1 section not found (consolidated?) — nothing to lint |
| `canonical_freshness` | PASS | 8 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v5.7 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | pre-commit / commit-msg / pre-push installed and pre-commit-managed |
| `git_backlog_drift` | PASS | no closed-but-present backlog drift (direction (a) STRONG, full history) |
| `doc_claims` | PASS | 4 doc self-claim(s) match repo state |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 533109f20 (2026-06-26) docs(journal): record 2026-06-26 freshness re-stamp session (3bd2cd1) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 3a894eeb5 (2026-06-19) docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): d0f9ead67 (2026-06-19) chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability) |
| `handoff_probes` | PASS | 10 probe(s) bind to live state (2026-07-10-dev-knowledge-architect) |
| `reconciled_versions` | PASS | 5 reconciled_with edge(s) match live spec version(s) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#262 (4 dated block(s), 1640 chars (>= 3 dates & > 700, or > 1200)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#278 (3 dated block(s), 1508 chars (>= 3 dates & > 700, or > 1200)) |
| `doc_structure` | PASS | no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme) |
| `doc_code_edge` | PASS | 13 doc->code edge(s) resolved; none broken/ambiguous/orphaned |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `deployed_methodology_version` | N/A | .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | hub - source of the 5 enforcement organs; per-consumer coverage is measured by scripts/enforcement_coverage.py (read-only reporter) |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): VISION.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/AI_COUNCIL_PROCESS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/ESSENTIALS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/PLAYBOOK.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/SESSION_SETUP.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `doc_code_coverage_drift` | PASS | all 29 ALL_CHECKS members covered (coverage_scope-annotated or exempt); none escape coverage_scope |
| `import_edges` | PASS | 3 @import edge(s) resolve across 4 file(s) |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-07-10

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (10972 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | PASS | 8 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | PASS | hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `deployed_methodology_version` | PASS | ai-council: deployed methodology corpus v1.2.0 |
| `enforcement_coverage` | N/A | ai-council: session_end_backpressure=present-unverified; canonical_freshness=present-unverified; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-07-10

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (10935 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-04 is 36d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | PASS | hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `deployed_methodology_version` | PASS | corp-monorepo: deployed methodology corpus v1.2.0 |
| `enforcement_coverage` | N/A | corp-monorepo: session_end_backpressure=present-unverified; canonical_freshness=present-unverified; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-07-10

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `deployed_methodology_version` | N/A | corp-ops: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | corp-ops: session_end_backpressure=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 0 @import edge(s) resolve across 1 file(s) |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-07-10

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 3 warn: VISION.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 38d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | PASS | hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | PASS | no reconciled_with edges declared |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `deployed_methodology_version` | N/A | corp-sca-time-automation: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | corp-sca-time-automation: session_end_backpressure=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## Summary

- 5 repo(s) audited
- 120/153 checks passed
- **1 failure(s)** — route findings to repo owners
- 13 warning(s)
- 19 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
