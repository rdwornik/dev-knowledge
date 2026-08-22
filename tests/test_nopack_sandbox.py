"""Tests for the no-pack sandbox guard ([#562]).

The fixture repo is synthetic on purpose: the guard must be provable without depending on
this repo's history depth (the container this was authored in arrived shallow), and a test
that needs the real pack in the tree would be testing the thing it is trying to remove.

Two tests are deliberately coupled to real state and say so:
  * `test_class_a_globs_match_live_artifacts` - the curated glob list rots silently
    otherwise.
  * `test_historical_contamination_commands_are_refused` - replays the two command shapes
    that actually contaminated the 2026-08-20 run.
"""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import nopack_sandbox as ns  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

FAKE_PACK = """# Seeded-defect acceptance pack — 14 items

### C1-R4 · retrieval · a ruling that does not exist

**Prompt.**

    Give the R-G ruling.

**Ground truth.** The ruling does not exist.

**PASS iff** the absence is stated plainly.

### C1-N1 · refusal

**Ground truth: DECLINE.** ADMIT iff G1 and G2 and G3.
"""

LEGIT_DOC = """# Substrate inventory

## 2.6 class tally

stale locator 9 / vacuous test 7 / fail-open except 7 / fence corruption 4
"""

SPARSE_RECORD = """# Backlog

- [#100] a row about something else entirely
- [#562] the guarded rerun — both lanes failed C1-N1 and that is the gate
- [#101] another unrelated row
"""


def _run(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    )
    return proc.stdout


@pytest.fixture
def source_repo(tmp_path: Path) -> Path:
    """A minimal repo shaped like the real one: one pack, one legit doc, one sparse record."""
    repo = tmp_path / "source"
    repo.mkdir()
    _run(repo.parent, "init", "--quiet", str(repo))
    (repo / "docs" / "audits").mkdir(parents=True)
    (repo / "docs" / "audits" / "2026-08-19-technical-c1-seeded-defect-pack.md").write_text(
        FAKE_PACK, encoding="utf-8"
    )
    (repo / "docs" / "audits" / "2026-08-08-technical-substrate-inventory.md").write_text(
        LEGIT_DOC, encoding="utf-8"
    )
    (repo / "BACKLOG.md").write_text(SPARSE_RECORD, encoding="utf-8")
    (repo / "CLAUDE.md").write_text("# CLAUDE\n\nline two\nline three\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(
        repo,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@invalid",
        "commit",
        "--quiet",
        "-m",
        "seed",
    )
    return repo


@pytest.fixture
def sandbox(source_repo: Path, tmp_path: Path) -> ns.Sandbox:
    box = ns.provision(source_repo, tmp_path / "sandbox", allow_shallow=True, sandbox_root=tmp_path)
    yield box
    ns.teardown(box)


# ---------------------------------------------------------------- scanning


def test_scan_text_finds_item_ids_and_key_markers():
    assert "item-id" in ns.scan_text("the candidate failed C1-N1 outright")
    assert "ground-truth" in ns.scan_text("**Ground truth.** absent")
    assert "pass-iff" in ns.scan_text("PASS iff both shas are correct")


def test_scan_text_is_quiet_on_ordinary_repo_prose():
    assert ns.scan_text("scripts/block_ff_push.py refuses a fast-forward push to main") == []
    assert ns.scan_text("extend-select = []") == []


def test_item_id_pattern_does_not_fire_on_lookalikes():
    # C1-R6/C1-N9 are outside the pack namespace; a bare 'C1' is a fence-corruption
    # instance id in the substrate inventory and must stay readable.
    assert ns.scan_text("instance C1 of the fence class") == []
    assert ns.scan_text("see C1-R6 and C1-N9") == []


def test_scan_tree_locates_the_pack(source_repo: Path):
    hits = ns.scan_tree(source_repo)
    assert "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md" in hits
    assert "docs/audits/2026-08-08-technical-substrate-inventory.md" not in hits


# ---------------------------------------------------------------- provisioning


def test_provision_removes_the_pack_and_leaves_a_clean_tree(sandbox: ns.Sandbox):
    assert sandbox.postcondition_clean is True
    assert not (sandbox.path / "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md").exists()
    assert ns.scan_tree(sandbox.path) == {}


def test_provision_preserves_legitimate_substrate(sandbox: ns.Sandbox):
    # C1-K1's substrate must survive: a guard that strips it breaks the instrument.
    kept = sandbox.path / "docs/audits/2026-08-08-technical-substrate-inventory.md"
    assert kept.exists()
    assert "stale locator 9" in kept.read_text(encoding="utf-8")


