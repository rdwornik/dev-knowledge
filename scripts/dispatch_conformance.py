#!/usr/bin/env python
"""dispatch_conformance.py — the generator<->verb conformance probe (AX25-2, `[#675]` clause 1).

THE DEFECT THIS EXISTS TO CLOSE, in AX25-1's own words: *"the lane-launch path has two owners
and no conformance test between them. Every patch so far fixed one symptom of that seam. Rows
`[#716]` `[#717]` `[#718]` are symptoms, not the defect."* `[#740]` is the fourth symptom.

The two owners:

  * **the writer** — `scripts/gen_lane_contract.py`, which renders a contract's `## Dispatch`
    fenced block;
  * **the reader** — win-tooling's `scripts/dispatch/Invoke-Dispatch.ps1`, behind the ruled
    operator verb `dispatch <FILE.md>` (STANDING_RULINGS V1, PLAYBOOK Ch8's dispatch table).

Four symptoms accumulated on that seam while every individual check passed, because each check
looked at one half: `[#716]` base, `[#717]` model, `[#718]` contract location, `[#740]` fence.
**So this probe reports the four as ONE record and its witness asserts them in ONE assertion.**
Four separate assertions can each be made green against a different half of the seam, which is
precisely how four symptoms co-existed with a green suite.

WHAT THE FOUR PROPERTIES ARE, and each is a property of ONE artifact — the command line that
actually launches the lane:

  ``fence``     the `## Dispatch` block's head token is a program the reader will run.
                `Assert-ClaudeCommand` admits only `claude` — *"this script never runs an
                arbitrary command from a contract file"* — and that refusal is a deliberate
                safety property, not a bug to widen.
  ``location``  the reader resolves the contract by the BARE FILENAME the writer's own printed
                dispatch line carries, from the directory the writer wrote it to (`[#718]`).
  ``model``     the line carries `--model <the contract's declared model>` (`[#717]`): a line
                that drops it silently re-decides the most expensive constant on it.
  ``base``      the line carries `--worktree <slug>`, so the lane lands on `worktree-<slug>` —
                the ADR-110 pairing, and the name that carries the merge exemption (`[#716]`).

TIERS — MACHINE-DEPENDENCE IS DECLARED, NEVER SKIPPED. This is `dispatch_drift.py`'s ratified
posture and the reason is the same: *"a check that cannot compute its ground truth and renders
green is the defect this organ is made of"* (the 2026-08-25 green-by-skip sweep).

  ``TIER_HOST``      a PowerShell and the ruled verb both resolve here. The line under test is
                     the verb's REAL `-DryRun` resolution, and `fence` is the verb's own verdict.
  ``TIER_NO_VERB``   a PowerShell, but `dispatch` does not resolve (no win-tooling checkout).
  ``TIER_NO_SHELL``  no PowerShell at all — CI (`ubuntu-latest`), a container, a cloud lane.

On the two lower tiers the line under test is the contract's own fenced line and `fence` is
judged against `ADMISSION_HEAD_TOKEN`, a PINNED measurement carrying its locator and date.
**The coverage does not narrow; the EVIDENCE weakens, and the record says which it used.** All
four properties are computed on every tier, so the witness never skips and is RED today on a
bare Linux runner exactly as it is RED on the operator's Windows box.

HONEST LIMITS, stated so this does not overclaim:

  * The pin is a MEASUREMENT, not a live read. On `TIER_NO_VERB`/`TIER_NO_SHELL` a verb that
    changed its admission rule since `ADMISSION_MEASURED` would not be noticed here.
    `verify_admission_live()` is the leg that keeps the pin honest, and it runs on host only.
  * `location` is exercised by addressing the contract as a bare filename from the directory it
    was written to — `Resolve-ContractPath` tries the cwd-relative form FIRST. It therefore does
    NOT exercise the prompts-directory fallback, and deliberately: that path resolves the
    User-scope `CLAUDE_PROMPTS_DIR` authority, which on this fleet is a Google Drive mount that
    refuses by name when absent. A probe that wrote into the operator's real prompts directory
    to test a resolver would be a side effect, not a test.
  * A green here says the writer's line is one the reader ACCEPTS AND RESOLVES. It does not say
    the launched session does the right thing — no `claude` is ever spawned.

Layer-2 / read-only (ADR-28/36): renders a contract into a caller-supplied directory and asks a
local verb to resolve it with `-DryRun`. Drives no state in any repo.
"""
from __future__ import annotations

