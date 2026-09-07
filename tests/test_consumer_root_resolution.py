"""[#605] — consumer-root resolution is explicit in BOTH modules, sibling-LAST.

The premise the row was opened on: on any substrate that is not the operator's laptop
there is no `Dev/` sibling tree, so neither instantiation (`deploy/tool.py`) nor
measurement (`scripts/audit.py`) of a consumer is reachable. Verified at HEAD before the
fix, and the two modules were NOT the same defect:

- `deploy/tool.py::resolve_repo_root` was UNCONDITIONAL — `return (hub_root.parent /
  repo).resolve()`, no escape of any kind;
- `scripts/audit.py::resolve_repo_path` already honoured a stored per-repo path first and
  only then fell back to the sibling — but that stored path lives in
  `ecosystem/<repo>/state.yaml`, which is **gitignored**, so on a fresh checkout the
  fallback is all there is and the outcome is identical.

Both now implement the same four-step precedence over the same env vars and the same
registry file: explicit argument -> `DEV_KNOWLEDGE_REPO_ROOT_<SLUG>` -> the registry
entry -> the sibling default (whose parent is `DEV_KNOWLEDGE_FLEET_ROOT` when set).

Two things this file is careful about, because getting either wrong makes the tests lie:

- **Nothing is moved on disk.** Every non-sibling layout is built under `tmp_path`, and
  the resolvers are driven with an INJECTED environment mapping (`env=`) or a
  monkeypatched module root — never by mutating the ambient process environment.
- **Nothing shells out to git.** `GIT_DIR` overrides both `cwd=` and `-C`, so a test that
  ran git would silently read the developer's own repo. The one test that exercises the
  `audit repo <name>` command drives its callback with the git-touching writers injected
  out, exactly as `tests/test_writer_integrity.py` does.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

import audit as aud
import tool


# ---------------------------------------------------------------------------
# Shared: the env-var name is DERIVED from the registry key, not listed.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module", [tool, aud], ids=["deploy_tool", "audit"])
@pytest.mark.parametrize(
    "repo, expected",
    [
        ("ai-council", "DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL"),
        ("corp-monorepo", "DEV_KNOWLEDGE_REPO_ROOT_CORP_MONOREPO"),
        ("corp-sca-time-automation", "DEV_KNOWLEDGE_REPO_ROOT_CORP_SCA_TIME_AUTOMATION"),
        (".dev-knowledge", "DEV_KNOWLEDGE_REPO_ROOT_DEV_KNOWLEDGE"),
    ],
)
def test_env_var_name_is_derived_from_the_registry_key(module, repo, expected):
    """A newly registered consumer needs no code change to become overridable.

    Both modules must derive the SAME name, or an operator who sets one variable would
    move one module's answer and not the other's -- worse than neither honouring it.
    """
    assert module.repo_root_env_var(repo) == expected


def test_both_modules_agree_on_the_env_var_constants():
    """The two resolvers are deliberately NOT folded; the constants are what bind them."""
    assert tool.FLEET_ROOT_ENV == aud.FLEET_ROOT_ENV == "DEV_KNOWLEDGE_FLEET_ROOT"
    assert tool.REPO_ROOT_ENV_PREFIX == aud.REPO_ROOT_ENV_PREFIX


# ---------------------------------------------------------------------------
# deploy/tool.py::resolve_repo_root
# ---------------------------------------------------------------------------


def _hub_with_no_siblings(tmp_path: Path) -> Path:
    """A hub checkout whose parent holds nothing else -- the off-laptop substrate."""
    hub = tmp_path / "substrate" / ".dev-knowledge"
    (hub / "ecosystem").mkdir(parents=True)
    return hub


def test_deploy_sibling_default_is_unchanged_when_nothing_is_set(tmp_path):
    """The regression guard: a caller passing nothing behaves exactly as before [#605]."""
    hub = _hub_with_no_siblings(tmp_path)

    resolved = tool.resolve_repo_root("ai-council", hub, env={})

    assert resolved == (hub.parent / "ai-council").resolve()


def test_deploy_resolves_a_non_sibling_layout_from_the_environment(tmp_path):
    """The done-item: a consumer that is NOT a sibling resolves, with no sibling tree."""
    hub = _hub_with_no_siblings(tmp_path)
    elsewhere = tmp_path / "srv" / "checkouts" / "ai-council"
    elsewhere.mkdir(parents=True)
    assert not (hub.parent / "ai-council").exists(), "the sibling layout must be absent"

    resolved = tool.resolve_repo_root(
        "ai-council", hub, env={"DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL": str(elsewhere)}
    )

    assert resolved == elsewhere.resolve()


def test_deploy_resolves_a_non_sibling_layout_from_the_registry(tmp_path):
    """Step 3: `path:` in ecosystem/<repo>/state.yaml, the fleet's existing path registry."""
    hub = _hub_with_no_siblings(tmp_path)
    elsewhere = tmp_path / "srv" / "ai-council"
    elsewhere.mkdir(parents=True)
    state = hub / "ecosystem" / "ai-council" / "state.yaml"
    state.parent.mkdir(parents=True)
    state.write_text(f"path: {elsewhere}\n", encoding="utf-8")

    assert tool.registry_repo_root("ai-council", hub) == elsewhere
    assert tool.resolve_repo_root("ai-council", hub, env={}) == elsewhere.resolve()


def test_deploy_fleet_root_relocates_the_sibling_parent(tmp_path):
    """Step 4 keeps the sibling SHAPE while moving what `<dev>` means."""
    hub = _hub_with_no_siblings(tmp_path)
    fleet = tmp_path / "fleet"
    (fleet / "ai-council").mkdir(parents=True)

    resolved = tool.resolve_repo_root(
        "ai-council", hub, env={"DEV_KNOWLEDGE_FLEET_ROOT": str(fleet)}
    )

    assert resolved == (fleet / "ai-council").resolve()


def test_deploy_precedence_is_explicit_then_env_then_registry_then_sibling(tmp_path):
    """All four steps armed at once: each higher step must beat every lower one."""
    hub = _hub_with_no_siblings(tmp_path)
    explicit = tmp_path / "explicit"
    from_env = tmp_path / "from-env"
    from_registry = tmp_path / "from-registry"
    for p in (explicit, from_env, from_registry, hub.parent / "ai-council"):
        p.mkdir(parents=True, exist_ok=True)
    state = hub / "ecosystem" / "ai-council" / "state.yaml"
    state.parent.mkdir(parents=True)
    state.write_text(f"path: {from_registry}\n", encoding="utf-8")
    env = {"DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL": str(from_env)}

    assert tool.resolve_repo_root(
        "ai-council", hub, explicit=explicit, env=env
    ) == explicit.resolve()
    assert tool.resolve_repo_root("ai-council", hub, env=env) == from_env.resolve()
    assert tool.resolve_repo_root("ai-council", hub, env={}) == from_registry.resolve()
    state.unlink()
    assert tool.resolve_repo_root("ai-council", hub, env={}) == (
        hub.parent / "ai-council"
    ).resolve()


@pytest.mark.parametrize(
    "body", ["", "not a mapping\n", "path:\n", "path: '   '\n", "{oh no\n"]
)
def test_deploy_registry_step_is_fail_soft(tmp_path, body):
    """An absent / empty / malformed state file contributes nothing; it is not an error.

    Fail-soft matters here: state.yaml is gitignored, so "missing" is the NORMAL case on a
    fresh checkout. A raise would make the sibling fallback unreachable.
    """
    hub = _hub_with_no_siblings(tmp_path)
    state = hub / "ecosystem" / "ai-council" / "state.yaml"
    state.parent.mkdir(parents=True)
    state.write_text(body, encoding="utf-8")

    assert tool.registry_repo_root("ai-council", hub) is None
    assert tool.resolve_repo_root("ai-council", hub, env={}) == (
        hub.parent / "ai-council"
    ).resolve()


def test_deploy_hub_resolves_to_itself(tmp_path):
    """What the sibling rule already produced for the default root, stated explicitly."""
    hub = _hub_with_no_siblings(tmp_path)

    assert tool.resolve_repo_root(hub.name, hub, env={}) == hub.resolve()


# ---------------------------------------------------------------------------
# scripts/audit.py::resolve_repo_path
# ---------------------------------------------------------------------------


def test_audit_sibling_default_is_unchanged_when_nothing_is_set(monkeypatch, tmp_path):
    """The regression guard for the gate module: no override set == pre-[#605] behaviour."""
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))

    assert aud.resolve_repo_path("ai-council", None, env={}) == hub.parent / "ai-council"


