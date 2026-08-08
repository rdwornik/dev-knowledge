"""[#396] — `scripts/gitenv.py` is the ONE definition of the subprocess-git env scrub.

WHAT THIS LOCKS, and why each property is load-bearing:

  * **Leaf-ness** (`test_gitenv_is_a_leaf_module`). The scrub could not be consolidated
    before because `audit.py` imports `fleet_parity` LAZILY and bundle selection must not
    acquire a dependency on that import path. The ONLY thing that makes a top-level
    `import gitenv` in `audit.py` safe is that `gitenv` imports nothing from this repo. That
    is an invariant, not a coincidence, so it is asserted on the AST — a future `import
    audit` inside `gitenv` would re-open the exact hazard the duplication was protecting
    against, and would do it silently.

  * **Single definition** (`test_the_scrub_is_defined_exactly_once`). Three hand-copies is
    what [#396] exists to retire; a re-grown local `def _git_location_env` in a consumer
    would restore the rot mode while every call site still looked right.

  * **Semantics unchanged** (the two set tests). The move must be byte-equivalent: the 15
    pinned fallback names and the 2 `_EXTRA` scoping names, scrubbed BY NAME, with the
    identity/transport/global-config vars a `startswith("GIT_")` strip would have eaten
    deliberately PRESERVED.

  * **WHERE it fires is unchanged** (`test_the_deliberate_git_index_file_path_is_not_scrubbed`).
    `audit.py`'s fleet-automation commit path sets `GIT_INDEX_FILE` ON PURPOSE through its
    own explicit `env=` dict. [#396] changes where the scrub LIVES, never where it FIRES —
    routing that path through the scrub would silently break it.
"""
from __future__ import annotations

import ast
import inspect
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud  # noqa: E402
import batch_manifest as bm  # noqa: E402
import fleet_analytics as fa  # noqa: E402
import fleet_parity as fp  # noqa: E402
import gitenv  # noqa: E402

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
_GITENV = _SCRIPTS / "gitenv.py"

# Every GIT_* name the scrub is contracted to remove: git's 15 repo-local vars plus the 2
# repo-SCOPING vars git does not class as local-env but which still redirect discovery.
_EXPECTED_FALLBACK = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
    "GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS", "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
)
_EXPECTED_EXTRA = ("GIT_CEILING_DIRECTORIES", "GIT_NAMESPACE")


def _top_level_imports(path: Path) -> set[str]:
    """Root package names imported by `path`, from the AST (never by running it)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            if node.level:                       # a relative import is a package edge
                names.add(f".{node.module or ''}")
            elif node.module:
                names.add(node.module.split(".")[0])
    return names


def _defines(path: Path, name: str) -> bool:
    """Does `path` contain a real `def <name>` (as opposed to an alias assignment)?"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name
               for n in ast.walk(tree))


# --- the invariant that makes consolidation legal ---------------------------

def test_gitenv_is_a_leaf_module():
    """Stdlib-only, ZERO repo imports — the property `audit.py`'s lazy-import constraint
    rests on. If this fails, `audit.py` has acquired an import-path dependency it was
    explicitly designed not to have, and the fix is to move the offending code OUT of
    gitenv, never to relax this test."""
    sibling_modules = {p.stem for p in _SCRIPTS.glob("*.py")} - {"gitenv"}
    sibling_packages = {p.name for p in _SCRIPTS.iterdir()
                        if p.is_dir() and (p / "__init__.py").exists()}
    repo_names = sibling_modules | sibling_packages | {"scripts", "deploy", "tests"}

    imported = _top_level_imports(_GITENV)
    assert not (imported & repo_names), f"gitenv is no longer a leaf: {sorted(imported & repo_names)}"
    assert not any(n.startswith(".") for n in imported), "gitenv must not use relative imports"

    # Stdlib-only: nothing third-party either (a dependency would make the leaf install-gated).
    assert imported <= {"__future__", "os", "subprocess"}, f"unexpected imports: {sorted(imported)}"


def test_the_scrub_is_defined_exactly_once():
    """`gitenv` defines the pair; the consumers ALIAS it. A re-grown local `def` in a
    consumer is the three-hand-copies state [#396] retired."""
    assert _defines(_GITENV, "git_location_env")
    assert _defines(_GITENV, "scrubbed_git_env")

    for consumer in ("audit.py", "fleet_parity.py", "fleet_analytics.py"):
        path = _SCRIPTS / consumer
        assert not _defines(path, "_git_location_env"), f"{consumer} re-grew a local scrub definition"

    # ...and at runtime the aliases really resolve to THIS file, not to a look-alike.
    #
    # Asserted on the defining FILE rather than on object identity (terra HIGH, 2026-08-08).
    # `import gitenv` and `from scripts import gitenv` name the same file but produce two
    # distinct module objects when both `scripts/` and the repo root are importable — which
    # `python -m pytest` from the repo root really does. Object identity therefore encoded
    # the import LAYOUT, not the invariant; the invariant is that there is one DEFINITION.
    # (The consumers prefer the bare name precisely so the objects also converge in practice,
    # but this assertion must hold either way, and two caches are behaviourally identical.)
    for alias in (aud._git_location_env, fp._git_location_env, fp._scrubbed_git_env):
        assert Path(inspect.getfile(alias)).resolve() == _GITENV.resolve(), \
            f"{alias.__qualname__} is not defined in gitenv.py"
    assert fp._GIT_LOCATION_ENV_FALLBACK == gitenv.GIT_LOCATION_ENV_FALLBACK
    assert aud._GIT_LOCATION_ENV_EXTRA == gitenv.GIT_LOCATION_ENV_EXTRA


