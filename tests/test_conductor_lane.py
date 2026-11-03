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
import os
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
                   substituted_from: str | None = None, status: str = "ok",
                   model_requested: str | None = None) -> None:
    round_dir.mkdir(parents=True, exist_ok=True)
    sha = (hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
           if payload is not None else None)
    data = {"schema": "phase-receipt/1", "organ": f"phase:{phase}", "status": status, "exit_code": 0,
            "duration_ms": 1, "input_hash": _HEX, "model_requested": model_requested, "model_reported": None,
            "command": [head, "-p", "x"], "finished_at": _NOW, "row": "toy-row", "lane": "toy", "phase": phase,
            "round": 1, "vendor": vendor, "cli_version": None, "served_model": None, "started_at": _NOW,
            "inputs": [], "nonce": "n" * 16, "usage": None, "payload_sha256": sha, "payload": payload,
            "substituted_from": substituted_from}
    (round_dir / f"{phase}.json").write_text(json.dumps(data), encoding="utf-8")


def _vendors(round_dir: Path, *, p3="copilot", p6a="codex", p6b="copilot", p7="codex",
             p3_model="claude-sonnet-5.5", p6a_model="gpt-5.6-terra",
             p6b_model="gemini-4-argon", p7_model="gpt-6-sol",
             p3_sub: str | None = None) -> None:
    heads = {"claude": "anthropic", "codex": "openai", "grok": "xai", "copilot": "copilot-enterprise",
             "python": "local"}
    for phase, head, model, sub in (
        ("P3", p3, p3_model, p3_sub),
        ("P6a", p6a, p6a_model, None),
        ("P6b", p6b, p6b_model, None),
        ("P7", p7, p7_model, None),
    ):
        _write_receipt(round_dir, phase, head, heads[head], substituted_from=sub, model_requested=model)


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


def test_c_vendor_at_p4_needs_only_a_readable_p3_receipt_and_family_independence_is_checked_after_p7(tmp_path):
    c = _conductor()
    repo = _new_repo(tmp_path, "vendor")
    p3_only, full, missing_p3 = (tmp_path / n for n in ("p3-only", "full", "missing-p3"))
    _write_receipt(p3_only, "P3", "copilot", "copilot-enterprise", model_requested="claude-sonnet-5.5")
    _vendors(full)
    _vendors(missing_p3)
    (missing_p3 / "P3.json").unlink()
    assert c.check_constraint("C-VENDOR", _ctx(repo, p3_only))[0] is True
    assert c.check_constraint("C-VENDOR", _ctx(repo, full))[0] is True
    bad, why = c.check_constraint("C-VENDOR", _ctx(repo, missing_p3))
    assert bad is False and "P3" in why, "a missing P3 receipt fails closed"

    independent = tmp_path / "independent"
    _vendors(independent)
    ok, why, phase = c.check_independence(_ctx(repo, independent))
    assert (ok, phase) == (True, None), why

    for phase, model_kw in (
        ("P6a", {"p6a_model": "claude-sonnet-5.5"}),
        ("P6b", {"p6b_model": "claude-sonnet-5.5"}),
        ("P7", {"p7_model": "claude-sonnet-5.5"}),
    ):
        seed, twin = tmp_path / f"same-{phase}", tmp_path / f"twin-{phase}"
        _vendors(seed, **model_kw)
        _vendors(twin)
        ok, why, refused_phase = c.check_independence(_ctx(repo, seed))
        assert (ok, refused_phase) == (False, phase), why
        assert c.check_independence(_ctx(repo, twin))[0] is True

    missing, twin = tmp_path / "missing-P6a", tmp_path / "twin-missing-P6a"
    _vendors(missing)
    _vendors(twin)
    (missing / "P6a.json").unlink()
    ok, why, phase = c.check_independence(_ctx(repo, missing))
    assert (ok, phase) == (False, "P6a") and "P6a" in why
    assert c.check_independence(_ctx(repo, twin))[0] is True


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


# --- P4 finding: the declared checker argv runs conductor.py as a SCRIPT ---------------------------

@pytest.mark.parametrize("cid", ["C-SCOPE", "C-RED", "C-VENDOR"])
def test_a_receipt_reading_checker_runs_as_declared_without_an_import_error(tmp_path, cid):
    """harness.yaml runs `python scripts/conductor.py lane --constraint <id>`: only scripts/ is on
    sys.path then, so the PhaseReceipt import must not depend on the caller's path."""
    import os  # noqa: PLC0415
    repo = _new_repo(tmp_path, "asscript")
    rdir = tmp_path / "round"
    rdir.mkdir()
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    out = subprocess.run([sys.executable, str(_CONDUCTOR), "lane", "--constraint", cid,
                          "--repo-root", str(repo), "--base", "HEAD", "--round-dir", str(rdir),
                          "--row", "1535"],
                         capture_output=True, text=True, encoding="utf-8", cwd=str(tmp_path), env=env,
                         timeout=120)
    assert "Traceback" not in out.stderr and "ModuleNotFoundError" not in out.stderr, out.stderr
    assert out.returncode == 1 and cid in out.stdout, (out.returncode, out.stdout, out.stderr)


# --- lane contracts ([#1689]): phase rows come from the frozen contract -------------------------

_CONTRACT = _REPO / "tests" / "fixtures" / "e30-three-phase-contract.md"
_ADVISOR_TOKEN = "--disallowedTools=AskUserQuestion,advisor"


def _claude_head(argv: list[str]) -> bool:
    head = argv[0].replace("\\", "/").rsplit("/", 1)[-1].lower()
    return head.removesuffix(".exe").removesuffix(".cmd") == "claude"


def test_contract_phases_parses_the_three_phase_fixture():
    phases = _conductor().contract_phases(_CONTRACT.read_text(encoding="utf-8"))
    assert [phase["id"] for phase in phases] == ["P1", "P2", "P3"]
    assert [phase["name"] for phase in phases] == ["spec", "red", "implement"]


def test_contract_phases_returns_none_without_a_phases_section():
    assert _conductor().contract_phases("# Contract\n\nNo phase table here.\n") is None


@pytest.mark.parametrize("block", [
    "other: []",
    "phases:\n  - id: P1\n    name: spec\n    row_phase: build\n    role: plan\n"
    "    cli: uv\n    gate: payload\n    timeout_s: 60\n",
    "phases:\n  - id: P1\n    name: spec\n    row_phase: build\n    role: plan\n"
    "    cli: uv\n    gate: payload\n    timeout_s: 60\n    command: []\n",
    "phases:\n  - id: P1\n    name: spec\n    row_phase: build\n    role: plan\n"
    "    cli: uv\n    gate: invalid\n    timeout_s: 60\n    command: [uv]\n",
    "phases:\n  - id: P1\n    name: spec\n    row_phase: build\n    role: plan\n"
    "    cli: uv\n    gate: exit\n    timeout_s: 60\n    command: [uv]\n"
    "  - id: P1\n    name: duplicate\n    row_phase: build\n    role: plan\n"
    "    cli: uv\n    gate: exit\n    timeout_s: 60\n    command: [uv]\n",
])
def test_contract_phases_rejects_malformed_phase_tables(block):
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases(f"## Phases\n\n```yaml\n{block}```\n")


