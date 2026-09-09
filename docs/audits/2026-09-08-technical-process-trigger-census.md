# Process-trigger census — what actually fires, and what is only inventory

> **Class:** technical · **Date:** 2026-09-08 · **Batch V REPORT**, not a lane.
> **Commissioned by:** `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md` §4.
> **Consumer:** `docs/audits/2026-09-09-technical-batch-v-close-packet.md` — the orphan list
> below is the retirement-or-wiring list V+1 works from.
> **Posture:** read-only. This census changed no wiring and closed no row.

## Headline

```
population                216 rows
  TRIGGERED               160
  ON-DEMAND-BY-OPERATOR    24
  ORPHAN                   32
```

Per population:

```
A  scripts/ + plugin scripts   139   triggered 115   on-demand  4   orphan 20
B  hooks (L0 ~/.claude)          5   triggered   2   on-demand  0   orphan  3
C  commands + skills            17   triggered   0   on-demand  8   orphan  9
D  organs in audit.ALL_CHECKS   55   triggered  43   on-demand 12   orphan  0
```

**The populations overlap by design and the total is not a count of distinct files.** The 55
organs of population D are *functions* inside modules already counted in A (`audit.py` and
`scripts/audit_checks/*`). §4 names both populations, so both are reported; a distinct-file
count would answer a question nobody asked.

**`.claude/hooks/` does not exist in this repo.** Its git hooks are declared in
`.pre-commit-config.yaml` and its session hooks in `.claude/settings.json`, both pointing into
`scripts/`. Population B is therefore the L0 hook directory `~/.claude/hooks/`, which is where
the only actual hook *files* live.

## Method — what counted as a trigger

Mechanism, not reading. Roots were taken from the seven wiring surfaces that can fire something
without a human deciding in the moment:

```
.pre-commit-config.yaml                     git hooks (pre-commit / commit-msg / pre-push)
.pre-commit-hooks.yaml                      EXPORTED hook ids — fire in a CONSUMER repo
.claude/settings.json                       session hooks (SessionStart / Stop / PreToolUse)
plugins/tier1-lifecycle/hooks/hooks.json    plugin session hook (Stop)
~/.claude/settings.json                     L0 session hooks
scripts/fleet-baseline.task.xml             the ONE live schedule (daily 09:00)
.github/workflows/report-only-wall.yml      CI on `push` — not a schedule
```

From those roots the call graph was closed transitively over `scripts/`, counting an edge
**only** for a real `import`/`from` statement or a string literal naming `<mod>.py` in
executable position — parsed with `ast`, with docstrings excluded. Two earlier passes of this
census were wrong and are recorded here because the errors are instructive:

1. A regex pass counted any *docstring mention* as a call site. `audit.py`'s docstrings name
   nearly every module in the repo, so 133 of 139 scripts came back "triggered". A prose
   mention is the opposite of a trigger.
2. An AST pass keyed modules by bare filename. Seven names collide
   (`cli`, `check`, `generator`, `__init__`, and the three plugin derived copies), so
   `scripts/toc/generator.py` was credited with `scripts/codemap/`'s call site. Keys are now
   package-qualified.

Classification follows the DECLARE, not this seat's judgement:

- **ON-DEMAND-BY-OPERATOR is a closed list of seven** — the five decisions (GO · ratification ·
  tag · destructive acts · seat release) plus deploy and sitting. Anything else that calls
  itself "on-demand" is an **orphan** (§2).
- **A call site inside a lane contract is NOT a trigger.** That is a seat running a script once,
  under a contract that has since been merged and closed — the process never runs it again.
  Every such row below is marked orphan and says so.
- A `tests/` reference is not a trigger. A test proves a module works; nothing schedules it.
- Prose in `ARCHITECTURE.md`, `PLAYBOOK.md` or `organ-index.md` is not a trigger.

## THE ORPHAN LIST — V+1's retirement-or-wiring list (32 rows)

Each row **either gets a trigger or is removed. There is no third state** (§4). The `Trigger`
column states why it is an orphan; the note under a row, where present, is evidence bearing on
*which* of the two dispositions fits — not a third option.

