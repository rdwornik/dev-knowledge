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

THE STORE'S HOME AND ITS REDACTION POSTURE (`LANE-5B4-15-runtime-data-home`, R17 -- placement
of the harness's runtime data researched against industry practice; full decision recorded in
`to-browser/SESSION-lane-runtime-data-home.md`). Two changes from this module's original
shape, both because this store can carry per-call detail a public, git-tracked repo must
never hold:

  1. THE STORE LIVES OUTSIDE THE REPOSITORY ENTIRELY, not merely gitignored inside it.
     `default_db_path()` resolves a per-user OS state directory via `platformdirs` (already
     resolved in `uv.lock`, no new dependency), following the same convention every major
     packaging/dev tool uses for local, non-portable runtime state (pip's cache, npm's
     `~/.npm`, `platformdirs`' own `user_state_dir` -- XDG's `$XDG_STATE_HOME` names exactly
     this class: "logs, history, ... action history"). Gitignoring in place only stops an
     accidental `git add`; a path that is never inside the working tree cannot reach origin
     by ANY route -- a stray `git add -f`, a zipped-up repo folder for a bug report, a
     `.gitignore` typo -- which is the stronger guarantee the value statement promises.
  2. THE STORE REFUSES RAW MESSAGE-BODY CONTENT AND REDACTS PATH/TOKEN-SHAPED FREE TEXT.
     Superseding this docstring's original claim ("this module applies no redaction and no
     privacy gating; ... that posture belongs to the caller"): with exactly one wired caller
     today (`provider_router.record_routing_call`, which passes no `events`) and zero callers
     that populate `events`, a guarantee conditional on every future caller's own care is no
     guarantee. See `_check_events_are_permitted` and `_redact_string` below for the two
     mechanisms, and `tests/test_telemetry_redaction.py` for the RED-first proof of both.

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
import re
import sqlite3
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import platformdirs

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

#: The store's filename. UPPERCASE-KEBAB stem per the 2026-07-22 `logs/` naming ruling
#: (CLAUDE.md section 9); `.db` stays honest to the format. No longer a repo-relative path
#: (see `default_db_path()`, `LANE-5B4-15-runtime-data-home`) -- kept as a bare filename so
#: the naming ruling still applies to the one thing that travelled off-tree with it.
DB_FILENAME = "GENAI-TELEMETRY.db"

#: The per-user OS state directory's app identity (`platformdirs`). Not literally the repo's
#: directory name -- a stable identity independent of where this checkout happens to sit on
#: disk, so a renamed or re-cloned working copy still finds the SAME store. `appauthor=False`
#: (below) avoids `platformdirs`' default `<author>/<app>` doubling on Windows when the two
#: are identical, which is this repo's case: measured 2026-09-27, `user_state_dir("dev-
#: knowledge")` alone resolves `...\AppData\Local\dev-knowledge\dev-knowledge`.
_APP_NAME = "dev-knowledge"

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
#: filter by system/model/run. `events_json` carries only events whose name is on this store's
#: (currently empty) permitted-events allowlist -- deny-by-default, so B-1 table 2's
#: message-body events and everything else are REFUSED before a row is built
#: (`_check_events_are_permitted`, `LANE-5B4-15-runtime-data-home`). Every string value this
#: module writes is scrubbed for token- and foreign-path-shaped substrings (`_redact_string`)
#: before serialization -- the free-text field (`error.type`) with the full scrub, the
#: identifier fields (`gen_ai.conversation.id`, `devknowledge.run_id`) with the narrower one
#: that never touches a legitimate UUID-/hash-shaped value.
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
    """The store location: `$DEV_KNOWLEDGE_GENAI_TELEMETRY_DB` if set, else a per-user OS
    state directory (`platformdirs.user_state_dir`), never a path inside any repository.

    `LANE-5B4-15-runtime-data-home` (R17) moved this off-tree entirely -- superseding the
    original `<repo>/logs/GENAI-TELEMETRY.db` (`telemetry_emit.repo_root()`-relative) shape.
    Full decision (industry-practice research, options, thesis-method matrix):
    `to-browser/SESSION-lane-runtime-data-home.md`.

    THIS IS ALSO A BUG FIX, not merely a relocation. The old shape resolved PER WORKTREE
    (`repo_root()` answers `--show-toplevel`, which is the calling worktree's own root, not
    the primary checkout's) -- the exact class of defect `telemetry_emit.default_db_path()`
    was already fixed for (see that function's own docstring: a per-worktree counter store
    "dies with `git worktree remove`", wrong for data a fleet-wide read needs to survive it).
    `record_routing_call`'s re-rank needs the SAME cross-lane continuity `[#565]`'s run_id
    correlation assumes; a per-user, non-git-derived path shares one file across the primary
    checkout and every linked worktree with no git dependency at all, which is a STRONGER
    fix than reusing `telemetry_emit.common_repo_root()` would have been (that resolver can
    still answer differently across two clones of the same remote on one machine; this one
    cannot fail to resolve at all, since it asks the OS, never git).
    """
    override = os.environ.get(DB_PATH_ENV)
    if override:
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME, appauthor=False)) / DB_FILENAME


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
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


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