def test_contract_phases_rejects_multiple_yaml_blocks():
    text = "## Phases\n\n```yaml\nphases: []\n```\n\n```yaml\nphases: []\n```\n"
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases(text)


def test_contract_phases_rejects_a_phases_section_without_a_yaml_block():
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases("## Phases\n\nPhase table intentionally omitted.\n")


@pytest.mark.parametrize("head", [
    "claude",
    "claude.cmd",
    r"C:\Program Files\Claude\claude.exe",
])
def test_add_disallowed_advisor_handles_claude_commands_and_fallbacks_idempotently(head):
    import copy  # noqa: PLC0415

    c = _conductor()
    rows = [{"id": "P1", "command": [head, "-p"], "fallback": ["claude", "-p"]},
            {"id": "P2", "command": ["uv", "run"], "fallback": ["copilot", "-p"]}]
    before = copy.deepcopy(rows)
    transformed = c.add_disallowed_advisor(rows)

    assert transformed[0]["command"] == [head, _ADVISOR_TOKEN, "-p"]
    assert transformed[0]["fallback"] == ["claude", _ADVISOR_TOKEN, "-p"]
    assert transformed[1] == rows[1]
    assert c.add_disallowed_advisor(transformed) == transformed
    assert transformed[0]["command"].count(_ADVISOR_TOKEN) == 1
    assert transformed[0]["fallback"].count(_ADVISOR_TOKEN) == 1
    assert rows == before, "the input rows must not be mutated"


def test_render_contract_harness_merges_phases_preserves_constraints_and_adds_advisor(tmp_path):
    c = _conductor()
    original_bytes = _HARNESS.read_bytes()
    original = yaml.safe_load(original_bytes)
    out = tmp_path / "receipts" / "LANE-test" / "r1" / "harness.contract.yaml"
    harness_path, source = c.render_contract_harness(_CONTRACT, _HARNESS, out)

    assert harness_path == out and out.is_file()
    assert "contract" in source.lower() and str(_CONTRACT) in source
    rendered = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert [phase["id"] for phase in rendered["phases"]] == ["P1", "P2", "P3"]
    assert rendered["constraints"] == original["constraints"]
    for phase in rendered["phases"]:
        for field in ("command", "fallback"):
            argv = phase.get(field)
            if argv and _claude_head(argv):
                assert argv[1] == _ADVISOR_TOKEN
                assert argv.count(_ADVISOR_TOKEN) == 1
    assert hashlib.sha256(_HARNESS.read_bytes()).digest() == hashlib.sha256(original_bytes).digest()


def test_render_contract_harness_falls_back_without_writing_output(tmp_path):
    c = _conductor()
    contract = tmp_path / "no-phases.md"
    contract.write_text("# Contract\n\nNo phase table.\n", encoding="utf-8")
    out = tmp_path / "receipts" / "LANE-test" / "r1" / "harness.contract.yaml"

    harness_path, source = c.render_contract_harness(contract, _HARNESS, out)

    assert harness_path == _HARNESS
    assert "no ## phases" in source.lower() or "ecosystem/harness.yaml" in source or str(_HARNESS) in source
    assert not out.exists()


def test_lane_cli_runs_only_contract_phases_and_writes_the_contract_harness(tmp_path):
    lane = "e30-test-" + uuid.uuid4().hex
    marker = tmp_path / "phase-runs.txt"
    receipts = tmp_path / "receipts"
    env = {**os.environ, "STUB_PHASE_MARKER": str(marker)}
    out = subprocess.run(
        [sys.executable, str(_CONDUCTOR), "lane", "--lane", lane, "--round", "1",
         "--contract", str(_CONTRACT), "--receipts", str(receipts)],
        capture_output=True, text=True, encoding="utf-8", cwd=_REPO, env=env, timeout=240)

    assert out.returncode == 0, out.stdout + out.stderr
    source = next((line for line in out.stdout.splitlines() if line.startswith("harness source:")), "")
    assert "contract" in source.lower() and str(_CONTRACT) in source
    round_dir = receipts / f"LANE-{lane}" / "r1"
    assert all((round_dir / f"{pid}.json").is_file() for pid in ("P1", "P2", "P3"))
    assert (round_dir / "harness.contract.yaml").is_file()
    assert len(marker.read_text(encoding="utf-8").splitlines()) == 3


def test_lane_cli_falls_back_to_the_requested_harness_when_contract_has_no_phases(tmp_path):
    contract = tmp_path / "no-phases.md"
    contract.write_text("# Contract\n\nNo phase table.\n", encoding="utf-8")
    harness, markers = _toy_round_harness(tmp_path)
    lane = "e30-fallback-" + uuid.uuid4().hex
    receipts = tmp_path / "receipts"
    out = subprocess.run(
        [sys.executable, str(_CONDUCTOR), "lane", "--lane", lane, "--round", "1",
         "--contract", str(contract), "--harness", str(harness), "--receipts", str(receipts)],
        capture_output=True, text=True, encoding="utf-8", cwd=_REPO, timeout=240)

    assert out.returncode == 0, out.stdout + out.stderr
    source = next((line for line in out.stdout.splitlines() if line.startswith("harness source:")), "")
    assert str(harness) in source
    assert str(contract) not in source
    assert "no ## phases" in source.lower()
    round_dir = receipts / f"LANE-{lane}" / "r1"
    assert all((round_dir / f"{pid}.json").is_file() for pid in ("P1", "P2", "P3", "P7"))
    assert (markers / "count.txt").is_file()


_FULL_ROW = {"id": "P1", "name": "spec", "row_phase": "build", "role": "plan", "cli": "uv", "model": None,
             "payload_model": "PhasePayload", "gate": "exit", "timeout_s": 60, "budget_usd": 0,
             "max_rounds": 2, "inputs": [], "command": ["uv", "run"]}


def _phases_text(row: dict) -> str:
    return "## Phases\n\n```yaml\n" + yaml.safe_dump({"phases": [row]}) + "```\n"


def test_contract_phases_accepts_a_row_with_the_full_harness_schema():
    assert _conductor().contract_phases(_phases_text(_FULL_ROW)) == [_FULL_ROW]


@pytest.mark.parametrize("key", ["model", "payload_model", "budget_usd", "max_rounds", "inputs"])
def test_contract_phases_rejects_a_row_missing_a_harness_schema_key(key):
    row = {k: v for k, v in _FULL_ROW.items() if k != key}
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases(_phases_text(row))


@pytest.mark.parametrize("field, value", [("inputs", "not-a-list"), ("max_rounds", 0),
                                          ("max_rounds", "2"), ("budget_usd", -1),
                                          ("budget_usd", "free"), ("payload_model", 3)])
def test_contract_phases_rejects_a_wrongly_typed_harness_schema_value(field, value):
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases(_phases_text({**_FULL_ROW, field: value}))


