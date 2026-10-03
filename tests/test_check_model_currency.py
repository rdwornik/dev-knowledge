"""Model currency (R61): the registry lists the ids served on 2026-10-03 with evidence, and one
check lists every pinned id and flags what the registry lacks or has not verified for 14 days.

Lane `foundation-10-model-currency`, Done-contract items 1 and 2. Every test here is an
OUTCOME test written before the code it exercises (RED on origin/main `3157d69b`):

* Item 1 -- the registry lists `claude-opus-5-5`, `claude-sonnet-5-5`, `grok-4.7`,
  `gpt-5.6-terra` and `gemini-3.8-flash` (agy 1.2.16) each with `last_verified: 2026-10-03`
  and an evidence reference that resolves; the schema accepts the new fields.
* Item 2 -- `scripts/check_model_currency.py`: a fixture with an unknown id and a 15-day-old
  entry has both flagged; a clean fixture has none; the same check is an `audit.py health`
  finding at WARN and adds no blocking hook.

The registry tests do NOT import the new script, so they fail for their own reason (the entry
is missing) rather than for an ImportError. The script tests import it inside a fixture, never
through `importorskip`: a missing module is a failure here, not a skip.
"""
from __future__ import annotations

import copy
import datetime
import os
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import provider_registry as preg  # noqa: E402

from ecosystem.schema.provider_registry import ProviderRegistry  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The day the five ids below were read as served (N2 of the lane contract).
_SERVED_DAY = datetime.date(2026, 10, 3)

#: id -> provider the row must sit under. `gemini-3.8-flash` is reached through `agy`, which
#: the registry declares as the `antigravity` provider.
_SERVED_TODAY = {
    "claude-opus-5-5": "anthropic",
    "claude-sonnet-5-5": "anthropic",
    "grok-4.7": "xai",
    "gpt-5.6-terra": "openai",
    "gemini-3.8-flash": "antigravity",
}

_TRANSPORT_PREFIX = "transport:"


def _as_date(value) -> datetime.date | None:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    return datetime.date.fromisoformat(str(value))


# --- Done item 1: the registry lists the ids served today -----------------------------------

@pytest.mark.parametrize("model_id", sorted(_SERVED_TODAY))
def test_registry_lists_each_served_id_with_its_date_and_evidence(model_id: str) -> None:
    models = preg.models()
    assert model_id in models, f"`{model_id}` was served on 2026-10-03 and is not in the registry"
    row = models[model_id]
    assert row["provider"] == _SERVED_TODAY[model_id]
    assert _as_date(row.get("last_verified")) == _SERVED_DAY
    evidence = row.get("evidence") or []
    assert evidence, f"`{model_id}` carries a last_verified date and no evidence"


@pytest.mark.parametrize("model_id", sorted(_SERVED_TODAY))
def test_each_served_ids_evidence_resolves_in_the_repository(model_id: str) -> None:
    """At least one reference per row is an in-repo path that exists; a `transport:` reference
    may ride beside it but never stands alone (CI cannot read the transport)."""
    evidence = preg.models()[model_id].get("evidence") or []
    in_repo = [e for e in evidence if not str(e).startswith(_TRANSPORT_PREFIX)]
    assert in_repo, f"`{model_id}`: every evidence reference is transport-only: {evidence}"
    for ref in in_repo:
        assert (_REPO_ROOT / ref).is_file(), f"`{model_id}`: evidence `{ref}` does not resolve"


def test_the_agy_version_note_names_the_served_release() -> None:
    """The antigravity comment still read 1.1.21 (R66 E3); agy 1.2.16 served Gemini 3.8 Flash."""
    text = (_REPO_ROOT / "ecosystem" / "provider-registry.yaml").read_text(encoding="utf-8")
    assert "1.2.16" in text


def test_only_the_role_pins_whose_seams_sit_in_this_lanes_files_move() -> None:
    """N3: the `sonnet` re-pin moves seams outside this lane's files (`dispatch.py`
    MODEL_ALIASES, `plan_lint.py`), so `roles.implement` stays on `claude-sonnet-5` and the gap
    is a ROWS-OWED line. No seam outside the registry names an `xai` model, so both `xai` role
    entries move to the id served on 2026-10-03 and their stale-pin exceptions go."""
    roles = preg.roles()
    assert roles["implement"]["order"][0]["model"] == "claude-sonnet-5"
    xai = [e for spec in roles.values() for e in spec["order"] if e["provider"] == "xai"]
    assert len(xai) == 2
    assert all(e["model"] == "grok-4.7" for e in xai), [e["model"] for e in xai]
    assert all(e.get("currency_exception") is None for e in xai)


