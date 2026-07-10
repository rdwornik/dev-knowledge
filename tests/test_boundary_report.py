"""Tests for scripts/boundary_report.py (#312 fleet CLAUDE.md boundary reporter).

Parser units (marker pairing / id alignment / loud-on-unbalanced / default=project) +
reporter units on inline tmp_path fixture repos (marked-clean / marked-drifted / unmarked
/ unavailable) + a live-repo assertion. Firing assertions (status + evidence substrings),
not presence.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "boundary_report.py"


def _load():
    spec = importlib.util.spec_from_file_location("boundary_report", _P)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so module-level @dataclass can resolve cls.__module__.
    sys.modules["boundary_report"] = module
    spec.loader.exec_module(module)
    return module


br = _load()


# --- parser: pairing, id alignment, default=project -------------------------

def test_parse_balanced_pair_captures_id_owner():
    text = ("intro\n"
            "<!-- methodology:start id=alpha owner=hub -->\n"
            "the body\n"
            "<!-- methodology:end id=alpha -->\n")
    regions, warns = br.parse_regions(text)
    assert warns == []
    assert len(regions) == 1
    assert (regions[0].id, regions[0].owner, regions[0].body) == ("alpha", "hub", "the body")


def test_parse_owner_repo_and_optional_v():
    text = ("<!-- methodology:start id=proj owner=repo v=1.2.0 -->\n"
            "x\n"
            "<!-- methodology:end id=proj -->\n")
    regions, warns = br.parse_regions(text)
    assert warns == []
    assert regions[0].owner == "repo"
    assert regions[0].v == "1.2.0"


def test_parse_no_markers_is_empty_default_project():
    regions, warns = br.parse_regions("# a doc\n\nno markers here\n- a bullet\n")
    assert regions == []
    assert warns == []


def test_parse_inline_marker_mention_is_not_a_region():
    # A prose line that merely QUOTES the marker text (e.g. CLAUDE.md's §12 entry) is not
    # a marker — only a line that is ENTIRELY the marker counts.
    text = "explaining `<!-- methodology:start id=x owner=hub -->` inline in prose\n"
    regions, warns = br.parse_regions(text)
    assert regions == []
    assert warns == []


def test_parse_mismatched_close_id_warns():
    text = ("<!-- methodology:start id=alpha owner=hub -->\n"
            "body\n"
            "<!-- methodology:end id=beta -->\n")
    regions, warns = br.parse_regions(text)
    assert any("does not match open id=alpha" in w for w in warns)


def test_parse_unclosed_region_warns():
    text = ("<!-- methodology:start id=alpha owner=hub -->\n"
            "body with no close\n")
    regions, warns = br.parse_regions(text)
    assert any("never closed" in w for w in warns)


def test_parse_orphan_close_warns():
    text = "body\n<!-- methodology:end id=ghost -->\n"
    regions, warns = br.parse_regions(text)
    assert any("no open region" in w for w in warns)


def test_parse_nested_warns():
    text = ("<!-- methodology:start id=outer owner=hub -->\n"
            "<!-- methodology:start id=inner owner=hub -->\n"
            "b\n"
            "<!-- methodology:end id=inner -->\n"
            "<!-- methodology:end id=outer -->\n")
    regions, warns = br.parse_regions(text)
    assert any("nested" in w for w in warns)


# --- diff / finding units ---------------------------------------------------

def test_diff_and_finding_match_is_pass():
    baseline = {"a": "abody", "b": "bbody"}
    regions = [br.Region("a", "hub", None, "abody"),
               br.Region("b", "hub", None, "bbody"),
               br.Region("p", "repo", None, "proj")]
    d = br.diff_consumer(baseline, regions)
    assert d.match == ["a", "b"] and d.drift == [] and d.missing == [] and d.project_n == 1
    f = br.to_finding("consumer-x", d)
    assert f.check_name == "claude_md_boundary"
    assert f.status == "pass"
    assert "|" not in f.evidence


def test_diff_body_differs_is_drift_warn():
    baseline = {"a": "abody", "b": "bbody"}
    regions = [br.Region("a", "hub", None, "DRIFTED"),
               br.Region("b", "hub", None, "bbody")]
    d = br.diff_consumer(baseline, regions)
    assert d.drift == ["a"] and d.match == ["b"]
    f = br.to_finding("consumer-x", d)
    assert f.status == "warn"
    assert "drift: a" in f.evidence
    assert "|" not in f.evidence


def test_unmarked_consumer_is_warn():
    baseline = {"a": "abody"}
    d = br.diff_consumer(baseline, [])  # no regions at all
    assert d.hub_n == 0
    f = br.to_finding("consumer-x", d)
    assert f.status == "warn"
    assert "unmarked" in f.evidence


def test_unavailable_finding():
    f = br.to_finding("gone", None, unavailable=True)
    assert f.status == "unavailable"
    assert "not found" in f.evidence


# --- reporter integration on inline tmp_path fixture repos ------------------

_HUB = ("# CLAUDE.md\n"
        "<!-- methodology:start id=alpha owner=hub -->\n"
        "alpha body\n"
        "<!-- methodology:end id=alpha -->\n"
        "<!-- methodology:start id=beta owner=hub -->\n"
        "beta body\n"
        "<!-- methodology:end id=beta -->\n"
        "<!-- methodology:start id=proj owner=repo -->\n"
        "hub project region\n"
        "<!-- methodology:end id=proj -->\n")


def _wire(monkeypatch, tmp_path, hub_text, consumers):
    """Build a tmp hub + consumer trees; monkeypatch the audit enumerator/state.
    `consumers`: {name: claude_md_text | None(=no CLAUDE.md -> unavailable)}."""
    hub = tmp_path / "hub"
    hub.mkdir()
    (hub / "CLAUDE.md").write_text(hub_text, encoding="utf-8")
    roots = {}
    for name, text in consumers.items():
        d = tmp_path / name
        d.mkdir()
        if text is not None:
            (d / "CLAUDE.md").write_text(text, encoding="utf-8")
        roots[name] = d

    class _State:
        def __init__(self, path):
            self.path = str(path)

    monkeypatch.setattr(br.audit, "discover_repos", lambda: list(consumers.keys()))
    monkeypatch.setattr(br.audit, "load_state", lambda name: _State(roots[name]))
    return hub


def test_reporter_marked_clean_is_pass(monkeypatch, tmp_path):
    consumer = ("# CLAUDE.md\n"
                "<!-- methodology:start id=alpha owner=hub -->\n"
                "alpha body\n"
                "<!-- methodology:end id=alpha -->\n"
                "<!-- methodology:start id=beta owner=hub -->\n"
                "beta body\n"
                "<!-- methodology:end id=beta -->\n"
                "<!-- methodology:start id=local owner=repo -->\n"
                "consumer project\n"
                "<!-- methodology:end id=local -->\n")
    hub = _wire(monkeypatch, tmp_path, _HUB, {"clean-repo": consumer})
    findings, digest = br.run_report(hub, today="2026-07-11")
    f = [x for x in findings if "clean-repo" in x.evidence][0]
    assert f.status == "pass"
    assert "2 hub regions match" in f.evidence
    assert "1 project" in f.evidence
    assert "| clean-repo | 2 |" in digest


def test_reporter_marked_drifted_is_warn(monkeypatch, tmp_path):
    consumer = ("# CLAUDE.md\n"
                "<!-- methodology:start id=alpha owner=hub -->\n"
                "DRIFTED alpha\n"
                "<!-- methodology:end id=alpha -->\n"
                "<!-- methodology:start id=beta owner=hub -->\n"
                "beta body\n"
                "<!-- methodology:end id=beta -->\n")
    hub = _wire(monkeypatch, tmp_path, _HUB, {"drift-repo": consumer})
    findings, digest = br.run_report(hub, today="2026-07-11")
    f = [x for x in findings if "drift-repo" in x.evidence][0]
    assert f.status == "warn"
    assert "drift: alpha" in f.evidence
    assert "consumers_drift: 1" in digest


def test_reporter_unmarked_is_warn_and_counted(monkeypatch, tmp_path):
    hub = _wire(monkeypatch, tmp_path, _HUB,
                {"bare-repo": "# CLAUDE.md\n\nno markers at all\n"})
    findings, digest = br.run_report(hub, today="2026-07-11")
    f = [x for x in findings if "bare-repo" in x.evidence][0]
    assert f.status == "warn"
    assert "unmarked" in f.evidence
    assert "consumers_unmarked: 1" in digest


def test_reporter_missing_claude_md_is_unavailable(monkeypatch, tmp_path):
    hub = _wire(monkeypatch, tmp_path, _HUB, {"ghost-repo": None})
    findings, digest = br.run_report(hub, today="2026-07-11")
    f = [x for x in findings if "ghost-repo" in x.evidence][0]
    assert f.status == "unavailable"
    assert "consumers_unavailable: 1" in digest


def test_reporter_skips_the_hub_itself(monkeypatch, tmp_path):
    # A registered entry whose path IS the hub root must be skipped (not diffed vs itself).
    hub = tmp_path / "hub"
    hub.mkdir()
    (hub / "CLAUDE.md").write_text(_HUB, encoding="utf-8")

    class _State:
        def __init__(self, path):
            self.path = str(path)

    monkeypatch.setattr(br.audit, "discover_repos", lambda: ["the-hub"])
    monkeypatch.setattr(br.audit, "load_state", lambda name: _State(hub))
    findings, digest = br.run_report(hub, today="2026-07-11")
    assert not any("the-hub" in f.evidence for f in findings)
    assert "consumers_total: 0" in digest


def test_surface_line_distinguishes_unmarked(monkeypatch, tmp_path):
    hub = _wire(monkeypatch, tmp_path, _HUB, {"bare-repo": "# CLAUDE.md\n"})
    _findings, digest = br.run_report(hub, today="2026-07-11")
    f = tmp_path / "BOUNDARY-DRIFT.md"
    f.write_text(digest, encoding="utf-8")
    line = br.surface_line(f)
    assert line.startswith("[boundary]")
    assert "unmarked" in line and "2026-07-11" in line


# --- live-repo (asserts against the live fleet, not a tmp fixture) -----------

@pytest.mark.live_repo
def test_live_hub_baseline_and_consumers_legal():
    # (a) the grandfather landed: the hub baseline carries >= 1 owner=hub region.
    hub_text = (br._REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    regions, _warns = br.parse_regions(hub_text)
    baseline = br.build_baseline(regions)
    assert len(baseline) >= 1

    findings, digest = br.run_report()
    # (b) the digest renders with every discovered consumer present in a LEGAL state
    #     (do NOT pin "all unmarked" — that encodes today's pre-rollout moment and would
    #     falsely fail at first consumer rollout; the rollout fact is JOURNAL evidence).
    legal = {"pass", "warn", "unavailable"}
    consumer_findings = [f for f in findings
                         if f.check_name == "claude_md_boundary"
                         and not f.evidence.startswith("hub baseline")]
    assert consumer_findings, "expected >=1 registered consumer"
    for f in consumer_findings:
        assert f.status in legal, f"illegal status {f.status!r}: {f.evidence}"
    assert "| Repo | Hub regions |" in digest
