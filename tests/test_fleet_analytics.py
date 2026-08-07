"""Tests for scripts/fleet_analytics.py — the [#384] L5a descriptive analytics reporter.

Firing tests, not presence: the pure classifiers (numstat parse, rename aliasing, indentation
complexity, the three frame builders, the token map, the reference scan) are exercised
DIRECTLY on literals, and the end-to-end behaviour is proven against a REAL temp git repo.
The parser tests use BYTE literals in git's actual `-z` grammar — the shape was captured from
live `git log` output, so a format regression fails here rather than silently emptying a frame.

No live counts are pinned. Asserting "the hub has N hotspots" would encode today's moment and
break on the next commit; the live smoke asserts SHAPE and INVARIANTS only.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "fleet_analytics.py"


def _load():
    spec = importlib.util.spec_from_file_location("fleet_analytics", _P)
    module = importlib.util.module_from_spec(spec)
    # Register before exec so module-level @dataclass can resolve cls.__module__.
    sys.modules["fleet_analytics"] = module
    spec.loader.exec_module(module)
    return module


fa = _load()
CFG = fa.Config()


def _hdr(sha: str, ts: int, subject: str = "s") -> bytes:
    return f"\x01{sha}\x02{ts}\x02{ts}\x02{subject}".encode()


# ---------------------------------------------------------------------------
# 1. The numstat parse -- byte literals in git's real -z grammar
# ---------------------------------------------------------------------------

def test_parse_normal_change_record():
    raw = _hdr("a" * 40, 1700) + b"\x00\n3\t1\tsrc/a.py\x00"
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == []
    assert len(commits) == 1
    (ch,) = commits[0].changes
    assert (ch.path, ch.added, ch.deleted, ch.binary) == ("src/a.py", 3, 1, False)
    assert commits[0].ts == 1700


def test_parse_rename_consumes_two_following_tokens():
    """The -z rename record is `adds\\tdels\\t` with an EMPTY path, then old, then new.

    Verified against live `git log` output. This is why -z is load-bearing: without it the
    same rename arrives as `{a => b}` or `a => b`, both of which need bespoke parsing.
    """
    raw = _hdr("b" * 40, 1800) + b"\x00\n0\t0\t\x00docs/old.md\x00docs/new.md\x00"
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == []
    (ch,) = commits[0].changes
    assert ch.path == "docs/new.md"
    assert ch.old_path == "docs/old.md"


def test_parse_binary_record_is_zero_churn_not_an_anomaly():
    raw = _hdr("c" * 40, 1900) + b"\x00\n-\t-\tassets/logo.png\x00"
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == []
    (ch,) = commits[0].changes
    assert ch.binary is True
    assert (ch.added, ch.deleted) == (0, 0)


def test_parse_empty_commit_yields_commit_with_no_changes():
    raw = _hdr("d" * 40, 2000) + b"\x00"
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == []
    assert len(commits) == 1 and commits[0].changes == ()


def test_parse_multiple_commits_in_one_stream():
    raw = (_hdr("e" * 40, 2100) + b"\x00\n1\t0\ta.py\x00"
           + _hdr("f" * 40, 2200) + b"\x00\n2\t0\tb.py\x00")
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == []
    assert [c.ts for c in commits] == [2100, 2200]


def test_parse_garbage_becomes_an_anomaly_and_never_raises():
    """A silent skip is how a format assumption breaks unnoticed -- anomalies must surface."""
    raw = _hdr("0" * 40, 2300) + b"\x00\nnot-a-numstat-record\x00"
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert len(anomalies) == 1 and "unrecognized" in anomalies[0]
    assert commits[0].changes == ()


def test_parse_empty_input_is_clean():
    assert fa.parse_numstat_stream(b"") == ([], [])


def test_parse_truncated_rename_is_an_anomaly():
    raw = _hdr("1" * 40, 2400) + b"\x00\n0\t0\t\x00only-old-path"
    _commits, anomalies = fa.parse_numstat_stream(raw)
    assert any("rename" in a for a in anomalies)


def test_posix_strips_dot_slash_prefix_not_characters():
    """`lstrip('./')` would strip leading dots -- mangling dotfiles. Prefix-strip only."""
    assert fa._posix("./a/b.py") == "a/b.py"
    assert fa._posix(".pre-commit-config.yaml") == ".pre-commit-config.yaml"
    assert fa._posix("a\\b.py") == "a/b.py"


# ---------------------------------------------------------------------------
# 2. Rename aliasing
# ---------------------------------------------------------------------------

def _commit(ts, *changes):
    return fa.CommitRec("x" * 40, ts, ts, "s", tuple(changes))


def _chg(path, old=None, added=5, deleted=0, binary=False):
    return fa.FileChange(path, old, added, deleted, binary)


def test_rename_alias_requires_newest_first_ordering():
    commits = [_commit(300, _chg("new.md", old="old.md")), _commit(200, _chg("old.md"))]
    alias = fa.build_rename_alias(commits)
    assert alias == {"old.md": "new.md"}
    assert fa.canonical_path("old.md", alias) == "new.md"


def test_canonical_path_follows_a_three_hop_chain():
    commits = [_commit(300, _chg("c.md", old="b.md")), _commit(200, _chg("b.md", old="a.md"))]
    alias = fa.build_rename_alias(commits)
    assert fa.canonical_path("a.md", alias) == "c.md"


def test_canonical_path_survives_a_cycle():
    alias = {"a": "b", "b": "a"}
    assert fa.canonical_path("a", alias) in {"a", "b"}  # terminates, does not hang


def test_renamed_file_keeps_its_pre_rename_revisions():
    """Aliasing must run BEFORE the existence intersection, or a rename resets history."""
    commits = [_commit(300, _chg("new.md", old="old.md"))] + [
        _commit(200 - i, _chg("old.md")) for i in range(4)]
    alias = fa.build_rename_alias(commits)
    revs = fa.revision_counts(commits, alias, {"new.md"}, since_ts=None, cfg=CFG)
    assert revs["new.md"] == 5
    assert "old.md" not in revs


# ---------------------------------------------------------------------------
# 3. Indentation complexity (the D2 deviation)
# ---------------------------------------------------------------------------

def test_flat_markdown_weighted_lines_equals_line_count():
    """Pins D2. Under pure CodeScene (sum of indents) a flat prose doc scores 0 and could
    never rank; the +1 per line is what makes a docs-heavy corpus measurable at all."""
    prof = fa.indent_profile("alpha\nbeta\ngamma\n")
    assert prof.total_indent == 0          # the pure CodeScene quantity
    assert prof.weighted_lines == prof.n_lines == 3


def test_indent_profile_counts_depth():
    prof = fa.indent_profile("a\n    b\n        c\n")
    assert (prof.n_lines, prof.total_indent, prof.max_indent) == (3, 3, 2)
    assert prof.weighted_lines == 6


def test_indent_profile_expands_tabs_and_skips_blank_lines():
    prof = fa.indent_profile("a\n\n   \n\tb\n")
    assert prof.n_lines == 2               # blank + whitespace-only skipped
    assert prof.max_indent == 1            # one tab -> 4 spaces -> 1 unit


def test_indent_profile_handles_crlf():
    assert fa.indent_profile("a\r\n    b\r\n").n_lines == 2


def test_indent_profile_empty_text():
    prof = fa.indent_profile("")
    assert prof.n_lines == 0 and prof.weighted_lines == 0


# ---------------------------------------------------------------------------
# 4. Hotspot frame
# ---------------------------------------------------------------------------

def _profiles(**kv):
    return {p: fa.indent_profile("x\n" * n) for p, n in kv.items()}


def test_hotspot_frame_excludes_deleted_files():
    """A file absent from `existing` can never rank -- it was deleted."""
    commits = [_commit(500 - i, _chg("gone.md"), _chg("here.md")) for i in range(6)]
    revs = fa.revision_counts(commits, {}, {"here.md"}, since_ts=None, cfg=CFG)
    df = fa.hotspot_frame(revs, _profiles(**{"here.md": 10}), cfg=CFG)
    assert list(df["file"]) == ["here.md"]


def test_hotspot_frame_min_revisions_floor_fires():
    revs = fa.Counter({"a.md": 4, "b.md": 9})
    df = fa.hotspot_frame(revs, _profiles(**{"a.md": 10, "b.md": 10}), cfg=CFG)
    assert list(df["file"]) == ["b.md"]


def test_hotspot_frame_ranks_more_revisions_higher_at_equal_complexity():
    revs = fa.Counter({"hot.md": 40, "warm.md": 10, "cool.md": 5})
    df = fa.hotspot_frame(revs, _profiles(**{"hot.md": 20, "warm.md": 20, "cool.md": 20}),
                          cfg=CFG)
    assert list(df["file"]) == ["hot.md", "warm.md", "cool.md"]


def test_hotspot_frame_file_without_a_profile_cannot_rank():
    """Binary / unreadable files have no complexity axis, so they are not hotspots."""
    revs = fa.Counter({"img.png": 50, "a.md": 10})
    df = fa.hotspot_frame(revs, _profiles(**{"a.md": 10}), cfg=CFG)
    assert list(df["file"]) == ["a.md"]


def test_hotspot_frame_empty_input_returns_typed_empty_frame():
    df = fa.hotspot_frame(fa.Counter(), {}, cfg=CFG)
    assert len(df) == 0 and "score" in df.columns


def test_concentration_flags_a_skewed_distribution():
    flat_share, flat_gini = fa.concentration([5] * 100)
    skew_share, skew_gini = fa.concentration([1] * 99 + [900])
    assert flat_gini == pytest.approx(0.0, abs=0.01)
    assert skew_gini > 0.8 and skew_share > flat_share


def test_concentration_handles_empty_and_zero():
    assert fa.concentration([]) == (0.0, 0.0)
    assert fa.concentration([0, 0]) == (0.0, 0.0)


# ---------------------------------------------------------------------------
# 5. Change coupling
# ---------------------------------------------------------------------------

def test_wide_commit_is_skipped_entirely_not_truncated():
    """Truncating to the first N picks an alphabetically-biased subset -- a silent
    distortion. Skipping is loud and counted."""
    wide = _commit(100, *[_chg(f"f{i:03}.py") for i in range(40)])
    narrow = _commit(101, _chg("a.py"), _chg("b.py"))
    existing = {f"f{i:03}.py" for i in range(40)} | {"a.py", "b.py"}
    sets, skipped = fa.commit_file_sets([wide, narrow], {}, existing, since_ts=None, cfg=CFG)
    assert skipped == 1
    assert sets == [frozenset({"a.py", "b.py"})]
    counts = fa.coupling_counts(sets)
    assert ("f000.py", "f001.py") not in counts      # the wide commit contributed nothing


def test_single_file_commit_contributes_no_pairs():
    sets, skipped = fa.commit_file_sets([_commit(1, _chg("solo.py"))], {}, {"solo.py"},
                                        since_ts=None, cfg=CFG)
    assert sets == [] and skipped == 0


def test_coupling_counts_are_order_independent():
    counts = fa.coupling_counts([frozenset({"b.py", "a.py"}), frozenset({"a.py", "b.py"})])
    assert counts == {("a.py", "b.py"): 2}


def test_jaccard_gate_kills_the_lopsided_pair():
    """A 6-revision file that always rides along with a 300-revision one reads as degree
    1.00 under CodeScene's formula. Jaccard is the symmetric gate that rejects it."""
    counts = fa.Counter({("rare.py", "hot.py"): 6})
    revs = fa.Counter({"rare.py": 6, "hot.py": 300})
    df, considered = fa.coupling_frame(counts, revs, cfg=CFG)
    assert considered == 1
    assert len(df) == 0                       # degree would be 1.0; jaccard 6/300 = 0.02


