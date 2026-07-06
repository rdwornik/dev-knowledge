"""Tests for the deploy orchestrator's EXECUTE half (ADR-92 C2b — deploy/tool.py).

The WRITER: apply -> verify per carrier, gate the version-record write on EVERY
carrier verifying (Decision 9); on full success two writes in two contexts --
stage the consumer (write-yes / commit-no, Decision 3) + commit the record on a
hub branch the operator merges (Decision 4). The matrix:

- clean (all absent -> apply -> verify -> record written + consumer staged);
- drifted (apply -> verify -> record);
- idempotent (all correct, no force -> verify-only, no apply, no consumer
  mutation, nothing staged, record still written);
- verify-fails -> NO record (abort; record file unchanged; right carrier named;
  a raising git proves no write was even attempted);
- partial failure (carrier 3 of 4 raises in apply -> carriers 1-2 applied, no
  record, the later carrier untouched, rerunnable);
- --force (re-applies an already-correct carrier);
- re-run safety (record branch already exists -> RecordError, never clobbered);
- two-context asserts: consumer is STAGED not committed; the record lands on a
  hub branch, NOT main; main/HEAD/working-tree untouched;
- CLI wiring: --execute renders + exits non-zero on abort.

Hermetic: the "fleet" is two throwaway git repos in tmp_path; carriers are fakes;
the plugin CLI is never touched. The real git binary drives the temp repos (that
is how the plumbing + staging are honestly exercised), but nothing leaves tmp.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import contract  # noqa: E402
import tool  # noqa: E402
from contract import ApplyResult, CarrierState, VerifyResult  # noqa: E402

# #251 (stale-test): the CLI prints the record branch via Rich `console.print`, whose
# ReprHighlighter wraps the `1.0.0` semver in ANSI SGR codes MID-TOKEN when highlighting
# is active (real TTY / FORCE_COLOR / CliRunner(color=True)) -> the branch string is
# operator-visible and correctly emitted (tool.py:1199-1202, unconditional), but a LITERAL
# substring `in res.output` breaks. Strip SGR sequences before matching so the assertion is
# robust to whether Rich colorizes. Test-only: tool.py is unchanged (no product defect).
_ANSI_SGR_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    """Remove ANSI SGR (color) escape sequences so output assertions are ANSI-robust."""
    return _ANSI_SGR_RE.sub("", text)


REGISTRY_TEXT = (
    # Non-ASCII in the header (em-dash + middle-dot) so every record-write test
    # exercises the ENCODING axis: cp1252-decoding git output would mojibake these.
    "# Deployed methodology-corpus version per repo — ADR-91 · HEADER COMMENT.\n"
    "# This explanatory block MUST survive a record write.\n"
    "repos:\n"
    "  ai-council:\n"
    "    deployed_methodology_version: null\n"
    "    deployed_date: null\n"
    "    source_tag: null\n"
    "  corp-ops:\n"
    "    deployed_methodology_version: null\n"
    "    deployed_date: null\n"
    "    source_tag: null\n"
)


# ---------------------------------------------------------------------------
# Test doubles + fixtures.
# ---------------------------------------------------------------------------


class FakeExecCarrier(contract.Carrier):
    """A carrier whose detect/apply/verify are scripted; apply writes a real file."""

    def __init__(
        self, cid, detect_state, *, verify_ok=True, write_rel=None,
        apply_raises=None, verify_raises=None,
    ):
        self.carrier_id = cid
        self._detect = detect_state
        self._verify_ok = verify_ok
        self._write_rel = write_rel
        self._apply_raises = apply_raises
        self._verify_raises = verify_raises
        self.repo_root: Path | None = None
        self.calls: list[str] = []

    def detect(self, target):
        self.calls.append("detect")
        return self._detect

    def apply(self, target):
        self.calls.append("apply")
        if self._apply_raises is not None:
            raise self._apply_raises
        if self._write_rel and self.repo_root is not None:
            p = self.repo_root / self._write_rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(self.carrier_id + "\n", encoding="utf-8")
        return ApplyResult(changed=True, changes=(self._write_rel or "x",))

    def verify(self, target):
        self.calls.append("verify")
        if self._verify_raises is not None:
            raise self._verify_raises
        return VerifyResult(
            ok=self._verify_ok,
            failures=() if self._verify_ok else (f"{self.carrier_id} unsatisfied",),
        )


def factory_of(*carriers):
    cmap = {c.carrier_id: c for c in carriers}

    def factory(repo_root):
        for c in cmap.values():
            c.repo_root = repo_root
        return cmap

    return factory


def manifest_of(*ids):
    return {
        "methodology_version": "1.0.0",
        "source_tag": "v1.0.0",
        "carriers": [
            {"id": cid, "order": n + 1, "implemented": True, "target": {}}
            for n, cid in enumerate(ids)
        ],
    }


def raising_git(*args, **kwargs):
    raise AssertionError(f"git must NOT be called on abort: {args}")


@pytest.fixture
def world(tmp_path):
    """Two throwaway git repos: a hub (with the registry on main) + a clean consumer."""
    hub = tmp_path / "hub"
    consumer = tmp_path / "consumer"

    def g(repo, *args):
        r = subprocess.run(
            ["git", *args], cwd=str(repo), capture_output=True, text=True
        )
        assert r.returncode == 0, (args, r.stderr)
        return r.stdout.strip()

    hub.mkdir()
    g(hub, "init", "-b", "main")
    g(hub, "config", "user.email", "t@t")
    g(hub, "config", "user.name", "T")
    (hub / "ecosystem").mkdir()
    (hub / "ecosystem" / "deployed-versions.yaml").write_text(REGISTRY_TEXT, encoding="utf-8")
    g(hub, "add", "-A")
    g(hub, "commit", "-m", "init")

    consumer.mkdir()
    g(consumer, "init", "-b", "main")
    g(consumer, "config", "user.email", "t@t")
    g(consumer, "config", "user.name", "T")
    (consumer / "seed.txt").write_text("seed\n", encoding="utf-8")
    g(consumer, "add", "-A")
    g(consumer, "commit", "-m", "seed")

    return {
        "hub": hub,
        "consumer": consumer,
        "git": g,
        "main_before": g(hub, "rev-parse", "main"),
        "head_before": g(hub, "rev-parse", "HEAD"),
        "cons_head_before": g(consumer, "rev-parse", "HEAD"),
    }


def ctx_of(world, manifest, repo="ai-council"):
    return tool.PreflightContext(
        repo=repo,
        version="v1.0.0",
        bare_version="1.0.0",
        repo_root=world["consumer"],
        source_tag="v1.0.0",
        manifest=manifest,
        manifest_path=Path("manifest-v1.0.0.yaml"),
    )


def _run(world, factory, manifest, *, force=False, git=None):
    return tool.execute(
        ctx_of(world, manifest),
        carrier_factory=factory,
        force=force,
        git=git or tool._default_git,
        hub_root=world["hub"],
        today="2026-06-30",
    )


def _record_on(world, branch):
    """The registry text as it stands on a given hub branch."""
    return world["git"](
        world["hub"], "show", f"{branch}:ecosystem/deployed-versions.yaml"
    )


# ---------------------------------------------------------------------------
# Clean + drifted -> apply -> verify -> record + stage.
# ---------------------------------------------------------------------------


def test_clean_all_absent_applies_verifies_records_and_stages(world):
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    c2 = FakeExecCarrier("floor", CarrierState.ABSENT, write_rel=".claude/CLAUDE-FLOOR.md")
    res = _run(world, factory_of(c1, c2), manifest_of("precommit", "floor"))

    assert res.aborted is False
    assert res.record_branch == "deploy/record-ai-council-1.0.0"
    assert all(o.applied and o.verify_ok for o in res.outcomes)

    # record landed on the hub BRANCH, with the values + comments preserved
    rec = _record_on(world, res.record_branch)
    assert "HEADER COMMENT" in rec
    data = yaml.safe_load(rec)
    assert data["repos"]["ai-council"]["deployed_methodology_version"] == "1.0.0"
    assert data["repos"]["ai-council"]["deployed_date"] == "2026-06-30"
    assert data["repos"]["ai-council"]["source_tag"] == "v1.0.0"
    assert data["repos"]["corp-ops"]["deployed_methodology_version"] is None  # untouched

    # NOT main: main + HEAD + working tree untouched
    assert world["git"](world["hub"], "rev-parse", "main") == world["main_before"]
    assert world["git"](world["hub"], "rev-parse", "HEAD") == world["head_before"]
    assert world["git"](world["hub"], "status", "--porcelain") == ""

    # consumer STAGED, not committed
    assert world["git"](world["consumer"], "rev-parse", "HEAD") == world["cons_head_before"]
    staged = world["git"](world["consumer"], "diff", "--cached", "--name-only").split()
    assert set(staged) == {".pre-commit-config.yaml", ".claude/CLAUDE-FLOOR.md"}
    assert set(res.staged_paths) == set(staged)


def test_drifted_applies_and_records(world):
    c1 = FakeExecCarrier("precommit", CarrierState.PRESENT_DRIFTED, write_rel=".pre-commit-config.yaml")
    res = _run(world, factory_of(c1), manifest_of("precommit"))
    assert res.aborted is False
    assert c1.calls == ["detect", "apply", "verify"]
    data = yaml.safe_load(_record_on(world, res.record_branch))
    assert data["repos"]["ai-council"]["deployed_methodology_version"] == "1.0.0"


def test_idempotent_all_correct_verify_only_no_mutation(world):
    c1 = FakeExecCarrier("precommit", CarrierState.PRESENT_CORRECT, write_rel=".pre-commit-config.yaml")
    c2 = FakeExecCarrier("floor", CarrierState.PRESENT_CORRECT, write_rel=".claude/CLAUDE-FLOOR.md")
    res = _run(world, factory_of(c1, c2), manifest_of("precommit", "floor"))

    assert res.aborted is False
    # verify-only: apply never called
    assert c1.calls == ["detect", "verify"]
    assert c2.calls == ["detect", "verify"]
    # no consumer mutation -> nothing staged, but the record is still written
    assert res.staged_paths == ()
    assert world["git"](world["consumer"], "diff", "--cached", "--name-only") == ""
    assert res.record_branch == "deploy/record-ai-council-1.0.0"


# ---------------------------------------------------------------------------
# Failure paths -> NO record, NO stage.
# ---------------------------------------------------------------------------


def test_verify_fails_writes_no_record_and_does_not_stage(world):
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    c2 = FakeExecCarrier("floor", CarrierState.ABSENT, verify_ok=False, write_rel=".claude/CLAUDE-FLOOR.md")
    # a raising git proves the writers are NEVER even reached on abort
    res = _run(world, factory_of(c1, c2), manifest_of("precommit", "floor"), git=raising_git)

    assert res.aborted is True
    assert res.failed_carrier == "floor"
    assert res.record_branch is None
    assert res.staged_paths == ()
    # the record on main is unchanged (still all null); no record branch exists
    assert world["git"](world["hub"], "branch", "--list", "deploy/record-*") == ""
    assert "null" in _record_on(world, "main")
    # consumer not staged (carrier wrote files, but the tool staged nothing)
    assert world["git"](world["consumer"], "diff", "--cached", "--name-only") == ""


def test_partial_failure_earlier_applied_no_record_rerunnable(world):
    c1 = FakeExecCarrier("global-config", CarrierState.ABSENT, write_rel="a.txt")
    c2 = FakeExecCarrier("tier1-plugin", CarrierState.ABSENT, write_rel="b.txt")
    c3 = FakeExecCarrier("precommit", CarrierState.ABSENT, apply_raises=RuntimeError("install blew up"))
    c4 = FakeExecCarrier("floor", CarrierState.ABSENT, write_rel="d.txt")
    res = _run(
        world,
        factory_of(c1, c2, c3, c4),
        manifest_of("global-config", "tier1-plugin", "precommit", "floor"),
        git=raising_git,
    )

    assert res.aborted is True
    assert res.failed_carrier == "precommit"
    # carriers 1-2 applied + verified; 3 raised in apply; 4 never apply/verified
    assert c1.calls == ["detect", "apply", "verify"]
    assert c2.calls == ["detect", "apply", "verify"]
    assert c3.calls == ["detect", "apply"]
    assert c4.calls == ["detect"]  # assess detected it; execute never reached it
    # rerunnable: 1-2's writes are on disk in the consumer
    assert (world["consumer"] / "a.txt").exists()
    assert (world["consumer"] / "b.txt").exists()
    assert not (world["consumer"] / "d.txt").exists()
    # no record, no stage
    assert res.record_branch is None
    assert world["git"](world["hub"], "branch", "--list", "deploy/record-*") == ""


# ---------------------------------------------------------------------------
# --force + re-run safety.
# ---------------------------------------------------------------------------


def test_force_reapplies_a_correct_carrier(world):
    c1 = FakeExecCarrier("precommit", CarrierState.PRESENT_CORRECT, write_rel=".pre-commit-config.yaml")
    res = _run(world, factory_of(c1), manifest_of("precommit"), force=True)
    assert res.aborted is False
    assert c1.calls == ["detect", "apply", "verify"]  # applied despite being correct
    assert res.record_branch is not None


def test_record_branch_already_exists_raises_never_clobbers(world):
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    _run(world, factory_of(c1), manifest_of("precommit"))  # first run creates the branch
    first = world["git"](world["hub"], "rev-parse", "deploy/record-ai-council-1.0.0")
    # second run (branch still unmerged) must refuse rather than clobber
    c2 = FakeExecCarrier("precommit", CarrierState.PRESENT_CORRECT, write_rel=".pre-commit-config.yaml")
    with pytest.raises(tool.RecordError, match="already exists|record branch"):
        _run(world, factory_of(c2), manifest_of("precommit"))
    # the existing record branch is unchanged
    assert world["git"](world["hub"], "rev-parse", "deploy/record-ai-council-1.0.0") == first


# ---------------------------------------------------------------------------
# Unit: the comment-preserving surgical record edit.
# ---------------------------------------------------------------------------


def test_set_repo_record_preserves_comments_and_other_repos():
    out = tool._set_repo_record(
        REGISTRY_TEXT, "ai-council",
        deployed_version="1.0.0", deployed_date="2026-06-30", source_tag="v1.0.0",
    )
    assert "HEADER COMMENT" in out
    data = yaml.safe_load(out)
    assert data["repos"]["ai-council"] == {
        "deployed_methodology_version": "1.0.0",
        "deployed_date": "2026-06-30",
        "source_tag": "v1.0.0",
    }
    assert data["repos"]["corp-ops"]["deployed_methodology_version"] is None


def test_set_repo_record_raises_for_unknown_repo():
    with pytest.raises(tool.RecordError, match="not found"):
        tool._set_repo_record(
            REGISTRY_TEXT, "ghostrepo",
            deployed_version="1.0.0", deployed_date="2026-06-30", source_tag="v1.0.0",
        )


# ---------------------------------------------------------------------------
# CLI wiring (hermetic: preflight + execute monkeypatched).
# ---------------------------------------------------------------------------


def _fake_ctx():
    return tool.PreflightContext(
        repo="ai-council", version="v1.0.0", bare_version="1.0.0",
        repo_root=Path("."), source_tag="v1.0.0",
        manifest=manifest_of("precommit"), manifest_path=Path("m"),
    )


def test_cli_execute_aborts_with_nonzero_exit(monkeypatch):
    monkeypatch.setattr(tool, "preflight", lambda *a, **k: _fake_ctx())
    aborted = tool.ExecuteResult(
        repo="ai-council", version="v1.0.0", source_tag="v1.0.0",
        outcomes=(tool.CarrierExecOutcome("precommit", 1, CarrierState.ABSENT,
                                          applied=True, apply_changed=True, verify_ok=False,
                                          verify_failures=("nope",)),),
        aborted=True, failed_carrier="precommit", record_branch=None, staged_paths=(),
    )
    monkeypatch.setattr(tool, "execute", lambda *a, **k: aborted)
    res = CliRunner().invoke(tool.deploy, ["ai-council", "--target", "v1.0.0", "--execute"])
    assert res.exit_code == 1
    assert "ABORTED" in res.output


def test_cli_execute_success_reports_branch_and_zero_exit(monkeypatch):
    monkeypatch.setattr(tool, "preflight", lambda *a, **k: _fake_ctx())
    ok = tool.ExecuteResult(
        repo="ai-council", version="v1.0.0", source_tag="v1.0.0",
        outcomes=(tool.CarrierExecOutcome("precommit", 1, CarrierState.ABSENT,
                                          applied=True, apply_changed=True, verify_ok=True),),
        aborted=False, failed_carrier=None,
        record_branch="deploy/record-ai-council-1.0.0",
        staged_paths=(".pre-commit-config.yaml",),
    )
    monkeypatch.setattr(tool, "execute", lambda *a, **k: ok)
    res = CliRunner().invoke(tool.deploy, ["ai-council", "--target", "v1.0.0", "--execute"])
    assert res.exit_code == 0
    assert "SUCCESS" in _strip_ansi(res.output)
    # ANSI-robust (#251): Rich highlights the `1.0.0` semver mid-token when colorizing.
    assert "deploy/record-ai-council-1.0.0" in _strip_ansi(res.output)


# tempfile import kept meaningful: assert the writer leaves no throwaway index.
def test_no_temp_index_leftovers(world):
    before = set(os.listdir(tempfile.gettempdir()))
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    _run(world, factory_of(c1), manifest_of("precommit"))
    after = set(os.listdir(tempfile.gettempdir()))
    # #233: assert ONLY this run's temp artifacts — the record writer names its index
    # `deploy-record-index-<pid>-...` (tool.py), so pid-scoping the check makes it
    # concurrency-robust: a CONCURRENT pytest process/xdist worker has a different pid, so
    # its leftover files no longer trip this set-diff (the witnessed 2026-07-01 false-fail).
    own = f"deploy-record-index-{os.getpid()}-"
    assert not any(p.startswith(own) for p in after - before)


def test_record_blob_is_lf_and_utf8_faithful(world):
    # Regression guard for BOTH axes of the Windows-text-mode-git-I/O class:
    #   (a) EOL  -- the record blob must be LF (0 CR): text-mode hash-object stdin
    #       baked CRLF into the object store, flipping the whole registry on merge.
    #   (b) ENCODING -- the record blob must preserve non-ASCII byte-for-byte:
    #       cp1252-decoding `git show` output then UTF-8-encoding the write
    #       mojibake'd the registry's em-dashes (E2 80 94 -> "â€").
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    res = _run(world, factory_of(c1), manifest_of("precommit"))
    record_blob = subprocess.run(
        ["git", "show", f"{res.record_branch}:ecosystem/deployed-versions.yaml"],
        cwd=str(world["hub"]), capture_output=True,
    ).stdout
    # (a) EOL: LF only -- no whole-file CRLF flip on merge
    assert b"\r" not in record_blob
    # (b) ENCODING: em-dash (E2 80 94) + middle-dot (C2 B7) survive byte-for-byte
    assert b"\xe2\x80\x94" in record_blob
    assert b"\xc2\xb7" in record_blob
    assert "â€" not in record_blob.decode("utf-8")  # no cp1252 mojibake
    # the merge target (main) is LF too, so the record diff is the 3 fields, not the file
    main_blob = subprocess.run(
        ["git", "show", "main:ecosystem/deployed-versions.yaml"],
        cwd=str(world["hub"]), capture_output=True,
    ).stdout
    assert b"\r" not in main_blob


def test_malformed_base_registry_raises_loudly_not_silent(world):
    # Strict-stdout-decode guard: a non-UTF-8 byte in the committed base registry
    # must raise RecordError (loud) -- NOT be silently replaced with U+FFFD and
    # baked into the record blob. This is what stops _default_git's stdout decode
    # from regressing to errors="replace" (the latent silent-corruption handler).
    bad = (
        b"# header with an invalid UTF-8 byte: \x80\n"
        b"repos:\n  ai-council:\n    deployed_methodology_version: null\n"
        b"    deployed_date: null\n    source_tag: null\n"
    )
    (world["hub"] / "ecosystem" / "deployed-versions.yaml").write_bytes(bad)
    world["git"](world["hub"], "commit", "-am", "malformed registry")
    c1 = FakeExecCarrier("precommit", CarrierState.ABSENT, write_rel=".pre-commit-config.yaml")
    with pytest.raises(tool.RecordError, match="non-UTF-8"):
        _run(world, factory_of(c1), manifest_of("precommit"))
    # loud fail = NO record branch written (no silent partial / no U+FFFD blob)
    assert world["git"](world["hub"], "branch", "--list", "deploy/record-*") == ""


def test_tombstone_reason_preserves_bracketed_id_247():
    # #247: a tombstone reason carrying a bracketed backlog id must survive the Rich render
    # verbatim (Rich reads `[#244]` as a markup tag and DROPS it without escape()). The
    # printed record is the copy-source for the JOURNAL tombstone; a vanished [#id] there
    # trips backlog-id-on-close / git_backlog_drift at fleet scale.
    from rich.console import Console

    po = tool.PruneExecOutcome(
        component_id="ruff-gate", carrier_id="precommit", removed_in="1.2.0",
        reason="P2/[#244] n=1 prune truth-maker", state=None, pruned=True, verify_ok=True)
    result = tool.ExecuteResult(
        repo="ai-council", version="1.2.0", source_tag="v1.2.0", outcomes=(),
        aborted=False, failed_carrier=None, record_branch=None, staged_paths=(),
        prune_outcomes=(po,))
    console = Console(record=True, width=200, force_terminal=False)
    tool.render_execute(result, console)
    text = _strip_ansi(console.export_text())
    assert "[#244]" in text  # the bracketed id survives verbatim (the escape() fix)
    assert "reason: P2/[#244] n=1 prune truth-maker" in text
