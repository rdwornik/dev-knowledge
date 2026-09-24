#!/usr/bin/env python
"""handback_schema.py -- the ONE schema for every inter-seat artifact a lane hands back (RC3,
LANE-W4B-2-handback-organ Done-contract 2).

THE DEFECT THIS CLOSES (DECLARE-WAVE4B-DIRECTION-2026-09-22, RC3): "Handback line, LANE-END
report, STATE line, REFUSED order and session-file name are each defined in contracts,
common-rule files and code, and they drift: `audit.py handback` refuses the common-rule form,
two LANE-END shapes circulate, one lane wrote no report, the pre-handback self-check omitted
ship-gate, sessions left polls running three times." Four shapes, one dataclass each, one
parser and one renderer per shape -- so a second grammar for the same artifact cannot arise by
a caller improvising its own string formatting.

  * `HandbackLine`   -- `HANDBACK <branch> @ <sha> [code|docs-only] review=<reviewer> HIGH:n MED:n LOW:n`.
                        NOT reimplemented here: `parse`/`validate` call straight into
                        `audit._review_handback_parse` / `audit.review_handback_verdict` --
                        the SAME functions `audit.py handback` runs -- so "the organ's form and
                        `audit.py handback` agree" is true by construction, not by a second
                        regex that might drift from the first (D-1's own lesson, applied to
                        itself).
  * `StateLine`      -- `STATE <lane> <WAITING|MERGED|REFUSED|CLOSED> <sha> <timestamp> [note]`.
                        Scoped to the LANE-level line a lane or the integrator writes about ONE
                        lane; the batch-level `STATE batch <NAME> ...` variant belongs to the
                        batch-close digest (a different lane, FR5) and is out of scope here --
                        an honest limit, not an oversight.
  * `LaneEndReport`  -- the `# <lane> -- lane-end report` markdown `transport_report.py` writes
                        and `lane_digest.py` reads back. The render/parse pair MOVED here from
                        `transport_report.py` verbatim (byte-for-byte the same output); that
                        module now imports both rather than defining its own copy.
  * `RefusedOrder`   -- new: what the handback organ writes when its self-check fails. A
                        `to-browser/HANDBACK-REFUSED-<lane>.md` naming which leg failed and why,
                        plus the same facts as a JSON receipt, so a refusal is inspectable by a
                        human (the file) and a machine (the receipt) from one write. The
                        `HANDBACK-` prefix is D10 (DECLARE-WINDOW-DEFECTS-2026-09-23): plain
                        `REFUSED-<lane>.md` is the INTEGRATOR's own repair-order filename, and
                        wave-4B measured the collision when this organ's self-refusal receipt
                        landed there and overwrote the integrator's executable order.

Read-only where it can be (rendering and parsing are pure functions of their inputs); the one
side effect this module can have is `HandbackLine`'s import of `audit.py` for the grammar it
does not re-derive.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

SCHEMA_VERSION = 1


def _audit():
    """`audit.py`, imported lazily.

    `transport_report.py` (the Stop-hook organ, 15s shared budget, "Standard library only" by
    its own docstring) imports THIS module for the LANE-END shapes only and never touches
    `HandbackLine`. A module-level `import audit` would still cost every Stop-hook turn end
    (`audit.py` pulls in `click` and `yaml` and is ~6800 lines) even though only the organ CLI
    (`scripts/handback.py`, not on that path) ever calls the functions below that need it.
    """
    import audit as _mod  # noqa: PLC0415
    return _mod


# --- 1. HANDBACK line ------------------------------------------------------------------------

#: `("code", "docs-only")` -- computed lazily (see `_audit` above), so importing this module
#: costs nothing until a caller actually asks for a HANDBACK-line grammar object.
def _handback_classes() -> tuple[str, ...]:
    return _audit()._REVIEW_HANDBACK_CLASSES


@dataclass(frozen=True)
class HandbackLine:
    """One 027 HANDBACK line, parsed or about to be rendered. `reviewer`/`high`/`med`/`low` are
    `None` for a docs-only line carrying no review token -- the class distinguishes "no review
    owed" from "review reported zero of everything", which a `0`/`None` conflation would lose."""
    branch: str
    sha: str
    cls: str
    reviewer: Optional[str] = None
    high: Optional[int] = None
    med: Optional[int] = None
    low: Optional[int] = None

    def render(self) -> str:
        parts = [f"HANDBACK {self.branch} @ {self.sha} {self.cls}"]
        if self.reviewer is not None:
            parts.append(f"review={self.reviewer}")
        if self.high is not None and self.med is not None and self.low is not None:
            parts.append(f"HIGH:{self.high} MED:{self.med} LOW:{self.low}")
        return " ".join(parts)

    @classmethod
    def parse(cls, line: str) -> Optional["HandbackLine"]:
        """Structural parse -- accepts a well-SHAPED line whether or not it would MERGE (a
        docs-only line with no review token parses fine; `validate()` is the merge verdict)."""
        audit = _audit()
        parsed = audit._review_handback_parse(line)
        if parsed is None:
            return None
        tokens = parsed["tokens"]
        branch_cls = tokens[0] if tokens else None
        if branch_cls not in _handback_classes():
            return None
        reviewers = [m.group("reviewer") for m in
                     (audit._REVIEW_TOKEN_RE.match(t) for t in tokens[1:]) if m]
        if len(reviewers) > 1:
            # `review_handback_verdict` REFUSES >1 review= token outright (D-1: "a line that
            # contradicts itself asserts nothing") -- collapsing to reviewer=None here would
            # make `parse(line).validate()` MERGE a line `validate_handback_line(line)` refuses,
            # the exact round-trip drift this schema exists to make impossible (terra HIGH).
            return None
        reviewer = reviewers[0] if reviewers else None
        counts = audit._review_handback_tally(tokens[1:])
        return cls(branch=parsed["branch"], sha=parsed["sha"], cls=branch_cls,
                    reviewer=reviewer,
                    high=counts.get("HIGH") if counts else None,
                    med=counts.get("MED") if counts else None,
                    low=counts.get("LOW") if counts else None)

    def validate(self) -> tuple[bool, str]:
        """The merge verdict -- delegates to `audit.review_handback_verdict` on this line's own
        rendering, so this can never accept a line the CLI would refuse, or vice versa."""
        return _audit().review_handback_verdict(self.render())


