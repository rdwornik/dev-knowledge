#!/usr/bin/env python
"""lane_handback_gate.py -- the Stop hook that REFUSES to let a LANE session end without a
clean, machine-parseable closing `HANDBACK <branch> @ <sha> <kind>` line ([#1010], WAVE5B-N1
lane-handback-stop-hook).

THE DEFECT THIS CLOSES: the handback line's grammar was not enforced at write time. Two
wave-5A handbacks reached the integrator 2-4 h late -- one swallowed by an orphaned poll loop,
one because the HANDBACK line sat inside inline backticks, invisible to a caret-anchored poll
-- and one lane handed back with a `## HANDBACK` heading instead of the machine line entirely
(`to-browser/SESSION-integrator-wave5a-2026-09-23.md`). None of those three shapes stop a
session today; this gate makes them refuse it instead.

WHY THIS IS A SEPARATE MODULE FROM `lane_end_guard.py`. That guard's own docstring states an
invariant load-bearing for its own tests (DECLARE-NIGHT N3): "NEVER BLOCKS THE SESSION" -- it
returns 0 on every path, by design, because it is a MOMENT TRIGGER, not a gate. Folding a block
into it would break that invariant and the tests that pin it. This module is the opposite kind
of organ on purpose: it exists ONLY to block.

WHY BLOCKING IS SAFE HERE WHEN IT WAS RETIRED ELSEWHERE. `session_end_backpressure.py`
(this repo's other Stop hook) tried a HARD block once and reverted it (ADR-85 amendment
2026-08-03): a Stop hook's unit is a model-turn boundary, the host force-ends a turn after N
consecutive blocks, and on an ordinary INTERACTIVE session that boundary recurs on every reply
-- nine consecutive blocks bought zero enforcement and ended in a silent auto-bypass. This gate
avoids that fate by scope, not by a smarter loop: it fires ONLY for a LANE session (see
`resolve_lane`), which stops rarely (completion, plus at most two dispatcher nudges per the
batch common rules) rather than on every interactive reply. A non-lane session -- the operator's
own -- is untouched: `main` returns 0 with no decision before it ever reads a session file.

THE STOP-HOOK CONTRACT this repo has already corrected against the live runtime (CC 2.1.178,
`session_end_backpressure.py`'s own docstring): `{"decision":"block","reason":...}` on stdout
blocks the stop; plain stdout or a bare non-zero exit do not reach the model. This gate uses the
same JSON contract, once, per turn end -- deliberately WITHOUT the fire-once suppression that
module uses for its advisories, because fire-once exists to keep a non-blocking nudge from
looping into the block-cap; a gate that is SUPPOSED to keep blocking until fixed must not
silence itself on the retry.

THREE NAMED REASONS, not one generic refusal (`classify`): the closing line can be `missing`
(no HANDBACK-shaped text anywhere), `backtick-wrapped` (a shaped candidate exists but sits
inside inline backticks or a fenced code block -- the exact wave-5A incident), or `malformed`
(a shaped attempt exists but is missing a field). Grammar only: this deliberately does NOT run
`handback_schema.HandbackLine.validate()` (the merge-eligibility verdict, restricted to the
`code`/`docs-only` classes `audit.py` knows) -- real closing lines in this batch alone use
`code`, `docs` and `report` (a read-only lane's kind), so a class-enum check here would refuse
lines the batch's own common rules accept. `<kind>` is required to be PRESENT, never a member of
a fixed set.

NEVER BRICKS A SESSION ON INFRASTRUCTURE IT DOES NOT CONTROL (the repo-wide fail-soft
convention -- fail-CLOSED on a real, positively-detected bad line, fail-OPEN on everything
else): an unresolvable transport, an unreadable session file, or an internal exception in this
script all return 0 with no decision, exactly like `lane_end_guard.py`'s own REFUSED/skip
paths. Only a session file this gate could actually read and found lacking ever blocks.

FLOOR: hub-only, for the same one-line reason as `lane_end_guard.py` and `transport_report.py`:
it reads the operator's transport drive and the lane's own harness environment, neither of
which a consumer repo carries.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Mapping, Optional

from markdown_it import MarkdownIt

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

from lane_end_guard import resolve_lane  # noqa: E402 -- the ONE lane predicate, never a second copy

STATUS_OK = "ok"
STATUS_MISSING = "missing"
STATUS_WRAPPED = "backtick-wrapped"
STATUS_MALFORMED = "malformed"

# A candidate: `HANDBACK <branch> @ <sha>`, with an optional third `<kind>` token. Looser than
# the full batch-common shape (no fixed kind enum, trailing `review=...`/`HIGH:n` tokens
# ignored) -- this gate checks PRESENCE and SHAPE, never merge-eligibility.
_CANDIDATE_RE = re.compile(r"HANDBACK\s+(?P<branch>\S+)\s+@\s+(?P<sha>\S+)(?:\s+(?P<kind>\S+))?")
_WORD_RE = re.compile(r"\bHANDBACK\b")
_MD = MarkdownIt("commonmark")


def _fenced_lines(text: str) -> set[int]:
    """0-based source lines CommonMark says are INSIDE a fenced or indented code block -- any
    fence style (```` ``` ````, `~~~`, any fence length, up to the 3-space indent CommonMark
    allows), library-first (O-12) the same way `normalize_headers.py::_heading_lines` already
    does for headings, and for the identical reason recorded in that function's own docstring:
    a hand-rolled ` ``` `-only toggle misses every other fence shape (the named defect it once
    shipped with). POSITIVE identification via a real CommonMark parse, not a blocklist pattern.
    Fail-soft: an unparseable document contributes no fenced lines rather than raising."""
    try:
        tokens = _MD.parse(text)
    except Exception:
        return set()
    lines: set[int] = set()
    for tok in tokens:
        if tok.type in ("fence", "code_block") and tok.map:
            lines.update(range(tok.map[0], tok.map[1]))
    return lines


def classify(text: str) -> tuple[str, Optional[str]]:
    """`(status, line)` -- the LAST HANDBACK-shaped candidate wins (closing-line semantics, the
    same rule `lane_end_guard.last_handback` uses), so an earlier bad mention never poisons a
    later clean one, and a later stray mention never downgrades an earlier clean one once `ok`
    has been found. A candidate counts as clean only when its line, stripped, starts with
    `HANDBACK` itself (no prose before it), carries no backtick anywhere on the line (an inline
    code span), and is not inside a fenced/indented code block -- "on its own line and outside
    any code span", the batch common rules' own phrase for a valid closing line."""
    fenced = _fenced_lines(text)
    ok_line = wrapped_line = malformed_line = None
    saw_word = False
    for i, raw in enumerate(text.splitlines()):
        if _WORD_RE.search(raw):
            saw_word = True
        m = _CANDIDATE_RE.search(raw)
        if not m:
            continue
        stripped = raw.strip()
        if i in fenced or "`" in raw or not stripped.startswith("HANDBACK"):
            wrapped_line = stripped
            continue
        if m.group("kind") is None:
            malformed_line = stripped
            continue
        ok_line = stripped
    if ok_line is not None:
        return STATUS_OK, ok_line
    if wrapped_line is not None:
        return STATUS_WRAPPED, wrapped_line
    if malformed_line is not None:
        return STATUS_MALFORMED, malformed_line
    if saw_word:
        return STATUS_MALFORMED, None
    return STATUS_MISSING, None


def reason(status: str, line: Optional[str], session_path: str) -> str:
    """`what failed -> expected -> directive` (the same shape `session_end_backpressure.py`
    uses for its own advisory lines) -- empty for `STATUS_OK`, since a clean line never blocks."""
    where = f"in {session_path}"
    if status == STATUS_OK:
        return ""
    if status == STATUS_MISSING:
        return (f"HANDBACK missing: no closing line found {where} -> expected "
                f"`HANDBACK <branch> @ <sha> <kind>` as its own line, outside any code span -> "
                f"write the closing HANDBACK line before ending.")
    if status == STATUS_WRAPPED:
        return (f"HANDBACK backtick-wrapped: found {line!r} {where} inside a code span or "
                f"fenced block -> expected the same line on its own, outside any code span -> "
                f"move the closing HANDBACK line out of the backticks/fence.")
    return (f"HANDBACK malformed: found {line!r} {where} but it does not match "
            f"`HANDBACK <branch> @ <sha> <kind>` -> expected all three fields (branch, sha, "
            f"kind) -> fix the line's shape before ending.")


def _default_resolve_transport() -> Path:
    import transport_report  # noqa: PLC0415 -- stdlib-only; imported only once a lane needs it
    return transport_report.resolve_transport()


def main(argv: Optional[list[str]] = None, *, environ: Mapping[str, str] = os.environ,
         root: Path = _ROOT, resolve_transport=None) -> int:
    """Returns 0 on every path (never the code a Stop hook reads as a raw block). A refusal is
    communicated ONLY via `{"decision":"block","reason":...}` JSON on stdout -- the live
    Stop-hook contract this repo already corrected against CC 2.1.178
    (`session_end_backpressure.py`)."""
    try:
        lane = resolve_lane(environ, root)
        if not lane:
            return 0  # Done-contract 2: non-lane sessions are unaffected
        session = environ.get("HARNESS_SESSION_FILE")
        if not session:
            try:
                session = str((resolve_transport or _default_resolve_transport)()
                              / f"SESSION-{lane}.md")
            except Exception:
                return 0  # transport unresolvable: an infra problem, never blocks
        try:
            text = Path(session).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return 0  # session file not there yet: an infra/timing problem, never blocks
        status, line = classify(text)
        if status == STATUS_OK:
            return 0
        print(json.dumps({"decision": "block", "reason": reason(status, line, session)}))
        return 0
    except Exception as exc:  # noqa: BLE001 -- a broken gate must never brick a session
        print(f"lane_handback_gate: DEGRADED ({exc!r}) -- allowing stop", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
