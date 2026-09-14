"""Tokens and USD per lane and per model, RED-first (`[#751]`).

THE TARGET, verbatim from the lane contract's Done-when 2:

    The lane receipt carries tokens and USD, per lane AND per model, resolved from that file
    at run time -- never a rate table hard-coded into this lane, and never a literal in the
    receipt writer.

and its clause 1, which corrects the roster's premise:

    the rates DO NOT YET EXIST ... This lane therefore AUTHORS a machine-readable rate
    structure in that file as its first act, rather than reading one that is not there.

WHAT THESE TESTS REFUSE. Three lies, and each has a test whose name says which:

  1. **A receipt that reports minutes and no money.** `[#675]` bought itemised minutes; a
     merge's other cost is tokens, and a receipt silent about them reads exactly like a cheap
     one. The completeness predicate names the absence rather than rendering a blank.
  2. **A rate that lives in this lane.** The whole point is that `ecosystem/provider-registry.yaml`
     becomes the rate's one home. The witness is a CHANGED registry producing a CHANGED dollar
     figure -- a literal anywhere in the pricing path survives that edit, and this test does not.
  3. **An unpriced model costed at zero.** The most dangerous plausible value this module can
     produce, and the same class `merge_receipt` records for a 0.0-minute receipt: it meets any
     budget spectacularly and means nothing. A model with no declared rate REFUSES, by name.

WHAT THEY DO NOT TEST. That any particular rate is correct. A rate is a declared fact with a
recorded `as_of` and a source; asserting a number here would put a second copy of it in the
repository, which is the drift the registry exists to end. What is asserted is that the number
in the report is the number in the file.
"""
from __future__ import annotations

import json

import pytest

import lane_cost as lc
import provider_registry as pr


# --- helpers ----------------------------------------------------------------------------

#: A registry small enough to read at a glance and complete enough to load: the loader's
#: two-collection guard wants `providers:` and `models:`, and the schema wants each model to
#: name a declared provider.
_REGISTRY = """\
rate_card:
  currency: USD
  unit: per_million_tokens
  as_of: "2026-09-14"
  basis: list-price
  source: test fixture
  cache_write_multiplier: 1.25
  cache_read_multiplier: 0.1

providers:
  anthropic:
    display_name: Anthropic
    cli: claude
    version_command: ["claude", "--version"]

models:
  priced-model:
    provider: anthropic
    rates:
      input: {input_rate}
      output: {output_rate}
  unpriced-model:
    provider: anthropic
"""


def _registry(tmp_path, *, input_rate: float = 5.0, output_rate: float = 25.0):
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "provider-registry.yaml"
    path.write_text(_REGISTRY.format(input_rate=input_rate, output_rate=output_rate),
                    encoding="utf-8", newline="\n")
    return path


def _turn(model: str, *, uuid: str, input_tokens: int = 0, output_tokens: int = 0,
          cache_write: int = 0, cache_read: int = 0) -> str:
    """One assistant turn in the Claude Code transcript shape, as measured on this host."""
    return json.dumps({
        "type": "assistant",
        "uuid": uuid,
        "message": {
            "id": f"msg_{uuid}",
            "model": model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_write,
                "cache_read_input_tokens": cache_read,
            },
        },
    })


def _transcript(dir_path, name: str, lines: list[str]):
    dir_path.mkdir(parents=True, exist_ok=True)
    path = dir_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


# --- LIE 1: a receipt that reports minutes and no money ------------------------------------

def test_a_lane_receipt_with_no_tokens_and_no_usd_is_refused_by_name(tmp_path):
    """The founding complaint, in this lane's own terms.

    `merge_receipt`'s own argument is that an unrecorded step reads exactly like a fast one.
    An unrecorded token spend reads exactly like a cheap merge, so the predicate returns the
    REASON rather than a bare boolean -- an exclusion a reader cannot account for looks like a
    bug in the tool (the `REMEDIES` argument `merge_receipt.incompleteness_reason` makes).
    """
    reason = lc.uncosted_reason(tmp_path, "lane-y-751-cost-in-money")
    assert reason is not None, "a receipt with no cost row must not read as a costed one"
    assert "lane-y-751-cost-in-money" in reason
    assert lc.is_costed(tmp_path, "lane-y-751-cost-in-money") is False


def test_a_receipt_is_costed_once_its_cost_row_is_appended(tmp_path):
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    cost = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path))
    lc.append_cost(tmp_path, cost)
    assert lc.uncosted_reason(tmp_path, "lane-a") is None
    assert lc.is_costed(tmp_path, "lane-a") is True


# --- LIE 2: a rate that lives in this lane -------------------------------------------------

