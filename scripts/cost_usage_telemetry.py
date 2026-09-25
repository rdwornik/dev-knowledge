#!/usr/bin/env python
"""cost_usage_telemetry.py -- DM-2 (`lane-f-6-observability-otel`): OTel GenAI-shaped model-call
telemetry. Library only; no call sites -- same posture `telemetry_emit.py` shipped at Stage 1.

WHAT THIS IS. The emitter half of the schema TIER (B) B-1 drafted
(`docs/audits/2026-09-01-technical-tierb-b1-otel-genai-event-schema.md`), consumed by DM-2 per
`LANE-f-6-observability-otel.md`. One model-call = one SPAN, shaped to the OpenTelemetry GenAI
semantic conventions (`gen_ai.*`) with a `devknowledge.*` extension namespace for the concepts
B-1 found no standard slot for: cache tokens, client-side cost, lane/batch/run correlation, and
substrate. **THE VERDICT LAYER (trends -> rulings) IS UNCHANGED** -- this module emits
call-shaped, cost-shaped, routing-shaped facts; it carries no ruling and no
`devknowledge.verdict.ruling_ref` (B-1 section 1: "Deliberately NOT modeled here"). If a span
ever needs to reference a ruling, that is a link added later, never an attribute that reshapes
the span.

THIS IS A NEW EMITTER, NOT AN EXTENSION OF `telemetry_emit.py`'S STAGE-1 STORE -- B-1 says why
(section 4): Stage-1's `EVENT_TYPES` enum (`check_run`, `hook_run`, `blocker_fired`) has no
model-call type, and folding GenAI spans into that table would be scope creep -- different axis
(audit-gate telemetry vs. GenAI call telemetry), different cardinality (one row per gate fire vs.
one row per model call). What IS reused: the `[#565]` `run_id` correlation concept, via
`telemetry_emit.current_run_id()` itself -- so a lane's gate events and its model-call spans
share ONE correlation id rather than this module minting a second, competing one. That is B-1's
own instruction (table 1, "Which lane/worktree/batch fired this call": "reuse the existing
run_id correlation concept from telemetry_emit.py rather than minting a second one").

THE COLLECTOR SEAM, AND WHY IT STOPS WHERE IT STOPS. B-1's own FINDING (section 2, verbatim in
the schema draft): no `opentelemetry-sdk` / `opentelemetry-exporter-otlp*` package is declared in
`pyproject.toml` / `uv.lock` today (confirmed again here -- neither file names one), and adding
one is a separately gated ADR-106 act, never a side effect of drafting a schema. This lane's own
done-contract item 4 repeats the identical rule. So THIS MODULE EMITS NO LIVE OTLP WIRE TRAFFIC
and imports no `opentelemetry.*` package -- there is nothing on this host to import. What it DOES
do is keep the seam B-1 describes real at the code-shape level: `SpanExporter` is the interface
(resolved from config/env, never branched on inline); the only concrete implementation shipped
here is `AtRestExporter`, which writes the OTel-GenAI-shaped row as conforming JSON into a local
SQLite store -- exactly the "paper/at-rest format" B-1 names as safe to write today, and exactly
the "Both [Phoenix, Langfuse] are DISCHARGED ... do not hard-wire either" instruction in the
lane's done-contract item 2. A `phoenix` or `langfuse` collector target is *resolvable*
(`resolve_exporter`), but each live-OTLP-backed exporter is INTENTIONALLY UNIMPLEMENTED and
raises `CollectorNotAvailable`, naming the missing package and the ADR-106 gate -- this is the
"STOP and report" the done-contract asks for, expressed in code, at the one seam where a silent
dependency add could otherwise sneak in through a wiring site rather than a reviewed commit.

===============================================================================
CALL SURFACE
===============================================================================

    from cost_usage_telemetry import emit_genai_span

    emit_genai_span(
        system="anthropic",
        request_model="claude-opus-5",
        response_model="claude-opus-5",
        input_tokens=1200,
        output_tokens=340,
        cache_read_tokens=88000,
        duration_ms=4210,
        cost_estimated_usd=0.0142,
        lane_id="lane-f-6-observability-otel",
        batch_id="batch-e",
        substrate="local",
        role="implement",              # [#691] -- one of ROLES
        outcome="passed",              # [#691] -- one of CALL_OUTCOMES
        reviewed_by="gpt-5.6-terra",   # [#691] -- AX22-2, never the producing model
    )

THE `[#691]` EXTENSION -- `role`, `outcome`, `reviewed_by` (AX21-2 / AX22-2). AX21-2 names the
re-rank's input verbatim: *"every call records model, tokens, cost and outcome (tests green?
review HIGH-free?) in the tally"*. Model, tokens and cost were emitted here from day one; the
three fields above are the right-hand side of that ratio, and they are an EXTENSION of this
emitter rather than a second one because the exists-before-build answer for `[#691]` step 2 is
that AX5-1's telemetry already exists -- this module IS it. What it could not answer was
per-ROLE pass rate (a provider strong at `read` and weak at `implement` has no single
meaningful rate), whether the WORK PRODUCT passed as opposed to the CALL succeeding, and who
reviewed -- the last being AX22-2's *"the tally records both roles"*, without which
reviewer-not-producer is unauditable after the fact.

All three are OPTIONAL: a span carrying none is valid, the pre-`[#691]` call surface is
unchanged, and a caller with no role to declare writes none rather than a fabricated one. All
three are REFUSED when malformed, before the row is built, so a refusal leaves no partial write.

Returns the new row id (`int`) when the resolved collector durably stores the span (the default,
`AtRestExporter`); a future live exporter may return `None` for a fire-and-forget export. Every
call accepts `db_path`, `ts`, and `run_id` overrides for the same reasons `telemetry_emit.py`'s
`emit_event` does (tests, replay, an outer correlation scope). `collector=` overrides the
`$DEV_KNOWLEDGE_GENAI_COLLECTOR` env var per call; both default to `"at-rest"`.

Programming errors raise (`GenAiTelemetryError` and `CollectorNotAvailable`, its subclass for an
unimplemented live target). A wiring site that must never break its host process wraps the call
in `safe_emit_genai_span()`, which swallows store/IO failures only -- refusals and unknown
collector targets still propagate, the same split `telemetry_emit.safe_emit` draws.

Reading back is `sqlite3` and SQL against the `genai_spans` table; this module owns no read
surface, matching `telemetry_emit.py`'s own Stage-3 deferral.
"""
from __future__ import annotations

