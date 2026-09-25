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

WHY BLOCKING IS SAFE HERE WHEN IT WAS RETIRED ELSEWHERE -- FIRE-ONCE, NOT SCOPE ALONE. An
earlier version of this module reasoned that scoping the block to LANE sessions (see
`resolve_lane`) was enough on its own to avoid the ADR-85 block-cap exhaustion that retired
`session_end_backpressure.py`'s own hard leg. A terra review (`docs/audits/
2026-09-25-codex-lane-handback-stop-hook.md`, CRITICAL) correctly rejected that: `resolve_lane`
identifies a LANE, not a genuine completion attempt, and a lane can legitimately pause mid-work
at a Stop boundary before it is actually done -- blocking every such pause unconditionally
reaches the host's consecutive-block cap exactly as ADR-85 describes, and worse, pressures the
agent into writing a premature HANDBACK just to get past the gate. The fix is the SAME
FIRE-ONCE mechanism `session_end_backpressure.py` already uses for its advisories, applied here
to a genuine block instead of a nudge: `stop_hook_active` (present in this CC runtime's
Stop-hook stdin, per that module's own live-witnessed docstring) distinguishes a fresh stop
attempt (`False`) from the host's own automatic retry after THIS hook's last block (`True`).
Blocking fires at most ONCE per fresh attempt -- enough to hand the agent a named reason and let
it fix the line on the very next attempt (the happy path resolves in one round trip, nowhere
near the cap) -- and never chains into a second, third, ... consecutive block within the same
automatic retry, which is the only thing the cap actually counts. A NEW attempt later (e.g. a
dispatcher nudge) is a fresh `stop_hook_active=False` boundary and can refuse again if the line
is still bad -- so the SAME structural condition is caught every time the agent genuinely tries
to conclude, without ever risking a silent auto-bypass mid-attempt. The STRUCTURAL FLOOR mirrors
that module's own: if a runtime omits `stop_hook_active` entirely, this gate stays silent
(never blocks) rather than reintroduce the unconditional-block hazard with no reset signal at
all -- a missing safety mechanism must fail toward inert, not toward the very risk it exists to
prevent.

A non-lane session -- the operator's own -- is untouched: `main` returns 0 with no decision
before it ever reads a session file or `stop_hook_active`.

THE STOP-HOOK CONTRACT this repo has already corrected against the live runtime (CC 2.1.178,
`session_end_backpressure.py`'s own docstring): `{"decision":"block","reason":...}` on stdout
blocks the stop; plain stdout or a bare non-zero exit do not reach the model. This gate uses the
same JSON contract.

THREE NAMED REASONS, not one generic refusal (`classify`): the closing line can be `missing`
(no HANDBACK-shaped text anywhere), `backtick-wrapped` (a shaped candidate exists but sits
inside an inline code span or a fenced/indented code block -- the exact wave-5A incident), or
`malformed` (a shaped attempt exists but is missing a field). Grammar only: this deliberately
does NOT run `handback_schema.HandbackLine.validate()` (the merge-eligibility verdict,
restricted to the `code`/`docs-only` classes `audit.py` knows) -- real closing lines in this
batch alone use `code`, `docs` and `report` (a read-only lane's kind), so a class-enum check
here would refuse lines the batch's own common rules accept. `<kind>` is required to be
PRESENT, never a member of a fixed set.

LAST CANDIDATE WINS, TRULY -- not "any clean candidate found anywhere" (a second terra HIGH
finding against the first cut of this module, which let an earlier clean draft mask a later
bad one; fixed by tracking exactly one running verdict, overwritten by whichever candidate
comes LAST in document order, the same rule `lane_end_guard.last_handback` applies to its own,
looser match). CODE-SPAN DETECTION IS TOKEN-BASED, NOT A PER-LINE BACKTICK SUBSTRING CHECK (the
first cut's second gap: a CommonMark inline code span can itself cross a physical line break,
converting the newline to a space -- `` `\nHANDBACK worktree-x @ sha code\n` `` parses as ONE
`code_inline` token whose own content line has no backtick character on it at all, so a
per-line "does this line contain a backtick" check misses it entirely). This walks the real
`markdown_it` token stream instead: a `fence`/`code_block` token's content is always a code
region; an `inline` token's `.children` are walked directly, splitting `code_inline` children
(opaque, never re-split on the newlines CommonMark already collapsed) from `text`/`softbreak`/
`hardbreak` children (reconstructed as prose, its OWN line breaks preserved, so the "own line"
check still applies precisely). Library-first (O-12): `markdown_it` is already a declared
dependency, the same tool `scripts/normalize_headers.py::_heading_lines` already uses for
CommonMark structure, chosen over a hand-rolled ` ``` `-only toggle for the identical reason
that function's own docstring records (`~~~` fences, indented blocks, longer fences all miss a
naive toggle).

NEVER BRICKS A SESSION ON INFRASTRUCTURE IT DOES NOT CONTROL (the repo-wide fail-soft
convention -- fail-CLOSED on a real, positively-detected bad line, fail-OPEN on everything
else): an unresolvable transport, an unreadable session file, or an internal exception in this
script all return 0 with no decision, exactly like `lane_end_guard.py`'s own REFUSED/skip
paths. Only a session file this gate could actually read and found lacking, on a fresh stop
attempt, ever blocks.

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
from collections.abc import Iterator, Mapping

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


