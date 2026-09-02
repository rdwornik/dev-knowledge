"""Tests for the deploy-runbook waiver-honoring fix ([#276] D2, LANE d-4).

deploy/carrier_precommit.py:777 `_classify_prune` used to return PRESENT_MODIFIED
(REFUSE) with no waiver input at all -- a consumer-declared divergence in the
consumer's own `.methodology.yaml` was invisible to the deploy tool, so BOTH legs
broke on it: the prune sweep REFUSE-aborted the whole instantiation, and the
add/converge leg re-appended a hook the consumer had legitimately excluded.

Covers [#276]'s Done-when verbatim, both directions:

- PRUNE leg: a consumer-declared divergence -> the sweep SKIPs it (ALREADY_ABSENT,
  no REFUSE, nothing removed) -- proven on BOTH live-corpus shapes (ruling 3,
  docs/audits/2026-09-01-technical-ruff-gate-divergence-classification.md):
  ai-council's bare `id: ruff` re-activation, and corp-monorepo's `args: []`
  ruff-format omission. A CONTRAST test proves the undeclared case still REFUSEs
  (the mechanism discriminates, it does not blanket-disable the hash-guard).
- ADD/converge leg: a consumer-declared divergence for a required hub-hook id ->
  detect/apply/verify treat it as NOT required, so `--execute` never re-appends it
  and verify does not demand it back.

Fixtures are temp repo dirs with crafted .pre-commit-config.yaml + .methodology.yaml
-- no network, no real consumer repos, exactly the existing carrier test style
(tests/test_deploy_precommit.py, tests/test_deploy_prune.py).
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


import carrier_precommit as cp  # noqa: E402
from contract import CarrierState, PruneState  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_V120 = yaml.safe_load(
    (_REPO_ROOT / "deploy" / "manifest-v1.2.0.yaml").read_text(encoding="utf-8")
)
_RUFF_COMPONENT = next(c for c in _V120["components"] if c["id"] == "ruff-gate")
_RUFF_REPO = _RUFF_COMPONENT["prune"]["match"]["repo"]
_RUFF_EXPECTED = _RUFF_COMPONENT["prune"]["expected"]  # {rev: v0.15.5, hooks: [{id: ruff, name:..., args: []}]}


def _carrier(repo: Path) -> cp.PrecommitCarrier:
    return cp.PrecommitCarrier(repo)


def _write_config(repo: Path, data: dict) -> Path:
    path = repo / ".pre-commit-config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")
    return path


def _write_methodology_yaml(repo: Path, *, component: str, reason: str = "consumer-owned; see JOURNAL",
                            review_date: str = "2099-01-01") -> Path:
    """A minimal consumer `.methodology.yaml` -- the SAME shape/field-names the hub's
    own root file and the Informant (scripts/enforcement_coverage.py) already use."""
    path = repo / ".methodology.yaml"
    path.write_text(
        "sanctioned_divergences:\n"
        f"  - component: {component}\n"
        f"    reason: >-\n"
        f"      {reason}\n"
        f"    review_date: {review_date}\n",
        encoding="utf-8", newline="\n",
    )
    return path


# ---------------------------------------------------------------------------
# _waived_components -- the single reader.
# ---------------------------------------------------------------------------


def test_waived_components_empty_when_file_absent(tmp_path):
    assert cp._waived_components(tmp_path) == frozenset()


def test_waived_components_reads_declared_component(tmp_path):
    _write_methodology_yaml(tmp_path, component="ruff-gate")
    assert cp._waived_components(tmp_path) == frozenset({"ruff-gate"})


def test_waived_components_ignores_entry_with_no_reason(tmp_path):
    (tmp_path / ".methodology.yaml").write_text(
        "sanctioned_divergences:\n"
        "  - component: ruff-gate\n"
        "    reason: ''\n"
        "    review_date: 2099-01-01\n",
        encoding="utf-8", newline="\n",
    )
    assert cp._waived_components(tmp_path) == frozenset()


# ---------------------------------------------------------------------------
# Date handling fails CLOSED ([#276] Done-contract item 2, LANE g-276). Terra
# recorded the LANE d-4 shape (shape-only: reason present -> honored, dates never
# inspected) as failing OPEN on bad dates -- a waiver whose date is missing,
# unparseable, or in the past must NOT be honored on either leg. Each case here is
# a bare `.methodology.yaml` write (not the review_date="2099-01-01" default from
# `_write_methodology_yaml`) so the date defect is the ONLY variable.
# ---------------------------------------------------------------------------


def test_waived_components_refuses_entry_with_no_date(tmp_path):
    """Waiver MISSING: a reason but no expiry/review_date at all -- not honored."""
    (tmp_path / ".methodology.yaml").write_text(
        "sanctioned_divergences:\n"
        "  - component: ruff-gate\n"
        "    reason: >-\n"
        "      consumer-owned; see JOURNAL\n",
        encoding="utf-8", newline="\n",
    )
    assert cp._waived_components(tmp_path) == frozenset()


def test_waived_components_refuses_entry_with_unparseable_date(tmp_path):
    """Waiver INVALID: the date field is present but not ISO-8601 -- not honored."""
    (tmp_path / ".methodology.yaml").write_text(
        "sanctioned_divergences:\n"
        "  - component: ruff-gate\n"
        "    reason: >-\n"
        "      consumer-owned; see JOURNAL\n"
        "    review_date: not-a-date\n",
        encoding="utf-8", newline="\n",
    )
    assert cp._waived_components(tmp_path) == frozenset()


def test_waived_components_refuses_expired_entry(tmp_path):
    """Waiver EXPIRED: a well-formed date that has already passed -- not honored."""
    (tmp_path / ".methodology.yaml").write_text(
        "sanctioned_divergences:\n"
        "  - component: ruff-gate\n"
        "    reason: >-\n"
        "      consumer-owned; see JOURNAL\n"
        "    review_date: 2020-01-01\n",
        encoding="utf-8", newline="\n",
    )
    assert cp._waived_components(tmp_path) == frozenset()


def test_waived_components_honors_a_valid_unexpired_date(tmp_path):
    """Contrast: a well-formed, not-yet-passed date IS honored -- the fix
    discriminates, it does not blanket-disable the waiver."""
    _write_methodology_yaml(tmp_path, component="ruff-gate", review_date="2099-01-01")
    assert cp._waived_components(tmp_path) == frozenset({"ruff-gate"})


def test_prune_refuses_on_an_expired_waiver(tmp_path):
    """End-to-end, prune leg: an expired waiver does not lift the hash-guard REFUSE."""
    _write_config(tmp_path, {"repos": [_ai_council_ruff_entry()]})
    _write_methodology_yaml(tmp_path, component="ruff-gate", review_date="2020-01-01")
    car = _carrier(tmp_path)
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_MODIFIED
    assert car.prune(_RUFF_COMPONENT).refused


def test_add_leg_re_adds_the_hook_on_an_expired_waiver(tmp_path):
    """End-to-end, add leg: an expired waiver does not excuse the hook -- DRIFTED,
    and --execute re-appends it, same as the no-waiver baseline."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    _write_methodology_yaml(tmp_path, component=_WAIVED_HOOK, review_date="2020-01-01")
    car = _carrier(tmp_path)
    assert car.detect(_hub_hooks_target()) is CarrierState.PRESENT_DRIFTED
    result = car.apply(_hub_hooks_target())
    assert result.changed is True
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ids = {h["id"] for e in data["repos"] for h in e.get("hooks", [])}
    assert _WAIVED_HOOK in ids


