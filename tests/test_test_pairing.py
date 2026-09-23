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


# --- the second codex terra pass: four HIGH findings against the plugin path -------------------

def test_a_malformed_event_row_fails_closed(tmp_path):
    events = tmp_path / "events.jsonl"
    events.write_text('{"id": "t.py::a", "when": "call", "outcome": "passed"}\n{"id": "t.py::b", "wh\n',
                      encoding="utf-8")
    with pytest.raises(test_pairing.PairingError):
        test_pairing.read_events(events)


def test_a_missing_event_file_fails_closed_rather_than_reading_as_all_green(repo, tmp_path,
                                                                          monkeypatch):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "a real red")
    monkeypatch.setattr(test_pairing, "_PLUGIN", "")  # the reporting plugin does nothing at all

    with pytest.raises(SystemExit) as exc:
        test_pairing.main([base, head, "--repo", str(root), "--out", str(tmp_path / "v.json"),
                           "--workers", "0"])

    assert exc.value.code == 2, "a run that reported nothing must not become a CLEAN verdict"


def test_a_skipped_only_run_is_not_mistaken_for_a_missing_report(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_skip.py":
                          "import pytest\n\n\ndef test_skip():\n    pytest.skip('nope')\n"}, "skips")

    code, verdict = _run(root, base, head, tmp_path)

    assert verdict["verdict"] == "CLEAN" and code == 0


def test_many_workers_lose_no_result(tmp_path):
    clone = tmp_path / "scratch" / "clone"
    (clone / "tests").mkdir(parents=True)
    (clone / "tests" / "test_many.py").write_text(
        "import pytest\n\n\n@pytest.mark.parametrize('n', range(300))\ndef test_n(n):\n    pass\n",
        encoding="utf-8")

    results = test_pairing.run_pytest(clone, ["tests/test_many.py"], workers=3, timeout=None)

    assert len(results) == 300 and set(results.values()) == {"PASSED"}


def test_the_callers_pythonpath_is_not_inherited_by_the_clone_run(repo, tmp_path, monkeypatch):
    root, base = repo
    log = tmp_path / "pythonpath.log"
    monkeypatch.setenv("PAIRING_PP_LOG", str(log))
    monkeypatch.setenv("PYTHONPATH", str(tmp_path / "the-callers-checkout"))
    probe = ("import os\n\n\ndef test_probe():\n"
             "    open(os.environ['PAIRING_PP_LOG'], 'a').write(os.environ.get('PYTHONPATH', '') + '\\n')\n")
    head = _commit(root, {"tests/test_pp.py": probe}, "probe PYTHONPATH")

    _run(root, base, head, tmp_path)

    seen = log.read_text(encoding="utf-8")
    assert "the-callers-checkout" not in seen, "the caller's path can shadow the tree under test"


@pytest.mark.parametrize("target", ["tests", ".", "scripts", "tests/"])
def test_explicit_tests_must_be_files_never_a_directory(repo, tmp_path, target):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    with pytest.raises(SystemExit) as exc:
        test_pairing.main([base, head, "--repo", str(root), "--out", str(tmp_path / "v.json"),
                           "--workers", "0", "--tests", target])
    assert exc.value.code == 2


def test_an_explicit_node_id_is_accepted(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "red")

    code, verdict = _run(root, base, head, tmp_path, "--tests", "tests/test_new.py::test_new")

    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_new"] and code == 1


def test_no_option_can_run_the_full_suite():
    assert "--full" not in (_SCRIPTS / "test_pairing.py").read_text(encoding="utf-8")


# =============================================================================================
# lane-known-reds (W4-1, R-W4-2): the BATCH-LEVEL registry. One base run per batch records main's
# reds and skip count; every lane is then compared against that registry instead of getting a
# fresh base run of its own. Written before the code: this is the frozen pass/fail criterion.
# Synthetic repositories only, receipts home redirected into tmp_path, never the live hub.
# =============================================================================================

