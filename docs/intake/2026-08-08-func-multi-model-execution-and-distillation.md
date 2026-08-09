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

---

## AMENDMENT 2026-08-09 (ARC-2 consolidation, architect amendment 3) — two commissions fold in here

Two of the six research commissions had **no owning intake**. Rather than file two more intakes —
which would take the pending set from four to seven and break the same ceiling this consolidation
enforces on rows — they fold in here, because this is already the measurement/instrumentation
intake. **Zero births by this amendment; the S3a MEASURE-FIRST precondition binds both folds.**

### Fold A — agent instrumentation & telemetry (memo `wf-02c940ef`)

**It converges with S3a and largely pre-empts it.** The memo's headline — *"Most of what you want is
already recorded"* — matches N3-21's independent finding almost exactly, and two sources reaching
it separately is the strongest signal in the batch on this point:

- Claude Code already writes a complete per-session JSONL (`~/.claude/projects/<encoded-path>/<session-id>.jsonl`)
  carrying per-message model id, per-request token usage (input / output / cache-read / cache-creation),
  timestamps, `tool_use`/`tool_result` entries and subagent sidechains — plus `gitBranch`, which is
  free lane attribution.
- It also emits **native OpenTelemetry** (session, token, cost, LOC, code-edit decisions, active-time)
  with **no SaaS** — console, Prometheus scrape, or a local OTLP collector.
- **So S3a's first move is EXTRACTION, not plumbing.** N3-21 states the same conclusion in the
  repo's own vocabulary: *"the correct organ is a READER, not a RECORDER."*

**Carried constraints, each already matching a landed repo ruling:**

- The transcript format is **explicitly "internal" and version-unstable** — Anthropic warns against
  building parsers on undocumented record relationships. Any reader is version-pinned by construction.
- N3-22's anti-goal stands and the memo does not contradict it: **no `PostToolUse` hook** (it fires on
  every tool call, sits on the operator's latency path, and re-records data already on disk). One
  `SessionEnd` hook, fail-soft — **not `Stop`**, per the ADR-85 "an organ that can be exhausted
  cannot carry teeth" finding.
- **The dangerous metrics are named:** LOC, commit counts and self-reported speed. DORA and SPACE both
  warn against single-dimension productivity metrics, and every proxy becomes gameable once it is a
  target. Defensible instead: cost-per-*solved*-task, wall-clock/active-time per completed task,
  retry-loop counts, edit-revert rates, rows closed per window — always paired with an outcome verdict.
- **The cross-provider denominator is narrow**: only wall-clock, tokens in/out, tool-call counts and
  outcome map cleanly across providers. Copilot CLI meters in *premium requests / AI credits*, which
  do **not** normalize onto tokens. Record raw provider units plus a separately computed token-based
  estimate, and **never mix subscription-plan and API-billed cost in one ledger.**

**The model-comparison bar, which binds any future bake-off:** paired within-task designs, ≥5–10
repeats per model, distributions with bootstrap confidence intervals, gated on a **private, versioned
seeded-defect corpus**. Nondeterminism persists at temperature 0; public benchmarks are contaminated;
the METR RCT found experienced developers were **19% slower** with AI while believing they were 20%
faster. Consequence for this repo, ruled: the 2026-07-31 single-diff A/B is **precedent for method,
not an admission instrument**, and **no bake-off runs before the seeded-defect corpus exists.**

### Fold B — the dependency/ontology graph (memo `wf-f6851745`)

Folded here because a graph is a measurement surface, not a new domain.

**The proposed shape is deliberately small:** a committed, regenerated JSONL **edge log** that the
*existing* validators emit into, queried through DuckDB recursive CTEs or stdlib SQLite, exposed via
a thin CLI — **not a new database platform, not a running server, not a SaaS.** The memo's own
framing is that most fragments (`reconciled_with` edges, the parity manifest, carrier manifests,
serialize-groups, doc-claims, ADR-101 tokens) are **already mechanisms**; the work is to make each
*also* emit typed edges into one file, then query the union.

**Its own evidence is mixed and it says so** — graphs win decisively for multi-hop "what breaks if I
change X" structural questions and **lose or tie** for semantic/keyword lookup, where plain BM25 was
optimal. Mäder & Egyed (2015, n=71, 461 tasks) is the strongest pro-traceability result (24% faster,
50% more correct solutions); ReqToCode's counter-warning is quoted verbatim in the memo: *"stale
links are not merely useless but actively harmful when they mislead developers."*

**Two flags this repo must carry, not the memo's to resolve:**

1. **A claim in it is FALSE about this repo.** It states grimp is *"already the engine behind your
   import-linter usage."* Verified 2026-08-09: **neither `grimp` nor `import-linter` exists anywhere
   in this repo** — not in `pyproject.toml`, `.pre-commit-config.yaml` or `uv.lock`. The only hit in
   the tree is an unrelated placeholder in `templates/ARCHITECTURE-template.md`. The memo's cheapest
   proposed edge source is **not free here; it is an unadopted dependency.**
2. **The architect flags the graph STORAGE choice as one of the memo's two least-defended sections** —
   it "reads like a decision and is not". DuckDB-vs-SQLite is therefore **open**, not ruled.

**The `footprint:` link is the memo's highest-leverage step and is measured here:** live 2026-08-09,
**5 of 168 open rows (3.0%)** declare `footprint:`. Ruled by this consolidation as a **landing
predicate on new and touched rows — never a backfill migration.** The memo's numerator agrees; its
denominator (169) is one window stale.

**Anti-rot is not optional and the memo is unambiguous:** every hand-authored link needs a check that
fails on dangling ids, orphan nodes and stale versions. `validate_reconciliation` is the template.
Everything structural — imports, coverage, commit-touched files — should be **derived, never typed by
hand**; only intent a machine cannot infer (decision↔code, requirement↔code) is worth curating.
