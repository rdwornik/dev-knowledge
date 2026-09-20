#!/usr/bin/env python
"""graph_queries.py -- the commit-tier REFUSALS over the persisted FPG-1 store ([#664]).

WHAT THIS IS. `[#664]`'s acceptance clause, in code: *"three queries, each a REFUSAL at commit
tier"*. `orphan_census`, `task_coverage` and `process_list`, each wired to its own pre-commit
hook, each exiting non-zero on the property it refuses. A query that reports without refusing
discharges nothing -- the row says so and the frozen contract repeats it.

A FOURTH REFUSAL, `edge_class_census`, ARMS THE ROW'S OTHER HALF. `[#664]`'s Done-when has a
second bar the three queries do not reach: the five-kind edge computations (DECLARE-REVIEWS
section A.1, as narrowed by `ff103444`) re-measured and migrated. Lane `v-664` measured them
and nothing held the line afterwards. It is a RATCHET rather than a bar -- the set may shrink
and may not grow -- because ADR-118 section 5 rules the migration one organ per lane, so
refusing all eighteen at once would refuse every commit in the repo on a defect no committer
can repair. It is also the one refusal here that is NOT a view: see its section below.

ORGANS ARE VIEWS (ADR-118 §2). Every predicate here is a SELECT over
`scripts/graph_store.py`. Nothing in this module walks the tree for an edge, parses a config,
or computes a relation of its own; where a relation was missing it was added to FPG-1
(`triggers`, `imports`, `implements`) rather than computed here. That is intake #86's
acceptance criterion 5 -- *"a test asserts the organ imports the graph rather than walking the
tree"* -- and it is the whole point of the landing: a private computation here would defeat
the thing it is meant to prove.

STDLIB ONLY ON THE READ PATH, and it is deliberate. This module imports `graph_store`, which
defers its `file_purpose_graph` import into `rebuild()`. So three hooks per commit pay for
sqlite and nothing else; `rustworkx` is loaded once, by the rebuild hook, and never by a
reader.

THE ONE THING THIS MODULE HOLDS THAT IS NOT A QUERY -- `ORPHAN_DISPOSITIONS`, and it is
declared as an exception rather than left to be noticed. It is a curated register with a
reason and an owner per row: the "kept-as-manifest with a reason" form, and the same shape
`ecosystem/disposition-register.yaml` already uses for known WARNs. It lives HERE rather than
there for exactly one reason, which is footprint: `[#664]`'s frozen contract gives this lane
`scripts/`, `tests/`, `.pre-commit-config.yaml` and one audit, and `ecosystem/` is not its to
write. **Relocating it to `ecosystem/disposition-register.yaml` is an owed follow-up**, named
in this lane's artifact rather than left as a surprise.

NO LLM ANYWHERE IN A QUERY. `[#664]`'s anti-patterns list it first, ADR-118 §4 rules it
("no gate calls an LLM on its hot path"), and every predicate below is mechanical and seeded
by a fixture.

Usage:
    python scripts/graph_queries.py orphan-census  [--repo-root .] [--db PATH]
    python scripts/graph_queries.py task-coverage  [--repo-root .] [--staged PATH ...]
    python scripts/graph_queries.py process-list   [--repo-root .] [--render]
    python scripts/graph_queries.py edge-class-census [--repo-root .] [--staged PATH ...]
    python scripts/graph_queries.py moments        [--repo-root .]
"""

from __future__ import annotations

import argparse
import ast
import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

import graph_store as gs  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("graph-queries")

#: Reachability over these two kinds is what "triggered" means: a wiring surface fires a
#: process directly (`triggers`), and a fired process reaches what it calls (`imports`).
TRIGGER_KINDS = ("triggers", "imports")
#: The one kind `task_coverage` reads. Both of its directions are `implements` edges -- the
#: row naming the file and the file naming the row -- so the query asks ONE question.
COVERAGE_KINDS = ("implements",)


@dataclass(frozen=True)
class Finding:
    """One refusal. `subject` is the path; `evidence` is why, in the operator's terms."""
    subject: str
    evidence: str


@dataclass(frozen=True)
class Disposition:
    """A recorded reason a process may have no trigger, and who owns the decision.

    A DISPOSITION IS NOT AN EXEMPTION. It records that the absence of a trigger has been
    LOOKED AT and ruled, and it names who can change that. ADR-75's decoration rule is what
    keeps it honest: a disposition naming a file that is gone is surfaced by
    `stale_dispositions()` and pinned by a test, so the register cannot rot into paper
    suppressions.
    """
    reason: str
    owner: str


@dataclass(frozen=True)
class ProcessRow:
    """One row of the traversal that answers "all processes"."""
    path: str
    process_class: str
    triggered: bool
    trigger: str
    disposition: Disposition | None = None


# --------------------------------------------------------------- the disposition register
#
# THE 32-vs-20 GAP, RULED RATHER THAN ROUNDED -- `[#664]`'s clause 4, and the frozen
# contract's warning that *"32 -> 0 against a 20-item predicate is unreachable by
# construction"*.
#
# THE RULING: widen the node class to EVERY IN-TREE PROCESS FILE, and name what a corpus
# graph of this repo cannot see. `docs/audits/2026-09-08-technical-process-trigger-census.md`
# counted 32 orphans across three populations -- 20 script-class, 3 L0 hooks, 9 commands and
# skills. Of those, 6 are on the OPERATOR'S DISK under `~/.claude/` (three
# `block-onedrive.SUPERSEDED*.ps1` copies, `~/.claude/commands/codex-review.md`, two
# `~/.claude/skills/gotchas/` files). They are not tracked by this repo, so they are not nodes
# in a graph of this repo's corpus -- unrepresentable, not overlooked. The census already
# rules their disposition operator-owned (*"a file deletion in an exclusion-adjacent
# directory and is the operator's call, not a lane's"*), and ADR-54 makes `~/.claude/` a home
# this repo authors nothing in.
#
# Widening was chosen over "give the other 12 their own queries" because that 12 splits 6/6
# across in-repo and out-of-tree: a second query would still not reach the out-of-tree half,
# so it would buy a surface without buying an answer.
#
# WHAT THE WIDENED CLASS MEASURES, live: 38 orphans, not the census's 26 in-repo. The
# difference is measured, not hand-waved, and every row of it is below:
#   * +11 commands and +2 skills. The census reports 9 command/skill orphans and rules the
#     other 8 ON-DEMAND-BY-OPERATOR against a closed list of seven acts. That list is a
#     RULING, not a computation -- nothing in the tree fires a command -- so the mechanism
#     finds every in-repo command and skill, and the eight the census ruled on-demand are
#     dispositioned here with the act each maps to. The classification is preserved; what
#     changes is that it is now written down where a gate can read it.
#   * +2 script-class arrivals since the census's 2026-09-08 cut: `gen_ledger.py` (landed by
#     lane V-000 on 2026-09-09) and the derived-copy pair below.
#   * -1: `scripts/file_purpose_graph.py` is NO LONGER AN ORPHAN. It is the row's own
#     headline landing -- FPG-1 acquired a trigger, the `graph-rebuild` pre-commit hook, and
#     drops off this list by being wired rather than by being dispositioned.
#
# Every entry carries a reason and an owner, both asserted by tests.

_LANE_BUILT = ("lane-built and never adopted -- the process-trigger census's DECLARE §5 "
               "finding in mechanism form: lanes build organs and nothing adopts them "
               "afterwards. Retirement-or-wiring is V+1's list, not this lane's act")

_HOOKS_EMERGENCY_DISABLED = (
    "TEMPORARILY UNWIRED, not retired -- its only trigger was a .claude/settings.json hook, "
    "and ALL hook families were disabled 2026-09-17 by operator emergency order because hook "
    "processes are created SUSPENDED and never resumed (0 s CPU, no image path, one thread in "
    "Wait/Suspended), so no timeout can fire on them. The hook block is recoverable verbatim "
    "at 33246c0a and returns when [#863] lands; delete this row in that same act")