def test_lane_cli_with_a_contract_and_relative_receipts_works_from_outside_the_repo_root(tmp_path):
    """Sol judge finding: the rendered harness and the receipts root were handed to the doit child
    (cwd = repo root) as caller-relative paths, so a run from any other directory lost both."""
    lane = "e30-relative-" + uuid.uuid4().hex
    out = subprocess.run(
        [sys.executable, str(_CONDUCTOR), "lane", "--repo-root", str(_REPO), "--lane", lane,
         "--round", "1", "--contract", str(_CONTRACT), "--receipts", "rel-receipts"],
        capture_output=True, text=True, encoding="utf-8", cwd=tmp_path, timeout=240)

    assert out.returncode == 0, out.stdout + out.stderr
    round_dir = tmp_path / "rel-receipts" / f"LANE-{lane}" / "r1"
    assert all((round_dir / f"{pid}.json").is_file() for pid in ("P1", "P2", "P3")), out.stdout
    assert (round_dir / "harness.contract.yaml").is_file()
    assert not (_REPO / "rel-receipts").exists(), "receipts must resolve against the caller, not the repo"


@pytest.mark.parametrize("argv, expected", [
    (["claude", "-p", "--disallowedTools=Bash"],
     ["claude", "--disallowedTools=Bash,AskUserQuestion,advisor", "-p"]),
    (["claude", "--disallowedTools=advisor,Edit", "-p"],
     ["claude", "--disallowedTools=advisor,Edit,AskUserQuestion", "-p"]),
    (["claude", "-p", "--disallowedTools", "Bash,Edit"],
     ["claude", "--disallowedTools=Bash,Edit,AskUserQuestion,advisor", "-p"]),
    (["claude", "-p", "--disallowed-tools=Bash"],
     ["claude", "--disallowedTools=Bash,AskUserQuestion,advisor", "-p"]),
])
def test_add_disallowed_advisor_merges_into_an_existing_disallowed_tools_flag(argv, expected):
    """Sol judge finding: a second --disallowedTools flag could override the inserted advisor block."""
    c = _conductor()
    for field_name in ("command", "fallback"):
        out = c.add_disallowed_advisor([{"id": "P1", field_name: list(argv)}])[0][field_name]
        flags = [t for t in out if t.startswith("--disallow")]
        assert out == expected
        assert len(flags) == 1
        assert c.add_disallowed_advisor([{"id": "P1", field_name: out}])[0][field_name] == out


def test_contract_phases_rejects_an_unhashable_phase_id_as_a_contract_error():
    with pytest.raises(_conductor().ContractPhasesError):
        _conductor().contract_phases(_phases_text({**_FULL_ROW, "id": ["P1"]}))


@pytest.mark.parametrize("argv, expected", [
    (["claude", "-p", "--disallowedTools"],
     ["claude", "--disallowedTools=AskUserQuestion,advisor", "-p"]),
    (["claude", "--disallowedTools", "--model", "x", "-p"],
     ["claude", "--disallowedTools=AskUserQuestion,advisor", "--model", "x", "-p"]),
])
def test_add_disallowed_advisor_does_not_consume_an_option_as_a_bare_flags_value(argv, expected):
    """Terra review finding: a valueless bare flag stayed in argv (two flags), or ate the next option."""
    c = _conductor()
    out = c.add_disallowed_advisor([{"id": "P1", "command": list(argv)}])[0]["command"]
    assert out == expected
    assert len([t for t in out if t.startswith("--disallow")]) == 1


# --- lane e30-conductor-phase-order: red contract tests ------------------------------------------

def _item1_prompts():
    codex = (
        "You are phase P7 (judge) of lane {lane}, row {row}. Judge ONLY from these inputs: "
        "the contract {contract}; the diff (git diff {base}...HEAD); "
        "{round_dir}/P6c-OUTPUT.txt, the pushed-run CI verdict of HEAD; and the review payloads "
        "{round_dir}/P6a.payload.json and {round_dir}/P6b.payload.json. Read no other file in "
        "{round_dir} and no producer prose (no P1, P2 or P3 payload or OUTPUT file). Decide whether "
        "the round is accepted against the contract's Done-contract. Your final message is ONLY one "
        "JSON object (a PhasePayload: nonce, input_hash, outcome ACCEPT or REFUSE, findings, detail) "
        "with nonce set to {nonce} and input_hash set to {input_hash} exactly."
    )
    claude = (
        "You are phase P7 (judge) of lane {lane}, row {row}. Judge ONLY from these inputs: "
        "the contract {contract}; the diff (git diff {base}...HEAD); "
        "{round_dir}/P6c-OUTPUT.txt, the pushed-run CI verdict of HEAD; and the review payloads "
        "{round_dir}/P6a.payload.json and {round_dir}/P6b.payload.json. Read no other file in "
        "{round_dir} and no producer prose (no P1, P2 or P3 payload or OUTPUT file). Decide whether "
        "the round is accepted against the contract's Done-contract. Write ONE JSON object (a "
        "PhasePayload: nonce, input_hash, outcome ACCEPT or REFUSE, findings, detail) to {payload}, "
        "with nonce set to {nonce} and input_hash set to {input_hash} exactly."
    )
    return codex, claude


def _item1_render(prompt, values):
    for key, value in values.items():
        prompt = prompt.replace("{" + key + "}", str(value))
    return prompt


def _item1_target_phases():
    import copy  # noqa: PLC0415

    doc = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))
    return copy.deepcopy(doc["phases"])


def _item1_setup(tmp_path, *, same_family=False):
    import shutil  # noqa: PLC0415

    tmp_path.mkdir(parents=True, exist_ok=True)
    repo = tmp_path / "repo"
    repo.mkdir()
    for name in ("scripts", "ecosystem"):
        shutil.copytree(_REPO / name, repo / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                        copy_function=os.link)
    (repo / ".gitignore").write_text(".doit.db*\n__pycache__/\n*.pyc\nlogs/receipts/\n",
                                     encoding="utf-8")
    (repo / "tracked.txt").write_text("committed\n", encoding="utf-8")
    contract = tmp_path / "contract.md"
    contract.write_text("Done-contract fixture\n", encoding="utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture base")

    phases = _item1_target_phases()
    stub = _REPO / "tests" / "fixtures" / "conductor_round_stub.py"
    for phase in phases:
        # C05 of lane e30-round-verdict-handback: P5 is now a live uv ci_verdict.py row, so this fixture stubs it like P4 and P6c
        # (the stub names no ci_verdict.py, so no T2-STALE:P5 check applies).
        if phase["id"] in {"P4", "P5", "P6c"}:
            phase["command"] = [sys.executable, str(stub), phase["id"]]
    if same_family:
        p6b = next(phase for phase in phases if phase["id"] == "P6b")
        p6b["model"] = "claude-sonnet-5.5"
        p6b["command"][p6b["command"].index("gemini-4-argon")] = "claude-sonnet-5.5"
    harness = tmp_path / "harness.yaml"
    harness.write_text(yaml.safe_dump({"stages": [], "moments": [], "phases": phases},
                                      sort_keys=False), encoding="utf-8")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for cli in ("claude", "codex", "copilot"):
        if os.name == "nt":
            wrapper = bin_dir / f"{cli}.cmd"
            wrapper.write_text(f'@echo off\r\n"{sys.executable}" "{stub}" {cli} %*\r\n',
                               encoding="utf-8")
        else:
            wrapper = bin_dir / cli
            wrapper.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{stub}" {cli} "$@"\n',
                               encoding="utf-8")
            wrapper.chmod(0o755)
    receipts = tmp_path / "receipts"
    marker = tmp_path / "marker.log"
    env = {
        "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", ""),
        "HARNESS_CONTRACT": str(contract),
        "STUB_MARKER": str(marker),
    }
    return repo, harness, receipts, marker, contract, env


