"""Tests for the manifest-only re-stamp verb of scripts/gen_handoff.py (green-main-2026-10-14, X2).

RED-FIRST. The 2026-10-14 architect bundle was COMMITTED with a cold-cut `HANDOFF_RECEIPT.json`
`manifest.files` after its SUPPLEMENT / RESIDUAL / HANDOFF_BOOT / PASTE_THIS / PROBES were filled, so
`verify_handoff_probes` `BD-manifest` hard-fails on main. The only existing re-stamp path
(`--filled`) goes through `generate()`, whose `_resolve_bundle_dir` refuses a git-TRACKED bundle
(`BundleCollisionError`), and a full re-render would rewrite shipped content. Nothing here exists
yet; every test below fails today because the function / flag is missing, not because a fixture
errors.

INTERFACE FIXED FOR THE IMPLEMENTER (do not rename without changing these tests):

  * Python seam (the narrowest testable one):

        gen_handoff.restamp_manifest(repo_root: Path, bundle_dir: Path) -> list[str]

    Rewrites ONLY `receipt["manifest"]["files"]` in `<bundle_dir>/HANDOFF_RECEIPT.json` to
    `_bundle_file_shas(bundle_dir)` -- every other receipt key (cut_id, source_sha,
    generation_time, row_freshness, boot_cost, ...) and every other bundle file stays
    byte-identical; written with `newline="\\n"`. Returns the sorted relative names whose recorded
    sha changed. Works on a git-TRACKED bundle (does not go through `_resolve_bundle_dir`), runs no
    preflight and re-renders nothing.

  * Refusal: raises `gen_handoff.RestampRefusedError(RuntimeError)` and writes nothing when ANY of:
    the failing-probe set of `verify_handoff_probes.verify(bundle_dir, repo_root=repo_root)` is not
    exactly {"BD-manifest"} (so BD-ci / BD-seats drift is NOT waived here -- nothing is
    re-rendered to re-derive them -- and a bundle that fails nothing is refused too); a mismatch is
    an ADDED or REMOVED file; a mismatch is a content change outside `_BD_MANIFEST_FILL_SURFACE`.
    The message names the offending probe id / file.

  * CLI: a new flag on the existing click command `gen_handoff.main`:

        gen_handoff.py --restamp-manifest --slug <bundle-slug>

    Resolves `<bundle_root>/<slug>` with the same `_REPO_ROOT` / `docs/handoffs` rule the other
    modes use, calls `restamp_manifest`, exits 0 on success and exits 1 through the existing
    `raise SystemExit(f"[error] {exc}")` path on `RestampRefusedError`. It needs no `--mode` and
    does not run the preflight. NOTE: adding the flag changes the flag set pinned by the EXISTING
    `tests/test_gen_handoff.py::test_cli_flags_and_refusal_exit_code_are_unchanged`
    (`expected_flags`); the implementer extends that set by exactly `--restamp-manifest`.
"""
from __future__ import annotations

import json
import os
import subprocess

import pytest

import gen_handoff as gh  # noqa: E402
import verify_handoff_probes as vhp  # noqa: E402

from test_gen_handoff import (  # noqa: E402 -- shared fixtures, precedent: test_handoff_state.py
    _SEATS_LATER, _cut_and_fill, _live_state)

_GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def _commit_all(repo, msg="commit the bundle"):
    for args in (["add", "-A"], ["commit", "-q", "-m", msg]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, env=_GIT_ENV,
                       capture_output=True)


def _snapshot(bundle):
    return {p.relative_to(bundle).as_posix(): p.read_bytes()
            for p in sorted(bundle.rglob("*")) if p.is_file()}


def _failing(bundle, repo):
    return {r.probe_id for r in vhp.verify(bundle, repo_root=repo) if r.status == "fail"}


def _committed_filled_bundle(tmp_path, monkeypatch):
    """The 10-14 shape: cut cold, run the documented fill step WITHOUT the --filled re-render
    (so the receipt manifest is stale), then COMMIT the bundle."""
    # No live transport: with the operator's Drive attached, the Decisions row spawns one `git`
    # per decision file against this tmp repo and every `verify` takes minutes (a plain
    # non-git stub fails fast, a committed one does not). The re-stamp does not read it.
    monkeypatch.setattr(gh, "transport_root", lambda *_a, **_k: None)
    repo, _sha, bundle = _cut_and_fill(tmp_path, monkeypatch)
    _commit_all(repo)
    assert gh._tracked_under(repo, bundle), "fixture: the bundle must be git-tracked"
    return repo, bundle


