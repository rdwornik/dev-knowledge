#!/usr/bin/env python
"""backlog_source.py — the ONE reader for the backlog's FULL-BODY canonical text.

WHY THIS MODULE EXISTS ([#589]). Before this arc the committed `BACKLOG.md` WAS the
full-body text: every row rendered its whole line, so "read BACKLOG.md" and "read the
rows" were the same act, and a dozen gates did exactly that. [#589] turned the committed
file into a ONE-LINE-PER-ROW **projection** (`gen_task_tree.render_view`) to cut the boot
read from ~280 KB to ~66 KB. The bodies did not move -- they were already in `tasks/`,
the ADR-107 source of truth -- but the surface that USED to carry them stopped.

That split has exactly one dangerous failure mode, and it is silent: a gate that greps a
row body for `· routine:` / `· kill-candidates:` / `Done when:` against the projection
finds NOTHING and reports a clean PASS. It measures an empty set and calls it green. Four
live checks were in that position (`routine_consumers`, `preflight_backlog_ids`,
`validate_backlog`, `validate_doc_rot`'s two BACKLOG arms), so the fix is single-sourced
here rather than repeated -- one reader, one fallback rule, one place to be wrong.

THE RULE: if `tasks/manifest.json` is present, the canonical text is what the tree
reassembles (`gen_task_tree.reassemble_from_tree` -- byte-for-byte what `BACKLOG.md` used
to hold); otherwise it is `BACKLOG.md` itself, read as-is.

THE FALLBACK IS NOT DEFENSIVE PADDING -- it is the CONSUMER-REPO case, and it is the whole
reason this is a function and not a constant. A child repo carries a hand-authored
`BACKLOG.md` with full bodies and NO `tasks/` tree (that is what `probe_child_backlogs.py`
measures and what the plugin floor twin validates). `routine_consumers` and the doc-rot
scanner both run per-repo across the fleet, so on a consumer they must keep reading the
file. Hub and consumer reach the same text by different routes; neither branch is a
degraded mode of the other.

STATED LIMIT: line numbers. A caller that reports "line N" now numbers the CANONICAL text,
not the committed projection, on any repo with a `tasks/` tree. The two agreed before
[#589] and no longer do. Callers that surface a locus say so; the durable locus is the
`[#id]`, which is stable across both.

Layer-2 / read-only (ADR-28/36): reads only, writes nothing, drives no state anywhere.
Loose top-level module BY DESIGN (mirrors gen_audit_index.py): no codemap node.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


def _gen_task_tree():
    """Import gen_task_tree the way every other sibling in scripts/ does.

    Deferred to call time and tolerant of both import shapes (`scripts.gen_task_tree` when
    the repo root is on the path, bare when `scripts/` itself is) because the callers are
    split across both: `audit.py` imports package-relative, the pre-commit entries run the
    module as a script. A hard top-level import would work for one and not the other.
    """
    try:
        from scripts import gen_task_tree as gtt  # noqa: PLC0415
    except ImportError:
        if str(_SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(_SCRIPTS_DIR))
        import gen_task_tree as gtt  # noqa: PLC0415
    return gtt


def has_task_tree(repo_root: Path | None = None) -> bool:
    """True when `repo_root` carries a `tasks/manifest.json` source tree."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    return (root / "tasks" / "manifest.json").is_file()


def canonical_text(repo_root: Path | None = None) -> Optional[str]:
    """The FULL-BODY backlog text for `repo_root`, or None when there is none.

    Returns the `tasks/` reassembly on a repo with a source tree, else the raw
    `BACKLOG.md`, else None (no backlog at all -- callers render that as NOT-APPLICABLE,
    never as an empty-and-therefore-clean scan).

    RAISES NOTHING IT CAN HELP: a malformed manifest / unreadable task file propagates the
    underlying OSError/ValueError, deliberately. A reassembly that cannot be computed is a
    LOUD failure at the caller, not a silent fall-through to the projection -- falling back
    to `BACKLOG.md` here would hand a body-reading gate the very one-line view this module
    exists to keep it away from, and it would pass.

    THE CONSUMER FALLBACK DECODES STRICTLY, and that is the same rule stated once more
    rather than an inconsistency (terra HIGH, 2026-08-26). The first version passed
    `errors="replace"`, which silently substitutes U+FFFD for undecodable bytes: a corrupted
    `BACKLOG.md` would come back as text with body markers erased or altered, every
    body-reading gate would scan the damaged text, find nothing, and report CLEAN. The
    reassembly path already decodes strictly (`read_bytes().decode("utf-8")`), and
    `routine_consumers` already declares a `UnicodeDecodeError` -> FAIL arm that a lenient
    decode here made unreachable. A source that cannot be decoded is unreadable, which is a
    failed computation of an available ground truth -- the callers' job to report, not this
    module's to paper over.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    if has_task_tree(root):
        return _gen_task_tree().reassemble_from_tree(root / "tasks")
    backlog = root / "BACKLOG.md"
    if backlog.is_file():
        # Strict decode, then normalize line endings. The normalization is not cosmetic and
        # not new behaviour: `Path.read_text` (what this replaced) applies universal newlines,
        # so a consumer repo whose `BACKLOG.md` is checked out CRLF has always reached these
        # scanners as LF. Decoding strictly WITHOUT normalizing would have fixed the leniency
        # defect and introduced a CRLF one in the same line — `parse_backlog` refuses CRLF
        # outright, so a Windows consumer checkout would have started failing where it used to
        # pass. The reassembly branch above needs none of this: `tasks/` is pure LF by contract.
        # BOTH line-ending forms, CRLF then any REMAINING lone CR (terra HIGH, round 2). The
        # first version normalized only `\r\n`, which is a narrower rule than the `read_text`
        # it replaced: universal newlines also translates a bare `\r`, so an old-Mac-style
        # consumer backlog would have reached `parse_backlog` with CRs and been REFUSED where
        # it used to be processed. Order matters — collapsing CRLF first means the second pass
        # only ever sees CRs that were genuinely alone.
        return backlog.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return None


def canonical_source_label(repo_root: Path | None = None) -> str:
    """Human name of where `canonical_text` read from -- for evidence lines."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    return "tasks/ (reassembled)" if has_task_tree(root) else "BACKLOG.md"