def validate_handback_line(line: str) -> tuple[bool, str]:
    """Verdict on a raw line, without constructing a `HandbackLine` first -- what the organ's
    self-check and `audit.py handback` both call, so a caller never has two ways to ask."""
    return _audit().review_handback_verdict(line)


# --- 2. STATE line ----------------------------------------------------------------------------

STATE_WAITING = "WAITING"
STATE_MERGED = "MERGED"
STATE_REFUSED = "REFUSED"
STATE_CLOSED = "CLOSED"
STATE_VERDICTS = frozenset({STATE_WAITING, STATE_MERGED, STATE_REFUSED, STATE_CLOSED})

_STATE_LINE_RE = re.compile(
    r"^STATE[ \t]+(?P<lane>\S+)[ \t]+(?P<verdict>[A-Z]+)[ \t]+(?P<sha>\S+)[ \t]+(?P<ts>\S+)"
    r"(?:[ \t]+(?P<note>.*))?$")
_STATE_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
_STATE_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


@dataclass(frozen=True)
class StateLine:
    """A LANE-level `STATE` line -- what a lane declares about itself at handback (`WAITING`),
    and what the integrator later overwrites it to (`MERGED` / `REFUSED` / `CLOSED`). The
    batch-level `STATE batch <NAME> ...` shape is a different grammar and is not modelled here
    (see module docstring)."""
    lane: str
    verdict: str
    sha: str
    timestamp: str
    note: str = ""

    def render(self) -> str:
        tail = f" {self.note}" if self.note else ""
        return f"STATE {self.lane} {self.verdict} {self.sha} {self.timestamp}{tail}"

    @classmethod
    def parse(cls, line: str) -> Optional["StateLine"]:
        if not line or "\n" in line or "\r" in line:
            return None
        m = _STATE_LINE_RE.match(line.strip())
        if m is None:
            return None
        return cls(lane=m.group("lane"), verdict=m.group("verdict"), sha=m.group("sha"),
                   timestamp=m.group("ts"), note=(m.group("note") or "").strip())

    def validate(self) -> tuple[bool, str]:
        where = f"{self.lane} {self.sha}"
        if self.verdict not in STATE_VERDICTS:
            return False, (f"REFUSE {where}: verdict {self.verdict!r} is not one of "
                           f"{sorted(STATE_VERDICTS)}")
        if not _STATE_SHA_RE.match(self.sha):
            return False, f"REFUSE {where}: {self.sha!r} is not a sha (>=7 hex)"
        if not _STATE_TS_RE.match(self.timestamp):
            return False, (f"REFUSE {where}: {self.timestamp!r} is not "
                           f"YYYY-MM-DDTHH:MM:SSZ")
        return True, f"OK {self.lane} {self.verdict} {self.sha} {self.timestamp}"