ORPHAN_DISPOSITIONS: dict[str, Disposition] = {
    # ---- population 0: SessionStart/Stop hook targets orphaned by the 2026-09-17 disable ----
    # These six are orphans only because their settings.json wiring was removed in an
    # emergency, not because nothing adopted them. A disposition, not a retirement, is the
    # honest verdict: the wiring is coming back under `[#863]`, which owns removing these rows.
    "scripts/changelog_sentinel.py": Disposition(reason=_HOOKS_EMERGENCY_DISABLED, owner="[#863]"),
    "scripts/codespace_regime.py": Disposition(reason=_HOOKS_EMERGENCY_DISABLED, owner="[#863]"),
    "scripts/logs_retention.py": Disposition(reason=_HOOKS_EMERGENCY_DISABLED, owner="[#863]"),
    "scripts/resource_lifecycle.py": Disposition(reason=_HOOKS_EMERGENCY_DISABLED, owner="[#863]"),
    "scripts/session_end_backpressure.py": Disposition(reason=_HOOKS_EMERGENCY_DISABLED,
                                                       owner="[#863]"),
    "scripts/surface_triage.ps1": Disposition(reason=_HOOKS_EMERGENCY_DISABLED, owner="[#863]"),
    # ---- population A: scripts, lane-built and never wired (the census's own class) ----
    # NOT population A, and the row is a KEEP rather than the DELETE its old text implied. That
    # text -- `_LANE_BUILT` plus "only call site is LANE-f-6-observability-otel.md:27" -- said
    # lane-built-and-never-adopted with a spent lane contract for a call site, which reads as a
    # retirement candidate and is how `[#664]`'s census found it. It was STALE, and the census
    # said so in its own §4.2; corrected here by `[#664]`'s ratified register-row correction
    # (2026-09-13, lane `lane-x-664-delete-list-execution`).
    #
    # WHAT IS ACTUALLY TRUE: `[#694]` records this module PARTIALLY DISCHARGED -- *"no longer
    # inventory"* -- and FPG-1 confirms the call site rather than the lane contract:
    # `why scripts/cost_usage_telemetry.py` -> `is imported by file:scripts/provider_router.py
    # [wiring]`. So it is an ADOPTED library whose ADOPTER is untriggered, which is a different
    # condition from an unadopted organ and takes a different remedy: it inherits the row above
    # and moves with it. Wiring it independently would assert the very call `[#691]` Half A is
    # forbidden from placing.
    "scripts/cost_usage_telemetry.py": Disposition(
        reason="KEEP -- ADOPTED, not inventory, and this text replaces a stale one that read "
               "as a DELETE. [#694] records it PARTIALLY DISCHARGED ('no longer inventory') and "
               "FPG-1 holds the real call site: imported by scripts/provider_router.py. It is "
               "untriggered ONLY because that caller is, so it inherits provider_router.py's "
               "row above and is adopted by the same act -- [#691] Half B routing through the "
               "router. Wiring it on its own would place the non-Claude call AX23-2 forbids",
        owner="[#691] Half B, jointly with the provider_router.py row above; [#694] owns the "
              "telemetry decision itself"),
    # NOT population A, and the distinction is the whole reason this row is written out rather
    # than folded into `_LANE_BUILT`. `provider_router.py` is not an organ nobody adopted; it
    # is an organ whose consumer is a lane that has not run yet, and the gap is REQUIRED by the
    # clause that ordered it.
    #
    # AX23-2 splits `[#691]` in two: Half A builds the routing mechanism with NO non-Claude
    # provider ordered, Half B does the admission calls. A router acquires a trigger by
    # something routing through it, and in Half A nothing may -- placing a call is the one act
    # the lane is defined by not doing. So "wire it" is unavailable to the lane that wrote it,
    # by construction rather than by omission, and shipping it unwired is the correct state
    # rather than a deferred chore.
    #
    # The other two remedies are wrong here for reasons worth recording. "Retire it" would
    # delete the mechanism the next lane consumes. "Wire it to a pre-commit hook" was
    # considered and rejected: a gate asserting every role resolves to an eligible provider is
    # a genuinely good idea, but a NEW hook is an AX4-1 floor-declaration event requiring an
    # `ecosystem/parity-surfaces.yaml` registration, and that surface is not this lane's to
    # write. It is named in the lane artifact as an owed follow-up, not left to be noticed.
    #
    # This row's OWNER is therefore a specific successor lane, not a general list: Half B
    # adopts it by routing through it, at which point the row is deleted rather than updated.
    "scripts/provider_router.py": Disposition(
        reason=("[#691] Half A built the routing mechanism under AX23-2, which forbids the lane "
                "from ordering any non-Claude provider -- so the router cannot acquire a "
                "trigger in the half that wrote it, because routing through it IS placing a "
                "call. Unwired is the contract-required state, not an unadopted one. A "
                "pre-commit gate over it is an AX4-1 floor-declaration act needing a "
                "parity-surfaces registration, which is outside this lane's footprint"),
        owner="[#691] Half B (non-Claude admission), which adopts it by routing through it"),
    # SAME SHAPE AS THE ROW ABOVE, and cited as the precedent rather than argued from scratch:
    # a mechanism whose ADOPTER is the very thing its authoring lane is forbidden to build.
    #
    # `scripts/codespace_state.py` is the recovery-container discriminator and the lane-state
    # cross. What would trigger it is an OBSERVER -- something that polls a codespace's state,
    # or receives a progress push from inside one, and calls this classifier with the result.
    # Which of those it is, or whether it is both, is the open architectural question filed as
    # intake 102 and routed to the decision engine by operator directive on 2026-09-15. The
    # directive is explicit that the question is not to be settled in a diff, so writing the
    # observer here would decide it by implementation -- which is the one act this work is
    # defined by not doing.
    #
    # The other two remedies are wrong for reasons worth recording. "Retire it" would delete the
    # classifier every one of the options A/B/C would call -- it is the part of the design that
    # does NOT depend on the ruling, which is precisely why it was safe to build first. "Wire it
    # to a pre-commit hook" is unavailable on its merits rather than on footprint: the organ
    # needs a LIVE codespace name to classify, and a commit-time gate has none.
    #
    # It is not untested: `tests/test_codespace_state.py` holds its RED-first witnesses and two
    # register trip-tests (QR-OBS-004, QR-OBS-005) run against it and go RED when it is neutered.
    # A test is not a wiring surface, which is why this row exists rather than the census being
    # wrong.
    "scripts/codespace_state.py": Disposition(
        reason=("the classifier's adopter is an observer whose shape -- poll from outside, push "
                "from inside, or both -- is the open architectural question filed as intake 102 "
                "and routed to the decision engine by operator directive, which forbids settling "
                "it in a diff. Unwired is the directive-required state, not an unadopted one. A "
                "pre-commit gate is unavailable on merits: classifying needs a live codespace "
                "name and a commit-time gate has none"),
        owner="the ratification of intake 102, whose chosen observer adopts it by calling it"),
    # `scripts/gen_trend_dashboard.py` and `scripts/gen_north_star.py` WERE dispositioned here,
    # both on `_LANE_BUILT`. `[#664]`'s ratified DELETE list retired them (2026-09-13, lane
    # `lane-x-664-delete-list-execution`), in that order -- the dashboard imports the north-star
    # view through `importlib`, so deleting the importer second would have turned a clean
    # removal into a broken load. The rows leave WITH their subjects: a disposition says "this
    # orphan was LOOKED AT and ruled", and a file that is gone is not an orphan, so keeping the
    # row would be the paper suppression `stale_dispositions()` exists to surface.
    # NOT population A either, and the distinction earns its own comment rather than being
    # folded into `_LANE_BUILT`. `merge_receipt.py` IS adopted: `.claude/commands/
    # lane-integrate.md` issues it at four points of the merge walk, which is the opposite of
    # lane-built-and-never-wired. The census cannot see that, because the `[#664]` wiring
    # surfaces are `.pre-commit-config.yaml`, `.claude/settings.json`, the plugin `hooks.json`,
    # the scheduled task and the CI workflows -- and a COMMAND FILE is none of them. So EVERY
    # operator-invoked organ in this repo reads as an orphan by construction, whatever its real
    # adoption. That is a gap in the census's input list, not a property of this module, and it
    # is recorded here rather than only in a lane artifact because this row is where a reader
    # meets it.
    #
    # Widening the surface list is deliberately NOT done from here. It would change what
    # `graph-orphan-census` refuses across the whole repo, from a lane whose contract is merge
    # cost -- the same discipline `[#675]` clause 1 states one organ over ("a lane that fixes
    # dispatch properly while making clause 1 green has overrun its contract").
    #
    # A pre-commit trigger was considered and rejected ON THE MERITS, not merely as out of
    # scope: a stopwatch has nothing to gate. Elapsed time is not a property a commit can be
    # refused for, and a hook that ran the receipt would have Layer 2 execute the very merge
    # this module is built not to drive (Critical Rule #4).
    "scripts/merge_receipt.py": Disposition(
        reason="[#675] target 3.1. Wired to .claude/commands/lane-integrate.md (open / time / "
               "race / close across the merge walk), which is not one of the [#664] wiring "
               "surfaces the census reads -- so an operator-invoked organ reads as an orphan "
               "by construction. A pre-commit trigger is wrong on the merits, not merely out "
               "of scope: a stopwatch has nothing to gate, and a hook that ran it would make "
               "Layer 2 execute the merge this module exists NOT to drive",
        owner="the [#664] wiring-surface list, which owns whether .claude/commands/*.md is a "
              "trigger surface; this row is deleted by that decision, not by a lane"),
    # SAME CLASS AS `merge_receipt.py` ABOVE, and the repetition is the point: two organs added
    # by one lane, both genuinely adopted by `.claude/commands/lane-integrate.md`, both reading
    # as orphans because a command file is not a `[#664]` wiring surface. One such row is a
    # curiosity; two from a single lane is the shape of a gap, and it is recorded as one here
    # rather than left for a third lane to rediscover.
    "scripts/actions_verdict.py": Disposition(
        reason="[#675] target 3.2. Wired to .claude/commands/lane-integrate.md (the merge-walk "
               "read of the Actions verdict, and refuse-to-finish checklist row 2b), which is "
               "not one of the [#664] wiring surfaces the census reads. A pre-commit trigger "
               "is wrong on the merits: it reads a GitHub Actions run for a merge SHA, which "
               "does not exist at commit time -- the gate would query a run that cannot have "
               "started and refuse every commit",
        owner="the [#664] wiring-surface list, which owns whether .claude/commands/*.md is a "
              "trigger surface; this row is deleted by that decision, not by a lane"),
    # THIRD OF THE SAME SHAPE FROM ONE LANE, and at three it stops being a coincidence and
    # becomes the finding: `[#675]` added `merge_receipt.py`, `actions_verdict.py` and this,
    # all three adopted by `.claude/commands/lane-integrate.md`, all three orphans to a census
    # whose wiring surfaces do not include command files. The lane's end artifact carries the
    # proposed diff; these rows carry the evidence that it is a class rather than an instance.
    "scripts/review_packet.py": Disposition(
        reason="[#675] target 3.5. Wired to .claude/commands/lane-integrate.md (the assemble "
               "step of the merge walk, and refuse-to-finish checklist row 2c), which is not "
               "one of the [#664] wiring surfaces the census reads. A pre-commit trigger is "
               "wrong on the merits: it assembles a REVIEW input over a merge range against a "
               "lane contract, neither of which exists at commit time in the lane being "
               "reviewed",
        owner="the [#664] wiring-surface list, which owns whether .claude/commands/*.md is a "
              "trigger surface; this row is deleted by that decision, not by a lane"),
    # A DIFFERENT SHAPE FROM THE THREE ABOVE, and the difference is the whole disposition.
    # Those three have a trigger the census cannot see. This one has no trigger AT ALL and
    # should not have one.
    # THE SAME SHAPE AS `provider_bench.py` BELOW -- no trigger AT ALL, and none is wanted --
    # but for a different reason, so it is stated rather than inherited. `provider_bench` has no
    # trigger because firing it costs money. This one has no trigger because NO HOOK TYPE CAN
    # MAKE ITS DECISION.
    "scripts/context_reclamation.py": Disposition(
        reason="[#792]'s context-reclamation half. Its caller is a SEAT deciding to clear its "
               "own context at a checkpoint, judged on that seat's own running cost median -- "
               "a decision no event in the [#664] wiring-surface list is positioned to make. "
               "A commit-tier trigger is wrong on the merits (a commit is not a checkpoint and "
               "carries no cost history); a SessionStart trigger is wrong at both ends (a seat "
               "at session start has no turns to have a median of, and the act is a CLEAR "
               "which a start hook cannot perform). Its consumers are named rather than "
               "invented: tests/test_context_reclamation.py proves the mechanism including the "
               "trip-test, and docs/audits/2026-09-15-technical-lane-aa-14-resource-lifecycle.md "
               "section 3.1 carries the derivation its threshold rests on. Wiring it to a hook "
               "that merely PRINTS, to satisfy this census, would be declared enforcement "
               "without enforcement -- the exact shape QR-RES-004 records against the seat "
               "boot -- and would be the census changing the design. Its SIBLING is wired: "
               "scripts/resource_lifecycle.py sits on SessionStart, because a session start IS "
               "a seat allocation and that half of the organ has a real event to hang on",
        owner="[#791], which carries intake 101 through the decision engine and owns the "
              "question of who initiates reclamation. When that ADR answers it, the answer "
              "names a trigger and this row is deleted by [#791]'s lane -- not by this one"),
    "scripts/provider_bench.py": Disposition(
        reason="[#785]'s unattended provider benchmark. It is a one-off MEASUREMENT, not an "
               "organ: every subcommand makes real PAID network calls to five vendor CLIs, so "
               "a commit-tier or session-tier trigger would bill the operator on every commit "
               "to measure something that changes only when a vendor ships. The night plan's "
               "rule is 'no new organ without a trigger and a NAMED CONSUMER', and the "
               "consumers are named rather than invented: docs/audits/"
               "2026-09-15-technical-lane-z-4-non-claude-execution.md reads its ledger, "
               "logs/PROVIDER-BENCH-RUNS.jsonl is the ledger, and tests/test_provider_bench.py "
               "proves the instrument. Wiring it to a hook to satisfy this census would be the "
               "census changing the design, which is the wrong way round",
        owner="[#676], which owns the commit-tier provider-invocation check. If that check "
              "lands and consumes these shapes as data, the offline half gains a real trigger "
              "and this row is deleted by [#676]'s lane -- not by this one"),
    # SAME REASON AS `provider_bench.py` ABOVE FOR A DIFFERENT COST -- no trigger AT ALL, and
    # none is wanted, because the one hook that would give it one already states, in its own
    # docstring, why that hook does not scan transcripts: `lane_cost.cost_health_line` reads
    # ONE precomputed ledger file rather than the session store, specifically because
    # SessionStart pays for the digest on EVERY boot and a transcript walk would make that cost
    # grow with the history rather than with the batch. This module's `organ_usage_report()` IS
    # a transcript walk -- that is the only way AX9-5's metric can exist at all, since nothing
    # in this repo persists a raw-search-vs-organ-call event -- so wiring it to SessionStart
    # would reintroduce the exact anti-pattern `cost_health_line` was written to avoid, on the
    # widest-audience hook in the repo.
    "scripts/organ_usage_metric.py": Disposition(
        reason="[#694]'s AX9-5 metric (raw-search vs organ calls per session, organs uncalled "
               "in 30d). An on-demand operator report over Claude Code's own session "
               "transcripts, deliberately NOT a SessionStart digest line: `fleet_health.py`'s "
               "existing cost line reads one precomputed ledger for exactly this reason -- a "
               "boot-time transcript scan grows with history, not with the batch. Its consumer "
               "is named rather than invented: tests/test_organ_usage_metric.py proves the "
               "classifier and the report, and its own CLI (`report` subcommand) is the "
               "operator's call site",
        owner="[#709] (the log-review routine AX9-5 names as its regression-flagging "
              "consumer) or a future on-demand digest command; either adopts it by calling "
              "it, at which point this row is deleted rather than updated"),
    # `scripts/logs_retention.py` WAS dispositioned here, on the DECLARE §3 finding that
    # `run_retention()` had 0 callers -- which is `[#655]`'s entire title. It is GONE from this
    # register because it is WIRED: `[#664]`'s second ratified TRIGGER row put it on the
    # `SessionStart` path in `.claude/settings.json` (2026-09-13, lane
    # `lane-x-664-delete-list-execution`). SessionStart rather than Stop, deliberately: the
    # producer of the files it retains is `propose_closures.py` on the plugin's Stop hook, and
    # a renamer sharing that event with the producer's own `**/PROPOSALS-*.md` read buys
    # nothing that the next session's start does not. Pinned by
    # `tests/test_logs_retention.py::test_the_retention_trigger_is_on_SESSION_START_not_STOP`.
    # `scripts/nopack_sandbox.py` and `scripts/trace_writer.py` WERE dispositioned here. Retired
    # by `[#664]`'s ratified DELETE list (2026-09-13, lane
    # `lane-x-664-delete-list-execution`). These two carried NO inbound edge of any kind -- not
    # a row, not an import, not a wiring surface -- so unlike the four above they left no
    # `task-implements` residue behind them. Their only recorded call sites were spent lane
    # contracts, which are immutable and already run.
    # `scripts/window_metrics.py` and `scripts/failed_set.py` WERE dispositioned here. Retired
    # by `[#664]`'s ratified DELETE list in that order (2026-09-13, lane
    # `lane-x-664-delete-list-execution`): `failed_set` was an orphan BY INHERITANCE from
    # `window_metrics.py:359`, and its row said in its own words that it is "dispositioned WITH
    # its caller and not before it" -- so it is retired with its caller and not before it
    # either. Same rule as the pair above: the row leaves with its subject.
    # KEPT, and the reason is a FINDING rather than a deferral. The AX13-2 retire stage
    # deleted this module on a SAFE oracle verdict and the full suite went RED: nothing
    # static reaches it, but `tests/test_membership_agreement.py` loads it BY NAME through
    # importlib, which is exactly the invisible-edge class ADR-89 declares its static
    # Pyright oracle cannot see. The verdict was a false PASS -- non-blocking by design,
    # and caught only because the lane ran a paired baseline/tip suite. Restored whole.
    "scripts/desired_state_loader.py": Disposition(
        reason="KEPT 2026-09-12 on POSITIVE EVIDENCE -- not an unadopted organ. It is an "
               "orphan to a STATIC census only: tests/test_membership_agreement.py loads it "
               "by name through importlib and pins parse_registry_md as the reference "
               "implementation that keeps audit.py's duplicated inline registry reader "
               "honest. Deleting it REDs that test, so the retire stage's SAFE verdict on it "
               "was a false PASS inside ADR-89's own declared static-only limit",
        owner="none -- retire only WITH the importlib pin in test_membership_agreement.py"),
    "scripts/gen_ledger.py": Disposition(
        reason="ARRIVED AFTER THE CENSUS -- landed 2026-09-09 by lane V-000 and therefore "
               "absent from its 32. Recorded as a NEW orphan rather than folded into the "
               "old count: the census is a dated measurement, not a live roster",
        owner="V+1 retirement-or-wiring list"),
    "scripts/offload_admission.py": Disposition(
        reason="ARRIVED AFTER THE CENSUS -- landed 2026-09-09 by lane "
               "v-000-offload-admission, same class as gen_ledger.py above and recorded the "
               "same way. It is UNWIRED BY DESIGN rather than by neglect: the lane's artifact "
               "section 7 states it does not write ecosystem/routing-table.yaml, because "
               "creating the offload role row is a routing decision and the lane REFUSED the "
               "only route it measured. Wiring it would assert an admission that was denied",
        owner="V+1 retirement-or-wiring list"),
    # ---- population A: tests are not triggers ----
    # `scripts/archive_row_body.py` WAS dispositioned here, on exactly that heading: referenced
    # only by its own test file, and a test proves a module works while scheduling nothing. It
    # is GONE from this register because it is WIRED, not because it was retired -- `[#664]`'s
    # ratified TRIGGER row landed the `row-archive-proof` pre-commit hook (2026-09-13, lane
    # `lane-x-664-delete-list-execution`), beside `validate-backlog`, which is the surface the
    # census named. A row leaves this register in both directions and for the same reason: the
    # register holds live rulings about orphans, and a wired module is not an orphan.
    # ---- population A: orphan BY DESIGN, and wiring it would RED a test ----
    "scripts/export_backlog_view.py": Disposition(
        reason="ORPHAN BY DESIGN: tests/test_export_backlog_view.py::test_no_gate_hook_or_"
               "script_reads_the_export ASSERTS that nothing reads it ([#563] one-way view "
               "layer). Wiring it would RED that test, so the disposition is a ruling rather "
               "than a defect and this row must never be 'fixed'",
        owner="[#563] -- settled; reopening needs a ruling, not a lane"),
    "scripts/setup-fleet-scheduler.ps1": Disposition(
        reason="one-shot INSTALLER. The task it registers is live (Get-ScheduledTask -> "
               "fleet-baseline, State=Ready), so the PROCESS is triggered; an installer is "
               "not a recurring process and never was",
        owner="operator -- machine setup, not repo wiring"),
    # ---- population A: derived-copy SOURCES, which fire as their copies ----
    "scripts/propose_closures.py": Disposition(
        reason="DERIVED-COPY SOURCE. The armed process is the plugin copy "
               "plugins/tier1-lifecycle/scripts/propose_closures.py, which the plugin Stop "
               "hook fires; this is the hub original it is generated from, registered in "
               "ecosystem/derived-copies.yaml. A source is not an orphan, it is upstream -- "
               "and the pair is exactly why the wiring loader resolves a plugin manifest's "
               "path against the PLUGIN root before the repo root",
        owner="ecosystem/derived-copies.yaml -- the registry that owns the pair"),
    "scripts/review_closures.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification. Invoked by /review-closures "
               "(plugins/tier1-lifecycle/commands/review-closures.md:20). Also the "
               "derived-copy source of the plugin copy below",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/scripts/review_closures.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification. The plugin copy invoked by "
               "/review-closures; no event fires it and none should",
        owner="operator -- one of the census's seven acts"),
    # ---- population A: on-demand, mapped to one of the seven acts ----
    "scripts/worktree_import_proof.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md:174)",
        owner="operator -- one of the census's seven acts"),
    "scripts/single_flight.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md:71) and /lane-integrate:132. A FINDING "
               "AGAINST THE CENSUS, recorded rather than quietly absorbed: it is absent "
               "from the census's 20 and this query finds it, which is exactly intake #86's "
               "acceptance criterion 2 -- 'every orphan the query finds that the sweep "
               "missed is recorded as a finding against the sweep', reported and never "
               "silently reconciled",
        owner="operator -- one of the census's seven acts"),
    "scripts/id_allocator.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md, section 6 'Run the lane') when a lane needs a "
               "new task id: it reserves the id by a create-only push BEFORE the lane writes "
               "it ([#804]/[#788]). No event should fire it, because a reservation is a "
               "lane's decision to file",
        owner="operator -- one of the census's seven acts; [#804] owns the allocator"),
    "scripts/lane_boot.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md, section 1 'Pre-flight') before any worktree "
               "exists. It is the manifest refusal PLAYBOOK claimed /lane-boot already made "
               "([#804]). The dispatch verb in win-tooling does not call it yet, and that is "
               "recorded as an out-of-footprint follow-up, not a trigger",
        owner="operator -- one of the census's seven acts; [#804] owns the refusal"),
    # ---- NOT population A: MACHINE-TRIGGERED, by a surface this census cannot see ----
    #
    # THIS ROW IS A FINDING AGAINST `WIRING_SURFACES`, not a ruling that the file has no
    # trigger. It is the same false-orphan verdict that got the module's predecessor DELETED,
    # written down this time instead of acted on. `scripts/cloud_provisioning.py` was retired at
    # `3c9418cc` ([#734]) as an unreferenced census orphan; its six callers were
    # `.devcontainer/provision.sh`, naming it BY PATH in a shell command. `safe_remove`'s static
    # importer scan cannot see that referrer and neither can this census, so a live module read
    # as dead, the deletion landed, and on 2026-09-14 a fresh codespace died into a recovery
    # container ([#746]: "can't open file .../scripts/cloud_provisioning.py", then
    # "Container creation failed" -> "Creating recovery container").
    #
    # WHAT ACTUALLY TRIGGERS IT, with no human deciding in the moment -- which is the census's
    # own predicate, taken verbatim from the process-trigger census's Method section:
    #   .devcontainer/devcontainer.json  "onCreateCommand"  -> bash .devcontainer/provision.sh
    #                                    "postCreateCommand" -> bash .devcontainer/provision.sh
    #                                    "postStartCommand"  -> bash .devcontainer/provision.sh --gate
    #   .devcontainer/provision.sh       leg2b_history / leg5_ecosystem / gate()
    #                                    -> uv run --no-sync python scripts/provision_legs.py
    # Every Codespaces container creation fires that chain. It satisfies the predicate as
    # squarely as any row in `WIRING_SURFACES` does; the enum simply does not list it, and
    # `_SCRIPT_PATH_RE` reads config VALUES rather than shell scripts, so even adding
    # devcontainer.json would not reach through `provision.sh` to this file.
    #
    # WHY A DISPOSITION AND NOT THE ENUM FIX. Widening `WIRING_SURFACES` changes the census
    # POPULATION repo-wide -- every `scripts/*.py` any shell script names stops being an orphan
    # at once -- and that is a change to what the corpus measures, not a lane's edit to make
    # inside a `.devcontainer/` footprint. Recorded here so the next census reads a ruling
    # instead of re-deriving the deletion.
    # `scripts/provision_legs.py` HAD A ROW HERE AND NO LONGER NEEDS ONE — DISCHARGED
    # 2026-09-15 ([#554] lane aa-1). The row said the file is machine-triggered, named
    # `.devcontainer/provision.sh` as the trigger, and closed with the honest sentence that
    # made it a placeholder rather than a ruling: *"the underlying WIRING_SURFACES gap is a
    # finding against the enum and is reported in this lane's end-of-lane artifact, not ruled
    # here."* The enum now lists the two provisioning surfaces, the census sees the trigger,
    # and `safe_remove` refuses the removal on the same edge — so the row would be a register
    # entry contradicting the graph, which
    # `test_a_disposition_register_entry_cannot_manufacture_its_own_trigger` refuses outright.
    #
    # Kept as a comment and not deleted silently, because a disposition that vanishes with no
    # trace reads as a file that stopped being interesting rather than as a gap that got
    # closed — and the next census would re-derive the deletion that cost a codespace.
    # ---- population C: commands. NOTHING FIRES A COMMAND, and that is the finding ----
    ".claude/commands/boot-session.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = sitting. No event fires a command; the census "
               "rules the seven acts a closed list and this is one of them",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/handoff.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = seat release",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/handoff-verify.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = seat release",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/lane-boot.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/lane-integrate.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/commands/review-closures.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/commands/ship.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = destructive acts",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/changelog-review.md": Disposition(
        reason="ORPHAN in the census's own terms: a PUSH trigger only. A SessionStart "
               "sentinel NUDGES it, and a nudge is not a trigger -- the distinction the "
               "census draws deliberately and this register preserves",
        owner="V+1 retirement-or-wiring list"),
    # `.claude/commands/override.md` WAS dispositioned here, on the 2026-09-07
    # census-templates ruling that "the file IS the retirement notice, which is why it is
    # kept rather than deleted". `5e17ecd7` ([#683], batch W, closed on the operator's word)
    # then DELETED it -- "remove /override: node, payload and the carrier leg, in one act".
    # The row is removed rather than re-worded: a disposition says "this orphan was LOOKED AT
    # and ruled", and a file that is gone is not an orphan, so keeping the row would be the
    # paper suppression `stale_dispositions()` exists to surface. The superseding act is
    # recorded here rather than in the register, because the register holds live rulings only.
    ".claude/commands/preflight.md": Disposition(
        reason="its own frontmatter says 'wired into no gate' -- a self-declared orphan, and "
               "an adoption-first read-only helper is a legitimate shape for one",
        owner="V+1 retirement-or-wiring list"),
    ".claude/commands/save.md": Disposition(
        reason="convenience wrapper, not one of the seven acts. INVISIBLE TO THE CENSUS'S "
               "OWN MECHANISM until this lane made every process file a node -- nothing "
               "named it, so it had no vertex to be counted at",
        owner="V+1 retirement-or-wiring list"),
    # ---- population C: skills. A MANDATE IN PROSE IS NOT A TRIGGER ----
    ".claude/skills/verify/SKILL.md": Disposition(
        reason="no event fires a skill; a skill is read when a seat chooses to read it. The "
               "census's finding, not a filing error -- and [#664]'s anti-pattern list rules "
               "the repair: a skill's mandate becomes a HOOK, never a graph row",
        owner="V+1 retirement-or-wiring list"),
    ".claude/skills/check-against-spec/SKILL.md": Disposition(
        reason="no event fires a skill. Same class as `verify` above; the mandate lives in "
               "prose and prose is carried by seats' diligence, which is the missing spine "
               "the DECLARE §5 names",
        owner="V+1 retirement-or-wiring list"),
    # SAME CLASS AS `gen_ledger.py` ABOVE: a NEW operator-transport report generator, arrived
    # after the census, ON-DEMAND-BY-CLI rather than hook-fired. [#730] AX27-5's closure list is
    # read by the operator at `to-browser/CLOSURE-LIST-<date>.md`, the same shape gen_ledger.py
    # and gen_handoff.py already use for that directory -- a wiring surface for it is a
    # [#664]-scope decision (would a CLI report generator's own invocation count as a trigger?),
    # not this lane's to make, and dispositioned rather than silently left for the census to
    # rediscover.
    "scripts/propose_row_closures.py": Disposition(
        reason="[#730] AX16-2/AX27-5's witness scan. ARRIVED AFTER THE CENSUS, same class as "
               "gen_ledger.py above: an operator-transport report generator (writes "
               "to-browser/CLOSURE-LIST-<date>.md), run on demand from the CLI rather than "
               "fired by any [#664] wiring surface. This lane's own footprint is `scripts/` "
               "and `tests/` -- deciding whether a command file should invoke it is a "
               "successor act, not spent here",
        owner="V+1 retirement-or-wiring list"),
}


