#!/usr/bin/env python
"""dispatch_drift.py — the dispatch drift organ (`[#592]`, intake #52 I4, act 2 of 3).

THE DEFECT THIS EXISTS TO MAKE UNRECURRABLE. The hub documented FOUR rival launch commands
for one act, and `.claude/commands/lane-boot.md` — the surface a seat invokes most — emitted
the form Ch8 itself labels a fallback, silently dropping `--model` and `--effort`. Roughly
thirty consecutive browser seats failed to launch a lane: *"They were not uninformed; they
were informed by four sources that disagreed"* (`protocols/STANDING_RULINGS.md` section V).
Acts 2 and 3 fixed the pages. Nothing stopped them drifting again — section V's own closing
paragraph says so verbatim: *"The drift organ that would assert every literal command in Ch8
resolves via `Get-Command` on the operator's machine, and that `/lane-boot` names the ruled
verb, is owed and unbuilt; until it exists these rulings bind the seat and not the tree."*

This module is that organ. Two legs:

  1. **Ch8 → machine.** Every literal command in the dispatch table resolves via `Get-Command`
     on the operator's host.
  2. **`/lane-boot` → ruling.** `.claude/commands/lane-boot.md` contains the ruled verb
     (`dispatch`), and does not carry a rival launch form.

WHAT COUNTS AS A LITERAL COMMAND, measured rather than guessed. Two surfaces inside the
section `#### The dispatch table — the SOLE literal-command site`:

  * the FENCED command blocks under "Layer 2 — the commands, per substrate" — the lines Ch8
    tells a seat to copy verbatim (*"A seat copies one; it does not compose one"*). The first
    whitespace token of each fenced line is the command;
  * `Verb-Noun` tokens inside backtick spans in that section's prose — the PowerShell verbs
    named as fallbacks and session-management commands (`Dispatch-Local`, `Get-CloudSession`,
    `Stop-DispatchCodespace`, …). The Verb-Noun shape is the discriminator because it is
    PowerShell's own naming law, so it admits commands and rejects the flags, paths and field
    names sharing the same backtick decoration.

TWO DELIBERATE EXCLUSIONS, each because the section itself declares them not to be commands:

  * the interactive FIRST MESSAGE (`Read <PROMPTS_DIR>\\<FILE>.md and execute it exactly.`) —
    Ch8 says in terms *"the second line is its **first message**, not a shell command"*, and
    resolving `Read` against the host would be checking a chat sentence for a verb;
  * a fenced CONTINUATION line, whose first token is a parameter rather than a command. Both
    fall out of the command-shape filter rather than needing a name-list.

MACHINE-DEPENDENCE IS DECLARED, NOT SKIPPED — this is intake #52's open question 2, and the
requirement answers it: *"It is machine-dependent by design… it must not report green-by-skip."*

  * `TIER_HOST` — a PowerShell is on this machine. Commands are resolved for real; an
    unresolvable one is a **fail**.
  * `TIER_NO_SHELL` — no PowerShell (CI, a container, a cloud lane). The resolution leg reports
    a **warn** naming the tier and the commands it did NOT resolve.

`warn` and NOT `unavailable`, and the distinction is the whole point of the tier. `audit.py`'s
`_STATUS_LABEL` renders `unavailable` as "N/A", `_check_outcome` projects it onto `pass`, and
`cmd_ship_gate` blocks only on `fail` plus undispositioned `warn` — so an `unavailable`
detector SHIPS GREEN having measured nothing. That is the green-by-skip class swept on
2026-08-25 (`docs/audits/2026-08-25-technical-green-by-skip-sweep.md`), and a check whose whole
subject is machine-dependence would be its purest instance. Leg 2 is host-independent and runs
on every tier, so this organ never degrades to measuring nothing at all.

HONEST LIMITS:
  * It asserts a command RESOLVES, not that it BEHAVES. `Get-Command dispatch` succeeding says
    a `dispatch` exists on this PATH, not that it is win-tooling's `Invoke-Dispatch.ps1`.
  * The corpus is Ch8's dispatch-table SECTION. A literal command Ch8 grows in another section,
    or another doc grows anywhere, is outside this scan — which is sound only for as long as
    the "SOLE literal-command site" ruling holds, and this organ does not enforce that ruling.
  * `TIER_HOST` proves resolution ON THE MACHINE THAT RAN IT. A green here is not a claim about
    any other seat's machine.

Layer-2 / read-only (ADR-28/36): reads two files and asks the host about names. No writes.
"""
from __future__ import annotations

import logging
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable, Iterable

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch-drift")

PLAYBOOK_RELPATH = "protocols/PLAYBOOK.md"
LANE_BOOT_RELPATH = ".claude/commands/lane-boot.md"