def test_audit_resolves_a_non_sibling_layout_from_the_environment(monkeypatch, tmp_path):
    """The done-item, audit side: a non-sibling consumer resolves with no sibling tree."""
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    elsewhere = tmp_path / "srv" / "checkouts" / "ai-council"
    elsewhere.mkdir(parents=True)
    assert not (hub.parent / "ai-council").exists(), "the sibling layout must be absent"

    resolved = aud.resolve_repo_path(
        "ai-council", None, env={"DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL": str(elsewhere)}
    )

    assert resolved == elsewhere.resolve()


def test_audit_fleet_root_relocates_the_sibling_parent(monkeypatch, tmp_path):
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    fleet = tmp_path / "fleet"
    (fleet / "ai-council").mkdir(parents=True)

    resolved = aud.resolve_repo_path(
        "ai-council", None, env={"DEV_KNOWLEDGE_FLEET_ROOT": str(fleet)}
    )

    assert resolved == fleet / "ai-council"


def test_audit_precedence_is_explicit_then_env_then_stored_then_sibling(
    monkeypatch, tmp_path
):
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    explicit = tmp_path / "explicit"
    from_env = tmp_path / "from-env"
    stored = tmp_path / "stored"
    for p in (explicit, from_env, stored):
        p.mkdir()
    env = {"DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL": str(from_env)}

    assert aud.resolve_repo_path(
        "ai-council", str(stored), explicit=str(explicit), env=env
    ) == explicit.resolve()
    assert aud.resolve_repo_path("ai-council", str(stored), env=env) == from_env.resolve()
    assert aud.resolve_repo_path("ai-council", str(stored), env={}) == stored
    assert aud.resolve_repo_path("ai-council", None, env={}) == hub.parent / "ai-council"


