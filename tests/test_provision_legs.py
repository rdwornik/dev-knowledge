"""[#746] tests for the two restored provisioning legs — B1 history, L5 ecosystem.

RESTORED, NOT REWRITTEN. These are `tests/test_cloud_provisioning.py`'s history and ecosystem
cases, carried across at `3c9418cc^` when `[#746]` restored the legs into
`scripts/provision_legs.py`. They are kept because each one pins a MEASURED finding from the
2026-08-21 terra rounds — several of them CRITICAL data-loss paths (a diverged ref force-updated,
a rewound remote swallowing local commits, a write escaping the checkout through a symlink) — and
a restoration that dropped them would restore the code without the reasons it looks the way it
does. The prebuild cases are NOT carried: `prebuild` is not one of `[#746]`'s legs and
`scripts/provision_legs.py` does not implement it.

The history tests build REAL git repositories rather than mocking `subprocess`: the whole
finding this module exists for — that a clone can carry full depth and still not resolve `main` —
is a property of git's ref layout, and a mock of git cannot be wrong about it in the same way git
is. Each test therefore constructs the exact clone shape the proof lane measured and asserts the
guard's verdict on it.
"""
from __future__ import annotations

import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import provision_legs as cp  # noqa: E402


# --- fixtures: real repositories, real clone shapes ---------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
    return r


def _commit(root: Path, name: str) -> None:
    (root / name).write_text(name, encoding="utf-8")
    _git(root, "add", name)
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", name)


@pytest.fixture
def origin(tmp_path: Path) -> Path:
    """An upstream repo with a few commits on `main` and one other branch."""
    root = tmp_path / "origin"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    for n in ("a", "b", "c"):
        _commit(root, n)
    _git(root, "branch", "worktree-lane-probe")
    return root


def _config(tmp_path: Path, **history: object) -> Path:
    """Write a minimal, schema-valid declaration and return its path."""
    body: dict[str, object] = {
        "schema": cp.CONFIG_SCHEMA,
        "history": {"disposition": "repair", "required_refs": ["main"], **history},
        "ecosystem": {"self_register": True, "self_name": ".dev-knowledge"},
        # The `prebuild` block is deliberately ABSENT. The live declaration still carries one,
        # and the loader must neither read it nor trip over it — `test_the_live_declaration_loads`
        # is the other half of that pair.
    }
    path = tmp_path / "provisioning.yaml"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    return path


# --- config ---------------------------------------------------------------------------------


def test_load_config_reads_every_block(tmp_path: Path) -> None:
    cfg = cp.load_config(_config(tmp_path))
    assert cfg.history.disposition == "repair"
    assert cfg.history.required_refs == ("main",)
    assert cfg.ecosystem.self_register is True
    assert cfg.ecosystem.self_name == ".dev-knowledge"


def test_load_config_refuses_a_foreign_schema(tmp_path: Path) -> None:
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({"schema": "something/else"}), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match="schema"):
        cp.load_config(path)


def test_load_config_refuses_an_off_enum_disposition(tmp_path: Path) -> None:
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["history"]["disposition"] = "ignore"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match="disposition"):
        cp.load_config(path)


@pytest.mark.parametrize(("block", "key"), [
    ("ecosystem", "self_register"),
])
@pytest.mark.parametrize("bad", ["false", "no", "0", 0, 1, None])
def test_load_config_refuses_a_non_boolean_where_a_boolean_is_meant(
        tmp_path: Path, block: str, key: str, bad: object) -> None:
    """`bool("false")` is True (terra HIGH round 4, 2026-08-21).

    A declaration written `self_register: "false"` — quoted by hand, or by a generator that
    stringifies — silently meant the opposite, and on `self_register` that AUTHORISES a tree
    mutation the declaration meant to forbid. Refusing to read the file is the lesser harm, and
    it is a could-not-look, so it raises.
    """
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body[block][key] = bad
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match=key):
        cp.load_config(path)


def test_load_config_accepts_real_yaml_booleans(tmp_path: Path) -> None:
    """The discrimination, not just the refusal: genuine booleans still load."""
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["ecosystem"]["self_register"] = False
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    assert cp.load_config(path).ecosystem.self_register is False


@pytest.mark.parametrize(("block", "key"), [
    ("history", "required_refs"),
    ("history", "spine_walking_instruments"),
])
@pytest.mark.parametrize("bad", ["main", 42, {"a": 1}, ["", "main"], [None]])
def test_load_config_refuses_a_scalar_where_a_list_is_meant(
        tmp_path: Path, block: str, key: str, bad: object) -> None:
    """`tuple("main")` is `("m","a","i","n")` (terra HIGH round 7, 2026-08-21).

    A declaration written `required_refs: main` instead of a list produced four one-character
    ref names and four false exit-1 violations — a malformed configuration reported as
    positively observed drift, which is the exact confusion the 1/2 split exists to prevent.
    """
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body[block][key] = bad
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match=key):
        cp.load_config(path)


def test_load_config_refuses_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(cp.ProvisioningError, match="not found"):
        cp.load_config(tmp_path / "absent.yaml")