### A · scripts (20)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `scripts/archive_row_body.py` | referenced only by `tests/` — a test is not a trigger | `tests/test_archive_row_body.py:1` |
| `scripts/boundary_headers.py` | named in prose only — documented, never wired | `ARCHITECTURE.md:480` |
| `scripts/boundary_report.py` | called only by untriggered `boundary_headers` | `scripts/boundary_headers.py:58` |
| `scripts/cloud_provisioning.py` | referenced only by `tests/` — a test is not a trigger | `tests/test_cloud_provisioning.py:24` |
| `scripts/cost_usage_telemetry.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-f-6-observability-otel.md:27` |
| `scripts/desired_state_loader.py` | called only by untriggered `desired_state_report` | `scripts/desired_state_report.py:50` |
| `scripts/desired_state_report.py` | named in prose only — documented, never wired | `ARCHITECTURE.md:504` |
| `scripts/export_backlog_view.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-08-25-technical-batch1-launch-contracts/LANE-G-governance-spine.md:61` |
| `scripts/failed_set.py` | called only by untriggered `window_metrics` | `scripts/window_metrics.py:359` |
| `scripts/file_purpose_graph.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-09-01-technical-batchf-launch-contracts/LANE-b-2-handoff-v7.md:90` |
| `scripts/gen_north_star.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-08-31-technical-batche-launch-contracts/CUT.md:40` |
| `scripts/gen_trend_dashboard.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-n-14-trends-burndown-and-quota-panel.md:27` |
| `scripts/logs_retention.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-09-01-technical-batchf-launch-contracts/LANE-c-3-logs-retention-callers.md:39` |
| `scripts/nopack_sandbox.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-09-01-technical-batchf-launch-contracts/LANE-e-5-vision-relocation.md:46` |
| `scripts/probe_child_backlogs.py` | referenced only by `tests/` — a test is not a trigger | `tests/test_probe_child_backlogs.py:1` |
| `scripts/seed_runbook.py` | referenced only by `tests/` — a test is not a trigger | `tests/test_seed_runbook.py:1` |
| `scripts/setup-fleet-scheduler.ps1` | NONE — zero references on any surface | `—` |
| `scripts/trace_writer.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-09-06-technical-batch-t-launch-contracts/LANE-t-000-trace-scorecard.md:47` |
| `scripts/validate_onboarding_rulings.py` | referenced only by `tests/` — a test is not a trigger | `tests/test_onboarding_rulings.py:19` |
| `scripts/window_metrics.py` | call site is a LANE CONTRACT — a seat, not the process | `docs/audits/2026-09-05-technical-batch-r5p-launch-contracts/LANE-r-000-zc-candidates.md:39` |

