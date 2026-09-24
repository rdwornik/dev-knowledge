"""RED-first witnesses for the re-rank — `[#691]` step 5, AX21-2.

THE CLAUSE, verbatim, because every test here is a leg of it:

    "every call records model, tokens, cost and outcome in the tally; `provider-registry.yaml`
     holds per-role ordered lists that THE ROUTER RE-RANKS BY MEASURED PASS RATE PER COST; the
     log-review routine demotes a provider whose pass rate drops and files the anomaly as a
     row."

And the failure it is written against, from this lane's own contract:

    "a router re-ranked on nothing measured is a fixed list wearing a router's name."

That sentence is the spec for most of this file. A re-rank that quietly returns the declared
order when it has no data LOOKS identical to one that measured and confirmed it — and the
difference is the whole of AX21-2. So the central property under test is not "the ordering is
right"; it is **the re-rank always says whether it measured anything**, and every caller can
tell a measured order from a declared one without inspecting the tally itself.

THE HALF A STATE, which makes this testable and is also its limit: the shipped tally is
EMPTY, because Half A places no calls. So the live re-rank measures nothing and says so, and
every test of actual reordering below seeds a synthetic store. Seeding a store is not placing
a call — no provider is contacted by anything in this file.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def router():
    spec = importlib.util.spec_from_file_location(
        "provider_router", _ROOT / "scripts" / "provider_router.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["provider_router"] = module
    spec.loader.exec_module(module)
    return module


def _seed(router, db, *, provider, role, passed, failed, unknown=0, cost=0.01, model=None):
    """Write N synthetic spans. Not a call — a row in a local SQLite file."""
    for outcome, n in (("passed", passed), ("failed", failed), ("unknown", unknown)):
        for _ in range(n):
            router.record_routing_call(
                role=role, provider=provider, model=model or provider,
                outcome=outcome, cost_usd=cost, db_path=db,
            )


# --- the central property: a declared order never masquerades as a measured one --------------


def test_the_rerank_reports_that_it_measured_nothing_when_the_tally_is_empty(router, tmp_path):
    """THE ONE THAT MATTERS. An empty tally yields the declared order AND
    `measured is False` — so a caller can tell "confirmed by measurement" from "nothing to
    measure", which are the two states a bare list cannot distinguish.
    """
    result = router.rerank("implement", repo=".dev-knowledge", db_path=tmp_path / "empty.db")
    assert result.measured is False
    assert result.order == [c.provider for c in
                            router.route("implement", repo=".dev-knowledge", strict=False)]
    assert "no measured calls" in result.basis.lower()


def test_the_live_tally_is_empty_in_half_a_and_the_rerank_says_so(router):
    """Half A's own boundary, measured rather than asserted: this lane places no calls, so the
    shipped store has nothing in it and the live re-rank is honest about ranking on nothing.

    If this ever goes RED with `measured is True`, either Half B has run or something placed a
    call inside Half A — both of which are things a reader of this lane should be told.
    """
    result = router.rerank("implement", repo=".dev-knowledge")
    assert result.measured is False


def test_a_measured_rerank_says_so_and_names_its_sample(router, tmp_path):
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="verify", passed=10, failed=0)
    result = router.rerank("verify", repo=".dev-knowledge", db_path=db, min_sample=10)
    assert result.measured is True
    assert result.stats["anthropic"].judged == 10


# --- the arithmetic: what counts, and what must not ------------------------------------------


def test_unknown_outcomes_are_excluded_from_the_rate_but_still_counted(router, tmp_path):
    """The reason `unknown` exists as a first-class outcome rather than an omission.

    An unjudged call is not evidence of a pass. Counting it in the denominator would understate
    a provider; omitting it from the record entirely would let `passed / (passed + failed)`
    read a half-measured provider as a fully-measured one. So it is excluded from the RATE and
    reported in the COUNT, and `judged` is the honest sample size.
    """
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="verify", passed=6, failed=2, unknown=12)
    stats = router.measure("verify", db_path=db)["anthropic"]
    assert stats.calls == 20
    assert stats.judged == 8
    assert stats.unknown == 12
    assert stats.pass_rate == pytest.approx(0.75)


def test_a_provider_below_the_minimum_sample_keeps_its_declared_position(router, tmp_path):
    """AX22-1 measures over TEN tasks, and that number is the reason a floor exists at all: a
    provider that passed its only call has a measured pass rate of 1.0, and promoting it on
    that would be ranking on noise while calling it measurement.

    Below the floor the declared position stands and the reason is reported, rather than the
    provider being silently dropped or silently promoted.
    """
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="verify", passed=1, failed=0)
    result = router.rerank("verify", repo=".dev-knowledge", db_path=db, min_sample=10)
    assert result.measured is False
    assert "sample" in result.basis.lower()


def test_pass_rate_per_cost_ranks_the_cheaper_equal_performer_first(router, tmp_path):
    """AX21-2's actual metric. Two providers, identical pass rates, one an order of magnitude
    cheaper — the cheap one wins, and it wins on the tally rather than on a list."""
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="implement", passed=10, failed=0, cost=0.10)
    _seed(router, db, provider="xai", role="implement", passed=10, failed=0, cost=0.01)
    ranked = router.rank_by_score(router.measure("implement", db_path=db), min_sample=10)
    assert ranked[0] == "xai"


def test_a_better_pass_rate_beats_a_cheaper_failure(router, tmp_path):
    """Cost alone is not the metric — the clause says pass rate PER cost. A provider half the
    price that fails most of the time loses to a reliable one."""
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="implement", passed=10, failed=0, cost=0.10)
    _seed(router, db, provider="xai", role="implement", passed=2, failed=8, cost=0.05)
    ranked = router.rank_by_score(router.measure("implement", db_path=db), min_sample=10)
    assert ranked[0] == "anthropic"


def test_a_provider_with_no_recorded_cost_is_not_scored_on_cost(router, tmp_path):
    """An honest limit, reported rather than papered over with a sentinel.

    A subscription-metered provider records no per-call cost, so pass-rate-per-cost is not
    computable for it. Assigning infinity would make it unbeatable; assigning zero would make
    it last. Both are fabrications. It is reported as unscored and keeps its declared position,
    which is the only answer the data supports.
    """
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="verify", passed=10, failed=0, cost=None)
    stats = router.measure("verify", db_path=db)["anthropic"]
    assert stats.pass_rate == pytest.approx(1.0)
    assert stats.score is None
    assert stats.cost_usd == 0.0


# --- the pin AX21-1 puts on orchestration ----------------------------------------------------


def test_a_non_rerankable_role_is_never_reordered_however_good_the_numbers(router, tmp_path):
    """"Orchestration never routes to a cheaper tier ... the one line of the role table that is
    not subject to re-ranking."

    Seeded so a naive re-rank WOULD reorder — a cheap challenger with a perfect record — and
    asserted not to. A pin that is only tested on data that would not have moved it is not
    tested at all.
    """
    db = tmp_path / "t.db"
    _seed(router, db, provider="anthropic", role="orchestrate", passed=10, failed=0, cost=1.00)
    result = router.rerank("orchestrate", repo=".dev-knowledge", db_path=db, min_sample=10)
    assert result.measured is False
    assert "rerankable" in result.basis or "not subject to re-ranking" in result.basis
    assert result.order == ["anthropic"]


# --- reporting the admission state (the step's second, separate act) -------------------------


def test_the_report_names_every_provider_admission_state(router):
    """The contract's step 5, second sentence: *"Report each provider's recorded admission
    state — for every non-Claude entry that state is NOT ADMITTED, and REPORTING IT IS NOT THE
    SAME ACT AS MEASURING IT."*

    So the report reads the registry's recorded verdicts. It runs no trial task and contacts
    no provider; it says what the file says.
    """
    rows = router.admission_report()
    by_provider = {r.provider: r for r in rows}
    assert by_provider["anthropic"].admitted_in, "anthropic holds admission in at least one role"
    # `copilot-enterprise` is the 2026-09-23 exception (operator ruling O-3): ADMITTED on
    # `implement` specifically, still NOT ADMITTED on every other role it appears in. Checked
    # separately below rather than folded into the "admitted nowhere" loop, which now excludes it.
    assert by_provider["copilot-enterprise"].admitted_in == ["implement"]
    for provider in ("xai", "antigravity", "openai"):
        assert by_provider[provider].admitted_in == [], f"{provider} is NOT ADMITTED anywhere"


def test_the_report_distinguishes_reporting_from_measuring(router):
    """The distinction the clause insists on, carried in the artifact rather than left to the
    reader. A report that did not say this could be mistaken for a measurement result."""
    rows = router.admission_report()
    assert all(r.measured is False for r in rows)
    assert all("AX22-1" in r.basis or "not measured" in r.basis.lower() for r in rows)


def test_the_report_carries_the_licence_alongside_the_admission(router):
    """The two gates are independent and a report showing only one invites the wrong
    conclusion. Before 2026-09-23, copilot-enterprise was blocked on BOTH, and an admission
    measurement would not have cleared its licence — that pairing is why the report carries
    both fields at all. Operator ruling O-3 (2026-09-23) cleared its licence repo-wide; its
    `implement` admission followed on in-repo evidence (see `test_provider_router.py`), so both
    fields now read cleared for it, and `xai` — licensed but still genuinely unadmitted
    everywhere — is what still demonstrates the two-fields-are-independent point directly."""
    by_provider = {r.provider: r for r in router.admission_report()}
    assert by_provider["copilot-enterprise"].licence == "permitted"
    assert by_provider["xai"].licence == "permitted"
    assert by_provider["xai"].admitted_in == [], "xai: licensed but still unadmitted anywhere"


# --- the CLI (done-contract item 4: "Click for a CLI where one is warranted") -----------------


def test_the_cli_reports_without_touching_any_provider(router):
    from click.testing import CliRunner

    result = CliRunner().invoke(router.cli, ["report"])
    assert result.exit_code == 0, result.output
    assert "NOT ADMITTED" in result.output
    assert "copilot-enterprise" in result.output


def test_the_cli_route_subcommand_shows_refusals_with_reasons(router):
    from click.testing import CliRunner

    result = CliRunner().invoke(router.cli, ["route", "implement", "--repo", "corp-monorepo"])
    assert result.exit_code == 0, result.output
    assert "off-allowlist" in result.output
    assert "AX22-5" in result.output