import logging
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch-conformance")

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import gen_lane_contract as glc
except ImportError:                                  # imported as `scripts.dispatch_conformance`
    from scripts import gen_lane_contract as glc     # type: ignore[no-redef]


# --- the pin ---------------------------------------------------------------------------------

#: The reader's admission rule. A PIN — measured against the live verb, carried with its locator
#: and its date, and re-measured by `verify_admission_live()` on any host that has the verb.
#: It is NOT a restatement of the verb's prose: the value below was read off a real refusal.
ADMISSION_HEAD_TOKEN = "claude"
ADMISSION_SOURCE = ("win-tooling scripts/dispatch/Invoke-Dispatch.ps1::Assert-ClaudeCommand "
                    "(line 285 at the time of measurement)")
ADMISSION_MEASURED = "2026-09-12"
#: The stable fragment of that refusal's text, used to tell an admission refusal apart from
#: every other way a dry run can fail (a missing file, an unmounted drive, a dead interpreter).
#: Matched as a SUBSTRING of the message, not as the whole message: the message interpolates the
#: offending token and is ASCII-folded on the way out.
ADMISSION_REFUSAL_MARK = "must invoke 'claude'"

#: Placeholder spellings that must NOT survive into a resolved line. The reader substitutes
#: exactly one literal (`$env:CLAUDE_PROMPTS_DIR`); anything else rides through into the
#: launched session's prompt as a path that does not exist. `<PROMPTS_DIR>` is listed by name
#: because it is the near-miss that actually happened: it is the INTERACTIVE shape's legitimate
#: prose placeholder, which the operator resolves by eye, and it reads as correct in a local
#: line right up to the moment a lane cannot find its own contract.
UNRESOLVED_PLACEHOLDER_MARKS: tuple[str, ...] = (
    "<PROMPTS_DIR>", "$env:CLAUDE_PROMPTS_DIR", "%CLAUDE_PROMPTS_DIR%", "${CLAUDE_PROMPTS_DIR}",
)

#: The ruled operator verb for a LOCAL lane (STANDING_RULINGS V1). Read from `dispatch_surface`
#: where that module can reach PLAYBOOK; this constant is the fallback for a caller probing
#: outside a checkout.
RULED_VERB = "dispatch"

TIER_HOST = "host"
TIER_NO_VERB = "no-verb"
TIER_NO_SHELL = "no-shell"

#: The four properties, in the order the symptom rows accumulated on them.
PROPERTIES: tuple[str, ...] = ("fence", "location", "model", "base")
#: What a conforming seam looks like. The witness asserts `properties() == CONFORMANT` — ONE
#: assertion over all four, which is AX25-2's shape clause rather than a style note.
CONFORMANT: dict[str, bool] = {p: True for p in PROPERTIES}

#: The verb's resolution line: `[dispatch] claude --bg --model opus … --worktree <slug> <prompt>`.
_RESOLVED_LINE_RE = re.compile(r"^\[dispatch\]\s+(?P<line>(?!source:)\S.*)$", re.MULTILINE)
#: The verb's provenance line. `contract` means the fenced block was used VERBATIM; `derived`
#: means it fell back to the Model/Effort table, which is a different mechanism wearing the same
#: output and must never read as a conforming fence.
_SOURCE_LINE_RE = re.compile(r"^\[dispatch\]\s+source:\s*(?P<source>.+?)\s*$", re.MULTILINE)
#: The head token of a `## Dispatch` fenced block, read from the contract itself.
_FENCE_BLOCK_RE = re.compile(r"^##\s*Dispatch\s*$.*?^```[^\n]*\n(?P<body>.*?)^```",
                             re.MULTILINE | re.DOTALL)

#: How long the verb gets to answer. A dry run spawns no `claude`; it reads one file. Generous
#: enough for a cold PowerShell start-up (~1 s) plus an unmounted-drive timeout, tight enough
#: that a wedge is a FAIL rather than an occupied machine.
VERB_TIMEOUT_S = 120