#: The section heading that bounds the corpus, and the heading that ends it. Matched on the
#: heading TEXT rather than a line number: an anchor rots inside its own branch, and this file
#: is edited by every dispatch-doctrine act.
SECTION_START = "#### The dispatch table"
SECTION_END = "#### Standing operator-interface rules"

#: The ruled sole operator verb for a LOCAL lane (STANDING_RULINGS V1).
RULED_VERB = "dispatch"

#: Launch forms `/lane-boot` may not emit. V4: *"The raw `claude --bg` / `--worktree` form is
#: FALLBACK-ONLY. It does not appear in a command file or a template."* This is the exact
#: regression act 2 fixed, so it is the exact one worth a standing guard.
_RIVAL_FORM_RES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("the raw `claude --worktree` form", re.compile(r"claude\s+--worktree\b")),
    ("the raw `claude --bg` form", re.compile(r"claude\s+(?:-\S+\s+)*--bg\b")),
)

TIER_HOST = "host"
TIER_NO_SHELL = "no-shell"

_FENCE_BLOCK_RE = re.compile(r"^```.*?\n(?P<body>.*?)^```", re.MULTILINE | re.DOTALL)
#: A command token: an identifier or a PowerShell Verb-Noun. Anchored whole so a flag
#: (`-DryRun`), a bracketed parameter (`[-Machine`) or a path never reads as a command.
_COMMAND_TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*$")
#: A `Verb-Noun` opening a backtick span. The trailing class admits `` `Get-CloudSession` `` and
#: `` `Get-CloudSession cse_01ABC` `` alike — the live section writes both shapes.
_PROSE_VERB_NOUN_RE = re.compile(r"`([A-Z][a-z]+-[A-Za-z][A-Za-z0-9]*)(?=[ `])")
#: The interactive first message, declared by Ch8 as a chat message rather than a shell line.
_INTERACTIVE_MESSAGE_RE = re.compile(r"and execute it exactly\.\s*$")


class DispatchDriftError(RuntimeError):
    """A corpus this organ could not read or locate. Raised, never degraded to an empty scan —
    an empty scan reports zero drift, which is what a broken scan looks like."""


@dataclass(frozen=True)
class CommandRef:
    """One literal command, and where in the section it was found."""
    name: str
    surface: str          # "fence" | "prose"


@dataclass(frozen=True)
class Resolution:
    """The host's answer for one command."""
    name: str
    resolved: bool
    detail: str = ""


def dispatch_table_section(playbook_text: str) -> str:
    """The dispatch-table section's text.

    Raises when either boundary is absent: a heading rename is exactly the drift this organ
    exists to notice, and silently scanning the whole file (or nothing) would convert a
    structural change into a clean pass.
    """
    try:
        start = playbook_text.index(SECTION_START)
    except ValueError as exc:
        raise DispatchDriftError(
            f"{PLAYBOOK_RELPATH} carries no {SECTION_START!r} heading — the sole "
            f"literal-command site was renamed or removed") from exc
    end = playbook_text.find(SECTION_END, start)
    if end == -1:
        raise DispatchDriftError(
            f"{PLAYBOOK_RELPATH}: {SECTION_END!r} does not follow {SECTION_START!r} — the "
            f"section's end boundary was renamed or removed")
    return playbook_text[start:end]


def extract_commands(section: str) -> list[CommandRef]:
    """Every literal command the section declares, ordered, deduplicated by name.

    Fence lines first (the copy-verbatim surface), then prose Verb-Nouns.
    """
    seen: dict[str, CommandRef] = {}
    for fence in _FENCE_BLOCK_RE.finditer(section):
        for line in fence.group("body").splitlines():
            stripped = line.strip()
            if not stripped or _INTERACTIVE_MESSAGE_RE.search(stripped):
                continue
            token = stripped.split()[0]
            if _COMMAND_TOKEN_RE.match(token):
                seen.setdefault(token, CommandRef(token, "fence"))
    for match in _PROSE_VERB_NOUN_RE.finditer(section):
        seen.setdefault(match.group(1), CommandRef(match.group(1), "prose"))
    return list(seen.values())


# --- host resolution -----------------------------------------------------------------------

def find_powershell() -> str | None:
    """The PowerShell this host has, or None.

    `pwsh` first (PowerShell 7, the shell the dispatch helpers are deployed for), then
    `powershell` (5.1) — the same two the helpers are documented to resolve identically in.
    """
    for exe in ("pwsh", "powershell"):
        found = shutil.which(exe)
        if found:
            return found
    return None


def host_tier(shell: str | None = None) -> str:
    """Which tier this host is on. Declared, so a caller can report it rather than skip."""
    return TIER_HOST if (shell or find_powershell()) else TIER_NO_SHELL


