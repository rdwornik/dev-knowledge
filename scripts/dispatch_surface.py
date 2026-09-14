#!/usr/bin/env python
"""dispatch_surface.py — R5: ONE reader for the ruled dispatch form, and the gate §V owes.

WHY THIS EXISTS. `protocols/STANDING_RULINGS.md` §V (2026-08-25) records that the hub carried
FOUR rival literal launch commands for one act, that `.claude/commands/lane-boot.md` emitted the
form Ch8 itself labels a fallback while silently dropping `--model` and `--effort`, and that
"roughly thirty consecutive browser seats failed to launch a lane. They were not uninformed;
they were informed by four sources that disagreed." Its own closing line names the remedy as
outstanding: "the drift organ that would assert every literal command in Ch8 resolves ... and
that `/lane-boot` names the ruled verb, is owed and unbuilt; until it exists these rulings bind
the seat and not the tree."

This module builds the tree-side half of that organ, and it does it by READING rather than
restating. Ch8's dispatch table is "the only place in the repository that carries a literal
launch command" — so a handoff bundle that wants to put the ruled verb in front of a seat
renders `ruled_form()` at generation time instead of carrying a fifth copy. A copy is what the
ruling was about.

HONEST LIMIT, and it is half the organ §V describes. The other half — asserting every literal
command in Ch8 actually RESOLVES via `Get-Command` on the operator's machine — is a live probe
of an L0 surface (`win-tooling`'s DispatchHelpers module) and is not buildable here: Layer 2
never executes (Critical Rule #4; ADR-28/36), and the module is not in this repo. What is built
is the half that lives in the tree: the ruled verb reaches the two point-of-use surfaces, and no
rival literal form sits beside it. A verb that agrees everywhere and resolves nowhere would pass
this gate — that is a stated gap, not a covered one.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch-surface")

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# The SOLE literal-command site, by its own heading (PLAYBOOK Ch8). Anchored on the heading text
# rather than a line number: an anchor rots inside its own branch, a heading survives an edit.
PLAYBOOK_PATH = "protocols/PLAYBOOK.md"
_TABLE_HEADING = "#### The dispatch table — the SOLE literal-command site"
# The row inside it that carries the LOCAL background-lane form — the shape a batch lane uses.
_LOCAL_ROW = "**1 — LOCAL background lane**"

# The two point-of-use surfaces §V names. Both are POINTERS to Ch8 by construction; this gate
# asserts the pointer still points at the same verb the table rules.
AGREEMENT_SITES = (".claude/commands/lane-boot.md", "templates/prompt-template.md")

# Rival literal launch forms, refused inside a FENCED BLOCK only. The distinction is deliberate
# and load-bearing: §V's correction is RECORDED in the prose of both files ("this line used to
# emit a raw `claude --worktree … --bg …` form"), and a gate that refused the mention would
# force the two surfaces to delete the very history that explains why they changed. What V4
# actually rules is narrower and checkable: the raw form "does not appear in a command file or a
# template" — as a command a seat would type, which in a markdown file means inside a fence.
#
# `Dispatch-Local` is NOT a rival: V2 makes it the documented manual fallback. The version-named
# aliases are (V3 — deprecated, fully working, and not what an operator types).
_RIVAL_FORMS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^claude\b.*--bg\b"), "raw `claude … --bg` form (§V V4 — FALLBACK-ONLY, "
                                       "documented once in Ch8 and never in a command file "
                                       "or a template)"),
    (re.compile(r"^claude\b.*--worktree\b"), "raw `claude --worktree` form (§V V4 — "
                                             "FALLBACK-ONLY)"),
    (re.compile(r"\bDispatch-CloudBrief\b"), "`Dispatch-CloudBrief` (superseded; it prints its "
                                             "own supersession notice)"),
    (re.compile(r"\bDispatch-Lane\b"), "`Dispatch-Lane` (§V V3 — a version-named alias, "
                                       "deprecated in favour of `Dispatch-Local`)"),
    (re.compile(r"\bDispatch-CloudV2\b"), "`Dispatch-CloudV2` (§V V3 — a version-named alias)"),
)


def fenced_lines(text: str) -> list[str]:
    """Every line inside a triple-backtick fence, stripped. Fences toggle on any ``` line.

    A markdown fence is where a literal command a seat TYPES lives; prose backticks are where a
    seat READS about one. The whole rival test rests on that split, so it is one function."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            inside = not inside
            continue
        if inside and line.strip():
            out.append(line.strip())
    return out


def ruled_form(repo_root: Path | None = None) -> list[str] | None:
    """The literal LOCAL-lane dispatch line(s), read LIVE from Ch8's dispatch table.

    Returns the fenced block's lines, or None when the table, the row, or its fence cannot be
    found — the caller then emits a POINTER. It never falls back to a remembered command: a
    second copy of the line is precisely the defect §V ruled on, and a stale copy that renders
    confidently is worse than a pointer that makes the seat open the table."""
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    try:
        text = (root / PLAYBOOK_PATH).read_text(encoding="utf-8")
    except OSError:
        return None
    head = text.find(_TABLE_HEADING)
    if head == -1:
        return None
    # BOUND the search to the table's own section. The LOCAL row's marker could plausibly appear
    # again later in the chapter as explanatory prose, and an unbounded `find` would then select
    # that occurrence and render whatever fence followed it as if it were the ruled command —
    # so the very drift this reader exists to detect (the row leaving the table) would render a
    # confident wrong answer instead of degrading. The section ends at the next heading of the
    # table's own level or shallower; `#####` sub-rows inside it are deliberately included.
    body = text[head + len(_TABLE_HEADING):]
    end = re.search(r"^#{1,4} ", body, re.MULTILINE)
    section = body[:end.start()] if end else body
    row = section.find(_LOCAL_ROW)
    if row == -1:
        return None
    m = re.search(r"^```[^\n]*\n(.*?)^```", section[row:], re.DOTALL | re.MULTILINE)
    if m is None:
        return None
    lines = [ln.rstrip() for ln in m.group(1).splitlines() if ln.strip()]
    return lines or None


