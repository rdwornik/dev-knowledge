# Census appendix — full per-file inventory of `scripts/` and `tests/` (2026-09-07)

**Consumer:** `[#397]` (`scripts/` target structure — the closed row whose caller-impact map
this supersedes), `[#493]` (the scheduler pair), `intake #73` (home grammar). The substantive
citation is the main artifact, `docs/audits/2026-09-07-technical-census-scripts-tests.md`;
this file carries only the tables that would push it past the 40 KB lane budget.

**READ-ONLY.** Every verdict is a PROPOSAL for the operator to rule. Nothing here was moved,
edited, renamed or deleted.

Generated mechanically at `21576e3` from `git ls-files` + an AST import graph + a
verbatim-token index over the whole tracked tree. The witness column names WHY a file is
kept; a row with no witness would read `UNDETERMINED` and none does — see the main
artifact's `## Honest limits` for what that does and does not prove.

## A1 · `scripts/` — 135 tracked files

Witness classes, in the order they are tried: `wired:` (named in `.pre-commit-config.yaml`,
`.pre-commit-hooks.yaml`, `.claude/settings.json`, `.github/workflows/`,
`.claude/commands|skills|workflows/`, `plugins/`, `deploy/manifest-v*.yaml`, or
`scripts/audit_checks/registry.py`) · `imported by` (AST edge from a non-test module) ·
`test importer` / `named in N test file(s)` · operator CLI (`if __name__ == "__main__"`) plus
a governance-doc mention · a named OPEN backlog row.