- **`scripts/export_backlog_view.py`** — ORPHAN **BY DESIGN**: `tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export` ASSERTS nothing reads it ([#563] one-way view layer). Wiring it would RED that test. Disposition is a ruling, not a bug.
- **`scripts/setup-fleet-scheduler.ps1`** — One-shot installer. The task it registers IS live (`Get-ScheduledTask` → `fleet-baseline`, State=Ready), so the *process* is triggered; the installer is not a recurring process and never was.
- **`scripts/file_purpose_graph.py`** — FPG-1. `[#618]`/ADR-118 (Proposed, NOT ratified).
- **`scripts/logs_retention.py`** — The DECLARE §3 names `run_retention()` at 0 callers; this census confirms it at module level too.

**Eleven of these were built by a lane and never wired.** The lane contract is cited as the
*only* call site: `cost_usage_telemetry`, `export_backlog_view`, `file_purpose_graph`,
`gen_north_star`, `gen_trend_dashboard`, `logs_retention`, `nopack_sandbox`, `trace_writer`,
`window_metrics` — plus `failed_set` and `desired_state_loader`, reachable only from an
untriggered module. This is the DECLARE §5 finding in mechanism form: lanes build organs,
and nothing in the process adopts them afterwards.

### B · hooks, L0 (3)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `~/.claude/hooks/block-onedrive.SUPERSEDED-2026-07-07-allowlist-v1.ps1` | SUPERSEDED copy — retired, still on disk | `—` |
| `~/.claude/hooks/block-onedrive.SUPERSEDED-2026-07-08-emptygrant-v2.ps1` | SUPERSEDED copy — retired, still on disk | `—` |
| `~/.claude/hooks/block-onedrive.SUPERSEDED.ps1` | SUPERSEDED copy — retired, still on disk | `—` |

Three `block-onedrive.SUPERSEDED*.ps1` copies sit beside the live guard. They are wired to
nothing; the live `block-onedrive.ps1` is the armed one. Retirement here is a file deletion in
an **exclusion-adjacent** directory and is the operator's call, not a lane's.

### C · commands and skills (9)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `/changelog-review` | PUSH trigger only — a SessionStart sentinel NUDGES it, which is not a trigger | `.claude/commands/changelog-review.md:1` |
| `/override` | RETIRED (ADR-85 amend. §A2) — discharges no gate | `.claude/commands/override.md:1` |
| `/preflight` | its own frontmatter: "wired into no gate" | `.claude/commands/preflight.md:1` |
| `/save` | convenience wrapper — not one of the seven | `.claude/commands/save.md:1` |
| `/codex-review` | operator-invoked review — not one of the seven | `~/.claude/commands/codex-review.md:1` |
| `skill `check-against-spec`` | no event fires a skill; not one of the seven | `.claude/skills/check-against-spec/SKILL.md:1` |
| `skill `verify`` | no event fires a skill; not one of the seven | `.claude/skills/verify/SKILL.md:1` |
| `skill `gotchas`` | no event fires a skill; not one of the seven | `~/.claude/skills/gotchas/gotchas.md:1` |
| `skill `gotchas`` | no event fires a skill; not one of the seven | `~/.claude/skills/gotchas/SKILL.md:1` |

**All three skills are orphans under the DECLARE's own definition, and that is the finding, not
a filing error.** No event fires a skill; a skill is read when a seat chooses to read it.
`gotchas` is *mandated* by `CLAUDE.md` ("Before modifying any file, check …") — which is
precisely the "carried by seats' diligence" that §5 names as the missing spine. A mandate in
prose is not a trigger.

### D · organs (0)

**Zero.** Every member of `audit.ALL_CHECKS` is reached: 43 at commit tier by the `audit-health`
pre-commit hook, 12 at ship tier by `/ship`. The organ registry is the one population in this
repo with no orphans — which is what a registry is for.

## ON-DEMAND-BY-OPERATOR (24 rows)

Legitimate harness *inputs* under §2, each mapped to one of the seven acts.

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `scripts/review_closures.py` | `/review-closures` — ratification | `plugins/tier1-lifecycle/commands/review-closures.md:20` |
| `scripts/worktree_import_proof.py` | `/lane-boot` — GO | `.claude/commands/lane-boot.md:174` |
| `scripts/worktree_seed.py` | `/lane-boot` — GO | `.claude/commands/lane-boot.md:124` |
| `plugins/tier1-lifecycle/scripts/review_closures.py` | `/review-closures` — ratification | `plugins/tier1-lifecycle/commands/review-closures.md:20` |
| `/boot-session` | sitting | `.claude/commands/boot-session.md:1` |
| `/handoff-verify` | seat release | `.claude/commands/handoff-verify.md:1` |
| `/handoff` | seat release | `.claude/commands/handoff.md:1` |
| `/lane-boot` | GO | `.claude/commands/lane-boot.md:1` |
| `/lane-integrate` | GO | `.claude/commands/lane-integrate.md:1` |
| `/session-summary` | seat release | `~/.claude/commands/session-summary.md:1` |
| `/review-closures` | ratification | `plugins/tier1-lifecycle/commands/review-closures.md:1` |
| `/ship` | destructive acts | `plugins/tier1-lifecycle/commands/ship.md:1` |
| `check_generated_artifact_freshness` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_stale_worktrees` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_git_backlog_drift` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_doc_claims` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_doc_structure` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_doc_code_edge` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_undeclared_edges` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_fleet_parity` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_review_artifact_coverage` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_funnel_coverage` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_routing_agreement` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |
| `check_funnel_lifecycle` | `/ship` ship-gate only — destructive acts | `plugins/tier1-lifecycle/commands/ship.md:47` |

**The 12 ship-tier organs are the load-bearing entry here.** `audit.py health` — the per-commit
gate — passes `tier=TIER_COMMIT` and runs 43 of 55 checks; a ship-tier check appears in its
report as an `n/a` naming the deferral. `ship-gate` passes no tier and runs all 55
(`scripts/audit.py:6647`). So those 12 organs have teeth **only** when an operator runs `/ship`.
That is sanctioned — `/ship` is a destructive act — but it means a third of the doc-and-drift
mesh does not fire on any commit.

## TRIGGERED (160 rows) — grouped by what fires them

```
  80  reached by a call site inside a triggered module
  44  git hook `audit-health`
   7  session hook (project)
   1  git hook `block-commit-on-main`
   1  git hook `block-ff-push`
   1  git hook `block-unanchored-push`
   1  git hook `backlog-id-on-close`
   1  git hook `backlog-filing-backpressure`
   1  git hook `derived-copies-rebind`
   1  git hook `provider-registry-agreement`
   1  git hook `check-seal-identity`
   1  git hook `codemap-freshness`
   1  EXPORTED hook `codemap-freshness`
   1  git hook `coherence-nudge`
   1  IS the Routine schedule
   1  CI (`push` to main + workflow_dispatch; NOT a schedule)
   1  git hook `audit-index-freshness`
   1  git hook `claude-rosters-freshness`
   1  git hook `doc-counts-pytest-freshness`
   1  git hook `intake-index-freshness`
   1  git hook `lane-contract-check`
   1  git hook `roster-freshness`
   1  git hook `organ-index-freshness`
   1  git hook `normalize-dated-headers`
   1  package `__init__` (executes when a triggered submodule imports)
   1  git hook `toc-freshness-playbook`
   1  EXPORTED hook `toc-freshness`
   1  git hook `validate-backlog`
   1  git hook `validate-hermetization`
   1  session hook (plugin Stop)
   1  session hook (L0 PreToolUse)
   1  session hook (L0 SessionStart)
```

Full rows, with the wiring line for each:

### A · scripts (115)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `scripts/arm_hooks.py` | session hook (project) | `.claude/settings.json:62` |
| `scripts/assemble_paste.py` | call site in `audit` | `scripts/audit.py:2711` |
| `scripts/audit.py` | git hook `audit-health` [pre-commit] | `.pre-commit-config.yaml:371` |
| `scripts/audit_checks/_common.py` | call site in `registry` | `scripts/audit_checks/registry.py:42` |
| `scripts/audit_checks/check_adr38_baseline.py` | call site in `registry` | `scripts/audit_checks/registry.py:52` |
| `scripts/audit_checks/check_adr_status_grammar.py` | call site in `registry` | `scripts/audit_checks/registry.py:53` |
| `scripts/audit_checks/check_amendment_coherence.py` | call site in `registry` | `scripts/audit_checks/registry.py:54` |
| `scripts/audit_checks/check_boot_byte_budget.py` | call site in `registry` | `scripts/audit_checks/registry.py:60` |
| `scripts/audit_checks/check_canonical_md_visibility.py` | call site in `registry` | `scripts/audit_checks/registry.py:61` |
| `scripts/audit_checks/check_canonical_structure.py` | call site in `registry` | `scripts/audit_checks/registry.py:66` |
| `scripts/audit_checks/check_claude_md.py` | call site in `registry` | `scripts/audit_checks/registry.py:71` |
| `scripts/audit_checks/check_consumer_at_landing.py` | call site in `registry` | `scripts/audit_checks/registry.py:72` |
| `scripts/audit_checks/check_dispatch_drift.py` | call site in `registry` | `scripts/audit_checks/registry.py:73` |
| `scripts/audit_checks/check_dot_prefix_discipline.py` | call site in `registry` | `scripts/audit_checks/registry.py:75` |
| `scripts/audit_checks/check_floor_integrity.py` | call site in `registry` | `scripts/audit_checks/registry.py:80` |
| `scripts/audit_checks/check_handoff_bundle_structure.py` | call site in `registry` | `scripts/audit_checks/registry.py:86` |
| `scripts/audit_checks/check_handoff_version_stamp.py` | call site in `registry` | `scripts/audit_checks/registry.py:92` |
| `scripts/audit_checks/check_proof_layer.py` | call site in `registry` | `scripts/audit_checks/registry.py:97` |
| `scripts/audit_checks/check_reconciled_versions.py` | call site in `registry` | `scripts/audit_checks/registry.py:98` |
| `scripts/audit_checks/check_residual_completeness.py` | call site in `registry` | `scripts/audit_checks/registry.py:99` |
| `scripts/audit_checks/check_routine_consumers.py` | call site in `registry` | `scripts/audit_checks/registry.py:100` |
| `scripts/audit_checks/check_routing_agreement.py` | call site in `registry` | `scripts/audit_checks/registry.py:74` |
| `scripts/audit_checks/check_safe_removal.py` | call site in `registry` | `scripts/audit_checks/registry.py:116` |
| `scripts/audit_checks/check_substrate_declaration.py` | call site in `registry` | `scripts/audit_checks/registry.py:117` |
| `scripts/audit_checks/check_vision_md.py` | call site in `registry` | `scripts/audit_checks/registry.py:118` |
| `scripts/audit_checks/check_workspace_settings.py` | call site in `registry` | `scripts/audit_checks/registry.py:119` |
| `scripts/audit_checks/registry.py` | call site in `audit` | `scripts/audit.py:268` |
| `scripts/backlog_source.py` | call site in `audit` | `scripts/audit.py:4654` |
| `scripts/batch_manifest.py` | call site in `consumer_at_landing` | `scripts/consumer_at_landing.py:363` |
| `scripts/billing_leak_sentinel.ps1` | session hook (project) | `.claude/settings.json:52` |
| `scripts/block_commit_on_main.py` | git hook `block-commit-on-main` [pre-commit] | `.pre-commit-config.yaml:47` |
| `scripts/block_ff_push.py` | git hook `block-ff-push` [pre-push] | `.pre-commit-config.yaml:409` |
| `scripts/block_unanchored_push.py` | git hook `block-unanchored-push` [pre-push] | `.pre-commit-config.yaml:425` |
| `scripts/boot_frontier.py` | call site in `fleet_health` | `scripts/fleet_health.py:1050` |
| `scripts/canonical_docs.py` | call site in `consumer_at_landing` | `scripts/consumer_at_landing.py:91` |
| `scripts/canonical_freshness_gate.py` | call site in `audit` | `scripts/audit.py:227` |
| `scripts/changelog_sentinel.py` | session hook (project) | `.claude/settings.json:57` |
| `scripts/check_backlog_commit_msg.py` | git hook `backlog-id-on-close` [commit-msg] | `.pre-commit-config.yaml:387` |
| `scripts/check_backlog_filing.py` | git hook `backlog-filing-backpressure` [commit-msg] | `.pre-commit-config.yaml:396` |
| `scripts/check_derived_copies.py` | git hook `derived-copies-rebind` [pre-commit] | `.pre-commit-config.yaml:362` |
| `scripts/check_provider_registry.py` | git hook `provider-registry-agreement` [pre-commit] | `.pre-commit-config.yaml:268` |
| `scripts/check_seal_identity.py` | git hook `check-seal-identity` [pre-commit] | `.pre-commit-config.yaml:237` |
| `scripts/codemap/__init__.py` | call site in `ast_walker` | `scripts/codemap/ast_walker.py:26` |
| `scripts/codemap/ast_walker.py` | call site in `generator` | `scripts/codemap/generator.py:11` |
| `scripts/codemap/check.py` | call site in `cli` | `scripts/codemap/cli.py:8` |
| `scripts/codemap/cli.py` | git hook `codemap-freshness` [pre-commit] | `.pre-commit-config.yaml:60` |
| `scripts/codemap/generator.py` | call site in `cli` | `scripts/codemap/cli.py:9` |
| `scripts/codemap/mermaid_emit.py` | call site in `text_emit` | `scripts/codemap/text_emit.py:12` |
| `scripts/codemap/text_emit.py` | call site in `generator` | `scripts/codemap/generator.py:12` |
| `scripts/codemap_hook.py` | EXPORTED hook `codemap-freshness` [pre-commit] — fires in a CONSUMER repo | `.pre-commit-hooks.yaml:26` |
| `scripts/coherence_enumerator.py` | call site in `validate_reconciliation` | `scripts/validate_reconciliation.py:335` |
| `scripts/coherence_nudge.py` | git hook `coherence-nudge` [pre-commit] | `.pre-commit-config.yaml:381` |
| `scripts/consumer_at_landing.py` | call site in `funnel_lifecycle` | `scripts/funnel_lifecycle.py:130` |
| `scripts/dispatch_drift.py` | call site in `check_dispatch_drift` | `scripts/audit_checks/check_dispatch_drift.py:57` |
| `scripts/dispatch_surface.py` | call site in `audit` | `scripts/audit.py:2856` |
| `scripts/enforcement_coverage.py` | call site in `fleet_health` | `scripts/fleet_health.py:407` |
| `scripts/fleet-baseline.task.xml` | IS the Routine schedule — registered live, daily 09:00 (State=Ready) | `scripts/fleet-baseline.task.xml:28` |
| `scripts/fleet_analytics.py` | CI (`push` to main + workflow_dispatch; NOT a schedule) | `.github/workflows/report-only-wall.yml:65` |
| `scripts/fleet_health.py` | session hook (project) | `.claude/settings.json:21` |
| `scripts/fleet_parity.py` | call site in `audit` | `scripts/audit.py:3199` |
| `scripts/funnel_coverage.py` | call site in `consumer_at_landing` | `scripts/consumer_at_landing.py:90` |
| `scripts/funnel_lifecycle.py` | call site in `fleet_health` | `scripts/fleet_health.py:1042` |
| `scripts/gen_audit_index.py` | git hook `audit-index-freshness` [pre-commit] | `.pre-commit-config.yaml:138` |
| `scripts/gen_claude_rosters.py` | git hook `claude-rosters-freshness` [pre-commit] | `.pre-commit-config.yaml:111` |
| `scripts/gen_dashboard.py` | call site in `generated_artifact_freshness` | `scripts/generated_artifact_freshness.py:154` |
| `scripts/gen_doc_counts.py` | git hook `doc-counts-pytest-freshness` [pre-commit] | `.pre-commit-config.yaml:184` |
| `scripts/gen_handoff.py` | call site in `assemble_paste` | `scripts/assemble_paste.py:219` |
| `scripts/gen_intake_index.py` | git hook `intake-index-freshness` [pre-commit] | `.pre-commit-config.yaml:225` |
| `scripts/gen_intake_tree.py` | call site in `audit` | `scripts/audit.py:205` |
| `scripts/gen_lane_contract.py` | git hook `lane-contract-check` [pre-commit] | `.pre-commit-config.yaml:324` |
| `scripts/gen_methodology_roster.py` | git hook `roster-freshness` [pre-commit] | `.pre-commit-config.yaml:93` |
| `scripts/gen_task_tree.py` | call site in `funnel_lifecycle` | `scripts/funnel_lifecycle.py:132` |
| `scripts/generate_floor.py` | call site in `check_floor_integrity` | `scripts/audit_checks/check_floor_integrity.py:22` |
| `scripts/generate_organ_index.py` | git hook `organ-index-freshness` [pre-commit] | `.pre-commit-config.yaml:201` |
| `scripts/generated_artifact_freshness.py` | call site in `audit` | `scripts/audit.py:245` |
| `scripts/gitenv.py` | call site in `fleet_analytics` | `scripts/fleet_analytics.py:112` |
| `scripts/governance_health.py` | call site in `audit` | `scripts/audit.py:135` |
| `scripts/hooks/block_immutable_edits.py` | session hook (project) | `.claude/settings.json:31` |
| `scripts/journal_anchor.py` | call site in `block_unanchored_push` | `scripts/block_unanchored_push.py:83` |
| `scripts/normalize_headers.py` | git hook `normalize-dated-headers` [pre-commit] | `.pre-commit-config.yaml:54` |
| `scripts/preflight_contract.py` | call site in `audit` | `scripts/audit.py:4639` |
| `scripts/proof_layer.py` | call site in `check_proof_layer` | `scripts/audit_checks/check_proof_layer.py:54` |
| `scripts/propose_closures.py` | call site in `validate_git_backlog` | `scripts/validate_git_backlog.py:56` |
| `scripts/provider_registry.py` | call site in `changelog_sentinel` | `scripts/changelog_sentinel.py:39` |
| `scripts/reverse_dep_oracle.py` | call site in `safe_remove` | `scripts/safe_remove.py:53` |
| `scripts/routing_agreement.py` | call site in `check_routing_agreement` | `scripts/audit_checks/check_routing_agreement.py:39` |
| `scripts/safe_remove.py` | call site in `check_safe_removal` | `scripts/audit_checks/check_safe_removal.py:17` |
| `scripts/scan_undeclared_edges.py` | call site in `audit` | `scripts/audit.py:219` |
| `scripts/session_end_backpressure.py` | session hook (project) | `.claude/settings.json:9` |
| `scripts/silent_rule_detector.py` | call site in `audit` | `scripts/audit.py:173` |
| `scripts/single_flight.py` | call site in `gen_dashboard` | `scripts/gen_dashboard.py:822` |
| `scripts/surface_triage.ps1` | session hook (project) | `.claude/settings.json:47` |
| `scripts/telemetry_emit.py` | call site in `block_ff_push` | `scripts/block_ff_push.py:88` |
| `scripts/toc/__init__.py` | package init — `cli` is triggered | `scripts/toc/__init__.py:1` |
| `scripts/toc/check.py` | call site in `cli` | `scripts/toc/cli.py:13` |
| `scripts/toc/cli.py` | git hook `toc-freshness-playbook` [pre-commit] | `.pre-commit-config.yaml:74` |
| `scripts/toc/generator.py` | call site in `cli` | `scripts/toc/cli.py:14` |
| `scripts/toc_hook.py` | EXPORTED hook `toc-freshness` [pre-commit] — fires in a CONSUMER repo | `.pre-commit-hooks.yaml:44` |
| `scripts/validate_adr_status.py` | call site in `funnel_lifecycle` | `scripts/funnel_lifecycle.py:133` |
| `scripts/validate_backlog.py` | git hook `validate-backlog` [pre-commit] | `.pre-commit-config.yaml:249` |
| `scripts/validate_branch_naming.py` | call site in `batch_manifest` | `scripts/batch_manifest.py:134` |
| `scripts/validate_doc_claims.py` | call site in `audit` | `scripts/audit.py:106` |
| `scripts/validate_doc_code_edge.py` | call site in `audit` | `scripts/audit.py:153` |
| `scripts/validate_doc_rot.py` | call site in `audit` | `scripts/audit.py:147` |
| `scripts/validate_doc_structure.py` | call site in `audit` | `scripts/audit.py:159` |
| `scripts/validate_git_backlog.py` | call site in `audit` | `scripts/audit.py:100` |
| `scripts/validate_hermetization.py` | git hook `validate-hermetization` [pre-commit] | `.pre-commit-config.yaml:214` |
| `scripts/validate_landing_predicate.py` | call site in `audit` | `scripts/audit.py:212` |
| `scripts/validate_no_ff.py` | call site in `block_ff_push` | `scripts/block_ff_push.py:78` |
| `scripts/validate_reconciliation.py` | call site in `coherence_nudge` | `scripts/coherence_nudge.py:37` |
| `scripts/validate_residual_completeness.py` | call site in `check_residual_completeness` | `scripts/audit_checks/check_residual_completeness.py:18` |
| `scripts/validate_substrate.py` | call site in `batch_manifest` | `scripts/batch_manifest.py:155` |
| `scripts/verify_handoff_probes.py` | call site in `audit` | `scripts/audit.py:118` |
| `plugins/tier1-lifecycle/scripts/propose_closures.py` | session hook (plugin Stop) | `plugins/tier1-lifecycle/hooks/hooks.json:10` |
| `plugins/tier1-lifecycle/scripts/validate_backlog.py` | call site in `propose_closures` | `plugins/tier1-lifecycle/scripts/propose_closures.py:521` |

### B · hooks, L0 (2)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `~/.claude/hooks/block-onedrive.ps1` | session hook (L0 PreToolUse) | `~/.claude/settings.json:23` |
| `~/.claude/hooks/surface-closures.ps1` | session hook (L0 SessionStart) | `~/.claude/settings.json:34` |

### D · organs, commit tier (43)

| Row | Trigger | Evidence (file:line) |
|---|---|---|
| `check_vision_md` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_adr38_baseline` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_claude_md` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_dot_prefix_discipline` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_canonical_md_visibility` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_workspace_settings` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_handoff_bundle_structure` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_canonical_freshness` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_no_sibling_orphans` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_canonical_structure` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_handoff_version_stamp` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_amendment_coherence` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_floor_integrity` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_hooks_armed` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_no_ff_merges` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_handoff_probes` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_supplement_folded` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_dispatch_verb_agreement` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_reconciled_versions` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_doc_rot` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_safe_removal` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_residual_completeness` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_deployed_methodology_version` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_plugin_version_drift` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_enforcement_coverage` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_doc_code_coverage_drift` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_import_edges` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_routine_consumers` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_silent_rule_ratchet` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_task_tree_coherence` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_intake_tree_coherence` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_boot_byte_budget` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_fleet_audit_replication` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_membership_agreement` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_journal_spine_anchor` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_journal_day_letters` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_preflight_backlog_ids` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_landing_predicate` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_adr_status_grammar` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_substrate_declaration` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_dispatch_drift` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_consumer_at_landing` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |
| `check_proof_layer` | git hook `audit-health` [pre-commit] — commit tier | `.pre-commit-config.yaml:371` |

## Three corrections to DECLARE §3

§3 is explicitly the browser seat's *witness* list, hedged as such. This census is the
mechanism check, and it disagrees in three places.

**1 · `propose_closures` IS event-triggered.** §3 lists it as inventory, "run by a lane, never
by an event". It is wired to the plugin `Stop` hook at
`plugins/tier1-lifecycle/hooks/hooks.json:10`, the plugin is enabled in
`.claude/settings.json`, and this session's own SessionStart banner reported
`[closures] 224 closure(s) proposed`. It fires on every turn-stop. Move it out of inventory.

**2 · There is no nightly Routine in this repo.** §3 lists "nightly Routine (claimed, not
witnessed by me this window): rot detectors, scorecard" — the claim is not substantiated by any
in-repo definition. There is **zero** `cron:` or `schedule:` anywhere in `.github/`,
`ecosystem/` or `scripts/`. The only workflow, `report-only-wall.yml`, triggers on `push` to
main plus `workflow_dispatch`, and its own header declares it "REPORT-ONLY FOREVER". The only
live schedule on this machine is the Task Scheduler entry `fleet-baseline` (daily 09:00,
verified `State=Ready`), and it runs exactly one thing: `scripts/fleet_health.py`. The rot
detectors and scorecard §3 attributes to a nightly Routine are audit organs whose real trigger
is the per-commit `audit-health` hook — or, for 12 of them, `/ship`.

**3 · `codemap_hook.py` / `toc_hook.py` are wired, but not here.** They are entries in
`.pre-commit-hooks.yaml`, the surface this repo *exports* for consumer repos to install. They
fire in a consumer's git hooks and never in the hub. Counted TRIGGERED, with the distinction
stated, because "runs in a consumer" and "runs here" are different facts and the census would
lie either way if it collapsed them.

## Where the evidence stops

- **Reachability is static.** A module imported inside a `try:` or behind a feature flag counts
  as reached. This census proves *wiring*, not execution.
- **Function granularity is out of scope.** A module can be TRIGGERED while a specific entry
  point inside it has no caller — `run_retention()` in `logs_retention.py` is the DECLARE's own
  example. Module-level orphans are complete; function-level ones are not enumerated.
- **The L0 rows are read live from this machine.** `~/.claude` is not in the tree, so these
  three rows are machine-dependent and would differ on another host — the same boundary
  `ecosystem/organ-registry.yaml` documents for the organ index.
- **Two organs named in §3 have no file at all** and so appear in no population: `orphan_census`
  (intake `#86`, DRAFT — the organ does not exist) and the SDA-1 benchmark (designed, never
  built). Absence from this census is not evidence they were retired.
- **`.pre-commit-hooks.yaml` exports two `stages: [manual]` ids** (`codemap-generate`,
  `toc-generate`). Manual stage never fires automatically, in the hub or a consumer.

=== END ===