_REG_NAME = "TEST-PAIRING-REGISTRY-B1.json"
_RED = "def test_red():\n    assert False\n"
_SKIP = "import pytest\n\n\ndef test_skipped():\n    pytest.skip('env')\n"


@pytest.fixture
def home(tmp_path: Path, monkeypatch) -> Path:
    """The receipts home, redirected: the only place a registry may be created."""
    path = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(path))
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    return path


def _record(root: Path, commit: str, *extra: str) -> int:
    return test_pairing.main(["record-base", "--commit", commit, "--batch", "B1", "--repo", str(root),
                              "--workers", "0", *extra])


def _compare(root: Path, head: str, tmp_path: Path, *extra: str) -> tuple[int, dict]:
    out = tmp_path / "verdict.json"
    code = test_pairing.main(["compare", "--batch", "B1", "--head", head, "--repo", str(root),
                              "--out", str(out), "--workers", "0", *extra])
    return code, json.loads(out.read_text(encoding="utf-8"))


def _registry(home: Path) -> dict:
    return json.loads((home / _REG_NAME).read_text(encoding="utf-8"))


def _spy_clones(monkeypatch) -> list[tuple[str, Path]]:
    made: list[tuple[str, Path]] = []
    real = test_pairing.make_clone

    def spy(repo, sha, dest):
        path = real(repo, sha, dest)
        made.append((sha, path))
        return path

    monkeypatch.setattr(test_pairing, "make_clone", spy)
    return made


def test_record_base_writes_the_red_set_and_the_skip_count_into_the_receipts_home(repo, home):
    root, _ = repo
    base = _commit(root, {"tests/test_red.py": _RED, "tests/test_skip.py": _SKIP}, "main's state")

    code = _record(root, base, "--tests", "tests/test_mod.py", "tests/test_red.py", "tests/test_skip.py")

    assert code == 0
    registry = _registry(home)
    assert registry["schema"] == "test-pairing-registry/1"
    assert registry["batch"] == "B1" and registry["commit"] == base
    assert sorted(registry["red"]) == ["tests/test_red.py::test_red"]
    assert registry["skip_count"] == 1, "the skip count is recorded WITH the red set"
    assert registry["skipped"] == ["tests/test_skip.py::test_skipped"]
    assert registry["files"] == ["tests/test_mod.py", "tests/test_red.py", "tests/test_skip.py"]


def test_the_registry_lives_in_the_cited_receipts_home_undated_and_nowhere_else(repo, home, tmp_path):
    root, base = repo
    before = {p.name for p in tmp_path.iterdir()}

    _record(root, base, "--tests", "tests/test_mod.py")

    assert [p.name for p in home.iterdir()] == [_REG_NAME], "UPPERCASE-KEBAB, no date in the name"
    assert {p.name for p in tmp_path.iterdir()} - before == {"receipts"}, "nothing outside the home"
    doc = test_pairing.__doc__
    assert "RECON-NIGHT-2026-09-20" in doc and "shape (a)" in doc, "the choice is cited in the module"


def test_the_registry_is_written_once_and_reused_by_every_comparison(repo, home, tmp_path,
                                                                    monkeypatch):
    root, _ = repo
    base = _commit(root, {"scripts/old.py": "X = 1\n",
                          "tests/test_old.py": "import old\n\n\ndef test_old():\n    assert False\n"},
                   "a red on main")
    made = _spy_clones(monkeypatch)
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_old.py")
    written = (home / _REG_NAME).read_bytes()
    assert [sha for sha, _ in made] == [base], "the base is run exactly once, at record time"
    lane_a = _commit(root, {"scripts/old.py": "X = 2\n"}, "lane a")
    lane_b = _commit(root, {"scripts/mod.py": "def value():\n    return 1\n# b\n"}, "lane b")
    made.clear()

    code_a, verdict_a = _compare(root, lane_a, tmp_path)
    code_b, verdict_b = _compare(root, lane_b, tmp_path)

    assert (home / _REG_NAME).read_bytes() == written, "a comparison never rewrites the registry"
    assert base not in [sha for sha, _ in made], "no comparison ran the base commit again"
    assert [sha for sha, _ in made] == [lane_a, lane_b], "one clone per comparison: the merged tree"
    assert all(not path.exists() for _, path in made), "no leftovers"
    assert verdict_a["preexisting"] == ["tests/test_old.py::test_old"] and code_a == 0
    assert verdict_b["verdict"] == "CLEAN" and code_b == 0


