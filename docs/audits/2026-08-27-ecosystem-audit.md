# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-08-27  
**Generated:** 2026-08-27T11:44:20  
**Repos audited:** 6  
**Checks:** 382 total — 115 pass, 6 fail, 115 warn, 0 unavailable, 146 n/a

---

## .dev-knowledge — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (41511 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `canonical_freshness` | PASS | 9 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `generated_artifact_freshness` | PASS | conformance-dashboard: 2d stale (baseline 4d) — ecosystem/conformance.md committed 2026-08-24, newest input BACKLOG.md committed 2026-08-26 |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | 8 linked worktree(s) registered, each committed within the 7d horizon and present on disk - live batch lanes, not leftovers |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v6.2.0 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | pre-commit / commit-msg / pre-push installed and pre-commit-managed |
| `git_backlog_drift` | PASS | no closed-but-present backlog drift (direction (a) STRONG, full history) |
| `doc_claims` | WARN | 1 prose claim(s) drifted from repo state: pytest_collected@ecosystem/doc-counts.md (doc 3977 != actual 3978) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 533109f20 (2026-06-26) docs(journal): record 2026-06-26 freshness re-stamp session (3bd2cd1) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 3a894eeb5 (2026-06-19) docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): d0f9ead67 (2026-06-19) chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability) |
| `handoff_probes` | WARN | P0a skipped in 2026-08-25-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0b skipped in 2026-08-25-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0c skipped in 2026-08-25-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P1a skipped in 2026-08-25-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P1b skipped in 2026-08-25-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P8 skipped in 2026-08-25-dev-knowledge-architect: tool absent: ls |
| `reconciled_versions` | WARN | templates/CONTRIBUTING-md-template.md: malformed (reconciled_with not '<spec-id>@<version>') |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#547 (2099 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#533 (2239 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#534 (1640 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#552 (3576 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#546 (2227 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#549 (1491 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#564 (1826 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#571 (1602 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#420 (1370 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#559 (3073 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#577 (3193 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#568 (1671 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#491 (3727 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#578 (2711 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#570 (1439 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#541 (1758 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#561 (2386 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#567 (1746 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#348 (4 history dates spanning 32d, 1360 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#348 (1360 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#426 (1370 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#555 (1508 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: grooming-cadence BACKLOG#grooming-cadence (last groom 2026-07-30, 28d ago (> 21d cadence, ADR-41)) |
| `doc_structure` | PASS | no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme) |
| `doc_code_edge` | PASS | 16 doc->code edge(s) resolved; none broken/ambiguous/orphaned |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub - source of the 5 enforcement organs; per-consumer coverage is measured by scripts/enforcement_coverage.py (read-only reporter) |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): VISION.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): VISION.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-30-tech-browser-architect-orientation.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-05-func-simplification-distribution-wave.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-06-tech-adoption-consolidation-intake.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-22-tech-document-dependency-graph-organ.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/AI_COUNCIL_PROCESS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/ESSENTIALS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_BOOT.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_PROCESS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/PLAYBOOK.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> prompt-template (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-26-tech-handoff-operator-interface.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/README.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): ecosystem/conformance.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `doc_code_coverage_drift` | PASS | all 46 ALL_CHECKS members covered (coverage_scope-annotated or exempt); none escape coverage_scope |
| `import_edges` | PASS | 3 @import edge(s) resolve across 4 file(s) |
| `fleet_parity` | PASS | fleet at parity -- AT-PARITY 187, PASS-declared 19, advisory-rewarn 3, gate-ahead-declared 1, skipped-pre-deploy 6, stale-declaration 1 (blocking verdicts: 0) |
| `routine_consumers` | PASS | 3 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | PASS | live 442 <= baseline 443 under detector silent-rule-v5 (58 file(s) in scope); 1 below baseline — ratchet-down available |
| `task_tree_coherence` | PASS | BACKLOG.md coherent with the tasks/ source of truth (structure + frontmatter honesty + full reassembly) |
| `intake_tree_coherence` | PASS | intake residue carrier coherent (330 node(s), 21984 README.md byte(s)) |
| `boot_byte_budget` | PASS | protocols/HANDOFF_BOOT.md is 17196 bytes, within its 18000-byte budget |
| `fleet_audit_replication` | WARN | automation/fleet-audit is 1 commit(s) ahead of origin -- a recent push likely failed; ADR-80's durable record is behind |
| `membership_agreement` | PASS | 9 declared (ADR-104); 5 resolved members (deployed-versions); coverage registry-md 9/9, index-yaml 6/9, deployed-versions 5/9, parity-surfaces 9/9, onboarding-rulings 4/9, state-dirs 6/9; declared-but-not-deployed: demo-prep [registry-md, parity-surfaces, onboarding-rulings]; life-architect [registry-md, parity-surfaces, onboarding-rulings]; terminal-setup [registry-md, parity-surfaces]; win-tooling [registry-md, index-yaml, parity-surfaces, state-dirs] |
| `membership_agreement` | PASS | declaration source: ADR-104 anchor 'adr104-fleet-members', 9 ids, agrees with audit.ADR104_FLEET_DECLARATION |
| `journal_spine_anchor` | FAIL | 1 first-parent spine entry(ies) above the disposition floor 24882f8cc carry no JOURNAL anchor: 08b0d192 (2026-08-26) Merge branch 'chore/workspace-provider-roots-2026-08-26' |
| `journal_spine_anchor` | WARN | anchored by mention, not by record: 9646389 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: ac677b6 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: df57f2e appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: dd2f78d appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 9058308 appears outside an explicit 'Anchors:' record line (+643 more) |
| `journal_day_letters` | PASS | JOURNAL day-letter suffixes are unique per day since 2026-07-30 |
| `preflight_backlog_ids` | PASS | every kill-candidates assertion names an open row |
| `review_artifact_coverage` | WARN | 35 code-impact merge(s) since 2026-08-05 carry no linked review artifact: ac677b6e worktree-prompts-revocation, 852e145c docs/endgame-2026-08-26, 1858849a docs/rl-registry-filings-dispatch, d74a9809 worktree-lane-x-failloud, 13d4f05e docs/discharge-38-c1-closures (+30 more) -- advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `review_artifact_coverage` | WARN | 1 linked artifact(s) carry no parseable **Tally:** line: 5af0b33c -> 2026-08-06-codex-lane-c-504-failclosed.md -- persistence is not machine-auditability; advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `landing_predicate` | PASS | F2 (names, paths and identifiers derive from validators and enums) landed uniformly: scripts/validate_branch_naming.py=True; scripts/batch_manifest.py=True |
| `landing_predicate` | PASS | N-1 (the `markdown_it` fence-region ADOPT (2026-08-03)) landed uniformly: scripts/toc/generator.py=True; scripts/normalize_headers.py=True; scripts/audit.py=True; scripts/validate_doc_structure.py=True |
| `landing_predicate` | PASS | N-2 (the `yaml.safe_load` frontmatter-reader ADOPT (2026-08-03)) landed uniformly: scripts/gen_intake_index.py=True; scripts/gen_claude_rosters.py=True |
| `landing_predicate` | PASS | N-3 (Ch8's dispatch surface is a PATH command, not a dot-sourced alias — [#513]'s own first test case) landed uniformly: protocols/PLAYBOOK.md=True |
| `landing_predicate` | PASS | R-2 (Routing and the reviewer pin are L0 surfaces, outside repo-universalization scope) landed uniformly: ARCHITECTURE.md=True; CLAUDE.md=True |
| `adr_status_grammar` | WARN | 88 ADR status field(s); 0 enum/single-field defects; baseline WARNs: coherence=3, duplicate-id=2, grammar=47, wrapped-value=1 |
| `funnel_coverage` | WARN | 2026-08-23-technical-backlog-adjudication-prep.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-funnel-retro-classification.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-lane-dashboard-commit-path.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-lane-dispatch-codification.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-lane-docs-actual-state.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-lane-provider-config.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-lane-status-grammar.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-research-model-bus.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-23-technical-ruling-provenance-audit.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-batch-close.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-discharge-38-ruling-packet.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-lane-v1-register-verification.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-lane-v3-gates-and-ci.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-lane-v4-lifecycle-verification.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-lane-v5-register-verification.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-probe-substrate.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-research-candidate-register.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-research-register-addendum.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-verify-register-v2.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-technical-warn-triage-and-teardown.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-verification-integrator-merged-result.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-24-verification-l6-rulings-landing.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-dispatch-brief-to-architect.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-dispatch-codespace-build.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-dispatch-consolidation-plan.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-dispatch-surface-measured.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-green-by-skip-sweep.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-harvest-v-consolidation.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-lane-g-governance-spine.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-probe-dsh-report.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-probe-providers-report.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-register-ruling-packet.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-research-agents-md-standard.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-research-delivery-telemetry-attribution.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-25-technical-research-operator-dispatch-playbook.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-codex-adr115-acceptance-review.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-birth-row-bodies-579-586.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-hub-diagnostic.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-perf-recon.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-provider-surface-repair-summary.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-research-backlog-management.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-research-chinese-coding-models.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-technical-research-cost-usage-telemetry.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-08-26-verification-batch-1-close-packet.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (33406 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-07-23 is 35d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-27 is 31d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-24 is 34d old (> 30d cadence) |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | FAIL | 3 blocking defect(s): enum ADR-01-synthesizer-selection.md:6 — value 'Revised (2026-07-18)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED); enum ADR-02-default-panel.md:6 — value 'Revised (2026-05-11)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED); enum ADR-06-cost-optimization.md:6 — value 'Revised 2026-05-11 (Qwen trial deferred/abandoned)' starts with no declared enum member (Explored, not adopted, Partially superseded, Superseded, Deprecated, Proposed, Accepted, PARKED) // also detected: grammar=16, unindexed=16 |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |

History: [`ecosystem\ai-council\history/`](ecosystem\ai-council\history/)

---

## corp-monorepo — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-monorepo`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-07-12 is 46d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-13 is 45d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-18 is 40d old (> 30d cadence) |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | FAIL | 14 blocking defect(s): single-field ADR-01-knowledge-architecture.md — no status field found in the header window; single-field ADR-02-extraction-quality.md — no status field found in the header window; single-field ADR-03-model-selection.md — no status field found in the header window; single-field ADR-04-vault-structure.md — no status field found in the header window; single-field ADR-05-reextraction-strategy.md — no status field found in the header window; single-field ADR-06-quality-gate.md — no status field found in the header window; single-field ADR-07-vault-navigation.md — no status field found in the header window; single-field ADR-08a-model-tiering.md — no status field found in the header window (+6 more) // also detected: duplicate-id=1, grammar=14, unindexed=23 |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |

History: [`ecosystem\corp-monorepo\history/`](ecosystem\corp-monorepo\history/)

---

## corp-ops — PASS

**Path:** `C:\Users\1028120\Documents\Dev\corp-ops`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence) |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | WARN | corpus unusable: no ADR-*.md files under C:\Users\1028120\Documents\Dev\corp-ops\docs\decisions |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |

History: [`ecosystem\corp-ops\history/`](ecosystem\corp-ops\history/)