import json
import math
import os
import sqlite3
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

# Same bare-import-first shape as `block_ff_push.py` / `governance_health.py`: one module
# object per invocation mode (`python scripts/cost_usage_telemetry.py` vs. `-m scripts...`),
# so `current_run_id()`'s per-process cache is the SAME cache this module observes.
try:
    import telemetry_emit as _te
except ImportError:
    from scripts import telemetry_emit as _te

#: Env var that relocates the store. Set it in a test, a sandbox, or a satellite checkout --
#: same shape as `telemetry_emit.DB_PATH_ENV`, deliberately a DIFFERENT variable, because this
#: is a different store (see module docstring, "NEW EMITTER").
DB_PATH_ENV = "DEV_KNOWLEDGE_GENAI_TELEMETRY_DB"

#: Default store location. UPPERCASE-KEBAB stem per the 2026-07-22 `logs/` naming ruling
#: (CLAUDE.md section 9); `.db` stays honest to the format.
DEFAULT_DB_RELPATH = Path("logs") / "GENAI-TELEMETRY.db"

#: Env var naming the collector target, resolved once per call and never branched on inline --
#: B-1 section 2's seam. `"at-rest"` (the default) writes the OTel-GenAI-shaped row into the
#: local SQLite store; `"phoenix"` / `"langfuse"` are named but unimplemented (see
#: `CollectorNotAvailable`).
COLLECTOR_ENV = "DEV_KNOWLEDGE_GENAI_COLLECTOR"