def test_a_second_record_base_is_refused_because_it_would_launder_a_red_into_the_registry(repo, home):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    written = (home / _REG_NAME).read_bytes()

    with pytest.raises(SystemExit) as exc:
        _record(root, base, "--tests", "tests/test_mod.py")

    assert exc.value.code == 2
    assert (home / _REG_NAME).read_bytes() == written
    assert _record(root, base, "--tests", "tests/test_mod.py", "--replace") == 0


def test_a_red_in_both_the_registry_and_the_merged_tree_is_preexisting(repo, home, tmp_path):
    root, _ = repo
    base = _commit(root, {"scripts/old.py": "X = 1\n",
                          "tests/test_old.py": "import old\n\n\ndef test_old():\n    assert False\n"},
                   "a red on main")
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_old.py")
    merged = _commit(root, {"scripts/old.py": "X = 2\n"}, "the lane touches the module the red covers")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["preexisting"] == ["tests/test_old.py::test_old"]
    assert verdict["lane"] == [] and verdict["turned_red"] == []
    assert verdict["verdict"] == "CLEAN" and code == 0


def test_a_red_only_in_the_merged_tree_is_the_lanes(repo, home, tmp_path):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"tests/test_new.py": _RED}, "the lane adds a red test")

    code, verdict = _compare(root, merged, tmp_path)

    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_red"]
    assert verdict["lane"][0]["was"] == "absent"
    assert verdict["preexisting"] == []
    assert verdict["verdict"] == "LANE-RED" and code == 1


def test_a_registry_green_that_is_red_in_the_merged_tree_is_newly_red(repo, home, tmp_path):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"scripts/mod.py": "def value():\n    return 2\n"}, "the lane breaks mod")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["lane"][0]["was"] == "PASSED"
    assert verdict["turned_red"] == ["tests/test_mod.py::test_value"]
    assert code == 1


def test_a_red_that_passes_on_rerun_is_a_flake_not_the_lanes(repo, home, tmp_path, monkeypatch):
    root, base = repo
    monkeypatch.setenv("PAIRING_FLAKE_COUNTER", str(tmp_path / "flaky-counter.txt"))
    _record(root, base, "--tests", "tests/test_mod.py")
    flaky = ("import os\nfrom pathlib import Path\n\n\ndef test_flaky():\n"
             "    p = Path(os.environ['PAIRING_FLAKE_COUNTER'])\n"
             "    n = int(p.read_text()) if p.exists() else 0\n"
             "    p.write_text(str(n + 1))\n    assert n >= 1\n")
    merged = _commit(root, {"tests/test_flaky.py": flaky}, "a test that is red only once")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["lane"] == [] and [f["id"] for f in verdict["flakes"]] == ["tests/test_flaky.py::test_flaky"]
    assert verdict["flakes"][0]["observations"] == ["FAILED", "PASSED"]
    assert code == 0


# --- the skip-count guard --------------------------------------------------------------------