def test_audit_env_cannot_undo_the_hub_binding(monkeypatch, tmp_path):
    """[#465] must survive [#605]: no ENVIRONMENT may move the hub off its live tree.

    The hub short-circuit sits BELOW `explicit` (`--repo-path` already outranked it at the
    CLI) and ABOVE env + registry. If an env var could capture the hub, every hub-only
    check would skip as `n/a` from a mis-set shell -- the exact 14-WARN collapse [#465]
    closed, re-opened through a new door.
    """
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    decoy = tmp_path / "decoy"
    decoy.mkdir()
    env = {
        aud.repo_root_env_var(aud.HUB_REPO_NAME): str(decoy),
        "DEV_KNOWLEDGE_FLEET_ROOT": str(decoy),
    }

    assert aud.resolve_repo_path(aud.HUB_REPO_NAME, str(decoy), env=env) == Path(hub)
    assert aud.resolve_repo_path(
        aud.HUB_REPO_NAME, None, explicit=str(decoy), env=env
    ) == decoy.resolve()


def test_audit_repo_command_runs_from_a_checkout_with_no_sibling_tree(
    monkeypatch, tmp_path
):
    """Done-item 3, end to end at the command: `audit repo <name>` with NO sibling tree.

    Everything that would touch git or the real fleet is injected out (the
    `test_writer_integrity.py` pattern), so the command is exercised without shelling to
    git -- `GIT_DIR` overrides both `cwd=` and `-C`, and a real invocation here would read
    whichever repo the developer happens to be standing in.

    What is actually asserted is the thing the row cares about: the path `audit_repo`
    receives is the non-sibling consumer tree, reached with no `--repo-path` and no
    `state.yaml`.
    """
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    consumer = tmp_path / "srv" / "checkouts" / "ai-council"
    consumer.mkdir(parents=True)
    assert not (hub.parent / "ai-council").exists(), "the sibling layout must be absent"
    monkeypatch.setenv("DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL", str(consumer))

    audited: dict[str, Path] = {}

    def fake_audit_repo(name, path, run_date):
        audited[name] = Path(path)
        return aud.RepoState(
            name=name, path=str(path), last_audit="2026-08-28",
            findings=[aud.Finding("a_check", "pass", "fine")],
        )

    monkeypatch.setattr(aud, "load_state", lambda _n: None)
    monkeypatch.setattr(aud, "audit_repo", fake_audit_repo)
    monkeypatch.setattr(aud, "save_state", lambda _s: None)
    monkeypatch.setattr(aud, "append_history", lambda *_a, **_k: None)
    monkeypatch.setattr(aud, "generate_report", lambda *_a, **_k: "report")
    monkeypatch.setattr(aud, "write_report", lambda *_a, **_k: tmp_path / "r.md")
    monkeypatch.setattr(aud, "_commit_routine_outputs", lambda *_a, **_k: None)

    callback = getattr(aud.cmd_repo, "callback", aud.cmd_repo)
    callback("ai-council", None)

    assert audited["ai-council"] == consumer.resolve(), (
        "audit repo resolved to the sibling default -- on a substrate with no sibling "
        "tree the command would audit a path that does not exist ([#605])"
    )