def test_genuinely_coupled_pair_is_admitted():
    counts = fa.Counter({("a.py", "b.py"): 9})
    revs = fa.Counter({"a.py": 10, "b.py": 10})
    df, _ = fa.coupling_frame(counts, revs, cfg=CFG)
    assert len(df) == 1
    assert df.iloc[0]["degree"] == pytest.approx(0.9)
    assert df.iloc[0]["jaccard"] == pytest.approx(9 / 11, abs=1e-3)


def test_min_co_changes_gate_fires():
    counts = fa.Counter({("a.py", "b.py"): 4})
    revs = fa.Counter({"a.py": 5, "b.py": 5})
    df, _ = fa.coupling_frame(counts, revs, cfg=CFG)
    assert len(df) == 0


def test_same_dir_is_a_column_not_a_filter():
    """test_x.py <-> x.py is healthy evidence, not noise -- surface it, do not drop it."""
    counts = fa.Counter({("pkg/x.py", "pkg/y.py"): 9})
    revs = fa.Counter({"pkg/x.py": 10, "pkg/y.py": 10})
    df, _ = fa.coupling_frame(counts, revs, cfg=CFG)
    assert len(df) == 1 and bool(df.iloc[0]["same_dir"]) is True


def test_mechanical_lockstep_pairs_sort_below_genuine_coupling():
    counts = fa.Counter({("m1.py", "m2.py"): 10, ("g1.py", "g2.py"): 9})
    revs = fa.Counter({"m1.py": 10, "m2.py": 10, "g1.py": 10, "g2.py": 12})
    df, _ = fa.coupling_frame(counts, revs, cfg=CFG)
    assert bool(df.iloc[-1]["mechanical"]) is True


