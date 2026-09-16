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
import logging
import pathlib

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
    #: ASSERT THE INVARIANT, NOT THE SENTENCE. The exact phrasing gained the word "measured"
    #: when the review widened this refusal to cover transcript-less rows as well as an empty
    #: file; a test pinned to the old wording would have read as a regression when the
    #: predicate had only got stricter.
    assert "cost receipts" in rendered.lower()
    assert "undefined" in rendered.lower() and "not zero" in rendered.lower()
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


# --- feeding logs/TOKEN-LOG.md (the ADR-29/ADR-39 append-only leg) --------------------------

_TOKEN_LOG = """\
# Token Usage Log

Append /stats snapshot weekly. Never edit previous entries.

## 2026-08-04 (delta: 2026-07-25 to 2026-08-04, via ccusage --json)
Delta: 10 active days, sessions N/A (not in ccusage --json), $1676.83
Opus 5: 72.1% (in: 96K, out: 5925K)
"""


def _seeded_token_log(tmp_path):
    path = tmp_path / lc.TOKEN_LOG_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_TOKEN_LOG, encoding="utf-8", newline="\n")
    return path


def _one_row_report(tmp_path):
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    lc.append_cost(tmp_path, lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                                          registry_path=_registry(tmp_path),
                                          slug_dirs=["proj--lane-a"]))
    return lc.batch_report(tmp_path)


def test_feeding_the_token_log_rewrites_not_one_existing_byte(tmp_path):
    """THE ruling's whole safety property, and the reason the file is fed rather than deleted.

    `logs/TOKEN-LOG.md` is append-only in the STRICT sense (ADR-29/ADR-39 -- unlike LESSONS.md
    it has no archival exception), and it is newest-first, so "append" here means PREPEND under
    the header. The assertion is byte-level in both directions: the header survives unchanged
    at the front and every pre-existing entry survives unchanged at the back. A feeder that
    reformatted, reflowed or re-sorted would pass a line-count check and fail this one.
    """
    path = _seeded_token_log(tmp_path)
    before = path.read_text(encoding="utf-8")
    head, tail = before.split("\n")[:4], before.split("\n")[4:]

    lc.append_token_log(tmp_path, lc.token_log_entry(_one_row_report(tmp_path), on="2026-09-14"))

    after = path.read_text(encoding="utf-8")
    assert after.startswith("\n".join(head)), "the header was rewritten"
    assert after.endswith("\n".join(tail)), "an existing entry was rewritten"
    assert "## 2026-09-14" in after
    assert after.index("## 2026-09-14") < after.index("## 2026-08-04"), "newest-first"


def test_the_entry_states_its_method_because_the_two_are_not_comparable(tmp_path):
    """The existing entries are fleet-wide, by calendar week, with cache tokens EXCLUDED "for
    comparability"; these are per-lane, by cost receipt, with cache INCLUDED. An entry that did
    not say which it was would invite diffing two incomparable numbers and calling it a trend.
    """
    entry = lc.token_log_entry(_one_row_report(tmp_path), on="2026-09-14")
    assert "lane_cost.py" in entry
    assert "NOT comparable" in entry
    assert "Cache:" in entry


def test_feeding_refuses_to_create_the_file_it_is_supposed_to_feed(tmp_path):
    """Whether `logs/TOKEN-LOG.md` exists AT ALL is the recorded fed-or-deleted decision. A
    feeder that created it on absence would silently re-take that decision every time someone
    ran it against a repo where it had been deliberately removed."""
    with pytest.raises(lc.CostError) as exc:
        lc.append_token_log(tmp_path, "## 2026-09-14\nirrelevant")
    assert lc.TOKEN_LOG_RELPATH in str(exc.value)


# --- THE INTEGRATOR'S REVIEW FINDINGS, RED-first ([#751], held merge) ----------------------
#
# Four findings from the batch-Y integrator's Codex pass. All four are in AGGREGATION or
# ATTRIBUTION; the pricing arithmetic was re-derived by hand against the live card and is
# correct, so nothing below touches the pricing path.


def _unmeasured_row(slug: str, batch: str = "Y") -> "lc.LaneCost":
    """A cost row for a lane whose transcript was never found.

    NOT a synthetic edge case: `transcript_dirs` documents that a `--bg` lane's transcript is
    filed under its LAUNCHING session and carries no directory of its own, so the first honest
    `close --slug <bg-lane>` produces exactly this row. Every remaining batch-Y lane is `--bg`.
    """
    return lc.LaneCost(slug=slug, batch=batch, models=(), measured="2026-09-14T00:00:00+00:00")


