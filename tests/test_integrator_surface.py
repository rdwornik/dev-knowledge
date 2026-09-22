"""lane-l4-integrator-surface: the merge calls its organs, and the gates become one list.

RED-FIRST (ADR-108 section B, DECLARE-NIGHT N2): authored and witnessed FAILING before
`scripts/gates.py`, the `review_packet.py` merge range and the `lane-integrate.md` rewrite existed;
the RED output is quoted in the RED commit body.

Every test that touches git builds a SYNTHETIC repository under `tmp_path` -- no real branch is
merged, and nothing here writes into the checkout's own `logs/`. The moment test drives a real
`doit` subprocess against a harness derived from the REAL `moments.merge` declaration, so the
rows that run are the rows the repo declares, with only test-plumbing flags spliced in.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_DODO = _SCRIPTS / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_COMMAND = _REPO / ".claude" / "commands" / "lane-integrate.md"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-l4-fixture"


# --- helpers ------------------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t",
                          "-c", "commit.gpgsign=false", *args],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _synthetic_merge(tmp: Path) -> tuple[Path, str]:
    """main + a lane branch + a `--no-ff` merge of it. Returns (repo, merge sha)."""
    repo = tmp / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / "base.txt").write_text("base\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "checkout", "-q", "-b", f"worktree-{LANE}")
    (repo / "lane-a.txt").write_text("a\n", encoding="utf-8")
    (repo / "lane-b.txt").write_text("b\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "lane work")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "-m", "merge the lane", f"worktree-{LANE}")
    return repo, _git(repo, "rev-parse", "HEAD")


_CONTRACT = """# LANE fixture

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Done-contract (immutable)

1. `lane-a.txt` exists.
2. `lane-b.txt` exists.

**Files you own:** `lane-a.txt`, `lane-b.txt`.
"""


# --- clause 3: the review range comes from the merge itself -------------------------------------

def test_the_old_range_is_empty_after_the_merge_and_the_merge_range_is_not(tmp_path):
    """WHY the old range was empty: after `git merge --no-ff`, main already contains the branch,
    so `main..worktree-<lane>` selects no commit at all -- it is empty BY CONSTRUCTION. The merge
    commit against its first parent still holds exactly what the merge brought in."""
    import review_packet as rp

    repo, merge = _synthetic_merge(tmp_path)
    old = _git(repo, "rev-list", f"main..worktree-{LANE}")
    assert old == "", "the old formulation must be empty once the branch is merged"
    assert _git(repo, "diff", "--name-only", f"main..worktree-{LANE}") == ""

    rng = rp.merge_range(repo, merge)
    assert rng == f"{merge}^1..{merge}"
    assert _git(repo, "rev-list", rng), "the merge range selected no commit"
    assert rp.changed_in_merge(repo, merge) == ("lane-a.txt", "lane-b.txt")


def test_merge_range_refuses_a_commit_that_is_not_a_merge(tmp_path):
    import review_packet as rp

    repo, merge = _synthetic_merge(tmp_path)
    plain = _git(repo, "rev-parse", f"{merge}^1")
    with pytest.raises(rp.PacketIncomplete):
        rp.merge_range(repo, plain)


def test_the_cli_turns_an_empty_post_merge_range_into_the_merge_range(tmp_path):
    """The declared organ still passes `--range main..worktree-<lane>`. Run after the merge that
    range is empty, so the CLI must resolve the lane's merge commit itself rather than render a
    packet against nothing -- and the packet it writes names the MERGE range."""
    repo, merge = _synthetic_merge(tmp_path)
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    out = tmp_path / "packet.md"
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "review_packet.py"), "--repo", str(repo), "--lane", LANE,
         "--contract", str(contract), "--range", f"main..worktree-{LANE}",
         "--handback", "HANDBACK x @ y code review=codex HIGH:0 MED:0 LOW:0",
         "--changed", "lane-a.txt", "--changed", "lane-b.txt", "--out", str(out)],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = out.read_text(encoding="utf-8")
    assert f"{merge}^1..{merge}" in text
    assert f"main..worktree-{LANE}" not in text


def test_a_merge_range_reads_the_file_list_off_the_merge_not_off_the_caller(tmp_path):
    """The declared organ hands `--changed <one placeholder>`. After a merge the change IS the merge
    commit, so a caller-supplied list -- necessarily an abbreviation of it -- is not trusted."""
    repo, merge = _synthetic_merge(tmp_path)
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    out = tmp_path / "packet.md"
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "review_packet.py"), "--repo", str(repo), "--lane", LANE,
         "--contract", str(contract), "--range", f"main..worktree-{LANE}",
         "--handback", "HANDBACK x @ y code review=codex HIGH:0 MED:0 LOW:0",
         "--changed", "lane-a.txt", "--out", str(out)],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "Files actually changed (2)" in text and "lane-b.txt" in text


def test_the_cli_derives_the_changed_files_from_an_explicit_merge(tmp_path):
    repo, merge = _synthetic_merge(tmp_path)
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    out = tmp_path / "packet.md"
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "review_packet.py"), "--repo", str(repo), "--lane", LANE,
         "--contract", str(contract), "--merge", merge,
         "--handback", "HANDBACK x @ y code review=codex HIGH:0 MED:0 LOW:0", "--out", str(out)],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "Files actually changed (2)" in text and "lane-a.txt" in text and "lane-b.txt" in text


def test_an_empty_range_with_no_merge_to_find_is_refused_not_rendered(tmp_path):
    """A lane branch that was never merged and has no commits of its own is an empty range with
    nothing to resolve to: refuse, do not write an empty packet."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "branch", f"worktree-{LANE}")
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "review_packet.py"), "--repo", str(repo), "--lane", LANE,
         "--contract", str(contract), "--range", f"main..worktree-{LANE}", "--handback", "HANDBACK",
         "--changed", "f.txt", "--out", str(tmp_path / "p.md")],
        capture_output=True, text=True)
    assert proc.returncode != 0
    assert "empty" in (proc.stdout + proc.stderr).lower(), proc.stdout + proc.stderr
    assert not (tmp_path / "p.md").exists()