# ---------------------------------------------------------------------------
# PRUNE leg -- [#276]'s two live divergences (ruling 3), each in both directions.
# ---------------------------------------------------------------------------


def _ai_council_ruff_entry() -> dict:
    """Live shape: ai-council's re-activated consumer-owned gate -- bare `id: ruff`,
    no `name:` (fleet ruling 2026-07-12 overriding the [#244] prune)."""
    return {"repo": _RUFF_REPO, "rev": _RUFF_EXPECTED["rev"], "hooks": [{"id": "ruff"}]}


def _corp_monorepo_ruff_entry() -> dict:
    """Live shape: corp-monorepo's own unified gate -- `args: []`, ruff-format
    omitted (core.autocrlf=true CRLF/LF collision), no `name:`."""
    return {
        "repo": _RUFF_REPO, "rev": _RUFF_EXPECTED["rev"],
        "hooks": [{"id": "ruff", "args": []}],
    }


@pytest.mark.parametrize(
    "entry_factory", [_ai_council_ruff_entry, _corp_monorepo_ruff_entry],
    ids=["ai-council-shape", "corp-monorepo-shape"],
)
def test_prune_refuses_without_a_waiver(tmp_path, entry_factory):
    """Baseline (the bug, still true when nothing is declared): a byte-divergent
    consumer-owned ruff entry REFUSEs the prune -- the hash-guard doing its job."""
    _write_config(tmp_path, {"repos": [entry_factory()]})
    car = _carrier(tmp_path)
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_MODIFIED
    result = car.prune(_RUFF_COMPONENT)
    assert result.pruned is False
    assert result.refused  # REFUSE-abort's evidence trail


