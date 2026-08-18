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
    assert len(first) == 3


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
    assert len(before) == 3
    assert not any("appended after the first read" in e for e in before)

    with open(tmp_path / "JOURNAL.md", "a", encoding="utf-8", newline="\n") as fh:
        fh.write(_NEW_ENTRY)

    after = ja._entries(ja.journal_text(tmp_path))
    assert len(after) == 4
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
    assert len(ja._entries(_FIXTURE)) == 3
    assert len(ja._entries(grown)) == 4


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
