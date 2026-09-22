"""lane-l8-lane-end: lane_digest -- one plain-language digest from the receipts of a batch.

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/lane_digest.py` existed
(see the RED commit of the lane; these tests were split out of `test_lane_end.py` afterwards so each
script has the test file the impacted-tests guard looks for).
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_DIGEST = _SCRIPTS / "lane_digest.py"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-l8-lane-end"


def _mod(name: str):
    return importlib.import_module(name)


def _receipt(organ: str, status: str = "ok", exit_code: int = 0, duration_ms: int = 12) -> dict:
    return {"schema": 1, "organ": organ, "status": status, "exit_code": exit_code,
            "duration_ms": duration_ms, "input_hash": "abc123", "model_requested": None,
            "model_reported": None, "command": ["x"], "output_file": None,
            "finished_at": "2026-09-20T10:00:00+00:00"}


def _write_receipts(receipts: Path, rows: list[dict]) -> None:
    receipts.mkdir(parents=True, exist_ok=True)
    for row in rows:
        (receipts / f"MOMENT-{row['organ'].upper().replace('_', '-')}.json").write_text(
            json.dumps(row), encoding="utf-8")


# --- the digest ---------------------------------------------------------------------------------

def _lane(ld, name, receipts, did=(), cost=None):
    return ld.LaneInput(name=name, receipts=list(receipts), did=list(did), cost_usd=cost)


def test_digest_names_every_lane_and_every_open_item():
    ld = _mod("lane_digest")
    lanes = [
        _lane(ld, "lane-l2-dispatch-guards", [_receipt("lane_cost"), _receipt("gates")],
              did=["guard the dispatch verb"], cost=3.5),
        _lane(ld, "lane-l3-organ-truth",
              [_receipt("lane_cost"), _receipt("gates", "failed", 1),
               _receipt("no_leftovers", "SKIPPED-NOT-BUILT", 0)], did=["fix the organ table"]),
        _lane(ld, "lane-l4-integrator-surface", []),
    ]
    text = ld.render_digest(lanes)
    for name in ("lane-l2-dispatch-guards", "lane-l3-organ-truth", "lane-l4-integrator-surface"):
        assert name in text
    assert "guard the dispatch verb" in text and "fix the organ table" in text
    # every non-ok organ is an open item, in words
    assert "gates" in text and "no leftovers" in text
    # a lane with no receipts is itself an open item
    assert "no receipts" in text.lower()


def test_digest_gives_each_lane_a_verdict_and_a_cost_or_says_none_was_recorded():
    ld = _mod("lane_digest")
    text = ld.render_digest([
        _lane(ld, "lane-a", [_receipt("gates")], cost=12.34),
        _lane(ld, "lane-b", [_receipt("gates", "failed", 1)]),
    ])
    assert "12.34" in text
    assert "not recorded" in text.lower()
    verdicts = ld.verdicts([_lane(ld, "lane-a", [_receipt("gates")]),
                            _lane(ld, "lane-b", [_receipt("gates", "failed", 1)]),
                            _lane(ld, "lane-c", [_receipt("gates", "SKIPPED-NOT-BUILT", 0)])])
    assert verdicts["lane-a"] != verdicts["lane-b"] != verdicts["lane-c"]
    assert len(set(verdicts.values())) == 3


def test_digest_is_plain_language_no_internal_identifiers():
    ld = _mod("lane_digest")
    text = ld.render_digest([_lane(ld, "lane-a", [
        _receipt("gates", "failed", 1), _receipt("digest", "SKIPPED-NOT-BUILT", 0),
        _receipt("transport_report", "SKIPPED-NO-INPUT", 0)])])
    assert "SKIPPED" not in text and "abc123" not in text and ".json" not in text
    assert "exit_code" not in text and "input_hash" not in text


def test_a_receipt_of_an_unrecognised_shape_is_an_open_item_never_dropped(tmp_path):
    ld = _mod("lane_digest")
    receipts = tmp_path / "receipts"
    _write_receipts(receipts, [_receipt("gates")])
    (receipts / "MOMENT-ODD.json").write_text(json.dumps({"status": "ok"}), encoding="utf-8")
    (receipts / "MOMENT-LIST.json").write_text("[1, 2]", encoding="utf-8")
    (receipts / "MOMENT-BROKEN.json").write_text("{not json", encoding="utf-8")
    lane = ld.LaneInput(name="lane-a", receipts=ld.load_receipts(receipts))
    assert ld.verdict(lane) == ld.VERDICT_ATTENTION
    items = ld.open_items(lane)
    assert len(items) == 3 and all("could not be read" in i for i in items)


def test_digest_cli_reads_the_receipts_of_a_batch(tmp_path):
    root = tmp_path / "worktrees"
    _write_receipts(root / "lane-a" / "logs" / "receipts", [_receipt("gates")])
    _write_receipts(root / "lane-b" / "logs" / "receipts", [_receipt("gates", "failed", 1)])
    costs = tmp_path / "LANE-COSTS.jsonl"
    costs.write_text(json.dumps({"slug": "lane-a", "usd": 7.25}) + "\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_DIGEST), "--root", str(root), "--costs-file", str(costs),
                           "--repo", str(tmp_path)], capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "lane-a" in proc.stdout and "lane-b" in proc.stdout and "7.25" in proc.stdout


# --- R-W4-3: the reports-root batch view (never git, never the integrator's checkout) ------------

def _write_report(reports_dir: Path, lane: str, commits: list[str] = (),
                  receipts: list[dict] = ()) -> None:
    tr = _mod("transport_report")
    reports_dir.mkdir(parents=True, exist_ok=True)
    parts = [f"# {lane} -- lane-end report", "", "generated: 2026-09-22T00:00:00Z", "",
             f"## Commits ({len(commits)})", ""]
    parts += [f"- {c}" for c in commits] if commits else ["No commits recorded."]
    parts += ["", "## Changed files (0)", "", "No changed files.", "",
             "## Verdict", "", tr._lane_verdict(list(receipts)), "",
             "## Session summary", "", "branch: x", "",
             f"## Receipts ({len(receipts)})", ""]
    for i, row in enumerate(receipts):
        parts += [f"### MOMENT-{i}.json", "", "```json", json.dumps(row), "```", ""]
    (reports_dir / f"LANE-END-{lane}.md").write_text("\n".join(parts), encoding="utf-8")


def test_reports_root_names_every_roster_lane_including_a_missing_one(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_report(reports, "lane-a", commits=["fix: a thing"], receipts=[_receipt("gates")])
    # lane-b is named in the roster but never wrote a report -- must be NAMED, not dropped.
    lanes = ld.reports_root_lanes(reports, ["lane-a", "lane-b"], {}, {})
    names = {lane.name for lane in lanes}
    assert names == {"lane-a", "lane-b"}
    text = ld.render_digest(lanes)
    assert "lane-a" in text and "lane-b" in text
    assert "no report reached the transport" in text
    assert ld.verdict([lane for lane in lanes if lane.name == "lane-b"][0]) == ld.VERDICT_INCOMPLETE


def test_reports_root_reads_did_from_the_report_never_git(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_report(reports, "lane-a", commits=["feat: from the report, not git"])
    # tmp_path is not a git repository at all -- if this read shelled out to git it would find
    # nothing (or error), never this commit subject.
    lanes = ld.reports_root_lanes(reports, ["lane-a"], {}, {})
    assert lanes[0].did == ["feat: from the report, not git"]


def test_a_report_with_no_commits_says_so_in_the_digest(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_report(reports, "lane-a", commits=[])
    text = ld.render_digest(ld.reports_root_lanes(reports, ["lane-a"], {}, {}))
    assert "Did: no commits recorded." in text


def test_reports_root_shows_the_merge_sha_from_the_integrators_ledger(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    ledger = tmp_path / "MERGE-RECEIPTS.jsonl"
    ledger.write_text(
        json.dumps({"slug": "lane-a", "batch": "WAVE4", "merge_sha": "deadbeef", "closed": "x"}) + "\n"
        + json.dumps({"slug": "lane-a", "batch": "WAVE4", "merge_sha": "cafef00d", "closed": "y"}) + "\n",
        encoding="utf-8")
    _write_report(reports, "lane-a", commits=["x"])
    shas = ld.load_merge_shas(ledger)
    assert shas == {"lane-a": "cafef00d"}   # the newest row for the slug wins
    text = ld.render_digest(ld.reports_root_lanes(reports, ["lane-a"], {}, shas))
    assert "Merge: cafef00d" in text


def test_a_reused_lane_slug_across_batches_does_not_misattribute_the_merge_sha(tmp_path):
    """Codex terra HIGH (2026-09-22): with no batch filter, a later batch's row for a reused slug
    would win as "the newest", handing an EARLIER batch's digest a merge sha that is not its own."""
    ld = _mod("lane_digest")
    ledger = tmp_path / "MERGE-RECEIPTS.jsonl"
    ledger.write_text(
        json.dumps({"slug": "lane-a", "batch": "WAVE3", "merge_sha": "wave3sha", "closed": "2026-09-01"}) + "\n"
        + json.dumps({"slug": "lane-a", "batch": "WAVE4", "merge_sha": "wave4sha", "closed": "2026-09-22"}) + "\n",
        encoding="utf-8")
    assert ld.load_merge_shas(ledger, batch="WAVE3") == {"lane-a": "wave3sha"}
    assert ld.load_merge_shas(ledger, batch="WAVE4") == {"lane-a": "wave4sha"}
    # unnamed batch: the old, batch-unaware behaviour (newest row overall) -- unchanged for a
    # caller that does not know which batch to prefer.
    assert ld.load_merge_shas(ledger) == {"lane-a": "wave4sha"}