# --- clause 4 + 5d/5e: gates.py -----------------------------------------------------------------

def _marker_gate(gates, name: str, marker: Path, code: int = 0):
    src = f"open(r'{marker}', 'a').write('x'); raise SystemExit({code})"
    return gates.Gate(name=name, argv=(sys.executable, "-c", src))


def test_a_red_gate_is_reported_red_and_the_run_exits_nonzero(tmp_path):
    import gates

    listing = (_marker_gate(gates, "green-one", tmp_path / "g1"),
               _marker_gate(gates, "red-one", tmp_path / "r1", code=3),
               _marker_gate(gates, "green-two", tmp_path / "g2"))
    verdict = gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    by_name = {g["name"]: g for g in verdict["gates"]}
    assert by_name["red-one"]["exit_code"] == 3
    assert by_name["green-one"]["exit_code"] == 0 and by_name["green-two"]["exit_code"] == 0
    assert verdict["verdict"] == "RED"
    assert gates.exit_code_for(verdict) != 0
    # a red gate does not hide the gates after it: the artifact is complete
    assert (tmp_path / "g2").exists()


def test_a_gate_that_cannot_start_is_red_not_swallowed(tmp_path):
    import gates

    listing = (gates.Gate(name="ghost", argv=("definitely-not-a-real-program-l4",)),)
    verdict = gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    assert verdict["verdict"] == "RED"
    assert verdict["gates"][0]["exit_code"] != 0
    assert verdict["gates"][0]["exit_code"] is not None


def test_an_all_green_list_is_green_and_exits_zero(tmp_path):
    import gates

    listing = (_marker_gate(gates, "a", tmp_path / "a"), _marker_gate(gates, "b", tmp_path / "b"))
    verdict = gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    assert verdict["verdict"] == "GREEN"
    assert gates.exit_code_for(verdict) == 0


def test_each_declared_gate_runs_exactly_once(tmp_path):
    import gates

    markers = [tmp_path / f"m{i}" for i in range(4)]
    listing = tuple(_marker_gate(gates, f"gate-{i}", m) for i, m in enumerate(markers))
    gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    assert [m.read_text() for m in markers] == ["x", "x", "x", "x"], \
        "every gate must have run once and only once"