# --- FINDING 1: an unmeasured lane absorbed as $0.00 ---------------------------------------

def test_an_unmeasured_lane_is_never_absorbed_into_a_total_as_zero(tmp_path):
    """`LaneCost.render()` already refuses this lie one level down -- "NO TRANSCRIPT FOUND ...
    UNKNOWN rather than zero" -- and `BatchCostReport.render()`'s own docstring states the
    principle: "An empty ledger is not a free batch -- it is no measurement." An empty ROW is
    not a free LANE, and the guard the module already owns (`has_transcript()`) has to reach
    the aggregate too.

    The measured lane costs SOMETHING; the unmeasured one must not drag the batch's figure
    toward zero, nor appear in the per-batch map as a batch that cost nothing.
    """
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    measured = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                            registry_path=_registry(tmp_path), slug_dirs=["proj--lane-a"])
    lc.append_cost(tmp_path, measured)
    lc.append_cost(tmp_path, _unmeasured_row("lane-b", batch="Z"))

    report = lc.batch_report(tmp_path)
    assert report.usd == pytest.approx(measured.usd), "an unmeasured lane moved the total"
    assert "Z" not in report.by_batch(), "a batch with no measurement read as a $0.00 batch"
    assert [r.slug for r in report.unmeasured()] == ["lane-b"]


def test_an_unmeasured_lane_is_not_counted_in_the_receipt_count(tmp_path):
    """`n=` is the denominator a reader divides by. Counting a lane whose spend is UNKNOWN
    makes the average wrong in the direction that flatters -- and silently, which is the part
    that matters. The count is of MEASUREMENTS, and the unmeasured lanes are named instead."""
    lc.append_cost(tmp_path, _unmeasured_row("lane-b"))
    report = lc.batch_report(tmp_path)

    assert report.measured() == (), "a transcript-less row counted as a measurement"
    rendered = report.render()
    assert "n=1" not in rendered, "an unmeasured lane was counted in n="
    assert "$0.00" not in rendered, "UNKNOWN spend was rendered as a zero figure"
    assert "lane-b" in rendered, "the unmeasured lane was dropped instead of named"


def test_the_digest_line_is_silent_when_every_row_is_unmeasured(tmp_path):
    """`fleet_health` prints this on every boot. A `[cost] $0.00 over 1 lane(s)` line built
    from a transcript-less row is the same lie with the widest possible audience."""
    lc.append_cost(tmp_path, _unmeasured_row("lane-b"))
    assert lc.cost_health_line(tmp_path) is None


# --- FINDING 2: a re-close double-counts, permanently --------------------------------------

def test_a_reclose_supersedes_rather_than_double_counting(tmp_path):
    """The sequence is the NORMAL one, not a mistake: finding 1 says the first honest close of
    a `--bg` lane appends an empty row, and the operator then learns to re-close with
    `--slug-dir`. Two rows for one lane on first correct use.

    The ledger is append-only (ADR-29/39), so there is no sanctioned repair -- the bad line
    cannot be deleted. The fix therefore has to live in the READER, and last-wins-per-slug is
    the semantics `uncosted_reason` already uses on `rows[-1]`.
    """
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    cost = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path), slug_dirs=["proj--lane-a"])

    lc.append_cost(tmp_path, _unmeasured_row("lane-a"))   # the first, empty close
    lc.append_cost(tmp_path, cost)                        # the re-close with --slug-dir

    report = lc.batch_report(tmp_path)
    assert report.usd == pytest.approx(cost.usd), "a re-close inflated the batch total"
    assert len(report.measured()) == 1, "one lane produced two measurements"
    assert report.by_batch()["Y"] == pytest.approx(cost.usd)


