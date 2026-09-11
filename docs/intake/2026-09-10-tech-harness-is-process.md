---
intake-id: 92
status: DRAFT
origin: DECLARE-HARNESS-IS-PROCESS-2026-09-08 — outgoing browser seat (Fable), operator's word 2026-09-08, one refinement and witnessed trigger points only; carried into the repo 2026-09-11 by batch W lane lane-w-000-harness-is-process-intake under [#688], from the operator's transport at to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md (4,130 B, LF, sha256 0796e5714dd2af2af392060b120378ea1688099259241408848574dfd8add1df). The body below is byte-identical to the DECLARE body — only the transport's carried-by line is excluded, as transport metadata whose named successor IS this file
consumed-by:
---

# DECLARE-HARNESS-IS-PROCESS-2026-09-08 — the operator's definition adopted: harness = the set of automatically triggered processes; anything not triggered by a process is not harness
<!-- outgoing browser seat, Fable · operator's word 2026-09-08 · one refinement (§2) · witnessed trigger points only (§3); the full census is CC's (§4) -->

## 1 · Definition adopted
A harness is process management: a registry of `(trigger event → organ → artifact it reads/writes)`. A capability with no trigger row — a library nobody's process calls, a check no event runs, a script the operator would have to ask for — is not harness; it is inventory. This is the same statement as PROVENANCE §3.1 (a declared relation with zero runs is UNWIRED), seen from the operator's side: not "does it run?" but "what runs it?".

## 2 · One refinement (pushback, small)
Some acts are legitimately operator-triggered — the five decisions (GO · ratification · tag · destructive acts · seat release) plus their explicit commands (deploy, sitting). Those are not orphans; they are the harness's inputs. Everything else must have an event trigger. An "on-demand" organ that is not one of these inputs is an orphan by definition.

## 3 · Trigger points witnessed this window (what the harness IS today)
- **commit**: pre-commit roster (audit health, seal identity, lane-contract-check, ADR grammar incl. Flip-condition/Alternatives, intake tree coherence, doc claims), commit-msg gates (`kill-candidates:` / `[#id]`).
- **push**: `block-ff-push`, `block-unanchored-push` (ADR-85 anchor, main only).
- **session start**: `arm_hooks.py`; prompts-dir guard (loud); **PreToolUse** guard (armed 09-08); transcript-immutability guard (ADR-77).
- **session stop**: session-end hygiene hook (advisory).
- **handoff**: `/handoff` preflight (9 rows), `/handoff-verify` (15 probes incl. P11 — currently tabular, not real).
- **dispatch**: step 0 (manifest machine count, contract shape gate, [#441] test, DryRun since today).
- **integration**: ship-gate on demand by the integrator; JOURNAL anchor arcs.
- **nightly Routine (claimed, not witnessed by me this window)**: rot detectors, scorecard.
## Witnessed as INVENTORY (no trigger): FPG-1 graph · `run_retention()` (0 callers) · `propose_closures` (run by a lane, never by an event) · SDA-1 benchmark (designed, never run) · `cost_usage_telemetry.py` (library only) · seal on consumers (lane-run) · derived-copies render (U4 registry exists; render on commit not yet) · orphan_census (DRAFT) · offload/Enterprise (no row).

## 4 · The census that answers "how many orphan processes" — CC's, by mechanism
For every script under `scripts/`, every hook under `.claude/hooks/`, every command/skill, every organ in `audit.py`: name its trigger (hook stage · command · Routine schedule · another script's call site) or `NONE`. Output: `docs/audits/<date>-technical-process-trigger-census.md` with the count `triggered / on-demand-by-operator / orphan`. The orphan list is the retirement-or-wiring list for V+1 — each row either gets a trigger or is removed; a third state does not exist. This census becomes the relations registry of PROVENANCE §3.1 (generated, then kept by the coverage check).

## 5 · AJ conclusions, restated in the operator's frame (they are in DECLARE-F / DECLARE-F-2; here is what they say about THIS point)
The Maister plugin's only real structural advantage was a **process spine**: an orchestrator state file that triggered phases and knew where the task stood (A-30/A-31). Its gates were prose; ours are mechanisms — but ours have **no spine**, so organs fire at commit and push while the process between them is carried by seats' diligence. The operator's definition today is that spine, named. The other AJ deltas (reviewer re-runs tests, resumable lane state, reference-implementation seeding, cost per command) are all *triggers* the process lacks, not features. Everything else in the course we already enforce or deliberately rejected.
=== END ===
