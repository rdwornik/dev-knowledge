# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-07-25  
**Generated:** 2026-07-25T15:32:59  
**Repos audited:** 6  
**Checks:** 186 total — 153 pass, 3 fail, 7 warn, 0 unavailable, 23 n/a

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-07-25

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (39363 chars) |
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
| `hooks_armed` | PASS | hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | PASS | hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | PASS | hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | PASS | hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | PASS | 11 probe(s) bind to live state (2026-07-23-dev-knowledge-architect) |
| `reconciled_versions` | WARN | templates/CONTRIBUTING-md-template.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | .dev-knowledge: session_end_backpressure=present-unverified; canonical_freshness=absent; reconciled_versions=absent; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 3 @import edge(s) resolve across 4 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-07-25

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (30507 chars) |
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
| `reconciled_versions` | WARN | CONTRIBUTING.md: unknown-spec (protocols/HANDOFF_PROCESS.md absent or version unparseable) |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | ai-council: deployed methodology corpus v1.3.1 |
| `enforcement_coverage` | N/A | ai-council: session_end_backpressure=present-unverified; canonical_freshness=present-unverified; reconciled_versions=absent; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-07-25

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence) |
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
| `reconciled_versions` | WARN | CONTRIBUTING.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | PASS | hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | PASS | hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | PASS | hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | corp-monorepo: deployed methodology corpus v1.2.0 |
| `enforcement_coverage` | N/A | corp-monorepo: session_end_backpressure=present-unverified; canonical_freshness=present-unverified; reconciled_versions=absent; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-07-25

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
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence) |
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
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | corp-ops: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | corp-ops: session_end_backpressure=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 0 @import edge(s) resolve across 1 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-07-25

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
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 3 warn: VISION.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 53d old (> 30d cadence) |
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
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | corp-sca-time-automation: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | corp-sca-time-automation: session_end_backpressure=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## win-tooling — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\win-tooling`  
**Last audit:** 2026-07-25

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6859 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | no docs/handoffs/ — nothing to validate |
| `handoff_tag_canonicity` | N/A | no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `canonical_freshness` | FAIL | 2 stale (edited since review): VISION.md: last_reviewed 2026-07-11 predates last edit 2026-07-12 - edited but not re-reviewed; ARCHITECTURE.md: last_reviewed 2026-07-11 predates last edit 2026-07-12 - edited but not re-reviewed |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
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
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | WARN | win-tooling not listed in deployed-versions.yaml (ADR-91) |
| `enforcement_coverage` | N/A | win-tooling: session_end_backpressure=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | PASS | hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | PASS | hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 0 @import edge(s) resolve across 1 file(s) |
| `fleet_parity` | PASS | hub-only -- fleet-parity walk skipped (not the hub repo) |

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 6 repo(s) audited
- 153/186 checks passed
- **3 failure(s)** — route findings to repo owners
- 7 warning(s)
- 23 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
