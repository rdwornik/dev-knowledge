# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-08-07  
**Generated:** 2026-08-07T09:40:28  
**Repos audited:** 6  
**Checks:** 264 total — 105 pass, 3 fail, 31 warn, 0 unavailable, 125 n/a

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (28505 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `canonical_freshness` | PASS | 9 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v6.0.1 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | pre-commit / commit-msg / pre-push installed and pre-commit-managed |
| `git_backlog_drift` | PASS | no closed-but-present backlog drift (direction (a) STRONG, full history) |
| `doc_claims` | PASS | 4 doc self-claim(s) match repo state |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 533109f20 (2026-06-26) docs(journal): record 2026-06-26 freshness re-stamp session (3bd2cd1) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 3a894eeb5 (2026-06-19) docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): d0f9ead67 (2026-06-19) chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability) |
| `handoff_probes` | WARN | P0a skipped in 2026-08-06-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0b skipped in 2026-08-06-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0c skipped in 2026-08-06-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P1a skipped in 2026-08-06-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P1b skipped in 2026-08-06-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P8 skipped in 2026-08-06-dev-knowledge-architect: tool absent: ls |
| `reconciled_versions` | WARN | templates/CONTRIBUTING-md-template.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#492 (3 dated block(s), 1035 chars (>= 3 dates & > 700, or > 1200)) |
| `doc_structure` | PASS | no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme) |
| `doc_code_edge` | PASS | 15 doc->code edge(s) resolved; none broken/ambiguous/orphaned |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub - source of the 5 enforcement organs; per-consumer coverage is measured by scripts/enforcement_coverage.py (read-only reporter) |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): VISION.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-30-tech-browser-architect-orientation.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/AI_COUNCIL_PROCESS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/ESSENTIALS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/PLAYBOOK.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/SESSION_SETUP.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/README.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `doc_code_coverage_drift` | PASS | all 41 ALL_CHECKS members covered (coverage_scope-annotated or exempt); none escape coverage_scope |
| `import_edges` | PASS | 3 @import edge(s) resolve across 4 file(s) |
| `fleet_parity` | WARN | ai-council root-sweep WARN-undeclared: top-level entry 'conftest.py' is not in the template for role 'consumer' |
| `routine_consumers` | PASS | 2 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | PASS | live 441 <= baseline 441 under detector silent-rule-v4 (57 file(s) in scope) |
| `task_tree_coherence` | PASS | BACKLOG.md coherent with the tasks/ source of truth (structure + frontmatter honesty + full reassembly) |
| `intake_tree_coherence` | PASS | intake residue carrier coherent (261 node(s), 15160 README.md byte(s)) |
| `boot_byte_budget` | PASS | protocols/HANDOFF_BOOT.md is 16842 bytes, within its 18000-byte budget |
| `fleet_audit_replication` | PASS | automation/fleet-audit is replicated to origin (0 commits ahead) |
| `membership_agreement` | PASS | 9 declared (ADR-104); 5 resolved members (deployed-versions); coverage registry-md 9/9, index-yaml 6/9, deployed-versions 5/9, parity-surfaces 5/9, onboarding-rulings 4/9, state-dirs 6/9; declared-but-not-deployed: demo-prep [registry-md, onboarding-rulings]; life-architect [registry-md, onboarding-rulings]; terminal-setup [registry-md]; win-tooling [registry-md, index-yaml, state-dirs] |
| `membership_agreement` | PASS | declaration source: ADR-104 anchor 'adr104-fleet-members', 9 ids, agrees with audit.ADR104_FLEET_DECLARATION |
| `journal_spine_anchor` | PASS | every first-parent spine entry above the ADR-85 disposition floor 24882f8cc is JOURNAL-anchored |
| `preflight_backlog_ids` | WARN | 1 kill-candidates assertion(s) name a non-open row: [#310] -> #292 — advisory per the [#483] ruling R3 |
| `review_artifact_coverage` | WARN | 2 code-impact merge(s) since 2026-08-05 carry no linked review artifact: a4f4f1e9 worktree-lane-b-503-doc-currency, 6714f7cd worktree-lane-a-501-ci-recorder -- advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `review_artifact_coverage` | WARN | 1 linked artifact(s) carry no parseable **Tally:** line: 5af0b33c -> 2026-08-06-codex-lane-c-504-failclosed.md -- persistence is not machine-auditability; advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — PASS

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (33406 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | PASS | 9 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | WARN | CONTRIBUTING.md: unknown-spec (protocols/HANDOFF_PROCESS.md absent or version unparseable) |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | ai-council: deployed methodology corpus v1.3.1 |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] ai-council: block_unanchored_push=absent; canonical_freshness=present-unverified; reconciled_versions=absent; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- fleet-parity walk skipped (not the hub repo) |
| `routine_consumers` | PASS | 0 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the detector's scope roots are hub governance surfaces |
| `task_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — tasks/ is a hub-owned tree |
| `intake_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the docs/intake/ residue carrier is hub-owned |
| `boot_byte_budget` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot |
| `fleet_audit_replication` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- automation/fleet-audit is hub-owned machinery |
| `membership_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the ecosystem/ membership surfaces are hub-owned |
| `journal_spine_anchor` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | 1 linked worktree(s) registered, each committed within the 7d horizon and present on disk - live batch lanes, not leftovers |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | WARN | CONTRIBUTING.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | corp-monorepo: deployed methodology corpus v1.2.0 |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] corp-monorepo: block_unanchored_push=absent; canonical_freshness=present-unverified; reconciled_versions=absent; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- fleet-parity walk skipped (not the hub repo) |
| `routine_consumers` | PASS | 0 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the detector's scope roots are hub governance surfaces |
| `task_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — tasks/ is a hub-owned tree |
| `intake_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the docs/intake/ residue carrier is hub-owned |
| `boot_byte_budget` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot |
| `fleet_audit_replication` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- automation/fleet-audit is hub-owned machinery |
| `membership_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the ecosystem/ membership surfaces are hub-owned |
| `journal_spine_anchor` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] corp-ops: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] corp-ops: block_unanchored_push=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 0 @import edge(s) resolve across 1 file(s) |
| `fleet_parity` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- fleet-parity walk skipped (not the hub repo) |
| `routine_consumers` | PASS | 0 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the detector's scope roots are hub governance surfaces |
| `task_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — tasks/ is a hub-owned tree |
| `intake_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the docs/intake/ residue carrier is hub-owned |
| `boot_byte_budget` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot |
| `fleet_audit_replication` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- automation/fleet-audit is hub-owned machinery |
| `membership_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the ecosystem/ membership surfaces are hub-owned |
| `journal_spine_anchor` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 3 warn: VISION.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 66d old (> 30d cadence) |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] corp-sca-time-automation: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] corp-sca-time-automation: block_unanchored_push=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 1 @import edge(s) resolve across 2 file(s) |
| `fleet_parity` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- fleet-parity walk skipped (not the hub repo) |
| `routine_consumers` | PASS | 0 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the detector's scope roots are hub governance surfaces |
| `task_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — tasks/ is a hub-owned tree |
| `intake_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the docs/intake/ residue carrier is hub-owned |
| `boot_byte_budget` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot |
| `fleet_audit_replication` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- automation/fleet-audit is hub-owned machinery |
| `membership_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the ecosystem/ membership surfaces are hub-owned |
| `journal_spine_anchor` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## win-tooling — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\win-tooling`  
**Last audit:** 2026-08-07

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6859 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 2 stale (edited since review): VISION.md: last_reviewed 2026-07-11 predates last edit 2026-07-12 - edited but not re-reviewed; ARCHITECTURE.md: last_reviewed 2026-07-11 predates last edit 2026-08-06 - edited but not re-reviewed |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | WARN | win-tooling not listed in deployed-versions.yaml (ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] win-tooling: block_unanchored_push=absent; canonical_freshness=absent; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
| `undeclared_edges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — undeclared-edge scan skipped (not the hub repo) |
| `doc_code_coverage_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- coverage drift-guard skipped (not the hub repo) |
| `import_edges` | PASS | 0 @import edge(s) resolve across 1 file(s) |
| `fleet_parity` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- fleet-parity walk skipped (not the hub repo) |
| `routine_consumers` | PASS | 0 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the detector's scope roots are hub governance surfaces |
| `task_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — tasks/ is a hub-owned tree |
| `intake_tree_coherence` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — the docs/intake/ residue carrier is hub-owned |
| `boot_byte_budget` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot |
| `fleet_audit_replication` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- automation/fleet-audit is hub-owned machinery |
| `membership_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the ecosystem/ membership surfaces are hub-owned |
| `journal_spine_anchor` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 6 repo(s) audited
- 105/264 checks passed
- **3 failure(s)** — route findings to repo owners
- 31 warning(s)
- 125 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
