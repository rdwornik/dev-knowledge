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

#: The refusal ids, in the order the lane contract enumerates them (four contracted plus the
#: fifth added by AMEND-BATCH-V-002 §1). A seat template cites these ids; tests assert the roster.
REFUSALS: tuple[str, ...] = (
    "sleeping-poll", "lane-ceiling", "reviewer-mismatch", "carried-by", "dryrun-step0",
    # SIXTH, added by `[#675]` target 3.4. It joins the STEP-0 family rather than standing
    # alone, because its whole argument is the one `lane-ceiling` already makes: a collision
    # found after provisioning has already been paid for.
    "file-collision",
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
    "dispatcher": ("lane-ceiling", "file-collision", "carried-by", "sleeping-poll",
                   "dryrun-step0"),
    "integrator": ("reviewer-mismatch", "carried-by", "sleeping-poll"),
    "filings": ("carried-by", "sleeping-poll"),
    "handoff": ("carried-by", "sleeping-poll"),
    "lane": ("reviewer-mismatch", "sleeping-poll"),
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

def refuse_lane_ceiling(lanes: "list[str]", *, ceiling: int = LANE_CEILING,
                        already_provisioned: "list[str] | None" = None) -> list[str]:
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

#: A repo-relative path. Same shape `file_purpose_graph._REL_PATH_RE` uses, deliberately: two
#: organs disagreeing about what counts as a path is a class of defect this repo already carries.
_CONTRACT_PATH_RE = re.compile(
    r"(?:^|[\s`'\"(\[])((?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6})")

#: Prefixes a lane can actually WRITE to. A contract cites the transport (`LANE-x-000-other.md`),
#: absolute operator paths and prose nouns; none of those is a repo file two lanes can collide on.
_WRITE_ROOTS: tuple[str, ...] = (
    "scripts/", "tests/", "tasks/", "protocols/", "docs/", ".claude/", ".github/",
    "ecosystem/", "templates/", "deploy/", "logs/",
)


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

    HONEST LIMIT, and it is the row's own: a contract declares what it INTENDS to touch. A lane
    that writes outside its declaration is invisible here -- which is why the contract separately
    forbids exactly that ("No edits outside this lane's declared footprint"). This checks
    declared collisions, and says so rather than implying it checked the trees.
    """
    match = _DONE_CONTRACT_RE.search(contract_text)
    if match is None:
        return set()
    return {path for path in _CONTRACT_PATH_RE.findall(match.group("body"))
            if path.startswith(_WRITE_ROOTS)}


def undeclared_lanes(footprints: "dict[str, set[str]]") -> list[str]:
    """Lanes whose contract declared NO repo path -- reported, never counted as clean.

    NEVER GREEN-BY-SKIP (the 2026-08-25 tiered-machine-dependence sweep, applied to a different
    absence): a lane this check could not see and a lane that genuinely collides with nothing
    both produce no finding, and reporting one word for both is how a check comes to pass
    because it cannot see its own case -- which is the row this refusal is filed under.
    """
    return sorted(lane for lane, paths in footprints.items() if not paths)


def refuse_file_collision(contracts: "dict[str, str]", *,
                          already_provisioned: "list[str] | None" = None
                          ) -> "dict[str, set[str]]":
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

    claimants: "dict[str, list[str]]" = {}
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


def write_decision_file(path: "str | Path", text: str, *, encoding: str = "utf-8") -> Path:
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


def refuse_dispatcher_step0_without_dryrun(step0_text: str, *, contracts: "list[str]") -> int:
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


# --- the CLI -- so a seat template carries a RUNNABLE refusal, not a reminder ------------------
#
# A seat boot that says "remember the ceiling" has said nothing this repo has not already said in
# prose and then watched be broken. So every refusal above is reachable as one command line, and
# the rendered boot carries the LINE rather than the sentiment. Exit 1 on a refusal, 0 on a pass;
# the refusal message goes to stderr, so a caller piping stdout still sees why it stopped.


def _fail(exc: SeatRefusal) -> "None":
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
                     check_worktrees: bool, repo_root: "str | None") -> None:
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
                       check_worktrees: bool, repo_root: "str | None") -> None:
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


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