def _item1_run_round(tmp_path, *, same_family=False, lane=None, round_no=1, env=None):
    repo, harness, receipts, marker, _contract, base_env = _item1_setup(tmp_path, same_family=same_family)
    lane = lane or "e30-" + uuid.uuid4().hex[:12]
    result = _conductor().run_round(
        lane, round_no, repo_root=repo, harness=harness, receipts=receipts, row="1848",
        env={**base_env, **(env or {})},
    )
    return result, receipts / f"LANE-{lane}" / f"r{round_no}", repo, marker, harness, base_env


def _receipt_json(round_dir, phase, *, vendor, model_requested=None, served_model=None,
                  command=None, substituted_from=None, inputs=None, lane="lane-e30", row="1848",
                  nonce="n" * 16):
    heads = {
        "anthropic": "claude",
        "openai": "codex",
        "google": "copilot",
        "xai": "grok",
        "copilot-enterprise": "copilot",
        "local": "python",
    }
    argv = command or [heads[vendor], "-p", "receipt fixture"]
    data = {
        "schema": "phase-receipt/1",
        "organ": f"phase:{phase}",
        "status": "ok",
        "exit_code": 0,
        "duration_ms": 1,
        "input_hash": _HEX,
        "model_requested": model_requested,
        "model_reported": served_model,
        "command": argv,
        "finished_at": _NOW,
        "row": row,
        "lane": lane,
        "phase": phase,
        "round": 1,
        "vendor": vendor,
        "cli_version": None,
        "served_model": served_model,
        "started_at": _NOW,
        "inputs": inputs or [],
        "nonce": nonce,
        "usage": None,
        "payload_sha256": None,
        "payload": None,
        "substituted_from": substituted_from,
    }
    round_dir.mkdir(parents=True, exist_ok=True)
    path = round_dir / f"{phase}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _item1_seed_independence(round_dir, *, p3_model="claude-sonnet-5.5",
                             p6b_model="gemini-4-argon", p7_model="gpt-6-sol"):
    _receipt_json(round_dir, "P3", vendor="copilot-enterprise", model_requested=p3_model)
    _receipt_json(round_dir, "P6a", vendor="openai", model_requested="gpt-5.6-terra")
    _receipt_json(round_dir, "P6b", vendor="copilot-enterprise", model_requested=p6b_model)
    _receipt_json(round_dir, "P7", vendor="openai", model_requested=p7_model)


def _item1_admission_phases():
    import copy  # noqa: PLC0415

    return copy.deepcopy(_item1_target_phases())


def _item1_admission_case(tmp_path, *, command_changes=None, substituted_from="openai",
                          prompt_change=None, p7_output=None, p3_output=None, p6b_model="gemini-4-argon",
                          phases=None):
    from types import SimpleNamespace  # noqa: PLC0415

    c = _conductor()
    round_dir = tmp_path / "round"
    contract = tmp_path / "contract.md"
    tmp_path.mkdir(parents=True, exist_ok=True)
    contract.write_text("contract\n", encoding="utf-8")
    ctx = c.LaneContext(repo_root=_REPO, base="base-ref", round_dir=round_dir, row="1848")
    _receipt_json(round_dir, "P3", vendor="copilot-enterprise", model_requested="claude-sonnet-5.5")
    _receipt_json(round_dir, "P6a", vendor="openai", model_requested="gpt-5.6-terra")
    _receipt_json(round_dir, "P6b", vendor="copilot-enterprise", model_requested=p6b_model)
    p7_row = next(row for row in (phases or _item1_admission_phases()) if row["id"] == "P7")
    values = {
        "lane": "lane-e30",
        "row": "1848",
        "contract": str(contract),
        "base": ctx.base,
        "round_dir": str(round_dir),
        "nonce": "n" * 16,
        "input_hash": _HEX,
        "payload": str(round_dir / "P7.payload.json"),
    }
    _codex_prompt, claude_prompt = _item1_prompts()
    prompt = _item1_render(claude_prompt, values)
    if prompt_change:
        prompt = prompt.replace("P6b.payload.json", prompt_change)
    command = ["claude", "-p", "--model", "claude-opus-5-5", prompt]
    command.extend(command_changes or [])
    _receipt_json(
        round_dir, "P7", vendor="anthropic", model_requested="claude-opus-5-5",
        command=command, substituted_from=substituted_from,
        inputs=[{"path": str(contract), "sha256": _HEX}], lane="lane-e30", row="1848",
    )
    if p7_output is not None:
        (round_dir / "P7-OUTPUT.txt").write_text(p7_output, encoding="utf-8")
    if p3_output is not None:
        (round_dir / "P3-OUTPUT.txt").write_text(p3_output, encoding="utf-8")
    return c, ctx, phases or _item1_admission_phases(), SimpleNamespace(
        command=command, prompt=prompt, values=values, configured=p7_row["command"])


def test_item1a_fixture_round_with_valid_receipts_and_payloads_accepts(tmp_path):
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    result, round_dir, _repo, _marker, _harness, _env = _item1_run_round(tmp_path)
    assert (result.verdict, result.exit_code) == ("ACCEPT", 0), result.phases
    assert set(("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")).issubset(
        {path.stem for path in round_dir.glob("*.json")}
    )
    for phase in ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7"):
        PhaseReceipt.model_validate(json.loads((round_dir / f"{phase}.json").read_text(encoding="utf-8")))
    assert result.refused_by is None


def test_item1b_c_vendor_needs_only_readable_p3_receipt(tmp_path):
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    c = _conductor()
    round_dir = tmp_path / "round"
    for phase, vendor, model in (
        ("P1", "anthropic", "claude-opus-5-5"),
        ("P2", "anthropic", "claude-sonnet-5-5"),
        ("P3", "copilot-enterprise", "claude-sonnet-5.5"),
    ):
        _receipt_json(round_dir, phase, vendor=vendor, model_requested=model)
    for phase in ("P1", "P2", "P3"):
        PhaseReceipt.model_validate(json.loads((round_dir / f"{phase}.json").read_text(encoding="utf-8")))
    ok, why = c.check_constraint("C-VENDOR", c.LaneContext(_REPO, "HEAD", round_dir))
    assert ok is True and "missing receipt" not in why
    (round_dir / "P3.json").unlink()
    ok, why = c.check_constraint("C-VENDOR", c.LaneContext(_REPO, "HEAD", round_dir))
    assert ok is False and "P3" in why


def test_item1c_same_model_family_for_p6b_is_refused_after_p7(tmp_path):
    c = _conductor()
    round_dir = tmp_path / "round"
    _item1_seed_independence(round_dir, p6b_model="claude-sonnet-5.5")
    ok, why, phase = c.check_independence(c.LaneContext(_REPO, "base", round_dir),
                                         phases=_item1_admission_phases())
    assert (ok, phase) == (False, "P6b")
    assert why


def test_item1d_same_cli_with_different_model_families_is_independent(tmp_path):
    c = _conductor()
    round_dir = tmp_path / "round"
    _item1_seed_independence(round_dir)
    ok, why, phase = c.check_independence(c.LaneContext(_REPO, "base", round_dir),
                                         phases=_item1_admission_phases())
    assert (ok, phase) == (True, None), why


