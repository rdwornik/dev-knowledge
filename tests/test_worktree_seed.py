"""[#429] leg (a) — the fleet worktree seed manifest, stated once in the hub.

WHAT THESE PIN, and why each is a defect waiting rather than a coverage box:

  * THE HUB FILE IS GENERATED, NOT AUTHORED. `.worktreeinclude` and the manifest in
    `scripts/worktree_seed.py` are one declaration in two places, and a hand-edit to the file
    is silent — it changes what worktrees seed with nothing reporting it. `--check` is the
    regen-and-diff that makes it loud, so a test asserts the shipped file matches.
  * THE REFUSAL IS THE LAYER-2 BOUNDARY. `--write` pointed at a consumer would make this hub
    tool drive state in a child repo (ADR-28/36). The refusal is the invariant, so it is
    asserted as behaviour rather than trusted to the docstring.
  * THE COPY BLOCK USES A PATH GLOB, NOT A RECURSIVE BASENAME SEARCH. This is the one property
    with a live blast radius: the hub's own lanes live at `.claude/worktrees/` INSIDE the
    primary tree, so `-Recurse -Filter settings.local.json` run during a batch would descend
    into every sibling lane's checkout and copy whichever file it reached first. The first
    draft of this module did exactly that. A test pins the shape so the regression is not
    re-introduced by someone shortening the emitted command.
  * `env_bootstrap` IS DERIVED, NEVER DECLARED. That is the property that makes a satellite's
    answer survive its own toolchain changes without a hub edit, so the tests drive it off
    synthetic repos rather than off the live fleet.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import worktree_seed as ws  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_HUB = Path(__file__).resolve().parent.parent


# --- helpers ----------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.invalid")
    _git(path, "config", "user.name", "t")
    (path / "seed.txt").write_text("x", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path


# --- the manifest -----------------------------------------------------------

def test_universal_patterns_apply_to_a_repo_with_no_entry_of_its_own():
    """The portability property, at its smallest: a satellite the manifest has never heard of
    still gets an answer. If this returned () for an unknown name, leg (a) would be a hub
    lookup table rather than a fleet manifest."""
    patterns = ws.copy_patterns("some-repo-nobody-declared")
    assert patterns == ws.UNIVERSAL_COPY


def test_the_hub_entry_is_the_universal_set_plus_its_own_ecosystem_state():
    patterns = ws.copy_patterns(ws.HUB_REPO_NAME)
    assert patterns[: len(ws.UNIVERSAL_COPY)] == ws.UNIVERSAL_COPY
    assert "ecosystem/*/state.yaml" in patterns


def test_rendered_worktreeinclude_carries_every_pattern_on_its_own_line():
    rendered = ws.render_worktreeinclude(ws.HUB_REPO_NAME)
    body = [ln for ln in rendered.splitlines() if ln and not ln.startswith("#")]
    assert body == list(ws.copy_patterns(ws.HUB_REPO_NAME))


def test_rendered_file_says_where_to_edit_it():
    """A generated file that does not name its generator gets hand-edited. The pointer is the
    only thing standing between a reader and an edit `--check` will later reject."""
    rendered = ws.render_worktreeinclude(ws.HUB_REPO_NAME)
    assert "scripts/worktree_seed.py" in rendered


def test_the_shipped_hub_worktreeinclude_matches_the_manifest():
    """Regen-and-diff, as a test rather than only as a CLI flag."""
    shipped = (_HUB / ".worktreeinclude").read_text(encoding="utf-8")
    assert shipped == ws.render_worktreeinclude(ws.HUB_REPO_NAME)


# --- derived environment bootstrap ------------------------------------------

def test_a_repo_with_a_uv_lock_bootstraps_through_uv(tmp_path):
    (tmp_path / "uv.lock").write_text("", encoding="utf-8")
    kind, commands = ws.env_bootstrap(tmp_path)
    assert kind == ws.ENV_UV
    assert any("uv sync --locked" in c for c in commands)


def test_a_packaged_repo_without_a_lock_bootstraps_a_venv_and_editable_install(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n'
        '[project]\nname = "demo-pkg"\nversion = "0"\n\n'
        '[project.optional-dependencies]\ndev = ["pytest"]\n',
        encoding="utf-8",
    )
    pkg = tmp_path / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")

    kind, commands = ws.env_bootstrap(tmp_path)
    assert kind == ws.ENV_VENV_EDITABLE
    assert any("venv" in c for c in commands)
    assert any('-e ".[dev]"' in c for c in commands)


def test_the_dev_extra_is_dropped_when_the_repo_does_not_declare_one(tmp_path):
    """Emitting `.[dev]` at a repo with no `dev` extra hands the lane a command that fails."""
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n[project]\nname = "demo-pkg"\nversion = "0"\n',
        encoding="utf-8",
    )
    pkg = tmp_path / "demo_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")

    _, commands = ws.env_bootstrap(tmp_path)
    assert any('-e "."' in c for c in commands)
    assert not any("[dev]" in c for c in commands)


def test_a_build_system_without_a_package_on_disk_needs_no_bootstrap(tmp_path):
    """The hub's own shape: it declares `[build-system]` and ships no importable package, so
    telling it to install itself editable would be a command with no subject."""
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n[project]\nname = "no-pkg"\nversion = "0"\n',
        encoding="utf-8",
    )
    assert ws.env_bootstrap(tmp_path)[0] == ws.ENV_NONE


def test_a_repo_with_no_pyproject_at_all_needs_no_bootstrap(tmp_path):
    assert ws.env_bootstrap(tmp_path) == (ws.ENV_NONE, ())


def test_the_live_hub_derives_the_uv_path():
    assert ws.env_bootstrap(_HUB)[0] == ws.ENV_UV


# --- plans over real checkouts ----------------------------------------------

@requires_git
def test_a_plan_over_a_worktree_names_the_primary_as_the_copy_source(tmp_path):
    primary = _init_repo(tmp_path / "demo")
    linked = tmp_path / "linked"
    _git(primary, "worktree", "add", "-q", str(linked), "-b", "worktree-demo")

    plan = ws.build_plan(linked)
    assert plan.is_worktree
    assert plan.root == linked.resolve()
    assert plan.primary == primary.resolve()

    _git(primary, "worktree", "remove", "--force", str(linked))


@requires_git
def test_a_plan_over_the_primary_reports_it_as_the_primary(tmp_path):
    primary = _init_repo(tmp_path / "demo")
    plan = ws.build_plan(primary)
    assert not plan.is_worktree
    assert plan.root == plan.primary


@requires_git
def test_a_declared_pattern_absent_from_the_primary_is_reported_not_dropped(tmp_path):
    """`.env` is declared for every repo and present in almost none. Dropping it silently
    would make "this repo does not use it" indistinguishable from "this repo lost it"."""
    primary = _init_repo(tmp_path / "demo")
    plan = ws.build_plan(primary)
    assert ".env" in plan.copy
    assert ".env" not in plan.present
    assert ".env" in ws.render_plan(plan)


@requires_git
def test_the_emitted_copy_block_globs_a_path_and_never_recurses_by_basename(tmp_path):
    """THE regression guard. A recursive basename search run from the hub's primary would walk
    into `.claude/worktrees/`, i.e. into every other lane of a live batch."""
    primary = _init_repo(tmp_path / "demo")
    (primary / ".env").write_text("K=v", encoding="utf-8")
    linked = tmp_path / "linked"
    _git(primary, "worktree", "add", "-q", str(linked), "-b", "worktree-demo")

    block = "\n".join(ws._copy_block(ws.build_plan(linked)))
    assert "-Recurse" not in block
    assert "-Filter" not in block
    assert "Get-ChildItem -Path (Join-Path $primary $p)" in block

    _git(primary, "worktree", "remove", "--force", str(linked))


@requires_git
def test_a_plan_always_ends_by_naming_the_proof(tmp_path):
    """The plan is a claim about provisioning; the proof is the only thing that measures it.
    A plan that did not hand the reader the verification step would be advice."""
    primary = _init_repo(tmp_path / "demo")
    assert "worktree_import_proof.py" in ws.render_plan(ws.build_plan(primary))


# --- the Layer-2 refusal ----------------------------------------------------

@requires_git
def test_write_refuses_a_target_that_is_not_the_hub(tmp_path):
    """ADR-28/36: Layer 2 drives no state in a child repo. Asserted as behaviour, because a
    refusal that lives only in a docstring is not a refusal."""
    consumer = _init_repo(tmp_path / "some-consumer")
    assert ws.main(["--repo", str(consumer), "--write"]) == ws.EXIT_ERROR
    assert not (consumer / ".worktreeinclude").exists()


@requires_git
def test_check_also_refuses_outside_the_hub(tmp_path):
    consumer = _init_repo(tmp_path / "some-consumer")
    assert ws.main(["--repo", str(consumer), "--check"]) == ws.EXIT_ERROR


def test_render_needs_no_checkout_at_all(capsys):
    """A satellite is served by NAME, not by having the tool run inside it — which is what
    lets the hub answer for a repo it is not sitting in."""
    assert ws.main(["--render", "ai-council"]) == ws.EXIT_OK
    assert ".claude/settings.local.json" in capsys.readouterr().out


def test_plan_and_render_and_check_are_mutually_exclusive():
    with pytest.raises(SystemExit):
        ws.main(["--render", "x", "--check"])


def test_an_action_is_required():
    with pytest.raises(SystemExit):
        ws.main([])


# --- drift detection --------------------------------------------------------

def test_check_reports_drift_when_the_file_diverges(tmp_path, monkeypatch):
    """Proves `--check` can FAIL. A regen-and-diff gate nobody has watched fail is a gate
    nobody knows is wired to anything."""
    fake_hub = tmp_path / ws.HUB_REPO_NAME
    fake_hub.mkdir()
    (fake_hub / ".worktreeinclude").write_text("hand-edited\n", encoding="utf-8")
    monkeypatch.setattr(ws, "resolve_checkout", lambda repo: (fake_hub, fake_hub))

    assert ws.main(["--repo", str(fake_hub), "--check"]) == ws.EXIT_DRIFT

    assert ws.main(["--repo", str(fake_hub), "--write"]) == ws.EXIT_OK
    assert ws.main(["--repo", str(fake_hub), "--check"]) == ws.EXIT_OK
