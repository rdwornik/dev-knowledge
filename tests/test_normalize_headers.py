"""Tests for scripts/normalize_headers.py — dated-log entry header normalizer.

Rules (deterministic, idempotent):
  - Date-only entry headers (H2 or H3) -> `### YYYY-MM-DD`
  - Date + " — Topic" suffix -> `### YYYY-MM-DD — Topic` (preserved verbatim)
  - LESSONS pipe-schema entries (`### YYYY-MM-DD | source | ...`) -> unchanged
  - Non-date headings -> unchanged
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import normalize_headers as nh


# ---------------------------------------------------------------------------
# Single-line normalization
# ---------------------------------------------------------------------------

def test_h2_date_only_becomes_h3() -> None:
    assert nh.normalize_line("## 2026-05-16") == "### 2026-05-16"


def test_h3_date_only_unchanged() -> None:
    assert nh.normalize_line("### 2026-05-16") == "### 2026-05-16"


def test_h2_date_with_topic_becomes_h3_preserved() -> None:
    assert (
        nh.normalize_line("## 2026-05-16 — Session D: cleanup")
        == "### 2026-05-16 — Session D: cleanup"
    )


def test_h3_date_with_topic_unchanged() -> None:
    line = "### 2026-05-16 — Session D: cleanup"
    assert nh.normalize_line(line) == line


def test_h3_date_with_hyphen_topic_preserved() -> None:
    assert (
        nh.normalize_line("## 2026-05-16 - hyphen topic")
        == "### 2026-05-16 - hyphen topic"
    )


def test_lessons_pipe_schema_unchanged() -> None:
    line = "### 2026-05-16 | source | the lesson | category | [scope: meta] | action"
    assert nh.normalize_line(line) == line


def test_h2_with_pipe_schema_left_alone() -> None:
    """An H2 that already carries pipe payload is a non-canonical edge case — preserve."""
    line = "## 2026-05-16 | source | lesson | category | [scope: meta] | action"
    assert nh.normalize_line(line) == line


def test_non_date_h2_unchanged() -> None:
    assert nh.normalize_line("## Some Section Heading") == "## Some Section Heading"


def test_non_date_h3_unchanged() -> None:
    assert nh.normalize_line("### Topic with no date") == "### Topic with no date"


def test_h1_unchanged() -> None:
    assert nh.normalize_line("# Lessons Learned") == "# Lessons Learned"


def test_bullet_or_text_unchanged() -> None:
    assert nh.normalize_line("- 2026-05-16 in a bullet") == "- 2026-05-16 in a bullet"
    assert nh.normalize_line("Plain prose 2026-05-16.") == "Plain prose 2026-05-16."


# ---------------------------------------------------------------------------
# Whole-file normalization + idempotency
# ---------------------------------------------------------------------------

MESSY = """# Title

<!-- scope: meta -->

## 2026-05-16
body a

## 2026-05-15 — Topic with em-dash
body b

### 2026-05-14 - hyphen topic
body c

### 2026-05-13 | source | lesson | category | [scope: meta] | action
body d

## Some Non-Date Section
body e
"""

CLEAN = """# Title

<!-- scope: meta -->

### 2026-05-16
body a

### 2026-05-15 — Topic with em-dash
body b

### 2026-05-14 - hyphen topic
body c

### 2026-05-13 | source | lesson | category | [scope: meta] | action
body d

