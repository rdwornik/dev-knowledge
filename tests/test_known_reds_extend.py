"""RED-first tests for dated, ratified known-reds expiry extensions."""
from __future__ import annotations

import copy
import datetime as dt
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_TODAY = dt.date(2026, 10, 24)
_OLD_EXPIRY = "2026-10-31"
_NEW_EXPIRY = "2026-11-09"
_RATIFICATION_ID = "R-1"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def kr():
    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    return _load("known_reds_extend_under_test", _REPO / "scripts" / "known_reds.py")


def _entry(expiry: str = _OLD_EXPIRY) -> dict:
    return {"attribution": "pre-freeze", "task": "[#1]", "owner": "rob", "expiry": expiry}


def _registry(kr, *, members=None, hooks=None, members_by_os=None):
    return kr.Registry(
        schema="known-reds-registry/2",
        baseline_id="synthetic",
        measured_at_sha="synthetic",
        measured_via="test",
        workers=1,
        members=members or {},
        hooks=hooks or {},
        members_by_os=members_by_os or {},
    )


def _write_registry(tmp_path: Path, kr, registry=None, **buckets) -> tuple[Path, object]:
    registry = registry or _registry(kr, **buckets)
    path = tmp_path / "registry.json"
    kr.write_registry(path, registry)
    return path, kr.load_registry(path, today=_TODAY)