@pytest.mark.parametrize(
    "entry_factory", [_ai_council_ruff_entry, _corp_monorepo_ruff_entry],
    ids=["ai-council-shape", "corp-monorepo-shape"],
)
def test_prune_skips_a_declared_divergence(tmp_path, entry_factory):
    """[#276] Done-when, prune leg: a consumer-declared divergence -> the sweep
    SKIPs it -- no REFUSE, nothing removed, the entry is left byte-untouched."""
    _write_config(tmp_path, {"repos": [entry_factory()]})
    _write_methodology_yaml(tmp_path, component="ruff-gate")
    car = _carrier(tmp_path)

    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.ALREADY_ABSENT

    before = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    result = car.prune(_RUFF_COMPONENT)
    assert result.pruned is False
    assert result.refused == ()  # not a REFUSE -- a skip
    after = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert after == before  # untouched


def test_prune_waiver_is_per_component_id(tmp_path):
    """A waiver declared for a DIFFERENT component id does not blanket-suppress the
    hash-guard -- the mechanism discriminates by exact id, not by presence of the
    allowlist file."""
    _write_config(tmp_path, {"repos": [_ai_council_ruff_entry()]})
    _write_methodology_yaml(tmp_path, component="some-other-component")
    car = _carrier(tmp_path)
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_MODIFIED
    assert car.prune(_RUFF_COMPONENT).refused


def test_prune_already_absent_is_unaffected_by_waiver(tmp_path):
    """A waiver does not change the genuinely-absent case -- both read ALREADY_ABSENT,
    for different reasons, and prune stays a no-op either way."""
    _write_config(tmp_path, {"repos": []})
    _write_methodology_yaml(tmp_path, component="ruff-gate")
    car = _carrier(tmp_path)
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.ALREADY_ABSENT
    result = car.prune(_RUFF_COMPONENT)
    assert result.pruned is False
    assert result.refused == ()


# ---------------------------------------------------------------------------
# ADD/converge leg -- a required hub-hook id the consumer excludes.
# ---------------------------------------------------------------------------

_HUB_REPO = "https://github.com/rdwornik/dev-knowledge"
_HUB_REV = "v1.5.0"
_WAIVED_HOOK = "codemap-freshness"  # #276's original live example (FOLD 2026-07-11)
_KEPT_HOOK = "toc-freshness"


