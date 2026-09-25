"""seat_refusals.py -- rules that failed in practice, rebuilt as REFUSALS.

FIVE FROM BATCHES T AND U, plus a sixth added by `[#675]` target 3.4. The sixth arrives from a
different direction and that is worth saying: the first five are rules that existed in prose and
were breached; `file-collision` is a rule that did NOT exist, found by measuring what a real
batch's contracts actually declare. Both end in the same place, because both failures are the
same shape -- a cost paid before anything is in a position to refuse it.

WHY CODE AND NOT PROSE. Every rule below already existed in `protocols/PLAYBOOK.md` Ch8 and was
broken anyway, by seats that had read it (DECLARE-REVIEWS-2026-09-07 §B R-6: "under-mechanised,
failed in T/U"). A rule a reader can skim past and still breach is not enforcement -- so these
raise `SeatRefusal`. A warning printed afterwards is the state being replaced: by then the lane
has ended its turn on an intention, the seventh worktree exists, the substituted reviewer's
finding count is already in the tally, and the decision file is already on the transport with no
carrier. **A prose reminder is not a refusal**, which is the anti-pattern this module's own
contract names.

THE SIX, and where each one is ruled:

  1. `sleeping-poll`     Ch8 "Batch communication" -> "Poll-as-code -- NO SEAT ENDS A TURN ON A
                         WAIT". A wait is a loop with an interval, a bound and a state predicate
                         read from the file surface; a turn that ends on an intention has no
                         next tick, so nothing wakes the session.
  2. `lane-ceiling`      Ch8 "The dispatch table" -> "The ceiling is checked at STEP 0, and it is
                         a REFUSAL". ADR-110's 4-6 batch ceiling. WHERE the check sits is the
                         whole mechanism, so calling it late is itself refused.
  3. `reviewer-mismatch` Ch8 "Model + effort" -> "The reviewer's MODEL ID rides the tally line".
                         A review by an unrequested model is a different measurement wearing the
                         requested one's label; the honest report is `review=NONE`.
  4. `carried-by`        Handoff probe P11 / OPERATOR-INTERFACE §1. A DECLARE-/AMEND-/BATCH-
                         file states the repo home that carries its decision, or the literal
                         OPEN. This is the WRITE-TIME leg: `[#643]`'s lane builds the read-time
                         `preflight_rows` leg, and the two are deliberately different organs.
  5. `dryrun-step0`      AMEND-BATCH-V-002 §1. `-DryRun` of every generated contract is the LAST
                         LINE of dispatcher step 0. Batch V discovered a generator/verb defect by
                         running it; a dispatcher that skips the DryRun launches into a refusal.
  6. `file-collision`    `[#675]` target 3.4. No two lanes in a batch declare writes to the same
                         file. Evaluated on the FROZEN CONTRACT SET at step 0, before the first
                         worktree exists -- run later, the collision has already been paid for
                         and every remaining option is a teardown.

HONEST LIMITS, stated because a refusal that overstates its reach is worse than none:

  * `refuse_sleeping_poll` reads TEXT. It catches a wait written as an English intention and a
    wait declaration missing one of its three parts. It cannot tell whether a well-formed
    predicate is TRUE of the file surface, or whether the loop that carries it was ever run.
  * `refuse_lane_ceiling` is called by a seat; nothing calls it for one. It is wired into the
    dispatcher seat template (`templates/seats/`) and asserted there by test, which is a wiring
    proof and not an enforcement proof -- no gate counts a plan's lane list.
  * `refuse_uncarried_decision_write` checks that a carrier VALUE is well-formed. Whether a path
    value resolves on `main` is the read-time leg's question, and it is not asked here: the write
    happens on the transport, often before the carrier has landed.
  * `refuse_file_collision` reads DECLARED footprints. A contract states the files it intends to
    touch; a lane that writes outside its declaration is invisible to this check, which is why
    the contract separately forbids that ("No edits outside this lane's declared footprint").
    It also cannot see a collision through a DERIVED surface -- two lanes declaring different
    sources that regenerate one index do collide in fact and not in declaration. Both limits are
    under-reach, never over-reach: this refuses only what it can actually see.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import boot_frontier as _bf
except ImportError:                                  # imported as `scripts.seat_refusals`
    from scripts import boot_frontier as _bf

try:
    import validate_hermetization as _herm
except ImportError:                                  # imported as `scripts.seat_refusals`
    from scripts import validate_hermetization as _herm

#: The refusal ids, in the order the lane contract enumerates them (four contracted plus the
#: fifth added by AMEND-BATCH-V-002 §1). A seat template cites these ids; tests assert the roster.
REFUSALS: tuple[str, ...] = (
    "sleeping-poll", "lane-ceiling", "reviewer-mismatch", "carried-by", "dryrun-step0",
    # SIXTH, added by `[#675]` target 3.4. It joins the STEP-0 family rather than standing
    # alone, because its whole argument is the one `lane-ceiling` already makes: a collision
    # found after provisioning has already been paid for.
    "file-collision",
    # SEVENTH, added by lane `aa-2` with the integrator's plan/execute split. It is the only
    # refusal addressed to a seat's CHEAPER HALF, and that is the whole of its argument: the
    # split routes the mechanical walk to Sonnet, and "escalate anything the plan does not rule"
    # is -- as an instruction -- a judgment call handed to the half that cannot make one. This
    # turns it into a predicate the execute half RUNS. A boundary whose enforcement depends on
    # the model reading it has not moved judgment out of the cheap half; it has only stopped
    # writing it down.
    "unruled-merge",
    # EIGHTH and NINTH, added by `[#833]` (lane ab-833). The first seven refuse a seat's ACTS; these
    # two refuse on a seat's STATE, read from `seat_registry.py`, where `state` is written by hook
    # events and never by a model. `no-live-integrator`: a lane dispatched into a batch nobody is
    # receiving (a half-day with no integrator, week of 2026-09-16). `lane-owned`: a second session
    # onto a lane whose owner is live -- witnessed on lane ab-833 itself, 2026-09-17, and admitted
    # into scope by operator ruling the same day.
    "no-live-integrator", "lane-owned",
)

#: WHICH SEAT RUNS WHICH REFUSAL, and in the order its boot runs them. A seat's absence from a
#: refusal's audience is a claim that the seat cannot commit that failure -- `lane-ceiling` and
#: `dryrun-step0` are dispatcher-only because only the dispatcher opens a batch, and a lane never
#: writes a DECLARE-/AMEND-/BATCH- file, so `carried-by` would be an unrunnable line in its boot.
#: `sleeping-poll` is universal: every seat has waits, and every seat stalled on one in T/U.
SEAT_REFUSALS: dict[str, tuple[str, ...]] = {
    # ORDER IS LOAD-BEARING for the dispatcher: `lane-ceiling` opens step 0 (before the first
    # worktree exists) and `dryrun-step0` CLOSES it, because AMEND-BATCH-V-002 §1 makes the
    # DryRun the LAST LINE of step 0. `tests/test_gen_seat_boot.py` runs the DryRun refusal
    # against the rendered step 0 itself, so a reorder here fails the suite rather than quietly
    # moving the check off the boundary it guards.
    # `file-collision` sits BETWEEN them, and the position is the mechanism as much as it is for
    # the two it sits between: it needs the lane list the ceiling just validated (a plan naming a
    # lane twice would collide it with itself and report a nonsense pair), and it must precede
    # the DryRun because the DryRun is the last line of step 0 -- after it the dispatcher fires.
    # `no-live-integrator` follows `file-collision` for the same reason `file-collision` follows the
    # ceiling: every STEP-0 check must precede the DryRun, after which the dispatcher fires.
    "dispatcher": ("lane-ceiling", "file-collision", "no-live-integrator", "carried-by",
                   "sleeping-poll", "dryrun-step0"),
    # `unruled-merge` is LAST for the integrator, and the position is the mechanism the way it is
    # for the dispatcher's two: the other three run once, before the queue opens, while this one
    # runs ONCE PER MERGE, immediately before it. A check that ran at boot would have read a plan
    # the operator went on to amend -- and the amendment is the escalation path working.
    # The integrator runs `no-live-integrator` FIRST, against itself, right after binding: a bind
    # that did not take (wrong batch, no runtime session id) is found at boot, not by the first lane.
    "integrator": ("no-live-integrator", "reviewer-mismatch", "carried-by", "sleeping-poll",
                   "unruled-merge"),
    "filings": ("carried-by", "sleeping-poll"),
    "handoff": ("carried-by", "sleeping-poll"),
    # A lane runs the two seat-state refusals before any work: the owner check first, because two
    # committing sessions on one index is the more expensive failure.
    "lane": ("lane-owned", "no-live-integrator", "reviewer-mismatch", "sleeping-poll"),
}

#: ADR-110's batch ceiling, READ from the organ that already declares it rather than retyped.
#: A second literal `6` is a second thing to keep true, and the chapter carried two rival
#: ceilings in two paragraphs until 2026-09-08 -- which is exactly that failure.
LANE_CEILING: int = _bf.BATCH_WIDTH_MAX


class SeatRefusal(RuntimeError):
    """A seat rule was breached. Raised, never logged -- the caller gets no result at all.

    `refusal` is one of `REFUSALS`; `remedy` says what to do instead, because a refusal that
    names no way forward gets worked around rather than fixed.
    """

    def __init__(self, refusal: str, detail: str, *, remedy: str) -> None:
        self.refusal = refusal
        self.detail = detail
        self.remedy = remedy
        super().__init__(f"REFUSED [{refusal}]: {detail} -- {remedy}")


# --- 1. the sleeping poll ----------------------------------------------------------------------

#: Formulations of a wait-as-intention. Deliberately a SHORT closed list of phrasings that were
#: actually witnessed, not a general "wait" match: a broad regex would fire on every mention of
#: waiting anywhere in a boot paste and the refusal would be turned off within a window.
_WAIT_INTENT_RE = re.compile(
    r"\b(wait(?:s)?\s+(?:for|on|until)|check\s+back|look\s+again\s+later"
    r"|come\s+back\s+to\s+(?:this|it)|resume\s+when|idle\s+until)\b",
    re.IGNORECASE,
)
#: A declared wait. The three keys are Ch8's three parts, named so a missing one is nameable.
_WAIT_DECL_RE = re.compile(r"<!--\s*WAIT:\s*(?P<body>.*?)-->", re.DOTALL)
_WAIT_KEYS = ("interval", "bound", "predicate")
_CH8_BEGIN = re.compile(r"<!--\s*ch8:begin\b")
_CH8_END = re.compile(r"<!--\s*ch8:end\b")
_FENCE = re.compile(r"^\s*```")
#: How far after a wait-intention its declaration may sit. A wait is stated and then written, so
#: the two are adjacent in every honest form of this. The window is what makes the check
#: PER-INTENTION rather than per-document: without it, one valid declaration anywhere in a file
#: satisfies every intention in it, and a seat can still end a turn on an unbounded wait while
#: the refusal reports PASS (terra HIGH, 2026-09-09).
_WAIT_WINDOW = 10


def _authored_lines(text: str) -> list[tuple[int, str]]:
    """`(lineno, line)` for the seat's OWN prose -- quoted Ch8 and fenced code excluded.

    A rendered boot QUOTES Ch8, and Ch8's own `**WAITS.**` paragraph contains the phrase "wait
    for message". That is the rule, not an instance of breaking it, so a checker that fired on it
    would refuse every correct render. Fenced blocks are excluded for the mirror reason: a poll
    loop written as code is the sanctioned form, and its own comments are code.
    """
    out: list[tuple[int, str]] = []
    in_ch8 = in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if _CH8_BEGIN.search(line):
            in_ch8 = True
            continue
        if _CH8_END.search(line):
            in_ch8 = False
            continue
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_ch8 or in_fence:
            continue
        out.append((i, line))
    return out


def _parse_wait(body: str) -> dict[str, str]:
    """`key=value` pairs out of one WAIT declaration. Values run to the next key or the end."""
    keys = "|".join(_WAIT_KEYS)
    found: dict[str, str] = {}
    for m in re.finditer(rf"\b(?P<k>{keys})\s*=\s*(?P<v>.*?)(?=\s+\b(?:{keys})\s*=|$)",
                         body, re.DOTALL):
        found[m.group("k")] = m.group("v").strip()
    return found


def _positive(raw: str) -> bool:
    """True when `raw` opens with a number greater than zero (`60s`, `30`, `2m` all parse)."""
    m = re.match(r"\s*(\d+(?:\.\d+)?)", raw)
    return m is not None and float(m.group(1)) > 0


def refuse_sleeping_poll(text: str, *, site: str) -> int:
    """Every wait in `text` is written as code. Returns the number of declared waits.

    Two legs, and both are needed. LEG A: any wait-INTENTION in the seat's own prose with no
    `<!-- WAIT: ... -->` declaration anywhere in the document is refused -- that is the turn that
    ends with nothing to wake it. LEG B: every declaration carries a positive `interval`, a
    positive `bound` and a non-empty `predicate`; an unbounded loop is the same stall wearing a
    loop's clothes, and a loop with no predicate never terminates into Ch8 point 4's fallback.
    """
    lines = text.splitlines()
    decl_lines = {n for n, line in enumerate(lines, start=1) if "<!-- WAIT:" in line}
    decls = [_parse_wait(m.group("body")) for m in _WAIT_DECL_RE.finditer(text)]
    intents = [(n, line) for n, line in _authored_lines(text) if _WAIT_INTENT_RE.search(line)]
    # PER-INTENTION, not per-document: each stated wait needs a declaration of its own within
    # `_WAIT_WINDOW` lines after it. A document-wide "is there any declaration?" test lets one
    # valid wait elsewhere in the file vouch for every intention in it.
    unmatched = [n for n, _ in intents
                 if not any(n < d <= n + _WAIT_WINDOW for d in decl_lines)]
    if unmatched:
        where = ", ".join(f"line {n}" for n in unmatched[:3])
        more = f" (+{len(unmatched) - 3} more)" if len(unmatched) > 3 else ""
        raise SeatRefusal(
            "sleeping-poll",
            f"{site}: {len(unmatched)} wait(s) stated as an INTENTION with no declaration "
            f"within {_WAIT_WINDOW} lines -- {where}{more}",
            remedy="write the wait as a loop and declare it beside the sentence that states it: "
                   "<!-- WAIT: interval=<n>s bound=<n> predicate=<state read from the file "
                   "surface> --> ; a turn that ends on an intention has no next tick",
        )
    for i, decl in enumerate(decls, start=1):
        for key in _WAIT_KEYS:
            if not decl.get(key):
                raise SeatRefusal(
                    "sleeping-poll",
                    f"{site}: WAIT declaration {i} carries no {key}",
                    remedy=f"a wait is an interval, a bound and a predicate; add {key}",
                )
        for key in ("interval", "bound"):
            if not _positive(decl[key]):
                raise SeatRefusal(
                    "sleeping-poll",
                    f"{site}: WAIT declaration {i} has {key}={decl[key]!r}",
                    remedy=f"{key} must be greater than zero; an unbounded or zero-interval "
                           "loop is the stall this refusal exists to prevent",
                )
    return len(decls)


# --- 2. the lane ceiling, checked at step 0 ----------------------------------------------------

def refuse_lane_ceiling(lanes: list[str], *, ceiling: int = LANE_CEILING,
                        already_provisioned: list[str] | None = None) -> list[str]:
    """The batch plan's lane list is within ADR-110's ceiling, and was checked BEFORE provisioning.

    Returns `lanes` unchanged when it passes. Three refusals:

    LATE: any worktree already provisioned means the coordination cost the ceiling exists to
    prevent has already been paid, every remaining option is a teardown, and the seventh lane
    gets run "since it is already provisioned" -- which is the exact reasoning the ceiling
    forbids. Ch8 says the placement is the whole mechanism, so the placement is checked.

    DUPLICATE: a plan naming a lane twice miscounts its own width, and the pairing rule is one
    lane = one contract = one branch, so a repeat is a defect regardless of the count.

    WIDTH: the excess lanes are named and handed BACK to the plan, never forward to a queue --
    they are the next batch's opening rows.
    """
    provisioned = list(already_provisioned or [])
    if provisioned:
        raise SeatRefusal(
            "lane-ceiling",
            f"the ceiling was checked LATE: {len(provisioned)} lane(s) already provisioned "
            f"({', '.join(provisioned[:6])})",
            remedy="run this at STEP 0, before the first worktree exists; run afterwards the "
                   "number is decorative and every remaining option is a teardown",
        )
    seen: set[str] = set()
    dupes = [name for name in lanes if name in seen or seen.add(name)]  # type: ignore[func-returns-value]
    if dupes:
        raise SeatRefusal(
            "lane-ceiling",
            f"the plan names {', '.join(sorted(set(dupes)))} more than once",
            remedy="one lane = one contract file = one worktree = one branch (ADR-110 per-lane "
                   "requirement 5); de-duplicate the list before counting it",
        )
    if len(lanes) > ceiling:
        excess = lanes[ceiling:]
        raise SeatRefusal(
            "lane-ceiling",
            f"the plan names {len(lanes)} lanes against a ceiling of {ceiling}; the excess is "
            f"{', '.join(excess)}",
            remedy="hand the excess back to the plan -> they are the next batch's opening rows; "
                   "the batch does not proceed until the plan is re-cut to "
                   f"<={ceiling} (the bound is integration capacity, which is serial)",
        )
    return lanes


# --- 6. the same-file collision, at dispatcher step 0 (`[#675]` target 3.4) -------------------

#: The section a lane's WRITES are specified in. Read from here and not from the whole file, and
#: that choice is MEASURED rather than stylistic -- see `declared_footprint`.
_DONE_CONTRACT_RE = re.compile(
    r"^##\s+Done-contract.*?$(?P<body>.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)

#: The repo's sanctioned TOP-LEVEL files, taken from the organ that already computes them
#: rather than retyped (`[#743]`). `validate_hermetization` derives this set from the shape
#: spec's `root_allowlist` clause unioned with the canonical living-doc registry, and it is the
#: set ADR-101 refuses a NEW root file against -- so it is the repo's one answer to "what may
#: sit at the root", and a root file admitted by a future ruling reaches this check for free.
#:
#: A CLOSED SET IS THE POINT, not an implementation detail. `[#743]` says so in its own words:
#: *"a bare `*.md` admission that lets `LANE-x-000-other.md` through is a regression, not a
#: fix"*. The transport's contract filenames, the absolute operator paths and the prose nouns
#: the `_WRITE_ROOTS` comment exists to exclude are all root-shaped, and only an enumeration
#: tells them apart from `ARCHITECTURE.md`.
ROOT_LEVEL_FILES: frozenset[str] = frozenset(_herm.SANCTIONED_TIER1_FILES)

#: Longest-first so `.pre-commit-config.yaml` cannot be shadowed by a shorter prefix, and the
#: trailing guard excludes only name characters -- NOT `.` -- so `ARCHITECTURE.md.` at the end
#: of a sentence still matches while `README.mdx` does not.
_ROOT_FILE_ALTERNATION = "|".join(
    re.escape(name) for name in sorted(ROOT_LEVEL_FILES, key=len, reverse=True))

#: A repo-relative path. The FIRST branch is the shape `file_purpose_graph._REL_PATH_RE` uses,
#: deliberately: two organs disagreeing about what counts as a path is a class of defect this
#: repo already carries. The SECOND branch is `[#743]`'s fix -- a root-level file has no `/`,
#: so the directory-requiring shape could not see `ARCHITECTURE.md` at all, and two lanes
#: declaring one could both pass step 0. Directory form is tried first so a full path is never
#: split at its basename.
_CONTRACT_PATH_RE = re.compile(
    r"(?:^|[\s`'\"(\[])("
    r"(?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6}"
    rf"|(?:{_ROOT_FILE_ALTERNATION})(?![A-Za-z0-9_-])"
    r")")

#: Prefixes a lane can actually WRITE to. A contract cites the transport (`LANE-x-000-other.md`),
#: absolute operator paths and prose nouns; none of those is a repo file two lanes can collide on.
_WRITE_ROOTS: tuple[str, ...] = (
    "scripts/", "tests/", "tasks/", "protocols/", "docs/", ".claude/", ".github/",
    "ecosystem/", "templates/", "deploy/", "logs/",
)


def _is_declarable(path: str) -> bool:
    """A path two lanes can genuinely collide on: under a write root, or AT the root.

    The root leg is membership in a closed set, never a prefix or a glob -- see
    `ROOT_LEVEL_FILES`. `str.startswith` cannot express "at the root" without also admitting
    every sibling basename on the operator's disk.
    """
    return path.startswith(_WRITE_ROOTS) or path in ROOT_LEVEL_FILES


def declared_footprint(contract_text: str) -> set[str]:
    """The repo paths a contract's Done-contract section declares it will write.

    READ FROM THE DONE-CONTRACT, NOT THE WHOLE FILE, and the choice was measured on the live
    batch-X set (13 contracts, 2026-09-12) rather than reasoned about:

        Done-contract extraction -> 1 colliding pair in 78, and NO path cited by 3+ contracts
        whole-file extraction    -> every lane shares references (ADRs, PLAYBOOK, the organs it
                                    reasons about), so a collision means nothing

    That difference is the whole viability of the check. A refusal that fires on shared
    REFERENCES would be turned off inside a window, and this module's own contract says a
    refusal that overstates its reach is worse than none.

    ROOT-LEVEL FILES COUNT TOO, since `[#743]` (2026-09-13). Before that both legs of the
    extraction required a `/` -- the regex matched only `dir/.../file.ext` and `_WRITE_ROOTS`
    was a tuple of directory prefixes -- so `ARCHITECTURE.md`, `.pre-commit-config.yaml` and
    `pyproject.toml` were invisible and two lanes could each declare one and both pass step 0.
    THAT WAS LIVE IN THE BATCH THAT FIXED IT: wave 4's own step-0 run reported "no file claimed
    twice" while one lane declared `ARCHITECTURE.md` and another `.pre-commit-config.yaml`.
    They happened not to collide with each other, so the PASS was correct by luck.

    HONEST LIMIT, and it is the row's own: a contract declares what it INTENDS to touch. A lane
    that writes outside its declaration is invisible here -- which is why the contract separately
    forbids exactly that ("No edits outside this lane's declared footprint"). This checks
    declared collisions, and says so rather than implying it checked the trees.

    SECOND HONEST LIMIT, and it is the root admission's own, measured over all 57 contracts on
    the transport on 2026-09-13: a filename QUOTED inside the Done-contract reads as declared,
    because this function cannot tell a write clause from a quotation and does not guess. One
    contract in 57 tripped it -- the one carrying `[#743]`'s row body verbatim into its
    Done-contract, where the row enumerates root filenames as examples. Excluding it, the
    widening produced ZERO in-batch false collisions. The sanctioned shape is the one the
    Done-contract-vs-whole-file measurement already implies: carry quoted row bodies in their
    own section, not in the Done-contract. Pinned by
    `test_a_row_body_QUOTED_INSIDE_the_done_contract_reads_as_a_declaration`.
    """
    match = _DONE_CONTRACT_RE.search(contract_text)
    if match is None:
        return set()
    return {path for path in _CONTRACT_PATH_RE.findall(match.group("body"))
            if _is_declarable(path)}


def undeclared_lanes(footprints: dict[str, set[str]]) -> list[str]:
    """Lanes whose contract declared NO repo path -- reported, never counted as clean.

    NEVER GREEN-BY-SKIP (the 2026-08-25 tiered-machine-dependence sweep, applied to a different
    absence): a lane this check could not see and a lane that genuinely collides with nothing
    both produce no finding, and reporting one word for both is how a check comes to pass
    because it cannot see its own case -- which is the row this refusal is filed under.
    """
    return sorted(lane for lane, paths in footprints.items() if not paths)


def refuse_file_collision(contracts: dict[str, str], *,
                          already_provisioned: list[str] | None = None
                          ) -> dict[str, set[str]]:
    """No two lanes in this batch declare writes to the same file. Dispatcher STEP 0.

    `contracts` maps lane name -> contract TEXT. Returns `{lane: footprint}` when it passes, so
    the caller can report what it saw rather than only that nothing fired.

    LATE IS ITSELF A REFUSAL, in the row's own words: run after provisioning, "the collision it
    exists to prevent has already been paid for and every remaining option is a teardown". Two
    lanes editing one file hand back either a merge conflict the integrator resolves serially or
    -- worse -- two trees that each regenerated the same derived surface against the other's
    absence. Neither is recoverable more cheaply than tearing a lane down, so the check that runs
    late is decorative and the placement is the mechanism.

    EVERY COLLIDING LANE IS NAMED, not the first pair. A refusal that stops at the first pair
    sends the dispatcher back for a second round trip, and a second round of step 0 is exactly
    the cost step 0 exists to avoid paying twice.

    WHAT `contracts` MUST BE, and this is load-bearing rather than a usage note. It is the
    batch's contract set as the MANIFEST declares it -- NOT a directory listing of the
    transport. MEASURED 2026-09-12: globbing `LANE-x-*.md` off the live transport yields 13
    contracts and one collision, on `deploy/manifest-v1.5.0.yaml` between
    `LANE-x-734-retire-stage` and `LANE-x-734-retire-stage-2` -- and only the SECOND is
    provisioned. The first is a superseded re-cut still sitting on the transport, so the
    collision is real in the directory and absent from the batch. A glob makes this refusal
    report a false collision on every superseded contract the transport has accumulated.

    That is deliberately NOT re-solved here: `batch_manifest.freeze_manifest_contract_agreement`
    (`[#630]`) already refuses when the manifest's lane slugs and the contract set disagree, and
    it is the organ that owns the question. Run it first; this one assumes its answer. Two
    organs computing "is this the right contract set" privately is the defect class this repo
    keeps filing, so the dependency is stated rather than duplicated.
    """
    provisioned = list(already_provisioned or [])
    if provisioned:
        raise SeatRefusal(
            "file-collision",
            f"the collision check was checked LATE: {len(provisioned)} lane(s) already "
            f"provisioned ({', '.join(provisioned[:6])})",
            remedy="run this at STEP 0, on the frozen contract set, before the first worktree "
                   "exists; run afterwards the collision has already been paid for and every "
                   "remaining option is a teardown",
        )

    footprints = {lane: declared_footprint(text) for lane, text in contracts.items()}

    claimants: dict[str, list[str]] = {}
    for lane in sorted(footprints):
        for path in footprints[lane]:
            claimants.setdefault(path, []).append(lane)
    collisions = {path: lanes for path, lanes in claimants.items() if len(lanes) > 1}

    if collisions:
        detail = "; ".join(
            f"{path} <- {', '.join(lanes)}" for path, lanes in sorted(collisions.items()))
        raise SeatRefusal(
            "file-collision",
            f"{len(collisions)} file(s) are declared by more than one lane: {detail}",
            remedy="re-cut the contracts so one file has one owning lane, or SEQUENCE the "
                   "colliding lanes into different batches -- the second is the honest option "
                   "when the work genuinely shares a surface, and it costs one batch rather "
                   "than one teardown",
        )
    return footprints


# --- 7. the merge the plan half did not rule ---------------------------------------------------
#
# THE ONE REFUSAL ADDRESSED TO A SEAT'S CHEAPER HALF, and its whole argument is in that sentence.
# Lane `aa-2` routes the integrator's mechanical walk to Sonnet and its judgment to Opus, with the
# seam a FILE: the plan half writes `MERGE-PLAN-<batch>.md`, the execute half boots from it. The
# instruction that seam rests on -- *escalate anything the plan does not rule* -- is, as prose, a
# JUDGMENT CALL, handed to the half chosen because it is not doing judgment. That is the exact
# failure the lane's contract names: *"a split that silently lets the cheap half make expensive
# decisions is worse than no split -- it buys a lower cost line by moving judgment somewhere that
# cannot exercise it."*
#
# So authority is GRANTED PER ENTRY and checked by a predicate, not interpreted. Nothing about the
# answer depends on which model reads it, which is the property that makes the cheap half safe to
# be cheap.
#
# THE GRAMMAR IS DELIBERATELY NARROW. One list item per branch:
#
#     - `worktree-lane-aa-1` -> MERGE · INDEPENDENT
#     - `worktree-lane-aa-2` -> MERGE · SERIAL, after aa-1
#     - `worktree-lane-aa-3` -> HOLD · the suite baseline moved; operator asked
#
# A looser grammar would let a plan that MENTIONS a branch read as one that authorises it, and
# mentions are what a plan is full of.

#: A plan entry. The branch is backticked so a prose sentence naming a branch is not an entry:
#: the plan's discussion of a merge and its ruling on one must not be the same shape.
_PLAN_ENTRY_RE = re.compile(
    r"^[-*]\s+`(?P<branch>[^`\n]+)`\s*(?:->|--|→)\s*(?P<verdict>[A-Z]+)\b(?P<rest>[^\n]*)$",
    re.MULTILINE)

#: The only verdict that authorises a merge. Everything else -- including a verdict this module
#: has never heard of -- is an escalation: an unknown word in the authorising position is exactly
#: where a reader must not guess generously.
_MERGE_VERDICT = "MERGE"

#: A merge the plan marked as not depending on any other. The execute half may continue with these
#: after escalating a different one; without the marker it may not, because "these two are
#: independent" is a claim about the diffs and is therefore plan-half work.
_INDEPENDENT_MARKER = "INDEPENDENT"


@dataclass(frozen=True)
class PlanEntry:
    """One branch's ruling, as the plan half wrote it."""

    branch: str
    verdict: str
    detail: str
    independent: bool

    @property
    def mergeable(self) -> bool:
        return self.verdict == _MERGE_VERDICT


