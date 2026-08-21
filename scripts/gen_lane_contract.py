#!/usr/bin/env python
"""gen_lane_contract.py — emit (and check) a batch-lane frozen contract.

WHY A GENERATOR RATHER THAN A TEMPLATE ([#539] Done-item 2, "the generator as the
guarantee"). `templates/prompt-template.md` is the point-of-use *card* for a work-lane
prompt: a human copies it and fills placeholders. That is exactly the surface batch 6
falsified — a hand-assembled dispatch line passed the intended BRANCH name where the flag
takes the bare WORKTREE name, uniformly across all twelve lanes, and nothing surfaced it
until the integrator's merge queue matched 0 of 12 (`protocols/PLAYBOOK.md` Ch8, "The
dispatch surface is `dispatch <file>`"). A generator removes the class rather than warning
about it: the mechanical regions of a contract are BAKED IN here, so a contract cannot be
emitted missing its decision budget, missing its worktree-file pairing line, or naming an
effort tier the dispatch surface refuses.

WHAT IS BAKED IN, and each is asserted by a test rather than trusted:
  * the `## Dispatch` block, in the `Dispatch-Lane <slug> <file> [-Effort <tier>]` form,
    with the dispatch constants STATED (`--permission-mode bypassPermissions`, `--bg`)
    and `opus` as the model default;
  * the worktree <-> file pairing line (slug -> branch -> contract file), the 1:1 property
    ADR-110's fifth per-lane requirement asks for;
  * the V-2 decision budget, with its three ask-classes (a)/(b)/(c);
  * the receipt-gate fields for a cloud lane (STANDING_RULINGS Q5), emitted only for
    `--cloud`, since a local lane has no receipt to carry.

LIBRARY-FIRST, stated rather than claimed. The lane-name grammar is NOT re-implemented
here: `validate_branch_naming.validate_lane_worktree_name` is the repo's existing checker
and is called directly, so the generator and `/lane-boot` cannot drift apart on what a
lane name is. The emitted markdown's *shape* follows `templates/prompt-template.md` v1.14
(the `## Dispatch` block, the Model/Mode/Effort table, the What-NOT-to-do close), and the
CLI shape follows `scripts/gen_handoff.py` — the closest sibling generator, Click-based,
which is why this one is Click-based too.

THE EFFORT ENUM CARRIES A DECLARED DIVERGENCE, and it is surfaced rather than resolved
here. `[#539]`'s contract names `{low|medium|high|xhigh|max}` as this generator's enum;
`protocols/PLAYBOOK.md` Ch8 records the dispatch surface's enum as the CLOSED four
`{low|medium|high|xhigh}`, with `max` held OUT of dispatch routing by the 2026-08-07
architect ruling. This module implements the five the contract names — refusing anything
outside them — and LOGS A WARNING naming the divergence whenever `max` is selected, so the
conflict surfaces at generation time rather than at the operator's terminal. Choosing
between the two enums is a ruling, and a generator is not the place one gets made.

Layer-2 / read-only with respect to tracked spine files (ADR-28/36): writes ONLY the
contract path it is given, and never JOURNAL / BACKLOG / any index.
"""
from __future__ import annotations

import datetime as _dt
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

from validate_branch_naming import validate_lane_worktree_name  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("gen-lane-contract")

# --- the baked-in constants ---------------------------------------------------------------

#: The effort tiers this generator accepts, as `[#539]`'s contract enumerates them.
#: See the module docstring: the dispatch surface's own enum is the first FOUR.
EFFORT_ENUM: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")

#: The subset the dispatch surface routes (`protocols/PLAYBOOK.md` Ch8, "Model + effort are
#: stated at dispatch"). A tier in `EFFORT_ENUM` but not here is emitted WITH a warning.
DISPATCH_ROUTED_EFFORT: frozenset[str] = frozenset(EFFORT_ENUM[:4])