#: The two collector targets B-1's done-contract discharges (item 2) but this module does not
#: implement, and the package each would need to stop being a paper format. Maps target name ->
#: the human-readable reason `CollectorNotAvailable` names, so the STOP is legible without
#: reading this module's source.
_LIVE_COLLECTOR_PACKAGES: dict[str, str] = {
    "phoenix": "opentelemetry-sdk + opentelemetry-exporter-otlp* (Phoenix ingests standard OTLP)",
    "langfuse": "opentelemetry-sdk + opentelemetry-exporter-otlp* (Langfuse's self-hosted OTLP ingest endpoint)",
}

#: The ROLE vocabulary, closed -- `[#691]` / AX21-1's role->model table, verbatim and in its
#: order: orchestrate / plan -> implement -> review -> read -> verify. (AX21-1 writes
#: "read / scan"; the token is `read`, hyphen-only names per the lane's done-contract item 4.)
#:
#: WHY CLOSED. A role is a LOOKUP KEY on three surfaces -- the registry's `roles:` collection,
#: `provider_router.route()`, and the re-rank's GROUP BY. An open vocabulary makes a typo
#: (`implment`) emit a span every one of those three silently drops, which is the
#: present-but-unread failure mode `ecosystem/schema/provider_registry.py` already refuses with
#: `extra="forbid"`. Deliberately NOT shared with `routing-table.yaml`'s coarse
#: producer/reviewer/adversarial/fan_out vocabulary: that table routes a role to a CLI, this one
#: keys a measured pass rate, and collapsing them would make one of the two lie.
ROLES: frozenset[str] = frozenset(
    {"orchestrate", "plan", "implement", "review", "read", "verify"}
)

#: The WORK-PRODUCT outcome, closed -- AX21-2's parenthetical ("tests green? review
#: HIGH-free?"), which is a DIFFERENT fact from whether the HTTP call succeeded. A call that
#: returns cleanly and produces code failing the lane's tests is `failed` here and carries no
#: `error.type`. The call-level failure axis stays `error.type`; these never merge.
#:
#: `unknown` IS FIRST-CLASS, for the reason `telemetry_emit.py` states on unresolved coverage
#: (constraint 2, "UNRESOLVED COVERAGE IS `unknown`, NEVER `0`"): a call whose product has not
#: been judged yet is a KNOWN state. Omitting the field instead would make an unjudged call
#: indistinguishable from a passing one to any rate computed as `passed / (passed + failed)`,
#: which silently inflates every provider's measured rate -- the exact defect AX21-2's
#: "measured, not declared" clause exists to prevent.
#:
#: The tokens deliberately do NOT reuse `telemetry_emit.OUTCOMES` (`pass`/`block`/`error`).
#: Those label a GATE fire. Sharing the token `pass` across the two stores would make two
#: different facts indistinguishable in any join across the two tables.
CALL_OUTCOMES: frozenset[str] = frozenset({"passed", "failed", "unknown"})

#: `genai_spans` -- one row per model-call span. `attributes_json` carries the full
#: OTel-GenAI-shaped attribute dict (the `gen_ai.*` + `devknowledge.*` mapping from B-1 table 1);
#: the handful of denormalized columns exist only so a reader does not have to parse JSON to
#: filter by system/model/run. `events_json` carries B-1 table 2's opt-in content-capture events
#: (`gen_ai.user.message`, `gen_ai.choice`, ...) verbatim -- this module applies no redaction and
#: no privacy gating; a caller that wants content capture supplies already-gated events.
SCHEMA = """
CREATE TABLE IF NOT EXISTS genai_spans (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    ts               TEXT    NOT NULL,
    run_id           TEXT    NOT NULL DEFAULT '',
    gen_ai_system    TEXT    NOT NULL,
    operation_name   TEXT    NOT NULL,
    request_model    TEXT    NOT NULL,
    response_model   TEXT,
    duration_ms      INTEGER,
    attributes_json  TEXT    NOT NULL DEFAULT '{}',
    events_json      TEXT    NOT NULL DEFAULT '[]'
)
"""


class GenAiTelemetryError(Exception):
    """Base for every refusal this module raises. Callers that must not break their host
    catch this (or use `safe_emit_genai_span`); callers that want the defect loud let it
    propagate."""