def ruled_verb(repo_root: Path | None = None) -> str | None:
    """The lead token of the ruled LOCAL-lane form — the verb an operator types (`dispatch`)."""
    lines = ruled_form(repo_root)
    if not lines:
        return None
    first = lines[0].split()
    return first[0] if first else None


def agreement_findings(repo_root: Path | None = None) -> list[str]:
    """Every disagreement between the two point-of-use sites and Ch8's ruled verb.

    Returns a list of human-readable violation strings; [] when the surfaces agree. Two classes,
    both from §V: a site that does not NAME the ruled verb in a fence (the pointer stopped
    pointing), and a site carrying a RIVAL literal form in a fence (a fifth source to disagree
    with). Read-only."""
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    verb = ruled_verb(root)
    if verb is None:
        return [f"the ruled dispatch form is unreadable at {PLAYBOOK_PATH} "
                f"'{_TABLE_HEADING}' / '{_LOCAL_ROW}' — the SOLE literal-command site moved "
                "or was reworded; re-anchor this gate rather than removing it"]
    out: list[str] = []
    for rel in AGREEMENT_SITES:
        path = root / rel
        try:
            fenced = fenced_lines(path.read_text(encoding="utf-8"))
        except OSError:
            out.append(f"{rel}: unreadable — cannot verify it names the ruled verb `{verb}`")
            continue
        if not any(ln.split()[:1] == [verb] for ln in fenced):
            out.append(f"{rel}: no fenced line names the ruled verb `{verb}` "
                       f"({PLAYBOOK_PATH} '{_TABLE_HEADING}')")
        for line in fenced:
            for rx, why in _RIVAL_FORMS:
                if rx.search(line):
                    out.append(f"{rel}: rival literal launch form in a fenced block — {why}")
    return out


