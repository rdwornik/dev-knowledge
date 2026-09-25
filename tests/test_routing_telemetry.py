"""RED-first witnesses for the routing half of the model-call tally — AX21-2 / AX5-1.

WHAT THIS COVERS, and why it is a SEPARATE file from `test_cost_usage_telemetry.py`. That
file covers the numeric-payload contract DM-2 shipped. This one covers the three fields
`[#691]` adds on top of it, and it is the RED-first witness for step 2 of
`LANE-x-691-routing-half-a`: the tally must record **which role a call served**, **whether
the work it produced was good** and **who reviewed it** — not merely what it cost.

WHY THOSE THREE AND NOT MORE. AX21-2 names the re-rank input verbatim: *"every call records
model, tokens, cost and outcome (tests green? review HIGH-free?) in the tally"*. Model,
tokens and cost were already emitted by `emit_genai_span` before this lane
(`gen_ai.request.model`, `gen_ai.usage.*`, `devknowledge.cost.estimated_usd`) — so the
exists-before-build answer for step 2 is that MOST of AX5-1 already exists and the honest
act is to extend it rather than to ship a second emitter. What was missing is the whole
right-hand side of the re-rank ratio:

  * `role`     — a pass rate is per ROLE. AX21-1's table is role-keyed, and a provider that
                 is strong at `read` and weak at `implement` has no single meaningful rate.
                 Without this field the tally cannot answer the question the router asks.
  * `outcome`  — AX21-2's own parenthetical. A span carrying `error.type` records that the
                 CALL failed; it says nothing about whether the WORK PRODUCT passed, which
                 is the different and load-bearing fact. A call that returns 200 and
                 produces code that fails the lane's tests is a `failed` outcome on a
                 successful call.
  * `reviewed_by` — AX22-2 verbatim: *"the tally records both roles."* Reviewer-not-producer
                 is unenforceable after the fact if the tally never wrote down who reviewed.

`unknown` IS A FIRST-CLASS OUTCOME, deliberately, and it is the same posture
`telemetry_emit.py` takes on unresolved coverage (constraint 2: *"UNRESOLVED COVERAGE IS
`unknown`, NEVER `0`"*). A call whose work product has not been judged yet is a KNOWN state.
The alternative — omitting the field — makes an unjudged call indistinguishable from a
passing one to the re-rank, which silently inflates every pass rate. See
`test_unknown_outcome_is_recorded_not_omitted`.
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


def _emit(mod, tmp_path, **kwargs):
    """Emit one span into a throwaway store and hand back its attribute dict."""
    db = tmp_path / "GENAI-TELEMETRY.db"
    base = dict(system="anthropic", request_model="claude-opus-5", db_path=db, run_id="r-1")
    base.update(kwargs)
    row_id = mod.emit_genai_span(**base)
    with sqlite3.connect(str(db)) as conn:
        (attrs,) = conn.execute(
            "SELECT attributes_json FROM genai_spans WHERE id = ?", (row_id,)
        ).fetchone()
    return json.loads(attrs)


# --- the closed vocabularies ----------------------------------------------------------------


def test_the_role_vocabulary_is_exactly_the_ax21_1_table():
    """The six roles AX21-1 names, and no seventh invented in passing.

    A role is a LOOKUP KEY: the router reads the registry by it and the re-rank groups by it.
    An open vocabulary here means a typo (`implment`) emits a span that every consumer
    silently drops, which is the present-but-unread failure mode the registry schema already
    refuses with `extra="forbid"`.
    """
    mod = _load()
    assert frozenset(
        {"orchestrate", "plan", "implement", "review", "read", "verify"}
    ) == mod.ROLES


def test_the_outcome_vocabulary_is_closed_and_carries_unknown():
    mod = _load()
    assert frozenset({"passed", "failed", "unknown"}) == mod.CALL_OUTCOMES


@pytest.mark.parametrize("bad", ["implment", "IMPLEMENT", "producer", ""])
def test_an_unknown_role_is_refused_and_nothing_is_written(bad, tmp_path):
    """A refusal leaves no row — the same discipline `emit_genai_span` already keeps for an
    unavailable collector. A half-written tally is worse than an empty one, because the
    re-rank cannot tell the difference."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="anthropic", request_model="claude-opus-5", role=bad, db_path=db
        )
    assert "role" in str(exc.value)
    assert _count(db) == 0