class CollectorNotAvailable(GenAiTelemetryError):
    """A named live collector target (`phoenix`, `langfuse`) has no exporter here, because the
    package it needs is not a declared dependency of this repo. THIS IS THE "STOP and report"
    the lane's done-contract item 4 asks for, raised at the seam instead of silently falling
    back to `at-rest` or silently vendoring the package. Adding the package is a separately
    gated ADR-106 act."""


@runtime_checkable
class SpanExporter(Protocol):
    """The collector seam. B-1 section 2: 'the smallest interface that keeps both interchangeable
    is the standard OTLP exporter contract' -- this is that interface's shape, minus the OTel SDK
    types this repo does not depend on. A conforming exporter takes one already-built row (the
    same shape `AtRestExporter` stores) and returns a row id when it durably stored one, or
    `None` for a fire-and-forget export."""

    def export(self, row: Mapping[str, Any]) -> int | None: ...


class AtRestExporter:
    """The one concrete `SpanExporter` this module ships. Writes the OTel-GenAI-shaped row as
    conforming JSON into the per-repo SQLite store -- B-1 section 2's "paper/at-rest format":
    schema-conforming, not live-exported, because the OTLP wire path needs a package this repo
    does not declare (see module docstring)."""

    def __init__(self, db_path: str | os.PathLike[str] | None = None) -> None:
        self._db_path = db_path

    def export(self, row: Mapping[str, Any]) -> int:
        with connect(self._db_path) as conn:
            cur = conn.execute(
                "INSERT INTO genai_spans "
                "(ts, run_id, gen_ai_system, operation_name, request_model, response_model, "
                " duration_ms, attributes_json, events_json) "
                "VALUES (:ts, :run_id, :gen_ai_system, :operation_name, :request_model, "
                " :response_model, :duration_ms, :attributes_json, :events_json)",
                dict(row),
            )
            return int(cur.lastrowid)


def resolve_exporter(target: str | None = None, *, db_path: str | os.PathLike[str] | None = None) -> SpanExporter:
    """Resolve a collector target (`target`, else `$DEV_KNOWLEDGE_GENAI_COLLECTOR`, else
    `"at-rest"`) to a `SpanExporter`. The ONLY branch in this module on the collector's identity
    -- every other line treats the exporter as an opaque `SpanExporter`, which is what keeps
    swapping collectors a config change rather than a code change (B-1 section 2).

    Raises `CollectorNotAvailable` for `"phoenix"` / `"langfuse"` -- named, discharged, and
    deliberately not hard-wired, per the lane's done-contract item 2. Raises
    `GenAiTelemetryError` for anything else unrecognized.
    """
    resolved = (target if target is not None else os.environ.get(COLLECTOR_ENV, "at-rest")).strip().lower()
    if resolved in ("", "at-rest", "none"):
        return AtRestExporter(db_path=db_path)
    if resolved in _LIVE_COLLECTOR_PACKAGES:
        raise CollectorNotAvailable(
            f"collector target {resolved!r} needs {_LIVE_COLLECTOR_PACKAGES[resolved]}, which is not "
            f"declared in pyproject.toml/uv.lock. Adding it is a separately gated ADR-106 act (B-1 "
            f"finding; lane-f-6-observability-otel done-contract item 4) -- STOP and report rather than "
            f"add it as a side effect. Until that gate runs, spans are written at-rest only "
            f"(collector='at-rest', the default)."
        )
    raise GenAiTelemetryError(
        f"unknown collector target {resolved!r}; expected 'at-rest' (default), 'phoenix', or 'langfuse'"
    )


def default_db_path() -> Path:
    """The store location: `$DEV_KNOWLEDGE_GENAI_TELEMETRY_DB` if set, else
    `<repo>/logs/GENAI-TELEMETRY.db` where `<repo>` is `telemetry_emit.repo_root()` -- the
    CALLER's repository, resolved at call time. Reuses that resolver rather than re-deriving it,
    for the same R6(c) reason `telemetry_emit.py` states on its own copy: a module-frozen path
    answers "where does this file live", every caller wants "which repository is being emitted
    for", and the two diverge in a linked worktree.
    """
    override = os.environ.get(DB_PATH_ENV)
    if override:
        return Path(override)
    root = _te.repo_root()
    if root is None:
        raise GenAiTelemetryError(
            f"cannot resolve the genai telemetry store: `git rev-parse --show-toplevel` did not answer "
            f"from {Path.cwd()}. Set ${DB_PATH_ENV} to an explicit path, pass `db_path=`, or run inside "
            f"a repository"
        )
    return root / DEFAULT_DB_RELPATH