def test_item1c_missing_receipt_or_model_fails_closed_by_phase(tmp_path):
    c = _conductor()
    for missing in ("P3", "P6a", "P6b", "P7"):
        round_dir = tmp_path / missing
        _item1_seed_independence(round_dir)
        (round_dir / f"{missing}.json").unlink()
        ok, why, phase = c.check_independence(
            c.LaneContext(_REPO, "base", round_dir), phases=_item1_admission_phases(),
        )
        assert (ok, phase) == (False, missing)
        assert missing in why
    round_dir = tmp_path / "no-model"
    _item1_seed_independence(round_dir)
    _receipt_json(round_dir, "P7", vendor="openai", model_requested=None)
    ok, why, phase = c.check_independence(
        c.LaneContext(_REPO, "base", round_dir), phases=_item1_admission_phases(),
    )
    assert (ok, phase) == (False, "P7")
    assert "model" in why.lower()


@pytest.mark.parametrize("flag", [
    "--resume", "--resume=session", "--continue", "-c", "-r", "--session-id", "--session-id=abc",
])
def test_item1e_admission_refuses_each_session_reuse_flag(tmp_path, flag):
    c, ctx, phases, _details = _item1_admission_case(tmp_path, command_changes=[flag])
    ok, why, phase = c.check_independence(ctx, phases=phases)
    assert (ok, phase) == (False, "P7")
    assert why


@pytest.mark.parametrize("prompt_change,substituted_from,wrong_primary", [
    ("P3.payload.json", "openai", False),
    (None, "anthropic", False),
    (None, None, False),
    (None, "openai", True),
])
def test_item1e_admission_refuses_a_missing_prompt_substitution_or_primary_leg(
        tmp_path, prompt_change, substituted_from, wrong_primary):
    c, ctx, configured, _details = _item1_admission_case(
        tmp_path, prompt_change=prompt_change, substituted_from=substituted_from,
        phases=_item1_admission_phases(),
    )
    if wrong_primary:
        p7 = next(row for row in configured if row["id"] == "P7")
        p7["command"] = ["codex", "exec", "-m", "other-model", "-s", "read-only", "-o",
                         "{payload}", _item1_prompts()[0]]
    ok, why, phase = c.check_independence(ctx, phases=configured)
    assert (ok, phase) == (False, "P7")
    assert why


def test_item1e_equal_claude_session_ids_refuse_but_unavailable_ids_do_not(tmp_path):
    import json as _json  # noqa: PLC0415

    c, ctx, phases, _details = _item1_admission_case(
        tmp_path / "equal", p7_output=_json.dumps({"type": "result", "session_id": "same"}),
        p3_output=_json.dumps({"type": "result", "session_id": "same"}),
    )
    ok, why, phase = c.check_independence(ctx, phases=phases)
    assert (ok, phase) == (False, "P7")
    assert why
    for name, p7_text, p3_text in (
        ("absent", None, None),
        ("empty", "", _json.dumps({"type": "result", "session_id": "same"})),
        ("unparseable", "{", _json.dumps({"type": "result", "session_id": "same"})),
        ("no-session", _json.dumps({"type": "result"}), _json.dumps({"type": "result"})),
        ("copilot-producer", _json.dumps({"type": "result", "session_id": "judge"}),
         "copilot output, not Claude JSON"),
    ):
        case_dir = tmp_path / name
        c, ctx, phases, _details = _item1_admission_case(
            case_dir, p7_output=p7_text, p3_output=p3_text,
        )
        ok, why, phase = c.check_independence(ctx, phases=phases)
        assert (ok, phase) == (True, None), why


def test_item1e_isolated_anthropic_fallback_is_admitted(tmp_path):
    c, ctx, phases, _details = _item1_admission_case(tmp_path)
    ok, why, phase = c.check_independence(ctx, phases=phases)
    assert (ok, phase) == (True, None), why


def test_item1e_prompt_constants_are_hash_pinned_and_match_both_harness_argvs():
    import hashlib as _hashlib  # noqa: PLC0415

    c = _conductor()
    assert _hashlib.sha256(c.ISOLATED_JUDGE_PROMPT_CODEX.encode("utf-8")).hexdigest() == (
        "4a86f888e88be25a6ec27d4430172edaf156ddd7b9c4a1b9f36909e1445de0cb"
    )
    assert _hashlib.sha256(c.ISOLATED_JUDGE_PROMPT_CLAUDE.encode("utf-8")).hexdigest() == (
        "4dc6fc3b6c3a1c7e6cc6a50ff458e3c67817a9b8026931cfdf77bb71dd25c594"
    )
    phases = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["phases"]
    p7 = next(row for row in phases if row["id"] == "P7")
    values = {
        "lane": "lane-fixed", "row": "1848", "base": "origin/example",
        "round_dir": "C:\\round\\r1", "nonce": "n" * 16, "input_hash": _HEX,
        "contract": "C:\\contract.md", "payload": "C:\\round\\r1\\P7.payload.json",
    }
    codex_prompt = _item1_render(c.ISOLATED_JUDGE_PROMPT_CODEX, values)
    claude_prompt = _item1_render(c.ISOLATED_JUDGE_PROMPT_CLAUDE, values)
    primary = [token.replace("{payload}", values["payload"]) for token in p7["command"]]
    fallback = [token.replace("{payload}", values["payload"]) for token in p7["fallback"]]
    for key, value in values.items():
        primary = [token.replace("{" + key + "}", value) for token in primary]
        fallback = [token.replace("{" + key + "}", value) for token in fallback]
    assert primary[-1] == codex_prompt
    assert fallback[fallback.index(claude_prompt)] == claude_prompt
    for prompt in (primary[-1], fallback[fallback.index(claude_prompt)]):
        assert f'{values["round_dir"]}/P6c-OUTPUT.txt' in prompt
        assert f'{values["round_dir"]}/P1' not in prompt
        assert f'{values["round_dir"]}/P2' not in prompt
        assert f'{values["round_dir"]}/P3' not in prompt
    assert "Write ONE JSON object" in claude_prompt and values["payload"] in claude_prompt


def test_item1f_model_families_and_receipt_model_precedence(tmp_path):
    from types import SimpleNamespace  # noqa: PLC0415

    c = _conductor()
    registry = tmp_path / "registry.yaml"
    registry.write_text("models:\n  custom-id:\n    family: custom-family\n", encoding="utf-8")
    assert c.model_family("custom-id", registry) == "custom-family"
    assert c.model_family("gemini-4-argon") == "google"
    assert c.model_family("gpt-6-sol") == "openai"
    assert c.model_family("claude-sonnet-5.5") == "anthropic"
    assert c.model_family("claude-sonnet-5-5") == "anthropic"
    with pytest.raises(c.FamilyError, match="mistral-x"):
        c.model_family("mistral-x")
    assert c.receipt_model_id(SimpleNamespace(served_model="claude-opus-5-5",
                                              model_requested="gpt-6-sol")) == "claude-opus-5-5"
    assert c.receipt_model_id(SimpleNamespace(served_model="UNVERIFIED",
                                              model_requested="gpt-6-sol")) == "gpt-6-sol"
    assert c.receipt_model_id(SimpleNamespace(served_model="", model_requested="gpt-6-sol")) == "gpt-6-sol"
    assert c.receipt_model_id(SimpleNamespace(served_model=None, model_requested=None)) is None
    round_dir = tmp_path / "unknown-family"
    _item1_seed_independence(round_dir, p6b_model="mistral-x")
    ok, why, phase = c.check_independence(c.LaneContext(_REPO, "base", round_dir),
                                         phases=_item1_admission_phases())
    assert (ok, phase) == (False, "P6b") and "mistral-x" in why