#: Model tiers, per the Ch8 routing matrix. `opus` is the `.dev-knowledge` default.
MODEL_ENUM: tuple[str, ...] = ("opus", "sonnet", "haiku")
DEFAULT_MODEL = "opus"

#: Lane modes. `execute` is the work-lane default (plan-mode-by-exception — the contract
#: IS the plan; `templates/prompt-template.md` v1.14).
MODE_ENUM: tuple[str, ...] = ("execute", "plan-then-auto", "plan")
DEFAULT_MODE = "execute"

#: Dispatch constants that ride every dispatch without being re-decided (Ch8).
PERMISSION_MODE = "--permission-mode bypassPermissions"
BACKGROUND_FLAG = "--bg"

#: The branch a worktree name produces, via `claude --worktree <name>`.
BRANCH_PREFIX = "worktree-"

#: Mandatory headings every emitted contract carries. `--check` reads for exactly these.
MANDATORY_SECTIONS: tuple[str, ...] = (
    "Dispatch",
    "Worktree pairing",
    "Done-contract",
    "Decision budget",
    "Steps",
    "What NOT to do",
)

#: The extra section a cloud lane carries (STANDING_RULINGS Q5).
CLOUD_SECTION = "Receipt gate"

#: The two receipt fields, checked as a conjunction (Q5).
RECEIPT_FIELDS: tuple[str, ...] = ("git-source-resolves-non-empty", "first-assistant-text-echoed")

_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
_DISPATCH_LINE_RE = re.compile(
    r"^Dispatch-Lane\s+(?P<slug>\S+)\s+(?P<file>\S+)(?:\s+-Effort\s+(?P<effort>\S+))?\s*$",
    re.MULTILINE,
)
_PAIRING_RE = re.compile(
    r"slug\s+`(?P<slug>[^`]+)`\s*->\s*branch\s+`(?P<branch>[^`]+)`\s*->\s*contract\s+`(?P<file>[^`]+)`"
)
#: The routing table's BODY row, anchored on its own `| Model | Mode | Effort |` header and
#: separator. Anchoring on the header is what keeps the header itself, and any other
#: three-column table in the file, from being read as the routing row.
_ROUTING_ROW_RE = re.compile(
    r"^\|[ \t]*Model[ \t]*\|[ \t]*Mode[ \t]*\|[ \t]*Effort[ \t]*\|[ \t]*\r?\n"
    r"^\|[-: \t|]+\|[ \t]*\r?\n"
    r"^\|[ \t]*(?P<model>[^|\n]*?)[ \t]*\|[ \t]*(?P<mode>[^|\n]*?)[ \t]*\|"
    r"[ \t]*(?P<effort>[^|\n]*?)[ \t]*\|[ \t]*$",
    re.MULTILINE,
)
#: A fenced code block, either ``` or ~~~ delimited.
_FENCE_RE = re.compile(r"^(?P<fence>```+|~~~+).*?^(?P=fence)\s*$", re.MULTILINE | re.DOTALL)


def strip_fenced_blocks(text: str) -> str:
    """Blank out fenced code blocks, keeping line count and offsets stable.

    A contract's *prose* is what carries its headings and its decision budget; a fenced block
    carries the dispatch line and nothing structural. Scanning raw text for both let a file
    whose entire body sat inside one fence report OK — every heading and every ask-class was
    "present", as example text (terra 2026-08-21, finding 1). Headings and ask-classes are
    therefore read from the de-fenced text; the dispatch line, which legitimately lives inside
    a fence, is still read from the whole file.
    """
    return _FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


class LaneContractError(ValueError):
    """A refusal: an input this generator declines to bake into a contract."""


# --- validation ---------------------------------------------------------------------------