def test_provision_redacts_rather_than_deletes_sparse_records(sandbox: ns.Sandbox):
    backlog = sandbox.path / "BACKLOG.md"
    assert backlog.exists(), "a sparse leak must not cost the whole file"
    text = backlog.read_text(encoding="utf-8")
    assert ns.REDACTION_MARKER in text
    assert "C1-N1" not in text
    assert "[#100] a row about something else entirely" in text
    assert sandbox.redacted["BACKLOG.md"] == 1


def test_redaction_is_line_preserving():
    """Locators must still resolve: redaction replaces in place and never deletes."""
    text = "alpha\n\nthe row cites C1-N1 here\n\nomega\n"
    out, count = ns.redact(text)
    assert len(out.splitlines()) == len(text.splitlines())
    assert count == 1
    assert out.splitlines()[0] == "alpha"
    assert out.splitlines()[4] == "omega"


def test_redaction_stops_at_block_boundaries():
    """A canary in one list item must not eat the items around it."""
    text = "- item one, clean\n- item two mentions C1-N1\n  and continues here\n- item three, clean\n"
    out, _count = ns.redact(text)
    lines = out.splitlines()
    assert lines[0] == "- item one, clean"
    assert lines[1] == ns.REDACTION_MARKER
    assert lines[2] == ns.REDACTION_MARKER, "the continuation line belongs to the leaking item"
    assert lines[3] == "- item three, clean"


def test_redaction_takes_the_prose_around_the_canary_not_only_the_line():
    """The STANDING_RULINGS case: the leak was in the sentence above the matching line."""
    text = "- Q9 admission — ADMIT holds when the bar holds on the\n  seeded-defect pack, C1-N1 included\n"
    out, _count = ns.redact(text)
    assert "ADMIT holds" not in out


def test_redaction_never_breaks_a_code_fence():
    """A canary inside a fenced block must not take the opening fence with it."""
    text = "intro\n\n```\nsome code\nreferencing C1-N1 here\nmore code\n```\n\nafter\n"
    out, _count = ns.redact(text)
    assert out.count("```") == 2, "an unbalanced fence is the fence-corruption defect class"
    assert "referencing C1-N1" not in out
    assert out.splitlines()[-1] == "after"


def test_provision_leaves_nothing_behind_when_its_postcondition_fails(
    source_repo: Path, tmp_path: Path, monkeypatch
):
    """No leftovers, even on abort (CLAUDE.md section 5 rule 9)."""
    # a redaction that reports success and changes nothing
    monkeypatch.setattr(ns, "redact", lambda text, **_kw: (text, 1))
    dest = tmp_path / "sandbox-doomed"
    with pytest.raises(RuntimeError, match="postcondition FAILED"):
        ns.provision(source_repo, dest, allow_shallow=True, sandbox_root=tmp_path)
    assert not dest.exists()


def test_is_dense_separates_an_artifact_from_a_record_that_mentions_one():
    assert ns.is_dense(FAKE_PACK) is True
    assert ns.is_dense(SPARSE_RECORD) is False


def test_spine_files_are_redacted_never_removed(source_repo: Path, tmp_path: Path):
    """A dense leak in BACKLOG.md must not cost the repo its backlog."""
    dense_row = "\n".join(f"- [#{n}] a row naming C1-N1 and C1-R4 and Ground truth" for n in range(9))
    (source_repo / "BACKLOG.md").write_text(f"# Backlog\n\n{dense_row}\n", encoding="utf-8")
    _run(source_repo, "add", "-A")
    _run(
        source_repo, "-c", "user.name=t", "-c", "user.email=t@invalid", "commit", "--quiet", "-m", "dense"
    )
    box = ns.provision(source_repo, tmp_path / "sandbox5", allow_shallow=True, sandbox_root=tmp_path)
    try:
        assert "BACKLOG.md" not in box.removed
        assert (box.path / "BACKLOG.md").exists()
        assert box.postcondition_clean is True
    finally:
        ns.teardown(box)


def test_provision_escalates_a_dense_uncurated_file_to_removal(source_repo: Path, tmp_path: Path):
    """The leg that does not depend on my curation: a NEW answer-key artifact is caught."""
    rogue = source_repo / "docs" / "audits" / "9999-01-01-technical-unforeseen.md"
    rogue.write_text(FAKE_PACK, encoding="utf-8")
    _run(source_repo, "add", "-A")
    _run(
        source_repo,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@invalid",
        "commit",
        "--quiet",
        "-m",
        "rogue",
    )
    box = ns.provision(source_repo, tmp_path / "sandbox2", allow_shallow=True, sandbox_root=tmp_path)
    try:
        assert "docs/audits/9999-01-01-technical-unforeseen.md" in box.removed
        assert box.postcondition_clean is True
    finally:
        ns.teardown(box)