def test_audit_run_bootstrap_path_outranks_the_environment(monkeypatch, tmp_path):
    """`run --repo-path` is an EXPLICIT answer and must not be demoted by the env var.

    Terra HIGH on the [#605] diff, and a regression the seam itself introduced: before
    [#605] the bootstrap path reached the resolver as `stored_path` (via the state.yaml
    the command has just written) and nothing outranked it. Adding the env var ABOVE the
    stored path silently inverted that -- `run --repo-path D:\\new\\repo` would register
    one tree and then audit whichever tree `DEV_KNOWLEDGE_REPO_ROOT_<SLUG>` named.

    The fix carries the bootstrapped (name, path) forward as `explicit` for that repo
    only, so this test fails if that carry is ever dropped.
    """
    hub = _hub_with_no_siblings(tmp_path)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(hub))
    bootstrap = tmp_path / "bootstrapped" / "ai-council"
    bootstrap.mkdir(parents=True)
    decoy = tmp_path / "from-env" / "ai-council"
    decoy.mkdir(parents=True)
    monkeypatch.setenv("DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL", str(decoy))

    audited: dict[str, Path] = {}

    def fake_audit_repo(name, path, run_date):
        audited[name] = Path(path)
        return aud.RepoState(
            name=name, path=str(path), last_audit="2026-08-28",
            findings=[aud.Finding("a_check", "pass", "fine")],
        )

    monkeypatch.setattr(aud, "discover_repos", lambda: ["ai-council"])
    monkeypatch.setattr(aud, "load_state", lambda _n: None)
    monkeypatch.setattr(aud, "audit_repo", fake_audit_repo)
    monkeypatch.setattr(aud, "save_state", lambda _s: None)
    monkeypatch.setattr(aud, "append_history", lambda *_a, **_k: None)
    monkeypatch.setattr(aud, "generate_report", lambda *_a, **_k: "report")
    monkeypatch.setattr(aud, "write_report", lambda *_a, **_k: tmp_path / "r.md")
    monkeypatch.setattr(aud, "_commit_routine_outputs", lambda *_a, **_k: None)

    callback = getattr(aud.cmd_run, "callback", aud.cmd_run)
    callback(str(bootstrap))

    assert audited["ai-council"] == bootstrap.resolve(), (
        "the environment outranked the path the operator just bootstrapped -- the run "
        "registers one tree and audits another"
    )