# --- RESOLVING A DECLARED ROUTING ROW INTO FLAGS THE LAUNCHER HONOURS ([#752]) -----------------
#
# A DIFFERENT QUESTION FROM THE ONE ABOVE. Everything above asks whether this repository's
# surfaces AGREE about the launch verb. Nothing asked whether the values a contract DECLARES can
# be HONOURED by the launcher its declared shape actually uses — and two surfaces that agree
# about the same wrong thing pass an agreement check perfectly.
#
# THE MEASUREMENT. `lane-x-689-conductor-e-proof` froze `| opusplan | execute | high |` under
# `**Shape:** local`. The operator ruled that tier onto the routing row AND onto the dispatch
# line so the lane could not re-decide it; `gen_lane_contract.MODEL_ENUM` was widened RED-first
# to admit it; `dispatch -DryRun` printed it; `claude --print --model opusplan` resolves where a
# bogus id returns `[claude-code:unrecognized_model]`. The lane then ran 84 of 84 assistant
# messages on `claude-sonnet-5`, zero Opus, while sibling lanes in the same fire returned exactly
# as ordered — so the instrument discriminates rather than reporting one answer. Every routing
# decision in that window was advisory.
#
# THE MODE COLUMN IS THE SAME DEFECT ONE COLUMN OVER, and it was never even visible.
# `gen_lane_contract.MODE_ENUM` has carried `plan` from the start and `check_contract` validates
# the declared value against it — and NOTHING anywhere resolved the column into a launcher
# argument. A contract declaring `| opus | plan | high |` under `**Shape:** local` dispatched
# byte-identically to one declaring `execute`. A declared field no code reads is a decision the
# tree records and does not make.
#
# THE VOCABULARY IS READ, NOT RESTATED — the discipline `ruled_form` applies to Ch8, applied to
# the enums. They live in `gen_lane_contract`, which owns them because it is what bakes them into
# a contract; this module reaches them rather than keeping a fifth copy, a second copy of a launch
# vocabulary being the precise defect §V was ruled on.

#: Model tiers whose behaviour under a BACKGROUND launch differs from their name, each carrying
#: the measurement that established it. A recorded observation about the CLI rather than a
#: doctrine restatement — which is why it lives in code: there is no doc to point at, and the one
#: surface that disagreed with the order was the one nobody was reading.
BACKGROUND_INERT_MODELS: dict[str, str] = {
    "opusplan": (
        "`opusplan` is a SPLIT tier -- Opus while the session is in plan mode, Sonnet after -- "
        "and every dispatch constant puts a lane on `--permission-mode bypassPermissions`, which "
        "NEVER enters plan mode. No plan phase means no Opus phase, so the tier collapses to its "
        "implement half. MEASURED 2026-09-13 on `lane-x-689-conductor-e-proof`: ordered "
        "`opusplan`, ran 84 of 84 assistant messages on `claude-sonnet-5`, zero Opus, while "
        "sibling lanes in the same fire returned exactly as ordered. Firing it literally does NOT "
        "honour the order either -- it yields Sonnet, which no contract names -- so there is no "
        "faithful-literal option and the choice is between two deviations. Name `opus` or "
        "`sonnet` explicitly. The scope is narrower than it looks: `opusplan` is CORRECT for an "
        "ATTENDED seat, which can enter plan mode, and AX22-3 routes the integrator seat to it"),
}

#: `--permission-mode` per declared MODE -- the resolution that makes the column mean something.
MODE_PERMISSION_MODE: dict[str, str] = {
    "execute": "bypassPermissions",
    "plan": "plan",
    # `plan-then-auto` ENTERS plan mode, and the "-then-auto" half is a seat act no flag spells.
    # The resolution is the half a launcher can carry; the rest stays the seat's, which is exactly
    # what makes it honourable for an attended shape and not for an unattended one.
    "plan-then-auto": "plan",
}

#: The permission mode a background lane runs under, and the only one it CAN. A `--bg` lane has
#: nobody to answer a prompt, so any mode that can stop and ask stalls it silently -- which is why
#: the dispatch constants carry it rather than defaulting it.
BACKGROUND_PERMISSION_MODE = "bypassPermissions"

#: The dispatch shapes that launch through `claude --bg`.
#:
#: HONEST LIMIT, stated because it bounds every green verdict below: only Ch8 row 1 ("LOCAL
#: background lane") is modelled here. `cloud` and `codespace` reach their substrates through
#: their own transports, which this reader does not open, and `interactive` is attended by
#: definition. A contract on one of those shapes is resolved WITHOUT the background legs -- not
#: because they are known safe there, but because this organ has not measured them.
BACKGROUND_SHAPES: tuple[str, ...] = ("local",)


class DispatchResolutionError(RuntimeError):
    """The declared vocabulary could not be read. FAIL-LOUD rather than degraded: guessing an
    enum here would resolve a contract against a vocabulary nobody declared, which is strictly
    worse than refusing to resolve it at all."""