class DispatchConformanceError(RuntimeError):
    """A probe that could not be taken at all — a contract that would not render, a verb that
    could not be spawned. Raised, never degraded to an all-False record: an all-False record is
    what a genuinely non-conforming seam looks like, and the two must not be confusable."""


def head_token(line: str) -> str:
    """The program a command line names, normalised the way the reader normalises it.

    `Assert-ClaudeCommand` compares `GetFileNameWithoutExtension($head).ToLowerInvariant()`, so
    `claude`, `claude.cmd` and `C:\\…\\claude.exe` are the same program to it and `Dispatch-Lane`
    is not. Mirroring that normalisation is the point: a probe that compared raw strings would
    call a legitimate absolute-path invocation non-conforming.
    """
    stripped = line.strip()
    if not stripped:
        return ""
    # `posix=False`, and the choice is measured rather than stylistic: the reader tokenizes a
    # WINDOWS command line, where `C:\path\claude.exe` is a path and not an escape sequence.
    # POSIX lexing eats those backslashes and hands back a token no filesystem ever held. The
    # non-POSIX lexer keeps the surrounding quotes on the token, so they are stripped after.
    lexer = shlex.shlex(stripped, posix=False)
    lexer.whitespace_split = True
    try:
        head = next(iter(lexer), "")
    except ValueError:                               # an unterminated quote — the reader throws
        return ""                                    # on it too, so "no admissible head" is true
    return Path(head.strip('"\'')).stem.lower()


def fence_line(contract_text: str) -> str:
    """The single command line a contract's `## Dispatch` fenced block carries.

    Joined on whitespace exactly as `Get-DispatchBlockLine` joins it, so a block a future author
    wraps over two lines reads here the way it reads there."""
    match = _FENCE_BLOCK_RE.search(contract_text)
    if match is None:
        return ""
    lines = [ln.strip() for ln in match.group("body").splitlines() if ln.strip()]
    return " ".join(lines)


# --- host resolution -------------------------------------------------------------------------

def find_powershell() -> Optional[str]:
    """The PowerShell this host has, or None. `pwsh` first — the shell the dispatch helpers are
    deployed for — then `powershell` (5.1). Same order as `dispatch_drift.find_powershell`."""
    for exe in ("pwsh", "powershell"):
        found = shutil.which(exe)
        if found:
            return found
    return None


def verb_resolves(verb: str = RULED_VERB, *, shell: Optional[str] = None) -> bool:
    """Does the ruled verb resolve on this host?

    `Get-Command`, never `Get-Alias`: these verbs reach the session through PSModulePath
    AUTO-LOADING, which fires on command resolution. `Get-Alias` does not trigger it and reports
    a fully-working install as missing — measured on this fleet, 2026-09-12.
    """
    shell = shell or find_powershell()
    if shell is None:
        return False
    try:
        out = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-Command",
             f"if (Get-Command {verb} -ErrorAction SilentlyContinue) {{ 'OK' }} else {{ 'NO' }}"],
            capture_output=True, text=True, timeout=VERB_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError):
        return False
    return "OK" in (out.stdout or "")


def host_tier(*, shell: Optional[str] = None, verb: str = RULED_VERB) -> str:
    """Which tier this host is on. Declared, so a caller REPORTS it instead of skipping."""
    shell = shell or find_powershell()
    if shell is None:
        return TIER_NO_SHELL
    return TIER_HOST if verb_resolves(verb, shell=shell) else TIER_NO_VERB


# --- the probe -------------------------------------------------------------------------------

