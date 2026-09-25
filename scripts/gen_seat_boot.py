"""gen_seat_boot.py -- render the five SEAT-BOOT pastes from PLAYBOOK Ch8, at bundle-cut time.

WHY THIS IS GENERATED AND NEVER COMPOSED. Two consecutive browser seats did not know how a
dispatcher / integrator / filings / handoff session is booted, composed a boot paste anyway, and
both were withdrawn (operator ruling INBOX-dev-knowledge-2026-09-08-038; AMEND-BATCH-V-001 §1).
The knowledge was already in the repo -- Ch8's batch protocol and dispatch table -- and never
reached the operator as a paste-ready form. A composed paste is a second copy of Ch8, free to
drift from it, and the drift is invisible: a boot that quotes a superseded ceiling reads exactly
like one that quotes the live one.

So: **Ch8 is the source, the render is the only path, and drift is a test failure.** The seat
template supplies STRUCTURE (which refusal at which step, where each Ch8 region lands); every
byte of doctrine is machine-extracted by `seat_ch8` at the moment of the cut; probe **P12**
re-extracts and byte-compares, so a Ch8 edit re-issues the pastes automatically and a bundle
carrying a stale one FAILS.

WHAT THIS MODULE REFUSES, and each is a way the guarantee dies quietly:

  * **A template whose `{{CH8:...}}` set disagrees with `seat_ch8.SEAT_BLOCKS`.** Either a
    declared block renders nowhere (doctrine that never reaches the seat) or the template asks
    for one the map does not give it. Both look fine in the output.
  * **A rendered artifact carrying `<PROMPTS_DIR>` or a typed path.** AMEND-BATCH-V-002 §3(b):
    every rendered boot resolves `CLAUDE_PROMPTS_DIR` from User scope itself -- no placeholder,
    no path typed by the operator, ever. The closure is N -> 0 with a render test that fails on
    either, and this is that test's enforcement half.
  * **An unresolved `{{TOKEN}}`.** A paste shipped with a live token is a paste the seat cannot
    run, and it ships looking complete.
  * **A rendered boot that fails the seat refusals it carries.** The boots are the first
    consumer of `seat_refusals`; a boot telling a seat to write its waits as code while stating
    its own as an intention would be the exact failure it is teaching against.

HONEST LIMIT. P12 proves a rendered file equals a fresh render of the CURRENT Ch8. It does not
prove Ch8 is right, and it does not prove the render reached anyone: a bundle carrying five
perfect SEAT-BOOT files that no seat opens is a green probe over an unread artifact. What closes
that leg is the incoming seat's first dispatch using one verbatim, which is INBOX 038's own
Done-when and is not a property any test in this repo can hold.
"""
from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import dispatch_surface
    import seat_ch8
    import seat_refusals
except ImportError:                                  # imported as `scripts.gen_seat_boot`
    from scripts import dispatch_surface, seat_ch8, seat_refusals  # type: ignore[no-redef]

_REPO_ROOT = _SCRIPTS.parent

TMPL_RELPATH = "templates/handoff/seats"
TMPL_SUFFIX = ".md.tmpl"

#: THE SEAM OF A SPLIT SEAT, as two file paths. Declared here, above `_REFUSAL_LINES`, because a
#: refusal line names them: the boundary between a split seat's halves is a FILE, so the check
#: that enforces it and the boot that explains it must point at the same one. See SEAT_PHASES.
#:
#: The artifact that crosses the boundary FORWARD -- the plan half's ruling, which the execute
#: half boots from. Under `$d`, which every rendered boot binds in its own section 0.
HANDOFF_ARTIFACT = "$d/to-cc/MERGE-PLAN-<batch>.md"
#: The artifact that crosses it BACKWARD. A separate file rather than an append to the plan, so
#: the plan stays a thing the execute half can re-read from the top without re-reading questions
#: it already asked.
ESCALATION_ARTIFACT = "$d/to-cc/ESCALATE-<batch>.md"

#: The token a template uses to place one Ch8 region: `{{CH8:<key>}}`.
_CH8_TOKEN_RE = re.compile(r"\{\{CH8:(?P<key>[a-z0-9\-]+)\}\}")
#: Any token still live after substitution -- a paste that cannot be run, shipped looking whole.
_LEFTOVER_TOKEN_RE = re.compile(r"\{\{[A-Z0-9_:\-]+\}\}")
#: A leading `<!-- ... -->` authoring note, dropped at render exactly as `gen_handoff` drops one.
_LEADING_NOTE_RE = re.compile(r"\A<!--.*?-->\s*(?=#)", re.DOTALL)

