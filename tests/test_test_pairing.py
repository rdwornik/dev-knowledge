"""lane-l6-test-pairing: which reds are the lane's -- RED-first witnesses for `scripts/test_pairing.py`.

Written BEFORE the module (ADR-108 section B): this file is the frozen pass/fail criterion.

EVERY TEST RUNS AGAINST A SYNTHETIC REPOSITORY built in `tmp_path` -- never the live hub or its
worktrees (the contract's "what NOT to do"). The four scenarios the done-contract names are each
one test: a failing test the second commit adds (attributed), a red present in both
(pre-existing), a passing test that becomes red (attributed), a test that fails once and passes
on rerun (FLAKE). The rest pin the properties the recorded procedure requires: a clone and not a
worktree, the impacted selection and not the full suite, a machine-readable verdict.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import test_pairing  # noqa: E402  -- the module under test; absent until the GREEN commit

_BASE = {
    "pyproject.toml": '[tool.pytest.ini_options]\npythonpath = ["scripts"]\n',
    "scripts/mod.py": "def value():\n    return 1\n",
    "tests/test_mod.py": "import mod\n\n\ndef test_value():\n    assert mod.value() == 1\n",
}


def _git(repo: Path, *args: str) -> str:
    cmd = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
           "-c", "core.hooksPath=", *args]
    done = subprocess.run(cmd, cwd=repo, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def _write(repo: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")


def _commit(repo: Path, files: dict[str, str], message: str) -> str:
    _write(repo, files)
    _git(repo, "add", "-A")
    _git(repo, "commit", "--no-verify", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> tuple[Path, str]:
    """A synthetic repository with one passing test, and the SHA of its base commit."""
    root = tmp_path / "src-repo"
    root.mkdir()
    _git(root, "init", "-b", "main")
    return root, _commit(root, _BASE, "base")


def _run(repo_root: Path, base: str, head: str, tmp_path: Path, *extra: str) -> tuple[int, dict]:
    out = tmp_path / "verdict.json"
    code = test_pairing.main(
        [base, head, "--repo", str(repo_root), "--out", str(out), "--workers", "0", *extra]
    )
    return code, json.loads(out.read_text(encoding="utf-8"))


def _ids(entries) -> list[str]:
    return sorted(e["id"] if isinstance(e, dict) else e for e in entries)


# --- the four scenarios the done-contract names ----------------------------------------------

def test_a_failing_test_the_second_commit_adds_is_the_lanes(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "add a red")

    code, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_new"]
    assert verdict["lane"][0]["was"] == "absent"
    assert verdict["preexisting"] == []
    assert verdict["verdict"] == "LANE-RED"
    assert code == 1


def test_a_red_present_in_both_commits_is_preexisting_not_the_lanes(repo, tmp_path):
    root, _ = repo
    base = _commit(root, {"scripts/old.py": "X = 1\n",
                          "tests/test_old.py": "import old\n\n\ndef test_old():\n    assert False\n"},
                   "a red that predates the lane")
    head = _commit(root, {"scripts/old.py": "X = 2\n"}, "touch the module the red covers")

    code, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["preexisting"]) == ["tests/test_old.py::test_old"]
    assert verdict["lane"] == []
    assert verdict["verdict"] == "CLEAN"
    assert code == 0


def test_a_passing_test_that_becomes_red_is_attributed_and_named_turned_red(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"scripts/mod.py": "def value():\n    return 2\n"}, "break the module")

    code, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["lane"]) == ["tests/test_mod.py::test_value"]
    assert verdict["lane"][0]["was"] == "PASSED"
    assert verdict["turned_red"] == ["tests/test_mod.py::test_value"]
    assert code == 1


def test_a_test_that_fails_once_and_passes_on_rerun_is_a_flake_not_the_lanes(repo, tmp_path,
                                                                            monkeypatch):
    root, base = repo
    counter = tmp_path / "flaky-counter.txt"  # outside every clone, so the rerun sees the first run
    monkeypatch.setenv("PAIRING_FLAKE_COUNTER", str(counter))
    flaky = (
        "import os\nfrom pathlib import Path\n\n\ndef test_flaky():\n"
        "    p = Path(os.environ['PAIRING_FLAKE_COUNTER'])\n"
        "    n = int(p.read_text()) if p.exists() else 0\n"
        "    p.write_text(str(n + 1))\n"
        "    assert n >= 1\n"
    )
    head = _commit(root, {"tests/test_flaky.py": flaky}, "add a test that is red only once")

    code, verdict = _run(root, base, head, tmp_path)

    assert verdict["lane"] == []
    assert len(verdict["flakes"]) == 1
    flake = verdict["flakes"][0]
    assert flake["id"] == "tests/test_flaky.py::test_flaky"
    assert flake["observations"] == ["FAILED", "PASSED"], "both observations are recorded"
    assert verdict["verdict"] == "CLEAN"
    assert code == 0


def test_a_red_that_stays_red_on_rerun_keeps_both_observations(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "add a red")

    _, verdict = _run(root, base, head, tmp_path)

    assert verdict["lane"][0]["observations"] == ["FAILED", "FAILED"]
    assert verdict["flakes"] == []


# --- the recorded procedure ----------------------------------------------------------------

def test_isolation_is_a_clone_and_never_the_source_tree_or_a_new_worktree(repo, tmp_path,
                                                                        monkeypatch):
    root, base = repo
    cwd_log = tmp_path / "cwd.log"
    monkeypatch.setenv("PAIRING_CWD_LOG", str(cwd_log))
    probe = (
        "import os\nfrom pathlib import Path\n\n\ndef test_probe():\n"
        "    with open(os.environ['PAIRING_CWD_LOG'], 'a') as f:\n"
        "        f.write(str(Path.cwd()) + '\\n')\n"
    )
    head = _commit(root, {"tests/test_probe.py": probe}, "probe where tests run")
    worktrees_before = _git(root, "worktree", "list")

    _, verdict = _run(root, base, head, tmp_path)

    ran_in = {Path(line) for line in cwd_log.read_text().split()}
    assert ran_in, "the probe test never ran"
    assert root.resolve() not in {p.resolve() for p in ran_in}, "ran in the source tree"
    assert all(not p.exists() for p in ran_in), "the clones were left behind"
    assert _git(root, "worktree", "list") == worktrees_before, "a worktree was added to the source"
    assert verdict["isolation"] == "clone"


def test_the_module_states_in_one_line_why_a_clone_and_not_a_worktree():
    reason = test_pairing.ISOLATION_REASON
    assert "\n" not in reason
    assert "worktree list" in reason


def test_a_failed_run_still_removes_its_clones(repo, tmp_path, monkeypatch):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    made: list[Path] = []
    real = test_pairing.make_clone

    def spy(*args, **kwargs):
        path = real(*args, **kwargs)
        made.append(path)
        return path

    monkeypatch.setattr(test_pairing, "make_clone", spy)

    def boom(*args, **kwargs):
        raise test_pairing.PairingError("boom")

    monkeypatch.setattr(test_pairing, "run_pytest", boom)
    with pytest.raises(SystemExit) as exc:
        test_pairing.main([base, head, "--repo", str(root),
                           "--out", str(tmp_path / "v.json"), "--workers", "0"])
    assert exc.value.code == 2
    assert made, "no clone was made, so the cleanup was not exercised"
    assert all(not p.exists() for p in made)


# --- the impacted selection, not the full suite --------------------------------------------

def test_the_impacted_selection_runs_only_the_covering_tests(repo, tmp_path):
    root, base = repo
    _commit(root, {"scripts/other.py": "Y = 1\n",
                   "tests/test_other.py": "def test_other():\n    assert False\n"}, "unrelated red")
    base = _git(root, "rev-parse", "HEAD")
    head = _commit(root, {"scripts/mod.py": "def value():\n    return 1\n# touched\n"}, "touch mod")

    _, verdict = _run(root, base, head, tmp_path)

    sel = verdict["selection"]
    assert sel["declined"] is False
    assert sel["test_files"] == ["tests/test_mod.py"]
    assert verdict["preexisting"] == [], "the unrelated red was not selected, so was not run"


def test_a_selection_that_declines_to_narrow_says_so_and_never_runs_everything(repo, tmp_path):
    root, base = repo
    _commit(root, {"scripts/other.py": "Y = 1\n",
                   "tests/test_other.py": "def test_other():\n    assert False\n"}, "unrelated red")
    base = _git(root, "rev-parse", "HEAD")
    head = _commit(root, {"pyproject.toml": _BASE["pyproject.toml"] + "# env change\n",
                          "tests/test_new.py": "def test_new():\n    assert False\n"}, "env change")

    code, verdict = _run(root, base, head, tmp_path)

    sel = verdict["selection"]
    assert sel["declined"] is True
    assert sel["ran_full_suite"] is False
    assert "declined" in sel["note"]
    assert sel["test_files"] == ["tests/test_new.py"], "only the changed test files, never the suite"
    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_new"]
    assert verdict["preexisting"] == [], "test_other.py was not run"
    assert code == 1


def test_a_declined_selection_with_nothing_to_fall_back_on_is_not_evaluated(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"pyproject.toml": _BASE["pyproject.toml"] + "# env change\n"}, "env")

    code, verdict = _run(root, base, head, tmp_path)

    assert verdict["verdict"] == "NOT-EVALUATED"
    assert verdict["selection"]["declined"] is True
    assert code == 3, "a verdict that evaluated nothing must not read as a pass"


# --- machine-readable surface --------------------------------------------------------------

def test_the_verdict_artifact_carries_the_three_sets_and_the_commits(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "red")

    _, verdict = _run(root, base, head, tmp_path)

    assert verdict["schema"] == "test-pairing/1"
    assert verdict["base"] == base and verdict["head"] == head
    for key in ("preexisting", "lane", "turned_red", "flakes", "fixed", "selection", "counts"):
        assert key in verdict


def test_lane_mode_pairs_the_merge_base_against_the_lane_branch(repo, tmp_path):
    root, base = repo
    _git(root, "checkout", "-b", "worktree-demo")
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "lane work")
    _git(root, "checkout", "main")
    _commit(root, {"README.md": "main moved on\n"}, "main advances")
    out = tmp_path / "v.json"

    code = test_pairing.main(["--lane", "demo", "--repo", str(root), "--out", str(out),
                              "--workers", "0"])

    verdict = json.loads(out.read_text(encoding="utf-8"))
    assert verdict["base"] == base, "the base is the merge-base, not main's tip"
    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_new"]
    assert code == 1


def test_the_default_verdict_path_honours_the_receipts_home(repo, tmp_path, monkeypatch):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    home = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(home))

    code = test_pairing.main([base, head, "--repo", str(root), "--workers", "0"])

    assert code == 0
    assert json.loads((home / "TEST-PAIRING-VERDICT.json").read_text(encoding="utf-8"))["schema"]


def test_results_come_from_exact_node_ids_not_from_a_parsed_summary(tmp_path):
    events = tmp_path / "events.jsonl"
    rows = [
        {"id": "tests/test_a.py::test_ok", "when": "call", "outcome": "passed"},
        {"id": "tests/test_a.py::test_bad", "when": "call", "outcome": "failed"},
        {"id": "tests/test_b.py::test_p[a] - [b]", "when": "call", "outcome": "failed"},
        {"id": "tests/test_c.py", "when": "collect", "outcome": "failed"},
        {"id": "tests/test_d.py::test_fx", "when": "setup", "outcome": "failed"},
        {"id": "tests/test_e.py::test_skip", "when": "setup", "outcome": "skipped"},
        {"id": "tests/test_f.py::test_td", "when": "call", "outcome": "passed"},
        {"id": "tests/test_f.py::test_td", "when": "teardown", "outcome": "failed"},
    ]
    events.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

    parsed = test_pairing.read_events(events)

    assert parsed == {
        "tests/test_a.py::test_ok": "PASSED",
        "tests/test_a.py::test_bad": "FAILED",
        "tests/test_b.py::test_p[a] - [b]": "FAILED",
        "tests/test_c.py": "ERROR",
        "tests/test_d.py::test_fx": "ERROR",
        "tests/test_f.py::test_td": "ERROR",
    }


# --- the codex terra review's five HIGH findings -----------------------------------------------

def test_a_transient_baseline_red_does_not_mask_a_lane_red_as_preexisting(repo, tmp_path,
                                                                        monkeypatch):
    root, _ = repo
    counter = tmp_path / "base-counter.txt"
    monkeypatch.setenv("PAIRING_FLAKE_COUNTER", str(counter))
    flaky = (
        "import os\nfrom pathlib import Path\n\n\ndef test_shared():\n"
        "    p = Path(os.environ['PAIRING_FLAKE_COUNTER'])\n"
        "    n = int(p.read_text()) if p.exists() else 0\n"
        "    p.write_text(str(n + 1))\n"
        "    assert n >= 1\n"
    )
    base = _commit(root, {"tests/test_shared.py": flaky}, "a baseline red that is only transient")
    head = _commit(root, {"tests/test_shared.py": "def test_shared():\n    assert False\n"},
                   "the lane makes it really fail")

    code, verdict = _run(root, base, head, tmp_path)

    assert verdict["preexisting"] == [], "a red that passes on a base rerun was never pre-existing"
    assert _ids(verdict["lane"]) == ["tests/test_shared.py::test_shared"]
    assert verdict["lane"][0]["was"] == "red-once-on-base"
    assert verdict["baseline_confirmed"] is True
    assert code == 1


def test_a_stable_baseline_red_is_still_preexisting_after_confirmation(repo, tmp_path):
    root, _ = repo
    base = _commit(root, {"scripts/old.py": "X = 1\n",
                          "tests/test_old.py": "import old\n\n\ndef test_old():\n    assert False\n"},
                   "a stable red")
    head = _commit(root, {"scripts/old.py": "X = 2\n"}, "touch")

    code, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["preexisting"]) == ["tests/test_old.py::test_old"]
    assert verdict["baseline_confirmed"] is True and code == 0


def test_the_baseline_confirmation_can_be_skipped_and_the_verdict_says_so(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")

    _, verdict = _run(root, base, head, tmp_path, "--no-confirm-baseline")

    assert verdict["baseline_confirmed"] is False


def test_a_parametrised_id_with_unmatched_brackets_is_recorded_exactly(repo, tmp_path):
    root, base = repo
    odd = ("import pytest\n\n\n@pytest.mark.parametrize('x', ['a] - [b'])\n"
           "def test_odd(x):\n    assert False\n")
    head = _commit(root, {"tests/test_odd.py": odd}, "an id that defeats a bracket count")

    _, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["lane"]) == ["tests/test_odd.py::test_odd[a] - [b]"]
    assert verdict["lane"][0]["observations"] == ["FAILED", "FAILED"], "the rerun target was exact"


def test_a_collection_error_records_ERROR_as_its_first_observation(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_broken.py": "import no_such_module_xyz\n"}, "cannot import")

    _, verdict = _run(root, base, head, tmp_path)

    assert _ids(verdict["lane"]) == ["tests/test_broken.py"]
    assert verdict["lane"][0]["observations"] == ["ERROR", "ERROR"]


def test_zero_reruns_is_refused_because_it_would_disable_the_flake_rule(repo, tmp_path):
    root, base = repo
    with pytest.raises(SystemExit) as exc:
        test_pairing.main([base, base, "--repo", str(root), "--reruns", "0",
                           "--out", str(tmp_path / "v.json")])
    assert exc.value.code == 2


def test_a_leftover_clone_is_a_non_zero_exit_even_when_the_pairing_is_clean(repo, tmp_path,
                                                                          monkeypatch):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    leaked: list[Path] = []
    real = test_pairing.remove_tree

    def fake(path):
        leaked.append(path)
        return False

    monkeypatch.setattr(test_pairing, "remove_tree", fake)
    try:
        code, verdict = _run(root, base, head, tmp_path)
    finally:
        for p in leaked:
            real(p)

    assert verdict["verdict"] == "CLEAN"
    assert verdict["cleanup"].startswith("LEFTOVER")
    assert code == 2


def test_parsing_and_isolation_use_only_the_standard_library():
    tree = ast.parse((_SCRIPTS / "test_pairing.py").read_text(encoding="utf-8"))
    allowed = set(sys.stdlib_module_names) | {"impacted_tests"}
    seen: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            seen.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            seen.add(node.module.split(".")[0])
    assert seen - allowed == set(), f"non-stdlib imports: {sorted(seen - allowed)}"


def test_no_option_can_run_the_full_suite():
    assert "--full" not in (_SCRIPTS / "test_pairing.py").read_text(encoding="utf-8")