@dataclass(frozen=True)
class Probe:
    """One conformance measurement: the four properties, the artifact they were read off, and
    the evidence tier that produced it. ONE record, because the seam is one seam."""

    tier: str
    #: `verb` — the reader's own `-DryRun` resolution. `pin` — the contract's fenced line judged
    #: against `ADMISSION_HEAD_TOKEN`. Always stated; never inferred by a caller from the tier,
    #: because a host-tier probe whose verb crashed falls back to `pin` and must say so.
    evidence: str
    slug: str
    model: str
    effort: str
    contract_name: str
    contract_dir: str
    #: The contract's own `## Dispatch` fenced line — what the writer emitted.
    fence: str
    #: The line under test: the verb's resolution where there is one, else `fence`.
    line: str
    #: The verb's `source:` verdict (`contract` / `derived …`), or "" off host.
    source: str = ""
    #: The verb's refusal text, or "". Non-empty means the reader declined the writer's line.
    refusal: str = ""
    #: The verb's exit code, recorded rather than trusted — every `-DryRun` on this fleet exits
    #: 1 while printing a correct resolution (batch-x2 manifest §4, defect 2), so a caller that
    #: branched on it would read every success as a refusal.
    returncode: Optional[int] = None
    notes: tuple[str, ...] = field(default_factory=tuple)

    def properties(self) -> dict[str, bool]:
        """The four, as ONE dict — the shape AX25-2's single assertion compares."""
        return {
            "fence": self._fence_ok(),
            "location": self._location_ok(),
            "model": f"--model {self.model}" in self.line,
            "base": f"--worktree {self.slug}" in self.line,
        }

    def _fence_ok(self) -> bool:
        """The writer named a program the reader will run.

        On `verb` evidence this is the reader's OWN verdict twice over: no admission refusal,
        and `source: contract` — a `derived` source means the fenced block was not used at all,
        which is a fallback mechanism passing itself off as a conforming fence."""
        if head_token(self.fence) != ADMISSION_HEAD_TOKEN:
            return False
        if self.evidence != "verb":
            return True
        return not self.refusal and self.source.startswith("contract")

    def _location_ok(self) -> bool:
        """The contract is findable TWICE — by the reader, and then by the session it launches.

        Two legs, because `[#718]` has two ends and the first one alone is not the property:

          1. **the reader finds the contract** it was handed, addressed as the writer addresses
             it (a bare filename, from the directory the writer wrote to);
          2. **the resolved line carries no unsubstituted placeholder.** The reader replaces
             exactly one literal, `$env:CLAUDE_PROMPTS_DIR`. A line built on any other
             placeholder resolves, dry-runs plausibly, and launches a real session whose prompt
             names a path no filesystem holds.

        LEG 2 IS HERE BECAUSE ITS ABSENCE WAS MEASURED. On 2026-09-12 this probe went GREEN on
        a generator emitting the interactive shape's `<PROMPTS_DIR>` prose placeholder into the
        machine-read local line — a lane that would have booted and been unable to find its own
        contract. A conformance check that reads "the reader found the contract" and stops has
        not checked that the SESSION will.
        """
        if self.evidence == "verb":
            # DELIBERATELY NOT `bool(self.source)`. The reader prints `source:` only AFTER the
            # admission check, so keying leg 1 on it would make a fence refusal red this
            # property too — and four properties that fail together are one property wearing
            # four names, which is the opposite of what the single assertion is for. The reader
            # RESOLVING the path and then declining its contents are different answers, and
            # `Resolve-ContractPath` has its own refusal text for the former.
            found = self.returncode is not None and "not found" not in self.refusal.lower()
            return found and not self._unsubstituted_placeholders()
        return (Path(self.contract_dir) / self.contract_name).is_file() \
            and self.contract_name in self.fence

    def _unsubstituted_placeholders(self) -> list[str]:
        """Placeholder spellings still present in the RESOLVED line — every one of them a path
        the launched session cannot open. Empty when the line is fully resolved.

        Only meaningful on `verb` evidence: off host there is no resolved line to have
        substituted anything, so the contract's own fence legitimately still carries its token.
        """
        if self.evidence != "verb" or not self.line:
            return []
        return [p for p in UNRESOLVED_PLACEHOLDER_MARKS if p in self.line]

    @property
    def conforms(self) -> bool:
        return self.properties() == CONFORMANT

    def report(self) -> str:
        """Everything a reader needs to act, including why the answer is what it is."""
        props = self.properties()
        lines = [
            f"tier={self.tier} evidence={self.evidence} "
            f"(pin {ADMISSION_HEAD_TOKEN!r} measured {ADMISSION_MEASURED} from {ADMISSION_SOURCE})",
            f"contract: {self.contract_dir}/{self.contract_name}  "
            f"slug={self.slug} model={self.model} effort={self.effort}",
            f"fence:    {self.fence or '<none>'}",
            f"line:     {self.line or '<none>'}",
        ]
        if self.source:
            lines.append(f"source:   {self.source}")
        if self.refusal:
            mark = " (ADMISSION refusal — the fence seam, `[#740]`)" \
                if ADMISSION_REFUSAL_MARK in self.refusal else ""
            lines.append(f"refusal:  {self.refusal.strip()}{mark}")
        stranded = self._unsubstituted_placeholders()
        if stranded:
            lines.append(f"stranded: {', '.join(stranded)} survived into the RESOLVED line — "
                         f"the launched session's prompt names a path nothing holds "
                         f"(`[#718]`, leg 2)")
        if self.returncode is not None:
            lines.append(f"exit:     {self.returncode} (recorded, not trusted — see Probe.returncode)")
        lines.extend(f"note:     {n}" for n in self.notes)
        lines.append("properties: " + "  ".join(
            f"{p}={'OK' if props[p] else 'RED'}" for p in PROPERTIES))
        return "\n".join(lines)