@contextmanager
def connect(db_path: str | os.PathLike[str] | None = None):
    """Open the store with `telemetry_emit`'s three WAL pragmas applied (reused, not
    re-declared -- same concurrency reasoning: parallel lanes and hooks may write both stores in
    the same window) and this module's own schema ensured. Creates the parent directory if
    absent. Commits on clean exit, rolls back on exception, always closes.
    """
    path = Path(db_path) if db_path is not None else default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5.0)
    try:
        for pragma, value in _te.WAL_PRAGMAS:
            conn.execute(f"PRAGMA {pragma}={value}")
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds")


def _check_int(label: str, value: Any) -> None:
    if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
        raise GenAiTelemetryError(f"{label} must be an int or None, got {type(value).__name__}")


def _check_number(label: str, value: Any) -> None:
    """A number, and a FINITE one.

    LEG 1 of two (terra HIGH, pre-merge review 2026-09-01). `NaN` and the infinities are
    `float` instances, so a type check alone admits them -- and `json.dumps` serialises them as
    the bare tokens `NaN` / `Infinity`, which **RFC 8259 does not permit**. A strict OTLP or
    JSON consumer rejects the whole payload, so the span is not merely wrong, it is silently
    absent at the far end. That is the worst shape for a telemetry emitter: the failure lands
    in someone else's parser, and the emitting side reports success.
    """
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise GenAiTelemetryError(f"{label} must be a number or None, got {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise GenAiTelemetryError(
            f"{label} must be finite, got {value!r} -- NaN and the infinities serialise as "
            f"non-standard JSON tokens that a strict consumer refuses")


def _check_vocabulary(label: str, value: Any, allowed: frozenset[str]) -> None:
    """A closed-vocabulary field: absent, or exactly one of `allowed`.

    CASE-SENSITIVE AND UNTRIMMED-REFUSING, for the reason
    `ecosystem/schema/provider_registry._require_lowercase` already states about this repo's
    other lookup keys: every consumer matches these RAW, so silently normalising `IMPLEMENT`
    to `implement` would make the committed value differ from the value, while accepting it
    raw would make a role resolve nowhere. Refusal is the only option that leaves the store
    readable.
    """
    if value is None:
        return
    if not isinstance(value, str) or value != value.strip() or value not in allowed:
        raise GenAiTelemetryError(
            f"{label} must be one of {sorted(allowed)} or None, got {value!r} -- this is a "
            f"lookup key the registry, the router and the re-rank all match raw, so an "
            f"unrecognised token emits a span every one of them silently drops"
        )


def _check_reviewer_is_not_the_producer(
    reviewed_by: Any, response_model: Any, request_model: Any
) -> None:
    """AX22-2 (*"Reviewer != producer, always"*) enforced AT THE TALLY.

    The registry encodes the exclusion and `provider_router` enforces it before dispatch --
    but this is the only leg that can catch a violation AFTER the fact, and the record is what
    the AX8-2 log-review routine reads. A tally that happily wrote `reviewed_by ==
    response_model` would make the violation invisible in exactly the surface built to expose
    it.

    FALLS BACK TO `request_model` when no response model was recorded, and that fallback is
    load-bearing rather than tidy: a caller who simply omits `response_model` would otherwise
    buy an unchecked self-review, which turns an optional field into a bypass.
    """
    if reviewed_by is None:
        return
    producer = response_model if response_model is not None else request_model
    if producer is not None and str(reviewed_by).strip() == str(producer).strip():
        raise GenAiTelemetryError(
            f"reviewed_by is {reviewed_by!r}, which is the producing model -- AX22-2 forbids "
            f"a model reviewing its own output, and a tally that recorded it would hide the "
            f"violation from the log-review routine that reads this store"
        )