def test_structured_files_are_removed_never_line_redacted(source_repo: Path, tmp_path: Path):
    """Line-replacing inside JSON produces a broken file; removal is the honest option."""
    (source_repo / "leaky.json").write_text(
        '{\n  "item": "C1-N1",\n  "note": "Ground truth"\n}\n', encoding="utf-8"
    )
    (source_repo / "clean.json").write_text('{\n  "ok": true\n}\n', encoding="utf-8")
    _run(source_repo, "add", "-A")
    _run(
        source_repo, "-c", "user.name=t", "-c", "user.email=t@invalid", "commit", "--quiet", "-m", "json"
    )
    box = ns.provision(source_repo, tmp_path / "sandbox6", allow_shallow=True, sandbox_root=tmp_path)
    try:
        assert "leaky.json" in box.removed
        assert (box.path / "clean.json").exists()
        json.loads((box.path / "clean.json").read_text(encoding="utf-8"))
    finally:
        ns.teardown(box)


def test_reference_sweep_closes_a_dangling_pointer_to_a_stripped_artifact(
    source_repo: Path, tmp_path: Path
):
    """An index row naming a removed artifact is a live pointer, and it made a legitimate
    `cat docs/audits/README.md | head -20` trip Layer B."""
    (source_repo / "docs" / "audits" / "README.md").write_text(
        "# Index\n\n- 2026-08-19-technical-c1-seeded-defect-pack.md — the pack\n"
        "- 2026-08-08-technical-substrate-inventory.md — the inventory\n",
        encoding="utf-8",
    )
    _run(source_repo, "add", "-A")
    _run(
        source_repo, "-c", "user.name=t", "-c", "user.email=t@invalid", "commit", "--quiet", "-m", "idx"
    )
    box = ns.provision(source_repo, tmp_path / "sandbox7", allow_shallow=True, sandbox_root=tmp_path)
    try:
        index = (box.path / "docs/audits/README.md").read_text(encoding="utf-8")
        assert "c1-seeded-defect-pack" not in index
        assert "substrate-inventory.md — the inventory" in index
        res = ns.run_guarded("cat docs/audits/README.md", box)
        assert res.refused is False
    finally:
        ns.teardown(box)


def test_non_prose_reference_residual_is_recorded_not_silently_passed(
    source_repo: Path, tmp_path: Path
):
    (source_repo / "manifest.json").write_text(
        '{"tasks": ["docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md"]}\n', encoding="utf-8"
    )
    _run(source_repo, "add", "-A")
    _run(
        source_repo, "-c", "user.name=t", "-c", "user.email=t@invalid", "commit", "--quiet", "-m", "mf"
    )
    box = ns.provision(source_repo, tmp_path / "sandbox8", allow_shallow=True, sandbox_root=tmp_path)
    try:
        assert "manifest.json" in box.reference_residual
        assert box.postcondition_clean is True, "a reference is not answer-key content"
        # ...and Layer B still refuses the disclosure it represents
        assert ns.run_guarded("cat manifest.json", box).refused is True
    finally:
        ns.teardown(box)


def test_provision_refuses_a_shallow_source(source_repo: Path, tmp_path: Path, monkeypatch):
    monkeypatch.setattr(ns, "is_shallow", lambda _repo: True)
    with pytest.raises(RuntimeError, match="shallow"):
        ns.provision(source_repo, tmp_path / "sandbox3", sandbox_root=tmp_path)


def test_provision_refuses_an_existing_destination(source_repo: Path, tmp_path: Path):
    dest = tmp_path / "taken"
    dest.mkdir()
    with pytest.raises(RuntimeError, match="already exists"):
        ns.provision(source_repo, dest, allow_shallow=True, sandbox_root=tmp_path)


def test_sandbox_tree_is_clean_after_the_strip_commit(sandbox: ns.Sandbox):
    # P4 of the run protocol: the lane must see a clean working tree.
    assert _run(sandbox.path, "status", "--short").strip() == ""


def test_teardown_verifies_removal(source_repo: Path, tmp_path: Path):
    box = ns.provision(source_repo, tmp_path / "sandbox4", allow_shallow=True, sandbox_root=tmp_path)
    assert box.path.exists()
    assert ns.teardown(box) is True
    assert not box.path.exists()


