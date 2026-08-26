"""Tests for `scripts/journal_anchor.py`: the entry-split memo ([#533] leg 2, STEP 2/3), the
single-pass anchor index ([#587]) and the one-process spine parent map ([#588]).

The three arcs answer the same question at three depths -- stop re-doing work whose input has
not changed -- and they share one safety argument, so they share one test file. Sections 4 and
5 carry their own why-this-exists headers; the [#533] narrative below is the original.

WHY THIS FILE EXISTS. STEP-1 attribution measured `journal_anchor._entries` re-splitting the
same immutable 2607 KiB `JOURNAL.md` **934 times in one process** — 2.47 GB of regex work for
one answer, 76.9 s, 37% of `check_journal_spine_anchor` and 23% of the entire 43-check
`audit.py health` loop. The fix is a memo. The contract that ruled the memo also ruled its
hazard, in one sentence worth restating here because it is what these tests are actually for:

    "A stale anchor cache is WORSE than slow -- it produces false push-gate verdicts."

`journal_anchor` is imported by `audit.py`, `batch_manifest.py`, `block_unanchored_push.py` and
`enforcement_coverage.py`; `block_unanchored_push` is the ADR-85 HARD pre-push leg. A memo that
returned yesterday's entries would let an unanchored push through while reporting a pass, which
is the one failure mode this module's whole fail-CLOSED posture exists to prevent.

THE SAFETY ARGUMENT, stated so the tests below can check it rather than assume it: the memo is
keyed on the journal **text**, not on a path, an mtime or a run. A different journal is a
different key by construction, so "the file grew between two calls" cannot produce a stale hit —
there is nothing to invalidate. `test_append_between_runs_*` and `test_journal_text_is_not_cached`
are the pair that hold that property down, and the second is the more important one: the way this
memo could still go wrong later is somebody caching the FILE READ (`journal_text`) on top of it,
which WOULD be mtime-sensitive and WOULD go stale.

`-n 0` in-lane per the batch convention; none of these tests need git or the live tree.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess

import pytest

import journal_anchor as ja


# An independent restatement of the split rule, deliberately NOT imported from the module under
# test -- an oracle that shares the implementation's regex object proves nothing about the
# implementation. This is the pre-memo body, verbatim in behaviour.
_REFERENCE_SPLIT_RE = re.compile(r"(?=^### )", re.MULTILINE)


def _reference_entries(journal: str) -> list[str]:
    return [p for p in _REFERENCE_SPLIT_RE.split(journal) if p.strip()]


_FIXTURE = """# JOURNAL

Preamble prose that belongs to no entry.

### 2026-08-18 (a) - first entry

Anchors: `deadbee1`.
Body line.

### 2026-08-18 (b) - second entry

Confirmed `cafe0021` in passing prose.

### 2026-08-17 (a) - third entry

**Anchors:** `0badf00d`.
"""

_NEW_ENTRY = """
### 2026-08-19 (a) - appended after the first read