def render_probe_contract(out_dir: Path, *, slug: str, model: str, effort: str,
                          purpose: str) -> Path:
    """Write one generator-emitted LOCAL contract into `out_dir`, and return its path.

    Goes through `gen_lane_contract.render_contract` — the generator itself, not a fixture of
    what it used to emit. A fixture would freeze the writer's half and the probe would then
    measure nothing when the writer moved, which is the seam all over again.

    `needs_base_sync=False` is pinned: the `[#716]` step-0 region is prose below the dispatch
    block and cannot change the line under test, while reading the LIVE base-ref property would
    make this probe's output depend on the checkout it happened to run in.
    """
    spec = glc.LaneSpec(slug=slug, purpose=purpose, repo=".dev-knowledge", task_id=None,
                        model=model, mode="execute", effort=effort, shape="local",
                        strict_slug=False, needs_base_sync=False)
    try:
        text = glc.render_contract(spec)
    except glc.LaneContractError as exc:
        raise DispatchConformanceError(
            f"the writer would not render a probe contract for slug {slug!r}: {exc}") from exc
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / glc.contract_filename(spec.validated().slug)
    target.write_text(text, encoding="utf-8", newline="\n")
    return target


def run_verb_dryrun(contract: Path, *, verb: str = RULED_VERB,
                    shell: Optional[str] = None) -> tuple[str, str, Optional[int]]:
    """`dispatch <bare filename> -DryRun`, from the contract's own directory.

    BARE FILENAME and `cwd=<the directory the writer wrote to>`, which is the `location`
    property under test: `Resolve-ContractPath` tries the cwd-relative form first, so this
    exercises the reader's resolution without touching the User-scope prompts-directory
    authority — a drive this fleet's reader refuses BY NAME when it is not mounted.

    Returns `(stdout, stderr, returncode)`. The exit code is returned for the record and is not
    interpreted: every `-DryRun` on this fleet exits 1 while printing a correct resolution.
    """
    shell = shell or find_powershell()
    if shell is None:
        raise DispatchConformanceError("no PowerShell on this host — probe at a lower tier")
    try:
        out = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-Command",
             f"& {verb} '{contract.name}' -DryRun"],
            cwd=str(contract.parent), capture_output=True, text=True,
            timeout=VERB_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise DispatchConformanceError(f"could not run {verb!r} via {shell}: {exc!r}") from exc
    return out.stdout or "", out.stderr or "", out.returncode