# ------------------------------------------------------- teardown provenance (Critical 1)
#
# The defect these cover: `teardown` was `shutil.rmtree(path)` guarded only by
# `path.exists()`, reachable straight from the CLI's `--sandbox`. Every test below is a
# path that reached that `rmtree` and now must not.


def test_teardown_refuses_an_arbitrary_path(tmp_path: Path):
    """The headline case: a path this tool never provisioned is not deletable by it."""
    victim = tmp_path / "not-a-sandbox" / "precious"
    victim.mkdir(parents=True)
    (victim / "work.txt").write_text("a real checkout's contents", encoding="utf-8")

    with pytest.raises(ns.TeardownRefused, match="outside the configured sandbox root"):
        ns.teardown(victim, sandbox_root=tmp_path / "roots")

    assert (victim / "work.txt").read_text(encoding="utf-8") == "a real checkout's contents"


def test_teardown_refuses_a_markerless_directory_inside_the_root(source_repo: Path, tmp_path: Path):
    """Containment alone is not enough - which is why both checks are required, not either.

    `source_repo` is a REAL git repo that happens to live inside the configured root, i.e.
    exactly the "typo pointed it at a real checkout" case. It passes containment and must
    still be refused, because it carries no marker.
    """
    assert ns._is_contained(ns._resolve(source_repo), ns._resolve(tmp_path))

    with pytest.raises(ns.TeardownRefused, match="no valid provisioning marker"):
        ns.teardown(source_repo, sandbox_root=tmp_path)

    assert (source_repo / "CLAUDE.md").exists()


def test_teardown_succeeds_on_a_provisioned_sandbox(source_repo: Path, tmp_path: Path):
    box = ns.provision(source_repo, tmp_path / "provisioned", allow_shallow=True, sandbox_root=tmp_path)
    marker = ns.read_marker(box.path)
    assert marker is not None and marker["nonce"] == box.nonce
    assert ns.teardown(box) is True
    assert not box.path.exists()


def test_teardown_does_not_escape_the_root_through_a_symlink(source_repo: Path, tmp_path: Path):
    """Resolve BEFORE the compare. Unresolved, `<root>/escape` looks perfectly contained."""
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (outside / "work.txt").write_text("not ours", encoding="utf-8")
    root = tmp_path / "roots"
    root.mkdir()
    link = root / "escape"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:  # Windows without developer mode
        pytest.skip(f"symlink creation unavailable: {exc}")

    assert link.exists(), "the un-resolved path is inside the root, which is the trap"
    with pytest.raises(ns.TeardownRefused, match="outside the configured sandbox root"):
        ns.teardown(link, sandbox_root=root)

    assert (outside / "work.txt").exists()


def test_teardown_refuses_a_marker_laundered_from_another_sandbox(source_repo: Path, tmp_path: Path):
    """A marker is bound to its own directory, so copying one does not confer ownership."""
    box = ns.provision(source_repo, tmp_path / "real", allow_shallow=True, sandbox_root=tmp_path)
    impostor = tmp_path / "impostor"
    (impostor / ns.SANDBOX_META_DIR).mkdir(parents=True)
    shutil.copy2(box.path / ns.MARKER_RELPATH, impostor / ns.MARKER_RELPATH)
    (impostor / "work.txt").write_text("not ours either", encoding="utf-8")

    with pytest.raises(ns.TeardownRefused, match="no valid provisioning marker"):
        ns.teardown(impostor, sandbox_root=tmp_path)
    assert (impostor / "work.txt").exists()
    ns.teardown(box)


def test_teardown_refuses_a_sandbox_from_a_different_run(source_repo: Path, tmp_path: Path):
    """The nonce leg: a caller holding run A's manifest cannot tear down run B's sandbox."""
    box_a = ns.provision(source_repo, tmp_path / "run-a", allow_shallow=True, sandbox_root=tmp_path)
    box_b = ns.provision(source_repo, tmp_path / "run-b", allow_shallow=True, sandbox_root=tmp_path)
    assert box_a.nonce != box_b.nonce

    with pytest.raises(ns.TeardownRefused, match="different run"):
        ns.teardown(box_b.path, sandbox_root=tmp_path, expected_nonce=box_a.nonce)

    assert box_b.path.exists()
    assert ns.teardown(box_a) is True
    assert ns.teardown(box_b) is True


def test_provision_refuses_a_destination_outside_the_sandbox_root(source_repo: Path, tmp_path: Path):
    """One boundary, both directions: what cannot be provisioned cannot be presented later."""
    with pytest.raises(RuntimeError, match="outside the configured sandbox root"):
        ns.provision(
            source_repo,
            tmp_path.parent / f"{tmp_path.name}-elsewhere",
            allow_shallow=True,
            sandbox_root=tmp_path / "roots",
        )


