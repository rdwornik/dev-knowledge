"""[#429] leg (b) — the runnable check that a checkout's pytest imports THAT checkout's source.

THE CHECK'S OWN FAILURE MODES ARE THE POINT. An organ built to refuse a silent green must not
have a silent green of its own, so the tests below concentrate on the three ways this one could
acquire it:

  * A SKIP THAT READS AS A PASS. `NOT-APPLICABLE` is exit 3 and is asserted to be distinct from
    0 — a repo the tool cannot examine has to be distinguishable from one it examined and
    cleared. Pinned as a value, because folding it into 0 is a one-character regression.
  * AN IMPORT ERROR COUNTED AS AN IMPORT. A package that would not load is not evidence that
    the right package did. `_inside` returns False for the error case, and a test says so.
  * A VERDICT THAT IS REALLY ABOUT THE CALLER. This one was a live defect, not a hypothetical:
    the first draft fell back to `sys.executable`, so running the tool from the hub under
    `uv run` handed an unprovisioned satellite the HUB's interpreter and reported
    `ModuleNotFoundError` — a FAIL whose stated cause was "the package is missing" when the
    real finding is "the package came from the wrong checkout". `_caller_free_path` and the
    `py`-first fallback order are what fixed it, and both are pinned below.

The end-to-end coverage here runs the real subprocess pipeline against synthetic repos. The
wrong-tree import itself is proved live rather than synthetically — reproducing it needs a
shared editable install, which is a property of an installed environment and not of a tmp_path.
That evidence is `docs/audits/2026-08-07-technical-lane-2-worktree-portability.md`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import worktree_import_proof as wip  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_HUB = Path(__file__).resolve().parent.parent


# --- helpers ----------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _repo_with_package(path: Path, dist: str, package: str, *, src_layout: bool = False) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.invalid")
    _git(path, "config", "user.name", "t")
    (path / "pyproject.toml").write_text(
        f'[build-system]\nrequires = ["setuptools"]\n\n'
        f'[project]\nname = "{dist}"\nversion = "0"\n\n'
        f'[tool.pytest.ini_options]\nminversion = "9.0"\n',
        encoding="utf-8",
    )
    base = (path / "src") if src_layout else path
    pkg = base / package
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path


# --- exit-code contract -----------------------------------------------------

def test_not_applicable_is_not_success():
    """The single most important line in this file."""
    assert wip.EXIT_NOT_APPLICABLE != wip.EXIT_PASS
    assert wip.EXIT_NOT_APPLICABLE == 3


def test_error_is_not_success_either():
    assert wip.EXIT_ERROR not in (wip.EXIT_PASS, wip.EXIT_FAIL)


@requires_git
def test_a_repo_with_no_importable_package_reports_not_applicable(tmp_path, capsys):
    plain = tmp_path / "plain"
    plain.mkdir()
    _git(plain, "init", "-q")
    _git(plain, "config", "user.email", "t@example.invalid")
    _git(plain, "config", "user.name", "t")
    (plain / "f.txt").write_text("x", encoding="utf-8")
    _git(plain, "add", "-A")
    _git(plain, "commit", "-qm", "init")

    assert wip.main(["--repo", str(plain)]) == wip.EXIT_NOT_APPLICABLE
    assert "NOT-APPLICABLE" in capsys.readouterr().out


def test_the_live_hub_is_not_applicable_and_says_so(capsys):
    """The hub ships no importable package. It must not report PASS — there is nothing here
    whose checkout could have been wrong, and claiming a clean bill would be the exact
    over-claim the module refuses."""
    assert wip.main(["--repo", str(_HUB)]) == wip.EXIT_NOT_APPLICABLE
    assert "Nothing was proved" in capsys.readouterr().out


def test_a_path_that_is_not_a_checkout_is_an_error_not_a_pass(tmp_path):
    assert wip.main(["--repo", str(tmp_path / "nowhere")]) == wip.EXIT_ERROR


# --- package discovery ------------------------------------------------------

@requires_git
def test_discovery_falls_back_to_the_distribution_name_normalised(tmp_path):
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    assert wip.declared_packages(repo) == ("demo_pkg",)


@requires_git
def test_discovery_finds_a_src_layout_package(tmp_path):
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg", src_layout=True)
    assert wip.declared_packages(repo) == ("demo_pkg",)


@requires_git
def test_discovery_reads_the_setuptools_include_globs(tmp_path):
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    extra = repo / "helper"
    extra.mkdir()
    (extra / "__init__.py").write_text("", encoding="utf-8")
    (repo / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n'
        '[project]\nname = "demo-pkg"\nversion = "0"\n\n'
        '[tool.setuptools.packages.find]\ninclude = ["demo_pkg*", "helper*"]\n',
        encoding="utf-8",
    )
    assert set(wip.declared_packages(repo)) == {"demo_pkg", "helper"}


@requires_git
def test_a_declared_package_absent_from_disk_is_not_reported_as_checked(tmp_path):
    """A name that could never have resolved locally proves nothing about which checkout won,
    so counting it would inflate the report with packages nobody examined."""
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    (repo / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n'
        '[project]\nname = "demo-pkg"\nversion = "0"\n\n'
        '[tool.setuptools.packages.find]\ninclude = ["demo_pkg*", "ghost*"]\n',
        encoding="utf-8",
    )
    assert wip.declared_packages(repo) == ("demo_pkg",)


# --- the inside/outside decision -------------------------------------------

def test_a_file_under_the_root_is_inside(tmp_path):
    assert wip._inside(tmp_path, {"file": str(tmp_path / "pkg" / "__init__.py")})


def test_a_file_outside_the_root_is_not_inside(tmp_path):
    assert not wip._inside(tmp_path / "here", {"file": str(tmp_path / "elsewhere" / "m.py")})


def test_an_import_error_is_never_inside(tmp_path):
    """An unimportable package is a failure, not an absence of evidence."""
    assert not wip._inside(tmp_path, {"error": "ModuleNotFoundError: no"})


def test_a_namespace_package_needs_every_search_path_inside(tmp_path):
    inside = str(tmp_path / "a")
    outside = str(tmp_path.parent / "b")
    assert wip._inside(tmp_path, {"namespace_paths": [inside]})
    assert not wip._inside(tmp_path, {"namespace_paths": [inside, outside]})


def test_a_namespace_package_with_no_paths_is_not_inside(tmp_path):
    assert not wip._inside(tmp_path, {"namespace_paths": []})


# --- interpreter resolution (the live-defect guards) ------------------------

def test_a_checkout_with_its_own_venv_wins_outright(tmp_path, monkeypatch):
    venv_python = tmp_path / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("", encoding="utf-8")

    argv, own = wip.resolve_interpreter(tmp_path)
    assert own is True
    assert argv == [str(venv_python)]


def test_the_fallback_tries_the_system_launcher_first():
    """Order is the fix for the live defect. `py` lives outside every virtualenv, so it is the
    one name an activated environment cannot shadow — and the system interpreter is where a
    shared editable install actually sits."""
    assert wip._FALLBACK_INTERPRETERS[0] == "py"


def test_the_caller_free_path_drops_the_callers_own_prefix():
    prefix = Path(sys.prefix).resolve()
    remaining = [Path(p).resolve() for p in wip._caller_free_path().split(os.pathsep) if p]
    assert all(p != prefix and prefix not in p.parents for p in remaining)


def test_the_caller_free_path_keeps_everything_else(monkeypatch, tmp_path):
    keep = tmp_path / "keep"
    keep.mkdir()
    monkeypatch.setenv("PATH", os.pathsep.join([str(Path(sys.prefix) / "Scripts"), str(keep)]))
    assert str(keep) in wip._caller_free_path()


def test_a_checkout_without_a_venv_reports_that_it_has_none(tmp_path):
    assert wip.resolve_interpreter(tmp_path)[1] is False


# --- the child environment --------------------------------------------------

def test_the_child_environment_drops_the_inherited_venv_pointers(tmp_path, monkeypatch):
    """These four are the leak under investigation. A proof that inherited them could report
    the parent seat's answer while appearing to ask the child."""
    for name in ("VIRTUAL_ENV", "PYTHONHOME", "PYTHONPATH", "PYTHONSTARTUP"):
        monkeypatch.setenv(name, "leaked")
    env = wip._child_env(tmp_path, ("pkg",), tmp_path / "out.json")
    for name in ("VIRTUAL_ENV", "PYTHONHOME", "PYTHONPATH", "PYTHONSTARTUP"):
        assert name not in env


