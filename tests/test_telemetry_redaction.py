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

THIS FILE'S SECOND PASS, after a Codex terra review of the first cut found 3 Critical + 1
High (`docs/audits/2026-09-27-codex-lane-runtime-data-home.md`):

  - CRITICAL: refusing only B-1 table 2's three NAMED events and accepting everything else
    verbatim is trivially bypassed -- ordinary prose under any other event name matches
    neither the path nor the token regex. Fixed by flipping to DENY-BY-DEFAULT: `events` is
    refused unless its name is on `_PERMITTED_EVENT_NAMES`, currently empty.
  - CRITICAL: the path regexes were an enumerated allowlist of top-level directory names and
    missed ordinary absolute paths / UNC shares. Fixed by broadening to a general shape match.
  - CRITICAL + HIGH: excluding `devknowledge.run_id` from ALL redaction, and applying the
    generic hex-blob catch-all to `gen_ai.conversation.id`, are two sides of one mistake --
    identifier fields need the NAMED-token and path legs (a caller could still misuse an id
    field to smuggle a recognisable secret) but must never lose the generic hex-blob leg,
    which is exactly what a legitimate UUID/hash-shaped identifier looks like. Fixed by a
    `scan_generic_hex=False` mode applied to both fields uniformly, rather than an
    unconditional run_id exemption paired with an unconditional conversation_id sweep.

THIS FILE'S THIRD PASS, after a Codex terra FOLLOW-UP review of the round-2 fixes found 3
MORE Critical (`docs/audits/2026-09-27-codex-lane-runtime-data-home-followup.md`; the
deny-by-default and identifier-split fixes above were confirmed resolved):

  - CRITICAL: only `error.type` was on the scrubbed-field allowlist -- `lane_id`, `batch_id`,
    `reviewed_by`, `finish_reasons` and every other attribute were serialized with NO scrub at
    all. Fixed the same way `events` was: scrub is now the DEFAULT for every attribute, with
    the two identifier fields as the (narrower-scrub, not no-scrub) exemption.
  - CRITICAL: the path regexes stopped each segment at the first whitespace, so a real path
    with an embedded space (a "Rob Smith"-style directory name) redacted only its first word.
    Fixed by letting `_PATH_SEGMENT` tolerate a few embedded spaces per segment.
  - CRITICAL: `_NAMED_TOKEN_RE`'s `Bearer` match was case-sensitive, though the HTTP scheme
    name is not (RFC 9110 SS11.6.2) -- `bearer`/`BEARER` sailed through unredacted. Fixed with
    a scoped case-insensitive group, `(?i:bearer)`.

TWO MECHANISMS, not one, matching the two different risks:

  1. `events` is refused unless every entry's `name` is on `_PERMITTED_EVENT_NAMES`
     (deny-by-default, currently empty -- no legitimate name exists yet with zero real
     callers). Refused, never redacted-and-kept: redacting a user turn would still store
     SOME of the conversation, and refusing is the only shape that makes "holds no prompt
     text" true regardless of what a caller passes.
  2. Every other attribute is scanned and REDACTED (substring replaced, call still succeeds)
     for token- and foreign-path-shaped substrings by DEFAULT -- full scrub, except the two
     identifier-shaped fields (`gen_ai.conversation.id`, `devknowledge.run_id`), which get the
     narrower scrub (no generic hex-blob leg) that never touches a legitimate UUID-/hash-shaped
     value.
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


