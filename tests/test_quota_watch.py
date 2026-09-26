"""Witnesses for `scripts/quota_watch.py` -- R7 quota watch (LANE-5B2-6-quota-watch).

THE THREE THINGS THIS FILE REFUSES TO LET SLIP, one test class per claim:

  1. **A crossing is a comparison, not a snapshot.** 79% alone means nothing; only a PRIOR read
     makes 81% a crossing. `TestCrossingIsAComparison` walks the contract's own fixture pair
     (79% then 81%) through the ledger and asserts exactly one crossing, at 80%, on the second
     read -- not on the first, and not at 50% or 100%.
  2. **The one hard veto, and only the one.** `TestTheOneHardVeto` asserts `check` refuses a
     Codespaces launch that would cross the 180-core-hour quota and nothing else in this module
     can produce a non-zero exit.
  3. **A crossing WARNS (writes `QUOTA-WARN-<date>.md`); it never refuses.** `TestRecordWarnsNeverRefuses`
     drives the `record` CLI against a tmp transport root and reads the file back through
     `transport.classify`, the same gate a real writer goes through.

Fixtures under `tests/fixtures/quota_watch/` are real `gh api` response SHAPES (the baseline
one is the lane's own 2026-09-26 live read, verbatim) -- never a rate or quota asserted as
"correct" here, only that the number in a report is the number the fixture said.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import quota_watch as qw  # noqa: E402
from scripts import transport as _transport  # noqa: E402

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "quota_watch"


def _load(name: str) -> dict:
    return json.loads((_FIXTURES / name).read_text(encoding="utf-8"))


# --- the declared registry ------------------------------------------------------------------

def test_load_quotas_reads_the_declared_registry():
    quotas = qw.load_quotas()
    assert quotas["codespaces_core_hours"].quota == 180
    assert quotas["codespaces_core_hours"].unit == "core-hours"
    assert quotas["actions_minutes"].quota == 3000
    assert quotas["codespaces_storage"].quota == 20
    assert quotas["codespaces_core_hours"].thresholds == (0.5, 0.8, 1.0)


def test_copilot_is_absent_from_the_declared_registry():
    """Copilot's quota is read LIVE (the API states its own entitlement) -- declaring a second,
    hand-typed copy here would be exactly the drift the registry exists to end."""
    assert "copilot" not in qw.load_quotas()


def test_a_row_with_no_quota_is_skipped_not_defaulted_to_zero(tmp_path):
    reg = tmp_path / "quotas.yaml"
    reg.write_text("account: x\nskus:\n  no_quota_row:\n    unit: widgets\n", encoding="utf-8")
    assert qw.load_quotas(reg) == {}


# --- reading the billing summary ------------------------------------------------------------

def test_core_hours_reads_cores_from_the_sku_name_itself():
    """d2 -> 2 cores, d4 -> 4 cores -- the lane's own 2026-09-26 live read."""
    items, cycle_start = qw.parse_billing_summary(_load("billing_baseline.json"))
    used = qw.codespaces_core_hours_used(items)
    assert used == pytest.approx(8.01392 * 2 + 5.91882 * 4)
    assert cycle_start == date(2026, 9, 1)


def test_actions_minutes_used_reads_the_actions_linux_sku():
    items, _ = qw.parse_billing_summary(_load("billing_baseline.json"))
    assert qw.actions_minutes_used(items) == pytest.approx(5375.0)


def test_storage_is_normalised_from_gigabyte_hours_to_gigabyte_months():
    items, _ = qw.parse_billing_summary(_load("billing_baseline.json"))
    assert qw.codespaces_storage_used(items) == pytest.approx(1.106545569 / 730.0)


def test_a_summary_with_no_time_period_is_refused():
    with pytest.raises(qw.QuotaWatchError):
        qw.parse_billing_summary({"usageItems": []})


def test_first_billed_dollar_is_none_when_every_item_is_fully_discounted():
    items, _ = qw.parse_billing_summary(_load("billing_baseline.json"))
    assert qw.first_billed_dollar(items) is None


def test_first_billed_dollar_names_the_item():
    items, _ = qw.parse_billing_summary(_load("billing_first_billed_dollar.json"))
    billed = qw.first_billed_dollar(items)
    assert billed is not None and billed.sku == "codespaces_compute_d4"
    assert billed.net_amount == pytest.approx(0.36)


def test_copilot_credits_read_from_the_bounded_premium_interactions_snapshot():
    used, entitlement = qw.parse_copilot_credits(_load("copilot_user.json"))
    assert used == 285
    assert entitlement == 22500


def test_copilot_refuses_when_no_bounded_snapshot_is_present():
    with pytest.raises(qw.QuotaWatchError):
        qw.parse_copilot_credits({"quota_snapshots": {"chat": {"unlimited": True}}})


