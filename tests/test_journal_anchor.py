"""Tests for `scripts/journal_anchor.py`'s entry-split memo ([#533] leg 2, STEP 2/3).

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


def _counting_git(calls):
    """A `_git` stand-in that records every invocation and answers the two rev-list forms."""
    def _git(repo, *args):
        calls.append((str(repo), args))
        if args[:2] == ("rev-list", "--parents"):
            return f"{args[-1]} {_PARENT}\n"
        if args[0] == "rev-list":
            return f"{args[-1].split('..')[-1]}\n{_SHA_B}\n"
        raise AssertionError(f"unexpected git call: {args}")
    return _git


def test_introduced_memoizes_a_full_sha_and_stops_spawning_git(monkeypatch, tmp_path):
    """The whole point: the second identical call must cost ZERO subprocesses.

    Asserted on the git-call log rather than on a hit counter alone, because the saving that
    matters here is process spawns (~144 ms each on this platform), not cache bookkeeping.
    """
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))

    first = ja.introduced(tmp_path, _SHA_A)
    assert len(calls) == 2                     # rev-list --parents, then rev-list range
    second = ja.introduced(tmp_path, _SHA_A)
    assert len(calls) == 2                     # unchanged: served from the memo
    assert first == second
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
    assert len(calls) == 4
    assert a != b


def test_distinct_repos_do_not_share_a_cache_entry(monkeypatch, tmp_path):
    """Two checkouts can hold the same SHA; keying on the sha alone would be a real bug."""
    calls = []
    monkeypatch.setattr(ja, "_git", _counting_git(calls))
    ja.introduced(tmp_path / "one", _SHA_A)
    ja.introduced(tmp_path / "two", _SHA_A)
    assert len(calls) == 4
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
    monkeypatch.setattr(ja, "_git", lambda repo, *args: f"{_SHA_A}\n")
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
