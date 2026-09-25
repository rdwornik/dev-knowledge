#!/usr/bin/env python
"""plan_lint.py — the architect's plan is checked by code before it freezes (`[#961]`, FR6).

THE MISS THIS CLOSES. Three waves running, the architect missed two cross-lane dependencies,
wrote one lane's instructions so they contradicted another's, and set two time targets with no
measurement behind them (`DECLARE-WAVE4B-DIRECTION-2026-09-22.md` RC6). The concrete instance is
the wave-4a **W4-2 / W4-4 conflict**: `LANE-W4-2-merge-gates-truth.md` owns "the `merge` moment of
`ecosystem/harness.yaml`" and reorders its organ list; `LANE-W4-4-connection-hygiene.md` owns the
connection-test module, whose `tests/test_connection_loop.py` hard-codes that same moment's fired
organs as a literal Python list (`EXPECTED_STOPS`, the `merge.organs` assertion). Nothing before
this lane read the two contracts side by side and noticed they touch the same coupling. This
module is that read, run BEFORE a wave's contracts freeze rather than discovered mid-batch.

WHAT IT READS, AND WHAT IT NEVER DOES. Four inputs, all read-only: the wave's `LANE-*.md`
contracts (this repo's transport format — `## Dispatch`, `**Files you own:**`, `slug `<slug>``
the pairing line, an optional `**Serial: …**`, `**Starts after `<lane>` … is/are merged**`
clause, or `serialize-group: <label>`), `ecosystem/harness.yaml` (via
`graph_queries.load_declaration`, library-first — this module holds no second YAML reader), the
real test files those contracts claim to own, and `logs/MERGE-RECEIPTS.jsonl` for the estimate.
It writes nothing, ever — Layer 2 never executes (Critical Rule #4; ADR-28/36), and a plan LINT
is a reader by its very nature.

ONE GRAMMAR, WRITTEN AND READ (`lane-plan-lint-grammar`, WAVE5B-N1). Before this lane three
shapes of the same clause existed: `templates/lane-contract-template.md` wrote
`**Starts after `<lane>` is merged.**` (singular) and carried no `slug `<slug>`` pairing line at
all; this module's `_STARTS_AFTER_RE` matched only the plural `…are merged**`, silently blind to
the template's own singular spelling; `scripts/gen_lane_contract.py` enforces a THIRD shape
entirely (`## Decision budget` / `## Steps` / `## What NOT to do`, a `--model`-less Dispatch
line, and a `{opus|sonnet|haiku|opusplan}` alias in its routing row — the opposite of the
explicit-id rule below) and is out of this lane's scope (`Do not`). The template now carries the
pairing line and both the singular and plural spellings (proper subject-verb agreement: one
named dependency reads `is merged`, more than one reads `…are merged`); `_STARTS_AFTER_RE` below
reads both, so the grammar the template WRITES is the one this module READS.

SIX FINDING CLASSES (the Done-contract's own enumeration, plus D14's and this lane's additions),
each returning the two contracts involved (class 6 returns one contract against itself — a
self-finding, the same shape class 5 already uses):

  1. **File collision** — two lanes' `Files you own` overlap (exact path, or one path is a
     directory ancestor of the other).
  2. **Missing producer** — a lane's declared `**Consumes:** `X`` names an artifact no lane's
     `**Produces:** `X`` supplies. (Neither annotation is yet used by a real contract in this
     corpus — the convention is introduced here for a future contract to adopt; the synthetic
     acceptance tests exercise it, and it produces zero findings on the corpus as filed today.)
  3. **Moment/test coupling** (the W4-2/W4-4 class) — a lane owns a `harness.yaml` moment ("the
     `<moment>` moment of/in `ecosystem/harness.yaml`") and a DIFFERENT lane owns a test surface
     that hard-codes two or more of that moment's organ ids as literal quoted strings.
  4. **Serial mismatch** — a lane declares itself `**Serial: …**` with every/N other lanes
     waiting for its merge, and another lane in the same set explicitly declares it "wait[s] for
     none" / "depend[s] on no other lane" (a direct textual contradiction); or a lane declares it
     waits for a specifically named lane's merge that lane never declares itself serial for.
  5. **New organ, no fate** (DECLARE-WINDOW-DEFECTS-2026-09-23 D14, the LANE-W4B-2 instance) — a
     lane's `Files you own` names a `scripts/*.py` file that does not exist yet, and nothing in
     the contract's own text commits to a `fates:` line or a moment for it. See
     `find_new_organs_without_fate` for the full account.
  6. **Model alias** (`lane-plan-lint-grammar`, WAVE5B-N1) — a contract's Model table or
     Dispatch line names a bare alias (`opus`, `sonnet`, `haiku`, `opusplan`) instead of an
     explicit, versioned id — the night rule `BATCH-COMMON-WAVE5B-N1-2026-09-24.md` §5 states
     ("Ordered models tonight … explicit ids, no alias") and the registry's own alias-drift note
     explains why it matters (`ecosystem/provider-registry.yaml`, roles.orchestrate: Claude Code
     2.1.280 silently repointed the bare `opus` alias to a different model than the id the
     registry pins). A FREEZE-time refusal, distinct from `lane-launcher-fixes`' own alias check
     in `scripts/dispatch.py launch` (a LAUNCH-time warning that does not refuse). See
     `find_model_aliases` for the full account, including the honest limit on the id it names.

ORDERING SUPPRESSES CLASSES 1 AND 3, NEVER CLASS 4 — and that split is deliberate, not an
oversight. A file collision or a moment/test coupling is a REAL hazard only while the two lanes
could run unordered; `LANE-W4B-1-merge-path.md`'s own text — "Starts after `lane-handback-organ`
and `lane-gate-verdicts` are merged" — resolves the *exact same class* of coupling against
`LANE-W4B-3-gate-verdicts.md` (both own `tests/test_connection_loop.py`'s merge-moment
expectations) precisely by declaring the order this module can read. Reported as `ORDERED`
(informational) rather than dropped, because the coupling is still real — it is a merge-conflict
surface either way — but it is not the class this lane exists to force a freeze-time refusal on.
A serial mismatch is different in kind: it is a CONTRADICTION between two contracts' own claims
about the same fact, and no dependency edge resolves a contradiction — an edge is exactly what a
serial declaration IS, so "ordered" cannot be the answer to "do these two clauses agree".

HONEST LIMITS, so a finding here is not over-read:

  * **"Files you own" is prose, and this is a pattern reader, not a parser of English.** Only the
    grammar this repo's transport actually uses is recognised: backtick-quoted paths inside the
    `**Files you own:**` paragraph, `**Serial: …**`, `**Starts after `<lane>` … is/are merged**`
    (either subject-verb agreement, and the em-dash appositive real contracts add — "…every lane
    named here — are merged" — is transparent to the match either way), "wait for none" /
    "depend(s) on no other lane", `serialize-group: <label>`. A contract that states an ownership
    or a dependency some other way is invisible to this reader and produces no finding —
    silently, not with a refusal, because there is no way to distinguish "states nothing" from
    "states it in a form not yet taught to this module" from the text alone.
  * **`serialize-group:` orders a group, but not WHICH member runs first, and never overrides a
    DECLARED order.** The label (same grammar `tasks/*.md` frontmatter and
    `scripts/validate_backlog.py` already use — a shared-mutable-resource DISJOINTNESS marker,
    not a stated order) says two lanes must not run concurrently; it does not say which one goes
    first. For a pair with no `Serial`/`Starts after` edge between them, this module orders them
    in the sequence they were PASSED to `lint`/`build_edges` — the same sequence the batch's own
    "merge priority = the table's order" convention already gives a caller reason to pass them
    in. For a pair a `Serial`/`Starts after` edge ALREADY orders (in either direction), that
    declared edge wins and the input-order guess is dropped — an earlier version let the guess
    fight a real edge and manufacture a cycle out of a legitimate plan (Codex terra review,
    HIGH). A caller that passes a group in some other order gets that guessed order instead for
    the pairs with no declared edge; this module never re-derives "the table's order" from
    anything but its own argument sequence.
  * **The model-alias explicit id is a STATED snapshot, not a live query.** No CLI on this host
    exposes a model-listing subcommand for `claude` (Part Z, `to-browser/SESSION-step0-wave5b-n1-
    2026-09-24.md`: "claude 2.1.282: no model-listing subcommand"), so nothing in this repo can
    re-derive "what does `opus` resolve to today" at lint time; `_ALIAS_EXPLICIT_ID` is a small,
    dated, cited table, and a future alias repoint (the exact failure the registry's own
    "ALIAS DRIFT, MADE VISIBLE" note records already happened once) makes it stale until someone
    re-reads the source and edits it — this module cannot detect that staleness, only state the
    id it currently believes.
  * **A bare-directory ownership claim (`tests/` with no filename) is scoped to the CANDIDATE
    files this module can name, not every file under that directory.** The candidate set is the
    `.py` files directly inside the directory whose stem shares a keyword (5+ letters, common
    words excluded) with the prose that named the directory. Unscoped, "fixtures under `tests/`"
    would glob roughly 250 files and attribute every one of them — including modules owned by
    lanes years apart from this wave — to whichever lane merely wrote the word "tests". Scoped,
    it can also MISS a real coupling whose filename shares no word with the prose; that miss is
    accepted over the noise the unscoped version measured.
  * **The moment/test coupling check reads literal QUOTED organ-id strings, at a threshold of
    two.** One incidental match (an organ id mentioned in a comment, a docstring, an unrelated
    fixture) is not a coupling; the real W4-2/W4-4 instance carries five.
  * **The estimate is a stated formula, not a measured one.** `serial_chain_len x lane_median +
    lane_count x merge_median` — the longest dependency chain (in lane count) times the median
    single-lane work time, plus every lane's own merge cost at the median pickup-to-push time.
    Parallel lanes off the critical chain are assumed free relative to it; a batch bottlenecked
    elsewhere (seat ceiling, review capacity) will run longer than this number and the number does
    not know it. Read via `merge_receipt.median_report`, unmodified — this module holds no second
    copy of that arithmetic or its small-n caveats.

LIBRARY-FIRST, each cited: `graph_queries.load_declaration` reads `ecosystem/harness.yaml` (no
second YAML reader here); `merge_receipt.read_ledger` / `median_report` read and summarise
`logs/MERGE-RECEIPTS.jsonl` (no second statistics pass here). The alias table is local, static
data, not a live registry read — `ecosystem/provider-registry.yaml` records model IDENTITY and
ROLE RANKING (its own header), not a bare-alias resolution table, and no CLI on this host can be
queried for one (see the honest limit above) — so there is no second reader to defer to here.
This module's only new code is the contract-prose grammar, the dependency-edge graph over it,
and the six finding predicates.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(_SCRIPTS))

try:  # pragma: no cover -- exercised by whichever entrypoint the caller uses
    from scripts import graph_queries as gq
except ImportError:  # pragma: no cover
    import graph_queries as gq

try:  # pragma: no cover
    from scripts import merge_receipt as mr
except ImportError:  # pragma: no cover
    import merge_receipt as mr


# --- contract grammar ------------------------------------------------------------------------

#: The `**Files you own:**` paragraph: from the label to the next blank line (or end of text).
_FILES_YOU_OWN_RE = re.compile(
    r"\*\*Files you own:\*\*\s*(?P<body>.*?)(?:\n\s*\n|\Z)", re.DOTALL)
#: A backtick-quoted token that looks like a repo path (contains a `/`) — excludes bare
#: identifiers like `merge_receipt.open` or `harness.yaml`'s own moment name, which are quoted
#: in the same paragraph but are not files.
_PATH_TOKEN_RE = re.compile(r"`([^`]*/[^`]*)`")
#: "the `<moment>` moment of/in `ecosystem/harness.yaml`" — both prepositions are attested
#: (LANE-W4-2 uses "of", LANE-W4B-1 uses "in").
_MOMENT_OWNERSHIP_RE = re.compile(
    r"the `(?P<moment>[\w-]+)` moment (?:of|in) `ecosystem/harness\.yaml`")
#: "**Serial: <detail>**" — a single bolded span, the live grammar (`LANE-W4-1`, `LANE-W4B-0`).
_SERIAL_RE = re.compile(r"\*\*Serial:\s*(?P<detail>[^*]+)\*\*")
#: "**Starts after `<lane>` and `<lane>` … is/are merged**" (`LANE-W4B-1`, and the corrected
#: `templates/lane-contract-template.md`) — an explicit, named ordering, distinct from the
#: `Serial` clause's implicit "every other lane" scope. ONE GRAMMAR, READ BOTH WAYS
#: (`lane-plan-lint-grammar`, WAVE5B-N1): before this lane the regex matched only the plural
#: `…are merged**`, so the template's own singular `**Starts after `<lane>` is merged.**` (one
#: named dependency, correct subject-verb agreement) was invisible to it — the exact grammar
#: mismatch `LANE-5B-6-plan-lint-grammar.md`'s Value line names. `(?:is|are)` reads both; the
#: real corpus's em-dash appositive ("… — every lane named here — are merged") falls inside the
#: non-greedy `body` group either way, so it is transparent to the match, not a third spelling.
_STARTS_AFTER_RE = re.compile(
    r"\*\*Starts after\s+(?P<body>.*?)\s*(?:is|are) merged\.?\*\*", re.DOTALL)
#: "serialize-group: <label>" — the SAME clause grammar `tasks/*.md` frontmatter and
#: `scripts/validate_backlog.py::_SERIALIZE_CLAUSE_RE` already use for "these share a mutable
#: resource, do not run them concurrently": an ASCII token, `[A-Za-z0-9][A-Za-z0-9_-]*`. Not yet
#: used by a real `LANE-*.md` contract (the real corpus expresses the one instance of this need —
#: three lanes all touching `ecosystem/harness.yaml` — through ruling (g)/(f)'s additive-conflict
#: carve-out instead); introduced here for a future contract to adopt, exercised by the synthetic
#: acceptance tests, the same posture as `Produces:`/`Consumes:` below.
_SERIALIZE_GROUP_RE = re.compile(r"serialize-group:\s*(?P<group>[A-Za-z0-9][A-Za-z0-9_-]*)")
#: "wait for none" / "depend(s) on no other lane" (`LANE-W4-4` v1) — an explicit disclaimer of
#: every dependency, checked against a `Serial` lane's claim that this lane waits for it.
_WAIT_FOR_NONE_RE = re.compile(r"wait for none|depends? on no other lane", re.IGNORECASE)
#: "wait[s] for `<lane>`'s merge" — a NAMED wait, distinct from `Serial`'s implicit scope and
#: from `Starts after`'s explicit list. Not attested in this corpus; exercised by synthetic
#: fixtures only (class 4's second leg, "a wait on a lane that is not serial").
_NAMED_WAIT_RE = re.compile(r"waits? for `(?P<lane>[\w-]+)`'?s? merge", re.IGNORECASE)
#: `**Produces:** `X`, `Y`` / `**Consumes:** `X`` — a convention this lane introduces; not yet
#: used by a real contract, exercised by the synthetic acceptance tests.
_PRODUCES_RE = re.compile(r"\*\*Produces:\*\*\s*(?P<body>[^\n]*)")
_CONSUMES_RE = re.compile(r"\*\*Consumes:\*\*\s*(?P<body>[^\n]*)")
#: The lane slug, from the dispatch pairing line every contract carries
#: (`gen_lane_contract._PAIRING_RE`'s own grammar — read here rather than re-derived, since a
#: second copy of "where the slug lives" is exactly the drift class this repo's contracts exist
#: to avoid). Matched independently rather than imported: `gen_lane_contract` validates a
#: contract's STRUCTURE and raises on a malformed one, where this module's job is to read
#: whatever a real, already-frozen contract says, structurally valid or not.
_SLUG_RE = re.compile(r"slug\s+`(?P<slug>[^`]+)`")
#: A contract's own commitment to give a new organ a fate (class 5, D14): the literal YAML key
#: `fates:` (colon required — a bare "fate"/"fates" is ordinary English and would suppress the
#: finding on unrelated prose, Codex terra review HIGH,
#: `docs/audits/2026-09-24-codex-lane-handback-fixes.md`) or one of the two dated-fate shape
#: keywords `manual_until` / `retire_candidate`. The bare word "moment" is deliberately NOT
#: matched here — a lane declaring itself at a `harness.yaml` moment is already exempted at
#: the per-lane level via `moments_touched` (see `find_new_organs_without_fate`), and matching
#: "moment" as loose English (as in "at this moment") is exactly the over-suppression the same
#: review flagged. Anywhere in the contract, not scoped to `Files you own` — a fate is
#: typically declared in the Done-contract section, not the file list.
_FATE_MENTION_RE = re.compile(r"fates:|manual_until|retire.candidate", re.IGNORECASE)
#: The `| Model | Mode | Effort |` table's data row (`templates/lane-contract-template.md`,
#: `scripts/dispatch.py launch` reads the same table for the same field) — the first cell.
_MODEL_TABLE_RE = re.compile(
    r"\|\s*Model\s*\|\s*Mode\s*\|\s*Effort\s*\|\s*\n"
    r"\s*\|[-:\s|]+\|\s*\n"
    r"\s*\|\s*(?P<model>[^|\n]+?)\s*\|")
#: The `## Dispatch` heading's own fenced code block — scoped so `--model` is read ONLY from the
#: actual launch command, never from unrelated prose elsewhere in the contract (a `Do not` line
#: quoting `--model opus` as an example, or a `Read first` bullet). Codex terra review, HIGH: an
#: earlier version searched the WHOLE contract text for `--model`, so documentation mentioning
#: the flag could trip a BLOCKING alias finding that named no real Dispatch line.
_DISPATCH_FENCE_RE = re.compile(r"##\s*Dispatch\s*\n+```[^\n]*\n(?P<body>.*?)```", re.DOTALL)
#: The `--model <value>` token, read only within `_DISPATCH_FENCE_RE`'s captured body.
_DISPATCH_MODEL_RE = re.compile(r"--model\s+(?P<model>[^\s\"]+)")
#: Class 6's closed vocabulary — the four bare aliases the batch's night rule (`BATCH-COMMON-
#: WAVE5B-N1-2026-09-24.md` §5, "no alias in any contract") and `scripts/gen_lane_contract.py`'s
#: own `MODEL_ENUM` both name, matched only as an EXACT, case-insensitive value of the Model
#: table's first cell or a `--model` argument INSIDE the `## Dispatch` fence
#: (`_DISPATCH_FENCE_RE`) — never as a substring scan of the contract's whole prose, which would
#: false-positive on every explicit id that CONTAINS one of these words (`claude-opus-5-5`,
#: `claude-sonnet-5`), on ordinary discussion of the alias itself (this contract's own
#: Done-contract item 3 names all four), and on a `--model` mentioned outside the real launch
#: command (a `Do not` example, a `Read first` bullet) -- Codex terra review, HIGH, on the
#: `--model` leg specifically.
_ALIASES = frozenset({"opus", "opusplan", "sonnet", "haiku"})
#: Alias -> the explicit id it resolves to TODAY, per the registry's own alias-drift note
#: (`ecosystem/provider-registry.yaml`, `roles.orchestrate`: "Claude Code 2.1.280 made
#: `claude-opus-5-5` the DEFAULT Opus model, which means the bare `opus` alias … now RESOLVES to
#: `claude-opus-5-5`") and Part Z's per-provider currency probe
#: (`to-browser/SESSION-step0-wave5b-n1-2026-09-24.md`). `opusplan` is a MODE (plan mode) layered
#: on the opus alias (`scripts/gen_lane_contract.py`'s `MODEL_ENUM` comment), not a separate
#: model, so it resolves to the same id. HONEST LIMIT: a snapshot, not a live query — see the
#: module docstring's honest limits for why nothing in this repo can re-derive it at lint time.
_ALIAS_EXPLICIT_ID: dict[str, str] = {
    "opus": "claude-opus-5-5",
    "opusplan": "claude-opus-5-5",
    "sonnet": "claude-sonnet-5",
    "haiku": "claude-haiku-4-5-20251001",
}


def _quoted_tokens(text: str) -> tuple[str, ...]:
    return tuple(m.group(1) for m in re.finditer(r"`([\w-]+)`", text))


@dataclass(frozen=True)
class LaneContract:
    """One `LANE-*.md` contract, read for exactly the fields plan-lint needs.

    Every field defaults to "declares nothing" (`False`, `()`, `None`) rather than raising — a
    contract that uses none of this grammar is a legal contract this module simply has nothing
    to say about (see the module docstring's first honest limit).
    """
    path: Path
    slug: str
    title: str
    owned_paths: tuple[str, ...] = ()
    files_you_own_text: str = ""
    full_text: str = ""
    moments_touched: tuple[str, ...] = ()
    serial: bool = False
    serial_detail: str = ""
    starts_after: tuple[str, ...] = ()
    wait_for_none: bool = False
    named_waits: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()
    consumes: tuple[str, ...] = ()
    serialize_group: str | None = None
    model_tokens: tuple[str, ...] = ()


_TITLE_RE = re.compile(r"^#\s+LANE\s+\S+\s+—\s+(?P<title>.+?)\s*$", re.MULTILINE)


def parse_lane_contract(path: Path) -> LaneContract:
    """Read one `LANE-*.md` contract. Never raises on prose it does not recognise — see the
    module docstring's honest limits; a missing slug is the one thing this refuses on, since
    every finding this module emits is keyed by slug."""
    text = path.read_text(encoding="utf-8")
    slug_match = _SLUG_RE.search(text)
    if slug_match is None:
        raise PlanLintError(f"{path}: no `slug `<slug>`` pairing line found — cannot key this "
                            f"contract's findings without one")
    slug = slug_match.group("slug")
    title_match = _TITLE_RE.search(text)
    title = title_match.group("title") if title_match else slug

    files_match = _FILES_YOU_OWN_RE.search(text)
    files_text = files_match.group("body") if files_match else ""
    owned = tuple(dict.fromkeys(m.group(1) for m in _PATH_TOKEN_RE.finditer(files_text)))
    moments = tuple(dict.fromkeys(m.group("moment") for m in _MOMENT_OWNERSHIP_RE.finditer(files_text)))

    serial_match = _SERIAL_RE.search(text)
    serial = serial_match is not None
    serial_detail = serial_match.group("detail").strip() if serial_match else ""

    starts_after: tuple[str, ...] = ()
    starts_match = _STARTS_AFTER_RE.search(text)
    if starts_match is not None:
        starts_after = _quoted_tokens(starts_match.group("body"))

    wait_for_none = _WAIT_FOR_NONE_RE.search(text) is not None
    named_waits = tuple(dict.fromkeys(m.group("lane") for m in _NAMED_WAIT_RE.finditer(text)))

    produces: list[str] = []
    for m in _PRODUCES_RE.finditer(text):
        produces.extend(_quoted_tokens(m.group("body")))
    consumes: list[str] = []
    for m in _CONSUMES_RE.finditer(text):
        consumes.extend(_quoted_tokens(m.group("body")))

    group_match = _SERIALIZE_GROUP_RE.search(text)
    serialize_group = group_match.group("group") if group_match else None

    model_tokens: list[str] = []
    model_table_match = _MODEL_TABLE_RE.search(text)
    if model_table_match is not None:
        model_tokens.append(model_table_match.group("model").strip())
    dispatch_match = _DISPATCH_FENCE_RE.search(text)
    if dispatch_match is not None:
        model_tokens.extend(
            m.group("model") for m in _DISPATCH_MODEL_RE.finditer(dispatch_match.group("body")))

    return LaneContract(
        path=path, slug=slug, title=title, owned_paths=owned, files_you_own_text=files_text,
        full_text=text, moments_touched=moments, serial=serial, serial_detail=serial_detail,
        starts_after=starts_after, wait_for_none=wait_for_none, named_waits=named_waits,
        produces=tuple(dict.fromkeys(produces)), consumes=tuple(dict.fromkeys(consumes)),
        serialize_group=serialize_group, model_tokens=tuple(dict.fromkeys(model_tokens)))


def load_contracts(paths: Sequence[Path]) -> tuple[LaneContract, ...]:
    """Every contract in `paths`, parsed. Duplicate slugs are refused: a finding keyed by slug
    is meaningless if the key is not unique within the set being linted."""
    out = tuple(parse_lane_contract(Path(p)) for p in paths)
    seen: dict[str, Path] = {}
    for lane in out:
        if lane.slug in seen:
            raise PlanLintError(
                f"duplicate slug {lane.slug!r}: {seen[lane.slug]} and {lane.path} — plan-lint "
                f"keys every finding by slug and cannot tell these two contracts apart")
        seen[lane.slug] = lane.path
    return out


class PlanLintError(ValueError):
    """A refusal: an input plan-lint declines to read (see docstrings above for each cause)."""


# --- the dependency graph --------------------------------------------------------------------

def build_edges(lanes: Sequence[LaneContract]) -> frozenset[tuple[str, str]]:
    """Every `(before, after)` ordering pair this set of contracts declares.

    Three sources, kept distinct because they answer different questions (see the module
    docstring): a `Serial` lane orders itself before every OTHER lane in `lanes` (the live
    grammar's "every other lane" / "N lanes wait" is read as scoped to the set it is asked
    about, not to some larger wave this function was not given); `Starts after` orders the named
    lane(s) before this one, however many or few other lanes exist; `serialize-group:` orders
    every PAIR of lanes sharing a label against each other that a `Serial`/`Starts after` edge
    does not ALREADY order, in the order they appear in `lanes` — the label itself only says the
    two must not run concurrently (the same DISJOINTNESS reading `boot_frontier.py`/
    `validate_backlog.py` give it), not which one goes first, so this function supplies a
    direction from its own argument order rather than inventing one from the label, and never
    lets that guess override a real declared edge (see the module docstring's honest limit).
    """
    slugs = tuple(lane.slug for lane in lanes)
    edges: set[tuple[str, str]] = set()
    for lane in lanes:
        if lane.serial:
            edges.update((lane.slug, other) for other in slugs if other != lane.slug)
        edges.update((dep, lane.slug) for dep in lane.starts_after if dep in slugs)
    #: The DECLARED edges only (Serial + Starts after), frozen BEFORE serialize-group runs.
    #: Codex terra review, HIGH: an earlier version let `serialize-group`'s input-order guess
    #: add an edge opposite a REAL declared dependency, manufacturing a cycle out of a
    #: legitimate plan and refusing it (`_refuse_cycles`) for a reason that was this function's
    #: own guess, not the contract's. A group pair already ordered the other way by a declared
    #: edge is left alone; only a pair `serialize-group` is the SOLE source of ordering for gets
    #: one, from input order (the honest limit above still applies to that case).
    declared_edges = frozenset(edges)
    groups: dict[str, list[str]] = {}
    for lane in lanes:
        if lane.serialize_group:
            groups.setdefault(lane.serialize_group, []).append(lane.slug)
    for members in groups.values():
        for i, earlier in enumerate(members):
            for later in members[i + 1:]:
                if _reachable(declared_edges, later, earlier):
                    continue
                edges.add((earlier, later))
    return frozenset(edges)


def _reachable(edges: frozenset[tuple[str, str]], start: str, goal: str) -> bool:
    """Is `goal` reachable from `start` by following declared edges — the transitive closure,
    computed on demand rather than cached, since the graphs plan-lint sees are a handful of
    lanes."""
    stack = [start]
    seen = {start}
    while stack:
        node = stack.pop()
        for a, b in edges:
            if a == node and b not in seen:
                if b == goal:
                    return True
                seen.add(b)
                stack.append(b)
    return False


def is_ordered(edges: frozenset[tuple[str, str]], a: str, b: str) -> bool:
    """Do the declared edges order `a` and `b` relative to each other, either direction."""
    return _reachable(edges, a, b) or _reachable(edges, b, a)


def find_cycle(lanes: Sequence[LaneContract],
               edges: frozenset[tuple[str, str]]) -> tuple[str, ...] | None:
    """A cycle among the declared edges, or `None`. Codex terra review (`[#961]` diff, HIGH):
    a cyclic `Starts after` (A after B, B after A) made `is_ordered(A, B)` True by construction,
    which silently downgraded a genuine collision to `ORDERED` for a pair with NO executable
    ordering at all -- the opposite of what that severity claims. Checked once, before any
    finding is classified, rather than left for `_longest_chain`'s internal guard to paper over
    on every call site that walks the graph."""
    adjacency: dict[str, list[str]] = {}
    for a, b in edges:
        adjacency.setdefault(a, []).append(b)
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {lane.slug: WHITE for lane in lanes}
    path: list[str] = []

    def visit(node: str) -> tuple[str, ...] | None:
        color[node] = GRAY
        path.append(node)
        for nxt in adjacency.get(node, ()):
            if color.get(nxt) == GRAY:
                start = path.index(nxt)
                return tuple(path[start:] + [nxt])
            if color.get(nxt, WHITE) == WHITE:
                found = visit(nxt)
                if found is not None:
                    return found
        path.pop()
        color[node] = BLACK
        return None

    for lane in lanes:
        if color[lane.slug] == WHITE:
            found = visit(lane.slug)
            if found is not None:
                return found
    return None


def _longest_chain(lanes: Sequence[LaneContract], edges: frozenset[tuple[str, str]]) -> int:
    """The longest dependency chain in this set, counted in LANES (a lane alone with no edge is
    a chain of 1). Used by `estimate_wave` — see the module docstring's estimate formula."""
    slugs = [lane.slug for lane in lanes]
    adjacency: dict[str, list[str]] = {}
    for a, b in edges:
        adjacency.setdefault(a, []).append(b)
    memo: dict[str, int] = {}

    def depth(node: str, on_path: frozenset[str]) -> int:
        if node in memo:
            return memo[node]
        if node in on_path:  # a cycle in declared edges — refuse to loop, not to crash
            return 1
        best = 1
        for nxt in adjacency.get(node, ()):
            best = max(best, 1 + depth(nxt, on_path | {node}))
        memo[node] = best
        return best

    return max((depth(s, frozenset()) for s in slugs), default=0)


# --- findings ---------------------------------------------------------------------------------

BLOCKING = "BLOCKING"
ORDERED = "ORDERED"


@dataclass(frozen=True)
class Finding:
    """One thing plan-lint found, naming the two contracts involved (the Done-contract's own
    shape: "Findings, each with the two contracts involved")."""
    category: str
    severity: str
    lane_a: str
    lane_b: str
    detail: str

    def render(self) -> str:
        return f"[{self.severity}] {self.category}: {self.lane_a} <-> {self.lane_b}: {self.detail}"


def _paths_collide(a: str, b: str) -> bool:
    """Same path, or one is a directory ancestor of the other."""
    if a == b:
        return True
    a_dir = a if a.endswith("/") else a + "/"
    b_dir = b if b.endswith("/") else b + "/"
    return b.startswith(a_dir) or a.startswith(b_dir)


def find_file_collisions(lanes: Sequence[LaneContract],
                         edges: frozenset[tuple[str, str]]) -> list[Finding]:
    """Class 1: two lanes' `Files you own` overlap."""
    out: list[Finding] = []
    for i, lane_a in enumerate(lanes):
        for lane_b in lanes[i + 1:]:
            for pa in lane_a.owned_paths:
                for pb in lane_b.owned_paths:
                    if _paths_collide(pa, pb):
                        severity = ORDERED if is_ordered(edges, lane_a.slug, lane_b.slug) else BLOCKING
                        out.append(Finding(
                            "file-collision", severity, lane_a.slug, lane_b.slug,
                            f"both own `{pa}` / `{pb}`" if pa != pb else f"both own `{pa}`"))
    return out


def find_missing_producers(lanes: Sequence[LaneContract]) -> list[Finding]:
    """Class 2: a lane consumes an artifact no lane in the set produces (see module docstring —
    the `**Produces:**` / `**Consumes:**` convention is not yet used by a real contract)."""
    produced = {artifact for lane in lanes for artifact in lane.produces}
    out: list[Finding] = []
    for lane in lanes:
        for artifact in lane.consumes:
            producers = [p.slug for p in lanes if artifact in p.produces and p.slug != lane.slug]
            if artifact not in produced:
                out.append(Finding(
                    "missing-producer", BLOCKING, lane.slug, lane.slug,
                    f"consumes `{artifact}`, which no lane in this set produces"))
            elif not producers:
                # produced only by itself -- not a cross-lane gap, nothing to report
                continue
    return out


# --- class 5: a new organ with no declared fate or moment (D14) -------------------------------

def find_new_organs_without_fate(lanes: Sequence[LaneContract], repo_root: Path) -> list[Finding]:
    """Class 5 (DECLARE-WINDOW-DEFECTS-2026-09-23 D14): a lane's `Files you own` names a
    `scripts/*.py` file that does not exist yet, with no textual commitment anywhere in the
    CONTRACT to give it a fate or a moment.

    THE INSTANCE THIS CATCHES BEFORE FREEZE. `LANE-W4B-2-handback-organ.md` introduced
    `scripts/handback.py`, forbade `ecosystem/harness.yaml` by name, and said nothing about a
    fate for the new organ. `check_organ_truth` refused the merge over exactly that gap, and an
    8-hour ruling (`ANSWER-integrator-wave4b-handback-organ.md`) had to authorize one dated
    `fates:` line after the lane had already written the code. This class is that same read,
    run over the CONTRACT PROSE before a lane starts.

    A lane already declaring itself at ANY `harness.yaml` moment (`moments_touched`) is exempt
    for every script it owns -- the same coarse, per-lane (not per-script) grain
    `find_moment_test_conflicts` already reads at; a lane that owns the ecosystem declaration is
    presumed to know it needs one.

    HONEST LIMIT (consistent with the module's others): this reads the CONTRACT's commitment,
    not whether the fate is actually correct or later honoured -- `check_organ_truth` still
    enforces that at merge. Gated on `ecosystem/harness.yaml` being readable at `repo_root` at
    all (`gq.MomentsUnreadable` -> no findings): a repo that declares no moments has nothing
    for a fate to be declared IN, the same posture `check_organ_truth` itself takes.
    """
    try:
        gq.load_declaration(repo_root)
    except gq.MomentsUnreadable:
        return []
    out: list[Finding] = []
    for lane in lanes:
        if lane.moments_touched:
            continue
        for token in lane.owned_paths:
            if not token.startswith("scripts/") or not token.endswith(".py"):
                continue
            if (Path(repo_root) / token).is_file():
                continue
            if _FATE_MENTION_RE.search(lane.full_text):
                continue
            out.append(Finding(
                "new-script-no-fate", BLOCKING, lane.slug, lane.slug,
                f"owns `{token}`, a script that does not exist yet, with no fate or moment "
                f"declared anywhere in this contract -- give it a `fates:` line "
                f"(`manual_until`/`retire_candidate`/`moment`) in ecosystem/harness.yaml or "
                f"name the moment it runs at, or `organ_truth` will refuse it at merge "
                f"(the LANE-W4B-2 instance, DECLARE D14)"))
    return out


# --- class 6: a model alias where an explicit id belongs (`lane-plan-lint-grammar`) -----------

def find_model_aliases(lanes: Sequence[LaneContract]) -> list[Finding]:
    """Class 6: a bare model alias (`opus`, `sonnet`, `haiku`, `opusplan`) named in a contract's
    Model table or Dispatch line, where the night rule requires an explicit, versioned id.

    A SELF-FINDING, the same shape class 5 already uses (`lane_a == lane_b`) — this is a
    property of one contract, not a relationship between two. FREEZE-TIME, and distinct from
    `lane-launcher-fixes`' own alias check in `scripts/dispatch.py launch` (a LAUNCH-time
    warning that does not refuse a launch) — this one runs before any lane launches, over the
    contract text itself, and is BLOCKING: the night rule (`BATCH-COMMON-WAVE5B-N1-2026-09-24.md`
    §5) states "no alias in any contract", not "warn on one".

    ONLY the Model table's first cell and a Dispatch `--model` argument are read — an EXACT,
    case-insensitive match against the closed alias vocabulary, never a substring scan of the
    contract's prose (see `_ALIASES`'s own comment for why: it would false-positive on every
    explicit id built from one of these words, and on ordinary discussion of the alias itself).
    """
    out: list[Finding] = []
    for lane in lanes:
        seen: set[str] = set()
        for token in lane.model_tokens:
            key = token.lower()
            if key not in _ALIASES or key in seen:
                continue
            seen.add(key)
            explicit = _ALIAS_EXPLICIT_ID.get(
                key, "no explicit id on file here -- see plan_lint.py's honest limit")
            out.append(Finding(
                "model-alias", BLOCKING, lane.slug, lane.slug,
                f"names the alias `{token}` in its Model table or Dispatch line, where an "
                f"explicit, versioned id belongs -- resolves today to `{explicit}`"))
    return out


#: Below this many literal organ-id hits, a match is an incidental mention, not a hard-coded list.
_MIN_ORGAN_HITS = 2
#: Words too common in this corpus's prose to anchor a directory scan (see the module docstring's
#: second honest limit). Kept short and explicit rather than a general stopword list — this is a
#: narrow heuristic, and a general list would claim a precision this reader does not have.
_DIRECTORY_SCAN_STOPWORDS = frozenset({
    "files", "your", "module", "fixtures", "under", "their", "deploy", "manifest", "entry",
    "tests", "test", "scripts", "which", "other", "stops", "still", "every", "found", "state",
})


def _sentence_around(text: str, token: str) -> str:
    """The one SENTENCE of `text` containing `` `token` `` -- bounded by the nearest `.` on
    each side (or the text's own edges).

    Scoping to the sentence, not the whole `Files you own` paragraph, is load-bearing: a real
    paragraph runs on past the file list into unrelated prose in the SAME block
    (`LANE-W4-4-connection-hygiene.md` carries a dependency disclaimer AND "re-run by the
    integrator at batch close" in the same paragraph as its `tests/` clause). Unscoped, that
    prose contributed the keyword "integrator" and matched `tests/test_integrator_surface.py` --
    a file this lane does not own, owned instead by a wave-2 lane years apart from this one.
    Measured against the real transport corpus while proving this module on real data.
    """
    needle = f"`{token}`"
    idx = text.find(needle)
    if idx == -1:
        return text
    start = text.rfind(".", 0, idx)
    start = start + 1 if start != -1 else 0
    end = text.find(".", idx)
    if end == -1:
        end = len(text)
    return text[start:end]


def _directory_scan_keywords(lane: LaneContract, token: str) -> frozenset[str]:
    sentence = _sentence_around(lane.files_you_own_text, token)
    prose = _PATH_TOKEN_RE.sub(" ", sentence)  # strip explicit paths first
    words = re.findall(r"[a-z]{5,}", prose.lower())
    return frozenset(w for w in words if w not in _DIRECTORY_SCAN_STOPWORDS)


def _candidate_test_files(lane: LaneContract, repo_root: Path) -> list[Path]:
    """Every `.py` file this lane's owned paths could plausibly mean — see the module docstring's
    second honest limit for why a bare directory is keyword-scoped rather than globbed whole."""
    out: dict[Path, None] = {}
    for token in lane.owned_paths:
        candidate = repo_root / token
        if token.endswith(".py"):
            if candidate.is_file():
                out.setdefault(candidate, None)
            continue
        directory = candidate if candidate.is_dir() else (repo_root / token.rstrip("/"))
        if not directory.is_dir():
            continue
        keywords = _directory_scan_keywords(lane, token)
        if not keywords:
            continue  # nothing to anchor the scan on -- refuse to glob the whole directory
        for py_file in sorted(directory.glob("*.py")):
            stem = py_file.stem.lower()
            if any(kw in stem for kw in keywords):
                out.setdefault(py_file, None)
    return list(out)


def _organ_literal_hits(path: Path, organ_ids: Sequence[str]) -> tuple[str, ...]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ()
    return tuple(o for o in organ_ids if f'"{o}"' in text or f"'{o}'" in text)


def _moment_organs(repo_root: Path) -> dict[str, list[str]]:
    try:
        declared = gq.load_declaration(repo_root)
    except gq.MomentsUnreadable:
        return {}
    out: dict[str, list[str]] = {}
    for organ in declared:
        if organ.moment.startswith("spine stage"):
            continue
        out.setdefault(organ.moment, []).append(organ.organ)
    return out


def find_moment_test_conflicts(lanes: Sequence[LaneContract], repo_root: Path,
                               edges: frozenset[tuple[str, str]]) -> list[Finding]:
    """Class 3, the W4-2/W4-4 class: a lane touches a `harness.yaml` moment another lane's owned
    test surface hard-codes as a literal organ list."""
    moment_organs = _moment_organs(repo_root)
    out: list[Finding] = []
    for owner in lanes:
        for moment in owner.moments_touched:
            organ_ids = moment_organs.get(moment, [])
            if not organ_ids:
                continue
            for other in lanes:
                if other.slug == owner.slug:
                    continue
                for test_file in _candidate_test_files(other, repo_root):
                    hits = _organ_literal_hits(test_file, organ_ids)
                    if len(hits) >= _MIN_ORGAN_HITS:
                        severity = ORDERED if is_ordered(edges, owner.slug, other.slug) else BLOCKING
                        rel = test_file.relative_to(repo_root).as_posix()
                        out.append(Finding(
                            "moment-test-coupling", severity, owner.slug, other.slug,
                            f"{owner.slug} owns/touches the `{moment}` moment of "
                            f"ecosystem/harness.yaml; {other.slug}'s {rel} hard-codes "
                            f"{len(hits)} of its organ ids as literals: {', '.join(sorted(hits))}"))
    return out


def find_serial_mismatches(lanes: Sequence[LaneContract]) -> list[Finding]:
    """Class 4: a serial lane another lane explicitly does not wait for; a named wait on a lane
    that never declares itself serial."""
    out: list[Finding] = []
    by_slug = {lane.slug: lane for lane in lanes}
    serial_lanes = [lane for lane in lanes if lane.serial]
    for serial_lane in serial_lanes:
        for other in lanes:
            if other.slug == serial_lane.slug:
                continue
            if other.wait_for_none:
                out.append(Finding(
                    "serial-mismatch", BLOCKING, serial_lane.slug, other.slug,
                    f"{serial_lane.slug} declares itself Serial ({serial_lane.serial_detail!r}), "
                    f"implying every other lane waits for its merge, but {other.slug} explicitly "
                    f"declares it waits for none / depends on no other lane"))
    for lane in lanes:
        for named in lane.named_waits:
            target = by_slug.get(named)
            if target is not None and not target.serial:
                out.append(Finding(
                    "serial-mismatch", BLOCKING, lane.slug, named,
                    f"{lane.slug} declares it waits for {named}'s merge, but {named}'s contract "
                    f"never declares itself Serial"))
    return out


def _refuse_cycles(lanes: Sequence[LaneContract], edges: frozenset[tuple[str, str]]) -> None:
    cycle = find_cycle(lanes, edges)
    if cycle is not None:
        raise PlanLintError(
            f"declared dependency edges form a cycle: {' -> '.join(cycle)} -- a cyclic "
            f"ordering has no executable schedule, and `is_ordered` would otherwise read every "
            f"pair on the cycle as ordered, silently downgrading a real collision to ORDERED")


def lint(lanes: Sequence[LaneContract], repo_root: Path) -> list[Finding]:
    """All six finding classes, over one set of contracts read together (a wave, or any set the
    caller wants cross-checked)."""
    edges = build_edges(lanes)
    _refuse_cycles(lanes, edges)
    findings: list[Finding] = []
    findings.extend(find_file_collisions(lanes, edges))
    findings.extend(find_missing_producers(lanes))
    findings.extend(find_moment_test_conflicts(lanes, repo_root, edges))
    findings.extend(find_serial_mismatches(lanes))
    findings.extend(find_new_organs_without_fate(lanes, repo_root))
    findings.extend(find_model_aliases(lanes))
    return findings


def render_findings(findings: Sequence[Finding]) -> str:
    if not findings:
        return "plan-lint: no findings"
    blocking = [f for f in findings if f.severity == BLOCKING]
    lines = [f"plan-lint: {len(findings)} finding(s), {len(blocking)} BLOCKING"]
    for f in findings:
        lines.append("  " + f.render())
    return "\n".join(lines)


# --- estimates ---------------------------------------------------------------------------------

@dataclass(frozen=True)
class WaveEstimate:
    """`serial_chain_len x lane_median + lane_count x merge_median` — see the module docstring's
    estimate honest limit for what this formula assumes and does not know."""
    lane_median: mr.MedianReport
    merge_median: mr.MedianReport
    serial_chain_len: int
    lane_count: int

    @property
    def minutes(self) -> float | None:
        if self.lane_median.n == 0 or self.merge_median.n == 0:
            return None
        return (self.serial_chain_len * self.lane_median.median_minutes
                + self.lane_count * self.merge_median.median_minutes)

    def render(self) -> str:
        lines = [
            "wave estimate = serial_chain_len x lane_median + lane_count x merge_median",
            f"  serial_chain_len = {self.serial_chain_len} lane(s) (longest declared dependency chain)",
            f"  lane_count       = {self.lane_count} lane(s)",
            "", "-- lane work time (kind=arc) --", self.lane_median.render(),
            "", "-- pickup-to-push time (kind=merge) --", self.merge_median.render(),
        ]
        if self.minutes is None:
            lines.append("")
            lines.append("estimate: UNDEFINED -- one or both medians have n=0 (see above)")
        else:
            hours = self.minutes / 60.0
            lines.append("")
            lines.append(f"estimate: {self.minutes:.1f} min (~{hours:.1f} h) = "
                         f"{self.serial_chain_len} x {self.lane_median.median_minutes:.1f} + "
                         f"{self.lane_count} x {self.merge_median.median_minutes:.1f}")
        return "\n".join(lines)


def estimate_wave(lanes: Sequence[LaneContract], repo_root: Path) -> WaveEstimate:
    edges = build_edges(lanes)
    _refuse_cycles(lanes, edges)
    receipts = mr.read_ledger(repo_root)
    lane_median = mr.median_report(receipts, kind=mr.KIND_ARC)
    merge_median = mr.median_report(receipts, kind=mr.KIND_MERGE)
    chain_len = _longest_chain(lanes, edges)
    return WaveEstimate(lane_median=lane_median, merge_median=merge_median,
                        serial_chain_len=chain_len, lane_count=len(lanes))


# --- CLI ----------------------------------------------------------------------------------------

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Check a wave's lane contracts before they freeze, and estimate its cost from receipts."""


@cli.command("check")
@click.argument("contracts", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path),
              default=_SCRIPTS.parent, show_default=True)
def cmd_check(contracts: tuple[Path, ...], repo_root: Path) -> None:
    """Findings across CONTRACTS -- two or more `LANE-*.md` files, read together as one set."""
    lanes = load_contracts(contracts)
    findings = lint(lanes, Path(repo_root))
    click.echo(render_findings(findings))
    if any(f.severity == BLOCKING for f in findings):
        raise SystemExit(1)


@cli.command("estimate")
@click.argument("contracts", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path),
              default=_SCRIPTS.parent, show_default=True)
def cmd_estimate(contracts: tuple[Path, ...], repo_root: Path) -> None:
    """A wave-cost estimate for CONTRACTS, from `logs/MERGE-RECEIPTS.jsonl`."""
    lanes = load_contracts(contracts)
    click.echo(estimate_wave(lanes, Path(repo_root)).render())


@cli.command("report")
@click.argument("contracts", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path),
              default=_SCRIPTS.parent, show_default=True)
def cmd_report(contracts: tuple[Path, ...], repo_root: Path) -> None:
    """Findings AND the estimate, in one run -- what a freeze-time check calls.

    Exits non-zero on a BLOCKING finding, same as `check` (Codex terra review, `[#961]` diff,
    HIGH: this command's own docstring calls it the freeze-time command, and a freeze-time
    command that always exits 0 lets an automated gate accept an invalid plan)."""
    lanes = load_contracts(contracts)
    root = Path(repo_root)
    findings = lint(lanes, root)
    click.echo(render_findings(findings))
    click.echo("")
    click.echo(estimate_wave(lanes, root).render())
    if any(f.severity == BLOCKING for f in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