def test_the_verdict_artifact_names_each_gate_its_exit_code_and_duration(tmp_path):
    import gates

    listing = (_marker_gate(gates, "one", tmp_path / "o"),
               _marker_gate(gates, "two", tmp_path / "t", code=1))
    out = tmp_path / "VERDICT.json"
    verdict = gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    gates.write_verdict(verdict, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["lane"] == LANE and data["verdict"] == "RED"
    assert [g["name"] for g in data["gates"]] == ["one", "two"]
    for gate in data["gates"]:
        assert isinstance(gate["exit_code"], int)
        assert isinstance(gate["duration_ms"], int) and gate["duration_ms"] >= 0


def test_the_cli_writes_the_artifact_and_exits_with_the_verdict(tmp_path, monkeypatch):
    import gates
    from click.testing import CliRunner

    monkeypatch.setattr(gates, "GATES", (_marker_gate(gates, "bad", tmp_path / "b", code=2),))
    out = tmp_path / "V.json"
    result = CliRunner().invoke(gates.cli, ["run", "--lane", LANE, "--out", str(out)])
    assert result.exit_code != 0, result.output
    assert json.loads(out.read_text(encoding="utf-8"))["verdict"] == "RED"
    assert "bad" in result.output


def test_the_declared_list_composes_what_exists_and_holds_no_full_suite():
    """The list is audit, ship-gate, ruff and the impacted tests -- composed from organs that
    exist. The FULL suite is CI's; a gate whose argv runs bare `pytest` would put it back."""
    import gates

    names = [g.name for g in gates.GATES]
    assert names == ["audit-health", "ship-gate", "ruff", "impacted-tests"]
    flat = {g.name: " ".join(map(str, g.argv)) for g in gates.GATES if g.argv}
    assert "audit.py health" in flat["audit-health"]
    assert "audit.py ship-gate" in flat["ship-gate"]
    assert "ruff check" in flat["ruff"]
    for name, cmd in flat.items():
        assert not re.search(r"\bpytest\b", cmd), f"{name} runs pytest directly"
    impacted = next(g for g in gates.GATES if g.name == "impacted-tests")
    assert impacted.runner is not None, "impacted tests are select-then-run, not one argv"


def test_a_selector_that_declines_to_narrow_is_red_not_a_silent_full_suite(tmp_path, monkeypatch):
    import gates

    monkeypatch.setattr(gates, "_select_impacted",
                        lambda cwd, base: (0, "# FULL SUITE -- the selector declined to narrow"))
    ran: list[list[str]] = []
    monkeypatch.setattr(gates, "_run_pytest", lambda cwd, args: ran.append(args) or (0, ""))
    code, text = gates.impacted_tests_gate(tmp_path, base="HEAD^1")
    assert code != 0 and "declined to narrow" in text
    assert ran == [], "the gate must not fall back to running the full suite"


def test_impacted_tests_runs_only_the_selected_files(tmp_path, monkeypatch):
    import gates

    monkeypatch.setattr(gates, "_select_impacted",
                        lambda cwd, base: (0, "tests/test_a.py tests/test_b.py"))
    ran: list[list[str]] = []
    monkeypatch.setattr(gates, "_run_pytest", lambda cwd, args: ran.append(args) or (0, "ok"))
    code, _ = gates.impacted_tests_gate(tmp_path, base="HEAD^1")
    assert code == 0 and ran == [["tests/test_a.py", "tests/test_b.py"]]


# --- clause 1: the integrator command calls the declaration -------------------------------------

def _command_text() -> str:
    return _COMMAND.read_text(encoding="utf-8")


def test_the_integrator_calls_the_merge_moment_after_the_local_merge_and_teardown_after_push():
    text = _walk_block()  # the executable block, not the prose around it
    merge = text.index("git merge --no-ff")
    moment_merge = text.index("moment:merge")
    push = text.index("git push", moment_merge)
    remove = text.index("git worktree remove", push)
    moment_teardown = text.index("moment:teardown", remove)
    assert merge < moment_merge < push < remove < moment_teardown, (
        "order must be: merge locally, moment:merge (verify), push, remove, moment:teardown")


def test_the_command_no_longer_lists_the_moment_organs_as_prose_steps():
    """The organs run through the declaration; a hand-typed `review_packet.py` invocation in the
    per-lane block is the prose the declaration replaces."""
    text = _command_text()
    walk = text[text.index("## 2. Walk the queue"):text.index("## 3. The refuse-to-finish")]
    assert "scripts/review_packet.py" not in walk
    assert "merge_receipt.py models" not in walk


def test_the_command_says_why_the_old_range_was_empty():
    text = _command_text()
    assert "empty by construction" in text


# --- clause 1/2/5a/5b: the merge moment runs the comparator and the gates ------------------------

def _declared_merge_organs() -> dict[str, dict]:
    doc = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))
    moment = next(m for m in doc["moments"] if m["name"] == "merge")
    return {o["id"]: o for o in moment["organs"]}


