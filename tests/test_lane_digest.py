"""lane-l8-lane-end: lane_digest -- one plain-language digest from the receipts of a batch.

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/lane_digest.py` existed
(see the RED commit of the lane; these tests were split out of `test_lane_end.py` afterwards so each
script has the test file the impacted-tests guard looks for).
"""
from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

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


# --- LANE-5B2-17: the CI-red OPERATOR-ACTION line -----------------------------------------

def test_the_ci_red_threshold_never_drifts_from_ci_red_ages_own(monkeypatch):
    """The two threshold constants are duplicated (module docstring: `lane_digest.py` stays
    gh/click-free), so they can only be caught agreeing or disagreeing -- never merged into one
    import -- by a test that reads both."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("ci_red_age_pin", _SCRIPTS / "ci_red_age.py")
    cra = importlib.util.module_from_spec(spec)
    sys.modules["ci_red_age_pin"] = cra  # dataclass field resolution needs the module registered
    spec.loader.exec_module(cra)
    ld = _mod("lane_digest")
    assert ld._CI_RED_THRESHOLD_H == cra.RED_AGE_THRESHOLD_H


def test_ci_red_line_is_none_below_the_threshold():
    ld = _mod("lane_digest")
    assert ld.ci_red_line({"since": "s", "hours": 23.0, "sha": "a", "url": "u"}) is None


def test_ci_red_line_is_none_with_no_ci_red_data():
    ld = _mod("lane_digest")
    assert ld.ci_red_line(None) is None
    assert ld.ci_red_line({}) is None


def test_ci_red_line_names_hours_sha_and_url_over_the_threshold():
    ld = _mod("lane_digest")
    line = ld.ci_red_line({"since": "s", "hours": 25.3, "sha": "deadbeef", "url": "http://run"})
    assert line == "OPERATOR-ACTION: main CI red 25.3 h since deadbeef (http://run)"


def test_render_digest_prepends_the_ci_red_line_when_over_threshold():
    ld = _mod("lane_digest")
    text = ld.render_digest([_lane(ld, "lane-a", [_receipt("gates")])],
                            ci_red={"since": "s", "hours": 30.0, "sha": "abc", "url": "u"})
    assert "OPERATOR-ACTION: main CI red 30.0 h since abc (u)" in text
    assert text.index("OPERATOR-ACTION") < text.index("lane-a")


def test_render_digest_omits_the_ci_red_line_when_absent():
    ld = _mod("lane_digest")
    text = ld.render_digest([_lane(ld, "lane-a", [_receipt("gates")])])
    assert "OPERATOR-ACTION" not in text


def test_digest_cli_reads_ci_red_json_and_renders_the_line(tmp_path):
    root = tmp_path / "worktrees"
    _write_receipts(root / "lane-a" / "logs" / "receipts", [_receipt("gates")])
    ci_red = tmp_path / "ci-red.json"
    ci_red.write_text(json.dumps({"since": "2026-09-25T00:00:00Z", "hours": 30.0,
                                  "sha": "deadbeef", "url": "http://run"}), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_DIGEST), "--root", str(root),
                          "--ci-red-json", str(ci_red), "--repo", str(tmp_path)],
                         capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "OPERATOR-ACTION: main CI red 30.0 h since deadbeef (http://run)" in proc.stdout


def test_digest_cli_reads_ci_red_json_null_and_renders_nothing(tmp_path):
    root = tmp_path / "worktrees"
    _write_receipts(root / "lane-a" / "logs" / "receipts", [_receipt("gates")])
    ci_red = tmp_path / "ci-red.json"
    ci_red.write_text("null", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_DIGEST), "--root", str(root),
                          "--ci-red-json", str(ci_red), "--repo", str(tmp_path)],
                         capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "OPERATOR-ACTION" not in proc.stdout


def test_digest_cli_an_unreadable_ci_red_json_never_fails_the_digest(tmp_path):
    root = tmp_path / "worktrees"
    _write_receipts(root / "lane-a" / "logs" / "receipts", [_receipt("gates")])
    proc = subprocess.run([sys.executable, str(_DIGEST), "--root", str(root),
                          "--ci-red-json", str(tmp_path / "absent.json"), "--repo", str(tmp_path)],
                         capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "OPERATOR-ACTION" not in proc.stdout


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


# --- [#1368] the section-3 LANE REPORT schema and the section-4 batch rollup ---------------------
#
# RED-first (lane-bw-1368-lane-report-rollup). The schema is `ecosystem/schema/lane_report.py`
# (pydantic, already locked) and its generated JSON Schema file `lane-report.schema.json`; the
# rollup is this module's `--manifest` mode, reading the batch manifest's lane table
# (`batch_manifest.manifest_lane_rows`) and each `LANE-END-<lane>.md`'s one fenced json block
# (`handback_schema.parse_lane_report_block`).

if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_SCHEMA_FILE = _REPO / "ecosystem" / "schema" / "lane-report.schema.json"


def _lane_report(lane: str = "lane-x-1-demo", state: str = "COMPLETED", results=("PASS",),
                 **over) -> dict:
    """The section-3 example of `DIGEST-PROPOSAL-ADR-LANE-REPORT-CONTRACT-2026-10-11.md`,
    with its alternatives resolved to one concrete value each."""
    row = {
        "lane": lane, "batch": "B2-W3", "task": "[#1103]", "kind": "code", "state": state,
        "done": {"met": 4, "total": 4},
        "checks": [{"name": f"check-{i}", "how": "deterministic", "result": r,
                    "evidence": "tests/test_x.py:1"} for i, r in enumerate(results)],
        "intent_met": {"verdict": "YES",
                       "evaluator": {"vendor": "copilot", "model": "gpt-5", "session": "s-1"}},
        "unresolved": [], "operator_action": None, "merged_sha": None,
        "producer": {"vendor": "claude", "model": "claude-opus-5-5", "session": "p-1"},
        "cost_usd": None,
        "evidence": {"branch": f"worktree-{lane}", "check_run": None, "audit": None},
    }
    row.update(over)
    return row


def _write_lane_end(folder: Path, lane: str, report: dict) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"LANE-END-{lane}.md"
    path.write_text(
        "carried-by: OPEN\nkind: LANE_END\ndate: 2026-10-13\nsupersedes: none\n"
        f"summary: fixture\nby: test\n\n# LANE-END-{lane}\n\n{lane} | one line\n\n"
        "```json\n" + json.dumps(report) + "\n```\n", encoding="utf-8", newline="\n")
    return path


_MANIFEST = """---
batch: ZZ
---

