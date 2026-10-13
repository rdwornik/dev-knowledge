"""Tests for the generated HANDOFF STATE -- the seven F4 sections `gen_handoff.py` renders from
the rollups, the LEDGER and the map diff (batch BW lane D2 `handoff-gen`, row `[#680]` nearest).

RED-first (ADR-108 section B): written and watched to fail before `render_handoff_state` existed.
The load-bearing pair is `test_the_fixture_renders_the_seven_sections_each_naming_its_source`
(every section is present and says where it came from) and
`test_a_missing_input_is_printed_missing_never_silently_empty` (an absent input is LOUD).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

import gen_handoff as gh

_TODAY = "2026-10-13"

_ROLLUP = """\
# DIGEST -- B2-W4 rollup

batch BW wave D | expected 2 | received 2 | MISSING: none
lane-a | COMPLETED 1/1 | tests PASS | intent none | abcdef12 | $none | action none | open none
totals: COMPLETED 2

## DRAFT handoff
- STATE: main is `c1b65e6d`.
- PAST ERRORS WITH NO CHECK YET:
  1. A distiller import silently adopted a dispositioned orphan.
  2. `land` reads an in-progress baseline as UNATTRIBUTED.
  3. A refused integration branch blocks its slug.
- PRIORITIES: the B5 ruling.
"""

_LEDGER = """\
carried-by: OPEN
kind: LEDGER

# LEDGER -- dev-knowledge

## STATE -- each line is a claim followed by its witness

- **main is `c1b65e6d`.** Witness: `git fetch`.
- **F0 findings:** the Copilot run's lanes booted with no manifest.

## PAST ERRORS WITH NO CHECK YET

- Lanes booted with no manifest (F0.2).

## BLOCKED BY

1. **R98:** the operator rules on the known-reds expiry list.

## NEXT

