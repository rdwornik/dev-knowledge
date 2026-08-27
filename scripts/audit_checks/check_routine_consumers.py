"""`check_routine_consumers` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with the ten `_ROUTINE_*` constants and the three helpers
(`_routine_code_spans`, `_routine_in_code`, `_routine_value_is_named`) it exclusively owns.
No logic, naming, formatting or docstring change; `audit.py` re-exports every name.
"""

from __future__ import annotations

import re
from pathlib import Path

from ._common import _na, Finding


# ADR-105 routine marker. Clause-scoped extraction in the established
# _SERIALIZE_CLAUSE_RE idiom (validate_backlog.py:81) — delimiter-anchored, so a prose
# mention of the keyword in a task body cannot register as a phantom declaration.
_ROUTINE_MARKER_RE = re.compile("·\\s*routine\\s*:")
_ROUTINE_FIELD_RE = re.compile("·\\s*(consumer|consumption_path)\\s*=([^·]*)")
_ROUTINE_TASK_RE = re.compile(r"^- \[#(\d+)\]")
_ROUTINE_REQUIRED = ("consumer", "consumption_path")
# A LOOKALIKE delimiter before `routine:` (bullet/interpunct variants that are NOT the
# canonical U+00B7). Without this a mistyped marker parses as "no declaration" and fails
# OPEN -- the exact silent-inertness class [#424]/[#425] were filed for, so this check
# refuses to reproduce it. A bare prose "routine:" with no bullet is NOT a lookalike.
_ROUTINE_LOOKALIKE_RE = re.compile("[•∙‧⋅]\\s*routine\\s*:")
# Declaration CONTEXT — a lookalike is only a mistyped marker if the row also carries a
# `field=` clause. Without this, prose comparing bullet-listed terms false-FAILs.
_ROUTINE_ANYFIELD_RE = re.compile(r"\b(consumer|consumption_path|trigger|scope)\s*=")
_ROUTINE_FENCE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})")
_ROUTINE_TICK_RUN_RE = re.compile(r"`+")
_ROUTINE_INVISIBLE = str.maketrans({c: None for c in "​‌‍﻿⁠"})
# Values that carry word characters but name nothing.
_ROUTINE_SENTINELS = frozenset({"tbd", "todo", "tba", "n/a", "na", "none", "xxx", "?"})


def _routine_code_spans(line: str) -> list[tuple[int, int]]:
    """Inline-code spans as [start, end) — a backtick run opens, an EQUAL-length run closes.

    Length-matched per CommonMark, so a double-backtick span ``· routine:`` is ONE span
    rather than two single-tick spans that would leave the marker exposed. Deleting spans
    outright was the earlier bug: it erased legitimate backticked VALUES
    (`consumer=`ops-bot``), so spans are located and consulted, never removed.
    """
    runs = [(m.start(), m.end()) for m in _ROUTINE_TICK_RUN_RE.finditer(line)]
    spans: list[tuple[int, int]] = []
    i = 0
    while i < len(runs):
        start, start_end = runs[i]
        width = start_end - start
        for j in range(i + 1, len(runs)):
            close, close_end = runs[j]
            if close_end - close == width:
                spans.append((start, close_end))
                i = j
                break
        i += 1
    return spans


def _routine_in_code(idx: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= idx < b for a, b in spans)


def _routine_value_is_named(raw: str) -> bool:
    """True only for a value that actually NAMES something.

    Rejects blank, invisible-only, punctuation-only, sentinel (`TBD`/`TODO`/`N/A`), and
    unfilled `<template placeholders>`. A placeholder is angle-wrapped AND contains a
    space (ADR-105's template reads `consumer=<who reads it>`); an angle-wrapped autolink
    (`<https://…>`, `<mailto:…>`) has no space and is a legitimate consumption path, so
    it passes. Backticks around a value are formatting, not content.
    """
    v = raw.translate(_ROUTINE_INVISIBLE).strip().strip("`").strip()
    if not v:
        return False
    if v.startswith("<") and v.endswith(">") and " " in v:
        return False
    if v.lower() in _ROUTINE_SENTINELS:
        return False
    return any(ch.isalnum() for ch in v)