def test_a_comparison_whose_skip_count_differs_from_the_registrys_is_refused_as_unattributable(
        repo, home, tmp_path, capsys):
    root, _ = repo
    base = _commit(root, {"tests/test_skip.py": _SKIP}, "main skips one test")
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_skip.py")
    # the lane silences a second test: a red it would have shown is now a skip
    merged = _commit(root, {"tests/test_skip.py": _SKIP + "# touched, still skipped\n",
                            "tests/test_mod.py":
                            "import pytest\n\n\ndef test_value():\n    pytest.skip('hidden')\n"},
                     "the lane skips a test and touches the one main already skips")

    code, verdict = _compare(root, merged, tmp_path)

    assert code == 4, "a distinct exit: not clean, not lane-red, not a tool failure"
    assert verdict["verdict"] == "UNATTRIBUTABLE"
    assert verdict["lane"] == [] and verdict["preexisting"] == [], "nothing is classified on a mismatch"
    assert verdict["skip_guard"]["registry"] == 1 and verdict["skip_guard"]["head"] == 2
    assert verdict["skip_guard"]["added"] == ["tests/test_mod.py::test_value"]
    err = capsys.readouterr().err
    assert "unattributable" in err.lower() and "skip" in err.lower()


def test_a_new_skipped_test_added_inside_an_existing_covered_file_is_not_unattributable(
        repo, home, tmp_path):
    """Finding 2 (DIGEST-WAVE4-FINAL-2026-09-22): the skip-guard asymmetry.

    Before the fix, a NEW node id skipping inside an EXISTING (registry-covered) file
    tripped the guard identically to a KNOWN id being silenced -- purely because file-level
    `covered` membership was the only boundary the guard could see. The SAME new test added
    to a brand-NEW file was already exempt (`test_a_lane_added_skipped_test_does_not_trip_
    the_guard_because_the_registry_never_ran_it` below), so the asymmetry was which side of
    a FILE boundary the new id happened to land on -- not anything about risk: a node id
    the registry never recorded (not red, not passed, not skipped) cannot be hiding a
    registry-known result, because there was nothing recorded for it to hide.
    """
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"tests/test_mod.py":
                            "import pytest\nimport mod\n\n\ndef test_value():\n"
                            "    assert mod.value() == 1\n\n\ndef test_added():\n"
                            "    pytest.skip('new')\n"}, "a new skipped test in an existing file")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["skip_guard"]["status"] == "match", (
        "a brand-new node id has no registry identity to hide behind a skip"
    )
    assert verdict["verdict"] == "CLEAN" and code == 0


def test_a_collection_level_skip_that_silences_a_known_file_is_not_missed(repo, home, tmp_path):
    """Codex terra HIGH: a module skipped at COLLECTION time (`pytest.skip(...,
    allow_module_level=True)`, or a file-level `collect_ignore`) reports ONE skip whose id
    is the FILE, never a per-test node id -- so the old check (`a in known`, node ids only)
    let it slide past even while it silences every known result the registry has for that
    file. A file-level added id naming a file that carries known ids is exactly as
    dangerous as a known node id itself.
    """
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"tests/test_mod.py":
                            "import pytest\npytest.skip('silenced', allow_module_level=True)\n"
                            "import mod\n\n\ndef test_value():\n    assert mod.value() == 1\n"},
                     "the lane skips the whole module at collection time")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["skip_guard"]["status"] == "mismatch", (
        "a file-level collection skip that silences a known node must not read as a match"
    )
    assert verdict["verdict"] == "UNATTRIBUTABLE" and code == 4


def test_a_comparison_with_the_same_skip_count_is_attributed_normally(repo, home, tmp_path):
    root, _ = repo
    base = _commit(root, {"tests/test_skip.py": _SKIP}, "main skips one test")
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_skip.py")
    merged = _commit(root, {"tests/test_new.py": _RED, "tests/test_skip.py": _SKIP + "# touched\n"},
                     "the lane adds a red and touches the test main already skips")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["skip_guard"] == {"status": "match", "registry": 1, "head": 1,
                                     "added": [], "removed": []}
    assert _ids(verdict["lane"]) == ["tests/test_new.py::test_red"] and code == 1


def test_a_lane_added_skipped_test_does_not_trip_the_guard_because_the_registry_never_ran_it(
        repo, home, tmp_path):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"tests/test_new.py": _SKIP}, "the lane adds a test that skips")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["skip_guard"]["status"] == "match", "the guard counts the tests both sides ran"
    assert code == 0