#: AMEND-BATCH-V-002 §3(b) -- what a rendered boot may not carry. A Windows drive path, a POSIX
#: home path and the placeholder itself: the three shapes that make a paste machine-specific.
_FORBIDDEN_IN_RENDER: tuple[tuple[str, str], ...] = (
    (r"<PROMPTS_DIR>", "the `<PROMPTS_DIR>` placeholder"),
    (r"[A-Za-z]:[\\/](?:Users|My Drive)", "a literal Windows path"),
    (r"/(?:home|Users)/[A-Za-z0-9._-]+/", "a literal POSIX home path"),
)

#: §0 for every rendered boot. NOT composed here: `to-browser/SEAT-BOOT-integrator.md` §0 is the
#: form AMEND-BATCH-V-002 §3(b) names as "the corrected form", and the same ruling says "the
#: generator makes it structural" -- so generalising that block is applying the ruling. Three
#: lines because all three are load-bearing: an unset variable falls back LOUDLY (a silent
#: Downloads fallback is how "to-cc is empty" gets read as "nothing filed"), a stale inherited
#: PROCESS value is REPAIRED rather than reported (a long-lived daemon's environment block
#: predates the User setting), and the resolved directory is echoed so no later step has to
#: assume which one it read.
TRANSPORT_BLOCK = """```powershell
$d = [Environment]::GetEnvironmentVariable("CLAUDE_PROMPTS_DIR","User")
if (-not $d) { "CLAUDE_PROMPTS_DIR unset - Downloads fallback"; $d = "$env:USERPROFILE\\Downloads" }
if ($env:CLAUDE_PROMPTS_DIR -ne $d) { $env:CLAUDE_PROMPTS_DIR = $d; "process value OVERRIDDEN" }
"transport: $d"
```

Repair a stale process value; do not merely report it. Every path this boot names below is
relative to `$d` -- the variable is the source, and a directory typed by hand is a fact this
paste cannot keep current."""

#: Which Ch8 region states each seat's stop condition. The rendered line POINTS at it rather
#: than restating it: a second statement of a stop condition is a second thing to keep true.
SEAT_STOP_BLOCK: dict[str, str] = {
    "dispatcher": "two-touch",
    "integrator": "refuse-to-finish",
    "filings": "wave-close",
    "handoff": "window-equals-batch",
    "lane": "per-lane-requirements",
}

