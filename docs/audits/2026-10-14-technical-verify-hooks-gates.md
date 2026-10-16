# Archive copy of transport file DIGEST-VERIFY-hooks-gates-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-VERIFY-hooks-gates-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] c85c77032f5c2a4b. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
by: lane-nv-929-b-ci-gates (Sonnet 5.5), V7 hooks and gates, base b46836c8

Method: `pre-commit run <id> --all-files` (plus `--hook-stage manual`); settings hooks fed a stdin payload file. Tree clean after each batch. Caveat: --all-files on a clean tree. 12 ids are armed; the rest are `stages: [manual]`.

| element | class | witness | caller |
|---|---|---|---|
| 12 armed pre-commit ids (block-commit-on-main, codemap, roster, claude-rosters, audit-index, organ-index, quality-requirements, hermetization, intake-index, row-archive-proof, provider-registry, impacted-tests-guard) | WORKS | each "Passed", 11-24 s | pre-commit |
| 3 commit-msg ids | WORKS | `bad message` -> "no Conventional Commits type prefix"; `chore: probe` Passed | commit-msg |
| block-ff-push, block-unanchored-push | UNRUN | empty stdin rc=0; no ref given, refusal path not exercised | pre-push |
| manual: toc, audit-title, validate-backlog, prepend-order, derived-copies, coherence-nudge, doc-counts, graph-task-coverage/process-list/edge-class | WORKS | each "Passed" | CI conductor |
| graph-orphan-census | BROKEN | `REFUSED -- 15 finding(s)`, e.g. scripts/system_map.py "reached by no wiring surface" | manual; CI commit-gate |
| check-seal-identity | BROKEN | "SEAL-IDENTITY FAIL: refusing to seal docs\handoffs\2026-08-01-dev-knowledge-architect-2: slug mismatch" | manual |
| lane-contract-check | BROKEN | archived v-000, t-000, z-4 contracts: "no Kind line found" | manual |
| decision-coverage | BROKEN | "REFUSED -- 1 decision(s)": to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99 has no OPEN row | manual |
| audit-health | BROKEN | rc=1, "health: DEGRADED"; `handoff_probes: BD-manifest ... 5 file(s) differ` | manual; CI |
| graph-rebuild, normalize-dated-headers | UNRUN | they write; a gate must not | manual |
| ruff pre-commit id | DUPLICATE | manual; the CI `ruff` job does the same. AGENTS.md calls it a pre-commit gate (PREMISE-FAILED) | manual |
| PreToolUse scope_guard | WORKS | Read payload rc=0 | settings.json |
| PreToolUse reuse_gate | WORKS | "allow scripts/zz_probe.py -- no active lane contract for lane-nv-929-b-ci-gates (allow-and-log)": does not see prompt-dir lane contracts; not in CLAUDE.md §9 | settings.json |
| SessionStart session_start | WORKS | rc=0; side effect: starts a detached fleet_health producer | settings.json |
| Stop session_end_backpressure, lane_end_guard | WORKS | Stop payload rc=0 each | settings.json |
| Stop lane_handback_gate | WORKS | rc=0; not in CLAUDE.md §9 | settings.json |
| scripts/read_gate.py | DEAD | library, no CLI; harness.yaml:152 `manual_until: 2026-10-19`; no hook names it | none wired |
| required-tools | WORKS | `required-tools NOT_RUN: contract declares no required tools` | lane close-out |
| [hook-rate] declarations | BROKEN | 9 hooks DECLARED BROKEN, all "Disabled: NO"; propose_closures 49% bypassed | SessionStart |

OPERATOR-ACTION: decide whether the 9 DECLARED BROKEN hooks keep running.
DECIDED-BY-LANE: stdin payloads as files (guard refuses pipes); script reading, not agy.

CHECKER
vendor: OpenAI Codex CLI, served model gpt-5.6-terra (log header), stdin closed, session 01a13c5b; draft sha256 BC185EBB...DF44. Its rows verbatim; DISAGREE stands beside mine.

graph-orphan-census | AGREE | `.venv\Scripts\python.exe scripts\graph_queries.py orphan-census` → `REFUSED -- 15 finding(s)`.
check-seal-identity | DISAGREE | `.venv\Scripts\python.exe scripts\check_seal_identity.py` → exit `0` on the current unstaged tree; digest’s committed-bundle failure was not reproduced.
lane-contract-check | UNRUN | configured command is `scripts/gen_lane_contract.py check`; direct execution was not completed before timeout.
decision-coverage | UNRUN | `.venv\Scripts\python.exe scripts\decision_coverage.py check` exceeded the 30-second sandbox run.
audit-health | UNRUN | `.venv\Scripts\python.exe scripts\audit.py health --parallel` did not return within the sandboxed run.
graph-rebuild, normalize-dated-headers | UNRUN | skipped: both are documented write-capable maintenance commands.
ruff (pre-commit id) | AGREE | `.pre-commit-config.yaml` → `id: ruff`, `stages: [manual]`; static configuration supports duplicate/manual classification.
settings PreToolUse scope_guard | AGREE | `Select-String .claude/settings.json 'scope_guard'` → wired through `scripts/hooks/hook_launcher.py`.
settings PreToolUse reuse_gate | AGREE | `Select-String .claude/settings.json 'reuse_gate'` → matcher `Write|Edit|MultiEdit|NotebookEdit`.
settings SessionStart session_start | AGREE | `Select-String .claude/settings.json 'session_start'` → SessionStart command is wired.
settings Stop session_end_backpressure | AGREE | `Select-String .claude/settings.json 'session_end_backpressure'` → Stop command is wired.
settings Stop lane_end_guard | AGREE | `Select-String .claude/settings.json 'lane_end_guard'` → Stop command is wired.
settings Stop lane_handback_gate | AGREE | `Select-String .claude/settings.json 'lane_handback_gate'` → Stop command is wired.
scripts/read_gate.py | AGREE | `rg -n 'read_gate' .claude .pre-commit-config.yaml ecosystem scripts` → only harness/manual record and source references; no hook wiring.
SessionStart [hook-rate] declarations | AGREE | `rg -n 'DECLARED BROKEN|hook-rate' scripts .claude` → bounded-hook emits `DECLARED BROKEN`; settings retains individually-disabled hook declarations.

USAGE
Claude: lane_cost not run; agy 0; Copilot substitutions 0; Codex 1 call (79k tokens).