def probe(out_dir: Path, *, slug: str = "lane-probe-conformance", model: str = "sonnet",
          effort: str = "high", purpose: str = "probe the generator<->verb seam",
          tier: Optional[str] = None, shell: Optional[str] = None,
          verb: str = RULED_VERB) -> Probe:
    """Generate a contract and measure the four properties against the strongest evidence this
    host affords. Never skips; the tier and the evidence are on the record.

    `model` defaults to `sonnet` rather than the generator's own default, deliberately: a probe
    that asked for the default could not tell "the declared model reached the line" from "the
    line happens to carry the default", which is exactly the `[#717]` silence.
    """
    contract = render_probe_contract(Path(out_dir), slug=slug, model=model, effort=effort,
                                     purpose=purpose)
    fence = fence_line(contract.read_text(encoding="utf-8"))
    resolved_tier = tier or host_tier(shell=shell, verb=verb)
    notes: list[str] = []

    if resolved_tier != TIER_HOST:
        notes.append(f"tier {resolved_tier}: the ruled verb {verb!r} was NOT run here, so "
                     f"`fence` is judged against the pin rather than the reader's own verdict")
        return Probe(tier=resolved_tier, evidence="pin", slug=slug, model=model, effort=effort,
                     contract_name=contract.name, contract_dir=str(contract.parent),
                     fence=fence, line=fence, notes=tuple(notes))

    try:
        stdout, stderr, rc = run_verb_dryrun(contract, verb=verb, shell=shell)
    except DispatchConformanceError as exc:
        notes.append(f"the verb could not be spawned ({exc}); fell back to pin evidence")
        return Probe(tier=resolved_tier, evidence="pin", slug=slug, model=model, effort=effort,
                     contract_name=contract.name, contract_dir=str(contract.parent),
                     fence=fence, line=fence, notes=tuple(notes))

    source_m = _SOURCE_LINE_RE.search(stdout)
    resolved = [m.group("line") for m in _RESOLVED_LINE_RE.finditer(stdout)]
    # The refusal arrives on stderr as a PowerShell error record; keep it whole rather than
    # pattern-slicing it, so an UNEXPECTED failure mode is reported verbatim instead of being
    # silently reshaped into the one failure mode this probe knows the name of.
    refusal = stderr.strip()
    return Probe(
        tier=resolved_tier, evidence="verb", slug=slug, model=model, effort=effort,
        contract_name=contract.name, contract_dir=str(contract.parent), fence=fence,
        line=resolved[-1] if resolved else fence,
        source=source_m.group("source") if source_m else "",
        refusal=refusal, returncode=rc,
        notes=tuple(notes) + (() if resolved else
                              ("the verb printed no resolution line; the contract's own fence "
                               "is the line under test",)))