def validate_state_line(line: str) -> tuple[bool, str]:
    parsed = StateLine.parse(line)
    if parsed is None:
        return False, (f"REFUSE: not a single STATE line -- expected exactly "
                       f"`STATE <lane> <{'|'.join(sorted(STATE_VERDICTS))}> <sha> <timestamp> "
                       f"[note]`, one line, nothing around it")
    return parsed.validate()


# --- 3. LANE-END report ------------------------------------------------------------------------

VERDICT_CLEAN = "finished clean"
VERDICT_ATTENTION = "needs attention"
VERDICT_INCOMPLETE = "incomplete"
REPORT_VERDICTS = frozenset({VERDICT_CLEAN, VERDICT_ATTENTION, VERDICT_INCOMPLETE})

_HEADING_RE = re.compile(r"^#\s+(\S+)\s+--\s+lane-end report\s*$", re.MULTILINE)
_RECEIPT_BLOCK_RE = re.compile(r"^###\s+(\S+\.json)\s*$\n+```json\n(.*?)\n```",
                               re.MULTILINE | re.DOTALL)


def _section(text: str, heading: str) -> Optional[str]:
    """The body of one `## heading` (or `## heading (N)`) section, up to the next `## ` or the
    end of the text. `None` when the heading is not there at all -- distinct from empty."""
    pattern = re.compile(rf"^##\s+{re.escape(heading)}(?:\s*\(\d+\))?\s*$\n(.*?)(?=^##\s|\Z)",
                         re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip("\n") if match else None


def _bullets(body: Optional[str]) -> list[str]:
    if not body:
        return []
    return [line[2:].rstrip() for line in body.splitlines() if line.startswith("- ")]


@dataclass
class LaneEndReport:
    """What `LaneEndReport.parse` reads back out of a `LANE-END-<lane>.md` this module wrote.
    `lane_digest.py --reports-root` reads this (through `transport_report.parse_report`,
    kept as the stable import name) instead of re-deriving the same facts from git after a
    merge fast-forwards HEAD and the range that would answer them goes empty."""
    lane: Optional[str] = None
    commits: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    verdict: Optional[str] = None
    receipts: list[dict] = field(default_factory=list)

    @classmethod
    def parse(cls, text: str) -> "LaneEndReport":
        """Never raises -- a section that is not there reads as empty/None, the same
        "never silently dropped, always named" posture the receipt reader takes on a
        malformed embedded receipt."""
        heading = _HEADING_RE.search(text)
        receipts = []
        for name, body in _RECEIPT_BLOCK_RE.findall(_section(text, "Receipts") or ""):
            try:
                row = json.loads(body)
            except ValueError:
                row = None
            if not (isinstance(row, dict) and row.get("organ")):
                row = {"organ": name.rsplit(".", 1)[0], "status": "unreadable"}
            receipts.append(row)
        verdict_body = _section(text, "Verdict")
        return cls(lane=heading.group(1) if heading else None,
                   commits=_bullets(_section(text, "Commits")),
                   changed=_bullets(_section(text, "Changed files")),
                   verdict=verdict_body.strip() if verdict_body else None,
                   receipts=receipts)

    def validate(self) -> tuple[bool, str]:
        """Structural validity: a heading, a Commits section (even if empty) and a verdict in
        the enum -- the shape `parse_report` must be able to read something out of, per the
        plan's acceptance leg ("byte-validated against the schema")."""
        if not self.lane:
            return False, "REFUSE: no `# <lane> -- lane-end report` heading"
        if self.verdict is None:
            return False, f"REFUSE {self.lane}: no ## Verdict section"
        if self.verdict not in REPORT_VERDICTS:
            return False, (f"REFUSE {self.lane}: verdict {self.verdict!r} is not one of "
                           f"{sorted(REPORT_VERDICTS)}")
        return True, f"OK {self.lane}: {len(self.commits)} commit(s), verdict {self.verdict!r}"


def render_lane_end_report(lane: str, generated: str, commits: list[str], changed: list[str],
                           verdict: str, session_summary: str,
                           raw_receipts: list[tuple[str, str]]) -> str:
    """The markdown `transport_report.build_report` writes -- moved here verbatim so the
    render and the parse it must round-trip through live beside each other. `raw_receipts` are
    the VERBATIM (name, text) pairs `collect_receipts` reads off disk (never re-serialized
    through `json.dumps`, which would silently "fix" a truncated or malformed one)."""
    parts = [f"# {lane} -- lane-end report", "",
            f"generated: {generated} (replaced at every turn end; the newest run is the only copy)",
            "", f"## Commits ({len(commits)})", ""]
    parts += [f"- {c}" for c in commits] if commits else ["No commits recorded."]
    parts += ["", f"## Changed files ({len(changed)})", ""]
    parts += [f"- {c}" for c in changed] if changed else ["No changed files."]
    parts += ["", "## Verdict", "", verdict, "",
             "## Session summary", "", session_summary, "",
             f"## Receipts ({len(raw_receipts)})", ""]
    if not raw_receipts:
        parts += ["No receipts found for this lane.", ""]
    for name, text in raw_receipts:
        parts += [f"### {name}", "", "```json", text.rstrip(), "```", ""]
    return "\n".join(parts)


# --- 4. REFUSED order --------------------------------------------------------------------------

@dataclass(frozen=True)
class CheckResult:
    """One leg of the organ's self-check."""
    name: str
    ok: bool
    detail: str


@dataclass
class RefusedOrder:
    """What the handback organ writes when any self-check leg fails: `to-browser/HANDBACK-
    REFUSED-<lane>.md` (human-readable) and, embedded in it, the same facts as a JSON receipt
    (machine-readable) -- one write, two readers, the D-1 discipline applied to a refusal
    rather than a merge. The `HANDBACK-` prefix (D10) keeps this filename distinct from the
    integrator's own `REFUSED-<lane>.md` repair order -- see the module docstring."""
    lane: str
    branch: str
    checks: list[CheckResult]
    finished_at: str
    schema: int = SCHEMA_VERSION
    organ: str = "handback"

    @property
    def reasons(self) -> list[str]:
        return [f"{c.name}: {c.detail}" for c in self.checks if not c.ok]

    def to_receipt(self) -> dict:
        return {"schema": self.schema, "organ": self.organ, "status": "REFUSED",
                "lane": self.lane, "branch": self.branch,
                "checks": {c.name: {"ok": c.ok, "detail": c.detail} for c in self.checks},
                "reasons": self.reasons, "finished_at": self.finished_at}

    def render(self) -> str:
        lines = [f"# REFUSED -- {self.lane}", "",
                f"branch: {self.branch}", f"finished_at: {self.finished_at}", "",
                "## Self-check", ""]
        for c in self.checks:
            lines.append(f"- [{'ok' if c.ok else 'FAIL'}] {c.name}: {c.detail}")
        lines += ["", "## Reasons", ""]
        lines += [f"- {r}" for r in self.reasons] if self.reasons else \
                 ["(none named -- an internal error refused the run; see the receipt)"]
        lines += ["", "## Receipt", "", "```json",
                 json.dumps(self.to_receipt(), indent=2, sort_keys=True), "```", ""]
        return "\n".join(lines)

    @classmethod
    def parse(cls, text: str) -> Optional["RefusedOrder"]:
        """Reads a `HANDBACK-REFUSED-<lane>.md` this module wrote back into structure, via its
        embedded receipt block -- the same round-trip discipline the other three shapes carry."""
        m = re.search(r"^```json\n(.*?)\n```", text, re.MULTILINE | re.DOTALL)
        if not m:
            return None
        try:
            data = json.loads(m.group(1))
        except ValueError:
            return None
        if not isinstance(data, dict) or data.get("organ") != "handback":
            return None
        checks = [CheckResult(name=name, ok=bool(v.get("ok")), detail=str(v.get("detail", "")))
                 for name, v in (data.get("checks") or {}).items()]
        return cls(lane=str(data.get("lane", "")), branch=str(data.get("branch", "")),
                  checks=checks, finished_at=str(data.get("finished_at", "")),
                  schema=int(data.get("schema", SCHEMA_VERSION)))

    def validate(self) -> tuple[bool, str]:
        if not self.lane or not self.branch:
            return False, "REFUSE: a REFUSED order needs both a lane and a branch"
        if not self.reasons:
            return False, f"REFUSE {self.lane}: no failing check is named"
        return True, f"OK {self.lane}: refused on {len(self.reasons)} check(s)"