def test_the_live_declaration_loads() -> None:
    """The declaration this repo actually ships must satisfy its own loader."""
    cfg = cp.load_config()
    assert cfg.history.disposition in cp.DISPOSITIONS
    assert "main" in cfg.history.required_refs
    # Every enumerated spine walker is a file that exists — an enum naming a deleted script
    # would make `disposition: exclude` unfalsifiable.
    for instrument in cfg.history.spine_walking_instruments:
        assert (cp.REPO_ROOT / instrument).exists(), instrument


# --- history: the measured clone shapes ---------------------------------------------------


def test_full_clone_from_the_default_branch_is_already_sufficient(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "full"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert report.ok
    assert report.shallow is False
    assert report.refs["main"] == 3


def test_a_shallow_clone_is_refused(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", "file://" + str(origin).replace("\\", "/"), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("SHALLOW" in v for v in report.violations)


def test_the_measured_failure_full_depth_but_no_local_main(tmp_path: Path, origin: Path) -> None:
    """THE finding: depth is restored, `main` still does not resolve, so a spine walker errors.

    This is the shape `docs/audits/2026-08-19-technical-554-proof.md` §3 recorded — 5329 commits
    reachable and `fatal: Not a valid object name main`. Leg 2 alone reports such a clone clean.
    """
    clone = tmp_path / "branch-only"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.is_shallow(clone) is False           # leg 2's predicate is satisfied ...
    report = cp.assess_history(clone, cfg)
    assert not report.ok                            # ... and the clone is still unusable
    assert report.refs["main"] is None
    assert any("does not resolve" in v for v in report.violations)


def test_repair_restores_the_missing_ref(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "repairable"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.repair_history(clone, cfg)
    assert report.ok, report.violations
    assert report.refs["main"] == 3
    assert any("refs/heads/main" in a for a in report.actions)


def test_repair_is_idempotent_and_says_so(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "twice"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    cp.repair_history(clone, cfg)
    second = cp.repair_history(clone, cfg)
    assert second.ok
    assert second.actions == []


def test_a_repair_on_an_already_sufficient_clone_touches_NOTHING(
        tmp_path: Path, origin: Path) -> None:
    """A reported no-op must actually be one (terra HIGH round 6, 2026-08-21).

    An earlier version force-refreshed the remote-tracking refs on every repair run and
    deliberately left that out of `actions` — so a clean second run wrote `FETCH_HEAD` and could
    move `origin/<ref>` while reporting "no-op", which is a mutation hidden behind the very
    idempotency claim C1 exists to make checkable. The currency check reads `ls-remote`, so an
    accurate assessment needs no fetch at all.
    """
    clone = tmp_path / "already-fine"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    fetch_head = clone / ".git" / "FETCH_HEAD"
    if fetch_head.exists():
        fetch_head.unlink()
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.repair_history(clone, cfg)
    assert report.ok, report.violations
    assert report.actions == []
    assert not fetch_head.exists(), "the 'no-op' repair fetched"


def test_repair_updates_a_stale_ref_by_compare_and_swap_not_by_force_fetch(
        tmp_path: Path, origin: Path) -> None:
    """THE race guard (terra CRITICAL round 6, 2026-08-21).

    A `+refs/heads/<ref>:refs/heads/<ref>` refspec writes whatever the remote holds AT FETCH TIME
    straight over the local branch, so a force-push landing between the classification and the
    fetch could discard local commits despite the divergence guard having just approved. The
    repair now fetches into the tracking ref and moves the local one with
    `git update-ref <ref> <new> <old>`, which refuses if the local ref changed underneath it.
    """
    clone = tmp_path / "cas"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _git(clone, "update-ref", "refs/heads/main", "HEAD~2")
    _commit(origin, "d")
    cfg = cp.load_config(_config(tmp_path)).history

    # Observe the git commands ACTUALLY RUN, not what the report says was run: an earlier version
    # of this test searched `report.actions`, which a force-fetch omitted from that list would
    # have passed straight through, leaving the CRITICAL regression unprotected (terra HIGH round
    # 7, 2026-08-21).
    seen: list[tuple[str, ...]] = []
    real_git = cp._git

    def _spy(root: Path, *args: str) -> subprocess.CompletedProcess:
        seen.append(args)
        return real_git(root, *args)

    cp._git = _spy
    try:
        report = cp.repair_history(clone, cfg)
    finally:
        cp._git = real_git

    assert report.ok, report.violations
    assert report.refs["main"] == 4
    fetches = [a for a in seen if a and a[0] == "fetch"]
    assert fetches, seen
    # No fetch may name a LOCAL branch as its destination — that is the force-write this replaced.
    for args in fetches:
        for token in args:
            assert not token.endswith(":refs/heads/main"), args
    assert any(a and a[0] == "update-ref" for a in seen), seen
    assert any(a.startswith("git update-ref refs/heads/main") for a in report.actions), \
        report.actions


def test_a_remote_rewound_between_the_check_and_the_fetch_never_moves_the_local_ref(
        tmp_path: Path, origin: Path) -> None:
    """CAS protects the LOCAL ref; it says nothing about the remote (terra CRITICAL round 7).

    A force-push to an ANCESTOR between `ls-remote` and the fetch makes the arriving tip
    `current` — at which point compare-and-swap succeeds, because the local SHA is exactly what
    was observed, and the update rewinds the branch and discards its newer commits. Only a
    `behind` classification may move the ref.
    """
    clone = tmp_path / "rewound"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _commit(origin, "d")
    # Fetch first so the upstream tip is already an object here: the classification must reach
    # `behind`, which is the only state that authorises an update and therefore the only one from
    # which a rewind can do damage.
    _git(clone, "fetch", "-q", "origin")
    _git(clone, "update-ref", "refs/heads/main", "HEAD~1")     # local main is legitimately behind
    cfg = cp.load_config(_config(tmp_path)).history

    # THE WINDOW IS BETWEEN THE CLASSIFICATION AND THE FETCH, so the rewind has to land there —
    # not during the earlier read-only assessment, which would merely make the repair see the
    # rewound tip and classify it correctly (terra HIGH round 8, 2026-08-21: an earlier version
    # of this test rewound on the FIRST `live_remote_sha` call and so never entered the window
    # it claimed to cover).
    real_git = cp._git
    seen: list[tuple[str, ...]] = []
    rewound: list[bool] = []

    def _rewind_just_before_the_fetch(root: Path, *args: str) -> subprocess.CompletedProcess:
        if args and args[0] == "fetch" and not rewound:
            _git(origin, "update-ref", "refs/heads/main", "HEAD~3")   # force-push to an ancestor
            rewound.append(True)
        seen.append(args)
        return real_git(root, *args)

    local_before = _git(clone, "rev-parse", "refs/heads/main").stdout.strip()
    cp._git = _rewind_just_before_the_fetch
    try:
        cp.repair_history(clone, cfg)
    finally:
        cp._git = real_git

    assert rewound, "the rewind never fired — the race window was not entered"
    assert any(a and a[0] == "fetch" for a in seen), seen
    assert not any(a and a[0] == "update-ref" for a in seen), \
        "the local ref was updated from a tip that is not ahead of it"
    after = _git(clone, "rev-parse", "refs/heads/main").stdout.strip()
    assert after == local_before, "the local ref was rewound onto a force-pushed ancestor"


def test_repair_of_a_shallow_clone_deepens_it(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "deepen"
    _git(tmp_path, "clone", "-q", "--depth", "1", "file://" + str(origin).replace("\\", "/"), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.repair_history(clone, cfg)
    assert report.ok, report.violations
    assert "git fetch --unshallow" in report.actions
    assert report.refs["main"] == 3


def test_a_clone_with_no_remote_cannot_be_repaired_and_that_is_exit_2(
        tmp_path: Path, origin: Path) -> None:
    """"Nothing to repair from" is could-not-look, not drift (terra HIGH, 2026-08-21).

    The first version appended a violation here, so the CLI answered 1 — telling a caller the
    clone is wrong when the honest answer is that this environment gave the guard nothing to
    work with. The 1/2 split exists precisely to keep those apart.
    """
    clone = tmp_path / "orphan"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "remote", "remove", "origin")
    path = _config(tmp_path)

    with pytest.raises(cp.ProvisioningError, match="origin"):
        cp.repair_history(clone, cp.load_config(path).history)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_UNAVAILABLE


def test_an_unknown_required_ref_is_a_violation_not_a_crash(tmp_path: Path, origin: Path) -> None:
    """A ref no reachable clone carries IS positively observed — exit 1, not 2."""
    clone = tmp_path / "unknown-ref"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    path = _config(tmp_path, required_refs=["main", "no-such-branch"])

    report = cp.repair_history(clone, cp.load_config(path).history)
    assert not report.ok
    assert any("no-such-branch" in v for v in report.violations)
    assert report.refs["main"] == 3          # the ref that IS present still reports its length
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_VIOLATION


# --- history: the look-alike and the stale ref ---------------------------------------------


def test_a_tag_named_main_does_not_satisfy_the_required_ref(tmp_path: Path, origin: Path) -> None:
    """`git rev-parse main` resolves a TAG called `main`; the instruments mean the BRANCH.

    Accepting the look-alike would run a spine walk over whatever that tag points at and report
    clean — the vacuous-gate class this module exists to close (terra HIGH, 2026-08-21).
    """
    clone = tmp_path / "tagged"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "tag", "main", "HEAD")
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("does not resolve" in v for v in report.violations)


def test_a_stale_local_main_is_a_violation_and_repair_fast_forwards_it(
        tmp_path: Path, origin: Path) -> None:
    """A branch left behind its remote hides every spine entry in between."""
    clone = tmp_path / "stale"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _git(clone, "update-ref", "refs/heads/main", "HEAD~2")     # rewind the local branch only
    _commit(origin, "d")                                       # and move the upstream on
    _git(clone, "fetch", "-q", "origin")
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("BEHIND" in v for v in report.violations)

    repaired = cp.repair_history(clone, cfg)
    assert repaired.ok, repaired.violations
    assert repaired.refs["main"] == 4                           # a, b, c and the new d


def test_currency_is_reported_as_UNCOMPARED_when_there_is_no_remote_tracking_ref(
        tmp_path: Path, origin: Path) -> None:
    """No remote-tracking ref means not-compared, which is not the same fact as compared-clean."""
    clone = tmp_path / "local-only"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "remote", "remove", "origin")
    path = _config(tmp_path)

    report = cp.assess_history(clone, cp.load_config(path).history)
    assert report.ok                      # present and walkable — no violation is claimed
    assert report.uncompared == ["main"]  # ... and the limit of the check is stated
    # ... and the CLI says "could not look", not "clean" (terra HIGH round 2, 2026-08-21):
    # a stale local branch is indistinguishable from a current one when there is no remote.
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history"]) == cp.EXIT_UNAVAILABLE


def test_repair_fetches_the_remote_tracking_ref_so_currency_becomes_checkable(
        tmp_path: Path, origin: Path) -> None:
    """A `--single-branch` clone carries no `origin/main`; without this the repair would fetch
    the branch and leave currency permanently UNCOMPARED, so the check could never say clean."""
    clone = tmp_path / "single"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path)

    report = cp.repair_history(clone, cp.load_config(path).history)
    assert report.ok, report.violations
    assert report.uncompared == []
    # The tracking ref is refreshed as a convenience for the lane; the guard's own currency
    # answer comes from `ls-remote`, which is why the check below can succeed either way.
    assert cp.remote_ref(clone, "main") is not None
    assert cp.main(["--root", str(clone), "--config", str(path), "history"]) == cp.EXIT_OK


def test_a_DIVERGED_local_main_is_refused_and_never_force_updated(
        tmp_path: Path, origin: Path) -> None:
    """THE data-loss guard (terra CRITICAL, 2026-08-21).

    An earlier version asked only "is the remote an ancestor of local?" and treated every no as
    BEHIND, then force-fetched over it. A clone carrying an unpushed commit on local `main` would
    have lost the only reference to it the moment `origin/main` also advanced.
    """
    clone = tmp_path / "diverged"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _git(clone, "checkout", "-q", "main")
    _commit(clone, "local-only-work")                 # an unpushed commit on local main
    local_tip = _git(clone, "rev-parse", "refs/heads/main").stdout.strip()
    _git(clone, "checkout", "-q", "worktree-lane-probe")
    _commit(origin, "upstream-work")                  # and the upstream advances too
    _git(clone, "fetch", "-q", "origin")
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.ref_status(clone, "main", cp.remote_ref(clone, "main")) == cp.REF_DIVERGED
    report = cp.repair_history(clone, cfg)
    assert not report.ok
    assert any("DIVERGED" in v for v in report.violations)
    # The commit is still reachable: the repair refused rather than clobbering the ref.
    assert _git(clone, "rev-parse", "refs/heads/main").stdout.strip() == local_tip


def test_the_READ_ONLY_check_detects_a_stale_clone_without_fetching_anything(
        tmp_path: Path, origin: Path) -> None:
    """THE gate's soundness (terra HIGH round 4, 2026-08-21).

    Upstream advances; the clone never fetches, so its local `main` AND its cached
    `origin/main` are stale together — comparing the two finds them equal and reports clean.
    `--gate` runs exactly this read-only path on every container start, so a cache-based
    currency check meant a resumed container could pass while the spine walkers missed every
    commit added since. The comparison now asks the remote itself.
    """
    clone = tmp_path / "cached-stale"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _commit(origin, "d")
    _commit(origin, "e")

    # The clone has fetched nothing: both of its refs still say three commits.
    assert cp.spine_length(clone, "main") == 3
    assert cp.remote_ref(clone, "main") == _git(clone, "rev-parse", "refs/heads/main").stdout.strip()

    path = _config(tmp_path)
    cfg = cp.load_config(path).history
    report = cp.assess_history(clone, cfg)            # read-only, and it still catches it
    assert not report.ok
    assert any("BEHIND" in v for v in report.violations)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history"]) == cp.EXIT_VIOLATION

    repaired = cp.repair_history(clone, cfg)
    assert repaired.ok, repaired.violations
    assert repaired.refs["main"] == 5


def test_a_git_failure_is_never_reported_as_a_missing_ref_or_a_short_spine(
        tmp_path: Path, origin: Path) -> None:
    """Fatal git errors are could-not-look, not observed drift (terra HIGH round 8, 2026-08-21).

    `ref_resolves` treated every non-zero exit as "absent" and `spine_length` turned every failed
    walk into a violation — so a corrupt ref store or an unreadable object exited 1, telling the
    caller the clone is wrong when git simply could not answer.
    """
    clone = tmp_path / "corrupt"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    real_git = cp._git

    def _fatal(root: Path, *args: str) -> subprocess.CompletedProcess:
        if args[:2] == ("rev-parse", "--verify"):
            return subprocess.CompletedProcess(args, 128, "", "fatal: bad object")
        return real_git(root, *args)

    cp._git = _fatal
    try:
        with pytest.raises(cp.ProvisioningError, match="rev-parse"):
            cp.assess_history(clone, cp.load_config(_config(tmp_path)).history)
    finally:
        cp._git = real_git

    def _fatal_walk(root: Path, *args: str) -> subprocess.CompletedProcess:
        if args[:2] == ("log", "--first-parent"):
            return subprocess.CompletedProcess(args, 128, "", "fatal: unreadable object")
        return real_git(root, *args)

    cp._git = _fatal_walk
    try:
        with pytest.raises(cp.ProvisioningError, match="first-parent"):
            cp.assess_history(clone, cp.load_config(_config(tmp_path)).history)
    finally:
        cp._git = real_git

    path = _config(tmp_path)
    cp._git = _fatal
    try:
        assert cp.main(["--root", str(clone), "--config", str(path),
                        "history"]) == cp.EXIT_UNAVAILABLE
    finally:
        cp._git = real_git


def test_a_fatal_object_store_error_is_exit_2_and_mutates_nothing(
        tmp_path: Path, origin: Path) -> None:
    """A corrupt object store is not "the tip was never fetched" (terra HIGH round 9).

    `object_exists` folded every non-zero `cat-file` into False, so a fatal failure read as a
    missing remote tip — reported as drift on the read-only path, and ACTED ON with a fetch on
    the repair path. Only exit 1 (explicitly absent) may answer False.
    """
    clone = tmp_path / "bad-objects"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    path = _config(tmp_path)
    real_git = cp._git
    seen: list[tuple[str, ...]] = []

    def _fatal_cat_file(root: Path, *args: str) -> subprocess.CompletedProcess:
        seen.append(args)
        if args[:2] == ("cat-file", "-e"):
            return subprocess.CompletedProcess(args, 128, "", "fatal: unable to read object")
        return real_git(root, *args)

    cp._git = _fatal_cat_file
    try:
        assert cp.main(["--root", str(clone), "--config", str(path),
                        "history", "--repair"]) == cp.EXIT_UNAVAILABLE
    finally:
        cp._git = real_git

    assert not any(a and a[0] in ("fetch", "update-ref") for a in seen), seen


def test_an_unreachable_origin_is_exit_2_not_a_missing_branch(
        tmp_path: Path, origin: Path) -> None:
    """A transport failure is could-not-look; only `ls-remote` saying so means "no such branch".

    Before round 3 ANY failed fetch was reported as "origin has no such branch", so an auth
    failure, a DNS failure or an unreachable host all became exit 1 — a positively observed
    configuration violation asserted from a network error.
    """
    clone = tmp_path / "unreachable"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "remote", "set-url", "origin", str(tmp_path / "does-not-exist"))
    path = _config(tmp_path)

    with pytest.raises(cp.ProvisioningError):
        cp.repair_history(clone, cp.load_config(path).history)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_UNAVAILABLE


def test_a_remote_tip_reachable_only_via_a_SECOND_parent_is_refused_not_called_current(
        tmp_path: Path, origin: Path) -> None:
    """Generic ancestry is not first-parent coverage (terra HIGH round 5, 2026-08-21).

    Local `main` MERGES the upstream tip as a second parent, so `merge-base --is-ancestor` says
    it is contained — while `git log --first-parent main`, which is what every instrument in
    `spine_walking_instruments` runs, never traverses it. Reporting that clean is precisely the
    vacuous-gate condition this module exists to prevent.
    """
    clone = tmp_path / "second-parent"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "side")
    _commit(clone, "side-work")
    _commit(origin, "upstream-work")
    _git(clone, "fetch", "-q", "origin")
    upstream_tip = _git(clone, "rev-parse", "refs/remotes/origin/main").stdout.strip()
    # Rebuild local main as: side-work, then a merge whose SECOND parent is the upstream tip.
    _git(clone, "branch", "-f", "main", "side")
    _git(clone, "checkout", "-q", "main")
    _git(clone, "-c", "user.name=t", "-c", "user.email=t@t",
         "merge", "--no-ff", "-q", "-m", "merge upstream", upstream_tip)
    _git(clone, "checkout", "-q", "side")

    assert cp._is_ancestor(clone, upstream_tip, "refs/heads/main")          # contained ...
    assert not cp._on_first_parent_chain(clone, "refs/heads/main", upstream_tip)  # ... off-spine
    assert cp.ref_status(clone, "main", upstream_tip) == cp.REF_OFF_SPINE

    cfg = cp.load_config(_config(tmp_path)).history
    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("SECOND parent" in v for v in report.violations)