def _registry_dict() -> dict:
    return copy.deepcopy(preg.load_registry())


def test_the_schema_accepts_last_verified_and_evidence() -> None:
    data = _registry_dict()
    data["models"]["claude-opus-5-5"]["last_verified"] = datetime.date(2026, 10, 3)
    data["models"]["claude-opus-5-5"]["evidence"] = ["docs/audits/x.md", "transport:to-browser/y.md"]
    ProviderRegistry.model_validate(data)


def test_the_schema_refuses_a_date_with_no_evidence() -> None:
    """A verification date nobody can check is an assertion, not a record (R59)."""
    data = _registry_dict()
    data["models"]["claude-opus-5-5"]["last_verified"] = datetime.date(2026, 10, 3)
    data["models"]["claude-opus-5-5"]["evidence"] = []
    with pytest.raises(ValueError, match="names nothing to check"):
        ProviderRegistry.model_validate(data)


@pytest.mark.parametrize("bad", ["/abs/path.md", "../outside.md", "C:\\x\\y.md", "transport:",
                                 "", ".", "docs/audits/", "transport:."])
def test_the_schema_refuses_an_evidence_reference_that_cannot_resolve(bad: str) -> None:
    data = _registry_dict()
    data["models"]["claude-opus-5-5"]["last_verified"] = datetime.date(2026, 10, 3)
    data["models"]["claude-opus-5-5"]["evidence"] = [bad]
    with pytest.raises(ValueError, match="not a resolvable evidence reference|is blank"):
        ProviderRegistry.model_validate(data)


# --- Done item 2: the check script ----------------------------------------------------------

@pytest.fixture()
def cmc():
    import check_model_currency as module

    return module


_TODAY = datetime.date(2026, 10, 10)


def _make_root(tmp_path: Path, rows: dict[str, tuple[datetime.date | None, bool]], *,
               templates: dict[str, str] | None = None,
               extra_files: dict[str, str] | None = None) -> Path:
    """A minimal repository: a valid registry plus templates and contracts.

    `rows` maps a model id to (last_verified, evidence_file_exists)."""
    root = tmp_path / "repo"
    (root / "ecosystem").mkdir(parents=True)
    models: dict[str, dict] = {}
    for model_id, (last_verified, evidence_exists) in rows.items():
        row: dict = {"provider": "anthropic"}
        if last_verified is not None:
            ref = f"docs/audits/{model_id}.md"
            row["last_verified"] = last_verified
            row["evidence"] = [ref]
            if evidence_exists:
                (root / ref).parent.mkdir(parents=True, exist_ok=True)
                (root / ref).write_text("served\n", encoding="utf-8")
        models[model_id] = row
    registry = {"providers": {"anthropic": {"display_name": "Anthropic"}}, "models": models}
    (root / "ecosystem" / "provider-registry.yaml").write_text(
        yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
    for rel, text in (templates or {}).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for rel, text in (extra_files or {}).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def _days_ago(n: int) -> datetime.date:
    return _TODAY - datetime.timedelta(days=n)


def _kinds(report) -> set[tuple[str, str]]:
    return {(f.kind, f.model_id) for f in report.flags}


def test_a_clean_fixture_flags_nothing(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)},
                      templates={"templates/t.md": "the lane runs on claude-sonnet-5-5 today\n"})
    live = tmp_path / "LANE-live.md"
    live.write_text("| claude-sonnet-5-5 | execute | high |\n", encoding="utf-8")
    report = cmc.analyse(root, contracts=[live], today=_TODAY)
    assert report.flags == []
    assert cmc.main(["--root", str(root), "--contracts", str(live), "--today", _TODAY.isoformat()]) == 0