def plan_entries(plan_text: str) -> list[PlanEntry]:
    """Every ruling in a merge plan, IN THE PLAN'S OWN ORDER.

    The order is itself a ruling, and most of what the plan half was paid to produce. A queue the
    execute half re-derived would be the cheap half re-deciding the one thing the expensive half
    was there for.
    """
    out: list[PlanEntry] = []
    for match in _PLAN_ENTRY_RE.finditer(plan_text):
        rest = match.group("rest")
        out.append(PlanEntry(
            branch=match.group("branch").strip(),
            verdict=match.group("verdict").strip(),
            detail=rest.strip(" \t·-"),
            independent=_INDEPENDENT_MARKER in rest.upper(),
        ))
    return out


def ruled_merges(plan_text: str, *, include_unmergeable: bool = False) -> list[PlanEntry]:
    """The queue the execute half walks, in the plan's order.

    `include_unmergeable` is for REPORTING -- a seat saying what it did not do, which the
    refuse-to-finish checklist asks for. It is not a way to walk the held ones.
    """
    entries = plan_entries(plan_text)
    return entries if include_unmergeable else [e for e in entries if e.mergeable]


def refuse_unruled_merge(plan_text: str, *, branch: str) -> PlanEntry:
    """MAY THE EXECUTE HALF MERGE `branch`? The plan's entry, or a refusal naming the escalation.

    Four ways to answer no, and each is a different remedy, so each says which:

      * **No entries at all.** An empty plan and a plan that authorises everything are the same
        document to a reader that only asks whether a branch is forbidden. The question runs the
        other way: authority is granted per entry, so no entries is no authority.
      * **This branch is not in it.** The ordinary escalation, and the common one.
      * **Ruled, and not MERGE.** A HOLD is a ruling, and obeying it is the same act as escalating
        an unruled branch -- in neither case does the execute half decide. What it must never do
        is read *the plan mentions this branch* as *the plan authorises this merge*.
      * **Ruled twice, inconsistently.** Taking the first hit lets a superseded ruling authorise a
        merge; taking the last lets a stale append do it. Neither is the execute half's call, so
        an ambiguous plan is an escalation -- the posture `seat_ch8.extract` already takes on an
        ambiguous anchor, for the same reason.
    """
    entries = plan_entries(plan_text)
    if not entries:
        raise SeatRefusal(
            "unruled-merge",
            f"the merge plan carries NO plan entries, so it authorises nothing -- {branch!r} "
            f"included. Authority is granted PER ENTRY (``- `<branch>` -> MERGE``), never by a "
            f"plan's silence",
            remedy="ESCALATE: ask the plan half to rule the queue before you merge anything")
    matched = [e for e in entries if e.branch == branch]
    if not matched:
        raise SeatRefusal(
            "unruled-merge",
            f"the merge plan does not rule {branch!r}; it rules "
            f"{', '.join(repr(e.branch) for e in entries)}",
            remedy=("ESCALATE: append the branch, the reason you reached it and your question "
                    "to the escalation file, then STOP this merge and continue only with "
                    f"entries the plan marked {_INDEPENDENT_MARKER}. Do NOT decide this one"))
    verdicts = {e.verdict for e in matched}
    if len(verdicts) > 1:
        raise SeatRefusal(
            "unruled-merge",
            f"the merge plan rules {branch!r} twice and the rulings disagree "
            f"({', '.join(sorted(verdicts))}) -- an AMBIGUOUS plan",
            remedy=("ESCALATE: ask the plan half which ruling stands. Taking the first would "
                    "let a superseded ruling authorise a merge and taking the last would let a "
                    "stale append do it; neither is yours to pick"))
    entry = matched[0]
    if not entry.mergeable:
        raise SeatRefusal(
            "unruled-merge",
            f"the merge plan rules {branch!r} {entry.verdict}, not {_MERGE_VERDICT}"
            + (f" -- {entry.detail}" if entry.detail else ""),
            remedy=("obey the ruling; do not re-open it. A ruling against a merge is still a "
                    "ruling. ESCALATE only if you hold a fact the ruling was made without"))
    return entry


