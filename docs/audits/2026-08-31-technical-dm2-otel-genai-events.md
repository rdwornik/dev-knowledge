# DM-2 — telemetry now emits OTel GenAI-shaped events; the collector stays pluggable and unbuilt; the verdict layer is untouched

**Lane:** `lane-f-6-observability-otel` (branch `worktree-lane-f-6-observability-otel`), contract
`LANE-f-6-observability-otel.md`. **Blocked-by, discharged:** Tier (B)'s OTel GenAI event-schema
draft, `docs/audits/2026-09-01-technical-tierb-b1-otel-genai-event-schema.md` ("B-1" below).

## What landed

One new file in the frozen write-scope, `scripts/cost_usage_telemetry.py` — a library-only
emitter, no call sites, same posture `scripts/telemetry_emit.py` shipped at its own Stage 1.
`emit_genai_span()` takes one model-call's facts (system, model, token counts, cache tokens,
duration, client-side cost estimate, lane/batch correlation, substrate) and writes ONE row per
call into a new SQLite store, `logs/GENAI-TELEMETRY.db`, table `genai_spans`. The row's
`attributes_json` column is a flat dict keyed by the OTel GenAI semantic-convention attribute
names B-1 mapped (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, …) plus
the `devknowledge.*` extension namespace B-1 proposed for the concepts with no standard slot
(`devknowledge.gen_ai.usage.cache_read_tokens`, `devknowledge.cost.estimated_usd`,
`devknowledge.lane_id`, `devknowledge.substrate`, …). This is B-1's schema (section 1), written
down as code rather than re-decided.

## Why a new emitter, not an extension of Stage-1

`telemetry_emit.py`'s `EVENT_TYPES` enum (`check_run`, `hook_run`, `blocker_fired`) is
audit-gate telemetry, not model-usage telemetry, and B-1 section 4 says explicitly that folding
GenAI spans into that table would be scope creep — different axis, different cardinality (one
row per gate fire vs. one row per model call). What this lane DID reuse rather than
re-implement: the `[#565]` `run_id` correlation concept, via `telemetry_emit.current_run_id()`
called directly — a lane's gate events and its model-call spans now share one correlation id
instead of this module minting a second, competing one. Also reused: `telemetry_emit.repo_root()`
(the R6(c) fix for a module-frozen path answering the wrong question in a linked worktree) and
`telemetry_emit.WAL_PRAGMAS` (same concurrency reasoning — parallel lanes may write both stores
in the same window).

## The collector seam — kept real, kept unbuilt

B-1 section 2's seam is "the smallest interface that keeps both [Phoenix, Langfuse]
interchangeable is the standard OTLP exporter contract … swapping collectors is a config change,
not a code change." That shape is now in code as `SpanExporter` (a `Protocol`), resolved once
per call by `resolve_exporter()` from `collector=` or `$DEV_KNOWLEDGE_GENAI_COLLECTOR`, and
`emit_genai_span()` never branches on the exporter's identity after that one resolution point.

**Only one concrete exporter ships: `AtRestExporter`.** It writes the OTel-GenAI-shaped row as
conforming JSON into the local SQLite store — B-1's own "paper/at-rest format", schema-conforming
but not live-exported. This is deliberate, not partial: **B-1's FINDING (section 2) is that no
`opentelemetry-sdk` / `opentelemetry-exporter-otlp*` package is declared in
`pyproject.toml` / `uv.lock`**, and this lane re-confirmed that finding still holds (grepped both
files; neither names one). Emitting real OTLP wire traffic needs that dependency, and the
lane's own done-contract item 4 is explicit: *"No new dependency without an explicit ADR-106
gated act. If the schema needs a package, STOP and report — a `uv.lock` change is its own
decision, never a side effect."*

**STOP AND REPORT, IN CODE.** `resolve_exporter("phoenix")` and `resolve_exporter("langfuse")`
each raise `CollectorNotAvailable`, naming the missing package and the ADR-106 gate, rather than
silently falling back to `at-rest` or silently vendoring the dependency. This is the mechanism
that keeps a future wiring lane from adding `opentelemetry-*` as a side effect of flipping an env
var — the seam itself refuses. `pyproject.toml` and `uv.lock` are unmodified by this lane; `git
diff --stat` for this branch shows only the two files in the frozen write-scope.