## Some Non-Date Section
body e
"""


def test_known_messy_to_known_clean() -> None:
    assert nh.normalize_text(MESSY) == CLEAN


def test_idempotency_single_pass() -> None:
    """Already-clean input passes through unchanged."""
    assert nh.normalize_text(CLEAN) == CLEAN


def test_idempotency_double_pass() -> None:
    """Running twice produces the same result as running once."""
    once = nh.normalize_text(MESSY)
    twice = nh.normalize_text(once)
    assert once == twice


def test_does_not_touch_fenced_code_blocks() -> None:
    """A '## YYYY-MM-DD' line inside a fenced code block must NOT be rewritten."""
    src = (
        "# Title\n\n"
        "```\n"
        "## 2026-05-16\n"
        "```\n"
    )
    assert nh.normalize_text(src) == src


# ---------------------------------------------------------------------------
# File-level helper (writes only if changed)
# ---------------------------------------------------------------------------

def test_normalize_file_rewrites_messy(tmp_path: Path) -> None:
    p = tmp_path / "JOURNAL.md"
    p.write_text(MESSY, encoding="utf-8")
    changed = nh.normalize_file(p)
    assert changed is True
    assert p.read_text(encoding="utf-8") == CLEAN


def test_normalize_file_noop_on_clean(tmp_path: Path) -> None:
    p = tmp_path / "JOURNAL.md"
    p.write_text(CLEAN, encoding="utf-8")
    mtime_before = p.stat().st_mtime_ns
    changed = nh.normalize_file(p)
    assert changed is False
    # Content unchanged; mtime unchanged (file not rewritten when no diff)
    assert p.read_text(encoding="utf-8") == CLEAN
    assert p.stat().st_mtime_ns == mtime_before


# ---------------------------------------------------------------------------
# Fence recognition — the docstring promises "fenced code blocks -> unchanged".
# The hand-rolled `^``` ` toggle kept that promise for exactly ONE fence shape.
# This hook is DEPLOYED and it REWRITES, so a false negative here corrupts content.
# ---------------------------------------------------------------------------

_DATED = "## 2026-05-16\n"

FENCE_SHAPES = {
    "tilde": f"~~~\n{_DATED}~~~\n",
    "tilde_with_info": f"~~~text\n{_DATED}~~~\n",
    "tilde_four": f"~~~~text\n{_DATED}~~~~\n",
    "backtick_indented": f"   ```\n{_DATED}   ```\n",
    "backtick_four_wrapping_three": f"````\n```\n{_DATED}```\n````\n",
}


@pytest.mark.parametrize("shape", sorted(FENCE_SHAPES))
def test_dated_heading_inside_any_fence_shape_is_untouched(shape: str) -> None:
    """Failing-test shape, not a baseline pin: the module docstring already PROMISES
    "fenced code blocks -> unchanged", so the correct answer is documented and the test
    asserts it rather than freezing the broken behaviour.

    `~~~` is the named defect; the other shapes are the same class the `^``` ` toggle also
    missed — an indented fence (CommonMark allows up to 3 spaces) is never recognised as a
    fence at all, and a 4-backtick fence is closed early by the 3-backtick line it legally
    contains, so content after it is treated as prose and rewritten.
    """
    src = f"# Title\n\n{FENCE_SHAPES[shape]}"
    assert nh.normalize_text(src) == src


def test_headings_outside_fences_are_still_normalized_around_a_tilde_fence() -> None:
    """The other half of the contract: protecting fences must not stop the rewriter working.
    A fix that simply refused to normalize anything would pass the test above."""
    src = f"## 2026-01-01\n\n~~~\n{_DATED}~~~\n\n## 2026-02-02 — Topic\n"
    got = nh.normalize_text(src)
    assert got == f"### 2026-01-01\n\n~~~\n{_DATED}~~~\n\n### 2026-02-02 — Topic\n"


# ---------------------------------------------------------------------------
# Byte-level non-destruction over the live corpus (P1: this hook rewrites in place).
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKIP_PARTS = {".venv", ".git", "node_modules", "__pycache__", ".pytest_cache"}


def _corpus() -> list[Path]:
    return [p for p in sorted(_REPO_ROOT.rglob("*.md"))
            if not _SKIP_PARTS.intersection(p.parts)]


def _code_spans(text: str) -> list[tuple[int, int]]:
    """[start, end) line spans markdown_it classifies as code — derived from the parser,
    never a hand-written fence list, so the assertion covers whatever CommonMark covers."""
    return [tuple(t.map) for t in nh._MD.parse(text)
            if t.type in ("fence", "code_block") and t.map]


@pytest.mark.live_repo
def test_corpus_no_code_block_line_is_ever_modified() -> None:
    """BYTE-LEVEL non-destruction across every markdown file in the repo: for each file,
    every line inside a code region is byte-identical before and after normalization.

    This is the assertion the old implementation could not have passed, and the reason the
    fix needed proving rather than asserting: the hook is wired as an auto-format pre-commit
    hook, so a false negative silently edits committed content.
    """
    files = _corpus()
    assert len(files) > 100, f"corpus implausibly small ({len(files)}) — glob is wrong"

    checked_spans = 0
    for p in files:
        src = p.read_text(encoding="utf-8", errors="replace")
        got = nh.normalize_text(src)
        before = nh._split_keep_eol(src)
        after = nh._split_keep_eol(got)
        assert len(before) == len(after), f"{p}: line count changed"
        for start, end in _code_spans(src):
            checked_spans += 1
            for i in range(start, min(end, len(before))):
                assert before[i] == after[i], f"{p}: line {i + 1} inside a code block was rewritten"
    assert checked_spans > 50, f"only {checked_spans} code spans seen — corpus proves too little"


@pytest.mark.live_repo
def test_corpus_only_commonmark_headings_are_ever_modified() -> None:
    """The complement: every line that DID change is one CommonMark calls a heading. Together
    with the test above this bounds the rewrite to exactly the documented surface."""
    for p in _corpus():
        src = p.read_text(encoding="utf-8", errors="replace")
        got = nh.normalize_text(src)
        if got == src:
            continue
        headings = nh._heading_lines(src)
        before, after = nh._split_keep_eol(src), nh._split_keep_eol(got)
        for i, (b, a) in enumerate(zip(before, after)):
            if b != a:
                assert i in headings, f"{p}: line {i + 1} changed but is not a heading"


@pytest.mark.live_repo
def test_corpus_rewriter_still_fires_on_real_documents() -> None:
    """Non-destruction must not be achieved by refusing to work. Inject a messy dated heading
    into every real document and require it to normalize.

    The probe goes at LINE 0, and that position is load-bearing: a column-0 ATX heading on
    the first line of a document cannot be inside any container, so "this must normalize" is
    guaranteed structurally rather than by a guess about the file's contents. The first
    attempt appended at the END with a `src.count("```") % 2` balance guard, and the corpus
    refuted it — templates/archive/HANDOFF_QUESTION_TEMPLATE.md carries an UNTERMINATED fence
    (opened at line 442, never closed), which `count()` misses because it also counts inline
    and info-string backticks. The parser was right and the heuristic was wrong; the fix was
    to stop guessing, not to special-case the file.

    Guards the failure mode where "prove it changes nothing" quietly becomes "it does nothing".
    """
    fired = 0
    for p in _corpus():
        src = p.read_text(encoding="utf-8", errors="replace")
        probe = "## 2026-05-16 — probe\n\n" + src
        got = nh.normalize_text(probe)
        assert got.startswith("### 2026-05-16 — probe\n"), f"{p}: rewriter did not fire"
        fired += 1
    assert fired > 100, f"only {fired} documents exercised — proof too thin"