# --- 3. the reviewer's model id in the tally ---------------------------------------------------

_TALLY_RE = re.compile(
    r"Tally:\s*review=(?P<review>\S+)"
    r"(?:\s+reviewer=(?P<reviewer>\S+))?"
    r"\s+findings=(?P<findings>\d+)\s+fixed=(?P<fixed>\d+)"
)


@dataclass(frozen=True)
class Tally:
    """A parsed review tally line."""

    review: str
    reviewer: str
    findings: int
    fixed: int


def refuse_tally_reviewer(line: str, *, contracted_reviewer: str) -> Tally:
    """The tally names the reviewer that ACTUALLY ran, exactly, or it reports `review=NONE`.

    A review by an unrequested model is not a weaker review of the requested kind -- it is a
    different measurement wearing the requested one's label, and a tally that counts it hides the
    substitution while also consuming the slot the real review would have occupied. `NONE` is the
    honest report and is always preferred to a laundered one. `SELF` is honest too, and still
    carries the seat's own model id.

    The comparison is EXACT: `gpt-5.6` where `gpt-5.6-terra` was contracted is a mismatch, not a
    near miss -- the two scars behind this rule are both silent substitutions inside a family.
    """
    m = _TALLY_RE.search(line)
    if m is None:
        raise SeatRefusal(
            "tally-malformed",
            f"the tally line does not parse: {line.strip()!r}",
            remedy="the shape is `Tally: review=<lane|NONE|SELF> reviewer=<exact model id> "
                   "findings=<n> fixed=<n>`",
        )
    reviewer = m.group("reviewer")
    if not reviewer:
        raise SeatRefusal(
            "reviewer-absent",
            "the tally carries a verdict but no `reviewer=` field",
            remedy=f"state the EXACT model id that ran (contracted: {contracted_reviewer}); "
                   "a verdict with no identity cannot be checked against the dispatch line",
        )
    review = m.group("review")
    if reviewer != contracted_reviewer and review != "NONE":
        raise SeatRefusal(
            "reviewer-mismatch",
            f"the contract named {contracted_reviewer} and {reviewer} ran, but the tally reports "
            f"review={review}",
            remedy="report `review=NONE`. Not a downgraded finding count, not a note in the "
                   "body: NONE -- a substituted reviewer is a different measurement wearing the "
                   "requested one's label",
        )
    return Tally(review=review, reviewer=reviewer,
                 findings=int(m.group("findings")), fixed=int(m.group("fixed")))