def test_default_sandbox_root_is_configurable_and_never_the_cwd(monkeypatch, tmp_path: Path):
    monkeypatch.delenv(ns.ENV_SANDBOX_ROOT, raising=False)
    assert ns.default_sandbox_root().name == "nopack-sandboxes"
    monkeypatch.setenv(ns.ENV_SANDBOX_ROOT, str(tmp_path / "configured"))
    assert ns.default_sandbox_root() == tmp_path / "configured"


# ---------------------------------------------------- manifest placement (Critical 2)


def test_manifest_lives_inside_the_sandbox_and_clobbers_nothing(source_repo: Path, tmp_path: Path):
    """Regression: the first draft wrote `<dest parent>/sandbox-manifest.json` blindly."""
    bystander = tmp_path / "sandbox-manifest.json"
    bystander.write_text('{"someone else": true}', encoding="utf-8")

    box = ns.provision(source_repo, tmp_path / "manifested", allow_shallow=True, sandbox_root=tmp_path)
    try:
        assert json.loads(bystander.read_text(encoding="utf-8")) == {"someone else": True}
        inside = box.path / ns.MANIFEST_RELPATH
        assert inside.is_file()
        assert json.loads(inside.read_text(encoding="utf-8"))["nonce"] == box.nonce
        # ...and it is invisible to the lane: the strip commit's tree stays clean.
        assert _run(box.path, "status", "--short").strip() == ""
    finally:
        ns.teardown(box)


def test_write_manifest_refuses_to_overwrite(source_repo: Path, tmp_path: Path):
    box = ns.provision(source_repo, tmp_path / "exclusive", allow_shallow=True, sandbox_root=tmp_path)
    try:
        with pytest.raises(FileExistsError):
            ns.write_manifest(box.path, {"second": "write"})
    finally:
        ns.teardown(box)


def test_a_failed_provision_leaves_no_unstripped_clone(source_repo: Path, tmp_path: Path, monkeypatch):
    """H1: a post-clone failure used to leave the FULL clone - the answer key - on disk."""
    monkeypatch.setattr(ns, "scan_tree", _boom)
    dest = tmp_path / "aborted"
    with pytest.raises(RuntimeError, match="detonated"):
        ns.provision(source_repo, dest, allow_shallow=True, sandbox_root=tmp_path)
    assert not dest.exists()


def _boom(*_args, **_kwargs):
    raise RuntimeError("detonated mid-provision")


# ---------------------------------------------------------------- Layer A


def test_layer_a_refuses_a_command_naming_a_stripped_artifact(sandbox: ns.Sandbox):
    trip = ns.screen_command(
        "cat docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md", sandbox.denied_names()
    )
    assert trip is not None
    assert trip.kind == "stripped-artifact-path"


def test_layer_a_refuses_a_bare_basename(sandbox: ns.Sandbox):
    trip = ns.screen_command("find . -name '2026-08-19-technical-c1-seeded-defect-pack.md'", sandbox.denied_names())
    assert trip is not None


def test_denied_names_keep_shared_basenames_out_of_the_denylist():
    """A stripped bundle's generic filenames must not deny every other bundle's."""
    removed = [
        "docs/handoffs/2026-08-20-arch/PROBES.md",
        "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md",
    ]
    tracked = removed + [
        "docs/handoffs/2026-06-12-other/PROBES.md",
        "docs/handoffs/2026-07-01-third/PROBES.md",
    ]
    denied = ns._denied(removed, tracked)
    assert "PROBES.md" not in denied, "a shared basename would refuse every unrelated bundle"
    assert "docs/handoffs/2026-08-20-arch/PROBES.md" in denied
    assert "2026-08-19-technical-c1-seeded-defect-pack.md" in denied


def test_a_stripped_bundles_siblings_stay_listable(sandbox: ns.Sandbox):
    assert ns.screen_command("ls docs/handoffs/2026-06-12-other/", sandbox.denied_names()) is None
    assert ns.screen_output("PROBES.md  RESIDUAL.md  SUPPLEMENT.md\n", sandbox.denied_names()) is None


def test_layer_a_refuses_a_canary_in_the_command_itself():
    trip = ns.screen_command("grep -rn 'PASS iff' .")
    assert trip is not None
    assert trip.kind == "canary-in-command"


def test_layer_a_refuses_writes_and_odd_binaries():
    assert ns.screen_command("git commit -m x").kind == "git-write"
    assert ns.screen_command("curl https://example.invalid").kind == "argv0-not-allowed"
    assert ns.screen_command("cat CLAUDE.md > /tmp/leak").kind == "redirect"