# --- redaction (`LANE-5B4-15-runtime-data-home`, R17) ----------------------------------------
# Two mechanisms for two different risks -- see the module docstring's "STORE'S HOME AND ITS
# REDACTION POSTURE" section for the reasoning, and `tests/test_telemetry_redaction.py` for the
# RED-first proof of each. Both legs were tightened after a Codex terra review of this lane's
# first cut (`docs/audits/2026-09-27-codex-lane-runtime-data-home.md`, 3 Critical + 1 High) --
# see each fix's own comment below for the finding it closes.

#: `events` NAMES THIS STORE ADMITS -- empty today, DENY-BY-DEFAULT. Codex terra CRITICAL:
#: the original shape refused only B-1 table 2's three named message-body events and ACCEPTED
#: everything else verbatim, which is trivially bypassed by ordinary prose under any other
#: event name (prose matches neither the path nor the token regex, so nothing would have
#: caught it). With zero wired callers populating `events` today, there is no legitimate name
#: to admit yet -- refusing every event is not a stopgap, it is the only shape that makes
#: "holds no prompt text" true regardless of what a caller passes. A future content-capture
#: design that has actually reviewed its own gating adds its event name here, deliberately.
_PERMITTED_EVENT_NAMES: frozenset[str] = frozenset()

#: The one attribute this schema carries that is FREE TEXT rather than a controlled
#: identifier/enum/number -- every other attribute (`system`, `*.model`, `role`, `outcome`,
#: `conversation.id`, `run_id`, ...) is a short structured IDENTIFIER by construction, so a
#: blanket free-text scrub of any of them risks corrupting a legitimate correlation value for
#: no real gain (see `_IDENTIFIER_ATTR_KEYS` below for the narrower scrub those still get).
#: `error.type` is the one field a caller is likely to populate from a real exception's
#: `str()`, which is exactly where a stray absolute path or an accidentally-embedded
#: credential would leak in.
_FREE_TEXT_ATTR_KEYS: frozenset[str] = frozenset({"error.type"})

#: Identifier-shaped attributes: legitimately UUID-/hash-shaped values (a real
#: `gen_ai.conversation.id`, a caller-supplied `run_id`) that must not be torn up by the
#: generic hex-blob catch-all below, but that still deserve the NAMED-secret and path legs --
#: a caller could still misuse an identifier field to smuggle a recognisably-shaped credential.
#: See `_redact_string`'s `scan_generic_hex` parameter.
_IDENTIFIER_ATTR_KEYS: frozenset[str] = frozenset({"gen_ai.conversation.id"})