def test_excluded_generated_files_never_reach_the_coupling_frame():
    """audit.py rewrites every ecosystem/<n>/state.yaml on every run; without the exclude
    those pairs co-change 100% forever and own the frame ([#384] R4)."""
    paths = [f"ecosystem/r{i}/state.yaml" for i in range(3)]
    commits = [_commit(500 - i, *[_chg(p) for p in paths]) for i in range(8)]
    sets, _ = fa.commit_file_sets(commits, {}, set(paths), since_ts=None, cfg=CFG)
    assert sets == []


def test_excluded_matches_root_level_and_nested():
    assert fa.excluded("ecosystem/ai-council/state.yaml", CFG.exclude) is True
    assert fa.excluded("logs/FLEET-HEALTH.md", CFG.exclude) is True
    assert fa.excluded("scripts/audit.py", CFG.exclude) is False


# ---------------------------------------------------------------------------
# 6. Rot -- the token map and the reference scan
# ---------------------------------------------------------------------------

def test_ambiguous_basename_resolves_to_shortest_unique_suffix():
    """Measured: 71 hub basenames collide (PROBES.md x56). Bare-basename matching is not
    viable, so an ambiguous name must fall back to a unique suffix."""
    tokens = fa.match_tokens({"a/PROBES.md", "b/PROBES.md"})
    assert "PROBES.md" not in tokens
    assert tokens["a/PROBES.md"] == "a/PROBES.md"
    assert tokens["b/PROBES.md"] == "b/PROBES.md"


