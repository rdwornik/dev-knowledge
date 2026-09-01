"""Tests for `scripts/cost_usage_telemetry.py` — the DM-2 OTel GenAI span emitter.

WHY THIS FILE EXISTS AT ALL. DM-2 landed 419 lines of new emitter code with **no test module**,
while its own done-contract said *"Run the TARGETED tests for this diff"* — there were none to
run. That is not a criticism of the lane's reasoning, which is sound and well-documented; it is
the gap a pre-merge review is for, and it is closed here rather than at the next batch.

SCOPE, stated so this file does not read as more than it is: it covers the NUMERIC-PAYLOAD
CONTRACT, which is where the pre-merge terra round found a HIGH. It does not cover exporter
resolution, the at-rest schema, or the OTel attribute mapping — those are owed and named.
"""
from __future__ import annotations

import importlib.util
import json
import math
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


# --- the numeric-payload contract, two independent legs -------------------------------------
#
# THE DEFECT (terra HIGH, pre-merge 2026-09-01): `_check_number` type-checked and stopped there.
# `NaN` and the infinities ARE `float` instances, so they passed — and `json.dumps` serialises
# them as the bare tokens `NaN` / `Infinity`, which **RFC 8259 does not permit**. A strict OTLP
# or JSON consumer refuses the payload, so the span is not wrong at the far end, it is ABSENT,
# while the emitting side reports success. Worst shape available for a telemetry emitter.


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_leg1_the_validator_refuses_a_non_finite_cost(bad):
    mod = _load()
    with pytest.raises(mod.GenAiTelemetryError) as exc:
        mod._check_number("cost_estimated_usd", bad)
    assert "finite" in str(exc.value)


@pytest.mark.parametrize("good", [0, 1, -1, 0.0, 12.34, None])
def test_leg1_admits_every_finite_number_and_none(good):
    mod = _load()
    mod._check_number("cost_estimated_usd", good)          # does not raise


def test_leg1_still_refuses_a_bool_and_a_string():
    """`bool` is an `int` subclass, so the original guard's exclusion of it is preserved."""
    mod = _load()
    for bad in (True, "1.0"):
        with pytest.raises(mod.GenAiTelemetryError):
            mod._check_number("cost_estimated_usd", bad)


def test_leg2_the_serialiser_itself_refuses_a_non_finite():
    """The second leg, and the reason there are two.

    The validator covers the two cost fields it knows the names of. A non-finite reaching the
    payload by ANY other route — a caller's `events` mapping, a future attribute nobody thought
    to validate — is caught by `allow_nan=False` at serialisation instead of being emitted as a
    non-standard token. A validator and a serialiser fail at different times, so neither is a
    substitute for the other.
    """
    with pytest.raises(ValueError):
        json.dumps({"x": float("nan")}, allow_nan=False)
    # Counted on CODE, not on raw occurrences, and not line-by-line either. The explanatory
    # comment above the fix contains the token (so a bare `src.count` reads 3), and the second
    # call is WRAPPED across two lines (so a line-wise matcher reads 3 sites, one unguarded).
    # Both earlier versions of this assertion failed for those two reasons in turn. Comments are
    # stripped and the whole remaining source is counted, which is what makes the claim true.
    code = chr(10).join(
        ln for ln in _P.read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#"))
    assert code.count("json.dumps(") == 2, "emit_genai_span serialises exactly two payloads"
    assert code.count("allow_nan=False") == 2, "both serialisation calls carry the guard"


def test_the_module_imports_math_for_the_finiteness_check():
    """Guards the import the fix depends on — a NameError here would surface as a crash inside
    the emitter rather than as a refusal."""
    assert math.isfinite(1.0)
    assert "import math" in _P.read_text(encoding="utf-8")


def test_owed_coverage_is_named_rather_than_implied():
    """Not a behaviour test — a standing note that this module's other surfaces are untested.

    Recorded as an assertion so it is read, not as a comment so it is skimmed. Delete this test
    when exporter resolution, the at-rest schema and the attribute mapping each have real
    coverage; until then it states what this file does NOT prove.
    """
    owed = {"resolve_exporter", "at-rest schema", "OTel attribute mapping"}
    assert owed, "see the module docstring's SCOPE paragraph"