---

## corp-sca-time-automation — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\corp-sca-time-automation`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 3 warn: VISION.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 86d old (> 30d cadence) |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | WARN | corpus unusable: no ADR-*.md files under C:\Users\1028120\Documents\Dev\corp-sca-time-automation\docs\decisions |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |

History: [`ecosystem\corp-sca-time-automation\history/`](ecosystem\corp-sca-time-automation\history/)

---

## win-tooling — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\win-tooling`  
**Last audit:** 2026-08-27

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6859 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['VISION.md', 'ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 2 stale (edited since review): VISION.md: last_reviewed 2026-07-11 predates last edit 2026-07-12 - edited but not re-reviewed; ARCHITECTURE.md: last_reviewed 2026-07-11 predates last edit 2026-08-19 - edited but not re-reviewed | also 2 warn: CLAUDE.md: last_reviewed 2026-07-11 is 47d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-11 is 47d old (> 30d cadence) |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | 5 linked worktree(s) registered, each committed within the 7d horizon and present on disk - live batch lanes, not leftovers |
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
| `journal_day_letters` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- JOURNAL day-letter doctrine is hub-owned |
| `preflight_backlog_ids` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — BACKLOG.md kill-candidates assertions are a hub surface |
| `review_artifact_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the codex-review artifact convention is a hub practice |
| `landing_predicate` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only — landing-predicate scanner skipped (not the hub repo) |
| `adr_status_grammar` | N/A | [n/a-reason:SUBJECT-ABSENT] no docs/decisions/ in this repo — only the hub carries an ADR corpus |
| `funnel_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the audit-disposition ledger is a hub practice |

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 6 repo(s) audited
- 115/382 checks passed
- **6 failure(s)** — route findings to repo owners
- 115 warning(s)
- 146 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