def _hub_hooks_target() -> dict:
    return {
        "config_path": ".pre-commit-config.yaml",
        "required_repos": [],
        "hub_hooks": {
            "rev": _HUB_REV,
            "marker_hook_ids": [_WAIVED_HOOK, _KEPT_HOOK],
            "repo": _HUB_REPO,
            "hooks": [{"id": _WAIVED_HOOK}, {"id": _KEPT_HOOK}],
        },
    }


def _consumer_missing_waived_hook() -> dict:
    """A previously-deployed consumer's hub-hooks entry: present, at the right rev,
    but missing the hook the consumer declared excluded (the #276 FOLD shape)."""
    return {"repos": [{"repo": _HUB_REPO, "rev": _HUB_REV, "hooks": [{"id": _KEPT_HOOK}]}]}


def test_classify_drifted_without_a_waiver(tmp_path):
    """Baseline: a missing required hub-hook id is DRIFTED when nothing is declared."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    car = _carrier(tmp_path)
    assert car.detect(_hub_hooks_target()) is CarrierState.PRESENT_DRIFTED


def test_apply_re_adds_the_hook_without_a_waiver(tmp_path):
    """Baseline: --execute's apply() re-appends the missing hook -- the #276 bug
    ('re-adding it breaks them') when the consumer has NOT declared the exclusion."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    car = _carrier(tmp_path)
    result = car.apply(_hub_hooks_target())
    assert result.changed is True
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ids = {h["id"] for e in data["repos"] for h in e.get("hooks", [])}
    assert _WAIVED_HOOK in ids


def test_classify_correct_when_hook_is_waived(tmp_path):
    """[#276] Done-when, add leg: a declared divergence for the missing hook id ->
    it is NOT required -> the carrier reads PRESENT_CORRECT, not DRIFTED."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    _write_methodology_yaml(tmp_path, component=_WAIVED_HOOK)
    car = _carrier(tmp_path)
    assert car.detect(_hub_hooks_target()) is CarrierState.PRESENT_CORRECT


def test_apply_never_re_adds_a_waived_hook(tmp_path):
    """apply() is a no-op -- the waived hook is never appended, on a previously-
    deployed (present-but-incomplete) consumer."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    _write_methodology_yaml(tmp_path, component=_WAIVED_HOOK)
    car = _carrier(tmp_path)

    result = car.apply(_hub_hooks_target())
    assert result.changed is False

    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ids = {h["id"] for e in data["repos"] for h in e.get("hooks", [])}
    assert _WAIVED_HOOK not in ids
    assert _KEPT_HOOK in ids  # the non-waived requirement still holds


def test_verify_does_not_demand_a_waived_hook_back(tmp_path):
    """verify() (D9-independent of detect/apply) also honors the waiver -- else a
    consumer whose apply correctly skipped the hook would fail verify demanding it,
    aborting execute() on the very divergence it declared."""
    _write_config(tmp_path, _consumer_missing_waived_hook())
    _write_methodology_yaml(tmp_path, component=_WAIVED_HOOK)
    car = _carrier(tmp_path)
    result = car.verify(_hub_hooks_target())
    assert result.ok is True
    assert result.failures == ()


def test_waiver_does_not_excuse_a_different_missing_hook(tmp_path):
    """Discrimination check, add leg: waiving one hook id does not waive the OTHER
    required hook -- a genuinely missing, non-waived hook still DRIFTS and still
    fails verify. The entry carries the WAIVED hook (so it is findable at all) but
    is missing the KEPT one -- inverted from the earlier fixture on purpose."""
    _write_config(
        tmp_path,
        {"repos": [{"repo": _HUB_REPO, "rev": _HUB_REV, "hooks": [{"id": _WAIVED_HOOK}]}]},
    )
    _write_methodology_yaml(tmp_path, component=_WAIVED_HOOK)
    car = _carrier(tmp_path)
    assert car.detect(_hub_hooks_target()) is CarrierState.PRESENT_DRIFTED
    failures = car.verify(_hub_hooks_target()).failures
    assert any(_KEPT_HOOK in f for f in failures)
    assert not any(_WAIVED_HOOK in f for f in failures)