# --- 4. carried-by: on DECLARE- / AMEND- / BATCH- writes ---------------------------------------

#: The three transport prefixes P11 governs (OPERATOR-INTERFACE §1 filename grammar).
DECISION_PREFIXES: tuple[str, ...] = ("DECLARE-", "AMEND-", "BATCH-")
#: The HEAD window the probe reads. Six lines, matching the probe's own `head -6`.
CARRIER_HEAD_LINES = 6
_CARRIER_RE = re.compile(r"^carried-by:(?P<value>.*)$")
#: A value resolves as a path (`a/b`) or states the literal OPEN. Nothing else is a carrier.
_PATH_TOKEN_RE = re.compile(r"[\w.\-]+/[\w./\-]+")
#: `OPEN` as a STANDALONE token, alone or followed by a reason. A `startswith("OPEN")` test also
#: admits `OPENING` and `OPEN-not-a-carrier`, which are not the literal the probe accepts and
#: would transport as though they resolved (terra HIGH, 2026-09-09).
_OPEN_RE = re.compile(r"^OPEN(?:\s|$)")


def is_decision_file(filename: str) -> bool:
    """True when this basename is one of the three transport decision shapes."""
    return Path(filename).name.startswith(DECISION_PREFIXES)


def refuse_uncarried_decision_write(filename: str, text: str) -> bool:
    """A decision file states its carrier. Returns True when governed and carried, False when
    the filename is outside the three prefixes.

    Anchored and valued, both legs, because a bare substring match is a different and broken
    check (HANDOFF_PROCESS §5): the `carried-by:` must be FLUSH-LEFT and inside the head window,
    and its value must be a repo path or the literal `OPEN`. An indented line, a line further
    down the body, and a value that is a sentence rather than a locator all pass a substring
    grep and all fail the probe the moment the bundle is verified.

    Whether a path value resolves on `main` is deliberately NOT asked here -- that is the
    read-time leg, and at write time the carrier has often not landed yet.
    """
    if not is_decision_file(filename):
        return False
    head = text.splitlines()[:CARRIER_HEAD_LINES]
    match = next((m for m in (_CARRIER_RE.match(line) for line in head) if m), None)
    if match is None:
        raise SeatRefusal(
            "carried-by-absent",
            f"{Path(filename).name}: no flush-left `carried-by:` in the first "
            f"{CARRIER_HEAD_LINES} lines",
            remedy="add `carried-by: <repo path>` flush-left in the file head, or "
                   "`carried-by: OPEN -- <reason>` and name the OPEN in the bundle residual",
        )
    value = match.group("value").strip()
    if not value:
        raise SeatRefusal(
            "carried-by-empty",
            f"{Path(filename).name}: `carried-by:` carries no value",
            remedy="a key with no value is not a carrier; state a repo path or the literal OPEN",
        )
    if not _OPEN_RE.match(value) and not _PATH_TOKEN_RE.search(value):
        raise SeatRefusal(
            "carried-by-unresolvable",
            f"{Path(filename).name}: `carried-by: {value}` names neither a repo path nor OPEN",
            remedy="a decision's carrier is a FILE that will hold it -- prose is not a locator",
        )
    return True