def resolve_via_get_command(names: Iterable[str], *, shell: str | None = None,
                            timeout: int = 60) -> list[Resolution]:
    """Resolve every name in ONE `Get-Command` invocation.

    One invocation rather than N: a PowerShell start-up is ~0.5-1 s, and a per-command spawn
    would put this organ's cost on every commit at a multiple of the whole rest of the gate.
    Output is one `name<TAB>ok|MISSING` line per input, so a name that produces no line at all
    is reported UNRESOLVED rather than skipped.
    """
    names = list(names)
    if not names:
        return []
    shell = shell or find_powershell()
    if shell is None:
        raise DispatchDriftError("no PowerShell on this host — resolve at TIER_NO_SHELL instead")

    joined = ",".join(f"'{n}'" for n in names)
    script = (
        f"foreach ($n in @({joined})) {{ "
        f"$c = Get-Command $n -ErrorAction SilentlyContinue; "
        f"if ($c) {{ \"$n`t$($c.CommandType)\" }} else {{ \"$n`tMISSING\" }} }}")
    try:
        out = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", script],
                             capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise DispatchDriftError(f"could not run {shell}: {exc!r}") from exc

    answers: dict[str, str] = {}
    for line in (out.stdout or "").splitlines():
        if "\t" in line:
            name, _, verdict = line.partition("\t")
            answers[name.strip()] = verdict.strip()
    return [Resolution(n, answers.get(n, "MISSING") not in ("", "MISSING"),
                       answers.get(n, "no answer from Get-Command"))
            for n in names]


# --- the two legs --------------------------------------------------------------------------

@dataclass(frozen=True)
class DriftFinding:
    """One reported problem. `status` is `fail` or `warn` — never a green-rendering token."""
    status: str
    leg: str
    detail: str


def _fenced_and_prose(text: str) -> tuple[str, str]:
    """`(fenced text, prose text)` — the copyable surface and the narrating one.

    THE SPLIT IS LOAD-BEARING, and it is measured rather than stylistic. `/lane-boot` records
    its own history in prose: *"Until 2026-08-25 this line emitted a raw `claude --worktree …
    --bg …` form"*. That sentence is the reason the fix is legible, and a check that refused it
    would force deleting the explanation to satisfy the rule the explanation is about. Ch8
    draws the same line — *"A seat copies one; it does not compose one"* — so the fence is the
    surface a seat copies, and prose is the surface that explains.
    """
    fenced: list[str] = []
    prose = _FENCE_BLOCK_RE.sub(
        lambda m: fenced.append(m.group("body")) or "\n" * m.group(0).count("\n"), text)
    return "\n".join(fenced), prose


#: A supersession label. THE PREDICATE IS THE RULING'S OWN, not a taste call: V4 says the raw
#: form *"stays documented exactly once, in Ch8, **labelled as the fallback**"* — so labelling
#: is what separates a sanctioned record from a live instruction, and this is that word-set.
_SUPERSESSION_LABEL_RE = re.compile(
    r"fallback|supersed|deprecat|no longer|until \d{4}-\d{2}-\d{2}|previously|used to",
    re.IGNORECASE)
#: How far around a mention to look for its label — one paragraph either side, measured
#: generously rather than tightly, because a false WARN here would push an author to delete a
#: true historical note.
_LABEL_WINDOW = 400


def _is_labelled_mention(prose: str, at: int) -> bool:
    """Is this mention labelled as superseded/fallback within `_LABEL_WINDOW` characters?"""
    window = prose[max(0, at - _LABEL_WINDOW): at + _LABEL_WINDOW]
    return bool(_SUPERSESSION_LABEL_RE.search(window))


def check_lane_boot(lane_boot_text: str) -> list[DriftFinding]:
    """Leg 2 — host-independent, so this organ always measures something.

    Asserts the ruled verb is present as a standalone word in a FENCE (a command file names a
    command by showing it), and that no rival launch form is copyable from one. A rival form in
    PROSE is a **warn**, not a fail: it can still mislead a reader, so it is surfaced, but it is
    not a line anyone copies.
    """
    fenced, prose = _fenced_and_prose(lane_boot_text)
    verb_re = re.compile(rf"(?<![A-Za-z0-9-]){re.escape(RULED_VERB)}(?![A-Za-z0-9-])")
    out: list[DriftFinding] = []
    if not verb_re.search(fenced):
        out.append(DriftFinding(
            "fail", "lane-boot",
            f"{LANE_BOOT_RELPATH} shows no fenced command line carrying the ruled verb "
            f"{RULED_VERB!r} (STANDING_RULINGS V1) — the most-invoked boot surface in the "
            f"repo would hand a seat some other launch form"))
    for label, pattern in _RIVAL_FORM_RES:
        if pattern.search(fenced):
            out.append(DriftFinding(
                "fail", "lane-boot",
                f"{LANE_BOOT_RELPATH} carries {label} in a FENCE, i.e. as a line a seat "
                f"copies — STANDING_RULINGS V4 holds it FALLBACK-ONLY and out of every "
                f"command file and template"))
        else:
            for match in pattern.finditer(prose):
                if _is_labelled_mention(prose, match.start()):
                    continue
                out.append(DriftFinding(
                    "warn", "lane-boot",
                    f"{LANE_BOOT_RELPATH} mentions {label} in prose with no supersession "
                    f"label nearby — V4 keeps the raw form documented exactly once and "
                    f"*labelled as the fallback*, so an UNLABELLED mention in a command file "
                    f"reads as an instruction"))
    return out