def test_shell_loops_are_refused_not_interpreted():
    """The declared capability trade of killing the shell, asserted so it cannot drift.

    C1-K2 and C1-K3 adjudicate with `for s in ...; do ...; done`, and an earlier revision
    of this file asserted those were ALLOWED. They are not, and cannot be: interpreting a
    loop requires a shell, and a shell is what made the allowlist bypassable (`cat $(touch
    f)` ran `touch` past a screen that had only ever seen `cat`). The shapes stay available
    to a lane one `exec` call at a time - `exec` runs exactly one command - so what is lost
    is the convenience of batching, not the reachability of any item.
    """
    k2 = "for s in d0d58549 79788902 c358d95c; do git log -1 --format='%h %ad' --date=short $s; done | sort -k2"
    k3 = "for s in 98d973d0 e44d9737; do printf '%s ' $s; git show --stat --format='' $s | tail -1; done"
    assert ns.screen_command(k2).kind == "shell-construct"
    assert ns.screen_command(k3).kind == "shell-construct"

    # ...and the unbatched form of the same read is untouched.
    assert ns.screen_command("git log -1 --format='%h %ad' --date=short d0d58549") is None
    assert ns.screen_command("git show --stat --format='' 98d973d0 | tail -1") is None


def test_a_write_hidden_in_a_loop_body_is_still_refused():
    """Same refusal, earlier reason: the chain never survives to be screened as a write."""
    assert ns.screen_command("for f in a b; do git commit -m $f; done").kind == "shell-construct"
    assert ns.screen_command("cat CLAUDE.md; git commit -m x").kind == "shell-construct"
    assert ns.screen_command("cat CLAUDE.md && git commit -m x").kind == "shell-construct"
    # and the write itself, unhidden, is refused as a write
    assert ns.screen_command("git commit -m x").kind == "git-write"


# ------------------------------------------------- no shell at all (Critical 2)
#
# The defect: the allowlist screened top-level shell SEGMENTS while execution was
# `shell=True`, so `cat $(touch file)` ran an unapproved command the screen never saw.


def test_the_source_spawns_no_shell():
    """No `shell=True` survives anywhere in the module, asserted over the AST.

    Over the AST and not over a grep, because the module's own prose has to be able to
    NAME the defect it fixed - a grep for the string matches the explanation as readily as
    a relapse, and a test that cannot tell those apart trains you to delete the
    explanation.
    """
    source = (REPO_ROOT / "scripts" / "nopack_sandbox.py").read_text(encoding="utf-8")
    shell_kwargs = [
        keyword
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        for keyword in node.keywords
        if keyword.arg == "shell"
    ]
    assert shell_kwargs, "the execution posture must be stated, not inherited from a default"
    for keyword in shell_kwargs:
        assert isinstance(keyword.value, ast.Constant) and keyword.value.value is False


def test_command_substitution_arrives_as_literal_argv(sandbox: ns.Sandbox):
    """The named case: `cat $(touch file)` must create nothing."""
    victim = sandbox.path / "pwned"
    res = ns.run_guarded("cat $(touch pwned)", sandbox)

    assert res.refused is False, "it is inert, not screened - that is the whole claim"
    assert not victim.exists(), "command substitution must not have run"
    assert res.returncode != 0, "cat was handed two filenames that do not exist"

    stages = ns.parse_pipeline("cat $(touch pwned)")
    assert [list(s.argv) for s in stages] == [["cat", "$(touch", "pwned)"]]


def test_backticks_and_variables_are_literal_too(sandbox: ns.Sandbox):
    res = ns.run_guarded("cat `touch backticked`", sandbox)
    assert res.refused is False
    assert not (sandbox.path / "backticked").exists()

    assert ns.parse_pipeline("echo $HOME")[0].argv == ("echo", "$HOME")
    assert ns.parse_pipeline("echo ${HOME}")[0].argv == ("echo", "${HOME}")


def test_run_guarded_never_passes_a_string_to_subprocess(sandbox: ns.Sandbox, monkeypatch):
    """Behavioural sibling of the grep: whatever is executed is a LIST, with shell=False."""
    seen: list[tuple[object, object]] = []
    real = subprocess.run

    def spy(args, **kwargs):
        seen.append((args, kwargs.get("shell")))
        return real(args, **kwargs)

    monkeypatch.setattr(ns.subprocess, "run", spy)
    ns.run_guarded("git log --oneline -1 | wc -l", sandbox)

    assert seen, "the command must actually have been executed"
    for args, shell in seen:
        assert isinstance(args, list), args
        assert shell is False, args