def write_decision_file(path: str | Path, text: str, *, encoding: str = "utf-8") -> Path:
    """Write a transport decision file, refusing FIRST.

    The order is the whole point: a check that writes and then complains has refused nothing, and
    the file is already on the transport where the next seat will read it.
    """
    target = Path(path)
    refuse_uncarried_decision_write(target.name, text)
    target.write_text(text, encoding=encoding, newline="\n")
    return target


# --- 5. -DryRun is the LAST line of dispatcher step 0 (AMEND-BATCH-V-002 §1) -------------------

_DRYRUN_TOKEN = "-DryRun"
#: A markdown heading naming step 0, at any depth and with any decoration around it.
_STEP0_HEADING_RE = re.compile(r"^#{1,6}\s.*\bstep\s*0\b", re.IGNORECASE)
_ANY_HEADING_RE = re.compile(r"^#{1,6}\s")


def isolate_step0(text: str) -> str:
    """The step-0 SECTION of `text`, or the whole text when no step-0 heading is present.

    The rendered dispatcher boot tells the seat to check `<this file>`, and that file continues
    for several sections past step 0. Without this, a correct step 0 FAILS because a later
    section's last line is not a DryRun -- and, worse in the other direction, a DryRun appearing
    anywhere later would MASK a step 0 that carries none (terra HIGH, 2026-09-09). The isolation
    is what makes "the LAST line of step 0" mean step 0's last line.
    """
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if _STEP0_HEADING_RE.match(ln)), None)
    if start is None:
        return text
    end = next((i for i in range(start + 1, len(lines)) if _ANY_HEADING_RE.match(lines[i])),
               len(lines))
    return "\n".join(lines[start:end])