def test_the_dollar_figure_moves_when_the_registry_moves(tmp_path):
    """THE test for Done-when 2's "resolved from that file at run time".

    A literal anywhere in the pricing path -- a constant, a default, a fallback -- survives an
    edit to the registry. This assertion does not: the SAME tokens are priced twice against two
    registries and the two dollar figures must differ by exactly the ratio of the declared
    rates. A hard-coded table cannot pass it, and neither can a table that is merely seeded
    from the file and then cached across calls.
    """
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])

    cheap = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                         registry_path=_registry(tmp_path / "cheap", input_rate=5.0))
    dear = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path / "dear", input_rate=50.0))

    assert cheap.usd == pytest.approx(5.0)
    assert dear.usd == pytest.approx(50.0)


def test_every_token_class_is_priced_from_the_registry_including_cache(tmp_path):
    """Cache tokens are the bulk of this repo's spend, and pricing them at the input rate --
    or at nothing -- is the difference between a bill and a decoration. The multipliers are
    declared ONCE on the rate card and applied here; nothing in this module knows 1.25 or 0.1.
    """
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("priced-model", uuid="u1", input_tokens=1_000_000, output_tokens=1_000_000,
              cache_write=1_000_000, cache_read=1_000_000),
    ])
    cost = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path, input_rate=5.0, output_rate=25.0))
    # 5 (input) + 25 (output) + 6.25 (cache write, 1.25x) + 0.5 (cache read, 0.1x)
    assert cost.usd == pytest.approx(36.75)


def test_the_rate_resolves_out_of_the_registry_rather_than_a_module_constant(tmp_path):
    rate = pr.resolve_rate("priced-model", _registry(tmp_path, input_rate=7.0))
    assert rate.input == pytest.approx(7.0)
    assert rate.cache_write == pytest.approx(8.75)
    assert rate.cache_read == pytest.approx(0.7)
    assert rate.currency == "USD"


# --- LIE 3: an unpriced model costed at zero -----------------------------------------------

def test_a_model_with_no_declared_rate_refuses_rather_than_pricing_at_zero(tmp_path):
    with pytest.raises(pr.RateUnavailable) as exc:
        pr.resolve_rate("unpriced-model", _registry(tmp_path))
    assert "unpriced-model" in str(exc.value)


def test_a_model_absent_from_the_registry_refuses_by_name(tmp_path):
    with pytest.raises(pr.RateUnavailable) as exc:
        pr.resolve_rate("never-registered", _registry(tmp_path))
    assert "never-registered" in str(exc.value)


def test_an_unpriced_model_is_reported_on_the_receipt_never_summed_into_the_total(tmp_path):
    """The report must be honest in BOTH directions: the unpriced spend does not inflate the
    total, and it does not vanish from the receipt either. A reader has to be able to say how
    much of the lane is unaccounted for."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("priced-model", uuid="u1", input_tokens=1_000_000),
        _turn("unpriced-model", uuid="u2", input_tokens=9_000_000),
    ])
    cost = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path))
    assert cost.usd == pytest.approx(5.0), "the unpriced model must not be priced at zero"
    unpriced = cost.unpriced()
    assert [m.model for m in unpriced] == ["unpriced-model"]
    assert unpriced[0].usage.input_tokens == 9_000_000
    assert "unpriced" in cost.render()


# --- the transcript reader -----------------------------------------------------------------

def test_token_figures_are_read_per_model_and_summed_per_lane(tmp_path):
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("priced-model", uuid="u1", input_tokens=10, output_tokens=1),
        _turn("unpriced-model", uuid="u2", input_tokens=20, output_tokens=2),
    ])
    _transcript(sessions / "proj--lane-a", "b.jsonl", [
        _turn("priced-model", uuid="u3", input_tokens=30, output_tokens=3),
    ])
    per_model = lc.lane_usage("lane-a", sessions_root=sessions)
    assert per_model["priced-model"].input_tokens == 40
    assert per_model["priced-model"].output_tokens == 4
    assert per_model["priced-model"].calls == 2
    assert per_model["unpriced-model"].input_tokens == 20


def test_a_repeated_message_id_is_counted_once(tmp_path):
    """Transcripts carry the same assistant message twice -- measured on this host, two
    adjacent lines with byte-identical `usage`. Summing them doubles the bill, and a doubled
    bill is indistinguishable from a busy day."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("priced-model", uuid="u1", input_tokens=100),
        _turn("priced-model", uuid="u1", input_tokens=100),
    ])
    per_model = lc.lane_usage("lane-a", sessions_root=sessions)
    assert per_model["priced-model"].input_tokens == 100
    assert per_model["priced-model"].calls == 1


