# Archive copy of transport file DIGEST-HOW-WORK-RUNS-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-HOW-WORK-RUNS-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 11af8404bd4e5f1a. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
supersedes: none
summary: Part A of BATCH-GREEN-MAIN-PILOT-2026-10-14. The harness cannot start a multi-stage lane by itself: 15 GAPs between task and launch, 5 HARNESS steps. Census: 20 skills/commands, 19 KEEP, 1 REMOVE (/spine). D8 transport index PARTIAL (stale since 10-10), heads 38/40, janitor --apply never ran. System map 88f1bc52: 21 DEAD (18 manual hooks, 3 disarmed), 11 UNEXPLAINED.
by: CC session ab339d52 (Claude Code 2.1.299 bg job; served claude-opus-5-5[1m], orchestrating per R104). Read-only subagents: Haiku x3 (A2, A3, A4).

# DIGEST — how work runs (2026-10-14)

## GAP list (A1: Part B started through the harness, step by step)
- G1 dispatch map: `gen_handoff.py --dispatch-map --write` does not exist on main. Built in 2a2c3e67 on `worktree-lane-bw-1450-boot-teaching` (19 commits, never merged; BW closed without it). MAP-DISPATCH.md (10-10) used as-is.
- G2 task->contract: `gen_lane_contract.py distill --subject green-main` refuses: "no single BUILD-LIST row matches". A repair task has no contract path.
- G3 contract shape: distill emits ONE model and ONE `claude --bg` session per lane (e.g. `opus execute`). No multi-stage, multi-vendor chain; the 9 stages were orchestrated by hand.
- G4 roles: `provider_router.py route test|qa|judge` -> "role not in the registry". Only plan, implement, review, verify, read, orchestrate exist.
- G5 implement order: router gives anthropic first, copilot second; R104 puts Copilot first (registry mismatch, Phase 0 E5).
- G6 review model: router/registry head is `gpt-6-astra`; the order named Codex terra (`gpt-5.6-terra`, `~/.codex/config.toml` default). Ran terra.
- G7 reviewer B: xai is `requires_admission` and not admitted; the harness would route Sonnet. Gemini has no route. Ran grok-4.7 as ordered.
- G8 launch vendor: `dispatch.py launch` admits `claude|codex` heads (its --help); Copilot stages were launched by hand.
- G9 worktree: no harness verb provisions a lane worktree except `claude --bg --worktree` (one session). Used EnterWorktree (seeds state.yaml).
- G10 lane name: `lane_boot.py preflight --lane green-main-2026-10-14` -> "does not match lane-<batch>-<id>-<slug>". The order's name and the harness grammar disagree; preflight also needs an open batch and an id.
- G11 row filing: `task_record.py new` writes scratch JSON only and refuses `tasks/` (ADR-122 step 1). No verb files a row; ids are allocated by hand (23 rows filed this way).
- G12 cloud: `dispatch.py plan --substrate` admits `local|codespace`; MAP-DISPATCH lists cloud DECLARED, no start verb. The harness cannot launch cloud.
- G13 stage verdicts: no schema or verb for per-stage verdicts or isolation; lane_report schema covers one lane.
- G14 a phase has no heartbeat and no timeout: stage 3 (Copilot) ran 29 min then exited -1, relaunched and was cut by a hand-written 45-min watchdog. For [#689]'s phase table.
- G15 moment:merge stops on a lane with no contract: `merge/merge_receipt.models needs contract and it is unset`.
- HARNESS: `dispatch.py plan` local (full `claude --bg` argv) and codespace (create, ship, run, harvest, manifest-gated delete) given a contract; `merge_path.py land` (integration branch, CI, same sha to main); `consumer_at_landing.py --write-baseline`; `gen_task_tree.py --emit-source`/`--check`.

## A2 — skills and commands (30-day use since 2026-09-14; witness = transcript hit)
- repo cmd: boot-session none KEEP; changelog-review 09-23 KEEP; decide 09-30 KEEP; handoff 10-02 KEEP; handoff-verify 09-28 KEEP; lane-boot 10-05 KEEP; lane-integrate none KEEP (docstring callers); map 10-14 KEEP; preflight none KEEP (AGENTS.md); save none KEEP; spine none, no caller -> REMOVE (unused); why none KEEP (weak: reuse_gate names it).
- repo skill: aj-scan none KEEP; check-against-spec none KEEP (CLAUDE.md §4); verify none KEEP (CLAUDE.md §8).
- plugin: review-closures 09-24 KEEP; ship none KEEP.
- user: codex-review 09-30 KEEP; session-summary none KEEP; gotchas 09-26 KEEP.
- Totals: 20 entries, 19 KEEP, 1 REMOVE. Nothing deleted; removal is the operator's GO.

## A3 — Drive naming
- D8 (RATIFICATION-2026-10-12:61): `to-browser/INDEX.md` + `transport.py query`. Index PARTIAL: built 10-10 22:55, not refreshed; 84 newer files absent. Heads PARTIAL: 38/40 newest carry the head; the two QUESTION files lack `carried-by:`. `transport.py janitor --apply` (:1637, :1196): NEVER RAN (no git, log or transcript witness).

## A4 — system map 88f1bc52 (ecosystem/system-map-record.json on c2953534)
- DEAD 21, reason "no trigger (manual)": audit-health, audit-title-gate, check-seal-identity, coherence-nudge, decision-coverage, derived-copies-rebind, doc-counts-pytest-freshness, graph-edge-class-census, graph-orphan-census, graph-process-list, graph-rebuild, graph-task-coverage, lane-contract-check, normalize-dated-headers, prepend-order, ruff, toc-freshness-playbook, validate-backlog. Reason "status DISARMED": block-onedrive.ps1, surface-closures.ps1, claude-notify.ps1.
- UNEXPLAINED 11 (no file-purpose graph entry, reason null): .claude/agents/artifact-reader.md; ecosystem/audit-funnel-baseline.json, audit-title-baseline.json, dependency-baseline.yaml, excluded-roots.yaml, platform-skip-baseline.json, proof-layer-baseline.json, registry.md, substrate-registry.yaml; plugins/tier1-lifecycle/.claude-plugin/plugin.json, assets/ruff-pre-commit.yaml.
- LIVE per moment (names; the map carries no per-moment state): pre-launch worktree_occupancy, seat_refusals.refuse_no_live_integrator, routing_agreement; lane-start single_flight; merge merge_receipt.open, merge_receipt.models, go_reader, review_packet, gates, test_pairing, known_reds_refresh; teardown no_leftovers; lane-end lane_cost, fleet_health.seat_health_line, transport_report; batch-close digest, trial_cut; seat-release seat_release.notes/.bundle/.manifest/.copy.

usage: A2 82,832 / A3 101,910 / A4 64,874 subagent tokens (Haiku; source: Agent-tool subagent_tokens). Orchestrator: not readable in-session.
