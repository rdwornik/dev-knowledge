"""Coverage for scripts/backlog_source.py — the ONE reader for the full-body backlog text.

[#589] split the backlog into a committed one-line VIEW and a `tasks/` SOURCE. This module is
what keeps every body-reading gate on the second, and its fallback rule is what keeps the
per-repo fleet scan working on a consumer that has no tree. Both are load-bearing enough that
getting them wrong reports a clean PASS rather than an error — hence these tests.
"""
from __future__ import annotations

from pathlib import Path

import pytest


import audit as aud  # noqa: E402
import backlog_source as bs  # noqa: E402


def test_module_is_importable_and_repo_pinned():
    assert bs.canonical_text() is not None
    assert bs.has_task_tree() is True
    assert bs.canonical_source_label() == "tasks/ (reassembled)"


def test_the_hub_canonical_text_is_the_tree_reassembly():
    """Not the committed file: on the hub those are now different artifacts."""
    root = Path(bs._REPO_ROOT)
    assert bs.canonical_text(root) != (root / "BACKLOG.md").read_text(encoding="utf-8")
    assert "Done when:" in bs.canonical_text(root)


# --- [#589] terra round 1: the consumer fallback decodes STRICTLY -----------

def test_the_consumer_fallback_raises_on_undecodable_bytes(tmp_path):
    """terra HIGH — `errors="replace"` would substitute U+FFFD for corrupt bytes, so a
    body-reading gate would scan damaged text, find no markers, and report CLEAN. A source
    that cannot be decoded is unreadable; saying so is the caller's job, not this module's to
    paper over."""
    (tmp_path / "BACKLOG.md").write_bytes(b"# B\n- [#1] \xff\xfe not utf-8\n")
    with pytest.raises(UnicodeDecodeError):
        bs.canonical_text(tmp_path)


def test_routine_consumers_fails_rather_than_passes_on_undecodable_source(tmp_path):
    """...and the FAIL arm that leniency had made unreachable is live again."""
    (tmp_path / "BACKLOG.md").write_bytes(b"# B\n- [#1] \xff\xfe not utf-8\n")
    findings = aud.check_routine_consumers(tmp_path)
    assert findings[0].status == "fail", findings[0].evidence
    assert "cannot read the backlog source" in findings[0].evidence


def test_canonical_text_prefers_the_tree_and_falls_back_to_the_file(tmp_path):
    """The fallback rule itself, both branches, since every re-pointed gate rests on it."""
    assert bs.canonical_text(tmp_path) is None
    (tmp_path / "BACKLOG.md").write_bytes(b"# B\n")
    assert bs.canonical_text(tmp_path) == "# B\n"
    assert bs.canonical_source_label(tmp_path) == "BACKLOG.md"


def test_a_crlf_consumer_backlog_is_normalized_not_refused(tmp_path):
    """Strict decode must not smuggle in a CRLF regression.

    `Path.read_text` (what the strict decode replaced) applies universal newlines, so a
    Windows consumer checkout has always reached these scanners as LF — and `parse_backlog`
    REFUSES CRLF outright, so dropping the normalization would have turned a passing consumer
    repo into a failing one in the same line that fixed the leniency defect.
    """
    (tmp_path / "BACKLOG.md").write_bytes(b"# B\r\n- [#1] [P1][S] x\r\n")
    text = bs.canonical_text(tmp_path)
    assert "\r" not in text
    assert text == "# B\n- [#1] [P1][S] x\n"


def test_a_bare_cr_consumer_backlog_is_normalized_too(tmp_path):
    """terra HIGH, round 2 — `read_text`'s universal newlines translate a LONE `\r` as well as
    CRLF, so normalizing only CRLF was a narrower rule than the one it replaced: an
    old-Mac-style consumer backlog would have reached `parse_backlog` with CRs and been
    REFUSED where it used to be processed."""
    (tmp_path / "BACKLOG.md").write_bytes(b"# B\r- [#1] [P1][S] x\r")
    text = bs.canonical_text(tmp_path)
    assert "\r" not in text
    assert text == "# B\n- [#1] [P1][S] x\n"