def emit_genai_span(
    system: str,
    request_model: str,
    *,
    operation_name: str = "chat",
    response_model: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cache_write_tokens: int | None = None,
    duration_ms: int | None = None,
    cost_estimated_usd: float | None = None,
    cost_imputed_usd: float | None = None,
    conversation_id: str | None = None,
    finish_reasons: Sequence[str] | None = None,
    lane_id: str | None = None,
    batch_id: str | None = None,
    substrate: str | None = None,
    role: str | None = None,
    outcome: str | None = None,
    reviewed_by: str | None = None,
    error_type: str | None = None,
    events: Sequence[Mapping[str, Any]] | None = None,
    collector: str | None = None,
    db_path: str | os.PathLike[str] | None = None,
    ts: str | None = None,
    run_id: str | None = None,
) -> int | None:
    """Emit one model-call span, OTel-GenAI-shaped per B-1 table 1, and return the exporter's
    result (a row id for the default `at-rest` collector).

    `system` (-> `gen_ai.system`) and `request_model` (-> `gen_ai.request.model`) are required --
    an unattributed span cannot be read back as a model call. Every other field is optional and
    omitted from the attribute dict entirely when `None`, rather than written as a null, so a
    reader sees exactly the facts a caller actually had.

    Standard `gen_ai.*` attributes and the B-1-proposed `devknowledge.*` extensions this builds:

        gen_ai.operation.name, gen_ai.system, gen_ai.request.model, gen_ai.response.model,
        gen_ai.usage.input_tokens, gen_ai.usage.output_tokens, gen_ai.conversation.id,
        gen_ai.response.finish_reasons, error.type (generic OTel, not GenAI-specific)

        devknowledge.gen_ai.usage.cache_read_tokens, devknowledge.gen_ai.usage.cache_write_tokens,
        devknowledge.cost.estimated_usd, devknowledge.cost.imputed_usd, devknowledge.lane_id,
        devknowledge.batch_id, devknowledge.substrate, devknowledge.run_id

    `run_id` ([#565]) defaults to `telemetry_emit.current_run_id()` -- the SAME id a lane's gate
    events carry, not a second one (B-1's own instruction). It rides both the `run_id` column
    (for cheap SQL filtering) and `attributes_json["devknowledge.run_id"]` (so the JSON blob is
    self-contained without a join back to the column).

    `events` (B-1 table 2: `gen_ai.user.message`, `gen_ai.choice`, ...) is opt-in content capture,
    stored verbatim -- this module applies no redaction and no privacy gating; per B-1, that
    posture belongs to the caller, not this schema.

    `collector` resolves through `resolve_exporter()` BEFORE anything is built into a row that
    could be discarded -- a `CollectorNotAvailable` or unknown-target refusal leaves no partial
    write, matching `telemetry_emit.emit_event`'s "refusal leaves no row" discipline.
    """
    if not system or not str(system).strip():
        raise GenAiTelemetryError("system is required (gen_ai.system) -- an unattributed span cannot be read back")
    if not request_model or not str(request_model).strip():
        raise GenAiTelemetryError("request_model is required (gen_ai.request.model)")
    if not operation_name or not str(operation_name).strip():
        raise GenAiTelemetryError("operation_name must be non-empty")
    if run_id is not None and not str(run_id).strip():
        raise GenAiTelemetryError(
            "run_id must be a non-empty string when given explicitly -- a blank id is what a "
            "pre-correlation row would carry, and a new span must not be indistinguishable from one"
        )
    for label, value in (
        ("input_tokens", input_tokens),
        ("output_tokens", output_tokens),
        ("cache_read_tokens", cache_read_tokens),
        ("cache_write_tokens", cache_write_tokens),
        ("duration_ms", duration_ms),
    ):
        _check_int(label, value)
    for label, value in (("cost_estimated_usd", cost_estimated_usd), ("cost_imputed_usd", cost_imputed_usd)):
        _check_number(label, value)

    # `[#691]` AX21-2 / AX22-2 -- the re-rank's three inputs, validated BEFORE the row is
    # built, so a refusal leaves no partial write exactly as the collector refusal below does.
    _check_vocabulary("role", role, ROLES)
    _check_vocabulary("outcome", outcome, CALL_OUTCOMES)
    _check_reviewer_is_not_the_producer(reviewed_by, response_model, request_model)

    # Refuse an unavailable/unknown collector BEFORE building the row -- nothing is written.
    exporter = resolve_exporter(collector, db_path=db_path)

    resolved_run_id = str(run_id) if run_id is not None else _te.current_run_id()

    attrs: dict[str, Any] = {
        "gen_ai.operation.name": str(operation_name),
        "gen_ai.system": str(system),
        "gen_ai.request.model": str(request_model),
    }
    if response_model is not None:
        attrs["gen_ai.response.model"] = str(response_model)
    if input_tokens is not None:
        attrs["gen_ai.usage.input_tokens"] = input_tokens
    if output_tokens is not None:
        attrs["gen_ai.usage.output_tokens"] = output_tokens
    if cache_read_tokens is not None:
        attrs["devknowledge.gen_ai.usage.cache_read_tokens"] = cache_read_tokens
    if cache_write_tokens is not None:
        attrs["devknowledge.gen_ai.usage.cache_write_tokens"] = cache_write_tokens
    if cost_estimated_usd is not None:
        attrs["devknowledge.cost.estimated_usd"] = cost_estimated_usd
    if cost_imputed_usd is not None:
        attrs["devknowledge.cost.imputed_usd"] = cost_imputed_usd
    if conversation_id is not None:
        attrs["gen_ai.conversation.id"] = str(conversation_id)
    if finish_reasons is not None:
        attrs["gen_ai.response.finish_reasons"] = list(finish_reasons)
    if lane_id is not None:
        attrs["devknowledge.lane_id"] = str(lane_id)
    if batch_id is not None:
        attrs["devknowledge.batch_id"] = str(batch_id)
    if substrate is not None:
        attrs["devknowledge.substrate"] = str(substrate)
    if role is not None:
        attrs["devknowledge.role"] = str(role)
    if outcome is not None:
        attrs["devknowledge.outcome"] = str(outcome)
    if reviewed_by is not None:
        attrs["devknowledge.reviewed_by"] = str(reviewed_by)
    if error_type is not None:
        attrs["error.type"] = str(error_type)
    attrs["devknowledge.run_id"] = resolved_run_id

    try:
        # LEG 2, independent of `_check_number`: `allow_nan=False` makes the SERIALISER refuse a
        # non-finite instead of emitting `NaN`/`Infinity`. The validator covers the two cost
        # fields it knows about; this covers every other route into the payload -- a caller's
        # `events` mapping, or a future attribute nobody thought to validate. Two legs, because
        # a validator and a serialiser fail at different times and for different reasons.
        try:
            attributes_json = json.dumps(attrs, sort_keys=True, default=str, allow_nan=False)
            events_json = json.dumps(
                list(events) if events else [], sort_keys=True, default=str, allow_nan=False)
        except ValueError as exc:
            raise GenAiTelemetryError(
                f"span payload carries a non-finite number: {exc} -- it would serialise as a "
                f"non-standard JSON token and be refused by a strict consumer") from exc
    except (TypeError, ValueError) as exc:
        raise GenAiTelemetryError(f"span is not JSON-serializable: {exc}") from exc

    row = {
        "ts": ts or _utc_now_iso(),
        "run_id": resolved_run_id,
        "gen_ai_system": str(system),
        "operation_name": str(operation_name),
        "request_model": str(request_model),
        "response_model": str(response_model) if response_model is not None else None,
        "duration_ms": duration_ms,
        "attributes_json": attributes_json,
        "events_json": events_json,
    }
    return exporter.export(row)


def safe_emit_genai_span(**kwargs: Any) -> int | None:
    """Call `emit_genai_span`, swallowing store/IO failure and returning `None` instead of
    raising. Mirrors `telemetry_emit.safe_emit`'s split exactly: `GenAiTelemetryError` (a wiring
    defect -- missing required field, bad type, unserializable payload) and
    `CollectorNotAvailable` (the seam's own refusal) both propagate, because hiding either would
    make a gap in instrumentation or a silently-added dependency look like a normal event.
    """
    try:
        return emit_genai_span(**kwargs)
    except (sqlite3.Error, OSError):
        return None