1. **The night order runs.**
"""

_MAP = {
    "built_at": "d5276dded8724658fe57b5d6a83c906b8a37b886",
    "diff": {"added": ["file:scripts/new_organ.py"], "added_count": 1, "baseline": False,
             "removed": ["file:scripts/old_organ.py"], "removed_count": 1},
    "generator": "scripts/system_map.py build",
    "map_sha": "47a6388cda3cec80b4fe0976f979d93ba1c2eb9704243cff85dbdd6b2da5518c",
    "previous_sha": "1111111111111111111111111111111111111111111111111111111111111111",
    "node_count": 380,
    "nodes": [],
}


def _repo(tmp_path: Path) -> Path:
    """A minimal repo carrying the committed inputs the dated-items and ratification sections read."""
    root = tmp_path / "repo"
    (root / "logs").mkdir(parents=True)
    (root / "docs" / "decisions").mkdir(parents=True)
    (root / "logs" / "KNOWN-REDS-REGISTRY.json").write_text(json.dumps({
        "members": {
            "tests/test_a.py::test_one": {"task": "[#912]", "expiry": "2026-10-16"},
            "tests/test_a.py::test_two": {"task": "[#912]", "expiry": "2026-10-16"},
            "tests/test_b.py::test_three": {"task": "[#664]", "expiry": "2026-10-17"},
        },
        "members_by_os": {"windows-latest": {
            "tests/test_c.py::test_four": {"task": "[#1340]", "expiry": "2026-10-17"}}},
    }), encoding="utf-8")
    (root / ".methodology.yaml").write_text(
        "sanctioned_divergences:\n"
        "  - component: hub-rule-a\n    reason: r\n    review_date: 2026-10-13\n"
        "  - component: hub-rule-b\n    reason: r\n    expiry: 2026-11-01\n",
        encoding="utf-8")
    (root / "docs" / "decisions" / "ADR-125-governing-prose.md").write_text(
        "# ADR-125: Governing prose is replaced by code\n\n- **Status:** Proposed\n"
        "- **Date:** 2026-09-25\n", encoding="utf-8")
    (root / "docs" / "decisions" / "ADR-127-ci-verdict.md").write_text(
        "# ADR-127: CI is the verdict\n\n- **Status:** Accepted\n- **Date:** 2026-09-27\n",
        encoding="utf-8")
    return root


def _inputs(tmp_path: Path) -> "gh.StateInputs":
    (tmp_path / "ROLLUP.md").write_text(_ROLLUP, encoding="utf-8")
    (tmp_path / "LEDGER.md").write_text(_LEDGER, encoding="utf-8")
    (tmp_path / "map-record.json").write_text(json.dumps(_MAP), encoding="utf-8")
    return gh.StateInputs(rollups=(tmp_path / "ROLLUP.md",), ledger=tmp_path / "LEDGER.md",
                          map_record=tmp_path / "map-record.json")


def _sections(text: str) -> dict[str, str]:
    """`{title: body}` for each `## ` section, in order."""
    out: dict[str, str] = {}
    title = None
    for line in text.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            out[title] = ""
        elif title is not None:
            out[title] += line + "\n"
    return out


def test_the_fixture_renders_the_seven_sections_each_naming_its_source(tmp_path):
    text = gh.render_handoff_state(_repo(tmp_path), _inputs(tmp_path), today=_TODAY)
    sections = _sections(text)
    assert list(sections) == list(gh.STATE_SECTION_TITLES)
    assert len(gh.STATE_SECTION_TITLES) == 7
    for title, body in sections.items():
        assert "source:" in body, f"section {title!r} names no source"
        assert body.strip(), f"section {title!r} is empty"
    state, errors, prio, ratify, dated, pointers, mapd = sections.values()
    assert "main is `c1b65e6d`" in state and "totals: COMPLETED 2" in state
    # The rollup's three past errors AND the LEDGER's F0.2 one, each once.
    for needle in ("dispositioned orphan", "in-progress baseline", "blocks its slug",
                   "booted with no manifest"):
        assert errors.count(needle) == 1, (needle, errors)
    assert "R98" in prio and "The night order runs" in prio
    assert "ADR-125" in ratify and "ADR-127" not in ratify
    assert "2026-10-16" in dated and "[#912] 2" in dated and "EXPIRED" not in dated
    assert "hub-rule-a" in dated and "2026-10-13" in dated
    assert "protocols/HANDOFF_PROCESS.md" in pointers
    assert _MAP["map_sha"] in mapd and _MAP["previous_sha"] in mapd
    assert "+1 -1" in mapd and "scripts/new_organ.py" in mapd and "scripts/old_organ.py" in mapd


def test_a_missing_input_is_printed_missing_never_silently_empty(tmp_path):
    root = tmp_path / "empty-repo"
    root.mkdir()
    absent = gh.StateInputs(rollups=(tmp_path / "NO-ROLLUP.md",), ledger=None,
                            map_record=tmp_path / "no-record.json")
    text = gh.render_handoff_state(root, absent, today=_TODAY)
    sections = _sections(text)
    assert list(sections) == list(gh.STATE_SECTION_TITLES)
    for title, body in sections.items():
        assert body.strip(), f"section {title!r} is silently empty"
    assert "MISSING: rollup" in text
    assert "MISSING: LEDGER" in text
    assert "MISSING: map diff" in text
    assert "MISSING: logs/KNOWN-REDS-REGISTRY.json" in sections["5. Dated items"]
    assert "MISSING:" in sections["4. Ratification queue"]


def test_a_rollup_without_a_past_errors_block_says_so(tmp_path):
    (tmp_path / "R.md").write_text("totals: COMPLETED 1\n", encoding="utf-8")
    inputs = gh.StateInputs(rollups=(tmp_path / "R.md",), ledger=None, map_record=None)
    text = gh.render_handoff_state(_repo(tmp_path), inputs, today=_TODAY)
    assert "MISSING: a PAST ERRORS WITH NO CHECK YET block" in \
        _sections(text)["2. Past errors with no check yet"]


def test_an_expired_known_red_date_is_flagged(tmp_path):
    text = gh.render_handoff_state(_repo(tmp_path), _inputs(tmp_path), today="2026-10-16")
    dated = _sections(text)["5. Dated items"]
    line = next(ln for ln in dated.splitlines() if "2026-10-16" in ln and "[#912]" in ln)
    assert "EXPIRED" in line or "TODAY" in line


def test_the_writer_puts_the_state_in_the_bundle_file(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    out = gh._write_handoff_state(bundle, _repo(tmp_path), inputs=_inputs(tmp_path), today=_TODAY)
    assert out == bundle / gh.HANDOFF_STATE_FILE
    assert out.read_text(encoding="utf-8").count("\n## ") == 7


def test_the_cli_dry_run_writes_only_the_scratch_path(tmp_path, monkeypatch):
    monkeypatch.setattr(gh, "transport_root", lambda *a, **k: tmp_path)
    inputs = _inputs(tmp_path)
    out = tmp_path / "scratch" / "HANDOFF_STATE.md"
    handoffs = Path(gh._REPO_ROOT) / "docs" / "handoffs"
    before = sorted(p.name for p in handoffs.iterdir()) if handoffs.is_dir() else []
    res = CliRunner().invoke(gh.main, [
        "--state-out", str(out), "--rollup", str(inputs.rollups[0]),
        "--ledger", str(inputs.ledger), "--map-record", str(inputs.map_record),
        "--date", _TODAY])
    assert res.exit_code == 0, res.output
    assert out.is_file() and out.read_text(encoding="utf-8").count("\n## ") == 7
    after = sorted(p.name for p in handoffs.iterdir()) if handoffs.is_dir() else []
    assert before == after, "a state dry run must not write a bundle"


def test_a_state_out_inside_the_repo_is_refused(tmp_path, monkeypatch):
    """Codex r1 HIGH: `--state-out` takes the dry cut's target rule -- never a committable path."""
    monkeypatch.setattr(gh, "transport_root", lambda *a, **k: tmp_path)
    inputs = _inputs(tmp_path)
    target = Path(gh._REPO_ROOT) / "docs" / "handoffs" / "bw680-never" / "HANDOFF_STATE.md"
    res = CliRunner().invoke(gh.main, [
        "--state-out", str(target), "--rollup", str(inputs.rollups[0]),
        "--ledger", str(inputs.ledger), "--map-record", str(inputs.map_record)])
    assert res.exit_code != 0
    assert not target.exists() and not target.parent.exists()


