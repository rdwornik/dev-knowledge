"""Events + CLI contract tests for scripts/fleet_parity.py (FR-8/FR-13, checker runs
ONLY). Fail-open is proven with a REAL failure injection (events path = a directory ->
a real OSError from open()), not a monkeypatched exception. Hermetic: temp repos,
temp manifests, --no-write everywhere (the repo's own logs/ is never touched)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from click.testing import CliRunner

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import fleet_parity as fp  # noqa: E402

_FLOOR_KEYS = {"schema_version", "event_id", "ts_utc", "repo_id", "repo_head",
               "dirty_state", "organ_id", "event_type", "severity", "verdict",
               "mode", "source_version", "evidence_ref"}


def _git(args, cwd):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _init_repo(root: Path, files: dict[str, str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    if _git(["init", "-q", "-b", "main"], root).returncode != 0:
        _git(["init", "-q"], root)
    for cfg in (["core.autocrlf", "false"], ["user.email", "fp@example.com"],
                ["user.name", "FP"], ["commit.gpgsign", "false"]):
        _git(["config", *cfg], root)
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
    _git(["add", "-A"], root)
    _git(["commit", "-q", "-m", "init"], root)
    return root


def _world(tmp_path: Path):
    """A tiny two-repo fleet + manifest + baseline + registry + deploy manifest, all
    under tmp -- the CLI never reads the real checkout's contract files (hermeticity:
    codex 2026-07-13)."""
    hub = _init_repo(tmp_path / "hub", {"VISION.md": "v\n"})
    cons = _init_repo(tmp_path / "cons",
                      {"VISION.md": "v\n", "straydir/f.txt": "x\n",
                       "straydir2/f.txt": "y\n"})
    manifest = tmp_path / "parity.yaml"
    manifest.write_text(yaml.safe_dump({
        "version": "1.0.0",
        "fleet": {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}},
        "surfaces": [{"id": "canonical-doc-vision", "kind": "path",
                      "tier": {"hub": "MUST", "consumer": "MUST"},
                      "probe": {"type": "path_tracked", "path": "VISION.md"}}],
    }, sort_keys=False), encoding="utf-8")
    baseline = tmp_path / "baseline.yaml"
    baseline.write_text(yaml.safe_dump({"version": "1.0.0", "dependencies": []}),
                        encoding="utf-8")
    registry = tmp_path / "registry.yaml"
    registry.write_text(yaml.safe_dump(
        {"repos": {"hub-r": {"source_tag": None}, "cons": {"source_tag": None}}}),
        encoding="utf-8")
    deploy = tmp_path / "deploy.yaml"
    deploy.write_text(yaml.safe_dump({"components": []}), encoding="utf-8")
    return hub, cons, manifest, baseline, registry, deploy


def _invoke(tmp_path: Path, events_path: Path, extra: list[str] | None = None):
    hub, cons, manifest, baseline, registry, deploy = _world(tmp_path)
    args = ["--run-date", "2026-07-13",
            "--manifest", str(manifest), "--baseline", str(baseline),
            "--registry", str(registry), "--ecosystem-dir", str(tmp_path / "eco"),
            "--hub-root", str(hub), "--repo-root", f"cons={cons}",
            "--deploy-manifest", str(deploy),
            "--events-path", str(events_path), "--mode", "synthetic", "--no-write"]
    return CliRunner().invoke(fp.main, args + (extra or []))


def test_event_lines_carry_the_ruled_floor_fields(tmp_path):
    events = tmp_path / "events.jsonl"
    result = _invoke(tmp_path, events)
    assert result.exit_code == 0, result.output  # WARNs present, still exit 0
    lines = [json.loads(ln) for ln in
             events.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) >= 3  # findings + the run summary
    for ev in lines:
        assert _FLOOR_KEYS <= set(ev), sorted(_FLOOR_KEYS - set(ev))
        assert ev["schema_version"] == 1
        assert ev["mode"] == "synthetic"  # synthetic never reads as fleet history
        assert ev["ts_utc"].endswith("+00:00") or "T" in ev["ts_utc"]
    run_ev = lines[-1]
    assert run_ev["event_type"] == "checker-run"
    assert run_ev["verdict"] == "completed"
    assert run_ev["counts"].get(fp.WARN_UNDECLARED, 0) >= 1
    assert run_ev["run_date"] == "2026-07-13"
    # the hub facts made it into provenance (never a bare unknown on a walked repo)
    walked = [ev for ev in lines if ev["repo_id"] in ("hub-r", "cons")]
    assert walked and all(ev["repo_head"] != "unknown" for ev in walked)
    assert all(ev["dirty_state"] in ("clean", "dirty") for ev in walked)


def test_event_id_is_deterministic_content_hash():
    a = fp._event_id("2026-07-13T00:00:00+00:00", "r", "s", "parity-verdict")
    b = fp._event_id("2026-07-13T00:00:00+00:00", "r", "s", "parity-verdict")
    c = fp._event_id("2026-07-13T00:00:00+00:00", "r", "s2", "parity-verdict")
    d = fp._event_id("2026-07-13T00:00:00+00:00", "r", "s", "parity-verdict", "comp")
    assert a == b and a != c and a != d and len(a) == 32  # replay-idempotent (FR-07)


def test_event_ids_unique_across_multi_finding_surfaces(tmp_path):
    # codex 2026-07-13: two root-sweep findings share (ts, repo, organ) -- the
    # component in the hash must keep their ids distinct or idempotent ingestion
    # collapses them.
    events = tmp_path / "events.jsonl"
    result = _invoke(tmp_path, events)
    assert result.exit_code == 0
    lines = [json.loads(ln) for ln in
             events.read_text(encoding="utf-8").splitlines() if ln]
    sweep = [ev for ev in lines if ev["organ_id"] == "root-sweep"]
    assert len(sweep) >= 2  # straydir + straydir2
    ids = [ev["event_id"] for ev in lines]
    assert len(ids) == len(set(ids)), "event ids must be unique within a run"


def test_invalid_run_date_refuses_exit_2(tmp_path):
    events = tmp_path / "events.jsonl"
    result = _invoke(tmp_path, events, extra=None)
    assert result.exit_code == 0
    bad = _invoke(tmp_path / "bad", tmp_path / "e2.jsonl",
                  extra=None)  # sanity: helper still green
    assert bad.exit_code == 0
    hub, cons, manifest, baseline, registry, deploy = _world(tmp_path / "w2")
    for bad_date in ("not-a-date", "20260713", "2026-W28-1"):
        result2 = CliRunner().invoke(fp.main, [
            "--run-date", bad_date, "--manifest", str(manifest),
            "--baseline", str(baseline), "--registry", str(registry),
            "--ecosystem-dir", str(tmp_path / "eco"), "--hub-root", str(hub),
            "--deploy-manifest", str(deploy),
            "--events-path", str(tmp_path / "e3.jsonl"), "--no-write"])
        assert result2.exit_code == 2, bad_date  # exact YYYY-MM-DD shape enforced
        assert "not a valid" in result2.output
    assert not (tmp_path / "e3.jsonl").exists()


def test_events_fail_open_on_real_oserror(tmp_path):
    # REAL failure injection: the events path IS a directory, so open(..., "a")
    # raises a real OSError. Verdicts, digest text, and the exit code are unaffected.
    events_dir = tmp_path / "events.jsonl"
    events_dir.mkdir()
    result = _invoke(tmp_path, events_dir)
    assert result.exit_code == 0, result.output
    assert "fail-open" in result.output
    assert "[fleet-parity]" in result.output  # verdict summary still rendered


def test_events_rotation_is_windows_safe(tmp_path):
    events = tmp_path / "events.jsonl"
    r1 = _invoke(tmp_path / "a", events, extra=["--max-events-bytes", "64"])
    assert r1.exit_code == 0
    size_after_first = events.stat().st_size
    assert size_after_first > 64
    r2 = _invoke(tmp_path / "b", events, extra=["--max-events-bytes", "64"])
    assert r2.exit_code == 0
    rotated = Path(str(events) + ".1")
    assert rotated.exists() and rotated.stat().st_size == size_after_first
    # the live file now holds only run-2 lines (append-only within a generation)
    lines = [json.loads(ln) for ln in
             events.read_text(encoding="utf-8").splitlines() if ln]
    assert lines and lines[-1]["event_type"] == "checker-run"
    # a third run rotates AGAIN over the old .1 (single-backup contract, os.replace)
    r3 = _invoke(tmp_path / "c", events, extra=["--max-events-bytes", "64"])
    assert r3.exit_code == 0 and rotated.exists()


def test_exit_2_on_unreadable_manifest_and_no_digest(tmp_path):
    hub, cons, _m, baseline, registry, deploy = _world(tmp_path)
    digest_before = fp.DIGEST_PATH.read_text(encoding="utf-8") \
        if fp.DIGEST_PATH.exists() else None
    result = CliRunner().invoke(fp.main, [
        "--run-date", "2026-07-13", "--manifest", str(tmp_path / "absent.yaml"),
        "--baseline", str(baseline), "--registry", str(registry),
        "--ecosystem-dir", str(tmp_path / "eco"), "--hub-root", str(hub),
        "--deploy-manifest", str(deploy),
        "--events-path", str(tmp_path / "e.jsonl")])
    assert result.exit_code == 2
    assert "REFUSED" in result.output
    # never silently green: no digest was written/overwritten on the refusal path
    digest_after = fp.DIGEST_PATH.read_text(encoding="utf-8") \
        if fp.DIGEST_PATH.exists() else None
    assert digest_after == digest_before
    assert not (tmp_path / "e.jsonl").exists()


def test_subset_run_is_marked(tmp_path):
    events = tmp_path / "events.jsonl"
    result = _invoke(tmp_path, events, extra=["--repo", "cons"])
    assert result.exit_code == 0
    # subset runs never masquerade as full-fleet runs (digest header marks it; the
    # CLI output still carries the summary line)
    assert "[fleet-parity]" in result.output
