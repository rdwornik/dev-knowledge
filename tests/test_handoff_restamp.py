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

R107 ADDITION (operator ruling 2026-10-14, to-browser/RATIFICATION-2026-10-14.md v4): "Every use
writes a receipt." and "It rewrites only the manifest hashes of the filled files; nothing else
in the bundle changes." The use-receipt therefore lives OUTSIDE the bundle dir, following the
repo's committed-ledger convention (`logs/MERGE-RECEIPTS.jsonl`, `logs/CODESPACE-RECEIPTS.jsonl`:
append-only JSONL, one object per event):

  * PATH: `<repo_root>/logs/HANDOFF-RESTAMP-RECEIPTS.jsonl`, ONE appended line per call to
    `restamp_manifest` (success AND refusal -- the line is written before the error is raised).
  * KEYS (all required): `verb` ("restamp-manifest"), `slug` (bundle dir name), `bundle`
    (repo-relative posix path), `utc` (ISO-8601 UTC timestamp), `ruling` ("R107"), `files`
    (`{relative name: {"old": sha256, "new": sha256}}` for each file whose recorded sha changed;
    `{}` on a refusal), `head_sha` (`git rev-parse HEAD` of repo_root), `outcome` ("restamped" |
    "refused"), `reason` (null on restamped; the refusal message on refused).

ROUND 2 (judge r1, 6a.O1 / 6a.O2) -- contract additions:

  * OUTCOME ENUM is restamped | refused | error. An UNEXPECTED exception inside
    `restamp_manifest` (anything but RestampRefusedError) appends exactly one line with
    outcome "error" and reason "<ExceptionType>: <message>", then the exception PROPAGATES
    unchanged. `RestampRefusedError` stays outcome "refused". EVERY exit appends exactly one line.
  * DURABILITY: the append is `gen_handoff._append_restamp_receipt` (tests patch this name). No
    bundle change may exist without a receipt: if the append raises OSError, HANDOFF_RECEIPT.json
    is byte-identical to before (append-before-write, or restore on failure) and the OSError
    propagates.
  * CLI early exits (`--restamp-manifest` with no `--slug`; a slug naming no bundle dir) append
    one "refused" line (slug null / the slug as given, `files` {}, non-empty reason) and exit
    non-zero (1).
  * SLUG SAFETY: the CLI refuses, before any verify / read / write of any bundle, a slug that is
    not a single path component: anything containing "/" or "\\", an absolute path (Windows
    `C:\\...` or POSIX `/tmp/x`), "." or "..". Each refusal exits non-zero and appends one
    "refused" line (slug as given, `files` {}, non-empty reason; `bundle` may be null). The
    resolved bundle dir must be a direct child of `<repo>/docs/handoffs`.