**Anchors:** `abcdef12`.
"""


@pytest.fixture(autouse=True)
def _clear_memo():
    """Every test starts from a cold cache and leaves one behind for nobody.

    Without this the tests are order-dependent: a hit-count assertion would read counters some
    other test warmed. `cache_clear` is part of the surface the memo must expose precisely so a
    caller -- here, the suite -- can reason about it.
    """
    ja._entries.cache_clear()
    yield
    ja._entries.cache_clear()


# --- (a) the memo returns identical entries on the second call -------------------------

def test_memoized_second_call_returns_identical_entries():
    first = ja._entries(_FIXTURE)
    second = ja._entries(_FIXTURE)
    assert first == second
    # FOUR chunks, not three: the split is a lookahead at `### `, so everything BEFORE the first
    # heading -- the `# JOURNAL` title and its preamble prose -- survives as chunk 0. Pinned
    # explicitly because it is the one non-obvious thing about this function's output, and a
    # memo is exactly the kind of change under which such a detail could quietly move.
    assert len(first) == 4
    assert first[0].startswith("# JOURNAL")
    assert all(e.startswith("### ") for e in first[1:])


def test_the_second_call_is_actually_a_cache_hit_not_a_recompute():
    """Correctness alone cannot tell a memo from a re-run; the counter can.

    This is the assertion that makes the change worth committing -- without it the suite would
    stay green if the memo were silently dropped by a later refactor.
    """
    ja._entries(_FIXTURE)
    assert ja._entries.cache_info().hits == 0
    ja._entries(_FIXTURE)
    info = ja._entries.cache_info()
    assert info.hits == 1
    assert info.misses == 1


def test_the_cache_is_bounded():
    """An UNBOUNDED cache over multi-megabyte journal texts is a leak, not an optimization.

    `JOURNAL.md` is ~2.6 MiB and the split result is another ~2.6 MiB of fresh strings, so an
    `lru_cache(maxsize=None)` here would pin ~5 MiB per distinct journal text for the life of
    the process. A long-lived caller is not hypothetical: the audit runner holds one process
    across all 43 checks.
    """
    assert ja._entries.cache_info().maxsize is not None


# --- (b) append-between-runs, in ONE process -------------------------------------------

def test_append_between_runs_is_seen_by_the_second_call(tmp_path):
    """The contract's hazard case, end to end and in a single process.

    A journal that GROWS between two reads must produce entries that include the new one. The
    memo cannot get this wrong because it keys on content -- but the test asserts the OUTCOME
    (the second call sees the appended entry), not the mechanism, so it stays valid if the
    keying strategy is ever changed to file identity.
    """
    (tmp_path / "JOURNAL.md").write_text(_FIXTURE, encoding="utf-8", newline="\n")

    before = ja._entries(ja.journal_text(tmp_path))
    assert len(before) == 4          # preamble chunk + three entries
    assert not any("appended after the first read" in e for e in before)

    with open(tmp_path / "JOURNAL.md", "a", encoding="utf-8", newline="\n") as fh:
        fh.write(_NEW_ENTRY)

    after = ja._entries(ja.journal_text(tmp_path))
    assert len(after) == 5
    assert any("appended after the first read" in e for e in after)
    assert any("abcdef12" in e for e in after)


def test_journal_text_is_not_cached(tmp_path):
    """The file READ must stay uncached -- this is where a stale-anchor bug would actually live.

    `_entries` is content-keyed and therefore safe by construction. `journal_text` is NOT: it is
    the only place a path/mtime-keyed memo could be introduced, and such a memo would make
    `block_unanchored_push` -- the ADR-85 HARD leg -- judge a push against a journal the operator
    had already amended. Pinned here so that regression has to break a test to land.
    """
    (tmp_path / "JOURNAL.md").write_text(_FIXTURE, encoding="utf-8", newline="\n")
    first = ja.journal_text(tmp_path)
    with open(tmp_path / "JOURNAL.md", "a", encoding="utf-8", newline="\n") as fh:
        fh.write(_NEW_ENTRY)
    second = ja.journal_text(tmp_path)
    assert second != first
    assert second.startswith(first)
    assert "abcdef12" in second


def test_distinct_journal_texts_do_not_share_a_cache_entry():
    grown = _FIXTURE + _NEW_ENTRY
    assert ja._entries(_FIXTURE) != ja._entries(grown)
    assert len(ja._entries(_FIXTURE)) == 4
    assert len(ja._entries(grown)) == 5


# --- (c) byte-identity against the uncached reference ----------------------------------

@pytest.mark.parametrize("text", [
    _FIXTURE,
    _FIXTURE + _NEW_ENTRY,
    "",
    "no headings at all, just prose\n",
    "### only an entry, no preamble\n",
    "### a\n### b\n### c\n",
    "   \n\n   \n",
    "#### not a match on its own line\n### a real one\n",
    "prose mentioning ### mid-line, which is not a heading\n### real\n",
])
def test_entries_are_byte_identical_to_the_uncached_reference(text):
    """(c) of the contract: the memo changes speed, never bytes.

    Run twice so the assertion covers BOTH the cold path and the cached path -- a memo that is
    correct on a miss and wrong on a hit is exactly the defect worth catching.
    """
    expected = _reference_entries(text)
    assert ja._entries(text) == expected
    assert ja._entries(text) == expected


def test_a_realistic_multi_entry_body_splits_identically_under_the_memo():
    body = "".join(f"### 2026-08-{d:02d} (a) - entry {d}\n\nAnchors: `{d:07x}`.\n\n"
                   for d in range(1, 40))
    assert ja._entries(body) == _reference_entries(body)
    assert ja._entries(body) == _reference_entries(body)
    assert len(ja._entries(body)) == 39


# --- the mutation hazard a memo introduces ----------------------------------------------

def test_a_caller_mutating_the_result_cannot_poison_the_cache():
    """Returning the cached container itself would let any caller corrupt every later reader.

    None of today's callers mutate -- `mention_not_record_warnings` only iterates -- so this
    guards the future, which is the only thing a cache-safety test can usefully guard.
    """
    first = ja._entries(_FIXTURE)
    first.append("INJECTED")
    first[0] = "CLOBBERED"
    second = ja._entries(_FIXTURE)
    assert "INJECTED" not in second
    assert second == _reference_entries(_FIXTURE)


# --- the consumer's own output must not move --------------------------------------------

def test_mention_not_record_warnings_is_stable_across_repeated_calls(monkeypatch):
    """The one live consumer of `_entries`, exercised on both the cold and the cached path.

    `introduced` is stubbed rather than driven from a real repo: this test is about the split
    memo, and shelling out to git here would make a cache test depend on process spawning.
    """
    monkeypatch.setattr(ja, "introduced",
                        lambda repo, sha: ["cafe0021" + "0" * 32, "0badf00d" + "0" * 32])
    first = ja.mention_not_record_warnings(object(), "irrelevant", _FIXTURE)
    second = ja.mention_not_record_warnings(object(), "irrelevant", _FIXTURE)
    assert first == second
    # `cafe002` is mentioned in prose only; `0badf00` sits on an explicit `**Anchors:**` line.
    assert len(first) == 1
    assert "cafe002" in first[0]


# ==========================================================================================
# The `introduced` memo -- the SECOND pathology STEP-1 attribution found, and an addition
# BEYOND the two mechanisms the contract named. It is tested harder than the first for that
# reason: it caches the result of a git read, where `_entries` only caches a string split.
#
# The safety argument it rests on: what a commit INTRODUCED is fixed forever by the commit's
# own hash, because its parents -- and therefore their whole ancestry -- are part of what the
# hash commits to. A full 40-hex SHA is thus an immutable key. A REF is not, so `introduced`
# refuses to cache one at all rather than caching it under a caveat.
# ==========================================================================================

_SHA_A = "a" * 40
_SHA_B = "b" * 40
_PARENT = "c" * 40


@pytest.fixture(autouse=True)
def _clear_introduced_memo():
    ja.introduced.cache_clear()
    yield
    ja.introduced.cache_clear()


#: The stub DAG, since [#588] made the batched map the fast path: `_SHA_A` is a `--no-ff`
#: merge of `_PARENT` and `_SHA_B`, and `_SHA_B` sits on `_PARENT`. So `_PARENT.._SHA_A`
#: brings in BOTH (the merge plus what it merged) while `_PARENT.._SHA_B` brings in one --
#: the shape the two organs actually judge, rather than a pair of canned strings.
#: Line shape is `<commit-date> <sha> <parent>...`, newest-first, as `--parents --timestamp`
#: emits it.
_STUB_PARENT_MAP = (f"300 {_SHA_A} {_PARENT} {_SHA_B}\n"
                    f"200 {_SHA_B} {_PARENT}\n"
                    f"100 {_PARENT}\n")


def _counting_git(calls):
    """A `_git` stand-in that records every invocation and answers the rev-list forms."""
    def _git(repo, *args):
        calls.append((str(repo), args))
        if args == ja._PARENT_MAP_ARGS:
            return _STUB_PARENT_MAP
        if args[:2] == ("rev-list", "--parents"):
            return f"{args[-1]} {_PARENT}\n"
        if args[0] == "rev-list":
            return f"{args[-1].split('..')[-1]}\n{_SHA_B}\n"
        raise AssertionError(f"unexpected git call: {args}")
    return _git


@pytest.fixture(autouse=True)
def _clear_parent_map():
    """[#588]'s map is process-global like the other two memos, so it is reset per test.

    `_MAP_GENERATION` is cleared alongside the `lru_cache`: leaving a bumped generation behind
    would make the NEXT test's first lookup a miss against an empty cache, so the two must be
    reset together or the isolation is only apparent.
    """
    ja._parent_map.cache_clear()
    ja._MAP_GENERATION.clear()
    yield
    ja._parent_map.cache_clear()
    ja._MAP_GENERATION.clear()


def test_introduced_memoizes_a_full_sha_and_stops_spawning_git(monkeypatch, tmp_path):
    """The whole point: the second identical call must cost ZERO subprocesses.

    Asserted on the git-call log rather than on a hit counter alone, because the saving that
    matters here is process spawns (~144 ms each on this platform), not cache bookkeeping.

    ONE call, not two, since [#588]: the batched `rev-list --parents --all` answers what the
    per-SHA `rev-list --parents -n 1` + `rev-list <range>` pair used to.
    """
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))

    first = ja.introduced(tmp_path, _SHA_A)
    assert len(calls) == 1                     # the batched parent map, and nothing else
    assert calls[0][1] == ja._PARENT_MAP_ARGS
    second = ja.introduced(tmp_path, _SHA_A)
    assert len(calls) == 1                     # unchanged: served from the memo
    assert first == second
    assert first == [_SHA_A, _SHA_B]           # the merge plus the commit it merged in
    assert ja.introduced.cache_info().hits == 1


def test_introduced_refuses_to_memoize_a_moving_ref(monkeypatch, tmp_path):
    """`main` is not an immutable key -- it moves -- so it must hit git every single time.

    This is the guard that makes the safety argument true rather than merely plausible: without
    it, a long-lived process could answer for a `main` that had since advanced.
    """
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))

    ja.introduced(tmp_path, "main")
    assert len(calls) == 2
    ja.introduced(tmp_path, "main")
    assert len(calls) == 4                     # re-read, not remembered
    assert ja.introduced.cache_info().hits == 0
    assert ja.introduced.cache_info().misses == 0   # never entered the cache at all


@pytest.mark.parametrize("ref", ["main", "HEAD", "a" * 7, "a" * 39, "A" * 40, "z" * 40,
                                 "refs/heads/main", "HEAD~1", ""])
def test_only_a_full_lowercase_hex_object_name_is_treated_as_immutable(ref):
    assert ja._FULL_SHA_RE.match(ref) is None


def test_a_full_sha_is_treated_as_immutable():
    assert ja._FULL_SHA_RE.match(_SHA_A) is not None
    assert ja._FULL_SHA_RE.match("0123456789abcdef" * 2 + "01234567") is not None


def test_distinct_shas_do_not_share_a_cache_entry(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))
    a = ja.introduced(tmp_path, _SHA_A)
    b = ja.introduced(tmp_path, _SHA_B)
    assert len(calls) == 1                     # [#588]: ONE map answers both SHAs
    assert a == [_SHA_A, _SHA_B] and b == [_SHA_B]
    assert a != b


def test_distinct_repos_do_not_share_a_cache_entry(monkeypatch, tmp_path):
    """Two checkouts can hold the same SHA; keying on the sha alone would be a real bug.

    True of the [#588] parent map as well as of the `introduced` memo -- a map is per repo, so
    the count here is one read EACH, not one read total.
    """
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))
    ja.introduced(tmp_path / "one", _SHA_A)
    ja.introduced(tmp_path / "two", _SHA_A)
    assert len(calls) == 2
    assert {c[0] for c in calls} == {str(tmp_path / "one"), str(tmp_path / "two")}


def test_a_caller_mutating_the_introduced_result_cannot_poison_the_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(ja, "_git", _counting_git([]))
    first = ja.introduced(tmp_path, _SHA_A)
    first.append("INJECTED")
    assert "INJECTED" not in ja.introduced(tmp_path, _SHA_A)


def test_an_anchor_error_is_never_cached(monkeypatch, tmp_path):
    """FAIL-LOUD must survive the memo: an unreadable history re-reads and re-raises.

    `lru_cache` does not store exceptions, so this holds for free -- but "holds for free" is
    the kind of property that quietly stops holding when somebody swaps the caching strategy,
    and this module's entire posture is that an unknown anchoring state never renders as clean.
    """
    calls = []

    def _boom(repo, *args):
        calls.append(args)
        raise ja.AnchorError("git exploded")

    monkeypatch.setattr(ja, "_git", _boom)
    for _ in range(2):
        with pytest.raises(ja.AnchorError):
            ja.introduced(tmp_path, _SHA_A)
    assert len(calls) == 2                     # a real git read on BOTH attempts
    # A raising call still counts as a MISS -- the lookup did miss -- but `currsize` is what
    # says whether anything was retained, and nothing was. Asserting on `currsize` rather than
    # on the miss counter is the difference between testing the property and testing the
    # bookkeeping.
    assert ja.introduced.cache_info().currsize == 0


def test_the_introduced_cache_is_bounded():
    assert ja.introduced.cache_info().maxsize is not None


def test_a_root_commit_still_introduces_only_itself(monkeypatch, tmp_path):
    """The `len(parents) < 2` branch, preserved through the split into _introduced_uncached."""
    monkeypatch.setattr(ja, "_git", lambda repo, *args: f"100 {_SHA_A}\n")
    assert ja.introduced(tmp_path, _SHA_A) == [_SHA_A]


# --- real git: the memo must not change the ANSWER -----------------------------------------

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


@requires_git
def test_memoized_introduced_matches_the_uncached_body_on_a_real_no_ff_merge(tmp_path):
    """Parity against a real DAG, which is the only oracle that proves the memo is honest.

    Builds root -> branch(2 commits) -> `--no-ff` merge, then asserts the memoized `introduced`
    equals `_introduced_uncached` for the merge (which must report the merge plus both brought
    commits) and for a plain non-merge spine entry, on both the cold and the cached path.
    """
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "f.txt").write_text("1\n", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-q", "-m", "root")
    _git(repo, "checkout", "-q", "-b", "side")
    for i in (2, 3):
        (repo / "f.txt").write_text(f"{i}\n", encoding="utf-8")
        _git(repo, "commit", "-q", "-am", f"side {i}")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "side", "-m", "merge side")

    spine = ja.spine_entries(repo, "main")
    merge_sha, root_sha = spine[0], spine[-1]

    memoized = ja.introduced(repo, merge_sha)
    assert memoized == ja._introduced_uncached(repo, merge_sha)
    assert ja.introduced(repo, merge_sha) == memoized       # cached path, same answer
    assert len(memoized) == 3                               # the merge + both side commits

    assert ja.introduced(repo, root_sha) == ja._introduced_uncached(repo, root_sha)
    assert ja.introduced(repo, root_sha) == [root_sha]


@requires_git
def test_is_anchored_is_unchanged_by_the_memo_on_a_real_repo(tmp_path):
    """The predicate the ADR-85 organs actually call, exercised twice through the cache."""
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "f.txt").write_text("1\n", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-q", "-m", "root")
    _git(repo, "checkout", "-q", "-b", "side")
    (repo / "f.txt").write_text("2\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "side work")
    side_sha = ja.spine_entries(repo, "side")[0]
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    merge_sha = ja.spine_entries(repo, "main")[0]

    naming = f"### entry\n\n**Anchors:** `{side_sha[:7]}`.\n"
    silent = "### entry\n\nno shas here\n"
    for _ in range(2):
        assert ja.is_anchored(repo, merge_sha, naming) is True
        assert ja.is_anchored(repo, merge_sha, silent) is False


# ==========================================================================================
# [#587] THE SINGLE-PASS ANCHOR INDEX.
#
# WHY THIS SECTION EXISTS. The [#533] memo above stopped the journal being RE-SPLIT per call;
# it did not stop the journal being RE-WALKED per introduced commit. Telemetry run f0caf15a
# (2026-08-26, `DEV_KNOWLEDGE_TELEMETRY=1 audit.py health --parallel` on this host) measured
# `check_journal_spine_anchor` at **197.8 s**, rank 1 of 46 checks and 35% of the whole health
# loop -- on a PRE-COMMIT gate. The shape PERF-RECON named (B1/B3) was
# `mention_not_record_warnings` looping introduced-commit -> entry -> `entry.splitlines()`,
# re-splitting 2.9 MB on every outer iteration, and `is_anchored` substring-scanning the same
# 2.9 MB per introduced commit.
#
# WHAT THESE TESTS ARE FOR. The inversion must change SPEED and nothing else, so the oracle is
# an independent restatement of the pre-inversion body (`_reference_warnings` below) -- not the
# module's own regexes, which would prove only that the implementation agrees with itself. The
# risk the index introduces is a DOMAIN risk rather than a caching one: it answers a substring
# question out of a set of 7-char hex windows, so the tests below pin the two ways that could
# silently narrow -- overlapping windows inside a longer run, and a needle that is not hex.
# ==========================================================================================

_REFERENCE_RECORD_RE = re.compile(r"^\*{0,2}Anchors?\b", re.IGNORECASE)


def _reference_warnings(shas, journal):
    """The pre-inversion `mention_not_record_warnings` body, restated independently."""
    entries = _reference_entries(journal)
    out = []
    for c in shas:
        short = c[:7]
        recorded = False
        mentioned = False
        for entry in entries:
            for line in entry.splitlines():
                if short not in line:
                    continue
                if _REFERENCE_RECORD_RE.match(line.strip()):
                    recorded = True
                else:
                    mentioned = True
        if mentioned and not recorded:
            out.append(f"anchored by mention, not by record: {short} appears outside an "
                       "explicit 'Anchors:' record line")
    return out


#: Deliberately awkward. `0badf00dcafe` is a TWELVE-char run, so `0badf00` and `badf00d` and
#: four more windows all live inside one token -- the case a tokenizer would get wrong and a
#: substring test gets right. `defaced` is seven hex letters occurring as an English word.
#: `DEADBEE1` is uppercase, which the lowercase predicate must NOT match. `cafe002` appears on
#: both a record line and a prose line, which is the `present AND recorded` case that must NOT
#: warn.
_INDEX_FIXTURE = """# JOURNAL

Preamble naming 0badf00dcafe in prose.

### 2026-08-18 (a) - first

**Anchors:** `cafe0021`, `1234567`.
Prose that also mentions cafe0021 in passing.

### 2026-08-18 (b) - second

The word defaced is seven hex letters. DEADBEE1 is uppercase.
Confirmed `9998887` in prose only.

### 2026-08-17 (a) - third

Anchors this arc's own spine: `abcdef0`.
"""


@pytest.fixture(autouse=True)
def _clear_anchor_index():
    ja._anchor_index.cache_clear()
    yield
    ja._anchor_index.cache_clear()


# --- (a) the window enumeration is a substring test, not a tokenizer --------------------

def test_hex_shorts_enumerates_every_window_inside_a_long_run():
    """`0badf00dcafe` is 12 chars, so it contains SIX distinct 7-char windows.

    A tokenizing implementation would record only the first (or only the whole token) and would
    then report `is_anchored` False for a commit whose short prefix sits mid-run -- a FALSE
    UNANCHORED verdict on the gate that refuses pushes. This is the assertion that keeps the
    index a substring index.
    """
    assert ja._hex_shorts("x 0badf00dcafe y") == {
        "0badf00", "badf00d", "adf00dc", "df00dca", "f00dcaf", "00dcafe"}


@pytest.mark.parametrize("line, expected", [
    ("nothing here", set()),
    ("short 123456 run", set()),                      # six chars: below the window
    ("exactly 1234567 seven", {"1234567"}),
    ("DEADBEE1 uppercase", set()),                    # the predicate is lowercase-only
    ("defaced", {"defaced"}),                         # prose that IS hex -- and must count
    ("`abcdef0`", {"abcdef0"}),                       # backticks are not hex, so they bound it
])
def test_hex_shorts_matches_the_substring_domain(line, expected):
    assert ja._hex_shorts(line) == expected


def test_every_index_key_really_occurs_in_the_text():
    """The index may not INVENT a key: `short in index.present` must imply `short in journal`.

    The converse direction (`short in journal` implies present, for a hex short) is covered by
    `test_index_agrees_with_the_raw_substring_test_on_the_live_journal`.
    """
    index = ja._anchor_index(_INDEX_FIXTURE)
    for short in index.present | index.recorded:
        assert short in _INDEX_FIXTURE, f"index invented {short!r}"


# --- (b) the classification: present / recorded -----------------------------------------

def test_the_index_splits_record_lines_from_prose_lines():
    index = ja._anchor_index(_INDEX_FIXTURE)
    assert "cafe002" in index.present and "cafe002" in index.recorded   # both lines
    assert "1234567" in index.recorded                                  # record line only
    assert "9998887" in index.present and "9998887" not in index.recorded
    assert "abcdef0" in index.recorded          # `Anchors this arc's own spine:` matches
    assert "0badf00" in index.present and "0badf00" not in index.recorded


def test_mention_not_record_warnings_is_byte_identical_to_the_pre_inversion_body(monkeypatch):
    """The contract's own done-when, at unit scale: findings byte-identical, order included."""
    shas = [s + "0" * 33 for s in ("9998887", "cafe002", "1234567", "0badf00", "abcdef0",
                                   "eeeeeee")]
    monkeypatch.setattr(ja, "introduced", lambda repo, sha: shas)
    got = ja.mention_not_record_warnings(object(), "irrelevant", _INDEX_FIXTURE)
    assert got == _reference_warnings(shas, _INDEX_FIXTURE)
    # Stated positively too, so a reference that silently became vacuous could not pass this:
    # only the prose-only short warns, and the ORDER follows `introduced`.
    assert len(got) == 2
    assert "9998887" in got[0] and "0badf00" in got[1]


@pytest.mark.parametrize("text", [
    _FIXTURE,
    _FIXTURE + _NEW_ENTRY,
    _INDEX_FIXTURE,
    "",
    "no headings at all, just prose\n",
    "### only an entry, no preamble\n",
    "   \n\n   \n",
    "### a\nAnchors: `1234567`\n### b\n1234567 in prose\n",     # recorded THEN mentioned
    "### a\n1234567 in prose\n### b\nAnchors: `1234567`\n",     # mentioned THEN recorded
    "### a\n**anchor:** `1234567`\n",                            # lowercase, singular, bolded
])
def test_warnings_match_the_reference_across_journal_shapes(monkeypatch, text):
    shas = [s + "0" * 33 for s in ("1234567", "cafe002", "deadbee", "0badf00", "abcdef1")]
    monkeypatch.setattr(ja, "introduced", lambda repo, sha: shas)
    expected = _reference_warnings(shas, text)
    assert ja.mention_not_record_warnings(object(), "x", text) == expected
    assert ja.mention_not_record_warnings(object(), "x", text) == expected   # cached path


# --- (c) the inversion itself: ONE journal walk, not one per commit ----------------------

def test_the_journal_is_walked_once_no_matter_how_many_commits(monkeypatch):
    """THE regression guard for [#587] -- the assertion that makes the change worth committing.

    Counting `_entries` calls is the honest proxy for "walks the journal": the pre-inversion
    body called it once per introduced commit, and it is the single function both the old inner
    loop and the new index builder go through. Asserted BEHAVIOURALLY rather than on wall-clock
    (flaky under load, first thing muted) and rather than on source text (which would pass for a
    rewrite that reintroduced the same shape under a different spelling).

    Call-counting works here where `test_spine_date_lookup_stays_batched` had to fall back to
    source inspection, and the difference is worth naming: that test drives the leg through
    `audit.py`, where the dual-import idiom means a patched top-level `journal_anchor` may not
    be the module object under test. This test calls `ja` directly, so there is one module.
    """
    calls = []
    real = ja._entries
    monkeypatch.setattr(ja, "_entries", lambda journal: (calls.append(1), real(journal))[1])
    monkeypatch.setattr(ja, "introduced",
                        lambda repo, sha: [f"{i:07x}" + "0" * 33 for i in range(200)])

    ja.mention_not_record_warnings(object(), "x", _INDEX_FIXTURE)
    assert len(calls) == 1, "the journal is being re-walked per introduced commit again"
    ja.mention_not_record_warnings(object(), "x", _INDEX_FIXTURE)
    assert len(calls) == 1, "the second scan re-walked the journal instead of hitting the memo"


def test_the_index_is_a_cache_hit_on_the_second_call():
    ja._anchor_index(_INDEX_FIXTURE)
    assert ja._anchor_index.cache_info().hits == 0
    ja._anchor_index(_INDEX_FIXTURE)
    info = ja._anchor_index.cache_info()
    assert info.hits == 1 and info.misses == 1


def test_the_index_cache_is_bounded():
    """Same leak argument as `_entries`': the audit runner holds ONE process across 46 checks."""
    assert ja._anchor_index.cache_info().maxsize is not None


def test_a_grown_journal_is_a_different_index(tmp_path):
    """The [#533] hazard, re-asked of the new memo: a stale anchor index would produce false
    push-gate verdicts, so a journal that GREW must not register a hit against the old one."""
    (tmp_path / "JOURNAL.md").write_text(_FIXTURE, encoding="utf-8", newline="\n")
    before = ja._anchor_index(ja.journal_text(tmp_path))
    assert "abcdef1" not in before.present
    with open(tmp_path / "JOURNAL.md", "a", encoding="utf-8", newline="\n") as fh:
        fh.write(_NEW_ENTRY)
    after = ja._anchor_index(ja.journal_text(tmp_path))
    assert "abcdef1" in after.present and "abcdef1" in after.recorded


def test_a_caller_cannot_mutate_the_cached_index():
    index = ja._anchor_index(_INDEX_FIXTURE)
    assert isinstance(index.present, frozenset) and isinstance(index.recorded, frozenset)


# --- (d) `is_anchored` is the same predicate, answered from the index --------------------

def test_is_anchored_agrees_with_the_raw_substring_test(monkeypatch):
    """§A7 unchanged: anchored iff the journal NAMES a SHA the entry introduced."""
    for short, expected in (("0badf00", True), ("badf00d", True), ("9998887", True),
                            ("deadbee", False), ("eeeeeee", False)):
        monkeypatch.setattr(ja, "introduced", lambda repo, sha, s=short: [s + "0" * 33])
        assert ja.is_anchored(object(), "x", _INDEX_FIXTURE) is expected
        assert (short in _INDEX_FIXTURE) is expected      # the test the index replaced


def test_a_non_object_name_needle_falls_back_instead_of_reporting_absent(monkeypatch):
    """The index's domain is 7-char lowercase hex. A needle outside it is NOT evidence of
    absence, so both consumers fall back to their pre-inversion scan rather than answering
    confidently from a set that could never have held it.

    Unreachable from any caller in this repo -- `introduced` yields git object names -- which is
    exactly why it is pinned: an unreachable narrowing is the kind that is discovered later, by
    a caller that did not exist when the narrowing was made.
    """
    journal = "### a\n\nthe branch main-2 shipped\n"
    monkeypatch.setattr(ja, "introduced", lambda repo, sha: ["main-2"])
    assert ja.is_anchored(object(), "x", journal) is True
    assert ja.mention_not_record_warnings(object(), "x", journal) == \
        _reference_warnings(["main-2"], journal)


# --- (e) the live corpus, which is the only oracle for scale ----------------------------

_LIVE_JOURNAL = pathlib.Path(__file__).resolve().parents[1] / "JOURNAL.md"


@pytest.mark.skipif(not _LIVE_JOURNAL.exists(), reason="live JOURNAL.md not present")
def test_index_agrees_with_the_raw_substring_test_on_the_live_journal():
    """Both directions, over the real 2.9 MB corpus -- no git, just the file.

    Direction 1: every key the index holds occurs in the text (it invents nothing).
    Direction 2: every 7-char hex short the RAW test finds is in the index (it drops nothing).
    Direction 2 is the one that matters for the gate: a dropped key is a false UNANCHORED.
    """
    journal = _LIVE_JOURNAL.read_text(encoding="utf-8")
    index = ja._anchor_index(journal)
    assert len(index.present) > 100, "the live corpus should be rich in object names"
    for short in index.present:
        assert short in journal
    # Direction 2, sampled deterministically across the whole corpus rather than exhaustively
    # (2.9M windows is a minute of pure Python for a property one window in ten already pins).
    hex_run = re.compile(r"[0-9a-f]{7,}")
    checked = 0
    for m in hex_run.finditer(journal):
        run = m.group()
        for i in range(0, len(run) - 6, 10):
            checked += 1
            assert run[i:i + 7] in index.present, f"index dropped {run[i:i + 7]!r}"
    assert checked > 100


# ==========================================================================================
# [#588] ONE GIT PROCESS FOR THE WHOLE SPINE.
#
# WHY THIS SECTION EXISTS. `introduced` used to spawn TWO `git rev-list` processes per unique
# spine entry. This module's own docstring records the measurement that motivated the [#533]
# memo -- 808 spawns, 116.8 s in one `audit.py health` run -- and the memo removed only the
# duplicate half. The 2026-08-26 parity harness measured the remainder at 82.6 s for 312 spine
# entries, i.e. essentially the whole residual cost of the #1 check in a PRE-COMMIT gate.
#
# WHAT THESE TESTS ARE FOR. A batched map trades subprocesses for a Python graph walk, and
# introduces exactly two ways to be wrong that git could not be: (1) the SET can differ, and a
# set that is too LARGE reports a spine entry ANCHORED that is not -- a false clean on a push
# gate, the worst direction; (2) the ORDER can differ, and order is output here, because
# `check_journal_spine_anchor` joins the FIRST FIVE mention-warnings into its evidence. So the
# oracle is `_introduced_uncached` -- git's own answer -- and the assertions are on equality of
# the LIST, never on membership. The third hazard is staleness: a map built before a commit
# existed must not answer for it, which is `test_a_commit_made_after_the_map_was_built`.
# ==========================================================================================


def _chain_parent_map(n: int) -> str:
    """`--parents --timestamp --all` output for a spine of `n` `--no-ff` merges.

    `s{i}` merges `b{i}` onto `s{i+1}`; `s{n-1}` is the root. Newest-first, which is the order
    git emits. Dates DESCEND with `i` and each merge is one second newer than the side commit
    it brought in, so the expected order is [merge, side] and a regression that dropped the
    date ordering would show up here rather than only on a real repo.
    """
    lines = []
    for i in range(n - 1):
        merge_ts, side_ts = 10_000 - 2 * i, 10_000 - 2 * i - 1
        lines.append(f"{merge_ts} {i:040x} {i + 1:040x} {i + 1000:040x}")
        lines.append(f"{side_ts} {i + 1000:040x} {i + 1:040x}")
    lines.append(f"{10_000 - 2 * n} {n - 1:040x}")               # root: no parents
    return "\n".join(lines) + "\n"


def test_one_git_process_answers_the_whole_spine(monkeypatch, tmp_path):
    """THE regression guard for [#588]: process count is O(1) in the length of the range.

    200 spine entries answered by ONE `git rev-list`, where the pre-batch shape spawned 400.
    Call-counting is the right instrument here (unlike `test_spine_date_lookup_stays_batched`,
    which had to inspect source because it drives its leg through `audit.py`'s dual import):
    this test calls `ja` directly, so the patched `_git` IS the one under test. And the saving
    being claimed is process spawns, so counting them is measuring the thing rather than a
    proxy for it.
    """
    calls = []

    def _git(repo, *args):
        calls.append(args)
        if args == ja._PARENT_MAP_ARGS:
            return _chain_parent_map(200)
        raise AssertionError(f"per-SHA git read reintroduced: {args}")

    monkeypatch.setattr(ja, "_git", _git)
    for i in range(199):
        assert ja.introduced(tmp_path, f"{i:040x}") == [f"{i:040x}", f"{i + 1000:040x}"]
    assert ja.introduced(tmp_path, f"{199:040x}") == [f"{199:040x}"]      # the root
    assert len(calls) == 1, f"{len(calls)} git processes for a 200-entry spine"


def test_a_sha_the_map_cannot_reach_falls_back_to_git_rather_than_answering_wrong(
        monkeypatch, tmp_path):
    """A commit reachable from no ref is absent from `--all`. Absence is NOT an answer.

    The map defers to `_introduced_uncached` -- git's definition -- because the alternative
    (treating an unknown SHA as introducing only itself) would silently shrink an introduced
    set, and a shrunk set turns an anchored spine entry into a reported GAP.
    """
    calls = []

    def _git(repo, *args):
        calls.append(args)
        if args == ja._PARENT_MAP_ARGS:
            return _STUB_PARENT_MAP
        if args[:2] == ("rev-list", "--parents"):
            return f"{args[-1]} {_PARENT}\n"
        return f"{args[-1].split('..')[-1]}\n"

    monkeypatch.setattr(ja, "_git", _git)
    orphan = "d" * 40
    assert ja.introduced(tmp_path, orphan) == [orphan]
    # Exactly four reads, in this order: the map, ONE rebuild-on-miss (a miss can mean the
    # snapshot is simply older than the commit), then the two-call `_introduced_uncached` body.
    assert len(calls) == 4
    assert calls[0] == ja._PARENT_MAP_ARGS
    assert calls[1] == ja._PARENT_MAP_ARGS
    assert calls[2] == ("rev-list", "--parents", "-n", "1", orphan)
    assert calls[3] == ("rev-list", f"{_PARENT}..{orphan}")


def test_a_map_that_is_not_ancestry_closed_defers_instead_of_over_reporting(
        monkeypatch, tmp_path):
    """A parent naming a commit the map does not carry means the map cannot be walked.

    `--all` should never produce that shape. It is pinned anyway because the failure it would
    cause is the dangerous direction: a truncated exclusion walk yields a TOO LARGE introduced
    set, and a too-large set reports a spine entry ANCHORED that is not -- a false clean on the
    ADR-85 hard leg.
    """
    truncated = f"300 {_SHA_A} {_PARENT} {_SHA_B}\n200 {_SHA_B} {_PARENT}\n"   # `_PARENT` absent
    seen = []

    def _git(repo, *args):
        seen.append(args)
        if args == ja._PARENT_MAP_ARGS:
            return truncated
        if args[:2] == ("rev-list", "--parents"):
            return f"{_SHA_A} {_PARENT}\n"
        return f"{_SHA_A}\n"

    monkeypatch.setattr(ja, "_git", _git)
    assert ja._introduced_from_map(tmp_path, _SHA_A) is None
    assert ja.introduced(tmp_path, _SHA_A) == [_SHA_A]        # git's answer, via the fallback


# --- real git: the batched map must not change the ANSWER ---------------------------------

def _multi_merge_repo(path):
    """root -> three `--no-ff` merges, one of them carrying two commits, plus a plain commit."""
    path.mkdir()
    _git(path, "init", "-q", "-b", "main")
    _git(path, "config", "user.email", "t@t")
    _git(path, "config", "user.name", "t")
    (path / "f.txt").write_text("root\n", encoding="utf-8")
    _git(path, "add", "f.txt")
    _git(path, "commit", "-q", "-m", "root")
    for n in (1, 2, 3):
        _git(path, "checkout", "-q", "-b", f"side{n}")
        for i in range(n):
            (path / "f.txt").write_text(f"{n}-{i}\n", encoding="utf-8")
            _git(path, "commit", "-q", "-am", f"side{n} commit {i}")
        _git(path, "checkout", "-q", "main")
        _git(path, "merge", "-q", "--no-ff", f"side{n}", "-m", f"merge side{n}")
    (path / "g.txt").write_text("direct\n", encoding="utf-8")
    _git(path, "add", "g.txt")
    _git(path, "commit", "-q", "-m", "a plain non-merge spine entry")
    return path


@requires_git
def test_the_batched_map_is_byte_identical_to_git_over_a_whole_spine(tmp_path):
    """The done-when, at unit scale: EVERY spine entry, list equality, order included.

    `_introduced_uncached` is the oracle because it IS git's answer -- the map is only ever an
    optimisation of it. Compared as LISTS and not as sets, deliberately: order is output.
    """
    repo = _multi_merge_repo(tmp_path / "r")
    spine = ja.spine_entries(repo, "main")
    assert len(spine) == 5                     # root + 3 merges + 1 plain commit
    for sha in spine:
        assert ja.introduced(repo, sha) == ja._introduced_uncached(repo, sha), sha
    # And the shapes are the ones the predicate depends on, stated rather than implied.
    merges = [s for s in spine if len(ja.introduced(repo, s)) > 1]
    assert sorted(len(ja.introduced(repo, s)) for s in merges) == [2, 3, 4]


@requires_git
def test_a_commit_made_after_the_map_was_built_is_still_answered_correctly(tmp_path):
    """THE staleness hazard, end to end in ONE process -- the [#533] question re-asked of a
    map instead of a split.

    A stale anchor answer is worse than a slow one: it produces false push-gate verdicts. Here
    the map is built, the repo then GROWS, and the new merge must be answered from a rebuilt
    map rather than from the snapshot that predates it. The test asserts the OUTCOME (git's
    answer) rather than the rebuild mechanism, so it survives a change of caching strategy.
    """
    repo = _multi_merge_repo(tmp_path / "r")
    ja.introduced(repo, ja.spine_entries(repo, "main")[0])       # builds the snapshot

    _git(repo, "checkout", "-q", "-b", "late")
    (repo / "h.txt").write_text("late\n", encoding="utf-8")
    _git(repo, "add", "h.txt")
    _git(repo, "commit", "-q", "-m", "late work")
    late_sha = ja.spine_entries(repo, "late")[0]
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "late", "-m", "merge late")
    merge_sha = ja.spine_entries(repo, "main")[0]

    got = ja.introduced(repo, merge_sha)
    assert got == ja._introduced_uncached(repo, merge_sha)
    assert got == [merge_sha, late_sha]
    # The point of the whole predicate: the merge is anchored by a JOURNAL naming what it
    # BROUGHT IN, never its own hash -- and that must survive the map having been rebuilt.
    assert ja.is_anchored(repo, merge_sha, f"### e\n\n**Anchors:** `{late_sha[:7]}`.\n") is True
    unrelated = ja.spine_entries(repo, "main")[2]
    assert ja.is_anchored(repo, merge_sha, f"### e\n\n**Anchors:** `{unrelated[:7]}`.\n") is False