def _emit_row(mod, tmp_path, **kwargs) -> dict:
    """Like `_emit_attrs`, but returns every DENORMALISED column too -- the CRITICAL fix below
    (repair 1) needs the raw `gen_ai_system` / `operation_name` / `request_model` /
    `response_model` columns, not the `attributes_json` copy `_emit_attrs` reads."""
    db = tmp_path / "GENAI-TELEMETRY.db"
    base = dict(system="anthropic", request_model="claude-opus-5", db_path=db, run_id="r-1")
    base.update(kwargs)
    row_id = mod.emit_genai_span(**base)
    with sqlite3.connect(str(db)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM genai_spans WHERE id = ?", (row_id,)).fetchone()
    return dict(row)


# --- mechanism 1: events are refused unless explicitly permitted (deny-by-default) -----------


@pytest.mark.parametrize(
    "event_name", ["gen_ai.system.message", "gen_ai.user.message", "gen_ai.choice"]
)
def test_a_b1_content_capture_event_is_refused_and_nothing_is_written(event_name, tmp_path):
    """The three names B-1 table 2 documents are refused -- same as every other name, since
    the set they'd need to be on is empty; not a special case, a consequence of the default."""
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


def test_an_arbitrary_unlisted_event_name_is_also_refused_deny_by_default(tmp_path):
    """THE CRITICAL FIX. Pre-fix, an event under any name other than the three B-1 names was
    ACCEPTED verbatim -- ordinary prose here would have sailed straight past both redaction
    regexes with nothing to catch it. Deny-by-default means there is no such gap: an event is
    refused unless its name is explicitly permitted, and the permitted set is empty today."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="anthropic",
            request_model="claude-opus-5",
            events=[{"name": "devknowledge.debug.note",
                     "body": "this is ordinary prose that no redaction regex would ever catch"}],
            db_path=db,
        )
    assert "devknowledge.debug.note" in str(exc.value)
    assert _count(db) == 0


def test_a_non_mapping_event_is_refused_rather_than_silently_admitted(tmp_path):
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError):
        mod.emit_genai_span(
            system="anthropic", request_model="claude-opus-5",
            events=["a bare string, not a mapping"], db_path=db,
        )
    assert _count(db) == 0


def test_the_refusal_names_the_reason_a_reader_would_need(tmp_path):
    """A refusal that only says 'invalid event' sends the next reader to the source."""
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
    assert "permitted-events" in message
    assert "content-capture" in message


def test_admitting_a_name_lets_it_through_and_its_free_text_is_still_redacted(tmp_path, monkeypatch):
    """The OTHER half of deny-by-default: a name that IS on `_PERMITTED_EVENT_NAMES` is
    accepted, and its strings still pass through the same path/token scrub as everything
    else in the store -- admission is not the same as trusting the payload's content."""
    mod = _load()
    monkeypatch.setattr(mod, "_PERMITTED_EVENT_NAMES", frozenset({"devknowledge.debug.note"}))
    db = tmp_path / "GENAI-TELEMETRY.db"
    mod.emit_genai_span(
        system="anthropic", request_model="claude-opus-5",
        events=[{"name": "devknowledge.debug.note",
                 "body": r"see C:\Users\1028120\Documents\secret\file.txt"}],
        db_path=db,
    )
    with sqlite3.connect(str(db)) as conn:
        (events_json,) = conn.execute(
            "SELECT events_json FROM genai_spans ORDER BY id DESC LIMIT 1").fetchone()
    assert r"C:\Users\1028120" not in events_json
    assert "[REDACTED-PATH]" in events_json


# --- mechanism 2: token- and path-shaped substrings in free-text fields are redacted ---------


def test_every_string_attribute_is_scrubbed_by_default_not_an_explicit_allowlist(tmp_path):
    """THE CRITICAL FIX (round 2). Pre-fix, only `error.type` was scrubbed (an explicit
    allowlist, `_FREE_TEXT_ATTR_KEYS`) -- `lane_id`, `batch_id`, `reviewed_by`, and
    `finish_reasons` (a list-valued attribute) were serialized with NO scrub at all, so a
    caller passing a foreign path or a named token through any of THOSE fields sailed straight
    into the store. Scrubbing is now the default for every attribute except the two
    identifier-shaped ones; a new field this module adds tomorrow inherits the scrub without
    anyone having to remember to add it to a list."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        lane_id=r"C:\Users\1028120\Documents\Dev\secret\lane-notes.txt",
        batch_id="sk-abcdEFGH1234567890abcdEFGH1234567890",
        reviewed_by=r"/workspaces/dev-knowledge/secret/reviewer-notes.txt",
        finish_reasons=[r"C:\Users\1028120\Documents\Dev\secret\reason.txt", "stop"],
    )
    assert r"C:\Users\1028120" not in attrs["devknowledge.lane_id"]
    assert "[REDACTED-PATH]" in attrs["devknowledge.lane_id"]
    assert "sk-abcdEFGH1234567890abcdEFGH1234567890" not in attrs["devknowledge.batch_id"]
    assert "[REDACTED-TOKEN]" in attrs["devknowledge.batch_id"]
    assert "/workspaces/dev-knowledge/secret" not in attrs["devknowledge.reviewed_by"]
    assert "[REDACTED-PATH]" in attrs["devknowledge.reviewed_by"]
    assert r"C:\Users\1028120" not in attrs["gen_ai.response.finish_reasons"][0]
    assert "[REDACTED-PATH]" in attrs["gen_ai.response.finish_reasons"][0]
    assert attrs["gen_ai.response.finish_reasons"][1] == "stop"


def test_a_foreign_windows_path_in_error_type_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type=r"FileNotFoundError: C:\Users\1028120\Documents\Dev\secret\keys.txt missing",
    )
    assert r"C:\Users\1028120" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


@pytest.mark.parametrize("path", [
    "/Users/rob/Documents/secret/id_rsa",
    "/home/rob/.ssh/id_rsa",
    "/workspaces/dev-knowledge/secret/keys.txt",
    "/srv/app/config/secrets.yaml",
    "/data/private/dump.sql",
    "/usr/local/etc/app/secret.conf",
])
def test_a_foreign_posix_path_in_error_type_is_redacted(path, tmp_path):
    """THE CRITICAL FIX. Pre-fix, the POSIX matcher was an enumerated allowlist of top-level
    directory names (home/Users/root/etc/var/tmp/opt/mnt) and missed ordinary absolute paths
    like `/workspaces/...`, `/srv/...` and `/data/...` outright -- this is now a general
    shape match (any absolute path of 2+ segments), not a fixed name list."""
    mod = _load()
    attrs = _emit_attrs(mod, tmp_path, error_type=f"OSError: {path} not found")
    assert path not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_unc_path_in_error_type_is_redacted(tmp_path):
    """THE CRITICAL FIX (UNC leg). Pre-fix, a Windows network share had no matcher at all."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type=r"PermissionError: \\fileserver\share\secret\data.csv denied",
    )
    assert r"\\fileserver\share\secret" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_posix_path_with_an_embedded_space_is_fully_redacted(tmp_path):
    """THE CRITICAL FIX (round 2). Pre-fix, the POSIX/UNC matchers stopped at the first
    whitespace, so a real path with a space in a directory name -- "Rob Smith", a common
    Windows-share-mapped-as-POSIX shape -- redacted only its first word and left the rest
    (username, share name, secret suffix) in the clear. `_PATH_SEGMENT` now tolerates a few
    embedded spaces per segment."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type="OSError: /Users/Rob Smith/private/secret-key.pem not found",
    )
    assert "Rob Smith" not in attrs["error.type"]
    assert "secret-key.pem" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_unc_path_with_an_embedded_space_is_fully_redacted(tmp_path):
    """THE CRITICAL FIX (round 2), UNC leg -- same gap, a network share name with a space."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type=r"PermissionError: \\fileserver\Team Share\secret\data.csv denied",
    )
    assert "Team Share" not in attrs["error.type"]
    assert r"\secret\data.csv" not in attrs["error.type"]
    assert "[REDACTED-PATH]" in attrs["error.type"]