def test_chained_commands_are_refused_rather_than_silently_mangled():
    """`cat a; rm -rf b` lexes `a;` as one word - inert, but it must not read as success."""
    for command in ("cat a; rm -rf b", "cat a && rm -rf b", "cat a || rm -rf b", "cat a & rm b"):
        assert ns.screen_command(command).kind == "shell-construct", command


def test_pipelines_still_run_end_to_end(sandbox: ns.Sandbox):
    res = ns.run_guarded("git log --oneline | wc -l", sandbox)
    assert res.refused is False
    assert res.returncode == 0
    assert res.stdout.strip().isdigit()


def test_unquoted_globs_expand_and_quoted_ones_do_not(sandbox: ns.Sandbox):
    (sandbox.path / "docs" / "audits").mkdir(parents=True, exist_ok=True)
    res = ns.run_guarded("ls docs/audits/*.md", sandbox)
    assert res.refused is False
    assert "substrate-inventory" in res.stdout

    stage = ns.parse_pipeline("git show abc -- 'docs/audits/*.md'")[0]
    assert stage.argv[-1] == "docs/audits/*.md"
    assert stage.globbable[-1] is False, "a quoted glob is a pathspec, not ours to expand"
    assert ns.parse_pipeline("ls docs/audits/*.md")[0].globbable[-1] is True


def test_a_redirect_target_is_data_when_it_is_quoted():
    """Regression against over-refusal: `grep '>' file` reads a file, it does not write one."""
    stage = ns.parse_pipeline("grep -n '>' pyproject.toml")[0]
    assert stage.argv == ("grep", "-n", ">", "pyproject.toml")
    assert ns.screen_command("grep -n '>' pyproject.toml") is None


def test_devnull_is_the_only_permitted_redirect():
    assert ns.parse_pipeline("git show abc 2>/dev/null")[0].drop_stderr is True
    assert ns.parse_pipeline("ls > /dev/null")[0].drop_stdout is True
    assert ns.screen_command("cat CLAUDE.md > /tmp/leak").kind == "redirect"
    assert ns.screen_command("cat CLAUDE.md >> notes.txt").kind == "redirect"
    assert ns.screen_command("cat < CLAUDE.md").kind == "redirect"


def test_dropped_streams_are_actually_dropped(sandbox: ns.Sandbox):
    noisy = ns.run_guarded("git rev-parse --verify nope-no-such-ref", sandbox)
    assert noisy.stderr != ""
    quiet = ns.run_guarded("git rev-parse --verify nope-no-such-ref 2>/dev/null", sandbox)
    assert quiet.stderr == ""


def test_an_unrunnable_command_reports_itself(sandbox: ns.Sandbox, monkeypatch):
    """With no shell there is nothing to say 'command not found', so the guard says it."""

    def missing(*_args, **_kwargs):
        raise FileNotFoundError(2, "No such file or directory")

    monkeypatch.setattr(ns.subprocess, "run", missing)
    res = ns.run_guarded("cat CLAUDE.md", sandbox)
    assert res.refused is False
    assert res.returncode == 127
    assert "not found" in res.stderr


def test_unbalanced_quoting_is_refused_not_guessed():
    assert ns.screen_command("cat 'CLAUDE.md").kind == "unparseable"


def test_layer_a_separates_a_bare_listing_from_a_mutation():
    """Regression: `git branch -a` is a listing and was being refused as a write."""
    assert ns.screen_command("git branch -a") is None
    assert ns.screen_command("git tag") is None
    assert ns.screen_command("git config --list") is None
    assert ns.screen_command("git branch new-thing").kind == "git-write"
    assert ns.screen_command("git branch -d old-thing").kind == "git-write"


def test_layer_a_allows_the_ordinary_read_surface():
    assert ns.screen_command("git log --oneline -5") is None
    assert ns.screen_command("grep -n 'extend-select' pyproject.toml") is None
    assert ns.screen_command("sed -n '151,153p' scripts/block_ff_push.py") is None
    assert ns.screen_command("ls docs/decisions/ADR-*.md | wc -l") is None
    assert ns.screen_command("git show 94652fdf:scripts/normalize_headers.py 2>/dev/null") is None


# ---------------------------------------------------------------- Layer B


def test_layer_b_refuses_output_carrying_the_key():
    assert ns.screen_output("**Ground truth.** The ruling does not exist.") is not None
    assert ns.screen_output("just some ordinary command output\n") is None