def test_the_real_declaration_names_the_comparator_and_the_gate_list_at_the_merge_moment():
    organs = _declared_merge_organs()
    assert "merge_receipt.py" in " ".join(map(str, organs["merge_receipt.models"]["command"]))
    assert "models" in organs["merge_receipt.models"]["command"]
    gates_cmd = list(map(str, organs["gates"]["command"]))
    assert "scripts/gates.py" in gates_cmd and "run" in gates_cmd
    # the order the moment runs them in: the comparator first, so a disagreement refuses before
    # anything else is spent
    ids = list(organs)
    assert ids.index("merge_receipt.models") < ids.index("gates")


def _splice(command: list, script: str, extra: list[str]) -> list[str]:
    """The REAL declared command with test-plumbing flags placed right after the script name."""
    argv = [str(t) for t in command]
    at = next(i for i, t in enumerate(argv) if t.endswith(script))
    return argv[:at + 1] + extra + argv[at + 1:]


def _merge_moment_harness(tmp: Path, repo: Path, tree: Path, gate_list: Path) -> Path:
    organs = _declared_merge_organs()
    rows = []
    for organ_id, script, extra in (
            ("merge_receipt.models", "merge_receipt.py", ["--repo-root", str(repo)]),
            ("gates", "gates.py", [])):
        row = dict(organs[organ_id])
        command = _splice(row["command"], script, extra)
        if organ_id == "merge_receipt.models":
            command += ["--worktree", str(tree)]
        else:
            command += ["--gate-list", str(gate_list)]
        row["command"] = command
        rows.append(row)
    doc = {"stages": [{"stage": 1, "name": "s", "field": "f", "kind": "deterministic",
                       "command": [sys.executable, "-c", "pass"]}],
           "moments": [{"name": "merge", "trigger": "test", "organs": rows}]}
    path = tmp / "harness.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def _seed(tmp: Path, ran_model: str, *, pre_open: bool = True) -> tuple[Path, Path, Path, Path, dict]:
    import routing_agreement as ra

    repo = tmp / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    tree = tmp / "tree"
    tree.mkdir()
    home = tmp / "home"
    store = home / ".claude" / "projects" / ra.session_slug(tree)
    store.mkdir(parents=True)
    lines = [json.dumps({"type": "assistant", "message": {"model": ran_model}}) for _ in range(3)]
    (store / "s.jsonl").write_text("\n".join(lines), encoding="utf-8")
    contract = tmp / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    gate_list = tmp / "gates.json"
    marker = tmp / "gate-ran.txt"
    gate_list.write_text(json.dumps([{"name": "probe", "argv": [
        sys.executable, "-c", f"open(r'{marker}', 'a').write('x')"]}]), encoding="utf-8")
    env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home),
           "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": "x", "HARNESS_LANE": LANE, "HARNESS_BATCH": "x",
           "HARNESS_CONTRACT": str(contract),
           "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")}
    env.pop("HARNESS_YAML", None)
    if pre_open:
        # The integrator's own `merge_receipt.py open` (lane-integrate.md §2, before the handback
        # verdict) -- most fixtures want this already done, the way the walk always does it. The
        # one that does NOT (`pre_open=False`) is testing the OTHER caller: `doit moment:merge` on
        # its own, which is what the declared `merge_receipt.open` organ (R-W4-4) is for.
        opened = subprocess.run(
            [sys.executable, str(_SCRIPTS / "merge_receipt.py"), "--repo-root", str(repo), "open",
             "--slug", LANE, "--batch", "x"], capture_output=True, text=True, env=env)
        assert opened.returncode == 0, opened.stdout + opened.stderr
    return repo, tree, contract, gate_list, env