def validate_effort(effort: str) -> str:
    """Return the effort tier, or raise `LaneContractError` naming the enum.

    A miss is a refusal rather than a guess — the posture the dispatch surface already
    takes, so a typo surfaces here instead of booting a lane at an effort nobody chose.
    """
    raw = (effort or "").strip()
    if raw not in EFFORT_ENUM:
        raise LaneContractError(
            f"effort {effort!r} is outside the enum {{{' | '.join(EFFORT_ENUM)}}} — "
            f"a miss is refused, never rounded to a neighbour")
    if raw not in DISPATCH_ROUTED_EFFORT:
        logger.warning(
            "effort %r is accepted by this generator but sits OUTSIDE the dispatch "
            "surface's closed enum {%s} (protocols/PLAYBOOK.md Ch8, 'Model + effort are "
            "stated at dispatch'); the emitted line is expected to be refused at dispatch",
            raw, " | ".join(sorted(DISPATCH_ROUTED_EFFORT)))
    return raw


def validate_model(model: str) -> str:
    """Return the model tier, or raise `LaneContractError` naming the enum."""
    raw = (model or "").strip()
    if raw not in MODEL_ENUM:
        raise LaneContractError(
            f"model {raw!r} is outside the enum {{{' | '.join(MODEL_ENUM)}}}")
    return raw


def validate_mode(mode: str) -> str:
    """Return the lane mode, or raise `LaneContractError` naming the enum."""
    raw = (mode or "").strip()
    if raw not in MODE_ENUM:
        raise LaneContractError(
            f"mode {raw!r} is outside the enum {{{' | '.join(MODE_ENUM)}}}")
    return raw


def validate_slug(slug: str, *, strict: bool = True) -> str:
    """Return the lane slug, or raise `LaneContractError`.

    `strict` (the default) applies the repo's own batch-lane grammar via
    `validate_branch_naming.validate_lane_worktree_name` — `lane-<letter>-<id>-<slug>` —
    rather than a second copy of it here. `strict=False` relaxes to hyphen-only kebab, for
    a non-batch worktree lane, whose name the same chapter allows to be a bare purpose slug.
    """
    raw = (slug or "").strip()
    if not raw:
        raise LaneContractError("empty lane slug")
    if not _KEBAB_RE.match(raw):
        raise LaneContractError(
            f"lane slug {raw!r} is not hyphen-only kebab-case — lowercase letters, digits "
            f"and single hyphens, no underscores and no leading/trailing/double hyphen")
    if strict:
        reason = validate_lane_worktree_name(raw)
        if reason is not None:
            raise LaneContractError(f"lane slug refused by the batch-lane grammar: {reason}")
    return raw


def contract_filename(slug: str) -> str:
    """The contract file paired 1:1 with `slug`. Hyphen-only, by construction.

    A leading `lane-` is dropped, so `lane-a-539-ch8` pairs with `LANE-a-539-ch8.md` rather
    than with a stuttering `LANE-lane-a-539-ch8.md`. This is the live convention, read off
    the pair this generator was itself dispatched under (`lane-539-ch8-codification` <->
    `LANE-539-ch8-codification.md`) rather than invented — and it stays a pure derivation,
    which is what lets `parse_contract` check the pairing rather than trust it.
    """
    stem = slug[len("lane-"):] if slug.startswith("lane-") else slug
    return f"LANE-{stem}.md"


def branch_name(slug: str) -> str:
    """The branch `claude --worktree <slug>` produces. Prefixed exactly ONCE — the batch-6
    doubled-prefix class this generator exists partly to remove."""
    return f"{BRANCH_PREFIX}{slug}"


# --- the emitted contract ------------------------------------------------------------------

@dataclass(frozen=True)
class LaneSpec:
    """Everything a contract needs that the generator cannot derive."""
    slug: str
    purpose: str
    repo: str = ".dev-knowledge"
    task_id: Optional[str] = None
    model: str = DEFAULT_MODEL
    mode: str = DEFAULT_MODE
    effort: str = "high"
    cloud: bool = False
    strict_slug: bool = True

    def validated(self) -> "LaneSpec":
        """Return a copy with every enum-bearing field checked. Raises `LaneContractError`."""
        return LaneSpec(
            slug=validate_slug(self.slug, strict=self.strict_slug),
            purpose=(self.purpose or "").strip() or "<one sentence — what this lane achieves>",
            repo=(self.repo or "").strip() or ".dev-knowledge",
            task_id=(self.task_id or "").strip() or None,
            model=validate_model(self.model),
            mode=validate_mode(self.mode),
            effort=validate_effort(self.effort),
            cloud=self.cloud,
            strict_slug=self.strict_slug,
        )

    @property
    def board_label(self) -> str:
        ident = f"#{self.task_id}" if self.task_id else self.slug
        return f"[{self.repo} · {ident} · {self.slug}]"