| file | bytes | verdict | witness |
|---|---:|---|---|
| `scripts/archive_row_body.py` | 50106 | KEEP | test importer: test_archive_row_body.py |
| `scripts/arm_hooks.py` | 8156 | KEEP | wired: session-hook, deploy manifest; imported by 2 module(s): carrier_floor.py +1; test importer: test_audit.py +1 |
| `scripts/assemble_paste.py` | 19403 | KEEP | wired: command/skill, deploy manifest; imported by 4 module(s): audit.py +3; test importer: test_audit.py +1 |
| `scripts/audit.py` | 376544 | KEEP | wired: pre-commit, session-hook, CI, command/skill, plugin, deploy manifest; imported by 9 module(s): release_lint.py +8; test importer: test_adr85_integration_enforcement.py +41 |
| `scripts/audit_checks/_common.py` | 4648 | KEEP | wired: audit registry; imported by 23 module(s): check_adr38_baseline.py +22; named in 1 test file(s) |
| `scripts/audit_checks/check_adr38_baseline.py` | 2932 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_adr_status_grammar.py` | 7209 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; test importer: test_validate_adr_status.py |
| `scripts/audit_checks/check_amendment_coherence.py` | 7398 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_boot_byte_budget.py` | 3202 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_canonical_md_visibility.py` | 2794 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; test importer: test_canonical_docs.py |
| `scripts/audit_checks/check_canonical_structure.py` | 3727 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; test importer: test_canonical_docs.py |
| `scripts/audit_checks/check_claude_md.py` | 861 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_consumer_at_landing.py` | 4935 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_dispatch_drift.py` | 5050 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_dot_prefix_discipline.py` | 2361 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_floor_integrity.py` | 4537 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; named in 1 test file(s) |
| `scripts/audit_checks/check_handoff_bundle_structure.py` | 5290 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_handoff_version_stamp.py` | 2804 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_proof_layer.py` | 4781 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_reconciled_versions.py` | 3776 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_residual_completeness.py` | 3239 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_routine_consumers.py` | 10127 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_routing_agreement.py` | 3580 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; test importer: test_routing_agreement.py |
| `scripts/audit_checks/check_safe_removal.py` | 3985 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_substrate_declaration.py` | 11824 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/check_vision_md.py` | 3625 | KEEP | wired: audit registry; imported by 1 module(s): registry.py; test importer: test_canonical_docs.py |
| `scripts/audit_checks/check_workspace_settings.py` | 3543 | KEEP | wired: audit registry; imported by 1 module(s): registry.py |
| `scripts/audit_checks/registry.py` | 12114 | KEEP | wired: pre-commit, audit registry; test importer: test_audit.py +3 |
| `scripts/backlog_source.py` | 7003 | KEEP | imported by 4 module(s): audit.py +3; test importer: test_backlog_source.py +1 |
| `scripts/batch_manifest.py` | 49359 | KEEP | imported by 6 module(s): audit.py +5; test importer: test_adr85_integration_enforcement.py +4 |
| `scripts/billing_leak_sentinel.ps1` | 1219 | KEEP | wired: session-hook; named in 2 test file(s) |
| `scripts/block_commit_on_main.py` | 11599 | KEEP | wired: pre-commit; test importer: test_block_commit_on_main.py +1 |
| `scripts/block_ff_push.py` | 20016 | KEEP | wired: pre-commit, deploy manifest; imported by 1 module(s): block_unanchored_push.py; test importer: test_adr85_integration_enforcement.py +2 |
| `scripts/block_unanchored_push.py` | 11529 | KEEP | wired: pre-commit, CI, command/skill; test importer: test_adr85_integration_enforcement.py +1 |
| `scripts/boot_frontier.py` | 14229 | KEEP | wired: command/skill, deploy manifest; imported by 1 module(s): fleet_health.py; test importer: test_boot_frontier.py |
| `scripts/boundary_headers.py` | 19864 | KEEP | wired: deploy manifest; named in 2 test file(s) |
| `scripts/boundary_report.py` | 15715 | KEEP | imported by 1 module(s): boundary_headers.py; test importer: test_boundary_headers.py |
| `scripts/canonical_docs.py` | 18697 | KEEP | wired: deploy manifest; imported by 13 module(s): audit.py +12; test importer: test_audit.py +3 |
| `scripts/canonical_freshness_gate.py` | 11470 | KEEP | wired: deploy manifest; imported by 2 module(s): release_lint.py +1; test importer: test_canonical_docs.py +2 |
| `scripts/changelog_sentinel.py` | 5155 | KEEP | wired: session-hook, command/skill; test importer: test_provider_registry.py |
| `scripts/check_backlog_commit_msg.py` | 2384 | KEEP | wired: pre-commit, plugin, deploy manifest; named in 3 test file(s) |
| `scripts/check_backlog_filing.py` | 6425 | KEEP | wired: pre-commit; named in 1 test file(s) |
| `scripts/check_provider_registry.py` | 21785 | KEEP | wired: pre-commit; test importer: test_provider_registry.py |
| `scripts/check_seal_identity.py` | 3711 | KEEP | wired: pre-commit; named in 1 test file(s) |
| `scripts/cloud_provisioning.py` | 51815 | KEEP | test importer: test_cloud_provisioning.py |
| `scripts/codemap/__init__.py` | 347 | KEEP | named in 7 test file(s) |
| `scripts/codemap/ast_walker.py` | 2148 | KEEP | imported by 1 module(s): generator.py; test importer: test_codemap.py |
| `scripts/codemap/check.py` | 2012 | KEEP | imported by 2 module(s): __init__.py +1; test importer: test_codemap.py |
| `scripts/codemap/cli.py` | 4554 | KEEP | wired: pre-commit; imported by 1 module(s): codemap_hook.py; named in 5 test file(s) |
| `scripts/codemap/generator.py` | 2895 | KEEP | wired: pre-commit; imported by 3 module(s): __init__.py +2; test importer: test_codemap.py |
| `scripts/codemap/mermaid_emit.py` | 4049 | KEEP | imported by 1 module(s): text_emit.py; test importer: test_codemap.py |
| `scripts/codemap/text_emit.py` | 2372 | KEEP | imported by 1 module(s): generator.py; test importer: test_codemap.py |
| `scripts/codemap_hook.py` | 537 | KEEP | wired: pre-commit |
| `scripts/coherence_enumerator.py` | 16956 | KEEP | wired: command/skill; imported by 1 module(s): scan_undeclared_edges.py; test importer: test_coherence_enumerator.py +1 |
| `scripts/coherence_nudge.py` | 6197 | KEEP | wired: pre-commit; test importer: test_coherence_nudge.py |
| `scripts/consumer_at_landing.py` | 26817 | KEEP | imported by 3 module(s): check_consumer_at_landing.py +2; test importer: test_consumer_at_landing.py +1 |
| `scripts/cost_usage_telemetry.py` | 23284 | KEEP | named in 1 test file(s) |
| `scripts/desired_state_loader.py` | 15977 | KEEP | imported by 1 module(s): desired_state_report.py; test importer: test_desired_state_loader.py +1 |
| `scripts/desired_state_report.py` | 9775 | KEEP | test importer: test_desired_state_report.py |
| `scripts/dispatch_drift.py` | 19825 | KEEP | imported by 1 module(s): check_dispatch_drift.py; test importer: test_dispatch_drift.py |
| `scripts/dispatch_surface.py` | 8585 | KEEP | imported by 2 module(s): audit.py +1; test importer: test_dispatch_surface.py +1 |
| `scripts/enforcement_coverage.py` | 56992 | KEEP | wired: deploy manifest; imported by 5 module(s): carrier_precommit.py +4; test importer: test_enforcement_coverage.py |
| `scripts/export_backlog_view.py` | 23909 | KEEP | test importer: test_export_backlog_view.py |
| `scripts/failed_set.py` | 9490 | KEEP | test importer: test_failed_set.py |
| `scripts/file_purpose_graph.py` | 45647 | KEEP | named in 1 test file(s) |
| `scripts/fleet-baseline.task.xml` | 1708 | KEEP | named by open backlog row [#493] |
| `scripts/fleet_analytics.py` | 56654 | KEEP | wired: CI; test importer: test_gitenv.py |
| `scripts/fleet_health.py` | 71836 | KEEP | wired: session-hook, command/skill, deploy manifest; imported by 2 module(s): fleet_parity.py +1; named in 5 test file(s) |
| `scripts/fleet_parity.py` | 105455 | KEEP | imported by 1 module(s): audit.py; test importer: test_audit.py +3 |
| `scripts/funnel_coverage.py` | 45541 | KEEP | imported by 3 module(s): audit.py +2; test importer: test_funnel_coverage.py +1 |
| `scripts/funnel_lifecycle.py` | 38282 | KEEP | wired: command/skill, deploy manifest; imported by 2 module(s): audit.py +1; test importer: test_funnel_lifecycle.py +1 |
| `scripts/gen_audit_index.py` | 18856 | KEEP | wired: pre-commit, command/skill; imported by 1 module(s): generated_artifact_freshness.py; test importer: test_audit.py +2 |
| `scripts/gen_claude_rosters.py` | 10448 | KEEP | wired: pre-commit; test importer: test_gen_claude_rosters.py |
| `scripts/gen_dashboard.py` | 68575 | KEEP | test importer: test_generated_artifact_freshness.py |
| `scripts/gen_doc_counts.py` | 7688 | KEEP | wired: pre-commit; test importer: test_gen_doc_counts.py |
| `scripts/gen_handoff.py` | 73191 | KEEP | wired: command/skill, deploy manifest; imported by 2 module(s): assemble_paste.py +1; test importer: test_batch_manifest.py +3 |
| `scripts/gen_intake_index.py` | 22375 | KEEP | wired: pre-commit; imported by 2 module(s): funnel_lifecycle.py +1; named in 2 test file(s) |
| `scripts/gen_intake_tree.py` | 29170 | KEEP | imported by 1 module(s): audit.py; named in 2 test file(s) |
| `scripts/gen_lane_contract.py` | 62632 | KEEP | wired: pre-commit; test importer: test_gen_lane_contract.py +1 |
| `scripts/gen_methodology_roster.py` | 8811 | KEEP | wired: pre-commit, deploy manifest; test importer: test_gen_methodology_roster.py |
| `scripts/gen_north_star.py` | 13692 | KEEP | test importer: test_gen_north_star.py |
| `scripts/gen_task_tree.py` | 91125 | KEEP | wired: plugin; imported by 7 module(s): archive_row_body.py +6; test importer: test_archive_row_body.py +4 |
| `scripts/gen_trend_dashboard.py` | 68224 | KEEP | named in 2 test file(s) |
| `scripts/generate_floor.py` | 18933 | KEEP | wired: plugin, deploy manifest; imported by 2 module(s): carrier_floor.py +1; test importer: test_audit.py +1 |
| `scripts/generate_organ_index.py` | 39957 | KEEP | wired: pre-commit; test importer: test_generate_organ_index.py |
| `scripts/generated_artifact_freshness.py` | 35167 | KEEP | imported by 1 module(s): audit.py; test importer: test_audit.py +2 |
| `scripts/gitenv.py` | 6007 | KEEP | imported by 5 module(s): fleet_analytics.py +4; test importer: test_gitenv.py |
| `scripts/governance_health.py` | 33824 | KEEP | imported by 1 module(s): audit.py; test importer: test_gen_handoff.py +1 |
| `scripts/hooks/block_immutable_edits.py` | 8037 | KEEP | wired: session-hook; named in 1 test file(s) |
| `scripts/journal_anchor.py` | 47442 | KEEP | imported by 2 module(s): audit.py +1; test importer: test_adr85_integration_enforcement.py +2 |
| `scripts/logs_retention.py` | 12382 | KEEP | wired: plugin; named in 6 test file(s) |
| `scripts/nopack_sandbox.py` | 113396 | KEEP | test importer: test_nopack_sandbox.py |
| `scripts/normalize_headers.py` | 5976 | KEEP | wired: pre-commit; test importer: test_normalize_headers.py |
| `scripts/preflight_contract.py` | 66443 | KEEP | wired: command/skill; imported by 1 module(s): audit.py; test importer: test_preflight_contract.py +1 |
| `scripts/probe_child_backlogs.py` | 11766 | KEEP | named in 1 test file(s) |
| `scripts/proof_layer.py` | 26696 | KEEP | imported by 1 module(s): check_proof_layer.py; test importer: test_proof_layer.py |
| `scripts/propose_closures.py` | 29764 | KEEP | wired: plugin, deploy manifest; imported by 1 module(s): validate_git_backlog.py; named in 11 test file(s) |
| `scripts/provider_registry.py` | 7905 | KEEP | wired: pre-commit; imported by 2 module(s): changelog_sentinel.py +1; test importer: test_provider_registry.py +1 |
| `scripts/reverse_dep_oracle.py` | 23659 | KEEP | wired: CI; imported by 1 module(s): safe_remove.py; test importer: test_legibility_graph_conformance.py +1 |
| `scripts/review_closures.py` | 10336 | KEEP | wired: plugin, deploy manifest; named in 6 test file(s) |
| `scripts/routing_agreement.py` | 11777 | KEEP | wired: deploy manifest; imported by 1 module(s): check_routing_agreement.py; test importer: test_routing_agreement.py |
| `scripts/safe_remove.py` | 15379 | KEEP | imported by 1 module(s): check_safe_removal.py; test importer: test_safe_remove.py |
| `scripts/scan_undeclared_edges.py` | 15521 | KEEP | imported by 1 module(s): audit.py; test importer: test_legibility_graph_conformance.py +1 |
| `scripts/seed_runbook.py` | 6348 | KEEP | test importer: test_seed_runbook.py |
| `scripts/session_end_backpressure.py` | 28067 | KEEP | wired: session-hook, command/skill, deploy manifest; test importer: test_adr85_integration_enforcement.py +1 |
| `scripts/setup-fleet-scheduler.ps1` | 5934 | KEEP | named by open backlog row [#493] |
| `scripts/silent_rule_detector.py` | 19564 | KEEP | imported by 2 module(s): audit.py +1; test importer: test_preflight_freeze_predicates.py +1 |
| `scripts/single_flight.py` | 49410 | KEEP | wired: command/skill; test importer: test_single_flight.py +1 |
| `scripts/surface_triage.ps1` | 5390 | KEEP | wired: session-hook; named in 3 test file(s) |
| `scripts/telemetry_emit.py` | 36704 | KEEP | imported by 6 module(s): audit.py +5; test importer: test_telemetry_emit.py +2 |
| `scripts/toc/__init__.py` | 431 | KEEP | named in 7 test file(s) |
| `scripts/toc/check.py` | 1620 | KEEP | imported by 2 module(s): __init__.py +1; test importer: test_toc.py |
| `scripts/toc/cli.py` | 2553 | KEEP | wired: pre-commit; imported by 1 module(s): toc_hook.py; named in 5 test file(s) |
| `scripts/toc/generator.py` | 5487 | KEEP | wired: pre-commit; imported by 6 module(s): audit.py +5; test importer: test_toc.py |
| `scripts/toc_hook.py` | 525 | KEEP | wired: pre-commit |
| `scripts/trace_writer.py` | 4823 | KEEP | named in 1 test file(s) |
| `scripts/validate_adr_status.py` | 39381 | KEEP | imported by 2 module(s): check_adr_status_grammar.py +1; test importer: test_validate_adr_status.py |
| `scripts/validate_backlog.py` | 20050 | KEEP | wired: pre-commit, plugin; imported by 1 module(s): file_purpose_graph.py; named in 8 test file(s) |
| `scripts/validate_branch_naming.py` | 17190 | KEEP | wired: command/skill; imported by 3 module(s): batch_manifest.py +2; test importer: test_batch_manifest.py +2 |
| `scripts/validate_doc_claims.py` | 17869 | KEEP | imported by 2 module(s): audit.py +1; test importer: test_doc_counts_commit_tiering.py +2 |
| `scripts/validate_doc_code_edge.py` | 16318 | KEEP | imported by 2 module(s): audit.py +1; test importer: test_legibility_graph_conformance.py |
| `scripts/validate_doc_rot.py` | 31828 | KEEP | imported by 2 module(s): archive_row_body.py +1; test importer: test_canonical_docs.py +1 |
| `scripts/validate_doc_structure.py` | 17329 | KEEP | imported by 1 module(s): audit.py; test importer: test_canonical_docs.py +1 |
| `scripts/validate_git_backlog.py` | 6402 | KEEP | imported by 1 module(s): audit.py; test importer: test_validate_git_backlog.py |
| `scripts/validate_hermetization.py` | 26543 | KEEP | wired: pre-commit, deploy manifest; imported by 1 module(s): batch_manifest.py; test importer: test_canonical_docs.py +2 |
| `scripts/validate_landing_predicate.py` | 7329 | KEEP | imported by 1 module(s): audit.py; test importer: test_validate_landing_predicate.py |
| `scripts/validate_no_ff.py` | 6579 | KEEP | wired: pre-commit, deploy manifest; imported by 2 module(s): audit.py +1; test importer: test_block_ff_push.py +1 |
| `scripts/validate_onboarding_rulings.py` | 5334 | KEEP | test importer: test_onboarding_rulings.py |
| `scripts/validate_reconciliation.py` | 19670 | KEEP | wired: command/skill; imported by 4 module(s): check_reconciled_versions.py +3; test importer: test_coherence_integration.py +4 |
| `scripts/validate_residual_completeness.py` | 9128 | KEEP | imported by 1 module(s): check_residual_completeness.py; test importer: test_gen_handoff.py +1 |
| `scripts/validate_substrate.py` | 42633 | KEEP | imported by 2 module(s): check_substrate_declaration.py +1; test importer: test_batch_manifest.py +1 |
| `scripts/verify_handoff_probes.py` | 47209 | KEEP | wired: command/skill; imported by 1 module(s): audit.py; test importer: test_gen_handoff.py +2 |
| `scripts/window_metrics.py` | 38221 | KEEP | named in 1 test file(s) |
| `scripts/worktree_import_proof.py` | 27681 | KEEP | wired: command/skill; test importer: test_worktree_import_proof.py +1 |
| `scripts/worktree_seed.py` | 18837 | KEEP | wired: command/skill; test importer: test_worktree_seed.py |

## A2 · `tests/` — 160 `test_*.py` files

`how it reaches its subject`: `import` = a bare-name import resolved by the
`pythonpath = [".", "scripts", "deploy"]` substrate; `importlib` = `spec_from_file_location`
against an explicit path; `subprocess` = the script is spawned as a process; `tree-read` = the
test asserts against the live repo tree rather than importing a module.

| test file | bytes | subject module(s) resolved | how it reaches its subject | markers |
|---|---:|---|---|---|
| `tests/test_adr85_integration_enforcement.py` | 38592 | audit, batch_manifest, block_ff_push +3 | import | — |
| `tests/test_agents_md_byte_cap.py` | 11308 | — | tree-read | — |
| `tests/test_archive_row_body.py` | 23797 | archive_row_body, gen_task_tree | import | — |
| `tests/test_assemble_paste.py` | 30331 | — | subprocess | — |
| `tests/test_audit.py` | 165123 | arm_hooks, assemble_paste, audit +10 | import | live_repo |
| `tests/test_audit_index_merge_free.py` | 9741 | gen_audit_index, generated_artifact_freshness, scripts +1 | import | live_repo |
| `tests/test_audit_parallel.py` | 22793 | audit, audit_checks.registry | import | live_repo |
| `tests/test_backlog_source.py` | 3783 | audit, backlog_source | import | — |
| `tests/test_batch_manifest.py` | 51497 | audit, batch_manifest, gen_handoff +3 | import | live_repo |
| `tests/test_block_commit_on_main.py` | 16872 | block_commit_on_main | import | live_repo |
| `tests/test_block_ff_push.py` | 27579 | block_ff_push, validate_no_ff | import | — |
| `tests/test_block_immutable_edits.py` | 7210 | — | subprocess | — |
| `tests/test_boot_frontier.py` | 6692 | boot_frontier, gen_task_tree | import | live_repo |
| `tests/test_boundary_headers.py` | 28781 | boundary_report | import | — |
| `tests/test_boundary_report.py` | 10749 | — | importlib | live_repo |
| `tests/test_canonical_docs.py` | 44599 | audit, audit_checks, audit_checks.check_canonical_md_visibility +9 | import | live_repo |
| `tests/test_canonical_freshness_gate.py` | 9033 | canonical_freshness_gate | import | — |
| `tests/test_carrier_hooks_source.py` | 14597 | carrier_precommit, contract | import | — |
| `tests/test_carrier_precommit.py` | 15542 | carrier_precommit, contract | import | — |
| `tests/test_changelog_sentinel.py` | 3332 | — | importlib | — |
| `tests/test_check_backlog_commit_msg.py` | 1700 | — | importlib | — |
| `tests/test_check_backlog_filing.py` | 4603 | — | importlib | — |
| `tests/test_check_seal_identity.py` | 5844 | — | importlib | — |
| `tests/test_claude_md_byte_cap.py` | 10054 | — | tree-read | — |
| `tests/test_closure_token_quoting.py` | 9616 | — | subprocess | — |
| `tests/test_cloud_provisioning.py` | 65490 | audit, cloud_provisioning | import | — |
| `tests/test_codemap.py` | 16895 | codemap.ast_walker, codemap.check, codemap.generator +2 | import | — |
| `tests/test_codex_instruction_home.py` | 8126 | carrier_globalconfig | import | live_repo |
| `tests/test_coherence_enumerator.py` | 11089 | coherence_enumerator | import | live_repo |
| `tests/test_coherence_integration.py` | 7237 | audit, coherence_enumerator, validate_reconciliation | import | — |
| `tests/test_coherence_nudge.py` | 4533 | coherence_nudge, validate_reconciliation | import | — |
| `tests/test_consumer_at_landing.py` | 13008 | consumer_at_landing | import | live_repo |
| `tests/test_consumer_root_resolution.py` | 20211 | audit, tool | import | — |
| `tests/test_cost_usage_telemetry.py` | 4872 | — | importlib | — |
| `tests/test_deploy_docs.py` | 13977 | carrier_docs, contract, tool | import | — |
| `tests/test_deploy_floor.py` | 46172 | arm_hooks, carrier_floor, contract | import | — |
| `tests/test_deploy_globalconfig.py` | 7525 | carrier_globalconfig, contract | import | — |
| `tests/test_deploy_mesh.py` | 8273 | carrier_mesh, contract, tool | import | — |
| `tests/test_deploy_plugin.py` | 14156 | carrier_plugin, contract | import | — |
| `tests/test_deploy_precommit.py` | 20593 | carrier_precommit, contract | import | — |
| `tests/test_deploy_precommit_surgical.py` | 11128 | carrier_precommit | import | — |
| `tests/test_deploy_prune.py` | 19761 | carrier_precommit, contract, tool | import | — |
| `tests/test_deploy_tool.py` | 7841 | carrier_precommit, contract, tool | import | — |
| `tests/test_deploy_tool_assess.py` | 16921 | carrier_plugin, contract, tool | import | — |
| `tests/test_deploy_tool_execute.py` | 22175 | contract, tool | import | — |
| `tests/test_desired_state_loader.py` | 16762 | ecosystem.schema, scripts, scripts.desired_state_loader | import | live_repo |
| `tests/test_desired_state_report.py` | 12061 | scripts, scripts.desired_state_loader, scripts.desired_state_report | import | live_repo |
| `tests/test_desired_state_schema.py` | 23092 | ecosystem.schema | import | live_repo |
| `tests/test_dispatch_drift.py` | 11274 | dispatch_drift | import | live_repo |
| `tests/test_dispatch_surface.py` | 9664 | audit, dispatch_surface | import | live_repo |
| `tests/test_doc_code_edge.py` | 53576 | audit | import | live_repo |
| `tests/test_doc_counts_commit_tiering.py` | 5266 | validate_doc_claims | import | — |
| `tests/test_e2e_consumer_lifecycle.py` | 12232 | — | subprocess | slow |
| `tests/test_enforcement_coverage.py` | 47466 | audit, contract, enforcement_coverage | import | — |
| `tests/test_essence_spec.py` | 4823 | contract, tool | import | — |
| `tests/test_export_backlog_view.py` | 22932 | export_backlog_view, gen_task_tree | import | live_repo |
| `tests/test_failed_set.py` | 6088 | failed_set | import | — |
| `tests/test_file_purpose_graph.py` | 24929 | — | subprocess | live_repo |
| `tests/test_fleet_analytics.py` | 29714 | — | subprocess | live_repo,slow |
| `tests/test_fleet_audit_replication.py` | 11827 | audit | import | — |
| `tests/test_fleet_health.py` | 77168 | — | subprocess | — |
| `tests/test_fleet_parity.py` | 85901 | audit, fleet_parity | import | live_repo |
| `tests/test_fleet_parity_events.py` | 9779 | fleet_parity | import | — |
| `tests/test_fleet_shape_spec.py` | 16155 | scripts, scripts.canonical_docs, validate_hermetization | import | — |
| `tests/test_floor_conformance.py` | 17373 | carrier_floor, carrier_precommit, floor_conformance | import | — |
| `tests/test_floor_mechanisms.py` | 14902 | floor_mechanisms | import | — |
| `tests/test_funnel_coverage.py` | 53704 | audit, funnel_coverage | import | — |
| `tests/test_funnel_lifecycle.py` | 36448 | audit, audit_checks.registry, funnel_lifecycle | import | — |
| `tests/test_gen_audit_index.py` | 16967 | gen_audit_index | import | — |
| `tests/test_gen_claude_rosters.py` | 5309 | gen_claude_rosters | import | — |
| `tests/test_gen_dashboard.py` | 40038 | — | subprocess | — |
| `tests/test_gen_doc_counts.py` | 2980 | gen_doc_counts, validate_doc_claims | import | — |
| `tests/test_gen_handoff.py` | 73908 | audit_checks.registry, dispatch_surface, funnel_lifecycle +4 | import | live_repo |
| `tests/test_gen_intake_index.py` | 17776 | canonical_freshness_gate | import | — |
| `tests/test_gen_intake_tree.py` | 20395 | audit | import | — |
| `tests/test_gen_lane_contract.py` | 45372 | batch_manifest, gen_lane_contract, validate_branch_naming | import | — |
| `tests/test_gen_methodology_roster.py` | 7120 | gen_methodology_roster | import | — |
| `tests/test_gen_north_star.py` | 4627 | gen_north_star | import | — |
| `tests/test_gen_task_tree.py` | 70621 | gen_task_tree | import | — |
| `tests/test_gen_trend_dashboard.py` | 16857 | — | importlib | — |
| `tests/test_generate_floor.py` | 13262 | generate_floor | import | — |
| `tests/test_generate_organ_index.py` | 24647 | generate_organ_index | import | live_repo |
| `tests/test_generated_artifact_freshness.py` | 22786 | gen_dashboard, generated_artifact_freshness | import | — |
| `tests/test_generator_newlines.py` | 8480 | — | importlib | — |
| `tests/test_gitenv.py` | 14835 | audit, batch_manifest, fleet_analytics +4 | import | — |
| `tests/test_glob_relocated_proposals.py` | 4743 | — | importlib | — |
| `tests/test_governance_health.py` | 22968 | audit, governance_health, scripts.audit +1 | import | live_repo,slow |
| `tests/test_green_by_skip_sweep.py` | 5557 | audit | import | live_repo |
| `tests/test_handoff_modes.py` | 6171 | — | tree-read | live_repo |
| `tests/test_hook_telemetry.py` | 15986 | block_commit_on_main, block_ff_push, block_unanchored_push | import | slow |
| `tests/test_hub_identity.py` | 6174 | audit | import | — |
| `tests/test_journal_anchor.py` | 52940 | journal_anchor | import | — |
| `tests/test_legibility_graph_conformance.py` | 16601 | audit, reverse_dep_oracle, scan_undeclared_edges +2 | import | — |
| `tests/test_lived_sandbox.py` | 7738 | floor_conformance, lived_sandbox | import | — |
| `tests/test_lived_sandbox_consumer.py` | 20573 | lived_sandbox | import | — |
| `tests/test_lived_sandbox_observer.py` | 46412 | lived_sandbox | import | — |
| `tests/test_logs_retention.py` | 14290 | — | importlib | — |
| `tests/test_manifest_link_route.py` | 14799 | batch_manifest, consumer_at_landing, funnel_coverage +1 | import | — |
| `tests/test_membership_agreement.py` | 19662 | audit | import | live_repo |
| `tests/test_merge_serialization.py` | 5567 | — | subprocess | — |
| `tests/test_nopack_sandbox.py` | 68508 | nopack_sandbox | import | — |
| `tests/test_normalize_headers.py` | 21204 | normalize_headers | import | live_repo |
| `tests/test_onboarding_rulings.py` | 5652 | validate_onboarding_rulings | import | — |
| `tests/test_preflight_contract.py` | 32109 | preflight_contract | import | live_repo |
| `tests/test_preflight_freeze_predicates.py` | 29461 | preflight_contract, silent_rule_detector | import | — |
| `tests/test_probe_child_backlogs.py` | 10658 | — | importlib | — |
| `tests/test_proof_layer.py` | 12679 | proof_layer | import | live_repo,slow |
| `tests/test_propose_closures.py` | 16641 | — | subprocess | — |
| `tests/test_propose_closures_bucket_write.py` | 9500 | — | importlib | — |
| `tests/test_propose_closures_detector_error.py` | 9713 | — | importlib | — |
| `tests/test_propose_closures_twin_parity.py` | 3746 | — | importlib | — |
| `tests/test_provider_registry.py` | 21430 | changelog_sentinel, check_provider_registry, provider_registry | import | live_repo |
| `tests/test_provider_registry_schema.py` | 15811 | ecosystem.schema, scripts, scripts.provider_registry | import | live_repo |
| `tests/test_release_lint.py` | 16231 | canonical_docs, release_lint | import | — |
| `tests/test_report_only_wall.py` | 6454 | — | tree-read | — |
| `tests/test_residual_completeness.py` | 10857 | audit, validate_residual_completeness | import | — |
| `tests/test_reverse_dep_oracle.py` | 10201 | — | importlib | — |
| `tests/test_review_artifact_coverage.py` | 29129 | audit | import | live_repo |
| `tests/test_review_closures.py` | 9990 | — | subprocess | — |
| `tests/test_routing_agreement.py` | 7866 | audit_checks.check_routing_agreement, routing_agreement | import | — |
| `tests/test_safe_remove.py` | 11452 | audit, reverse_dep_oracle, safe_remove | import | — |
| `tests/test_scan_undeclared_edges.py` | 15237 | scan_undeclared_edges, validate_reconciliation | import | — |
| `tests/test_seed_runbook.py` | 4215 | seed_runbook | import | — |
| `tests/test_session_end_backpressure.py` | 41247 | — | subprocess | — |
| `tests/test_ship_gate.py` | 11955 | audit | import | — |
| `tests/test_silent_rule_ratchet.py` | 31264 | audit, scripts.silent_rule_detector, silent_rule_detector | import | live_repo |
| `tests/test_single_flight.py` | 18908 | single_flight | import | — |
| `tests/test_single_flight_races.py` | 29678 | single_flight | import | — |
| `tests/test_skip_is_not_pass.py` | 3861 | audit | import | — |
| `tests/test_stale_worktrees.py` | 22043 | audit | import | live_repo |
| `tests/test_supplement_folded.py` | 13111 | audit | import | live_repo |
| `tests/test_surface_triage.py` | 3791 | — | subprocess | — |
| `tests/test_task_tree_gate.py` | 17988 | audit, gen_task_tree | import | live_repo |
| `tests/test_telemetry_emit.py` | 22921 | telemetry_emit | import | slow |
| `tests/test_telemetry_run_id.py` | 16166 | telemetry_emit | import | — |
| `tests/test_telemetry_wiring.py` | 19234 | audit, telemetry_emit | import | slow |
| `tests/test_toc.py` | 14589 | toc.check, toc.generator | import | live_repo |
| `tests/test_trace_writer.py` | 4750 | — | importlib | — |
| `tests/test_trend_dashboard.py` | 30816 | — | importlib | — |
| `tests/test_undeclared_edges_leg.py` | 5449 | audit | import | — |
| `tests/test_v6_frozen_contract.py` | 15220 | assemble_paste, gen_handoff, verify_handoff_probes | import | — |
| `tests/test_validate_adr_status.py` | 45945 | audit_checks.check_adr_status_grammar, validate_adr_status | import | — |
| `tests/test_validate_backlog.py` | 17310 | — | importlib | live_repo |
| `tests/test_validate_backlog_twin_parity.py` | 6899 | — | importlib | — |
| `tests/test_validate_branch_naming.py` | 14713 | validate_branch_naming | import | live_repo |
| `tests/test_validate_doc_claims.py` | 26007 | audit, validate_doc_claims | import | live_repo |
| `tests/test_validate_doc_rot.py` | 41318 | audit, backlog_source, validate_doc_rot | import | live_repo |
| `tests/test_validate_doc_structure.py` | 14552 | audit, validate_doc_structure | import | live_repo |
| `tests/test_validate_git_backlog.py` | 10723 | audit, validate_git_backlog | import | — |
| `tests/test_validate_hermetization.py` | 19563 | — | subprocess | live_repo |
| `tests/test_validate_landing_predicate.py` | 6725 | validate_landing_predicate | import | live_repo |
| `tests/test_validate_no_ff.py` | 9583 | audit, validate_no_ff | import | — |
| `tests/test_validate_reconciliation.py` | 11421 | audit, validate_reconciliation | import | — |
| `tests/test_validate_substrate.py` | 34931 | audit_checks, gen_lane_contract, validate_substrate | import | — |
| `tests/test_verify_handoff_probes.py` | 93673 | audit, verify_handoff_probes | import | live_repo,slow |
| `tests/test_verify_skill.py` | 5925 | — | subprocess | — |
| `tests/test_window_metrics.py` | 22717 | — | importlib | live_repo |
| `tests/test_worktree_import_proof.py` | 19651 | worktree_import_proof | import | — |
| `tests/test_worktree_seed.py` | 15128 | worktree_import_proof, worktree_seed | import | — |
| `tests/test_writer_integrity.py` | 26354 | audit | import | live_repo |

## A3 · `tests/fixtures/` — 63 tracked files in 13 directories

Not tabulated per-file. Every one of the 13 fixture directories is named by at least one
`test_*.py`, verified by `grep -rl <name> tests/*.py`:

| fixture | named by |
|---|---|
| `codemap-arch-clean` | `tests/test_codemap.py` |
| `codemap-arch-drift` | `tests/test_codemap.py` |
| `codemap-arch-nomarkers` | `tests/test_codemap.py` |
| `codemap-simple-repo` | `tests/test_codemap.py` |
| `codemap-with-cycle` | `tests/test_codemap.py` |
| `codemap-with-orphan` | `tests/test_codemap.py` |
| `codemap-with-tach` | `tests/test_codemap.py` |
| `doc-code-edge` | `tests/test_doc_code_edge.py`, `tests/test_file_purpose_graph.py`, `tests/test_legibility_graph_conformance.py` |
| `doc-code-structural` | `tests/test_doc_code_edge.py` |
| `lived-workflow` | `tests/test_lived_sandbox.py`, `tests/test_lived_sandbox_observer.py` |
| `manifest-v1.1.0-pre-essence.yaml` | `tests/test_essence_spec.py` |
| `repo-with-structural-checks` | `tests/test_audit.py`, `tests/test_canonical_docs.py`, `tests/test_probe_child_backlogs.py` |
| `README.md` (the fixtures index) | the directory's own front door; not a fixture |

Verdict for the whole directory: **KEEP**.
