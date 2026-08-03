"""Tests for scripts/normalize_headers.py — dated-log entry header normalizer.

Rules (deterministic, idempotent):
  - Date-only entry headers (H2 or H3) -> `### YYYY-MM-DD`
  - Date + " — Topic" suffix -> `### YYYY-MM-DD — Topic` (preserved verbatim)
  - LESSONS pipe-schema entries (`### YYYY-MM-DD | source | ...`) -> unchanged
  - Non-date headings -> unchanged
"""
from __future__ import annotations

import os
import re
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


# An INDEPENDENT oracle for "this line is syntactically an ATX heading" — CommonMark's own
# rule (up to 3 leading spaces, 1-6 '#', then whitespace or end of line), written here rather
# than obtained from the module under test.
_ATX_RE = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
_DEMOTE_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2})", re.MULTILINE)

# Headings legally live inside containers, so a heading token's source line may carry
# blockquote markers or a list bullet before the `#`. The corpus refuted an oracle that
# ignored this (`> ### Night-batch work ...` in a 2026-07-30 audit). Stripping the container
# prefix keeps the oracle faithful WITHOUT making it permissive enough to hide a desync: a
# slid index lands on ordinary prose, which still fails the ATX test after stripping.
_CONTAINER_PREFIX_RE = re.compile(r"^(?:\s{0,3}(?:>|[-*+]|\d{1,9}[.)])\s*)*")


def _looks_like(rx: re.Pattern, line: str) -> bool:
    """`rx` matches the line either as-is or with one container prefix removed.

    Both forms are tried because the strip is necessarily approximate in the other direction:
    a setext underline `---` is itself indistinguishable from three bullet markers, so
    stripping unconditionally turns a valid underline into the empty string. Trying the raw
    line first keeps that case honest while still allowing `> ### Heading`.
    """
    return bool(rx.match(line) or rx.match(_CONTAINER_PREFIX_RE.sub("", line, count=1)))


@pytest.mark.live_repo
def test_corpus_every_rewritten_line_is_syntactically_a_heading() -> None:
    """The complement to the code-block test: every line that DID change is syntactically a
    heading. Together they bound the rewrite to exactly the documented surface.

    REBUILT after terra HIGH (2026-08-03) killed the first version on two counts, both of
    them this arc's own defect class:

      TAUTOLOGY  it asked `nh._heading_lines` whether a changed line was a heading — the exact
                 helper `normalize_text` used to decide to change it. It could never detect a
                 heading-map/splitter desync, which is the safety claim that matters for an
                 in-place rewriter. Now the oracle is `_ATX_RE`, CommonMark's syntax rule
                 restated here, independent of the module.
      VACUITY    the live corpus is already normalized, so `if got == src: continue` fired for
                 every file and the loop made ZERO assertions. Now each document is DEMOTED
                 first (`### YYYY-MM-DD` -> `## YYYY-MM-DD`, by pure line syntax — no fence
                 knowledge, so the demotion cannot smuggle in the assumption under test), which
                 forces the rewriter to fire on real in-document headings at real depths.
    """
    changed_files = changed_lines = 0
    for p in _corpus():
        src = p.read_text(encoding="utf-8", errors="replace")
        demoted = _DEMOTE_RE.sub(r"## \1", src)
        got = nh.normalize_text(demoted)
        before, after = nh._split_keep_eol(demoted), nh._split_keep_eol(got)
        assert len(before) == len(after), f"{p}: line count changed"
        touched = 0
        for i, (b, a) in enumerate(zip(before, after)):
            if b != a:
                touched += 1
                assert _ATX_RE.match(b[0]), (
                    f"{p}: line {i + 1} was rewritten but is not syntactically a heading: "
                    f"{b[0][:60]!r} — heading map and line splitter have desynced")
        changed_lines += touched
        changed_files += bool(touched)

    assert changed_files > 20, (
        f"only {changed_files} corpus files were rewritten — the demotion did not force enough "
        "work for this to prove anything")
    assert changed_lines > 50, f"only {changed_lines} lines exercised — proof too thin"