def test_lane_roster_prefers_the_explicit_flag_then_the_env_then_a_glob(tmp_path, monkeypatch):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_report(reports, "lane-a")
    _write_report(reports, "lane-b")
    assert ld.lane_roster(reports, "lane-x, lane-y") == ["lane-x", "lane-y"]
    monkeypatch.setenv("HARNESS_LANES", "lane-z lane-w")
    assert ld.lane_roster(reports, None) == ["lane-z", "lane-w"]
    monkeypatch.delenv("HARNESS_LANES", raising=False)
    assert ld.lane_roster(reports, None) == ["lane-a", "lane-b"]


def test_the_unedited_harness_row_reaches_reports_mode_through_harness_lanes(tmp_path, monkeypatch, capsys):
    """`ecosystem/harness.yaml`'s `batch-close` row is out of this lane's reach (the contract: "do
    not edit harness.yaml ... the trigger exists"; DECLARE-WAVE4A hard precondition 5 confines every
    harness.yaml edit this wave to lane W4-2's `merge` moment). So its declared command --
    `lane_digest.py --lane {batch} --receipts-dir {receipts}` -- must reach the reports view
    UNCHANGED, armed only by `$HARNESS_LANES` in the environment (the same convention `HARNESS_BATCH`
    already is). This drives that exact argv shape, in-process so the resolution is pinned to a
    synthetic transport rather than racing this machine's own registered `CLAUDE_PROMPTS_DIR`."""
    ld = _mod("lane_digest")
    reports = tmp_path / "drive" / "to-browser"
    _write_report(reports, "lane-a", commits=["feat: from the transport"], receipts=[_receipt("gates")])
    receipts_dir = tmp_path / "integrator-checkout" / "logs" / "receipts"   # empty; must be ignored
    receipts_dir.mkdir(parents=True)
    monkeypatch.setattr(ld._tr, "resolve_transport", lambda root=None: reports)
    monkeypatch.setenv("HARNESS_LANES", "lane-a,lane-missing")
    code = ld.main(["--lane", "WAVE4", "--receipts-dir", str(receipts_dir), "--repo", str(tmp_path)])
    assert code == 0
    out = capsys.readouterr().out
    assert "lane-a" in out and "feat: from the transport" in out
    assert "lane-missing" in out and "no report reached the transport" in out
    assert "WAVE4" not in out   # never read as a lane name in this mode