def test_item1g_real_harness_phase_shape_and_phase_row_validation():
    c = _conductor()
    lines = _HARNESS.read_text(encoding="utf-8").splitlines()
    doc = yaml.safe_load("\n".join(lines))
    phases = doc["phases"]
    ids = [row["id"] for row in phases]
    assert ids == ["P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7"]
    p6b = next(row for row in phases if row["id"] == "P6b")
    assert p6b["name"] == "review-gemini"
    assert (p6b["cli"], p6b["model"]) == ("copilot", "gemini-4-argon")
    expected_p6b_prompt = (
        "You are phase P6b (review) of lane {lane}, row {row}. Review the diff against {base} "
        "for the contract {contract}: report only bugs and contract breaks, with evidence. Do not "
        "edit the repository. Write ONE JSON object (a PhasePayload: nonce, input_hash, outcome "
        "PASS or FAIL, findings, detail) to {payload}, with nonce set to {nonce} and input_hash "
        "set to {input_hash} exactly."
    )
    assert p6b["command"] == [
        "copilot", "-p", expected_p6b_prompt, "--model", "gemini-4-argon", "--allow-all-tools",
        "--no-ask-user", "--usage-output-file", "{round_dir}/P6b.usage.json", "-s", "--no-color",
    ]
    assert all("grok" not in json.dumps(row).lower() for row in phases)
    p6a = next(row for row in phases if row["id"] == "P6a")
    read_only = p6a["command"].index("read-only")
    assert p6a["command"][read_only + 1:read_only + 3] == ["-o", "{payload}"]
    p6c = next(row for row in phases if row["id"] == "P6c")
    assert p6c == {
        "id": "P6c", "name": "t2-verdict", "row_phase": "build", "role": "qa", "cli": "uv",
        "model": None, "payload_model": "PhasePayload", "gate": "exit", "timeout_s": 1500,
        "budget_usd": 0, "max_rounds": 2, "inputs": ["{contract}"],
        # C05 of lane e30-round-verdict-handback appends --landable to the P6c command.
        "command": ["uv", "run", "--locked", "python", "scripts/ci_verdict.py", "--ref", "HEAD",
                    "--timeout", "1200", "--landable"],
    }
    p7 = next(row for row in phases if row["id"] == "P7")
    assert (p7["cli"], p7["model"]) == ("codex", "gpt-6-sol")
    assert p7["command"] == [
        "codex", "exec", "-m", "gpt-6-sol", "-s", "read-only", "-o", "{payload}",
        c.ISOLATED_JUDGE_PROMPT_CODEX,
    ]
    assert p7["inputs"] == [
        "{contract}", "{round_dir}/P6c-OUTPUT.txt",
        "{round_dir}/P6a.payload.json", "{round_dir}/P6b.payload.json",
    ]
    fallback = p7["fallback"]
    assert fallback[0] == "claude" and fallback[fallback.index("--model") + 1] == "claude-opus-5-5"
    assert fallback[fallback.index("--disallowedTools=AskUserQuestion,advisor")] == (
        "--disallowedTools=AskUserQuestion,advisor"
    )
    assert p7["fallback"].count("--disallowedTools=AskUserQuestion,advisor") == 1
    rendered = c.add_disallowed_advisor(phases)
    rendered_fallback = next(row for row in rendered if row["id"] == "P7")["fallback"]
    assert rendered_fallback.count("--disallowedTools=AskUserQuestion,advisor") == 1
    assert "model family" in next(row for row in doc["constraints"] if row["id"] == "C-VENDOR")["reuses"]
    # cap 202 -> 204, the same cap as tests/test_dodo.py (Q-PO-1/Q-SV-1 cap rule): P6c ([#1848]) and system_view_full (L13)
    assert len(lines) < 204
    c._validate_phase_rows(phases)


def test_item1g_p6c_orders_phases_halts_and_invalidates_p7_cache(tmp_path):
    result, round_dir, _repo, marker, _harness, env = _item1_run_round(tmp_path / "order")
    assert result.verdict == "ACCEPT"
    marks = marker.read_text(encoding="utf-8").splitlines()
    assert marks.index("P6b copilot") < marks.index("P6c local") < marks.index("P7 codex")

    failed, failed_dir, _repo, failed_marker, _harness, failed_env = _item1_run_round(
        tmp_path / "failed", env={"STUB_FAIL": "P6c"},
    )
    assert (failed.verdict, failed.halted_at, failed.exit_code) == ("HALTED", "P6c", 1)
    assert "P7 codex" not in failed_marker.read_text(encoding="utf-8").splitlines()
    assert not (failed_dir / "P7.json").exists()

    lane = "e30-cache-" + uuid.uuid4().hex[:8]
    repo, harness, receipts, cached_marker, _contract, base_env = _item1_setup(tmp_path / "cache")
    c = _conductor()
    cached = c.run_round(lane, 1, repo_root=repo, harness=harness, receipts=receipts,
                         row="1848", env=base_env)
    cached_dir = receipts / f"LANE-{lane}" / "r1"
    assert cached.verdict == "ACCEPT"
    output = cached_dir / "P6c-OUTPUT.txt"
    data = json.loads(output.read_text(encoding="utf-8"))
    data["run_id"] = 2
    output.write_text(json.dumps(data), encoding="utf-8")
    second = c.run_round(lane, 1, repo_root=repo, harness=harness, receipts=receipts,
                         row="1848", env=base_env)
    assert second.verdict == "ACCEPT"
    assert cached_marker.read_text(encoding="utf-8").splitlines().count("P7 codex") == 2
    assert cached_marker.read_text(encoding="utf-8").splitlines().count("P6c local") == 1


def test_item1g_p7_is_not_launched_when_p6c_does_not_complete(tmp_path):
    result, round_dir, _repo, marker, _harness, _env = _item1_run_round(
        tmp_path, env={"STUB_FAIL": "P6c"},
    )
    assert (result.verdict, result.halted_at) == ("HALTED", "P6c")
    assert not (round_dir / "P7.json").exists()
    assert "P7 codex" not in marker.read_text(encoding="utf-8").splitlines()


def test_item1h_p6b_requires_payload_and_records_usage_argv(tmp_path):
    failed, _dir, _repo, _marker, _harness, _env = _item1_run_round(
        tmp_path / "missing", env={"STUB_SKIP_PAYLOAD": "P6b"},
    )
    assert (failed.verdict, failed.halted_at) == ("HALTED", "P6b")

    result, round_dir, _repo, _marker, _harness, _env = _item1_run_round(tmp_path / "payload")
    assert result.verdict == "ACCEPT"
    data = json.loads((round_dir / "P6b.json").read_text(encoding="utf-8"))
    command = data["command"]
    usage_index = command.index("--usage-output-file")
    assert command[usage_index + 1] == f"{round_dir}/P6b.usage.json"