#: Foreign-path patterns. No typed field in this schema is ever meant to carry a filesystem
#: path -- model ids, roles, outcomes and run ids are all short identifiers by design -- so a
#: path-shaped substring appearing in one means content leaked in by accident (an exception
#: message, a stray f-string), never a legitimate value to preserve. Codex terra CRITICAL: the
#: original POSIX/UNC coverage was an enumerated allowlist of top-level directory names
#: (`/home`, `/Users`, ...) that missed ordinary absolute paths (`/workspaces/...`,
#: `/srv/...`, `/data/...`) and every UNC share (`\\server\share\...`) outright. Both are now
#: general shape matches -- any absolute path of two or more segments, not a fixed name list.
_WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*")
_UNC_PATH_RE = re.compile(r"\\\\[^\\\s\"'<>]+\\[^\\\s\"'<>]+(?:\\[^\\\s\"'<>]+)*")
_POSIX_PATH_RE = re.compile(r"(?<![\w./])/[^\s\"'<>]+/[^\s\"'<>]*")

#: NAMED vendor API-key / bearer-header shapes -- unambiguous enough to apply everywhere,
#: including to an identifier field, because no legitimate UUID or hash could accidentally
#: match one of these prefixes.
_NAMED_TOKEN_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[A-Za-z0-9_-]{20,}|"
    r"Bearer\s+[A-Za-z0-9._-]{10,})\b"
)

#: A bare 32+-character hex run, as a generic catch-all -- but ONLY for genuinely free-text
#: fields (`error.type`, an accepted event's own strings), never for an identifier field.
#: Codex terra CRITICAL + HIGH: applying this to `gen_ai.conversation.id` (HIGH) and to a
#: caller-supplied `run_id` (CRITICAL, since only the auto-generated id was exempted, not a
#: caller-supplied one of the same shape) silently destroys real UUID-hex correlation values
#: -- the exact defect `test_a_real_run_id_survives_the_redaction_scan_unmarked` was written
#: to catch, and did not catch, because it only exercised the auto-generated path. Both fields
#: now route through `_IDENTIFIER_ATTR_KEYS`/`run_id`'s own dedicated call with
#: `scan_generic_hex=False` instead of being scrubbed as free text.
_GENERIC_HEX_BLOB_RE = re.compile(r"\b[A-Fa-f0-9]{32,}\b")

_PATH_REDACTION = "[REDACTED-PATH]"
_TOKEN_REDACTION = "[REDACTED-TOKEN]"


def _redact_string(value: str, *, scan_generic_hex: bool = True) -> str:
    """Scrub path- and token-shaped substrings from one string, in place semantics (returns
    the scrubbed copy). Order matters: paths first, so a token pattern cannot partially
    consume a path substring and leave a mangled remainder for the path regex to miss.
    `scan_generic_hex=False` (identifier fields) skips only the bare-hex-blob catch-all;
    named vendor-token shapes and paths are still scrubbed everywhere."""
    value = _WINDOWS_PATH_RE.sub(_PATH_REDACTION, value)
    value = _UNC_PATH_RE.sub(_PATH_REDACTION, value)
    value = _POSIX_PATH_RE.sub(_PATH_REDACTION, value)
    value = _NAMED_TOKEN_RE.sub(_TOKEN_REDACTION, value)
    if scan_generic_hex:
        value = _GENERIC_HEX_BLOB_RE.sub(_TOKEN_REDACTION, value)
    return value


def _redact_json_value(value: Any) -> Any:
    """Recursively scrub every string leaf of a JSON-shaped value (dict/list/scalar) -- the
    shape an accepted `events` payload arrives in, once `_check_events_are_permitted` has
    already refused everything not on `_PERMITTED_EVENT_NAMES`."""
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, list):
        return [_redact_json_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _redact_json_value(v) for k, v in value.items()}
    return value