def check_routine_consumers(repo_path: Path) -> list[Finding]:
    """[#419]/ADR-105 — a declared routine must name a `consumer` and a `consumption_path`.

    COVERAGE BOUNDARY — read before reading a green result: this checks ONLY BACKLOG
    rows carrying an ADR-105 `· routine:` marker, which at acceptance is exactly ONE row
    ([#348]). The ~30 live routines — session hooks, commit-time gates, scheduled jobs —
    are not BACKLOG rows, carry no marker, and are NOT checked; a pass here says nothing
    whatever about them (retrofit: [#426]). Green does NOT mean the fleet's routines have
    consumers.

    ADR-105 gates at ACTIVATION, not at filing: a row that merely *proposes* a routine
    carries no marker and is correctly not checked. ADR-105 declares six fields; this
    gates the two that make output reach a decision — the other four
    (trigger/scope/verified_by/review_date) are declared, not gated. A marker whose
    `consumer` or `consumption_path` is missing, blank, placeholder, or duplicated is a
    FAIL: an unconsumed routine is the defect [#419] names, and a routine that cannot
    name a consumer is retired rather than activated (that decision is the operator's,
    never this check's).

    Parsing is deliberately hostile to near-misses: fields are read ONLY from the suffix
    after the marker (so prose earlier in the row cannot satisfy the gate), duplicates
    are rejected rather than last-wins, fenced blocks and inline-code spans are stripped
    (so a row *quoting* the marker stays a proposal), and a lookalike delimiter is
    surfaced rather than failing open. Read-only.
    """
    name = "routine_consumers"
    # [#589] — READ THE CANONICAL FULL-BODY TEXT. `· routine:` markers and their
    # `consumer=`/`consumption_path=` fields live in a row BODY, and the committed
    # `BACKLOG.md` is now a one-line projection that carries none of them. Pointed at the
    # projection this check finds zero markers, reports "no routines declared", and PASSES
    # — measuring an empty set and calling it green, which is the precise silent-inertness
    # class [#424]/[#425] were filed for and that the lookalike-delimiter leg above already
    # exists to refuse. On a consumer repo (no `tasks/` tree) `canonical_text` returns the
    # hand-authored `BACKLOG.md`, so the per-repo fleet scan is unchanged.
    try:
        from scripts import backlog_source as _bs
    except ImportError:
        import backlog_source as _bs
    try:
        text = _bs.canonical_text(Path(repo_path))
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        # FAIL, not "unavailable" (green-by-skip sweep, 2026-08-25; same call
        # check_silent_rule_ratchet made at terra HIGH 2026-07-27). `unavailable` renders
        # as N/A and `_check_outcome` projects it onto `pass`, so ship-gate waves it
        # through -- a check that measured NOTHING would ship green. The absent-source case
        # is NOT-APPLICABLE below, so reaching here means a source EXISTS and could not be
        # read or reassembled: a failed computation of an available ground truth, not an
        # inapplicable context. The non-OSError arms are [#589]'s: a malformed manifest or
        # an unreadable task file now fails HERE rather than in a file read.
        return [Finding(name, "fail", f"cannot read the backlog source: {exc}")]
    if text is None:
        return [_na(name, "NOT-APPLICABLE", "no backlog source in this repo")]
    bad: list[str] = []
    declared = 0
    fence: tuple[str, int] | None = None      # (char, run-length) of the OPEN fence
    for lineno, line in enumerate(text.splitlines(), 1):
        fm = _ROUTINE_FENCE_RE.match(line)
        if fm:
            run = fm.group("fence")
            if fence is None:
                fence = (run[0], len(run))    # indented >3 never opens (regex bounds it)
                continue
            if run[0] == fence[0] and len(run) >= fence[1]:
                fence = None                  # only a same-char, >=-length run closes
            continue
        if fence is not None:
            continue                          # an example is not a declaration
        task = _ROUTINE_TASK_RE.match(line)
        if not task:
            continue
        loc = f"[#{task.group(1)}] line {lineno}"
        spans = _routine_code_spans(line)
        markers = [m for m in _ROUTINE_MARKER_RE.finditer(line)
                   if not _routine_in_code(m.start(), spans)]
        if not markers:
            look = _ROUTINE_LOOKALIKE_RE.search(line)
            if look and not _routine_in_code(look.start(), spans) \
                    and _ROUTINE_ANYFIELD_RE.search(line):
                bad.append(f"{loc}: lookalike delimiter before 'routine:' — a mistyped "
                           f"marker must not fail open".replace("|", "/"))
            continue
        declared += 1
        if len(markers) > 1:
            # A second marker would lend its fields to an incomplete first declaration.
            bad.append(f"{loc}: {len(markers)} 'routine:' markers on one row — "
                       f"ambiguous declaration".replace("|", "/"))
            continue
        suffix = line[markers[0].end():]  # fields belong to the DECLARATION, not the row
        found: dict[str, list[str]] = {}
        for key, value in _ROUTINE_FIELD_RE.findall(suffix):
            found.setdefault(key, []).append(value)
        problems: list[str] = []
        for required in _ROUTINE_REQUIRED:
            values = found.get(required, [])
            if len(values) > 1:
                problems.append(f"{required} declared {len(values)}x")
            elif not values or not _routine_value_is_named(values[0]):
                problems.append(required)
        if problems:
            bad.append(f"{loc}: {', '.join(problems)}".replace("|", "/"))
    if bad:
        return [Finding(name, "fail",
                        "declared routine(s) with no named consumer/consumption_path: "
                        + "; ".join(bad))]
    return [Finding(name, "pass",
                    f"{declared} declared routine row(s) name a consumer and a "
                    f"consumption_path (live hooks/schedules out of scope — [#426])")]