@pytest.mark.parametrize("p7_session,expected_verdict,expected_refusal", [
    ("different", "ACCEPT", None),
    ("same", "REFUSED", "C-VENDOR:P7"),
    ("none", "ACCEPT", None),
])
def test_item1i_claude_fallback_session_evidence_controls_admission(
        tmp_path, p7_session, expected_verdict, expected_refusal):
    env = {
        "STUB_FAIL": "P7:codex",
        "STUB_SESSION_P3": "session-producer",
    }
    if p7_session == "different":
        env["STUB_SESSION_P7"] = "session-judge"
    elif p7_session == "same":
        env["STUB_SESSION_P7"] = "session-producer"
    else:
        env["STUB_NO_JSON"] = "P7"
    result, round_dir, _repo, marker, _harness, _base_env = _item1_run_round(
        tmp_path, env=env,
    )
    p7 = json.loads((round_dir / "P7.json").read_text(encoding="utf-8"))
    assert p7["substituted_from"] == "openai"
    assert (round_dir / "P7-OUTPUT.txt").is_file()
    assert marker.read_text(encoding="utf-8").splitlines().count("P7 codex") == 1
    if p7_session == "none":
        assert (round_dir / "P7-OUTPUT.txt").read_text(encoding="utf-8").strip() == ""
    else:
        assert json.loads((round_dir / "P7-OUTPUT.txt").read_text(encoding="utf-8"))["session_id"] == (
            "session-producer" if p7_session == "same" else "session-judge"
        )
    assert (result.verdict, result.refused_by) == (expected_verdict, expected_refusal)
    assert marker.read_text(encoding="utf-8").splitlines().count("P7 claude") == 1


def test_item1j_same_family_reviewer_refuses_without_halting(tmp_path):
    result, _round_dir, _repo, _marker, _harness, _env = _item1_run_round(
        tmp_path, same_family=True,
    )
    assert (result.verdict, result.exit_code, result.refused_by, result.halted_at) == (
        "REFUSED", 2, "C-VENDOR:P6b", None,
    )


@pytest.mark.parametrize("stale_kind", ["working-tree", "wrong-sha"])
def test_item1k_t2_stale_tree_or_verdict_sha_refuses(tmp_path, stale_kind):
    env = {}
    if stale_kind == "working-tree":
        env = {
            "STUB_EDIT_PHASE": "P5",
            "STUB_EDIT_PATH": str(tmp_path / "repo" / "tracked.txt"),
        }
    else:
        env = {"STUB_BAD_P6C_SHA": "1"}
    result, _round_dir, _repo, _marker, _harness, _base_env = _item1_run_round(
        tmp_path, env=env,
    )
    assert (result.verdict, result.exit_code, result.refused_by) == (
        "REFUSED", 2, "T2-STALE:P6c",
    )


@pytest.mark.parametrize("base_mode,expected", [
    ("argument", "feature/non-default"),
    ("environment", "feature/from-env"),
    ("default", "origin/main"),
])
def test_item1l_lane_cli_renders_base_argument_environment_or_default(tmp_path, base_mode, expected):
    repo, harness, receipts, _marker, contract, base_env = _item1_setup(tmp_path)
    lane = "e30-base-" + uuid.uuid4().hex[:8]
    args = [
        sys.executable, str(_CONDUCTOR), "lane", "--lane", lane, "--round", "1",
        "--repo-root", str(repo), "--harness", str(harness), "--receipts", str(receipts),
    ]
    if base_mode == "argument":
        args.extend(["--base", expected])
    elif base_mode == "environment":
        base_env["HARNESS_BASE"] = expected
    child_env = {**os.environ, **base_env}
    if base_mode != "environment":
        child_env.pop("HARNESS_BASE", None)
    out = subprocess.run(args, cwd=repo, env=child_env, capture_output=True, text=True, timeout=180)
    assert out.returncode == 0, out.stdout + out.stderr
    round_dir = receipts / f"LANE-{lane}" / "r1"
    p6a = json.loads((round_dir / "P6a.json").read_text(encoding="utf-8"))
    prompt = next(token for token in p6a["command"] if "Review the diff" in token)
    assert f"against {expected} for the contract" in prompt