# ---------------------------------------------------------------------- query 1: the census


def orphan_census(repo_root: Path | str, store: gs.GraphStore,
                  dispositions: dict[str, Disposition] | None = None) -> list[Finding]:
    """REFUSE on a process node no wiring surface reaches, transitively, and nothing rules.

    intake #86's organ, at commit tier. The predicate is a REACHABILITY query over the store
    -- in-degree alone would be wrong, because a module reached only through three imports is
    triggered just as truly as one a hook names directly, and the census closes its call
    graph for exactly that reason.
    """
    del repo_root  # the store answers; the tree is not read here, and that is the point
    register = ORPHAN_DISPOSITIONS if dispositions is None else dispositions
    reached = store.reachable(store.roots(), TRIGGER_KINDS)
    findings: list[Finding] = []
    for node in store.processes():
        if node.key in reached or node.path in register:
            continue
        findings.append(Finding(
            subject=node.path,
            evidence=(f"{node.process_class} reached by no wiring surface over "
                      f"{'/'.join(TRIGGER_KINDS)}. Wire it, retire it, or add a disposition "
                      f"with a reason and an owner to ORPHAN_DISPOSITIONS.")))
    return findings


def stale_dispositions(repo_root: Path | str,
                       dispositions: dict[str, Disposition] | None = None) -> list[str]:
    """Dispositioned paths that are no longer on disk -- ADR-75's decoration rule.

    Surfaced, never blocking: a register allowed to rot into paper suppressions is worse than
    no register, and a stale row is a fact about the register rather than about the commit.
    """
    root = Path(repo_root)
    register = ORPHAN_DISPOSITIONS if dispositions is None else dispositions
    return sorted(path for path in register if not (root / path).exists())