# --- crossing detection: the pure predicate ---------------------------------------------------

class TestCrossingIsAComparison:
    def test_a_first_read_crosses_every_threshold_at_or_below_it(self):
        assert qw.detect_crossings(None, 0.79, (0.5, 0.8, 1.0)) == [0.5]

    def test_79_then_81_crosses_exactly_80_percent(self):
        """The contract's own fixture pair, verbatim: 79% then 81% shows exactly one 80%
        crossing -- not 50% (already behind the prior read) and not 100% (not yet reached)."""
        assert qw.detect_crossings(0.79, 0.81, (0.5, 0.8, 1.0)) == [0.8]

    def test_a_threshold_already_passed_does_not_refire(self):
        assert qw.detect_crossings(0.81, 0.95, (0.5, 0.8, 1.0)) == []

    def test_reaching_the_quota_exactly_crosses_100_percent(self):
        assert qw.detect_crossings(0.95, 1.0, (0.5, 0.8, 1.0)) == [1.0]

    def test_billed_dollar_crossing_fires_once_on_the_false_to_true_edge(self):
        assert qw.detect_billed_dollar_crossing(False, True) is True
        assert qw.detect_billed_dollar_crossing(True, True) is False
        assert qw.detect_billed_dollar_crossing(False, False) is False


class TestProjectedExhaustionIsCappedAtTheCycleReset:
    """Codex terra HIGH (this lane's own review): an uncapped straight-line projection can
    report an exhaustion date past the monthly reset, which is not an exhaustion of THIS
    cycle at all."""

    def test_a_projection_landing_past_the_cycle_reset_reports_no_exhaustion(self):
        quota = qw.SkuQuota(group="g", quota=180.0, unit="core-hours",
                            thresholds=(0.5, 0.8, 1.0), account="rdwornik")
        # 1 core-hour used on day 1 of a 30-day September -> burn 1/day; 179 remaining takes
        # 179 days, landing in March -- long past the 2026-10-01 reset.
        status = qw.sku_status("g", quota, used=1.0, cycle_start=date(2026, 9, 1),
                               now=date(2026, 9, 1))
        assert status.projected_exhaustion is None

    def test_a_projection_landing_inside_the_cycle_is_reported(self):
        quota = qw.SkuQuota(group="g", quota=10.0, unit="core-hours",
                            thresholds=(0.5, 0.8, 1.0), account="rdwornik")
        # 9 used by day 5 -> burn 1.8/day; 1 remaining exhausts in <1 day, well inside September.
        status = qw.sku_status("g", quota, used=9.0, cycle_start=date(2026, 9, 1),
                               now=date(2026, 9, 5))
        assert status.projected_exhaustion is not None
        assert status.projected_exhaustion < date(2026, 10, 1)

    def test_cycle_end_rolls_over_december_into_january(self):
        assert qw._cycle_end(date(2026, 12, 1)) == date(2027, 1, 1)


class TestLedgerLockSerializesConcurrentRecords:
    """Codex terra HIGH (this lane's own review): two concurrent `record` invocations reading
    the same prior row could both claim the same crossing. `_LedgerLock` is the fix; these
    tests exercise the lock mechanics directly rather than a real race (which is timing-
    dependent and not reproducible in a unit test)."""

    def test_a_held_lock_blocks_a_second_acquire_until_released(self, tmp_path):
        ledger = tmp_path / "QUOTA-READS.jsonl"
        lock = qw._LedgerLock(ledger, timeout_s=0.3)
        with lock:
            second = qw._LedgerLock(ledger, timeout_s=0.3)
            with pytest.raises(qw.QuotaWatchError):
                with second:
                    pass  # unreachable: the outer lock is still held

    def test_the_lock_releases_and_can_be_reacquired(self, tmp_path):
        ledger = tmp_path / "QUOTA-READS.jsonl"
        with qw._LedgerLock(ledger, timeout_s=1.0):
            pass
        with qw._LedgerLock(ledger, timeout_s=1.0):
            pass  # no timeout: the first `with` released it