#: One runnable line per refusal, `{seat}`-agnostic. The seat boot carries the LINE, not the
#: sentiment -- a boot that says "remember the ceiling" has said what this repo already said in
#: prose and then watched be broken.
_REFUSAL_LINES: dict[str, tuple[str, str]] = {
    "lane-ceiling": (
        "uv run --locked python scripts/seat_refusals.py lane-ceiling --check-worktrees "
        "--lane <slug> [--lane <slug> ...]",
        "STEP 0, before the first worktree exists. `--check-worktrees` reads the live list "
        "rather than asking you to self-report what you have already provisioned.",
    ),
    # BETWEEN the ceiling and the DryRun, and the position is the mechanism (`[#675]` 3.4). It
    # needs the lane list the ceiling just validated, and it must precede the DryRun because
    # after the DryRun the dispatcher fires -- at which point a collision has been paid for.
    "file-collision": (
        "uv run --locked python scripts/seat_refusals.py file-collision --check-worktrees "
        "--contract <LANE-*.md> [--contract ...]",
        "STEP 0, on the batch's contract set AS THE MANIFEST DECLARES IT -- never a glob of the "
        "transport, which still holds superseded re-cuts that collide with their own "
        "replacements (measured 2026-09-12 on batch X). Run "
        "`freeze_manifest_contract_agreement` ([#630]) first; it owns whether the set is right. "
        "Two lanes declaring one file hand back either a serial merge conflict or two trees "
        "that each regenerated the same derived surface against the other's absence.",
    ),
    # TWO lines, and the ORDER inside the block is the ruling. The checker runs first, against
    # this step 0's own text; the DryRun of every generated contract is then the LAST thing step
    # 0 does (AMEND-BATCH-V-002 §1). A block that ended on the checker would have moved the
    # DryRun off the boundary it guards, which is the failure the ruling names.
    "dryrun-step0": (
        "uv run --locked python scripts/seat_refusals.py dryrun-step0 --step0 <this file> "
        "--contract <LANE-*.md> [--contract ...]\n"
        "dispatch <LANE-*.md> -DryRun          # once per generated contract, and nothing after",
        "The LAST line of step 0 (AMEND-BATCH-V-002 §1). Present, last, and covering every "
        "generated contract -- the one left out is the one that fails at dispatch. Batch V froze "
        "six contracts the live verb refused and found out by running this.",
    ),
    "carried-by": (
        "uv run --locked python scripts/seat_refusals.py carried-by "
        "$d/to-cc/DECLARE-*.md $d/to-cc/AMEND-*.md $d/to-cc/BATCH-*.md",
        "Before the write, not after it. Flush-left `carried-by:` in the head window, valued "
        "with a repo path or the literal OPEN; a bare substring match is a different check.",
    ),
    "reviewer-mismatch": (
        "uv run --locked python scripts/seat_refusals.py reviewer --contracted <exact model id> "
        "<review artifact>",
        "The tally names the reviewer that actually ran, exactly. A substitution that does not "
        "report `review=NONE` is refused: `gpt-5.6` for `gpt-5.6-terra` is a mismatch.",
    ),
    # THE SPLIT'S ENFORCEMENT HALF, and the only refusal addressed to a seat's CHEAPER half.
    # Per merge rather than once at boot: a check that ran at boot would have read a plan the
    # operator went on to amend, and the amendment IS the escalation path working.
    "unruled-merge": (
        "uv run --locked python scripts/seat_refusals.py unruled-merge "
        f"--plan {HANDOFF_ARTIFACT} --branch <branch>",
        "IMMEDIATELY BEFORE each `git merge --no-ff`, and it is how the execute half knows it "
        "is authorised rather than deciding that it is. The plan file grants authority PER "
        "ENTRY; an unruled branch, a HOLD, or a branch ruled twice inconsistently all REFUSE, "
        "and each refusal names what to escalate. "
        f"Append the merge, the refusal verbatim and your question to `{ESCALATION_ARTIFACT}`, "
        "STOP that merge, and continue only with entries the plan marked INDEPENDENT.",
    ),
    # `[#833]`: the two refusals on seat STATE, read from `scripts/seat_registry.py` where `state` is
    # written by hook events only. The bind is NOT on this line on purpose: a dispatcher or a lane
    # that ran it would register a role it does not hold, so the clause names who binds.
    "no-live-integrator": (
        "uv run --locked python scripts/seat_refusals.py no-live-integrator --batch <batch>",
        "Before any lane enters the batch. Only a LIVE integrator bound to this batch passes; a "
        "wedged, starved or absent one is named and refused. The integrator seat itself runs "
        "`uv run --locked python scripts/seat_registry.py bind --role integrator --batch <batch>` "
        "from its own session first, then this line to prove the bind took.",
    ),
    "lane-owned": (
        "uv run --locked python scripts/seat_refusals.py lane-owned --lane <lane worktree name>",
        "A lane's first act. Refuses when another session already owns this lane and is live -- on "
        "2026-09-17 a second session was dispatched onto lane ab-833 and found its owner only by "
        "reading staged files. A wedged or absent owner does not refuse: relaunching is the remedy.",
    ),
    "sleeping-poll": (
        "uv run --locked python scripts/seat_refusals.py sleeping-poll <your own working notes>",
        "Every wait you write is a loop with an interval, a bound and a predicate read from the "
        "file surface. A turn that ends on an intention has no next tick.",
    ),
}


class RenderRefusal(RuntimeError):
    """A seat boot could not be rendered honestly. Raised -- the caller gets no file."""


def _template_path(seat: str, repo_root: Path) -> Path:
    return repo_root / TMPL_RELPATH / f"SEAT-BOOT-{seat}{TMPL_SUFFIX}"


def out_name(seat: str) -> str:
    """The rendered artifact's filename, per INBOX 038 (`SEAT-BOOT-<role>.md`)."""
    return f"SEAT-BOOT-{seat}.md"


# =================================================================================================
# SEAT PHASES -- which model each seat's work runs at, and where a SPLIT seat's halves divide
# =================================================================================================
#
# Distinct from the Ch8 routing matrix, which routes an ARC's work: this is the tier the seat
# itself runs at. Operator ruling AX22-3 (2026-09-11) set the two largest Opus sinks -- the
# dispatcher's work is mechanical (freeze, DryRun, fire, receipts), and the integrator "judges
# merge verdicts on Opus while running suites and teardowns on Sonnet".
#
# THE INTEGRATOR IS THE ONE SEAT WHOSE TIER IS NOT A SINGLE VALUE, and until this lane it was
# stated as one anyway (`opusplan`). Two things were wrong with that, and each was measured:
#
#   1. **It reached no flag.** This map is rendered into the boot's `<!-- GENERATED -->` comment.
#      The launch command the boot actually carries came from Ch8 dispatch row 3 -- the bare word
#      `claude`, with no `--model`. That is `[#717]`'s closed defect one surface over: `[#717]`
#      fixed the LANE CONTRACT generator's line and the SEAT boot's line was never in its scope.
#      Batch Z's integrator seat ran **100% `claude-opus-5`, USD 82.53, 30.5% of the night**,
#      under a header that said `opusplan`.
#
#   2. **`opusplan` keys on plan MODE, and this seat's halves are not modes.** Judgment and
#      mechanics interleave many times per merge, and the prompt cache is PER MODEL. Measured on
#      six mixed-model transcripts on this host: the turn after a model switch carries a
#      cache-write of 29,751-379,585 tokens against a same-session median of 614-1,759 (a 48x to
#      391x jump) while its cache-read collapses to the small shared prefix. At the integrator's
#      own measured mean context of 232,875 tokens/call, one switch into Opus costs USD 1.46 and
#      one into Sonnet USD 0.58, against a saving of USD 0.0812 per turn moved. **A per-turn
#      split needs 25 consecutive cheap turns to repay one round trip** and a merge walk has
#      roughly eight.
#
# SO THE BOUNDARY IS COARSE AND IT IS A FILE: two SESSIONS, not two modes. Each holds its own
# context on its own model, permanently cached; an escalation is a message between two live
# sessions rather than a switch that re-caches 232,875 tokens. Ch8 point 6 already rules STATE IS
# FILES, and this applies that rule to the seam inside one seat.