# -------------------------------------------------------------------- query 2: task coverage

#: Surfaces that cannot carry an ownership claim, each with the reason it cannot. This is a
#: SHORT and REASONED list, not a convenience escape: every entry is either generated (its
#: content is not authored, so a row citation in it would be a generator's, not a claim) or
#: is a record of every row at once (a journal entry names every row a session touched, so
#: reading it as ownership would make everything covered).
COVERAGE_EXEMPT: dict[str, str] = {
    "JOURNAL.md": "names every row a session touched -- ownership read from it is vacuous",
    "BACKLOG.md": "generated VIEW of tasks/; never read for an edge (FPG-1 input 4's rule)",
    "tasks/manifest.json": "generated by gen_task_tree.py",
    "ecosystem/organ-index.md": "generated by generate_organ_index.py",
    "ecosystem/doc-counts.md": "generated by gen_doc_counts.py",
    "docs/audits/README.md": "generated by gen_audit_index.py",
    "docs/intake/README.md": "generated by gen_intake_tree.py",
    "docs/intake/manifest.json": "generated by gen_intake_tree.py",
    ".claude/methodology-roster.md": "generated by gen_methodology_roster.py",
    "uv.lock": "generated by uv; ADR-106 owns its lifecycle",
}
#: Directory prefixes under the same rule.
COVERAGE_EXEMPT_PREFIXES: tuple[str, ...] = (".claude/generated/",)


def staged_paths(repo_root: Path | str) -> list[str]:
    """The files this commit is about to write -- `git diff --cached`, ACMR.

    THE ONE PLACE THIS MODULE READS COMMIT STATE RATHER THAN THE GRAPH, and it is named
    rather than hidden. DECLARE-REVIEWS §A.1 correction 2 rules that a two-tree gate cannot
    be a view: the staged set is commit-time state and stays a gate; the `implements`
    relation is corpus structure and is a query. `task_coverage` is the JOIN of the two, and
    calling it a pure view would be the mis-filing that correction exists to prevent.
    """
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=repo_root, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
        return []
    if out.returncode != 0:
        return []
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def _merge_in_progress(repo_root: Path | str) -> bool:
    """`MERGE_HEAD` present in the RESOLVED git dir -- a merge is being committed.

    Resolved, never `repo_root / ".git" / "MERGE_HEAD"`: in a worktree `.git` is a file and
    the naive spelling answers False for every merge a lane ever makes, which is the one
    place this carve-out has to work.
    """
    git_dir = gs._resolved_git_dir(Path(repo_root))
    return bool(git_dir and (git_dir / "MERGE_HEAD").exists())


def _worktree_skew(repo_root: Path | str) -> set[str]:
    """Files whose WORKING-TREE bytes are not what this commit will write.

    Unstaged modifications to tracked files, plus untracked files. Empty when git cannot
    answer, which is the same posture `staged_paths` takes: with no git there is no staged
    set either, so the gate has nothing to be lenient about.
    """
    skew: set[str] = set()
    for args in (["git", "diff", "--name-only", "--diff-filter=ACMR"],
                 ["git", "ls-files", "--others", "--exclude-standard"]):
        try:
            out = subprocess.run(args, cwd=repo_root, capture_output=True, text=True,
                                 timeout=60)
        except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
            return set()
        if out.returncode != 0:
            return set()
        skew.update(line.strip() for line in out.stdout.splitlines() if line.strip())
    return skew


def _evidence_paths(store: gs.GraphStore, relpath: str, edges: list[dict]) -> set[str]:
    """Every file the coverage claim for `relpath` actually rests on.

    Both legs, because coverage holds in both directions: the file itself (it may name the
    row) and each row that names it. A claim is only as staged as the file carrying it.
    """
    paths = {relpath}
    for edge in edges:
        node = store.node(edge["src"])
        if node and node.path:
            paths.add(node.path)
    return paths


def _exempt(relpath: str) -> str | None:
    if relpath in COVERAGE_EXEMPT:
        return COVERAGE_EXEMPT[relpath]
    for prefix in COVERAGE_EXEMPT_PREFIXES:
        if relpath.startswith(prefix):
            return f"under {prefix} -- generated"
    return None


def task_coverage(repo_root: Path | str, store: gs.GraphStore,
                  staged: list[str] | None = None) -> list[Finding]:
    """REFUSE on a staged file with no inbound `implements` edge from an OPEN row.

    "nic bez taska" as a mechanism, AT OPEN and not only at CLOSE -- `[#664]`'s own framing.
    Coverage holds if the row names the file OR the file names the row; both are `implements`
    edges, so the query asks one question of the graph rather than two of the tree.

    TWO TREES, AND THE SKEW BETWEEN THEM IS THIS GATE'S ONE REAL HAZARD. The subject set is
    the INDEX (`git diff --cached`); the `implements` relation comes from a graph built off
    the WORKING TREE. Left alone, that gap is a bypass: stage an unclaimed change, leave the
    `[#id]` mention -- or a whole open row -- unstaged or untracked beside it, and the tree
    supplies an edge for a claim the commit does not carry. Terra pre-merge review found it.

    THE FIX REFUSES THE SKEW RATHER THAN REBUILDING THE GRAPH FROM THE INDEX, and the choice
    is a design one rather than a shortcut. The store is a TREE artifact -- one build per
    commit, shared by three queries and every other reader -- so an index-shaped graph would
    be a second graph with a second lifetime, which ADR-118's "one graph" rules out and no
    ruling licenses here. So coverage is accepted only when every file the claim rests on is
    what the commit will actually write. In the hook path this costs nothing: pre-commit
    stashes unstaged changes, so the tracked-unstaged set is empty by the time this runs, and
    the untracked leg is exactly the hole -- a new row that is going to be committed has been
    `git add`ed, so an UNTRACKED row is never legitimate evidence.
    """
    if staged is None and _merge_in_progress(repo_root):
        # A MERGE IS TRANSPORT, NOT AUTHORSHIP, and this carve-out has direct precedent in
        # this repo: `block_commit_on_main` carries exactly one, `MERGE_HEAD present =>
        # allow`, for the same reason. Without it the gate refuses a lane's SYNC MERGE
        # because main's own commits brought files this branch never wrote -- ten of them on
        # the first live merge, all filed on main by other lanes. Refusing them here would
        # ask this lane to claim, or to retire, work it has not assessed.
        return []
    paths = staged_paths(repo_root) if staged is None else staged
    skew = _worktree_skew(repo_root)
    findings: list[Finding] = []
    for relpath in paths:
        if _exempt(relpath):
            continue
        key = store.key_for_path(relpath)
        if key and key.startswith("task:"):
            # A ROW FILE IS ITS OWN CLAIM. `tasks/665-*.md` IS `[#665]`; asking it to be
            # named by an open row is asking it to name itself, and FPG-1 keys it on the
            # row's identity rather than its path precisely because the two are one thing.
            # Found by this gate firing on a real merge, which is where a predicate written
            # from the row's wording meets the tree's actual shape.
            continue
        edges = store.in_edges(key, COVERAGE_KINDS) if key else []
        if edges:
            unstaged = sorted(p for p in _evidence_paths(store, relpath, edges) if p in skew)
            if not unstaged:
                continue
            findings.append(Finding(
                subject=relpath,
                evidence=("the claim covering this file is in the WORKING TREE, not in the "
                          f"commit: {', '.join(unstaged)}. The graph is built from the tree "
                          "and the commit writes the index, so an unstaged or untracked "
                          "claim covers nothing. Stage it.")))
            continue
        findings.append(Finding(
            subject=relpath,
            evidence=("no `implements` edge from an OPEN row. Name this file in the row's "
                      "body, or name the row `[#id]` in this file -- either direction is "
                      "the claim, and one of them is owed before the change lands.")))
    return findings