def background_honoured_modes() -> tuple[str, ...]:
    """Modes a `--bg` launcher honours -- DERIVED from the two constants above, never listed.

    A mode is honourable for a background lane exactly when its `--permission-mode` is the one
    such a lane can run under. A separate list would be free to drift from the table, and a
    drifted list is how `plan` stayed declarable-and-unresolvable for as long as it did."""
    return tuple(mode for mode, perm in MODE_PERMISSION_MODE.items()
                 if perm == BACKGROUND_PERMISSION_MODE)


def _vocabulary():
    """`gen_lane_contract` — the module that OWNS the four declared enums and the routing-row
    grammar — imported lazily.

    LAZILY, for two reasons rather than taste. That module imports `gen_handoff`, which reaches
    back into this one, so a module-level import would make the pair load-order dependent; and
    `audit.py` imports this module on every run just to read `ruled_form`, which has no business
    paying for the generator's dependency chain.

    IT REACHES PRIVATE NAMES, and the alternative is worse. `_ROUTING_ROW_RE` is the grammar the
    generator EMITS, so a second copy here would be two organs reading one field by two rules --
    the split `validate_substrate` already paid for once, when a hand-authored contract tripped a
    gate on a word it had no way to know was reserved. A rename in the generator breaks this
    LOUDLY, through the refusals below, rather than silently producing a different answer."""
    try:
        from scripts import gen_lane_contract as _glc  # noqa: PLC0415
    except ImportError:  # pragma: no cover -- the scripts/-on-sys.path entrypoint
        import gen_lane_contract as _glc               # noqa: PLC0415
    return _glc


def _grammar(name: str):
    """One private grammar off `gen_lane_contract`, or a loud refusal naming it."""
    found = getattr(_vocabulary(), name, None)
    if found is None:  # pragma: no cover -- the loud half of `_vocabulary`'s private reach
        raise DispatchResolutionError(
            f"gen_lane_contract.{name} is gone: the grammar it held moved or was renamed. "
            f"Re-point this reader at its new name -- do NOT restate the grammar here, which is "
            f"what put four rival launch forms in this repository")
    return found


@dataclass(frozen=True)
class Launch:
    """One resolved launch: what a contract DECLARED, and the flags that honour it.

    `refusals` is a list rather than an exception because a contract can be wrong in several ways
    at once, and a seat fixing them one exception at a time learns the vocabulary the slow way.
    """
    model: str
    mode: str
    effort: str
    shape: str
    slug: str
    flags: tuple[str, ...] = ()
    refusals: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.refusals

    def render(self) -> str:
        """The resolved line, for a `-DryRun`-style receipt. EMPTY when the launch was refused --
        a refused launch has no line, and printing a partial one invites copying it."""
        return " ".join(("claude", *self.flags)) if self.ok else ""