#: Why AX22-3's INTENT is kept and its named MECHANISM is not. Carried in the module rather than
#: in a commit message because the next seat to read this map will ask, and a ruling's quoted
#: token outliving its merits is how a measured defect becomes doctrine.
SPLIT_RATIONALE = (
    "AX22-3 (2026-09-11) ruled the integrator seat split -- judgment on Opus, mechanics on "
    "Sonnet -- and named `opusplan` as the means. The substance is kept exactly and encoded in "
    "SEAT_PHASES. The means is replaced on measured evidence: `opusplan` keys on plan MODE "
    "rather than on the work, it was measured INERT on a background shape "
    "(`dispatch_surface.BACKGROUND_INERT_MODELS`), and at this seat's context size a per-turn "
    "split costs more in per-model cache re-writes than the cheaper tier saves. A ruling binds "
    "its merits, not its quoted token."
)


@dataclass(frozen=True)
class Phase:
    """One routed half of a seat's work.

    `does` is the DECIDABLE boundary -- what work belongs to this phase, written so a seat can
    classify a turn without asking. `escalates` is what this phase does when it meets work that
    is not its own; for the cheap half of a split that answer must be a STOP and never a
    judgment call, which is the failure this lane's contract names by name: *"a split that
    silently lets the cheap half make expensive decisions is worse than no split -- it buys a
    lower cost line by moving judgment somewhere that cannot exercise it."*
    """

    name: str
    model: str
    mode: str
    effort: str
    does: str
    escalates: str
    #: Does this phase's seat LAUNCH ITSELF? True for the four attended seats, which the operator
    #: starts by hand at Ch8 dispatch row 3 (INTERACTIVE). FALSE for `lane`, and the distinction
    #: is not cosmetic: a lane is dispatched `--bg` BY THE DISPATCHER, so a launch line in a
    #: lane's own boot would be a command that seat can never run -- and a raw `claude … --bg
    #: --worktree` form in a template is precisely the rival launch form register section V was
    #: ruled on (`dispatch_surface._RIVAL_FORMS`). A non-self-launching seat's tier is still
    #: DECLARED here -- it is what the render header records, and `[#717]` already puts it on the
    #: contract line the dispatcher fires -- but the boot POINTS at that rather than restating it.
    self_launched: bool = True