def _ratification_file(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "ratification.md"
    path.write_text(content, encoding="utf-8")
    return path


def _extend_args(
    root: Path,
    ratification_file: Path,
    *,
    ids: tuple[str, ...] = ("members[node-a]",),
    new_expiry: str = _NEW_EXPIRY,
    ratification_id: str = _RATIFICATION_ID,
    write: bool = False,
    all_expiring_on: str | None = None,
) -> list[str]:
    args = [
        "--repo-root",
        str(root),
        "extend",
        "--registry",
        "registry.json",
    ]
    if all_expiring_on is not None:
        args.extend(["--all-expiring-on", all_expiring_on])
    else:
        args.extend(["--ids", *ids])
    args.extend([
        "--new-expiry",
        new_expiry,
        "--ratification-file",
        str(ratification_file),
        "--ratification-id",
        ratification_id,
        "--today",
        _TODAY.isoformat(),
    ])
    if write:
        args.append("--write")
    return args


@pytest.mark.parametrize(
    ("ratification_exists", "row", "ratification_id"),
    [
        (True, "| R-OTHER | approved through 2026-11-09 |", _RATIFICATION_ID),
        (False, "", _RATIFICATION_ID),
        (True, "| R-1 | approved without a date |", _RATIFICATION_ID),
    ],
    ids=["missing-row", "missing-file", "row-with-no-date"],
)
def test_extend_refuses_unratified_or_undated_rows_without_writing(
    kr, tmp_path, capsys, ratification_exists, row, ratification_id
):
    registry_path, registry = _write_registry(
        tmp_path, kr, members={"node-a": _entry()}
    )
    original_bytes = registry_path.read_bytes()
    ratification_file = tmp_path / "missing.md"
    if ratification_exists:
        ratification_file = _ratification_file(tmp_path, row)

    with pytest.raises(kr.ExtendRefused):
        kr.extend(
            registry,
            ids=("members[node-a]",),
            new_expiry=dt.date(2026, 11, 9),
            ratification_file=ratification_file,
            ratification_id=ratification_id,
            today=_TODAY,
        )

    assert kr.main(_extend_args(tmp_path, ratification_file)) == 5
    capsys.readouterr()
    assert registry_path.read_bytes() == original_bytes


@pytest.mark.parametrize(
    ("new_expiry", "row"),
    [
        ("2026-10-31", "| R-1 | approved through 2026-11-09 |"),
        ("2026-10-30", "| R-1 | approved through 2026-11-09 |"),
        ("2026-11-08", "| R-1 | cap=2026-11-07, approved 2026-11-09 |"),
        ("2026-11-11", "| R-1 | approved through 2026-11-10 |"),
    ],
    ids=["equal-current-expiry", "earlier-than-current", "past-explicit-cap", "past-default-cap"],
)
def test_extend_refuses_nonincreasing_or_over_cap_expiries(kr, tmp_path, new_expiry, row):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(tmp_path, row)

    with pytest.raises(kr.ExtendRefused):
        kr.extend(
            registry,
            ids=("members[node-a]",),
            new_expiry=dt.date.fromisoformat(new_expiry),
            ratification_file=ratification_file,
            ratification_id=_RATIFICATION_ID,
            today=_TODAY,
        )


@pytest.mark.parametrize(
    ("row", "expected_cap"),
    [
        ("| R-1 | cap=2026-11-09 | approved through 2026-11-12 |", "2026-11-09"),
        ("| R-1 | approved 2026-11-02 until 2026-11-09 |", "2026-11-09"),
    ],
    ids=["explicit-cap", "latest-date-default-cap"],
)
def test_extend_accepts_new_expiry_equal_to_ratified_cap(kr, tmp_path, row, expected_cap):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(tmp_path, row)

    result, changes = kr.extend(
        registry,
        ids=("members[node-a]",),
        new_expiry=dt.date.fromisoformat(expected_cap),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )

    assert result.members["node-a"]["expiry"] == expected_cap
    assert changes == [{
        "label": "members[node-a]",
        "old_expiry": _OLD_EXPIRY,
        "new_expiry": expected_cap,
    }]


def test_extend_touches_only_the_named_bucket_label(kr, tmp_path):
    _, registry = _write_registry(
        tmp_path,
        kr,
        members={"node-a": _entry(), "node-b": _entry()},
        hooks={"hook-a": _entry()},
        members_by_os={"windows": {"node-a": _entry()}},
    )
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    result, _ = kr.extend(
        registry,
        ids=("members[node-a]",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )

    assert result.members["node-a"]["expiry"] == _NEW_EXPIRY
    assert result.members["node-b"] == registry.members["node-b"]
    assert result.hooks == registry.hooks
    assert result.members_by_os == registry.members_by_os


def test_extend_refuses_an_id_not_present_in_any_bucket(kr, tmp_path):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    with pytest.raises(kr.ExtendRefused):
        kr.extend(
            registry,
            ids=("members[missing]",),
            new_expiry=dt.date(2026, 11, 9),
            ratification_file=ratification_file,
            ratification_id=_RATIFICATION_ID,
            today=_TODAY,
        )


def test_extend_bare_id_expands_to_every_bucket_that_holds_it(kr, tmp_path):
    _, registry = _write_registry(
        tmp_path,
        kr,
        members={"shared": _entry()},
        hooks={"shared": _entry()},
        members_by_os={"windows": {"shared": _entry()}},
    )
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    result, changes = kr.extend(
        registry,
        ids=("shared",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )

    assert result.members["shared"]["expiry"] == _NEW_EXPIRY
    assert result.hooks["shared"]["expiry"] == _NEW_EXPIRY
    assert result.members_by_os["windows"]["shared"]["expiry"] == _NEW_EXPIRY
    assert {change["label"] for change in changes} == {
        "members[shared]",
        "hooks[shared]",
        "members_by_os[windows][shared]",
    }


def test_extend_adds_exact_record_without_mutating_the_input(kr, tmp_path):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    before = copy.deepcopy(registry.to_json())
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    result, _ = kr.extend(
        registry,
        ids=("members[node-a]",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )

    assert registry.to_json() == before
    assert result is not registry
    assert result.members["node-a"]["extended"] == {
        "ratification_file": ratification_file.name,
        "ratification_id": _RATIFICATION_ID,
        "old_expiry": _OLD_EXPIRY,
        "new_expiry": _NEW_EXPIRY,
        "date": _TODAY.isoformat(),
    }
    assert set(result.members["node-a"]["extended"]) == {
        "ratification_file",
        "ratification_id",
        "old_expiry",
        "new_expiry",
        "date",
    }
    assert {
        key: value for key, value in result.members["node-a"].items() if key != "extended"
    } == before["members"]["node-a"]


def test_extend_cli_defaults_to_dry_run_and_write_persists_the_diff(kr, tmp_path, capsys):
    registry_path, _ = _write_registry(
        tmp_path,
        kr,
        members={"node-a": _entry(), "node-b": _entry()},
    )
    original_bytes = registry_path.read_bytes()
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    assert kr.main(_extend_args(tmp_path, ratification_file)) == 0
    dry_run_output = capsys.readouterr().out

    assert registry_path.read_bytes() == original_bytes
    assert "--- " in dry_run_output and "+++ " in dry_run_output
    assert any(line.startswith("-") and '"expiry": "2026-10-31"' in line
               for line in dry_run_output.splitlines())
    assert any(line.startswith("+") and '"expiry": "2026-11-09"' in line
               for line in dry_run_output.splitlines())
    assert any(line.startswith("+") and '"extended": {' in line
               for line in dry_run_output.splitlines())

    assert kr.main(_extend_args(tmp_path, ratification_file, write=True)) == 0
    capsys.readouterr()
    written = kr.load_registry(registry_path, today=_TODAY)
    assert written.members["node-a"]["expiry"] == _NEW_EXPIRY
    assert written.members["node-b"]["expiry"] == _OLD_EXPIRY


def test_extend_cli_all_expiring_on_selects_every_matching_entry(kr, tmp_path, capsys):
    registry_path, _ = _write_registry(
        tmp_path,
        kr,
        members={
            "node-a": _entry(),
            "node-b": _entry(),
            "node-c": _entry("2026-11-05"),
        },
    )
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    assert kr.main(_extend_args(
        tmp_path,
        ratification_file,
        all_expiring_on=_OLD_EXPIRY,
        write=True,
    )) == 0
    written = kr.load_registry(registry_path, today=_TODAY)
    capsys.readouterr()

    assert written.members["node-a"]["expiry"] == _NEW_EXPIRY
    assert written.members["node-b"]["expiry"] == _NEW_EXPIRY
    assert written.members["node-c"]["expiry"] == "2026-11-05"


def test_extended_result_passes_registry_problems_and_tampering_is_reported(kr, tmp_path):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )
    result, _ = kr.extend(
        registry,
        ids=("members[node-a]",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )
    assert kr.registry_problems(result, _TODAY) == []

    result.members["node-a"]["extended"]["new_expiry"] = "2026-11-10"
    problems = kr.registry_problems(result, _TODAY)
    assert problems
    assert any("extended" in problem for problem in problems)


def test_extend_and_cli_do_not_call_refresh_or_subprocess(kr, tmp_path, monkeypatch, capsys):
    _, registry = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("expiry extension must not invoke refresh or a subprocess")

    monkeypatch.setattr(kr, "refresh", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)

    kr.extend(
        registry,
        ids=("members[node-a]",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )
    assert kr.main(_extend_args(tmp_path, ratification_file)) == 0
    capsys.readouterr()


def test_unrecorded_expiry_moves_distinguishes_bare_and_code_applied_changes(kr, tmp_path):
    _, base = _write_registry(tmp_path, kr, members={"node-a": _entry()})
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )

    bare_edit = _registry(
        kr,
        members={"node-a": {**base.members["node-a"], "expiry": _NEW_EXPIRY}},
    )
    assert kr.unrecorded_expiry_moves(base, bare_edit)

    extended, _ = kr.extend(
        base,
        ids=("members[node-a]",),
        new_expiry=dt.date(2026, 11, 9),
        ratification_file=ratification_file,
        ratification_id=_RATIFICATION_ID,
        today=_TODAY,
    )
    assert kr.unrecorded_expiry_moves(base, extended) == []

    extended.members["node-a"]["extended"]["new_expiry"] = "2026-11-10"
    assert kr.unrecorded_expiry_moves(base, extended)


def test_real_registry_shape_dry_run_and_write_only_change_expiry_records(
    kr, tmp_path, capsys
):
    source = _REPO / "logs" / "KNOWN-REDS-REGISTRY.json"
    if not source.is_file():
        pytest.skip("real known-reds registry is absent")

    registry_path = tmp_path / "registry.json"
    shutil.copyfile(source, registry_path)
    original_bytes = registry_path.read_bytes()
    before = json.loads(original_bytes)
    ratification_file = _ratification_file(
        tmp_path, "| R-1 | approved through 2026-11-09 |"
    )
    args = _extend_args(
        tmp_path,
        ratification_file,
        all_expiring_on=_OLD_EXPIRY,
    )

    assert kr.main(args) == 0
    dry_run_output = capsys.readouterr().out
    assert registry_path.read_bytes() == original_bytes
    assert "--- " in dry_run_output and "+++ " in dry_run_output
    allowed_keys = {
        "expiry",
        "extended",
        "ratification_file",
        "ratification_id",
        "old_expiry",
        "new_expiry",
        "date",
    }
    changed_lines = [
        line[1:].strip()
        for line in dry_run_output.splitlines()
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    ]
    assert changed_lines
    assert all(
        any(f'"{key}"' in line for key in allowed_keys)
        for line in changed_lines
    )
    original_matching = sum(
        1
        for bucket in ("members", "hooks")
        for entry in before.get(bucket, {}).values()
        if entry.get("expiry") == _OLD_EXPIRY
    ) + sum(
        1
        for entries in before.get("members_by_os", {}).values()
        for entry in entries.values()
        if entry.get("expiry") == _OLD_EXPIRY
    )
    assert original_matching > 0

    assert kr.main([*args, "--write"]) == 0
    capsys.readouterr()
    written = kr.load_registry(registry_path, today=_TODAY)
    assert kr.registry_problems(written, _TODAY) == []
    for bucket in ("members", "hooks"):
        for label, entry in before.get(bucket, {}).items():
            if entry.get("expiry") == _OLD_EXPIRY:
                assert getattr(written, bucket)[label]["expiry"] == _NEW_EXPIRY
    for os_key, entries in before.get("members_by_os", {}).items():
        for label, entry in entries.items():
            if entry.get("expiry") == _OLD_EXPIRY:
                assert written.members_by_os[os_key][label]["expiry"] == _NEW_EXPIRY