# ---------------------------------------------------------------------------
# W2-F2 -- the `--consumer` spelling, and the WORKTREE consumer it exists for.
#
# [#605] landed the override MECHANISM (`explicit=` / `--repo-root`) on 2026-08-28,
# with the sixteen tests above. Two things it did not land:
#
# - the `--consumer <path>` spelling the deployment model's own record asks for;
# - any test at all over the case the override exists to serve -- a consumer whose
#   working tree is a WORKTREE, which never sits at `<dev>/<repo>`.
#
# The second gap is recorded in prose rather than under a gate. `ecosystem/
# deployed-versions.yaml`, in the `win-tooling:` block, explains why that deploy's
# record was hand-written instead of earned by `deploy/tool.py --execute`: "the
# RULING-W shape binds the deploy to a consumer WORKTREE and the tool resolves the
# consumer as `hub_root.parent / repo` with no override -- so the lane drove the
# tool's own carriers against the worktree". These tests put that sentence under a
# gate, so the next lane meets a failing assertion rather than a paragraph.
# ---------------------------------------------------------------------------


def _consumer_with_a_worktree(tmp_path: Path) -> tuple[Path, Path, Path]:
    """A hub, a sibling consumer checkout, and that consumer's WORKTREE.

    The worktree sits where `claude --worktree` puts it -- `<consumer>/.claude/
    worktrees/<lane>` -- which is precisely NOT `<dev>/<repo>`. The sibling layout
    built here is entirely correct; that is the point. Step 4 still cannot name the
    tree the deploy has to bind to.
    """
    hub = tmp_path / "substrate" / ".dev-knowledge"
    (hub / "ecosystem").mkdir(parents=True)
    consumer = hub.parent / "win-tooling"
    worktree = consumer / ".claude" / "worktrees" / "lane-w-000-example"
    worktree.mkdir(parents=True)
    return hub, consumer, worktree


def test_deploy_sibling_default_cannot_name_a_worktree_consumer(tmp_path):
    """The obstacle itself, under a gate: step 4 answers the CHECKOUT, never a worktree."""
    hub, consumer, worktree = _consumer_with_a_worktree(tmp_path)

    resolved = tool.resolve_repo_root("win-tooling", hub, env={})

    assert resolved == consumer.resolve()
    assert resolved != worktree.resolve()


def test_deploy_explicit_override_reaches_a_worktree_consumer(tmp_path):
    """...and step 1 is what reaches it -- the reason the override exists at all."""
    hub, consumer, worktree = _consumer_with_a_worktree(tmp_path)

    resolved = tool.resolve_repo_root("win-tooling", hub, explicit=worktree, env={})

    assert resolved == worktree.resolve()
    assert resolved != consumer.resolve()


@pytest.mark.parametrize("spelling", ["--repo-root", "--consumer"])
def test_deploy_cli_both_spellings_thread_a_worktree_into_preflight(
    monkeypatch, tmp_path, spelling
):
    """Both spellings are ONE option: each reaches `preflight(repo_root=...)` verbatim.

    Driven against a worktree path, so this covers the CLI half of the case above.
    `preflight` is replaced rather than run: what is measured here is the threading,
    and the real gates would shell out to git against a tmp_path that is no checkout.
    """
    _, _, worktree = _consumer_with_a_worktree(tmp_path)
    seen: dict[str, object] = {}

    def _capture(repo, version, **kwargs):
        seen["repo"] = repo
        seen["repo_root"] = kwargs.get("repo_root", "ABSENT")
        raise tool.PreflightError("threading is what this test measures")

    monkeypatch.setattr(tool, "preflight", _capture)

    res = CliRunner().invoke(
        tool.deploy, ["win-tooling", "--target", "v1.4.0", spelling, str(worktree)]
    )

    assert "No such option" not in res.output
    assert seen["repo"] == "win-tooling"
    assert seen["repo_root"] == str(worktree)


def test_deploy_cli_default_is_unchanged_when_no_spelling_is_passed(monkeypatch):
    """The regression guard: a caller passing neither spelling still sends None.

    `--consumer` is an added SPELLING of an existing option, not a new resolution
    step. Every carrier invocation that passes nothing must keep resolving through
    env -> registry -> sibling exactly as it did before this lane.
    """
    seen: dict[str, object] = {}

    def _capture(repo, version, **kwargs):
        seen["repo_root"] = kwargs.get("repo_root", "ABSENT")
        raise tool.PreflightError("threading is what this test measures")

    monkeypatch.setattr(tool, "preflight", _capture)

    CliRunner().invoke(tool.deploy, ["win-tooling", "--target", "v1.4.0"])

    assert seen["repo_root"] is None