**Both collectors stay DISCHARGED, neither hard-wired**, per the done-contract item 2: Phoenix
and Langfuse are named, their divergence is documented in B-1 section 2 (Langfuse's Basic-Auth
OTLP headers + session/user attributes; Phoenix's project-identifier header), and neither is
picked. `resolve_exporter`'s default remains `"at-rest"`.

## The verdict layer — unchanged, and not modeled

Nothing in `scripts/cost_usage_telemetry.py` reads, writes, or references a ruling. Per B-1
section 1 ("Deliberately NOT modeled here") and this lane's done-contract item 3, the schema
carries no `devknowledge.verdict.ruling_ref` or equivalent — a span records that a call
happened, with what cost/tokens; it does not carry why a trend became a ruling. Trends → rulings
stays exactly as it is; this lane moved the emission format, not the judgment.

## What this schema still cannot express (carried forward from B-1 section 3, unchanged by this lane)

Ground-truth cost, flat-fee subscription utilization, decision-budget/escalation semantics,
cross-call causality, and content-capture completeness are all out of scope here for the same
reasons B-1 gives — this lane did not re-decide any of them, and the module docstring points
back to B-1 rather than restating the rationale.

## Verification

- `uv run --locked ruff check scripts/cost_usage_telemetry.py` — clean.
- A smoke run of `emit_genai_span()` against a scratch SQLite file (outside the repo, deleted
  after the check) confirmed: a full span round-trips with every `gen_ai.*` / `devknowledge.*`
  attribute in the row named above; an unknown collector target raises `GenAiTelemetryError`; a
  `phoenix` target raises `CollectorNotAvailable` naming the missing package; a blank `system`
  raises `GenAiTelemetryError`; `safe_emit_genai_span()` swallows an `OSError` from a bad store
  path and returns `None`.
- `uv run --locked pytest tests/test_telemetry_emit.py tests/test_telemetry_run_id.py -x
  --tb=short` — 52 passed. These are the targeted tests for this diff's one dependency
  (`telemetry_emit.py`, imported for `current_run_id()` / `repo_root()` / `WAL_PRAGMAS`); this
  lane's own write-scope names no test file, so none was added, per "No edits outside the
  declared footprint."
- `uv run --locked python scripts/worktree_import_proof.py --repo .` — `NOT-APPLICABLE`: this
  repo declares no importable package in `pyproject.toml`, the same answer the hub itself gives.
- No `pyproject.toml` / `uv.lock` change. No new dependency.

## Decisions taken under the V-2 budget

None of the three escalation classes fired: no curated-baseline touch, no rule-vs-ruling
conflict, no fork class lacking a standing ruling. Judgment calls made per contract defaults,
recorded here rather than escalated:

- **New store file, not a reused table.** B-1 section 4 states the reason directly (scope
  creep); this lane treated that as decided rather than re-litigating it.
- **`SpanExporter` is a hand-rolled `Protocol`, not `opentelemetry.sdk.trace.export.SpanExporter`.**
  The OTel SDK type is unavailable (undeclared dependency); a same-shaped local interface keeps
  the seam real without importing the package the done-contract forbids adding as a side effect.
- **`run_id` rides both the SQLite column and `attributes_json["devknowledge.run_id"]`.** The
  column keeps cheap SQL filtering (matching `telemetry_emit.py`'s own shape); the JSON key keeps
  the attribute dict self-contained, since B-1 proposed `devknowledge.run_id` as an attribute in
  its own right, not only as an out-of-band column.
- **No call sites wired.** The contract's step 2 ("Emit the events; keep the collector behind a
  seam") reads as building the capability, matching the write-scope (one library file, one
  report) and `telemetry_emit.py`'s own Stage-1 precedent ("library only; no call sites").
  Instrumenting an actual model-call site is a separate, later lane's footprint.

## Consumed by

`[#614]` (batch E's frozen execution arc). This report discharges DM-2.