# --- the shape of the command and its refusals -------------------------------------------------

def test_a_batch_is_required_and_must_be_a_plain_name(repo, home):
    root, base = repo
    for extra in (["--batch", "../escape"], ["--batch", "a b"], []):
        argv = ["record-base", "--commit", base, "--repo", str(root), "--workers", "0",
                "--tests", "tests/test_mod.py"]
        if extra:
            argv = [a for a in argv] + extra
        with pytest.raises(SystemExit) as exc:
            test_pairing.main(argv)
        assert exc.value.code == 2, extra
    assert not home.exists(), "a refused registry left nothing behind"


def test_the_batch_falls_back_to_the_environment(repo, home, monkeypatch):
    root, base = repo
    monkeypatch.setenv("HARNESS_BATCH", "B1")

    code = test_pairing.main(["record-base", "--commit", base, "--repo", str(root), "--workers", "0",
                              "--tests", "tests/test_mod.py"])

    assert code == 0 and (home / _REG_NAME).is_file()


def test_comparing_without_a_registry_fails_closed_rather_than_reading_as_clean(repo, home, tmp_path):
    root, base = repo
    with pytest.raises(SystemExit) as exc:
        test_pairing.main(["compare", "--batch", "B1", "--head", base, "--repo", str(root),
                           "--out", str(tmp_path / "v.json"), "--workers", "0"])
    assert exc.value.code == 2


def test_a_registry_of_another_schema_is_refused(repo, home, tmp_path):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    data = _registry(home)
    data["schema"] = "test-pairing-registry/0"
    (home / _REG_NAME).write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        test_pairing.main(["compare", "--batch", "B1", "--head", base, "--repo", str(root),
                           "--out", str(tmp_path / "v.json"), "--workers", "0"])
    assert exc.value.code == 2


def test_record_base_takes_its_files_from_the_batchs_lanes(repo, home):
    root, _ = repo
    _git(root, "checkout", "-b", "worktree-demo")
    _commit(root, {"scripts/mod.py": "def value():\n    return 1\n# lane\n",
                   "tests/test_new.py": _RED}, "lane work")
    _git(root, "checkout", "main")
    base = _commit(root, {"README.md": "main moved on\n"}, "main advances")

    code = _record(root, base, "--lane", "demo")

    registry = _registry(home)
    assert code == 0
    assert registry["files"] == ["tests/test_mod.py"], "a test the lane adds does not exist on the base"
    assert registry["lanes"] == ["demo"]


def test_a_docs_only_selection_resolves_the_live_repo_marker_to_files(repo, home, tmp_path):
    root, _ = repo
    live = ("import pytest\n\npytestmark = pytest.mark.live_repo\n\n\ndef test_live():\n"
            "    assert False\n")
    base = _commit(root, {"tests/test_live.py": live}, "a live-repo red on main")
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_live.py")
    merged = _commit(root, {"README.md": "a docs-only lane\n"}, "docs only")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["selection"]["test_files"] == ["tests/test_live.py"]
    assert verdict["preexisting"] == ["tests/test_live.py::test_live"] and code == 0


# --- the codex terra review's three HIGH findings (docs/audits/2026-09-22-codex-lane-known-reds.md) ---

def test_swapping_which_test_is_skipped_keeps_the_count_but_is_still_unattributable(repo, home,
                                                                                    tmp_path):
    root, _ = repo
    red = "def test_hidden():\n    assert False\n"
    base = _commit(root, {"tests/test_a.py": _SKIP, "tests/test_b.py": red}, "one skipped, one red")
    _record(root, base, "--tests", "tests/test_a.py", "tests/test_b.py")
    # the lane un-skips one test and skips the red one: the COUNT is unchanged, the red is hidden
    merged = _commit(root, {"tests/test_a.py": "def test_skipped():\n    assert True\n",
                            "tests/test_b.py": "import pytest\n\n\ndef test_hidden():\n"
                                               "    pytest.skip('hidden')\n"}, "swap the skips")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["skip_guard"]["registry"] == verdict["skip_guard"]["head"] == 1
    assert verdict["skip_guard"]["added"] == ["tests/test_b.py::test_hidden"]
    assert verdict["verdict"] == "UNATTRIBUTABLE" and code == 4