def test_unique_basename_is_admitted_as_a_token():
    tokens = fa.match_tokens({"scripts/audit.py", "docs/notes.md"})
    assert tokens["audit.py"] == "scripts/audit.py"


def test_stoplisted_basename_contributes_full_path_only():
    """README.md is mentioned generically in prose; a repo-unique one is still unsafe."""
    tokens = fa.match_tokens({"docs/README.md", "scripts/audit.py"})
    assert "README.md" not in tokens
    assert tokens["docs/README.md"] == "docs/README.md"


def test_inbound_counts_distinct_referrers_not_mentions():
    """One doc naming a path 40 times is ONE referrer."""
    tokens = fa.match_tokens({"scripts/audit.py", "docs/a.md"})
    texts = {"docs/a.md": "see scripts/audit.py\n" * 40}
    all_c, excl_c, _ = fa.inbound_reference_counts(texts, tokens, cfg=CFG)
    assert all_c["scripts/audit.py"] == 1
    assert excl_c["scripts/audit.py"] == 1


def test_self_reference_is_excluded():
    tokens = fa.match_tokens({"scripts/audit.py"})
    texts = {"scripts/audit.py": "this file is scripts/audit.py"}
    all_c, _, _ = fa.inbound_reference_counts(texts, tokens, cfg=CFG)
    assert all_c.get("scripts/audit.py", 0) == 0


def test_backslash_paths_are_normalized_when_scanned():
    tokens = fa.match_tokens({"scripts/audit.py", "docs/a.md"})
    texts = {"docs/a.md": r"see scripts\audit.py"}
    all_c, _, _ = fa.inbound_reference_counts(texts, tokens, cfg=CFG)
    assert all_c["scripts/audit.py"] == 1