def test_item2_cli_prints_accept_line_and_exits_zero(tmp_path):
    repo, harness, receipts, _marker, _contract, env = _item1_setup(tmp_path)
    lane = "e30-cli-" + uuid.uuid4().hex[:8]
    out = subprocess.run(
        [sys.executable, str(_CONDUCTOR), "lane", "--lane", lane, "--round", "1",
         "--repo-root", str(repo), "--harness", str(harness), "--receipts", str(receipts)],
        cwd=repo, env={**os.environ, **env}, capture_output=True, text=True, timeout=180,
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert f"conductor lane {lane} r1: ACCEPT" in out.stdout


def test_item2_cli_prints_c_vendor_refusal_and_exits_two(tmp_path):
    repo, harness, receipts, _marker, _contract, env = _item1_setup(tmp_path, same_family=True)
    lane = "e30-cli-refused-" + uuid.uuid4().hex[:8]
    out = subprocess.run(
        [sys.executable, str(_CONDUCTOR), "lane", "--lane", lane, "--round", "1",
         "--repo-root", str(repo), "--harness", str(harness), "--receipts", str(receipts)],
        cwd=repo, env={**os.environ, **env}, capture_output=True, text=True, timeout=180,
    )
    assert out.returncode == 2, out.stdout + out.stderr
    assert f"conductor lane {lane} r1: REFUSED by C-VENDOR:P6b" in out.stdout


# --- lane e30-round-verdict-handback: P5 verdict binding -----------------------------------------

def _p5_round_setup(tmp_path, *, p5_mode="ok", p5_command_is_ci=True, include_p6a=False,
                    post_mode="keep", push_state="matching"):
    import shutil  # noqa: PLC0415

    repo = tmp_path / "round-repo"
    repo.mkdir()
    for folder in ("scripts", "ecosystem"):
        shutil.copytree(_REPO / folder, repo / folder,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                        copy_function=os.link)
    (repo / ".gitignore").write_text(
        ".doit.db*\n__pycache__/\n*.pyc\nlogs/receipts/\n", encoding="utf-8", newline="\n"
    )
    (repo / "tracked.txt").write_text("committed\n", encoding="utf-8", newline="\n")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture base")

    p5_script = tmp_path / ("ci_verdict.py" if p5_command_is_ci else "toy_p5.py")
    p5_script.write_text(textwrap.dedent("""\
        import json
        import os
        import subprocess
        import sys
        from pathlib import Path

        mode = sys.argv[1]
        if mode == "fail":
            print("stub P5 failed")
            raise SystemExit(1)
        if mode == "move-head":
            Path("tip.txt").write_text("new tip\\n", encoding="utf-8")
            subprocess.run(["git", "add", "tip.txt"], check=True)
            subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.com",
                            "commit", "-q", "-m", "move head"], check=True)
        if mode == "invalid":
            print("not json")
            raise SystemExit(0)
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        if mode == "wrong-output":
            sha = "0" * 40
        round_dir = (Path(os.environ["HARNESS_RECEIPTS_DIR"]) / f"LANE-{os.environ['HARNESS_LANE']}"
                     / f"r{os.environ['HARNESS_ROUND']}")
        if mode == "move-head":
            (round_dir / "PUSH.json").write_text(json.dumps({"sha": sha}) + "\\n",
                                                  encoding="utf-8")
        print(json.dumps({"sha": sha}))
        """), encoding="utf-8", newline="\n")
    p6a_script = tmp_path / "p6a_stub.py"
    p6a_script.write_text(
        "from pathlib import Path\nimport sys\nPath(sys.argv[1]).write_text('launched')\n",
        encoding="utf-8", newline="\n",
    )
    post_script = tmp_path / "post_stub.py"
    post_script.write_text(textwrap.dedent("""\
        import json
        import os
        import sys
        from pathlib import Path

        if sys.argv[1] == "remove":
            path = (Path(os.environ["HARNESS_RECEIPTS_DIR"]) / f"LANE-{os.environ['HARNESS_LANE']}"
                    / f"r{os.environ['HARNESS_ROUND']}" / "P5-OUTPUT.txt")
            path.unlink()
        Path(sys.argv[2]).write_text(json.dumps({
            "nonce": sys.argv[3], "input_hash": sys.argv[4], "outcome": "ACCEPT"
        }), encoding="utf-8")
        """), encoding="utf-8", newline="\n")

    rows = [
        {"id": "P1", "name": "spec", "row_phase": "build", "role": "toy", "cli": "python",
         "model": None, "payload_model": "PhasePayload", "gate": "payload", "timeout_s": 60,
         "budget_usd": 0, "max_rounds": 2, "inputs": [],
         "command": [sys.executable, str(_REPO / "tests" / "fixtures" / "stub_phase.py"),
                     "{payload}", "{nonce}", "{input_hash}"]},
        {"id": "P5", "name": "qa", "row_phase": "build", "role": "qa", "cli": "python",
         "model": None, "payload_model": "PhasePayload", "gate": "exit", "timeout_s": 60,
         "budget_usd": 0, "max_rounds": 2, "inputs": [],
         "command": [sys.executable, str(p5_script), p5_mode]},
    ]
    marker = tmp_path / "p6a-started"
    if include_p6a:
        rows.append({
            "id": "P6a", "name": "review", "row_phase": "build", "role": "review",
            "cli": "python", "model": None, "payload_model": "PhasePayload", "gate": "exit",
            "timeout_s": 60, "budget_usd": 0, "max_rounds": 2, "inputs": [],
            "command": [sys.executable, str(p6a_script), str(marker)],
        })
    rows.append({
        "id": "P7", "name": "judge", "row_phase": "build", "role": "toy", "cli": "python",
        "model": None, "payload_model": "PhasePayload", "gate": "payload", "timeout_s": 60,
        "budget_usd": 0, "max_rounds": 2, "inputs": [],
        "command": [sys.executable, str(post_script), post_mode, "{payload}", "{nonce}",
                    "{input_hash}"]
        if post_mode != "keep" else
        [sys.executable, str(_REPO / "tests" / "fixtures" / "stub_phase.py"),
         "{payload}", "{nonce}", "{input_hash}"],
    })
    harness = tmp_path / "harness.yaml"
    harness.write_text(yaml.safe_dump({"stages": [], "moments": [], "phases": rows},
                                      sort_keys=False), encoding="utf-8", newline="\n")
    lane = "p5-" + uuid.uuid4().hex[:10]
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{lane}" / "r1"
    round_dir.mkdir(parents=True)
    if push_state == "matching":
        push = {"sha": _git(repo, "rev-parse", "HEAD").strip()}
        (round_dir / "PUSH.json").write_text(json.dumps(push) + "\n", encoding="utf-8")
    elif push_state == "mismatch":
        (round_dir / "PUSH.json").write_text(json.dumps({"sha": "1" * 40}) + "\n",
                                              encoding="utf-8")
    elif push_state == "malformed":
        (round_dir / "PUSH.json").write_text("{bad json\n", encoding="utf-8")
    elif push_state == "directory":
        (round_dir / "PUSH.json").mkdir()
    env = {"HARNESS_CONTRACT": str(tmp_path / "contract.md")}
    return repo, harness, receipts, lane, round_dir, marker, env


def _run_p5_round(tmp_path, **kwargs):
    repo, harness, receipts, lane, round_dir, marker, env = _p5_round_setup(tmp_path, **kwargs)
    result = _conductor().run_round(
        lane, 1, repo_root=repo, harness=harness, receipts=receipts, env=env
    )
    return result, round_dir, marker, repo


def _assert_real_p5_is_landable():
    phases = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["phases"]
    by_id = {phase["id"]: phase for phase in phases}
    assert "--landable" in by_id["P5"]["command"]
    assert "--require-clean-tree" in by_id["P5"]["command"]
    assert "--landable" in by_id["P6c"]["command"]


def test_item2a_failing_p5_halts_before_p6a_stub_launches(tmp_path):
    _assert_real_p5_is_landable()
    result, _round_dir, marker, _repo = _run_p5_round(
        tmp_path, p5_mode="fail", include_p6a=True
    )

    assert (result.verdict, result.halted_at, result.exit_code) == ("HALTED", "P5", 1)
    assert not marker.exists()


def test_item2b_successful_p5_with_current_head_sha_continues_the_round(tmp_path):
    _assert_real_p5_is_landable()
    result, round_dir, _marker, repo = _run_p5_round(tmp_path)

    assert result.verdict == "ACCEPT"
    assert json.loads((round_dir / "P5-OUTPUT.txt").read_text(encoding="utf-8"))["sha"] == (
        _git(repo, "rev-parse", "HEAD").strip()
    )


@pytest.mark.parametrize(
    ("mode", "push_state", "reason"),
    [
        ("ok", "mismatch", "PUSH.json sha mismatch"),
        ("move-head", "matching", "receipt head_sha mismatch"),
        ("ok", "missing", "missing PUSH.json"),
        ("ok", "malformed", "malformed PUSH.json"),
        ("ok", "directory", "unreadable PUSH.json directory"),
    ],
)
def test_item2b_push_and_p5_receipt_sha_mismatches_refuse(tmp_path, mode, push_state, reason):
    result, _round_dir, _marker, _repo = _run_p5_round(
        tmp_path, p5_mode=mode, push_state=push_state
    )

    assert (result.verdict, result.exit_code, result.refused_by) == (
        "REFUSED", 2, "T2-STALE:P5",
    ), reason


@pytest.mark.parametrize(("mode", "post_mode"), [
    ("wrong-output", "keep"), ("ok", "remove"), ("invalid", "keep"),
])
def test_item2c_wrong_missing_or_unparseable_p5_output_refuses(tmp_path, mode, post_mode):
    result, _round_dir, _marker, _repo = _run_p5_round(
        tmp_path, p5_mode=mode, post_mode=post_mode
    )

    assert (result.verdict, result.exit_code, result.refused_by) == (
        "REFUSED", 2, "T2-STALE:P5",
    )


def test_item2e_toy_p5_not_using_ci_verdict_is_not_sha_checked(tmp_path):
    _assert_real_p5_is_landable()
    result, round_dir, _marker, _repo = _run_p5_round(
        tmp_path, p5_mode="invalid", p5_command_is_ci=False, push_state="missing"
    )

    assert result.verdict == "ACCEPT"
    assert (round_dir / "P5-OUTPUT.txt").is_file()
