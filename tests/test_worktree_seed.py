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

import shutil
import subprocess
from pathlib import Path

import pytest


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


def test_a_pep420_namespace_package_still_gets_an_editable_bootstrap(tmp_path):
    """Without this the repo derives ENV_NONE and its worktree keeps the shared interpreter --
    the exact condition leg (b) exists to remove (terra P1, fifth pass)."""
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\n\n'
        '[project]\nname = "demo-pkg"\nversion = "0"\n',
        encoding="utf-8",
    )
    pkg = tmp_path / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "mod.py").write_text("", encoding="utf-8")   # no __init__.py
    assert ws.env_bootstrap(tmp_path)[0] == ws.ENV_VENV_EDITABLE


def test_the_two_package_predicates_agree(tmp_path):
    """`worktree_seed` and `worktree_import_proof` each carry their own on-disk package
    predicate -- deliberately, so neither imports the other and each stands alone. The cost is
    that they can drift, and a drift means the plan and the proof disagree about whether a repo
    has anything to check. Pinned across the shapes that distinguish them."""
    import worktree_import_proof as wip

    cases = {
        "regular": lambda d: (d / "demo_pkg").mkdir() or
                             (d / "demo_pkg" / "__init__.py").write_text("", encoding="utf-8"),
        "namespace": lambda d: (d / "demo_pkg").mkdir() or
                               (d / "demo_pkg" / "mod.py").write_text("", encoding="utf-8"),
        "module": lambda d: (d / "demo_pkg.py").write_text("", encoding="utf-8"),
        "data-only": lambda d: (d / "demo_pkg").mkdir() or
                               (d / "demo_pkg" / "x.csv").write_text("", encoding="utf-8"),
        "absent": lambda d: None,
    }
    data = {"project": {"name": "demo-pkg"}}
    for label, build in cases.items():
        root = tmp_path / label
        root.mkdir()
        build(root)
        assert ws._has_importable_package(root, data) == wip._package_dir_exists(root, "demo_pkg"),             f"predicates disagree on the {label!r} shape"


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


def test_powershell_literals_double_embedded_apostrophes():
    r"""A path is not a safe string (terra P1, fourth pass). `C:\Users\O'Brien` closes the
    literal early: at best the emitted block is a syntax error, at worst the tail is parsed as
    PowerShell. Single-quoted strings do not interpolate, so doubling is the complete escape."""
    assert ws._ps_single_quote(r"C:\Users\O'Brien\repo") == r"'C:\Users\O''Brien\repo'"
    assert ws._ps_single_quote("plain") == "'plain'"


@requires_git
def test_the_emitted_copy_block_survives_an_apostrophe_in_the_path(tmp_path):
    """End to end, through `_copy_block` rather than only through the helper: every path the
    block interpolates has to go through the escape, not just the ones a reader remembered."""
    primary = _init_repo(tmp_path / "O'Brien demo")
    (primary / ".env").write_text("K=v", encoding="utf-8")
    linked = tmp_path / "lane"
    _git(primary, "worktree", "add", "-q", str(linked), "-b", "worktree-demo")

    block = "\n".join(ws._copy_block(ws.build_plan(linked)))
    assert "O''Brien" in block
    assert "O'Brien demo'" not in block   # an unescaped literal would leave a dangling quote

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


@requires_git
def test_write_refuses_a_lookalike_repo_that_merely_shares_the_hub_name(tmp_path):
    """THE identity guard (terra P1, third pass). A refusal keyed to a directory NAME is one a
    stranger satisfies by renaming a folder — a clone at another path, a restored backup, an
    unrelated repo. `--write` may only rewrite the checkout this script runs from."""
    impostor = _init_repo(tmp_path / ws.HUB_REPO_NAME)
    (impostor / ".worktreeinclude").write_text("do not touch\n", encoding="utf-8")

    assert ws.main(["--repo", str(impostor), "--write"]) == ws.EXIT_ERROR
    assert (impostor / ".worktreeinclude").read_text(encoding="utf-8") == "do not touch\n"


def test_the_write_guard_resolves_this_scripts_own_checkout():
    """`_own_checkout` is the whole basis of the guard above, so it is asserted directly rather
    than only through the refusal it produces."""
    assert (ws._own_checkout() / "scripts" / "worktree_seed.py").is_file()
    assert ws._own_checkout() == _HUB


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
    monkeypatch.setattr(ws, "_own_checkout", lambda: fake_hub)

    assert ws.main(["--repo", str(fake_hub), "--check"]) == ws.EXIT_DRIFT

    assert ws.main(["--repo", str(fake_hub), "--write"]) == ws.EXIT_OK
    assert ws.main(["--repo", str(fake_hub), "--check"]) == ws.EXIT_OK
