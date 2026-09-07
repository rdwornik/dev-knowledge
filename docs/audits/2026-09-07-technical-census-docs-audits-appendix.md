# Census appendix — per-file inventory of `docs/audits/` (sweep 2026-09-07, lane S-04)

**Consumers:** this file is the inventory table split out of
`docs/audits/2026-09-07-technical-census-docs-audits.md` under that contract's 40 KB rule, and is
read with it. It carries no verdict of its own: the reasoning, the witnesses and the honest limits
live in the parent census. Governance: `[#552]` (the row owning this folder's disposition backlog),
`[#595]` (the `consumer_at_landing` ratchet), `ADR-100` (retention — keep-all-accepted),
`ADR-101` (naming grammar).

**READ-ONLY.** Nothing was moved, deleted, edited or renamed. Measured at
`21576e3a4fe77373c936247e6560263b7cd3fbd2`, excluding this lane's own two artifacts.

## Column meanings

- **path** — relative to `docs/audits/`. A row showing two paths joined by `+` is a
  `.md`/`.html` sidecar pair, counted as one artifact with their bytes summed.
- **bytes** — `stat` size at the measured commit.
- **class** — the whole-token longest-match against the live
  `validate_hermetization.AUDIT_CLASS_ENUM`. `(grandfathered)` = no enum class in the name;
  `(subdir, ungoverned)` = inside a lane-contract directory, where the naming grammar does not
  reach.
- **witness tier** — `A pool` cited by the governance pool · `B peer` cited only by another audit ·
  `C log` named only in `JOURNAL.md` or a handoff · `D code` named only under `scripts/`, `tests/`
  or `ecosystem/` · `E gen` present only on generated surfaces · `F none` no reference anywhere.
  Definitions and their limits: parent census §0 and Honest limits §4.
- **Rule B** — `ok` conforms to the live ADD-time naming grammar · `GRANDFATHERED` would be refused
  today but predates the rule (`ADR-101` §6, no retroactive rename) · `-` the rule is silent on it
  (non-`.md`, or one directory deeper — parent census finding F-1).
- **verdict** — a PROPOSAL the operator rules. `KEEP` carries the folder-level witness stated once
  in the parent census (`ADR-100` keep-all-accepted; no `docs/audits/archive/` exists);
  `RELOCATE` is the nine `.py` files in a documentation home (parent census finding F-2).

## Inventory

| # | path under `docs/audits/` | bytes | class | witness tier | Rule B | verdict |
|---:|---|---:|---|---|---|---|
| 1 | `2026-03-30-dev-practice-os-state-audit.md` | 7071 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 2 | `2026-04-21-corp-monorepo-operating-model-analysis.md` | 71933 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 3 | `2026-04-21-council-27-brief.md` | 27584 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 4 | `2026-04-21-dev-knowledge-inventory.md` | 10468 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 5 | `2026-04-21-dev-knowledge-scope-tagging.md` | 16260 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 6 | `2026-04-24-council-28-29-consolidated-actions.md` | 7300 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 7 | `2026-04-24-playbook-tagging-sanity-check.md` | 6341 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 8 | `2026-04-24-stream-a-gap-report.md` | 4941 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 9 | `2026-04-24-stream-b-gaps-mapping.md` | 11552 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 10 | `2026-04-25-claude-code-features-inventory.md` | 13813 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 11 | `2026-04-26-codex-adr-30-default-branch-main.md` | 2941 | codex | A pool | ok | KEEP |
| 12 | `2026-04-27-deep-cleansing-diagnostic.md` | 16039 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 13 | `2026-04-27-numbers-audit.md` | 9910 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 14 | `2026-04-27-pre-debate-audit-cross-repo-and-handoff.md` | 9988 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 15 | `2026-04-30-ai-council-audit-report.md` | 11251 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 16 | `2026-04-30-ai-council-discovery.md` | 11799 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 17 | `2026-04-30-ai-council-rediscovery.md` | 8035 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 18 | `2026-04-30-dev-knowledge-self-audit.md` | 18040 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 19 | `2026-05-11-ai-council-scrum-master-review.md` | 13427 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 20 | `2026-05-11-codex-prompt-b-docs-alignment.md` | 2626 | codex | B peer | ok | KEEP |
| 21 | `2026-05-12-codex-ai-council-handoff-stage3.md` | 2507 | codex | B peer | ok | KEEP |
| 22 | `2026-05-12-handoff-process-audit.md` | 28350 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 23 | `2026-05-12-hooks-discovery-resolution.md` | 4264 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 24 | `2026-05-12-hooks-discovery.md` | 11746 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 25 | `2026-05-15-ecosystem-audit.md` | 6298 | ecosystem-audit | B peer | ok | KEEP |
| 26 | `2026-05-16-ecosystem-audit.md` | 1406 | ecosystem-audit | B peer | ok | KEEP |
| 27 | `2026-05-17-corp-monorepo-governance-rollout-plan.md` | 29685 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 28 | `2026-05-17-skills-hooks-usage-review.md` | 7637 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 29 | `2026-05-19-cohort1-verification.md` | 7617 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 30 | `2026-05-19-corp-monorepo-architecture-inspection.md` | 12293 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 31 | `2026-05-19-dev-knowledge-posture-audit.md` | 31970 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 32 | `2026-05-19-rollout-readiness.md` | 14029 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 33 | `2026-05-20-handoff-process.md` | 27537 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 34 | `2026-05-20-posture-audit-verification.md` | 10926 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 35 | `2026-05-22-codex-codemap-generator-tool.md` | 2113 | codex | B peer | ok | KEEP |
| 36 | `2026-05-22-codex-drift-burndown-2026-05-22.md` | 1187 | codex | B peer | ok | KEEP |
| 37 | `2026-05-23-.dev-knowledge-audit.md` | 816 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 38 | `2026-05-23-ai-council-deep-audit.md` | 31967 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 39 | `2026-05-23-codex-codemap-amendment-and-dogfood.md` | 977 | codex | B peer | ok | KEEP |
| 40 | `2026-05-23-codex-codemap-mermaid-fence-wrap.md` | 686 | codex | B peer | ok | KEEP |
| 41 | `2026-05-23-corp-monorepo-deep-audit.md` | 28970 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 42 | `2026-05-23-ecosystem-audit.md` | 1885 | ecosystem-audit | B peer | ok | KEEP |
| 43 | `2026-05-24-backlog-audit-and-universalization-scoping.md` | 18131 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 44 | `2026-05-24-dev-knowledge-self-audit.md` | 16714 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 45 | `2026-05-25-ai-council-universalization-audit-refresh.md` | 19505 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 46 | `2026-05-25-ai-council-universalization-execution-plan.md` | 21362 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 47 | `2026-05-25-council-debate-forensics.md` | 4755 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 48 | `2026-05-25-council-mechanism-discovery.md` | 8654 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 49 | `2026-05-25-council-pipeline-audit.md` | 13305 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 50 | `2026-05-25-council-pipeline-discovery.md` | 20412 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 51 | `2026-05-25-council-pipeline-index.md` | 3447 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 52 | `2026-05-25-council-pipeline-proposal.md` | 9893 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 53 | `2026-05-26-ai-council-audit-status-reference.md` | 5329 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 54 | `2026-05-26-corp-monorepo-audit-refresh.md` | 16802 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 55 | `2026-05-26-corp-monorepo-execution-plan.md` | 18822 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 56 | `2026-05-26-corp-ops-audit-refresh.md` | 11676 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 57 | `2026-05-26-corp-ops-execution-plan.md` | 12954 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 58 | `2026-05-26-corp-sca-time-automation-audit-refresh.md` | 11541 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 59 | `2026-05-26-corp-sca-time-automation-execution-plan.md` | 14815 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 60 | `2026-05-26-cross-repo-audit-discovery.md` | 11916 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 61 | `2026-05-26-cross-repo-universalization-synthesis.md` | 9639 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 62 | `2026-05-26-cross-repo-universalization-verification.md` | 21648 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 63 | `2026-05-26-handoff-stabilization-discovery.md` | 11367 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 64 | `2026-05-26-handoff-stabilization-validation-report.md` | 9986 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 65 | `2026-05-27-ai-council-visual-pattern-retrofit-plan.md` | 3751 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 66 | `2026-05-27-concurrency-anomaly-cleanup-2026-05-26.md` | 3312 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 67 | `2026-05-27-corp-monorepo-visual-pattern-retrofit-plan.md` | 7433 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 68 | `2026-05-27-corp-ops-visual-pattern-retrofit-plan.md` | 3525 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 69 | `2026-05-27-corp-sca-time-automation-visual-pattern-retrofit-plan.md` | 3628 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 70 | `2026-05-27-cross-repo-retrofit-verification.md` | 15731 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 71 | `2026-05-27-taxonomy-simplification-verification.md` | 13639 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 72 | `2026-05-28-final-state-and-process-diagrams-verification.md` | 11365 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 73 | `2026-05-28-mermaid-dark-theme-verification.md` | 3787 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 74 | `2026-05-28-mermaid-readability-v2-verification.md` | 5583 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 75 | `2026-05-28-universalization-durability-audit.md` | 20953 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 76 | `2026-05-29-ecosystem-coherence-audit.md` | 12805 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 77 | `2026-05-29-handoff-v3.4-fix-campaign-verification.md` | 7349 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 78 | `2026-05-29-handoff-v3.4-process-audit.md` | 15236 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 79 | `2026-05-29-harness-engineering-positioning.md` | 21238 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 80 | `2026-05-29-overnight-morning-briefing.md` | 6797 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 81 | `2026-05-31-backlog-architecture-diagnosis.md` | 17464 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 82 | `2026-05-31-backlog-reconciliation-classification.md` | 9097 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 83 | `2026-05-31-methodology-canonical-audit.md` | 25828 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 84 | `2026-06-01-backlog-commit-naming-retro.md` | 2375 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 85 | `2026-06-01-backlog-migration-inventory.md` | 6176 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 86 | `2026-06-01-child-repo-relocation-proposal.md` | 5696 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 87 | `2026-06-01-codex-backlog-migration-adr64.md` | 3140 | codex | B peer | ok | KEEP |
| 88 | `2026-06-01-codex-backlog-story-map.md` | 3214 | codex | B peer | ok | KEEP |
| 89 | `2026-06-01-codex-precommit-enforcement-gate.md` | 858 | codex | B peer | ok | KEEP |
| 90 | `2026-06-01-codex-sacred-files-cadence-check10.md` | 3348 | codex | B peer | ok | KEEP |
| 91 | `2026-06-01-fresh-eyes-backlog-migration.md` | 2846 | fresh-eyes | B peer | ok | KEEP |
| 92 | `2026-06-01-fresh-eyes-precommit-enforcement-gate.md` | 3096 | fresh-eyes | B peer | ok | KEEP |
| 93 | `2026-06-01-fresh-eyes-sacred-files-cadence.md` | 3533 | fresh-eyes | B peer | ok | KEEP |
| 94 | `2026-06-01-fresh-eyes-story-map.md` | 1989 | fresh-eyes | B peer | ok | KEEP |
| 95 | `2026-06-02-codex-canonical-standard-lock.md` | 1135 | codex | B peer | ok | KEEP |
| 96 | `2026-06-02-codex-no-leftovers-detector.md` | 907 | codex | B peer | ok | KEEP |
| 97 | `2026-06-02-codex-pytest-ini-exception.md` | 1689 | codex | B peer | ok | KEEP |
| 98 | `2026-06-02-ecosystem-audit.md` | 8291 | ecosystem-audit | B peer | ok | KEEP |
| 99 | `2026-06-03-codemap-grounding.md` | 10582 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 100 | `2026-06-03-codex-audit-self-documenting.md` | 1289 | codex | B peer | ok | KEEP |
| 101 | `2026-06-03-codex-doctools-hook-repo.md` | 1613 | codex | B peer | ok | KEEP |
| 102 | `2026-06-03-codex-dynamic-toc.md` | 1556 | codex | B peer | ok | KEEP |
| 103 | `2026-06-03-codex-tier1-precommit-stage-fix.md` | 1385 | codex | B peer | ok | KEEP |
| 104 | `2026-06-03-doc-tooling-inventory.md` | 13341 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 105 | `2026-06-03-ecosystem-audit.md` | 8291 | ecosystem-audit | B peer | ok | KEEP |
| 106 | `2026-06-03-phase0-workflow-gates-findings.md` | 10014 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 107 | `2026-06-03-protocols-rot-audit.md` | 13757 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 108 | `2026-06-04-conformance-nightly-digest.md` | 11267 | conformance-nightly-digest | B peer | ok | KEEP |
| 109 | `2026-06-04-conformance-rerun-delta-digest.md` | 5778 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 110 | `2026-06-04-ecosystem-audit.md` | 8396 | ecosystem-audit | B peer | ok | KEEP |
| 111 | `2026-06-04-pilot81-hub-conformance-digest.md` | 10810 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 112 | `2026-06-05-conformance-nightly-digest.md` | 8732 | conformance-nightly-digest | A pool | ok | KEEP |
| 113 | `2026-06-05-ecosystem-audit.md` | 8291 | ecosystem-audit | B peer | ok | KEEP |
| 114 | `2026-06-05-living-doc-staleness.md` | 4510 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 115 | `2026-06-05-machinery-inventory.md` | 16175 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 116 | `2026-06-06-85-validation-record.md` | 4755 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 117 | `2026-06-06-codex-85-fleet-scheduler.md` | 2023 | codex | B peer | ok | KEEP |
| 118 | `2026-06-06-codex-immutability-guard.md` | 3211 | codex | B peer | ok | KEEP |
| 119 | `2026-06-06-conformance-nightly-digest.md` | 9304 | conformance-nightly-digest | A pool | ok | KEEP |
| 120 | `2026-06-06-corp-monorepo-audit.md` | 2099 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 121 | `2026-06-06-ecosystem-audit.md` | 8801 | ecosystem-audit | B peer | ok | KEEP |
| 122 | `2026-06-07-changelog-review.md` | 3693 | changelog-review | B peer | ok | KEEP |
| 123 | `2026-06-07-codex-max-audit.md` | 8415 | codex | B peer | ok | KEEP |
| 124 | `2026-06-07-conformance-nightly-digest.md` | 7955 | conformance-nightly-digest | A pool | ok | KEEP |
| 125 | `2026-06-07-copilot-collections-peer-audit-v2.md` | 26315 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 126 | `2026-06-07-ecosystem-audit.md` | 8900 | ecosystem-audit | B peer | ok | KEEP |
| 127 | `2026-06-07-methodology-transfer-audit.md` | 12227 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 128 | `2026-06-07-platform-max-audit.md` | 13961 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 129 | `2026-06-07-wave-a-validation.md` | 3720 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 130 | `2026-06-08-corp-sca-time-automation-audit.md` | 2354 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 131 | `2026-06-08-ecosystem-audit.md` | 9420 | ecosystem-audit | B peer | ok | KEEP |
| 132 | `2026-06-08-floor-pilot-corp-sca-validation.md` | 5040 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 133 | `2026-06-08-floor-repilot-corp-sca-validation.md` | 4709 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 134 | `2026-06-09-codex-prose-state-checker-89.md` | 2994 | codex | B peer | ok | KEEP |
| 135 | `2026-06-09-conformance-nightly-digest.md` | 9749 | conformance-nightly-digest | B peer | ok | KEEP |
| 136 | `2026-06-09-ecosystem-audit.md` | 9524 | ecosystem-audit | B peer | ok | KEEP |
| 137 | `2026-06-10-codex-147-ship-gate.md` | 2396 | codex | B peer | ok | KEEP |
| 138 | `2026-06-10-codex-amendment-gate-11.md` | 2041 | codex | B peer | ok | KEEP |
| 139 | `2026-06-10-conformance-nightly-digest.md` | 8831 | conformance-nightly-digest | B peer | ok | KEEP |
| 140 | `2026-06-10-consolidation-audit.md` | 8884 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 141 | `2026-06-10-ecosystem-audit.md` | 10471 | ecosystem-audit | B peer | ok | KEEP |
| 142 | `2026-06-10-fleet-handoff-readiness.md` | 8953 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 143 | `2026-06-11-architecture-coherence-audit.md` | 18284 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 144 | `2026-06-11-conformance-nightly-digest.md` | 10986 | conformance-nightly-digest | B peer | ok | KEEP |
| 145 | `2026-06-11-ecosystem-audit.md` | 11016 | ecosystem-audit | B peer | ok | KEEP |
| 146 | `2026-06-11-surface-responsibility-audit.md` | 18966 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 147 | `2026-06-12-conformance-nightly-digest.md` | 12684 | conformance-nightly-digest | B peer | ok | KEEP |
| 148 | `2026-06-12-ecosystem-audit.md` | 11435 | ecosystem-audit | B peer | ok | KEEP |
| 149 | `2026-06-13-codex-156-taskgraph.md` | 1055 | codex | B peer | ok | KEEP |
| 150 | `2026-06-13-codex-163-basename-fallback.md` | 2479 | codex | B peer | ok | KEEP |
| 151 | `2026-06-13-codex-163-probe-validator.md` | 2141 | codex | B peer | ok | KEEP |
| 152 | `2026-06-13-conformance-nightly-digest.md` | 11811 | conformance-nightly-digest | B peer | ok | KEEP |
| 153 | `2026-06-13-ecosystem-audit.md` | 11496 | ecosystem-audit | B peer | ok | KEEP |
| 154 | `2026-06-14-codex-q9-automation-isolation.md` | 2528 | codex | B peer | ok | KEEP |
| 155 | `2026-06-14-conformance-nightly-digest.md` | 9556 | conformance-nightly-digest | B peer | ok | KEEP |
| 156 | `2026-06-14-ecosystem-audit.md` | 12109 | ecosystem-audit | A pool | ok | KEEP |
| 157 | `2026-06-15-changelog-review.md` | 4936 | changelog-review | A pool | ok | KEEP |
| 158 | `2026-06-17-codex-coherence-integration.md` | 2069 | codex | B peer | ok | KEEP |
| 159 | `2026-06-19-consolidation-state-report.md` | 9757 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 160 | `2026-06-19-hook-completeness-audit.md` | 11911 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 161 | `2026-06-19-playbook-essentials-currency-audit.md` | 16911 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 162 | `2026-06-20-pyright-reverse-dep-oracle-findings.md` | 20844 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 163 | `2026-06-20-removal-closure-spike-findings.md` | 15847 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 164 | `2026-06-21-audit-ops-findings.md` | 17467 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 165 | `2026-06-21-audit-process-findings.md` | 17209 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 166 | `2026-06-21-audit-technical-findings.md` | 21167 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 167 | `2026-06-21-doc-code-edge-fit-check.md` | 10382 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 168 | `2026-06-23-architecture-fidelity-audit.md` | 20424 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 169 | `2026-06-23-canonical-corpus-coherence-audit.md` | 29225 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 170 | `2026-06-23-handoff-process-audit-findings.md` | 33215 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 171 | `2026-06-23-playbook-fidelity-audit.md` | 36007 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 172 | `2026-06-25-dependency-architecture-coverage-audit.md` | 32274 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 173 | `2026-06-25-process-trigger-usage-audit.md` | 27821 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 174 | `2026-06-26-corpus-graph-justify-or-retire.md` | 20594 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 175 | `2026-06-26-playbook-condensation-rule-inventory.md` | 9857 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 176 | `2026-07-02-comprehensive-system-audit-for-external-review.md` | 76255 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 177 | `2026-07-04-codex-lived-sandbox-slice-a.md` | 3588 | codex | B peer | ok | KEEP |
| 178 | `2026-07-04-coherence-spine-review.md` | 22702 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 179 | `2026-07-04-fable-architecture-review.md` | 43879 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 180 | `2026-07-04-handoff-adoption-review.md` | 25209 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 181 | `2026-07-04-rot-algorithm-design.md` | 23293 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 182 | `2026-07-05-ai-council-measurement-2.md` | 12237 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 183 | `2026-07-05-audit-vs-reality.md` | 22370 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 184 | `2026-07-05-codex-consumer-arc.md` | 988 | codex | B peer | ok | KEEP |
| 185 | `2026-07-05-codex-slice-b-fix-batch.md` | 2247 | codex | B peer | ok | KEEP |
| 186 | `2026-07-05-draft-tier2-nightly-layer.md` | 4553 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 187 | `2026-07-05-draft-tier3-claudemd-generability.md` | 5365 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 188 | `2026-07-05-overnight-autonomy-run.md` | 16586 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 189 | `2026-07-06-ai-council-measurement-3.md` | 7113 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 190 | `2026-07-06-arc5-buy-vs-build-verdicts.md` | 9834 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 191 | `2026-07-06-arc5-must-verification.md` | 6760 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 192 | `2026-07-06-arc5-routines-pilot-design.md` | 4980 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 193 | `2026-07-06-changelog-review.md` | 9224 | changelog-review | A pool | ok | KEEP |
| 194 | `2026-07-06-codex-consumer-instrument-hardening.md` | 4753 | codex | B peer | ok | KEEP |
| 195 | `2026-07-06-codex-g7-mirror.md` | 2018 | codex | B peer | ok | KEEP |
| 196 | `2026-07-07-ai-council-measurement-4.md` | 4948 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 197 | `2026-07-07-changelog-review.md` | 3524 | changelog-review | A pool | ok | KEEP |
| 198 | `2026-07-07-overnight-mission-ledger.md` | 26232 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 199 | `2026-07-07-stage3-adjudication-memo.md` | 5482 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 200 | `2026-07-08-census-amendment-docs-handoffs-ruling.md` | 2896 | census | A pool | ok | KEEP |
| 201 | `2026-07-08-demo-prep-global-infra-incident.md` | 10297 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 202 | `2026-07-08-fleet-consistency-census.md` | 28757 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 203 | `2026-07-08-grooming-worksheet.md` | 28883 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 204 | `2026-07-08-qa-role-incident-evidence.md` | 3192 | qa | B peer | ok | KEEP |
| 205 | `2026-07-09-changelog-review.md` | 6149 | changelog-review | B peer | ok | KEEP |
| 206 | `2026-07-09-deletion-candidates-report.md` | 8187 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 207 | `2026-07-09-night-hygiene-audit.md` | 18829 | (grandfathered) | A pool | GRANDFATHERED | KEEP |
| 208 | `2026-07-09-night-verification-report.md` | 10890 | (grandfathered) | B peer | GRANDFATHERED | KEEP |
| 209 | `2026-07-11-census-consolidated-morning-brief.md` | 49155 | census | A pool | ok | KEEP |
| 210 | `2026-07-11-changelog-review-codex-cc.md` | 10114 | changelog-review | B peer | ok | KEEP |
| 211 | `2026-07-11-technical-audit-corpus-verb-list.md` | 59157 | technical | B peer | ok | KEEP |
| 212 | `2026-07-11-technical-fleet-boundary-marker-design.md` | 26358 | technical | A pool | ok | KEEP |
| 213 | `2026-07-11-technical-fleet-boundary-matrix.md` | 31495 | technical | A pool | ok | KEEP |
| 214 | `2026-07-11-technical-fleet-parity-register.md` | 23666 | technical | A pool | ok | KEEP |
| 215 | `2026-07-11-technical-fleet-structure-comparison.md` | 6382 | technical | A pool | ok | KEEP |
| 216 | `2026-07-12-codex-ruff-hub-pin.md` | 1052 | codex | A pool | ok | KEEP |
| 217 | `2026-07-12-technical-night-c4-requirements.md` | 23607 | technical | A pool | ok | KEEP |
| 218 | `2026-07-12-technical-night-codex-review.md` | 9444 | technical | A pool | ok | KEEP |
| 219 | `2026-07-12-technical-night-delete-candidates.md` | 5437 | technical | A pool | ok | KEEP |
| 220 | `2026-07-12-technical-night-e2e-evidence.md` | 6202 | technical | B peer | ok | KEEP |
| 221 | `2026-07-12-technical-night-plan-continuity-proposal.md` | 3854 | technical | B peer | ok | KEEP |
| 222 | `2026-07-12-technical-night-rollout-ai-council.md` | 14158 | technical | B peer | ok | KEEP |
| 223 | `2026-07-12-technical-night-rollout-corp-monorepo.md` | 15144 | technical | B peer | ok | KEEP |
| 224 | `2026-07-12-technical-night-verdict-sheet.md` | 9059 | technical | B peer | ok | KEEP |
| 225 | `2026-07-13-technical-a0-traceability-closure.md` | 22015 | technical | B peer | ok | KEEP |
| 226 | `2026-07-13-technical-content-parity-inventory.md` | 40518 | technical | B peer | ok | KEEP |
| 227 | `2026-07-13-technical-satellite-onboarding-census.md` | 38148 | technical | A pool | ok | KEEP |
| 228 | `2026-07-13-technical-wave3-reading-friction-census.md` | 18201 | technical | B peer | ok | KEEP |
| 229 | `2026-07-16-codex-tail-firstread-lessons.md` | 362 | codex | B peer | ok | KEEP |
| 230 | `2026-07-16-technical-fleet-structure-census.md` | 37952 | technical | A pool | ok | KEEP |
| 231 | `2026-07-17-codex-adr29-legacy-split-amendment.md` | 4113 | codex | B peer | ok | KEEP |
| 232 | `2026-07-17-codex-arc3-ownership-axis.md` | 1013 | codex | B peer | ok | KEEP |
| 233 | `2026-07-17-codex-gate-rev-axis.md` | 4842 | codex | B peer | ok | KEEP |
| 234 | `2026-07-17-codex-role-governance.md` | 951 | codex | B peer | ok | KEEP |
| 235 | `2026-07-17-technical-night-divergence-ledger.md` | 21686 | technical | B peer | ok | KEEP |
| 236 | `2026-07-17-technical-night-handoff-evidence-pack.md` | 5783 | technical | B peer | ok | KEEP |
| 237 | `2026-07-17-technical-night-live-fire-sheet.md` | 7039 | technical | B peer | ok | KEEP |
| 238 | `2026-07-17-technical-night-verdict-sheet.md` | 5230 | technical | B peer | ok | KEEP |
| 239 | `2026-07-18-codex-adr-101-two-tier-new-path-v2.md` | 1822 | codex | B peer | ok | KEEP |
| 240 | `2026-07-18-codex-adr-101-two-tier-new-path-v3.md` | 1542 | codex | B peer | ok | KEEP |
| 241 | `2026-07-18-codex-adr-101-two-tier-new-path-v4.md` | 2282 | codex | B peer | ok | KEEP |
| 242 | `2026-07-18-codex-adr-101-two-tier-new-path-v5.md` | 977 | codex | B peer | ok | KEEP |
| 243 | `2026-07-18-codex-adr-101-two-tier-new-path.md` | 2390 | codex | B peer | ok | KEEP |
| 244 | `2026-07-18-codex-ruling-w-adr-amendment-v2.md` | 361 | codex | B peer | ok | KEEP |
| 245 | `2026-07-18-codex-ruling-w-adr-amendment.md` | 1845 | codex | B peer | ok | KEEP |
| 246 | `2026-07-18-technical-arc4-leg1-ruff-equalization.md` | 6430 | technical | B peer | ok | KEEP |
| 247 | `2026-07-19-census-silent-rule-ledger.md` | 27890 | census | A pool | ok | KEEP |
| 248 | `2026-07-19-codex-canon-inoculation.md` | 2553 | codex | B peer | ok | KEEP |
| 249 | `2026-07-19-codex-cycle-close-sol-adversarial-diff.md` | 10091 | codex | B peer | ok | KEEP |
| 250 | `2026-07-19-codex-cycle-close-terra-review.md` | 5347 | codex | A pool | ok | KEEP |
| 251 | `2026-07-19-codex-residual-completeness-gate.md` | 2638 | codex | A pool | ok | KEEP |
| 252 | `2026-07-19-codex-residual-rule-declaration.md` | 3146 | codex | A pool | ok | KEEP |
| 253 | `2026-07-19-technical-arc5-educate.md` | 7709 | technical | B peer | ok | KEEP |
| 254 | `2026-07-19-technical-night-consolidated-cycle-close.md` | 29527 | technical | A pool | ok | KEEP |
| 255 | `2026-07-19-technical-night-luna-carrier-inventory.md` | 4009 | technical | B peer | ok | KEEP |
| 256 | `2026-07-19-technical-night-s1-intake-adr-lifecycle.md` | 14591 | technical | B peer | ok | KEEP |
| 257 | `2026-07-19-technical-night-s2-backlog-decision-ops.md` | 13309 | technical | B peer | ok | KEEP |
| 258 | `2026-07-19-technical-night-s3-archives-lifecycle-records.md` | 13344 | technical | B peer | ok | KEEP |
| 259 | `2026-07-19-technical-night-s4-handoff-playbook-currency.md` | 16338 | technical | A pool | ok | KEEP |
| 260 | `2026-07-19-technical-night-s5-consumer-disk-info-audit.md` | 21839 | technical | B peer | ok | KEEP |
| 261 | `2026-07-19-technical-night-s6-worktree-discipline.md` | 13790 | technical | B peer | ok | KEEP |
| 262 | `2026-07-19-technical-night-s7-prompt-authoring-quality.md` | 17359 | technical | A pool | ok | KEEP |
| 263 | `2026-07-19-technical-night-s8-fleet-state-management.md` | 15634 | technical | B peer | ok | KEEP |
| 264 | `2026-07-19-technical-night-s9-testing-harness-agentic.md` | 16024 | technical | B peer | ok | KEEP |
| 265 | `2026-07-19-verification-night-e1-probe-fire-evidence.md` | 17665 | verification | B peer | ok | KEEP |
| 266 | `2026-07-20-codex-leg1-fleet-parity-gitdir-scrub.md` | 2538 | codex | B peer | ok | KEEP |
| 267 | `2026-07-20-codex-leg2-handoff-bundle-selection.md` | 3809 | codex | B peer | ok | KEEP |
| 268 | `2026-07-20-technical-352-boundary-render-diagnostic.md` | 10340 | technical | A pool | ok | KEEP |
| 269 | `2026-07-21-technical-night-backlog-audit.md` | 22996 | technical | B peer | ok | KEEP |
| 270 | `2026-07-21-technical-night-code-audit.md` | 54367 | technical | B peer | ok | KEEP |
| 271 | `2026-07-21-technical-night-vision-audit.md` | 26029 | technical | A pool | ok | KEEP |
| 272 | `2026-07-22-technical-hygiene-pre-handoff-inventory.md` | 8529 | technical | A pool | ok | KEEP |
| 273 | `2026-07-22-technical-night-batch-deep-audit.md` | 27355 | technical | A pool | ok | KEEP |
| 274 | `2026-07-22-verification-night-batch-integration-386-384.md` | 6128 | verification | A pool | ok | KEEP |
| 275 | `2026-07-23-technical-status-enum-reconcile.md` | 8342 | technical | A pool | ok | KEEP |
| 276 | `2026-07-25-codex-fix-live-backlog-test.md` | 733 | codex | B peer | ok | KEEP |
| 277 | `2026-07-25-codex-lane-d-rulings.md` | 3415 | codex | B peer | ok | KEEP |
| 278 | `2026-07-25-codex-vision-reread-recheck.md` | 2356 | codex | B peer | ok | KEEP |
| 279 | `2026-07-25-codex-vision-reread.md` | 2494 | codex | B peer | ok | KEEP |
| 280 | `2026-07-26-codex-routine-consumer-prose.md` | 1007 | codex | B peer | ok | KEEP |
| 281 | `2026-07-26-codex-routine-consumers-check.md` | 10173 | codex | B peer | ok | KEEP |
| 282 | `2026-07-27-census-silent-rule-ratchet-arm-measurement.md` | 21855 | census | A pool | ok | KEEP |
| 283 | `2026-07-27-codex-436-ratchet-clear.md` | 3464 | codex | B peer | ok | KEEP |
| 284 | `2026-07-27-codex-436-ratchet-final.md` | 3359 | codex | A pool | ok | KEEP |
| 285 | `2026-07-27-codex-436-ratchet-gate10.md` | 1438 | codex | B peer | ok | KEEP |
| 286 | `2026-07-27-codex-436-ratchet-gate5.md` | 4126 | codex | B peer | ok | KEEP |
| 287 | `2026-07-27-codex-436-ratchet-gate6.md` | 2621 | codex | B peer | ok | KEEP |
| 288 | `2026-07-27-codex-436-ratchet-gate7.md` | 2007 | codex | B peer | ok | KEEP |
| 289 | `2026-07-27-codex-436-ratchet-gate8.md` | 1852 | codex | B peer | ok | KEEP |
| 290 | `2026-07-27-codex-436-ratchet-gate9.md` | 1693 | codex | B peer | ok | KEEP |
| 291 | `2026-07-27-codex-436-ratchet-recheck.md` | 3232 | codex | B peer | ok | KEEP |
| 292 | `2026-07-27-codex-436-silent-rule-ratchet.md` | 4480 | codex | B peer | ok | KEEP |
| 293 | `2026-07-27-codex-adversarial-review-adr-107-sol.md` | 4460 | codex | A pool | ok | KEEP |
| 294 | `2026-07-27-codex-conformance-extraction-aggregate.md` | 2915 | codex | A pool | ok | KEEP |
| 295 | `2026-07-27-codex-handoff-v6-pack.md` | 4936 | codex | B peer | ok | KEEP |
| 296 | `2026-07-27-codex-lane-filings-uv-bakeoff-extraction.md` | 2808 | codex | B peer | ok | KEEP |
| 297 | `2026-07-27-verification-433-schema-spike.md` | 20146 | verification | A pool | ok | KEEP |
| 298 | `2026-07-27-verification-conformance-extraction-aggregate.md` | 16298 | verification | A pool | ok | KEEP |
| 299 | `2026-07-27-verification-handoff-process-audit.md` | 32132 | verification | A pool | ok | KEEP |
| 300 | `2026-07-28-codex-437-closure-design.md` | 4782 | codex | B peer | ok | KEEP |
| 301 | `2026-07-28-codex-437-closure-diff.md` | 3721 | codex | B peer | ok | KEEP |
| 302 | `2026-07-28-codex-437-closure-recheck.md` | 3655 | codex | B peer | ok | KEEP |
| 303 | `2026-07-28-codex-444-release-0-1-11.md` | 1166 | codex | B peer | ok | KEEP |
| 304 | `2026-07-28-codex-p6-prep-review.md` | 2952 | codex | B peer | ok | KEEP |
| 305 | `2026-07-28-technical-364-cap-option-matrix.md` | 6886 | technical | B peer | ok | KEEP |
| 306 | `2026-07-28-technical-382-charter.md` | 8738 | technical | A pool | ok | KEEP |
| 307 | `2026-07-28-technical-437-closure-token-design.md` | 17781 | technical | B peer | ok | KEEP |
| 308 | `2026-07-28-technical-d-queue-0826.md` | 6847 | technical | B peer | ok | KEEP |
| 309 | `2026-07-28-technical-drain-slice-prep.md` | 17209 | technical | B peer | ok | KEEP |
| 310 | `2026-07-28-technical-vscode-sizing-decision-surface.md` | 8088 | technical | B peer | ok | KEEP |
| 311 | `2026-07-29-codex-postflip-fix-batch-review.md` | 4541 | codex | A pool | ok | KEEP |
| 312 | `2026-07-29-conformance-nightly-digest.md` | 15549 | conformance-nightly-digest | B peer | ok | KEEP |
| 313 | `2026-07-29-technical-intake18-ratification-dossier.md` | 16030 | technical | B peer | ok | KEEP |
| 314 | `2026-07-29-technical-postflip-stale-procedure-audit.md` | 11990 | technical | A pool | ok | KEEP |
| 315 | `2026-07-29-technical-vscode-w1-visibility-ruling.md` | 4426 | technical | B peer | ok | KEEP |
| 316 | `2026-07-30-census-fleet-state-boot-prep.md` | 29908 | census | B peer | ok | KEEP |
| 317 | `2026-07-30-codex-446-v6-boot-build.md` | 4073 | codex | B peer | ok | KEEP |
| 318 | `2026-07-30-codex-446-v6-boot-prose.md` | 6103 | codex | B peer | ok | KEEP |
| 319 | `2026-07-30-conformance-nightly-digest.md` | 15243 | conformance-nightly-digest | B peer | ok | KEEP |
| 320 | `2026-07-30-qa-assemble-paste-test-gap-review.md` | 13834 | qa | B peer | ok | KEEP |
| 321 | `2026-07-30-technical-intake18-ratification-record.md` | 13644 | technical | A pool | ok | KEEP |
| 322 | `2026-07-30-technical-night-batch-standing-section-draft.md` | 11140 | technical | B peer | ok | KEEP |
| 323 | `2026-07-30-technical-proposals-2026-07-29-triage.md` | 40865 | technical | B peer | ok | KEEP |
| 324 | `2026-07-30-technical-v6-open-questions-ruling-dossier.md` | 37418 | technical | B peer | ok | KEEP |
| 325 | `2026-07-30-technical-v6-spec-sol-draft.md` | 16608 | technical | A pool | ok | KEEP |
| 326 | `2026-07-30-technical-vscode-w1-execution-record.md` | 5400 | technical | A pool | ok | KEEP |
| 327 | `2026-07-31-codex-382-w2-schema-v1.md` | 6731 | codex | B peer | ok | KEEP |
| 328 | `2026-07-31-codex-382-w3-loader.md` | 5155 | codex | B peer | ok | KEEP |
| 329 | `2026-07-31-codex-382-w4-report.md` | 5127 | codex | B peer | ok | KEEP |
| 330 | `2026-07-31-codex-intake-split-generality-discharge.md` | 3591 | codex | B peer | ok | KEEP |
| 331 | `2026-07-31-conformance-nightly-digest.md` | 14721 | conformance-nightly-digest | B peer | ok | KEEP |
| 332 | `2026-07-31-ecosystem-audit.md` | 27087 | ecosystem-audit | B peer | ok | KEEP |
| 333 | `2026-07-31-technical-382-arc-educate.md` | 5578 | technical | B peer | ok | KEEP |
| 334 | `2026-07-31-technical-382-registry-prep-dossier.md` | 51486 | technical | A pool | ok | KEEP |
| 335 | `2026-07-31-technical-382-schema-derivation-sol.md` | 28533 | technical | A pool | ok | KEEP |
| 336 | `2026-07-31-technical-382-w2-grok-shadow-ab.md` | 16215 | technical | B peer | ok | KEEP |
| 337 | `2026-07-31-technical-433-spike-prep.md` | 28105 | technical | B peer | ok | KEEP |
| 338 | `2026-07-31-technical-closure-ids-negation-defect.md` | 20206 | technical | B peer | ok | KEEP |
| 339 | `2026-07-31-technical-intake-split-generality-discharge.md` | 9215 | technical | B peer | ok | KEEP |
| 340 | `2026-07-31-technical-intake22-d-research-rows.md` | 27017 | technical | B peer | ok | KEEP |
| 341 | `2026-07-31-technical-p10-grooming-dossier.md` | 34741 | technical | A pool | ok | KEEP |
| 342 | `2026-07-31-technical-v6-frozen-contract.md` | 7596 | technical | B peer | ok | KEEP |
| 343 | `2026-07-31-technical-v6-open-rulings.md` | 3185 | technical | A pool | ok | KEEP |
| 344 | `2026-07-31-verification-382-ladder-evidence.md` | 16205 | verification | A pool | ok | KEEP |
| 345 | `2026-07-31-verification-first-live-v6-boot-report.md` | 6166 | verification | B peer | ok | KEEP |
| 346 | `2026-08-01-codex-460-replication-and-close.md` | 1301 | codex | B peer | ok | KEEP |
| 347 | `2026-08-01-codex-462-membership-agreement-census.md` | 1271 | codex | B peer | ok | KEEP |
| 348 | `2026-08-01-codex-generator-newlines-and-groom.md` | 872 | codex | B peer | ok | KEEP |
| 349 | `2026-08-01-conformance-nightly-digest.md` | 14912 | conformance-nightly-digest | B peer | ok | KEEP |
| 350 | `2026-08-01-technical-codex-wrapper-model-pin-and-lf.md` | 4613 | technical | A pool | ok | KEEP |
| 351 | `2026-08-01-technical-night-batch-l1-filing-pre-pack.md` | 15524 | technical | B peer | ok | KEEP |
| 352 | `2026-08-01-technical-night-batch-l2-repomix-pilot.md` | 13000 | technical | A pool | ok | KEEP |
| 353 | `2026-08-01-technical-night-batch-l3-copier-record.md` | 9859 | technical | B peer | ok | KEEP |
| 354 | `2026-08-01-technical-night-batch-l4-frontmatter-parser.md` | 8875 | technical | A pool | ok | KEEP |
| 355 | `2026-08-01-technical-night-batch-l5-delta-groom.md` | 15381 | technical | B peer | ok | KEEP |
| 356 | `2026-08-01-technical-night-batch-l6-460-decision-pack.md` | 16084 | technical | B peer | ok | KEEP |
| 357 | `2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md` | 8983 | technical | B peer | ok | KEEP |
| 358 | `2026-08-01-technical-night-batch-plan-prep.md` | 12116 | technical | B peer | ok | KEEP |
| 359 | `2026-08-01-technical-window-metrics.md` | 941 | technical | A pool | ok | KEEP |
| 360 | `2026-08-02-conformance-nightly-digest.md` | 14150 | conformance-nightly-digest | B peer | ok | KEEP |
| 361 | `2026-08-02-technical-night-batch-lb-fleet-audit-commits.md` | 9923 | technical | B peer | ok | KEEP |
| 362 | `2026-08-02-technical-night-batch-lc-agents-md-analysis.md` | 13274 | technical | B peer | ok | KEEP |
| 363 | `2026-08-02-technical-night-batch-ld-currency-audit.md` | 11682 | technical | B peer | ok | KEEP |
| 364 | `2026-08-02-technical-night-batch-le-library-first.md` | 8774 | technical | B peer | ok | KEEP |
| 365 | `2026-08-02-technical-night-batch-lf-backlog-health.md` | 10091 | technical | B peer | ok | KEEP |
| 366 | `2026-08-02-technical-night-ladder-and-plan-audit.md` | 28236 | technical | B peer | ok | KEEP |
| 367 | `2026-08-03-codex-472-declaration-anchor.md` | 2763 | codex | B peer | ok | KEEP |
| 368 | `2026-08-03-codex-472-terra-round2.md` | 2897 | codex | B peer | ok | KEEP |
| 369 | `2026-08-03-codex-474-gen-task-tree-write-guard-retro.md` | 2967 | codex | B peer | ok | KEEP |
| 370 | `2026-08-03-codex-475-seal-identity-precommit-gate-retro.md` | 3024 | codex | B peer | ok | KEEP |
| 371 | `2026-08-03-codex-adr85-integration-enforcement.md` | 4789 | codex | B peer | ok | KEEP |
| 372 | `2026-08-03-codex-arc2-terra-round2.md` | 2016 | codex | B peer | ok | KEEP |
| 373 | `2026-08-03-codex-arc2-vacuous-green-trio.md` | 2845 | codex | B peer | ok | KEEP |
| 374 | `2026-08-03-codex-arc3-mechanical-adoptions.md` | 2810 | codex | B peer | ok | KEEP |
| 375 | `2026-08-03-codex-arc3-terra-round2.md` | 1953 | codex | B peer | ok | KEEP |
| 376 | `2026-08-03-conformance-nightly-digest.md` | 14817 | conformance-nightly-digest | B peer | ok | KEEP |
| 377 | `2026-08-03-technical-383-caches-wave-record.md` | 11809 | technical | A pool | ok | KEEP |
| 378 | `2026-08-03-technical-night-batch-digest.md` | 26530 | technical | B peer | ok | KEEP |
| 379 | `2026-08-03-technical-night-la-w2-verification.md` | 26041 | technical | A pool | ok | KEEP |
| 380 | `2026-08-03-technical-night-lb-groom.md` | 44125 | technical | A pool | ok | KEEP |
| 381 | `2026-08-03-technical-night-lc-w4-staging.md` | 42219 | technical | B peer | ok | KEEP |
| 382 | `2026-08-03-technical-night-ld-472-option-b.md` | 25844 | technical | B peer | ok | KEEP |
| 383 | `2026-08-03-technical-night-le-library-first.md` | 19958 | technical | B peer | ok | KEEP |
| 384 | `2026-08-03-technical-night-lf-rulings-prep.md` | 40030 | technical | A pool | ok | KEEP |
| 385 | `2026-08-04-codex-465-leg4-inert-check-detector.md` | 3778 | codex | B peer | ok | KEEP |
| 386 | `2026-08-04-codex-465-terra-round2.md` | 3117 | codex | B peer | ok | KEEP |
| 387 | `2026-08-04-codex-481-organ-id-rename.md` | 7111 | codex | A pool | ok | KEEP |
| 388 | `2026-08-04-codex-482-glob-engine-true-glob.md` | 7702 | codex | B peer | ok | KEEP |
| 389 | `2026-08-04-codex-483-preflight-contract.md` | 4927 | codex | B peer | ok | KEEP |
| 390 | `2026-08-04-codex-483-preflight-discrimination.md` | 11040 | codex | A pool | ok | KEEP |
| 391 | `2026-08-04-codex-483-terra-round2.md` | 3972 | codex | B peer | ok | KEEP |
| 392 | `2026-08-04-conformance-nightly-digest.md` | 15665 | conformance-nightly-digest | B peer | ok | KEEP |
| 393 | `2026-08-04-technical-480-ruling-input-pack.md` | 12692 | technical | B peer | ok | KEEP |
| 394 | `2026-08-04-technical-483-enforcement-ruling.md` | 5647 | technical | A pool | ok | KEEP |
| 395 | `2026-08-04-technical-closure-proposal-ranked-sheet.md` | 29885 | technical | B peer | ok | KEEP |
| 396 | `2026-08-05-codex-480-review-artifact-organ.md` | 6446 | codex | B peer | ok | KEEP |
| 397 | `2026-08-05-codex-498-hook-exec-bit.md` | 2341 | codex | A pool | ok | KEEP |
| 398 | `2026-08-05-conformance-nightly-digest.md` | 13310 | conformance-nightly-digest | B peer | ok | KEEP |
| 399 | `2026-08-05-technical-night-batch-morning-report.md` | 26561 | technical | A pool | ok | KEEP |
| 400 | `2026-08-06-codex-batch-protocol.md` | 5182 | codex | B peer | ok | KEEP |
| 401 | `2026-08-06-codex-lane-c-504-failclosed.md` | 1823 | codex | B peer | ok | KEEP |
| 402 | `2026-08-06-technical-batch-1-integration-packet.md` | 11364 | technical | B peer | ok | KEEP |
| 403 | `2026-08-06-technical-batch1-verification.md` | 41054 | technical | A pool | ok | KEEP |
| 404 | `2026-08-06-technical-lane-a-architecture-rows.md` | 7393 | technical | B peer | ok | KEEP |
| 405 | `2026-08-06-technical-night-408-coupling-manifest-design.md` | 28975 | technical | A pool | ok | KEEP |
| 406 | `2026-08-06-technical-night-library-research.md` | 26785 | technical | B peer | ok | KEEP |
| 407 | `2026-08-06-technical-night-morning-packet.md` | 27678 | technical | B peer | ok | KEEP |
| 408 | `2026-08-06-technical-night-prep-packs.md` | 34789 | technical | A pool | ok | KEEP |
| 409 | `2026-08-06-technical-night-window-review.md` | 36118 | technical | B peer | ok | KEEP |
| 410 | `2026-08-06-verification-lane-c-arch-327.md` | 8792 | verification | B peer | ok | KEEP |
| 411 | `2026-08-07-codex-lane-1-490-430-parity-manifest.md` | 4282 | codex | B peer | ok | KEEP |
| 412 | `2026-08-07-codex-lane-2-worktree-portability.md` | 12967 | codex | B peer | ok | KEEP |
| 413 | `2026-08-07-codex-lane-a-501-retro.md` | 4885 | codex | B peer | ok | KEEP |
| 414 | `2026-08-07-codex-lane-b-503-retro.md` | 3007 | codex | B peer | ok | KEEP |
| 415 | `2026-08-07-codex-morning-f4-retro.md` | 6599 | codex | B peer | ok | KEEP |
| 416 | `2026-08-07-codex-mutmut-sandbox-skip.md` | 3250 | codex | B peer | ok | KEEP |
| 417 | `2026-08-07-codex-pre-cut-retro-batch2-consolidation.md` | 855 | codex | B peer | ok | KEEP |
| 418 | `2026-08-07-codex-pre-cut-retro-handoff-engine-thinning.md` | 1343 | codex | A pool | ok | KEEP |
| 419 | `2026-08-07-codex-pre2-arc-retro.md` | 8153 | codex | B peer | ok | KEEP |
| 420 | `2026-08-07-codex-pre2-selfreview-arc.md` | 4835 | codex | B peer | ok | KEEP |
| 421 | `2026-08-07-conformance-nightly-digest.md` | 10042 | conformance-nightly-digest | B peer | ok | KEEP |
| 422 | `2026-08-07-technical-batch-2-lessons.md` | 16022 | technical | A pool | ok | KEEP |
| 423 | `2026-08-07-technical-batch-2-manifest.md` | 10125 | technical | B peer | ok | KEEP |
| 424 | `2026-08-07-technical-batch-2-packet.md` | 27068 | technical | A pool | ok | KEEP |
| 425 | `2026-08-07-technical-fleet-backup-posture.md` | 4449 | technical | B peer | ok | KEEP |
| 426 | `2026-08-07-technical-handoff-engine-thinning.md` | 16885 | technical | B peer | ok | KEEP |
| 427 | `2026-08-07-technical-lane-2-worktree-portability.md` | 23010 | technical | B peer | ok | KEEP |
| 428 | `2026-08-08-codex-batch-3-integrator-arc.md` | 4344 | codex | B peer | ok | KEEP |
| 429 | `2026-08-08-codex-deploy-doc-carrier.md` | 3495 | codex | B peer | ok | KEEP |
| 430 | `2026-08-08-codex-lane-290-floor-teeth.md` | 5367 | codex | B peer | ok | KEEP |
| 431 | `2026-08-08-codex-lane-e-396-512-gitenv-scrub.md` | 7425 | codex | B peer | ok | KEEP |
| 432 | `2026-08-08-conformance-nightly-digest.md` | 13373 | conformance-nightly-digest | B peer | ok | KEEP |
| 433 | `2026-08-08-technical-502-pythonpath-measurement.md` | 13683 | technical | A pool | ok | KEEP |
| 434 | `2026-08-08-technical-506-open-set-grooming-sheet.md` | 58913 | technical | B peer | ok | KEEP |
| 435 | `2026-08-08-technical-archival-lifecycle-audit.md` | 25799 | technical | B peer | ok | KEEP |
| 436 | `2026-08-08-technical-batch-3-consolidation-report.md` | 45218 | technical | B peer | ok | KEEP |
| 437 | `2026-08-08-technical-batch-3-manifest.md` | 11635 | technical | B peer | ok | KEEP |
| 438 | `2026-08-08-technical-batch-3-packet.md` | 9569 | technical | A pool | ok | KEEP |
| 439 | `2026-08-08-technical-closure-wave-proposals.md` | 53268 | technical | B peer | ok | KEEP |
| 440 | `2026-08-08-technical-handoff-cut-staging.md` | 41188 | technical | B peer | ok | KEEP |
| 441 | `2026-08-08-technical-lane-c-393-corpsca-rot-review.md` | 23613 | technical | B peer | ok | KEEP |
| 442 | `2026-08-08-technical-library-research.md` | 46119 | technical | A pool | ok | KEEP |
| 443 | `2026-08-08-technical-seeded-defect-substrate-inventory.md` | 28625 | technical | A pool | ok | KEEP |
| 444 | `2026-08-08-technical-successor-prep.md` | 41462 | technical | A pool | ok | KEEP |
| 445 | `2026-08-09-codex-arc1-doc-defects-retro.md` | 4909 | codex | B peer | ok | KEEP |
| 446 | `2026-08-09-codex-batch-3-integrator-arc.md` | 5695 | codex | B peer | ok | KEEP |
| 447 | `2026-08-09-conformance-nightly-digest.md` | 14336 | conformance-nightly-digest | B peer | ok | KEEP |
| 448 | `2026-08-09-technical-batch-night-manifest.md` | 9139 | technical | B peer | ok | KEEP |
| 449 | `2026-08-09-technical-batch-night-packet.md` | 25244 | technical | B peer | ok | KEEP |
| 450 | `2026-08-09-technical-challenge-retrieval.md` | 57828 | technical | B peer | ok | KEEP |
| 451 | `2026-08-09-technical-consolidation-report.md` | 41447 | technical | A pool | ok | KEEP |
| 452 | `2026-08-09-technical-decision-sheet.md` | 10226 | technical | B peer | ok | KEEP |
| 453 | `2026-08-09-technical-n1-position-northstar.md` | 40090 | technical | B peer | ok | KEEP |
| 454 | `2026-08-09-technical-n4-code-review.md` | 34351 | technical | B peer | ok | KEEP |
| 455 | `2026-08-09-technical-night-batch-findings-index.md` | 61219 | technical | B peer | ok | KEEP |
| 456 | `2026-08-09-technical-night-n2-mechanism-map.md` | 60328 | technical | B peer | ok | KEEP |
| 457 | `2026-08-09-technical-night-n3-performance-instrumentation.md` | 52733 | technical | A pool | ok | KEEP |
| 458 | `2026-08-09-technical-night-n5-library-first-sweep.md` | 33821 | technical | B peer | ok | KEEP |
| 459 | `2026-08-10-census-conformance-digest-content.md` | 35380 | census | B peer | ok | KEEP |
| 460 | `2026-08-10-conformance-nightly-digest.md` | 21588 | conformance-nightly-digest | B peer | ok | KEEP |
| 461 | `2026-08-10-technical-backlog-testability-census.md` | 82458 | technical | A pool | ok | KEEP |
| 462 | `2026-08-10-technical-batch-4-execution-plan-draft.md` | 56590 | technical | A pool | ok | KEEP |
| 463 | `2026-08-10-technical-batch-4-prep-evidence.md` | 60147 | technical | B peer | ok | KEEP |
| 464 | `2026-08-10-technical-batch-night-cloud-manifest.md` | 10424 | technical | B peer | ok | KEEP |
| 465 | `2026-08-10-technical-batch-night-cloud-packet.md` | 7967 | technical | B peer | ok | KEEP |
| 466 | `2026-08-10-technical-decision-sheet-verification.md` | 14993 | technical | A pool | ok | KEEP |
| 467 | `2026-08-10-technical-night-n1-window-synthesis.md` | 33275 | technical | B peer | ok | KEEP |
| 468 | `2026-08-10-technical-night-n3-ratification-pack.md` | 70290 | technical | B peer | ok | KEEP |
| 469 | `2026-08-10-technical-origin-branch-census.md` | 10831 | technical | B peer | ok | KEEP |
| 470 | `2026-08-10-technical-research-corpus-distillate.md` | 43916 | technical | A pool | ok | KEEP |
| 471 | `2026-08-10-technical-research-ingest-reconcile-and-packet.md` | 21976 | technical | B peer | ok | KEEP |
| 472 | `2026-08-10-technical-satisfied-row-census.md` | 14824 | technical | B peer | ok | KEEP |
| 473 | `2026-08-10-verification-arc9-rulings-recording.md` | 20610 | verification | A pool | ok | KEEP |
| 474 | `2026-08-10-verification-fable-adversarial-plan-review.md` | 27151 | verification | A pool | ok | KEEP |
| 475 | `2026-08-10-verification-ruled-dispositions-and-digest-gap.md` | 13623 | verification | B peer | ok | KEEP |
| 476 | `2026-08-11-codex-arc9-absorb-m6-gen-audit-index.md` | 4331 | codex | B peer | ok | KEEP |
| 477 | `2026-08-11-codex-batch4-w1-lane-regex.md` | 3515 | codex | B peer | ok | KEEP |
| 478 | `2026-08-11-codex-batch4-w5-organ-index.md` | 7335 | codex | B peer | ok | KEEP |
| 479 | `2026-08-11-codex-lane-b-270-load-gauge.md` | 7041 | codex | A pool | ok | KEEP |
| 480 | `2026-08-11-codex-lane-f-521-syspath-substrate.md` | 7138 | codex | A pool | ok | KEEP |
| 481 | `2026-08-11-technical-batch-4-brief-next-architect.md` | 6357 | technical | A pool | ok | KEEP |
| 482 | `2026-08-11-technical-batch-4-manifest.md` | 40739 | technical | A pool | ok | KEEP |
| 483 | `2026-08-11-technical-batch-4-packet.md` | 20877 | technical | A pool | ok | KEEP |
| 484 | `2026-08-11-technical-batch-4-w1-lane-contract.md` | 4815 | technical | B peer | ok | KEEP |
| 485 | `2026-08-11-technical-batch-4-w2-lane-contract.md` | 4887 | technical | A pool | ok | KEEP |
| 486 | `2026-08-11-technical-batch-4-w5-lane-contract.md` | 3927 | technical | B peer | ok | KEEP |
| 487 | `2026-08-11-technical-batch-4-w521-lane-contract.md` | 4268 | technical | B peer | ok | KEEP |
| 488 | `2026-08-11-verification-batch-4-challenge-answer.md` | 8341 | verification | B peer | ok | KEEP |
| 489 | `2026-08-12-codex-closing-arc-organ-index-guard.md` | 8024 | codex | B peer | ok | KEEP |
| 490 | `2026-08-12-technical-night-2-lessons-governance-strategy.md` | 111084 | technical | A pool | ok | KEEP |
| 491 | `2026-08-12-technical-roadmap-north-star-frozen.md` | 6605 | technical | A pool | ok | KEEP |
| 492 | `2026-08-12-verification-night-1-truth-audit-and-handoff-numbers.md` | 71651 | verification | A pool | ok | KEEP |
| 493 | `2026-08-13-codex-w3-landing-predicate.md` | 1712 | codex | B peer | ok | KEEP |
| 494 | `2026-08-13-technical-492-corpus-reconciliation-lane-contract.md` | 2721 | technical | B peer | ok | KEEP |
| 495 | `2026-08-13-technical-524-check-extensions-lane-contract.md` | 3389 | technical | B peer | ok | KEEP |
| 496 | `2026-08-13-technical-batch-4-w3-lane-contract.md` | 3440 | technical | B peer | ok | KEEP |
| 497 | `2026-08-13-technical-batch-4-w4c-lane-contract.md` | 3030 | technical | B peer | ok | KEEP |
| 498 | `2026-08-13-technical-batch-4-w4d-lane-contract.md` | 2917 | technical | B peer | ok | KEEP |
| 499 | `2026-08-13-technical-w4a-conversions-lane-contract.md` | 2881 | technical | B peer | ok | KEEP |
| 500 | `2026-08-13-technical-w4b-conversions-lane-contract.md` | 4341 | technical | B peer | ok | KEEP |
| 501 | `2026-08-13-verification-492-corpus-reconciliation.md` | 6235 | verification | A pool | ok | KEEP |
| 502 | `2026-08-14-census-night2-census.md` | 64699 | census | A pool | ok | KEEP |
| 503 | `2026-08-14-codex-524-check-extensions.md` | 2809 | codex | A pool | ok | KEEP |
| 504 | `2026-08-14-qa-night2-quality.md` | 40786 | qa | B peer | ok | KEEP |
| 505 | `2026-08-14-technical-525-arch-organ-rows-lane-contract.md` | 2919 | technical | B peer | ok | KEEP |
| 506 | `2026-08-14-technical-batch-4-true-close-packet.md` | 5532 | technical | A pool | ok | KEEP |
| 507 | `2026-08-14-technical-night2-latency.md` | 33736 | technical | A pool | ok | KEEP |
| 508 | `2026-08-14-technical-night2-research.md` | 45520 | technical | A pool | ok | KEEP |
| 509 | `2026-08-14-technical-w4-wave2-conversion-drafts.md` | 43103 | technical | B peer | ok | KEEP |
| 510 | `2026-08-14-verification-night2-hygiene.md` | 62508 | verification | B peer | ok | KEEP |
| 511 | `2026-08-14-verification-night2-plancheck.md` | 38793 | verification | B peer | ok | KEEP |
| 512 | `2026-08-15-codex-m-review.md` | 3437 | codex | B peer | ok | KEEP |
| 513 | `2026-08-15-codex-n-review.md` | 3210 | codex | B peer | ok | KEEP |
| 514 | `2026-08-15-codex-o-review.md` | 3502 | codex | B peer | ok | KEEP |
| 515 | `2026-08-15-codex-p-review.md` | 7648 | codex | B peer | ok | KEEP |
| 516 | `2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md` | 3190 | technical | B peer | ok | KEEP |
| 517 | `2026-08-15-technical-293-consumer-runbook-fan-out-lane-packet.md` | 6447 | technical | B peer | ok | KEEP |
| 518 | `2026-08-15-technical-527-block-main-lane-contract.md` | 3455 | technical | B peer | ok | KEEP |
| 519 | `2026-08-15-technical-528-legs12-latency-lane-contract.md` | 3969 | technical | B peer | ok | KEEP |
| 520 | `2026-08-15-technical-528-legs12-manifest.md` | 9240 | technical | B peer | ok | KEEP |
| 521 | `2026-08-15-technical-528-legs12-packet.md` | 13058 | technical | A pool | ok | KEEP |
| 522 | `2026-08-15-technical-529-telemetry-emit-lane-contract.md` | 6146 | technical | B peer | ok | KEEP |
| 523 | `2026-08-15-technical-529-telemetry-emit-lane-packet.md` | 13753 | technical | B peer | ok | KEEP |
| 524 | `2026-08-15-technical-530-single-flight-lane-contract.md` | 3866 | technical | B peer | ok | KEEP |
| 525 | `2026-08-15-technical-530-single-flight-lane-packet.md` | 12033 | technical | B peer | ok | KEEP |
| 526 | `2026-08-15-technical-batch-phase1-manifest.md` | 16961 | technical | B peer | ok | KEEP |
| 527 | `2026-08-15-technical-batch-phase1-packet.md` | 24293 | technical | A pool | ok | KEEP |
| 528 | `2026-08-15-technical-gateclose-drain8-lane-contract.md` | 3406 | technical | B peer | ok | KEEP |
| 529 | `2026-08-15-technical-night2-consolidated-briefing.md` | 121382 | technical | A pool | ok | KEEP |
| 530 | `2026-08-15-technical-night3-decision-queue.md` | 35610 | technical | A pool | ok | KEEP |
| 531 | `2026-08-15-technical-night3-research.md` | 37436 | technical | A pool | ok | KEEP |
| 532 | `2026-08-15-technical-night3-sessionplan.md` | 32513 | technical | B peer | ok | KEEP |
| 533 | `2026-08-15-technical-w20-draft-landing-lane-contract.md` | 5176 | technical | B peer | ok | KEEP |
| 534 | `2026-08-15-verification-night3-landed-review.md` | 39942 | verification | B peer | ok | KEEP |
| 535 | `2026-08-15-verification-night3-warn-ledger.md` | 48846 | verification | A pool | ok | KEEP |
| 536 | `2026-08-16-census-nb4-closing-campaign.md` | 39997 | census | A pool | ok | KEEP |
| 537 | `2026-08-16-census-nb6-archive-sweep.md` | 34897 | census | A pool | ok | KEEP |
| 538 | `2026-08-16-technical-210-conversions-lane-contract.md` | 3807 | technical | B peer | ok | KEEP |
| 539 | `2026-08-16-technical-271-conversions-lane-contract.md` | 1086 | technical | B peer | ok | KEEP |
| 540 | `2026-08-16-technical-277-issues-evidence-lane-contract.md` | 1237 | technical | B peer | ok | KEEP |
| 541 | `2026-08-16-technical-310-ledger-docs-lane-contract.md` | 2921 | technical | B peer | ok | KEEP |
| 542 | `2026-08-16-technical-409-conversions-lane-a-contract.md` | 1281 | technical | B peer | ok | KEEP |
| 543 | `2026-08-16-technical-532-docrot-arms-lane-contract.md` | 1554 | technical | B peer | ok | KEEP |
| 544 | `2026-08-16-technical-533-audit-decompose-lane-contract.md` | 5407 | technical | A pool | ok | KEEP |
| 545 | `2026-08-16-technical-82-conversions-lane-contract.md` | 4025 | technical | B peer | ok | KEEP |
| 546 | `2026-08-16-technical-batch-6-manifest.md` | 21889 | technical | A pool | ok | KEEP |
| 547 | `2026-08-16-technical-batch-6-packet.md` | 5240 | technical | A pool | ok | KEEP |
| 548 | `2026-08-16-technical-k-293-cross-repo-seeding-lane-contract.md` | 1314 | technical | B peer | ok | KEEP |
| 549 | `2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` | 31385 | technical | A pool | ok | KEEP |
| 550 | `2026-08-16-technical-nb4-consolidated-briefing.md` | 64208 | technical | B peer | ok | KEEP |
| 551 | `2026-08-16-technical-nb4-fleet-parity.md` | 20792 | technical | B peer | ok | KEEP |
| 552 | `2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` | 29117 | technical | A pool | ok | KEEP |
| 553 | `2026-08-16-technical-nb4-g-scaleout-substrate.md` | 58979 | technical | B peer | ok | KEEP |
| 554 | `2026-08-16-technical-nb4-llm-acceptance.md` | 42167 | technical | B peer | ok | KEEP |
| 555 | `2026-08-16-technical-nb4-telemetry-read.md` | 39089 | technical | B peer | ok | KEEP |
| 556 | `2026-08-16-technical-nb5-consumer-home.md` | 32303 | technical | B peer | ok | KEEP |
| 557 | `2026-08-16-technical-nb5-seam-repoint.md` | 30544 | technical | A pool | ok | KEEP |
| 558 | `2026-08-16-technical-nb6-handoff-prep.md` | 47094 | technical | B peer | ok | KEEP |
| 559 | `2026-08-16-technical-w2c-conversions-lane-contract.md` | 937 | technical | B peer | ok | KEEP |
| 560 | `2026-08-16-technical-w2d-lane-contract.md` | 3194 | technical | B peer | ok | KEEP |
| 561 | `2026-08-16-technical-w2f-conversions-lane-contract.md` | 1006 | technical | B peer | ok | KEEP |
| 562 | `2026-08-16-verification-nb4-equilibrium.md` | 44682 | verification | A pool | ok | KEEP |
| 563 | `2026-08-16-verification-nb4-playbook-gap.md` | 58659 | verification | A pool | ok | KEEP |
| 564 | `2026-08-16-verification-nb6-achievements.md` | 19546 | verification | B peer | ok | KEEP |
| 565 | `2026-08-16-verification-nb6-backlog-truth.md` | 51478 | verification | A pool | ok | KEEP |
| 566 | `2026-08-17-census-nb7-orphan-census.md` | 41475 | census | A pool | ok | KEEP |
| 567 | `2026-08-17-census-north-star-inventory.md` | 44373 | census | B peer | ok | KEEP |
| 568 | `2026-08-17-technical-audit-disposition-ledger.md` | 47493 | technical | A pool | ok | KEEP |
| 569 | `2026-08-17-technical-batch-7a-lane-a-contract.md` | 8203 | technical | B peer | ok | KEEP |
| 570 | `2026-08-17-technical-batch-7a-lane-b-contract.md` | 8843 | technical | A pool | ok | KEEP |
| 571 | `2026-08-17-technical-batch-7a-lane-c-contract.md` | 7726 | technical | B peer | ok | KEEP |
| 572 | `2026-08-17-technical-batch-7a-manifest.md` | 14684 | technical | A pool | ok | KEEP |
| 573 | `2026-08-17-technical-batch-7a-packet.md` | 17273 | technical | B peer | ok | KEEP |
| 574 | `2026-08-17-technical-nb7-lifecycle-instrument-verdict.md` | 47147 | technical | B peer | ok | KEEP |
| 575 | `2026-08-17-technical-research-intake-lane-contract.md` | 12205 | technical | A pool | ok | KEEP |
| 576 | `2026-08-18-census-adoption-preflight.md` | 33798 | census | B peer | ok | KEEP |
| 577 | `2026-08-18-census-p10-grooming-evidence.md` | 42321 | census | B peer | ok | KEEP |
| 578 | `2026-08-18-codex-review-batch1-a.md` | 6311 | codex | B peer | ok | KEEP |
| 579 | `2026-08-18-codex-review-batch1-c-e.md` | 23860 | codex | B peer | ok | KEEP |
| 580 | `2026-08-18-technical-502-mutmut-attribution.md` | 14930 | technical | B peer | ok | KEEP |
| 581 | `2026-08-18-technical-502-mutmut-lane-contract.md` | 4578 | technical | B peer | ok | KEEP |
| 582 | `2026-08-18-technical-533-leg2-lane-contract.md` | 6023 | technical | B peer | ok | KEEP |
| 583 | `2026-08-18-technical-533-leg2-measurements.md` | 17956 | technical | B peer | ok | KEEP |
| 584 | `2026-08-18-technical-554-devcontainer-lane-contract.md` | 30825 | technical | A pool | ok | KEEP |
| 585 | `2026-08-18-technical-a9-trim-lane-contract.md` | 3598 | technical | B peer | ok | KEEP |
| 586 | `2026-08-18-technical-a9-trim-lane-packet.md` | 18999 | technical | B peer | ok | KEEP |
| 587 | `2026-08-18-technical-adoption-preflight-lane-contract.md` | 2481 | technical | B peer | ok | KEEP |
| 588 | `2026-08-18-technical-batch1-integrator-contract.md` | 6659 | technical | B peer | ok | KEEP |
| 589 | `2026-08-18-technical-batch1-integrator-packet.md` | 20691 | technical | B peer | ok | KEEP |
| 590 | `2026-08-18-technical-p10-regen-lane-contract.md` | 2736 | technical | B peer | ok | KEEP |
| 591 | `2026-08-18-technical-phase0-baselines.md` | 13982 | technical | A pool | ok | KEEP |
| 592 | `2026-08-18-technical-review-lane-contract.md` | 3373 | technical | B peer | ok | KEEP |
| 593 | `2026-08-19-technical-171-dashboard-lane-contract.md` | 3860 | technical | B peer | ok | KEEP |
| 594 | `2026-08-19-technical-486-cp1252-lane-contract.md` | 2409 | technical | B peer | ok | KEEP |
| 595 | `2026-08-19-technical-554-proof-lane-contract.md` | 3251 | technical | B peer | ok | KEEP |
| 596 | `2026-08-19-technical-554-proof.md` | 20409 | technical | B peer | ok | KEEP |
| 597 | `2026-08-19-technical-backlogmd-trial-lane-contract.md` | 3576 | technical | B peer | ok | KEEP |
| 598 | `2026-08-19-technical-backlogmd-trial.md` | 39883 | technical | A pool | ok | KEEP |
| 599 | `2026-08-19-technical-c-lanes-consolidated.md` | 19378 | technical | B peer | ok | KEEP |
| 600 | `2026-08-19-technical-c1-seeded-defect-pack.md` | 43544 | technical | A pool | ok | KEEP |
| 601 | `2026-08-19-technical-c1-seeded-defects-contract.md` | 3629 | technical | B peer | ok | KEEP |
| 602 | `2026-08-19-technical-c2-review-profiles-contract.md` | 2591 | technical | B peer | ok | KEEP |
| 603 | `2026-08-19-technical-c2-review-profiles.md` | 33337 | technical | A pool | ok | KEEP |
| 604 | `2026-08-19-technical-c3-grooming-wave2-contract.md` | 2258 | technical | B peer | ok | KEEP |
| 605 | `2026-08-19-technical-c3-grooming-wave2.md` | 121571 | technical | B peer | ok | KEEP |
| 606 | `2026-08-19-technical-c4-ruling-prework-contract.md` | 3279 | technical | B peer | ok | KEEP |
| 607 | `2026-08-19-technical-c4-ruling-prework.md` | 29042 | technical | A pool | ok | KEEP |
| 608 | `2026-08-19-technical-c6-telemetry-readpath-contract.md` | 2281 | technical | B peer | ok | KEEP |
| 609 | `2026-08-19-technical-c6-telemetry-readpath.md` | 64603 | technical | B peer | ok | KEEP |
| 610 | `2026-08-19-technical-cloud-c1-brief.md` | 1879 | technical | B peer | ok | KEEP |
| 611 | `2026-08-19-technical-cloud-c2-brief.md` | 1630 | technical | B peer | ok | KEEP |
| 612 | `2026-08-19-technical-cloud-c3-brief.md` | 1666 | technical | B peer | ok | KEEP |
| 613 | `2026-08-19-technical-cloud-c4-brief.md` | 1651 | technical | B peer | ok | KEEP |
| 614 | `2026-08-19-technical-cloud-c6-brief.md` | 1806 | technical | B peer | ok | KEEP |
| 615 | `2026-08-19-technical-l2-wiring-lane-contract.md` | 5076 | technical | B peer | ok | KEEP |
| 616 | `2026-08-19-technical-l2-wiring-lane-packet.md` | 35084 | technical | B peer | ok | KEEP |
| 617 | `2026-08-19-technical-morning-consolidation-contract.md` | 4780 | technical | B peer | ok | KEEP |
| 618 | `2026-08-19-technical-n1-529-530-wiring-spec.md` | 42889 | technical | B peer | ok | KEEP |
| 619 | `2026-08-19-technical-n1-wiring-spec-contract.md` | 3598 | technical | B peer | ok | KEEP |
| 620 | `2026-08-19-technical-n2-seam-worksheet-contract.md` | 3786 | technical | B peer | ok | KEEP |
| 621 | `2026-08-19-technical-n2-seam-worksheet.md` | 44970 | technical | B peer | ok | KEEP |
| 622 | `2026-08-19-technical-n3-ratification-pack-contract.md` | 3466 | technical | B peer | ok | KEEP |
| 623 | `2026-08-19-technical-n3-ratification-pack.md` | 77948 | technical | A pool | ok | KEEP |
| 624 | `2026-08-19-technical-n4-grooming-wave1.md` | 56933 | technical | A pool | ok | KEEP |
| 625 | `2026-08-19-technical-n5-codification-pack-contract.md` | 3931 | technical | B peer | ok | KEEP |
| 626 | `2026-08-19-technical-n5-codification-pack.md` | 49838 | technical | A pool | ok | KEEP |
| 627 | `2026-08-19-technical-s1-seat-arc-contract.md` | 4047 | technical | A pool | ok | KEEP |
| 628 | `2026-08-19-technical-s1-seat-arc-packet.md` | 16193 | technical | B peer | ok | KEEP |
| 629 | `2026-08-20-technical-codespaces-audit.md` | 61534 | technical | A pool | ok | KEEP |
| 630 | `2026-08-20-technical-final-integrator-contract.md` | 3755 | technical | B peer | ok | KEEP |
| 631 | `2026-08-20-technical-gemini-ab-lane-contract-slot1.md` | 1798 | technical | B peer | ok | KEEP |
| 632 | `2026-08-20-technical-gemini-ab-lane-contract.md` | 5247 | technical | B peer | ok | KEEP |
| 633 | `2026-08-20-technical-gemini-ab-results-slot1.md` | 13139 | technical | B peer | ok | KEEP |
| 634 | `2026-08-20-technical-gemini-ab-results.md` | 61794 | technical | A pool | ok | KEEP |
| 635 | `2026-08-20-technical-grok-ab-lane-contract-2.md` | 3350 | technical | B peer | ok | KEEP |
| 636 | `2026-08-20-technical-grok-ab-results-2.md` | 76292 | technical | A pool | ok | KEEP |
| 637 | `2026-08-20-technical-parallel-flip-lane-contract.md` | 1255 | technical | B peer | ok | KEEP |
| 638 | `2026-08-20-technical-playbook-status-lane-contract.md` | 3685 | technical | B peer | ok | KEEP |
| 639 | `2026-08-20-technical-playbook-status.md` | 38896 | technical | A pool | ok | KEEP |
| 640 | `2026-08-20-technical-transcription-seat-contract.md` | 6312 | technical | A pool | ok | KEEP |
| 641 | `2026-08-21-census-cloud-r4-adr-review.md` | 37037 | census | B peer | ok | KEEP |
| 642 | `2026-08-21-fresh-eyes-cloud-r1-governance-drift.md` | 37010 | fresh-eyes | B peer | ok | KEEP |
| 643 | `2026-08-21-fresh-eyes-cloud-r2-universalization.md` | 56039 | fresh-eyes | A pool | ok | KEEP |
| 644 | `2026-08-21-fresh-eyes-cloud-r3-conformance.md` | 16952 | fresh-eyes | A pool | ok | KEEP |
| 645 | `2026-08-21-technical-ch8-dispatch-codification-lane-contract.md` | 3591 | technical | B peer | ok | KEEP |
| 646 | `2026-08-21-technical-ch8-dispatch-codification.md` | 32265 | technical | B peer | ok | KEEP |
| 647 | `2026-08-21-technical-cloud-r1-brief.md` | 1997 | technical | B peer | ok | KEEP |
| 648 | `2026-08-21-technical-cloud-r2-brief.md` | 2246 | technical | B peer | ok | KEEP |
| 649 | `2026-08-21-technical-cloud-r3-brief.md` | 1488 | technical | B peer | ok | KEEP |
| 650 | `2026-08-21-technical-cloud-r4-brief.md` | 1557 | technical | B peer | ok | KEEP |
| 651 | `2026-08-21-technical-graph-and-workflows-lane-contract.md` | 4801 | technical | B peer | ok | KEEP |
| 652 | `2026-08-21-technical-graph-and-workflows.md` | 37764 | technical | A pool | ok | KEEP |
| 653 | `2026-08-21-technical-lane-554-cloud-provisioning-lane-contract.md` | 3217 | technical | B peer | ok | KEEP |
| 654 | `2026-08-21-technical-lane-554-cloud-provisioning.md` | 25048 | technical | B peer | ok | KEEP |
| 655 | `2026-08-21-technical-lane-arch-lifecycle-archival-lane-contract.md` | 2463 | technical | B peer | ok | KEEP |
| 656 | `2026-08-21-technical-lane-arch-lifecycle-archival.md` | 23220 | technical | B peer | ok | KEEP |
| 657 | `2026-08-21-technical-lane-rat-intake-ratification-lane-contract.md` | 2275 | technical | B peer | ok | KEEP |
| 658 | `2026-08-21-technical-lane-rat-intake-ratification.md` | 27135 | technical | A pool | ok | KEEP |
| 659 | `2026-08-21-technical-lane-tel-run-id-lane-contract.md` | 2050 | technical | B peer | ok | KEEP |
| 660 | `2026-08-21-technical-lane-tel-run-id.md` | 19089 | technical | A pool | ok | KEEP |
| 661 | `2026-08-21-technical-library-first-research-lane-contract.md` | 6483 | technical | B peer | ok | KEEP |
| 662 | `2026-08-21-technical-library-first-research.md` | 51843 | technical | A pool | ok | KEEP |
| 663 | `2026-08-21-technical-north-star-position.md` | 39714 | technical | B peer | ok | KEEP |
| 664 | `2026-08-21-technical-seat-act0-act1-contract.md` | 5753 | technical | B peer | ok | KEEP |
| 665 | `2026-08-22-codex-562-guard-fix-terra-r10.md` | 2058 | codex | B peer | ok | KEEP |
| 666 | `2026-08-22-codex-562-guard-fix-terra-r11.md` | 2775 | codex | B peer | ok | KEEP |
| 667 | `2026-08-22-codex-562-guard-fix-terra-r12.md` | 1548 | codex | B peer | ok | KEEP |
| 668 | `2026-08-22-codex-562-guard-fix-terra-r2.md` | 3088 | codex | B peer | ok | KEEP |
| 669 | `2026-08-22-codex-562-guard-fix-terra-r3.md` | 3508 | codex | B peer | ok | KEEP |
| 670 | `2026-08-22-codex-562-guard-fix-terra-r4.md` | 4263 | codex | B peer | ok | KEEP |
| 671 | `2026-08-22-codex-562-guard-fix-terra-r5.md` | 3376 | codex | B peer | ok | KEEP |
| 672 | `2026-08-22-codex-562-guard-fix-terra-r6.md` | 3005 | codex | B peer | ok | KEEP |
| 673 | `2026-08-22-codex-562-guard-fix-terra-r7.md` | 2228 | codex | B peer | ok | KEEP |
| 674 | `2026-08-22-codex-562-guard-fix-terra-r8.md` | 2426 | codex | B peer | ok | KEEP |
| 675 | `2026-08-22-codex-562-guard-fix-terra-r9.md` | 1839 | codex | B peer | ok | KEEP |
| 676 | `2026-08-22-codex-562-guard-fix-terra.md` | 4307 | codex | B peer | ok | KEEP |
| 677 | `2026-08-22-codex-562-nopack-sandbox-terra.md` | 4190 | codex | B peer | ok | KEEP |
| 678 | `2026-08-22-codex-563-view-layer-terra.md` | 1874 | codex | B peer | ok | KEEP |
| 679 | `2026-08-22-codex-cloud4v2-registries-terra.md` | 2156 | codex | B peer | ok | KEEP |
| 680 | `2026-08-22-fresh-eyes-cloud-4v2.md` | 28558 | fresh-eyes | B peer | ok | KEEP |
| 681 | `2026-08-22-technical-annotation-and-rulings-ledger.md` | 14612 | technical | A pool | ok | KEEP |
| 682 | `2026-08-22-technical-cloud-1-562-admission-rerun.md` | 35191 | technical | B peer | ok | KEEP |
| 683 | `2026-08-22-technical-cloud-2-563-view-layer.md` | 23240 | technical | B peer | ok | KEEP |
| 684 | `2026-08-22-technical-cloud-3-566-axis-lean.md` | 19511 | technical | B peer | ok | KEEP |
| 685 | `2026-08-22-technical-cloud-wave-close-funnel.md` | 31623 | technical | A pool | ok | KEEP |
| 686 | `2026-08-22-technical-intake-r1-decision-packet.md` | 17864 | technical | A pool | ok | KEEP |
| 687 | `2026-08-22-technical-lane-fix-562-guard.md` | 21079 | technical | B peer | ok | KEEP |
| 688 | `2026-08-23-technical-backlog-adjudication-prep.md` | 305453 | technical | A pool | ok | KEEP |
| 689 | `2026-08-23-technical-funnel-retro-classification.md` | 100553 | technical | B peer | ok | KEEP |
| 690 | `2026-08-23-technical-lane-562-local-admission.md` | 78030 | technical | A pool | ok | KEEP |
| 691 | `2026-08-23-technical-lane-dashboard-commit-path.md` | 77670 | technical | A pool | ok | KEEP |
| 692 | `2026-08-23-technical-lane-dispatch-codification.md` | 43857 | technical | B peer | ok | KEEP |
| 693 | `2026-08-23-technical-lane-docs-actual-state.md` | 45724 | technical | B peer | ok | KEEP |
| 694 | `2026-08-23-technical-lane-docs-governance.md` | 25877 | technical | A pool | ok | KEEP |
| 695 | `2026-08-23-technical-lane-funnel-coverage.md` | 70330 | technical | B peer | ok | KEEP |
| 696 | `2026-08-23-technical-lane-provider-config.md` | 62151 | technical | B peer | ok | KEEP |
| 697 | `2026-08-23-technical-lane-status-grammar.md` | 52482 | technical | B peer | ok | KEEP |
| 698 | `2026-08-23-technical-phase0-preconditions.md` | 79378 | technical | A pool | ok | KEEP |
| 699 | `2026-08-23-technical-research-model-bus.md` | 34104 | technical | B peer | ok | KEEP |
| 700 | `2026-08-23-technical-ruling-provenance-audit.md` | 44450 | technical | A pool | ok | KEEP |
| 701 | `2026-08-23-technical-wave-close-funnel.md` | 11217 | technical | A pool | ok | KEEP |
| 702 | `2026-08-23-technical-window-seal.md` | 14916 | technical | B peer | ok | KEEP |
| 703 | `2026-08-24-technical-batch-close.md` | 18032 | technical | B peer | ok | KEEP |
| 704 | `2026-08-24-technical-discharge-38-ruling-packet.md` | 11477 | technical | A pool | ok | KEEP |
| 705 | `2026-08-24-technical-lane-v1-register-verification.md` | 14491 | technical | B peer | ok | KEEP |
| 706 | `2026-08-24-technical-lane-v3-gates-and-ci.md` | 11470 | technical | B peer | ok | KEEP |
| 707 | `2026-08-24-technical-lane-v4-lifecycle-verification.md` | 9419 | technical | B peer | ok | KEEP |
| 708 | `2026-08-24-technical-lane-v5-register-verification.md` | 10655 | technical | B peer | ok | KEEP |
| 709 | `2026-08-24-technical-probe-substrate.md` | 24127 | technical | B peer | ok | KEEP |
| 710 | `2026-08-24-technical-research-candidate-register.md` | 20190 | technical | B peer | ok | KEEP |
| 711 | `2026-08-24-technical-research-register-addendum.md` | 7774 | technical | B peer | ok | KEEP |
| 712 | `2026-08-24-technical-verify-register-v2.md` | 9210 | technical | B peer | ok | KEEP |
| 713 | `2026-08-24-technical-warn-triage-and-teardown.md` | 5984 | technical | B peer | ok | KEEP |
| 714 | `2026-08-24-verification-integrator-merged-result.md` | 6519 | verification | B peer | ok | KEEP |
| 715 | `2026-08-24-verification-l6-rulings-landing.md` | 7128 | verification | B peer | ok | KEEP |
| 716 | `2026-08-25-technical-batch1-launch-contracts/LANE-CS-codespace-transport.md` | 4419 | (subdir, ungoverned) | E gen | - | KEEP |
| 717 | `2026-08-25-technical-batch1-launch-contracts/LANE-G-governance-spine.md` | 6147 | (subdir, ungoverned) | B peer | - | KEEP |
| 718 | `2026-08-25-technical-batch1-launch-contracts/LANE-RL-registry-filings-v2.md` | 8306 | (subdir, ungoverned) | B peer | - | KEEP |
| 719 | `2026-08-25-technical-batch1-launch-contracts/LANE-RL-registry-filings.md` | 6611 | (subdir, ungoverned) | A pool | - | KEEP |
| 720 | `2026-08-25-technical-batch1-launch-contracts/LANE-X-failloud-sweep.md` | 6051 | (subdir, ungoverned) | B peer | - | KEEP |
| 721 | `2026-08-25-technical-dispatch-brief-to-architect.md` | 12221 | technical | A pool | ok | KEEP |
| 722 | `2026-08-25-technical-dispatch-codespace-build.md` | 34043 | technical | A pool | ok | KEEP |
| 723 | `2026-08-25-technical-dispatch-consolidation-plan.md` | 7469 | technical | A pool | ok | KEEP |
| 724 | `2026-08-25-technical-dispatch-surface-measured.md` | 115882 | technical | A pool | ok | KEEP |
| 725 | `2026-08-25-technical-green-by-skip-sweep.md` | 35544 | technical | A pool | ok | KEEP |
| 726 | `2026-08-25-technical-harvest-v-consolidation.md` | 66436 | technical | A pool | ok | KEEP |
| 727 | `2026-08-25-technical-lane-g-governance-spine.md` | 13672 | technical | B peer | ok | KEEP |
| 728 | `2026-08-25-technical-probe-dsh-report.md` | 8973 | technical | A pool | ok | KEEP |
| 729 | `2026-08-25-technical-probe-providers-report.md` | 8362 | technical | A pool | ok | KEEP |
| 730 | `2026-08-25-technical-register-ruling-packet.md` | 21329 | technical | A pool | ok | KEEP |
| 731 | `2026-08-25-technical-research-agents-md-standard.md` | 21199 | technical | A pool | ok | KEEP |
| 732 | `2026-08-25-technical-research-delivery-telemetry-attribution.md` | 22684 | technical | A pool | ok | KEEP |
| 733 | `2026-08-25-technical-research-operator-dispatch-playbook.md` | 25896 | technical | B peer | ok | KEEP |
| 734 | `2026-08-26-codex-adr115-acceptance-review.md` | 13947 | codex | A pool | ok | KEEP |
| 735 | `2026-08-26-codex-w2a-perf-core.md` | 4988 | codex | B peer | ok | KEEP |
| 736 | `2026-08-26-codex-w2b-surfaces-r2.md` | 4633 | codex | B peer | ok | KEEP |
| 737 | `2026-08-26-codex-w2b-surfaces.md` | 4605 | codex | B peer | ok | KEEP |
| 738 | `2026-08-26-technical-birth-row-bodies-579-586.md` | 27476 | technical | A pool | ok | KEEP |
| 739 | `2026-08-26-technical-handoff-census.md` | 23156 | technical | A pool | ok | KEEP |
| 740 | `2026-08-26-technical-hub-diagnostic.md` | 128782 | technical | A pool | ok | KEEP |
| 741 | `2026-08-26-technical-perf-recon.md` | 20657 | technical | A pool | ok | KEEP |
| 742 | `2026-08-26-technical-provider-surface-repair-summary.md` | 10555 | technical | A pool | ok | KEEP |
| 743 | `2026-08-26-technical-provider-surface-v2.md` | 12203 | technical | A pool | ok | KEEP |
| 744 | `2026-08-26-technical-research-backlog-management.md` | 35528 | technical | A pool | ok | KEEP |
| 745 | `2026-08-26-technical-research-chinese-coding-models.md` | 25162 | technical | A pool | ok | KEEP |
| 746 | `2026-08-26-technical-research-cost-usage-telemetry.md` | 26063 | technical | A pool | ok | KEEP |
| 747 | `2026-08-26-technical-w2a-perf-core.md` | 21734 | technical | B peer | ok | KEEP |
| 748 | `2026-08-26-technical-w2b-surfaces.md` | 18124 | technical | B peer | ok | KEEP |
| 749 | `2026-08-26-technical-w3prep-recon.md` | 16327 | technical | A pool | ok | KEEP |
| 750 | `2026-08-26-verification-batch-1-close-packet.md` | 24317 | verification | A pool | ok | KEEP |
| 751 | `2026-08-27-codex-lane-na-gates.md` | 3716 | codex | B peer | ok | KEEP |
| 752 | `2026-08-27-codex-lane-nb-tiering.md` | 6157 | codex | E gen | ok | KEEP |
| 753 | `2026-08-27-technical-backlog-quality-census.md` | 25156 | technical | A pool | ok | KEEP |
| 754 | `2026-08-27-technical-doc-diet-plan.md` | 22620 | technical | A pool | ok | KEEP |
| 755 | `2026-08-27-technical-journal-rotation-recon.md` | 18019 | technical | A pool | ok | KEEP |
| 756 | `2026-08-27-technical-lane-h-handoff-mech.md` | 15026 | technical | E gen | ok | KEEP |
| 757 | `2026-08-27-technical-lane-na-gates.md` | 13163 | technical | E gen | ok | KEEP |
| 758 | `2026-08-27-technical-lane-nb-tiering-durations.md` | 14025 | technical | B peer | ok | KEEP |
| 759 | `2026-08-27-technical-lane-nb-tiering.md` | 24124 | technical | A pool | ok | KEEP |
| 760 | `2026-08-27-technical-night-harvest-consumption-ledger.md` | 7933 | technical | A pool | ok | KEEP |
| 761 | `2026-08-27-technical-night-harvest-manifest.md` | 3695 | technical | A pool | ok | KEEP |
| 762 | `2026-08-27-technical-python-kodeks-census.md` | 16429 | technical | A pool | ok | KEEP |
| 763 | `2026-08-27-verification-batch-w2-close-packet.md` | 15179 | verification | B peer | ok | KEEP |
| 764 | `2026-08-28-codex-batch1-lane-a-review.md` | 5248 | codex | B peer | ok | KEEP |
| 765 | `2026-08-28-codex-batch1-lane-b-review.md` | 4330 | codex | E gen | ok | KEEP |
| 766 | `2026-08-28-codex-batch1-lane-c-review.md` | 3713 | codex | E gen | ok | KEEP |
| 767 | `2026-08-28-codex-batch1-lane-d-review.md` | 2641 | codex | E gen | ok | KEEP |
| 768 | `2026-08-28-codex-batch1-lane-e-review.md` | 4482 | codex | E gen | ok | KEEP |
| 769 | `2026-08-28-technical-batch-1-manifest.md` | 2900 | technical | B peer | ok | KEEP |
| 770 | `2026-08-28-technical-batch-2-manifest.md` | 13740 | technical | A pool | ok | KEEP |
| 771 | `2026-08-28-technical-batch1-end-of-batch-packet.md` | 21781 | technical | B peer | ok | KEEP |
| 772 | `2026-08-28-technical-batch1-lane-c-fanout-preflights.md` | 8169 | technical | E gen | ok | KEEP |
| 773 | `2026-08-28-technical-batch1-launch-contracts/BATCH1-LANE-CONTRACTS-2026-08-28.md` | 13213 | (subdir, ungoverned) | A pool | - | KEEP |
| 774 | `2026-08-28-technical-batch1-launch-contracts/MANIFEST.md` | 4798 | (subdir, ungoverned) | A pool | - | KEEP |
| 775 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C1-candidate-triage.md` | 4588 | (subdir, ungoverned) | E gen | - | KEEP |
| 776 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C2-slow-marker.md` | 4715 | (subdir, ungoverned) | B peer | - | KEEP |
| 777 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C3-intake61.md` | 5065 | (subdir, ungoverned) | E gen | - | KEEP |
| 778 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C4-codex-census.md` | 4836 | (subdir, ungoverned) | B peer | - | KEEP |
| 779 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-C5-readme-vision.md` | 4932 | (subdir, ungoverned) | B peer | - | KEEP |
| 780 | `2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-FMC-funnel-census.md` | 6948 | (subdir, ungoverned) | B peer | - | KEEP |
| 781 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-A-604-wintooling-deploy.md` | 12225 | (subdir, ungoverned) | E gen | - | KEEP |
| 782 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-B-610-dispatch-verbs.md` | 7656 | (subdir, ungoverned) | A pool | - | KEEP |
| 783 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-C-610-night-protocol.md` | 10290 | (subdir, ungoverned) | B peer | - | KEEP |
| 784 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-D-612-docrot-archival.md` | 10009 | (subdir, ungoverned) | E gen | - | KEEP |
| 785 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-E-605-consumer-root.md` | 9485 | (subdir, ungoverned) | B peer | - | KEEP |
| 786 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-F-577-byte-cap.md` | 10086 | (subdir, ungoverned) | B peer | - | KEEP |
| 787 | `2026-08-28-technical-batch2-launch-contracts/NB2-LANE-G-591-preflight-predicates.md` | 11802 | (subdir, ungoverned) | B peer | - | KEEP |
| 788 | `2026-08-28-technical-closure-harvest-k4.md` | 12059 | technical | A pool | ok | KEEP |
| 789 | `2026-08-28-technical-fm-wave2-frozen-bundle.md` | 9924 | technical | B peer | ok | KEEP |
| 790 | `2026-08-28-technical-nb2-a-packet.md` | 31098 | technical | B peer | ok | KEEP |
| 791 | `2026-08-28-technical-nb2-c-packet.md` | 23750 | technical | B peer | ok | KEEP |
| 792 | `2026-08-28-technical-nb2-d-packet.md` | 27263 | technical | E gen | ok | KEEP |
| 793 | `2026-08-28-technical-nb2-e-packet.md` | 18477 | technical | E gen | ok | KEEP |
| 794 | `2026-08-28-technical-nb2-f-packet.md` | 16726 | technical | E gen | ok | KEEP |
| 795 | `2026-08-28-technical-nb2-g-packet.md` | 25537 | technical | E gen | ok | KEEP |
| 796 | `2026-08-28-technical-night-batch2-frozen-bundle.md` | 15510 | technical | B peer | ok | KEEP |
| 797 | `2026-08-28-technical-night-mission-authorization.md` | 6758 | technical | A pool | ok | KEEP |
| 798 | `2026-08-28-technical-sda1-benchmark-design-adversarial.md` | 35435 | technical | B peer | ok | KEEP |
| 799 | `2026-08-29-census-essentials-consumers.md` | 24867 | census | A pool | ok | KEEP |
| 800 | `2026-08-29-census-nb2-codex-surface.md` | 26763 | census | A pool | ok | KEEP |
| 801 | `2026-08-29-census-nb2-funnel.md` | 32953 | census | A pool | ok | KEEP |
| 802 | `2026-08-29-census-nb2-readme-vision.md` | 46524 | census | A pool | ok | KEEP |
| 803 | `2026-08-29-codex-e2-terra-post-merge-round6-lanes-n-i.md` | 3825 | codex | A pool | ok | KEEP |
| 804 | `2026-08-29-technical-614-consumer-enumeration.md` | 19387 | technical | A pool | ok | KEEP |
| 805 | `2026-08-29-technical-614-lane-b-packet.md` | 17812 | technical | A pool | ok | KEEP |
| 806 | `2026-08-29-technical-aut-r1-autonomous-sdlc-orchestration.md` | 53209 | technical | A pool | ok | KEEP |
| 807 | `2026-08-29-technical-aut-r2-decision-quality-frameworks.md` | 66751 | technical | A pool | ok | KEEP |
| 808 | `2026-08-29-technical-aut-r3-repo-as-reinforcement-environment.md` | 58358 | technical | A pool | ok | KEEP |
| 809 | `2026-08-29-technical-aut-r4-dispatch-record.md` | 6449 | technical | A pool | ok | KEEP |
| 810 | `2026-08-29-technical-aut-r4a-dispatch-brief.md` | 8598 | technical | A pool | ok | KEEP |
| 811 | `2026-08-29-technical-aut-r4a-harness-evals-observability.md` | 78435 | technical | A pool | ok | KEEP |
| 812 | `2026-08-29-technical-aut-r4b-dispatch-brief.md` | 9991 | technical | A pool | ok | KEEP |
| 813 | `2026-08-29-technical-aut-r4b-orchestration-memory-loop.md` | 68573 | technical | A pool | ok | KEEP |
| 814 | `2026-08-29-technical-autonomy-arc-filing-packet.md` | 21379 | technical | A pool | ok | KEEP |
| 815 | `2026-08-29-technical-autonomy-arc-rejected-and-parked.md` | 17559 | technical | A pool | ok | KEEP |
| 816 | `2026-08-29-technical-autonomy-synthesis.md` | 110291 | technical | A pool | ok | KEEP |
| 817 | `2026-08-29-technical-batch-3-manifest.md` | 2812 | technical | E gen | ok | KEEP |
| 818 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-SMOKE6-zg3-entry.md` | 1137 | (subdir, ungoverned) | B peer | - | KEEP |
| 819 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-H-FM1-lifecycle.md` | 9222 | (subdir, ungoverned) | B peer | - | KEEP |
| 820 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-I-FM2-funnel-check.md` | 13007 | (subdir, ungoverned) | B peer | - | KEEP |
| 821 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-J-FM3-shrinkage.md` | 17644 | (subdir, ungoverned) | B peer | - | KEEP |
| 822 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-K-FM4-boot-surface.md` | 8717 | (subdir, ungoverned) | B peer | - | KEEP |
| 823 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-L-FM5-governance-health.md` | 8391 | (subdir, ungoverned) | B peer | - | KEEP |
| 824 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-M-FPG1-file-purpose-graph.md` | 9734 | (subdir, ungoverned) | E gen | - | KEEP |
| 825 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-N-DB1-dashboard.md` | 11434 | (subdir, ungoverned) | B peer | - | KEEP |
| 826 | `2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-O-A4-agy.md` | 12807 | (subdir, ungoverned) | E gen | - | KEEP |
| 827 | `2026-08-29-technical-batchd-a-619-fm-coupling-packet.md` | 18034 | technical | A pool | ok | KEEP |
| 828 | `2026-08-29-technical-batchd-launch-contracts/LANE-a-619-fm-coupling-repair.md` | 5123 | (subdir, ungoverned) | B peer | - | KEEP |
| 829 | `2026-08-29-technical-batchd-launch-contracts/LANE-b-614-vision-to-readme.md` | 5020 | (subdir, ungoverned) | B peer | - | KEEP |
| 830 | `2026-08-29-technical-batchd-launch-contracts/LANE-c-000-claude-md-regenre.md` | 4336 | (subdir, ungoverned) | E gen | - | KEEP |
| 831 | `2026-08-29-technical-batchd-launch-contracts/LANE-d-000-codex-fate.md` | 4605 | (subdir, ungoverned) | B peer | - | KEEP |
| 832 | `2026-08-29-technical-batchd-launch-contracts/LANE-e-000-essentials-census.md` | 5165 | (subdir, ungoverned) | E gen | - | KEEP |
| 833 | `2026-08-29-technical-batchd-launch-contracts/LANE-f-000-adr81-fuzzy-band.md` | 4752 | (subdir, ungoverned) | E gen | - | KEEP |
| 834 | `2026-08-29-technical-batchd-launch-contracts/LANE-g-000-autonomy-synthesis.md` | 6076 | (subdir, ungoverned) | B peer | - | KEEP |
| 835 | `2026-08-29-technical-batchd-launch-contracts/LANE-h-000-codex-universalise.md` | 6227 | (subdir, ungoverned) | E gen | - | KEEP |
| 836 | `2026-08-29-technical-claude-md-regenre.md` | 18980 | technical | A pool | ok | KEEP |
| 837 | `2026-08-29-technical-codex-fate-reference-map.md` | 9138 | technical | B peer | ok | KEEP |
| 838 | `2026-08-29-technical-lane-f-fuzzy-band-design.md` | 15583 | technical | A pool | ok | KEEP |
| 839 | `2026-08-29-technical-nb2-candidate-triage.md` | 25230 | technical | B peer | ok | KEEP |
| 840 | `2026-08-29-technical-nb2-h-packet.md` | 19445 | technical | E gen | ok | KEEP |
| 841 | `2026-08-29-technical-nb2-i-packet.md` | 26612 | technical | E gen | ok | KEEP |
| 842 | `2026-08-29-technical-nb2-intake61-ratification.md` | 42570 | technical | A pool | ok | KEEP |
| 843 | `2026-08-29-technical-nb2-j-packet.md` | 24381 | technical | E gen | ok | KEEP |
| 844 | `2026-08-29-technical-nb2-k-packet.md` | 16972 | technical | A pool | ok | KEEP |
| 845 | `2026-08-29-technical-nb2-l-packet.md` | 25031 | technical | B peer | ok | KEEP |
| 846 | `2026-08-29-technical-nb2-m-packet.md` | 25346 | technical | A pool | ok | KEEP |
| 847 | `2026-08-29-technical-nb2-n-packet.md` | 25690 | technical | A pool | ok | KEEP |
| 848 | `2026-08-29-technical-nb2-o-packet.md` | 26597 | technical | B peer | ok | KEEP |
| 849 | `2026-08-29-technical-nb2-slow-marker-evidence.md` | 36115 | technical | B peer | ok | KEEP |
| 850 | `2026-08-29-technical-nb2-wave-candidate-sweep.md` | 25750 | technical | A pool | ok | KEEP |
| 851 | `2026-08-29-technical-night-harvest-consumption-ledger.md` | 12216 | technical | B peer | ok | KEEP |
| 852 | `2026-08-29-technical-night-harvest-manifest.md` | 7855 | technical | B peer | ok | KEEP |
| 853 | `2026-08-29-technical-pn-two-row-reconcile.md` | 14882 | technical | A pool | ok | KEEP |
| 854 | `2026-08-29-technical-sda1-adversarial-incumbent-baseline.md` | 5044 | technical | A pool | ok | KEEP |
| 855 | `2026-08-29-technical-sda1-analysis-role-freeze.md` | 13500 | technical | B peer | ok | KEEP |
| 856 | `2026-08-29-technical-sda1-analysis-role-item-pack.md` | 10999 | technical | B peer | ok | KEEP |
| 857 | `2026-08-29-technical-thesis-compare-out.md` | 46939 | technical | A pool | ok | KEEP |
| 858 | `2026-08-29-verification-614-p1a-probe-evidence.md` | 6087 | verification | A pool | ok | KEEP |
| 859 | `2026-08-29-verification-night-mission-close-packet.md` | 37482 | verification | A pool | ok | KEEP |
| 860 | `2026-08-29-verification-wave-2-close-packet.md` | 18809 | verification | A pool | ok | KEEP |
| 861 | `2026-08-30-technical-autonomy-decision-tree.md` | 7841 | technical | A pool | ok | KEEP |
| 862 | `2026-08-30-technical-window-close-operator-brief.md` | 6335 | technical | C log | ok | KEEP |
| 863 | `2026-08-31-census-doc-freshness-derivation.md` | 23089 | census | A pool | ok | KEEP |
| 864 | `2026-08-31-census-single-file-folders.md` | 31997 | census | A pool | ok | KEEP |
| 865 | `2026-08-31-census-stale-doctrine-references.md` | 32619 | census | A pool | ok | KEEP |
| 866 | `2026-08-31-census-templates-consumers.md` | 28284 | census | A pool | ok | KEEP |
| 867 | `2026-08-31-technical-agy-admission-and-quota-visibility.md` | 34507 | technical | A pool | ok | KEEP |
| 868 | `2026-08-31-technical-batch-e-manifest.md` | 15277 | technical | A pool | ok | KEEP |
| 869 | `2026-08-31-technical-batche-launch-contracts/CUT.md` | 10197 | (subdir, ungoverned) | A pool | - | KEEP |
| 870 | `2026-08-31-technical-batche-launch-contracts/LANE-a-1-vision-to-readme.md` | 3773 | (subdir, ungoverned) | A pool | - | KEEP |
| 871 | `2026-08-31-technical-batche-launch-contracts/LANE-b-2-essentials-and-claude-md.md` | 6578 | (subdir, ungoverned) | A pool | - | KEEP |
| 872 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a1-single-file-folder-census.md` | 6399 | (subdir, ungoverned) | B peer | - | KEEP |
| 873 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a2-templates-consumer-census.md` | 5805 | (subdir, ungoverned) | B peer | - | KEEP |
| 874 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a3-stale-doctrine-reference-census.md` | 6534 | (subdir, ungoverned) | B peer | - | KEEP |
| 875 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a4-doc-freshness-derivation-audit.md` | 6369 | (subdir, ungoverned) | B peer | - | KEEP |
| 876 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a5-harness-portability-map.md` | 6230 | (subdir, ungoverned) | B peer | - | KEEP |
| 877 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a6-langgraph-class-rejection-record.md` | 6788 | (subdir, ungoverned) | B peer | - | KEEP |
| 878 | `2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a7-agy-admission-and-quota-visibility.md` | 7108 | (subdir, ungoverned) | B peer | - | KEEP |
| 879 | `2026-08-31-technical-batche-launch-contracts/LANE-c-3-root-contract.md` | 2705 | (subdir, ungoverned) | A pool | - | KEEP |
| 880 | `2026-08-31-technical-batche-launch-contracts/LANE-d-4-ai-council-instantiation.md` | 2853 | (subdir, ungoverned) | A pool | - | KEEP |
| 881 | `2026-08-31-technical-batche-launch-contracts/LANE-e-5-eval-sda1-harbor.md` | 2677 | (subdir, ungoverned) | B peer | - | KEEP |
| 882 | `2026-08-31-technical-batche-launch-contracts/LANE-f-6-observability-otel.md` | 2770 | (subdir, ungoverned) | B peer | - | KEEP |
| 883 | `2026-08-31-technical-batche-launch-contracts/LANE-g-7-typed-multi-layer-graph.md` | 3128 | (subdir, ungoverned) | E gen | - | KEEP |
| 884 | `2026-08-31-technical-batche-launch-contracts/LANE-h-8-local-memory-tier-l-evaluation.md` | 4824 | (subdir, ungoverned) | B peer | - | KEEP |
| 885 | `2026-08-31-technical-batche-launch-contracts/LANE-i-9-distiller-filing-amendment.md` | 2667 | (subdir, ungoverned) | E gen | - | KEEP |
| 886 | `2026-08-31-technical-batche-launch-contracts/LANE-j-10-equilibrium-checkpoint-blind-spots.md` | 2688 | (subdir, ungoverned) | E gen | - | KEEP |
| 887 | `2026-08-31-technical-batche-launch-contracts/LANE-k-11-derived-doc-freshness.md` | 3650 | (subdir, ungoverned) | D code | - | KEEP |
| 888 | `2026-08-31-technical-batche-launch-contracts/LANE-l-12-logs-retention-rule.md` | 3107 | (subdir, ungoverned) | E gen | - | KEEP |
| 889 | `2026-08-31-technical-batche-launch-contracts/LANE-m-13-templates-disposition.md` | 3280 | (subdir, ungoverned) | B peer | - | KEEP |
| 890 | `2026-08-31-technical-batche-launch-contracts/LANE-n-14-trends-burndown-and-quota-panel.md` | 3359 | (subdir, ungoverned) | E gen | - | KEEP |
| 891 | `2026-08-31-technical-batche-launch-contracts/LANE-o-15-wintooling-local-default.md` | 3223 | (subdir, ungoverned) | E gen | - | KEEP |
| 892 | `2026-08-31-technical-batche-launch-contracts/PLAN.md` | 29066 | (subdir, ungoverned) | A pool | - | KEEP |
| 893 | `2026-08-31-technical-batche-launch-contracts/PROBE-batch-e-c-codespace-admission.md` | 4243 | (subdir, ungoverned) | A pool | - | KEEP |
| 894 | `2026-08-31-technical-batche-launch-contracts/TIER-B-COPILOT-PAYLOADS.md` | 7960 | (subdir, ungoverned) | A pool | - | KEEP |
| 895 | `2026-08-31-technical-dm1-eval-comparison.md` | 18841 | technical | A pool | ok | KEEP |
| 896 | `2026-08-31-technical-dm2-otel-genai-events.md` | 8201 | technical | A pool | ok | KEEP |
| 897 | `2026-08-31-technical-harness-portability-map.md` | 13486 | technical | A pool | ok | KEEP |
| 898 | `2026-08-31-technical-hy3-disposition.md` | 16890 | technical | A pool | ok | KEEP |
| 899 | `2026-08-31-technical-langgraph-class-rejection-record.md` | 29267 | technical | A pool | ok | KEEP |
| 900 | `2026-08-31-verification-codespace-admission-probe.md` | 6160 | verification | A pool | ok | KEEP |
| 901 | `2026-09-01-census-atlas-r1-def-usage-ledger.html + 2026-09-01-census-atlas-r1-def-usage-ledger.md` | 35451 | census | A pool | - | KEEP |
| 902 | `2026-09-01-technical-629-630-lane-g-packet.md` | 11388 | technical | A pool | ok | KEEP |
| 903 | `2026-09-01-technical-act-one-preserved.md` | 49200 | technical | A pool | ok | KEEP |
| 904 | `2026-09-01-technical-agy-admission-verdict.md` | 28870 | technical | A pool | ok | KEEP |
| 905 | `2026-09-01-technical-article-harness-substrate-brief.md` | 72867 | technical | B peer | ok | KEEP |
| 906 | `2026-09-01-technical-atlas-r1-layer-graph.html + 2026-09-01-technical-atlas-r1-layer-graph.md` | 37585 | technical | A pool | ok | KEEP |
| 907 | `2026-09-01-technical-batch-e-close-packet.md` | 23301 | technical | A pool | ok | KEEP |
| 908 | `2026-09-01-technical-batch-f-manifest.md` | 30132 | technical | A pool | ok | KEEP |
| 909 | `2026-09-01-technical-batchf-derivation.md` | 24368 | technical | A pool | ok | KEEP |
| 910 | `2026-09-01-technical-batchf-launch-contracts/LANE-a-1-codespace-pow-and-router-adr.md` | 6240 | (subdir, ungoverned) | E gen | - | KEEP |
| 911 | `2026-09-01-technical-batchf-launch-contracts/LANE-b-2-handoff-v7.md` | 9799 | (subdir, ungoverned) | B peer | - | KEEP |
| 912 | `2026-09-01-technical-batchf-launch-contracts/LANE-c-3-logs-retention-callers.md` | 4795 | (subdir, ungoverned) | E gen | - | KEEP |
| 913 | `2026-09-01-technical-batchf-launch-contracts/LANE-d-4-deploy-waiver-honoring.md` | 4936 | (subdir, ungoverned) | B peer | - | KEEP |
| 914 | `2026-09-01-technical-batchf-launch-contracts/LANE-e-5-vision-relocation.md` | 8452 | (subdir, ungoverned) | A pool | - | KEEP |
| 915 | `2026-09-01-technical-batchf-launch-contracts/LANE-f-6-agy-admission.md` | 4459 | (subdir, ungoverned) | B peer | - | KEEP |
| 916 | `2026-09-01-technical-batchf-launch-contracts/LANE-g-7-contract-validator-predicates.md` | 5355 | (subdir, ungoverned) | B peer | - | KEEP |
| 917 | `2026-09-01-technical-boot-r1-prioritization-scheduling.md` | 42757 | technical | A pool | ok | KEEP |
| 918 | `2026-09-01-technical-dc3-split.md` | 10814 | technical | A pool | ok | KEEP |
| 919 | `2026-09-01-technical-dm4-local-memory-tier-l-evaluation.md` | 8209 | technical | A pool | ok | KEEP |
| 920 | `2026-09-01-technical-followon-launch-contracts/LANE-w-1-wintooling-canonical-restamp.md` | 6380 | (subdir, ungoverned) | A pool | - | KEEP |
| 921 | `2026-09-01-technical-lane-b-2-handoff-v7-close-packet.md` | 12550 | technical | B peer | ok | KEEP |
| 922 | `2026-09-01-technical-lane-d-4-deploy-waiver-honoring.md` | 6622 | technical | B peer | ok | KEEP |
| 923 | `2026-09-01-technical-night-window-report.md` | 49951 | technical | A pool | ok | KEEP |
| 924 | `2026-09-01-technical-ruff-gate-divergence-classification.md` | 4539 | technical | A pool | ok | KEEP |
| 925 | `2026-09-01-technical-tierb-b1-otel-genai-event-schema.md` | 16505 | technical | A pool | ok | KEEP |
| 926 | `2026-09-01-technical-tierb-b2-sda1-harbor-translation.md` | 15137 | technical | A pool | ok | KEEP |
| 927 | `2026-09-01-technical-universalization-instantiation-prep.md` | 14127 | technical | A pool | ok | KEEP |
| 928 | `2026-09-01-technical-v7-history-delta-equilibrium-map.md` | 13949 | technical | A pool | ok | KEEP |
| 929 | `2026-09-01-verification-atlas-r1-harvest-attempt.md` | 5400 | verification | A pool | ok | KEEP |
| 930 | `2026-09-01-verification-batche-post-merge-terra-round.md` | 6057 | verification | A pool | ok | KEEP |
| 931 | `2026-09-01-verification-batchf-integration-suite.md` | 4699 | verification | A pool | ok | KEEP |
| 932 | `2026-09-01-verification-batchf-terra-tallies.md` | 3259 | verification | B peer | ok | KEEP |
| 933 | `2026-09-01-verification-codespace-admission-report.md` | 4760 | verification | A pool | ok | KEEP |
| 934 | `2026-09-01-verification-codespace-longrun-proof.md` | 19417 | verification | A pool | ok | KEEP |
| 935 | `2026-09-01-verification-model-routing-witness.md` | 5865 | verification | A pool | ok | KEEP |
| 936 | `2026-09-02-technical-batch-f-close-packet.md` | 25639 | technical | A pool | ok | KEEP |
| 937 | `2026-09-02-technical-batch-g-close-packet.md` | 24851 | technical | B peer | ok | KEEP |
| 938 | `2026-09-02-technical-batch-g-manifest.md` | 4051 | technical | B peer | ok | KEEP |
| 939 | `2026-09-02-technical-lane-g-276-deploy-waiver.md` | 10807 | technical | B peer | ok | KEEP |
| 940 | `2026-09-02-technical-lane-g-611-bundle-thinning.md` | 24727 | technical | B peer | ok | KEEP |
| 941 | `2026-09-02-technical-lane-g-614-hygiene-close-packet.md` | 10450 | technical | B peer | ok | KEEP |
| 942 | `2026-09-02-technical-lane-g-621-freshness-absent.md` | 10114 | technical | B peer | ok | KEEP |
| 943 | `2026-09-02-technical-lane-g-626-terra-tally.md` | 2784 | technical | A pool | ok | KEEP |
| 944 | `2026-09-02-technical-lane-g-628-essentials-debless-packet.md` | 9366 | technical | B peer | ok | KEEP |
| 945 | `2026-09-02-verification-base-failed-set-1e064921.json` | 1355 | verification | B peer | - | KEEP |
| 946 | `2026-09-02-verification-parity-b5753f52.md` | 6137 | verification | A pool | ok | KEEP |
| 947 | `2026-09-02-verification-parity-container-set-b5753f52.json` | 1650 | verification | A pool | - | KEEP |
| 948 | `2026-09-03-technical-lane-g-621-c7.md` | 14436 | technical | B peer | ok | KEEP |
| 949 | `2026-09-05-technical-627-readjudication-artifacts/ARM3_NOTE.md` | 3288 | (subdir, ungoverned) | B peer | - | KEEP |
| 950 | `2026-09-05-technical-627-readjudication-artifacts/SEED_RUBRIC.md` | 4315 | (subdir, ungoverned) | B peer | - | KEEP |
| 951 | `2026-09-05-technical-627-readjudication-artifacts/VERDICT_RULE.md` | 3551 | (subdir, ungoverned) | B peer | - | KEEP |
| 952 | `2026-09-05-technical-627-readjudication-artifacts/check_63_65.py` | 2084 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 953 | `2026-09-05-technical-627-readjudication-artifacts/drive.py` | 2956 | (subdir, ungoverned) | A pool | - | RELOCATE |
| 954 | `2026-09-05-technical-627-readjudication-artifacts/drive2.py` | 6267 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 955 | `2026-09-05-technical-627-readjudication-artifacts/extract_prompts.py` | 2434 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 956 | `2026-09-05-technical-627-readjudication-artifacts/recount_n04.py` | 1890 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 957 | `2026-09-05-technical-627-readjudication-artifacts/run_adddir.py` | 2532 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 958 | `2026-09-05-technical-627-readjudication-artifacts/run_agy.py` | 2964 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 959 | `2026-09-05-technical-627-readjudication-artifacts/score_f0.py` | 1469 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 960 | `2026-09-05-technical-627-readjudication-artifacts/seed_corpus.py` | 7223 | (subdir, ungoverned) | B peer | - | RELOCATE |
| 961 | `2026-09-05-technical-627-readjudication.md` | 44163 | technical | A pool | ok | KEEP |
| 962 | `2026-09-05-technical-aj-second-pass-lane-contract.md` | 11009 | technical | A pool | ok | KEEP |
| 963 | `2026-09-05-technical-batch-h0-close-packet.md` | 21435 | technical | B peer | ok | KEEP |
| 964 | `2026-09-05-technical-batch-h0-manifest.md` | 6069 | technical | B peer | ok | KEEP |
| 965 | `2026-09-05-technical-batch-r5p-close-packet.md` | 21325 | technical | B peer | ok | KEEP |
| 966 | `2026-09-05-technical-batch-r5p-launch-contracts/LANE-r-000-bundle-gitlog.md` | 4959 | (subdir, ungoverned) | B peer | - | KEEP |
| 967 | `2026-09-05-technical-batch-r5p-launch-contracts/LANE-r-000-docrot-arm2.md` | 4242 | (subdir, ungoverned) | B peer | - | KEEP |
| 968 | `2026-09-05-technical-batch-r5p-launch-contracts/LANE-r-000-zc-candidates.md` | 5952 | (subdir, ungoverned) | B peer | - | KEEP |
| 969 | `2026-09-05-technical-batch-r5p-manifest.md` | 6301 | technical | B peer | ok | KEEP |
| 970 | `2026-09-05-technical-browser-prose-rule-census.md` | 12415 | technical | A pool | ok | KEEP |
| 971 | `2026-09-05-technical-browser-seat-notes.md` | 48692 | technical | A pool | ok | KEEP |
| 972 | `2026-09-05-technical-claude-md-section-history-ledger.md` | 4667 | technical | A pool | ok | KEEP |
| 973 | `2026-09-05-technical-corpus-coherence-gemini.md` | 16807 | technical | A pool | ok | KEEP |
| 974 | `2026-09-05-technical-fleet-readiness.md` | 91379 | technical | A pool | ok | KEEP |
| 975 | `2026-09-05-technical-funnel-groom-lane-contract.md` | 7757 | technical | A pool | ok | KEEP |
| 976 | `2026-09-05-technical-funnel-groom-sheet.md` | 52773 | technical | A pool | ok | KEEP |
| 977 | `2026-09-05-technical-lane-h0-trace-close.md` | 6203 | technical | A pool | ok | KEEP |
| 978 | `2026-09-05-technical-lane-r-000-zc-candidates.md` | 9921 | technical | C log | ok | KEEP |
| 979 | `2026-09-05-technical-r5-disposition-sheet.md` | 41900 | technical | A pool | ok | KEEP |
| 980 | `2026-09-05-technical-r5-funnel-disposition-ledger.md` | 15761 | technical | A pool | ok | KEEP |
| 981 | `2026-09-05-technical-r5p-lane1-docrot-arm2.md` | 10828 | technical | A pool | ok | KEEP |
| 982 | `2026-09-05-technical-research-aj-second-pass.md` | 33030 | technical | A pool | ok | KEEP |
| 983 | `2026-09-05-technical-research-architekt-jutra-gap-analysis.md` | 45823 | technical | A pool | ok | KEEP |
| 984 | `2026-09-05-technical-research-python-quality-speed.md` | 71947 | technical | A pool | ok | KEEP |
| 985 | `2026-09-05-technical-v150-tag-checklist.md` | 2949 | technical | A pool | ok | KEEP |
| 986 | `2026-09-05-verification-lane-h0-suite-speed.md` | 7339 | verification | B peer | ok | KEEP |
| 987 | `2026-09-05-verification-lane-r-000-bundle-gitlog.md` | 9490 | verification | E gen | ok | KEEP |
| 988 | `2026-09-06-technical-archive-report-stage.md` | 55256 | technical | B peer | ok | KEEP |
| 989 | `2026-09-06-technical-batch-t-close-packet.md` | 44050 | technical | A pool | ok | KEEP |
| 990 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-aj-research.md` | 18825 | (subdir, ungoverned) | D code | - | KEEP |
| 991 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-batch-p-audit-speed.md` | 18397 | (subdir, ungoverned) | D code | - | KEEP |
| 992 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-browser-floor.md` | 15089 | (subdir, ungoverned) | D code | - | KEEP |
| 993 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-nc1-clear.md` | 18784 | (subdir, ungoverned) | D code | - | KEEP |
| 994 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-playbook.md` | 14944 | (subdir, ungoverned) | D code | - | KEEP |
| 995 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-readme.md` | 13709 | (subdir, ungoverned) | D code | - | KEEP |
| 996 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-reds-spine.md` | 14156 | (subdir, ungoverned) | D code | - | KEEP |
| 997 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-shape-seal.md` | 15867 | (subdir, ungoverned) | D code | - | KEEP |
| 998 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-trace-scorecard.md` | 16784 | (subdir, ungoverned) | D code | - | KEEP |
| 999 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-v2-logs.md` | 14371 | (subdir, ungoverned) | D code | - | KEEP |
| 1000 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-v4-archive-report.md` | 17638 | (subdir, ungoverned) | D code | - | KEEP |
| 1001 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-v5-closures.md` | 16902 | (subdir, ungoverned) | D code | - | KEEP |
| 1002 | `2026-09-06-technical-batch-t-launch-contracts/LANE-t-628-v1-release.md` | 16084 | (subdir, ungoverned) | D code | - | KEEP |
| 1003 | `2026-09-06-technical-batch-t-manifest.md` | 20793 | technical | B peer | ok | KEEP |
| 1004 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-adr-carrier-split.md` | 18021 | (subdir, ungoverned) | F none | - | KEEP |
| 1005 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-adr-template-flip-condition.md` | 18082 | (subdir, ungoverned) | F none | - | KEEP |
| 1006 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-batch-p-local.md` | 18586 | (subdir, ungoverned) | F none | - | KEEP |
| 1007 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-batch-protocol-mechanisms.md` | 18544 | (subdir, ungoverned) | F none | - | KEEP |
| 1008 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-branch-enum-parity.md` | 18903 | (subdir, ungoverned) | F none | - | KEEP |
| 1009 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-carrier-floor-v150-mechanisms.md` | 18581 | (subdir, ungoverned) | F none | - | KEEP |
| 1010 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-closures-local.md` | 17808 | (subdir, ungoverned) | F none | - | KEEP |
| 1011 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-deploy-tool-consumer-override.md` | 17963 | (subdir, ungoverned) | F none | - | KEEP |
| 1012 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-derived-copies-registry.md` | 18152 | (subdir, ungoverned) | F none | - | KEEP |
| 1013 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-dispatch-receipt-is-work.md` | 19128 | (subdir, ungoverned) | F none | - | KEEP |
| 1014 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-erratum-aj-second-pass.md` | 18066 | (subdir, ungoverned) | F none | - | KEEP |
| 1015 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-handoff-v71-build.md` | 19093 | (subdir, ungoverned) | F none | - | KEEP |
| 1016 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-intake-id-next-free.md` | 18668 | (subdir, ungoverned) | F none | - | KEEP |
| 1017 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-plugin-version-record-and-drift.md` | 18123 | (subdir, ungoverned) | B peer | - | KEEP |
| 1018 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-prompts-dir-guard.md` | 18630 | (subdir, ungoverned) | F none | - | KEEP |
| 1019 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-seal-report-fleet.md` | 18275 | (subdir, ungoverned) | F none | - | KEEP |
| 1020 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-shape-spec-finalize.md` | 18850 | (subdir, ungoverned) | F none | - | KEEP |
| 1021 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-trace-scorecard-consumer.md` | 18546 | (subdir, ungoverned) | F none | - | KEEP |
| 1022 | `2026-09-06-technical-batch-u-launch-contracts/LANE-u-628-release-commit.md` | 19549 | (subdir, ungoverned) | F none | - | KEEP |
| 1023 | `2026-09-06-technical-batch-u-manifest.md` | 11751 | technical | B peer | ok | KEEP |
| 1024 | `2026-09-06-technical-closure-proposals.md` | 156896 | technical | B peer | ok | KEEP |
| 1025 | `2026-09-06-technical-erratum-aj-second-pass.md` | 18505 | technical | A pool | ok | KEEP |
| 1026 | `2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md` | 53283 | technical | A pool | ok | KEEP |
| 1027 | `2026-09-06-technical-seal-report-corp-monorepo.md` | 18398 | technical | A pool | ok | KEEP |
| 1028 | `2026-09-07-technical-seal-report-fleet.md` | 32235 | technical | C log | ok | KEEP |