"""
from __future__ import annotations

import json
import os
import re
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


# ADR-132 D2: `--restamp-manifest` is no longer a verb -- the cut restamps the manifest as an internal
# step. The CLI tests of the verb (its flag, its refusal exit, its slug-safety guards) went with it
# (GO-2 witnesses): the restamp's behaviour and its R107 use receipt stay covered by the function-level
# tests below, `tests/test_handoff_cut.py::test_the_manifest_is_restamped_after_the_extra_files_are_written`
# covers the cut's internal step, and `test_the_hand_verbs_the_cut_replaces_are_gone_from_the_cli` holds
# the flag gone (no slug input reaches a path any more, so the slug-safety guards have no surface).


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






# --- R107: every use writes a receipt (outside the bundle); only manifest hashes change --------

_USE_RECEIPT = "logs/HANDOFF-RESTAMP-RECEIPTS.jsonl"
_USE_RECEIPT_KEYS = {"verb", "slug", "bundle", "utc", "ruling", "files", "head_sha", "outcome",
                     "reason"}


def _use_receipts(repo):
    path = repo / _USE_RECEIPT
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _head(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


def test_R107_a_successful_restamp_writes_exactly_one_use_receipt(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    old_files = json.loads((bundle / vhp.RECEIPT_FILE).read_text(encoding="utf-8"))["manifest"]["files"]
    assert _use_receipts(repo) == []

    changed = gh.restamp_manifest(repo, bundle)

    receipts = _use_receipts(repo)
    assert len(receipts) == 1, receipts
    rec = receipts[0]
    assert set(rec) == _USE_RECEIPT_KEYS, set(rec) ^ _USE_RECEIPT_KEYS
    assert rec["verb"] == "restamp-manifest" and rec["ruling"] == "R107"
    assert rec["slug"] == bundle.name
    assert rec["bundle"] == bundle.relative_to(repo).as_posix()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|\+00:00)", rec["utc"]), rec["utc"]
    assert rec["head_sha"] == _head(repo)
    assert rec["outcome"] == "restamped" and rec["reason"] is None
    assert set(rec["files"]) == set(changed) and changed
    new_files = gh._bundle_file_shas(bundle)
    for name, pair in rec["files"].items():
        assert pair == {"old": old_files[name], "new": new_files[name]}, name
        assert pair["old"] != pair["new"], name
    assert not (bundle / "logs").exists()                  # the receipt is outside the bundle


def test_R107_a_refused_restamp_also_writes_a_use_receipt_with_its_reason(tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    (bundle / "SNEAKED-IN.md").write_text("not part of any fill step\n", encoding="utf-8")
    _commit_all(repo, "add a file")

    with pytest.raises(gh.RestampRefusedError) as exc:
        gh.restamp_manifest(repo, bundle)

    receipts = _use_receipts(repo)
    assert len(receipts) == 1, receipts                    # every use, refusals included
    rec = receipts[0]
    assert set(rec) == _USE_RECEIPT_KEYS, set(rec) ^ _USE_RECEIPT_KEYS
    assert rec["outcome"] == "refused" and rec["ruling"] == "R107"
    assert rec["slug"] == bundle.name and rec["head_sha"] == _head(repo)
    assert rec["files"] == {}
    assert "SNEAKED-IN.md" in rec["reason"] and rec["reason"] in str(exc.value)


def test_R107_only_the_manifest_hashes_of_the_changed_files_differ_afterwards(
        tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    before = _snapshot(bundle)
    receipt_before = json.loads(before[vhp.RECEIPT_FILE])

    changed = gh.restamp_manifest(repo, bundle)

    after = _snapshot(bundle)
    assert set(after) == set(before)
    assert {n for n in after if n != vhp.RECEIPT_FILE and after[n] != before[n]} == set()
    receipt_after = json.loads(after[vhp.RECEIPT_FILE])
    # every key identical except manifest.files, and inside it only the changed files' entries
    assert {k: v for k, v in receipt_after.items() if k != "manifest"} == \
        {k: v for k, v in receipt_before.items() if k != "manifest"}
    assert {k: v for k, v in receipt_after["manifest"].items() if k != "files"} == \
        {k: v for k, v in receipt_before["manifest"].items() if k != "files"}
    files_before, files_after = receipt_before["manifest"]["files"], receipt_after["manifest"]["files"]
    assert set(files_after) == set(files_before)
    assert {n for n in files_after if files_after[n] != files_before[n]} == set(changed)


# --- round 2 (judge r1 6a.O1 / 6a.O2): every exit receipts; no unreceipted mutation; slug safety --

def test_R107_r2_an_unexpected_exception_still_appends_one_error_receipt_and_propagates(
        tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    before = _snapshot(bundle)

    def boom(*_a, **_k):
        raise RuntimeError("probe verifier exploded")

    monkeypatch.setattr(vhp, "verify", boom)
    with pytest.raises(RuntimeError, match="probe verifier exploded"):
        gh.restamp_manifest(repo, bundle)

    receipts = _use_receipts(repo)
    assert len(receipts) == 1, receipts
    assert set(receipts[0]) == _USE_RECEIPT_KEYS
    assert receipts[0]["outcome"] == "error" and receipts[0]["ruling"] == "R107"
    assert "RuntimeError" in receipts[0]["reason"] and "probe verifier exploded" in receipts[0]["reason"]
    assert receipts[0]["files"] == {}
    assert _snapshot(bundle) == before


def test_R107_r2_a_failing_receipt_append_leaves_the_bundle_receipt_byte_identical(
        tmp_path, monkeypatch):
    repo, bundle = _committed_filled_bundle(tmp_path, monkeypatch)
    before = _snapshot(bundle)

    def disk_full(*_a, **_k):
        raise OSError("no space left on device")

    monkeypatch.setattr(gh, "_append_restamp_receipt", disk_full)
    with pytest.raises(OSError):
        gh.restamp_manifest(repo, bundle)

    assert _snapshot(bundle)[vhp.RECEIPT_FILE] == before[vhp.RECEIPT_FILE]
    assert _snapshot(bundle) == before                     # no bundle change without a receipt






def _decoy_copy(bundle, dest):
    import shutil

    shutil.copytree(bundle, dest)
    return dest




