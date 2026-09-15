"""One trip-test per `measured` entry of `ecosystem/quality-requirements.yaml` ([#765]).

WHAT A TRIP-TEST IS, AND WHAT IT IS NOT. A trip-test proves that the organ a requirement
names REFUSES a violation of that requirement. It is not a test of the organ's whole
contract -- the organ's own test module owns that -- and it is deliberately narrow: one
violating input that has to be refused, one conforming input that has to be admitted. The
conforming half is what stops a trip-test from being satisfiable by an organ that refuses
everything, which is as useless as one that refuses nothing.

EVERY TRIP BODY IS A FUNCTION OF ITS ORGAN, and that is the load-bearing design decision
in this module. `trip_qr_perf_001(organ, tmp_path)` takes the thing it is testing as an
argument rather than reaching for the import, so `tests/test_quality_requirements.py` can
call the same body with a NEUTERED stand-in -- the real module with exactly one refusal
replaced by a permissive one -- and require it to go RED. A trip-test that passes with its
organ disabled is proving nothing about the organ, and without this seam there is no way
to tell one from a real proof except by reading it.

ASSERTIONS RATHER THAN `pytest.raises` FOR THE REFUSAL LEGS. `pytest.raises` fails by
raising `Failed`, which derives from `BaseException` rather than `Exception`; the neutered
leg wants an ordinary `AssertionError` it can catch narrowly. So each refusal leg captures
the exception itself and asserts on it, which also lets the message be checked -- a refusal
that names nothing gets worked around rather than fixed, so "it raised" is not the whole
property.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import impacted_tests  # noqa: E402
import merge_receipt  # noqa: E402
import provider_registry  # noqa: E402
import seat_refusals  # noqa: E402


class NeuteredOrgan:
    """The real organ with one attribute replaced -- everything else proxies through.

    A whole fake module would prove the trip-test can fail against SOMETHING; replacing one
    refusal proves it fails against the ABSENCE OF THAT REFUSAL, which is the property the
    register claims. The difference matters: a trip-test that merely needs a well-formed
    organ would pass against any other real organ too.
    """

    def __init__(self, organ: Any, **overrides: Any) -> None:
        self._organ = organ
        self._overrides = overrides

    def __getattr__(self, name: str) -> Any:
        if name in self._overrides:
            return self._overrides[name]
        return getattr(self._organ, name)

    def __repr__(self) -> str:  # pragma: no cover - diagnostic only
        return f"<neutered {self._organ.__name__}: {sorted(self._overrides)} disabled>"


# ------------------------------------------------------------------ QR-PERF-001


def trip_qr_perf_001(organ: Any, tmp_path: Path) -> None:
    """A changed `scripts/*.py` that selects zero tests is refused, naming the witness."""
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "tests").mkdir()
    (repo / "scripts" / "qr_probe_uncovered.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "tests" / "test_something_else.py").write_text(
        "def test_something_else():\n    assert True\n", encoding="utf-8")

    findings = organ.guard_findings(repo, ["scripts/qr_probe_uncovered.py"])
    assert findings, (
        "QR-PERF-001 VIOLATED: a scripts/ file no test covers was NOT refused -- "
        "guard_findings returned nothing for an uncovered source")
    source, witness = findings[0]
    assert source == "scripts/qr_probe_uncovered.py", f"refusal names {source!r}"
    assert witness == "tests/test_qr_probe_uncovered.py", (
        "QR-PERF-001's refusal has to NAME the RED-first witness to write; it named "
        f"{witness!r}")

    # The conforming control: the same source, now covered by its conventional test.
    (repo / "tests" / "test_qr_probe_uncovered.py").write_text(
        "def test_qr_probe_uncovered():\n    assert True\n", encoding="utf-8")
    assert organ.guard_findings(repo, ["scripts/qr_probe_uncovered.py"]) == [], (
        "the organ refuses a COVERED source too -- a gate that refuses everything proves "
        "nothing about the requirement")


def test_qr_perf_001_uncovered_script_is_refused(tmp_path):
    trip_qr_perf_001(impacted_tests, tmp_path)


# ------------------------------------------------------------------ QR-AVAIL-001


_STALLED_SEAT = (
    "## Step 4\n"
    "The dispatcher waits for lane 3 to hand back before merging the queue.\n"
)
_DECLARED_WAIT = (
    "## Step 4\n"
    "The dispatcher waits for lane 3 to hand back before merging the queue.\n"
    "<!-- WAIT: interval=60s bound=30 predicate=lane 3's branch tip moves, read from "
    "git -->\n"
)


def trip_qr_avail_001(organ: Any, tmp_path: Path) -> None:
    """A wait stated as an intention, with no declaration, is refused."""
    raised = None
    try:
        organ.refuse_sleeping_poll(_STALLED_SEAT, site="qr-trip")
    except organ.SeatRefusal as exc:
        raised = exc
    assert raised is not None, (
        "QR-AVAIL-001 VIOLATED: a turn ending on a wait-INTENTION with no declaration was "
        "accepted -- nothing wakes such a session, which is the incident this requirement "
        "carries")
    assert raised.refusal == "sleeping-poll", f"refusal id is {raised.refusal!r}"
    assert "declaration" in str(raised), "the refusal does not say what is missing"

    # The conforming control: the same sentence, with the wait written as code beside it.
    organ.refuse_sleeping_poll(_DECLARED_WAIT, site="qr-trip")


def test_qr_avail_001_sleeping_poll_is_refused(tmp_path):
    trip_qr_avail_001(seat_refusals, tmp_path)


# ------------------------------------------------------------------ QR-OBS-001


_PROBE_SHA = "0123456789abcdef0123456789abcdef01234567"


def _complete_merge_receipt(organ: Any, sha: str) -> Any:
    """A receipt complete on every leg of `incompleteness_reason`, naming `sha`.

    Built through the organ so the neutered stand-in constructs the same object the live
    one does -- only the REFUSAL is replaced, never the vocabulary the trip speaks in.
    """
    receipt = organ.Receipt(
        slug="qr-trip", batch="z", opened="2026-09-15T00:00:00.000+00:00", host="trip",
        concurrent_seats=0, kind=organ.KIND_MERGE, merge_sha=sha,
        closed="2026-09-15T00:06:00.000+00:00")
    for step in organ.REQUIRED_STEPS:
        receipt.steps.append(organ.StepTiming(
            step=step, step_class=organ.CLASS_CEREMONY, seconds=90.0, ok=True,
            returncode=0, command="-", started="-"))
    receipt.steps.append(organ.StepTiming(
        step=organ.ACTIONS_STEP, step_class=organ.CLASS_TESTS, seconds=0.0, ok=True,
        returncode=0, command="-", started="-",
        verdict_state=organ.COMPLETE_SUITE_STATES[0]))
    return receipt


def trip_qr_obs_001(organ: Any, tmp_path: Path) -> None:
    """A merge that no complete receipt names is refused, and the refusal says why."""
    problems = organ.audit_merges([_PROBE_SHA], [])
    assert problems, "the organ returned no verdict at all for a merge with no receipt"
    sha, reason = problems[0]
    assert sha == _PROBE_SHA
    assert reason is not None, (
        "QR-OBS-001 VIOLATED: a merge with NO receipt was accepted -- an unrecorded merge "
        "reads exactly like a fast one, which is this requirement's whole complaint")
    assert "NO RECEIPT" in reason, f"the refusal does not name the absence: {reason!r}"

    # A receipt that names the merge but times nothing is refused for a DIFFERENT reason,
    # and the two are kept apart because their remedies are opposite: open a receipt, or
    # finish the one you opened.
    hollow = organ.Receipt(
        slug="qr-trip-hollow", batch="z", opened="2026-09-15T00:00:00.000+00:00",
        host="trip", concurrent_seats=0, kind=organ.KIND_MERGE, merge_sha=_PROBE_SHA)
    _, hollow_reason = organ.audit_merges([_PROBE_SHA], [hollow])[0]
    assert hollow_reason is not None and "INCOMPLETE" in hollow_reason, (
        "QR-OBS-001 VIOLATED: a receipt that was opened and abandoned discharged a merge")

    # The conforming control: a receipt complete on every leg passes.
    complete = _complete_merge_receipt(organ, _PROBE_SHA)
    assert organ.audit_merges([_PROBE_SHA], [complete]) == [(_PROBE_SHA, None)], (
        "the organ refuses a COMPLETE receipt -- a bar nothing can satisfy is not a bar")


def test_qr_obs_001_unreceipted_merge_is_refused(tmp_path):
    trip_qr_obs_001(merge_receipt, tmp_path)


# ------------------------------------------------------------------ QR-OBS-002


_UNREGISTERED_MODEL = "qr-trip-no-such-model"


def _a_priced_model(organ: Any) -> str:
    """Any model the live registry prices, read from the registry rather than pinned.

    A literal id here would be a live-data pin: the registry is a maintained file, and a
    test that names one of its rows turns every future registry edit into a test edit.
    """
    for model_id, row in organ.models().items():
        if isinstance(row.get("rates"), dict):
            return model_id
    raise AssertionError("the live provider registry prices no model at all")


def trip_qr_obs_002(organ: Any, tmp_path: Path) -> None:
    """A model with no declared rate raises rather than resolving to a zero price."""
    raised = None
    try:
        organ.resolve_rate(_UNREGISTERED_MODEL)
    except organ.RateUnavailable as exc:
        raised = exc
    assert raised is not None, (
        "QR-OBS-002 VIOLATED: an unregistered model resolved to a rate -- absent and free "
        "are different facts, and a total that cannot tell them apart is not a measurement")
    assert _UNREGISTERED_MODEL in str(raised), (
        f"the refusal does not NAME the model it could not price: {raised!r}")

    # The conforming control: a model the registry does price resolves to a positive cost,
    # so the refusal above is about the missing rate and not about the call shape.
    rate = organ.resolve_rate(_a_priced_model(organ))
    cost = rate.usd(input_tokens=1_000_000, output_tokens=0,
                    cache_write_tokens=0, cache_read_tokens=0)
    assert cost > 0, "a priced model resolved to a zero cost"


def test_qr_obs_002_unpriced_model_is_refused(tmp_path):
    trip_qr_obs_002(provider_registry, tmp_path)


# ------------------------------------------------------------------ the seam


#: register id -> (trip body, live organ, the neutered stand-in for that organ).
#:
#: `tests/test_quality_requirements.py` drives this mapping: it checks that every `measured`
#: entry in the register appears here, runs each body against the live organ, and runs it
#: again against the stand-in requiring an AssertionError. The stand-in disables exactly the
#: refusal the requirement rests on and nothing else.
TRIPS: dict[str, tuple[Any, Any, Any]] = {
    "QR-PERF-001": (
        trip_qr_perf_001, impacted_tests,
        lambda: NeuteredOrgan(impacted_tests, guard_findings=lambda *a, **k: []),
    ),
    "QR-AVAIL-001": (
        trip_qr_avail_001, seat_refusals,
        lambda: NeuteredOrgan(seat_refusals, refuse_sleeping_poll=lambda *a, **k: 0),
    ),
    "QR-OBS-001": (
        trip_qr_obs_001, merge_receipt,
        lambda: NeuteredOrgan(
            merge_receipt,
            audit_merges=lambda shas, receipts: [(s, None) for s in shas]),
    ),
    "QR-OBS-002": (
        trip_qr_obs_002, provider_registry,
        # The neutering here is the LIE the requirement forbids, spelled out: instead of
        # raising, the stand-in hands back the rate of a model that IS priced -- which is
        # exactly "price the unknown thing as if it were a known one".
        lambda: NeuteredOrgan(
            provider_registry,
            resolve_rate=lambda model_id, path=None: provider_registry.resolve_rate(
                _a_priced_model(provider_registry), path)),
    ),
}