def test_a_bearer_header_in_error_type_is_redacted(tmp_path):
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type="401: Authorization Bearer abcXYZ123token456value789here failed",
    )
    assert "abcXYZ123token456value789here" not in attrs["error.type"]
    assert "[REDACTED-TOKEN]" in attrs["error.type"]


@pytest.mark.parametrize("scheme", ["bearer", "BEARER", "BeArEr"])
def test_a_lowercase_or_mixed_case_bearer_header_is_also_redacted(scheme, tmp_path):
    """THE CRITICAL FIX (round 2). Pre-fix, `_NAMED_TOKEN_RE` matched only capitalized
    `Bearer`, but RFC 9110 SS11.6.2 makes the HTTP auth scheme name case-insensitive -- a real
    `bearer <token>` or `BEARER <token>` header is exactly as real as `Bearer <token>` and was
    passing through unredacted."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path,
        error_type=f"401: Authorization {scheme} abcXYZ123token456value789here failed",
    )
    assert "abcXYZ123token456value789here" not in attrs["error.type"]
    assert "[REDACTED-TOKEN]" in attrs["error.type"]


def test_a_named_token_shaped_value_in_conversation_id_is_redacted(tmp_path):
    """A named vendor-key SHAPE is unambiguous enough to redact even in an identifier field
    -- no legitimate UUID or hash could accidentally match an `sk-...` prefix."""
    mod = _load()
    attrs = _emit_attrs(
        mod, tmp_path, conversation_id="sk-abcdEFGH1234567890abcdEFGH1234567890",
    )
    assert "sk-abcdEFGH1234567890abcdEFGH1234567890" not in attrs["gen_ai.conversation.id"]
    assert "[REDACTED-TOKEN]" in attrs["gen_ai.conversation.id"]


def test_a_named_token_in_an_explicit_run_id_is_still_redacted(tmp_path):
    """THE CRITICAL FIX. Pre-fix, `run_id` was excluded from redaction UNCONDITIONALLY, which
    covered the auto-generated uuid4 case but also silently exempted a CALLER-SUPPLIED run_id
    carrying a real, recognisably-shaped secret. Named-token shapes are still caught in an
    identifier field; only the generic hex-blob catch-all is skipped for it."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    mod.emit_genai_span(
        system="anthropic", request_model="claude-opus-5",
        run_id="Bearer abcXYZ123token456value789here", db_path=db,
    )
    with sqlite3.connect(str(db)) as conn:
        (run_id_col, attrs_json) = conn.execute(
            "SELECT run_id, attributes_json FROM genai_spans ORDER BY id DESC LIMIT 1"
        ).fetchone()
    assert "abcXYZ123token456value789here" not in run_id_col
    assert "[REDACTED-TOKEN]" in run_id_col
    assert "abcXYZ123token456value789here" not in attrs_json
    assert "[REDACTED-TOKEN]" in json.loads(attrs_json)["devknowledge.run_id"]