@pytest.mark.live_repo
def test_corpus_heading_map_indices_land_on_heading_syntax() -> None:
    """DIRECT desync detector, and the one assertion that does not trust either side alone.

    For every document in the corpus, every heading span markdown_it reports must line up with
    heading SYNTAX in the lines `_split_keep_eol` produces — judged by `_ATX_RE` and the setext
    underline rule written here, not by asking the module. If the splitter and the parser ever
    disagree about what line N is (the failure mode a mixed-EOL or exotic-line-boundary
    document would cause) the indices slide and this fails, without either component being
    asked to grade its own work.

    The setext branch is not hypothetical padding. markdown_it runs plain CommonMark with no
    frontmatter plugin, so a `---` / `key: value` / `---` YAML block parses as a SETEXT
    heading: `.claude/agents/artifact-reader.md` reports a heading whose span starts at
    `name: artifact-reader`. The underline is the LAST line of the span (`map[1] - 1`), not
    the line after the first — an earlier version of this test assumed the latter and was
    correctly refuted by the corpus. Harmless for the rewriter (frontmatter lines cannot match
    `^(##|###)\\s+DATE`), but it must be modelled correctly here or the oracle is wrong.
    """
    underline = re.compile(r"^ {0,3}(=+|-+)\s*$")
    checked = 0
    for p in _corpus():
        src = p.read_text(encoding="utf-8", errors="replace")
        pieces = nh._split_keep_eol(src)
        assert "".join(b + e for b, e in pieces) == src, f"{p}: split is lossy"
        lines = [b for b, _e in pieces]
        for t in nh._MD.parse(src):
            if t.type != "heading_open" or not t.map:
                continue
            start, end = t.map
            assert start < len(lines), f"{p}: heading start {start} past end ({len(lines)})"
            if t.markup.startswith("#"):
                assert _looks_like(_ATX_RE, lines[start]), (
                    f"{p}: ATX heading at line {start + 1} is not heading syntax: "
                    f"{lines[start][:60]!r} — splitter and parser have desynced")
            else:
                assert _looks_like(underline, lines[end - 1]), (
                    f"{p}: setext heading span {t.map} does not end on an underline: "
                    f"{lines[end - 1][:60]!r} — splitter and parser have desynced")
            checked += 1
    assert checked > 500, f"only {checked} heading spans checked — proof too thin"


def test_mixed_and_exotic_line_boundaries_do_not_desync_the_heading_map() -> None:
    """The desync case with a HAND-COMPUTED expectation, not a derived one.

    `\\x0b`, `\\x0c`, `\\u2028` and `\\u2029` are line boundaries to `str.splitlines` but NOT to
    CommonMark. Splitting on them would shift every subsequent index by one and the rewriter
    would edit the wrong line — silently, in place. `_split_keep_eol` matches markdown_it's own
    `\\r\\n | \\r | \\n` rule exactly, so they stay inside their line.
    """
    src = (
        "## 2026-01-01\r\n"            # line 0  CRLF   -> must normalize
        "para with   inside\r"    # line 1  CR      (u2028 must NOT split)
        "## 2026-02-02\n"              # line 2  LF     -> must normalize
        "text \x0b and \x0c here\n"    # line 3          (must NOT split)
        "```\n"                        # line 4
        "## 2026-03-03\n"              # line 5  in code -> must NOT change
        "```"                          # line 6  no trailing EOL
    )
    assert len(nh._split_keep_eol(src)) == 7, nh._split_keep_eol(src)
    assert "".join(b + e for b, e in nh._split_keep_eol(src)) == src

    got = nh.normalize_text(src)
    assert got == src.replace("## 2026-01-01", "### 2026-01-01").replace(
        "## 2026-02-02", "### 2026-02-02")
    assert "## 2026-03-03" in got, "the fenced heading was rewritten"


def test_parse_failure_is_non_destructive_AND_announced(capsys, monkeypatch) -> None:
    """terra CRITICAL (2026-08-03): the fail-safe returned the text unchanged with NO
    diagnostic, so a dependency or API failure would make this rewriting hook quietly no-op
    while still exiting 0 — indistinguishable from "nothing to normalize". Non-destruction is
    right; silence is not. Exit code stays 0: the documented contract is that an auto-format
    hook never fails-and-asks."""
    def _boom(_text):
        raise RuntimeError("simulated parser failure")

    monkeypatch.setattr(nh, "_heading_lines", _boom)
    src = "## 2026-05-16\n"
    assert nh.normalize_text(src) == src, "a parse failure must not rewrite"
    err = capsys.readouterr().err
    assert "PARSE FAILED" in err and "UNCHANGED" in err, err
    assert "simulated parser failure" in err, err


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
