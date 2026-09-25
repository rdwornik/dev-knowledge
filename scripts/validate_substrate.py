#!/usr/bin/env python
"""validate_substrate.py — the substrate validator, LAYER 2 (`[#591]`, intake #52 I4).

WHAT LAYER 1 ALREADY DOES, so this module does not repeat it. `gen_lane_contract.py` checks a
contract's SHAPE: that a declared `**Shape:**` line and the command line beneath it are the
same shape, that the mandatory sections are present, that the worktree pairing derives its
branch from its slug exactly once. Its own docstring states the honest limit this module
exists to close — *"it checks SHAPE, never whether a contract's footprint claims are true"*.

LAYER 2 IS THE DECLARATION-VS-CONTENT CHECK. A contract names a substrate and nothing checks
that the substrate exists, that its gates can run there, or that its paths are reachable from
it (intake #52, "Problem / motivation"). Four legs, in the intake's own order:

  1. `substrate-no-live-verb`            REFUSE — the substrate is unregistered, has no live
                                         verb, or the contract declares none at all.
  2. `substrate-cloud-gate-dependent`    REFUSE — cloud + a gate in the Done-when.
  3. `substrate-offmachine-operator-path` REFUSE — cloud/codespace + an operator-disk path.
  4. `substrate-second-local-writer`     WARN   — two local writers in one checkout.

Plus `substrate-unknown-override`, which is not a substrate defect: it is a deviation line
naming a rule that does not exist, reported rather than swallowed, so a typo cannot read as a
discharge.

WHY REFUSING COMES FIRST. Intake #52 orders its three remaining acts and says why: *"The
substrate VALIDATOR — first, because it refuses… refusing is cheaper than detecting drift
after the fact."* This module is that act.

THE OVERRIDE IS AN EXPLICIT RECORDED DEVIATION, and it is the requirement's own wording: *"An
override is an explicit recorded deviation, never a silent pass."* A `**Substrate deviation:**
<rule-id> — <reason>` line downgrades exactly the rule it names from `refuse` to `warn`, marks
the refusal `overridden`, and carries the reason into the rendered evidence. There is no code
path that removes a refusal from the returned list. A reason shorter than
`OVERRIDE_REASON_FLOOR` characters is not a reason — it is a token — and does not override.

THE VOCABULARY IS READ, NOT INVENTED. Substrates, verbs and capability facts come from
`ecosystem/substrate-registry.yaml`, whose every field cites the Ch8 line or STANDING_RULINGS
V-clause it projects. This module hard-codes no substrate name.

TWO DECLARATION SPELLINGS ARE LIVE, and both are read rather than one being refused on form:
`gen_lane_contract` emits ``**Shape:** `local` `` while Ch8 and every hand-authored contract
write `**Substrate:** local` / `**Substrate: LOCAL worktree**`. Refusing either would refuse
half the live corpus for a spelling nobody ruled on.

A DECLARATION IS A FENCED TOKEN; PROSE IS NOT A DECLARATION (finding C-F, fixed 2026-08-28).
`**Shape:**` is read FIRST, and while it accepted a BARE token that precedence rule was only
safe as long as the word "Shape" could not occur as an ordinary heading — which, in a design
document, is close to the least safe assumption available. Run against the live batch-1
contract, whose second line reads ``**Shape:** ONE plan -> 5 file-disjoint lanes``,
`declared_substrate` returned ``'one'`` and, returning on first match, never reached that
contract's real `Substrate: LOCAL` line. `_SHAPE_RE` now requires the backticks that layer 1's
`gen_lane_contract._SHAPE_LINE_RE` has always required, so an unfenced `**Shape:**` heading
falls through to the prose spelling instead of binding garbage ahead of it.

HONEST LIMITS, stated because they bound what a clean verdict means:

  * **Leg 2 is TOKEN-based, not semantic.** It matches a measured set of gate tokens inside
    the Done-when section. A Done-when that depends on a gate without naming one passes, and
    a Done-when that names `pytest` in a sentence saying the lane does NOT run it is refused.
    The trade is deliberate: the alternative is reading English.
  * **Leg 3 matches PATH SHAPES**, not reachability. A cloud lane citing a path that happens
    to exist inside its own container is still refused, because the shapes matched are
    operator-disk shapes (drive letters, the home-relative Downloads dir, the prompts-dir
    tokens).
  * **Leg 4 is a WARN by the row's own words**, and it compares contracts within ONE batch
    handed to `validate_batch`. It cannot see a lane already running that was not passed in.
  * **Nothing here asserts a contract is CORRECT.** A contract can be internally consistent,
    pass all four legs, and still ask for the wrong work.

Layer-2 / read-only (ADR-28/36): reads the registry and the text it is given, writes nothing.
"""
from __future__ import annotations

import datetime as _dt
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional

import yaml

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

# The lane-branch enum is IMPORTED, never restated. `batch_manifest` imports from the same
# module for the ADR-110 exemption, so the enum leg 5 checks and the enum the exemption grants
# on come from ONE definition — which is the whole point: a copy could drift, and a drifted
# copy would report coverage the teardown does not actually have.
#
# WHICH symbol changed, and why (this lane). Leg 5 imported `LANE_BRANCH_RE` — the BATCH-lane
# grammar — and so asked a narrower question than the one it is written to ask. Three ruled
# lane kinds (`claude/<slug>`, `epic/<slug>`, `automation/<slug>`) are lane branches that
# grammar cannot express, so every cloud lane was refused by a validator whose sibling
# `classify()` called the same branch a conforming `cloud-lane`. `is_lane_branch` is the set;
# the regex is one member's grammar. See `validate_branch_naming.LANE_BRANCH_KINDS`.
from validate_branch_naming import is_lane_branch  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("validate-substrate")

