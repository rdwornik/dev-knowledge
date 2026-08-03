"""normalize_headers.py — dated-log entry header normalizer.

Deterministic, idempotent rewriter for dated-log entry headers in LESSONS.md
and JOURNAL.md (and any markdown file with ISO-date headings). Wired as an
auto-format pre-commit hook: it rewrites; it never fails-and-asks.

Rules:
  - `## YYYY-MM-DD`              -> `### YYYY-MM-DD`
  - `## YYYY-MM-DD — Topic`      -> `### YYYY-MM-DD — Topic`  (separator + topic preserved verbatim)
  - `### YYYY-MM-DD`             -> unchanged
  - `### YYYY-MM-DD — Topic`     -> unchanged
  - `### YYYY-MM-DD | a | b ...` -> unchanged   (LESSONS 6-field pipe schema)
  - `## YYYY-MM-DD | a | b ...`  -> unchanged   (non-canonical pipe form left alone)
  - Non-date headings, prose, bullets, fenced code blocks -> unchanged

Usage:
    python scripts/normalize_headers.py LESSONS.md JOURNAL.md
    python scripts/normalize_headers.py --check LESSONS.md   # exit 0 always; rewrites in place
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

_DATE = r"\d{4}-\d{2}-\d{2}"

_DATE_ONLY = re.compile(rf"^(##|###)\s+({_DATE})\s*$")
_DATE_WITH_PIPE = re.compile(rf"^(##|###)\s+({_DATE})\s*\|")
_DATE_WITH_SEP = re.compile(rf"^(##|###)\s+({_DATE})(\s+[—–\-]\s+.+)$")

# Line splitter matching markdown_it's OWN newline normalization (`\r\n | \r | \n`) exactly,
# so our line indices and its token `map` indices cannot desync. `str.splitlines` must NOT be
# used here: it also breaks on \x0b \x0c    , which CommonMark does not treat as line
# boundaries, and one such character anywhere in the file would shift every index after it.
_EOL_RE = re.compile(r"\r\n|\r|\n")

_MD = MarkdownIt("commonmark")


def _split_keep_eol(text: str) -> list[tuple[str, str]]:
    """[(line_body, line_ending), ...] — lossless: ``"".join(b + e ...) == text``."""
    out: list[tuple[str, str]] = []
    pos = 0
    for m in _EOL_RE.finditer(text):
        out.append((text[pos:m.start()], m.group(0)))
        pos = m.end()
    if pos < len(text) or not out:
        out.append((text[pos:], ""))
    return out


def _heading_lines(text: str) -> set[int]:
    """0-based source lines that CommonMark says are headings.

    POSITIVE IDENTIFICATION, not a blocklist of protected regions — this is the whole fix.
    The former `^``` ` toggle tried to enumerate where NOT to rewrite and missed every fence
    shape but one: `~~~` fences (the named defect), tilde fences of any length, fences
    indented up to the 3 spaces CommonMark allows, and a 4-backtick fence closed early by the
    3-backtick line it legally contains. Each miss let a REWRITING, DEPLOYED hook edit content
    inside a code block, against its own docstring.

    Asking markdown_it which lines are headings inverts that: a line is rewritten only when
    the parser affirms it is a heading, so code blocks, indented code and HTML blocks are all
    excluded by construction rather than by a pattern someone remembered to add.
    """
    return {t.map[0] for t in _MD.parse(text) if t.type == "heading_open" and t.map}


def normalize_line(line: str) -> str:
    """Rewrite a single line per the rules. Lines outside fenced blocks only."""
    # LESSONS pipe schema — leave alone regardless of header level
    if _DATE_WITH_PIPE.match(line):
        return line
    m_only = _DATE_ONLY.match(line)
    if m_only:
        return f"### {m_only.group(2)}"
    m_sep = _DATE_WITH_SEP.match(line)
    if m_sep:
        # Preserve separator + topic verbatim; only the heading level changes
        return f"### {m_sep.group(2)}{m_sep.group(3)}"
    return line


def normalize_text(text: str) -> str:
    """Normalize all dated-log entry headers in a markdown document.

    A line is rewritten only where CommonMark says it is a heading AND the rules in
    ``normalize_line`` match it. Everything else — code blocks fenced with any shape,
    indented code, HTML blocks, prose — is passed through verbatim.

    FAIL-SAFE, AND LOUD: if the parse raises, the document is returned UNCHANGED **and the
    failure is announced on stderr**. This hook rewrites files in place, so an unknown
    document structure must produce no edit rather than an edit made on a guess — but a
    silent no-op is its own defect (terra CRITICAL, 2026-08-03): a dependency or API failure
    would make the formatter quietly stop working while still reporting success, and nothing
    would distinguish "nothing to normalize" from "I could not look". The exit code stays 0
    because this is an auto-format hook whose documented contract is that it never
    fails-and-asks; visibility is the fix, not a new block.
    """
    try:
        headings = _heading_lines(text)
    except Exception as exc:  # noqa: BLE001 — a rewriter that cannot parse must not rewrite
        print(f"normalize_headers: PARSE FAILED ({exc!r}) — document left UNCHANGED. "
              "No headers were normalized in this file; this is a no-op, not a clean pass.",
              file=sys.stderr)
        return text
    out: list[str] = []
    for i, (body, eol) in enumerate(_split_keep_eol(text)):
        out.append((normalize_line(body) if i in headings else body) + eol)
    return "".join(out)


def normalize_file(path: Path) -> bool:
    """Normalize one file in place. Returns True iff content changed."""
    original = path.read_text(encoding="utf-8")
    rewritten = normalize_text(original)
    if rewritten == original:
        return False
    path.write_text(rewritten, encoding="utf-8", newline="\n")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        sys.stderr.write("usage: normalize_headers.py FILE [FILE ...]\n")
        return 0  # auto-format hooks should not fail
    for arg in argv:
        p = Path(arg)
        if not p.exists() or p.is_dir():
            continue
        normalize_file(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
