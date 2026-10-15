"""lane-bu-1535-outer-loop: `conductor.py lane` -- constraint selection, the five baseline checkers, one round.

RED-FIRST ([#1535] Done-when (2), (4), ADR-108 section B): authored and witnessed FAILING before
`select_constraints`, `check_constraint`, `run_round`, `LaneContext`, `BASELINE`,
`ConstraintSelectionError` and the `lane` subcommand exist in `scripts/conductor.py`. `conductor`
itself exists on base, but every NEW attribute is reached inside a test or helper, so each test
fails on its own rather than the file failing at collection.

Each C-* checker is driven against a seeded tmp git repo (a base commit tagged `base`, then the
seed commits) and a matching clean twin: a checker that cannot tell the two apart is decorative.
Receipts are written as plain dicts in the PhaseReceipt shape; `test_the_seed_receipts_...` pins
that the dicts are VALID receipts, so a checker is never tested against an invalid fixture.
`run_round` tests drive a real `doit` through a toy harness (see `tests/test_dodo_phases.py` for the
toy idiom) under a unique lane per test.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import textwrap
import uuid
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_CONDUCTOR = _REPO / "scripts" / "conductor.py"
for _p in (str(_REPO), str(_REPO / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_BASELINE = ("C-TASK", "C-SCOPE", "C-RED", "C-VENDOR", "C-CLEAN")
_NOW = "2026-10-15T00:00:00+00:00"
_HEX = "ab" * 32

_TOY = textwrap.dedent("""\
    import json, os, sys
    from pathlib import Path
    pid, mdir = sys.argv[1], Path(sys.argv[2])
    with open(mdir / "count.txt", "a") as fh:
        fh.write(pid + "\\n")
    (mdir / f"started-{pid}").write_text("x")
    target = os.environ.get("PHASE_PAYLOAD")
    if target:
        out = mdir / f"outcome-{pid}"
        Path(target).write_text(json.dumps({
            "nonce": os.environ["PHASE_NONCE"], "input_hash": os.environ["PHASE_INPUT_HASH"],
            "outcome": out.read_text().strip() if out.exists() else "ACCEPT"}))
    code = mdir / f"exit-{pid}"
    sys.exit(int(code.read_text()) if code.exists() else 0)
    """)


# --- helpers ------------------------------------------------------------------------------------

def _conductor():
    from scripts import conductor  # noqa: PLC0415 -- new attributes are reached through this, per test

    return conductor


def _doc(*ids: str, extra: list[dict] | None = None) -> dict:
    rows = [{"id": cid, "kind": "deterministic", "checker": ["true"], "applies_when": {"always": True},
             "reuses": "x"} for cid in ids]
    return {"constraints": rows + (extra or [])}


def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(["git", "-c", "user.name=toy", "-c", "user.email=toy@example.com",
                          "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", "-C", str(repo), *args],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, f"git {args}: {out.stdout}{out.stderr}"
    return out.stdout


def _commit(repo: Path, files: dict[str, str], msg: str = "c") -> None:
    for rel, text in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)


def _new_repo(tmp: Path, name: str) -> Path:
    repo = tmp / name
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, {"README.md": "base\n"}, "base")
    _git(repo, "tag", "base")
    return repo


def _ctx(repo: Path, round_dir: Path, row: str = ""):
    return _conductor().LaneContext(repo_root=repo, base="base", round_dir=round_dir, row=row)


def _payload_dict(**kw) -> dict:
    base = {"nonce": "n" * 16, "input_hash": _HEX, "outcome": "PASS", "findings": [], "detail": "",
            "files_in_scope": [], "red_test_ids": [], "constraints_add": []}
    base.update(kw)
    return base


def _write_receipt(round_dir: Path, phase: str, head: str, vendor: str, *, payload: dict | None = None,
                   substituted_from: str | None = None, status: str = "ok") -> None:
    round_dir.mkdir(parents=True, exist_ok=True)
    sha = (hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
           if payload is not None else None)
    data = {"schema": "phase-receipt/1", "organ": f"phase:{phase}", "status": status, "exit_code": 0,
            "duration_ms": 1, "input_hash": _HEX, "model_requested": None, "model_reported": None,
            "command": [head, "-p", "x"], "finished_at": _NOW, "row": "toy-row", "lane": "toy", "phase": phase,
            "round": 1, "vendor": vendor, "cli_version": None, "served_model": None, "started_at": _NOW,
            "inputs": [], "nonce": "n" * 16, "usage": None, "payload_sha256": sha, "payload": payload,
            "substituted_from": substituted_from}
    (round_dir / f"{phase}.json").write_text(json.dumps(data), encoding="utf-8")


def _vendors(round_dir: Path, *, p3="claude", p6a="codex", p6b="grok", p7="copilot", p3_sub: str | None = None) -> None:
    heads = {"claude": "anthropic", "codex": "openai", "grok": "xai", "copilot": "copilot-enterprise",
             "python": "local"}
    for phase, head, sub in (("P3", p3, p3_sub), ("P6a", p6a, None), ("P6b", p6b, None), ("P7", p7, None)):
        _write_receipt(round_dir, phase, head, heads[head], substituted_from=sub)


# --- Done-when (4): the registry is selected, never assumed -------------------------------------

def test_the_baseline_is_the_five_mandatory_constraints():
    assert tuple(_conductor().BASELINE) == _BASELINE


def test_selecting_from_a_harness_with_no_constraints_raises():
    c = _conductor()
    with pytest.raises(c.ConstraintSelectionError):
        c.select_constraints({})
    with pytest.raises(c.ConstraintSelectionError):
        c.select_constraints({"constraints": []})


def test_selecting_from_a_registry_missing_a_baseline_id_raises():
    c = _conductor()
    with pytest.raises(c.ConstraintSelectionError):
        c.select_constraints(_doc(*_BASELINE[:-1]))


def test_selecting_from_the_real_harness_returns_the_five_baseline_rows():
    doc = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))
    assert set(_BASELINE) <= {row["id"] for row in _conductor().select_constraints(doc)}


def test_a_conditional_constraint_is_selected_by_change_kind_or_by_path():
    c = _conductor()
    extra = {"id": "C-EXTRA", "kind": "deterministic", "checker": ["true"], "reuses": "x",
             "applies_when": {"change_kind": ["WIRE"], "paths": ["scripts/*.py"]}}
    doc = _doc(*_BASELINE, extra=[extra])

    def ids(**kw):
        return {r["id"] for r in c.select_constraints(doc, **kw)}

    assert "C-EXTRA" in ids(change_kind="WIRE")
    assert "C-EXTRA" in ids(paths=["scripts/x.py"])
    assert "C-EXTRA" not in ids(change_kind="DOCS", paths=["docs/x.md"])
    assert set(_BASELINE) <= ids(change_kind="DOCS")


def test_lane_select_exits_one_on_a_harness_with_no_constraints(tmp_path):
    empty = tmp_path / "empty.yaml"
    empty.write_text(yaml.safe_dump({"stages": [], "moments": []}), encoding="utf-8")
    out = subprocess.run([sys.executable, str(_CONDUCTOR), "lane", "--select", "--harness", str(empty)],
                         capture_output=True, text=True, cwd=_REPO, timeout=120)
    assert out.returncode == 1, out.stdout + out.stderr


def test_lane_select_prints_the_baseline_ids_for_the_real_harness():
    out = subprocess.run([sys.executable, str(_CONDUCTOR), "lane", "--select", "--harness", str(_HARNESS)],
                         capture_output=True, text=True, cwd=_REPO, timeout=120)
    assert out.returncode == 0, out.stdout + out.stderr
    for cid in _BASELINE:
        assert cid in out.stdout, cid


def test_an_unknown_constraint_id_fails_and_says_so(tmp_path):
    ok, why = _conductor().check_constraint("C-NOPE", _ctx(_new_repo(tmp_path, "r"), tmp_path / "rd"))
    assert ok is False and "unknown" in why.lower()


# --- the seed receipts are valid receipts (the fixtures are not the thing under test) ------------

def test_the_seed_receipts_are_valid_phase_receipts(tmp_path):
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    rd = tmp_path / "rd"
    _vendors(rd)
    _write_receipt(rd, "P1", "claude", "anthropic", payload=_payload_dict(files_in_scope=["src/"]))
    for phase in ("P1", "P3", "P6a", "P6b", "P7"):
        PhaseReceipt.model_validate(json.loads((rd / f"{phase}.json").read_text(encoding="utf-8")))


# --- Done-when (4): each C-* checker, on a seed and on a clean twin -----------------------------

_VALID_BACKLOG = textwrap.dedent("""\
    # Backlog

    ## Big picture

    A toy.

    ## Theme A

    ### [S1] Toy story
    So that the toy validates.

    - [#1] Do the thing [P2][S] · Done when: `x` passes. · phase: {phase}
    """)


def test_c_task_refuses_an_unknown_phase_clause_and_passes_a_valid_backlog(tmp_path):
    c = _conductor()
    seed, twin, bare = (tmp_path / n for n in ("seed", "twin", "bare"))
    for path in (seed, twin, bare):
        path.mkdir()
    (seed / "BACKLOG.md").write_text(_VALID_BACKLOG.format(phase="bogus"), encoding="utf-8")
    (twin / "BACKLOG.md").write_text(_VALID_BACKLOG.format(phase="task"), encoding="utf-8")
    bad, why = c.check_constraint("C-TASK", _ctx(seed, tmp_path / "rd"))
    assert bad is False and why
    assert c.check_constraint("C-TASK", _ctx(twin, tmp_path / "rd"))[0] is True
    assert c.check_constraint("C-TASK", _ctx(bare, tmp_path / "rd"))[0] is False, "no backlog source fails"


def test_c_scope_refuses_a_changed_path_outside_the_p1_scope_and_passes_inside_it(tmp_path):
    c = _conductor()
    repo = _new_repo(tmp_path, "scope")
    _commit(repo, {"src/a.py": "x = 1\n", "docs/x.md": "d\n"}, "work")
    seed, twin, empty = (tmp_path / n for n in ("seed", "twin", "empty"))
    _write_receipt(seed, "P1", "claude", "anthropic", payload=_payload_dict(files_in_scope=["src/"]))
    _write_receipt(twin, "P1", "claude", "anthropic", payload=_payload_dict(files_in_scope=["src/", "docs/x.md"]))
    _write_receipt(empty, "P1", "claude", "anthropic", payload=_payload_dict(files_in_scope=[]))
    bad, why = c.check_constraint("C-SCOPE", _ctx(repo, seed))
    assert bad is False and "docs/x.md" in why
    assert c.check_constraint("C-SCOPE", _ctx(repo, twin))[0] is True
    assert c.check_constraint("C-SCOPE", _ctx(repo, empty))[0] is False, "an empty allowed set fails closed"


def test_c_red_refuses_code_before_tests_and_a_missing_p2_receipt_and_passes_tests_first(tmp_path):
    c = _conductor()
    seed, twin = _new_repo(tmp_path, "red-seed"), _new_repo(tmp_path, "red-twin")
    _commit(seed, {"src/a.py": "x = 1\n"}, "code first")
    _commit(seed, {"tests/test_a.py": "def test_a(): pass\n"}, "tests second")
    _commit(twin, {"tests/test_a.py": "def test_a(): pass\n"}, "tests first")
    _commit(twin, {"src/a.py": "x = 1\n"}, "code second")
    rd, no_p2 = tmp_path / "rd", tmp_path / "no-p2"
    _write_receipt(rd, "P2", "codex", "openai")
    no_p2.mkdir()
    bad, why = c.check_constraint("C-RED", _ctx(seed, rd))
    assert bad is False and why
    assert c.check_constraint("C-RED", _ctx(twin, rd))[0] is True
    assert c.check_constraint("C-RED", _ctx(twin, no_p2))[0] is False, "no P2 receipt fails closed"


def test_c_vendor_refuses_a_reviewer_or_judge_of_the_producers_vendor_and_a_missing_receipt(tmp_path):
    c = _conductor()
    repo = _new_repo(tmp_path, "vendor")
    twin, same_reviewer, same_judge, substituted, partial = (
        tmp_path / n for n in ("twin", "same-reviewer", "same-judge", "substituted", "partial"))
    _vendors(twin)
    _vendors(same_reviewer, p6a="claude")
    _vendors(same_judge, p7="claude")
    _vendors(substituted, p7="claude", p3_sub="openai")
    _vendors(partial)
    (partial / "P7.json").unlink()
    assert c.check_constraint("C-VENDOR", _ctx(repo, twin))[0] is True
    assert c.check_constraint("C-VENDOR", _ctx(repo, same_reviewer))[0] is False
    assert c.check_constraint("C-VENDOR", _ctx(repo, same_judge))[0] is False
    assert c.check_constraint("C-VENDOR", _ctx(repo, substituted))[0] is True, \
        "a substituted anthropic producer may be judged by anthropic (common rules (j))"
    assert c.check_constraint("C-VENDOR", _ctx(repo, partial))[0] is False, "a missing receipt fails closed"


def test_c_clean_refuses_a_changed_python_file_ruff_rejects_and_passes_a_clean_one(tmp_path):
    c = _conductor()
    seed, twin, docs = (_new_repo(tmp_path, n) for n in ("clean-seed", "clean-twin", "clean-docs"))
    _commit(seed, {"bad.py": "import os\n"}, "unused import")
    _commit(twin, {"good.py": "VALUE = 1\n"}, "clean module")
    _commit(docs, {"notes.md": "prose\n"}, "docs only")
    bad, why = c.check_constraint("C-CLEAN", _ctx(seed, tmp_path / "rd"))
    assert bad is False and why
    assert c.check_constraint("C-CLEAN", _ctx(twin, tmp_path / "rd"))[0] is True
    assert c.check_constraint("C-CLEAN", _ctx(docs, tmp_path / "rd"))[0] is True, "no .py changed passes"


# --- Done-when (2): one round, driven through a toy harness --------------------------------------

def _toy_round_harness(tmp: Path) -> tuple[Path, Path]:
    toy, markers = tmp / "toy.py", tmp / "markers"
    markers.mkdir()
    toy.write_text(_TOY, encoding="utf-8")
    rows = []
    for pid in ("P1", "P2", "P3", "P7"):
        rows.append({"id": pid, "name": pid.lower(), "row_phase": "build", "role": "toy", "cli": "python",
                     "model": None, "payload_model": "PhasePayload",
                     "gate": "payload" if pid == "P7" else "exit", "timeout_s": 60, "budget_usd": 0,
                     "max_rounds": 2, "inputs": [], "command": [sys.executable, str(toy), pid, str(markers)]})
    harness = tmp / "harness.yaml"
    harness.write_text(yaml.safe_dump({"stages": [], "moments": [], "phases": rows}, sort_keys=False),
                       encoding="utf-8")
    return harness, markers


def _round(tmp: Path, markers: Path, round_no: int = 1):
    harness, lane = tmp / "harness.yaml", "toy" + uuid.uuid4().hex[:10]
    result = _conductor().run_round(lane, round_no, repo_root=_REPO, harness=harness,
                                    receipts=tmp / "receipts", row="toy-row")
    return result, tmp / "receipts" / f"LANE-{lane}" / f"r{round_no}"


@pytest.mark.parametrize("round_no", [0, 3])
def test_a_round_outside_one_to_max_rounds_is_refused_and_runs_nothing(tmp_path, round_no):
    _harness, markers = _toy_round_harness(tmp_path)
    result, _dir = _round(tmp_path, markers, round_no)
    assert (result.verdict, result.exit_code) == ("REFUSED", 2)
    assert not (markers / "count.txt").exists(), "a refused round must not start a phase"


def test_a_round_whose_judge_accepts_exits_zero(tmp_path):
    _harness, markers = _toy_round_harness(tmp_path)
    result, _dir = _round(tmp_path, markers)
    assert (result.verdict, result.exit_code) == ("ACCEPT", 0)


def test_a_refusing_judge_is_refuse_exit_three_at_round_one_and_failed_exit_one_at_round_two(tmp_path):
    _harness, markers = _toy_round_harness(tmp_path)
    (markers / "outcome-P7").write_text("REFUSE")
    first, _dir = _round(tmp_path, markers, 1)
    assert (first.verdict, first.exit_code) == ("REFUSE", 3)
    second, _dir = _round(tmp_path, markers, 2)
    assert (second.verdict, second.exit_code) == ("FAILED", 1)


def test_a_failing_phase_halts_the_round_at_that_phase_and_leaves_no_later_receipt(tmp_path):
    _harness, markers = _toy_round_harness(tmp_path)
    (markers / "exit-P2").write_text("1")
    result, round_dir = _round(tmp_path, markers)
    assert (result.verdict, result.halted_at, result.exit_code) == ("HALTED", "P2", 1)
    assert not (round_dir / "P3.json").exists()
    assert not (markers / "started-P3").exists()


def test_a_payload_asking_for_input_is_input_required_exit_four(tmp_path):
    _harness, markers = _toy_round_harness(tmp_path)
    (markers / "outcome-P7").write_text("INPUT_REQUIRED")
    result, _dir = _round(tmp_path, markers)
    assert (result.verdict, result.exit_code) == ("INPUT_REQUIRED", 4)