def refuse_dispatcher_step0_without_dryrun(step0_text: str, *, contracts: list[str]) -> int:
    """Step 0 ends by DryRunning every generated contract. Returns the count DryRun'd.

    Batch V discovered a generator/verb defect by running the DryRun, after freezing six
    contracts the live verb refused. A dispatcher that skips it launches into a refusal, having
    already spent the freeze. Three legs: the DryRun is PRESENT, it is LAST (a step that
    continues past it has moved the check off the boundary it guards), and it covers EVERY
    generated contract -- one unchecked contract is the one that fails at dispatch.
    """
    if not contracts:
        raise SeatRefusal(
            "dryrun-no-contracts",
            "step 0 was asked to DryRun an empty contract set",
            remedy="a batch with no generated contract has no plan to freeze; name the contracts",
        )
    lines = isolate_step0(step0_text).splitlines()
    dryrun_lines = [line for line in lines if _DRYRUN_TOKEN in line]
    if not dryrun_lines:
        raise SeatRefusal(
            "dryrun-absent",
            f"step 0 carries no `{_DRYRUN_TOKEN}` line",
            remedy="make the DryRun of every generated contract the LAST line of step 0 "
                   "(AMEND-BATCH-V-002 §1); it refuses rather than warns",
        )
    tail = [line for line in lines if line.strip() and not _FENCE.match(line)]
    if not tail or _DRYRUN_TOKEN not in tail[-1]:
        last = tail[-1].strip() if tail else "<empty>"
        raise SeatRefusal(
            "dryrun-not-last",
            f"step 0 continues past its DryRun; its last line is {last!r}",
            remedy="the DryRun is the LAST LINE of step 0 -- a step that continues past it has "
                   "moved the check off the boundary it guards",
        )
    blob = "\n".join(dryrun_lines)
    missing = [c for c in contracts if c not in blob]
    if missing:
        raise SeatRefusal(
            "dryrun-incomplete",
            f"step 0 DryRuns {len(contracts) - len(missing)} of {len(contracts)} contracts; "
            f"missing: {', '.join(missing)}",
            remedy="DryRun EVERY generated contract -- the one left out is the one that fails "
                   "at dispatch",
        )
    return len(contracts)