# --- [#716]: a lane's base equals `main` HEAD at dispatch ----------------------------------
#
# RED-first witness, ADR-108 section B. The defect reproduced on the lane sent to fix it: this
# lane's worktree branched at 78d99d55 while local `main` stood at 0be08b3c -- SEVEN commits
# behind, fast-forwarded by the step-0 sync the contract mandates. `worktree.baseRef` was unset
# in both `.claude/settings.json` and the operator's `~/.claude/settings.json`, so Claude Code's
# documented default `fresh` applied and the base was `origin/main`.
#
# THE ASSERTION IS THE PROPERTY, NOT THE SETTING, and `[#716]`'s Done-when says so in as many
# words: "asserted by a TEST rather than by the setting's value -- so a dispatcher on a
# non-`main` branch cannot satisfy it accidentally". A test reading `baseRef == "head"` would
# pass while a dispatcher on a feature branch seeded every lane from that branch instead. So
# the live test below asks the question the row asks: does a lane dispatched right now branch
# from `main` HEAD?


def test_the_base_ref_enum_is_the_two_values_claude_code_documents():
    """`fresh | head`, verified against the shipped binary rather than from memory.

    Claude Code 2.1.268 carries `baseRef:Y(["fresh","head"]).optional()`. Pinning the enum here
    means a third value appearing upstream reddens this test instead of silently falling into
    `base_ref_verdict`'s unknown-value branch.
    """
    assert ws.BASE_REF_ENUM == ("fresh", "head")
    assert ws.BASE_REF_DEFAULT == "fresh", "unset means fresh; that is the whole defect"


def test_base_ref_is_read_NESTED_because_that_is_the_shape_the_binary_writes(tmp_path):
    """`{"worktree": {"baseRef": ...}}`, not a flat `"worktree.baseRef"` key.

    The dotted form is only how the setting is NAMED in messages -- the binary reads
    `w.worktree?.baseRef`. A flat key in settings.json is ignored in SILENCE, which would be
    this same row's failure mode one layer on: a fix that looks applied and is not.
    """
    nested = tmp_path / "nested.json"
    nested.write_text('{"worktree": {"baseRef": "head"}}', encoding="utf-8")
    flat = tmp_path / "flat.json"
    flat.write_text('{"worktree.baseRef": "head"}', encoding="utf-8")

    assert ws.read_base_ref(tmp_path, chain=(nested,)) == "head"
    assert ws.read_base_ref(tmp_path, chain=(flat,)) is None, (
        "a flat dotted key was read as a setting -- the binary would ignore it, so reading it "
        "here would report a fix that is not in force")


def test_a_later_file_in_the_settings_chain_wins(tmp_path):
    """Precedence is nearest-last, as Claude Code merges it: user, then project, then local."""
    user = tmp_path / "user.json"
    user.write_text('{"worktree": {"baseRef": "fresh"}}', encoding="utf-8")
    project = tmp_path / "project.json"
    project.write_text('{"worktree": {"baseRef": "head"}}', encoding="utf-8")
    assert ws.read_base_ref(tmp_path, chain=(user, project)) == "head"


def test_a_missing_or_unparseable_settings_file_is_skipped_not_fatal(tmp_path):
    """`settings.local.json` legitimately does not exist on a fresh clone, and a trailing comma
    should narrow this answer rather than wedge every caller."""
    absent = tmp_path / "nope.json"
    broken = tmp_path / "broken.json"
    broken.write_text('{"worktree": {"baseRef": "head",}}', encoding="utf-8")
    good = tmp_path / "good.json"
    good.write_text('{"worktree": {"baseRef": "head"}}', encoding="utf-8")

    assert ws.read_base_ref(tmp_path, chain=(absent, broken)) is None
    assert ws.read_base_ref(tmp_path, chain=(absent, broken, good)) == "head"


@requires_git
def test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH():
    """`[#716]`'s Done-when, against the LIVE repo. This is the witness that had to redden.

    Deliberately not a fixture. The row's cost is measured on real checkouts -- this lane
    branched behind twice -- and a synthetic repo would assert that the function computes what
    it computes. The question is whether THIS machine, configured as it is now, dispatches a
    lane onto `main` HEAD.

    RED before the fix: baseRef unset -> `fresh` -> base `origin/main`, which sat 7 commits
    behind local `main`. GREEN after: the repo declares `head`, and the dispatching checkout is
    the primary, which is on `main`.
    """
    verdict = ws.base_ref_verdict(_HUB)
    assert verdict.holds, verdict.why