def test_a_selected_file_that_existed_on_the_base_but_is_not_in_the_registry_is_unattributable(
        repo, home, tmp_path):
    root, _ = repo
    base = _commit(root, {"scripts/other.py": "Y = 1\n",
                          "tests/test_other.py": "import other\n\n\ndef test_other():\n    assert False\n"},
                   "an unrecorded red on main")
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"scripts/other.py": "Y = 2\n"}, "a lane touches what the registry never ran")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["verdict"] == "UNATTRIBUTABLE" and code == 4
    assert verdict["unregistered"] == ["tests/test_other.py"]
    assert verdict["lane"] == [] and verdict["preexisting"] == [], "nothing is classified"


def test_a_file_the_lane_added_is_not_unregistered_because_it_did_not_exist_on_the_base(repo, home,
                                                                                         tmp_path):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    merged = _commit(root, {"tests/test_new.py": _RED}, "the lane adds a red")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["unregistered"] == [] and code == 1


def test_write_registry_never_replaces_an_existing_registry_unless_told_to(repo, home):
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    path = home / _REG_NAME
    written = path.read_bytes()
    other = test_pairing.Registry.from_json({**_registry(home), "commit": "0" * 40}, "x")

    with pytest.raises(test_pairing.PairingError):
        test_pairing.write_registry(path, other)

    assert path.read_bytes() == written, "a racing writer cannot overwrite without --replace"
    assert [p.name for p in home.iterdir()] == [_REG_NAME], "no temp file left beside the registry"
    test_pairing.write_registry(path, other, replace=True)
    assert json.loads(path.read_text(encoding="utf-8"))["commit"] == "0" * 40


def test_the_existing_two_commit_form_is_untouched_by_the_registry_commands(repo, tmp_path):
    root, base = repo
    head = _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "red")

    code, verdict = _run(root, base, head, tmp_path)

    assert code == 1 and _ids(verdict["lane"]) == ["tests/test_new.py::test_new"]


# =============================================================================================
# lane-verify-in-lane (W4B-4), Done-contract 2: RECORD BY TREE. A lane runs its own selection
# on `origin/main + lane`, classifies against the batch registry, and persists the verdict
# keyed by (tree sha, origin/main sha) -- `record-lane`. A second mode, `reuse-check`, tells
# the integrator whether that record still applies: REUSABLE (origin/main unchanged),
# STALE-TREE (the lane advanced -- the record answers for a tree that no longer exists at the
# lane's tip), or MAIN-MOVED (only main moved -- report the SUBSET impacted by main's own
# diff, not the lane's whole selection again). Synthetic repos only, as above.
# =============================================================================================

def _record_lane(root: Path, lane: str, *extra: str) -> int:
    return test_pairing.main(["record-lane", "--batch", "B1", "--lane", lane, "--main", "main",
                              "--repo", str(root), "--workers", "0", *extra])


def _reuse_check(root: Path, lane: str, *extra: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "test_pairing.py"), "reuse-check", "--batch", "B1",
         "--lane", lane, "--main", "main", "--repo", str(root), *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode, json.loads(proc.stdout)


def _lane_record(home: Path, lane: str) -> dict:
    return json.loads((home / f"TEST-PAIRING-LANE-B1-{lane}.json").read_text(encoding="utf-8"))


@pytest.fixture
def lane_registry_repo(repo, home) -> tuple[Path, str]:
    """A registry recorded off `main`, with `worktree-demo` branched from it."""
    root, base = repo
    _record(root, base, "--tests", "tests/test_mod.py")
    _git(root, "checkout", "-b", "worktree-demo")
    return root, base