REGISTRY_RELPATH = "ecosystem/substrate-registry.yaml"

# --- the closed rule surface ---------------------------------------------------------------

RULE_NO_LIVE_VERB = "substrate-no-live-verb"
RULE_CLOUD_GATE = "substrate-cloud-gate-dependent"
RULE_OFFMACHINE_PATH = "substrate-offmachine-operator-path"
RULE_SECOND_LOCAL_WRITER = "substrate-second-local-writer"
#: Leg 5 (batch E, prerequisite 0a). ADR-116 sat stranded on `claude/lane-f` until a window
#: close because the batch teardown iterates an enum that cannot see a cloud lane. This makes
#: that a FREEZE-time refusal rather than an integration surprise.
#:
#: AMENDED (this lane): the leg now reads `validate_branch_naming.is_lane_branch` — the whole
#: ratified lane SET — where it read `LANE_BRANCH_RE`, one member's grammar. A cloud lane on
#: `claude/<slug>` no longer trips it, because a cloud lane IS in the enum a teardown
#: iterates; what the old predicate proved was only that the enum's own reader disagreed with
#: `classify()`. The refusal that remains is a branch outside the enum altogether.
RULE_TEARDOWN_ENUM = "substrate-teardown-enum-coverage"
#: Leg 6 (batch E, CUT-3(c)). The cut collapsed two colliding doctrine lanes into one and
#: stripped a file from a third's scope; it then required that disjointness be RE-VERIFIED
#: here at freeze rather than asserted in prose. This is that verification.
RULE_WRITE_SCOPE_DISJOINT = "substrate-lane-write-scope-disjoint"
#: Leg 7 (`[#629]`, batch F). DC-3 was dispatched by APPENDING an amendment reading "do not
#: perform Act One" to a frozen contract whose body still CONTAINED Act One in full, and the
#: lane performed it -- correctly, by the only artifact it was given. An amendment is
#: ADDITIVE; a ruling that narrows a frozen contract must REISSUE it through
#: `gen_lane_contract`, never annotate it. This leg makes the annotation shape a refusal.
RULE_AMENDMENT_SUBTRACTS = "amendment-subtracts-an-act"
#: Leg 8 (`[#554]` lane aa-1, L2). THE PRE-DISPATCH HALF OF THE HEARTBEAT, and the reason it
#: lives HERE rather than beside dispatch in prose: this module is the organ that refuses a
#: contract before it is dispatched, so a substrate proven dead becomes a refusal AT DISPATCH
#: instead of a discovery mid-batch.
#:
#: THE DEFECT IT ANSWERS. The codespace substrate died at one commit and nobody noticed for two
#: weeks because NOTHING RAN THERE — `provision.sh` reached a call site for a module retired
#: twelve days earlier, Codespaces substituted a recovery container, and the platform reported
#: Available throughout. Eight lanes were deferred off the back of it. A validator that checks
#: a contract's declarations while the substrate it names is dead is checking the spelling of a
#: destination nobody can reach.
#:
#: OFF-MACHINE ONLY. A `local` lane runs on the operator's machine, whose liveness is not in
#: question because the operator is sitting at it; gating that on a cloud probe would refuse the
#: one substrate that is definitely alive, which is how a refusal gate becomes noise.
RULE_HEARTBEAT_DEAD = "substrate-heartbeat-dead"
RULE_UNKNOWN_OVERRIDE = "substrate-unknown-override"

#: Order is the intake's own. This tuple IS the checkable surface — a new leg enters it
#: deliberately, the way the branch-prefix enum does.
RULE_IDS: tuple[str, ...] = (
    RULE_NO_LIVE_VERB,
    RULE_CLOUD_GATE,
    RULE_OFFMACHINE_PATH,
    RULE_SECOND_LOCAL_WRITER,
    RULE_TEARDOWN_ENUM,
    RULE_WRITE_SCOPE_DISJOINT,
    RULE_AMENDMENT_SUBTRACTS,
    RULE_HEARTBEAT_DEAD,
    RULE_UNKNOWN_OVERRIDE,
)

#: PER-LEG arm dates, for predicates added to this module AFTER the commit-time adapter
#: (`audit_checks/check_substrate_declaration.py`) first armed 2026-08-27. A leg written today
#: cannot honestly gate a contract dispatched before it existed -- the reason legs 5 and 6
#: carry their own arm dates too, in that adapter (they predate this leg and armed there
#: first). THIS dict is the single home for a leg's date, and the adapter's map READS leg 8's
#: entry from here rather than restating it, so the two cannot disagree. Declaring it here and
#: stopping was measured and is wrong: the adapter never consulted this dict, so the grandfather
#: existed and never fired, and the commit gate refused 20 committed contracts back to
#: 2026-08-29 — each a record of a dispatch that already happened, undischargeable without
#: falsifying it. `tests/test_validate_substrate.py` asserts the two maps agree.
#:
#: FREEZE IS UNSCOPED BY DATE, exactly like legs 5/6 (`validate_substrate.validate_batch`'s own
#: docstring, and the batch-F manifest's own words: "the FREEZE does not [grandfather];
#: `validate_substrate` run directly ... applies every leg with no date grandfather at all").
#: The grandfather is a COMMIT-TIME adapter concern only, and stays one here.
LEG_ARM_DATES: dict[str, _dt.date] = {
    RULE_AMENDMENT_SUBTRACTS: _dt.date(2026, 9, 1),
    # TOMORROW, not today, and the off-by-one is the module's own rule applied to itself: two
    # committed contracts dated 2026-09-15 declare `cloud`, and they were dispatched BEFORE this
    # leg existed. Arming on their own date would retro-refuse a record of a dispatch that
    # already happened, which is the falsification the grandfather exists to prevent.
    RULE_HEARTBEAT_DEAD: _dt.date(2026, 9, 16),
}