def check_commands(commands: list[CommandRef], *, tier: str,
                   resolver: Callable[[Iterable[str]], list[Resolution]] | None = None,
                   ) -> list[DriftFinding]:
    """Leg 1 — Ch8's literal commands against the machine.

    `resolver` is injectable so a test can plant a dead command without a PowerShell, and so
    the tier decision stays the caller's rather than being re-derived here.
    """
    if not commands:
        return [DriftFinding(
            "fail", "commands",
            f"{PLAYBOOK_RELPATH}'s dispatch table declares NO literal command — the section "
            f"whose entire purpose is to be the sole literal-command site is empty, which "
            f"reads as zero drift and is not")]
    if tier != TIER_HOST:
        return [DriftFinding(
            "warn", "commands",
            f"tier {tier}: no PowerShell on this host, so {len(commands)} literal command(s) "
            f"were NOT resolved ({', '.join(c.name for c in commands)}) — reported rather "
            f"than skipped, because a check that cannot compute its ground truth and renders "
            f"green is the defect this organ is made of")]

    resolve = resolver or (lambda names: resolve_via_get_command(names))
    by_name = {c.name: c for c in commands}
    out: list[DriftFinding] = []
    for res in resolve([c.name for c in commands]):
        if res.resolved:
            continue
        ref = by_name.get(res.name)
        surface = ref.surface if ref else "unknown"
        out.append(DriftFinding(
            "fail", "commands",
            f"{PLAYBOOK_RELPATH} dispatch table names {res.name!r} ({surface}) and this host "
            f"cannot resolve it via Get-Command ({res.detail}) — a page naming a command the "
            f"machine does not have is how four rival verbs arose"))
    return out


def scan(repo_root: Path, *, tier: str | None = None,
         resolver: Callable[[Iterable[str]], list[Resolution]] | None = None,
         ) -> tuple[str, list[DriftFinding], list[CommandRef]]:
    """Both legs. Returns `(tier, findings, commands)`. Raises `DispatchDriftError` on a
    corpus it cannot read — an unreadable corpus is an error, not a clean scan."""
    root = Path(repo_root)
    try:
        playbook = (root / PLAYBOOK_RELPATH).read_text(encoding="utf-8")
    except OSError as exc:
        raise DispatchDriftError(f"could not read {PLAYBOOK_RELPATH}: {exc!r}") from exc
    try:
        lane_boot = (root / LANE_BOOT_RELPATH).read_text(encoding="utf-8")
    except OSError as exc:
        raise DispatchDriftError(f"could not read {LANE_BOOT_RELPATH}: {exc!r}") from exc

    commands = extract_commands(dispatch_table_section(playbook))
    resolved_tier = tier or host_tier()
    findings = check_commands(commands, tier=resolved_tier, resolver=resolver)
    findings.extend(check_lane_boot(lane_boot))
    return resolved_tier, findings, commands


# --- CLI -----------------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Dispatch drift organ — every literal command in PLAYBOOK Ch8's dispatch "
                    "table resolves on this machine, and /lane-boot names the ruled verb "
                    "([#592]).")
    parser.add_argument("--repo-root", type=Path,
                        default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--list", action="store_true",
                        help="print the extracted command corpus and exit")
    args = parser.parse_args(argv)

    try:
        if args.list:
            text = (args.repo_root / PLAYBOOK_RELPATH).read_text(encoding="utf-8")
            for ref in extract_commands(dispatch_table_section(text)):
                print(f"{ref.name}\t{ref.surface}")
            return 0
        tier, findings, commands = scan(args.repo_root)
    except DispatchDriftError as exc:
        logger.error("%s", exc)
        return 2

    for finding in findings:
        (logger.error if finding.status == "fail" else logger.warning)(
            "[%s] %s", finding.leg, finding.detail)
    if not findings:
        logger.info("tier %s: %d literal command(s) resolve; %s names the ruled verb %r",
                    tier, len(commands), LANE_BOOT_RELPATH, RULED_VERB)
    return 1 if any(f.status == "fail" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(_main())