def test_an_input_neither_committed_nor_on_the_transport_is_refused(tmp_path, monkeypatch):
    """Codex r1 HIGH: an override input must be a generated transport surface or a tracked file."""
    transport = tmp_path / "transport"
    transport.mkdir()
    monkeypatch.setattr(gh, "transport_root", lambda *a, **k: transport)
    loose = tmp_path / "loose"
    loose.mkdir()
    inputs = _inputs(loose)
    out = tmp_path / "scratch" / "HANDOFF_STATE.md"
    res = CliRunner().invoke(gh.main, ["--state-out", str(out), "--rollup", str(inputs.rollups[0])])
    assert res.exit_code != 0 and "rollup" in res.output
    assert not out.exists()


def test_each_source_without_a_past_errors_block_is_named_missing(tmp_path):
    """Codex r1 HIGH (F0.2): a source that records no PAST ERRORS block is named, never skipped --
    a past error recorded only in free text shows up as that source's MISSING line."""
    inputs = _inputs(tmp_path)
    (tmp_path / "LEDGER.md").write_text(_LEDGER.replace("PAST ERRORS WITH NO CHECK YET", "OTHER"),
                                        encoding="utf-8")
    text = gh.render_handoff_state(_repo(tmp_path), inputs, today=_TODAY)
    errors = _sections(text)["2. Past errors with no check yet"]
    assert "dispositioned orphan" in errors
    assert "MISSING: a PAST ERRORS WITH NO CHECK YET block in LEDGER" in errors