class TestRecordReadAgainstTheLedger:
    """`record_read` ties the pure predicate to a persisted ledger row per SKU-group+cycle --
    the thing that makes "79% then 81%" possible across two separate process invocations."""

    def _quota(self):
        return qw.SkuQuota(group="codespaces_core_hours", quota=180.0, unit="core-hours",
                           thresholds=(0.5, 0.8, 1.0), account="rdwornik")

    def test_the_79_then_81_fixture_pair_shows_exactly_one_80_percent_crossing(self, tmp_path):
        ledger = tmp_path / "QUOTA-READS.jsonl"
        quota = self._quota()

        items_79, cycle = qw.parse_billing_summary(_load("billing_79pct.json"))
        used_79 = qw.codespaces_core_hours_used(items_79)
        assert used_79 == pytest.approx(142.2)
        first = qw.record_read(ledger, "codespaces_core_hours", quota, used_79, cycle,
                               billed=False)
        assert first.crossings == ("50%",)  # first read this cycle: crosses 50%, not 80%

        items_81, _ = qw.parse_billing_summary(_load("billing_81pct.json"))
        used_81 = qw.codespaces_core_hours_used(items_81)
        assert used_81 == pytest.approx(145.8)
        second = qw.record_read(ledger, "codespaces_core_hours", quota, used_81, cycle,
                                billed=False)
        assert second.crossings == ("80%",)

        # exactly two rows -- one per read, append-only
        assert len(qw.read_ledger(ledger)) == 2

    def test_a_third_read_still_above_80_does_not_refire(self, tmp_path):
        ledger = tmp_path / "QUOTA-READS.jsonl"
        quota = self._quota()
        cycle = date(2026, 9, 1)
        qw.record_read(ledger, "codespaces_core_hours", quota, 145.8, cycle, billed=False)
        third = qw.record_read(ledger, "codespaces_core_hours", quota, 150.0, cycle, billed=False)
        assert third.crossings == ()

    def test_the_first_billed_dollar_fixture_warns(self, tmp_path):
        ledger = tmp_path / "QUOTA-READS.jsonl"
        quota = self._quota()
        items_before, cycle = qw.parse_billing_summary(_load("billing_unbilled.json"))
        used = qw.codespaces_core_hours_used(items_before)
        before = qw.record_read(ledger, "codespaces_core_hours", quota, used, cycle, billed=False)
        assert "FIRST_BILLED_DOLLAR" not in before.crossings

        items_after, _ = qw.parse_billing_summary(_load("billing_first_billed_dollar.json"))
        billed_now = qw.first_billed_dollar(items_after) is not None
        assert billed_now is True
        after = qw.record_read(ledger, "codespaces_core_hours", quota, used, cycle,
                               billed=billed_now)
        assert after.crossings == ("FIRST_BILLED_DOLLAR",)


# --- the one hard veto -------------------------------------------------------------------------

class TestTheOneHardVeto:
    def test_a_launch_that_would_cross_the_quota_is_refused(self):
        verdict = qw.codespaces_launch_check(used_core_hours=170.0, projected_core_hours=16.0,
                                             quota=180.0)
        assert verdict.refused is True
        assert "REFUSED" in verdict.reason

    def test_a_launch_that_fits_is_not_refused(self):
        verdict = qw.codespaces_launch_check(used_core_hours=100.0, projected_core_hours=16.0,
                                             quota=180.0)
        assert verdict.refused is False
        assert "OK" in verdict.reason

    def test_landing_exactly_on_the_quota_is_not_a_crossing(self):
        verdict = qw.codespaces_launch_check(used_core_hours=164.0, projected_core_hours=16.0,
                                             quota=180.0)
        assert verdict.refused is False

    def test_a_negative_projection_is_refused_at_the_function_boundary(self):
        """Codex terra HIGH (this lane's own review): a negative projection would SUBTRACT from
        cumulative usage and could turn a real crossing into a false OK -- for the one command
        in this module allowed to refuse a launch."""
        with pytest.raises(ValueError):
            qw.codespaces_launch_check(used_core_hours=170.0, projected_core_hours=-50.0,
                                       quota=180.0)

    def test_check_cli_refuses_a_negative_projection_before_computing_anything(self):
        from click.testing import CliRunner
        result = CliRunner().invoke(qw.cli, [
            "check", "--projected-core-hours", "-1",
            "--billing-json", str(_FIXTURES / "billing_baseline.json")])
        assert result.exit_code != 0
        assert "REFUSED" not in result.output  # never reads as the real veto's own message

    def test_check_cli_exits_1_on_refusal(self):
        from click.testing import CliRunner
        result = CliRunner().invoke(qw.cli, [
            "check", "--projected-core-hours", "1000",
            "--billing-json", str(_FIXTURES / "billing_baseline.json")])
        assert result.exit_code == 1
        assert "REFUSED" in result.output

    def test_check_cli_exits_0_when_it_fits(self):
        from click.testing import CliRunner
        result = CliRunner().invoke(qw.cli, [
            "check", "--projected-core-hours", "1",
            "--billing-json", str(_FIXTURES / "billing_baseline.json")])
        assert result.exit_code == 0
        assert "OK" in result.output


# --- record warns, never refuses ----------------------------------------------------------------