SEVERITY_REFUSE = "refuse"
SEVERITY_WARN = "warn"

#: A deviation shorter than this is a token, not a recorded reason. Measured against the
#: shortest genuine deviation this repo records (the Ch8 cloud `python3` guard, 88 chars):
#: the floor clears it by ~3x and rejects every one-word dodge. Same posture as
#: `funnel_coverage._REJECTED_MIN_LOCATOR`, and the same honest weakness — it distinguishes a
#: recorded reason from a token, and nothing more.
OVERRIDE_REASON_FLOOR = 30


class SubstrateRegistryError(RuntimeError):
    """The registry itself could not be read. Raised for an unreadable or malformed file —
    an inert validator is reported as an error, not as a clean pass."""


@dataclass(frozen=True)
class Substrate:
    """One registry row. Pure data; every field is a projection of a cited Ch8/V-clause line."""
    name: str
    family: str
    verbs: tuple[str, ...]
    aliases: tuple[str, ...]
    live: bool
    admits_gate_dependent_work: bool
    operator_disk: bool
    shared_checkout: bool = False
    branch_prefix: Optional[str] = None


@dataclass(frozen=True)
class Refusal:
    """One fired rule. `severity` is `refuse` unless an override downgraded it to `warn`."""
    rule: str
    source: str
    detail: str
    substrate: Optional[str] = None
    severity: str = SEVERITY_REFUSE
    overridden: bool = False

    def render(self) -> str:
        """One line naming the rule, the contract and the reason — the requirement's
        *"each refusal names the rule it fired on"*."""
        tail = " [OVERRIDDEN — recorded deviation]" if self.overridden else ""
        return f"{self.source}: {self.severity.upper()} {self.rule} — {self.detail}{tail}"


# --- registry loading ----------------------------------------------------------------------

def repo_root() -> Path:
    """The repo root, derived from this file's location. `scripts/` is a direct child."""
    return _SCRIPTS.parent


_REQUIRED_FIELDS = ("family", "verbs", "live", "admits_gate_dependent_work", "operator_disk")


def load_registry(repo_path: Path) -> dict[str, Substrate]:
    """Read `ecosystem/substrate-registry.yaml` into `{name: Substrate}`.

    RAISES rather than degrading. A missing or malformed registry makes every leg inert, and
    an inert validator that returns an empty refusal list is indistinguishable from a clean
    contract — the exact green-by-skip class `[#583]` sweeps for. The caller decides what an
    unreadable registry means; this function refuses to decide it silently.
    """
    path = Path(repo_path) / REGISTRY_RELPATH
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SubstrateRegistryError(f"could not read {REGISTRY_RELPATH}: {exc!r}") from exc
    except yaml.YAMLError as exc:
        raise SubstrateRegistryError(f"{REGISTRY_RELPATH} is not valid YAML: {exc}") from exc
    if not isinstance(raw, dict) or not isinstance(raw.get("substrates"), dict):
        raise SubstrateRegistryError(
            f"{REGISTRY_RELPATH} carries no `substrates:` mapping")

    out: dict[str, Substrate] = {}
    for name, row in raw["substrates"].items():
        if not isinstance(row, dict):
            raise SubstrateRegistryError(f"substrate {name!r} is not a mapping")
        missing = [f for f in _REQUIRED_FIELDS if f not in row]
        if missing:
            raise SubstrateRegistryError(
                f"substrate {name!r} is missing required field(s): {', '.join(missing)}")
        verbs = tuple(row.get("verbs") or ())
        if not verbs:
            raise SubstrateRegistryError(f"substrate {name!r} declares no verb")
        out[str(name)] = Substrate(
            name=str(name),
            family=str(row["family"]),
            verbs=verbs,
            aliases=tuple(row.get("aliases") or ()),
            live=bool(row["live"]),
            admits_gate_dependent_work=bool(row["admits_gate_dependent_work"]),
            operator_disk=bool(row["operator_disk"]),
            shared_checkout=bool(row.get("shared_checkout", False)),
            branch_prefix=row.get("branch_prefix") or None,
        )
    return out


# --- reading the contract ------------------------------------------------------------------

#: The generator's spelling: ``**Shape:** `local` ``. The BACKTICKS ARE REQUIRED, and that is
#: the whole of the C-F fix (batch-1 finding C-F; LESSONS.md 2026-08-28, architect premise
#: error 3 of 3). This pattern used to spell them ``  `? ``, which made an ordinary English
#: heading a declaration: the batch-1 contract's second line reads
#: ``**Shape:** ONE plan -> 5 file-disjoint lanes -> ONE integration`` and bound the substrate
#: to ``'one'`` — an off-enum value RETURNED rather than reported. Worse than the wrong value
#: was the masking: `declared_substrate` returns on its first match, so the contract's genuine
#: ``Real substrate: LOCAL`` line was never read at all.
#:
#: A DECLARATION IS A FENCED TOKEN; PROSE IS NOT A DECLARATION. The tightening direction is
#: deliberate and is the one the contract for this fix names: the alternative — loosening the
#: substrate check so ``'one'`` "passes" — would keep the parser bug and hide it.
#:
#: This is not a newly invented grammar. It is LAYER 1's existing one:
#: `gen_lane_contract._SHAPE_LINE_RE` has always required the backticks
#: (``^\*\*Shape:\*\*\s+`(?P<shape>[a-z]+)` ``). The two organs read the generator's own field
#: identically now, instead of disagreeing about what counts as a declaration — which is what
#: let a hand-authored contract trip a gate on a word it had no way to know was reserved.
#: ANCHORED to line start (terra HIGH, this arc). Unanchored, an EXAMPLE of the field --
#: a contract explaining ``**Shape:** `cloud` `` mid-sentence, which the corpus does -- wins
#: the precedence race over the real declaration further down, masking it exactly the way
#: the prose heading did. Layer 1 anchors for the same reason; matching its anchoring is the
#: rest of matching its grammar.
_SHAPE_RE = re.compile(r"^\*\*Shape:\*\*\s*`(?P<value>[A-Za-z][A-Za-z0-9_-]*)`", re.I | re.M)
#: Ch8's spelling, bolded or not, with or without the colon inside the bold markers:
#: `**Substrate:** cloud` · `**Substrate: LOCAL worktree**` · `Substrate: codespace`.
_SUBSTRATE_RE = re.compile(
    r"\*{0,2}Substrate\*{0,2}\s*:\s*\*{0,2}\s*`?(?P<value>[A-Za-z][A-Za-z0-9_-]*)`?", re.I)

