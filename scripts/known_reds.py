#!/usr/bin/env python
"""known_reds.py -- the known-reds organ (ADR-121 step 1, LANE-5A-1).

WHY THIS EXISTS. `logs/SUITE-BASELINE-FREEZE.md` compares a run to a frozen roster of node ids,
but the roster carries no identity beyond a measurement SHA, and a red that lands ABOVE the
freeze is invisible until the next re-measure -- which is exactly how CI's regression count rose
from 9 to 17 while every batch's own local registry (`scripts/test_pairing.py`) reported clean:
each batch only knows the reds present when IT started, so a regression from an EARLIER batch
reads as "pre-existing" forever. `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` C5d/C7/C8
names this "laundering."

WHAT THIS MODULE ADDS, on top of `logs/SUITE-BASELINE-FREEZE.md`'s node-id-membership idea:
  1. **A baseline id** (`<date>-<content hash>`) stamped on every verdict this module renders,
     so a disagreement between two verdicts is visible as "different baseline" rather than silent
     (ADR-121 D5).
  2. **Attribution.** Every member of the registry carries either a real attribution
     (`{"first_bad_sha", "lane"}`, found by `attribute`'s `git bisect run`), `"pre-freeze"`
     (inherited from the 2026-09-17 measurement, before this organ existed), `"witness"` (the
     four `[#664]` commit-tier tests, deliberately kept OUT of every frozen/known set so a run
     showing them is never silently absorbed), or `"unattributed"` with a reason. No member is
     anonymous (done-contract item 2).
  3. **`refresh` refuses to launder.** A currently-failing node id that was not already a
     registry member and has no attribution in the supplied `--attribution` file is a REFUSAL,
     not a silent addition (done-contract item 5) -- the opposite of what a raw re-measure of
     the old freeze file would do.
  4. **OS-keyed membership and failure signatures** (WAVE5B-N4 L2, proposal D2, `[#965]` "made
     substrate-keyed"). `Registry.members_by_os` is an ADDITIVE overlay -- `{os_key:
     {node_id: entry}}` -- consulted only when `compare`/`refresh` are given an `os_key`
     (`compare` auto-detects one from `RUNNER_OS`/`sys.platform` so CI needs no
     `.github/workflows/conductor.yml` edit, owned by another lane this batch; `refresh`
     defaults to `None`, i.e. the shared/legacy set, so the merge-moment caller in
     `ecosystem/harness.yaml`, which never passes `--os`, is untouched). Every member may also
     carry a `signature` (the exception type + first failing assertion line, read from
     pytest's own `FAILED <id> - <reason>` short-summary line and then run through
     `normalize_signature` -- repair 1, REFUSED-lane-known-reds-signatures.md, 2026-09-27 --
     which masks run-volatile tokens: a fresh commit sha, a random generated-name suffix, an
     absolute runner path, a list literal that grows on its own): once a member has a
     recorded signature, `compare` treats a DIFFERENT current (also normalized) signature on
     the same node id as a regression, not a pass-through -- the "a registered test that fails
     worse still passes" defect (C1 above) closed at the signature level, not just the node-id
     level, without a run-to-run noise change alone counting as "worse". An **unattributed**
     known member is likewise a `compare`-time regression, never a silent pass: `[#965]`'s "one
     registry" becomes one registry that can still refuse to vouch for a member it cannot
     explain.

  5. **Every entry is owned, dated and tied to a row** (schema `/2`, foundation-1-honest-green,
     R52 Q2: "every current known-red gets its own row with a task id. The known-reds registry
     refuses an entry without one"). Each entry of `members`, `members_by_os` and `hooks` carries
     a `task` (`[#N]`, an open row), an `owner` and an `expiry` (ISO date); `load_registry`
     refuses a registry with an entry that lacks one of the three, or whose expiry has passed
     -- without them "known red" means "forgotten red".
  6. **A growing known failure is registered under a ceiling** (AM2-3, DCT section 1: "re-signing
     would launder them"). An entry may carry `ceiling: {pattern, max}` -- `pattern` has one
     `(?P<n>...)` group reading the measured number out of the failure text -- and `growth:
     {from, to, commits}` stating how it got there. `compare` treats a value above `max` as a
     regression, a failure that no longer reads as the registered one as a changed signature,
     and a value below `max` as slack the next `refresh` takes back (a ceiling only comes down).

Prior art (library-first): stdlib `re`, `json`, `datetime` -- the registry stays one JSON file
read by one CLI, so no dependency is added.

THE REGISTRY IS COMMITTED, THE BATCH REGISTRY IS NOT. `scripts/test_pairing.py`'s
`TEST-PAIRING-REGISTRY-<BATCH>.json` is gitignored and per-batch by design (recording it twice
would launder a lane's red into "pre-existing" for every OTHER lane of that batch -- see that
module's own docstring). This module's registry answers a different question -- "what does CI,
which has no batch context, already know about" -- so it lives at a path convention alongside
the other committed suite artifact it supersedes: `logs/KNOWN-REDS-REGISTRY.json`, sibling to
`logs/SUITE-BASELINE-FREEZE.md`. The two coexist until one CI run has judged a push against the
registry and come back green or with its new reds named (done-contract item 4); only then does
the frozen prose file retire.

THE BISECT WRAPPER (`attribute`) is a CLONE, never the caller's own worktree -- same
`ISOLATION_REASON` as `scripts/test_pairing.py`: `git bisect` repeatedly checks out different
commits, and doing that in a worktree several other tools read (`git worktree list`, open
editors, a live session's cwd) would make the checkout itself part of what is being measured.
Each bisect step runs the ONE named test, nothing else, and reports one of three outcomes to
`git bisect run`: 0 (good -- passed), 1 (bad -- collected and failed), 125 (skip -- the test
does not exist or does not collect at this commit, e.g. because the file was added later). `git
bisect run`'s own skip-tolerant binary search converges on the first commit where the test both
EXISTS and FAILS, which is what "first bad sha" means here even when the test file itself is
younger than the comparison range's start.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conductor  # noqa: E402 -- parse_failed_node_ids is the shared, tested extractor

#: `/2` adds the three R52-Q2 fields to every entry (and the optional `ceiling` / `growth` pair).
#: A `/1` file cannot carry them, so it is refused with a pointer here, never half-read.
SCHEMA = "known-reds-registry/2"
LEGACY_SCHEMA = "known-reds-registry/1"
REGISTRY_PATH = "logs/KNOWN-REDS-REGISTRY.json"
EXIT_UNCOMPARABLE = 2

#: The fields every entry carries (R52 Q2): the row that owns the red, who answers for it, and
#: the date after which the registry refuses to vouch for it.
OWNED_FIELDS = ("task", "owner", "expiry")
_TASK_RE = re.compile(r"^\[#\d+\]$")

#: A red that comes and goes on the same sha (DCT D11) -- the cause is timing, not a commit, so
#: there is no `first_bad_sha` to bisect to. Like `ENVIRONMENT_MISMATCH`, an attribution class.
FLAKY = "flaky"

WITNESS = "witness"
PRE_FREEZE = "pre-freeze"
UNATTRIBUTED = "unattributed"
#: A hook-red's attribution class, lane-ci-signal ([#802] evidence run 36099478580): the check
#: is genuinely FAIL on a stock ephemeral CI checkout (no armed git hooks, no registered repos,
#: PowerShell-alias resolution failing against commands that exist only in an operator's own
#: profile) and genuinely clean on the machine it was designed to police. Distinct from
#: `UNATTRIBUTED` -- the cause IS known, it is just not a tree defect this registry's usual
#: "first bad commit" shape can name, because no commit made it red; the environment did.
ENVIRONMENT_MISMATCH = "environment-mismatch"

#: The four [#664] commit-tier witnesses: `logs/SUITE-BASELINE-FREEZE.md` keeps them OUT of its
#: frozen set on purpose so every run keeps reporting them; this registry keeps them OUT of
#: `red`'s "known and quiet" bucket for the same reason, but tracks them by name (never
#: anonymous) with attribution "witness" rather than leaving them to read as ordinary regressions.
WITNESS_MEMBERS = (
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_live_spine_is_ordered_rebuild_first_and_always_runs",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-orphan-census]",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-process-list]",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-task-coverage]",
)


class KnownRedsError(RuntimeError):
    """The organ could not produce a verdict (as opposed to producing a red verdict)."""


# --- ownership (R52 Q2) and ceilings (AM2-3) -------------------------------------------------

def _ceiling_value(ceiling: dict, text: str) -> int | None:
    """The number the ceiling's `(?P<n>...)` group reads out of a failure text, or `None` when
    the text no longer reads as the registered failure (a changed failure, not a bigger one)."""
    m = re.search(ceiling["pattern"], text)
    if not m:
        return None
    try:
        return int(m.group("n").replace(",", ""))
    except ValueError:
        return None


def _mask_ceiling(ceiling: dict, text: str) -> str:
    """`text` with the ceiling's measured number masked, so two readings of the same failure at
    different values compare equal everywhere except the number the ceiling already judges."""
    m = re.search(ceiling["pattern"], text)
    if not m:
        return text
    start, end = m.span("n")
    return text[:start] + "<N>" + text[end:]


def _judge_ceiling(entry: dict, current_signature: str | None) -> str:
    """One ceiling entry against this run: `ok` | `slack` | `exceeded` | `changed`.

    `changed` covers both "reads differently" and "cannot be read" -- a ceiling that cannot be
    checked fails closed (R59), it never passes by default."""
    ceiling = entry["ceiling"]
    if not current_signature:
        return "changed"
    value = _ceiling_value(ceiling, current_signature)
    if value is None:
        return "changed"
    if value > ceiling["max"]:
        return "exceeded"
    registered = entry.get("signature")
    if registered and (normalize_signature(_mask_ceiling(ceiling, registered))
                       != normalize_signature(_mask_ceiling(ceiling, current_signature))):
        return "changed"
    return "slack" if value < ceiling["max"] else "ok"


def _ceiling_problems(label: str, entry: dict) -> list[str]:
    ceiling = entry.get("ceiling")
    if ceiling is None:
        return []
    if not isinstance(ceiling, dict):
        return [f"{label}: ceiling is not an object"]
    problems: list[str] = []
    try:
        compiled = re.compile(ceiling.get("pattern"))
    except (re.error, TypeError):
        problems.append(f"{label}: ceiling pattern does not compile")
    else:
        if "n" not in compiled.groupindex:
            problems.append(f"{label}: ceiling pattern has no (?P<n>...) group")
    ceiling_max = ceiling.get("max")
    if not isinstance(ceiling_max, int) or isinstance(ceiling_max, bool) or ceiling_max < 0:
        problems.append(f"{label}: ceiling max {ceiling_max!r} is not a non-negative integer")
    growth = entry.get("growth")
    if not isinstance(growth, dict) or any(growth.get(k) in (None, "") for k in
                                           ("from", "to", "commits")):
        problems.append(f"{label}: a ceiling states its growth -- growth.from, growth.to and "
                        "growth.commits (AM2-3: re-recording a larger value with no stated "
                        "growth is laundering)")
    else:
        try:
            growth_to = int(str(growth["to"]).replace(",", ""))
        except ValueError:
            problems.append(f"{label}: growth.to {growth['to']!r} is not an integer")
        else:
            if isinstance(ceiling_max, int) and not isinstance(ceiling_max, bool) \
                    and ceiling_max > growth_to:
                problems.append(f"{label}: ceiling max {ceiling_max:,} is above the growth it "
                                f"states (growth.to {growth_to:,}) -- a ceiling only comes down")
    return problems


def _entry_problems(label: str, entry, today: datetime.date) -> list[str]:
    """Everything wrong with one registry entry; empty when it is owned, dated and in date."""
    if not isinstance(entry, dict):
        return [f"{label}: not an object"]
    problems: list[str] = []
    for name in OWNED_FIELDS:
        value = entry.get(name)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"{label}: no {name}")
    task = entry.get("task")
    if isinstance(task, str) and task.strip() and not _TASK_RE.match(task):
        problems.append(f"{label}: task {task!r} is not a row id like [#912]")
    expiry = entry.get("expiry")
    if isinstance(expiry, str) and expiry.strip():
        try:
            due = datetime.date.fromisoformat(expiry)
        except ValueError:
            problems.append(f"{label}: expiry {expiry!r} is not an ISO date (YYYY-MM-DD)")
        else:
            if due < today:
                problems.append(f"{label}: EXPIRED {expiry} (task {task}) -- fix it, or "
                                "re-date it by a recorded ruling; the registry does not "
                                "vouch for it past its date")
    return problems + _ceiling_problems(label, entry)


def registry_problems(registry: Registry, today: datetime.date | None = None) -> list[str]:
    """Every entry of every bucket that is not owned, dated and in date (R52 Q2)."""
    today = today or datetime.date.today()
    problems: list[str] = []
    for node_id in sorted(registry.members):
        problems += _entry_problems(f"members[{node_id}]", registry.members[node_id], today)
    for os_key in sorted(registry.members_by_os):
        for node_id in sorted(registry.members_by_os[os_key]):
            problems += _entry_problems(f"members_by_os[{os_key}][{node_id}]",
                                        registry.members_by_os[os_key][node_id], today)
    for hook_id in sorted(registry.hooks):
        problems += _entry_problems(f"hooks[{hook_id}]", registry.hooks[hook_id], today)
    return problems


# --- baseline identity --------------------------------------------------------------------

def compute_baseline_id(members: dict, *, date: str, members_by_os: dict | None = None) -> str:
    """`<date>-<12 hex chars>`; the hash is over the sorted (id, attribution) pairs, so two
    registries with the same members and the same attributions always share a baseline id
    regardless of dict insertion order, and any change to who-is-known or why changes it.

    `members_by_os`, when non-empty, folds the OS-keyed overlay into the same hash (sorted by
    OS key, then by node id within each) so a change confined to one OS's bucket still changes
    the baseline id. Omitted or empty, the hash is byte-identical to the pre-D2 computation --
    every registry that never used `members_by_os` keeps its existing baseline id verbatim."""
    canonical_members = {k: members[k] for k in sorted(members)}
    if members_by_os:
        canonical = json.dumps(
            {"members": canonical_members,
             "members_by_os": {osk: {k: members_by_os[osk][k] for k in sorted(members_by_os[osk])}
                               for osk in sorted(members_by_os)}},
            sort_keys=True)
    else:
        canonical = json.dumps(canonical_members, sort_keys=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    return f"{date}-{digest}"


# --- registry ------------------------------------------------------------------------------

@dataclass(frozen=True)
class Registry:
    schema: str
    baseline_id: str
    measured_at_sha: str
    measured_via: str
    workers: int
    members: dict  # {node_id: {"attribution": ...} | {"attribution": ..., "reason": ...}}
    notes: tuple = field(default_factory=tuple)
    #: {hook_id: {"attribution": ..., "reason": ..., "checks": [...]?}} -- the non-pytest
    #: sibling of `members`, for a manual-stage pre-commit hook (`derived-copies-rebind`,
    #: `audit-health`, ...) that carries no pytest node id at all. ADDITIVE (lane-ci-signal,
    #: [#802] evidence run 36099478580): defaults to `{}` so every registry written before this
    #: field existed still loads, and `compare`'s existing pytest-only reading is untouched --
    #: only `compare_hook` reads this field. The optional `checks` list (LANE-5B3-8, Codex terra
    #: HIGH 2026-09-26) scopes the registration to the specific `audit.py health` check names it
    #: was measured against, when `compare_hook` is given the hook's raw output -- an entry with
    #: no `checks` list keeps the prior whole-hook-known behavior.
    hooks: dict = field(default_factory=dict)
    #: {os_key: {node_id: entry}} -- the D2 OS-keyed overlay (WAVE5B-N4 L2). ADDITIVE, same
    #: shape/reasoning as `hooks` above: defaults to `{}` so every registry written before this
    #: field existed still loads; `compare`/`refresh` only consult it when given an `os_key`.
    #: See the module docstring's "OS-keyed membership" paragraph.
    members_by_os: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        return {"schema": self.schema, "baseline_id": self.baseline_id,
                "measured_at_sha": self.measured_at_sha, "measured_via": self.measured_via,
                "workers": self.workers,
                "members": {k: self.members[k] for k in sorted(self.members)},
                "hooks": {k: self.hooks[k] for k in sorted(self.hooks)},
                "members_by_os": {osk: {k: self.members_by_os[osk][k]
                                        for k in sorted(self.members_by_os[osk])}
                                  for osk in sorted(self.members_by_os)},
                "notes": list(self.notes)}

    @classmethod
    def from_json(cls, data: dict, source: str) -> Registry:
        if data.get("schema") == LEGACY_SCHEMA:
            raise KnownRedsError(
                f"{source}: schema {LEGACY_SCHEMA!r} predates R52 Q2 -- its entries carry no "
                f"task, owner or expiry, so none of them can be vouched for. Migrate it to "
                f"{SCHEMA!r}: every entry names its open row, an owner and an expiry")
        if data.get("schema") != SCHEMA:
            raise KnownRedsError(f"{source}: schema {data.get('schema')!r}, expected {SCHEMA!r}")
        try:
            return cls(schema=data["schema"], baseline_id=data["baseline_id"],
                       measured_at_sha=data["measured_at_sha"], measured_via=data["measured_via"],
                       workers=int(data["workers"]), members=dict(data["members"]),
                       hooks=dict(data.get("hooks", {})),
                       members_by_os={osk: dict(v) for osk, v in
                                      data.get("members_by_os", {}).items()},
                       notes=tuple(data.get("notes", ())))
        except (KeyError, TypeError) as exc:
            raise KnownRedsError(f"{source}: malformed registry field: {exc}") from exc


def _refusal(source: str, problems: list[str]) -> KnownRedsError:
    shown = problems[:40]
    more = f"\n  ... and {len(problems) - len(shown)} more" if len(problems) > len(shown) else ""
    return KnownRedsError(
        f"{source}: {len(problems)} problem(s) -- R52 Q2: every entry carries a task, an owner "
        "and an expiry, and none is past its date:\n  " + "\n  ".join(shown) + more)


def load_registry(path: Path, *, today: datetime.date | None = None) -> Registry:
    """The committed registry, or `KnownRedsError`. Refuses (R52 Q2) a registry holding an
    entry with no task, owner or expiry, an expired entry, or a malformed ceiling -- a
    registry that cannot vouch for each entry is not one to judge a run against."""
    if not path.is_file():
        raise KnownRedsError(f"no registry at {path}: an absent registry must not read as "
                             "'nothing is known' -- run `refresh` first")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise KnownRedsError(f"{path}: not valid JSON: {exc}") from exc
    registry = Registry.from_json(data, str(path))
    problems = registry_problems(registry, today)
    if problems:
        raise _refusal(str(path), problems)
    return registry


def write_registry(path: Path, registry: Registry) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry.to_json(), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


# --- refresh: build/update the registry from a run + attribution evidence ------------------

def refresh(*, failed: frozenset, workers: int, commit: str, measured_via: str, date: str,
            attribution: dict, previous: Registry | None, os_key: str | None = None,
            signatures: dict | None = None,
            today: datetime.date | None = None) -> tuple[Registry, list[str]]:
    """Build the next registry. `attribution` supplies evidence for ids not already carried
    from `previous` (each value is `{"attribution": ...}` or `{"attribution": ..., "reason":
    ...}`). Returns (registry, dropped) where `dropped` lists previous members no longer
    failing (informational -- they are simply not carried forward, never re-added).

    Raises KnownRedsError naming every currently-failing id that is neither carried from
    `previous` nor present in `attribution`: a refresh that could not attribute a NEW red must
    refuse rather than silently file it as known (done-contract item 5).

    `os_key` (D2, WAVE5B-N4 L2): `None` (the default) writes the shared/legacy `members` set,
    byte-for-byte the pre-D2 behaviour -- the `ecosystem/harness.yaml` merge-moment caller never
    passes this flag and is untouched. A given `os_key` instead writes `members_by_os[os_key]`,
    seeded from THAT bucket's own prior members first, falling back to the shared set for a
    member not yet OS-scoped -- so a member's first OS-scoped capture stamps a FRESH `signature`
    from the current run (Codex terra HIGH, 2026-09-27: never the shared entry's own signature,
    which may have been captured on a different OS and would otherwise masquerade as this OS's
    fingerprint) while a member already OS-scoped keeps its recorded signature untouched on
    every later refresh (`compare`'s "changed signature" check depends on that signature being
    stable once set, not re-stamped every run).

    `signatures` ({node_id: text}, from `extract_failure_signatures`) fills a NEW member's
    `signature` field (carried-forward or attributed) only when that member does not already
    carry one -- never overwrites an existing recorded signature.

    R52 Q2 / AM2-3: every member written must carry a `task`, an `owner` and an in-date
    `expiry` (a NEW red supplies them in its `attribution` value), and a carried member with a
    `ceiling` is held to it -- measured ABOVE the ceiling is a refusal (growth never rides in on
    a refresh), measured below LOWERS the ceiling (it only comes down).
    """
    signatures = signatures or {}
    shared_prev = dict(previous.members) if previous else {}
    prev_os_bucket = (dict(previous.members_by_os.get(os_key, {}))
                      if (previous and os_key is not None) else {})
    prev_pool = shared_prev if os_key is None else {**shared_prev, **prev_os_bucket}
    members: dict = {}
    missing: list[str] = []
    exceeded: list[str] = []
    for node_id in failed:
        if node_id in WITNESS_MEMBERS:
            members[node_id] = {**prev_pool.get(node_id, {}), **attribution.get(node_id, {}),
                                "attribution": WITNESS,
                                "reason": "[#664] commit-tier witness -- deliberately never "
                                          "frozen; a run showing it is expected, not a surprise"}
        elif node_id in prev_pool:
            entry = dict(prev_pool[node_id])
            if os_key is not None and node_id not in prev_os_bucket:
                # First OS-scoped capture of a member seeded from the SHARED entry: any
                # signature there was captured in a different context, never this OS's -- drop
                # it and establish this OS's own fingerprint from the current run instead.
                entry.pop("signature", None)
                if node_id in signatures:
                    entry["signature"] = normalize_signature(signatures[node_id])
            elif "signature" not in entry and node_id in signatures:
                entry["signature"] = normalize_signature(signatures[node_id])
            ceiling = entry.get("ceiling")
            if isinstance(ceiling, dict) and node_id in signatures:
                measured = _ceiling_value(ceiling, signatures[node_id])
                if measured is None:
                    exceeded.append(f"{node_id}: no longer reads as the registered failure "
                                    f"(`{ceiling['pattern']}` finds no number)")
                elif measured > ceiling["max"]:
                    exceeded.append(f"{node_id}: measured {measured:,}, ceiling {ceiling['max']:,}")
                elif measured < ceiling["max"]:
                    entry["ceiling"] = {**ceiling, "max": measured}
            members[node_id] = entry
        elif node_id in attribution:
            entry = dict(attribution[node_id])
            if "signature" not in entry and node_id in signatures:
                entry["signature"] = normalize_signature(signatures[node_id])
            members[node_id] = entry
        else:
            missing.append(node_id)
    if missing:
        raise KnownRedsError(
            "refresh refused: " + str(len(missing)) + " currently-failing id(s) are neither "
            "carried from the previous registry nor attributed in --attribution -- a refresh "
            "never adds an unattributed red:\n  " + "\n  ".join(sorted(missing)))
    if exceeded:
        raise KnownRedsError(
            "refresh refused: " + str(len(exceeded)) + " known failure(s) grew past, or no "
            "longer read as, their ceiling -- growth is a regression to fix, never a value "
            "to re-record "
            "(AM2-3):\n  " + "\n  ".join(sorted(exceeded)))
    owned_today = today or datetime.date.today()
    unowned = [problem for node_id in sorted(members)
               for problem in _entry_problems(node_id, members[node_id], owned_today)]
    if unowned:
        raise KnownRedsError(
            "refresh refused: " + str(len(unowned)) + " member(s) are not owned and dated "
            "(R52 Q2 -- a new red's `attribution` value supplies task, owner and expiry):\n  "
            + "\n  ".join(unowned))

    prev_by_os = dict(previous.members_by_os) if previous else {}
    if os_key is None:
        dropped = sorted(set(shared_prev) - failed)
        new_members, new_by_os = members, prev_by_os
    else:
        dropped = sorted(set(prev_os_bucket) - failed)
        new_members = shared_prev
        new_by_os = {**prev_by_os, os_key: members}

    baseline_id = compute_baseline_id(new_members, date=date, members_by_os=new_by_os)
    registry = Registry(schema=SCHEMA, baseline_id=baseline_id, measured_at_sha=commit,
                        measured_via=measured_via, workers=workers, members=new_members,
                        notes=previous.notes if previous else (),
                        hooks=dict(previous.hooks) if previous else {},
                        members_by_os=new_by_os)
    return registry, dropped


# --- compare: CI's own comparator, replacing a node-id diff against the prose freeze -------

def compare(failed: frozenset, registry: Registry, *, workers: int,
            pytest_exit: int | None = None, os_key: str | None = None,
            signatures: dict | None = None) -> dict:
    """Judge one run against `registry`. Mirrors `conductor.suite_gate`'s shape (verdict,
    reason, regressions, pre_existing) plus `baseline_id` on every branch (done-contract item 3)
    and a `witnesses` bucket so a [#664] witness is reported by name, not folded into either
    'pre-existing' (which would hide that it is DESIGNED to fail) or 'regressions' (which would
    make every run report a fail that arming required-checks could never clear).

    D2 (WAVE5B-N4 L2), two more regression classes, neither a silent pass-through:
      - **unattributed member.** A known member registered with `attribution: "unattributed"`
        is reported (in `unattributed`) AND counted as a regression -- a registry entry that
        cannot explain itself never reads as "known-safe".
      - **changed signature.** When `signatures` supplies this run's failure text for a node id
        AND the registered entry already carries a `signature`, a mismatch is a regression (in
        `signature_changed`) even though the node id itself is a known member -- the same test
        id failing a DIFFERENT way is a new defect, not the old one (C1: "a registered test that
        fails worse still passes"). A member with no recorded signature, or a run with no
        `signatures` supplied, skips this check entirely (backward compatible: every member
        registered before D2 carries no `signature`).

    `os_key`, when given, merges `registry.members_by_os.get(os_key, {})` on top of the shared
    `registry.members` (the OS-specific entry wins on a shared key) -- omitted, behaviour is
    identical to the pre-D2 comparator.

    AM2-3 (foundation-1-honest-green): an entry carrying a `ceiling` is judged by its measured
    number, not by exact signature equality. A value above `ceiling.max` is a regression (in
    `ceiling_exceeded`); a failure that no longer reads as the registered one -- or one with no
    signature supplied to read -- is a changed signature (fail closed); a value below the
    ceiling passes and is listed in `ceiling_slack` so the next `refresh` lowers it.
    """
    base = {"baseline_id": registry.baseline_id, "os_key": os_key}
    empty = {"regressions": [], "pre_existing": [], "witnesses": [], "unattributed": [],
            "signature_changed": [], "ceiling_exceeded": [], "ceiling_slack": []}
    if pytest_exit is not None and pytest_exit not in (0, 1):
        return {**base, "verdict": "fail",
                "reason": f"NOT COMPARABLE -- pytest itself exited {pytest_exit}", **empty}
    if workers != registry.workers:
        return {**base, "verdict": "fail",
                "reason": f"NOT COMPARABLE -- resolved at {workers} workers, the registry is "
                          f"pinned at {registry.workers}", **empty}
    signatures = signatures or {}
    known = dict(registry.members)
    if os_key:
        known.update(registry.members_by_os.get(os_key, {}))

    regressions: list[str] = []
    pre_existing: list[str] = []
    witnesses: list[str] = []
    unattributed: list[str] = []
    signature_changed: list[str] = []
    ceiling_exceeded: list[str] = []
    ceiling_slack: list[str] = []
    for node_id in sorted(failed):
        entry = known.get(node_id)
        if entry is None:
            regressions.append(node_id)
            continue
        attribution_value = entry["attribution"]
        if attribution_value == WITNESS:
            witnesses.append(node_id)
            continue
        if attribution_value == UNATTRIBUTED:
            unattributed.append(node_id)
            regressions.append(node_id)
            continue
        registered_sig = entry.get("signature")
        current_sig = signatures.get(node_id)
        if isinstance(entry.get("ceiling"), dict):
            judged = _judge_ceiling(entry, current_sig)
            if judged == "exceeded":
                ceiling_exceeded.append(node_id)
                regressions.append(node_id)
            elif judged == "changed":
                signature_changed.append(node_id)
                regressions.append(node_id)
            else:
                pre_existing.append(node_id)
                if judged == "slack":
                    ceiling_slack.append(node_id)
            continue
        if (registered_sig and current_sig
                and normalize_signature(registered_sig) != normalize_signature(current_sig)):
            signature_changed.append(node_id)
            regressions.append(node_id)
            continue
        pre_existing.append(node_id)

    result_lists = {"regressions": sorted(regressions), "pre_existing": pre_existing,
                    "witnesses": witnesses, "unattributed": unattributed,
                    "signature_changed": signature_changed,
                    "ceiling_exceeded": ceiling_exceeded, "ceiling_slack": ceiling_slack}
    if regressions:
        return {**base, "verdict": "fail",
                "reason": f"REGRESSION -- {len(regressions)} failure(s) not in the registry "
                          f"(baseline {registry.baseline_id})",
                **result_lists}
    return {**base, "verdict": "pass",
            "reason": f"{len(pre_existing)} known failure(s), {len(witnesses)} witness(es), "
                      f"0 outside the registry (baseline {registry.baseline_id})",
            **result_lists}


def compare_to_base(tip_failed: frozenset, base_failed: frozenset, registry: Registry, *,
                    workers: int, os_key: str | None = None,
                    tip_signatures: dict | None = None,
                    base_signatures: dict | None = None) -> dict:
    """The TEST-LEVEL truth table for ONE OS leg: the tip's failing node ids against the base
    `main` run's failing node ids against the shrink-only registry (foundation-4-merge-gate, G4).

    WHY IT EXISTS. The merge path classified a CI run by JOB NAME, so a NEW test red inside a job
    that was already red read PRE-EXISTING (DVA A2; the `424d6c72` cut merge turned
    `test_registered_check_never_fails_on_live_repo` red for 16 runs while the pytest job was
    already red). This function is the replacement for that job-level set difference. It is PURE
    -- the failing sets and signatures are read from the CI job logs by the caller
    (`actions_verdict`), and the registry is loaded by the caller, so the table is testable
    row by row. `PRE-EXISTING` is `complete` ONLY when every failing id is accounted for:

      new                 the id fails at the tip and did not fail at the base -> REGRESSION
      signature_changed   the id fails on both sides, differently -> REGRESSION (fails worse)
      known               fails on both sides with the same signature AND the registry vouches
                          for it (membership, ceiling, unattributed) -> accounted for
      base_unregistered   fails on both sides but the registry does not list it -> FLAGGED, never
                          a silent baseline (D5(b)/DL8: a regression that reached `main` must not
                          become the baseline just because it is red on both sides)
      registry_regressions  listed, but the registry itself refuses it (unattributed, a ceiling
                          exceeded, a signature that no longer reads as the registered one)
      fixed               failed at the base, passes at the tip -> reported, never silent

    The registry judgement is `compare` itself -- one comparator, not a second copy -- fed the
    ids that are red on BOTH sides. NOT COMPARABLE (a worker count that is not the registry's
    pin) fails closed. The non-test half of "every failing thing is accounted for" (a job
    timeout, a collection error, an xdist crash, `cancelled`) is `actions_verdict`'s: those carry
    no node id to put in this table, and each is a regression there.
    """
    if workers != registry.workers:
        return {"baseline_id": registry.baseline_id, "os_key": os_key, "verdict": "fail",
                "complete": False,
                "reason": f"NOT COMPARABLE -- resolved at {workers} workers, the registry is "
                          f"pinned at {registry.workers}",
                "new": [], "signature_changed": [], "known": [], "base_unregistered": [],
                "registry_regressions": [], "fixed": []}
    tip_sigs, base_sigs = tip_signatures or {}, base_signatures or {}
    new = sorted(tip_failed - base_failed)
    fixed = sorted(base_failed - tip_failed)
    both = tip_failed & base_failed
    listed = dict(registry.members)
    if os_key:
        listed.update(registry.members_by_os.get(os_key, {}))

    def _no_basis(node_id: str) -> bool:
        """The tip says WHY it failed, and neither the base log nor the registry carries a
        signature to say it is the same why: nothing vouches for 'the same failure'."""
        entry = listed.get(node_id)
        registered = entry.get("signature") if isinstance(entry, dict) else None
        return bool(tip_sigs.get(node_id)) and not base_sigs.get(node_id) and not registered

    signature_changed = sorted(
        node_id for node_id in both
        if (tip_sigs.get(node_id) and base_sigs.get(node_id)
            and normalize_signature(tip_sigs[node_id]) != normalize_signature(base_sigs[node_id]))
        or _no_basis(node_id))
    judged = both - set(signature_changed)
    registry_view = compare(frozenset(judged), registry, workers=workers, os_key=os_key,
                            signatures=tip_sigs)
    base_unregistered = sorted(n for n in registry_view["regressions"] if n not in listed)
    registry_regressions = sorted(n for n in registry_view["regressions"] if n in listed)
    known = sorted(set(registry_view["pre_existing"]) | set(registry_view["witnesses"]))
    bad = bool(new or signature_changed or base_unregistered or registry_regressions)
    if bad:
        parts = [f"{len(new)} new", f"{len(signature_changed)} changed signature",
                 f"{len(base_unregistered)} base failure(s) absent from the registry",
                 f"{len(registry_regressions)} refused by the registry"]
        reason = f"REGRESSION -- {', '.join(parts)} (baseline {registry.baseline_id})"
    else:
        reason = (f"{len(known)} known failure(s), all accounted for, {len(fixed)} fixed "
                  f"(baseline {registry.baseline_id})")
    return {"baseline_id": registry.baseline_id, "os_key": os_key,
            "verdict": "fail" if bad else "pass", "complete": not bad, "reason": reason,
            "new": new, "signature_changed": signature_changed, "known": known,
            "base_unregistered": base_unregistered, "registry_regressions": registry_regressions,
            "fixed": fixed}


def render_compare_to_base(result: dict) -> str:
    """Flat key/value + bullet lines (CLAUDE.md section 4): no pipe tables."""
    lines = ["known-reds compare-to-base", "", f"baseline id    : {result['baseline_id']}"]
    if result.get("os_key"):
        lines.append(f"os key         : {result['os_key']}")
    lines.append(f"known          : {len(result['known'])}")
    for node_id in result["known"]:
        lines.append(f"  known         {node_id}")
    for key, tag in (("new", "NEW"), ("signature_changed", "SIG-CHANGED"),
                     ("base_unregistered", "BASE-UNREGISTERED"),
                     ("registry_regressions", "REGISTRY-REFUSED")):
        lines.append(f"{key.replace('_', ' '):<15}: {len(result[key])}")
        for node_id in result[key]:
            lines.append(f"  {tag:<14}{node_id}")
    lines.append(f"fixed          : {len(result['fixed'])}")
    for node_id in result["fixed"]:
        lines.append(f"  fixed         {node_id}")
    lines.append("")
    lines.append(f"verdict        : {result['verdict'].upper()} -- {result['reason']}")
    return "\n".join(lines)


#: D2 (WAVE5B-N4 L2): the failure signature -- exception type + first failing assertion line --
#: read verbatim from pytest's own short-summary `FAILED <id> - <reason>` / `ERROR <id> -
#: <reason>` line (`-q --tb=short`'s stable, dependency-free reason text; no junit/json plugin,
#: ADR-106 library-first). A bare `FAILED <id>` line with no ` - <reason>` suffix yields no
#: entry -- `compare` never treats an absent signature as "changed".
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
_FAILED_LINE_WITH_REASON_RE = re.compile(r"^(?:FAILED|ERROR)\s+(.+?)(?:\s+-\s+(.*))?$")


def extract_failure_signatures(pytest_output: str) -> dict:
    """{node_id: signature text}, from pytest's own short-summary lines (see above)."""
    signatures: dict = {}
    for raw in pytest_output.splitlines():
        line = _ANSI_RE.sub("", raw).strip()
        m = _FAILED_LINE_WITH_REASON_RE.match(line)
        if m and m.group(2) and conductor._FAILED_ID_RE.match(m.group(1).strip()):
            signatures[m.group(1).strip()] = m.group(2).strip()
    return signatures


#: Repair 1 (REFUSED-lane-known-reds-signatures.md, 2026-09-27): the raw short-summary reason
#: text above is verbatim, so it also carries whatever is run-volatile about the failure --
#: a freshly captured commit sha, a random generated-name suffix (`lane-zz-occupancy-witness-
#: <n>`), an absolute runner path (`D:\a\<repo>\<repo>`, `/home/runner/work/...`), or a list
#: literal that grows independently of the failure itself (a "carries no disposition" census).
#: Comparing that text verbatim turns an UNCHANGED failure into a "changed signature"
#: regression on every single run -- `compare`'s own point is to catch a test that fails
#: WORSE, not one that fails identically with different noise. Each pattern below names one
#: narrow, run-volatile token class; everything else -- the exception type, the stable wording
#: of the assertion, ordinary numbers that are not part of a generated name -- is left alone,
#: so a genuinely different assertion still normalizes to a different string.
#:
#: `_LIST_BODY_RE` is deliberately scoped to a list that trails an explanatory ": " (a
#: human-composed diagnostic message, e.g. `f"...verdict from: {census!r}"`), never a bare
#: pytest comparison repr like `assert ['old'] == ['expected']` -- Codex terra HIGH,
#: 2026-09-27: an unscoped `\[[^\[\]]*\]` would mask that second shape too, silently hiding a
#: genuinely different list-equality assertion behind the SAME "[<LIST>]" placeholder.
_WIN_ABS_PATH_RE = re.compile(r"[A-Za-z]:\\[^\s,'\")]+")
_POSIX_ABS_PATH_RE = re.compile(r"(?<![\w.])/(?:[\w.\-]+/)+[\w.\-]*")
_LIST_BODY_RE = re.compile(r"(?<=: )\[[^\[\]]*\]")
_HEX_SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
_GENERATED_NAME_SUFFIX_RE = re.compile(r"(?<=[A-Za-z])-\d+\b")


def normalize_signature(text: str) -> str:
    """Mask run-volatile tokens in a captured failure signature. Called on both sides before
    a signature is STORED (`refresh`) and before two signatures are COMPARED (`compare`), so
    two reasons differing only by a sha / a random generated-name suffix / an absolute path /
    a growing list body compare EQUAL, while a genuinely different assertion still compares
    CHANGED."""
    text = _WIN_ABS_PATH_RE.sub("<PATH>", text)
    text = _POSIX_ABS_PATH_RE.sub("<PATH>", text)
    text = _LIST_BODY_RE.sub("[<LIST>]", text)
    text = _HEX_SHA_RE.sub("<SHA>", text)
    text = _GENERATED_NAME_SUFFIX_RE.sub("-<N>", text)
    return text


def default_os_key() -> str:
    """The registry's OS key for the CURRENT process, auto-detected so `compare`'s new
    OS-awareness needs no edit to `.github/workflows/conductor.yml` (owned by another lane this
    batch, ruling (k)): GitHub Actions sets `RUNNER_OS`; anywhere else (a lane's own local push,
    a manual invocation) falls back to `sys.platform`. Matches the matrix's own context-naming
    convention (`pytest (ubuntu-latest)` / `pytest (windows-latest)`,
    `.github/workflows/conductor.yml:100`) so a captured `members_by_os` key always agrees with
    what a CI run on that OS will look up."""
    runner_os = os.environ.get("RUNNER_OS", "").strip().lower()
    if runner_os == "windows":
        return "windows-latest"
    if runner_os == "linux":
        return "ubuntu-latest"
    if runner_os == "macos":
        return "macos-latest"
    return "windows-latest" if sys.platform.startswith("win") else "ubuntu-latest"


#: Codex terra HIGH (2026-09-26, LANE-5B3-8): `[!!] <name>` from `audit.py health`'s self-audit
#: section (`click.echo(f"  {marker} {f.check_name}: {f.evidence}")`) and its operational
#: preflight section (`click.echo(f"  {marker} {label}{suffix}")`, suffix always non-empty on a
#: failing operational check). Two patterns because the two sections format differently; neither
#: check name contains the other section's separator, so they never cross-match.
_FAIL_SELF_AUDIT_RE = re.compile(r"^\s*\[!!\]\s+([^:\n]+):", re.MULTILINE)
_FAIL_OPERATIONAL_RE = re.compile(r"^\s*\[!!\]\s+([^:\n(]+?)\s{2}\(", re.MULTILINE)


def extract_failing_check_names(hook_output: str) -> set:
    """The specific `audit.py health` check names reported `[!!]` in raw hook stdout/stderr --
    NOT the hook's bare exit code. Used to scope a hook registration to the findings it was
    actually measured against (Codex terra HIGH, 2026-09-26): a hook registered whole-sale by
    `hook_id` alone would silently launder a NEW, different failing check under the same
    registration, exactly the "membership by count, not by identity" trap [#802]'s own pytest
    side already refuses ("A file with 3 frozen members that fails 4 has a regression, and the
    count alone hides it")."""
    names = {m.strip() for m in _FAIL_SELF_AUDIT_RE.findall(hook_output)}
    names |= {m.strip() for m in _FAIL_OPERATIONAL_RE.findall(hook_output)}
    return names


def compare_hook(hook_id: str, exit_code: int, registry: Registry,
                 hook_output: str | None = None) -> dict:
    """Judge one pre-commit hook's exit code against `registry.hooks` -- `compare`'s sibling for
    a check that carries no pytest node id (a manual-stage hook run by `pre-commit run
    --hook-stage manual`, as `conductor.yml`'s `commit-gate` job does). Same shape as `compare`:
    'pass' on a clean exit OR a REGISTERED known-red; 'fail' (REGRESSION) on an unregistered
    non-zero exit. A registration is keyed by `hook_id` alone -- it never covers a different
    hook, the same specificity `compare`'s per-node-id keying already has.

    `hook_output`, when given, and the entry carries a `checks:` allowlist (the specific
    `audit.py health` check names this registration was measured against): the ACTUAL failing
    check names extracted from `hook_output` must be a subset of that allowlist, or the names
    outside it are reported as a genuine regression even though `hook_id` itself is registered
    (Codex terra HIGH, 2026-09-26 -- see `extract_failing_check_names`). Omitting `hook_output`,
    or a registration with no `checks:` list, keeps the prior whole-hook behavior exactly
    (backward-compatible: no existing caller or committed registry entry is broken by this).
    """
    base = {"baseline_id": registry.baseline_id, "hook_id": hook_id}
    if exit_code == 0:
        return {**base, "verdict": "pass", "reason": f"{hook_id}: clean (exit 0)",
                "regressions": [], "registered": None}
    entry = registry.hooks.get(hook_id)
    if entry is None:
        return {**base, "verdict": "fail",
                "reason": f"REGRESSION -- {hook_id} exited {exit_code} and is not in the "
                          f"registry's hooks (baseline {registry.baseline_id})",
                "regressions": [hook_id], "registered": None}
    allowed = entry.get("checks")
    if hook_output is not None and allowed:
        failing = extract_failing_check_names(hook_output)
        unknown = sorted(failing - set(allowed))
        if unknown:
            return {**base, "verdict": "fail",
                    "reason": f"REGRESSION -- {hook_id} exited {exit_code} with check(s) "
                              f"{', '.join(unknown)} outside the registered set {sorted(allowed)} "
                              f"(baseline {registry.baseline_id})",
                    "regressions": unknown, "registered": entry}
    return {**base, "verdict": "pass",
            "reason": f"{hook_id}: known (registered {entry.get('attribution', UNATTRIBUTED)}) "
                      f"-- exit {exit_code} (baseline {registry.baseline_id})",
            "regressions": [], "registered": entry}


def render_compare_hook(result: dict) -> str:
    """Flat key/value + bullet lines (CLAUDE.md section 4): no pipe tables."""
    lines = ["known-reds compare-hook", "", f"baseline id    : {result['baseline_id']}",
             f"hook id        : {result['hook_id']}"]
    if result["registered"]:
        lines.append(f"registered as  : {result['registered'].get('attribution', UNATTRIBUTED)}")
    lines.append(f"regressions    : {len(result['regressions'])}")
    for hid in result["regressions"]:
        lines.append(f"  REGRESSION    {hid}")
    lines.append("")
    lines.append(f"verdict        : {result['verdict'].upper()} -- {result['reason']}")
    return "\n".join(lines)


def render_compare(result: dict) -> str:
    """Flat key/value + bullet lines (CLAUDE.md section 4): no pipe tables."""
    lines = ["known-reds compare", "", f"baseline id    : {result['baseline_id']}"]
    if result.get("os_key"):
        lines.append(f"os key         : {result['os_key']}")
    lines.append(f"pre-existing   : {len(result['pre_existing'])}")
    for nid in result["pre_existing"]:
        lines.append(f"  known         {nid}")
    lines.append(f"witnesses      : {len(result['witnesses'])}")
    for nid in result["witnesses"]:
        lines.append(f"  witness       {nid}")
    lines.append(f"regressions    : {len(result['regressions'])}")
    for nid in result["regressions"]:
        lines.append(f"  REGRESSION    {nid}")
    if result.get("unattributed"):
        lines.append(f"unattributed known members still failing: {len(result['unattributed'])}")
        for nid in result["unattributed"]:
            lines.append(f"  UNATTRIBUTED  {nid}")
    if result.get("signature_changed"):
        lines.append(f"changed signature (known id, different failure): "
                     f"{len(result['signature_changed'])}")
        for nid in result["signature_changed"]:
            lines.append(f"  SIG-CHANGED   {nid}")
    if result.get("ceiling_exceeded"):
        lines.append(f"grew past its ceiling (AM2-3 -- a growing red is a regression): "
                     f"{len(result['ceiling_exceeded'])}")
        for nid in result["ceiling_exceeded"]:
            lines.append(f"  OVER-CEILING  {nid}")
    if result.get("ceiling_slack"):
        lines.append(f"below its ceiling (run `refresh` to lower it): "
                     f"{len(result['ceiling_slack'])}")
        for nid in result["ceiling_slack"]:
            lines.append(f"  SLACK         {nid}")
    lines.append("")
    lines.append(f"verdict        : {result['verdict'].upper()} -- {result['reason']}")
    return "\n".join(lines)


# --- attribute: the git-bisect-run wrapper --------------------------------------------------

#: See the module docstring's "THE BISECT WRAPPER" paragraph for why this is a clone.
ISOLATION_REASON = (
    "a clone, not a worktree: git bisect repeatedly checks out different commits, and several "
    "tests read `git worktree list`, so bisecting in a worktree would make the checkout itself "
    "part of what is being measured"
)

_FIRST_BAD_RE = re.compile(r"^([0-9a-f]{40}) is the first 'bad' commit", re.MULTILINE)


def _git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if done.returncode != 0:
        raise KnownRedsError(f"git {' '.join(args)} failed: "
                             f"{done.stderr.strip() or done.stdout.strip()}")
    return done.stdout.strip()


def find_lane(repo: Path, first_bad_sha: str, bad_ref: str) -> str | None:
    """The `worktree-<lane>` name of the first LANE-MERGE (`Merge branch '...'`) on the
    ancestry path from `first_bad_sha` to `bad_ref` -- the merge that actually carried it
    into main -- or `None` if no such merge is found. Intervening `Merge remote-tracking
    branch 'origin/main' into worktree-...` sync merges (or any other merge subject that
    doesn't match the lane-merge pattern) are walked PAST, not stopped at, since they never
    carry a lane's work into main themselves."""
    if first_bad_sha == _git(repo, "rev-parse", first_bad_sha):
        subject = _git(repo, "log", "-1", "--format=%s", first_bad_sha)
        m = re.match(r"^Merge branch '(?:worktree-)?([^']+)'", subject)
        if m:
            return m.group(1)
    out = _git(repo, "log", "--merges", "--ancestry-path", "--reverse", "--format=%s",
              f"{first_bad_sha}..{bad_ref}")
    for line in out.splitlines():
        m = re.match(r"^Merge branch '(?:worktree-)?([^']+)'", line)
        if m:
            return m.group(1)
    return None


def attribute(repo: Path, test_id: str, *, good: str, bad: str, venv_python: Path,
             workdir: Path | None = None, timeout: float = 180.0) -> dict:
    """`git bisect run` the ONE test between `good` (assumed to pass, or to not yet collect)
    and `bad` (assumed to fail). Returns
    `{"test": test_id, "first_bad_sha": sha, "lane": name_or_None, "bisect_log": text}`.

    Raises KnownRedsError if bisect could not converge (too many skips, or `good` itself fails).
    """
    scratch_root = Path(tempfile.mkdtemp(prefix="known-reds-", dir=workdir))
    clone = scratch_root / "clone"
    try:
        _git(scratch_root, "clone", "--quiet", "--shared", "--no-checkout", str(repo), str(clone))
        _git(clone, "bisect", "start", bad, good)
        step_script = Path(__file__).resolve()
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["_KNOWN_REDS_BISECT_TEST_ID"] = test_id
        env["_KNOWN_REDS_BISECT_VENV_PY"] = str(venv_python)
        env["_KNOWN_REDS_BISECT_CLONE"] = str(clone)
        env["_KNOWN_REDS_BISECT_TIMEOUT"] = str(timeout)
        done = subprocess.run(
            ["git", "bisect", "run", str(venv_python), str(step_script), "_bisect-step"],
            cwd=clone, capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env, check=False)
        log = done.stdout + done.stderr
        m = _FIRST_BAD_RE.search(log)
        if not m:
            raise KnownRedsError(f"bisect for {test_id!r} did not converge on a first-bad "
                                 f"commit:\n{log[-2000:]}")
        first_bad_sha = m.group(1)
        lane = find_lane(clone, first_bad_sha, bad)
        return {"test": test_id, "first_bad_sha": first_bad_sha, "lane": lane, "bisect_log": log}
    finally:
        # No `git bisect reset` needed: the whole clone is removed next, so there is nothing
        # left to leave in a detached-HEAD state.
        _rmtree(scratch_root)


def _rmtree(path: Path) -> None:
    import shutil
    import stat

    def _writable_then_retry(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    if path.exists():
        shutil.rmtree(path, onexc=_writable_then_retry)


def _bisect_step() -> int:
    """One `git bisect run` step, invoked as `<venv-python> known_reds.py _bisect-step` with
    the test id / venv / clone / timeout passed by environment (see `attribute`). Exit 0 good
    (passed), 1 bad (collected and failed), 125 skip (does not exist / does not collect here)."""
    test_id = os.environ["_KNOWN_REDS_BISECT_TEST_ID"]
    venv_py = os.environ["_KNOWN_REDS_BISECT_VENV_PY"]
    clone = os.environ["_KNOWN_REDS_BISECT_CLONE"]
    timeout = float(os.environ["_KNOWN_REDS_BISECT_TIMEOUT"])
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)
    cmd = [venv_py, "-m", "pytest", "-q", "--no-header", "--color=no", "-p", "no:cacheprovider",
          "--continue-on-collection-errors", test_id]
    try:
        done = subprocess.run(cmd, cwd=clone, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 125  # untestable at this commit within budget -- skip rather than misreport
    out = done.stdout + done.stderr
    sys.stderr.write(out[-2000:])
    # pytest's own exit code is definitive for a real run (0 all passed, 1 some collected and
    # failed) -- checked BEFORE any substring sniffing, so a failing test whose output happens
    # to contain a skip-ish phrase (e.g. "no tests ran" inside a failure message/traceback) is
    # never misclassified as a bisect skip.
    if done.returncode == 0:
        return 0
    if done.returncode == 1:
        return 1
    lowered = out.lower()
    if "no tests ran" in lowered or "error: not found" in lowered or "collected 0 items" in out:
        return 125
    return 125  # collection error / interrupted / usage error: ambiguous, never call it bad


# --- CLI -------------------------------------------------------------------------------------

def _load_attribution_file(path: str | None) -> dict:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for node_id, entry in data.items():
        out[node_id] = entry if isinstance(entry, dict) else {"attribution": entry}
    return out


def main(argv: list[str] | None = None) -> int:
    if argv is None and len(sys.argv) > 1 and sys.argv[1] == "_bisect-step":
        return _bisect_step()

    ap = argparse.ArgumentParser(description="The known-reds organ: baseline id, attribution, "
                                            "and CI's comparator (ADR-121 step 1).")
    ap.add_argument("--repo-root", default=None)
    sub = ap.add_subparsers(dest="command", required=True)

    ref = sub.add_parser("refresh", help="build/update logs/KNOWN-REDS-REGISTRY.json")
    ref.add_argument("--pytest-output", required=True)
    ref.add_argument("--workers", required=True, type=int)
    ref.add_argument("--commit", required=True)
    ref.add_argument("--measured-via", default="local")
    ref.add_argument("--date", required=True, help="YYYY-MM-DD, for the baseline id")
    ref.add_argument("--attribution", default=None, help="JSON {node_id: {attribution, reason?}}")
    ref.add_argument("--previous", default=None, help="a prior registry to carry members from")
    ref.add_argument("--registry", default=REGISTRY_PATH)
    ref.add_argument("--os", dest="os_key", default=None,
                     help="D2: write members_by_os[OS] instead of the shared set. Omitted "
                          "(the default) keeps the pre-D2 behaviour exactly -- "
                          "ecosystem/harness.yaml's merge-moment caller never passes this")

    cmp_ = sub.add_parser("compare", help="judge a run against the committed registry")
    cmp_.add_argument("--pytest-output", required=True)
    cmp_.add_argument("--workers", required=True, type=int)
    cmp_.add_argument("--pytest-exit", default=None, type=int)
    cmp_.add_argument("--registry", default=REGISTRY_PATH)
    cmp_.add_argument("--os", dest="os_key", default=None,
                      help="D2: the OS key whose members_by_os overlay to merge in. Omitted, "
                           "auto-detected from RUNNER_OS/sys.platform (default_os_key()) -- "
                           "conductor.yml, owned by another lane, need not pass this")

    cmp_hook = sub.add_parser("compare-hook",
                              help="judge one non-pytest hook's exit code against "
                                   "the registry's `hooks` section")
    cmp_hook.add_argument("--hook-id", required=True)
    cmp_hook.add_argument("--exit-code", required=True, type=int)
    cmp_hook.add_argument("--registry", default=REGISTRY_PATH)
    cmp_hook.add_argument("--hook-output", default=None,
                          help="raw hook stdout/stderr; scopes a `checks:`-bearing "
                               "registration to the specific failing check names it names, "
                               "instead of the whole hook (Codex terra HIGH, 2026-09-26)")

    attr = sub.add_parser("attribute", help="git bisect run, one test, and name the lane")
    attr.add_argument("--test", required=True)
    attr.add_argument("--good", required=True)
    attr.add_argument("--bad", required=True)
    attr.add_argument("--venv-python", required=True)
    attr.add_argument("--workdir", default=None)
    attr.add_argument("--timeout", default=180.0, type=float)

    for p in (ref, cmp_, cmp_hook, attr):
        p.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd()

    if args.command == "refresh":
        text = Path(args.pytest_output).read_text(encoding="utf-8", errors="replace")
        failed = conductor.parse_failed_node_ids(text)
        try:
            previous = load_registry(root / args.previous) if args.previous else None
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        if previous is not None:
            try:
                _git(root, "merge-base", "--is-ancestor", previous.measured_at_sha, args.commit)
            except KnownRedsError:
                print(f"known_reds: refusing -- previous registry's measured_at_sha "
                     f"{previous.measured_at_sha!r} is not an ancestor of --commit "
                     f"{args.commit!r}; a --previous registry measured on unrelated or "
                     f"future history cannot be trusted to carry members forward. Pass a "
                     f"--previous registry measured on this history, or omit --previous to "
                     f"start a fresh baseline with no carried-forward members.",
                     file=sys.stderr)
                return 1
        attribution = _load_attribution_file(args.attribution)
        signatures = extract_failure_signatures(text)
        try:
            registry, dropped = refresh(failed=failed, workers=args.workers, commit=args.commit,
                                        measured_via=args.measured_via, date=args.date,
                                        attribution=attribution, previous=previous,
                                        os_key=args.os_key, signatures=signatures)
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        write_registry(root / args.registry, registry)
        report = (f"known_reds: wrote {args.registry} -- baseline {registry.baseline_id}, "
                 f"{len(registry.members)} member(s), {len(dropped)} dropped (no longer failing)")
        print(report)
        if args.out:
            Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        return 0

    if args.command == "compare":
        text = Path(args.pytest_output).read_text(encoding="utf-8", errors="replace")
        failed = conductor.parse_failed_node_ids(text)
        signatures = extract_failure_signatures(text)
        os_key = args.os_key or default_os_key()
        try:
            registry = load_registry(root / args.registry)
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return EXIT_UNCOMPARABLE
        result = compare(failed, registry, workers=args.workers, pytest_exit=args.pytest_exit,
                         os_key=os_key, signatures=signatures)
        report = render_compare(result)
        if args.out:
            Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        print(report)
        return 0 if result["verdict"] == "pass" else 1

    if args.command == "compare-hook":
        try:
            registry = load_registry(root / args.registry)
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return EXIT_UNCOMPARABLE
        hook_output = (Path(args.hook_output).read_text(encoding="utf-8", errors="replace")
                      if args.hook_output else None)
        result = compare_hook(args.hook_id, args.exit_code, registry, hook_output=hook_output)
        report = render_compare_hook(result)
        if args.out:
            Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        print(report)
        return 0 if result["verdict"] == "pass" else 1

    if args.command == "attribute":
        result = attribute(root, args.test, good=args.good, bad=args.bad,
                           venv_python=Path(args.venv_python), workdir=Path(args.workdir)
                           if args.workdir else None, timeout=args.timeout)
        report = json.dumps({k: v for k, v in result.items() if k != "bisect_log"}, indent=2)
        print(report)
        if args.out:
            Path(args.out).write_text(json.dumps(result, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
        return 0

    return 1  # pragma: no cover -- argparse's `required=True` makes this unreachable


if __name__ == "__main__":
    sys.exit(main())