def _prose_and_code_chunks(children) -> Iterator[tuple[bool, str]]:
    """From a flat markdown-it inline `.children` list, yield `(is_code, text)` chunks in
    document order. Prose chunks reconstruct the paragraph's own line breaks (`softbreak` /
    `hardbreak` -> `\\n`) so a later per-line "is this its own line" check still applies to the
    real source; a `code_inline` child's content is yielded WHOLE and opaque, never re-split on
    `\\n` -- CommonMark itself has already collapsed that span's internal line breaks to spaces,
    so there is no source line to recover. Structural markers with no text of their own
    (`strong_open`/`em_open`/`link_open`/their `_close`, images, …) are skipped; their nested
    text still arrives as ordinary flat `text` children."""
    buf: list[str] = []
    for child in children or ():
        t = child.type
        if t == "code_inline":
            if buf:
                yield False, "".join(buf)
                buf = []
            yield True, child.content
        elif t == "text":
            buf.append(child.content)
        elif t in ("softbreak", "hardbreak"):
            buf.append("\n")
    if buf:
        yield False, "".join(buf)


def classify(text: str) -> tuple[str, str | None]:
    """`(status, line)` -- the LAST HANDBACK-shaped candidate found anywhere in the document
    wins outright (closing-line semantics: whatever the LAST attempt looked like is the verdict,
    never "any clean one found anywhere"). A candidate counts as clean only when it sits in
    PROSE (never inside a fenced/indented code block or an inline code span, however that span
    is line-wrapped), its own line starts with `HANDBACK` itself (no prose before it on that
    line), and it carries all three fields -- "on its own line and outside any code span", the
    batch common rules' own phrase for a valid closing line."""
    try:
        tokens = _MD.parse(text)
    except Exception:
        tokens = []
    last_status: str | None = None
    last_line: str | None = None
    saw_word = False

    def consider(chunk: str, is_code: bool) -> None:
        nonlocal last_status, last_line, saw_word
        for raw_line in chunk.split("\n"):
            if _WORD_RE.search(raw_line):
                saw_word = True
            m = _CANDIDATE_RE.search(raw_line)
            if not m:
                continue
            stripped = raw_line.strip()
            if is_code or not stripped.startswith("HANDBACK"):
                last_status, last_line = STATUS_WRAPPED, stripped
            elif m.group("kind") is None:
                last_status, last_line = STATUS_MALFORMED, stripped
            else:
                last_status, last_line = STATUS_OK, stripped

    for tok in tokens:
        if tok.type in ("fence", "code_block"):
            consider(tok.content, is_code=True)
        elif tok.type == "inline":
            for is_code, chunk in _prose_and_code_chunks(tok.children):
                consider(chunk, is_code)

    if last_status is not None:
        return last_status, last_line
    if saw_word:
        return STATUS_MALFORMED, None
    return STATUS_MISSING, None


def reason(status: str, line: str | None, session_path: str) -> str:
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


def _read_stop_hook_active(environ: Mapping[str, str]) -> bool | None:
    """`stop_hook_active` from the Stop-hook's JSON stdin payload -- `True` on the host's own
    automatic retry after a block, `False` on a fresh stop attempt, `None` when the field is
    absent or stdin is empty/unparseable (fail-soft, matching `session_end_backpressure.py`'s
    own `_read_hook_input`). A test harness may instead set `HARNESS_STOP_HOOK_ACTIVE` directly
    (`"true"`/`"false"`) rather than fabricate a stdin pipe."""
    override = environ.get("HARNESS_STOP_HOOK_ACTIVE")
    if override is not None:
        return override.strip().lower() == "true"
    try:
        raw = sys.stdin.read()
    except Exception:
        return None
    if not raw or not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except Exception:
        return None
    if not isinstance(data, dict) or "stop_hook_active" not in data:
        return None
    return bool(data["stop_hook_active"])


def main(argv: list[str] | None = None, *, environ: Mapping[str, str] = os.environ,
         root: Path = _ROOT, resolve_transport=None) -> int:
    """Returns 0 on every path (never the code a Stop hook reads as a raw block). A refusal is
    communicated ONLY via `{"decision":"block","reason":...}` JSON on stdout -- the live
    Stop-hook contract this repo already corrected against CC 2.1.178
    (`session_end_backpressure.py`). Blocks at most once per fresh stop attempt (see the module
    docstring's FIRE-ONCE section) -- the STRUCTURAL FLOOR: when `stop_hook_active` cannot be
    read at all, this gate stays silent rather than block unconditionally with no reset signal."""
    try:
        lane = resolve_lane(environ, root)
        if not lane:
            return 0  # Done-contract 2: non-lane sessions are unaffected
        active = _read_stop_hook_active(environ)
        if active is not False:  # STRUCTURAL FLOOR: True (a retry) or None (unknown) -> silent
            return 0
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