def test_record_lane_writes_a_record_keyed_by_the_tree_and_origin_main_sha(lane_registry_repo, home):
    root, main_sha = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "lane work")
    lane_sha = _git(root, "rev-parse", "HEAD")

    code = _record_lane(root, "demo")

    assert code == 1, "the lane's own red is exit 1, same vocabulary as compare()"
    record = _lane_record(home, "demo")
    assert record["schema"] == "test-pairing-lane-record/1"
    assert record["batch"] == "B1" and record["lane"] == "demo"
    assert record["tree"] == lane_sha, "keyed by the LANE'S tree sha"
    assert record["origin_main"] == main_sha, "keyed by the origin/main sha it ran against"
    assert record["verdict"]["verdict"] == "LANE-RED"
    assert _ids(record["verdict"]["lane"]) == ["tests/test_new.py::test_new"]


def test_record_lane_rejects_zero_reruns_same_as_pair_and_compare(lane_registry_repo, home):
    """Codex terra P1: `record-lane --reruns 0` skipped the flake rerun entirely and would
    classify every initially failing lane test as LANE-RED with no flake protection --
    `pair()`/`compare()` already refuse this; `record_lane()` must refuse it identically."""
    root, _ = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "lane work")

    with pytest.raises(SystemExit) as exc:
        _record_lane(root, "demo", "--reruns", "0")

    assert exc.value.code == 2
    assert not (home / "TEST-PAIRING-LANE-B1-demo.json").exists()


def test_record_lane_selects_from_the_lanes_own_diff_not_the_registrys_two_dot_range(
        lane_registry_repo, home):
    """The registry's base and the lane's sync point can differ; record-lane uses the
    lane's OWN diff against `--main` (impacted_tests.select_lane_diff), not a two-dot
    diff against the registry's recorded commit."""
    root, main_sha = lane_registry_repo
    _commit(root, {"scripts/mod.py": "def value():\n    return 1\n# touched\n"}, "lane touches mod")

    _record_lane(root, "demo")

    record = _lane_record(home, "demo")
    assert record["verdict"]["selection"]["test_files"] == ["tests/test_mod.py"]


def test_record_lane_is_overwritten_by_a_later_run_no_replace_flag_needed(lane_registry_repo, home):
    """Unlike `record-base`, a lane's own record is never exclusive -- it is the lane's,
    and re-verifying after a new commit is the normal path, not a laundering risk."""
    root, _ = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    assert _record_lane(root, "demo") == 0
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "now red")

    code = _record_lane(root, "demo")

    assert code == 1
    assert _lane_record(home, "demo")["verdict"]["verdict"] == "LANE-RED"


def test_record_lane_refuses_when_the_lane_has_not_merged_main(lane_registry_repo, home):
    """Codex terra HIGH: `record_lane` clones only the lane's tip and never combines
    `--main` into the tested tree, so a record keyed to an origin/main sha the lane never
    actually merged would be false. Refuse rather than write a misleading REUSABLE claim.
    """
    root, _ = lane_registry_repo
    _git(root, "checkout", "main")
    _commit(root, {"scripts/other.py": "Y = 1\n"}, "main advances; the lane never merges it")
    _git(root, "checkout", "worktree-demo")

    with pytest.raises(SystemExit) as exc:
        _record_lane(root, "demo")

    assert exc.value.code == 2
    assert not (home / "TEST-PAIRING-LANE-B1-demo.json").exists()


def test_reuse_check_reports_not_recorded_when_no_record_exists(lane_registry_repo, home):
    root, _ = lane_registry_repo

    code, status = _reuse_check(root, "demo")

    assert status["status"] == "NOT-RECORDED" and status["reusable"] is False
    assert code == 5


def test_reuse_check_reports_reusable_when_neither_tree_nor_origin_main_moved(
        lane_registry_repo, home):
    root, _ = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    _record_lane(root, "demo")

    code, status = _reuse_check(root, "demo")

    assert status["status"] == "REUSABLE" and status["reusable"] is True
    assert status["verdict"]["verdict"] == "CLEAN"
    assert code == 0