def test_the_child_environment_blocks_user_site_packages(tmp_path):
    env = wip._child_env(tmp_path, ("pkg",), tmp_path / "out.json")
    assert env["PYTHONNOUSERSITE"] == "1"


def test_the_child_environment_carries_the_proof_parameters(tmp_path):
    env = wip._child_env(tmp_path, ("a", "b"), tmp_path / "out.json")
    assert env["WT_PROOF_ROOT"] == str(tmp_path)
    assert env["WT_PROOF_PACKAGES"] == "a,b"
    assert env["WT_PROOF_OUT"] == str(tmp_path / "out.json")


# --- end to end -------------------------------------------------------------

@requires_git
def test_end_to_end_pass_on_a_checkout_that_owns_its_source(tmp_path, monkeypatch):
    """The real subprocess pipeline: spawn pytest, collect the generated test, read the
    resolved paths back. The interpreter is pinned to this one so the test does not depend on
    what the system python happens to have installed."""
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    monkeypatch.setattr(wip, "resolve_interpreter", lambda root: ([sys.executable], True))

    proof = wip.run_proof(repo, ("demo_pkg",))
    assert proof.pytest_returncode == 0, proof.pytest_output
    assert proof.passed
    assert proof.outside == []
    assert proof.rootdir == repo.resolve()
    assert repo.resolve() in Path(proof.resolved["demo_pkg"]["file"]).parents