def _check_events_are_permitted(events: Sequence[Mapping[str, Any]] | None) -> None:
    """Refuse (raise, nothing written) any event whose `name` is not on
    `_PERMITTED_EVENT_NAMES` -- deny-by-default, not an allowlist of refused names (see that
    constant's own comment for why). A non-mapping event, or one with no `name` at all, is
    refused the same way: an event this module cannot identify is not one it can vouch for.
    Checked BEFORE the row is built, matching every other refusal in this module -- a
    half-written span is worse than none."""
    if not events:
        return
    for event in events:
        name = event.get("name") if isinstance(event, Mapping) else None
        if name not in _PERMITTED_EVENT_NAMES:
            raise GenAiTelemetryError(
                f"event {name!r} is not on this store's permitted-events list "
                f"({sorted(_PERMITTED_EVENT_NAMES) or 'currently empty'}) -- this store "
                f"refuses an unrecognised event by default rather than accepting-and-scrubbing "
                f"it, because ordinary prose matches neither the path nor the token redaction "
                f"pattern and would otherwise pass through verbatim; admit a name here only "
                f"once its content-capture shape has actually been reviewed"
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

    `events` is REFUSED unless every entry's `name` is on `_PERMITTED_EVENT_NAMES` (currently
    empty -- deny-by-default, not an allowlist of refused names; see that constant's own
    comment) -- `_check_events_are_permitted`, checked before anything else is built. `error_type`
    is scrubbed for path- and token-shaped substrings before serialization (`_redact_string`);
    `conversation_id` and `run_id` get the narrower identifier-safe scrub that never touches a
    legitimate UUID-/hash-shaped value (`scan_generic_hex=False`). See the module docstring's
    "STORE'S HOME AND ITS REDACTION POSTURE" section for why this superseded the original
    caller-gates-itself posture.

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

    # `LANE-5B4-15-runtime-data-home` (R17) -- refuse an event whose name is not permitted
    # BEFORE the row is built, same discipline as every refusal above.
    _check_events_are_permitted(events)

    # Refuse an unavailable/unknown collector BEFORE building the row -- nothing is written.
    exporter = resolve_exporter(collector, db_path=db_path)

    # Identifier-shaped, not free text -- `scan_generic_hex=False` so a legitimate
    # `uuid.uuid4().hex` (the auto-generated case) or a well-formed caller-supplied id passes
    # through unchanged; only a recognisably-shaped named secret or path embedded in a
    # CALLER-SUPPLIED run_id is scrubbed (Codex terra CRITICAL -- the original exemption
    # covered every run_id unconditionally, including a caller-supplied one carrying real
    # content, not merely the auto-generated uuid4 case
    # `test_a_real_run_id_survives_the_redaction_scan_unmarked` actually exercised).
    resolved_run_id = _redact_string(
        str(run_id) if run_id is not None else _te.current_run_id(), scan_generic_hex=False
    )

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
        # Identifier-shaped, not free text -- see `_IDENTIFIER_ATTR_KEYS`'s own comment for
        # why this is redacted with `scan_generic_hex=False` below rather than swept as prose.
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

    # `LANE-5B4-15-runtime-data-home` (R17) -- scrub free-text attributes for path-/
    # token-shaped substrings (full scrub, including the generic hex-blob catch-all) and
    # identifier attributes more narrowly (named tokens + paths, never the hex-blob catch-all
    # -- see `_IDENTIFIER_ATTR_KEYS`'s own comment). AFTER the dict is built (so every other
    # key, including `devknowledge.run_id`, which was already redacted at the identifier
    # level above, stays untouched) and BEFORE serialization.
    for key in _FREE_TEXT_ATTR_KEYS:
        if key in attrs and isinstance(attrs[key], str):
            attrs[key] = _redact_string(attrs[key])
    for key in _IDENTIFIER_ATTR_KEYS:
        if key in attrs and isinstance(attrs[key], str):
            attrs[key] = _redact_string(attrs[key], scan_generic_hex=False)
    redacted_events = _redact_json_value(list(events) if events else [])

    try:
        # LEG 2, independent of `_check_number`: `allow_nan=False` makes the SERIALISER refuse a
        # non-finite instead of emitting `NaN`/`Infinity`. The validator covers the two cost
        # fields it knows about; this covers every other route into the payload -- a caller's
        # `events` mapping, or a future attribute nobody thought to validate. Two legs, because
        # a validator and a serialiser fail at different times and for different reasons.
        try:
            attributes_json = json.dumps(attrs, sort_keys=True, default=str, allow_nan=False)
            events_json = json.dumps(
                redacted_events, sort_keys=True, default=str, allow_nan=False)
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