def test_reports_root_cli_reads_a_synthetic_transport_never_the_real_drive(tmp_path):
    """Transport isolation: an explicit `--reports-root` path is a synthetic tmp_path tree, and
    nothing here reaches CLAUDE_PROMPTS_DIR or a real H: drive."""
    reports = tmp_path / "drive" / "to-browser"
    _write_report(reports, "lane-a", commits=["feat: isolated"], receipts=[_receipt("gates")])
    proc = subprocess.run(
        [sys.executable, str(_DIGEST), "--reports-root", str(tmp_path / "drive"),
         "--lanes", "lane-a,lane-missing", "--repo", str(tmp_path)],
        capture_output=True, text=True, timeout=60,
        env={**os.environ, "CLAUDE_PROMPTS_DIR": str(tmp_path / "nonexistent-drive")})
    assert proc.returncode == 0, proc.stderr
    assert "lane-a" in proc.stdout and "lane-missing" in proc.stdout
    assert "no report reached the transport" in proc.stdout


def test_digest_lane_form_is_the_moment_command_and_never_fails_the_lane(tmp_path):
    """`lane_digest.py --lane {lane}` is the command harness.yaml declares."""
    receipts = tmp_path / "receipts"
    _write_receipts(receipts, [_receipt("gates")])
    proc = subprocess.run([sys.executable, str(_DIGEST), "--lane", LANE, "--receipts-dir", str(receipts),
                           "--repo", str(tmp_path), "--costs-file", str(tmp_path / "none.jsonl")],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert LANE in proc.stdout
