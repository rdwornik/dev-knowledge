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
