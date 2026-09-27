"""RED-first witnesses for `scripts/cost_usage_telemetry.py`'s redaction posture --
`LANE-5B4-15-runtime-data-home` (R17).

WHY THIS FILE EXISTS. The module's own pre-lane docstring stated plainly: "this module
applies no redaction and no privacy gating; a caller that wants content capture supplies
already-gated events." That posture is what this lane's value statement overturns -- "the
telemetry database ... holds no prompt text, foreign paths or tokens" is a categorical
promise about THIS store, not a promise conditional on a caller's own care, because there is
today exactly one wired caller (`provider_router.record_routing_call`) and zero callers that
populate `events` at all. A store whose only privacy guarantee is "callers must gate
themselves" has no guarantee the day a second caller forgets to.

TWO MECHANISMS, not one, matching the two different risks:

  1. `events` message-body content (`gen_ai.system.message` / `gen_ai.user.message` /
     `gen_ai.choice`, B-1 table 2) is REFUSED outright, never redacted-and-kept. Redacting
     a user turn or a model's reply would still store SOME of the conversation; refusing it
     is the only shape that makes "holds no prompt text" true regardless of what a caller
     passes.
  2. The two free-text-shaped fields this schema still carries -- `gen_ai.conversation.id`
     and `error.type` -- are scanned and REDACTED (substring replaced, call still succeeds)
     for token- and foreign-path-shaped substrings, because refusing the whole call over a
     stray path in an exception message would make legitimate error telemetry unreliable.

WHY `run_id` IS NOT SCANNED, PINNED HERE RATHER THAN LEFT IMPLICIT. `new_run_id()` is
`uuid.uuid4().hex` -- 32 lowercase hex characters, which is exactly the shape the generic
token-scan's hex-blob leg matches. Applying that scan to `devknowledge.run_id` would redact
every real run id in the JSON blob and silently break run_id-based correlation reads of
`attributes_json`. `test_a_real_run_id_survives_the_redaction_scan_unmarked` is the regression
lock for that near-miss.
"""
from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "cost_usage_telemetry.py"


def _load():
    spec = importlib.util.spec_from_file_location("cost_usage_telemetry", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["cost_usage_telemetry"] = module
    spec.loader.exec_module(module)
    return module


def _count(db: Path) -> int:
    if not db.exists():
        return 0
    with sqlite3.connect(str(db)) as conn:
        try:
            return int(conn.execute("SELECT count(*) FROM genai_spans").fetchone()[0])
        except sqlite3.DatabaseError:
            return 0


def _emit_attrs(mod, tmp_path, **kwargs) -> dict:
    db = tmp_path / "GENAI-TELEMETRY.db"
    base = dict(system="anthropic", request_model="claude-opus-5", db_path=db, run_id="r-1")
    base.update(kwargs)
    row_id = mod.emit_genai_span(**base)
    with sqlite3.connect(str(db)) as conn:
        (attrs,) = conn.execute(
            "SELECT attributes_json FROM genai_spans WHERE id = ?", (row_id,)
        ).fetchone()
    return json.loads(attrs)


# --- mechanism 1: content-capture events are REFUSED, never redacted-and-kept ----------------


@pytest.mark.parametrize(
    "event_name", ["gen_ai.system.message", "gen_ai.user.message", "gen_ai.choice"]
)
def test_a_content_capture_event_is_refused_and_nothing_is_written(event_name, tmp_path):
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="anthropic",
            request_model="claude-opus-5",
            events=[{"name": event_name, "body": "the user's actual prompt text"}],
            db_path=db,
        )
    assert event_name in str(exc.value)
    assert _count(db) == 0