def test_restamp_rewrites_only_the_receipt_manifest_files_of_a_committed_bundle(
        tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    assert _failing(bundle, repo) == {"BD-manifest"}      # the only thing wrong, as on main
    before = _snapshot(bundle)
    receipt_before = json.loads(before[vhp.RECEIPT_FILE])

    changed = gh.restamp_manifest(repo, bundle)

    after = _snapshot(bundle)
    receipt_after = json.loads(after[vhp.RECEIPT_FILE])
    assert {n for n in after if after[n] != before.get(n)} == {vhp.RECEIPT_FILE}
    assert set(after) == set(before)
    assert receipt_after["manifest"]["files"] == gh._bundle_file_shas(bundle)
    for key in ("cut_id", "source_sha", "generation_time", "row_freshness"):
        assert receipt_after["manifest"][key] == receipt_before["manifest"][key], key
    assert {k: v for k, v in receipt_after.items() if k != "manifest"} == \
        {k: v for k, v in receipt_before.items() if k != "manifest"}
    assert changed and set(changed) <= gh._BD_MANIFEST_FILL_SURFACE
    assert b"\r\n" not in after[vhp.RECEIPT_FILE]           # newline="\n" (test_generator_newlines)
    assert _failing(bundle, repo) == set()                  # BD-manifest now passes


def test_restamp_refuses_a_content_edit_outside_the_fill_surface(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    outside = sorted(p for p in bundle.iterdir() if p.is_file()
                     and p.name not in gh._BD_MANIFEST_FILL_SURFACE and p.name != vhp.RECEIPT_FILE)
    assert outside, sorted(p.name for p in bundle.iterdir())
    p = outside[0]
    p.write_text(p.read_text(encoding="utf-8") + "\n<!-- tampered -->\n", encoding="utf-8")
    _commit_all(repo, "tamper")
    before = _snapshot(bundle)

    with pytest.raises(gh.RestampRefusedError) as exc:
        gh.restamp_manifest(repo, bundle)

    assert p.name in str(exc.value)
    assert _snapshot(bundle) == before                      # a refusal writes nothing


def test_restamp_refuses_an_added_file(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    (bundle / "SNEAKED-IN.md").write_text("not part of any fill step\n", encoding="utf-8")
    _commit_all(repo, "add a file")
    before = _snapshot(bundle)

    with pytest.raises(gh.RestampRefusedError) as exc:
        gh.restamp_manifest(repo, bundle)

    assert "SNEAKED-IN.md" in str(exc.value)
    assert _snapshot(bundle) == before


def test_restamp_refuses_when_another_probe_is_failing(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    real_verify = vhp.verify
    monkeypatch.setattr(vhp, "verify", lambda *a, **k: [
        *real_verify(*a, **k),
        vhp.ProbeResult("P2", "fail", "a genuine, unrelated defect", bundle.name)])
    before = _snapshot(bundle)

    with pytest.raises(gh.RestampRefusedError) as exc:
        gh.restamp_manifest(repo, bundle)

    assert "P2" in str(exc.value)
    assert _snapshot(bundle) == before


def test_restamp_does_not_waive_live_drift_probes_the_way_filled_does(tmp_path, monkeypatch):
    """`_filled_waivable_fails` waives BD-ci / BD-seats because a re-render re-derives them. The
    re-stamp re-renders nothing, so the failing set must be exactly {BD-manifest}."""
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    _live_state(monkeypatch, ci="`816c7f6` NOT-RUN (run 2 still in_progress)",
                seats=_SEATS_LATER, seat_ids=("abcd1234ffff",))
    # (BD-ci on a COMMITTED bundle only WARNs; BD-seats is the live-drift probe that still fails)
    assert {"BD-seats", "BD-manifest"} <= _failing(bundle, repo)
    before = _snapshot(bundle)

    with pytest.raises(gh.RestampRefusedError):
        gh.restamp_manifest(repo, bundle)

    assert _snapshot(bundle) == before


def test_restamp_refuses_a_bundle_that_fails_nothing(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    gh.restamp_manifest(repo, bundle)                       # now consistent
    _commit_all(repo, "restamped")
    before = _snapshot(bundle)

    with pytest.raises(gh.RestampRefusedError):
        gh.restamp_manifest(repo, bundle)

    assert _snapshot(bundle) == before


def test_cli_restamp_manifest_flag_restamps_a_committed_bundle_and_exits_zero(
        tmp_path, monkeypatch):
    from click.testing import CliRunner

    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "_REPO_ROOT", repo)
    before = _snapshot(bundle)

    result = CliRunner().invoke(gh.main, ["--restamp-manifest", "--slug", bundle.name])

    assert result.exit_code == 0, result.output
    after = _snapshot(bundle)
    assert {n for n in after if after[n] != before.get(n)} == {vhp.RECEIPT_FILE}
    assert _failing(bundle, repo) == set()


def test_cli_restamp_manifest_refusal_exits_one_and_writes_nothing(tmp_path, monkeypatch):
    from click.testing import CliRunner

    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    (bundle / "SNEAKED-IN.md").write_text("not part of any fill step\n", encoding="utf-8")
    _commit_all(repo, "add a file")
    monkeypatch.setattr(gh, "_REPO_ROOT", repo)
    before = _snapshot(bundle)

    result = CliRunner().invoke(gh.main, ["--restamp-manifest", "--slug", bundle.name])

    assert result.exit_code == 1, result.output
    assert "SNEAKED-IN.md" in result.output
    assert _snapshot(bundle) == before