#: WHICH PHASES EACH SEAT RUNS, in order. Four seats have one; the integrator has two.
#:
#: STATED, NEVER DEFAULTED -- the posture the single-value map had before it, for the same
#: reason: a seat added to the enum without a decided tier must fail a test rather than render an
#: unresolved one.
SEAT_PHASES: dict[str, tuple[Phase, ...]] = {
    "dispatcher": (
        Phase(name="dispatch", model="sonnet", mode="execute", effort="high",
              does="the mechanical open: freeze the contract set, run step 0's refusals, DryRun "
                   "every generated contract, fire, and record what was fired.",
              escalates="A contract the freeze gate refuses, or a lane set that will not pass "
                        "the ceiling, is an OPERATOR question -- ask it rather than re-cutting "
                        "the batch."),
    ),
    # THE SPLIT. The order is the seam: plan runs first, once, and emits the file execute boots
    # from. Reversing them would put the mechanics in front of the ruling that authorises them.
    "integrator": (
        Phase(name="plan", model="opus", mode="plan", effort="high",
              does="JUDGMENT WITH SYSTEM CONTEXT, and all of it before the first merge: read the "
                   "whole merge queue, order it, adjudicate every conflict, rule on each lane's "
                   "hand-back, rule on every gate refusal already visible, and mark which merges "
                   "are INDEPENDENT of each other. Write one ruling per queued lane to "
                   f"`{HANDOFF_ARTIFACT}`. Merge NOTHING -- this half runs under "
                   "`--permission-mode plan` and is mechanically incapable of it, which is the "
                   "point rather than a side effect.",
              escalates="This half IS the escalation target. When "
                        f"`{ESCALATION_ARTIFACT}` gains an entry, rule on it, append the ruling "
                        f"to `{HANDOFF_ARTIFACT}`, and say so in the channel. Stay resident: a "
                        "resumed session pays a cache READ of its context, a re-launched one "
                        "pays a fresh cache WRITE of the same 232,875 tokens (USD 1.46)."),
        Phase(name="execute", model="sonnet", mode="execute", effort="high",
              does="THE MECHANICAL WALK, and nothing else: `git merge --no-ff` in the plan's "
                   "order, run the gates, read an exit code, file a receipt, run the "
                   "refuse-to-finish checklist, tear a worktree down. Single-file mechanics "
                   "carrying no system context. Boot from "
                   f"`{HANDOFF_ARTIFACT}` and treat it as the whole of your authority.",
              escalates="ANYTHING THE PLAN DOES NOT ALREADY RULE -- an unforeseen conflict, a "
                        "gate refusal with no standing ruling, a hand-back that reads wrong, a "
                        "lane that moved under you: append the merge, the refusal text verbatim "
                        f"and the question to `{ESCALATION_ARTIFACT}`, then **STOP that merge**. "
                        "Continue only with merges the plan marked INDEPENDENT. Do NOT rule. "
                        "One escalation costs at most the plan half's cache read; one turn you "
                        "keep on this tier saves USD 0.0812, so escalating early is cheap and "
                        "ruling wrongly is not."),
    ),
    "filings": (
        Phase(name="file", model="opus", mode="execute", effort="high",
              does="classification and the wave close -- judgment about what a finding IS, which "
                   "is the work that does not survive a cheaper tier.",
              escalates="A finding with no standing classification is an OPERATOR question "
                        "(ADR-108 SA routes functional questions to the operator)."),
    ),
    "handoff": (
        Phase(name="cut", model="opus", mode="execute", effort="high",
              does="the bundle cut and the residual -- an authored artifact, not a render.",
              escalates="A probe that cannot compute its ground truth is a REPORTED GAP, never "
                        "a pass (Z-G4). Report it; do not decide it."),
    ),
    "lane": (
        Phase(name="build", model="opus", mode="execute", effort="high",
              does="the lane's own arc, under its frozen contract.",
              escalates="The V-2 decision budget: curated-baseline touches, rule-vs-ruling "
                        "conflicts, and fork classes with no standing ruling go back to the "
                        "operator. Everything else takes the contract default and is REPORTED.",
              # The one seat that does not start itself. See `Phase.self_launched`.
              self_launched=False),
    ),
}

#: The model each seat BOOTS ON. DERIVED from the phase map -- its first phase -- and never a
#: second declaration. A tier stated in two places is two things to keep true, and the drift is
#: invisible: a header reading `opusplan` over a boot that launches `opus` looks exactly like one
#: that agrees, which is how batch Z's integrator seat ran a whole night at a tier nobody chose.
SEAT_MODELS: dict[str, str] = {seat: phases[0].model for seat, phases in SEAT_PHASES.items()}


def model_clause(seat: str) -> str:
    """The `model:` header value. NAMES EVERY PHASE for a split seat, never just the entry one.

    A header reporting one of two tiers is the same class of lie as `opusplan` over a boot that
    ran neither: it reads as a complete statement of how the seat runs. `opus (plan) + sonnet
    (execute)` is longer and it is checkable by eye against the launch lines below it.
    """
    phases = SEAT_PHASES[seat]
    if len(phases) == 1:
        return phases[0].model
    return " + ".join(f"{p.model} ({p.name})" for p in phases)


def _provenance(seat: str, batch: str, date: str, ch8_sha: str) -> str:
    """The render header. Machine-readable, because `verify()` reads `batch`/`date` back out of
    it to re-render under the same inputs -- a comparison against a render with different tokens
    would report drift that is not there.

    `model:` sits between `date:` and `ch8-sha256:` deliberately: `_HEADER_RE` stops at the
    pipe after `date`, so the field is additive and no existing reader has to change."""
    return (
        "<!-- GENERATED by scripts/gen_seat_boot.py from protocols/PLAYBOOK.md Ch8.\n"
        "     Do not hand-edit, and do not compose a rival: a composed boot paste is the defect\n"
        "     operator ruling INBOX-dev-knowledge-2026-09-08-038 withdrew.\n"
        f"     seat: {seat} | batch: {batch} | date: {date} | model: {model_clause(seat)}"
        f" | ch8-sha256: {ch8_sha}\n"
        "     Probe P12 re-extracts every ch8: region below and byte-compares; drift = FAIL. -->"
    )