# --------------------------------------------------------------------- query 3: the process list


#: A process path named in prose. Bounded to the trees that hold executables, for the reason
#: `_SCRIPT_PATH_RE` is bounded in `file_purpose_graph`: a doc path in a sentence is not a
#: process reference and must not be read as a dangling one.
_PROSE_PROCESS_RE = re.compile(r"(?:scripts|plugins)/[A-Za-z0-9_./-]+\.(?:py|ps1)")
#: The surface `ARCHITECTURE.md` Ch2 is rendered from. Rendering it is a DIFFERENT lane --
#: `[#664]`'s frozen contract pins ARCHITECTURE.md prose out of this one -- so this module
#: arms the refusal and PRODUCES the body, and does not rewrite the file.
PROSE_SURFACE = "ARCHITECTURE.md"


def process_list(repo_root: Path | str, store: gs.GraphStore) -> list[ProcessRow]:
    """The traversal that answers "all processes", with WHY each one runs.

    This is the query `[#664]` says the repo did not have: *"so 'list all processes' is
    answered by re-reading the repo."* It is answered here by reading the store.
    """
    del repo_root
    reached = store.reachable(store.roots(), TRIGGER_KINDS)
    rows: list[ProcessRow] = []
    for node in store.processes():
        triggered = node.key in reached
        rows.append(ProcessRow(
            path=node.path,
            process_class=node.process_class,
            triggered=triggered,
            trigger=store.trigger_of(node.key) if triggered else "",
            disposition=ORPHAN_DISPOSITIONS.get(node.path)))
    return rows


def dangling_references(repo_root: Path | str, store: gs.GraphStore) -> list[Finding]:
    """REFUSE on prose naming a process the graph does not hold -- a `dangling_reference`.

    `[#664]`: *"prose naming a process the graph lacks becomes a `dangling_reference`."* The
    graph holds every in-tree process file, so a prose path the graph lacks is a path that
    does not exist -- a stale locator in the document that is supposed to be the structural
    model, which is the worst place in this repo for one.
    """
    root = Path(repo_root)
    surface = root / PROSE_SURFACE
    if not surface.is_file():
        return []
    try:
        text = surface.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):  # pragma: no cover -- unreadable canonical doc
        return []
    findings: list[Finding] = []
    for token in sorted(set(_PROSE_PROCESS_RE.findall(text))):
        if store.key_for_path(token) is None:
            findings.append(Finding(
                subject=token,
                evidence=(f"{PROSE_SURFACE} names this process and the graph does not hold "
                          f"it. Either the path is stale, or the file was removed and the "
                          f"prose was not.")))
    return findings


def render_ch2(rows: list[ProcessRow]) -> str:
    """The Ch2 body, generated from the traversal rather than maintained by hand.

    PRODUCED, NOT LANDED. `[#664]`'s contract pins `ARCHITECTURE.md` prose out of this lane
    ("Ch2 is RENDERED by this lane's mechanism; the hand rewrite is step D of the recovery
    plan and a different lane"), so this returns the text and writes nothing. Flat bullets,
    no column padding -- CLAUDE.md output-formatting.
    """
    lines = ["## Processes -- generated from FPG-1 (`graph_queries.py process-list --render`)",
             ""]
    for klass in ("script", "command", "skill"):
        members = [row for row in rows if row.process_class == klass]
        armed = [row for row in members if row.triggered]
        lines.append(f"### {klass} ({len(armed)} triggered of {len(members)})")
        lines.append("")
        for row in members:
            if row.triggered:
                lines.append(f"- `{row.path}` -- triggered by `{row.trigger}`")
            else:
                reason = row.disposition.reason if row.disposition else "UNDISPOSITIONED"
                owner = row.disposition.owner if row.disposition else "-"
                lines.append(f"- `{row.path}` -- no trigger; {reason} [owner: {owner}]")
        lines.append("")
    return "\n".join(lines)


# ------------------------------------------------- query 4: the five-kind edge class, RATCHETED
#
# WHAT THIS REFUSES, AND WHAT IT DELIBERATELY DOES NOT. `[#664]`'s Done-when asks that the
# corpus-structure edge computations be re-measured under DECLARE-REVIEWS section A.1's
# five-kind class -- citation, generation, template, test, script call-site, as narrowed on
# main by `ff103444` -- and driven to 0, every organ holding one reading FPG-1 instead. Lane
# `v-664` re-measured them (section 2.5: N-before 18, N-after 18, migrated 0) and nothing has
# held the line since, which is the state this query ends.
#
# **It is a RATCHET, not a bar, and that is a ruling rather than a shortfall.** ADR-118
# section 5 rules the migration one organ per lane ("twelve lanes is the cost of having
# twelve proofs") and rejects the big bang by name. A gate refusing all eighteen would refuse
# every commit in the repo on a defect no single committer can legally repair -- the
# unbounded-refusal shape `decision_coverage.ARM_DATE` already exists to avoid. So the set may
# SHRINK and may not GROW: a module that newly acquires the shape and carries no verdict
# refuses, and an already-shaped module is admitted until its migration lane reaches it.
#
# THE MEASUREMENT IS THE REGISTER, and the register is not a view. `EDGE_COMPUTATIONS` is the
# second curated manifest in this module, declared as an exception the same way
# `ORPHAN_DISPOSITIONS` is: a verdict of "this module computes a corpus-structure edge
# privately" is a RULING about a module's design, which no graph holds and none should. What
# the query computes mechanically is only the SHAPE -- a property of one module's source, not
# a relation between two corpus files -- so nothing here re-derives an edge FPG-1 already
# answers, which is `[#664]`'s first anti-pattern.

#: DECLARE-REVIEWS section A.1's class, CLOSED. A sixth kind is a widening of that section
#: and therefore a ruling, not a register row.
FIVE_KINDS = ("citation", "generation", "template", "test", "script call-site")

#: Where the population lives. `plugins/` is deliberately OUT: it holds derived copies whose
#: sources are in `scripts/` and are verdicted there, so scanning both would refuse a copy
#: for its source's shape (`ecosystem/derived-copies.yaml` owns the pair).
EDGE_SCAN_PREFIX = "scripts/"

#: The three mechanical signals the shape predicate reads. SCAN or READ says the module
#: reaches corpus files; EXTRACT says it pulls structure out of what it finds. Neither half
#: alone is an edge computation -- walking a tree to sum file sizes is not, and two regexes
#: over an argument string are not.
_SCAN_CALLS = frozenset({"rglob", "glob", "iterdir", "walk"})
_READ_CALLS = frozenset({"read_text", "readlines", "read_bytes"})
_RE_CALLS = frozenset({"compile", "search", "match", "fullmatch", "findall", "finditer",
                       "sub", "split"})
_AST_CALLS = frozenset({"parse", "walk", "iter_child_nodes"})
#: Two, because one regex is how a module parses its own argument; two is how it reads a
#: corpus. Calibrated against the register: all twenty register files clear it.
_MIN_REGEXES = 2


#: The status a row carries. `private` computes the relation itself; `reconciled` is FPG-1
#: input rather than FPG-1's rival; `not-an-edge` is the verdict that the SHAPE matched and
#: the module is nonetheless not of this class.
#:
#: THE REGISTER MUST BE ABLE TO SAY NO, and this status is why. The shape predicate favours
#: recall (its docstring says so), so it will keep finding modules that read source text for
#: something other than corpus structure. Without a negative verdict the only way to admit
#: one would be a false `private` row -- which would inflate N, hand a W-G3 lane a migration
#: that does not exist, and make the one number this query reports a lie. Found by the gate
#: refusing the very commit that armed it: `graph_queries.py` grew an `ast` walk in this
#: change, and its subject is a MODULE'S SHAPE, never a relation between two corpus files.
REGISTER_STATUSES = ("private", "reconciled", "not-an-edge")
#: What `kind` a `not-an-edge` row carries -- outside `FIVE_KINDS` by construction, because
#: the row's whole content is that no kind applies.
NO_KIND = "none"


@dataclass(frozen=True)
class EdgeComputation:
    """One verdicted site of the five-kind class, and who owes its migration.

    `status` is one of `REGISTER_STATUSES`. `migrated` is the movement of `reconciled` over
    time, which is what makes it a count rather than a claim.
    """
    kind: str
    status: str
    owner: str
    note: str = ""


_W_G3 = ("a W-G3 migration lane (ADR-118 section 5 -- one organ per lane, each proving its "
         "edge set is a subset of FPG-1)")


def _private(kind: str, note: str = "") -> EdgeComputation:
    return EdgeComputation(kind=kind, status="private", owner=_W_G3, note=note)


def _reconciled(kind: str, note: str) -> EdgeComputation:
    return EdgeComputation(kind=kind, status="reconciled",
                           owner="none -- the graph consumes it", note=note)


def _not_an_edge(note: str) -> EdgeComputation:
    return EdgeComputation(kind=NO_KIND, status="not-an-edge",
                           owner="none -- verdicted out of the class", note=note)


#: The measurement every verdict below cites, so the next seat re-derives a row rather than
#: trusting it. Section 3 is the private population with each site's blocker (`D` absent
#: target, `T` other tree or ref, `C` consumer repo, `G` sub-file granularity); section 4 the
#: re-verdicts of registered rows; section 5 the not-an-edge population, one reason each.
_CENSUS = "docs/audits/2026-09-17-census-lane-ab-664-edge-class-remeasure.md"


def _measured(section: str, reason: str) -> str:
    return f"{_CENSUS} section {section}: {reason}"