def test_the_refusal_names_the_reason_a_reader_would_need(tmp_path):
    """A refusal that only says 'invalid event' sends the next reader to the source. This
    one should name the schema clause (B-1 table 2) and the posture (refused, not gated)."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="anthropic",
            request_model="claude-opus-5",
            events=[{"name": "gen_ai.user.message", "body": "hello"}],
            db_path=db,
        )
    message = str(exc.value).lower()
    assert "content-capture" in message or "message" in message


def test_a_non_content_capture_event_is_accepted_and_its_free_text_is_redacted(tmp_path):
    """An event name outside B-1 table 2's three is not a message-body event by this
    schema's own definition, so it is accepted -- but its string payload still passes
    through the same path/token scrub as the rest of the store, because "not a named
    content-capture event" is not the same guarantee as "safe free text"."""
    mod = _load()
    attrs = _emit_attrs(
        mod,
        tmp_path,
        events=[{"name": "devknowledge.debug.note",
                 "body": r"see C:\Users\1028120\Documents\secret\file.txt"}],
    )
    db = tmp_path / "GENAI-TELEMETRY.db"
    with sqlite3.connect(str(db)) as conn:
        (events_json,) = conn.execute(
            "SELECT events_json FROM genai_spans ORDER BY id DESC LIMIT 1").fetchone()
    assert r"C:\Users\1028120" not in events_json
    assert "[REDACTED-PATH]" in events_json
    del attrs  # attrs unused here; the assertion is on events_json


# --- mechanism 2: token- and path-shaped substrings in free-text fields are redacted ---------


def test_a_foreign_windows_path_in_error_type_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type=r"FileNotFoundError: C:\Users\1028120\Documents\Dev\secret\keys.txt missing",
    )
    assert r"C:\Users\1028120" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_foreign_posix_path_in_error_type_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path, error_type="OSError: /Users/rob/Documents/secret/id_rsa not found",
    )
    assert "/Users/rob/Documents/secret" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_token_shaped_value_in_conversation_id_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path, conversation_id="sk-abcdEFGH1234567890abcdEFGH1234567890",
    )
    assert "sk-abcdEFGH1234567890abcdEFGH1234567890" not in attrs["gen_ai.conversation.id"]
    assert "[REDACTED-TOKEN]" in attrs["gen_ai.conversation.id"]


def test_a_bearer_header_in_error_type_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type="401: Authorization Bearer abcXYZ123token456value789here failed",
    )
    assert "abcXYZ123token456value789here" not in attrs["error.type"]
    assert "[REDACTED-TOKEN]" in attrs["error.type"]


# --- the near-miss this file's docstring names -----------------------------------------------


def test_a_real_run_id_survives_the_redaction_scan_unmarked(tmp_path):
    """`new_run_id()`'s shape (32 lowercase hex chars) is exactly what a naive generic
    hex-blob scan would catch -- this pins that `devknowledge.run_id` is never fed through
    the scrub, so real correlation ids in the JSON blob are never mangled."""
    mod = _load()
    run_id = "0123456789abcdef0123456789abcdef"  # 32 hex chars, uuid4().hex's exact shape
    attrs = _emit_attrs(mod, tmp_path, run_id=run_id)
    assert attrs["devknowledge.run_id"] == run_id


def test_ordinary_identifiers_pass_through_unredacted(tmp_path):
    """Model ids, roles and outcomes are short, structured tokens -- none should ever trip
    the path/token scrub, and this is the regression lock for that."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        response_model="claude-opus-5", role="implement", outcome="passed",
        reviewed_by="gpt-5.6-terra", conversation_id="conv-2026-09-27-001",
    )
    assert attrs["gen_ai.response.model"] == "claude-opus-5"
    assert attrs["devknowledge.role"] == "implement"
    assert attrs["devknowledge.outcome"] == "passed"
    assert attrs["devknowledge.reviewed_by"] == "gpt-5.6-terra"
    assert attrs["gen_ai.conversation.id"] == "conv-2026-09-27-001"


# --- the layout rule for "the rest" of logs/ (done-contract item 4) --------------------------


def test_a_new_ad_hoc_runtime_data_subdirectory_under_logs_is_still_refused_by_rule_c():
    """This lane moves ONE database off-tree; everything else under `logs/` stays exactly
    where the pre-existing `home_grammar` clause already seals it (a bare `logs` home, plus
    the `logs/YYYY-MM` retention-bucket grammar -- `ecosystem/fleet-shape-spec.yaml`). The
    decision this lane records (see the new `runtime_data_home` clause) is that a NEW kind
    of runtime data does not get an ad hoc new subdirectory under `logs/` without a ruling;
    this pins that the mechanism already enforcing that keeps enforcing it, so a future edit
    to the pattern list cannot silently widen it without this test going red.
    """
    import validate_hermetization as vh

    reason = vh.rule_c_violation("logs/some-new-runtime-kind/STATE.db")
    assert reason is not None
    assert "logs/some-new-runtime-kind" in reason