def verify_admission_live(out_dir: Path, *, shell: Optional[str] = None,
                          verb: str = RULED_VERB) -> list[str]:
    """Keep the PIN honest: does the reader still refuse a non-`claude` head token, by the name
    the pin records?

    This is pin MAINTENANCE, not the conformance measurement — a different subject, so it is a
    different leg. It plants a contract whose fence head is deliberately wrong and asserts the
    reader refuses it with `ADMISSION_REFUSAL_MARK`. Host-only by nature: there is nothing to
    re-measure where the reader is absent. Returns [] when the pin holds.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    planted = out_dir / "LANE-pin-probe.md"
    planted.write_text(
        "# LANE pin-probe — plant a non-`claude` head token and read the refusal\n\n"
        "## Dispatch\n\n**Shape:** `local`\n\n```\nNot-AClaudeCommand --bg --worktree x\n```\n",
        encoding="utf-8", newline="\n")
    try:
        _, stderr, _ = run_verb_dryrun(planted, verb=verb, shell=shell)
    except DispatchConformanceError as exc:
        return [f"the pin could not be re-measured: {exc}"]
    if ADMISSION_REFUSAL_MARK not in stderr:
        return [f"the reader no longer refuses a non-{ADMISSION_HEAD_TOKEN!r} head token with "
                f"{ADMISSION_REFUSAL_MARK!r} — the pin recorded {ADMISSION_SOURCE} on "
                f"{ADMISSION_MEASURED} and the reader has moved since. Re-measure the pin "
                f"before trusting any lower-tier verdict. Got: {stderr.strip()!r}"]
    return []


# --- the refusal leg -------------------------------------------------------------------------

#: The hub's half of the seam. The reader is `Invoke-Dispatch.ps1` in ANOTHER REPO, so this gate
#: cannot watch it — stated as a limit, not papered over: a change landing there is caught by
#: the next run on a host that has the verb, not at the commit that makes it.
SEAM_PATHS: tuple[str, ...] = (
    "scripts/gen_lane_contract.py",      # the writer
    "scripts/dispatch_conformance.py",   # this probe — a gate that cannot police its own edit
)                                        # is the self-disarm class `impacted-tests-guard` names


def staged_from_git(repo_root: Path | None = None) -> list[str]:
    """Repo-relative paths staged for this commit, read from git rather than from argv.

    NOT `pass_filenames`, and the reason is measured next door: a commit can edit one side of
    the seam AND narrow a `files:` regex in the same act, and pre-commit evaluates the STAGED
    config — so a filtered gate is disarmed by exactly the change it exists to inspect
    (`impacted-tests-guard`, reviewer HIGH 2026-09-11). This hook `always_run`s and computes
    its own scope.
    """
    root = repo_root or _SCRIPTS.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "diff", "--cached", "--name-only",
             "--diff-filter=ACMRT"],
            capture_output=True, text=True, check=True, timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def guard(repo_root: Path | None = None, *, out_dir: Path | None = None) -> tuple[int, str]:
    """AX25-2's refusal leg: *"a commit that changes either side and leaves the test red is
    refused."* Returns `(exit_code, message)`.

    A commit touching neither side of the seam returns immediately having probed nothing —
    the probe spawns a PowerShell and renders a contract, and paying that on every unrelated
    commit is how a gate gets bypassed rather than fixed.
    """
    staged = set(staged_from_git(repo_root))
    touched = sorted(p for p in SEAM_PATHS if p in staged)
    if not touched:
        return 0, "no seam file staged; nothing to check"

    import tempfile
    with tempfile.TemporaryDirectory(prefix="dispatch-conformance-guard-") as tmp:
        try:
            result = probe(Path(out_dir) if out_dir else Path(tmp))
        except DispatchConformanceError as exc:
            return 1, (f"REFUSED -- the probe could not be taken "
                       f"({exc}). A seam change that cannot be measured is not a seam change "
                       f"that passed.")
    if result.conforms:
        return 0, (f"PASS -- {', '.join(touched)} staged; fence, "
                   f"location, model and base all resolve ({result.evidence} evidence, "
                   f"tier {result.tier})")
    red = [p for p, ok in result.properties().items() if not ok]
    return 1, ("REFUSED -- this commit changes the seam "
               f"({', '.join(touched)}) and leaves it non-conforming on: {', '.join(red)}.\n"
               "AX25-2: the generator's line must be a line the ruled verb `dispatch "
               "<FILE.md>` resolves. Fix it, or the next batch freezes contracts that are "
               "refused at dispatch -- which is what this gate exists to stop recurring.\n"
               + result.report())


# --- CLI -------------------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    import argparse
    import tempfile

    parser = argparse.ArgumentParser(
        description="Generator<->verb dispatch conformance probe (AX25-2, `[#675]` clause 1). "
                    "Renders a lane contract and measures fence / location / model / base "
                    "against the ruled verb's DryRun.")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="where to render the probe contract [default: a temp dir]")
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--effort", default="high")
    parser.add_argument("--verify-pin", action="store_true",
                        help="also re-measure the reader's admission rule against the pin")
    parser.add_argument("--guard", action="store_true",
                        help="AX25-2's refusal leg: probe ONLY when a seam file is staged, "
                             "and exit 1 when the seam is left non-conforming")
    args = parser.parse_args(argv)

    if args.guard:
        code, message = guard(out_dir=args.out_dir)
        (logger.error if code else logger.info)("%s", message)
        return code

    with tempfile.TemporaryDirectory(prefix="dispatch-conformance-") as tmp:
        out_dir = args.out_dir or Path(tmp)
        try:
            result = probe(out_dir, model=args.model, effort=args.effort)
        except DispatchConformanceError as exc:
            logger.error("%s", exc)
            return 2
        print(result.report())
        failures = [p for p, ok in result.properties().items() if not ok]
        if args.verify_pin and result.tier == TIER_HOST:
            for drift in verify_admission_live(out_dir):
                logger.error("pin: %s", drift)
                failures.append("pin")
    if failures:
        logger.error("NON-CONFORMING: %s", ", ".join(failures))
        return 1
    logger.info("conforming on all four properties (%s evidence)", result.evidence)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