# --- the near-misses this file exists to pin --------------------------------------------------


def test_a_real_run_id_survives_the_redaction_scan_unmarked(tmp_path):
    """`new_run_id()`'s shape (32 lowercase hex chars) is exactly what the generic hex-blob
    scan would catch -- this pins that `devknowledge.run_id` is scrubbed with
    `scan_generic_hex=False` (never the hex-blob leg), so a real, well-formed correlation id
    is never mangled."""
    mod = _load()
    run_id = "0123456789abcdef0123456789abcdef"  # 32 hex chars, uuid4().hex's exact shape
    attrs = _emit_attrs(mod, tmp_path, run_id=run_id)
    assert attrs["devknowledge.run_id"] == run_id


def test_a_hash_shaped_conversation_id_survives_unredacted(tmp_path):
    """THE HIGH-SEVERITY FIX. Pre-fix, ANY 32+ hex-char substring in `conversation_id` was
    replaced by the generic catch-all -- silently destroying a legitimate UUID-hex or hash
    correlation id, which is exactly the shape a real `gen_ai.conversation.id` takes. Now
    scrubbed with `scan_generic_hex=False`, matching `run_id`'s own treatment."""
    mod = _load()
    conv_id = "a1b2c3d4e5f60718293a4b5c6d7e8f90"  # 32 hex chars, a plausible real conv id
    attrs = _emit_attrs(mod, tmp_path, conversation_id=conv_id)
    assert attrs["gen_ai.conversation.id"] == conv_id


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


# --- the denormalised columns get the same scrub as their `attrs` JSON siblings --------------
# Codex terra CRITICAL (repair 1, docs/audits/2026-09-29-codex-codex-lane-runtime-data-home-2.md
# @ e8679b3a): `attributes_json` was scrubbed, but `gen_ai_system`, `operation_name`,
# `request_model` and `response_model` were inserted from the ORIGINAL unredacted call
# arguments -- a secret- or foreign-path-shaped value supplied through any of those four
# public string parameters reached the database verbatim despite the redaction guarantee.


def test_a_foreign_path_in_gen_ai_system_is_redacted_in_the_denormalised_column(tmp_path):
    mod = _load()
    path = "/Users/rob/Documents/secret/id_rsa"
    row = _emit_row(mod, tmp_path, system=f"anthropic {path}")
    assert path not in row["gen_ai_system"]
    assert "[REDACTED-PATH]" in row["gen_ai_system"]


def test_a_named_token_in_operation_name_is_redacted_in_the_denormalised_column(tmp_path):
    mod = _load()
    row = _emit_row(mod, tmp_path, operation_name="chat sk-abcdEFGH1234567890abcdEFGH1234567890")
    assert "sk-abcdEFGH1234567890abcdEFGH1234567890" not in row["operation_name"]
    assert "[REDACTED-TOKEN]" in row["operation_name"]


def test_a_foreign_path_in_request_model_is_redacted_in_the_denormalised_column(tmp_path):
    mod = _load()
    row = _emit_row(mod, tmp_path, request_model=r"claude-opus-5 \\fileserver\Team Share\secret\data.csv")
    assert "Team Share" not in row["request_model"]
    assert "[REDACTED-PATH]" in row["request_model"]


def test_a_named_token_in_response_model_is_redacted_in_the_denormalised_column(tmp_path):
    mod = _load()
    row = _emit_row(
        mod, tmp_path, response_model="claude-opus-5 ghp_ABCDEFGHIJ1234567890abcdefgh",
    )
    assert "ghp_ABCDEFGHIJ1234567890abcdefgh" not in row["response_model"]
    assert "[REDACTED-TOKEN]" in row["response_model"]


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