def test_a_local_main_AHEAD_of_origin_is_current_not_a_violation(
        tmp_path: Path, origin: Path) -> None:
    """Ahead is the normal workstation state and hides nothing from a spine walk."""
    clone = tmp_path / "ahead"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _commit(clone, "extra")
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.ref_status(clone, "main", cp.remote_ref(clone, "main")) == cp.REF_CURRENT
    assert cp.assess_history(clone, cfg).ok


# --- history: the exclusion disposition ---------------------------------------------------


def test_exclude_disposition_repairs_nothing_and_exits_clean(tmp_path: Path, origin: Path,
                                                             caplog: pytest.LogCaptureFixture) -> None:
    clone = tmp_path / "excluded"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path, disposition="exclude",
                   spine_walking_instruments=["scripts/validate_no_ff.py"])

    rc = cp.main(["--root", str(clone), "--config", str(path), "history", "--repair"])
    assert rc == cp.EXIT_OK
    assert "OUT OF SCOPE" in caplog.text
    assert "scripts/validate_no_ff.py" in caplog.text
    assert not cp.ref_resolves(clone, "main")     # it really did not repair


# --- exit codes: looked-and-failed vs could-not-look --------------------------------------


def test_history_check_exits_1_on_a_real_violation(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "violation"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path)
    assert cp.main(["--root", str(clone), "--config", str(path), "history"]) == cp.EXIT_VIOLATION