#: The verdicted sites. First carried from lane `v-664`'s section 2.5 table; RE-MEASURED by
#: lane `ab-664-spine-witnessed` over all 65 shape-matching modules and applied by operator
#: ruling 2026-09-17 (class (a)), on the condition that every re-verdicted row cites the
#: measurement behind it. Some rows are FUNCTIONS rather than modules (`<path>::<symbol>`):
#: `audit.py` computes in more than one check, and collapsing them to one file row would
#: hide one migration behind the other.
#:
#: A `D` blocker is not a migration waiting on effort. By the same ruling, a private site
#: whose refusal IS an absent target owes a measured, dispositioned dangling edge, and FPG-1
#: representing that edge at all is `[#839]`.
EDGE_COMPUTATIONS: dict[str, EdgeComputation] = {
    # ---- reconciled: already FPG-1 inputs, so the graph consumes them rather than rivals them
    "scripts/consumer_at_landing.py": _reconciled("citation", "FPG-1 input 3"),
    "scripts/validate_doc_code_edge.py": _reconciled("citation", "FPG-1 input 1"),
    "scripts/gen_audit_index.py": _reconciled("citation", "its output is FPG-1 input 2"),
    # BORN reconciled, never private -- so it is excluded from `migrated` (`BORN_RECONCILED`).
    "scripts/decision_coverage.py": _reconciled("citation", _measured(
        "4", "reads FPG-1 input 8 via store.in_edges; the shape came from its date regexes")),
    # MIGRATED by lane `ab-664-spine-witnessed` (W-G3 migration 1). Was `scripts/batch_manifest.py`
    # private citation; the parser is now split per linking surface and FPG-1 input 3 imports
    # it, so every manifest link is a `consumed-by` edge FROM the file that wrote it. Diff = 0
    # on the fixture and on the live tree but for named self-links, which the graph drops by
    # construction (`tests/test_graph_migrations.py`).
    "scripts/batch_manifest.py::manifest_link_surfaces": _reconciled(
        "citation", "FPG-1 input 3, manifest-link route"),
    # ---- private: citation (census section 3; blocker in the note)
    "scripts/validate_reconciliation.py": _private("citation", _measured(
        "3", "blocker none, S -- the next ruling-free migration")),
    "scripts/scan_undeclared_edges.py": _private("citation", _measured("3", "blocker G (tier 3)")),
    "scripts/funnel_coverage.py": _private("citation", _measured("3", "blocker D")),
    "scripts/funnel_lifecycle.py": _private("citation", _measured("3", "blocker D (leg c)")),
    "scripts/verify_handoff_probes.py": _private("citation", _measured("3", "blockers D T")),
    "scripts/preflight_contract.py": _private("citation", _measured("3", "blockers D T")),
    # KIND CORRECTED from `script call-site` (census section 4): a CLAUDE.md `@include` is
    # file-names-file, and the earlier "overlap with `imports`" note was false.
    "scripts/audit.py::check_import_edges": _private("citation", _measured(
        "3/4", "blockers D C; kind corrected from script call-site")),
    # MEASURED IN -- sites the register never saw (census section 3, `UNREGISTERED`).
    "scripts/audit.py::check_preflight_backlog_ids": _private("citation", _measured(
        "3", "measured in; blocker D")),
    "scripts/audit_checks/check_floor_integrity.py": _private("citation", _measured(
        "3", "measured in; blockers D C")),
    "scripts/governance_health.py": _private("citation", _measured(
        "3", "measured in; blocker G")),
    "scripts/propose_closures.py::find_weak": _private("citation", _measured(
        "3", "measured in, the WEAK leg; blockers C D")),
    "scripts/gen_dashboard.py::carrier_ids_for": _private("citation", _measured(
        "3", "measured in, borderline, the intake-mention leg; blocker none, S")),
    "scripts/fleet_analytics.py::inbound_reference_counts": _private("citation", _measured(
        "3", "measured in, borderline; blocker T")),
    # ---- private: script call-site
    "scripts/codemap/ast_walker.py": _private("script call-site", _measured(
        "3", "blocker C; closest overlap with FPG-1's `imports`")),
    "scripts/reverse_dep_oracle.py": _private("script call-site", _measured(
        "3", "blockers T G")),
    "scripts/safe_remove.py::_bare_stem_literal_hits": _private("script call-site", _measured(
        "3", "measured in; no structural blocker, but recall-heavy by design, so moving its "
             "grammar into FPG-1 `imports` would mint false edges the orphan census trusts")),
    # ---- not-an-edge: MEASURED OUT of the class (census section 4). Four clear, four on a
    # lean; each was a registered private row.
    "scripts/validate_doc_rot.py": _not_an_edge(_measured(
        "4", "was private citation; date tokens are blanked, no target resolved; every arm "
             "a one-file property")),
    "scripts/dispatch_drift.py": _not_an_edge(_measured(
        "4", "was private call-site; targets are host PowerShell commands (machine), leg 2 "
             "single-file state")),
    "scripts/proof_layer.py": _not_an_edge(_measured(
        "4", "was private test; extracts skipif-probed TOOLS (environment), never test -> "
             "script")),
    "scripts/gen_handoff.py": _not_an_edge(_measured(
        "4", "was private template; template -> bundle is the generator's own hard-coded "
             "authoring; other legs off-tree transport")),
    "scripts/audit.py::check_doc_claims": _not_an_edge(_measured(
        "4", "was private citation, lean; 3 of 4 claims are counts, the 4th is hook-id set "
             "parity and a hook id is not a corpus file")),
    "scripts/enforcement_coverage.py": _not_an_edge(_measured(
        "4", "was private call-site, lean; reads CONSUMER repos' wiring and proves firing by "
             "execution; the hub leg is n/a")),
    "scripts/generate_organ_index.py": _not_an_edge(_measured(
        "4", "was private call-site, lean; an existence inventory, one leg names a script by "
             "unresolved basename")),
    "scripts/archive_row_body.py": _not_an_edge(_measured(
        "4", "was private citation, lean; WRITES the row<->record relation, verify is byte "
             "parity, FPG-1 `archives` already holds live pairs")),
    "scripts/file_purpose_graph.py": _not_an_edge(_measured(
        "4", "it IS FPG-1; the graph cannot owe a migration onto itself")),
    # ---- not-an-edge: the previously UNVERDICTED population (census section 5, one line each)
    **{f"scripts/{module}.py": _not_an_edge(_measured("5", reason)) for module, reason in (
        ("assemble_paste", "writes PASTE_THIS from a fixed manifest (borderline generation, "
                           "program-authored)"),
        ("audit_checks/check_amendment_coherence",
         "declared coupled-surface version agreement"),
        ("audit_checks/check_handoff_version_stamp", "declared file list, value agreement"),
        ("audit_checks/check_substrate_declaration",
         "adapter; naming-grammar date; delegates to validate_substrate"),
        ("check_derived_copies", "declared derived-copies.yaml + byte parity + staged set"),
        ("check_provider_registry", "registry value agreement at hard-coded sites"),
        ("coherence_enumerator",
         "intra-document line sites; the pair relation is validate_reconciliation's"),
        ("dispatch_conformance", "writer vs an external verb's dry-run output"),
        ("dispatch_surface", "value agreement at declared sites + enum checks"),
        ("export_backlog_view", "renders task files to a view; resolves nothing"),
        ("fleet_health", "state files, dates, proposal log vs open ids (machine log)"),
        ("fleet_parity", "consumer repos' wiring (other trees) against a declared manifest"),
        ("gen_claude_rosters", "inventory of command frontmatter and ADR headers"),
        ("gen_lane_contract", "contract shape rendering"),
        ("gen_methodology_roster", "declared manifest read back"),
        ("gen_seat_boot", "template fill from PLAYBOOK Ch8 tokens, program-authored "
                          "(borderline template)"),
        ("gen_task_tree", "the generator of the view; declared clauses FPG-1 already loads"),
        ("generate_floor", "template render + F5 blacklist"),
        ("journal_anchor", "JOURNAL -> commit SHA is git history"),
        ("normalize_headers", "one file's heading format"),
        ("review_closures", "machine-written PROPOSALS register + state"),
        ("routing_agreement", "declared-copy parity with L0 + transcripts (machine)"),
        ("seat_refusals", "footprints in off-tree contracts; declared intent (borderline)"),
        ("session_end_backpressure", "four state gates"),
        ("toc/generator", "self-loop inside PLAYBOOK.md (borderline generation)"),
        ("validate_adr_status", "status grammar + index/header parity"),
        ("validate_backlog", "declared-clause existence (borderline; FPG-1 loads both "
                             "clauses)"),
        ("validate_doc_claims", "see audit.py::check_doc_claims"),
        ("validate_doc_structure", "intra-file numbering and TOC anchors"),
        ("validate_landing_predicate", "hand-declared `landed:` sites read back"),
        ("validate_residual_completeness", "unfilled regions + staged set"),
        ("validate_substrate", "contract text shape, declared write-scope"),
    )},
    # ---- not-an-edge: verdicted before the re-measure, each with its own reason
    "scripts/graph_queries.py": _not_an_edge(
        "this module. It grew an `ast` walk arming this very query, and the gate refused the "
        "commit that armed it -- the first thing the ratchet caught was itself. Its subject "
        "is a MODULE'S SHAPE (does this file read source text for structure), never a "
        "relation between two corpus files, so there is no edge here to read from FPG-1"),
    "scripts/provider_bench.py": _not_an_edge(
        "[#785]'s provider benchmark. Every text it extracts from is VENDOR OUTPUT -- a CLI's "
        "captured stdout, a `--usage-output-file` JSON, an agy session log under ~/.gemini -- "
        "and not one of them is a file of this corpus. The relations it discovers are "
        "`(provider, outcome) -> verdict` and `(run) -> served model`, which are properties "
        "of a paid network call and exist nowhere in FPG-1 to be read from. This is the "
        "recall-over-precision cost the shape predicate's own docstring predicts: it reads "
        "text and compiles regexes, so it matches, and the register saying NO is the "
        "designed outcome rather than a waiver"),
    "scripts/quality_requirements.py": _not_an_edge(
        "the quality-requirements register's reader ([#765], AN2-1). The shape matched "
        "because it compiles two regexes and reads files; the class does not apply because "
        "it COMPUTES no relation. `organ:` and `trip_test:` are written BY HAND in "
        "`ecosystem/quality-requirements.yaml`, and this module only resolves each declared "
        "side to a path that exists -- a DECLARED relation read back, which is what the "
        "three `reconciled` rows are one step earlier. There is nothing here for a W-G3 "
        "lane to migrate because nothing was discovered. Its two regexes match an `id` and "
        "a `file::test` locator INSIDE the register, never corpus source text"),
    "scripts/substrate_provenance.py": _not_an_edge(
        "L1's provenance marker ([#554], lane aa-1). The shape matched for the reason the "
        "predicate's own docstring predicts -- it reads files and compiles two regexes -- and "
        "the class does not apply because its subject is a MACHINE, not this corpus. The two "
        "texts it reads are `pyproject.toml`'s single-source uv pin and its own JSON marker "
        "outside the working tree; the facts it extracts are `uv --version`, the live "
        "interpreter, which tools resolve on PATH, and a git head. None of those is a "
        "relation between two corpus files, so there is nothing here for FPG-1 to hold and "
        "nothing for a W-G3 lane to migrate. The one repo relation it could have invented -- "
        "which files provisioning calls -- it deliberately does NOT compute: that is FPG-1's "
        "`triggers` input, and `safe_remove.wiring_referrers` consumes it from there"),
    "scripts/validate_hermetization.py": _not_an_edge(
        "the ADR-101 tree-seal gate. The shape matched when it grew its second `re` call -- the "
        "`logs/YYYY-MM` month-bucket grammar that admits the home `logs_retention.plan_moves` "
        "writes (operator ruling 2026-09-16, [#785]) -- beside the audit-name grammar it "
        "compiles from `fleet-shape-spec.yaml`, and it reads that YAML plus the lane "
        "declaration. The class does not apply because both regexes match ONE PATH SEGMENT "
        "against a naming grammar: whether a single name is an admitted home or audit name. "
        "Neither is a relation between two corpus files, so there is no edge for FPG-1 to hold "
        "and nothing for a W-G3 lane to migrate"),
    "scripts/conductor.py": _not_an_edge(
        "[#802]'s suite-baseline gate. The shape matched when it grew its regex trio reading "
        "`logs/SUITE-BASELINE-FREEZE.md` -- `parse_suite_baseline` extracts a roster of pytest "
        "NODE IDS a human wrote by hand into that file at freeze time. The class does not apply "
        "for the same reason as quality_requirements.py above: it is a DECLARED relation read "
        "back, not one discovered by scanning the corpus -- the roster is curated prose, not "
        "inferred structure. It is also not FPG-1-representable even in principle: a node id is "
        "sub-file granularity, and a parametrize id can embed spaces and quotes no graph path "
        "could hold (the batch-Z close-packet's 'Defect three' finding is exactly that "
        "fragility). There is no relation here for a W-G3 lane to migrate, because FPG-1 has "
        "nowhere to hold what was extracted"),
}