def render_contract(spec: LaneSpec) -> str:
    """Render one frozen lane contract. Pure — same spec in, byte-identical markdown out."""
    spec = spec.validated()
    fname = contract_filename(spec.slug)
    branch = branch_name(spec.slug)
    ident = f"[#{spec.task_id}]" if spec.task_id else f"`{spec.slug}`"

    parts: list[str] = []
    parts.append(f"# LANE {spec.slug} — {spec.purpose}\n")
    parts.append("| Model | Mode | Effort |")
    parts.append("|---|---|---|")
    parts.append(f"| {spec.model} | {spec.mode} | {spec.effort} |\n")

    parts.append("## Dispatch\n")
    parts.append("```")
    parts.append(f"Dispatch-Lane {spec.slug} {fname} -Effort {spec.effort}")
    parts.append("```\n")
    parts.append(
        f"The operator runs the line above verbatim. Dispatch constants ride it without being\n"
        f"re-decided: `{PERMISSION_MODE}`, `{BACKGROUND_FLAG}`, and the board label\n"
        f"`{spec.board_label}`. Model defaults to `{DEFAULT_MODEL}` — the `.dev-knowledge`\n"
        f"default per the Ch8 routing matrix — and this lane dispatches at `{spec.model}`.\n"
        f"Effort is a closed enum: {{{' | '.join(EFFORT_ENUM)}}}; a value outside it is refused\n"
        f"at the surface with the enum named, rather than guessed.\n")

    parts.append("## Worktree pairing\n")
    parts.append(
        f"slug `{spec.slug}` -> branch `{branch}` -> contract `{fname}`\n")
    parts.append(
        "One lane = one contract file = one worktree = one branch, so an open worktree resolves\n"
        "to the contract that created it and an orphan is attributable at a glance (ADR-110,\n"
        "fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag\n"
        "takes the bare lane name.\n")

    if spec.cloud:
        parts.append(f"## {CLOUD_SECTION}\n")
        parts.append(
            "This lane runs off-machine, so it carries a receipt "
            "(`protocols/STANDING_RULINGS.md` Q5).\nBoth fields, checked as a conjunction — "
            "either one alone reports a success the other refutes:\n")
        parts.append(f"- `{RECEIPT_FIELDS[0]}:` `<the resolved git source, non-empty>`")
        parts.append(f"- `{RECEIPT_FIELDS[1]}:` `<the session's first assistant text, echoed back>`\n")
        parts.append(
            "A dispatch missing either half is treated as not having started, and is\n"
            "re-dispatched. The lane also branches fresh off `origin/main` and leaves files it\n"
            "did not author and this contract does not name exactly as found (Q4).\n")

    parts.append("## Done-contract (immutable)\n")
    parts.append(f"1. `<what {ident} delivers — checkable, not aspirational>`")
    parts.append("2. `<the second done-when, or delete this line>`")
    parts.append("3. Docs and code in English; hyphen-only names; logging rather than print;\n"
                 "   Click for a CLI where one is warranted; `pytest` green.\n")

    parts.append("## Decision budget\n")
    parts.append(
        "**V-2 — this lane escalates on three classes only.** Everything else is decided per\n"
        "contract defaults and reported in the end packet rather than asked\n"
        "(`protocols/STANDING_RULINGS.md` \"The decision budget\"):\n")
    parts.append("- **(a)** curated-baseline touches")
    parts.append("- **(b)** genuine rule-vs-ruling conflicts")
    parts.append("- **(c)** fork classes with no standing ruling\n")
    parts.append(
        "A lane that discovers a refuted premise PAUSEs with the fact (Q10):\n"
        "deviation-with-disclosure is not a license — the disclosure discharges the reporting\n"
        "duty, it does not authorise the deviation.\n")

    parts.append("## Steps\n")
    parts.append("1. `<imperative — what is done>` **COMMIT**")
    parts.append("2. `<imperative>` **COMMIT**")
    parts.append("3. Final: `pytest` green, one end-of-lane artifact "
                 "(what changed · proposed diffs · open items), **COMMIT, then STOP.**\n")

    parts.append("## What NOT to do\n")
    parts.append("- No merges, no pushes to `main`, no touching another lane's branch — "
                 "commit-and-STOP;\n  integration is the integrator's act, from the primary checkout.")
    parts.append("- No JOURNAL entry — that is the integrator's surface "
                 "(`protocols/STANDING_RULINGS.md` P-1).")
    parts.append("- No index regeneration — the integrator is gate-of-record and regenerates once\n"
                 "  at the merge (Q1); a lane declares its single-hook bypass in the commit body.")
    parts.append("- No edits outside this lane's declared footprint.\n")

    return "\n".join(parts)