def test_an_unreadable_declaration_exits_2_not_1(tmp_path: Path) -> None:
    """Could-not-look and looked-and-failed must not share an exit code (F4)."""
    assert cp.main(["--config", str(tmp_path / "absent.yaml"), "history"]) == cp.EXIT_UNAVAILABLE


def test_history_check_exits_0_on_this_repo() -> None:
    """The live checkout satisfies its own precondition — the guard is not vacuously red."""
    assert cp.main(["--quiet", "history"]) == cp.EXIT_OK


# --- ecosystem -----------------------------------------------------------------------------


def test_registered_repos_counts_state_yaml_directories(tmp_path: Path) -> None:
    eco = tmp_path / "ecosystem"
    (eco / "alpha").mkdir(parents=True)
    (eco / "alpha" / "state.yaml").write_text("name: alpha\npath: /x\n", encoding="utf-8")
    (eco / "beta").mkdir()                       # a directory with no state.yaml does not count
    (eco / "schema").mkdir()
    assert cp.registered_repos(tmp_path) == ["alpha"]


def test_registered_repos_on_a_tree_with_no_ecosystem_dir(tmp_path: Path) -> None:
    assert cp.registered_repos(tmp_path) == []


@pytest.mark.parametrize("content", [
    "",                                  # truncated to nothing
    "name: alpha\n",                     # half-written: no path
    "path: /somewhere\n",                # half-written: no name
    "- not\n- a\n- mapping\n",
    "name: alpha\npath: [unclosed\n",    # not valid YAML
])
def test_a_broken_state_yaml_does_not_count_as_a_registration(
        tmp_path: Path, content: str) -> None:
    """Existence is not registration (terra HIGH round 8, 2026-08-21).

    `audit.discover_repos` counts existence, and so did this — so a truncated or half-written
    state.yaml permanently short-circuited the repair and let provisioning stamp a broken
    environment as registered. Being STRICTER than the audit predicate is safe in one direction
    only, and this is that direction: a file rejected here is re-seeded with a good one.
    """
    eco = tmp_path / "ecosystem" / "alpha"
    eco.mkdir(parents=True)
    (eco / "state.yaml").write_text(content, encoding="utf-8")
    assert cp.registered_repos(tmp_path) == []