@pytest.mark.parametrize("bad", ["green", "PASSED", "pass", ""])
def test_an_unknown_outcome_is_refused(bad, tmp_path):
    """`pass` is refused alongside the typos, and that is the point rather than pedantry:
    `telemetry_emit.OUTCOMES` uses `pass`/`block`/`error` for a GATE fire. Letting the same
    token mean 'the work product was good' in this store would make two different facts
    indistinguishable in a join across the two tables."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="anthropic", request_model="claude-opus-5", outcome=bad, db_path=db
        )
    assert "outcome" in str(exc.value)
    assert _count(db) == 0


# --- the three fields actually land ---------------------------------------------------------


def test_role_outcome_and_reviewer_land_in_the_attribute_dict(tmp_path):
    mod = _load()
    attrs = _emit(
        mod,
        tmp_path,
        role="implement",
        outcome="passed",
        reviewed_by="gpt-5.6-terra",
    )
    assert attrs["devknowledge.role"] == "implement"
    assert attrs["devknowledge.outcome"] == "passed"
    assert attrs["devknowledge.reviewed_by"] == "gpt-5.6-terra"


def test_unknown_outcome_is_recorded_not_omitted(tmp_path):
    """The whole reason `unknown` exists. An unjudged call must be VISIBLE to the re-rank as
    unjudged; omitting the key would let it be counted as neither a pass nor a fail, which
    reads as a pass to any rate computed as `passed / (passed + failed)`."""
    mod = _load()
    attrs = _emit(mod, tmp_path, role="implement", outcome="unknown")
    assert attrs["devknowledge.outcome"] == "unknown"


def test_the_three_fields_are_optional(tmp_path):
    """A span with none of them is still valid. The pre-existing DM-2 call surface does not
    break, and a caller that genuinely has no role to declare writes no role rather than a
    fabricated one."""
    mod = _load()
    attrs = _emit(mod, tmp_path)
    assert "devknowledge.role" not in attrs
    assert "devknowledge.outcome" not in attrs
    assert "devknowledge.reviewed_by" not in attrs


def test_reviewed_by_must_not_equal_the_responding_model(tmp_path):
    """AX22-2 at the TALLY, which is the one place it can be caught after the fact.

    The registry encodes the exclusion and the router enforces it before dispatch — but a
    tally that would happily record `reviewed_by == response_model` makes the violation
    invisible in the record, and the record is what the log-review routine reads.
    """
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod.emit_genai_span(
            system="openai",
            request_model="gpt-5.6-terra",
            response_model="gpt-5.6-terra",
            role="review",
            reviewed_by="gpt-5.6-terra",
            db_path=db,
        )
    # The refusal must NAME ITS RULE. A message that says only "invalid" sends the next
    # reader to the source to find out which rule bit; citing the clause id makes the refusal
    # self-explaining, and this repo's whole posture is that a locator beats a claim.
    message = str(exc.value).lower()
    assert "ax22-2" in message
    assert _count(db) == 0


def test_reviewed_by_falls_back_to_the_request_model_when_no_response_model(tmp_path):
    """A span that never learned which model actually answered still carries the request
    model, and the exclusion has to bite on that rather than pass vacuously — a caller who
    omits `response_model` must not thereby buy an unchecked self-review."""
    mod = _load()
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(mod.GenAiTelemetryError):
        mod.emit_genai_span(
            system="openai",
            request_model="gpt-5.6-terra",
            role="review",
            reviewed_by="gpt-5.6-terra",
            db_path=db,
        )
    assert _count(db) == 0