def resolve_launch(*, model: str, mode: str, effort: str, shape: str, slug: str) -> Launch:
    """Resolve a declared routing row into the flags its shape's launcher HONOURS.

    Every refusal names the value AND why it cannot be honoured, because the remedy differs by
    class: an off-enum value is a typo, an inert tier is a measurement, an unhonourable mode is a
    shape mismatch. A refused launch emits NO flags -- emitting the survivors would hand a seat a
    line that is most of a command, which is how a partial refusal becomes a launch.
    """
    glc = _vocabulary()
    model, mode, effort, shape = (str(v or "").strip() for v in (model, mode, effort, shape))
    refusals: list[str] = []

    for value, enum, label in ((model, glc.MODEL_ENUM, "model"),
                               (effort, glc.EFFORT_ENUM, "effort"),
                               (mode, glc.MODE_ENUM, "mode")):
        if value not in enum:
            refusals.append(f"{label} {value!r} is outside the enum {{{' | '.join(enum)}}} -- "
                            f"a miss is refused, never rounded to a neighbour")
    if shape not in glc.SHAPE_ENUM:
        refusals.append(f"dispatch shape {shape!r} is outside the enum "
                        f"{{{' | '.join(glc.SHAPE_ENUM)}}} -- rounding `remote` to `cloud`, or "
                        f"`worktree` to `local`, would emit a CONFIDENTLY WRONG command, which is "
                        f"strictly worse than emitting none")
    # A MODE THIS TABLE DOES NOT SPELL IS A REFUSAL, not a default. `MODE_ENUM` can gain a member
    # without this table gaining a row, and defaulting the gap would resolve a mode nobody mapped
    # into whatever `execute` happens to mean -- the same silent re-decision `[#717]` closed one
    # field over.
    if mode in glc.MODE_ENUM and mode not in MODE_PERMISSION_MODE:
        refusals.append(f"mode {mode!r} is in MODE_ENUM but no `--permission-mode` is declared "
                        f"for it in MODE_PERMISSION_MODE -- extend that table rather than "
                        f"defaulting the gap, which would silently re-decide the mode")

    background = shape in BACKGROUND_SHAPES
    if background and model in BACKGROUND_INERT_MODELS:
        refusals.append(f"model {model!r} is INERT on a `--bg` lane: "
                        f"{BACKGROUND_INERT_MODELS[model]}")
    if background and mode in MODE_PERMISSION_MODE and mode not in background_honoured_modes():
        refusals.append(
            f"mode {mode!r} resolves to `--permission-mode {MODE_PERMISSION_MODE[mode]}`, which "
            f"a `--bg` lane cannot run: there is nobody to approve a plan or answer a prompt, and "
            f"the standing dispatch constant `--permission-mode {BACKGROUND_PERMISSION_MODE}` is "
            f"precisely the mode that never enters one. Declare "
            f"{' or '.join(repr(m) for m in background_honoured_modes())} and let the contract BE "
            f"the plan, or dispatch this at an attended shape")

    if refusals:
        return Launch(model=model, mode=mode, effort=effort, shape=shape, slug=slug,
                      refusals=tuple(refusals))

    # EVERY CONSTANT IS EMITTED, none defaulted. §V's measured defect was a launch form that
    # silently dropped `--model` and `--effort`, after which roughly thirty consecutive seats
    # launched lanes at a tier nobody chose. A flag omitted here is that defect, rebuilt.
    flags: list[str] = ["--bg"] if background else []
    flags += ["--model", model, "--effort", effort, "--permission-mode",
              BACKGROUND_PERMISSION_MODE if background else MODE_PERMISSION_MODE[mode]]
    if background:
        flags += ["--worktree", slug]
    return Launch(model=model, mode=mode, effort=effort, shape=shape, slug=slug,
                  flags=tuple(flags))


# --- reading a CONTRACT, which is where the declaration actually lives -------------------------

def contract_routing(text: str) -> "dict[str, str] | None":
    """`{model, mode, effort}` from a contract's routing table, or None when it declares none.

    None rather than a default, for the reason `[#717]` records: the model is the most expensive
    constant on a dispatch line, and a reader that supplied one would be making the decision the
    contract exists to state. Read from the DE-FENCED prose, so a contract quoting an example
    table inside a fence does not thereby declare one.
    """
    match = _grammar("_ROUTING_ROW_RE").search(_vocabulary().strip_fenced_blocks(text))
    if match is None:
        return None
    return {key: match.group(key).strip() for key in ("model", "mode", "effort")}


def contract_shape(text: str) -> "str | None":
    """The declared ``**Shape:** `x` `` value, or None.

    A DECLARATION IS A FENCED TOKEN AND PROSE IS NOT, anchored at line start -- the grammar
    `gen_lane_contract` and `validate_substrate` already read the field by. Unanchored, a contract
    EXPLAINING the field mid-sentence wins the precedence race over the real declaration further
    down, which is a defect `validate_substrate` has already recorded paying for."""
    match = _grammar("_SHAPE_LINE_RE").search(text)
    return match.group("shape").strip() if match else None


def contract_slug(text: str) -> "str | None":
    """The slug from the ADR-110 worktree-pairing line (`slug X -> branch Y -> contract Z`)."""
    match = re.search(r"slug\s+`(?P<slug>[^`]+)`\s*->", text)
    return match.group("slug").strip() if match else None