def test_an_unknown_id_and_a_fifteen_day_old_entry_are_both_flagged(cmc, tmp_path: Path, capsys) -> None:
    root = _make_root(
        tmp_path,
        {"claude-sonnet-5-5": (_days_ago(1), True), "claude-opus-4-8": (_days_ago(15), True)},
        templates={"templates/t.md": "pin claude-opus-9-9 here\n"},
    )
    report = cmc.analyse(root, today=_TODAY)
    assert _kinds(report) == {("unknown-id", "claude-opus-9-9"), ("stale", "claude-opus-4-8")}
    code = cmc.main(["--root", str(root), "--today", _TODAY.isoformat()])
    out = capsys.readouterr().out
    assert code == 1
    assert "FLAG unknown-id claude-opus-9-9" in out
    assert "FLAG stale claude-opus-4-8" in out


def test_fourteen_days_is_fresh_and_fifteen_is_stale(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(14), True),
                                 "claude-opus-5-5": (_days_ago(15), True)})
    assert _kinds(cmc.analyse(root, today=_TODAY)) == {("stale", "claude-opus-5-5")}


def test_an_entry_with_no_last_verified_reads_stale(cmc, tmp_path: Path) -> None:
    """No evidence is not fresh (R59): an absent date is flagged, never read as current."""
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (None, False)})
    report = cmc.analyse(root, today=_TODAY)
    assert _kinds(report) == {("unverified", "claude-sonnet-5-5")}


def test_an_evidence_reference_that_does_not_resolve_is_flagged(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), False)})
    assert _kinds(cmc.analyse(root, today=_TODAY)) == {("evidence-missing", "claude-sonnet-5-5")}


def test_every_pinned_id_is_listed_with_where_it_is_pinned(cmc, tmp_path: Path, capsys) -> None:
    root = _make_root(
        tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)},
        templates={"templates/t.md": "line one\nuses claude-sonnet-5-5 here\n"},
        extra_files={"docs/LANE-x.md": "launch --model claude-sonnet-5-5\n"},
    )
    live = tmp_path / "LANE-live.md"
    live.write_text("grok-4.7 is named here\n", encoding="utf-8")
    report = cmc.analyse(root, contracts=[live], today=_TODAY)
    by_source = {(p.source, p.model_id) for p in report.pins}
    assert ("registry", "claude-sonnet-5-5") in by_source
    assert ("template", "claude-sonnet-5-5") in by_source
    assert ("contract", "claude-sonnet-5-5") in by_source      # the tracked LANE-*.md
    assert ("contract", "grok-4.7") in by_source                # the live one, by path
    template_pin = next(p for p in report.pins if p.source == "template")
    assert template_pin.where.endswith("templates/t.md:2")
    cmc.main(["--root", str(root), "--contracts", str(live), "--today", _TODAY.isoformat()])
    out = capsys.readouterr().out
    assert "claude-sonnet-5-5" in out and "grok-4.7" in out
    assert out.isascii()


def test_bare_aliases_are_reported_as_aliases_not_unknown_ids(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)})
    live = tmp_path / "LANE-live.md"
    live.write_text("claude --bg --model sonnet --effort high\n| opus | execute | high |\n"
                    "model: haiku\n", encoding="utf-8")
    report = cmc.analyse(root, contracts=[live], today=_TODAY)
    assert {p.model_id for p in report.pins if p.kind == "alias"} == {"sonnet", "opus", "haiku"}
    assert report.flags == []


def test_globs_and_date_like_tokens_are_not_pinned_ids(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)})
    live = tmp_path / "LANE-live.md"
    live.write_text("see gpt-6-* and DIGEST-grok-2026-10-03.md and grok-4.7.\n", encoding="utf-8")
    report = cmc.analyse(root, contracts=[live], today=_TODAY)
    assert _kinds(report) == {("unknown-id", "grok-4.7")}


def test_a_dated_suffix_and_an_effort_suffix_resolve_to_the_registered_id(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-haiku-4-5-20251001": (_days_ago(1), True),
                                 "gemini-3.8-flash": (_days_ago(1), True)})
    live = tmp_path / "LANE-live.md"
    live.write_text("claude-haiku-4-5 and gemini-3.8-flash-high and gemini-3.8-flash-low\n",
                    encoding="utf-8")
    assert cmc.analyse(root, contracts=[live], today=_TODAY).flags == []