def test_reuse_check_reports_stale_tree_when_the_lane_advanced_since_the_record(
        lane_registry_repo, home):
    root, _ = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    _record_lane(root, "demo")
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert False\n"}, "the lane moved on")

    code, status = _reuse_check(root, "demo")

    assert status["status"] == "STALE-TREE" and status["reusable"] is False
    assert code == 6


def test_reuse_check_reports_the_rerun_subset_when_only_origin_main_moved(lane_registry_repo, home):
    root, _ = lane_registry_repo
    _commit(root, {"tests/test_new.py": "def test_new():\n    assert True\n"}, "green")
    _record_lane(root, "demo")
    _git(root, "checkout", "main")
    _commit(root, {"scripts/other.py": "Y = 1\n",
                   "tests/test_other.py": "def test_other():\n    assert False\n"},
           "main advances while the lane waits")
    _git(root, "checkout", "worktree-demo")

    code, status = _reuse_check(root, "demo")

    assert status["status"] == "MAIN-MOVED" and status["reusable"] is False
    assert status["rerun_selection"]["test_files"] == ["tests/test_other.py"], (
        "only what main's OWN diff impacts, never the lane's whole selection again"
    )
    assert code == 7


# --- finding 8 (DIGEST-WAVE4-FINAL): the registry is node-id granular, not finding granular ---

def test_a_second_distinct_cause_inside_an_already_red_test_stays_masked_as_preexisting(
        repo, home, tmp_path):
    """Finding 8, disposed rather than silently accepted: documents the HONEST LIMIT.

    Base has ONE reason `test_old` is red; the lane's diff adds a SECOND, independent
    reason inside the SAME test. The node-id registry classifies this identically to a
    lane that touched nothing -- `preexisting`, not surfaced -- because a node id carries
    no notion of "which finding, or how many". This is the behaviour the module docstring
    names as an honest limit, not a defect this lane's contract asks it to fix.
    """
    root, _ = repo
    base = _commit(root, {"scripts/old.py": "def a():\n    return False\ndef b():\n    return True\n",
                          "tests/test_old.py":
                          "import old\n\n\ndef test_old():\n    assert old.a()\n"},
                   "one reason test_old is red")
    _record(root, base, "--tests", "tests/test_mod.py", "tests/test_old.py")
    merged = _commit(root, {"scripts/old.py":
                            "def a():\n    return False\ndef b():\n    return False\n",
                            "tests/test_old.py":
                            "import old\n\n\ndef test_old():\n    assert old.a()\n    assert old.b()\n"},
                     "the lane adds a SECOND, independent reason the same test is red")

    code, verdict = _compare(root, merged, tmp_path)

    assert verdict["preexisting"] == ["tests/test_old.py::test_old"], (
        "the second cause is real but invisible at node-id granularity -- masked, as documented"
    )
    assert verdict["lane"] == [] and verdict["verdict"] == "CLEAN" and code == 0


def test_the_named_alternative_instrument_is_finding_granular_not_node_id_granular():
    """`decision_coverage.py check` is what the docstring names as able to see it: it
    prints one ProbeFinding per decision, not one verdict per wrapping pytest node id."""
    import dataclasses
    import inspect

    sys.path.insert(0, str(_SCRIPTS))
    import decision_coverage as dc  # noqa: E402

    fields = {f.name for f in dataclasses.fields(dc.Finding)}
    assert {"subject", "evidence"} <= fields
    src = inspect.getsource(dc.main)
    assert "for finding in findings" in src, (
        "the CLI must print PER FINDING, not a single pass/fail for the whole check"
    )


def test_the_registry_commands_are_untouched_by_the_new_lane_commands(repo, home):
    root, base = repo

    code = _record(root, base, "--tests", "tests/test_mod.py")

    assert code == 0 and (home / "TEST-PAIRING-REGISTRY-B1.json").is_file()