def test_a_broken_state_yaml_is_reseeded_rather_than_accepted(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    eco = tmp_path / "ecosystem" / ".dev-knowledge"
    eco.mkdir(parents=True)
    (eco / "state.yaml").write_text("", encoding="utf-8")

    def _fake_seed(root: Path, name: str) -> str:
        target = root / "ecosystem" / name / "state.yaml"
        target.write_text(f"name: {name}\npath: {root}\n", encoding="utf-8")
        return str(target)

    monkeypatch.setattr(cp, "seed_self_registration", _fake_seed)
    assert cp.main(["--root", str(tmp_path), "--config", str(_config(tmp_path)),
                    "ecosystem", "--repair"]) == cp.EXIT_OK
    assert cp.registered_repos(tmp_path) == [".dev-knowledge"]


def test_ecosystem_check_reports_the_containers_symptom(tmp_path: Path) -> None:
    """A fresh clone: nothing registered, and `--check` says so rather than repairing."""
    (tmp_path / "ecosystem").mkdir()
    path = _config(tmp_path)
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem"]) == cp.EXIT_VIOLATION


def test_ecosystem_check_passes_when_something_is_registered(tmp_path: Path) -> None:
    eco = tmp_path / "ecosystem" / ".dev-knowledge"
    eco.mkdir(parents=True)
    (eco / "state.yaml").write_text("name: .dev-knowledge\npath: /x\n", encoding="utf-8")
    path = _config(tmp_path)
    assert cp.main(["--root", str(tmp_path), "--config", str(path), "ecosystem"]) == cp.EXIT_OK


def test_ecosystem_repair_success_path_registers_and_is_idempotent(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The path that ACTUALLY fixes a fresh container, exercised end to end (terra HIGH).

    Previously only detection, already-registered and self_register:false were covered, so
    deleting the code that writes `ecosystem/<name>/state.yaml` would have left the suite green
    while every fresh Codespace still failed provisioning. The seeder is stubbed to keep the test
    off a full `audit_repo` run; what it stands in for is pinned by the test below.
    """
    (tmp_path / "ecosystem").mkdir()
    seeded: list[Path] = []

    def _fake_seed(root: Path, name: str) -> str:
        target = root / "ecosystem" / name / "state.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"name: {name}\npath: {root}\n", encoding="utf-8")
        seeded.append(target)
        return str(target)

    monkeypatch.setattr(cp, "seed_self_registration", _fake_seed)
    path = _config(tmp_path)

    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_OK
    assert (tmp_path / "ecosystem" / ".dev-knowledge" / "state.yaml").exists()
    assert cp.registered_repos(tmp_path) == [".dev-knowledge"]

    # Second run: already registered, so the seeder is not called again.
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_OK
    assert len(seeded) == 1


def test_ecosystem_repair_reports_a_seed_that_did_not_land(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A seeder that returns a path but writes nothing must not be reported as success."""
    (tmp_path / "ecosystem").mkdir()
    monkeypatch.setattr(cp, "seed_self_registration", lambda root, name: "nowhere/state.yaml")
    assert cp.main(["--root", str(tmp_path), "--config", str(_config(tmp_path)),
                    "ecosystem", "--repair"]) == cp.EXIT_VIOLATION


def test_seed_self_registration_writes_under_the_REQUESTED_root(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The destination is forced, not assumed (terra CRITICAL round 5, 2026-08-21).

    `audit.save_state` resolves through the module-level `audit.ECOSYSTEM_DIR`, derived from
    `audit.py`'s own location — and `import audit` returns whatever `sys.modules` already holds.
    So `--root <another clone>` would have written that clone's audit state over THIS checkout's
    `state.yaml`, while the function returned a root-relative path claiming otherwise.

    `save_state` is deliberately NOT stubbed here: stubbing the writer would test the claim
    rather than the write.
    """
    sys.path.insert(0, str(cp.REPO_ROOT / "scripts"))
    import audit  # noqa: PLC0415

    root = tmp_path / "other-clone"
    (root / "scripts").mkdir(parents=True)
    monkeypatch.setattr(
        audit, "audit_repo",
        lambda name, path, run_date: audit.RepoState(
            name=name, path=str(path), last_audit=run_date.isoformat(), findings=[]))
    hub_state = audit.ECOSYSTEM_DIR

    written = cp.seed_self_registration(root, ".dev-knowledge")

    assert Path(written) == root / "ecosystem" / ".dev-knowledge" / "state.yaml"
    assert (root / "ecosystem" / ".dev-knowledge" / "state.yaml").exists()
    assert hub_state == audit.ECOSYSTEM_DIR          # restored, not left pointing elsewhere


@pytest.mark.parametrize("name", ["../escape", "a/b", "..", ".", "", "/abs/path"])
def test_seed_self_registration_refuses_a_name_that_is_not_a_directory_component(
        tmp_path: Path, name: str) -> None:
    """A registration name may not carry a path (terra HIGH round 10, 2026-08-21).

    `self_name` comes from a declaration file, and an absolute value or one carrying `..` would
    resolve the destination outside `root/ecosystem/` — letting an automatic provisioning step
    create or overwrite a `state.yaml` anywhere reachable.
    """
    (tmp_path / "scripts").mkdir()
    with pytest.raises(cp.ProvisioningError):
        cp.seed_self_registration(tmp_path, name)
    # Nothing was created anywhere on the way to the refusal.
    assert not (tmp_path / "ecosystem").exists()
    assert not (tmp_path.parent / "escape").exists()


def test_a_symlinked_ecosystem_directory_does_not_move_the_write_boundary(
        tmp_path: Path) -> None:
    """The boundary is the resolved ROOT, not the resolved ecosystem dir (terra HIGH round 11).

    Resolving `root/ecosystem` first makes a symlink's external target the trusted boundary, so
    the containment check passes while the write lands outside the checkout entirely — the round
    -10 traversal fix, defeated by one symlink.
    """
    root = tmp_path / "checkout"
    (root / "scripts").mkdir(parents=True)
    outside = tmp_path / "somewhere-else"
    outside.mkdir()
    try:
        (root / "ecosystem").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("this platform/user cannot create symlinks")

    with pytest.raises(cp.ProvisioningError, match="outside the checkout"):
        cp.seed_self_registration(root, ".dev-knowledge")
    assert not any(outside.iterdir()), sorted(p.name for p in outside.iterdir())


def test_an_unreadable_state_file_is_exit_2_and_is_never_overwritten(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Unreadable is not malformed (terra HIGH round 10, 2026-08-21).

    Folding a read failure into "malformed" reported exit 1 for a permission error AND let
    `--repair` overwrite a perfectly valid state file that happened to be locked at that instant.
    """
    eco = tmp_path / "ecosystem" / ".dev-knowledge"
    eco.mkdir(parents=True)
    state = eco / "state.yaml"
    state.write_text("name: .dev-knowledge\npath: /x\n", encoding="utf-8")

    real_read = Path.read_text

    def _locked(self: Path, *a: object, **k: object) -> str:
        if self == state:
            raise PermissionError("locked by another process")
        return real_read(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", _locked)
    seeded: list[str] = []
    monkeypatch.setattr(cp, "seed_self_registration",
                        lambda root, name: seeded.append(name) or "x")

    assert cp.main(["--root", str(tmp_path), "--config", str(_config(tmp_path)),
                    "ecosystem", "--repair"]) == cp.EXIT_UNAVAILABLE
    assert seeded == []


def test_seed_self_registration_refuses_when_the_state_did_not_land(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A return value is a claim; the file's existence is the proof."""
    stub = types.ModuleType("audit")
    stub.ECOSYSTEM_DIR = tmp_path / "ecosystem"
    stub.audit_repo = lambda name, path, run_date: object()
    stub.save_state = lambda state: None             # writes nothing at all
    monkeypatch.setitem(sys.modules, "audit", stub)
    (tmp_path / "scripts").mkdir()

    with pytest.raises(cp.ProvisioningError, match="did not land"):
        cp.seed_self_registration(tmp_path, ".dev-knowledge")


def test_seed_self_registration_uses_audit_repo_and_save_state_only(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Pins the REUSE claim: `audit_repo` + `save_state`, and none of `audit.py repo`'s extras.

    `audit.py repo` also appends history, writes a dated report under `docs/audits/` and commits
    its outputs — three things a provisioning step must never do to a container's tree. The
    module docstring says so; this asserts it.
    """
    calls: list[str] = []
    fake_state = object()

    def _save(state: object) -> None:
        calls.append("save_state")
        target = stub.ECOSYSTEM_DIR / ".dev-knowledge" / "state.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("name: .dev-knowledge\npath: /x\n", encoding="utf-8")

    stub = types.ModuleType("audit")
    stub.ECOSYSTEM_DIR = tmp_path / "ecosystem"
    stub.audit_repo = lambda name, path, run_date: (calls.append("audit_repo"), fake_state)[1]
    stub.save_state = _save
    for forbidden in ("append_history", "generate_report", "write_report",
                      "_commit_routine_outputs"):
        stub.__dict__[forbidden] = lambda *a, **k: calls.append(forbidden)
    monkeypatch.setitem(sys.modules, "audit", stub)

    (tmp_path / "scripts").mkdir()
    written = cp.seed_self_registration(tmp_path, ".dev-knowledge")

    assert calls == ["audit_repo", "save_state"]
    assert written.endswith("state.yaml")


def test_ecosystem_repair_refuses_when_self_register_is_off(tmp_path: Path) -> None:
    (tmp_path / "ecosystem").mkdir()
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["ecosystem"]["self_register"] = False
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_VIOLATION


# --- the declaration and the shell that invoke this module ----------------------------------


def test_a_declared_block_with_no_reader_is_ignored_rather_than_refused(tmp_path: Path) -> None:
    """The live declaration still carries a `prebuild:` block and this module reads none of it.

    Deliberate, and asserted rather than left to chance: `[#746]` restored the two legs the row
    names, not the retired module's third command, so the loader has to tolerate a block it does
    not consume. The alternative — refusing an unknown key — would turn a declaration of record
    into a container that will not provision.
    """
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["prebuild"] = {"configured": "not even a boolean", "regions": "not even a list"}
    body["something_invented_later"] = [1, 2, 3]
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    cfg = cp.load_config(path)
    assert cfg.history.required_refs == ("main",)
    assert not hasattr(cfg, "prebuild")


def test_every_invocation_the_declaration_documents_parses() -> None:
    """The YAML's comments name commands a reader will type (terra MEDIUM round 12, 2026-08-21).

    Two of them once said `prebuild --check`, and there is no such option — following the file's
    own documentation produced an argparse error. [#746] rewrote those comments onto a new module
    name, which is exactly the edit that reintroduces the class, so the check comes back with it.
    """
    text = (cp.REPO_ROOT / ".devcontainer" / "provisioning.yaml").read_text(encoding="utf-8")
    parser = cp.build_parser()
    found = 0
    for line in text.splitlines():
        _, sep, tail = line.partition("provision_legs.py ")
        if not sep:
            continue
        argv = [tok.strip("`.,") for tok in tail.split("`", 1)[0].split()]
        argv = [tok for tok in argv if tok]
        if not argv:
            continue
        parser.parse_args(argv)          # SystemExit here IS the failure
        found += 1
    assert found >= 2, text


def test_every_guard_invocation_in_provision_sh_parses() -> None:
    """WITNESSED 2026-08-21, in the container: the gate called `... history --quiet`, argparse
    put `--quiet` on the PARENT parser, and the gate died with `unrecognized arguments: --quiet`
    and REFUSED a perfectly good container. A gate that fails closed on its own typo is worse
    than no gate, and no unit test caught it because every test called `main()` with a
    hand-written argument list. This one reads the argument lists the shell actually uses.
    """
    text = (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    calls = []
    for line in code.splitlines():
        _, sep, tail = line.partition("provision_legs.py ")
        if not sep:
            continue
        argv = [tok for tok in tail.split("||")[0].split() if not tok.startswith("\\")]
        if argv:
            calls.append(argv)
    # Four: the read-only check and the repair in each of `leg2b_history` and `leg5_ecosystem`.
    # The two in `gate()` end in a line continuation and are reached by the same partition.
    assert len(calls) >= 4, calls
    parser = cp.build_parser()
    for argv in calls:
        parser.parse_args(argv)          # SystemExit here IS the failure