#: `**Substrate deviation:** <rule-id> — <reason>`. The dash is any of the three the corpus
#: writes (em dash, en dash, hyphen) or a colon; a deviation refused on punctuation would be a
#: refusal about typography rather than about substance.
_DEVIATION_RE = re.compile(
    r"\*{0,2}Substrate deviation\*{0,2}\s*:\s*\*{0,2}\s*`?(?P<rule>[a-z][a-z0-9-]*)`?\s*"
    r"[—–:-]\s*(?P<reason>.+)", re.I)

#: The Done-when section, by any of its live headings. `gen_lane_contract` emits
#: `## Done-contract (immutable)`; intake #52 and the rows say "Done-when"; hand-authored
#: contracts write `**Done when:**`. All three are the same section.
#: Up to three leading spaces, which is CommonMark's rule for a heading (four would be an
#: indented code block). Not decoration: a hand-authored contract indents freely, and a
#: column-0-only match returns an EMPTY Done-when section — which looks exactly like a
#: contract with no gate in it, i.e. leg 2 silently stops firing rather than reporting.
_DONE_HEADING_RE = re.compile(
    r"^ {0,3}(?:#{1,6}\s*|\*{0,2})(?:Done[- ]contract|Done[- ]when|Done)\b", re.I | re.M)
_ANY_HEADING_RE = re.compile(r"^ {0,3}#{1,6}\s+\S", re.M)

#: Gate tokens, taken from Ch8 Layer-1 Q1's own parenthetical — "(suite / hooks / ship-gate)"
#: — plus the two literal gate invocations this repo's contracts actually write. Deliberately
#: NOT the bare word "gate": it appears in ordinary prose and would refuse on a mention.
_GATE_TOKEN_RES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pytest", re.compile(r"\bpytest\b", re.I)),
    ("audit.py health", re.compile(r"audit\.py\s+health", re.I)),
    ("ship-gate", re.compile(r"\bship[- ]gate\b", re.I)),
    ("pre-commit", re.compile(r"\bpre-commit\b", re.I)),
    ("ruff", re.compile(r"\bruff\b", re.I)),
    ("uv run", re.compile(r"\buv run\b", re.I)),
    ("suite green", re.compile(r"\bsuite\s+green\b", re.I)),
    ("hooks armed", re.compile(r"\bhooks?\s+armed\b", re.I)),
    ("gates green", re.compile(r"\bgates?\s+green\b", re.I)),
)

#: Operator-disk path shapes. Each is a shape the operator's machine has and an off-machine
#: clone does not.
_OPERATOR_PATH_RES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("a Windows drive path", re.compile(r"\b[A-Za-z]:[\\/]{1,2}[A-Za-z0-9_.$-]")),
    ("the home-relative Downloads dir", re.compile(r"~[\\/]Downloads\b", re.I)),
    ("the prompts-dir token", re.compile(r"<PROMPTS_DIR>")),
    ("the prompts-dir environment variable", re.compile(r"\$env:CLAUDE_PROMPTS_DIR", re.I)),
    ("a Windows profile variable", re.compile(r"%USERPROFILE%|%USERNAME%", re.I)),
    ("a WSL host mount", re.compile(r"/mnt/[a-z]/", re.I)),
)

#: The worktree-pairing line, in both live shapes. Reused rather than re-derived: the branch
#: is what identifies a checkout.
_PAIRING_BRANCH_RE = re.compile(
    r"slug\s+`[^`]+`\s*->\s*branch\s+`(?P<branch>[^`]+)`")

#: The SLUG half of the same pairing line -- the FIRST field, `slug -> branch -> contract`
#: (ADR-110's fifth per-lane requirement). `[#630]` reads this to compare a contract's own
#: declared identity against the batch manifest's lane table, in `batch_manifest.py`.
_PAIRING_SLUG_RE = re.compile(r"slug\s+`(?P<slug>[^`]+)`\s*->")

PRIMARY_CHECKOUT = "<primary checkout>"

#: The write-scope section heading. `(frozen)` is the live spelling but is not required — a
#: contract that drops the parenthetical still declares a scope, and refusing to read it would
#: make leg 6 silently vacuous, which is the green-by-skip class `[#583]` sweeps for.
_SCOPE_HEADING_RE = re.compile(r"^ {0,3}#{1,6}\s*Write[- ]scope\b.*$", re.I | re.M)