def test_the_aggregate_and_the_per_slug_reader_agree_on_a_duplicate(tmp_path):
    """Two readers of ONE ledger must not disagree about what a duplicate means. `uncosted_
    reason` takes `rows[-1]`; the aggregate summed every row. Same file, two incompatible
    answers -- and the append-only rule makes the disagreement permanent."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-a", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])
    cost = lc.lane_cost("lane-a", batch="Y", sessions_root=sessions,
                        registry_path=_registry(tmp_path), slug_dirs=["proj--lane-a"])
    lc.append_cost(tmp_path, cost)
    lc.append_cost(tmp_path, cost)

    assert lc.batch_report(tmp_path).usd == pytest.approx(cost.usd)
    assert lc.uncosted_reason(tmp_path, "lane-a") is None
    assert lc.batch_report(tmp_path).by_model()["priced-model"] == pytest.approx(cost.usd)


def test_the_ledger_keeps_both_lines_because_it_is_append_only(tmp_path):
    """The reader supersedes; the FILE still never loses a byte. Superseding by rewriting the
    ledger would fix the arithmetic by breaking the ADR-29/39 guarantee, which is a worse
    trade -- the superseded row stays readable as the record of what was first measured."""
    lc.append_cost(tmp_path, _unmeasured_row("lane-a"))
    lc.append_cost(tmp_path, _unmeasured_row("lane-a"))
    raw = lc.cost_ledger_path(tmp_path).read_text(encoding="utf-8").strip().splitlines()
    assert len(raw) == 2, "the writer edited the ledger instead of appending to it"
    assert len(lc.read_cost_ledger(tmp_path)) == 2, "the raw reader hid a row"


# --- FINDING 3: containment matching is a widening -----------------------------------------

def test_a_truncated_slug_does_not_match_a_longer_lanes_directory(tmp_path):
    """`transcript_dirs` says "MATCHED, NOT GUESSED, AND NEVER WIDENED", and then matched on
    containment -- so `lane-y-75` swallowed `lane-y-751`'s transcript and priced one lane's
    spend onto another. No collision exists among batch Y's current ids, which is exactly why
    this needs a test rather than luck: the ids are data, and the next batch's may collide.
    """
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj--lane-y-751-cost", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1_000_000)])

    assert lc.transcript_dirs("lane-y-751-cost", sessions) != [], "the true slug stopped matching"
    assert lc.transcript_dirs("lane-y-75", sessions) == [], \
        "a truncated slug claimed a longer lane's transcript"


def test_an_ambiguous_slug_match_is_warned_not_silent(tmp_path, caplog):
    """The live risk is not the collision, it is the SILENCE. One slug matching directories
    that belong to two different lanes produces a confident wrong amount and no signal at all,
    and a wrong number nobody is told about is worse than a refusal."""
    sessions = tmp_path / "sessions"
    _transcript(sessions / "proj-a--lane-y-751", "a.jsonl",
                [_turn("priced-model", uuid="u1", input_tokens=1)])
    _transcript(sessions / "proj-b--lane-y-751", "b.jsonl",
                [_turn("priced-model", uuid="u2", input_tokens=1)])

    with caplog.at_level("WARNING"):
        matched = lc.transcript_dirs("lane-y-751", sessions)
    assert len(matched) == 2, "both directories genuinely match and both must be read"
    assert "lane-y-751" in caplog.text
    assert "proj-a--lane-y-751" in caplog.text and "proj-b--lane-y-751" in caplog.text


# --- FINDING 4: nothing prices against the LIVE registry -----------------------------------

def test_every_live_priced_model_prices_through_this_module():
    """RESOLVABILITY, not a number. Every pricing test above uses a fixture whose rates happen
    to equal the live `claude-opus-5` rates, so a live rate that went missing or to zero would
    still look right everywhere -- the fixture mirrors the truth it is supposed to check.

    What is asserted is that each model the LIVE card prices actually resolves through THIS
    module's pricing path and yields a positive figure for positive usage. Deliberately NOT
    asserted: any particular rate. Typing one here would put a second copy of a declared fact
    in the repository -- the drift the registry exists to end -- and would go RED at the next
    genuine price change, which is not a defect.
    """
    priced = pr.priced_models()
    assert priced, "the live registry prices no model at all"

    usage = lc.TokenUsage(input_tokens=1_000, output_tokens=1_000, calls=1)
    for model in priced:
        cost = lc.price_usage(model, usage)          # no registry_path: the LIVE card
        assert cost.is_priced, f"{model} carries rates on disk but does not price: " \
                               f"{cost.unpriced_reason}"
        assert cost.usd > 0, f"{model} priced positive usage at {cost.usd}"


def test_the_model_this_repo_actually_runs_is_priced_live():
    """The narrowest useful liveness check: the id every transcript in this repo names. It is
    read from the registry's own priced set rather than typed as a rate, so this test asserts
    PRESENCE, never price."""
    assert "claude-opus-5" in pr.priced_models(), \
        "the live surface's most-named model carries no rates -- every lane would be UNPRICED"


# ---------------------------------------------------------------- the transcript SIZE BOUND
#
# Added 2026-09-15 by batch AA lane aa-14 ([#792]), which owns the runtime-resource lifecycle
# and found this reader unbounded while measuring the thing it reads.
#
# MEASURED CORPUS, 2026-09-15: 3,108 transcripts under `~/.claude/projects`, 2.55 GB total,
# median 0.34 MB, LARGEST 29.56 MB. The longest single LINE across the 20 largest files is
# 1.360 MB. `path.read_text()` followed by `.splitlines()` holds the whole file as a str AND
# a list of str at once -- about 60 MB of peak for that one transcript -- and
# `scripts/fleet_health.py` imports this module, so it runs at SESSION START, on the box whose
# binding constraint this lane exists to manage.
#
# THE BOUND IS STREAMING, NOT A REFUSAL, and the distinction is the whole design. "Skip any
# transcript over N MB" would be a size bound too, and it would silently drop a lane's spend
# -- the number that means "not measured" becoming the number that means "free", which is the
# exact class `test_an_unpriced_model_refuses_rather_than_costing_zero` above already refuses
# one layer up. Streaming bounds memory to the longest LINE while every line is still counted.


def test_the_transcript_reader_never_holds_the_WHOLE_file(monkeypatch, tmp_path):
    """A reader that slurps is refused by construction: `read_text` is made to explode.

    This is a property, not a timing or a memory measurement -- a peak-RSS assertion would be
    flaky under a loaded box and under xdist, and the box IS loaded, which is why this lane
    exists. Any implementation that streams passes; any implementation that slurps fails, and
    there is no third behaviour to be vague about.
    """
    transcript = tmp_path / "s.jsonl"
    rows = []
    for n in range(50):
        rows.append(json.dumps({
            "message": {"id": f"m{n}", "model": "claude-opus-5",
                        "usage": {"input_tokens": 1, "output_tokens": 1}}}))
    transcript.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def _explode(*args, **kwargs):
        raise AssertionError(
            "read_transcript_usage read the WHOLE transcript into memory. The measured corpus "
            "has a 29.56 MB transcript, and read_text + splitlines holds two copies of it at "
            "once inside a module fleet_health.py runs at SessionStart")

    monkeypatch.setattr(pathlib.Path, "read_text", _explode)
    usage = lc.read_transcript_usage(transcript)
    assert usage["claude-opus-5"].input_tokens == 50, usage


def test_an_absurd_single_line_is_WARNED_and_skipped_not_silently_dropped(tmp_path, caplog):
    """The one thing streaming cannot bound is a single enormous line, so that has a bound of
    its own -- and it is LOUD. A skipped line is unmeasured spend, and unmeasured spend that
    says nothing is indistinguishable from no spend.

    The rest of the file must still be counted: a bound that zeroes a whole lane because one
    line was malformed prices the lane at nothing, which is the failure this file's header
    calls the most dangerous plausible value this module can produce.
    """
    transcript = tmp_path / "s.jsonl"
    good = json.dumps({"message": {"id": "ok", "model": "claude-opus-5",
                                   "usage": {"input_tokens": 7, "output_tokens": 0}}})
    huge = json.dumps({"message": {"id": "huge", "model": "claude-opus-5",
                                   "usage": {"input_tokens": 999_999, "output_tokens": 0},
                                   "pad": "x" * (lc.MAX_TRANSCRIPT_LINE_BYTES + 1024)}})
    transcript.write_text(good + "\n" + huge + "\n" + good.replace('"ok"', '"ok2"') + "\n",
                          encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        usage = lc.read_transcript_usage(transcript)

    assert usage["claude-opus-5"].input_tokens == 14, (
        f"the two good lines were not both counted: {usage}")
    assert any("line" in r.message.lower() or "line" in str(r.msg).lower()
               for r in caplog.records), (
        "the oversize line was dropped in SILENCE -- unmeasured spend that says nothing is "
        "indistinguishable from no spend")


def test_the_line_bound_clears_the_largest_line_this_repo_has_ever_written():
    """The bound is DERIVED, with headroom, from the measured corpus rather than picked.

    Largest real line measured 2026-09-15: 1.360 MB, across the 20 largest of 3,108
    transcripts. A bound at or below that would drop legitimate turns; the shipped bound sits
    well above it, so what it catches is corruption, not size.
    """
    largest_real_line_bytes = 1_360_000
    assert lc.MAX_TRANSCRIPT_LINE_BYTES > largest_real_line_bytes * 2, (
        f"the bound {lc.MAX_TRANSCRIPT_LINE_BYTES} leaves less than 2x headroom over the "
        f"largest line actually measured ({largest_real_line_bytes}) -- it would start "
        f"dropping real turns")