@requires_git
def test_end_to_end_fail_when_the_package_does_not_resolve(tmp_path, monkeypatch):
    """A real FAIL through the whole pipeline. Proves the organ can return 1 — an organ only
    ever watched to pass is an organ nobody knows is wired to anything."""
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    monkeypatch.setattr(wip, "resolve_interpreter", lambda root: ([sys.executable], True))

    proof = wip.run_proof(repo, ("not_a_real_package_xyz",))
    assert not proof.passed
    assert proof.outside == ["not_a_real_package_xyz"]
    assert "error" in proof.resolved["not_a_real_package_xyz"]


@requires_git
def test_the_proof_leaves_no_pytest_cache_in_the_target_tree(tmp_path, monkeypatch):
    """No-leftovers (CLAUDE.md §5 rule 9) applied to the repo being measured: a read-only
    organ that dirties the tree it inspects would trip the session-end gate of whoever ran it."""
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    monkeypatch.setattr(wip, "resolve_interpreter", lambda root: ([sys.executable], True))

    wip.run_proof(repo, ("demo_pkg",))
    assert not (repo / ".pytest_cache").exists()
    assert _git(repo, "status", "--porcelain").stdout.strip() == ""


@requires_git
def test_the_repos_own_pytest_ini_is_used(tmp_path):
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    assert wip._pytest_ini_arg(repo) == ["-c", str(repo / "pyproject.toml")]


def test_a_repo_with_no_ini_passes_no_config_flag(tmp_path):
    assert wip._pytest_ini_arg(tmp_path) == []


# --- reporting --------------------------------------------------------------

@requires_git
def test_the_report_names_the_remedy_when_it_fails(tmp_path, monkeypatch):
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    monkeypatch.setattr(wip, "resolve_interpreter", lambda root: ([sys.executable], True))

    text = wip.render(wip.run_proof(repo, ("not_a_real_package_xyz",)), applicable=True)
    assert "FAIL" in text
    assert "worktree_seed.py --plan" in text


@requires_git
def test_the_report_states_whether_the_venv_is_inside_the_checkout(tmp_path, monkeypatch):
    """The diagnosis leg (b) is about, printed on every run rather than only on failure."""
    repo = _repo_with_package(tmp_path / "demo", "demo-pkg", "demo_pkg")
    monkeypatch.setattr(wip, "resolve_interpreter", lambda root: ([sys.executable], False))
    text = wip.render(wip.run_proof(repo, ("demo_pkg",)), applicable=True)
    assert "NOT inside the checkout" in text