#: A backticked token inside the write-scope section that is shaped like a repo path. A bare
#: word in backticks (a rule id, a verb, a flag) is not a path and must not create a phantom
#: intersection: the token has to carry a `/` or a `.` and use path characters only.
_SCOPE_PATH_RE = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*)`")

#: The literal a read-only lane writes instead of paths. Matched case-insensitively on the
#: word alone, because the live spelling carries an em-dash clause after it.
_SCOPE_NONE_RE = re.compile(r"\bNONE\b")

#: A write-scope DECLARATION is a markdown list item. Prose in the same section is commentary
#: — see `write_scope_paths` for the measured failure this prevents.
_SCOPE_ITEM_RE = re.compile(r"^\s{0,3}[-*+]\s+")


def declared_substrate(text: str) -> Optional[str]:
    """The substrate a contract declares, lower-cased, or None when it declares none.

    `**Shape:**` is read FIRST because it is the generator's own field and therefore the
    machine-produced one; the prose `Substrate:` spelling is the hand-authored fallback.
    """
    for pattern in (_SHAPE_RE, _SUBSTRATE_RE):
        match = pattern.search(text)
        if match is not None:
            return match.group("value").strip().lower()
    return None


def declared_overrides(text: str) -> dict[str, str]:
    """`{rule-id: reason}` for every recorded deviation carrying a real reason.

    A deviation whose reason is shorter than `OVERRIDE_REASON_FLOOR` is dropped here, so it
    can never downgrade anything — and leg 5 still reports an UNKNOWN rule id, which is how a
    typo surfaces rather than reading as a discharge.
    """
    out: dict[str, str] = {}
    for match in _DEVIATION_RE.finditer(text):
        reason = match.group("reason").strip().rstrip("*").strip()
        if len(reason) >= OVERRIDE_REASON_FLOOR:
            out[match.group("rule").strip().lower()] = reason
    return out


def done_when_section(text: str) -> str:
    """The Done-when section's body, or `""` when the contract carries none.

    Scoped deliberately: the requirement is *"cloud + a gate in its Done-when"*, and a gate
    token in the Steps or in a note about what the integrator does later is not that.
    """
    heading = _DONE_HEADING_RE.search(text)
    if heading is None:
        return ""
    start = heading.end()
    nxt = _ANY_HEADING_RE.search(text, start)
    return text[start:nxt.start()] if nxt else text[start:]


def checkout_key(text: str, substrate: Substrate) -> str:
    """Which checkout a lane of this contract writes in.

    A local lane's checkout is its worktree branch, read off the pairing line. A substrate
    flagged `shared_checkout` (the interactive shape) has no lane branch at all and runs in
    the primary checkout — so every such lane resolves to the SAME key, which is exactly the
    contention leg 4 reports.
    """
    if substrate.shared_checkout:
        return PRIMARY_CHECKOUT
    match = _PAIRING_BRANCH_RE.search(text)
    return match.group("branch").strip() if match else PRIMARY_CHECKOUT


def lane_branch(text: str) -> Optional[str]:
    """The lane branch a contract pairs itself to, or None when it declares no pairing.

    Distinct from `checkout_key`, which answers *which checkout writes* and collapses the
    shared-checkout shape onto one key. Leg 5 needs the branch NAME as written, because the
    question it asks is whether the teardown enum can match that name.
    """
    match = _PAIRING_BRANCH_RE.search(text)
    return match.group("branch").strip() if match else None


def contract_slug(text: str) -> Optional[str]:
    """The lane slug a contract's own pairing line declares, lower-cased, or None.

    The FIRST field of `slug -> branch -> contract` -- a contract's own claim about its
    identity. `[#630]` (`batch_manifest.freeze_manifest_contract_agreement`) compares the set
    of these, across a batch's contract directory, against the manifest's own lane table: the
    measured batch-E defect was a slug renumbered between draft and dispatch with nothing
    anywhere comparing the two surfaces.
    """
    match = _PAIRING_SLUG_RE.search(text)
    return match.group("slug").strip().lower() if match else None


def write_scope_paths(text: str) -> set[str]:
    """The repo paths a contract declares it will write, as a set.

    Scoped to the Write-scope section deliberately: a path named in the Steps, in a Done-when
    or in a "what NOT to do" bullet is a *reference*, not a claim to write it, and treating
    those as scope would make every contract collide with every other one.

    A scope of NONE returns the empty set, so read-only census lanes intersect with nothing.
    """
    heading = _SCOPE_HEADING_RE.search(text)
    if heading is None:
        return set()
    start = heading.end()
    nxt = _ANY_HEADING_RE.search(text, start)
    body = text[start:nxt.start()] if nxt else text[start:]
    if _SCOPE_NONE_RE.search(body):
        return set()
    # LIST ITEMS ONLY, and the restriction is load-bearing rather than tidy. A write-scope
    # section legitimately contains PROSE about paths it does NOT claim — batch E's own DC-1
    # says, in this very section, that `CLAUDE.md` is *deliberately absent from this scope*.
    # Reading the whole body turned that disclaimer into a declaration and produced a phantom
    # DC-1 <-> DC-23 collision on the one file the cut had just separated. A declaration is a
    # bullet; everything else in the section is commentary.
    out: set[str] = set()
    for line in body.splitlines():
        if not _SCOPE_ITEM_RE.match(line):
            continue
        out.update(tok for tok in _SCOPE_PATH_RE.findall(line) if "/" in tok or "." in tok)
    return out


# --- leg 7 (`[#629]`): an amendment cannot SUBTRACT an act already in the body -------------
#
# THE DC-3 SHAPE. A frozen contract's body still contained "Act One" in full; an amendment
# appended to it read "do not perform Act One"; the lane executed the contract as handed. The
# validator only ever reads the body as authored, and an amendment that CONTRADICTS the body
# is still a well-formed body -- invisible to every predicate above.
#
# DETECTION IS TEXTUAL AND CONSERVATIVE, per the requirement's own words: refusing on a
# matched negation is cheap, and the escape is exactly the reissue the predicate is asking
# for. So this does not parse intent -- it looks for a NEGATION WORD, within a short span, of
# a TARGET (an `Act <word>`, a `Step <n>`, or a backticked write-scope-shaped token) that ALSO
# appears in the contract's own body BEFORE the amendment starts. The "before" requirement is
# what keeps this from firing on an amendment that merely explains itself in the negative
# ("Act Nine was never part of this contract") -- there is nothing earlier to subtract.

#: An `Amendment` block, however it is spelled: a heading (`## Amendment 1 — ...`) or a bold
#: lead-in (`**Amendment:**`). Same heading-detection shape as `_SCOPE_HEADING_RE` above.
_AMENDMENT_HEADING_RE = re.compile(r"^ {0,3}(?:#{1,6}\s*|\*{0,2})Amendment\b.*$", re.I | re.M)

#: The three subtraction targets the requirement names by name: "an act, step or write-scope
#: entry". `Act <word>` covers the DC-3 shape itself; `Step <n>` and a backticked token cover
#: the other two the same Done-contract line enumerates.
_SUBTRACTION_TARGET = (
    r"(?:Act\s+(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|\d+)"
    r"|Step\s+\d+"
    r"|`[^`]+`)")

#: A negation word, then the target within a short span -- short enough that the two are
#: talking about the same thing, not two unrelated clauses sharing a sentence.
_NEGATION_RE = re.compile(
    r"\b(?:do(?:es)?\s+not|no\s+longer|never|skip(?:s|ped)?|remov(?:e|es|ed)|drop(?:s|ped)?|"
    r"forbid(?:s)?|cancel(?:s|led|ed)?|without\s+(?:performing|running|doing))\b"
    r"[^.\n]{0,80}?(?P<target>" + _SUBTRACTION_TARGET + r")",
    re.I)


def _amendment_blocks(text: str) -> list[tuple[int, str]]:
    """Every `(start_offset, body)` pair for an Amendment block in `text`.

    `start_offset` is where the AMENDMENT HEADING begins -- everything before it is "the
    body" a subtraction has to already be present in. A contract can carry more than one
    amendment (the batch-F manifest itself carries four), so this returns all of them.
    """
    out: list[tuple[int, str]] = []
    for heading in _AMENDMENT_HEADING_RE.finditer(text):
        start = heading.end()
        nxt = _ANY_HEADING_RE.search(text, start)
        end = nxt.start() if nxt else len(text)
        out.append((heading.start(), text[start:end]))
    return out


def amendment_subtractions(text: str) -> list[str]:
    """Every subtraction target an amendment block negates that the contract's own BODY --
    the text strictly before that amendment -- already contains.

    A negation naming something not present earlier is not a subtraction (nothing to
    subtract); a negation inside prose that never reaches an Amendment heading is not this
    leg's business at all (an amendment is the thing that arrives after a contract is frozen).
    """
    out: list[str] = []
    for start, block in _amendment_blocks(text):
        body = text[:start]
        for match in _NEGATION_RE.finditer(block):
            target = match.group("target").strip()
            if target.lower() in body.lower():
                out.append(target)
    return out


# --- the four legs -------------------------------------------------------------------------

def _apply_override(refusal: Refusal, overrides: Mapping[str, str]) -> Refusal:
    """Downgrade a refusal the contract explicitly deviates from — and only that one.

    The refusal is never removed. Downgrading to `warn` plus an `overridden` flag plus the
    recorded reason in the evidence is what makes the deviation visible in every surface that
    renders it; dropping it would be the silent pass the requirement forbids.
    """
    reason = overrides.get(refusal.rule)
    if reason is None:
        return refusal
    return Refusal(rule=refusal.rule, source=refusal.source,
                   detail=f"{refusal.detail} · recorded deviation: {reason}",
                   substrate=refusal.substrate, severity=SEVERITY_WARN, overridden=True)


#: `heartbeat` not supplied means READ IT FROM THE REPO, never "skip the leg". A default of
#: `None` would make the pre-dispatch check opt-in, and an opt-in refusal is exactly the shape
#: that let a dead substrate pass for two weeks — the caller would have to remember to ask the
#: question that matters most when nobody is thinking about it. Passing `None` explicitly still
#: disables it, for the caller that genuinely has no repo to read.
_HEARTBEAT_AUTO = object()


def _heartbeat_refusal(substrate: Substrate, source: str, heartbeat,
                       now: Optional[_dt.datetime]) -> Optional[Refusal]:
    """Leg 8: is the substrate this contract names actually proven live? See RULE_HEARTBEAT_DEAD.

    Never raises and never REFUSES ON ITS OWN ABSENCE: if the heartbeat module cannot be
    imported at all, this reports nothing rather than refusing every off-machine contract on the
    strength of its own breakage. That is the one direction this leg must not be wrong in — a
    validator whose failure mode is "refuse everything" gets bypassed wholesale, and the bypass
    takes the other seven legs with it.
    """
    if substrate.operator_disk:
        return None                    # the operator is sitting at it; liveness is not in doubt
    try:
        try:
            from scripts import substrate_heartbeat as _hb
        except ImportError:            # pragma: no cover - the alternate launch path
            import substrate_heartbeat as _hb
    except ImportError:                # pragma: no cover - the module is genuinely absent
        return None

    receipt = _hb.read_receipt(_REPO_ROOT) if heartbeat is _HEARTBEAT_AUTO else heartbeat
    if receipt is None:
        return None
    lines = _hb.predispatch(_REPO_ROOT, substrate.name, now=now, receipt=receipt)
    if not lines:
        return None
    return Refusal(
        rule=RULE_HEARTBEAT_DEAD, source=source, substrate=substrate.name,
        detail=(f"declares substrate {substrate.name!r}, which runs off the operator's machine "
                f"and is not proven live: {'; '.join(lines)}. A dead substrate must be a "
                f"refusal at dispatch, not a discovery mid-batch — the codespace substrate was "
                f"dead for two weeks while the platform reported Available, and eight lanes "
                f"were deferred off the back of it ([#746])"))


def validate_contract(text: str, *, source: str,
                      registry: Mapping[str, Substrate],
                      heartbeat=_HEARTBEAT_AUTO,
                      now: Optional[_dt.datetime] = None) -> list[Refusal]:
    """Legs 1-3 and 8 plus the unknown-override report, for ONE contract.

    Leg 4 needs the whole batch and lives in `validate_batch`. Every problem is returned, not
    the first: a contract with two contradictions gets told about both, the same posture
    `gen_lane_contract.parse_contract` takes at layer 1.
    """
    overrides = declared_overrides(text)
    out: list[Refusal] = []

    for rule in sorted(set(overrides) - set(RULE_IDS)):
        out.append(Refusal(
            rule=RULE_UNKNOWN_OVERRIDE, source=source,
            detail=(f"a recorded deviation names rule {rule!r}, which is outside the closed "
                    f"set {{{' | '.join(RULE_IDS)}}} — a deviation from a rule that does not "
                    f"exist discharges nothing")))

    # --- leg 7 (`[#629]`): checked FIRST and unconditionally -- it is about the contract's
    # internal consistency, not its substrate, so it must fire even on a contract whose
    # substrate declaration is itself broken (the two defects are independent).
    subtracted = sorted(set(amendment_subtractions(text)))
    if subtracted:
        out.append(_apply_override(Refusal(
            rule=RULE_AMENDMENT_SUBTRACTS, source=source,
            detail=(f"an amendment block negates {', '.join(subtracted)}, which the "
                    f"contract's own body still contains — an amendment is ADDITIVE; a "
                    f"ruling that narrows a frozen contract must REISSUE it through "
                    f"`gen_lane_contract`, not annotate it (the DC-3 shape, `[#629]`)")),
            overrides))

    name = declared_substrate(text)
    substrate = registry.get(name) if name else None

    if substrate is None or not substrate.live:
        if name is None:
            detail = ("declares no substrate — a contract that does not say where it runs "
                      f"cannot have its content checked against anything (enum: "
                      f"{{{' | '.join(sorted(registry))}}})")
        elif substrate is None:
            detail = (f"declares substrate {name!r}, which is outside the registry "
                      f"{{{' | '.join(sorted(registry))}}} — a miss is refused, "
                      f"not rounded to a neighbour")
        else:
            detail = (f"declares substrate {name!r}, which is registered with no live verb "
                      f"({', '.join(substrate.verbs)}) — the substrate is declared and "
                      f"unbacked")
        out.append(_apply_override(
            Refusal(rule=RULE_NO_LIVE_VERB, source=source, detail=detail, substrate=name),
            overrides))
        return out

    if not substrate.admits_gate_dependent_work:
        done = done_when_section(text)
        hits = [label for label, pattern in _GATE_TOKEN_RES if pattern.search(done)]
        if hits:
            out.append(_apply_override(Refusal(
                rule=RULE_CLOUD_GATE, source=source, substrate=substrate.name,
                detail=(f"declares substrate {substrate.name!r} and its Done-when depends on "
                        f"a gate ({', '.join(hits)}) — PLAYBOOK Ch8 Layer-1 Q1 routes "
                        f"gate-dependent work away from it: no hook is armed there")), overrides))

    if not substrate.operator_disk:
        hits = [label for label, pattern in _OPERATOR_PATH_RES if pattern.search(text)]
        if hits:
            out.append(_apply_override(Refusal(
                rule=RULE_OFFMACHINE_PATH, source=source, substrate=substrate.name,
                detail=(f"declares substrate {substrate.name!r}, which runs off the "
                        f"operator's machine, and names {', '.join(hits)} — the transport "
                        f"cannot reach it")), overrides))

    # --- leg 5: the teardown enum must be able to SEE this lane ----------------------------
    #
    # THE PREDICATE IS `validate_branch_naming.is_lane_branch`, and it is NAMED in the refusal
    # rather than described, so a reader can run the same test the validator ran.
    #
    # WHAT THIS LEG USED TO ASK, and why it was the wrong question. It matched `LANE_BRANCH_RE`
    # — the BATCH-lane grammar, `worktree-lane-<letter>-<id>-<slug>` — so it refused every
    # cloud lane on `claude/<slug>`, every epic lane and every automation lane, all three of
    # which are RATIFIED members of the lane enum that `classify()` (same module, same file)
    # calls conforming. The leg was written to ask "can a teardown that iterates the enum see
    # this lane"; it was implemented asking "is this one particular member of the enum". The
    # gap between the two was paid in hand-written `**Substrate deviation:**` prose on every
    # cloud contract — three of them live on 2026-09-06 alone — which is a workaround for a
    # question the validator was asking wrong, not a deviation from a rule.
    #
    # WHAT STILL REFUSES. A name outside the enum entirely (`unknown`), and a bare
    # `worktree-<name>` native worktree, which is deliberately NOT in `LANE_BRANCH_KINDS`: it
    # pairs to no contract file, so an enum-iterating teardown has nothing to attribute it to.
    #
    # HONEST LIMIT, unchanged: this checks the branch NAME against the enum. It cannot check
    # that a teardown actually ran — only that the lane is of a shape an enum-iterating
    # teardown could reach. Nor does it promise the ADR-110 exemption will fire for the branch:
    # that rule needs a committed open manifest too, and its per-organ reach is narrower still
    # (`block_unanchored_push` carries no exemption AT ALL, by ADR-85 containment). A manifest
    # that enumerates the lane by name discharges this leg, and that is what the recorded
    # deviation is for.
    branch = lane_branch(text)
    if branch is not None and not is_lane_branch(branch):
        out.append(_apply_override(Refusal(
            rule=RULE_TEARDOWN_ENUM, source=source, substrate=name,
            detail=(f"pairs to branch {branch!r}, which `validate_branch_naming.is_lane_branch`"
                    f" does not admit — the batch teardown and the ADR-110 exemption both "
                    f"iterate that enum, so this lane is invisible to both (ADR-116 / "
                    f"`claude/lane-f`). The enum is `LANE_BRANCH_KINDS` = batch-lane "
                    f"(`worktree-lane-<letter>-<id>-<slug>`), cloud-lane (`claude/<slug>`), "
                    f"epic-lane (`epic/<slug>`), automation-lane (`automation/<slug>`); a bare "
                    f"`worktree-<name>` is NOT a lane. Declare the lane in the manifest and "
                    f"record the deviation, or rename it to a member of that set")), overrides))

    # --- leg 8: the substrate this contract names must be PROVEN LIVE ----------------------
    dead = _heartbeat_refusal(substrate, source, heartbeat, now)
    if dead is not None:
        out.append(_apply_override(dead, overrides))

    return out


def validate_batch(contracts: Mapping[str, str], *,
                   registry: Mapping[str, Substrate]) -> list[Refusal]:
    """Every leg, across a whole batch. Leg 4 lives here because it is a batch property.

    Returns the per-contract refusals in `contracts` iteration order, then the writer WARNs.
    A contract whose substrate is unresolvable is excluded from leg 4: it already carries a
    leg-1 refusal, and guessing its checkout would stack a second finding on the same defect.
    """
    out: list[Refusal] = []
    checkouts: dict[str, list[str]] = {}

    for source, text in contracts.items():
        out.extend(validate_contract(text, source=source, registry=registry))
        name = declared_substrate(text)
        substrate = registry.get(name) if name else None
        if substrate is None or not substrate.live or substrate.family != "local":
            continue
        checkouts.setdefault(checkout_key(text, substrate), []).append(source)

    for key, sources in sorted(checkouts.items()):
        if len(sources) < 2:
            continue
        overrides: dict[str, str] = {}
        for source in sources:
            overrides.update(declared_overrides(contracts[source]))
        out.append(_apply_override(Refusal(
            rule=RULE_SECOND_LOCAL_WRITER, source=", ".join(sources),
            severity=SEVERITY_WARN,
            detail=(f"{len(sources)} local lanes write in checkout {key!r} "
                    f"({', '.join(sources)}) — PLAYBOOK Ch8's concurrency ceiling is one "
                    f"WRITER per checkout; parallelism only across worktrees")), overrides))

    # --- leg 6: declared write-scopes must not intersect ------------------------------------
    #
    # Batch E's cut collapsed two colliding doctrine lanes into one and stripped a file from a
    # third's scope, then required the disjointness be re-verified HERE rather than asserted in
    # prose. Pairwise because the report has to name WHICH two lanes and WHICH file: a single
    # "some scopes overlap" finding is not actionable at freeze.
    #
    # HONEST LIMIT: this compares DECLARED scopes. A lane that writes outside its declaration
    # is a different defect and this leg cannot see it — layer 1's docstring makes the same
    # admission about footprint claims, and it is still true here.
    scopes = {source: write_scope_paths(text) for source, text in contracts.items()}
    ordered = list(contracts)
    for i, left in enumerate(ordered):
        for right in ordered[i + 1:]:
            shared = scopes[left] & scopes[right]
            if not shared:
                continue
            overrides = dict(declared_overrides(contracts[left]))
            overrides.update(declared_overrides(contracts[right]))
            out.append(_apply_override(Refusal(
                rule=RULE_WRITE_SCOPE_DISJOINT, source=f"{left}, {right}",
                detail=(f"declared write-scopes intersect on {', '.join(sorted(shared))} — "
                        f"two lanes writing one file is a merge conflict the batch has "
                        f"already decided to have; chain them into ONE lane or move the "
                        f"file out of one scope")), overrides))

    return out


def refusals_only(findings: Iterable[Refusal]) -> list[Refusal]:
    """The subset a CLI exits non-zero on: severity `refuse`, i.e. not overridden and not a
    leg that lands as a WARN by the row's own words."""
    return [f for f in findings if f.severity == SEVERITY_REFUSE]


# --- CLI -----------------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    """`python scripts/validate_substrate.py <contract.md> [...]`.

    Argparse rather than Click, deliberately: this module is imported by an `audit_checks`
    check that runs inside the commit hook, and the cloud substrate it validates is measured
    as having no `click` (intake #45). A validator that cannot import on the substrate it
    polices is the family-3 defect `[#596]` names.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Substrate validator, layer 2 — refuse a contract whose declared "
                    "substrate contradicts its own content ([#591]).")
    parser.add_argument("paths", nargs="+", type=Path, help="contract file(s) to validate")
    parser.add_argument("--repo-root", type=Path, default=repo_root(),
                        help="repo root holding the substrate registry")
    parser.add_argument("--rules", action="store_true",
                        help="print the closed rule surface and exit")
    args = parser.parse_args(argv)

    if args.rules:
        for rule in RULE_IDS:
            print(rule)
        return 0

    try:
        registry = load_registry(args.repo_root)
    except SubstrateRegistryError as exc:
        logger.error("%s", exc)
        return 2

    contracts: dict[str, str] = {}
    for path in args.paths:
        try:
            contracts[str(path)] = path.read_text(encoding="utf-8")
        except OSError as exc:
            logger.error("could not read %s: %r", path, exc)
            return 2

    findings = validate_batch(contracts, registry=registry)
    for finding in findings:
        (logger.error if finding.severity == SEVERITY_REFUSE else logger.warning)(
            "%s", finding.render())
    if not findings:
        logger.info("%d contract(s): OK — substrate declaration agrees with content",
                    len(contracts))
    return 1 if refusals_only(findings) else 0


if __name__ == "__main__":
    raise SystemExit(_main())