#: What one turn moved from Opus to Sonnet saves, and the context it was measured at. Both ride
#: into the boot, because "escalation is cheap" is a CLAIM and an unpriced one trains a seat
#: either to escalate on everything or to avoid it entirely -- and both defeat the split.
#: Measured on the batch-Z integrator session `9b8de937`: 232,875 tokens of cache read per call,
#: 624 calls, USD 89.88 whole-session / USD 82.53 in its declared window.
SEAT_TURN_SAVING_USD = "0.0812"
SEAT_MEAN_CONTEXT_TOKENS = "232,875"


def _phase_block(seat: str) -> str:
    """The seat's routing, as RESOLVED LAUNCH LINES -- one per phase, every constant emitted.

    THE LINE IS RESOLVED, NOT TYPED. `dispatch_surface.resolve_launch` owns the model -> flags
    resolution for `[#752]`, and reaching it here rather than formatting a line means this
    generator cannot drift from the organ that decides what a shape's launcher honours. It also
    means a phase declaring something unhonourable REFUSES instead of rendering: a boot carrying
    a partial command is worse than one that was never written, because a seat copies what is in
    front of it.
    """
    lines: list[str] = []
    for phase in SEAT_PHASES[seat]:
        if not phase.self_launched:
            # A POINTER, never a command. This seat is dispatched by another one, so a launch
            # line here would be a command it can never run -- and the `--bg --worktree` form it
            # would have to carry is the rival literal launch form section V was ruled on.
            lines.append(
                f"**Phase `{phase.name}` -- {phase.model}**\n\n"
                "This seat does NOT launch itself, so this boot carries no launch line: the "
                "dispatcher fires it, and the tier rides your CONTRACT's own routing row (the "
                "line is rendered from that row -- `[#717]`). If the tier you are running at "
                f"does not match your contract's row, that is a REPORTABLE defect, not a "
                f"preference. Declared tier for this seat: `{phase.model}`.\n\n"
                f"*Runs:* {phase.does}\n\n"
                f"*Hands off / escalates:* {phase.escalates}")
            continue
        launch = dispatch_surface.resolve_launch(
            model=phase.model, mode=phase.mode, effort=phase.effort,
            shape="interactive", slug=seat)
        if not launch.ok:
            raise RenderRefusal(
                f"REFUSED: {out_name(seat)} phase {phase.name!r} does not resolve into a launch "
                f"its shape can honour -- " + "; ".join(launch.refusals) + ". A boot carrying "
                "most of a command is worse than one that was never written: a seat copies what "
                "is in front of it")
        lines.append(
            f"**Phase `{phase.name}` -- {phase.model}**\n\n"
            f"```\n{launch.render()}\n```\n\n"
            f"*Runs:* {phase.does}\n\n"
            f"*Hands off / escalates:* {phase.escalates}")
    if len(SEAT_PHASES[seat]) == 1:
        return lines[0]
    return (
        "**THIS SEAT IS SPLIT, and the boundary is a FILE rather than a mode.** Two sessions, "
        f"not two toggles. The plan half rules and writes `{HANDOFF_ARTIFACT}`; the execute half "
        f"boots from that file and writes `{ESCALATION_ARTIFACT}` when it meets anything the "
        "plan does not rule. Each session keeps its own context on its own model, permanently "
        "cached — which is the whole reason the seam is a file. **The prompt cache is per "
        f"model**: a mid-session model switch re-writes all {SEAT_MEAN_CONTEXT_TOKENS} tokens of "
        "context at the new model's cache-write rate (measured 48x to 391x a normal turn's, on "
        "six mixed-model transcripts), which costs USD 1.46 into Opus and USD 0.58 into Sonnet "
        f"against a saving of USD {SEAT_TURN_SAVING_USD} per turn moved. A per-turn split needs "
        "25 consecutive cheap turns to repay one round trip and a merge walk has about eight; "
        "two resident sessions need none, because nothing switches.\n\n"
        + "\n\n".join(lines))


#: The seat's own cost line, and the verb that writes it. IN THE PASTE, because done-when 4 asks
#: for an instrument that "fires without being remembered" and a habit is the thing being
#: replaced -- batch Z's cost ledger carried ZERO rows for its own batch, and its close packet's
#: own words were *"a figure that must be recomputed at close is not a ledger"*.
_SEAT_COST_BLOCK = (
    "Your own sitting is a cost line, and on batch Z it was the LARGEST one — USD 82.53, "
    "30.5% of a USD 270.72 night, more than any single lane. Close it before you stop, with the "
    "window you actually worked:\n\n"
    "```\n"
    "uv run --locked python scripts/lane_cost.py seat-close --session <your session id> \\\n"
    "    --batch <batch> --since <first turn, UTC ISO-8601> --until <last turn, UTC ISO-8601>\n"
    "```\n\n"
    "A seat is keyed by **session**, never by directory: the primary checkout's store holds that "
    "checkout's whole history, and a directory-keyed read of this seat on batch Z returned "
    "USD 8,714.37 against a real USD 82.53 — a 32x overstatement that looked like a measurement. "
    "**The window rides the row** because a session transcript keeps growing: the same batch-Z "
    "file prices at USD 82.53 at 06:51:12Z and USD 89.88 at end-of-file, and a paired comparison "
    "measured under two different windows is worthless. If you skip this, the next seat's "
    "SessionStart banner names your batch as the one with no seat row.")