# --- 8/9. no-live-integrator and lane-owned: seat STATE, at step 0 (`[#833]`) --------------------
#
# Both read `seat_registry.seats()` -- a list of seats whose `state` was derived from hook-event
# timestamps, never asserted. They take the list rather than importing the registry, so this module
# stays importable by the registry itself (which raises `SeatRefusal`) without a cycle, and so a
# test hands them a registry built in `tmp_path`.

def refuse_no_live_integrator(batch: str, seats: list) -> object:
    """A lane may enter `batch` only while a `live` integrator seat is bound to it.

    Returns that seat (the most recently active, if several). A wedged, starved or absent integrator
    does NOT count and is NAMED in the refusal with its state: a handback addressed to a seat that
    stopped receiving is the same loss as one addressed to nobody, only slower to find.
    """
    wanted = str(batch).upper()
    bound = [s for s in seats if s.role == "integrator" and str(s.batch or "").upper() == wanted]
    live = [s for s in bound if s.state == "live"]
    if live:
        return max(live, key=lambda s: s.last_event)
    seen = "; ".join(f"{s.session_id[:8]} reads {s.state}" for s in bound) or "none registered"
    raise SeatRefusal(
        "no-live-integrator",
        f"batch {wanted} has no live integrator seat ({seen}) -- a lane dispatched now hands back "
        "to nobody",
        remedy=f"boot the integrator for batch {wanted} and, from ITS OWN session, run "
               f"`uv run --locked python scripts/seat_registry.py bind --role integrator --batch "
               f"{wanted}`; then dispatch. A dispatcher or lane never binds a role it does not hold",
    )


def refuse_lane_owned(lane: str, seats: list, *, own_session: str) -> None:
    """A second session may not boot onto a lane whose owner is `live`.

    Only `live` refuses. A wedged or absent owner is exactly the case where a relaunch IS the
    remedy -- lane ab-833's first boot sat 12 h 43 min at a SessionStart hook before its relaunch --
    and refusing that would trade one lost lane for a lane nobody may restart. The caller's own
    session never refuses itself.
    """
    owners = [s for s in seats
              if s.lane == lane and s.session_id != own_session and s.state == "live"]
    if not owners:
        return
    owner = max(owners, key=lambda s: s.last_event)
    raise SeatRefusal(
        "lane-owned",
        f"{lane} already has a live owner: session {owner.session_id} "
        f"({owner.minutes_since:.0f} min since its last event)",
        remedy="do not start a second session here -- two committing sessions share one index. "
               "Message the owner instead; if it is truly gone it reads wedged or absent within "
               "the registry's threshold and this refusal lifts on its own",
    )


# --- the CLI -- so a seat template carries a RUNNABLE refusal, not a reminder ------------------
#
# A seat boot that says "remember the ceiling" has said nothing this repo has not already said in
# prose and then watched be broken. So every refusal above is reachable as one command line, and
# the rendered boot carries the LINE rather than the sentiment. Exit 1 on a refusal, 0 on a pass;
# the refusal message goes to stderr, so a caller piping stdout still sees why it stopped.


def _fail(exc: SeatRefusal) -> None:
    click.echo(str(exc), err=True)
    raise SystemExit(1)


def _live_worktrees(repo_root: Path) -> list[str]:
    """The lane worktrees this repo currently has, READ from git rather than assumed.

    `--check-worktrees` exists because the late-check refusal is only as good as its input: a
    dispatcher asked to self-report what it has already provisioned is being asked the question
    the refusal exists to stop it answering for itself.
    """
    try:
        out = subprocess.run(["git", "-C", str(repo_root), "worktree", "list", "--porcelain"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    trees = [line.split(" ", 1)[1].strip() for line in out.splitlines()
             if line.startswith("worktree ")]
    return [t for t in trees if ".claude/worktrees" in t.replace("\\", "/")]


@click.group(help="The five seat refusals, as commands. Exit 1 = REFUSED.")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("list")
def cmd_list() -> None:
    """Print the refusal roster."""
    for name in REFUSALS:
        click.echo(name)


@cli.command("sleeping-poll")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True, dir_okay=False))
def cmd_sleeping_poll(files: tuple[str, ...]) -> None:
    """Every wait in FILES is written as code, not as an intention."""
    total = 0
    for path in files:
        try:
            total += refuse_sleeping_poll(Path(path).read_text(encoding="utf-8"), site=path)
        except SeatRefusal as exc:
            _fail(exc)
    click.echo(f"sleeping-poll: PASS -- {len(files)} file(s), {total} declared wait(s)")


@cli.command("lane-ceiling")
@click.option("--lane", "lanes", multiple=True, required=True, help="one lane slug; repeatable")
@click.option("--provisioned", multiple=True, help="a worktree that already exists")
@click.option("--check-worktrees", is_flag=True,
              help="read the live worktree list instead of trusting --provisioned")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
def cmd_lane_ceiling(lanes: tuple[str, ...], provisioned: tuple[str, ...],
                     check_worktrees: bool, repo_root: str | None) -> None:
    """STEP 0 ONLY: the batch plan is within ADR-110's lane ceiling."""
    already = list(provisioned)
    if check_worktrees:
        already += _live_worktrees(Path(repo_root) if repo_root else _SCRIPTS.parent)
    try:
        accepted = refuse_lane_ceiling(list(lanes), already_provisioned=already)
    except SeatRefusal as exc:
        _fail(exc)
    click.echo(f"lane-ceiling: PASS -- {len(accepted)} lane(s) <= {LANE_CEILING}, "
               "checked before any worktree exists")