def test_every_consumer_resolves_the_same_gitenv_file():
    """All four git callers — including [#512]'s `batch_manifest` — read ONE definition.
    Whichever spelling their dual-mode import lands on, it must be THIS file."""
    for mod in (aud._gitenv, fp._gitenv, bm._gitenv, fa.gitenv):
        assert Path(mod.__file__).resolve() == _GITENV.resolve(), mod


def test_the_dual_mode_import_prefers_the_bare_name():
    """terra HIGH, 2026-08-08. Both spellings resolve the same file but yield two distinct
    module objects (two caches) when `scripts/` AND the repo root are both importable —
    `python -m pytest` from the repo root does exactly that. Trying the BARE name first
    makes every consumer that can see `scripts/` converge on one object; the package-mode
    branch is reached only where no bare-name consumer can exist to disagree.

    Asserted on source order, because the failure it prevents is invisible at runtime in
    whichever layout the suite happens to be run under."""
    for mod in ("audit.py", "fleet_parity.py", "batch_manifest.py"):
        src = (_SCRIPTS / mod).read_text(encoding="utf-8")
        bare = src.index("import gitenv as _gitenv")
        pkg = src.index("from scripts import gitenv as _gitenv")
        assert bare < pkg, f"{mod} tries the package spelling first — see terra 2026-08-08"


# --- semantics: byte-equivalent to the copy this replaced -------------------

def test_the_pinned_name_set_is_unchanged_by_the_move():
    """The 15 + 2. Pinned literally so a "cleanup" that drops a name has to face this list."""
    assert gitenv.GIT_LOCATION_ENV_FALLBACK == _EXPECTED_FALLBACK
    assert gitenv.GIT_LOCATION_ENV_EXTRA == _EXPECTED_EXTRA
    assert len(_EXPECTED_FALLBACK) == 15

    scrub = gitenv.git_location_env()
    assert set(_EXPECTED_FALLBACK) | set(_EXPECTED_EXTRA) <= scrub


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="git not available")
def test_the_derived_set_still_covers_gits_own_local_env_var_list():
    """Derived from git, never hand-maintained: the first hand-written version of this list
    omitted 8 of git's 15. Kept here as well as in test_fleet_parity so the contract is
    asserted against the DEFINITION, not only against one consumer's alias."""
    r = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        pytest.skip("git could not report --local-env-vars")
    canonical = {ln.strip() for ln in r.stdout.split() if ln.strip()}
    assert canonical <= gitenv.git_location_env(), \
        f"not scrubbed: {sorted(canonical - gitenv.git_location_env())}"


def test_scrubbed_env_strips_the_location_vars_and_keeps_everything_else(monkeypatch):
    """The whole point: `cwd=`/`-C` decides which repo, because nothing in the env can
    override it. Scrubbed BY NAME — the identity/transport/config vars below are PRESERVED,
    and a `startswith("GIT_")` strip would silently eat every one of them."""
    for name in _EXPECTED_FALLBACK + _EXPECTED_EXTRA:
        monkeypatch.setenv(name, f"/foreign/{name}")
    preserved = {
        "GIT_AUTHOR_NAME": "a", "GIT_AUTHOR_DATE": "d", "GIT_COMMITTER_NAME": "c",
        "GIT_COMMITTER_DATE": "d", "GIT_CONFIG_GLOBAL": "g", "GIT_CONFIG_SYSTEM": "s",
        "GIT_SSH_COMMAND": "ssh", "GIT_TERMINAL_PROMPT": "0", "PATH_LIKE_SENTINEL": "keep",
    }
    for k, v in preserved.items():
        monkeypatch.setenv(k, v)

    env = gitenv.scrubbed_git_env()

    for name in _EXPECTED_FALLBACK + _EXPECTED_EXTRA:
        assert name not in env, f"{name} survived the scrub"
    for k, v in preserved.items():
        assert env[k] == v, f"{k} was scrubbed but must be preserved"


def test_fleet_analytics_scrub_is_the_same_scrub():
    """`fleet_analytics` kept its own wrapper name; it must not have kept its own SET.
    (It used to cache `audit._git_location_env()` in a second module-level cache.)"""
    assert fa._scrubbed_git_env().keys() == gitenv.scrubbed_git_env().keys()
    assert not any(isinstance(n, ast.Assign) and any(
        getattr(t, "id", "") == "_SCRUB_CACHE" for t in n.targets)
        for n in ast.walk(ast.parse((_SCRIPTS / "fleet_analytics.py").read_text(encoding="utf-8"))))


# --- WHERE the scrub fires is unchanged -------------------------------------

def test_the_deliberate_git_index_file_path_is_not_scrubbed():
    """`_commit_routine_outputs` sets GIT_INDEX_FILE ON PURPOSE (it commits to a detached
    automation branch through a temp index). [#396] moved where the scrub LIVES, never where
    it FIRES — this path must still build its own env and never route through the scrub."""
    src = inspect.getsource(aud._commit_routine_outputs)
    assert "GIT_INDEX_FILE=tmp_index" in src, "the deliberate temp-index env no longer exists"
    assert "_git_location_env" not in src, "the deliberate GIT_INDEX_FILE path acquired the scrub"
    assert "_scrubbed_git_env" not in src


def test_the_scrub_still_fires_where_it_always_did():
    """The three `audit.py` sites that DO scrub keep scrubbing. Asserted on source rather
    than behaviour because two of them are network/worktree paths a unit test cannot drive."""
    for fn in (aud._select_active_bundle, aud.check_fleet_audit_replication,
               aud._push_routine_branch):
        assert "_git_location_env()" in inspect.getsource(fn), f"{fn.__name__} lost its scrub"