def test_a_synthetic_turn_carries_no_model_and_is_skipped(tmp_path):
    """`<synthetic>` turns appear in every transcript on this host. They name no model, so
    they can be neither priced nor attributed; counting them would invent a model row."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("<synthetic>", uuid="u1", input_tokens=5),
        _turn("priced-model", uuid="u2", input_tokens=7),
    ])
    per_model = lc.lane_usage("lane-a", sessions_root=sessions)
    assert set(per_model) == {"priced-model"}


def test_an_unreadable_transcript_line_is_skipped_not_fatal(tmp_path):
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        "{not json",
        _turn("priced-model", uuid="u2", input_tokens=7),
    ])
    per_model = lc.lane_usage("lane-a", sessions_root=sessions)
    assert per_model["priced-model"].input_tokens == 7


# --- the ledger, and the per-batch / per-model report --------------------------------------

def test_the_cost_ledger_is_append_only(tmp_path):
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    registry = _registry(tmp_path)
    first = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions, registry_path=registry)
    second = lc.lane_cost("lane-b", batch="Y", sessions_root=sessions, registry_path=registry)
    lc.append_cost(tmp_path, first)
    before = (tmp_path / lc.COST_LEDGER_RELPATH).read_text(encoding="utf-8")
    lc.append_cost(tmp_path, second)
    after = (tmp_path / lc.COST_LEDGER_RELPATH).read_text(encoding="utf-8")
    assert after.startswith(before), "an append must never rewrite an earlier line"
    assert len(lc.read_cost_ledger(tmp_path)) == 2


def test_the_report_splits_by_batch_and_by_model(tmp_path):
    """Done-when 3, in one assertion: cost per batch AND cost per model."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    _transcript(sessions / "proj--lane-b", "b.jsonl",
                [_turn("priced-model", uuid="u2", input_tokens=2_000_000)])
    registry = _registry(tmp_path)
    lc.append_cost(tmp_path, lc.lane_cost("lane-a", batch="X", sessions_root=sessions,
                                          registry_path=registry, slug_dirs=["proj--lane-a"]))
    lc.append_cost(tmp_path, lc.lane_cost("lane-b", batch="Y", sessions_root=sessions,
                                          registry_path=registry, slug_dirs=["proj--lane-b"]))

    report = lc.batch_report(tmp_path)
    assert report.by_batch()["X"] == pytest.approx(5.0)
    assert report.by_batch()["Y"] == pytest.approx(10.0)
    assert report.by_model()["priced-model"] == pytest.approx(15.0)
    rendered = report.render()
    assert "X" in rendered and "Y" in rendered and "priced-model" in rendered


def test_the_report_over_an_empty_ledger_says_so_rather_than_reporting_zero(tmp_path):
    """A zero-dollar report over no receipts is the `merge_receipt` 0.0-minute failure in
    money: it is not a cheap batch, it is no measurement."""
    rendered = lc.batch_report(tmp_path).render()
    assert "no cost receipts" in rendered.lower()
    assert "$0.00" not in rendered


# --- the fleet_health digest line ----------------------------------------------------------

def test_the_cost_digest_line_names_a_batch_and_a_model(tmp_path):
    """Done-when 3 at the surface a session actually reads: `fleet_health` prints cost per
    batch AND per model."""
    import fleet_health as fh

    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    lc.append_cost(tmp_path, lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                                          registry_path=_registry(tmp_path),
                                          slug_dirs=["proj--lane-a"]))
    line = fh.cost_health_line(tmp_path)
    assert line.startswith("[cost]")
    assert "Y" in line and "priced-model" in line and "$5.00" in line


def test_the_cost_digest_line_is_silent_rather_than_zero_over_an_empty_ledger(tmp_path):
    """A `[cost] $0.00` line on a repo that has measured nothing is a number a reader would
    believe. Silence is the honest rendering of no measurement."""
    import fleet_health as fh

    assert fh.cost_health_line(tmp_path) is None


def test_the_cost_digest_line_calls_its_own_total_a_floor_when_a_model_is_unpriced(tmp_path):
    import fleet_health as fh

    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl", [
        _turn("priced-model", uuid="u1", input_tokens=1_000_000),
        _turn("unpriced-model", uuid="u2", input_tokens=9_000_000),
    ])
    lc.append_cost(tmp_path, lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                                          registry_path=_registry(tmp_path),
                                          slug_dirs=["proj--lane-a"]))
    line = fh.cost_health_line(tmp_path)
    assert "UNPRICED" in line and "floor" in line


def test_the_cost_digest_never_breaks_the_digest(tmp_path, monkeypatch):
    """Every fleet_health line is fail-soft: a surfacing organ that could break the boot digest
    would be a new failure mode rather than a warning about one."""
    import fleet_health as fh

    monkeypatch.setattr(fh, "_import_lane_cost",
                        lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    assert fh.cost_health_line(tmp_path) is None