def _run_moment(tmp: Path, harness: Path, env: dict) -> subprocess.CompletedProcess:
    env = {**env, "HARNESS_YAML": str(harness)}
    return subprocess.run(
        [sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(tmp), "--db-file",
         str(tmp / ".doit.db"), "moment:merge"],
        capture_output=True, text=True, env=env, cwd=tmp, timeout=300)


def _receipt(tmp: Path, name: str) -> dict:
    return json.loads((tmp / "receipts" / name).read_text(encoding="utf-8"))


def test_the_merge_moment_runs_the_comparator_and_the_gate_list_proven_from_the_receipts(tmp_path):
    repo, tree, _contract, gate_list, env = _seed(tmp_path, "claude-sonnet-5")
    harness = _merge_moment_harness(tmp_path, repo, tree, gate_list)
    proc = _run_moment(tmp_path, harness, env)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    models = _receipt(tmp_path, "MOMENT-MERGE-MODELS.json")
    assert models["organ"] == "merge/merge_receipt.models"
    assert models["status"] == "ok" and models["exit_code"] == 0
    assert "merge_receipt.py" in " ".join(models["command"])

    gate = _receipt(tmp_path, "MOMENT-MERGE-GATES.json")
    assert gate["organ"] == "merge/gates" and gate["status"] == "ok" and gate["exit_code"] == 0
    assert (tmp_path / "gate-ran.txt").read_text() == "x", "the gate list ran exactly once"


def test_a_disagreeing_model_comparison_refuses_the_merge_step(tmp_path):
    """The lane was ORDERED sonnet and its transcript says opus: the comparator exits non-zero,
    the receipt records the refusal, and the moment stops before the gate list ever runs."""
    repo, tree, _contract, gate_list, env = _seed(tmp_path, "claude-opus-5")
    harness = _merge_moment_harness(tmp_path, repo, tree, gate_list)
    proc = _run_moment(tmp_path, harness, env)
    assert proc.returncode != 0, "a disagreement must refuse the merge step"

    models = _receipt(tmp_path, "MOMENT-MERGE-MODELS.json")
    assert models["exit_code"] != 0 and models["status"] != "ok"
    output = (tmp_path / "receipts" / "MOMENT-MERGE-MODELS-OUTPUT.txt").read_text(encoding="utf-8")
    assert "opus" in output and "sonnet" in output, output  # the divergence itself, named
    assert not (tmp_path / "receipts" / "MOMENT-MERGE-GATES.json").exists(), \
        "the gates ran although the model comparison refused"
    assert not (tmp_path / "gate-ran.txt").exists()


# --- R-W4-4: the declared `merge` moment opens its own receipt before it compares -----------------

def _open_and_models_harness(tmp: Path, repo: Path, tree: Path) -> Path:
    """The REAL declared `merge_receipt.open` and `merge_receipt.models` organs, in the REAL
    declared order, with test-plumbing spliced into `models` only -- `open`'s command is the
    declaration's own `-c` snippet, unmodified, redirected entirely through `MERGE_RECEIPT_ROOT`
    (its own test seam, since a `-c` argument has no `scripts/merge_receipt.py` token to splice
    `--repo-root` after)."""
    organs = _declared_merge_organs()
    models = dict(organs["merge_receipt.models"])
    models["command"] = _splice(models["command"], "merge_receipt.py", ["--repo-root", str(repo)])
    models["command"] += ["--worktree", str(tree)]
    doc = {"stages": [{"stage": 1, "name": "s", "field": "f", "kind": "deterministic",
                       "command": [sys.executable, "-c", "pass"]}],
           "moments": [{"name": "merge", "trigger": "test",
                       "organs": [dict(organs["merge_receipt.open"]), models]}]}
    path = tmp / "harness-open.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def test_the_declared_open_organ_lets_a_moment_only_caller_reach_models(tmp_path):
    """R-W4-4: `merge_receipt.open` is the merge moment's FIRST declared organ so a caller that
    runs ONLY `doit moment:merge` -- no prior `merge_receipt.py open`, unlike the integrator's own
    walk -- still reaches `models` with an open receipt instead of stopping on 'no open receipt'.
    `pre_open=False` is the whole point: this is the moment-only caller the connection test named.
    """
    repo, tree, _contract, _gate_list, env = _seed(tmp_path, "claude-sonnet-5", pre_open=False)
    assert not (repo / "logs" / f".merge-receipt-{LANE}.json").exists(), \
        "the positive control: nothing opened this receipt yet"
    harness = _open_and_models_harness(tmp_path, repo, tree)
    env = {**env, "MERGE_RECEIPT_ROOT": str(repo)}
    proc = _run_moment(tmp_path, harness, env)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    opened = _receipt(tmp_path, "MOMENT-MERGE-OPEN.json")
    assert opened["organ"] == "merge/merge_receipt.open" and opened["status"] == "ok"
    models = _receipt(tmp_path, "MOMENT-MERGE-MODELS.json")
    assert models["organ"] == "merge/merge_receipt.models"
    assert models["status"] == "ok" and models["exit_code"] == 0