# --- parsing + checking ---------------------------------------------------------------------

@dataclass(frozen=True)
class ParsedContract:
    """What `parse_contract` recovers from an emitted contract. `problems` empty == valid."""
    sections: tuple[str, ...] = ()
    slug: Optional[str] = None
    contract_file: Optional[str] = None
    branch: Optional[str] = None
    effort: Optional[str] = None
    model: Optional[str] = None
    mode: Optional[str] = None
    receipt_fields: tuple[str, ...] = ()
    problems: tuple[str, ...] = field(default=())

    @property
    def ok(self) -> bool:
        return not self.problems


def parse_contract(text: str, *, expect_cloud: Optional[bool] = None) -> ParsedContract:
    """Parse a lane contract and report every problem found, rather than the first.

    `expect_cloud=None` (the default) infers cloud-ness from the presence of the receipt
    section, so a caller checking an unknown file does not have to know in advance.
    """
    problems: list[str] = []
    # Structure is read from the DE-FENCED text: a heading or an ask-class quoted inside an
    # example block is a mention, not a section (terra 2026-08-21, finding 1).
    prose = strip_fenced_blocks(text)
    sections = tuple(m.group("title") for m in _HEADING_RE.finditer(prose))

    # Matched by PREFIX, not equality: a heading may carry a trailing qualifier the emitter
    # writes and a reader relies on ("## Done-contract (immutable)"), and refusing that would
    # make the check reject the generator's own output.
    for required in MANDATORY_SECTIONS:
        if not any(s == required or s.startswith(required + " ") for s in sections):
            problems.append(f"missing mandatory section: '## {required}'")

    slug = contract_file = effort = None
    dispatch = _DISPATCH_LINE_RE.search(text)  # deliberately the FULL text — it lives in a fence
    if dispatch is None:
        problems.append(
            "no `Dispatch-Lane <slug> <file> [-Effort <tier>]` line found — the `## Dispatch` "
            "block carries the literal line, and the contract is its single source")
    else:
        slug = dispatch.group("slug")
        contract_file = dispatch.group("file")
        effort = dispatch.group("effort")
        # `-Effort` is optional in the dispatch GRAMMAR (the surface defaults it), but a frozen
        # contract states its own routing — an omitted tier is a contract that does not say what
        # it boots at, so it is reported rather than accepted (terra 2026-08-21, finding 3).
        if effort is None:
            problems.append(
                "dispatch line states no `-Effort <tier>` — a frozen contract carries its own "
                f"routing; enum {{{' | '.join(EFFORT_ENUM)}}}")
        elif effort not in EFFORT_ENUM:
            problems.append(
                f"dispatch line carries effort {effort!r}, outside "
                f"{{{' | '.join(EFFORT_ENUM)}}}")
        # The slug the dispatch line carries is validated, not merely echoed: a self-consistent
        # pair built on an off-grammar slug used to pass (terra 2026-08-21, finding 2). The bar
        # is hyphen-only kebab rather than the strict batch-lane grammar, because a non-batch
        # worktree lane's bare purpose slug is a legal name for this chapter.
        try:
            validate_slug(slug, strict=False)
        except LaneContractError as exc:
            problems.append(f"dispatch line carries an invalid lane slug: {exc}")
        if contract_file != contract_filename(slug):
            problems.append(
                f"dispatch line pairs slug {slug!r} with file {contract_file!r}; the 1:1 "
                f"pairing wants {contract_filename(slug)!r}")

    # The routing table is READ, not just emitted: an edited `| gpt | arbitrary | high |` row
    # used to pass unchallenged (terra 2026-08-21, finding 4).
    model = mode = None
    routing = _ROUTING_ROW_RE.search(prose)
    if routing is None:
        problems.append(
            "no `| model | mode | effort |` routing row found — the contract states the tier "
            "its lane boots at")
    else:
        model, mode = routing.group("model"), routing.group("mode")
        if model not in MODEL_ENUM:
            problems.append(
                f"routing row carries model {model!r}, outside {{{' | '.join(MODEL_ENUM)}}}")
        if mode not in MODE_ENUM:
            problems.append(
                f"routing row carries mode {mode!r}, outside {{{' | '.join(MODE_ENUM)}}}")
        row_effort = routing.group("effort")
        if row_effort not in EFFORT_ENUM:
            problems.append(
                f"routing row carries effort {row_effort!r}, outside "
                f"{{{' | '.join(EFFORT_ENUM)}}}")
        elif effort is not None and row_effort != effort:
            problems.append(
                f"routing row states effort {row_effort!r} but the dispatch line states "
                f"{effort!r} — two sources free to disagree is the class this generator removes")

    branch = None
    pairing = _PAIRING_RE.search(prose)
    if pairing is None:
        problems.append(
            "no worktree-pairing line found (slug -> branch -> contract)")
    else:
        branch = pairing.group("branch")
        p_slug = pairing.group("slug")
        if branch != branch_name(p_slug):
            problems.append(
                f"pairing line derives branch {branch!r} from slug {p_slug!r}; "
                f"expected {branch_name(p_slug)!r} — the prefix is applied exactly once")
        if slug is not None and p_slug != slug:
            problems.append(
                f"pairing line names slug {p_slug!r} but the dispatch line names {slug!r}")
        if contract_file is not None and pairing.group("file") != contract_file:
            problems.append(
                f"pairing line names contract {pairing.group('file')!r} but the dispatch "
                f"line names {contract_file!r}")

    is_cloud = CLOUD_SECTION in sections
    found_receipt = tuple(f for f in RECEIPT_FIELDS if f in prose)
    if expect_cloud is True and not is_cloud:
        problems.append(f"cloud lane expected, but no '## {CLOUD_SECTION}' section is present")
    if is_cloud:
        for missing in (f for f in RECEIPT_FIELDS if f not in found_receipt):
            problems.append(f"cloud lane is missing the receipt field: {missing}")
    elif expect_cloud is False and found_receipt:
        problems.append(
            "local lane carries receipt fields — the receipt gate is a cloud-lane rule (Q5)")

    for ask_class in ("(a)", "(b)", "(c)"):
        if ask_class not in prose:
            problems.append(f"decision budget is missing ask-class {ask_class}")

    return ParsedContract(
        sections=sections, slug=slug, contract_file=contract_file, branch=branch,
        effort=effort, model=model, mode=mode, receipt_fields=found_receipt,
        problems=tuple(problems))


