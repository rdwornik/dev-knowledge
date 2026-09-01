# Ecosystem Audit Report

<!-- scope: meta -->

**Date:** 2026-09-01  
**Generated:** 2026-09-01T09:08:59  
**Repos audited:** 6  
**Checks:** 475 total — 137 pass, 10 fail, 154 warn, 0 unavailable, 174 n/a

---

## .dev-knowledge — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`  
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (24067 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .dev-knowledge.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | PASS | 12 stamped v4 bundle(s) valid (structure + sections + budgets) |
| `canonical_freshness` | PASS | 9 canonical living files fresh (last_reviewed not before last edit; within 30d) |
| `canonical_freshness` | WARN | derived gated-and-stale: 3 - ARCHITECTURE.md (declared 2026-08-29 [frontmatter] at c20d92399; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare); protocols/ESSENTIALS.md (declared 2026-08-23 [frontmatter] at 96a48bf59; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare); protocols/SESSION_SETUP.md (declared 2026-08-28 [frontmatter] at 49dec3c56; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-stale: 3 - protocols/ENVIRONMENT.md (declared 2026-07-06 [prose] -> derived 2026-08-31, +56d); protocols/PLAYBOOK.md (declared 2026-08-01 [prose] -> derived 2026-09-01, +31d); protocols/OPERATOR-INTERFACE.md (declared 2026-08-26 [prose] -> derived 2026-08-28, +2d) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 26 - .claude/agents/artifact-reader.md (no stamp; last content 2026-07-06); .claude/commands/changelog-review.md (no stamp; last content 2026-08-28); .claude/commands/handoff-verify.md (no stamp; last content 2026-08-25); .claude/commands/handoff.md (no stamp; last content 2026-08-28); .claude/commands/lane-boot.md (no stamp; last content 2026-08-25); .claude/commands/lane-integrate.md (no stamp; last content 2026-08-26); .claude/commands/override.md (no stamp; last content 2026-08-06); .claude/commands/preflight.md (no stamp; last content 2026-08-04); .claude/commands/save.md (no stamp; last content 2026-05-16); .claude/methodology-roster.md (no stamp; last content 2026-09-01); .claude/rules/git-discipline.md (no stamp; last content 2026-08-28); .claude/skills/check-against-spec/SKILL.md (no stamp; last content 2026-06-25); .claude/skills/verify/SKILL.md (no stamp; last content 2026-08-28); AGENTS.md (no stamp; last content 2026-08-29); deploy/global-instructions-codex.md (no stamp; last content 2026-08-29); deploy/release-v1.3.x-contract.md (no stamp; last content 2026-08-08); plugins/tier1-lifecycle/INSTALL.md (no stamp; last content 2026-07-29); plugins/tier1-lifecycle/commands/review-closures.md (no stamp; last content 2026-07-29); plugins/tier1-lifecycle/commands/ship.md (no stamp; last content 2026-07-05); protocols/AGENT_FRAMEWORK.md (no stamp; last content 2026-08-23); protocols/FUNNEL_LIFECYCLE.md (no stamp; last content 2026-08-29); protocols/HANDOFF_BOOT.md (no stamp; last content 2026-08-28); protocols/HANDOFF_PROCESS.md (no stamp; last content 2026-08-29); protocols/README.md (no stamp; last content 2026-08-29); protocols/REPO_ONBOARDING.md (no stamp; last content 2026-08-23); protocols/STANDING_RULINGS.md (no stamp; last content 2026-08-29) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 6 of 39 living docs (7 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): protocols/PLAYBOOK.md  version handoff-process@6.3.0  declared 2026-08-01 (prose)  derived 2026-09-01 (5c7e9e370)  +31d  ungated-and-stale; ARCHITECTURE.md  version handoff-process@6.3.0  declared 2026-08-29 (frontmatter)  derived 2026-08-29 (e08cdf8ea, unrefined)  0d  1 unreviewed after stamp c20d92399  gated-and-stale; CLAUDE.md  version 2.70  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (c0fae6c1e, unrefined)  0d  gated-and-fresh; CONTRIBUTING.md  version handoff-process@6.3.0  declared 2026-08-28 (frontmatter)  derived 2026-08-28 (e4eaee05f, unrefined)  0d  gated-and-fresh; README.md  version 1.0  declared 2026-09-01 (frontmatter)  derived 2026-09-01 (96f956528, unrefined)  0d  ungated-and-fresh; VISION.md  version 1.1  declared 2026-08-29 (frontmatter)  derived 2026-08-29 (c20d92399, unrefined)  0d  gated-and-fresh; docs/handoffs/README.md  version handoff-process@6.3.0  declared 2026-08-28 (frontmatter)  derived 2026-08-28 (e4eaee05f, unrefined)  0d  gated-and-fresh; protocols/AI_COUNCIL_PROCESS.md  version 2.2  declared 2026-08-29 (frontmatter)  derived 2026-08-29 (99bf123ee, unrefined)  0d  gated-and-fresh; protocols/SESSION_SETUP.md  version handoff-process@6.3.0  declared 2026-08-28 (frontmatter)  derived 2026-08-28 (6adac1dc7, unrefined)  0d  1 unreviewed after stamp 49dec3c56  gated-and-stale; protocols/HANDOFF_BOOT.md  version handoff-process@6.3.0  declared - (none)  derived 2026-08-28 (e4eaee05f, unrefined)  -d  ungated-and-unstamped; protocols/HANDOFF_PROCESS.md  version 6.3.0  declared - (none)  derived 2026-08-29 (7156d4329, unrefined)  -d  ungated-and-unstamped; protocols/README.md  version handoff-process@6.3.0  declared - (none)  derived 2026-08-29 (214f11f45, unrefined)  -d  ungated-and-unstamped |
| `generated_artifact_freshness` | WARN | conformance-dashboard: 8d stale (baseline 4d) — ecosystem/conformance.md committed 2026-08-24, newest input tasks committed 2026-09-01; regenerate + commit: python scripts/gen_dashboard.py --write |
| `generated_artifact_freshness` | PASS | audits-index: 0d stale (baseline 0d) — docs/audits/README.md committed 2026-09-01, newest input docs/audits committed 2026-09-01 |
| `no_sibling_orphans` | PASS | No orphaned '.dev-knowledge-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | no linked worktrees registered (primary only) - nothing to close out |
| `stale_worktrees` | PASS | git stash list is empty - no stashed work outliving its lane |
| `canonical_structure` | PASS | All present canonical files carry their required [U] spine headings |
| `handoff_version_stamp` | PASS | All stamp occurrences in ['ARCHITECTURE.md', 'CONTRIBUTING.md'] match canonical HANDOFF_PROCESS v6.3.0 |
| `amendment_coherence` | PASS | 2 coupled-surface version mention(s) coherent across 1 set(s) |
| `floor_integrity` | N/A | [n/a-reason:NOT-APPLICABLE] no .claude/CLAUDE-FLOOR.md — repo has not adopted the methodology floor (skip) |
| `hooks_armed` | PASS | pre-commit / commit-msg / pre-push installed and pre-commit-managed; merge.ours.driver armed for the declared merge=ours pin |
| `git_backlog_drift` | WARN | closed-but-present (ADR-65 done-items-leave): #614 (closes in f2e1dc95f) still in BACKLOG |
| `doc_claims` | WARN | 2 prose claim(s) drifted from repo state: precommit_hook_count@ecosystem/doc-counts.md (doc 21 != actual 22); pytest_collected@ecosystem/doc-counts.md (doc 4645 != actual 4733) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 533109f20 (2026-06-26) docs(journal): record 2026-06-26 freshness re-stamp session (3bd2cd1) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): 3a894eeb5 (2026-06-19) docs(journal): 2026-06-19 session-wrap — anchor d0f9ead (transcript archive) |
| `no_ff_merges` | WARN | non-merge commit on main (FF/direct — expected a --no-ff merge): d0f9ead67 (2026-06-19) chore(transcripts): archive 2 deep-research reports (dependency-detection + doc<->code traceability) |
| `handoff_probes` | WARN | P0a skipped in 2026-08-31-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0b skipped in 2026-08-31-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P0c skipped in 2026-08-31-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P1a skipped in 2026-08-31-dev-knowledge-architect: tool absent: grep |
| `handoff_probes` | WARN | P1b skipped in 2026-08-31-dev-knowledge-architect: tool absent: sed |
| `handoff_probes` | WARN | P8 skipped in 2026-08-31-dev-knowledge-architect: tool absent: ls |
| `supplement_folded` | PASS | every filled SUPPLEMENT reached its paste — pre-era, immutable-and-lost (recorded, not repaired): 2026-08-23-dev-knowledge-architect |
| `dispatch_verb_agreement` | PASS | both point-of-use sites name the verb Ch8's dispatch table rules, and neither carries a rival literal launch form |
| `reconciled_versions` | PASS | 8 reconciled_with edge(s) match live spec version(s) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#611 (1407 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#547 (2099 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#599 (1825 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#600 (1637 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#602 (1796 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#603 (1802 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#619 (2653 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#112 (1330 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#153 (1594 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#533 (2088 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#534 (1640 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#552 (3576 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#601 (1605 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#615 (1392 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#624 (2172 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#234 (1445 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#277 (1340 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#241 (1625 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#267 (3 history dates spanning 53d, 2188 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#267 (2188 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#289 (1538 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#297 (3 history dates spanning 51d, 1327 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#297 (1327 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#303 (1558 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#324 (1407 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#605 (1936 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#546 (2227 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#548 (1338 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#549 (1491 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#564 (1826 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#285 (1740 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#571 (1602 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#269 (2015 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#614 (3778 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#607 (2019 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#82 (3 history dates spanning 51d, 2110 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#82 (2110 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#327 (1566 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#332 (1545 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#609 (2227 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#559 (3104 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#604 (1876 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#606 (2402 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#244 (2946 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#245 (1569 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-accretion BACKLOG#276 (3 history dates spanning 52d, 1599 chars (>= 3 dates & >= 30d span & > 700 chars)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#276 (1599 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#43 (1703 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#274 (1708 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#278 (1728 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#317 (1499 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#568 (1671 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#608 (2005 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#618 (2379 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#623 (1555 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#625 (2549 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#491 (2049 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#578 (2711 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#570 (1439 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#561 (2294 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#567 (1746 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#271 (2935 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#610 (4961 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#426 (1370 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: backlog-row-length BACKLOG#555 (1364 chars (declared ceiling 1320)) |
| `doc_rot` | WARN | history-accretion bloat: grooming-cadence BACKLOG#grooming-cadence (last groom 2026-07-30, 33d ago (> 21d cadence, ADR-41)) |
| `doc_structure` | PASS | no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme) |
| `doc_code_edge` | PASS | 16 doc->code edge(s) resolved; none broken/ambiguous/orphaned |
| `safe_removal` | PASS | no scripts/*.py module removal in the diff |
| `residual_completeness` | PASS | no unfilled FILL-IN region in changed handoff bundle files |
| `deployed_methodology_version` | N/A | [n/a-reason:NOT-APPLICABLE] .dev-knowledge: unset -- no methodology release deployed yet (deploy-runbook will populate; ADR-91) |
| `enforcement_coverage` | N/A | [n/a-reason:NOT-APPLICABLE] hub - source of the 5 enforcement organs; per-consumer coverage is measured by scripts/enforcement_coverage.py (read-only reporter) |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): BACKLOG.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): README.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): README.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-30-tech-browser-architect-orientation.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-05-func-simplification-distribution-wave.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-06-tech-adoption-consolidation-intake.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-22-tech-document-dependency-graph-organ.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-28-tech-handoff-engine-deployable-carrier.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/AI_COUNCIL_PROCESS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/ESSENTIALS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_BOOT.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/HANDOFF_PROCESS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/OPERATOR-INTERFACE.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/PLAYBOOK.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> handoff-process (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): protocols/STANDING_RULINGS.md -> prompt-template (tier 1) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md -> prompt-template (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-26-tech-handoff-operator-interface.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): docs/intake/README.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `undeclared_edges` | WARN | undeclared prose edge (ADR-88 FC2): ecosystem/conformance.md -> handoff-process (tier 2) — declare `reconciled_with` or disposition |
| `doc_code_coverage_drift` | PASS | all 54 ALL_CHECKS members covered (coverage_scope-annotated or exempt); none escape coverage_scope |
| `import_edges` | PASS | 4 @import edge(s) resolve across 5 file(s) |
| `fleet_parity` | PASS | fleet at parity -- AT-PARITY 193, PASS-declared 18, advisory-rewarn 3, gate-ahead-declared 1, skipped-pre-deploy 6, stale-declaration 1 (blocking verdicts: 0) |
| `routine_consumers` | PASS | 2 declared routine row(s) name a consumer and a consumption_path (live hooks/schedules out of scope — [#426]) |
| `silent_rule_ratchet` | PASS | live 440 <= baseline 443 under detector silent-rule-v5 (60 file(s) in scope); 3 below baseline — ratchet-down available |
| `task_tree_coherence` | PASS | BACKLOG.md coherent with the tasks/ source of truth (structure + frontmatter honesty + full reassembly) |
| `intake_tree_coherence` | PASS | intake residue carrier coherent (338 node(s), 23092 README.md byte(s)) |
| `boot_byte_budget` | PASS | protocols/HANDOFF_BOOT.md is 17196 bytes, within its 18000-byte budget |
| `fleet_audit_replication` | PASS | automation/fleet-audit is replicated to origin (0 commits ahead) |
| `membership_agreement` | PASS | 9 declared (ADR-104); 7 resolved members (deployed-versions); coverage registry-md 9/9, index-yaml 6/9, deployed-versions 7/9, parity-surfaces 9/9, onboarding-rulings 6/9, state-dirs 6/9; declared-but-not-deployed: demo-prep [registry-md, parity-surfaces, onboarding-rulings]; life-architect [registry-md, parity-surfaces, onboarding-rulings] |
| `membership_agreement` | PASS | declaration source: ADR-104 anchor 'adr104-fleet-members', 9 ids, agrees with audit.ADR104_FLEET_DECLARATION |
| `journal_spine_anchor` | PASS | every first-parent spine entry above the ADR-85 disposition floor 24882f8cc is JOURNAL-anchored, EXCEPT 2 lane merge(s) exempt under the ADR-110 declared-integration-arc rule while batch E is open (docs/audits/2026-08-31-technical-batch-e-manifest.md) -- the exemption expires when docs/audits/2026-09-01-technical-batch-e-close-packet.md lands |
| `journal_spine_anchor` | WARN | anchored by mention, not by record: e96638d appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 81a7547 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 666f2dc appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: 86bed82 appears outside an explicit 'Anchors:' record line; anchored by mention, not by record: cc0115d appears outside an explicit 'Anchors:' record line (+712 more) |
| `journal_day_letters` | PASS | JOURNAL day-letter suffixes are unique per day since 2026-07-30 |
| `preflight_backlog_ids` | PASS | every kill-candidates assertion names an open row |
| `review_artifact_coverage` | WARN | 75 code-impact merge(s) since 2026-08-05 carry no linked review artifact: db2c18db docs/dm4-harvest, 4e6e0e2e feat/consumed-artifact-locator-predicate, 5069ce5f feat/title-less-audit-gate, ba73b613 docs/filing-pass, 5fcb5195 docs/held-doctrine-landed (+70 more) -- advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `review_artifact_coverage` | WARN | 2 linked artifact(s) carry no parseable **Tally:** line: 584fb1ed -> 2026-08-27-codex-lane-na-gates.md, 5af0b33c -> 2026-08-06-codex-lane-c-504-failclosed.md -- persistence is not machine-auditability; advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives over two consecutive windows |
| `landing_predicate` | PASS | F2 (names, paths and identifiers derive from validators and enums) landed uniformly: scripts/validate_branch_naming.py=True; scripts/batch_manifest.py=True |
| `landing_predicate` | PASS | N-1 (the `markdown_it` fence-region ADOPT (2026-08-03)) landed uniformly: scripts/toc/generator.py=True; scripts/normalize_headers.py=True; scripts/audit.py=True; scripts/validate_doc_structure.py=True |
| `landing_predicate` | PASS | N-2 (the `yaml.safe_load` frontmatter-reader ADOPT (2026-08-03)) landed uniformly: scripts/gen_intake_index.py=True; scripts/gen_claude_rosters.py=True |
| `landing_predicate` | PASS | N-3 (Ch8's dispatch surface is a PATH command, not a dot-sourced alias — [#513]'s own first test case) landed uniformly: protocols/PLAYBOOK.md=True |
| `landing_predicate` | PASS | R-2 (Routing and the reviewer pin are L0 surfaces, outside repo-universalization scope) landed uniformly: ARCHITECTURE.md=True; CLAUDE.md=True |
| `adr_status_grammar` | WARN | 89 ADR status field(s); 0 enum/single-field defects; baseline WARNs: coherence=3, duplicate-id=2, grammar=47, wrapped-value=1 |
| `funnel_coverage` | WARN | 2026-09-01-technical-tierb-b1-otel-genai-event-schema.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `funnel_coverage` | WARN | 2026-09-01-technical-tierb-b2-sda1-harbor-translation.md carries no disposition and is not in the arm-time baseline -- record one of ACTIONED/FILED/REJECTED/SUPERSEDED with an evidence locator in a ledger row (architect ruling 2026-08-17), or PENDING with the exact question it needs |
| `substrate_declaration` | PASS | 30 lane contract(s) landed on/after 2026-08-27 agree with their declared substrate (5 earlier contract(s) grandfathered as records of an already-executed dispatch; 11 finding(s) from later-armed legs [substrate-lane-write-scope-disjoint, substrate-teardown-enum-coverage] grandfathered as debt — those legs are fully armed at FREEZE) |
| `routing_agreement` | FAIL | the L0 derived copy diverges from ecosystem/routing-table.yaml: adversarial (table: sol) — the L0 copy mentions the role but not sol beside it; fan_out (table: luna, haiku, gemini) — the L0 copy does not mention this role at all; producer (table: claude-code) — the L0 copy does not mention this role at all; reviewer (table: codex) — the L0 copy mentions the role but not codex beside it |
| `dispatch_drift` | PASS | tier host: 12 literal command(s) in protocols/PLAYBOOK.md Ch8's dispatch table resolve, and .claude/commands/lane-boot.md names the ruled verb 'dispatch' |
| `consumer_at_landing` | PASS | 903 artifact(s): every landing on/after 2026-08-27 declares a consumer, and the unconsumed set (621) has not grown past the committed baseline (750 earlier artifact(s) grandfathered; governance pool 563 files) |
| `proof_layer` | PASS | 243 environment-conditional guard(s) across 31 test module(s), all at the committed baseline; 10 gated on an enforcement runner (the sharpest form). A guard here is a question, not a verdict — see scripts/proof_layer.py |
| `funnel_lifecycle` | WARN | ready-past-threshold: docs/intake/2026-07-16-satellite-onboarding-prompts.md -- READY for 47 days (document age), past the ruled 30-day threshold at protocols/FUNNEL_LIFECYCLE.md:316, and carries no review-date: |

History: [`ecosystem\.dev-knowledge\history/`](ecosystem\.dev-knowledge\history/)

---

## ai-council — FAIL

**Path:** `C:\Users\1028120\Documents\Dev\ai-council`  
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (33406 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .ai-council.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-07-23 is 40d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-27 is 36d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-24 is 39d old (> 30d cadence) |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 10 - .claude/CLAUDE-FLOOR.md (no stamp; last content 2026-07-01); .claude/commands/override.md (no stamp; last content 2026-07-03); .claude/rules/code-standards.md (no stamp; last content 2026-08-12); .claude/rules/python-env.md (no stamp; last content 2026-03-20); .claude/rules/testing.md (no stamp; last content 2026-05-19); INSTALL.md (no stamp; last content 2026-07-21); protocols/COUNCIL_INVOCATION_CONTRACT.md (no stamp; last content 2026-07-18); protocols/COUNCIL_QUESTION_GUIDE.md (no stamp; last content 2026-07-23); protocols/README.md (no stamp; last content 2026-07-11); protocols/SYNTHESIS_QUALITY_RUBRIC.md (no stamp; last content 2026-07-02) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 4 of 14 living docs (4 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): CONTRIBUTING.md  version handoff-process@5.7  declared 2026-07-24 (frontmatter)  derived 2026-07-24 (66bb5b1f5, unrefined)  0d  gated-and-fresh; VISION.md  version 1.0  declared 2026-07-23 (frontmatter)  derived 2026-07-23 (f9d69857d, unrefined)  0d  gated-and-fresh |
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
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (22708 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-monorepo.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-07-12 is 51d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-07-13 is 50d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-07-18 is 45d old (> 30d cadence) |
| `canonical_freshness` | WARN | derived gated-and-stale: 1 - CLAUDE.md (declared 2026-07-13 [frontmatter] at fa8a4e342; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-stale: 1 - .claude/skills/gotchas/gotchas.md (declared 2026-06-06 [prose] at d0989ee3b; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 23 - .claude/CLAUDE-FLOOR.md (no stamp; last content 2026-07-07); .claude/commands/override.md (no stamp; last content 2026-07-07); .claude/skills/gotchas/SKILL.md (no stamp; last content 2026-03-30); INSTALL.md (no stamp; last content 2026-07-11); config/extractor/prompts/product_architecture.md (no stamp; last content 2026-03-29); eval/README.md (no stamp; last content 2026-07-10); eval/ontology_benchmark.md (no stamp; last content 2026-03-28); models/README.md (no stamp; last content 2026-08-08); protocols/CORP_INTERFACE.md (no stamp; last content 2026-07-12); protocols/README.md (no stamp; last content 2026-07-12); src/corp/actions/README.md (no stamp; last content 2026-07-17); src/corp/cleanup/README.md (no stamp; last content 2026-03-30); src/corp/cli/README.md (no stamp; last content 2026-04-15); src/corp/extraction/README.md (no stamp; last content 2026-04-15); src/corp/extractor/README.md (no stamp; last content 2026-03-30); src/corp/ingest/README.md (no stamp; last content 2026-03-30); src/corp/opportunity/README.md (no stamp; last content 2026-04-15); src/corp/ops/README.md (no stamp; last content 2026-03-30); src/corp/overnight/README.md (no stamp; last content 2026-03-30); src/corp/project/README.md (no stamp; last content 2026-04-15); src/corp/retrieve/README.md (no stamp; last content 2026-03-30); src/corp/rfp/README.md (no stamp; last content 2026-03-30); src/corp/schema/README.md (no stamp; last content 2026-04-15) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 3 of 28 living docs (3 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): CONTRIBUTING.md  version handoff-process@v5  declared 2026-07-18 (frontmatter)  derived 2026-07-18 (5b9c6c388, unrefined)  0d  gated-and-fresh; VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (539333b4c, unrefined)  0d  gated-and-fresh; CLAUDE.md  version 2.8  declared 2026-07-13 (frontmatter)  derived 2026-07-12 (20daab97d, unrefined)  -1d  1 unreviewed after stamp fa8a4e342  gated-and-stale |
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
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6818 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-ops.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | WARN | VISION.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); CLAUDE.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence) |
| `canonical_freshness` | WARN | derived gated-and-stale: 2 - ARCHITECTURE.md (declared 2026-06-02 [frontmatter] at 82b0343b2; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare); CLAUDE.md (declared 2026-06-02 [frontmatter] at 29ed7b7bd; 2 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 4 - .claude/rules/code-standards.md (no stamp; last content 2026-06-02); .claude/rules/python-env.md (no stamp; last content 2026-03-20); .claude/rules/testing.md (no stamp; last content 2026-03-20); INSTALL.md (no stamp; last content 2026-06-02) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 2 of 8 living docs (2 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (5515b300c, unrefined)  0d  gated-and-fresh |
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
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (6920 chars) |
| `dot_prefix_discipline` | PASS | All root config files dot-prefixed or on ADR-59 exception list |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | PASS | .corp-sca-time-automation.code-workspace present, dot-prefixed, required sort settings correct |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 1 stale (edited since review): CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08 - edited but not re-reviewed | also 3 warn: VISION.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); ARCHITECTURE.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence); CONTRIBUTING.md: last_reviewed 2026-06-02 is 91d old (> 30d cadence) |
| `canonical_freshness` | WARN | derived gated-and-stale: 2 - CLAUDE.md (declared 2026-06-02 [frontmatter] -> derived 2026-06-08, +6d); ARCHITECTURE.md (declared 2026-06-02 [frontmatter] at 112dc6acd; 1 CONTENT commit(s) landed AFTER it on the same date - invisible to the date compare) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 4 - .claude/CLAUDE-FLOOR.md (no stamp; last content 2026-06-08); .claude/rules/code-standards.md (no stamp; last content 2026-03-20); .claude/rules/python-env.md (no stamp; last content 2026-06-02); .claude/rules/testing.md (no stamp; last content 2026-06-02) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 2 of 8 living docs (2 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-06-02 (frontmatter)  derived 2026-06-02 (bf9cb88c7, unrefined)  0d  gated-and-fresh |
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
**Last audit:** 2026-09-01

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: ['last_reviewed', 'owner', 'status', 'version'] |
| `adr38_baseline` | PASS | All ADR-38 universal governance baseline files present |
| `claude_md` | PASS | CLAUDE.md present (9641 chars) |
| `dot_prefix_discipline` | FAIL | Root config files not dot-prefixed (not on ADR-59 exception list): ['config.yaml'] |
| `canonical_md_visibility` | PASS | Mandatory canonical files present + correctly cased: ['ARCHITECTURE.md', 'CLAUDE.md', 'BACKLOG.md', 'CONTRIBUTING.md', 'JOURNAL.md', 'LESSONS.md'] |
| `workspace_settings` | WARN | .win-tooling.code-workspace: explorer.sortOrder='<absent>' (expected 'default'); explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper') |
| `handoff_bundle_structure` | N/A | [n/a-reason:NOT-APPLICABLE] no docs/handoffs/ — nothing to validate |
| `canonical_freshness` | FAIL | 3 stale (edited since review): VISION.md: last_reviewed 2026-07-11 predates last edit 2026-07-12 - edited but not re-reviewed; ARCHITECTURE.md: last_reviewed 2026-07-11 predates last edit 2026-08-19 - edited but not re-reviewed; CLAUDE.md: last_reviewed 2026-07-11 predates last edit 2026-08-29 - edited but not re-reviewed | also 1 warn: CONTRIBUTING.md: last_reviewed 2026-07-11 is 52d old (> 30d cadence) |
| `canonical_freshness` | WARN | derived gated-and-stale: 3 - CLAUDE.md (declared 2026-07-11 [frontmatter] -> derived 2026-08-29, +49d); ARCHITECTURE.md (declared 2026-07-11 [frontmatter] -> derived 2026-08-19, +39d); VISION.md (declared 2026-07-11 [frontmatter] -> derived 2026-07-12, +1d) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | WARN | derived ungated-and-unstamped: 16 - .claude/CLAUDE-FLOOR.md (no stamp; last content 2026-08-29); .claude/commands/override.md (no stamp; last content 2026-08-29); INSTALL.md (no stamp; last content 2026-08-29); README.md (no stamp; last content 2026-09-01); config/dispatch/dispatch-cockpit.md (no stamp; last content 2026-08-13); config/dispatch/fixtures/WINTOOLING-42-fixture-block.md (no stamp; last content 2026-08-08); config/dispatch/fixtures/WINTOOLING-43-fixture-table.md (no stamp; last content 2026-08-08); config/dispatch/fixtures/WINTOOLING-44-fixture-bad-effort.md (no stamp; last content 2026-08-08); config/vscode-agents/vscode-agents-cockpit.md (no stamp; last content 2026-08-06); scripts/flow-launcher/README.md (no stamp; last content 2026-07-12); scripts/flow-launcher/windows-search-indexing.md (no stamp; last content 2026-07-12); scripts/typewhisper/README.md (no stamp; last content 2026-08-04); scripts/typewhisper/upstream-issue-draft-capture-warmup.md (no stamp; last content 2026-08-04); scripts/typewhisper/upstream-issue-idle-burn-351.md (no stamp; last content 2026-08-04); scripts/typewhisper/upstream-issue-latency-329.md (no stamp; last content 2026-08-04); tools/README.md (no stamp; last content 2026-07-11) -- full rows: audit.py doc-freshness |
| `canonical_freshness` | PASS | derived gated-and-fresh: 1 of 20 living docs (1 fresh overall; derived = last CONTENT commit, TOUCH commits [whitespace-only, frontmatter-only, stamp-line-only] walked past) |
| `canonical_freshness` | PASS | derived doctrine rows (live version + date): VISION.md  version 1.0  declared 2026-07-11 (frontmatter)  derived 2026-07-12 (7301041af)  +1d  gated-and-stale |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html |
| `generated_artifact_freshness` | N/A | [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — docs/audits/README.md |
| `no_sibling_orphans` | PASS | No orphaned 'win-tooling-*' siblings (each is a registered worktree or a real repo/folder, not a worktree remnant; or none exist) |
| `stale_worktrees` | PASS | 4 linked worktree(s) registered, each committed within the 7d horizon and present on disk - live batch lanes, not leftovers |
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
| `proof_layer` | WARN | no readable ecosystem/proof-layer-baseline.json — the proof-layer ratchet is INERT (18 environment-conditional guard(s) live); the gate is not measuring growth |
| `funnel_lifecycle` | N/A | [n/a-reason:NOT-APPLICABLE] hub-only -- the intake/ADR lifecycle doctrine is hub-owned |

History: [`ecosystem\win-tooling\history/`](ecosystem\win-tooling\history/)

---

## Summary

- 6 repo(s) audited
- 137/475 checks passed
- **10 failure(s)** — route findings to repo owners
- 154 warning(s)
- 174 n/a (check not applicable to that repo)

*Report generated by `scripts/audit.py`. Do not edit manually.*