@requires_git
def test_the_verdict_names_WHY_rather_than_only_failing():
    """A refusal that does not say which of the two ways it failed sends the reader to guess.

    The two failure modes are opposite: `fresh` fails on an unpushed local `main` (fix: push, or
    change the setting), `head` fails on a dispatcher off `main` (fix: move the dispatcher, NOT
    the setting). A verdict conflating them would point at the wrong repair.
    """
    verdict = ws.base_ref_verdict(_HUB)
    assert ws.BASE_REF_KEY in verdict.why
    assert verdict.effective in ws.BASE_REF_ENUM
    assert verdict.base_label
    if verdict.holds:
        assert verdict.base_sha == verdict.main_sha


def _stub(monkeypatch, setting, head_sha, main_sha, origin_sha):
    """Pin the three refs and the setting, so a verdict is tested against a stated state.

    Stubbed rather than staged on a real repo: the two failure modes are about which REF the
    base tracks, and reproducing them for real would mean unpushing origin or moving the
    primary checkout off `main` -- mutations of shared state that a test has no business making.
    """
    monkeypatch.setattr(ws, "read_base_ref", lambda repo, chain=None: setting)
    monkeypatch.setattr(ws, "resolve_checkout", lambda repo: (_HUB, _HUB))
    monkeypatch.setattr(ws, "_rev", lambda repo, ref: {
        "HEAD": head_sha, "main": main_sha, "origin/main": origin_sha,
    }.get(ref.replace("^{commit}", "")))


def test_fresh_is_reported_as_NOT_holding_when_local_main_is_unpushed(monkeypatch):
    """The state this lane started in, pinned so it cannot silently become acceptable.

    `fresh` binds the base to the REMOTE ref while the property is about local `main`, so a
    lane dispatched while anything is unpushed starts behind -- seven commits behind, on this
    lane, measured.
    """
    _stub(monkeypatch, ws.BASE_REF_FRESH, "b" * 40, "b" * 40, "a" * 40)
    verdict = ws.base_ref_verdict(_HUB)
    assert not verdict.holds
    assert not verdict.coincidental
    assert "unpushed" in verdict.why, verdict.why


def test_fresh_does_NOT_hold_merely_because_the_shas_AGREE_today(monkeypatch):
    """The witness that had to be hardened, and the reason is a live event rather than a theory.

    At this lane's step 0 the base lagged local `main` by seven commits. Hours later a PEER
    pushed `main`, `origin/main` caught up, and a verdict comparing only the two SHAs flipped to
    True under the SAME unset configuration -- nothing fixed in between. A test that can be
    turned green by someone else's push measures push timing, not configuration.

    So `fresh` reports `holds=False` with `coincidental=True`: the SHAs agree, the guarantee
    does not exist, and the two facts stay separately readable rather than one swallowing the
    other.
    """
    same = "e" * 40
    _stub(monkeypatch, ws.BASE_REF_FRESH, same, same, same)
    verdict = ws.base_ref_verdict(_HUB)
    assert not verdict.holds, "a coincidence was accepted as the property"
    assert verdict.coincidental
    assert "coincidence" in verdict.why, verdict.why


def test_head_on_main_holds_and_is_NOT_flagged_coincidental(monkeypatch):
    """The configuration that actually binds the base: `head`, dispatched from a checkout on
    `main`. Holds, and says so without the coincidence caveat."""
    same = "f" * 40
    _stub(monkeypatch, ws.BASE_REF_HEAD, same, same, "0" * 40)
    verdict = ws.base_ref_verdict(_HUB)
    assert verdict.holds, verdict.why
    assert not verdict.coincidental


def test_head_off_main_is_reported_as_the_ACCIDENTAL_satisfaction_the_row_warns_about(
        monkeypatch):
    """`head` + a dispatcher on a feature branch seeds every lane from that branch.

    This is why the Done-when asserts the property instead of the setting: a
    `baseRef == "head"` assertion would call this configuration fixed.
    """
    _stub(monkeypatch, ws.BASE_REF_HEAD, "c" * 40, "d" * 40, "d" * 40)
    verdict = ws.base_ref_verdict(_HUB)
    assert not verdict.holds
    assert "is not on main HEAD" in verdict.why, verdict.why
    assert "do NOT change the setting" in verdict.why, (
        "the two failure modes want opposite repairs; a verdict that does not say which one "
        "points the reader at the wrong fix")


def test_a_baseRef_outside_the_enum_is_REFUSED_rather_than_treated_as_a_neighbour(monkeypatch):
    """A typo'd value must not be assumed to behave like either documented one."""
    monkeypatch.setattr(ws, "read_base_ref", lambda repo, chain=None: "origin/main")
    monkeypatch.setattr(ws, "resolve_checkout", lambda repo: (_HUB, _HUB))
    verdict = ws.base_ref_verdict(_HUB)
    assert not verdict.holds
    assert "outside the documented enum" in verdict.why, verdict.why