def test_the_declared_open_organ_is_a_no_op_when_the_integrator_already_opened(tmp_path):
    """The full lane-integrate.md walk opens the receipt itself, well before `doit moment:merge`
    (§2, before the handback verdict). The declared organ must not then refuse a second open of
    the SAME slug -- it is `scratch_path(...).exists()` first, `open_receipt` only when that is
    false, so the ordinary walk (`pre_open=True`, the default) is unaffected by this lane's fix."""
    repo, tree, _contract, _gate_list, env = _seed(tmp_path, "claude-sonnet-5")  # pre_open=True
    assert (repo / "logs" / f".merge-receipt-{LANE}.json").exists()
    harness = _open_and_models_harness(tmp_path, repo, tree)
    env = {**env, "MERGE_RECEIPT_ROOT": str(repo)}
    proc = _run_moment(tmp_path, harness, env)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _receipt(tmp_path, "MOMENT-MERGE-OPEN.json")["status"] == "ok"


# --- Codex terra review findings: RED-first regressions -------------------------------------------

def _commit_tree(repo: Path, *parents: str, message: str = "synthetic") -> str:
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    args = ["commit-tree", tree]
    for parent in parents:
        args += ["-p", parent]
    return _git(repo, *args, "-m", message)


def test_an_octopus_merge_is_refused_not_rendered_as_a_lane_merge(tmp_path):
    import review_packet as rp

    repo, merge = _synthetic_merge(tmp_path)
    base = _git(repo, "rev-parse", f"{merge}^1")
    lane = _git(repo, "rev-parse", f"{merge}^2")
    third = _commit_tree(repo, base, message="a third, distinct parent")
    octopus = _commit_tree(repo, base, lane, third)
    with pytest.raises(rp.PacketIncomplete):
        rp.merge_range(repo, octopus)


def test_two_merges_of_the_same_tip_are_refused_as_ambiguous(tmp_path):
    import review_packet as rp

    repo, merge = _synthetic_merge(tmp_path)
    lane = _git(repo, "rev-parse", f"{merge}^2")
    again = _commit_tree(repo, merge, lane)
    _git(repo, "reset", "-q", "--hard", again)
    with pytest.raises(rp.PacketIncomplete, match="ambiguous|more than one"):
        rp.resolve_range(repo, f"main..worktree-{LANE}")


def test_an_empty_symmetric_range_is_refused_too(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "branch", f"worktree-{LANE}")
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8", newline="\n")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "review_packet.py"), "--repo", str(repo), "--lane", LANE,
         "--contract", str(contract), "--range", f"main...worktree-{LANE}", "--handback", "HANDBACK",
         "--changed", "f.txt", "--out", str(tmp_path / "p.md")],
        capture_output=True, text=True)
    assert proc.returncode != 0
    assert "empty" in (proc.stdout + proc.stderr).lower(), proc.stdout + proc.stderr
    assert not (tmp_path / "p.md").exists()


def test_a_runner_that_calls_sys_exit_is_a_red_gate_not_a_green_process(tmp_path):
    import gates

    def bad(_cwd, _base):
        raise SystemExit(0)

    marker = tmp_path / "after"
    listing = (gates.Gate(name="exits", runner=bad), _marker_gate(gates, "after", marker))
    verdict = gates.run_gates(listing, lane=LANE, cwd=tmp_path)
    assert verdict["verdict"] == "RED" and "exits" in verdict["red"]
    assert marker.exists(), "the gates after the one that exited must still run"