# Batch ZZ -- manifest

## 2 · The lanes

| # | Lane slug | Rows | Wave | Model / effort | Review | State |
|---|---|---|---|---|---|---|
| F1-A | `lane-zz-1-alpha` | `[#1]` | F1 | opus / high | Codex | GO |
| F1-B | `lane-zz-2-beta` | `[#2]` | F1 | opus / high | Codex | GO |
| F1-C | `lane-zz-3-gamma` | `[#3]` | F1 | opus / high | Codex | GO |
| C1 | `lane-zz-4-delta` | `[#4]` | C | opus / high | Codex | GO |

## 3 · Integration

Mentions `lane-zz-9-not-a-lane` outside the table.
"""


def test_the_lane_report_schema_accepts_the_section_3_example():
    from ecosystem.schema.lane_report import LaneReport
    report = LaneReport.model_validate(_lane_report())
    assert report.state == "COMPLETED"


def test_the_lane_report_schema_accepts_the_shape_the_f1_lanes_wrote():
    """intent_met may be null (the orchestrator writes it) or carry a note; review may be
    present or null -- every F1 LANE-END on the transport uses one of these."""
    from ecosystem.schema.lane_report import LaneReport
    LaneReport.model_validate(_lane_report(intent_met=None, review=None))
    LaneReport.model_validate(_lane_report(
        intent_met={"verdict": "UNSURE", "note": "architect R99.2",
                    "evaluator": {"vendor": "anthropic", "model": "m", "session": "s"}},
        review={"vendor": "openai", "model": "gpt-5.6-terra", "session": "01a1",
                "verdict": "APPROVE", "nonce": "8f3a1c7e"}))


def test_the_lane_report_schema_rejects_a_report_missing_state():
    import pydantic
    from ecosystem.schema.lane_report import LaneReport
    row = _lane_report()
    del row["state"]
    with pytest.raises(pydantic.ValidationError):
        LaneReport.model_validate(row)


def test_the_lane_report_schema_rejects_a_state_outside_the_closed_enum():
    import pydantic
    from ecosystem.schema.lane_report import LaneReport
    for bad in ("DONE", "completed", "UNSURE", ""):
        with pytest.raises(pydantic.ValidationError):
            LaneReport.model_validate(_lane_report(state=bad))


def test_the_lane_report_schema_rejects_a_vacuous_completed():
    """S-56 Done 4c: every check NOT_RUN (or no check at all) cannot be COMPLETED."""
    import pydantic
    from ecosystem.schema.lane_report import LaneReport
    with pytest.raises(pydantic.ValidationError, match="NOT_RUN"):
        LaneReport.model_validate(_lane_report(results=("NOT_RUN", "NOT_RUN")))
    with pytest.raises(pydantic.ValidationError, match="NOT_RUN"):
        LaneReport.model_validate(_lane_report(results=()))
    # the same checks are fine on a state that claims nothing passed
    LaneReport.model_validate(_lane_report(state="FAILED", results=("NOT_RUN",)))
    LaneReport.model_validate(_lane_report(results=("NOT_RUN", "PASS")))


def test_the_schema_file_is_the_models_own_json_schema():
    """The committed file is generated, never hand-edited: it equals the model's schema, so the
    file `claude -p --json-schema` receives and the validator the rollup runs cannot drift."""
    from ecosystem.schema.lane_report import SCHEMA_FILE, json_schema
    assert SCHEMA_FILE == _SCHEMA_FILE
    assert json.loads(_SCHEMA_FILE.read_text(encoding="utf-8")) == json_schema()


def test_the_schema_file_parses_as_a_json_schema_carrying_the_three_rules():
    schema = json.loads(_SCHEMA_FILE.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert "state" in schema["required"]
    assert schema["properties"]["state"]["enum"] == [
        "COMPLETED", "FAILED", "REJECTED", "INPUT_REQUIRED", "CANCELED"]
    rule = schema["allOf"][0]
    assert rule["if"]["properties"]["state"]["const"] == "COMPLETED"
    assert rule["then"]["properties"]["checks"]["contains"]["properties"]["result"]["enum"] == [
        "PASS", "FAIL"]
    # every $ref resolves inside the file -- a dangling ref is a schema the CLI cannot use
    text = _SCHEMA_FILE.read_text(encoding="utf-8")
    for ref in set(re.findall(r'"\$ref":\s*"#/\$defs/([^"]+)"', text)):
        assert ref in schema["$defs"], ref


def test_parse_lane_report_block_reads_the_one_json_fence():
    hs = _mod("handback_schema")
    text = ("# LANE-END-x\n\n### MOMENT-X.json\n\n```json\n{\"organ\": \"x\"}\n```\n\n"
            "```json\n" + json.dumps(_lane_report()) + "\n```\n")
    assert hs.parse_lane_report_block(text)["lane"] == "lane-x-1-demo"
    assert hs.parse_lane_report_block("# no block here\n") is None


def test_manifest_lane_rows_reads_the_numbered_lanes_table():
    bm = _mod("batch_manifest")
    rows = bm.manifest_lane_rows(_MANIFEST)
    assert rows == [("lane-zz-1-alpha", "F1"), ("lane-zz-2-beta", "F1"),
                    ("lane-zz-3-gamma", "F1"), ("lane-zz-4-delta", "C")]


def test_manifest_lane_rows_reads_this_batchs_own_manifest():
    bm = _mod("batch_manifest")
    text = (_REPO / "docs" / "audits" / "2026-10-12-technical-batch-bw-manifest.md").read_text(
        encoding="utf-8")
    f1 = [slug for slug, wave in bm.manifest_lane_rows(text) if wave == "F1"]
    assert f1 == ["lane-bw-1001-hook-launcher", "lane-bw-1447-distill-kind-fix",
                  "lane-bw-912-known-reds-expiry", "lane-bw-893-b2w3-carry", "lane-bw-926-main-red"]


def test_the_rollup_prints_an_absent_lane_as_missing_and_totals_by_state(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_lane_end(reports, "lane-zz-1-alpha", _lane_report("lane-zz-1-alpha"))
    _write_lane_end(reports, "lane-zz-2-beta", _lane_report(
        "lane-zz-2-beta", state="INPUT_REQUIRED", operator_action="rule R98 on 58 entries",
        unresolved=["one", "two"]))
    # lane-zz-3-gamma: no report.  lane-zz-4-delta: another wave, out of the F1 rollup.
    _write_lane_end(reports, "lane-zz-4-delta", _lane_report("lane-zz-4-delta"))
    out = ld.render_rollup("ZZ", _MANIFEST, reports, wave="F1")
    lines = out.rstrip("\n").splitlines()
    assert len(lines) <= 25
    assert lines[0] == "batch ZZ wave F1 | expected 3 | received 2 | MISSING: lane-zz-3-gamma"
    assert any(line.startswith("lane-zz-3-gamma | MISSING") for line in lines)
    assert any(line.startswith("lane-zz-1-alpha | COMPLETED 4/4 | check-0 PASS") for line in lines)
    assert "lane-zz-4-delta" not in out
    assert "totals: COMPLETED 1 · INPUT_REQUIRED 1 · MISSING 1" in lines
    assert "- lane-zz-2-beta: rule R98 on 58 entries" in lines


def test_the_rollup_counts_an_invalid_report_as_received_but_never_as_a_state(tmp_path):
    ld = _mod("lane_digest")
    reports = tmp_path / "to-browser"
    _write_lane_end(reports, "lane-zz-1-alpha", _lane_report("lane-zz-1-alpha", results=("NOT_RUN",)))
    (reports / "LANE-END-lane-zz-2-beta.md").write_text("# old prose report, no json\n",
                                                       encoding="utf-8")
    _write_lane_end(reports, "lane-zz-3-gamma", _lane_report("lane-zz-3-gamma", state="FAILED"))
    out = ld.render_rollup("ZZ", _MANIFEST, reports, wave="F1")
    assert "expected 3 | received 3 | MISSING: none" in out
    assert "lane-zz-1-alpha | INVALID" in out and "lane-zz-2-beta | INVALID" in out
    assert "totals: FAILED 1 · INVALID 2" in out


def test_the_rollup_never_exceeds_25_lines(tmp_path):
    ld = _mod("lane_digest")
    rows = "\n".join(f"| X{i} | `lane-zz-{i}-l` | `[#{i}]` | F1 | o | C | GO |" for i in range(1, 41))
    manifest = ("## 2 · The lanes\n\n| # | Lane slug | Rows | Wave | Model / effort | Review | State |\n"
                "|---|---|---|---|---|---|---|\n" + rows + "\n")
    reports = tmp_path / "to-browser"
    for i in range(1, 41, 2):
        _write_lane_end(reports, f"lane-zz-{i}-l", _lane_report(
            f"lane-zz-{i}-l", state="INPUT_REQUIRED", operator_action=f"act {i}"))
    out = ld.render_rollup("ZZ", manifest, reports, wave="F1")
    lines = out.rstrip("\n").splitlines()
    assert len(lines) <= 25
    assert lines[0].startswith("batch ZZ wave F1 | expected 40 | received 20 | MISSING: ")
    assert "totals: INPUT_REQUIRED 20 · MISSING 20" in lines


def test_the_rollup_cli_reads_a_synthetic_transport(tmp_path):
    manifest = tmp_path / "manifest.md"
    manifest.write_text(_MANIFEST, encoding="utf-8")
    drive = tmp_path / "drive"
    _write_lane_end(drive / "to-browser", "lane-zz-1-alpha", _lane_report("lane-zz-1-alpha"))
    proc = subprocess.run(
        [sys.executable, str(_DIGEST), "--manifest", str(manifest), "--wave", "F1",
         "--reports-root", str(drive)],
        capture_output=True, text=True, encoding="utf-8", timeout=60,
        env={**os.environ, "CLAUDE_PROMPTS_DIR": str(tmp_path / "nonexistent-drive"),
             "PYTHONIOENCODING": "utf-8"})
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.startswith("batch ZZ wave F1 | expected 3 | received 1 | MISSING: ")
    assert "lane-zz-2-beta | MISSING" in proc.stdout
