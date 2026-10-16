# ADR-130: The outer loop runs in code — Conductor E completion

- **Status:** Proposed
- **Date:** 2026-10-15
- **Decision tier:** Path A — a `/decide` proposal for operator ratification (R14, ADR-108 §A).
- **Related:** ADR-120 (the spine is the whole loop; doit chosen, no state machine); ADR-124 (one code standard, tach); ADR-127 (CI on Windows and Linux); rows `[#1535]` (this step), `[#689]` (Conductor E, stays open for its four §6 numbers), `[#669]` (the delivery-loop transitions); R76, R99, R104, R105 D1-D6, R106, R114.
- **Decommission:** none.
- **Source:** the design `to-browser/DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md` §6 (the draft), §1-§4 (the loop, the data, the runner matrix, the constraint gate); the challenge verdicts `to-browser/DIGEST-BUILD1-READY-2026-10-15.md` `## CHALLENGE`; landed in-repo by lane `lane-bu-1535-outer-loop`, batch BU (BUILD-1).

## Context

R105 rules that Conductor E is finished in code, B first (D1-D6, OLR v2 §3). Before this step:

- a spine stage ran with no timeout (`scripts/dodo.py` ran every stage through a bare `subprocess.run`), so a hung vendor CLI hung the run;
- no round loop existed, so a judge's REFUSE had nowhere to go: doit runs an acyclic task graph and stops at the first failed task (`scripts/dodo.py` `task_dep`);
- receipts had no shared shape (the pilot's eight receipts shared no field set and carried no exit code), and a vendor could write its own `vendor` or `served_model`;
- nothing refused an empty constraint set, a duplicate organ, or a browser idea no other vendor had challenged.

`copilot.exe` may never exit (codespace LANE-END G2), so a phase cannot be judged complete by its process exit; and a payload alone, written before the spawn, proves nothing (CHALLENGE M3, X-I4-3).

## Decision

- **D1 — lane phases are data, one process each, doit inside a round loop.** The `phases:` block of `ecosystem/harness.yaml` lists P1 spec, P2 RED, P3 implement, P4 constraints, P5 QA, P6a/P6b the two reviewers, P7 judge, each with its role, CLI, gate, timeout and `max_rounds: 2`. `scripts/conductor.py lane --round r` is a stdlib loop that runs ONE acyclic doit run per round (`doit -f scripts/dodo.py round`), receipts under `LANE-<slug>/r<r>/`. A failed phase halts the round at the doit `task_dep` boundary; a REFUSE at round 1 asks for round 2; a REFUSE at round 2 is FAILED. Every phase runs through `scripts/run_phase.py`, which kills the whole process tree at its timeout (`resource_lifecycle.teardown_tree`, verified survivors) and writes a heartbeat.
- **D2 — a harness-built receipt; the agent owns only its payload.** The agent writes `PhasePayload` (`extra="forbid"`: outcome, findings, detail, plus the spawn's nonce and input hash). The harness builds `PhaseReceipt` v1 (`ecosystem/schema/phase_receipt.py`), a superset of the ten `dodo.py` receipt keys, deriving `vendor` from the launched argv through `ecosystem/provider-registry.yaml` and `served_model` from the CLI's own record. A forged vendor or served model is refused. A point task is COMPLETE on a FRESH valid payload (schema-valid, this spawn's nonce and input hash, mtime after the spawn); its exit code is recorded and never required.
- **D3 — `[#669]`'s transitions on python-statemachine ==3.2.1 if the Q14a spike passes, else a stdlib table.** Not built here: the spike is `[#669]`'s step 0 (CHALLENGE M4); no dependency is added by this ADR's first step.
- **D4 — constraints are data with a mandatory baseline.** The `constraints:` block lists `{id, kind, checker, applies_when, reuses}`. C-TASK, C-SCOPE, C-RED, C-VENDOR and C-CLEAN are always selected; an empty selection, or a registry missing one of them, is a refusal. P1 may add a constraint, never remove one (ADR-81).
- **D5 — no workflow engine.** Receipts already resume a killed round (doit's `uptodate` over the receipt), so a durable engine buys nothing it does not also cost (design §3 option d).
- **D6 — dynamic workflows stay audit-only.** They have no direct filesystem or shell access and resume only in the same session (design §3 option b).

The distiller is the loop's front stage: `gen_lane_contract.py distill --row <id>` reads `tasks/<id>` (R106), refuses an unphased row, and emits a `DistillReceipt` whose reuse candidates come from `file_purpose_graph.py why` and `ecosystem/organ-index.md`. A plan that builds NEW where a candidate exists is refused unless it carries NEW-JUSTIFIED and a `ChallengeReceipt` from a vendor other than the producer's. A decision-class input gets a CHALLENGE: AGREE, AMEND or DISAGREE; a duplicate of an existing organ is DISAGREE and halts the row at INPUT_REQUIRED; no reachable reviewer is INPUT_REQUIRED, never a pass.

**R105 amendments carried.** R104: code picks what runs next; Opus keeps plan, judge and review. R99: the phase table orchestrates; `dispatch.py` stays the only launch path. `[#689]` carries an R105 D2 note.

## Quality attributes

- **Quality attribute(s):** reliability (no lost step, no hung phase), integrity (a receipt cannot be self-attested), cost visibility.
- **Scenario:** a vendor CLI hangs mid-P3, or never exits after writing its payload; a lane process is killed mid-round; a reviewer of the producer's own vendor is the only one routed.
- **Response measure:** the hung tree is killed at the phase timeout with zero surviving descendants; a fresh payload is harvested and the tree killed; a re-run resumes at the killed phase without re-running a fresh one; the same-vendor reviewer is refused by C-VENDOR. Target: no lost step, one trip-test per transition, USD per row recorded.
- **Decision evidence:** the RED-first witnesses `tests/test_run_phase.py`, `tests/test_dodo_phases.py`, `tests/test_conductor_lane.py`, `tests/test_distill_receipt.py`, `tests/test_challenge_receipt.py`; the runner matrix of design §3 (option e, 89, against a 86, d 80, b 49).

## Consequences

- No orchestrator LLM: what runs next is decided by data and code; every vendor is first-class through the same adapter.
- At most one new dependency (python-statemachine, behind `[#669]`'s spike).
- A red `main` blocks P5 (QA compares against the base).
- Live vendor runs of the phase table are witnessed by the steel thread (`[#1430]`, BUILD-2 slot 1), not by this step's toy harnesses.

## Flip-condition

Flip to option (d), a durable engine, if a killed round fails to resume from its receipts in the steel thread or in two consecutive batches, or if a phase table outgrows a linear chain per round (a fan-out the doit task graph cannot express). Flip D3 to the stdlib table if the python-statemachine spike fails or a CVE lands on the pinned version.

## Alternatives considered

- **(a) conductor + doit** — 86: kept as the base of (e).
- **(b) dynamic workflows** — 49: no filesystem or shell access from the workflow, Claude-only agents, resume only in the same session. Rejected (D6).
- **(c) a state machine only, no runner** — 88 but ineligible: it fires transitions and runs nothing.
- **(d) a durable engine (DBOS, Prefect, Temporal, Hatchet)** — 80: Prefect, Temporal and Hatchet need a server; DBOS adds a database for a resume the receipts already give. Rejected (D5).
- **(e) (a) + python-statemachine for `[#669]` + pydantic** — 89: chosen.