def _walk_block() -> str:
    """The per-lane bash block of the integrator command, placeholders made syntactically valid."""
    blocks = re.findall(r"```bash\n(.*?)```", _command_text(), flags=re.S)
    block = next(b for b in blocks if "moment:merge" in b and "git push" in b)
    return block.replace("<n>", "1")


def _run_walk(tmp: Path, fail_on: str) -> list[str]:
    """Run the REAL block under bash with `uv` and `git` stubbed onto PATH; return every call made."""
    import shutil

    bash = shutil.which("bash")
    assert bash, "bash is required to execute the integrator's command block"
    bindir = tmp / "bin"
    bindir.mkdir()
    log = tmp / "calls.log"
    (bindir / "git").write_text(
        '#!/bin/sh\necho "git $*" >> "$CALLS"\n[ "$1" = "rev-parse" ] && echo deadbeef\nexit 0\n',
        encoding="utf-8", newline="\n")
    (bindir / "uv").write_text(
        '#!/bin/sh\necho "uv $*" >> "$CALLS"\n'
        'if [ -n "$FAIL_ON" ]; then case "$*" in *"$FAIL_ON"*) exit 1;; esac; fi\nexit 0\n',
        encoding="utf-8", newline="\n")
    env = {**os.environ, "CALLS": str(log), "FAIL_ON": fail_on,
           "PATH": str(bindir) + os.pathsep + os.environ["PATH"]}
    subprocess.run([bash, "-c", _walk_block()], env=env, capture_output=True, text=True, cwd=tmp)
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def test_the_walk_reaches_push_when_every_verification_passes(tmp_path):
    """POSITIVE CONTROL: without it the refusals below would pass on a block that never runs."""
    calls = _run_walk(tmp_path, fail_on="")
    assert any(c.startswith("git push") for c in calls), calls
    assert any("moment:teardown" in c for c in calls), calls


@pytest.mark.parametrize("failing", ["moment:merge", "race"])
def test_a_refused_verification_never_reaches_push_or_teardown(tmp_path, failing):
    calls = _run_walk(tmp_path, fail_on=failing)
    assert any(failing in c for c in calls), f"the failing step never ran: {calls}"
    assert not any(c.startswith("git push") for c in calls), calls


# --- R-W4-4: the chain order, asserted from the command file's OWN text --------------------------

def test_the_walk_closes_the_receipt_and_commits_the_ledger_before_moment_teardown(tmp_path):
    """The connection test's first recorded stop, pinned: under the OLD order `close` ran after
    `moment:teardown` and `no_leftovers` FAILED on the untracked scratch file. The real block must
    now read: push < actions < close < commit the ledger < moment:teardown."""
    calls = _run_walk(tmp_path, fail_on="")

    def first(needle: str) -> int:
        return next(i for i, c in enumerate(calls) if needle in c)

    push_i = first("git push")
    actions_i = first("merge_receipt.py actions")
    close_i = first("merge_receipt.py close")
    commit_i = first("git commit")
    teardown_i = first("moment:teardown")
    assert push_i < actions_i < close_i < commit_i < teardown_i, calls


def test_the_command_file_text_orders_open_before_the_merge_moment():
    """R-W4-4's other half: `merge_receipt open` before `models`. `models` is not named in this
    file's prose any more (the organs run through the declaration -- see the sibling test above),
    so this is read as `open`'s own explicit command preceding the FIRST mention of `moment:merge`,
    the call that runs it."""
    text = _command_text()
    assert text.index("merge_receipt.py open") < text.index("moment:merge")


@pytest.mark.parametrize("failing", ["actions", "close"])
def test_a_refusal_after_the_push_never_reaches_teardown(tmp_path, failing):
    """A failure that lands AFTER the push (unlike the `moment:merge`/`race` case above, which
    never reaches it) must still stop the chain before `moment:teardown` -- an itemised receipt or
    an unread Actions verdict is exactly the silent case `[#750]`/`[#675]` exist to close."""
    calls = _run_walk(tmp_path, fail_on=failing)
    assert any(c.startswith("git push") for c in calls), calls
    assert any(failing in c for c in calls), f"the failing step never ran: {calls}"
    assert not any("moment:teardown" in c for c in calls), calls
