# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-09-26  
**Generated:** 2026-09-26T17:36:29  
**Repos audited:** 5  
**Checks:** 321 total — 87 pass, 8 fail, 45 warn, 0 unavailable, 181 n/a

---

## ai-council — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-09-26

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (33406 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct (explorer.sortOrderLexicographicOptions carries the sorting clause's asserted half), .vscode/ in-pattern |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-08-08 is 49d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-27 is 61d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-24 is 64d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 5 - INSTALL.md (no stamp; last content 2026-07-21); protocols/COUNCIL_INVOCATION_CONTRACT.md (no stamp; last content 2026-07-18); protocols/COUNCIL_QUESTION_GUIDE.md (no stamp; last content 2026-07-23); protocols/README.md (no stamp; last content 2026-07-11); protocols/SYNTHESIS_QUALITY_RUBRIC.md (no stamp; last content 2026-07-02) (+5 unstamped outside the gated set's directories, out of scope for this report) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 3 of 14 living docs (4 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): CONTRIBUTING.md  version handoff-process@5.7  declared 2026-07-24 (frontmatter)  derived 2026-07-24 (66bb5b1f5, unrefined)  0d  gated-and-fresh; VISION.md  version 1.0  declared 2026-07-23 (frontmatter)  derived 2026-07-23 (f9d69857d, unrefined)  0d  ungated-and-fresh |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | WARN | audits-index: declared input(s) with no git history — scripts/gen_audit_index.py; freshness cannot be verified over a partial input set; regenerate + commit: uv run --locked python scripts/gen_audit_index.py --write |
| `no_sibling_orphans` | PASS | No orphaned 'ai-council-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `supplement_folded` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no bundle whose supplement could be unfolded |
| `dispatch_verb_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/PLAYBOOK.md — no dispatch table to agree with |
| `reconciled_versions` | WARN | CONTRIBUTING.md: unknown-spec (protocols/HANDOFF_PROCESS.md absent or version unparseable) |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | ai-council: deployed methodology corpus v1.3.1 |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] ai-council: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | FAIL | 3 blocking defect(s): enum ADR-01-synthesizer-selection.md:6 — value 'Revised (2026-07-18)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED); enum ADR-02-default-panel.md:6 — value 'Revised (2026-05-11)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED); enum ADR-06-cost-optimization.md:6 — value 'Revised 2026-05-11 (Qwen trial deferred/abandoned)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED) // also detected: alternatives-considered-legacy=12, flip-condition-legacy=16, grammar=16, unindexed=16 |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |
| `substrate_declaration` | FAIL | substrate registry unreadable, so no contract was validated: could not read ecosystem/substrate-registry.yaml: FileNotFoundError(2, 'No such file or directory') |
| `routing_agreement` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/routing-table.yaml — this repo carries no routing table |
| `dispatch_drift` | N/A | [n/a-reason:SUBJECT-ABSENT] no protocols/PLAYBOOK.md / .claude/commands/lane-boot.md — this repo carries no dispatch surface |
| `consumer_at_landing` | WARN | 2026-03-15_CODE_REVIEW_REPORT.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-03-26_CODE_REVIEW_REPORT.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | no readable ecosystem/audit-consumer-baseline.json — the consumption ratchet is INERT (live unconsumed 111 of 138); the gate is not measuring growth |
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (0 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |
| `organ_truth` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/harness.yaml -- this repo declares no moments |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-09-26

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct (explorer.sortOrderLexicographicOptions carries the sorting clause's asserted half), .vscode/ in-pattern |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-07-12 is 76d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-13 is 75d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-18 is 70d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived gated-and-stale: 1 - CLAUDE.md (declared 2026-07-13 [frontmatter] at fa8a4e342; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-stale: 1 - .claude/skills/gotchas/gotchas.md (declared 2026-06-06 [prose] at d0989ee3b; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 3 - INSTALL.md (no stamp; last content 2026-07-11); protocols/CORP_INTERFACE.md (no stamp; last content 2026-07-12); protocols/README.md (no stamp; last content 2026-07-12) (+20 unstamped outside the gated set's directories, out of scope for this report) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 2 of 28 living docs (3 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): CONTRIBUTING.md  version handoff-process@v5  declared 2026-07-18 (frontmatter)  derived 2026-07-18 (5b9c6c388, unrefined)  0d  gated-and-fresh; VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (539333b4c, unrefined)  0d  ungated-and-fresh; CLAUDE.md  version 2.8  declared 2026-07-13 (frontmatter)  derived 2026-07-12 (20daab97d, unrefined)  -1d  1 unreviewed after stamp fa8a4e342  gated-and-stale |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — docs/audits/README.md |
| `no_sibling_orphans` | PASS | No orphaned 'corp-monorepo-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | WARN | 1 of 1 linked worktree(s) look unclosed (horizon 7d): vk/c35d-test [registered but gone from disk - run `git worktree prune`] - close them out per the /lane-integrate checklist, or say why they stay |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `supplement_folded` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no bundle whose supplement could be unfolded |
| `dispatch_verb_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/PLAYBOOK.md — no dispatch table to agree with |
| `reconciled_versions` | WARN | CONTRIBUTING.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | corp-monorepo: deployed methodology corpus v1.2.0 |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] corp-monorepo: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | FAIL | 14 blocking defect(s): single-field ADR-01-knowledge-architecture.md — no status field found in the header window; single-field ADR-02-extraction-quality.md — no status field found in the header window; single-field ADR-03-model-selection.md — no status field found in the header window; single-field ADR-04-vault-structure.md — no status field found in the header window; single-field ADR-05-reextraction-strategy.md — no status field found in the header window; single-field ADR-06-quality-gate.md — no status field found in the header window; single-field ADR-07-vault-navigation.md — no status field found in the header window; single-field ADR-08a-model-tiering.md — no status field found in the header window (+6 more) // also detected: alternatives-considered-legacy=22, duplicate-id=1, flip-condition-legacy=37, grammar=14, unindexed=23 |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |
| `substrate_declaration` | FAIL | substrate registry unreadable, so no contract was validated: could not read ecosystem/substrate-registry.yaml: FileNotFoundError(2, 'No such file or directory') |
| `routing_agreement` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/routing-table.yaml — this repo carries no routing table |
| `dispatch_drift` | N/A | [n/a-reason:SUBJECT-ABSENT] no protocols/PLAYBOOK.md / .claude/commands/lane-boot.md — this repo carries no dispatch surface |
| `consumer_at_landing` | WARN | 2026-07-07_AUDIT_demo-prep-recon.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_BRAINSTORM-BACKLOG_functional-requirements.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_BRIEF_algorithmic-adopt-map.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_BRIEF_golden-url-registry-knowledge-flow.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_BRIEF_obsidian-operating-model-v2.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_BRIEF_ontology-north-star.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_EVIDENCE_by-product-docs-tree-analysis.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-07_HANDOFF_functional-architect.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-08_AUDIT_fa-campaign-self-review.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-08_BRIEF_metadata-charter-T1.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | 2026-07-11_AUDIT_root-parity-disposition.md carries no resolvable landing date, so it cannot be placed against the 2026-08-27 cutoff — reported rather than assumed grandfathered |
| `consumer_at_landing` | WARN | no readable ecosystem/audit-consumer-baseline.json — the consumption ratchet is INERT (live unconsumed 43 of 64); the gate is not measuring growth |
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (0 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |
| `organ_truth` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/harness.yaml -- this repo declares no moments |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-09-26

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct (explorer.sortOrderLexicographicOptions carries the sorting clause's asserted half), .vscode/ in-pattern |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-06-02 is 116d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 116d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 116d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived gated-and-stale: 2 - ARCHITECTURE.md (declared 2026-06-02 [frontmatter] at 82b0343b2; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare); CLAUDE.md (declared 2026-06-02 [frontmatter] at 29ed7b7bd; 2 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 1 - INSTALL.md (no stamp; last content 2026-06-02) (+3 unstamped outside the gated set's directories, out of scope for this report) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 1 of 8 living docs (2 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (5515b300c, unrefined)  0d  ungated-and-fresh |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | WARN | audits-index: declared input(s) with no git history — scripts/gen_audit_index.py; freshness cannot be verified over a partial input set; regenerate + commit: uv run --locked python scripts/gen_audit_index.py --write |
| `no_sibling_orphans` | PASS | No orphaned 'corp-ops-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `supplement_folded` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no bundle whose supplement could be unfolded |
| `dispatch_verb_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/PLAYBOOK.md — no dispatch table to agree with |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] corp-ops: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] corp-ops: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | WARN | corpus unusable: no ADR-*.md files under C:\Users\1028120\Documents\Dev\corp-ops\docs\decisions |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |
| `substrate_declaration` | FAIL | substrate registry unreadable, so no contract was validated: could not read ecosystem/substrate-registry.yaml: FileNotFoundError(2, 'No such file or directory') |
| `routing_agreement` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/routing-table.yaml — this repo carries no routing table |
| `dispatch_drift` | N/A | [n/a-reason:SUBJECT-ABSENT] no protocols/PLAYBOOK.md / .claude/commands/lane-boot.md — this repo carries no dispatch surface |
| `consumer_at_landing` | WARN | no readable ecosystem/audit-consumer-baseline.json — the consumption ratchet is INERT (live unconsumed 2 of 2); the gate is not measuring growth |
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (0 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |
| `organ_truth` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/harness.yaml -- this repo declares no moments |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-09-26

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .corp-sca-time-automation.code-workspace: .vscode/keybindings.json is not shared editor configuration (vscode.dir_allowed) |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 6 warn: ARCHITECTURE.md: last_reviewed 2026-06-02 is 116d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 116d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived gated-and-stale: 2 - CLAUDE.md (declared 2026-06-02 [frontmatter] -> derived 2026-06-08, +6d); ARCHITECTURE.md (declared 2026-06-02 [frontmatter] at 112dc6acd; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 1 of 8 living docs (2 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (bf9cb88c7, unrefined)  0d  ungated-and-fresh |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | WARN | audits-index: declared input(s) with no git history — scripts/gen_audit_index.py; freshness cannot be verified over a partial input set; regenerate + commit: uv run --locked python scripts/gen_audit_index.py --write |
| `no_sibling_orphans` | PASS | No orphaned 'corp-sca-time-automation-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `supplement_folded` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no bundle whose supplement could be unfolded |
| `dispatch_verb_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/PLAYBOOK.md — no dispatch table to agree with |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] corp-sca-time-automation: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] corp-sca-time-automation: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | WARN | corpus unusable: no ADR-*.md files under C:\Users\1028120\Documents\Dev\corp-sca-time-automation\docs\decisions |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |
| `substrate_declaration` | FAIL | substrate registry unreadable, so no contract was validated: could not read ecosystem/substrate-registry.yaml: FileNotFoundError(2, 'No such file or directory') |
| `routing_agreement` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/routing-table.yaml — this repo carries no routing table |
| `dispatch_drift` | N/A | [n/a-reason:SUBJECT-ABSENT] no protocols/PLAYBOOK.md / .claude/commands/lane-boot.md — this repo carries no dispatch surface |
| `consumer_at_landing` | WARN | no readable ecosystem/audit-consumer-baseline.json — the consumption ratchet is INERT (live unconsumed 1 of 2); the gate is not measuring growth |
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (0 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |
| `organ_truth` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/harness.yaml -- this repo declares no moments |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## win-tooling — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\win-tooling`  
**Last audit:** 2026-09-26

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (10449 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | CONTRIBUTING.md: last_reviewed 2026-07-11 is 77d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 1 - README.md (no stamp; last content 2026-09-01) (+14 unstamped outside the gated set's directories, out of scope for this report) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 3 of 19 living docs (4 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (0286cd82d, unrefined)  0d  ungated-and-fresh |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — docs/audits/README.md |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | WARN | 6 of 6 linked worktree(s) look unclosed (horizon 7d): fix/cloud-models-fail-fast [last commit 31d ago]; feat/cloud-models [last commit 31d ago]; feat/codespace-name-from-stdout [last commit 11d ago]; fix/sanitise-external-text [last commit 31d ago]; fix/check-advisory-unowned-path [last commit 31d ago]; worktree-lane-ab-810-substrate-repair [last commit 10d ago] - close them out per the /lane-integrate checklist, or say why they stay |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/HANDOFF_PROCESS.md — nothing to validate |
| `amendment_coherence` | PASS | 0 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | PASS | CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean; pointers resolve (sha256 4d268f329a7e…) |
| `hooks_armed` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git-hook arming check skipped (not the hub repo) |
| `git_backlog_drift` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — git<->backlog drift check skipped (not the hub repo) |
| `doc_claims` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose-vs-state check skipped (not the hub repo) |
| `no_ff_merges` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — --no-ff guard skipped (not the hub repo) |
| `handoff_probes` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no probe bundle to validate |
| `supplement_folded` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — no bundle whose supplement could be unfolded |
| `dispatch_verb_agreement` | N/A | [n/a-reason:NOT-APPLICABLE] no protocols/PLAYBOOK.md — no dispatch table to agree with |
| `reconciled_versions` | N/A | [n/a-reason:NOT-APPLICABLE] no reconciled_with edges declared |
| `doc_rot` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc-rot / grooming checker skipped (not the hub repo) |
| `doc_structure` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — prose structural linter skipped (not the hub repo) |
| `doc_code_edge` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — doc->code edge check skipped (not the hub repo) |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | PASS | win-tooling: deployed methodology corpus v1.4.0 |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] win-tooling: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] win-tooling: block_unanchored_push=absent; canonical_freshness=present-unverified; reconciled_versions=n/a-no-edges; doc_claims=hub-scoped; git_backlog_drift=hub-scoped (static; enforcing-local proven only by scripts/enforcement_coverage.py) |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | N/A | [n/a-reason:SUBJECT-ABSENT] no docs/decisions/ in this repo — only the hub carries an ADR corpus |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |
| `substrate_declaration` | N/A | [n/a-reason:SUBJECT-ABSENT] no docs/audits/ — this repo carries no committed lane contracts |
| `routing_agreement` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/routing-table.yaml — this repo carries no routing table |
| `dispatch_drift` | N/A | [n/a-reason:SUBJECT-ABSENT] no protocols/PLAYBOOK.md / .claude/commands/lane-boot.md — this repo carries no dispatch surface |
| `consumer_at_landing` | N/A | [n/a-reason:SUBJECT-ABSENT] no docs/audits/ — this repo carries no audit corpus |
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (27 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |
| `organ_truth` | N/A | [n/a-reason:SUBJECT-ABSENT] no ecosystem/harness.yaml -- this repo declares no moments |

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 5 repo(s) audited
- 87/321 checks passed
- **8 failure(s)** — route findings to repo owners
- 45 warning(s)
- 181 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