def test_index_referrer_is_excluded_structurally():
    """A file naming > index_referrer_cut targets is a generated index (registry.md, a TOC).
    It would give every file a uniform +1. Excluded by a structural rule, not a hand-list."""
    targets = {f"docs/f{i:03}.md" for i in range(60)}
    tokens = fa.match_tokens(targets | {"docs/INDEX.md", "docs/real.md"})
    texts = {
        "docs/INDEX.md": "\n".join(sorted(targets)),
        "docs/real.md": "see docs/f001.md",
    }
    all_c, excl_c, index_refs = fa.inbound_reference_counts(texts, tokens, cfg=CFG)
    assert "docs/INDEX.md" in index_refs
    assert all_c["docs/f001.md"] == 2          # index + real
    assert excl_c["docs/f001.md"] == 1         # index discounted
    assert excl_c.get("docs/f002.md", 0) == 0  # index-only reference does not count


def test_extract_path_tokens_finds_paths_and_ignores_prose():
    toks = fa.extract_path_tokens("read scripts/audit.py and docs/a.md but not plainword")
    assert "scripts/audit.py" in toks and "docs/a.md" in toks
    assert "plainword" not in toks


# ---------------------------------------------------------------------------
# 7. Rot frame
# ---------------------------------------------------------------------------

_DAY = 86400
_NOW = 1_800_000_000


def test_last_meaningful_ts_ignores_tiny_churn():
    commits = [_commit(_NOW, _chg("a.md", added=1, deleted=0)),
               _commit(_NOW - 10 * _DAY, _chg("a.md", added=50, deleted=5))]
    out = fa.last_meaningful_ts(commits, {}, {"a.md"}, cfg=CFG)
    assert out["a.md"] == _NOW - 10 * _DAY


def test_last_meaningful_ts_ignores_wide_sweeps():
    """A 200-file lint sweep is not a meaningful edit to any single file."""
    sweep = _commit(_NOW, *[_chg(f"f{i:03}.md", added=9) for i in range(40)])
    real = _commit(_NOW - 20 * _DAY, _chg("f001.md", added=30))
    out = fa.last_meaningful_ts([sweep, real], {}, {"f001.md"}, cfg=CFG)
    assert out["f001.md"] == _NOW - 20 * _DAY


def test_last_meaningful_ts_ignores_binary_changes():
    commits = [_commit(_NOW, _chg("i.png", binary=True))]
    assert fa.last_meaningful_ts(commits, {}, {"i.png"}, cfg=CFG) == {}


def test_rot_requires_both_age_and_referrers():
    last = {"old_linked.md": _NOW - 400 * _DAY, "old_orphan.md": _NOW - 400 * _DAY,
            "fresh_linked.md": _NOW - 5 * _DAY}
    refs = fa.Counter({"old_linked.md": 4, "fresh_linked.md": 4})
    existing = set(last)
    df, orphans = fa.rot_frame(last, refs, refs, existing, now_ts=_NOW,
                               history_days=1000, cfg=CFG)
    assert list(df["file"]) == ["old_linked.md"]
    assert orphans == 1                       # the stale, unreferenced one


def test_zero_referrer_stale_file_is_an_orphan_not_rot():
    """The asymmetry that defines the frame: unreferenced stale is harmless; referenced
    stale is a live liability because readers follow the pointer."""
    last = {"a.md": _NOW - 500 * _DAY}
    df, orphans = fa.rot_frame(last, fa.Counter(), fa.Counter(), {"a.md"}, now_ts=_NOW,
                               history_days=1000, cfg=CFG)
    assert len(df) == 0 and orphans == 1


def test_rot_single_referrer_is_below_the_min_refs_floor():
    last = {"a.md": _NOW - 500 * _DAY}
    refs = fa.Counter({"a.md": 1})
    df, orphans = fa.rot_frame(last, refs, refs, {"a.md"}, now_ts=_NOW,
                               history_days=1000, cfg=CFG)
    assert len(df) == 0 and orphans == 0      # referenced, so not an orphan either


def test_rot_age_pct_normalizes_against_repo_history():
    last = {"a.md": _NOW - 500 * _DAY}
    refs = fa.Counter({"a.md": 5})
    df, _ = fa.rot_frame(last, refs, refs, {"a.md"}, now_ts=_NOW, history_days=1000, cfg=CFG)
    assert df.iloc[0]["age_days"] == 500
    assert df.iloc[0]["age_pct"] == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# 8. Digest + surface line
# ---------------------------------------------------------------------------