def _fence_findings(text: str) -> list[str]:
    """Refusals read off the contract's own `## Dispatch` fence -- the line a launcher RECEIVES.

    SCOPED TO WHAT NO OTHER ORGAN ASKS. `gen_lane_contract.check_contract` already asserts the
    routing row and the dispatch line name the SAME model; that leg is cited, not restated. What
    is missing there is the pair this module owns: a constant the line DROPS (§V's own defect --
    the form `/lane-boot` emitted silently lost `--model` and `--effort`), and an inert tier
    reaching a `--bg` line even when the row above it is clean. The two sources are free to
    disagree in BOTH directions, and a mismatch check reads only one of them.
    """
    out: list[str] = []
    for line in fenced_lines(text):
        tokens = line.split()
        if not tokens or tokens[0] != "claude" or "--bg" not in tokens:
            continue
        for flag in ("--model", "--effort", "--permission-mode"):
            if flag not in tokens:
                out.append(
                    f"the `--bg` dispatch line omits {flag} -- §V measured what a launch form "
                    f"that silently drops a constant costs: roughly thirty consecutive seats "
                    f"launched lanes at a value nobody chose. Every constant rides the line")
                continue
            index = tokens.index(flag) + 1
            value = tokens[index] if index < len(tokens) else ""
            if flag == "--model" and value in BACKGROUND_INERT_MODELS:
                out.append(f"the `--bg` dispatch line carries `--model {value}`, which is INERT "
                           f"there: {BACKGROUND_INERT_MODELS[value]}")
    return out


def contract_findings(path) -> list[str]:
    """Every way a lane contract declares something its launcher will not honour. `[]` when clean.

    Read-only, and WIRED INTO NO GATE BY CONSTRUCTION rather than by omission. A lane contract
    lives in an immutable `docs/audits/<date>-technical-<batch>-launch-contracts/` bundle, and the
    corpus holds contracts that legitimately froze values this organ now refuses -- x-689 among
    them, by operator ruling on the day. Armed tree-wide this would refuse that history, which is
    a ratchet against the record rather than a check on new work. It belongs at FREEZE time, over
    the contracts a batch is about to fire, beside `gen_lane_contract.check_contract` -- wiring it
    there is a change to a module this lane does not own, and is left as an open item rather than
    taken silently.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path.name}: unreadable -- cannot resolve its declared routing ({exc!r})"]

    row = contract_routing(text)
    if row is None:
        return [f"{path.name}: no `| Model | Mode | Effort |` routing row -- a contract states "
                f"the tier its lane boots at, and silence is not a declaration"]
    shape = contract_shape(text)
    if shape is None:
        return [f"{path.name}: no `**Shape:**` declaration, so there is no launcher to resolve "
                f"{row['model']}/{row['mode']} against"]

    launch = resolve_launch(model=row["model"], mode=row["mode"], effort=row["effort"],
                            shape=shape, slug=contract_slug(text) or "<slug>")
    return [f"{path.name}: {finding}"
            for finding in (*launch.refusals, *_fence_findings(text))]


# --- CLI ---------------------------------------------------------------------------------------

@click.group(help="Read the ruled dispatch form, and resolve a contract's declared routing row "
                  "into the flags its launcher actually honours ([#752]).")
def cli() -> None:
    """The dispatch surface, as a verb a seat can run."""


@cli.command("resolve")
@click.argument("contract", type=click.Path(exists=True, dir_okay=False))
def cmd_resolve(contract: str) -> None:
    """Print the launch line CONTRACT resolves to, or refuse and say why.

    Exits 1 on a refusal, so it is usable as a freeze-time check rather than only as a reader.
    """
    text = Path(contract).read_text(encoding="utf-8")
    row, shape = contract_routing(text), contract_shape(text)
    if row is None or shape is None:
        for finding in contract_findings(contract):
            click.echo(finding)
        raise SystemExit(1)
    launch = resolve_launch(model=row["model"], mode=row["mode"], effort=row["effort"],
                            shape=shape, slug=contract_slug(text) or "<slug>")
    findings = contract_findings(contract)
    if findings:
        for finding in findings:
            click.echo(f"REFUSED  {finding}")
        raise SystemExit(1)
    click.echo(launch.render())


@cli.command("check")
@click.argument("contracts", nargs=-1, required=True,
                type=click.Path(exists=True, dir_okay=False))
def cmd_check(contracts: tuple[str, ...]) -> None:
    """Refuse any CONTRACT declaring a value its launcher will not honour. Exit 1 on any finding."""
    findings = [finding for contract in contracts for finding in contract_findings(contract)]
    for finding in findings:
        click.echo(finding)
    click.echo(f"{len(contracts)} contract(s) read, {len(findings)} refusal(s)")
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
