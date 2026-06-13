"""Tests for scripts/verify_handoff_probes.py — #163 handoff-probe teeth validator.

A read-only Layer-2 validator (mirrors #89 validate_doc_claims): structurally prove
every probe in a v5 bundle's PROBES.md *binds to live state* — RESOLVE-ONLY, no
subprocess (operator ruling; Critical Rule #4 "Layer 2 never executes"; zero false
positives). The §10 ladder it mechanizes:
  malformed row / missing source file / missing command target -> FAIL
  named source file present but the `#`-anchor reworded/moved   -> WARN anchor-missing
  command's executable absent from PATH                         -> skipped (degraded)
  well-formed, all named files + anchors resolve, exe present   -> PASS

Scope boundary (do NOT duplicate): the manual probe-gate still owns rationale-quality
judgment (HANDOFF_PROCESS §5); #161 owns any reusable probe-core. This is structure only.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import verify_handoff_probes as vhp  # noqa: E402
import audit as aud  # noqa: E402

# --- mini-bundle fixtures (a self-consistent temp repo) ---------------------

_HDR = "| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |"
_SEP = "|---|---|---|---|---|"

# A repo whose live state satisfies the live-grounded probes below.
_FILES = {
    "VISION.md": "# V\n\n## Vision\nWhat .dev-knowledge is.\n",
    "ARCHITECTURE.md": "# A\n\n## Purpose [CORE]\nLayer 2 of the ADR-28 model.\n",
    "scripts/audit.py": "ALL_CHECKS = []\n",
}

# Canonical ladder rows: (id, question, source-locator, why, verification-command).
_PASS_SYMBOL = ("P2", "how many checks are in ALL_CHECKS",
                "`ALL_CHECKS` in `scripts/audit.py`", "the count drifts every commit",
                "`python scripts/audit.py checks`")
_PASS_ANCHOR = ("P1a", "quote the opening line of Vision",
                "`VISION.md` `## Vision`", "a paraphrase is not a substring",
                "`grep -A4 '^## Vision' VISION.md`")
_FAIL_MISSING = ("PX", "answer from a ghost file",
                 "`GHOST.md`", "nothing live binds here",
                 "`grep x GHOST.md`")
_ANCHOR_MOVED = ("PY", "quote a reworded section",
                 "`VISION.md` `## Gone`", "the anchor moved",
                 "`grep x VISION.md`")
_MALFORMED = ("PZ", "missing its command cell",
              "`VISION.md`", "the row is incomplete", "")
# P5 false-FAIL trap: secondary backtick span names `audit.py` (no scripts/ prefix,
# absent at repo root). First-span-only extraction must keep this a PASS.
_P5_TRAP = ("P5", "freshness relation",
            "`ARCHITECTURE.md`", "a relation over commits",
            "`git log -1 --format=%cs -- ARCHITECTURE.md` vs the stamp (or `audit.py health`)")
# Pure live-state probe with a literal `|` inside the command's backtick span.
_PIPE_CELL = ("P3", "current HEAD + tree",
              "`live git`", "the sha moves on any commit",
              "`git log | grep foo`")


def _table(rows, hdr=_HDR, sep=_SEP):
    lines = [hdr, sep]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def _probes_md(rows, *, preamble="# Probe manifest\n<!-- scope: meta -->\n\n> contract prose\n\n## Teeth\n\n"):
    return preamble + _table(rows) + "\n"


def _init_bundle(tmp_path, rows, *, repo_files=None, slug="2026-06-12-b", probes_md=None):
    repo = tmp_path / "repo"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    for rel, content in (_FILES if repo_files is None else repo_files).items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    (bundle / "PROBES.md").write_text(
        _probes_md(rows) if probes_md is None else probes_md, encoding="utf-8")
    return bundle


def _by_id(results):
    return {r.probe_id: r for r in results}


# --- pure core: split_row (the named failure mode) --------------------------

def test_split_row_basic_five_columns():
    cells = vhp.split_row("| P2 | q | `s` | why | `cmd` |")
    assert cells == ["P2", "q", "`s`", "why", "`cmd`"]


def test_split_row_keeps_pipe_inside_backtick_span():
    # THE named failure mode: a literal `|` inside a backtick code span must NOT split
    # the row. `git log | grep foo` is ONE cell, so the row still has 5 columns.
    line = "| P3 | q | `live git` | why | `git log | grep foo` |"
    cells = vhp.split_row(line)
    assert len(cells) == 5
    assert cells[4] == "`git log | grep foo`"
    assert "|" in cells[4]  # the pipe survived inside the command cell


def test_backtick_spans_returns_all_contents():
    assert vhp.backtick_spans("`ALL_CHECKS` in `scripts/audit.py`") == [
        "ALL_CHECKS", "scripts/audit.py"]


def test_first_span_returns_only_the_first():
    # P5-trap fixture: first span is the canonical command; the `audit.py` shorthand is later.
    cmd = "`git log -1 -- ARCHITECTURE.md` vs the stamp (or `audit.py health`)"
    assert vhp.first_span(cmd) == "git log -1 -- ARCHITECTURE.md"


# --- pure core: token extraction --------------------------------------------

def test_file_tokens_extracts_paths_not_args_or_symbols():
    toks = vhp.file_tokens("`python scripts/audit.py checks`")
    assert "scripts/audit.py" in toks
    assert "checks" not in toks and "python" not in toks


def test_file_tokens_ignores_non_path_symbols():
    # ALL_CHECKS / **N collected** are not file paths -> never resolved (precision-over-recall).
    assert vhp.file_tokens("`ALL_CHECKS` `**N collected**` live git") == []


def test_header_tokens_only_picks_markdown_headers():
    toks = vhp.header_tokens("`VISION.md` `## Vision`")
    assert toks == ["## Vision"]


def test_lead_exe_is_first_command_token():
    assert vhp.lead_exe("python scripts/audit.py checks") == "python"
    assert vhp.lead_exe("git log -1") == "git"


# --- pure core: parse_probes (header-name mapping, multi-table) --------------

def test_parse_probes_maps_columns_by_header_name_ignoring_id_col():
    rows = vhp.parse_probes(_probes_md([_PASS_SYMBOL]))
    assert len(rows) == 1
    r = rows[0]
    assert r["id"] == "P2"
    assert "ALL_CHECKS" in r["source"]
    assert r["command"] == "`python scripts/audit.py checks`"
    assert r["question"].startswith("how many")
    assert r["why"]


def test_parse_probes_skips_non_probe_tables():
    other = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    md = other + "\n" + _probes_md([_PASS_SYMBOL])
    rows = vhp.parse_probes(md)
    assert [r["id"] for r in rows] == ["P2"]


def test_parse_probes_reads_multiple_probe_tables():
    md = (_probes_md([_PASS_ANCHOR])
          + "\n## More teeth\n\n" + _table([_PASS_SYMBOL]) + "\n")
    rows = vhp.parse_probes(md)
    assert {r["id"] for r in rows} == {"P1a", "P2"}


# --- verify(): the §10 ladder -----------------------------------------------

def test_verify_pass_on_live_grounded_symbol_probe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL])
    by = _by_id(vhp.verify(bundle))
    assert by["P2"].status == "pass"


def test_verify_pass_on_live_grounded_anchor_probe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_ANCHOR])
    by = _by_id(vhp.verify(bundle))
    assert by["P1a"].status == "pass"


def test_verify_fail_on_missing_source_no_live_binding(tmp_path):
    # bluffable / no live binding: the named file does not exist -> FAIL (never pass).
    bundle = _init_bundle(tmp_path, [_FAIL_MISSING])
    by = _by_id(vhp.verify(bundle))
    assert by["PX"].status == "fail"


def test_verify_anchor_missing_does_not_silent_pass(tmp_path):
    # file present, the `#`-anchor reworded away -> WARN anchor-missing (NOT pass, NOT fail).
    bundle = _init_bundle(tmp_path, [_ANCHOR_MOVED])
    by = _by_id(vhp.verify(bundle))
    assert by["PY"].status == "anchor-missing"
    assert by["PY"].status != "pass"


def test_verify_fail_on_malformed_row(tmp_path):
    bundle = _init_bundle(tmp_path, [_MALFORMED])
    by = _by_id(vhp.verify(bundle))
    assert by["PZ"].status == "fail"
    assert "malformed" in by["PZ"].detail.lower()


def test_verify_p5_trap_secondary_span_does_not_false_fail(tmp_path):
    # ARCHITECTURE.md exists; root `audit.py` does NOT. First-span-only extraction must
    # keep this PASS (the `audit.py` shorthand in the 2nd span is never resolved).
    bundle = _init_bundle(tmp_path, [_P5_TRAP])
    by = _by_id(vhp.verify(bundle))
    assert by["P5"].status == "pass"


def test_verify_pipe_in_backtick_command_parses_and_passes(tmp_path):
    # The pipe inside the command must not break parsing; pure-git probe -> pass (git present).
    bundle = _init_bundle(tmp_path, [_PIPE_CELL])
    by = _by_id(vhp.verify(bundle))
    assert "P3" in by
    assert by["P3"].status == "pass"


def test_verify_skipped_when_executable_absent(tmp_path, monkeypatch):
    # tool absent -> skipped (degraded coverage visible), NEVER a synthesized pass.
    monkeypatch.setattr(vhp, "_exe_available", lambda name: False)
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL])
    by = _by_id(vhp.verify(bundle))
    assert by["P2"].status == "skipped"
    assert by["P2"].status != "pass"


def test_format_findings_lists_only_fails_no_pipe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL, _FAIL_MISSING])
    out = vhp.format_findings(vhp.verify(bundle))
    assert "PX" in out
    assert "P2" not in out      # a passing probe is not listed
    assert "|" not in out


# --- deployed audit check: check_handoff_probes -----------------------------

def _repo_with_bundle(tmp_path, rows, **kw):
    return _init_bundle(tmp_path, rows, **kw).parents[2]


def test_check_passes_when_no_probe_bundle(tmp_path):
    findings = aud.check_handoff_probes(tmp_path)
    assert len(findings) == 1
    assert findings[0].check_name == "handoff_probes"
    assert findings[0].status == "pass"


def test_check_fail_class_gates_on_a_failing_probe(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_FAIL_MISSING])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"        # FAIL-class -> blocks /ship
    assert "|" not in findings[0].evidence


def test_check_warns_on_anchor_missing(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_ANCHOR_MOVED])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "warn"
    assert "anchor" in findings[0].evidence.lower()


def test_check_passes_when_all_probes_bind(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_PASS_SYMBOL, _PASS_ANCHOR])
    assert aud.check_handoff_probes(repo)[0].status == "pass"


def test_check_validates_latest_bundle_only(tmp_path):
    # An OLDER broken bundle must be ignored; only the LATEST (lexically max slug) is validated.
    repo = tmp_path / "repo"
    _init_bundle(tmp_path, [_FAIL_MISSING], slug="2026-06-01-old")
    # second bundle (latest) is clean
    bundle2 = repo / "docs" / "handoffs" / "2026-06-12-new"
    bundle2.mkdir(parents=True)
    (bundle2 / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "pass"        # older broken bundle ignored


def test_check_failsoft_on_error(tmp_path, monkeypatch):
    repo = _repo_with_bundle(tmp_path, [_PASS_SYMBOL])

    def _boom(*a, **k):
        raise RuntimeError("parser exploded")

    monkeypatch.setattr(aud._vhp, "verify", _boom)
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "warn"
    assert "exploded" in findings[0].evidence or "degraded" in findings[0].evidence


def test_check_is_registered_in_all_checks():
    assert aud.check_handoff_probes in aud.ALL_CHECKS
    names = [c.__name__.removeprefix("check_") for c in aud.ALL_CHECKS]
    assert "handoff_probes" in names


def test_registered_check_never_fails_on_live_repo():
    # Production contract: the live hub's latest bundle must resolve (pass/warn), never FAIL.
    findings = aud.check_handoff_probes(Path(aud._REPO_ROOT))
    assert findings[0].status in {"pass", "warn"}
