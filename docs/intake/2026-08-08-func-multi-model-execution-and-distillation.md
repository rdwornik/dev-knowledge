---
intake-id: 29
status: DRAFT
origin: "Layer-1 architect (outgoing seat), 2026-08-08 — the operator's problem statement on long single-model sessions; landed VERBATIM by the frozen contract ARC-file-intakes-28-29 (S-write, zero births)"
note: "Class: functional. Provenance (from the body): the \"distillation engine\" intent carried NO repo locator until this intake — third instance of the intention-without-locator class; this filing is the F5-style repair. Triage rides the batch-4 planning GO with intake #28 as ONE ratification batch — this filing DECIDES nothing. The body carries its own metadata bullets (intake-id / Class / Date / Status / Author / Provenance note) verbatim as source text; this frontmatter is the schema-conformant carrier per docs/intake/README.md §3. The body's `intake-id: 29 (PROPOSED ...)` line is preserved as written — 29 was verified next-free across the live index and all git history before filing."
---

# Multi-model execution flow, session-cost instrumentation, and the distillation engine (measure-first)

- **intake-id:** 29 (PROPOSED — executor verifies next-free before filing)
- **Class:** functional · **Date:** 2026-08-08 · **Status:** DRAFT — triage rides the batch-4 planning GO with intake #28, ONE ratification batch
- **Author:** Layer-1 architect (outgoing seat), from the operator's problem statement 2026-08-08
- **Provenance note:** the "distillation engine" intent carried NO repo locator until this intake — third instance of the intention-without-locator class; this filing is the F5-style repair.

## Problem

Sessions run long (measured: 3h / 2h20 / 1h19 arcs) and every lane is a single-model monolith: opus performs retrieval, mechanical edits, test runs, gate sweeps, and judgment alike. The haiku→sonnet→opus flow exists in the routing table for SESSIONS but not WITHIN executions. Separately, no measured breakdown of where session time/tokens go exists — so any "optimization engine" would be built on impression, the exact failure mode [#511] just disproved for the handoff.

## Scope — three stages, each independently shippable

**S1 · Contract-level routing (zero build):** the lane/arc contract template gains a SUB-AGENT ROUTING section — retrieval, reads, greps, doc summarization → haiku sub-agents; bounded specified edits + suite/gate runs → sonnet sub-agent; design, judgment, review, integration → the main opus thread. Guard: sub-agents never decide against doctrine — they retrieve and execute specs; ambiguity routes UP.

**S2 · Versioned agents, adopt-native:** 2–3 repo agents in `.claude/agents/` with explicit `model:` — `reader` (haiku, read-only toolset), `mechanic` (sonnet, applies specified diffs, runs `uv run --locked pytest -n auto`), `gatekeeper` (sonnet, runs the gate mesh, reports verbatim). Referenced from Ch8; CC-native subagent mechanism = the library (library-first discharged by construction). Acceptance: one real lane runs with ≥2 sub-agent delegations and its packet reports the split.

**S3 · Distillation engine, MEASURE-FIRST:** (a) instrumentation before machinery — per-arc phase/time/token logging via hooks (session duration, per-phase wall-clock, model mix), two windows of data; (b) only then scope the engine against the measured sink (candidate shapes, to be chosen by data: contract-payload distiller · packet condenser · gate-context slimmer); (c) the engine, if built, is Tier-L (enters code) with a measured-divergence acceptance target derived from (a). Building (c) before (a) is out of scope by this intake's own text.

## Non-goals

No new orchestration frameworks (§B stands — CC subagents are native). No model-mix changes to the SESSION-level opus-default rule (it answered a measured failure; S1/S2 route WITHIN the opus session). No engine build on unmeasured premises.

## Births

ZERO at filing. Candidates at batch-4 planning: S1 template amendment (S-row, may fold into the batch-4 process slot) · S2 agents build (S) · S3a instrumentation (S). S3c exists only after S3a's data.

## Acceptance criterion

S1 ratified and live in the template; S2's acceptance lane demonstrated; S3a producing per-arc breakdowns in packets; the "distillation engine" question answerable with numbers by the window after next.