@cli.command("file-collision")
@click.option("--contract", "contracts", multiple=True, required=True,
              type=click.Path(exists=True, dir_okay=False),
              help="a FROZEN contract file; repeatable. Pass the batch's set AS THE MANIFEST "
                   "DECLARES IT, never a glob of the transport -- a superseded re-cut still "
                   "sitting there collides with its own replacement (measured 2026-09-12). "
                   "`batch_manifest.freeze_manifest_contract_agreement` ([#630]) is the organ "
                   "that refuses a wrong set; run it first")
@click.option("--provisioned", multiple=True, help="a worktree that already exists")
@click.option("--check-worktrees", is_flag=True,
              help="read the live worktree list instead of trusting --provisioned")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False))
def cmd_file_collision(contracts: tuple[str, ...], provisioned: tuple[str, ...],
                       check_worktrees: bool, repo_root: str | None) -> None:
    """STEP 0 ONLY: no two lanes in this batch declare writes to the same file."""
    already = list(provisioned)
    if check_worktrees:
        already += _live_worktrees(Path(repo_root) if repo_root else _SCRIPTS.parent)
    texts = {Path(path).stem: Path(path).read_text(encoding="utf-8", errors="replace")
             for path in contracts}
    try:
        footprints = refuse_file_collision(texts, already_provisioned=already)
    except SeatRefusal as exc:
        _fail(exc)
    declared = sum(len(paths) for paths in footprints.values())
    click.echo(f"file-collision: PASS -- {len(footprints)} contract(s), {declared} declared "
               "path(s), no file claimed twice; checked before any worktree exists")
    # NEVER GREEN-BY-SKIP: a lane this check could not see is named, because "no collision" and
    # "I could not read this lane" must not print the same word.
    blind = undeclared_lanes(footprints)
    if blind:
        click.echo(f"file-collision: {len(blind)} contract(s) declared NO repo path and were "
                   f"invisible to this check: {', '.join(blind)}")


@cli.command("unruled-merge")
@click.option("--plan", required=True, type=click.Path(exists=True, dir_okay=False),
              help="the merge plan the PLAN half wrote")
@click.option("--branch", required=True, help="the branch you are about to merge")
def cmd_unruled_merge(plan: str, branch: str) -> None:
    """The plan half RULED this merge -- run it immediately before each `git merge --no-ff`."""
    text = Path(plan).read_text(encoding="utf-8")
    try:
        entry = refuse_unruled_merge(text, branch=branch)
    except SeatRefusal as exc:
        _fail(exc)
    queue = ruled_merges(text)
    held = [e for e in ruled_merges(text, include_unmergeable=True) if not e.mergeable]
    click.echo(f"unruled-merge: PASS -- {entry.branch} ruled {entry.verdict}"
               f"{' INDEPENDENT' if entry.independent else ''}"
               f"{(' -- ' + entry.detail) if entry.detail else ''}")
    # THE QUEUE AND THE HELD SET, both printed, because the refuse-to-finish checklist asks a
    # seat what it did NOT do and a seat that never saw the held entries cannot answer.
    click.echo(f"unruled-merge: queue ({len(queue)}): "
               + ", ".join(e.branch for e in queue))
    if held:
        click.echo(f"unruled-merge: NOT mergeable ({len(held)}): "
                   + ", ".join(f"{e.branch}={e.verdict}" for e in held))


@cli.command("reviewer")
@click.option("--contracted", required=True, help="the exact model id the contract named")
@click.argument("artifact", type=click.Path(exists=True, dir_okay=False))
def cmd_reviewer(contracted: str, artifact: str) -> None:
    """The `Tally:` line in ARTIFACT names the reviewer that actually ran."""
    text = Path(artifact).read_text(encoding="utf-8")
    line = next((ln for ln in text.splitlines() if "Tally:" in ln), "")
    try:
        tally = refuse_tally_reviewer(line, contracted_reviewer=contracted)
    except SeatRefusal as exc:
        _fail(exc)
    click.echo(f"reviewer: PASS -- review={tally.review} reviewer={tally.reviewer}")


@cli.command("carried-by")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True, dir_okay=False))
def cmd_carried_by(files: tuple[str, ...]) -> None:
    """Every DECLARE-/AMEND-/BATCH- file among FILES states its carrier."""
    governed = 0
    for path in files:
        try:
            governed += bool(refuse_uncarried_decision_write(
                path, Path(path).read_text(encoding="utf-8")))
        except SeatRefusal as exc:
            _fail(exc)
    click.echo(f"carried-by: PASS -- {governed} of {len(files)} file(s) governed and carried")


@cli.command("dryrun-step0")
@click.option("--step0", required=True, type=click.Path(exists=True, dir_okay=False),
              help="the file carrying the dispatcher's step 0")
@click.option("--contract", "contracts", multiple=True, required=True,
              help="one generated contract filename; repeatable")
def cmd_dryrun_step0(step0: str, contracts: tuple[str, ...]) -> None:
    """Step 0 ends by DryRunning every generated contract (AMEND-BATCH-V-002 s1)."""
    try:
        count = refuse_dispatcher_step0_without_dryrun(
            Path(step0).read_text(encoding="utf-8"), contracts=list(contracts))
    except SeatRefusal as exc:
        _fail(exc)
    click.echo(f"dryrun-step0: PASS -- {count} contract(s) DryRun on the last line of step 0")


def _seat_registry():
    """Lazy: the registry imports this module, so this module imports it only when a verb runs."""
    try:
        import seat_registry  # noqa: PLC0415
    except ImportError:                                      # imported as `scripts.seat_refusals`
        from scripts import seat_registry  # type: ignore[no-redef]  # noqa: PLC0415
    return seat_registry


@cli.command("no-live-integrator")
@click.option("--batch", required=True, help="the batch token, e.g. AB")
def cmd_no_live_integrator(batch: str) -> None:
    """STEP 0: the batch has a LIVE integrator seat to receive its lanes ([#833])."""
    try:
        seat = refuse_no_live_integrator(batch, _seat_registry().seats())
    except SeatRefusal as exc:
        _fail(exc)
    click.echo(f"no-live-integrator: PASS -- batch {batch.upper()} is received by integrator "
               f"{seat.session_id} ({seat.minutes_since:.0f} min since its last event)")


@cli.command("lane-owned")
@click.option("--lane", required=True, help="the lane worktree name")
def cmd_lane_owned(lane: str) -> None:
    """STEP 0 of a lane: no OTHER live session owns this lane ([#833])."""
    own = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    try:
        refuse_lane_owned(lane, _seat_registry().seats(), own_session=own)
    except SeatRefusal as exc:
        _fail(exc)
    click.echo(f"lane-owned: PASS -- no other live session holds {lane}")


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