def test_an_incomplete_map_record_is_missing_not_a_clean_zero_diff(tmp_path):
    """Codex r2 HIGH: a record without `map_sha` or the diff counts is MISSING, never `+0 -0`."""
    inputs = _inputs(tmp_path)
    (tmp_path / "map-record.json").write_text(json.dumps({"node_count": 3}), encoding="utf-8")
    mapd = _sections(gh.render_handoff_state(_repo(tmp_path), inputs, today=_TODAY))[
        "7. Map sha and diff"]
    assert "MISSING: map diff" in mapd
    assert "+0 -0" not in mapd


def test_a_tracked_input_with_uncommitted_edits_is_refused(tmp_path, monkeypatch):
    """Codex r2 HIGH: a tracked file is committed only when it does not differ from HEAD."""
    repo = tmp_path / "repo"
    repo.mkdir()
    rec = repo / "record.json"
    rec.write_text(json.dumps(_MAP), encoding="utf-8")
    for args in (["init", "-q"], ["add", "record.json"],
                 ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "r"]):
        gh._git_status(repo, *args)
    assert gh._state_input_refusal(rec, "map-record", repo, None) is None
    rec.write_text(json.dumps({**_MAP, "map_sha": "edited"}), encoding="utf-8")
    assert "map-record" in (gh._state_input_refusal(rec, "map-record", repo, None) or "")


def test_a_state_out_symlink_into_the_repo_is_refused(tmp_path, monkeypatch):
    """Codex r2 HIGH: the output file is judged where it RESOLVES, not where its parent sits."""
    monkeypatch.setattr(gh, "transport_root", lambda *a, **k: tmp_path)
    inputs = _inputs(tmp_path)
    target = Path(gh._REPO_ROOT) / "docs" / "handoffs" / "bw680-never-link.md"
    link = tmp_path / "scratch" / "HANDOFF_STATE.md"
    link.parent.mkdir()
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("this platform refuses an unprivileged symlink")
    res = CliRunner().invoke(gh.main, [
        "--state-out", str(link), "--rollup", str(inputs.rollups[0]),
        "--ledger", str(inputs.ledger), "--map-record", str(inputs.map_record)])
    assert res.exit_code != 0
    assert not target.exists()


def test_an_unreadable_source_is_missing_in_section_two_even_beside_a_good_one(tmp_path):
    """Codex r3 HIGH: a rollup that cannot be read is named MISSING even when the LEDGER supplies
    past errors -- one good source never hides an absent one."""
    inputs = _inputs(tmp_path)
    both = gh.StateInputs(rollups=(tmp_path / "NO-ROLLUP.md",), ledger=inputs.ledger,
                          map_record=inputs.map_record)
    errors = _sections(gh.render_handoff_state(_repo(tmp_path), both, today=_TODAY))[
        "2. Past errors with no check yet"]
    assert "booted with no manifest" in errors
    assert "MISSING: rollup" in errors and "NO-ROLLUP.md" in errors


def test_sections_one_to_three_name_their_input_files(tmp_path):
    """Codex r3 HIGH: a source line names the FILE it read, not a bare 'LEDGER' or 'rollups'."""
    sections = _sections(gh.render_handoff_state(_repo(tmp_path), _inputs(tmp_path), today=_TODAY))
    for title in gh.STATE_SECTION_TITLES[:3]:
        source = next(ln for ln in sections[title].splitlines() if ln.startswith("source:"))
        assert "LEDGER.md" in source, (title, source)
    for title in gh.STATE_SECTION_TITLES[:2]:
        source = next(ln for ln in sections[title].splitlines() if ln.startswith("source:"))
        assert "ROLLUP.md" in source, (title, source)
