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

THE COMMAND LINE IS THE DELIVERABLE, AND SO IS ITS SHAPE (M10, lane L7, 2026-08-23).
`protocols/PLAYBOOK.md` Ch8 "Dispatching a session" names THREE dispatch shapes with three
different commands, and this generator selects between them from the contract's own declared
`shape`. Before that lane it emitted `Dispatch-Lane` UNCONDITIONALLY — `cloud` added a
receipt section and changed nothing else — so `emit --cloud` produced a cloud contract
carrying the LOCAL command, and `parse_contract` would have REFUSED the correct one. A lane
handed the wrong command is worse than a lane handed none, because a wrong command looks
authoritative; presence is therefore necessary and not sufficient, and the tests assert the
SELECTION rather than the presence.

WHAT IS BAKED IN, and each is asserted by a test rather than trusted:
  * the `## Dispatch` block: a declared `**Shape:**` line plus the ONE command line that
    shape takes — `claude --bg --model <m> --effort <e> --permission-mode bypassPermissions
    --worktree <slug> "Read and execute the frozen contract at
    $env:CLAUDE_PROMPTS_DIR\\<file>"` (local — and that token spelling is the one the reader
    substitutes, not the interactive shape's `<PROMPTS_DIR>` prose placeholder),
    `Dispatch-CloudV2 <file> -Title '<slug>'` (cloud), or `claude` plus its
    `Read <PROMPTS_DIR>\\<file> and execute it exactly.` first message (interactive) —
    with the dispatch constants STATED (`--permission-mode bypassPermissions`, `--bg`)
    and `opus` as the model default. **The local form is what the RULED VERB runs**
    (`[#675]` clause 1 / AX25-2): `dispatch <FILE.md>` executes the block verbatim and
    admits only a `claude` head token, so the `Dispatch-Lane` spelling this generator
    emitted until 2026-09-12 was refused by the very verb meant to launch it. That
    spelling stays ADMITTED by the checker for the already-frozen corpus and is no longer
    emitted;
  * the worktree <-> file pairing line (slug -> branch -> contract file), the 1:1 property
    ADR-110's fifth per-lane requirement asks for — with the branch DERIVED FROM THE SHAPE
    (`worktree-<slug>` local, `claude/<slug>` cloud per Ch8's cloud-lane section, and none
    at all for an interactive session, which runs in the primary checkout);
  * the V-2 decision budget, with its three ask-classes (a)/(b)/(c);
  * the receipt-gate fields for a cloud lane (STANDING_RULINGS Q5), emitted only for
    `--shape cloud`, since neither of the on-machine shapes has a receipt to carry.

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

[#630] LANDED here (lane-g-630, 2026-09-02): `cmd_check` gains the CONTRACT-MANIFEST
predicate (`_check_manifest_contract_agreement`), and `lane-contract-check` in
`.pre-commit-config.yaml` gains `always_run: true` + `pass_filenames: false` so the hook
runs on every commit rather than being Skipped on one touching zero `LANE-*.md` files. Both
witnessed live: the RED commit `522aadc7` shows the old "(no files to check) Skipped" line;
the very next commit `acd019dc`, touching zero `LANE-*.md` files, shows the same hook
line reading "Passed" instead — captured from real `pre-commit` output, not asserted.

END-OF-LANE VERIFICATION (Delta A2, contract text verbatim: "the set of failing nodeids
after your work must be a SUBSET of the committed base set"). Full suite measured twice at
`ee563973` against the committed base
(`docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`, 13 nodeids,
`1e064921`): the first pass (before `uv sync --locked --group analytics`) read 18
"regressions", all of them the known worktree-only noise class
(`lane-worktree-adds-two-suite-reds` — 17 `test_fleet_analytics.py` `ModuleNotFoundError`
from a fresh worktree venv lacking the analytics group, plus
`test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary`). After syncing
the group, ONE nodeid remained outside the base set:
`test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary`. Reproduced in
isolation: it fails because `aud._REPO_ROOT` (this worktree's own path) *is* a linked
worktree from `git worktree list`'s perspective — a structural property of running the
suite from inside ANY lane worktree, not of this diff. This exact nodeid is a STANDING
RULING, not a lane-local judgment call: `protocols/STANDING_RULINGS.md` "W2-reds ·
expected-RED lists are context-local" (2026-08-11) — "`test_linked_worktrees_reader_
excludes_the_primary` is worktree-context-only ... PASS on primary." Net regression count
against this lane's diff: ZERO. Two base failures additionally passed
(`tests/test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance`,
`::test_main_finding_json_exit_zero`) — not required by Delta A2, not claimed as this
lane's fix, reported because `failed_set.py --compare` surfaced them.
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
#: `[#630]` — the CONTRACT-MANIFEST predicate's pure comparison and open-batch resolver.
#: Imported BY NAME: no shadow-hole argument applies here the way it does for
#: `batch_manifest`'s own `LANE_BRANCH_RE` import — a shadowed `open_batches` would break
#: loudly (wrong shape / AttributeError), not silently widen an exemption. Imported by name
#: (rather than `import batch_manifest`) so `monkeypatch.setattr(glc, "open_batches", ...)`
#: reaches every call site in this module — the same reason `cmd_check`'s own tests patch it.
from batch_manifest import freeze_manifest_contract_agreement, open_batches  # noqa: E402
#: `[#718]` — THE ONE KEY for where a lane contract lives, imported rather than re-derived.
#: `Dispatch-Lane` takes a BARE FILENAME and resolves it against the operator's prompts
#: directory itself, so the writer's default and the verb's read have to be the same
#: resolution or the contract lands where nothing reads it — measured at batch scale: six
#: contracts written to `to-cc/`, six refused. `transport_root` is that resolution, already in
#: the tree and already tested (`CLAUDE_PROMPTS_DIR`, `~/Downloads` fallback, None when
#: unresolved). Imported BY NAME so this module has no second literal to drift from; a third
#: implementation here is exactly the defect `[#718]` records, one layer on.
from gen_handoff import transport_root  # noqa: E402
#: `[#716]` — THE STEP-0 SYNC RETIRES ITSELF. `worktree_seed` is the repo's worktree-
#: provisioning organ (live `graph_queries.py process-list`: "no trigger; ON-DEMAND-BY-OPERATOR,
#: invoked by /lane-boot"), and `base_ref_verdict` is its answer to "does a lane dispatched now
#: branch from `main` HEAD?". A contract's mandatory step-0 sync exists ONLY to paper over that
#: property being false, so the region is emitted from the predicate rather than typed into a
#: template by hand: it disappears the moment the property holds and comes back if the setting
#: is ever unset again. Retirement by mechanism, not by an editor remembering.
from worktree_seed import base_ref_verdict  # noqa: E402

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
#:
#: `opusplan` entered by RULING (AX22-3, 2026-09-12; re-ordered per-lane by the operator for
#: the wave-3 freeze, 2026-09-13), and the gap it closed is the same shape `codespace` closed
#: in `SHAPE_ENUM`. It is a SPLIT tier — Opus while the lane plans, Sonnet while it implements
#: — so it is a routing target the matrix's three tiers cannot spell, not a fourth point on the
#: same cost axis. It was ADMITTED AT THE SEAT and remained UNADMITTED IN THIS VOCABULARY,
#: which is a different admission and was not automatic: `to-browser/SEAT-BOOT-integrator.md`
#: has rendered `model: opusplan` since 2026-09-11, and `Dispatch-Lane` has always taken
#: `-Model` as an unconstrained `[string]` and handed it to `claude --model` verbatim. So the
#: live verb ran the tier while this module refused to state it — generator narrower than
#: verb, with no test between them, which is AX25-1's root cause in miniature.
#:
#: Admitted because the CLI RESOLVES it, not because a ruling named it: measured 2026-09-13,
#: `claude --print --model opusplan` returns a normal completion where a bogus id returns
#: `[claude-code:unrecognized_model]`. An enum that admitted an unresolvable string would move
#: the failure from freeze time to dispatch time, which is strictly worse.
MODEL_ENUM: tuple[str, ...] = ("opus", "opusplan", "sonnet", "haiku")
DEFAULT_MODEL = "opus"

#: Lane modes. `execute` is the work-lane default (plan-mode-by-exception — the contract
#: IS the plan; `templates/prompt-template.md` v1.14).
MODE_ENUM: tuple[str, ...] = ("execute", "plan-then-auto", "plan")
DEFAULT_MODE = "execute"

#: WHAT THE LANE'S WORK **IS** (`[#793]` clause 2) — the variable the routing default keys on,
#: and the one field in this vocabulary a generator cannot derive from the others.
#:
#: DECLARED, NEVER INFERRED, AND THERE IS DELIBERATELY NO DEFAULT. An inferred kind that is
#: wrong produces a refusal the author cannot act on: they declared nothing, so there is nothing
#: for them to correct, and the only remedy left is to argue with the gate. A missing
#: declaration is the one failure whose remedy is unambiguous — state the kind — which is why
#: absence is refused rather than defaulted. The inference that was available and rejected: read
#: the footprint out of the `## Steps` section and guess. It reads a draft, not a plan, and it
#: would have classified this very lane as `text` on its first paragraph.
#:
#: THREE VALUES, because the clause-2 table has three rows and a fourth would be this module
#: legislating. `text` is the contract's "text-only, deletion, read-only digest" row collapsed
#: to one token — the three share one routing answer, and splitting them would ask an author to
#: distinguish cases that route identically.
KIND_ENUM: tuple[str, ...] = ("text", "code", "review")

#: One line per kind, emitted beside the declared value so the contract says what the label
#: means without the reader going anywhere for it.
KIND_GLOSS: dict[str, str] = {
    "text": ("text-only, deletion, or read-only digest — prose, rows, rulings and removals; "
             "no executable code changes hands"),
    "code": "changes executable code — `scripts/`, `tests/`, hooks, schema, generators",
    "review": "judges work someone else produced — a diff, a design, an artifact",
}

#: The shapes that run UNATTENDED — every shape but `interactive`. Derived rather than listed a
#: second time: a shape added to `SHAPE_ENUM` is unattended unless it is the attended one, which
#: is the safe direction for a table whose whole job is refusing tiers nobody can supervise.
def unattended_shapes() -> tuple[str, ...]:
    """Every dispatch shape with nobody at the keyboard."""
    return tuple(s for s in SHAPE_ENUM if s != "interactive")

#: The four dispatch shapes `protocols/PLAYBOOK.md` Ch8 "Dispatching a session" names.
#: A shape is the SUBSTRATE a session runs on — deliberately NOT `MODE_ENUM`, which is how a
#: lane *thinks*. `MODE_ENUM` was the tempting hook here (it is already a declared enum on
#: the spec) and it is the wrong one: overloading it would make `plan` imply a substrate.
#:
#: `codespace` entered by RULING on 2026-08-31 (R-ENUM), and the gap it closed is worth the
#: comment. The substrate was ADMITTED FOR RUNNING that morning -- three legs green on a fresh
#: create -- and remained UNADMITTED IN THIS VOCABULARY, which is a different admission and was
#: not automatic. `validate_substrate` read `codespace` off `ecosystem/substrate-registry.yaml`
#: and ACCEPTED a contract this module REFUSED: two organs, one vocabulary, opposite verdicts,
#: which is exactly the split `[#514]` closed once already. A contract that passes the freeze
#: gate and fails the shape gate is the state that made both unenforceable.
SHAPE_ENUM: tuple[str, ...] = ("local", "cloud", "interactive", "codespace")
DEFAULT_SHAPE = "local"

#: One-line gloss per shape, emitted beside the declared `**Shape:**` value so the contract
#: says what the label means without the reader going to Ch8 for it.
SHAPE_GLOSS: dict[str, str] = {
    "local": "a background lane on the operator's machine, own worktree, commit-and-STOP",
    "cloud": "an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix",
    "interactive": "an operator-attended session — integration and seat acts live here",
    "codespace": ("an off-machine lane in the repo's own devcontainer, receipt-gated, "
                  "committing on the `worktree-` prefix like a local lane"),
}

#: Dispatch constants that ride every dispatch without being re-decided (Ch8).
PERMISSION_MODE = "--permission-mode bypassPermissions"
BACKGROUND_FLAG = "--bg"

#: The prompts-dir placeholder a dispatch line cites instead of a hard-coded absolute path
#: (Ch8, "Dispatch prompts and the contract of record"). Only the INTERACTIVE shape uses it:
#: cloud and codespace take a bare filename and resolve it against that directory themselves,
#: while an interactive first message is a chat message, so nothing expands a variable in it —
#: **the OPERATOR resolves this one by eye**, which is exactly why it is spelled as prose and
#: not as a shell expression.
PROMPTS_DIR_TOKEN = "<PROMPTS_DIR>"

#: THE OTHER PROMPTS-DIR TOKEN, and the two are not interchangeable — which is the whole
#: reason this constant exists rather than the one above being reused.
#:
#: The LOCAL form is read by a MACHINE, not by the operator: `dispatch <FILE.md>` performs
#: exactly one substitution on the `## Dispatch` block before running it, and the literal it
#: substitutes is `$env:CLAUDE_PROMPTS_DIR` (`Get-DispatchBlockLine`:
#: `$line.Replace('$env:CLAUDE_PROMPTS_DIR', $PromptsDir)`). Any other placeholder is passed
#: through UNTOUCHED, so a local line built on `<PROMPTS_DIR>` launches a real session whose
#: prompt names a path no filesystem holds — and it does so SILENTLY: the verb resolves, the
#: dry run prints a plausible line, and the lane boots and cannot find its own contract.
#:
#: Caught 2026-09-12 by `[#675]` clause 1's own probe going green on the wrong token, which is
#: why `dispatch_conformance.Probe._location_ok` now also asserts the resolved line carries NO
#: unsubstituted placeholder. A conformance check that reads "the reader found the contract"
#: and stops has not checked that the SESSION will.
READER_PROMPTS_DIR_TOKEN = "$env:CLAUDE_PROMPTS_DIR"

#: The branch a worktree name produces, via `claude --worktree <name>`.
BRANCH_PREFIX = "worktree-"

#: The branch prefix a CLOUD lane runs on (Ch8, "Cloud lanes"; CLAUDE.md §4's branch enum).
#: Emitting `worktree-` for a cloud lane declared a branch its own transport never creates.
#: A CODESPACE lane is the other way round and takes `BRANCH_PREFIX`: it commits and pushes
#: like a local lane, merely elsewhere, so `claude/` would name a branch nothing creates
#: (R-ENUM leg 3, 2026-08-31). Off-machine and cloud are not the same axis.
CLOUD_BRANCH_PREFIX = "claude/"

#: Mandatory headings every emitted contract carries. `--check` reads for exactly these.
MANDATORY_SECTIONS: tuple[str, ...] = (
    "Dispatch",
    "Worktree pairing",
    "Done-contract",
    "Decision budget",
    "Steps",
    "What NOT to do",
)

#: The extra section an OFF-MACHINE lane carries (STANDING_RULINGS Q5). The name is historical
#: -- the section is titled `Receipt gate` and the rule was written when `cloud` was the only
#: off-machine shape -- and it is kept rather than renamed because it is cited by that name from
#: `docs/audits/` and read by tests outside this module.
CLOUD_SECTION = "Receipt gate"

#: The two receipt fields a CLOUD lane carries, checked as a conjunction (Q5).
RECEIPT_FIELDS: tuple[str, ...] = ("git-source-resolves-non-empty", "first-assistant-text-echoed")

#: The shapes that carry a receipt gate: the OFF-MACHINE ones. Ch8's dispatch table states the
#: receipt for row 2 (cloud) and row 4 (codespace) in each row's own words, so keying this on
#: the literal string `cloud` was a rule written to one instance of its own class. A tuple, so
#: a fifth shape cannot be admitted without answering the question.
RECEIPT_SHAPES: tuple[str, ...] = ("cloud", "codespace")

#: The receipt FIELDS differ per shape, because the traps do. A codespace receipt is
#: `receipt.json` pulled back out of the container: `Ok` is the TRANSPORT's verdict and
#: `RemoteExitCode` is the WORK's -- gh's own code is 1 regardless, so a caller branching on
#: `Ok` alone reads a failed lane as a success -- and the receipt can carry a success `subtype`
#: while `is_error` is true, so `is_error` is the verdict field and `subtype` is the trap.
#: Both measured; both stated in Ch8 row 4 and in JOURNAL 2026-08-31 (k).
RECEIPT_FIELDS_BY_SHAPE: dict[str, tuple[str, ...]] = {
    "cloud": RECEIPT_FIELDS,
    "codespace": ("transport-ok-and-remote-exit-code-read-separately",
                  "is-error-false-not-subtype-success"),
}

#: Every receipt field any shape can carry, in a stable order -- what `parse_contract` reads a
#: contract's prose for before it knows which shape's set to demand.
ALL_RECEIPT_FIELDS: tuple[str, ...] = tuple(
    f for fields in RECEIPT_FIELDS_BY_SHAPE.values() for f in fields)

_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
#: `[#717]` WIDENED THIS, and the widening is half the fix rather than a convenience. Until
#: 2026-09-11 this read `^Dispatch-Lane <slug> <file>( -Effort <v>)?\s*$` — anchored, with NO
#: `-Model` alternative — so a line carrying the model was refused as "no dispatch command line
#: found". Rendering the model without widening here would have turned EVERY emitted contract
#: RED at `lane-contract-check`: a generator whose own parser rejects its output is worse than
#: one that omits the flag. `-Model` is OPTIONAL, and deliberately: every contract frozen before
#: `[#717]` carries a line without it, and making it mandatory would redden the whole existing
#: corpus. It trails `-Effort` because that is the order the generator emits; a reversed line is
#: refused rather than guessed at, which is the posture the rest of this module already takes.
_LEGACY_DISPATCH_LINE_RE = re.compile(
    r"^Dispatch-Lane\s+(?P<slug>\S+)\s+(?P<file>\S+)(?:\s+-Effort\s+(?P<effort>\S+))?"
    r"(?:\s+-Model\s+(?P<model>\S+))?\s*$",
    re.MULTILINE,
)

#: `[#675]` clause 1 / AX25-2: THE FORM THIS GENERATOR NOW EMITS, and the reason the seam
#: closed on this side rather than on the reader's.
#:
#: The ruled operator verb is `dispatch <FILE.md>` (STANDING_RULINGS V1, PLAYBOOK Ch8's
#: dispatch table). It reads the `## Dispatch` fence and runs it VERBATIM, and its
#: `Assert-ClaudeCommand` admits only a `claude` head token — *"this script never runs an
#: arbitrary command from a contract file"*. That refusal is a deliberate SAFETY property: a
#: `## Dispatch` block that could name any program is arbitrary execution from a file the
#: repo hands around. Widening it was the available alternative and is the wrong leg. So the
#: writer moved, and AX25-4 is satisfied by construction — no line of the retiring PowerShell
#: path was touched.
#:
#: THE LINE IS `Start-DispatchLane`'s OWN COMPOSITION, read off win-tooling's source rather
#: than invented here, so the verb path and the deprecated-alias path launch the same session:
#: `claude --bg --model <m> --effort <e> --permission-mode bypassPermissions --worktree <slug>
#: "Read and execute the frozen contract at <path>"`. `$env:CLAUDE_PROMPTS_DIR` is the ONE
#: token the reader substitutes (its own documented substitution), which is what lets a frozen
#: contract name its own location without hard-coding an absolute path.
#:
#: `--model` AND `--effort` ARE OPTIONAL *IN THE GRAMMAR*, EXACTLY AS `-Effort`/`-Model` ARE
#: ABOVE — and mandatory in what this generator EMITS. The distinction is the one terra finding
#: 3 already forced on the legacy form and it is mirrored rather than re-litigated: a pattern
#: that structurally required the flags would refuse a line missing one as *"no dispatch command
#: line found"*, which sends a reader hunting for a missing block instead of naming the missing
#: flag. Optional here, reported by name below — `parse_contract` carries the conjunctions, and
#: `_model_is_stated_by_the_emitted_form` adds the one `[#717]` needs for this form.
_CLAUDE_DISPATCH_LINE_RE = re.compile(
    r"^claude\s+--bg(?:\s+--model\s+(?P<model>\S+))?(?:\s+--effort\s+(?P<effort>\S+))?"
    r"\s+--permission-mode\s+bypassPermissions\s+--worktree\s+(?P<slug>\S+)"
    r'\s+"Read and execute the frozen contract at ' + re.escape(READER_PROMPTS_DIR_TOKEN)
    + r'\\(?P<file>[^"]+)"\s*$',
    re.MULTILINE,
)


class _EitherForm:
    """Two spellings of ONE shape's command line, read as one pattern.

    Python refuses a duplicate group name inside a single alternation, and both forms have to
    expose the same four groups (`slug`, `file`, `effort`, `model`) or every reader downstream
    would need a per-form branch — which is the two-owners-one-seam shape all over again, one
    layer down. So the alternation lives here instead, behind the `.search()` the readers
    already call.

    ORDER IS THE EMITTED FORM FIRST. Both patterns are anchored to a whole line and open on
    different tokens, so they cannot both match the same line; order decides only which is
    reported when a hand-edited contract carries both, and the emitted form is the right
    answer there.

    HONEST LIMIT: a contract carrying BOTH spellings reads as ONE local form here, so
    `parse_contract`'s "two dispatch command lines" refusal does not fire on it. That refusal
    guards two DIFFERENT SHAPES disagreeing (a cloud line in a local contract); two spellings
    of the same shape, pointing at the same slug and file, are not that class. A contract
    whose two spellings disagreed on slug, file, effort or model would be reported by the
    pairing and routing-row conjunctions below, which read whichever line matched.
    """

    def __init__(self, *patterns: re.Pattern[str]) -> None:
        self._patterns = patterns

    def search(self, text: str) -> "Optional[re.Match[str]]":
        for pattern in self._patterns:
            match = pattern.search(text)
            if match is not None:
                return match
        return None


#: The local form, either spelling. The legacy `Dispatch-Lane` spelling stays ADMITTED and
#: deliberately: every contract frozen before this change carries it, and a checker that
#: refused them would redden the whole existing corpus to make one new line legal — the same
#: reasoning `[#717]` used to keep `-Model` optional above. Admitted is not emitted; the
#: generator writes exactly one form.
_DISPATCH_LINE_RE = _EitherForm(_CLAUDE_DISPATCH_LINE_RE, _LEGACY_DISPATCH_LINE_RE)
#: The CLOUD command. `Dispatch-CloudV2` takes the brief as its first positional and the
#: session title as `-Title`; it has NO `-Effort` parameter, which is why the effort check
#: below is scoped to the local shape rather than dropped.
_CLOUD_DISPATCH_LINE_RE = re.compile(
    r"^Dispatch-CloudV2\s+(?P<file>\S+)\s+-Title\s+'(?P<slug>[^']+)'\s*$",
    re.MULTILINE,
)
#: The INTERACTIVE first message. Not a shell line — the operator sends it into a running
#: `claude` session — so it is matched as the sentence it is.
_INTERACTIVE_LINE_RE = re.compile(
    r"^Read\s+" + re.escape(PROMPTS_DIR_TOKEN) + r"\\(?P<file>\S+)\s+"
    r"and execute it exactly\.\s*$",
    re.MULTILINE,
)
#: The CODESPACE command (Ch8 dispatch table, row 4). The contract is shipped IN as a file and
#: so is the runner, so the line carries no quoted payload: a PowerShell string reaching a bash
#: login shell through gh's ssh transport is parsed twice, which is the failure class that
#: design exists to avoid. Only the two parameters a FROZEN contract must pin are emitted; the
#: machine, idle-timeout and retention flags are dispatch-time cost choices and freezing them
#: into a contract would state a spend the operator has not yet made.
_CODESPACE_DISPATCH_LINE_RE = re.compile(
    r"^Dispatch-Codespace\s+-Contract\s+(?P<file>\S+)\s+-Slug\s+(?P<slug>\S+)\s*$",
    re.MULTILINE,
)
#: The declared shape. Without it a checker cannot tell a correct command from a wrong one,
#: which is the whole property this generator exists to hold.
_SHAPE_LINE_RE = re.compile(r"^\*\*Shape:\*\*\s+`(?P<shape>[a-z]+)`", re.MULTILINE)

#: `[#793]`. Anchored at line start and fenced-token-only, for the reason `_SHAPE_LINE_RE`
#: records about itself: unanchored, a contract EXPLAINING the field mid-sentence wins the
#: precedence race over the real declaration further down.
_KIND_LINE_RE = re.compile(r"^\*\*Kind:\*\*\s+`(?P<kind>[a-z-]+)`", re.MULTILINE)

#: The command line for each shape, keyed so `find_command_line` and `parse_contract` read
#: ONE table rather than each carrying its own if-chain that could drift from the other.
_COMMAND_RES: dict[str, re.Pattern[str]] = {
    "local": _DISPATCH_LINE_RE,
    "cloud": _CLOUD_DISPATCH_LINE_RE,
    "interactive": _INTERACTIVE_LINE_RE,
    "codespace": _CODESPACE_DISPATCH_LINE_RE,
}

_PAIRING_RE = re.compile(
    r"slug\s+`(?P<slug>[^`]+)`\s*->\s*branch\s+`(?P<branch>[^`]+)`\s*->\s*contract\s+`(?P<file>[^`]+)`"
)
#: The interactive pairing: no lane branch exists to name, so naming one would be a claim the
#: tree never makes true. Cannot collide with `_PAIRING_RE` — that one requires `-> branch`
#: immediately after the slug, this one requires `-> contract`.
_PAIRING_NO_BRANCH_RE = re.compile(
    r"slug\s+`(?P<slug>[^`]+)`\s*->\s*contract\s+`(?P<file>[^`]+)`"
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


def validate_shape(shape: str) -> str:
    """Return the dispatch shape, or raise `LaneContractError` naming the enum.

    Same refusal posture as `validate_effort`: a miss names the enum and is never rounded to
    a neighbour. It matters more here than anywhere else in this module — rounding `remote`
    to `cloud`, or `worktree` to `local`, would emit a *confidently wrong* command, and that
    is strictly worse than emitting none.
    """
    raw = (shape or "").strip()
    if raw not in SHAPE_ENUM:
        raise LaneContractError(
            f"dispatch shape {shape!r} is outside the enum {{{' | '.join(SHAPE_ENUM)}}} — "
            f"a miss is refused, never rounded to a neighbour")
    return raw


def validate_mode(mode: str) -> str:
    """Return the lane mode, or raise `LaneContractError` naming the enum."""
    raw = (mode or "").strip()
    if raw not in MODE_ENUM:
        raise LaneContractError(
            f"mode {raw!r} is outside the enum {{{' | '.join(MODE_ENUM)}}}")
    return raw


def validate_kind(kind: "Optional[str]") -> str:
    """Return the lane kind, or raise `LaneContractError`. ABSENCE IS A REFUSAL (`[#793]`).

    The one validator here whose empty case is not a default. `validate_model` and friends
    answer "is this value in the enum"; this one answers that AND "was a value given at all",
    because clause 2's whole mechanism is a default keyed on the kind — and a generator that
    supplied the kind would be choosing the routing it exists to check.
    """
    raw = (kind or "").strip()
    if not raw:
        raise LaneContractError(
            f"the lane declares no KIND, and the routing default keys on it ([#793] clause 2) "
            f"— declare one of {{{' | '.join(KIND_ENUM)}}}. It is not inferred: a guessed kind "
            f"produces a refusal the author cannot act on, because they declared nothing to "
            f"correct")
    if raw not in KIND_ENUM:
        raise LaneContractError(
            f"lane kind {raw!r} is outside the enum {{{' | '.join(KIND_ENUM)}}} — "
            f"a miss is refused, never rounded to a neighbour")
    return raw


def background_inert_models() -> "dict[str, str]":
    """`{tier: why it is inert unattended}` — READ from the dispatch surface, never restated.

    The table is a recorded MEASUREMENT about the CLI and it lives where it was measured
    (`scripts/dispatch_surface.py`). Keeping a second copy here would be a second copy of a
    launch vocabulary, which is the precise defect the dispatch register's section V was ruled
    on. Imported lazily and in the same direction that module already reaches back into this
    one, so neither is load-order dependent.

    FAIL-LOUD on an unreadable surface. A table that degraded to `{}` would make this
    generator's most expensive refusal silently stop firing, which is the failure the refusal
    exists to prevent, arrived at from the other side.
    """
    try:
        from scripts import dispatch_surface as _ds  # noqa: PLC0415
    except ImportError:                              # pragma: no cover — path-shim fallback
        import dispatch_surface as _ds               # noqa: PLC0415
    return dict(_ds.BACKGROUND_INERT_MODELS)


def reviewer_cli() -> "Optional[str]":
    """The CLI the `reviewer` role routes to, READ from `ecosystem/routing-table.yaml`.

    THE AUTHORITY IS NOT RESTATED. Register ruling Z-G3 A2 puts role -> CLI in that file; this
    module holds the model TIER vocabulary and has no business holding a second opinion about
    which CLI runs a role. `provider-registry.yaml`'s `roles:` is a RANKING, not an authority,
    and is deliberately not consulted here — the two vocabularies differ (4 coarse vs 6 fine)
    on purpose and collapsing them makes one of them lie.

    `None` when the table cannot be read, and the refusal that uses it degrades to naming the
    FILE rather than the CLI. The refusal still fires: whether a review lane belongs on a
    `claude` dispatch line does not depend on this repo being able to open a YAML file.
    """
    try:
        from scripts import routing_agreement as _ra  # noqa: PLC0415
    except ImportError:                               # pragma: no cover — path-shim fallback
        import routing_agreement as _ra                # noqa: PLC0415
    try:
        roles, _ = _ra.load_table(Path(__file__).resolve().parents[1])
    except Exception:                                  # noqa: BLE001 — see the docstring
        return None
    clis = roles.get("reviewer") or []
    return clis[0] if clis else None


#: `ecosystem/routing-table.yaml`, named here so a refusal can cite the authority even when the
#: file cannot be opened. The PATH is a locator, not a second copy of the table's contents.
ROUTING_TABLE_REL = "ecosystem/routing-table.yaml"


def routing_refusals(*, model: str, kind: str, shape: str) -> list[str]:
    """Every way this (model, kind, shape) triple declares routing the launcher will not honour.

    `[]` when clean. PURE — no filesystem except `reviewer_cli`'s optional read, which only
    improves a message and never decides a verdict. Two clauses, kept as separate legs because
    they fail for unrelated reasons and a reader fixing one must not have to read the other:

    **Leg 1 — RESOLVE (clause 1).** A tier the BACKGROUND LAUNCHER cannot honour is refused
    HERE, at freeze, rather than passed through to evaporate at dispatch. `opusplan` is the
    measured case: a SPLIT tier that is Opus only while the session is in plan mode, on a lane
    whose `--permission-mode bypassPermissions` never enters one. Firing it literally does not
    honour the order either — it yields Sonnet, which no contract names — so there is no
    faithful-literal option, and the honest resolution is to refuse the token rather than
    preserve one that evaporates. The MEASUREMENT is on `local` (`lane-x-689`, 84 of 84
    assistant messages on `claude-sonnet-5`); the refusal extends to `cloud` and `codespace` by
    MECHANISM — every unattended shape carries the same permission mode by construction — and
    the extension is named here rather than smuggled. `interactive` keeps the tier: that seat
    can plan, and AX22-3 routes the integrator to it.

    **Leg 2 — the default by lane kind (clause 2).** A default that lives in a boot paste is a
    default a seat can not-read, so it lives where contracts are MADE. `text` never starts on
    Opus; `review` does not start on a `claude` dispatch line at all, because the reviewer role
    routes elsewhere; `code` is free to declare either half of the plan/implement split, and the
    emitted contract says in words that the split is TWO SESSIONS with a file between them
    rather than one session changing tier mid-flight — the prompt cache is keyed PER MODEL, and
    at this repo's measured context a single switch costs about 25 consecutive cheap turns to
    repay.

    THE TEXT-LANE REFUSAL SITS ON A RULE-VS-RULING CONFLICT AND SAYS SO. `protocols/PLAYBOOK.md`
    Ch8 makes `opus` the default for any arc touching `.dev-knowledge`, keyed on CONTEXT LOAD
    rather than diff size. Clause 2 narrows that for text-only lanes. A hub text-only lane is
    exactly where they disagree, which is escalation class (b) — so the refusal REPORTS the
    conflict at the point it fires instead of a winner being picked silently somewhere a reader
    would never look.
    """
    out: list[str] = []
    inert = background_inert_models()
    if shape in unattended_shapes() and model in inert:
        out.append(
            f"model {model!r} is REFUSED at freeze on the unattended shape {shape!r}: "
            f"{inert[model]} Declare a tier this launcher can honour — "
            f"{' or '.join(m for m in MODEL_ENUM if m not in inert)} — rather than a token that "
            f"evaporates between the contract and the run ([#793] clause 1, leg RESOLVE)")

    if kind == "text" and model in ("opus", "opusplan"):
        out.append(
            f"a {kind!r} lane (text-only, deletion, or read-only digest) declares {model!r}: "
            f"REFUSED at freeze ([#793] clause 2). The freeze is the last point at which "
            f"re-cutting is free, which is why this fires here and not at dispatch or at "
            f"review. Opus is a flat 2.5x Sonnet on BOTH legs (5.0/2.0 input, 25.0/10.0 "
            f"output) and both cache legs multiply the input rate, so the saving is 2.5x "
            f"regardless of token shape. CONFLICT, REPORTED RATHER THAN RESOLVED: "
            f"protocols/PLAYBOOK.md Ch8 'Model + effort are stated at dispatch' makes opus the "
            f"default for any arc touching `.dev-knowledge`, keyed on context load; clause 2 "
            f"narrows that for this kind. The two disagree on a hub text lane — escalation "
            f"class (b). Declare `sonnet` or `haiku`, or declare the kind honestly as `code`")

    if kind == "review":
        cli = reviewer_cli()
        names = f"routes the `reviewer` role to `{cli}`" if cli else "is the authority for it"
        out.append(
            f"a {kind!r} lane cannot be frozen on this dispatch line ([#793] clause 2). Every "
            f"shape this generator emits launches a `claude` session, and {ROUTING_TABLE_REL} "
            f"{names} (register ruling Z-G3 A2 — that file is the AUTHORITY for role -> CLI; "
            f"`provider-registry.yaml`'s `roles:` is a RANKING and is not consulted here). A "
            f"review is dispatched through the reviewer's own verb, not through a lane contract")
    return out


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


def branch_name(slug: str, shape: str = DEFAULT_SHAPE) -> Optional[str]:
    """The branch a lane of this `shape` runs on, or `None` when it has no lane branch.

    * `local` — `worktree-<slug>`, what `claude --worktree <slug>` produces. Prefixed exactly
      ONCE: the batch-6 doubled-prefix class this generator exists partly to remove.
    * `cloud` — `claude/<slug>`, the prefix Ch8's cloud-lane section and CLAUDE.md §4's branch
      enum both give a cloud session. Emitting `worktree-` here declared a branch the cloud
      transport never creates.
    * `codespace` — `worktree-<slug>`, the SAME prefix as a local lane (R-ENUM leg 3). A
      codespace lane commits and pushes like a local one, merely elsewhere, so `claude/` here
      would name a branch nothing creates. Off-machine and cloud are different axes, and this
      is the line where conflating them emits a wrong branch.
    * `interactive` — `None`. An operator-attended session runs in the primary checkout on an
      author-chosen branch, so there is nothing for the contract to declare, and inventing a
      name would be a claim the tree never makes true.

    The one-argument form keeps its old meaning (local), so every existing caller and the
    doubled-prefix regression test read exactly as they did.
    """
    shape = validate_shape(shape)
    if shape == "cloud":
        return f"{CLOUD_BRANCH_PREFIX}{slug}"
    if shape == "interactive":
        return None
    return f"{BRANCH_PREFIX}{slug}"


def dispatch_command(slug: str, contract_file: str, effort: str, shape: str,
                     model: str = DEFAULT_MODEL) -> str:
    """The literal command line for one shape — the single source both halves of this module
    read, so the emitter cannot write a form the parser will not accept.

    Returned WITHOUT a surrounding fence. For `interactive` the returned text is the first
    message only; `render_contract` emits the `claude` invocation above it, because the
    session has to exist before a message can reach it.

    `model` REACHES THE LOCAL LINE, and `[#717]` is why it has to. `Start-DispatchLane`'s
    `-Model` parameter defaults to `opus`; this function used to omit the flag. Neither half is
    wrong alone — together they meant a contract whose own routing row said `sonnet`, dispatched
    by the line that contract carries, ran at `opus`. The failure was silent and silent in the
    expensive direction: nothing refused and nothing warned, the lane produced entirely
    plausible work, and it announced itself only in the bill. A contract carrying its own launch
    line is making a promise about how it will run; a line that drops the model silently
    re-decides the most expensive constant on it.

    The three other shapes take no `-Model`: `Dispatch-CloudV2` and `Dispatch-Codespace` carry
    no such parameter (their tier is on the record in the routing row, as their `-Effort` is),
    and an interactive first message is a chat message rather than a command line. `model` is
    accepted for all four so callers have one signature, and is RENDERED only where a parameter
    exists to receive it — the same scoping `-Effort` already has.

    `[#675]` CLAUSE 1 / AX25-2 MOVED THE LOCAL FORM from `Dispatch-Lane <slug> <file> -Effort
    <e> -Model <m>` to the `claude --bg …` line the ruled verb will actually run, and the whole
    reason is that the two owners of this seam disagreed by construction: this generator wrote
    `Dispatch-Lane`, and `dispatch <FILE.md>` — the verb PLAYBOOK Ch8 rules as the sole
    operator verb for a local lane — admits only a `claude` head token. Every conforming local
    contract was refused by the verb meant to launch it, and four rows (`[#716]` `[#717]`
    `[#718]` `[#740]`) are symptoms of that one gap. `tests/test_dispatch_conformance.py` is
    the standing witness; `scripts/dispatch_conformance.py` is the probe.

    WHAT THE OPERATOR TYPES DOES NOT CHANGE: `dispatch LANE-<slug>.md`. What changed is the
    line the contract hands that verb. The composition is `Start-DispatchLane`'s own, read off
    win-tooling's source so the verb path and the deprecated `Dispatch-Lane` alias launch the
    same session rather than two that merely look alike.

    WHAT IS LOST, STATED RATHER THAN GLOSSED. `Start-DispatchLane` wraps its `claude` call in
    three guards — skip-if-branch-exists, an effort re-validation, and a branch-existence wait
    — and a line the verb runs verbatim gets none of them. The first is the one with teeth,
    and it is not unguarded: `seat_refusals`'s `lane-ceiling --check-worktrees` reads the live
    worktree list at STEP 0, before the first worktree exists, which is both earlier and
    broader than a per-dispatch branch check. The effort re-validation is redundant here (the
    generator holds the same closed enum, and `parse_contract` checks the emitted line against
    it). The wait is a convenience for a watching operator, not a property of the lane.
    """
    shape = validate_shape(shape)
    if shape == "cloud":
        return f"Dispatch-CloudV2 {contract_file} -Title '{slug}'"
    if shape == "interactive":
        return f"Read {PROMPTS_DIR_TOKEN}\\{contract_file} and execute it exactly."
    if shape == "codespace":
        return f"Dispatch-Codespace -Contract {contract_file} -Slug {slug}"
    return (f"claude {BACKGROUND_FLAG} --model {model} --effort {effort} {PERMISSION_MODE} "
            f"--worktree {slug} "
            f'"Read and execute the frozen contract at '
            f'{READER_PROMPTS_DIR_TOKEN}\\{contract_file}"')


def find_command_line(text: str) -> Optional[str]:
    """The dispatch command line a contract carries, or `None` when it carries none.

    Tries each shape's pattern and returns the first hit's matched text. Order does not
    matter: the three forms are disjoint by their opening token, so at most one can match a
    given line. `None` is the case M10 exists to close — a contract handed over with no
    command does not get started — and `parse_contract` turns it into a refusal.
    """
    for pattern in _COMMAND_RES.values():
        match = pattern.search(text)
        if match is not None:
            return match.group(0).strip()
    return None


# --- the emitted contract ------------------------------------------------------------------

@dataclass(frozen=True)
class LaneSpec:
    """Everything a contract needs that the generator cannot derive."""
    slug: str
    purpose: str
    repo: str = ".dev-knowledge"
    task_id: Optional[str] = None
    model: str = DEFAULT_MODEL
    #: `[#793]` clause 2. NO DEFAULT, and `validated()` refuses `None` — see `validate_kind`.
    #: A keyword field rather than a positional one so the dataclass's existing shape survives;
    #: what makes it mandatory is the validator, not the signature.
    kind: Optional[str] = None
    mode: str = DEFAULT_MODE
    effort: str = "high"
    shape: str = DEFAULT_SHAPE
    strict_slug: bool = True
    #: `[#716]`: emit the step-0 sync region. NOT a free choice — `cmd_emit` sets it from
    #: `base_ref_verdict`, so it tracks the live configuration. It stays a SPEC FIELD rather
    #: than a live read inside `render_contract` because rendering is pure by contract
    #: (`test_rendering_is_deterministic`), and a generator whose output depends on the state
    #: of the machine that ran it cannot be diffed.
    needs_base_sync: bool = False

    @property
    def cloud(self) -> bool:
        """Kept as a DERIVED read, not a second stored field.

        `cloud` used to be the stored flag, and it was the whole substrate model — which is
        why a cloud contract carried a local command. It survives as a property so the
        receipt-gate condition still reads in English, but there is exactly one source now
        and the two cannot disagree.
        """
        return self.shape == "cloud"

    def validated(self) -> "LaneSpec":
        """Return a copy with every enum-bearing field checked, AND its routing resolved.

        THE ROUTING REFUSAL FIRES HERE because every path that produces a contract goes through
        this method — `render_contract` calls it first thing, and `cmd_emit` calls it again for
        the line it echoes. A refusal placed on the CLI instead would be one a caller could
        route around by constructing a spec directly, which is how the last vocabulary gap
        (`opusplan` admitted at the seat, refused in this module) went unnoticed for two days.
        """
        refusals = self.routing_refusals()
        if refusals:
            raise LaneContractError("; ".join(refusals))
        return LaneSpec(
            slug=validate_slug(self.slug, strict=self.strict_slug),
            purpose=(self.purpose or "").strip() or "<one sentence — what this lane achieves>",
            repo=(self.repo or "").strip() or ".dev-knowledge",
            task_id=(self.task_id or "").strip() or None,
            model=validate_model(self.model),
            kind=validate_kind(self.kind),
            mode=validate_mode(self.mode),
            effort=validate_effort(self.effort),
            shape=validate_shape(self.shape),
            strict_slug=self.strict_slug,
            needs_base_sync=self.needs_base_sync,
        )

    def routing_refusals(self) -> list[str]:
        """This spec's clause-1 and clause-2 refusals. Enum-checked first, so a refusal never
        reports on a value that was not in the vocabulary to begin with."""
        return routing_refusals(model=validate_model(self.model),
                                kind=validate_kind(self.kind),
                                shape=validate_shape(self.shape))

    @property
    def board_label(self) -> str:
        ident = f"#{self.task_id}" if self.task_id else self.slug
        return f"[{self.repo} · {ident} · {self.slug}]"


def render_contract(spec: LaneSpec) -> str:
    """Render one frozen lane contract. Pure — same spec in, byte-identical markdown out."""
    spec = spec.validated()
    fname = contract_filename(spec.slug)
    branch = branch_name(spec.slug, spec.shape)
    ident = f"[#{spec.task_id}]" if spec.task_id else f"`{spec.slug}`"

    parts: list[str] = []
    parts.append(f"# LANE {spec.slug} — {spec.purpose}\n")
    parts.append("| Model | Mode | Effort |")
    parts.append("|---|---|---|")
    parts.append(f"| {spec.model} | {spec.mode} | {spec.effort} |\n")

    command = dispatch_command(spec.slug, fname, spec.effort, spec.shape, spec.model)

    parts.append("## Dispatch\n")
    parts.append(f"**Shape:** `{spec.shape}` — {SHAPE_GLOSS[spec.shape]}.\n")
    parts.append(f"**Kind:** `{spec.kind}` — {KIND_GLOSS[spec.kind]}.\n")
    parts.append(
        f"The kind is DECLARED, not inferred, and it is what the routing default keys on\n"
        f"(`[#793]` clause 2). A text-only, deletion or read-only-digest lane never starts on\n"
        f"Opus; a review lane is not dispatched from a lane contract at all, because\n"
        f"`{ROUTING_TABLE_REL}` is the authority for which CLI runs that role; a code lane\n"
        f"plans on Opus and implements on Sonnet **as two sessions with a file between them**,\n"
        f"never as one session changing tier mid-flight. The prompt cache is keyed PER MODEL,\n"
        f"so a mid-session switch re-writes the whole context: at this repo's measured mean of\n"
        f"232,875 tokens per call, one switch costs USD 1.46 into Opus or USD 0.58 into Sonnet\n"
        f"against USD 0.0812 saved per turn moved — about 25 consecutive cheap turns to repay\n"
        f"one round trip. Anything shaped like plan-then-execute is TWO SESSIONS.\n")
    parts.append("```")
    if spec.shape == "interactive":
        # The session has to exist before a message can reach it, so both halves are
        # emitted. Handing over the message alone is the M10 failure in miniature.
        parts.append("claude")
    parts.append(command)
    parts.append("```\n")

    if spec.shape == "local":
        parts.append(
            f"**The operator does NOT type the line above.** He types\n"
            f"`dispatch {fname}` **from the target repo root** — the ruled verb for a local\n"
            f"lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb\n"
            f"reads this `## Dispatch` block and runs it **verbatim**, substituting exactly\n"
            f"one literal — `{READER_PROMPTS_DIR_TOKEN}` — which is how a frozen contract\n"
            f"names its own location without hard-coding an absolute path. That spelling is\n"
            f"load-bearing: it is the only token the reader replaces, and any other\n"
            f"placeholder is passed through untouched into a real session's prompt.\n"
            f"The repo root still matters: the worktree\n"
            f"is created relative to the current repo, so dispatching from the wrong one\n"
            f"lands the lane in it.\n\n"
            f"The line carries every dispatch constant rather than defaulting it:\n"
            f"`{PERMISSION_MODE}` (a `{BACKGROUND_FLAG}` lane has nobody to answer a\n"
            f"permission prompt, so a default would stall it silently), `{BACKGROUND_FLAG}`,\n"
            f"and `--worktree {spec.slug}` — the name that produces `{branch}` and with it\n"
            f"the ADR-110 pairing and the merge exemption. Board label `{spec.board_label}`.\n"
            f"**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the\n"
            f"routing table above, so this lane dispatches at `{spec.model}` whatever any\n"
            f"surface default (`{DEFAULT_MODEL}`, the `.dev-knowledge` default per the Ch8\n"
            f"routing matrix) happens to be. A line that omitted it would silently re-decide\n"
            f"the most expensive constant on it. Effort is a closed enum:\n"
            f"{{{' | '.join(EFFORT_ENUM)}}}; a value outside it is refused with the enum named,\n"
            f"rather than guessed.\n\n"
            f"**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /\n"
            f"AX25-2). The verb refuses any other program — *\"this script never runs an\n"
            f"arbitrary command from a contract file\"* — so a contract's `## Dispatch` block\n"
            f"is not a place to name a helper. Until 2026-09-12 this generator emitted the\n"
            f"deprecated `Dispatch-Lane` alias here and **every contract it produced was\n"
            f"refused by the verb meant to launch it**. That alias still resolves as the\n"
            f"manual fallback and adds a skip-if-`{branch}`-exists guard the verb path does\n"
            f"not have; that guard's job is done earlier and more broadly at STEP 0 by\n"
            f"`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree\n"
            f"list before the first worktree exists.\n")
    elif spec.shape == "cloud":
        parts.append(
            f"The operator runs the line above verbatim. The **whole file is the brief** — it\n"
            f"travels in a JSON body, so one file is one lane and never a multi-lane bundle —\n"
            f"and the dispatch binds Revision `main`. `Dispatch-CloudV2` carries no `-Effort`\n"
            f"parameter, so this lane's tier is on the record in the routing table above\n"
            f"(`{spec.model}` / `{spec.effort}`) rather than on the command line. Permission\n"
            f"mode is `{PERMISSION_MODE.split()[-1]}`, as it is for an on-machine lane.\n"
            f"A cloud session clones from `origin`, so every input this contract names is\n"
            f"pushed before dispatch: it cannot see an unpushed branch or a local file.\n")
    elif spec.shape == "codespace":
        parts.append(
            f"The operator runs the line above verbatim. The contract is shipped IN **as a\n"
            f"file**, and so is the runner: nothing on the ssh command line is a quoted\n"
            f"payload, because a PowerShell string reaching a bash login shell through gh's\n"
            f"transport is parsed twice. Tier is on the record in the routing table above\n"
            f"(`{spec.model}` / `{spec.effort}`) — `Dispatch-Codespace` carries no `-Effort`.\n"
            f"Permission mode is `{PERMISSION_MODE.split()[-1]}`, as on every substrate.\n"
            f"**The container is CREATED, never rebuilt** (ruling 2026-08-31): a rebuilt\n"
            f"container has not applied its own `devcontainer.json` — no features, no\n"
            f"`postCreateCommand`, a stale clone — while a fresh create from the same HEAD\n"
            f"applies all of it. The clone starts at `origin`, so every input this contract\n"
            f"names is pushed before dispatch. Cost flags (`-Machine`, `-IdleTimeout`,\n"
            f"`-Retention`) are the operator's at dispatch and are deliberately not frozen\n"
            f"here; board label `{spec.board_label}`.\n")
    else:
        parts.append(
            f"`claude` starts the session; the second line is its **first message**, not a\n"
            f"shell command. `{PROMPTS_DIR_TOKEN}` is the prompts directory\n"
            f"(`$env:CLAUDE_PROMPTS_DIR`, `~\\Downloads` by default) — the operator resolves it\n"
            f"by eye here, because a chat message is not a shell and nothing expands the\n"
            f"variable for him. This shape exists for the acts a background lane cannot\n"
            f"perform: integration needs an operator GO per merge, and a `{BACKGROUND_FLAG}`\n"
            f"session can neither merge to `main` nor ask a question. Tier on the record above\n"
            f"(`{spec.model}` / `{spec.effort}`); board label `{spec.board_label}`.\n")

    parts.append("## Worktree pairing\n")
    if branch is None:
        parts.append(f"slug `{spec.slug}` -> contract `{fname}`\n")
        parts.append(
            "**No lane branch.** An interactive session runs in the primary checkout on an\n"
            "author-chosen branch, so there is no `worktree-` or `claude/` name for this\n"
            "contract to declare — and declaring one would be a claim the tree never makes\n"
            "true. The 1:1 property ADR-110's fifth per-lane requirement asks for still holds\n"
            "on the pair that exists: one contract file, one session.\n")
    else:
        parts.append(
            f"slug `{spec.slug}` -> branch `{branch}` -> contract `{fname}`\n")
        if spec.shape == "local":
            prefix_note = (
                "The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane\n"
                "name.\n")
        elif spec.shape == "codespace":
            prefix_note = (
                "A codespace lane runs on `worktree-`, the SAME prefix as a local lane and not\n"
                "the cloud transport's `claude/`: it commits and pushes like a local lane,\n"
                "merely elsewhere, so `claude/` would name a branch nothing creates (R-ENUM\n"
                "leg 3, 2026-08-31). Off-machine and cloud are different axes.\n")
        else:
            prefix_note = (
                "A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created\n"
                "by the cloud transport, not by a local worktree provisioner.\n")
        parts.append(
            "One lane = one contract file = one branch, so an open lane resolves to the\n"
            "contract that created it and an orphan is attributable at a glance (ADR-110,\n"
            f"fifth per-lane requirement). {prefix_note}")

    if spec.shape in RECEIPT_SHAPES and spec.shape == "codespace":
        parts.append(f"## {CLOUD_SECTION}\n")
        fields = RECEIPT_FIELDS_BY_SHAPE["codespace"]
        parts.append(
            "This lane runs off-machine in the repo's own devcontainer, so it carries a receipt\n"
            "(`protocols/STANDING_RULINGS.md` Q5) — `receipt.json`, pulled back out. Both\n"
            "fields, checked as a conjunction — either one alone reports a success the other\n"
            "refutes:\n")
        parts.append(f"- `{fields[0]}:` `<Ok=…, RemoteExitCode=…, read separately>`")
        parts.append(f"- `{fields[1]}:` `<is_error, verbatim from receipt.json>`\n")
        parts.append(
            "`Ok` is the TRANSPORT's verdict and `RemoteExitCode` is the WORK's: gh's own exit\n"
            "code is 1 regardless, so a caller branching on `Ok` alone reads a failed lane as a\n"
            "success. And a receipt can carry a success `subtype` while `is_error` is true, so\n"
            "`is_error` is the verdict field and `subtype` is the trap — a consumer keying on\n"
            "`subtype` records a successful run of an agent that never ran. A dispatch missing\n"
            "either half is treated as not having started, and is re-dispatched into a FRESH\n"
            "container (created, never rebuilt).\n")
    elif spec.cloud:
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

    # `[#716]`: emitted ONLY while a lane's base is not guaranteed to be `main` HEAD. The region
    # papers over a live defect, so it is conditioned on that defect rather than typed into a
    # template — it retires itself when the property starts holding, and restores itself if the
    # setting is ever unset again. `cmd_emit` sets the flag from `worktree_seed.base_ref_verdict`;
    # this function stays pure.
    if spec.needs_base_sync:
        parts.append("## Step 0 — sync before anything else "
                     "(MANDATORY while `[#716]` is unfixed)\n")
        parts.append(
            "`worktree.baseRef` does not currently guarantee that a lane branches from `main`\n"
            "HEAD, so this lane may start behind. **The step-0 sync is mandatory and may not be\n"
            "dropped on the grounds that `[#716]` is being fixed** — it retires only when the\n"
            "property holds, and this section stops being emitted at that moment. A generator\n"
            "run against a base that lags `main` silently DROPS rows that exist on `main`, and\n"
            "the dropped row looks like a clean regeneration.\n")
        parts.append("```")
        parts.append("git fetch origin")
        parts.append("git merge origin/main        # or: git merge main, from the primary's ref")
        parts.append("uv run --locked python -c \"print('base synced')\"")
        parts.append("```\n")
        parts.append("Then, and only then, run the lane's own steps.\n")

    return "\n".join(parts)


# --- parsing + checking ---------------------------------------------------------------------

@dataclass(frozen=True)
class ParsedContract:
    """What `parse_contract` recovers from an emitted contract. `problems` empty == valid."""
    sections: tuple[str, ...] = ()
    slug: Optional[str] = None
    contract_file: Optional[str] = None
    branch: Optional[str] = None
    shape: Optional[str] = None
    command: Optional[str] = None
    effort: Optional[str] = None
    model: Optional[str] = None
    mode: Optional[str] = None
    #: `[#793]` — the declared lane kind, or None when the contract declares none (reported).
    kind: Optional[str] = None
    receipt_fields: tuple[str, ...] = ()
    problems: tuple[str, ...] = field(default=())

    @property
    def ok(self) -> bool:
        return not self.problems


def parse_contract(text: str, *, expect_shape: Optional[str] = None) -> ParsedContract:
    """Parse a lane contract and report every problem found, rather than the first.

    `expect_shape=None` (the default) takes the shape from the contract's own `**Shape:**`
    line, so a caller checking an unknown file does not have to know in advance. Passing one
    asserts the substrate — the check the `lane-contract-check` hook does not make, because
    at commit time nothing outside the file says what shape it was meant to be.
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

    # --- the declared shape, and the command line it selects -------------------------------
    # Read the shape FIRST: without it a checker can see that a command line is present but
    # not that it is the right one, and a lane handed the wrong command is worse than a lane
    # handed none, because a wrong command looks authoritative (M10, lane L7).
    shape = None
    shape_match = _SHAPE_LINE_RE.search(prose)
    if shape_match is None:
        problems.append(
            "no `**Shape:** `<shape>`` line found in the `## Dispatch` block — a contract "
            f"that does not declare its shape ({' | '.join(SHAPE_ENUM)}) cannot have its "
            "command line checked against anything")
    else:
        shape = shape_match.group("shape")
        if shape not in SHAPE_ENUM:
            problems.append(
                f"declared shape {shape!r} is outside {{{' | '.join(SHAPE_ENUM)}}}")
            shape = None
    # --- the declared KIND (`[#793]` clause 2) ---------------------------------------------
    # ABSENT IS REPORTED, and the amnesty question was asked and answered rather than skipped.
    # The 124 lane contracts already in this tree carry no `**Kind:**` line, and none of them
    # is checked by the `lane-contract-check` hook: it runs `pass_filenames: false`, so `check`
    # sees zero paths on every commit and only the contract-manifest predicate fires. The
    # per-contract legs bite what a caller hands them by name — a freeze, or a deliberate
    # audit. So refusing an absent kind governs what is frozen NEXT without reddening what was
    # already written, which is the same line `[#717]` drew for an absent `--model`.
    kind = None
    kind_match = _KIND_LINE_RE.search(prose)
    if kind_match is None:
        problems.append(
            f"no `**Kind:** `<kind>`` line found in the `## Dispatch` block — the routing "
            f"default keys on the lane kind ([#793] clause 2), and it is DECLARED rather than "
            f"inferred; enum {{{' | '.join(KIND_ENUM)}}}")
    else:
        kind = kind_match.group("kind")
        if kind not in KIND_ENUM:
            problems.append(
                f"declared kind {kind!r} is outside {{{' | '.join(KIND_ENUM)}}}")
            kind = None

    if expect_shape is not None and shape is not None and shape != expect_shape:
        problems.append(
            f"contract declares shape {shape!r} but {expect_shape!r} was expected")

    # Which forms are actually present. Read from the FULL text — a command line legitimately
    # lives inside a fence.
    found = {name: pattern.search(text) for name, pattern in _COMMAND_RES.items()}
    present = [name for name, match in found.items() if match is not None]
    command = None

    slug = contract_file = effort = None
    if not present:
        problems.append(
            "no dispatch command line found — every contract carries the literal line that "
            "launches it, in the `## Dispatch` block, in exactly one of the four forms "
            "(`claude --bg --model … --worktree <slug> \"Read and execute the frozen "
            "contract at <PROMPTS_DIR>\\<file>\"`, or the legacy `Dispatch-Lane` spelling of "
            "it | `Dispatch-CloudV2` | `Dispatch-Codespace` | "
            "`Read <PROMPTS_DIR>\\<file> and execute it exactly.`); a contract handed "
            "over without one does not get started")
    elif len(present) > 1:
        problems.append(
            f"contract carries {len(present)} dispatch command lines ({', '.join(present)}) "
            "— one contract dispatches one way, and two forms free to disagree is the class "
            "this generator removes")
    elif shape is not None and present[0] != shape:
        problems.append(
            f"declared shape {shape!r} but the command line is the {present[0]!r} form — a "
            "lane handed another shape's command is worse than one handed none, because a "
            "wrong command looks authoritative")

    matched_shape = present[0] if len(present) == 1 else None
    if matched_shape is not None:
        command = found[matched_shape].group(0).strip()

    # The local form is the only one carrying a slug AND an effort on the line itself; the
    # cloud form carries file + title; the interactive form carries the file alone. Each is
    # read for exactly what it holds rather than for a shape it never had.
    dispatch = found["local"] if matched_shape == "local" else None
    line_model = None
    if matched_shape == "local":
        slug = dispatch.group("slug")
        contract_file = dispatch.group("file")
        effort = dispatch.group("effort")
        # `[#717]`: the model the LINE carries, held against the enum here and against the
        # routing row below. Absent is legal — every contract frozen before `[#717]` omits it —
        # so this is a check on what is present, not a demand that it be.
        line_model = dispatch.group("model")
        # `[#717]`, MADE STRUCTURAL FOR THE FORM THIS GENERATOR EMITS. Absence stays legal on
        # the LEGACY spelling — every contract frozen before `[#717]` omits the flag, and
        # reddening that corpus to enforce a new rule is the failure mode clause 2 named. The
        # emitted `claude` form has no such history, so on it an absent model is reported: the
        # amnesty is for what was already written, not for what is written next. `match.re` is
        # how the two spellings are told apart without either reader carrying a second copy of
        # the grammar.
        if dispatch.re is _CLAUDE_DISPATCH_LINE_RE and line_model is None:
            problems.append(
                "dispatch line states no `--model <m>` — this is the form the generator emits, "
                "and a launch line that omits the model silently re-decides the most expensive "
                f"constant on it ([#717]); enum {{{' | '.join(MODEL_ENUM)}}}")
        if line_model is not None and line_model not in MODEL_ENUM:
            problems.append(
                f"dispatch line carries model {line_model!r}, outside "
                f"{{{' | '.join(MODEL_ENUM)}}}")
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
    elif matched_shape in ("cloud", "codespace"):
        # Both off-machine forms carry a file and a name and no `-Effort`: cloud names the
        # lane with `-Title`, codespace with `-Slug`. Either way the name is read as the slug
        # and held to the SAME grammar and the same 1:1 pairing as the local form's — nothing
        # about running off-machine relaxes what a lane may be called.
        cloud_match = found[matched_shape]
        slug = cloud_match.group("slug")
        contract_file = cloud_match.group("file")
        try:
            validate_slug(slug, strict=False)
        except LaneContractError as exc:
            problems.append(f"dispatch line carries an invalid lane slug: {exc}")
        if contract_file != contract_filename(slug):
            problems.append(
                f"dispatch line pairs slug {slug!r} with file {contract_file!r}; the 1:1 "
                f"pairing wants {contract_filename(slug)!r}")
    elif matched_shape == "interactive":
        # The first message names the contract file and nothing else — there is no slug and
        # no tier on it to check. Both are still on the record: the slug on the pairing line
        # below, the tier in the routing row. Demanding an `-Effort` here would be demanding
        # a parameter the shape has no place to carry.
        contract_file = found["interactive"].group("file")

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
        elif line_model is not None and line_model != model:
            # `[#717]`, and the conjunction `-Effort` already gets. Widening the regex alone
            # would merely make a CONTRADICTING line parse: a contract declaring `sonnet` whose
            # own launch line says `-Model opus` would go from "silently dispatches at opus" to
            # "says opus out loud and still contradicts its own routing row". The defect being
            # closed is the divergence, not the omission.
            problems.append(
                f"routing row states model {model!r} but the dispatch line states "
                f"{line_model!r} — two sources free to disagree is the class this generator "
                f"removes, and this pair is the one that costs money ([#717])")
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

    # The pairing line's SHAPE follows the lane's: an interactive session has no lane branch,
    # so it pairs slug -> contract and the branch-derivation check has nothing to check. The
    # two patterns cannot both match — `_PAIRING_RE` requires `-> branch` where the other
    # requires `-> contract` — so this is a genuine either/or rather than a precedence rule.
    branch = None
    if shape == "interactive":
        pairing = _PAIRING_NO_BRANCH_RE.search(prose)
        if pairing is None:
            problems.append(
                "no pairing line found (slug -> contract) — an interactive contract pairs its "
                "slug with its file and declares no branch")
        else:
            p_slug = pairing.group("slug")
            if slug is None:
                slug = p_slug            # the only place an interactive contract names it
            elif p_slug != slug:
                problems.append(
                    f"pairing line names slug {p_slug!r} but the dispatch line names {slug!r}")
            if contract_file is not None and pairing.group("file") != contract_file:
                problems.append(
                    f"pairing line names contract {pairing.group('file')!r} but the dispatch "
                    f"line names {contract_file!r}")
    else:
        pairing = _PAIRING_RE.search(prose)
        if pairing is None:
            problems.append(
                "no worktree-pairing line found (slug -> branch -> contract)")
        else:
            branch = pairing.group("branch")
            p_slug = pairing.group("slug")
            # Derived under the DECLARED shape: a cloud lane runs on `claude/<slug>`, and
            # checking it against `worktree-<slug>` would refuse the correct branch. An
            # undeclared shape falls back to local, which is the historical reading.
            expected = branch_name(p_slug, shape or DEFAULT_SHAPE)
            if branch != expected:
                problems.append(
                    f"pairing line derives branch {branch!r} from slug {p_slug!r}; "
                    f"expected {expected!r} — the prefix is applied exactly once")
            if slug is not None and p_slug != slug:
                problems.append(
                    f"pairing line names slug {p_slug!r} but the dispatch line names {slug!r}")
            if contract_file is not None and pairing.group("file") != contract_file:
                problems.append(
                    f"pairing line names contract {pairing.group('file')!r} but the dispatch "
                    f"line names {contract_file!r}")

    # The receipt gate keys on the OFF-MACHINE shapes, declared rather than inferred from the
    # section's own presence — a contract that dropped the section used to read as "not an
    # off-machine lane" instead of "an off-machine lane missing its gate". Keying it on the
    # literal string `cloud` was a rule written to one instance of its own class, and it is
    # what refused the first codespace contract (R-ENUM, 2026-08-31).
    has_gate = CLOUD_SECTION in sections
    found_receipt = tuple(f for f in ALL_RECEIPT_FIELDS if f in prose)
    if shape in RECEIPT_SHAPES and not has_gate:
        problems.append(
            f"contract declares shape {shape!r} but carries no '## {CLOUD_SECTION}' section "
            f"— every off-machine dispatch carries one (STANDING_RULINGS Q5)")
    if has_gate:
        if shape is not None and shape not in RECEIPT_SHAPES:
            problems.append(
                f"contract declares shape {shape!r} but carries a '## {CLOUD_SECTION}' "
                f"section — the receipt gate is an off-machine-lane rule (Q5)")
        # An UNDECLARED shape keeps the historical reading (cloud's fields), so a contract
        # that lost its `**Shape:**` line is still checked rather than silently exempted.
        gate_shape = shape if shape is not None else "cloud"
        for missing in (f for f in RECEIPT_FIELDS_BY_SHAPE.get(gate_shape, ())
                        if f not in found_receipt):
            problems.append(f"{gate_shape} lane is missing the receipt field: {missing}")
    elif shape is not None and shape not in RECEIPT_SHAPES and found_receipt:
        problems.append(
            f"{shape} lane carries receipt fields — the receipt gate is an off-machine-lane "
            f"rule (Q5)")

    # The clause-1 and clause-2 refusals, applied to what the file actually DECLARES rather
    # than to what a spec was built from — the same predicate, read off the bytes. Held back
    # until here so it runs against the routing row's model, which is parsed above, and only
    # when all three inputs survived their own enum checks: a refusal computed from a value
    # already reported as off-enum would report the same defect twice under two names.
    if model is not None and kind is not None and shape is not None and model in MODEL_ENUM:
        problems.extend(routing_refusals(model=model, kind=kind, shape=shape))

    for ask_class in ("(a)", "(b)", "(c)"):
        if ask_class not in prose:
            problems.append(f"decision budget is missing ask-class {ask_class}")

    return ParsedContract(
        sections=sections, slug=slug, contract_file=contract_file, branch=branch,
        shape=shape, command=command, effort=effort, model=model, mode=mode, kind=kind,
        receipt_fields=found_receipt, problems=tuple(problems))


# --- CLI --------------------------------------------------------------------------------------

def _default_out_dir() -> Path:
    """Where a contract goes when the operator names no `--out-dir`: the root the VERB reads.

    `[#718]`, and the fix is an identity rather than an agreement. This used to return
    `Path.cwd()` — individually correct, and a second literal beside the reader's own. Batch W
    emitted six contracts into `to-cc/` while `Dispatch-Lane` resolved the prompts root, and
    all six were refused. There was no wrong line to find; there were two right lines that
    disagreed, which is why review never caught it.

    UNRESOLVED IS A REFUSAL, not a fall back to the cwd, and the row asks for exactly that:
    *"the refusal is the good outcome here, and it should survive the fix"*. Six refusals cost
    six dispatches; six contracts silently read from a stale location would have cost six lanes
    running against the wrong text. A cwd fallback would restore the split invisibly.
    """
    root = transport_root()
    if root is None:
        raise LaneContractError(
            "cannot resolve where a lane contract goes: `CLAUDE_PROMPTS_DIR` names no "
            "directory and `~/Downloads` is not one either. This is a REFUSAL rather than a "
            "fall back to the current directory — the dispatch verb reads the prompts root, "
            "and writing anywhere else puts the contract where nothing reads it ([#718]). "
            "Set CLAUDE_PROMPTS_DIR, or pass --out-dir to name the target explicitly.")
    return root


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
@click.option("--kind", type=click.Choice(KIND_ENUM), required=True,
              help="what the lane's work IS — the routing default keys on it ([#793] clause 2); "
                   "REQUIRED and never inferred")
@click.option("--mode", type=click.Choice(MODE_ENUM), default=DEFAULT_MODE, show_default=True)
@click.option("--effort", type=click.Choice(EFFORT_ENUM), default="high", show_default=True)
@click.option("--shape", type=click.Choice(SHAPE_ENUM), default=DEFAULT_SHAPE,
              show_default=True,
              help="dispatch substrate — selects the command line the contract carries")
@click.option("--loose-slug", is_flag=True, default=False,
              help="relax the batch-lane grammar to bare hyphen-only kebab")
@click.option("--out-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help="directory to write into  [default: the current directory]")
@click.option("--stdout", "to_stdout", is_flag=True, default=False,
              help="render to stdout instead of writing a file")
@click.option("--force", is_flag=True, default=False, help="overwrite an existing contract")
def cmd_emit(slug: str, purpose: str, repo: str, task_id: Optional[str], model: str, kind: str,
             mode: str, effort: str, shape: str, loose_slug: bool, out_dir: Optional[Path],
             to_stdout: bool, force: bool) -> None:
    """Emit one frozen lane contract."""
    # `[#716]`: the step-0 region is a function of the LIVE base-ref property, read once here so
    # `render_contract` stays pure. An unreadable verdict is treated as NOT guaranteed — the
    # region costs a lane one merge commit, its absence costs a silently-dropped row, so the
    # unknown case falls on the side that is cheap to be wrong about.
    try:
        verdict = base_ref_verdict(Path.cwd())
        needs_sync, why = not verdict.holds, verdict.why
    except Exception as exc:  # noqa: BLE001 — a git-less or odd checkout narrows, never wedges
        needs_sync, why = True, f"base-ref property could not be read ({exc}); assuming unmet"
    logger.info("step-0 sync region: %s — %s", "EMITTED" if needs_sync else "retired", why)

    spec = LaneSpec(slug=slug, purpose=purpose, repo=repo, task_id=task_id, model=model,
                    kind=kind, mode=mode, effort=effort, shape=shape,
                    strict_slug=not loose_slug, needs_base_sync=needs_sync)
    try:
        text = render_contract(spec)
    except LaneContractError as exc:
        raise click.ClickException(str(exc)) from exc

    if to_stdout:
        click.echo(text)
        return

    try:
        # `--out-dir` stays an operator override: the ONE key is the DEFAULT, not a jail.
        root = out_dir if out_dir is not None else _default_out_dir()
    except LaneContractError as exc:
        raise click.ClickException(str(exc)) from exc
    target = root / contract_filename(spec.validated().slug)
    if target.exists() and not force:
        raise click.ClickException(
            f"{target} already exists — a frozen contract is not silently overwritten; "
            f"pass --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    logger.info("wrote %s", target)
    # The operator reads this off the terminal, so it is a dispatch surface too — and it is
    # built from the SAME `dispatch_command` the file carries, rather than a second literal
    # that could drift from it.
    checked = spec.validated()
    line = dispatch_command(checked.slug, target.name, checked.effort, checked.shape,
                            checked.model)
    if checked.shape == "interactive":
        logger.info("dispatch with: start `claude`, then send: %s", line)
    else:
        logger.info("dispatch with: %s", line)


@cli.command("check")
@click.argument("paths", nargs=-1, required=False,
                type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--expect-shape", "expect_shape", type=click.Choice(SHAPE_ENUM), default=None,
              help="assert the lane's substrate; omitted, it is read from the contract")
def cmd_check(paths: tuple[Path, ...], expect_shape: Optional[str]) -> None:
    """Check existing contract(s): every mandatory field present and internally consistent,
    AND ([#630]) that an open batch's manifest and these contracts declare the SAME set of
    lane slugs.

    MANY paths, not one. The `lane-contract-check` pre-commit hook passes every staged
    contract in one invocation, so a single-`PATH` signature made the gate die with
    `Got unexpected extra arguments` the first time a batch staged more than one contract
    at once — the gate did not refuse a bad contract, it failed to run at all. Found
    2026-08-29 freezing six contracts in one commit; earlier batches staged them singly and
    never tripped it.

    PATHS may be EMPTY. The hook now runs `always_run: true` + `pass_filenames: false`
    ([#630]) — every commit, not just ones staging a `LANE-*.md` — so `check` sees zero
    paths on the overwhelming majority of invocations. It is not an error: the
    CONTRACT-MANIFEST predicate below reports "0 checked" explicitly rather than the CLI
    refusing to run at all.

    EVERY path is checked before exiting, so one bad contract does not mask the rest.
    """
    failed = 0
    contracts: dict[str, str] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        contracts[str(path)] = text
        parsed = parse_contract(text, expect_shape=expect_shape)
        if parsed.ok:
            logger.info("%s: OK — %d sections, shape %s, slug %s, branch %s, command %r",
                        path, len(parsed.sections), parsed.shape, parsed.slug,
                        parsed.branch or "(none — interactive)", parsed.command)
            continue
        failed += 1
        for problem in parsed.problems:
            logger.error("%s: %s", path, problem)

    failed += _check_manifest_contract_agreement(contracts)

    if failed:
        raise SystemExit(1)


def _check_manifest_contract_agreement(contracts: dict[str, str]) -> int:
    """`[#630]` — an OPEN batch's manifest and `contracts` (the paths `check` was given) must
    declare the SAME set of lane slugs. Returns the refusal count.

    The pure comparison (`batch_manifest.freeze_manifest_contract_agreement`) and the
    open-batch resolver (`batch_manifest.open_batches`) already exist and are unit-tested in
    `tests/test_batch_manifest.py`; this is the thin CLI adapter — the same
    logic-module / thin-adapter split `audit_checks/check_substrate_declaration.py` uses for
    a sibling validator.

    NEVER PASSES VACUOUSLY. Two distinct "nothing to compare" states, and both are REPORTED
    rather than silently returned: `contracts` empty (the hook's own every-commit invocation,
    since `pass_filenames: false`) and no batch open (the ordinary state — most days carry no
    open batch at all). Seeded from the measured batch-E defect (task-630): a slug renumbered
    between draft and dispatch, with nothing anywhere comparing the manifest's declared lanes
    against the contracts actually landed.
    """
    repo_root = _SCRIPTS.parent
    if not contracts:
        logger.info("contract-manifest predicate ([#630]): 0 contract(s) given — 0 checked")
        return 0

    # SCOPE: only contracts that LIVE IN THIS REPO are the batch's. A contract outside the tree
    # -- a tmp fixture, a draft in the prompts dir, a file being validated ad hoc -- is not part
    # of any open batch, and comparing it against the manifest refuses work that was never
    # claimed. Measured 2026-09-02: with batch G open, `check` on three tmp_path contracts
    # exited 1 because their slugs are absent from G's manifest, which is a refusal about the
    # FIXTURE rather than about the repo. The seeded batch-E defect is unaffected: a freeze
    # commit stages its contracts UNDER docs/audits/<batch>-launch-contracts/, so they are
    # in-tree and still compared.
    in_repo: dict[str, str] = {}
    for name, text in contracts.items():
        try:
            resolved = Path(name).resolve()
        except OSError:
            continue
        if resolved.is_relative_to(repo_root.resolve()):
            in_repo[name] = text
    skipped = len(contracts) - len(in_repo)
    if not in_repo:
        logger.info("contract-manifest predicate ([#630]): %d contract(s), none in this repo "
                    "— 0 checked", skipped)
        return 0
    contracts = in_repo

    batches = open_batches(repo_root)
    if not batches:
        logger.info("contract-manifest predicate ([#630]): no open batch — 0 checked")
        return 0

    failed = 0
    for batch in batches:
        try:
            manifest_text = (repo_root / batch.path).read_text(encoding="utf-8")
        except OSError as exc:
            failed += 1
            logger.error("%s: could not read to compare against %d contract(s): %r",
                        batch.path, len(contracts), exc)
            continue
        for refusal in freeze_manifest_contract_agreement(manifest_text, contracts):
            failed += 1
            logger.error("%s: %s", batch.path, refusal.render())

    if not failed:
        logger.info("contract-manifest predicate ([#630]): %d open batch(es), %d contract(s) "
                    "— OK", len(batches), len(contracts))
    return failed


@cli.command("enums")
def cmd_enums() -> None:
    """Print the baked-in enums — the checkable surface a contract author reads."""
    click.echo(f"effort (this generator): {' | '.join(EFFORT_ENUM)}")
    # Enum order, not alphabetical: these are a ladder, and printing them sorted reads as
    # `high | low | medium | xhigh`, which invites the wrong mental model.
    routed = " | ".join(e for e in EFFORT_ENUM if e in DISPATCH_ROUTED_EFFORT)
    click.echo(f"effort (dispatch-routed): {routed}")
    click.echo(f"model: {' | '.join(MODEL_ENUM)}   default: {DEFAULT_MODEL}")
    click.echo(f"kind: {' | '.join(KIND_ENUM)}   default: (none — REQUIRED, never inferred)")
    for _k in KIND_ENUM:
        click.echo(f"  {_k}: {KIND_GLOSS[_k]}")
    click.echo(f"mode: {' | '.join(MODE_ENUM)}   default: {DEFAULT_MODE}")
    click.echo(f"shape: {' | '.join(SHAPE_ENUM)}   default: {DEFAULT_SHAPE}")
    # The command each shape actually emits, shown against a placeholder lane — the surface a
    # contract author most often wants and would otherwise guess at.
    for shape in SHAPE_ENUM:
        line = dispatch_command("lane-a-000-example", "LANE-a-000-example.md", "high", shape,
                                DEFAULT_MODEL)
        prefix = "claude, then: " if shape == "interactive" else ""
        click.echo(f"  {shape}: {prefix}{line}")
    click.echo(f"mandatory sections: {', '.join(MANDATORY_SECTIONS)}")
    for receipt_shape in RECEIPT_SHAPES:
        fields = ', '.join(RECEIPT_FIELDS_BY_SHAPE[receipt_shape])
        click.echo(f"off-machine section ({receipt_shape}): {CLOUD_SECTION} ({fields})")
    click.echo(f"generated: {_dt.date.today().isoformat()}")


if __name__ == "__main__":
    cli()