class TestRecordWarnsNeverRefuses:
    def test_a_crossing_writes_quota_warn_through_the_registered_transport_gate(self, tmp_path):
        from click.testing import CliRunner
        transport_root = tmp_path / "transport"
        (transport_root / "to-browser").mkdir(parents=True)
        repo_root = tmp_path / "repo"
        repo_root.mkdir()

        runner = CliRunner()
        # First read establishes the baseline (crosses 50%, not 80%; writes nothing yet since
        # only a >=80% or billed-dollar crossing is warn-worthy in this scenario's numbers --
        # but ANY crossing writes, so assert the file after the SECOND read instead).
        r1 = runner.invoke(qw.cli, [
            "record", "--sku-group", "codespaces_core_hours",
            "--billing-json", str(_FIXTURES / "billing_79pct.json"),
            "--repo-root", str(repo_root), "--transport-root", str(transport_root)])
        assert r1.exit_code == 0, r1.output

        r2 = runner.invoke(qw.cli, [
            "record", "--sku-group", "codespaces_core_hours",
            "--billing-json", str(_FIXTURES / "billing_81pct.json"),
            "--repo-root", str(repo_root), "--transport-root", str(transport_root)])
        assert r2.exit_code == 0, r2.output
        assert "80%" in r2.output

        written = list((transport_root / "to-browser").glob("QUOTA-WARN-*.md"))
        assert len(written) == 1, written
        content = written[0].read_text(encoding="utf-8")
        assert "codespaces_core_hours" in content
        assert "80%" in content

        # the write went through the SAME registered gate a real writer does
        registry = _transport.load_registry()
        kind = _transport.classify(written[0].name, registry)
        assert kind is not None and kind.name == "QUOTA_WARN"
        assert "quota_watch" in kind.writers

    def test_no_write_flag_never_touches_the_transport(self, tmp_path):
        """A first read at 79% crosses 50% -- a crossing, and warn-worthy -- but `--no-write`
        must suppress the write even so; the transport stays empty."""
        from click.testing import CliRunner
        transport_root = tmp_path / "transport"
        (transport_root / "to-browser").mkdir(parents=True)
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = CliRunner().invoke(qw.cli, [
            "record", "--sku-group", "codespaces_core_hours", "--no-write",
            "--billing-json", str(_FIXTURES / "billing_79pct.json"),
            "--repo-root", str(repo_root), "--transport-root", str(transport_root)])
        assert result.exit_code == 0, result.output
        assert "50%" in result.output
        assert list((transport_root / "to-browser").glob("QUOTA-WARN-*.md")) == []

    def test_record_cli_never_exits_non_zero_for_a_crossing(self, tmp_path):
        """R7's Do-not: only `check`'s Codespaces core-hour veto may refuse a launch. `record`
        writes a warning and exits 0 even when every threshold is crossed at once."""
        from click.testing import CliRunner
        transport_root = tmp_path / "transport"
        (transport_root / "to-browser").mkdir(parents=True)
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = CliRunner().invoke(qw.cli, [
            "record",
            "--billing-json", str(_FIXTURES / "billing_first_billed_dollar.json"),
            "--repo-root", str(repo_root), "--transport-root", str(transport_root)])
        assert result.exit_code == 0, result.output


# --- the digest cost line -----------------------------------------------------------------------

def test_cost_line_reports_every_figure_the_contract_names():
    from click.testing import CliRunner
    result = CliRunner().invoke(qw.cli, [
        "line",
        "--billing-json", str(_FIXTURES / "billing_baseline.json"),
        "--copilot-json", str(_FIXTURES / "copilot_user.json"),
        "--cloud-sessions", "3"])
    assert result.exit_code == 0, result.output
    assert "Codespaces" in result.output and "core-hours" in result.output
    assert "Actions" in result.output
    assert "Copilot" in result.output and "22500" in result.output
    assert "cloud sessions: 3" in result.output


def test_cost_line_says_UNREAD_rather_than_a_silent_zero_when_copilot_cannot_be_read(tmp_path):
    from click.testing import CliRunner
    bad_copilot = tmp_path / "copilot.json"
    bad_copilot.write_text("{}", encoding="utf-8")
    result = CliRunner().invoke(qw.cli, [
        "line",
        "--billing-json", str(_FIXTURES / "billing_baseline.json"),
        "--copilot-json", str(bad_copilot)])
    assert result.exit_code == 0, result.output
    assert "Copilot UNREAD" in result.output
    assert "cloud sessions: not recorded" in result.output


# --- wiring: the dispatcher and integrator templates carry the two call sites -------------------

def test_dispatcher_template_runs_the_pre_launch_veto():
    text = (REPO_ROOT / "templates" / "dispatcher-order-template.md").read_text(encoding="utf-8")
    assert "quota_watch.py check --projected-core-hours" in text


def test_integrator_template_writes_the_close_cost_line():
    text = (REPO_ROOT / "templates" / "integrator-order-template.md").read_text(encoding="utf-8")
    assert "quota_watch.py line" in text