# --- CLI --------------------------------------------------------------------------------------

def _default_out_dir() -> Path:
    return Path.cwd()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Emit and check batch-lane frozen contracts ([#539])."""


@cli.command("emit")
@click.option("--slug", required=True,
              help="lane worktree name, e.g. lane-a-539-ch8-codification")
@click.option("--purpose", required=True, help="one sentence — what this lane achieves")
@click.option("--repo", default=".dev-knowledge", show_default=True, help="repo display name")
@click.option("--id", "task_id", default=None, help="BACKLOG task id, digits only (e.g. 539)")
@click.option("--model", type=click.Choice(MODEL_ENUM), default=DEFAULT_MODEL, show_default=True)
@click.option("--mode", type=click.Choice(MODE_ENUM), default=DEFAULT_MODE, show_default=True)
@click.option("--effort", type=click.Choice(EFFORT_ENUM), default="high", show_default=True)
@click.option("--cloud/--local", default=False, show_default=True,
              help="a cloud lane carries the Q5 receipt-gate fields")
@click.option("--loose-slug", is_flag=True, default=False,
              help="relax the batch-lane grammar to bare hyphen-only kebab")
@click.option("--out-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help="directory to write into  [default: the current directory]")
@click.option("--stdout", "to_stdout", is_flag=True, default=False,
              help="render to stdout instead of writing a file")
@click.option("--force", is_flag=True, default=False, help="overwrite an existing contract")
def cmd_emit(slug: str, purpose: str, repo: str, task_id: Optional[str], model: str, mode: str,
             effort: str, cloud: bool, loose_slug: bool, out_dir: Optional[Path],
             to_stdout: bool, force: bool) -> None:
    """Emit one frozen lane contract."""
    spec = LaneSpec(slug=slug, purpose=purpose, repo=repo, task_id=task_id, model=model,
                    mode=mode, effort=effort, cloud=cloud, strict_slug=not loose_slug)
    try:
        text = render_contract(spec)
    except LaneContractError as exc:
        raise click.ClickException(str(exc)) from exc

    if to_stdout:
        click.echo(text)
        return

    target = (out_dir or _default_out_dir()) / contract_filename(spec.validated().slug)
    if target.exists() and not force:
        raise click.ClickException(
            f"{target} already exists — a frozen contract is not silently overwritten; "
            f"pass --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    logger.info("wrote %s", target)
    logger.info("dispatch with: Dispatch-Lane %s %s -Effort %s",
                spec.validated().slug, target.name, spec.validated().effort)


@cli.command("check")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--cloud/--local", "expect_cloud", default=None,
              help="assert the lane's substrate; omitted, it is inferred from the file")
def cmd_check(path: Path, expect_cloud: Optional[bool]) -> None:
    """Check an existing contract: every mandatory field present and internally consistent."""
    parsed = parse_contract(path.read_text(encoding="utf-8"), expect_cloud=expect_cloud)
    if parsed.ok:
        logger.info("%s: OK — %d sections, slug %s, branch %s",
                    path, len(parsed.sections), parsed.slug, parsed.branch)
        return
    for problem in parsed.problems:
        logger.error("%s: %s", path, problem)
    raise SystemExit(1)


@cli.command("enums")
def cmd_enums() -> None:
    """Print the baked-in enums — the checkable surface a contract author reads."""
    click.echo(f"effort (this generator): {' | '.join(EFFORT_ENUM)}")
    click.echo(f"effort (dispatch-routed): {' | '.join(sorted(DISPATCH_ROUTED_EFFORT))}")
    click.echo(f"model: {' | '.join(MODEL_ENUM)}   default: {DEFAULT_MODEL}")
    click.echo(f"mode: {' | '.join(MODE_ENUM)}   default: {DEFAULT_MODE}")
    click.echo(f"mandatory sections: {', '.join(MANDATORY_SECTIONS)}")
    click.echo(f"cloud-only section: {CLOUD_SECTION} ({', '.join(RECEIPT_FIELDS)})")
    click.echo(f"generated: {_dt.date.today().isoformat()}")


if __name__ == "__main__":
    cli()