def _shape_signals(source: str) -> tuple[int, int, int, int]:
    """`(scans, reads, regexes, ast_calls)` over one module's source.

    AST rather than a text grep, for the reason the orphan census learned the hard way: a
    call string in a comment or a docstring is not an executable position, and a predicate
    that cannot tell the difference manufactures its own evidence.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return (0, 0, 0, 0)
    scans = reads = regexes = ast_calls = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        attr, base = node.func.attr, node.func.value
        named = base.id if isinstance(base, ast.Name) else None
        if attr in _SCAN_CALLS and named != "ast":
            scans += 1
        if attr in _READ_CALLS:
            reads += 1
        if attr in _RE_CALLS and named == "re":
            regexes += 1
        if attr in _AST_CALLS and named == "ast":
            ast_calls += 1
    return (scans, reads, regexes, ast_calls)


def is_edge_computation_shape(source: str) -> bool:
    """Does this module DISCOVER a corpus-structure relation by reading source text?

    EXTRACT and (SCAN or READ). Extraction is two or more `re` calls, or any `ast` parse --
    and `ast` is first-class here for a reason worth recording: the predicate lane `v-664`
    STATED for its section 2.5 table ("a module that walks the tree and compiles two or more
    regexes") does not reproduce that table. Four of its twenty-one rows fail it --
    `validate_doc_rot.py` and `dispatch_drift.py` walk no tree, `codemap/ast_walker.py` and
    `reverse_dep_oracle.py` compile no regex at all -- so inheriting the stated predicate
    would have armed a gate over a different population from the one the register records.

    RECALL OVER PRECISION, deliberately. A false positive costs one verdict row in the
    register, which is cheap and informative; a false negative is a private edge computation
    that lands unseen, which is the thing the ratchet exists to stop.
    """
    scans, reads, regexes, ast_calls = _shape_signals(source)
    extracts = regexes >= _MIN_REGEXES or ast_calls >= 1
    return extracts and (scans >= 1 or reads >= 1)


def _register_file(key: str) -> str:
    return key.split("::", 1)[0]


def _defines_symbol(source: str, symbol: str) -> bool:
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):  # pragma: no cover -- unparseable registered module
        return False
    return any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
               and node.name == symbol
               for node in ast.walk(tree))


def stale_edge_computations(repo_root: Path | str,
                            register: dict[str, EdgeComputation] | None = None
                            ) -> list[Finding]:
    """REFUSE on a register row naming a file, or a symbol, that is gone.

    WHY THIS BLOCKS WHERE `stale_dispositions()` ONLY NOTES, since the two registers sit in
    one module and the difference will otherwise read as an inconsistency. A stale ORPHAN
    disposition is harmless on its own terms: the file is gone, so the orphan is gone, and
    refusing the commit would punish the deletion. A stale EDGE-COMPUTATION row is not -- it
    is a migration obligation leaving the register silently, which moves N without anyone
    ruling that it moved. The repair is one line in the same commit that removed the file.
    """
    rows = EDGE_COMPUTATIONS if register is None else register
    root = Path(repo_root)
    findings: list[Finding] = []
    for key in sorted(rows):
        path = root / _register_file(key)
        if not path.is_file():
            findings.append(Finding(
                subject=key,
                evidence=("registered as a five-kind edge computation and the file is gone. "
                          "Remove the row in the commit that removed the file -- a register "
                          "row outliving its subject is a paper suppression, and it moves N "
                          "without a ruling")))
            continue
        if "::" not in key:
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):  # pragma: no cover -- unreadable module
            continue
        symbol = key.split("::", 1)[1]
        if not _defines_symbol(source, symbol):
            findings.append(Finding(
                subject=key,
                evidence=(f"registered at `{symbol}` and {_register_file(key)} no longer "
                          f"defines it. Re-point the row or remove it -- a row pinned to a "
                          f"symbol that was renamed suppresses silently")))
    return findings


def _head_source(repo_root: Path | str, relpath: str) -> str | None:
    """The module's bytes at `HEAD`, or None when the commit ADDS it.

    The second half of the ratchet. Comparing the staged shape against the HEAD shape is what
    separates "this module newly computes edges" from "this module always did and owes a
    migration lane" -- and an add-only reading would miss every module that GROWS the shape,
    which is the likelier of the two.
    """
    try:
        out = subprocess.run(["git", "show", f"HEAD:{relpath}"], cwd=repo_root,
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
        return None
    return out.stdout if out.returncode == 0 else None


def edge_class_census(repo_root: Path | str, store: gs.GraphStore,
                      staged: list[str] | None = None,
                      register: dict[str, EdgeComputation] | None = None) -> list[Finding]:
    """REFUSE on a NEW private edge computation, or on a register row that has rotted.

    Two legs, and the narrow one is first because it is the one that fires on an ordinary
    commit. A GATE THAT CONSULTS A REGISTER, not a view, and it says so: the staged set is
    commit-time state (the same carve-out `task_coverage` documents), the HEAD comparison is
    a second tree, and the verdict is a curated ruling. Calling this a query over FPG-1 would
    be the mis-filing DECLARE-REVIEWS section A.1 correction 2 exists to prevent.

    `store` is accepted and unused on purpose -- every refusal in this module takes the same
    signature so the CLI dispatches uniformly, and a leg that later needs the graph (the
    `imports` overlap two rows already name) does not change its callers to get it.
    """
    del store
    rows = EDGE_COMPUTATIONS if register is None else register
    root = Path(repo_root)
    findings = stale_edge_computations(root, rows)

    if staged is None:
        if _merge_in_progress(root):
            # A MERGE IS TRANSPORT, NOT AUTHORSHIP -- `task_coverage`'s carve-out, bound the
            # same way to the git-derived set only, so an explicit `staged=` is still checked.
            return findings
        staged = staged_paths(root)

    for relpath in staged:
        if not relpath.startswith(EDGE_SCAN_PREFIX) or not relpath.endswith(".py"):
            continue
        if any(_register_file(key) == relpath for key in rows):
            continue
        path = root / relpath
        if not path.is_file():
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):  # pragma: no cover -- unreadable staged file
            continue
        if not is_edge_computation_shape(source):
            continue
        before = _head_source(root, relpath)
        if before is not None and is_edge_computation_shape(before):
            continue  # already in the population; its migration lane owns it, not this commit
        findings.append(Finding(
            subject=relpath,
            evidence=("computes a corpus-structure relation of the five-kind class by "
                      "scanning source text, and no row of EDGE_COMPUTATIONS verdicts it. "
                      "Read the relation from FPG-1 instead (`scripts/graph_store.py`, or "
                      "`file_purpose_graph.py why`); or, if it genuinely cannot, add a row "
                      "naming its kind and its owner so the eighteen that already owe a "
                      "migration do not quietly become nineteen")))
    return findings


#: The three rows already reconciled when the register was written, so `migrated` counts
#: MOVEMENT rather than restating the arm-time state as progress.
ARM_TIME_RECONCILED = 3
#: Rows that were FPG-1 readers from their first commit and were only verdicted later. They
#: are `reconciled`, but no lane moved them, so counting them as `migrated` would report
#: progress nobody made.
BORN_RECONCILED = frozenset({"scripts/decision_coverage.py"})


def edge_class_metrics(repo_root: Path | str | None = None,
                       register: dict[str, EdgeComputation] | None = None) -> dict[str, int]:
    """`private` / `reconciled` / `migrated` / `not_an_edge`, so N is reported on every run.

    `migrated` is `reconciled` minus the three that were already FPG-1 inputs when the
    register was written -- the count a W-G3 lane moves, and the one number that says whether
    ADR-118 section 5 is progressing rather than merely declared. `not_an_edge` is reported
    beside them rather than hidden: a negative verdict that nobody can see is indistinguishable
    from a predicate that was quietly narrowed.
    """
    del repo_root
    rows = EDGE_COMPUTATIONS if register is None else register
    counted = {status: sum(1 for row in rows.values() if row.status == status)
               for status in REGISTER_STATUSES}
    born = sum(1 for key, row in rows.items()
               if key in BORN_RECONCILED and row.status == "reconciled")
    return {"private": counted["private"], "reconciled": counted["reconciled"],
            "not_an_edge": counted["not-an-edge"],
            "migrated": max(counted["reconciled"] - ARM_TIME_RECONCILED - born, 0)}


# ----------------------------------------------------------------- query 5: organ moments
#
# lane-l3-organ-truth. L1 declared WHICH organ runs at WHICH moment (`ecosystem/harness.yaml`,
# `moments:` plus the spine's `stages:`), so "declared nowhere" is finally a computable
# predicate: an organ in the process roster that no declaration names. This is a READ of that
# declaration, never an amendment of it, and it is the one query here whose ground truth is a
# declaration file rather than the FPG-1 store -- the roster it walks is still the store's
# (`process_list`), so it is a join, not a rival walk of the tree.
#
# THE ROSTER IS NOT NARROWED TO PASS. Every process node counts, dispositioned orphans
# included: a disposition says "this absence of a TRIGGER was looked at", which is a different
# fact from "this organ is declared at a moment", and conflating them would make the query
# agree with the register instead of with the declaration.

MOMENTS_DECLARATION_REL = "ecosystem/harness.yaml"
MOMENT_DECLARED = "declared-at-moment"
MOMENT_OPTIONAL_UNBUILT = "declared-optional-unbuilt"
MOMENT_MISSING = "declared-missing"
MOMENT_NOWHERE = "declared-nowhere"
MOMENT_STATUSES = (MOMENT_DECLARED, MOMENT_OPTIONAL_UNBUILT, MOMENT_MISSING, MOMENT_NOWHERE)

#: The lane that owes each not-yet-built organ, from the wave-2 order
#: (`to-cc/WAVE2-ORDER-2026-09-20.md`) and each contract's "Files you own" clause. A declared
#: organ MAY carry its own `owner:` key, which wins; this table is the fallback for L1's
#: declaration, which carries none and is not this lane's to edit. An organ with neither is
#: still a FAIL -- it just cannot name who owes it, and says so.
OWING_LANE: dict[str, str] = {
    "scripts/worktree_occupancy.py": "lane-l2-dispatch-guards",
    "scripts/gates.py": "lane-l4-integrator-surface",
    "scripts/review_packet.py": "lane-l4-integrator-surface",
    "scripts/no_leftovers.py": "lane-l5-no-leftovers",
    "scripts/test_pairing.py": "lane-l6-test-pairing",
    "scripts/transport_report.py": "lane-l8-lane-end",
    "scripts/lane_digest.py": "lane-l8-lane-end",
}

#: A file an organ's command names. `-c` code is handled separately (an import, not a path).
_COMMAND_PATH_RE = re.compile(
    r"(?:scripts|\.claude/commands|\.claude/skills|plugins)/[\w./-]+\.(?:py|ps1|md)")
#: `import a, b as c` and `from a import x` -- the two ways a `-c` snippet reaches a script.
_COMMAND_IMPORT_RE = re.compile(r"(?:^|[;\s])(?:from\s+(\w+)\s+import\b|import\s+([\w\s,]+))")


class MomentsUnreadable(Exception):
    """The declaration could not be read. A caller REFUSES on it; a query that cannot see its
    ground truth must not report the empty answer (register ruling Z-G4)."""


@dataclass(frozen=True)
class DeclaredOrgan:
    """One organ (or spine stage) the declaration names, with the files its command runs."""
    moment: str
    organ: str
    paths: tuple[str, ...]
    primary: str | None
    optional: bool
    owner: str | None


@dataclass(frozen=True)
class MomentRow:
    """One roster process (or declared-but-unbuilt organ) with its declaration status."""
    path: str
    process_class: str
    status: str
    moment: str = ""
    organ: str = ""
    owing_lane: str | None = None
    wired_elsewhere: bool = False


def _snippet_scripts(code: str, root: Path) -> list[str]:
    """The `scripts/<module>.py` files a `-c` snippet imports.

    A module counts when its script EXISTS, or -- so an organ that is not built yet is still
    seen -- when it is not stdlib and the snippet puts `scripts` on the path. Existence is
    classified afterwards by the caller, never used to DROP a candidate here (terra HIGH).
    """
    out: list[str] = []
    on_scripts_path = "scripts" in code
    for from_mod, import_list in _COMMAND_IMPORT_RE.findall(code):
        modules = [from_mod] if from_mod else [
            part.split(" as ")[0].strip() for part in import_list.split(",")]
        for module in modules:
            module = module.split()[0] if module.split() else ""
            if not module:
                continue
            rel = f"scripts/{module}.py"
            if (root / rel).is_file() or (on_scripts_path and module not in sys.stdlib_module_names):
                out.append(rel)
    return out


def _command_paths(command: list, root: Path, organ_id: str) -> tuple[tuple[str, ...], str | None]:
    """`(every file the command runs, the primary one)` -- the primary is the first file the
    argv names, else the first module a `-c` snippet imports that exists as a script."""
    paths: list[str] = []
    imported: list[str] = []
    after_c = False
    for arg in (str(a) for a in command):
        if after_c:
            imported.extend(_snippet_scripts(arg, root))
            after_c = False
            continue
        after_c = arg == "-c"
        for match in _COMMAND_PATH_RE.findall(arg):
            paths.append(match)
    # A dotted organ id (`merge_receipt.models`) names its module by convention.
    head = organ_id.split(".")[0]
    if "." in organ_id and (root / f"scripts/{head}.py").is_file():
        imported.append(f"scripts/{head}.py")
    everything = tuple(dict.fromkeys(paths + imported))
    primary = paths[0] if paths else (imported[0] if imported else None)
    return everything, primary


def load_declaration(repo_root: Path | str) -> list[DeclaredOrgan]:
    """Every organ and spine stage `ecosystem/harness.yaml` declares. Raises `MomentsUnreadable`
    when the file is absent, unparseable or not the shape L1 wrote."""
    import yaml  # deferred: the read path of the other queries stays stdlib + sqlite

    root = Path(repo_root)
    path = root / MOMENTS_DECLARATION_REL
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise MomentsUnreadable(f"cannot read {MOMENTS_DECLARATION_REL}: {exc!r}") from exc
    if not isinstance(raw, dict):
        raise MomentsUnreadable(f"{MOMENTS_DECLARATION_REL} is not a mapping")
    declared: list[DeclaredOrgan] = []
    for stage in raw.get("stages") or []:
        if not isinstance(stage, dict):
            raise MomentsUnreadable(f"{MOMENTS_DECLARATION_REL}: a stage is not a mapping")
        if stage.get("command") is None:
            continue  # `command: null` is a stage that does not exist yet -- dodo.py names it
        if not isinstance(stage["command"], list):
            raise MomentsUnreadable(
                f"{MOMENTS_DECLARATION_REL}: stage {stage.get('stage')} command is not a list")
        name = str(stage.get("name") or stage.get("stage"))
        paths, primary = _command_paths(stage["command"], root, "")
        declared.append(DeclaredOrgan(f"spine stage {stage.get('stage')} ({name})", name,
                                      paths, primary, False, None))
    for moment in raw.get("moments") or []:
        if not isinstance(moment, dict) or not isinstance(moment.get("organs") or [], list):
            raise MomentsUnreadable(
                f"{MOMENTS_DECLARATION_REL}: a moment is not a mapping with an `organs` list")
        for organ in moment.get("organs") or []:
            if not isinstance(organ, dict) or not organ.get("id"):
                raise MomentsUnreadable(
                    f"{MOMENTS_DECLARATION_REL}: moment {moment.get('name')!r} carries an organ "
                    f"that is not a mapping with an `id`")
            command = organ.get("command")
            if command is not None and not isinstance(command, list):
                raise MomentsUnreadable(
                    f"{MOMENTS_DECLARATION_REL}: organ {organ['id']!r} command is not a list")
            paths, primary = _command_paths(command or [], root, str(organ["id"]))
            declared.append(DeclaredOrgan(
                str(moment.get("name")), str(organ["id"]), paths, primary,
                bool(organ.get("optional")), str(organ["owner"]) if organ.get("owner") else None))
    return declared


def roster_rows(repo_root: Path | str) -> list[ProcessRow]:
    """The process roster, from the persisted store, through the freshness check."""
    root = Path(repo_root).resolve()
    return process_list(root, gs.ensure(root, gs.store_path(root)))


def organ_moments(repo_root: Path | str, roster: list[ProcessRow] | None = None,
                  declaration: list[DeclaredOrgan] | None = None) -> list[MomentRow]:
    """For every organ in the process roster: declared at a moment, declared optional and not
    yet built, or declared nowhere -- plus the declared organs whose command is not on disk.

    `roster` and `declaration` are seams for a fixture tree; `None` reads the live ones.
    """
    root = Path(repo_root)
    declared = load_declaration(root) if declaration is None else declaration
    processes = roster_rows(root) if roster is None else roster
    by_path: dict[str, DeclaredOrgan] = {}
    for organ in declared:
        for rel in organ.paths:
            by_path.setdefault(rel, organ)

    rows: list[MomentRow] = []
    seen: set[str] = set()
    for proc in processes:
        seen.add(proc.path)
        organ = by_path.get(proc.path)
        if organ is None:
            rows.append(MomentRow(proc.path, proc.process_class, MOMENT_NOWHERE,
                                  wired_elsewhere=proc.triggered))
        else:
            rows.append(MomentRow(proc.path, proc.process_class, MOMENT_DECLARED,
                                  organ.moment, organ.organ, wired_elsewhere=proc.triggered))
    for organ in declared:
        if not organ.primary or organ.primary in seen or (root / organ.primary).exists():
            continue
        seen.add(organ.primary)
        owing = organ.owner or OWING_LANE.get(organ.primary)
        rows.append(MomentRow(
            organ.primary, "script",
            MOMENT_OPTIONAL_UNBUILT if organ.optional else MOMENT_MISSING,
            organ.moment, organ.organ, owing))
    return sorted(rows, key=lambda r: (MOMENT_STATUSES.index(r.status), r.path))


def unbuilt_evidence(row: MomentRow) -> str:
    """The sentence a refusal carries for a declared organ whose command does not exist."""
    owed = (f"owed by {row.owing_lane}" if row.owing_lane
            else "no owning lane is recorded for it")
    kind = "optional and not yet built" if row.status == MOMENT_OPTIONAL_UNBUILT else (
        "NOT optional and does not exist, so its moment will stop at it")
    return (f"organ `{row.organ}` at moment `{row.moment}` is declared {kind}: its command "
            f"`{row.path}` is absent -- {owed}.")


def moments_findings(rows: list[MomentRow]) -> list[Finding]:
    """The refusals: one per declared-nowhere organ, one per declared-but-unbuilt organ."""
    findings: list[Finding] = []
    for row in rows:
        if row.status == MOMENT_NOWHERE:
            findings.append(Finding(
                row.path, f"{row.process_class} is declared at no moment and no spine stage in "
                          f"{MOMENTS_DECLARATION_REL}. Declare it there (L1's file, by ruling) "
                          f"or retire it."))
        elif row.status in (MOMENT_OPTIONAL_UNBUILT, MOMENT_MISSING):
            findings.append(Finding(row.path, unbuilt_evidence(row)))
    return findings


def moments_summary(rows: list[MomentRow]) -> str:
    counts = {status: sum(1 for r in rows if r.status == status) for status in MOMENT_STATUSES}
    nowhere = [r for r in rows if r.status == MOMENT_NOWHERE]
    wired = sum(1 for r in nowhere if r.wired_elsewhere)
    return (f"moments: {len(rows)} organs -- {counts[MOMENT_DECLARED]} declared at a moment, "
            f"{counts[MOMENT_OPTIONAL_UNBUILT]} declared optional and unbuilt, "
            f"{counts[MOMENT_MISSING]} declared and missing, {counts[MOMENT_NOWHERE]} declared "
            f"nowhere ({wired} of those are wired by another surface, {len(nowhere) - wired} "
            f"by none)")


# --------------------------------------------------------------------------------------- CLI


def _open(args) -> gs.GraphStore:
    """The store these queries answer from -- ALWAYS through the freshness check.

    EXISTS IS NOT FRESH, and the earlier shape here confused the two: it opened any store
    that was on disk and only built one that was absent. Terra pre-merge review named what
    that costs -- every invocation after a source file changes outside the hook chain
    answers `orphan-census`, `task-coverage` and `process-list` from yesterday's graph, and
    a stale graph does not fail, it just answers wrongly. `ensure` is the whole contract in
    one call: fresh store, rebuild if stale, one rebuilder at a time.

    THE HOOK CHAIN PAYS AN mtime SWEEP PER QUERY FOR THIS, and that is the right trade to
    make: `graph-rebuild` runs first and leaves the store fresh, so the three query hooks
    each pay `is_stale` and none of them rebuilds. Buying that back with an
    `--assume-fresh` flag would reintroduce the hole with a switch on it.
    """
    root = Path(args.repo_root).resolve()
    path = Path(args.db) if args.db else gs.store_path(root)
    return gs.ensure(root, path)


def _report(name: str, findings: list[Finding]) -> int:
    if not findings:
        print(f"{name}: OK")
        return 0
    print(f"{name}: REFUSED -- {len(findings)} finding(s)")
    for finding in findings:
        print(f"  - {finding.subject}")
        print(f"    {finding.evidence}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The three commit-tier refusals over the persisted FPG-1 store.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=".", help="repo to read (default: cwd)")
    common.add_argument("--db", default=None, help="store path (default: under the git dir)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("orphan-census", parents=[common],
                   help="refuse on a process nothing triggers")
    coverage = sub.add_parser("task-coverage", parents=[common],
                              help="refuse on a staged file no OPEN row claims")
    coverage.add_argument("--staged", nargs="*", default=None,
                          help="paths to check (default: git diff --cached)")
    listing = sub.add_parser("process-list", parents=[common],
                             help="every process with its trigger; refuse on a dangling ref")
    listing.add_argument("--render", action="store_true",
                         help="emit the ARCHITECTURE.md Ch2 body (writes nothing)")
    edges = sub.add_parser("edge-class-census", parents=[common],
                           help="refuse on a NEW private five-kind edge computation")
    edges.add_argument("--staged", nargs="*", default=None,
                       help="paths to check (default: git diff --cached)")
    edges.add_argument("--empty-register", action="store_true",
                       help=("verdict nothing -- the fixture flag the trip-tests use to "
                             "exercise the ratchet leg against a tree that is not this repo"))
    sub.add_parser("moments", parents=[common],
                   help="every organ: declared at a moment, optional-unbuilt, or nowhere")

    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve()
    try:
        store = _open(args)
    except gs.StoreUnreadable as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1

    if args.command == "orphan-census":
        stale = stale_dispositions(root)
        if stale:
            # Surfaced, never blocking -- ADR-75's decoration rule. A stale disposition is a
            # fact about the register, and refusing a commit for it would punish the wrong act.
            print("orphan-census: NOTE -- dispositions naming files that are gone: "
                  + ", ".join(stale))
        return _report("orphan-census", orphan_census(root, store))

    if args.command == "task-coverage":
        return _report("task-coverage", task_coverage(root, store, args.staged))

    if args.command == "moments":
        try:
            rows = organ_moments(root, roster=process_list(root, store))
        except MomentsUnreadable as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
        print(moments_summary(rows))
        for row in rows:  # the answer, per organ -- the refusal below only counts them
            where = f"  [{row.moment} / {row.organ}]" if row.organ else ""
            owed = f"  (owed by {row.owing_lane})" if row.owing_lane else ""
            print(f"  {row.status:<26} {row.path}{where}{owed}")
        findings = moments_findings(rows)
        print(f"moments: {'REFUSED -- ' + str(len(findings)) + ' finding(s)' if findings else 'OK'}")
        return 1 if findings else 0

    if args.command == "edge-class-census":
        register = {} if args.empty_register else None
        metrics = edge_class_metrics(root, register)
        print(f"edge-class-census: {metrics['private']} private, "
              f"{metrics['reconciled']} reconciled, {metrics['migrated']} migrated, "
              f"{metrics['not_an_edge']} verdicted out of the class")
        return _report("edge-class-census",
                       edge_class_census(root, store, args.staged, register))

    rows = process_list(root, store)
    if args.render:
        print(render_ch2(rows))
    else:
        armed = sum(1 for row in rows if row.triggered)
        print(f"process-list: {len(rows)} processes, {armed} triggered, "
              f"{len(rows) - armed} not")
    return _report("process-list", dangling_references(root, store))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