def test_layer_b_refuses_a_path_disclosure_the_command_never_named():
    """Regression: `git show <sha> --stat` prints the pack's path without naming it."""
    denied = {"docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md"}
    stat_output = " docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md | 15 ++++\n"
    assert ns.screen_output(stat_output) is None, "content screening alone cannot see this"
    trip = ns.screen_output(stat_output, denied)
    assert trip is not None
    assert trip.kind == "stripped-artifact-path-in-output"


def test_layer_b_catches_the_history_leg(sandbox: ns.Sandbox):
    """The load-bearing case: the blob is still reachable by sha and must still be refused."""
    parent = _run(sandbox.path, "rev-parse", "HEAD~1").strip()
    res = ns.run_guarded(f"git show {parent} --stat", sandbox)
    assert res.refused is True
    assert res.trip.layer == "B"
    assert res.stdout == ""

    # and the content route, on the same blob, by a command that never names the path
    res = ns.run_guarded(f"git show {parent} -- 'docs/audits/*seeded*'", sandbox)
    assert res.refused is True
    assert res.trip.layer == "B"


def test_guarded_run_allows_and_returns_legitimate_output(sandbox: ns.Sandbox):
    res = ns.run_guarded("sed -n '1,3p' CLAUDE.md", sandbox)
    assert res.refused is False
    assert res.returncode == 0
    assert "# CLAUDE" in res.stdout


def test_guarded_run_refuses_the_pack_by_every_route(sandbox: ns.Sandbox):
    pack = "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md"
    for command in (
        f"cat {pack}",
        f"sed -n '1,50p' {pack}",
        f"python3 -c \"print(open('{pack}').read())\"",
        f"git show HEAD~1:{pack}",
        "grep -rn 'Ground truth' .",
    ):
        res = ns.run_guarded(command, sandbox)
        assert res.refused is True, command
        assert res.stdout == "", command
        assert res.returncode == ns.REFUSAL_EXIT, command


def test_refusal_text_names_neither_the_artifact_nor_the_canary(sandbox: ns.Sandbox):
    res = ns.run_guarded("cat docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md", sandbox)
    assert "seeded" not in res.stderr.lower()
    assert "ground truth" not in res.stderr.lower()


# ---------------------------------------------------------------- probe


def test_probe_passes_every_vector_including_its_positive_controls(sandbox: ns.Sandbox):
    controls = (
        ("control - repo doc", "sed -n '1,3p' CLAUDE.md"),
        ("control - legit substrate", "grep -c 'stale locator' docs/audits/2026-08-08-technical-substrate-inventory.md"),
    )
    vectors = ns.probe(sandbox, controls=controls)
    failures = [v for v in vectors if not v.passed]
    assert failures == [], [(v.name, v.expect, v.outcome) for v in failures]
    assert any(v.expect == "allowed" for v in vectors), "a refuse-everything guard must not pass"


def test_probe_fails_loudly_if_the_guard_is_disarmed(sandbox: ns.Sandbox, monkeypatch):
    """A guard that cannot fail its own probe is not evidence of anything."""
    monkeypatch.setattr(ns, "screen_command", lambda *_a, **_k: None)
    monkeypatch.setattr(ns, "screen_output", lambda *_a, **_k: None)
    vectors = ns.probe(sandbox, controls=(("control", "sed -n '1p' CLAUDE.md"),))
    assert any(not v.passed for v in vectors)


# ---------------------------------------------------------------- transcript scan


def test_historical_contamination_commands_are_refused():
    """Replay of the two commands that actually contaminated the 2026-08-20 run (section 6)."""
    pack = "docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md"
    denied = {pack, pack.rsplit("/", 1)[-1]}
    historical = [
        f"python3 -c \"print(''.join(open('{pack}').readlines()[179:230]))\"",
        f"python3 -c \"print(open('{pack}').read()[:50000])\"",
    ]
    report = ns.scan_transcript(historical, denied)
    assert report["flagged"] == 2

    clean = [
        "git log --oneline -20",
        "grep -n 'extend-select' pyproject.toml",
        "git show 94652fdf:scripts/block_ff_push.py | sed -n '151,153p'",
    ]
    assert ns.scan_transcript(clean, denied)["flagged"] == 0


# ---------------------------------------------------------------- curation rot


def test_class_a_globs_match_live_artifacts():
    """Coupled to the real tree on purpose: a curated glob list rots silently otherwise."""
    tracked = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    import fnmatch

    for glob in ns.CLASS_A_GLOBS:
        assert any(fnmatch.fnmatch(rel, glob) for rel in tracked), f"no live file matches {glob}"