_HEADER_RE = re.compile(
    r"seat:\s*(?P<seat>\S+)\s*\|\s*batch:\s*(?P<batch>.*?)\s*\|\s*date:\s*(?P<date>\S+)\s*\|"
)


def _refusal_block(seat: str) -> str:
    """The seat's refusals, as runnable lines with one clause each on where and why."""
    lines: list[str] = []
    for name in seat_refusals.SEAT_REFUSALS[seat]:
        command, clause = _REFUSAL_LINES[name]
        lines.append(f"**`{name}`** -- {clause}\n\n```\n{command}\n```")
    return "\n\n".join(lines)


def _stop_condition(seat: str) -> str:
    """A POINTER at the region in this same file that states the stop, plus Ch8 point 6's file."""
    key = SEAT_STOP_BLOCK[seat]
    title = seat_ch8.BLOCKS[key].title
    return (
        f"Stated above, by the Ch8 region **{title}** -- this line adds nothing to it and is a "
        "pointer so there is one statement of it rather than two.\n\n"
        f"On stop, write `$d/to-browser/SESSION-{seat}.md` (Ch8 point 6, the STATE IS FILES "
        "region): a session that coordinated only by message leaves no state behind it."
    )


def _ch8_sha(playbook_text: str) -> str:
    """A short digest of the CHAPTER, so the header changes exactly when Ch8 does."""
    chapter = seat_ch8.chapter_text(playbook_text)
    return hashlib.sha256(chapter.encode("utf-8")).hexdigest()[:12]


def render(seat: str, *, batch: str, date: str, repo_root: Path | None = None,
           playbook_text: str | None = None) -> str:
    """One rendered SEAT-BOOT file, as text. Refuses rather than emitting a dishonest paste."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    if seat not in seat_ch8.SEAT_BLOCKS:
        raise RenderRefusal(
            f"REFUSED: {seat!r} is not a declared seat; the enum is {', '.join(seat_ch8.SEATS)}"
        )
    tmpl_path = _template_path(seat, root)
    if not tmpl_path.exists():
        raise RenderRefusal(f"REFUSED: no seat template at {tmpl_path}")
    template = tmpl_path.read_text(encoding="utf-8")

    declared = set(seat_ch8.SEAT_BLOCKS[seat])
    placed = {m.group("key") for m in _CH8_TOKEN_RE.finditer(template)}
    if placed != declared:
        raise RenderRefusal(
            f"REFUSED: {seat} template and seat_ch8.SEAT_BLOCKS disagree -- "
            f"declared-but-unplaced: {sorted(declared - placed) or 'none'}; "
            f"placed-but-undeclared: {sorted(placed - declared) or 'none'}. A declared block that "
            "renders nowhere is doctrine that never reaches the seat, and the output looks fine "
            "either way"
        )

    text = playbook_text if playbook_text is not None else seat_ch8.playbook_text(root)
    rendered = _LEADING_NOTE_RE.sub("", template, count=1)
    for key in declared:
        body = seat_ch8.extract(key, text)
        region = (f"<!-- ch8:begin {key} -->\n{seat_ch8.BLOCKS[key].label}\n\n{body}\n"
                  f"<!-- ch8:end {key} -->")
        rendered = rendered.replace("{{CH8:" + key + "}}", region)
    for token, value in (
        ("BATCH", batch),
        ("DATE", date),
        ("SEAT", seat),
        ("PROVENANCE", _provenance(seat, batch, date, _ch8_sha(text))),
        ("TRANSPORT_BLOCK", TRANSPORT_BLOCK),
        ("REFUSAL_BLOCK", _refusal_block(seat)),
        ("STOP_CONDITION", _stop_condition(seat)),
        ("PHASE_BLOCK", _phase_block(seat)),
        ("SEAT_COST_BLOCK", _SEAT_COST_BLOCK),
    ):
        rendered = rendered.replace("{{" + token + "}}", value)

    leftover = sorted({m.group(0) for m in _LEFTOVER_TOKEN_RE.finditer(rendered)})
    if leftover:
        raise RenderRefusal(
            f"REFUSED: {out_name(seat)} still carries {', '.join(leftover)} -- a paste shipped "
            "with a live token is one the seat cannot run, and it ships looking complete"
        )
    for pattern, what in _FORBIDDEN_IN_RENDER:
        m = re.search(pattern, rendered)
        if m:
            raise RenderRefusal(
                f"REFUSED: {out_name(seat)} carries {what} ({m.group(0)!r}) -- "
                "AMEND-BATCH-V-002 §3(b): a rendered boot resolves CLAUDE_PROMPTS_DIR from User "
                "scope itself, with no placeholder and no path typed by the operator"
            )
    seat_refusals.refuse_sleeping_poll(rendered, site=out_name(seat))
    return rendered.rstrip() + "\n"


def write_bundle(bundle_dir: str | Path, *, batch: str, date: str,
                 repo_root: Path | None = None) -> list[Path]:
    """Render all five boots into `bundle_dir`. Returns the written paths, in seat order.

    RENDER ALL, THEN WRITE. Writing each boot as it renders leaves a PARTIAL set behind when a
    later seat refuses -- and the caller, which catches the refusal and reports "no boots
    written", is then wrong about the directory it is describing (terra HIGH, 2026-09-09). Five
    files is a set: either the bundle carries it or it carries none of it.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    target = Path(bundle_dir)
    text = seat_ch8.playbook_text(root)
    rendered = {seat: render(seat, batch=batch, date=date, repo_root=root, playbook_text=text)
                for seat in seat_ch8.SEATS}
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for seat in seat_ch8.SEATS:
        path = target / out_name(seat)
        path.write_text(rendered[seat], encoding="utf-8", newline="\n")
        written.append(path)
    return written