def test_safe_strips_pipes_for_the_locked_finding_contract():
    assert "|" not in fa._safe("a | b")


def test_to_finding_matches_the_locked_three_field_shape():
    r = fa.RepoAnalytics("x", "pass", commits=5, files=3,
                         diagnostics={"hotspots": 1, "couplings": 2, "rot": 0, "orphans": 4})
    f = fa.to_finding(r)
    assert (f.check_name, f.status) == ("fleet_analytics", "pass")
    assert "|" not in f.evidence


def test_to_finding_reports_unavailable_repo():
    f = fa.to_finding(fa.RepoAnalytics("x", "unavailable", note="no HEAD"))
    assert f.status == "unavailable" and "no HEAD" in f.evidence


def test_digest_renders_every_section_with_no_repos():
    text = fa.build_digest([], "2026-07-22", CFG, {})
    for header in ["# Fleet analytics", "## Method and honest limits", "## Fleet roll-up",
                   "## Hotspots", "## Change coupling", "## Rot candidates",
                   "## Per-repo detail", "## Distribution diagnostics", "## Anomalies"]:
        assert header in text
    assert text.startswith("---")             # frontmatter present
    assert "review queue, not a verdict" in text


def test_digest_states_the_honest_limits_in_the_report_itself():
    """The digest is what gets read -- the limits cannot live only in the source docstring."""
    text = fa.build_digest([], "2026-07-22", CFG, {})
    assert "Staleness is not rot" in text
    assert "lower bound" in text
    assert "Cross-repo references are invisible" in text


def test_digest_is_ascii_only():
    text = fa.build_digest([], "2026-07-22", CFG, {})
    text.encode("ascii")                      # raises if a non-ASCII glyph slipped in


def test_surface_line_when_report_absent(tmp_path):
    assert "no report yet" in fa.surface_line(tmp_path / "missing.md")


def test_surface_line_reads_frontmatter(tmp_path):
    p = tmp_path / "FLEET-ANALYTICS.md"
    p.write_text("---\nrepos_mined: 6\ncommits_scanned: 99\nwindow_days: 365\n"
                 "top_hotspot: BACKLOG.md\ntop_hotspot_score: 0.99\n"
                 "coupling_pairs_admitted: 7\nrot_candidates: 3\nrun_date: 2026-07-22\n---\n",
                 encoding="utf-8")
    line = fa.surface_line(p)
    assert line.startswith("[analytics] 6 repos, 99 commits (365d)")
    assert "BACKLOG.md" in line and "2026-07-22" in line


# ---------------------------------------------------------------------------
# 9. End-to-end against a REAL temp git repo
# ---------------------------------------------------------------------------

def _run(args, cwd):
    subprocess.run(args, cwd=str(cwd), check=True, capture_output=True)


@pytest.fixture
def tiny_repo(tmp_path):
    """A real git repo with a rename, a delete, and a co-changing pair."""
    r = tmp_path / "tiny"
    r.mkdir()
    _run(["git", "init", "-q", "-b", "main"], r)
    _run(["git", "config", "user.email", "t@example.com"], r)
    _run(["git", "config", "user.name", "T"], r)

    (r / "old.md").write_text("line\n" * 20, encoding="utf-8")
    (r / "doomed.md").write_text("line\n" * 20, encoding="utf-8")
    (r / "a.py").write_text("x = 1\n" * 20, encoding="utf-8")
    (r / "b.py").write_text("y = 1\n" * 20, encoding="utf-8")
    _run(["git", "add", "-A"], r)
    _run(["git", "commit", "-qm", "init"], r)

    for i in range(6):  # a.py and b.py co-change every time
        (r / "a.py").write_text(f"x = {i}\n" * 20, encoding="utf-8")
        (r / "b.py").write_text(f"y = {i}\n" * 20, encoding="utf-8")
        _run(["git", "add", "-A"], r)
        _run(["git", "commit", "-qm", f"pair {i}"], r)

    _run(["git", "mv", "old.md", "new.md"], r)
    _run(["git", "commit", "-qm", "rename"], r)
    _run(["git", "rm", "-q", "doomed.md"], r)
    _run(["git", "commit", "-qm", "delete"], r)
    return r


