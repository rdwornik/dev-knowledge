# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-09-09  
**Generated:** 2026-09-09T00:59:33  
**Repos audited:** 6  
**Checks:** 468 total — 139 pass, 8 fail, 140 warn, 0 unavailable, 181 n/a

---

## .dev-knowledge — PASS

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | N/A | [n/a-reason:NOT-APPLICABLE] VISION.md is registry-RETIRED (canonical_docs.CANONICAL_RETIRED) -- root presence is no longer required |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (23222 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `canonical_freshness` | PASS | 8 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `canonical_freshness` | PASS | derived gated-and-fresh: 8 of 39 living docs (20 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): ARCHITECTURE.md  version handoff-process@7.0.0  declared 2026-09-08 (frontmatter)  derived 2026-09-08 (07425ce20, unrefined)  0d  gated-and-fresh; CLAUDE.md  version 2.77  declared 2026-09-08 (frontmatter)  derived 2026-09-08 (aab6dfea0, unrefined)  0d  gated-and-fresh; CONTRIBUTING.md  version handoff-process@7.0.0  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (c431873bc, unrefined)  0d  gated-and-fresh; README.md  version 1.1  declared 2026-09-06 (frontmatter)  derived 2026-09-06 (28e3b1c35, unrefined)  0d  ungated-and-fresh; docs/handoffs/README.md  version handoff-process@7.0.0  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (b8599fbc4, unrefined)  0d  gated-and-fresh; protocols/AI_COUNCIL_PROCESS.md  version 2.2  declared 2026-09-04 (frontmatter)  derived 2026-09-04 (51bfe4f8a, unrefined)  0d  gated-and-fresh; protocols/HANDOFF_BOOT.md  version handoff-process@7.0.0  declared 2026-09-07 (frontmatter)  derived 2026-09-07 (5cb41d6b4, unrefined)  0d  ungated-and-fresh; protocols/HANDOFF_PROCESS.md  version 7.0.0  declared 2026-09-08 (frontmatter)  derived 2026-09-08 (4aedae11f, unrefined)  0d  ungated-and-fresh; protocols/OPERATOR-INTERFACE.md  version handoff-process@7.0.0  declared 2026-09-08 (frontmatter)  derived 2026-09-08 (4aedae11f, unrefined)  0d  ungated-and-fresh; protocols/PLAYBOOK.md  version handoff-process@7.0.0  declared 2026-09-08 (prose)  derived 2026-09-08 (fc6ceae73, unrefined)  0d  ungated-and-fresh; protocols/README.md  version handoff-process@7.0.0  declared 2026-09-06 (frontmatter)  derived 2026-09-06 (c87d54b1e, unrefined)  0d  ungated-and-fresh; protocols/SESSION_SETUP.md  version handoff-process@7.0.0  declared 2026-09-02 (frontmatter)  derived 2026-09-02 (a8e801862, unrefined)  0d  gated-and-fresh |
| `generated_artifact_freshness` | PASS | conformance-dashboard: 3d stale (baseline 4d) — ecosystem/conformance.md committed 2026-09-05, newest input BACKLOG.md committed 2026-09-08 |
| `generated_artifact_freshness` | PASS | audits-index: 0d stale (baseline 0d) — docs/audits/README.md committed 2026-09-07, newest input docs/audits committed 2026-09-07 |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | 1 linked worktree(s) registered, each committed within the 7d horizon and present on disk - live batch lanes, not leftovers |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v7.0.0 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | pre-commit / commit-msg / pre-push installed and pre-commit-managed; merge.ours.driver armed for the declared merge=ours pin |
| `git_backlog_drift` | PASS | no closed-but-present backlog drift (direction (a) STRONG, full history) |
| `doc_claims` | PASS | 4 doc self-claim(s) match repo state |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 533109f20 (2026-06-26) docs(journal): record 2026-06-26 freshness re-stamp session (3bd2cd1) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 3a894eeb5 (2026-06-19) docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): d0f9ead67 (2026-06-19) chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability) |
| `handoff_probes` | PASS | 15 probe(s) bind to live state (2026-09-08-dev-knowledge-architect-2) |
| `supplement_folded` | PASS | every filled SUPPLEMENT reached its paste — pre-era, immutable-and-lost (recorded, not repaired): 2026-08-23-dev-knowledge-architect |
| `dispatch_verb_agreement` | PASS | both point-of-use sites name the verb Ch8's dispatch table rules, and neither carries a rival literal launch form |
| `reconciled_versions` | PASS | 14 reconciled_with edge(s) match live spec version(s) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#241 (3 history dates spanning 64d, 2553 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#267 (3 history dates spanning 53d, 2188 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#297 (3 history dates spanning 51d, 1327 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#285 (5 history dates spanning 61d, 2556 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#82 (3 history dates spanning 51d, 2110 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#row-length (78 of 231 rows over the declared ceiling 1320 chars (LONG, not rot: a row may be long for a ruled reason); longest 5438 chars; row-length p50/p75/p90 over all 231 rows = 1273/1602/2372 chars; trend: +2 vs previous run (76 -> 78)) |
| `doc_rot` | WARN | history-accretion bloat: grooming-cadence BACKLOG#grooming-cadence (last groom 2026-07-30, 41d ago (> 21d cadence, ADR-41)) |
| `doc_structure` | PASS | no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme) |
| `doc_code_edge` | PASS | 16 doc->code edge(s) resolved; none broken/ambiguous/orphaned |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `plugin_version_drift` | N/A | [n/a-reason:NOT-APPLICABLE] .dev-knowledge: unset -- no carrier #2 plugin version recorded yet (deploy-runbook writes it; DECLARE-F F-3) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub - source of the 5 enforcement organs; per-consumer coverage is measured by scripts/enforcement_coverage.py (read-only reporter) |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-30-tech-browser-architect-orientation.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-05-func-simplification-distribution-wave.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-06-tech-adoption-consolidation-intake.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/AI_COUNCIL_PROCESS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/ESSENTIALS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_BOOT.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_PROCESS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/PLAYBOOK.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> prompt-template (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/README.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): ecosystem/conformance.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `doc_code_coverage_drift` | PASS | all 55 ALL_CHECKS members covered (coverage_scope-annotated or exempt); none escape coverage_scope |
| `import_edges` | PASS | 4 @import edge(s) resolve across 5 file(s) |
| `fleet_parity` | PASS | fleet at parity -- AT-PARITY 192, PASS-declared 19, advisory-rewarn 3, gate-ahead-declared 1, skipped-pre-deploy 6, stale-declaration 1 (blocking verdicts: 0) |
| `routine_consumers` | PASS | 2 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | PASS | live 447 <= baseline 447 under detector silent-rule-v5 (64 file(s) in scope) |
| `task_tree_coherence` | PASS | BACKLOG.md coherent with the tasks/ source of truth (structure + frontmatter honesty + full reassembly) |
| `intake_tree_coherence` | PASS | intake residue carrier coherent (375 node(s), 27485 README.md byte(s)) |
| `boot_byte_budget` | PASS | protocols/HANDOFF_BOOT.md is 17987 bytes, within its 18000-byte budget |
| `fleet_audit_replication` | PASS | automation/fleet-audit is replicated to origin (0 commits ahead) |
| `membership_agreement` | PASS | 9 declared (ADR-104); 7 resolved members (deployed-versions); coverage registry-md 9/9, index-yaml 6/9, deployed-versions 7/9, parity-surfaces 9/9, onboarding-rulings 6/9, state-dirs 6/9; declared-but-not-deployed: demo-prep [registry-md, parity-surfaces, onboarding-rulings]; life-architect [registry-md, parity-surfaces, onboarding-rulings] |
| `membership_agreement` | PASS | declaration source: ADR-104 anchor 'adr104-fleet-members', 9 ids, agrees with audit.ADR104_FLEET_DECLARATION |
| `journal_spine_anchor` | PASS | every first-parent spine entry above the ADR-85 disposition floor 24882f8cc is JOURNAL-anchored |
| `journal_spine_anchor` | WARN | anchored by mention, not by record: aeea0e0 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 988944e appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: fc6ceae appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: a897c54 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 18bf725 appears outside an explicit 'Anchors:' record line (+857 more) |
| `journal_day_letters` | PASS | JOURNAL day-letter suffixes are unique per day since 2026-07-30 |
| `preflight_backlog_ids` | PASS | every kill-candidates assertion names an open row |
| `review_artifact_coverage` | WARN | 128 code-impact merge(s) since 2026-08-05 carry no linked review artifact: aeea0e0a fix/preflight-question-row-2026-09-08, 988944e8 fix/preflight-shipgate-row-2026-09-08, 837e49fc worktree-c2-living-docs-hygiene, dec60004 worktree-c4-handoff-preflight-rows, a415d720 chore/arm-prompts-guard-pretooluse (+123 more) -- advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `review_artifact_coverage` | WARN | 2 linked artifact(s) carry no parseable **Tally:** line: 584fb1ed -> 2026-08-27-codex-lane-na-gates.md, 5af0b33c -> 2026-08-06-codex-lane-c-504-failclosed.md -- persistence is not machine-auditability; advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `landing_predicate` | PASS | F2 (names, paths and identifiers derive from validators and enums) landed uniformly: scripts/validate_branch_naming.py=True; scripts/batch_manifest.py=True |
| `landing_predicate` | PASS | N-1 (the `markdown_it` fence-region ADOPT (2026-08-03)) landed uniformly: scripts/toc/generator.py=True; scripts/normalize_headers.py=True; scripts/audit.py=True; scripts/validate_doc_structure.py=True |
| `landing_predicate` | PASS | N-2 (the `yaml.safe_load` frontmatter-reader ADOPT (2026-08-03)) landed uniformly: scripts/gen_intake_index.py=True; scripts/gen_claude_rosters.py=True |
| `landing_predicate` | PASS | N-3 (Ch8's dispatch surface is a PATH command, not a dot-sourced alias — [#513]'s own first test case) landed uniformly: protocols/PLAYBOOK.md=True |
| `landing_predicate` | PASS | R-2 (Routing and the reviewer pin are L0 surfaces, outside repo-universalization scope) landed uniformly: ARCHITECTURE.md=True; CLAUDE.md=True |
| `adr_status_grammar` | WARN | 91 ADR status field(s); 0 enum/single-field defects; baseline WARNs: alternatives-considered-legacy=32, coherence=3, duplicate-id=2, flip-condition-legacy=89, grammar=47, wrapped-value=1 |
| `funnel_coverage` | WARN | 2026-09-06-technical-closure-proposals.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-06-technical-erratum-aj-second-pass.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-codex-adr-required-sections.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-deploy.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-audits-appendix.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-audits.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-decisions.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-handoffs.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-intake-appendix.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-docs-intake.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-ecosystem.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-fleet-crosscheck.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-logs.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-protocols.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-root.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-scripts-tests-appendix.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-scripts-tests.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-tasks-appendix.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-tasks.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-templates-claude.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-census-token-bottlenecks.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-07-technical-seal-report-fleet.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `substrate_declaration` | PASS | 73 lane contract(s) landed on/after 2026-08-27 agree with their declared substrate (5 earlier contract(s) grandfathered as records of an already-executed dispatch; 4 finding(s) from later-armed legs [substrate-lane-write-scope-disjoint, substrate-teardown-enum-coverage] grandfathered as debt — those legs are fully armed at FREEZE) |
| `routing_agreement` | PASS | 4 role(s) in ecosystem/routing-table.yaml corroborated by ~/.claude/ROUTING.md |
| `dispatch_drift` | PASS | tier host: 14 literal command(s) in protocols/PLAYBOOK.md Ch8's dispatch table resolve, and .claude/commands/lane-boot.md names the ruled verb 'dispatch' |
| `consumer_at_landing` | WARN | 2026-09-07-codex-adr-required-sections.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | 2026-09-07-technical-seal-report-fleet.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | ARM3_NOTE.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-r-000-bundle-gitlog.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-r-000-docrot-arm2.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-r-000-zc-candidates.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-aj-research.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-batch-p-audit-speed.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-browser-floor.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-nc1-clear.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-playbook.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-readme.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-reds-spine.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-shape-seal.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-trace-scorecard.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-v2-logs.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-v4-archive-report.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-000-v5-closures.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-t-628-v1-release.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-adr-carrier-split.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-adr-template-flip-condition.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-batch-p-local.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-batch-protocol-mechanisms.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-branch-enum-parity.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-carrier-floor-v150-mechanisms.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-closures-local.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-deploy-tool-consumer-override.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-derived-copies-registry.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-dispatch-receipt-is-work.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-erratum-aj-second-pass.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-handoff-v71-build.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-intake-id-next-free.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-plugin-version-record-and-drift.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-prompts-dir-guard.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-seal-report-fleet.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-shape-spec-finalize.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-000-trace-scorecard-consumer.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | LANE-u-628-release-commit.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | SEED_RUBRIC.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `consumer_at_landing` | WARN | VERDICT_RULE.md is cited by no governance surface and is not in the arm-time baseline — the unconsumed set grew. Name it from the row, ADR, register entry or intake that consumes it, or record why it has no consumer |
| `proof_layer` | WARN | test_review_artifact_coverage.py gates 1 test(s) behind a function-level skipif on 'git' — a proof that can be skipped on the machine that breaks the property is not a mechanism. Move the property that cannot be skipped OUT from behind the guard, or propagate the skip predicate into a reporting surface so a skipped proof renders as not-proven (sweep sections 9.2 and 9.6) |
| `proof_layer` | WARN | test_review_artifact_coverage.py gates 1 test(s) behind a function-level skipif on 'git' — a proof that can be skipped on the machine that breaks the property is not a mechanism. Move the property that cannot be skipped OUT from behind the guard, or propagate the skip predicate into a reporting surface so a skipped proof renders as not-proven (sweep sections 9.2 and 9.6) |
| `proof_layer` | WARN | test_review_artifact_coverage.py gates 1 test(s) behind a function-level skipif on 'git' — a proof that can be skipped on the machine that breaks the property is not a mechanism. Move the property that cannot be skipped OUT from behind the guard, or propagate the skip predicate into a reporting surface so a skipped proof renders as not-proven (sweep sections 9.2 and 9.6) |
| `proof_layer` | WARN | test_review_artifact_coverage.py gates 1 test(s) behind a function-level skipif on 'git' — a proof that can be skipped on the machine that breaks the property is not a mechanism. Move the property that cannot be skipped OUT from behind the guard, or propagate the skip predicate into a reporting surface so a skipped proof renders as not-proven (sweep sections 9.2 and 9.6) |
| `funnel_lifecycle` | PASS | 78 live + 12 archived intake(s), 91 live ADR(s), 371 row(s): no terminal object left in a live home, every ACCEPTED doc still owns an open row, and all 35 row(s) landed on/after 2026-08-27 carry resolving provenance |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (33406 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-08-08 is 32d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-27 is 44d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-24 is 47d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/ESSENTIALS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
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

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-07-12 is 59d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-13 is 58d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-18 is 53d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/ESSENTIALS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
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

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | ARCHITECTURE.md: last_reviewed 2026-06-02 is 99d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 99d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 99d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/ESSENTIALS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
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

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 7 warn: ARCHITECTURE.md: last_reviewed 2026-06-02 is 99d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 99d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/ESSENTIALS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
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

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## win-tooling — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\win-tooling`  
**Last audit:** 2026-09-09

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (10449 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | CONTRIBUTING.md: last_reviewed 2026-07-11 is 60d old (> 30d cadence); docs/handoffs/README.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/ESSENTIALS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/SESSION_SETUP.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/AI_COUNCIL_PROCESS.md: absent (registered but presence-optional here) - reported, not skipped silently; protocols/DEFINITION_OF_DONE.md: absent (registered but presence-optional here) - reported, not skipped silently |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 2 - INSTALL.md (no stamp; last content 2026-08-29); README.md (no stamp; last content 2026-09-01) (+14 unstamped outside the gated set's directories, out of scope for this report) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 3 of 20 living docs (4 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (0286cd82d, unrefined)  0d  ungated-and-fresh |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — docs/audits/README.md |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | WARN | 4 of 4 linked worktree(s) look unclosed (horizon 7d): fix/cloud-models-fail-fast [last commit 13d ago]; feat/cloud-models [last commit 13d ago]; fix/sanitise-external-text [last commit 13d ago]; fix/check-advisory-unowned-path [last commit 13d ago] - close them out per the /lane-integrate checklist, or say why they stay |
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

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 6 repo(s) audited
- 139/468 checks passed
- **8 failure(s)** — route findings to repo owners
- 140 warning(s)
- 181 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