def verify(bundle_dir: str | Path, *, repo_root: Path | None = None) -> list[str]:
    """PROBE P12 -- every SEAT-BOOT file in the bundle equals a fresh render from Ch8.

    Returns a list of drift descriptions; empty means PASS. `batch` and `date` are read back out
    of each file's own render header rather than supplied, so a re-render is compared under the
    inputs it was made with -- otherwise every file would report drift the moment the date rolled.

    A MISSING file is drift too. INBOX 038's closure is 0/5 -> 5/5, and a bundle carrying four
    correct boots passes any check that only compares the files that are there.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    target = Path(bundle_dir)
    text = seat_ch8.playbook_text(root)
    drift: list[str] = []
    for seat in seat_ch8.SEATS:
        path = target / out_name(seat)
        if not path.exists():
            drift.append(f"{out_name(seat)}: ABSENT -- the bundle carries no boot for this seat")
            continue
        found = path.read_text(encoding="utf-8")
        header = _HEADER_RE.search(found)
        if header is None:
            drift.append(f"{out_name(seat)}: no render header -- hand-written or hand-edited")
            continue
        try:
            fresh = render(seat, batch=header.group("batch"), date=header.group("date"),
                           repo_root=root, playbook_text=text)
        except (RenderRefusal, seat_ch8.ExtractionError, seat_refusals.SeatRefusal) as exc:
            drift.append(f"{out_name(seat)}: a fresh render REFUSES -- {exc}")
            continue
        if fresh != found:
            drift.append(
                f"{out_name(seat)}: DRIFT from Ch8 -- the file differs from a fresh render "
                f"({len(found)} B on disk, {len(fresh)} B fresh); regenerate with "
                "`python scripts/gen_seat_boot.py write --bundle <dir>`"
            )
    return drift


@click.group(help="Render the five SEAT-BOOT pastes from PLAYBOOK Ch8 (INBOX 038).")
def cli() -> None:                                           # pragma: no cover -- click plumbing
    pass


@cli.command("write")
@click.option("--bundle", required=True, type=click.Path(file_okay=False),
              help="the handoff bundle directory to render into")
@click.option("--batch", required=True, help="the batch this cut belongs to, e.g. V")
@click.option("--date", required=True, help="the window date, YYYY-MM-DD")
def cmd_write(bundle: str, batch: str, date: str) -> None:
    """Render SEAT-BOOT-{dispatcher,integrator,filings,handoff,lane}.md into BUNDLE."""
    try:
        written = write_bundle(bundle, batch=batch, date=date)
    except (RenderRefusal, seat_ch8.ExtractionError, seat_refusals.SeatRefusal) as exc:
        click.echo(str(exc), err=True)
        raise SystemExit(1) from exc
    for path in written:
        click.echo(f"{path} ({path.stat().st_size} B)")


@cli.command("verify")
@click.option("--bundle", required=True, type=click.Path(exists=True, file_okay=False))
def cmd_verify(bundle: str) -> None:
    """Probe P12: every SEAT-BOOT file equals a fresh render from Ch8."""
    drift = verify(bundle)
    for line in drift:
        click.echo(line, err=True)
    if drift:
        click.echo(f"P12: FAIL -- {len(drift)} of {len(seat_ch8.SEATS)} seat boot(s) drifted",
                   err=True)
        raise SystemExit(1)
    click.echo(f"P12: PASS -- {len(seat_ch8.SEATS)} seat boot(s) equal a fresh render from Ch8")


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