def test_a_role_or_dispatcher_pin_the_registry_lacks_is_flagged_unknown(cmc, tmp_path: Path,
                                                                          monkeypatch) -> None:
    """Codex terra P1 (review of this lane): role-order and dispatcher pins were excluded from
    the unknown-id leg with the model keys. The loader's schema normally refuses such a pin, so
    the leg is defence in depth -- shown here with the loader answering a registry whose role
    pin names a model that has no row."""
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)})
    data = {
        "providers": {}, "models": {"claude-sonnet-5-5": {
            "last_verified": _days_ago(1), "evidence": ["docs/audits/claude-sonnet-5-5.md"]}},
        "roles": {"implement": {"order": [{"provider": "xai", "model": "grok-9.0"}]}},
        "dispatcher": {"model": "claude-opus-9-9"},
    }
    monkeypatch.setattr(cmc._preg, "load_registry", lambda path=None: data)
    assert _kinds(cmc.analyse(root, today=_TODAY)) == {
        ("unknown-id", "grok-9.0"), ("unknown-id", "claude-opus-9-9")}


def test_a_live_contract_path_that_does_not_exist_is_an_error_not_a_pass(cmc, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (_days_ago(1), True)})
    missing = tmp_path / "LANE-gone.md"
    assert cmc.main(["--root", str(root), "--contracts", str(missing),
                     "--today", _TODAY.isoformat()]) == 2


def test_an_unreadable_registry_is_an_error(cmc, tmp_path: Path) -> None:
    assert cmc.main(["--root", str(tmp_path), "--today", _TODAY.isoformat()]) == 2


def test_the_live_registry_does_not_flag_the_ids_served_today(cmc) -> None:
    report = cmc.analyse(_REPO_ROOT, today=_SERVED_DAY + datetime.timedelta(days=1))
    flagged = {f.model_id for f in report.flags}
    assert not (flagged & set(_SERVED_TODAY)), flagged & set(_SERVED_TODAY)


# --- the health finding: WARN tier, informs, never blocks ------------------------------------

@pytest.fixture()
def adapter():
    from audit_checks import model_currency as module

    return module


def test_the_finding_warns_on_an_unknown_id(adapter, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (datetime.date.today(), True)},
                      templates={"templates/t.md": "pin claude-opus-9-9 here\n"})
    findings = adapter.check_model_currency(root)
    assert len(findings) == 1
    assert findings[0].check_name == "model_currency"
    assert findings[0].status == "warn"
    assert "claude-opus-9-9" in findings[0].evidence
    assert "|" not in findings[0].evidence


def test_the_finding_passes_on_a_clean_fixture(adapter, tmp_path: Path) -> None:
    root = _make_root(tmp_path, {"claude-sonnet-5-5": (datetime.date.today(), True)})
    assert [f.status for f in adapter.check_model_currency(root)] == ["pass"]


def test_the_finding_is_not_applicable_where_there_is_no_registry(adapter, tmp_path: Path) -> None:
    assert [f.status for f in adapter.check_model_currency(tmp_path)] == ["n/a"]


def test_an_unreadable_registry_warns_and_never_fails(adapter, tmp_path: Path) -> None:
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "provider-registry.yaml").write_text("not: [valid", encoding="utf-8")
    assert [f.status for f in adapter.check_model_currency(tmp_path)] == ["warn"]


def test_the_check_is_registered_in_all_checks_at_the_commit_tier() -> None:
    import audit as aud

    names = [c.__name__ for c in aud.ALL_CHECKS]
    assert "check_model_currency" in names
    check = aud.ALL_CHECKS[names.index("check_model_currency")]
    assert aud.tier_of(check) == aud.TIER_COMMIT            # shows in `audit.py health`


def test_the_live_finding_is_never_a_fail() -> None:
    import audit as aud

    findings = aud.check_model_currency(_REPO_ROOT)
    assert [f.status for f in findings] != ["fail"]
    assert all(f.status in {"pass", "warn"} for f in findings)


def test_no_blocking_hook_names_the_check() -> None:
    """AMEND-5: a health finding, not a hook -- the pre-commit config does not carry it."""
    config = (_REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "check_model_currency" not in config and "model_currency" not in config