@pytest.mark.slow
def test_end_to_end_tiny_repo(tiny_repo):
    raw, err = fa.mine_repo_log(tiny_repo)
    assert err is None
    commits, anomalies = fa.parse_numstat_stream(raw)
    assert anomalies == [], f"format assumption broke: {anomalies}"

    existing = fa.list_tracked(tiny_repo)
    assert "new.md" in existing
    assert "doomed.md" not in existing        # deleted files never rank

    alias = fa.build_rename_alias(commits)
    revs = fa.revision_counts(commits, alias, existing, since_ts=None, cfg=CFG)
    assert revs["new.md"] >= 2                # carries its pre-rename revision
    assert "old.md" not in revs
    assert "doomed.md" not in revs

    sets, _ = fa.commit_file_sets(commits, alias, existing, since_ts=None, cfg=CFG)
    counts = fa.coupling_counts(sets)
    assert counts[("a.py", "b.py")] >= 6      # the co-changing pair is detected


@pytest.mark.slow
def test_analyze_repo_on_a_real_repo_is_shaped_correctly(tiny_repo):
    r = fa.analyze_repo("tiny", tiny_repo, CFG, _NOW)
    assert r.status in {"pass", "unavailable"}
    if r.status == "pass":
        assert r.commits > 0 and r.files > 0
        assert r.diagnostics["files_unread"] >= 0


@pytest.mark.slow
def test_analyze_repo_fails_soft_on_a_non_repo(tmp_path):
    r = fa.analyze_repo("nope", tmp_path, CFG, _NOW)
    assert r.status == "unavailable"
    assert fa.to_finding(r).status == "unavailable"


def test_analyze_repo_fails_soft_on_unresolvable_path():
    r = fa.analyze_repo("gone", None, CFG, _NOW)
    assert r.status == "unavailable" and "unresolvable" in r.note


# ---------------------------------------------------------------------------
# 10. Live-repo smoke -- shape and invariants only, NEVER counts
# ---------------------------------------------------------------------------

@pytest.mark.live_repo
def test_hub_is_included_as_a_mining_target():
    """boundary_report SKIPS the hub (it is the diff baseline); this script must INCLUDE it.
    ecosystem/ holds only the consumers, so the hub is prepended explicitly."""
    fleet = fa.enumerate_fleet(fa._REPO_ROOT)
    assert len(fleet) >= 1
    assert fleet[0][1] == fa._REPO_ROOT
    names = [n for n, _ in fleet]
    assert len(names) == len(set(names)), "a repo was enumerated twice"

    # IDENTITY BY MARKER, NOT BY DIRECTORY NAME (2026-08-07, [#502]). This assertion used to
    # be `names[0] == ".dev-knowledge"`, a literal that is only true on the operator's host:
    # the GitHub Actions runner checks this repo out as `dev-knowledge`, DOTLESS. That is not
    # merely cosmetic -- mutmut refuses to mutate until its baseline test run is green, so the
    # hardcoded literal made the [#502] mutation pilot report all 84 mutants `not checked`
    # while its job stayed green. A test pinned to where it happens to be run is a portability
    # defect, and this one had a measurable cost.
    root = fleet[0][1]
    assert (root / "protocols" / "PLAYBOOK.md").is_file(), "hub marker missing"
    assert (root / "docs" / "decisions").is_dir(), "hub marker missing"

    # NAME derived from the git COMMON dir's parent, never `repo_root.name` -- the property
    # that stops a linked worktree inventing a fleet repo that does not exist. Re-derived here
    # through git directly rather than by calling `_hub_name`, so this is a check of the rule
    # and not an echo of the implementation.
    common = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-common-dir"],
                            capture_output=True, text=True, encoding="utf-8")
    if common.returncode == 0 and common.stdout.strip():
        primary = (root / common.stdout.strip()).resolve().parent
        assert names[0] == primary.name, (
            f"hub named {names[0]!r} but the primary checkout is {primary.name!r} -- "
            "the name must follow the common dir, not the current working tree")


@pytest.mark.live_repo
def test_reporter_is_not_registered_as_a_gate():
    """A reporter must never redden the ship-gate, and must not disturb the ALL_CHECKS
    count-pins that live in five places across the test suite."""
    names = {getattr(c, "__name__", "") for c in getattr(fa.audit, "ALL_CHECKS", [])}
    assert not any("analytics" in n for n in names)
