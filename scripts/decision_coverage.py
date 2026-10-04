#!/usr/bin/env python
"""decision_coverage.py -- a decided thing is never left unscheduled again ([#692], A9-1..A9-3).

WHAT THIS IS. The operator's rule of 2026-09-10, in code: *"A decision is safe only once it is
a row in the repo's backlog; a transport DECLARE/AMEND alone is SAID"* (STANDING_RULINGS AH-A1).
Every decision carries a LIFECYCLE STATE and either an implementing row or a written "no
implementation required" disposition; the refusal fires at commit tier and at onboarding, and it
LISTS the decisions and STATES WHAT MUST BE DONE -- *"a process deviation raises an exception
that teaches the browser"*, which is the half that makes it a teaching surface rather than a
tripwire.

EXISTS-BEFORE-BUILD (AX9-4), discharged before a line of this file was written and recorded in
`[#692]`'s row rather than asserted here. `graph_queries.py process-list` answers *"158
processes, 119 triggered, 39 not"* and no process node, and no `ecosystem/organ-index.md` row,
carries `decision` or `lifecycle` in a name or a trigger. The four nearest organs are enumerated
in `funnel_lifecycle`'s own docstring and not one of them asks this question: `funnel_coverage`
asks whether an AUDIT artifact was dispositioned, `consumer_at_landing` whether a landed audit
is CITED, `intake_tree_coherence` whether the intake index regenerates byte-identically, and
`funnel_lifecycle` itself whether a TERMINAL object's location still agrees with its status --
its leg a2 fires only where every named row is terminal, which is vacuously true over the empty
set and is exactly the population this organ is about. `validate_adr_status` reads the status
GRAMMAR and never asks what implements the ADR. So the resolvers here are BORROWED from those
four rather than rewritten, in the shape `funnel_lifecycle` established.

POPULATION FROM THE DOCUMENTS, RELATION FROM THE STORE -- and the split is the design, not a
compromise. FPG-1 mints an `adr:N` node only for an ADR something CITES, so a query that read
its population off the graph would be structurally blind to the uncited, unimplemented decision
this organ exists to find. The `implements` RELATION, by contrast, is corpus structure and comes
from the persisted store with no private recomputation -- intake #86's acceptance criterion 5,
and ADR-118 §1's rule that a new edge kind is added to FPG-1 (input 8, here) and never to a
script. DECLARE-REVIEWS §A.1 correction 2 already ruled this exact shape for `task_coverage`:
"a two-tree gate cannot be a view", so the join of a document-read population with a graph-read
relation is a GATE that consults a view, and it is filed as one.

THE ERA BOUND IS THIS LANE'S ONE DESIGN RULING, and it is stated loudly because an unstated
bound is an exemption. MEASURED on the live tree at build time: 84 ADRs carry `Accepted` and 20
intakes carry `ACCEPTED`, and none of them carries an `implements:` key, because the key did not
exist until this commit. A refusal over all 104 would refuse EVERY COMMIT IN THE REPO on a
defect the committer cannot legally repair -- the argument `audit.py` already settled when it
kept `check_funnel_lifecycle` at SHIP rather than COMMIT tier, and the same criterion
`verify_handoff_probes` applies to its own carriage rung ("the refusal has to land while the
bundle is still repairable"). So `ARM_DATE` bounds the REFUSAL and nothing else:

  * the LEDGER (A9-2) lists the whole population, era or not;
  * the METRIC (A9-3) counts the whole population, and its fourth number -- the age of the
    oldest accepted-but-unexecuted decision -- is precisely the instrument that keeps the
    grandfathered set from being forgotten. A bound that is not measured is an exemption;
  * only the REFUSALS are era-bounded, and `Metrics.grandfathered` states the size of what
    they decline to refuse on every run.

`consumer_at_landing.ARM_DATE` is the precedent, in terms: "the 290 historical orphans are
grandfathered, and the grandfathered count [is recorded]".

THE TRANSPORT CLASS COLLAPSES ONTO P11 RATHER THAN GROWING A RIVAL PREDICATE. A9-1 counts a
transport `DECLARE-`/`AMEND-` as a decision, and the repo already has a ratified answer to "did
this decision reach the tree": the `carried-by:` key and `gen_handoff.carriage_verdicts`. A
transport decision whose carrier RESOLVES ON `main` has landed as an in-repo object -- an ADR, an
intake, a row -- and that object is itself in this population with its own coverage question, so
the transport file is `done` and the question has MOVED rather than been dropped. One whose
carrier is `OPEN` or names no resolving home is undischarged, and is `accepted` unless a row
implements it directly. Measured 2026-09-11: 95 of 104 resolve, 7 carry no key, 2 are OPEN.
`BATCH-` is deliberately NOT in the population: A9-1 names two prefixes and a batch manifest is
a schedule, not a ruling.

WHAT THIS ORGAN DOES NOT SEE, stated rather than discovered later:
  * `protocols/STANDING_RULINGS.md` entries, in the THREE-CLASS query above. A9-1's population is
    three classes and the register is not among them; `[#721]` is the row that adds the fourth,
    at entry granularity, and it was filed beside `[#692]` precisely because `[#692]`'s Done-when
    carries A9-1 VERBATIM and cannot gain a class without ceasing to be verbatim. The fourth
    class is the `rulings` subcommand and the section "the ruling register leg" below (batch
    B2-W1, lane `b2-rulings-landing`, R79.3): it is a separate leg, not a fourth `Decision` kind,
    because a ruling's carrier is its own `Carried by:` line and not an `implements:` edge.
  * A transport decision when `CLAUDE_PROMPTS_DIR` is unresolved. That is reported as a DEGRADED
    class, never as an empty one -- DEFECT E-29's rule that an unknown boundary is not a clean
    one.
  * Whether an implementing row is the RIGHT row. Coverage is a structural claim; adequacy is a
    reviewer's judgement and no gate here pretends otherwise.

FLOOR: hub-only. One-line reason: the population includes the `CLAUDE_PROMPTS_DIR` transport and
the intake funnel's ACCEPTED tier, and no consumer repo carries either surface today; promotion
to MUST is owed the moment one does, and is `[#735]`'s to carry.

Usage:
    python scripts/decision_coverage.py check   [--repo-root .] [--db PATH] [--staged PATH ...]
    python scripts/decision_coverage.py ledger  [--repo-root .] [--db PATH]
    python scripts/decision_coverage.py metrics [--repo-root .] [--db PATH]
    python scripts/decision_coverage.py rulings [--repo-root .] [--no-transport]   # exit 1 = refused, 2 = leg (a) not measured
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

import file_purpose_graph as fpg  # noqa: E402
import graph_queries as gq  # noqa: E402
import graph_store as gs  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("decision-coverage")

#: The refusal shape is `graph_queries.Finding`, imported rather than redefined. One refusal
#: shape across the commit-tier organs is what lets the hook output read as one voice; a second
#: dataclass with the same two fields would be free to drift from it.
Finding = gq.Finding

#: On or after this date, an accepted decision with neither a row nor a disposition REFUSES.
#: Before it, it is counted and reported and never refuses. See the era-bound block above.
#: The date is this mechanism's own landing date -- the earliest day on which an author could
#: have known the `implements:` key existed.
ARM_DATE = _dt.date(2026, 9, 11)

# --------------------------------------------------------------------------- the vocabulary

KIND_ADR = "adr"
KIND_INTAKE = "intake"
KIND_TRANSPORT = "transport"

#: A9-1's lifecycle, verbatim: "considered -> accepted -> executing -> done | superseded".
#: `accepted` is the ACCEPTED-BUT-UNEXECUTED state and is the one the refusals fire on; a
#: decision that is being worked is `executing`, which is why the two are separate words.
STATE_CONSIDERED = "considered"
STATE_ACCEPTED = "accepted"
STATE_EXECUTING = "executing"
STATE_DONE = "done"
STATE_SUPERSEDED = "superseded"
LIFECYCLE: tuple[str, ...] = (STATE_CONSIDERED, STATE_ACCEPTED, STATE_EXECUTING, STATE_DONE,
                              STATE_SUPERSEDED)

#: The ADR status that puts a decision in the accepted population. `validate_adr_status`
#: owns the enum; this names the one member A9-1 selects.
ADR_ACCEPTED = "Accepted"
#: ADR statuses that have LEFT the lifecycle. Wider than
#: `validate_adr_status.TERMINAL_STATUSES`, which is the ARCHIVAL-eligibility set: "Explored,
#: not adopted" was never accepted and "Partially superseded" no longer wholly stands, and
#: neither can be asked for an implementing row. The difference is deliberate and is why this
#: set is named here rather than imported.
ADR_LEFT = frozenset({"Superseded", "Deprecated", "Partially superseded",
                      "Explored, not adopted"})
#: Intake statuses in the accepted population. A9-1 says "ACCEPTED/RATIFIED"; `RATIFIED` is
#: NOT a member of the live enum (`gen_intake_index._STATUS_ORDER`), so it is admitted here
#: and will simply never match until the enum grows it. Carried rather than silently dropped:
#: the clause is verbatim and this is the honest way to honour a token the enum lacks.
INTAKE_ACCEPTED = frozenset({"ACCEPTED", "RATIFIED"})
#: Intake statuses that have left the lifecycle. CONSUMED is `done` -- the doc's content
#: became rows and ADRs, which is what consumption means in `docs/intake/README.md` §5.
INTAKE_DONE = frozenset({"CONSUMED"})
INTAKE_LEFT = frozenset({"SUPERSEDED", "REJECTED"})

#: A9-1's two transport prefixes. `BATCH-` is in `gen_handoff.CARRIAGE_PREFIXES` and NOT here:
#: a batch manifest schedules lanes, it does not rule anything.
TRANSPORT_PREFIXES = ("DECLARE-", "AMEND-")

#: `**Date:** 2026-06-16` and `- **Date:** 2026-09-07` are BOTH live ADR grammars -- 58 of the
#: 84 accepted ADRs use one and the rest the other. One pattern for both; reading only the
#: flush-left form answered NO-DATE for 26 real ADRs when this was measured.
_ADR_DATE_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)
#: A `YYYY-MM-DD` prefix on a filename: `docs/intake/2026-09-10-tech-....md`, and the dated
#: half of the transport's naming (`DECLARE-cv-f2-2026-09-10.md`).
_FILENAME_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


@dataclass(frozen=True)
class Disposition:
    """A written "no implementation required", with who ruled it.

    Same shape and same discipline as `graph_queries.Disposition`: a disposition is NOT an
    exemption -- it records that the absence of a row has been LOOKED AT and ruled, and it
    names who can change that. ADR-75's decoration rule keeps it honest, and
    `stale_dispositions()` below surfaces a row naming a decision that is gone.
    """
    reason: str
    owner: str


@dataclass(frozen=True)
class Decision:
    """One decision, its lifecycle position, and what implements it."""
    key: str                       # `adr:118` | `intake:91` | `declare:AMEND-SESSION-PLAN-009`
    kind: str                      # KIND_ADR | KIND_INTAKE | KIND_TRANSPORT
    label: str                     # `ADR-118` | `intake #91` | `to-cc/AMEND-...md`
    status: str                    # the status token as written
    state: str                     # a member of LIFECYCLE
    date: _dt.date | None
    date_source: str               # "header" | "filename" | "mtime" | "absent"
    rows: tuple[str, ...]          # implementing row ids, open first
    open_rows: tuple[str, ...]
    locator: str                   # repo-relative path, or transport-relative for a transport
    disposition: Disposition | None = None

    @property
    def in_era(self) -> bool:
        """Whether a refusal may fire on this decision. A decision with NO computable date is
        NOT in the era: refusing on an unknown date would refuse on a guess."""
        return self.date is not None and self.date >= ARM_DATE


class PopulationUnreadable(RuntimeError):
    """A decision corpus this organ cannot read.

    A REFUSAL RATHER THAN AN EMPTY ANSWER, and the reason is `check_intake_tree_coherence`'s
    own ruling one level out: a coherence gate must not be satisfiable by deleting what it
    checks. An unreadable `docs/decisions/` is the one condition that must never render green.
    """


# ------------------------------------------------------------------ the disposition register
#
# A WRITTEN "no implementation required", one entry per decision, each with a reason and an
# owner. The register lives HERE for the same reason `graph_queries.ORPHAN_DISPOSITIONS` does
# -- footprint: `ecosystem/disposition-register.yaml` is not in this lane's write-scope, and a
# component whose declaration mechanism does not exist yet must not write into a registry a
# sweep reads. Relocating it there is an OWED follow-up, named in this lane's artifact rather
# than left to be discovered.
#
# IT WAS DELIBERATELY ALMOST EMPTY at first writing (one in-era decision, already ruled). Grown
# by LANE-5B3-4-decision-debt (2026-09-26) once P13's own onboarding rung named 40 accepted-and-
# undisposed in-era decisions -- measured live, not asserted: `decision_coverage.py ledger` at
# this lane's start. 13 of the 40 were resolved a different way first (their transport carrier
# turned out to have already landed; see `carrier_landed_check.py` and the lane's session file
# for the old/new `carried-by:` lines and shas), which moved them to `done` and off this
# register's population before a disposition was ever needed. The 24 entries below are the rest
# -- two GROUNDED classes, never invented:
#   * ADR-121..126 and every DRAFT/SEED intake here are Proposed/pre-triage. MEASURED pattern on
#     this tree: ADR-119 and ADR-120 (both Accepted) already carry implementing rows; no
#     Proposed ADR in this population does. Filing a row against an unratified ADR, or an
#     untriaged intake, would pre-empt the operator's own ratification / the funnel's own triage
#     (ADR-94; ADR-98; ADR-111) -- the disposition IS that reserved act, not yet performed.
#   * Two of the seven live `AMEND-BATCH-WAVE5B-N2-*` queue amendments (LANE8, QUEUE5) carry a
#     disposition -- each is FULLY settled, no gap and no still-executing lane, citing the
#     specific per-lane outcome the N2 close digest and the N3 batch manifest record for it.
#     CORRECTED TWICE: 2026-09-26 (Codex terra review round 2) from a first-draft blanket
#     "EXECUTED IN BATCH" reason that overclaimed uniform completion across all seven; then again
#     (round 3) once QUEUE, QUEUE4 and QUEUE6's own individually-reasoned round-2 text was found
#     to still overclaim -- each admitted a gap or a still-executing lane and got a whole-file
#     Disposition anyway, which the register's per-file granularity reads as wholly `done`. See
#     the comment above the register for the per-file grounding.
# The remaining 16 of the 40 have NEITHER grounding: no ratification/triage process governs them
# and no batch claims them as fully, honestly settled (QUEUE, QUEUE2, QUEUE3, QUEUE4 and QUEUE6 --
# each has at least one lane with no honest disposition, removed from this register across the
# round-2 and round-3 corrections). Those are `ROWS-OWED` lines in this lane's session file, per
# ruling (h) -- this lane files no rows.

#: The single reasoning ADR-121..126 and the pre-triage intakes below share, factored out so six
#: ADR entries and twelve intake entries do not restate it with room to drift.
_AWAITING_RATIFICATION = (
    "Proposed, awaiting the operator's ratification (ADR-94) -- one of the five reserved "
    "operator-only decisions (PLAYBOOK: GO / ratification / tag / destructive acts / seat "
    "release). MEASURED pattern on this tree, 2026-09-26: ADR-119 and ADR-120 (both Accepted) "
    "carry implementing rows; no Proposed ADR in this population carries one. Filing a row "
    "against a still-Proposed ADR would pre-empt the operator's own ruling on whether to adopt "
    "it at all.")
_AWAITING_TRIAGE = (
    "DRAFT or SEED, awaiting ADR-98's intake funnel (DRAFT -> ... -> CONSUMED) and ADR-111's "
    "decision funnel (OWNED / DISCHARGED / CANDIDATE / REJECTED). A row is filed once triage "
    "promotes the intake to CANDIDATE and a ruling accepts it -- filing one pre-emptively, "
    "before the funnel disposes the finding, would jump the process both ADRs exist to enforce.")
# CORRECTED 2026-09-26 (Codex terra review round 2, LANE-5B3-4-decision-debt, verified against
# ground truth rather than taken on faith): a first draft here used ONE blanket
# "EXECUTED IN BATCH WAVE5B-N2" reason for all 7 queue-amendment files, on the premise that the
# batch's close digest closing = its content executing. Direct comparison of each file's own
# appended-lane table against `to-browser/DIGEST-WAVE5B-N2-2026-09-26.md`'s per-lane outcomes
# (§2) and `to-cc/BATCH-WAVE5B-N3-2026-09-26.md`'s own lane table shows that is true for some
# files and false for others -- several lanes were HELD or NEVER-LAUNCHED in N2 with no
# continuing lane anywhere, which "executed" cannot honestly cover.
#
# CORRECTED AGAIN 2026-09-26 (Codex terra review round 3, on round 2's own fix): the register is
# keyed ONE ENTRY PER FILE, and `_state()` reads ANY `Disposition` on a key as the WHOLE decision
# being `done` -- there is no partial-disposition shape. Round 2's individually-reasoned QUEUE,
# QUEUE4 and QUEUE6 entries each said so themselves (lane 18, lane 24: "a genuine gap"; lane 31,
# lane 27: "EXECUTED / EXECUTING") and then registered a Disposition anyway, which silently reads
# those admitted gaps and admitted still-running lanes as `done` -- exactly the "decided and
# unscheduled" blindness `_state()`'s own comment (`AN OPEN ROW OUTRANKS A RESOLVING CARRIAGE`)
# exists to prevent, just reintroduced one layer up. Only a file whose FULL content is settled
# with no gap and no still-executing lane can honestly take a whole-file Disposition: LANE8 (one
# lane, MERGED, its one Optional item explicitly scoped out by the file's own text) and QUEUE5
# (both lanes REPORTED) qualify; QUEUE, QUEUE4 and QUEUE6 do not, and are now ROWS-OWED like
# QUEUE2/QUEUE3 -- their own per-lane narrative below states plainly which parts already have a
# citable home, but the FILE's own decision key stays undisposed since that mechanism has no way
# to say "the file is disposed except for this one lane."

# `declare:AMEND-CV-V10-001`'s disposition (OUT OF POPULATION, the batch X manifest's own
# scoping) was REMOVED here -- LANE-5B3-4-decision-debt, 2026-09-26 -- once
# `stale_dispositions` (correctly; see its own docstring) flagged it: no file named
# `AMEND-CV-V10-001*` exists anywhere on the live transport any more (checked directly, not
# inferred), pre-dating this lane's own edits -- this lane never touched, created or deleted
# any CV-V10 file. The disposition named a decision that is gone; removing it is maintaining
# the register, not writing a new one, and needs no ruling of its own -- the ruling it cited
# (the batch X manifest / AMEND-SESSION-PLAN-005 A5-1) already discharged by that decision's
# own disappearance from the corpus it was scoped out of.

DECISION_DISPOSITIONS: dict[str, Disposition] = {
    # -- ADR-121..126: Proposed, ratification pending (ADR-94) -- LANE-5B3-4-decision-debt -----
    "adr:121": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-121's Status line"),
    "adr:122": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-122's Status line"),
    "adr:123": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-123's Status line"),
    "adr:124": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-124's Status line"),
    "adr:125": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-125's Status line"),
    "adr:126": Disposition(reason=_AWAITING_RATIFICATION,
                           owner="the operator's ratification act, tracked at ADR-126's Status line"),

    # -- ADR-128: Accepted AND landed in the same commit -- lane-handoff-boot-dispatch,
    # batch WAVE5B-N5 row N5-3. Not "awaiting ratification" like 121-126 above -- R33 already
    # ratified it, and its own implementation (protocols/HANDOFF_BOOT.md's rewrite, discharging
    # row [#1037] in the same diff) lands in this ADR's own commit rather than in a later,
    # separate row. The lane contract's own "Do not" list forbids this lane from filing a
    # backlog row, so this disposition is the sanctioned alternative the decision-coverage
    # gate itself names.
    "adr:128": Disposition(
        reason="Accepted and self-executing: this ADR's Decision items 2/3 were already "
               "discharged by prior rows (closing [#1123]/[#1124], R33.5), and item 1's own "
               "implementation -- protocols/HANDOFF_BOOT.md's rewrite, plus [#1037]'s Done-when "
               "-- lands in the SAME commit as this ADR, not in a subsequent row. No open "
               "implementing work remains to file a row for.",
        owner="R33 (to-browser/RATIFICATION-2026-09-29-v3-superseded.md); re-open if a later "
              "reader finds protocols/HANDOFF_BOOT.md's Dispatch section incomplete against "
              "this ADR's own Decision text"),

    # -- ADR-129: Accepted AND landed in the same lane -- lane-handoff-redesign, batch
    # HANDOFF-REDESIGN-BUILD. Same shape as ADR-128 above: the lane contract's own "Do not"
    # list forbids filing more than the one (unrelated) backlog row of its Step 3.5, so this
    # disposition is the sanctioned alternative the decision-coverage gate itself names.
    "adr:129": Disposition(
        reason="Accepted and self-executing: this ADR's Decision (the handoff cut gated on "
               "the named handoff-relevant check set, parallel, in-process; the whole-repo "
               "verdict read-only from CI; the refusal log; the batch-close trial cut; the "
               "incremental review-artifact scan) is implemented across this SAME lane's own "
               "commits -- `53bca33d`, `e512e0a0`, `17926bf3`, `4b21f41b`, `7d88f13b` -- "
               "landed alongside this ADR's own commit (`6415639c`), not in a subsequent row. "
               "The one row this lane did file (`tasks/1331`) only REFS this ADR as "
               "precedent; it implements a separate, unrelated gap (the ruling register) and "
               "is correctly not an `implements:` row for this decision. No open implementing "
               "work remains to file a row for.",
        owner="R44 (the operator's paste of the batch order is its own ratification act, per "
              "the frozen contract's own citation); re-open if a later reader finds "
              "scripts/gen_handoff.py's cut path incomplete against this ADR's own Decision "
              "text"),

    # -- pre-triage intakes (DRAFT/SEED) -- LANE-5B3-4-decision-debt --------------------------
    "intake:93": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #93"),
    "intake:95": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #95"),
    "intake:96": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #96"),
    "intake:97": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #97"),
    "intake:98": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #98"),
    "intake:99": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #99"),
    "intake:100": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #100"),
    "intake:101": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #101"),
    "intake:102": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #102"),
    "intake:103": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #103"),
    "intake:104": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #104"),
    "intake:105": Disposition(reason=_AWAITING_TRIAGE, owner="ADR-98/ADR-111's intake funnel, not yet run over intake #105"),

    # -- live WAVE5B-N2 queue amendments, reasoned individually -- LANE-5B3-4-decision-debt ----
    # Only a file whose FULL content is settled (no gap, no still-executing lane) can honestly
    # take a whole-file Disposition (Codex terra review round 3; see the note above). QUEUE,
    # QUEUE2, QUEUE3, QUEUE4 and QUEUE6 have NO entry -- each has at least one lane that is
    # either a genuine gap (no continuing home anywhere in N3's manifest: QUEUE's lane 18,
    # QUEUE4's lane 24) or still executing (QUEUE6's lane 31, continuing as N3's own still-open
    # lane 13) -- all five are filed as ROWS-OWED in the session file instead, each noting which
    # of its OTHER lanes already has a citable home even though the file's own key stays
    # undisposed.
    "declare:AMEND-BATCH-WAVE5B-N2-LANE8-2026-09-25": Disposition(
        reason="EXECUTED, its own Required Done-when met: lane 8 (codespace-roundtrip-ci) "
               "MERGED @ 32791ac3, the devcontainer heartbeat green (run 36155929898, per "
               "AMEND-BATCH-WAVE5B-N2-QUEUE4-2026-09-25's own review of it). The Optional item "
               "(an agent round-trip in Actions) was explicitly marked optional and not "
               "attempted -- by this file's own text, not a gap. Its own ROWS-OWED clause "
               "('scheduled agent round-trip through Dispatch-Codespace') is carried verbatim "
               "into the batch's close digest.",
        owner="to-browser/DIGEST-WAVE5B-N2-2026-09-26.md §2 (lane 8) and §5 (the carried ROWS-OWED clause)"),
    "declare:AMEND-BATCH-WAVE5B-N2-QUEUE5-2026-09-25": Disposition(
        reason="EXECUTED, both of its own lanes' Done-when met: lane 25 "
               "(decision-verification-level) and lane 26 (decision-codespace-substrate) each "
               "REPORTED, producing the required SESSION-lane-*.md and HANDBACK kind report. "
               "(Lane 26's 51 KB cloud brief exceeded the batch's own 40 KB rule and was not "
               "re-run -- a caveat on HOW it ran, not evidence its Done-when went unmet: the "
               "report itself exists.) The holding rules (H1/H2) were procedural and were "
               "applied per the digest's own lane accounting.",
        owner="to-browser/DIGEST-WAVE5B-N2-2026-09-26.md §2 (lanes 25, 26)"),

    # The four superseded WAVE5B-N2 queue amendments (QUEUE2 / QUEUE6, -v1/-v2-superseded) that
    # were disposed here as dead branches left the live population on 2026-10-02: R53 (1) moved
    # every superseded OPEN decision file to the transport's `to-cc/archive/`, which
    # `decision_files` does not scan. Their entries were removed so the register names no
    # decision that is gone (`stale_dispositions`).

    # -- 2026-09-29..10-01 transport amendments, each with its own closing evidence -- R53 (2) --
    # Ruled by the browser seat at the 2026-10-02 handoff cut (P13 found them undisposed). Each
    # owner names the transport file that records the execution or the refusal; every cited file
    # was checked to exist before this entry was written.
    "declare:AMEND-BATCH-WAVE5B-N5-2026-09-29": Disposition(
        reason="EXECUTED in batch WAVE5B-N5, which closed with its digest.",
        owner="to-browser/DIGEST-WAVE5B-N5-2026-09-30.md (R53 (2), 2026-10-02)"),
    "declare:AMEND-BATCH-WAVE5B-N5-R-CYCLE-2-2026-09-29": Disposition(
        reason="EXECUTED in WAVE5B-N5-R cycle 2: the cycle-2 integrator (session d706f00c) "
               "recorded 'AMEND applied' in its receipt, and the batch STATE reads CLOSED "
               "2026-09-29T16:13:56+02:00 (cycle 2).",
        owner="to-browser/STATE-BATCH-WAVE5B-N5-R.md and to-browser/"
              "SESSION-integrator-wave5b-n5-r-2026-09-29.md §Cycle 2 (R53 (2), 2026-10-02)"),
    "declare:AMEND-BATCH-LAUNCH-SEATS-2026-09-29": Disposition(
        reason="EXECUTED by launcher session ce87636a, which applied it to the order it was "
               "executing and recorded each point in its receipt.",
        owner="to-browser/SESSION-launch-seats-2026-09-29.md (R53 (2), 2026-10-02)"),
    "declare:AMEND-HANDOFF-REDESIGN-BUILD-2026-10-01": Disposition(
        reason="EXECUTED in batch HANDOFF-REDESIGN-BUILD (ADR-129), which closed with its "
               "digest.",
        owner="to-browser/DIGEST-HANDOFF-REDESIGN-BUILD-2026-10-01.md (R53 (2), 2026-10-02)"),
    "declare:AMEND-INTEGRATOR-MERGE-PATH-2026-09-29-withdrawn": Disposition(
        reason="REFUSED in writing: withdrawn by R37.2 -- a withdrawn order is not executed.",
        owner="to-browser/RATIFICATION-2026-09-29.md (R37.2 withdrawn; R53 (2), 2026-10-02)"),
}


# ------------------------------------------------------------------------ population readers


def _read(path: Path) -> str:
    """Text with replacement decoding. A decision file this organ cannot decode still has a
    status and a date to read; it must not vanish from the population over one bad byte."""
    return path.read_text(encoding="utf-8", errors="replace")


def _filename_date(name: str) -> _dt.date | None:
    match = _FILENAME_DATE_RE.search(name)
    if not match:
        return None
    try:
        return _dt.date.fromisoformat(match.group(1))
    except ValueError:      # pragma: no cover -- a shaped-but-impossible date, e.g. 2026-13-01
        return None


def _adr_decisions(root: Path) -> list[tuple[str, str, str, _dt.date | None, str, str]]:
    """`(key, label, status, date, date_source, locator)` for every ADR in `docs/decisions/`.

    `validate_adr_status.scan_zone` is the reader -- the same one `funnel_lifecycle` borrows,
    for the same reason: two parsers for one `Status:` grammar is two answers to one question.
    """
    import validate_adr_status as vas  # noqa: PLC0415 -- deferred sibling import, the idiom here

    zone = root / "docs" / "decisions"
    if not zone.is_dir():
        raise PopulationUnreadable(f"no ADR corpus at {zone}")
    try:
        fields, missing, extra = vas.scan_zone(zone)
    except vas.CorpusUnusable as exc:
        raise PopulationUnreadable(f"ADR corpus unusable: {exc}") from exc
    if missing or extra:
        raise PopulationUnreadable(
            "ADR corpus carries files with zero or several Status fields -- a decision with no "
            f"computable status is not a decision with no status. missing={missing} extra={extra}")
    out = []
    for field in fields:
        number = vas.adr_number(field.path).removeprefix("ADR-")
        match = _ADR_DATE_RE.search(_read(field.path))
        if match:
            date, source = _dt.date.fromisoformat(match.group(1)), "header"
        else:
            date, source = _filename_date(field.path.name), "filename"
            if date is None:
                source = "absent"
        out.append((f"{fpg.NODE_ADR}:{number}", f"ADR-{number}", field.value, date, source,
                    field.path.relative_to(root).as_posix()))
    return out


def _intake_decisions(root: Path) -> list[tuple[str, str, str, _dt.date | None, str, str]]:
    """The same tuple for every doc at `docs/intake/` depth 1, via `gen_intake_index`."""
    import gen_intake_index as gii  # noqa: PLC0415

    zone = root / "docs" / "intake"
    if not zone.is_dir():
        return []          # an intake funnel is not universal; an ADR corpus is
    out = []
    for status, intake_id, filename, _title in gii.collect_intakes(zone):
        date = _filename_date(filename)
        out.append((f"{fpg.NODE_INTAKE}:{intake_id}", f"intake #{intake_id}", status, date,
                    "filename" if date else "absent", f"docs/intake/{filename}"))
    return out


def _transport_decisions(root: Path, transport) -> list[tuple]:
    """`(key, label, status, date, date_source, locator)` per transport `DECLARE-`/`AMEND-`.

    STATUS HERE IS THE P11 CARRIAGE VERDICT, not a frontmatter token, and that is the whole of
    the transport design: `carried-by:` resolving on `main` means the ruling reached an in-repo
    object, which this population already measures on its own terms.
    """
    import gen_handoff as gh  # noqa: PLC0415

    out = []
    for verdict in gh.carriage_verdicts(transport, root):
        path = verdict.path
        if not path.name.startswith(TRANSPORT_PREFIXES):
            continue
        stem = path.stem
        date = _filename_date(path.name)
        if date is not None:
            source = "filename"
        else:
            # mtime, and it is LABELLED rather than passed off as a date the file states. A
            # transport file carries no header date and the drive it sits on can re-touch one,
            # so a reader is told which of the two it is looking at.
            try:
                date = _dt.date.fromtimestamp(path.stat().st_mtime)
                source = "mtime"
            except OSError:                       # pragma: no cover -- an unreadable transport
                date, source = None, "absent"
        out.append((f"declare:{stem}", f"{path.parent.name}/{path.name}", verdict.kind, date,
                    source, f"{path.parent.name}/{path.name}"))
    return out


# ------------------------------------------------------------------------- the relation half


def _implementing_rows(store, key: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`(all rows, open rows)` implementing `key`, read from the STORE and nowhere else.

    Input 8's edges run ROW -> DECISION and carry the row's own status in `detail`, so one
    SELECT answers both "who implements this" and "is any of them still open" without a second
    pass over `tasks/`. The `detail` FORMAT is owned by `file_purpose_graph`, imported here so
    the two cannot drift.
    """
    rows: list[str] = []
    open_rows: list[str] = []
    for edge in store.in_edges(key, (fpg.EDGE_IMPLEMENTS,)):
        if edge.get("source") != fpg.INPUT_DECISION_IMPLEMENTS:
            continue
        src = edge["src"]
        if not src.startswith("task:"):
            continue
        task_id = src.removeprefix("task:")
        rows.append(task_id)
        detail = str(edge.get("detail", ""))
        if detail.removeprefix(fpg.DECISION_DETAIL_PREFIX).strip().lower() == "open":
            open_rows.append(task_id)
    return tuple(sorted(set(rows), key=int)), tuple(sorted(set(open_rows), key=int))


def _state(kind: str, status: str, open_rows: tuple[str, ...], rows: tuple[str, ...],
           disposition: Disposition | None) -> str:
    """A decision's lifecycle position. The ONE place the mapping lives."""
    if kind == KIND_ADR:
        if status in ADR_LEFT:
            return STATE_SUPERSEDED
        accepted = status == ADR_ACCEPTED
    elif kind == KIND_INTAKE:
        if status in INTAKE_LEFT:
            return STATE_SUPERSEDED
        if status in INTAKE_DONE:
            return STATE_DONE
        accepted = status in INTAKE_ACCEPTED
    else:
        # A transport ruling is ACCEPTED BY EXISTING -- it is a ruling, not a proposal. Its
        # carriage verdict says whether it has landed anywhere.
        #
        # AN OPEN ROW OUTRANKS A RESOLVING CARRIAGE, and the order is the claim. A carried
        # ruling is `done` only when nothing is still working on it: `carried-by:` says the
        # text reached a repo home, an OPEN `implements:` row says the work it ordered is in
        # flight, and those are different facts about the same decision. Reading carriage
        # first made every carried AMEND `done` the moment its text landed -- including the
        # ones whose lanes were still running, which is precisely the "decided and unscheduled"
        # blindness this organ exists to remove.
        if open_rows:
            return STATE_EXECUTING
        if status == gq_carriage_resolves():
            return STATE_DONE
        accepted = True
    if not accepted:
        return STATE_CONSIDERED
    if open_rows:
        return STATE_EXECUTING
    if disposition is not None or rows:
        return STATE_DONE
    return STATE_ACCEPTED


def gq_carriage_resolves() -> str:
    """`gen_handoff.CARRIAGE_RESOLVES`, resolved lazily so this module imports on a tree with
    no transport reader and so the token is never a second literal here."""
    try:
        import gen_handoff as gh  # noqa: PLC0415
        return gh.CARRIAGE_RESOLVES
    except ImportError:          # pragma: no cover -- gen_handoff is a sibling, always present
        return "resolves"


def decisions(repo_root, store, *, transport=None,
              dispositions: dict[str, Disposition] | None = None) -> list[Decision]:
    """The whole population, each decision with its state and its implementing rows.

    `transport=None` measures the two IN-REPO classes only, and a caller can tell -- no
    `KIND_TRANSPORT` row is present. That is DEGRADED, never silently empty.
    """
    root = Path(repo_root)
    register = DECISION_DISPOSITIONS if dispositions is None else dispositions
    raw: list[tuple] = [(*row, KIND_ADR) for row in _adr_decisions(root)]
    raw += [(*row, KIND_INTAKE) for row in _intake_decisions(root)]
    if transport is not None:
        raw += [(*row, KIND_TRANSPORT) for row in _transport_decisions(root, transport)]

    out: list[Decision] = []
    for key, label, status, date, date_source, locator, kind in raw:
        rows, open_rows = _implementing_rows(store, key)
        disposition = register.get(key)
        out.append(Decision(
            key=key, kind=kind, label=label, status=status,
            state=_state(kind, status, open_rows, rows, disposition),
            date=date, date_source=date_source, rows=rows, open_rows=open_rows,
            locator=locator, disposition=disposition))
    return sorted(out, key=lambda d: (d.kind, d.key))


#: "argument not given", distinct from an explicit `transport=None` (which MEANS "measure the
#: two in-repo classes only"). Without it a caller could not ask for the default resolution.
_UNSET = object()


def live_decisions(repo_root, *, db=None, transport=_UNSET) -> list[Decision]:
    """The LIVE population -- the persisted store plus the transport -- resolved in ONE place.

    Three consumers want a view of exactly this and nothing else: `gen_handoff` writes the A9-2
    ledger from it, `verify_handoff_probes` runs the A9-2 onboarding rung on it, and
    `fleet_health` renders A9-3's numbers from it. Written here rather than three times over
    there, because a consumer that resolves the population its own way is free to disagree with
    the organ that REFUSES on it -- and a gate and a report that disagree about what exists is
    the failure this whole lane is about.

    The store is opened through `gs.ensure`, never `gs.open`: exists is not fresh, and a stale
    graph does not fail, it answers wrongly (`graph_queries._open`'s contract, and `_open`
    below is the same call for the CLI).

    `transport=None` narrows to the two in-repo classes; the default resolves the live one.
    MEASURED 2026-09-11 on this tree: the transport leg costs ~23s and the two in-repo classes
    ~1.4s, because `gen_handoff.carriage_verdicts` spawns a `git cat-file` per carrier token
    and there are ~96 carriers. That is not this organ's cost to fix -- it is P11's existing
    reader, outside this lane's footprint -- but it IS why `fleet_health` passes `None` and says
    so on its line while the handoff cut, an explicit operator act, pays for the whole thing.

    RAISES rather than degrades. A caller that must not die on a boundary catches; this does
    not make that decision on their behalf, because the right degraded answer differs per
    consumer (a written `unavailable` block, a `skipped` probe rung, a dropped digest line).
    """
    root = Path(repo_root).resolve()
    store = gs.ensure(root, Path(db) if db else gs.store_path(root))
    return decisions(root, store,
                     transport=_transport_root() if transport is _UNSET else transport)


def store_is_stale(repo_root, *, db=None) -> bool:
    """True when the persisted store would have to be REBUILT before it could answer.

    Exposed so a SURFACING consumer can decline to trigger that rebuild. `fleet_health` runs at
    SessionStart on every session, and MEASURED 2026-09-11 on this tree a cold rebuild is ~16s
    against ~1.5s warm -- a cost a digest line has no business imposing. The rebuild belongs to
    the `graph-rebuild` pre-commit hook that owns it ([#664] clause 1), and it will be paid
    there at the next commit either way.

    A GATE never calls this. `decision_coverage check` goes through `ensure` unconditionally,
    because exists is not fresh and a stale graph does not fail, it answers wrongly.
    """
    root = Path(repo_root).resolve()
    return gs.is_stale(root, Path(db) if db else gs.store_path(root))


#: The key prefix each decision kind is keyed on -- the one place the mapping between a kind
#: and its key namespace lives, so `stale_dispositions` can tell "absent" from "not measured".
KEY_PREFIXES: dict[str, str] = {KIND_ADR: "adr:", KIND_INTAKE: "intake:",
                                KIND_TRANSPORT: "declare:"}


def stale_dispositions(found: list[Decision],
                       dispositions: dict[str, Disposition] | None = None) -> list[str]:
    """Dispositioned keys no longer in the population -- ADR-75's decoration rule.

    Surfaced, never blocking: a stale row is a fact about the register, and refusing a commit
    for it would punish the wrong act. `graph_queries.stale_dispositions` is the same shape.

    A CLASS THAT WAS NOT MEASURED IS NOT JUDGED, and this guard is load-bearing rather than
    defensive -- it was written after the live-tree witness caught the false positive. Called on
    a population measured with `transport=None`, the naive predicate reports every transport
    disposition as naming a decision that is gone, because the class was never read. "Absent"
    and "not measured" are different facts (DEFECT E-29's rule), and a register that
    self-reports as rotten whenever the transport is unresolved is a register nobody will read.
    """
    register = DECISION_DISPOSITIONS if dispositions is None else dispositions
    known = {d.key for d in found}
    measured = {d.kind for d in found}
    unmeasured = tuple(prefix for kind, prefix in KEY_PREFIXES.items() if kind not in measured)
    return sorted(key for key in register
                  if key not in known and not key.startswith(unmeasured))


# ----------------------------------------------------------------------------- the refusals


#: What the refusal tells the author to DO. A9-1's second half -- "states what must be done" --
#: and the reason it is a constant is that the commit-tier hook, the CLI and the onboarding
#: rung must all say the same thing.
REPAIR = ("File a row whose body carries `· implements: {token}` (the `implements:` frontmatter "
          "key is DERIVED from that clause), or record a written 'no implementation required' "
          "disposition with a reason and an owner in "
          "`scripts/decision_coverage.py::DECISION_DISPOSITIONS`.")


def _finding(decision: Decision) -> Finding:
    return Finding(
        subject=decision.label,
        evidence=(f"{decision.locator} is {decision.status} and no OPEN row implements it, and "
                  f"no disposition rules it. " + REPAIR.format(token=_token_for(decision))))


def _token_for(decision: Decision) -> str:
    """The `implements:` token that would cover this decision -- printed, so the author does not
    have to derive the grammar from a doc."""
    if decision.kind == KIND_ADR:
        return f"ADR-{decision.key.removeprefix('adr:')}"
    if decision.kind == KIND_INTAKE:
        return f"intake-{decision.key.removeprefix('intake:')}"
    return decision.key.removeprefix("declare:")


def uncovered(found: list[Decision]) -> list[Decision]:
    """Accepted and unexecuted -- the one state the refusals fire on, era or not."""
    return [d for d in found if d.state == STATE_ACCEPTED]


def decision_coverage(repo_root, store, *, staged: list[str] | None = None, transport=None,
                      dispositions: dict[str, Disposition] | None = None,
                      era_leg: bool = False) -> list[Finding]:
    """The commit-tier refusal. Two legs, and both are era-bounded.

    LEG 1 -- THE COMMIT'S OWN DECISION FILES. `staged=None` reads `git diff --cached`, the same
    subject set `task_coverage` uses and for the same reason: this is the moment a decision is
    landed or accepted, so it is the moment the obligation arises and the author can discharge
    it in the same commit. It cannot wedge a tree, because an author who touches no decision
    file is asked nothing.

    LEG 2 -- THE ERA. Opt-in (`era_leg=True`) and armed by the pre-commit hook, because leg 1
    alone is satisfiable by never touching the file again. It refuses on EVERY in-era accepted
    decision with neither a row nor a disposition, whether or not this commit named it.

    A MERGE IS TRANSPORT, NOT AUTHORSHIP -- the same carve-out `task_coverage` and
    `block_commit_on_main` both carry, for the same reason: main's own commits bring decision
    files this branch never wrote, and refusing them would ask this lane to schedule, or to
    refuse, work it has not assessed.
    """
    root = Path(repo_root)
    if staged is None and gq._merge_in_progress(root):
        return []
    found = decisions(root, store, transport=transport, dispositions=dispositions)
    by_locator = {d.locator: d for d in found}
    subjects = gq.staged_paths(root) if staged is None else staged

    hits: dict[str, Decision] = {}
    for relpath in subjects:
        decision = by_locator.get(relpath)
        if decision is not None and decision.state == STATE_ACCEPTED and decision.in_era:
            hits[decision.key] = decision
    if era_leg:
        for decision in uncovered(found):
            if decision.in_era:
                hits[decision.key] = decision
    return [_finding(hits[key]) for key in sorted(hits)]


# ------------------------------------------------------- A9-2: the onboarding refusal + ledger


@dataclass(frozen=True)
class ProbeFinding:
    """One onboarding rung result, in `verify_handoff_probes.ProbeResult`'s vocabulary."""
    probe_id: str
    status: str
    detail: str


#: The rung's id, in the family `verify_handoff_probes` already names its synthesized rows.
ONBOARDING_PROBE_ID = "P13-decision-ledger"


def onboarding_findings(found: list[Decision]) -> list[ProbeFinding]:
    """A9-2's probe: every open decision must be DISPOSED before the incoming plan is accepted.

    The three dispositions A9-2 names map onto states already computed here, which is why this
    is a probe and not prose: "executing in batch N" and "scheduled with a row" are both
    `executing`, and "refused in writing" is a disposition, which makes the decision `done`.
    `accepted` is therefore exactly the UNDISPOSED state, and it is the only one that FAILs.

    ERA-BOUNDED, like the commit-tier legs and for the same reason -- "any FAIL blocks
    onboarding", so an unbounded rung would block every handoff on the 104 decisions that
    predate the `implements:` key. The grandfathered count rides in the same detail line, so
    the debt is visible at the one moment someone is reading the bundle.
    """
    open_set = uncovered(found)
    in_era = [d for d in open_set if d.in_era]
    if not in_era:
        return []
    grandfathered = len(open_set) - len(in_era)
    named = ", ".join(f"{d.label} ({d.locator})" for d in in_era[:6])
    more = f" +{len(in_era) - 6} more" if len(in_era) > 6 else ""
    tail = (f" {grandfathered} further accepted-but-unexecuted decision(s) predate "
            f"{ARM_DATE.isoformat()} and are counted, not refused." if grandfathered else "")
    return [ProbeFinding(
        ONBOARDING_PROBE_ID, "fail",
        f"{len(in_era)} accepted decision(s) carry neither an implementing row nor a written "
        f"disposition: {named}{more}. The incoming seat's plan must dispose each one -- "
        f"executing in batch N, scheduled with a row, or refused in writing -- before the plan "
        f"is accepted (AMEND-SESSION-PLAN-009 A9-2).{tail}")]


#: The bundle artifact A9-2 asks for. A BUNDLE artifact, not a browser-visible one: it is
#: absent from `assemble_paste`'s v5 manifest, exactly as `FUNNEL_HEALTH.md` is, so the
#: answer-free invariant governing BOOT / RESIDUAL / PROBES is untouched by it.
LEDGER_FILE = "DECISION_LEDGER.md"
LEDGER_BEGIN = "<!-- DECISION-LEDGER:BEGIN (generated by decision_coverage — do not edit) -->"
LEDGER_END = "<!-- DECISION-LEDGER:END -->"

#: `gen_handoff._FUNNEL_UNAVAILABLE`'s word, reused rather than invented: the bundle already
#: has one spelling for "this block measured nothing", and a reader should not learn a second.
LEDGER_UNAVAILABLE = "unavailable"

#: States that are still IN the lifecycle. A9-2 says "every open decision", and `done` and
#: `superseded` have left it.
LEDGER_STATES: tuple[str, ...] = (STATE_ACCEPTED, STATE_EXECUTING, STATE_CONSIDERED)


def render_ledger(found: list[Decision], today: _dt.date | None = None) -> str:
    """A9-2's ledger, verbatim as it lands in the bundle.

    FLAT -- `key: value` lines and bullets, never a padded table. The bundle is read into a
    browser window and re-billed on every turn of it, and a column-padded markdown table costs
    roughly three times its content in tokens for a border the reader's client draws anyway
    (CLAUDE.md output-formatting; PLAYBOOK §8).
    """
    day = today or _dt.date.today()
    lines = [LEDGER_BEGIN, "## DECISION LEDGER (generated — every open decision, with its state)",
             "", f"source: scripts/decision_coverage.py (A9-2); arm date {ARM_DATE.isoformat()}",
             ""]
    for state in LEDGER_STATES:
        members = [d for d in found if d.state == state]
        lines.append(f"### {state} ({len(members)})")
        lines.append("")
        for d in members:
            age = f"{(day - d.date).days}d" if d.date else "age unknown"
            rows = ("rows " + "/".join(f"[#{r}]" for r in d.rows)) if d.rows else "no row"
            era = "in-era" if d.in_era else "grandfathered"
            lines.append(f"- {d.label} — {d.locator} — {rows} — {age} — {era}")
        lines.append("")
    lines.append(LEDGER_END)
    return "\n".join(lines) + "\n"


def render_ledger_unavailable(reason: str) -> str:
    """The ledger's DEGRADED form -- the same markers, the same heading, and WHY it is empty.

    An organ that vanishes when it cannot measure reads as a pass to everything downstream
    (DEFECT E-29, and `verify_handoff_probes` states the same rule for its carriage rung). For
    a LEDGER the failure is sharper than for a rung: a missing `DECISION_LEDGER.md` reads to
    the incoming seat as "no open decisions", which is the one answer this file must never
    give. So the block is written either way, and an unreadable population says so in words.
    """
    return "\n".join([
        LEDGER_BEGIN,
        "## DECISION LEDGER (generated \u2014 every open decision, with its state)",
        "",
        f"source: scripts/decision_coverage.py (A9-2); arm date {ARM_DATE.isoformat()}",
        "",
        f"{LEDGER_UNAVAILABLE}: {reason}",
        "",
        "This bundle states NOTHING about open decisions. It is not a clean ledger, and an "
        "incoming plan cannot dispose what it was never shown.",
        LEDGER_END,
    ]) + "\n"


# ------------------------------------------------------------------------- A9-3: the metric


@dataclass(frozen=True)
class Metrics:
    """A9-3's four numbers, plus the one the era bound owes: how much it declines to refuse."""
    accepted: int
    executing: int
    done: int
    oldest_unexecuted_days: int | None
    grandfathered: int
    #: False when the population was read with `transport=None`. The numbers are then CORRECT
    #: for what was measured and WRONG as a statement about the repo -- `executing` and `done`
    #: are carried almost entirely by the transport class -- so the narrowing is not something
    #: a reader may be left to infer from a number that looks like a clean zero.
    transport_measured: bool = True

    def render(self) -> str:
        """The `[decisions]` digest line. Flat, one line, no table."""
        oldest = ("none" if self.oldest_unexecuted_days is None
                  else f"{self.oldest_unexecuted_days}d")
        scope = "" if self.transport_measured else " -- in-repo classes only"
        return (f"[decisions] accepted {self.accepted} / executing {self.executing} / "
                f"done {self.done} / oldest unexecuted {oldest} "
                f"({self.grandfathered} grandfathered){scope}")


def metrics(found: list[Decision], today: _dt.date | None = None, *,
            transport_measured: bool = True) -> Metrics:
    """*"decisions accepted, executing, done, and age of the oldest accepted-but-unexecuted
    decision"* -- A9-3, over the WHOLE population rather than the era.

    `oldest_unexecuted_days` is None when nothing is unexecuted, never 0: an honest absence,
    because a 0 there reads as "nothing is old" and those are different facts.
    """
    day = today or _dt.date.today()
    open_set = uncovered(found)
    ages = [(day - d.date).days for d in open_set if d.date is not None]
    return Metrics(
        accepted=len(open_set),
        executing=sum(1 for d in found if d.state == STATE_EXECUTING),
        done=sum(1 for d in found if d.state == STATE_DONE),
        oldest_unexecuted_days=max(ages) if ages else None,
        grandfathered=sum(1 for d in open_set if not d.in_era),
        transport_measured=transport_measured)


# -------------------------------------------------- the ruling register leg ([#721], R79.3)
#
# R79 item 3 (operator, 2026-10-04): *"no decision is ever forgotten"* -- every ratified ruling
# lands in the repository, is carried by a backlog row or an explicit "no implementation
# required", and is enforced by a gate that refuses at batch close and at the handoff cut. This is
# that gate, and it is `[#721]`'s Done-when: the register's entries are counted AT ENTRY
# GRANULARITY and one with neither an implementing row nor a written disposition is NAMED.
#
# LIBRARY-FIRST, decided by lane `b2-rulings-landing` (AMEND-B2-W1-2: "CC designs it"):
#   * This module is the home (stdlib > established dependency > stabilized project): it already
#     joins a document-read population with a relation, carries `Disposition`, era-bounds its
#     refusals and returns `Finding`. A second module would restate all four.
#   * The row -> ruling link is the register entry's own `**Carried by:**` line, NOT a new
#     `implements:` token kind. Widening the grammar means two regexes (`file_purpose_graph`,
#     `validate_backlog`), a new FPG-1 node kind and a store rebuild, and `implements:` is derived
#     from a row-body clause that `gen_task_tree` owns. The register is where the ruling already
#     is, `landed:` predicates already parse it at entry granularity, and a one-way link is
#     checked from BOTH ends: the named row must exist, carry a status, state a Done-when, and
#     itself name the ruling.
#   * The ruling's identity is its R-number alone (R1-R79 are in practice globally unique: the
#     file that restarts at R1 restates the same rulings). A ruling counts as landed when a
#     register bullet `- **R<n>` exists -- the shape `handoff_state._LANDED_RE` counts, pinned
#     equal by a test -- and NEVER because a RATIFICATION file's `carried-by:` names the register:
#     P11 proves a home exists, not that the ruling is in it.
#
# THE ERA BOUND, stated as this lane's one design ruling. The `Carried by:` line did not exist
# before R55, and sections A..AQ are immutable to the lane that adds it, so 54 entries could
# never be repaired by the author the refusal would land on. `FIRST_GATED_RULING` bounds the
# REFUSAL and nothing else: `register_counts` reports how many entries it declines to refuse on
# every run, and `floor=` re-arms the same predicate over the older sections (the test for
# [#721]'s section-AH witness does exactly that).
#
# "UNLANDED FOR MORE THAN ONE BATCH" needs a batch clock, and the transport already has one:
# `to-browser/STATE-BATCH-<X>.md` reads `CLOSED <date>`. A ruling is aged by the number of
# batches CLOSED on a LATER day than its file's `date:` (a batch closed the same day it was
# ruled does not age it), and refuses when that number exceeds `GRACE_BATCHES`.
#
# WHAT THIS LEG DOES NOT SEE, stated rather than discovered later:
#   * Whether a named row is the RIGHT row (coverage is structural; adequacy is a reviewer's).
#   * A ruling whose RATIFICATION file has no `## R<n>` heading or `- **R<n>**` bullet.
#   * The transport when `CLAUDE_PROMPTS_DIR` is unresolved: the unlanded leg then reports
#     itself NOT MEASURED -- never an empty list, never a pass (DEFECT E-29's rule).

RULINGS_REL = "protocols/STANDING_RULINGS.md"
#: R55 is the first ruling that can carry a `Carried by:` line (it is the first one landed after
#: R79's rule existed); see the era-bound block above.
FIRST_GATED_RULING = 55
#: "more than one batch": a ruling unlanded across MORE than this many closed batches refuses.
GRACE_BATCHES = 1
#: A row in one of these states carries a ruling. `retired` and `superseded` rows do not: the
#: work they named is not going to happen under that id.
CARRYING_ROW_STATUSES = frozenset({"open", "closed", "deferred"})
NO_IMPLEMENTATION = "no implementation required"

#: The bundle's own landed-id shape. `tests/test_decision_coverage.py` pins it EQUAL to
#: `handoff_state._LANDED_RE.pattern`, so the two cannot disagree about what is landed.
_LANDED_RE = re.compile(r"(?m)^- \*\*R(\d+)\b")
_ENTRY_END_RE = re.compile(r"^(?:- \*\*R\d+\b|#{2,3} )")
_CARRIED_LINE_RE = re.compile(r"^\s*\*\*Carried by:\*\*\s*(\S.*?)\s*$")
_FENCE_RE = re.compile(r"^\s*```")
_ROW_REF_RE = re.compile(r"\[#(\d+)\]")
_DISPOSITION_RE = re.compile(
    rf"^{NO_IMPLEMENTATION}\s*(?:—|--|-)\s*(?P<reason>.+?)\s*\(owner:\s*(?P<owner>[^()]+?)\)\s*$",
    re.I | re.S)
_TITLE_RE = re.compile(r"^- \*\*R\d+\s*(?:—|--|-)?\s*([^*]*)\*\*")

REPAIR_RULING = ("Add a line `**Carried by:** [#<row id>]` to the entry in "
                 f"`{RULINGS_REL}` (the row must exist, state a Done-when and name the ruling), "
                 f"or `**Carried by:** {NO_IMPLEMENTATION} — <why> (owner: <who>)`.")


@dataclass(frozen=True)
class RegisterEntry:
    """One `- **R<n>` bullet of the register, with what its `Carried by:` line says."""
    number: int
    line: int                          # 1-based line of the bullet
    title: str
    carried: str | None                # the raw value after `**Carried by:**`, or None
    rows: tuple[str, ...]              # `[#id]` references, in order
    disposition: Disposition | None    # parsed only when the value is a well-formed one


def parse_register(text: str) -> list[RegisterEntry]:
    """Every register bullet `- **R<n>` OUTSIDE a fenced block, section-agnostic.

    Fenced text is skipped on both sides: a verbatim block quoting a source that itself contains
    `- **R71 ...` or `**Carried by:**` is the source's text, not an entry (a test pins it).
    An entry runs from its bullet to the next bullet or heading.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    entries: list[RegisterEntry] = []
    fenced = False
    current: dict | None = None

    def _close() -> None:
        nonlocal current
        if current is None:
            return
        carried = current["carried"]
        rows = tuple(_ROW_REF_RE.findall(carried)) if carried else ()
        disposition = None
        if carried and carried.lower().startswith(NO_IMPLEMENTATION):
            match = _DISPOSITION_RE.match(carried)
            if match and match.group("reason").strip() and match.group("owner").strip():
                disposition = Disposition(reason=match.group("reason").strip(),
                                          owner=match.group("owner").strip())
            rows = ()
        entries.append(RegisterEntry(current["number"], current["line"], current["title"],
                                     carried, rows, disposition))
        current = None

    for index, line in enumerate(lines, start=1):
        if _FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        bullet = _LANDED_RE.match(line)
        if bullet:
            _close()
            title = _TITLE_RE.match(line)
            current = {"number": int(bullet.group(1)), "line": index,
                       "title": (title.group(1).strip() if title else ""), "carried": None}
            continue
        if _ENTRY_END_RE.match(line):
            _close()
            continue
        if current is not None and current["carried"] is None:
            carried = _CARRIED_LINE_RE.match(line)
            if carried:
                current["carried"] = carried.group(1)
    _close()
    return entries


def _read_register(root: Path) -> str:
    path = root / RULINGS_REL
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise PopulationUnreadable(f"no ruling register at {path}: {exc}") from exc


def _task_row(root: Path, task_id: str) -> tuple[str, str] | None:
    """`(status, full text)` of `tasks/<id>-*.md`, or None when no such row file exists. Closed
    rows stay on disk with `status: closed`, so a closed row is found here like any other."""
    found = sorted((root / "tasks").glob(f"{task_id}-*.md"))
    if not found:
        return None
    text = found[0].read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?m)^status:\s*(\w+)", text)
    return (match.group(1).lower() if match else ""), text


_OWNER_RE = re.compile(r"(?<![\w-])(?<!not )owner:[ \t]*([^·\n]*)", re.I)   # not `non-owner:`
#: What an `owner:` value may not be: a placeholder names nobody. The gate checks that SOMEONE is
#: named, not that the name is a live lane -- that is a reading, and it stays the reviewer's.
_OWNER_PLACEHOLDER_RE = re.compile(r"^(?:none|n/?a|tbd|tba|nobody|unknown|unassigned|-+)\W*$", re.I)


def _names_an_owner(text: str) -> bool:
    """True when some `owner:` clause in the row carries a value that is not a placeholder."""
    for match in _OWNER_RE.finditer(text):
        value = match.group(1).strip()
        if value and not _OWNER_PLACEHOLDER_RE.match(value):
            return True
    return False


def _entry_defect(root: Path, entry: RegisterEntry) -> str | None:
    """Why this entry is not carried, or None when it is."""
    ruling = f"R{entry.number}"
    if entry.carried is None:
        return "it has no `Carried by:` line, so neither a row nor a written disposition"
    if entry.carried.lower().startswith(NO_IMPLEMENTATION):
        if entry.disposition is None:
            return ("its disposition does not name BOTH a reason and an owner "
                    f"(`{NO_IMPLEMENTATION} — <why> (owner: <who>)`)")
        return None
    if not entry.rows:
        return f"its `Carried by:` line names no `[#id]` row and is not a `{NO_IMPLEMENTATION}` line"
    problems = []
    for task_id in entry.rows:
        row = _task_row(root, task_id)
        if row is None:
            problems.append(f"[#{task_id}] does not exist under tasks/")
            continue
        status, text = row
        if status not in CARRYING_ROW_STATUSES:
            problems.append(f"[#{task_id}] has status `{status or 'none'}`, which carries nothing")
        elif not re.search(rf"\b{ruling}\b", text):
            problems.append(f"[#{task_id}] never names {ruling}")
        elif not re.search(r"done[ -]when", text, re.I):
            problems.append(f"[#{task_id}] states no Done-when")
        elif not _names_an_owner(text):
            problems.append(f"[#{task_id}] names no `owner:` (a wave or a lane)")
        else:
            return None
    return "no named row carries it: " + "; ".join(problems)


def uncarried_rulings(repo_root, *, floor: int = FIRST_GATED_RULING) -> list[Finding]:
    """[#721] and R79.3(b): a landed ruling with neither a row nor a 'no implementation required'
    line, named by the refusal. Entries below `floor` are not judged (see the era-bound block)."""
    root = Path(repo_root)
    out: list[Finding] = []
    for entry in parse_register(_read_register(root)):
        if entry.number < floor:
            continue
        defect = _entry_defect(root, entry)
        if defect is not None:
            out.append(Finding(
                subject=f"R{entry.number}",
                evidence=f"{RULINGS_REL}:{entry.line} -- {defect}. {REPAIR_RULING}"))
    return out


@dataclass(frozen=True)
class RegisterCounts:
    """How the register divides, so the era bound is MEASURED rather than silent."""
    total: int
    gated: int
    carried: int
    grandfathered: int


def register_counts(repo_root, *, floor: int = FIRST_GATED_RULING) -> RegisterCounts:
    root = Path(repo_root)
    entries = parse_register(_read_register(root))
    gated = [e for e in entries if e.number >= floor]
    bad = len(uncarried_rulings(root, floor=floor))
    return RegisterCounts(total=len(entries), gated=len(gated), carried=len(gated) - bad,
                          grandfathered=len(entries) - len(gated))


class TransportUnreadable(PopulationUnreadable):
    """The transport has no `to-browser/` to read -- NOT MEASURED, never 'no rulings'."""


@dataclass(frozen=True)
class FileRuling:
    file: str
    number: int
    date: _dt.date | None


_SUPERSEDED_NAME_RE = re.compile(r"superseded|withdrawn", re.I)
#: A ruling in a RATIFICATION file: a `## R<n>` / `### R<n>` heading, or the one-line register
#: bullet `- **R<n>**` the older files use. A range such as `- **R1-R23**` is not a ruling.
_FILE_RULING_RE = re.compile(r"(?m)^(?:#{2,3}[ \t]+\**R(\d+)\b|-[ \t]+\*\*R(\d+)\*\*)")
#: The WHOLE first token after the key, so `2026-09-01garbage` is read as that token and judged
#: invalid -- a regex that took only the valid-looking prefix would accept it.
_HEADER_DATE_RE = re.compile(r"(?m)^date:[ \t]*(\S*)")
_CLOSED_RE = re.compile(r"(?m)^CLOSED[ \t]+(\S+)")
_DAY_ONLY_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DAY_STAMP_RE = re.compile(r"(\d{4}-\d{2}-\d{2})(?:T\S*)?")     # `2026-09-05T08:00Z` is a day
_HEAD_LINES = 12


def _top(text: str) -> str:
    """The first `_HEAD_LINES` lines of a transport file, where its `date:` / `CLOSED` line sits.
    Takes the text, not a path: the caller owns the read, so a read failure is raised there."""
    return "\n".join(text.replace("\r\n", "\n").split("\n")[:_HEAD_LINES])


def ratification_files(transport) -> list[Path]:
    """The NON-SUPERSEDED RATIFICATION files of `to-browser/`: not `-vN-superseded`, not
    `-withdrawn`, not the `RATIFICATION-DIGEST` summary."""
    folder = Path(transport) / "to-browser"
    return sorted(p for p in _transport_files(folder, "RATIFICATION-")
                  if not _SUPERSEDED_NAME_RE.search(p.name)
                  and not p.name.startswith("RATIFICATION-DIGEST"))


def _transport_files(folder: Path, prefix: str) -> list[Path]:
    """The `<prefix>*.md` files of a transport folder. Enumerated with `os.listdir`, which raises,
    where `Path.glob` can swallow an enumeration error and read as an empty folder."""
    if not folder.is_dir():
        raise TransportUnreadable(f"no {folder.name}/ under the transport {folder.parent}")
    try:
        names = os.listdir(folder)
    except OSError as exc:
        raise TransportUnreadable(f"{folder.name}/ could not be listed: {exc}") from exc
    return sorted(folder / n for n in names
                  if n.startswith(prefix) and n.endswith(".md") and (folder / n).is_file())


def _parse_day(text: str, *, stamp: bool = False) -> _dt.date | None:
    """A whole token that is a real `YYYY-MM-DD` (or, with `stamp`, a `...T<time>` stamp of one),
    else None -- `2026-99-01` and `2026-09-01garbage` match a date's shape and are not dates."""
    match = (_DAY_STAMP_RE if stamp else _DAY_ONLY_RE).fullmatch(text)
    if match is None:
        return None
    try:
        return _dt.date.fromisoformat(match.group(1) if stamp else text)
    except ValueError:
        return None


def file_rulings(path: Path) -> list[FileRuling]:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        # NOT `[]`: a file that cannot be read is not a file with no rulings.
        raise TransportUnreadable(f"{path.name} could not be read: {exc}") from exc
    header = _HEADER_DATE_RE.search(_top(text))
    if header:
        # A header that is PRESENT and not a real day is undated, never the file-name date: the
        # name can sit inside the grace period and hide the refusal.
        date = _parse_day(header.group(1))
    else:
        date = _filename_date(path.name)
    seen: set[int] = set()
    out: list[FileRuling] = []
    for match in _FILE_RULING_RE.finditer(text):
        number = int(match.group(1) or match.group(2))
        if number not in seen:
            seen.add(number)
            out.append(FileRuling(path.name, number, date))
    return out


def closed_batch_dates(transport) -> list[_dt.date]:
    """The batch clock: the day every `STATE-BATCH-*.md` that reads `CLOSED` was closed. A batch
    that is running, or `FINISHED`, has not closed and ages nothing."""
    folder = Path(transport) / "to-browser"
    days = []
    for path in _transport_files(folder, "STATE-BATCH-"):
        try:
            head = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise TransportUnreadable(f"{path.name} could not be read: {exc}") from exc
        match = _CLOSED_RE.search(_top(head))
        if match:
            day = _parse_day(match.group(1), stamp=True)
            if day is None:
                raise TransportUnreadable(
                    f"{path.name} reads CLOSED {match.group(1)}, which is not a date -- the "
                    "batch clock cannot be trusted")
            days.append(day)
    return days


def ratification_population(transport) -> tuple[list[Path], list[FileRuling]]:
    """`(files, rulings)` of the non-superseded RATIFICATION files -- the population leg (a) reads,
    returned so a report can say HOW MANY it read (an empty read must not look like a clean one)."""
    files = ratification_files(transport)
    return files, [r for path in files for r in file_rulings(path)]


def unlanded_rulings(repo_root, transport, *, grace: int = GRACE_BATCHES,
                     population: "list[FileRuling] | None" = None) -> list[Finding]:
    """R79.3(a): a ruling in a non-superseded RATIFICATION file that is not landed in the register
    and has outlived MORE than `grace` closed batches. Raises `TransportUnreadable` when the
    transport has no `to-browser/` -- the caller reports that as NOT MEASURED."""
    root = Path(repo_root)
    landed = {e.number for e in parse_register(_read_register(root))}
    closed = closed_batch_dates(transport)
    out: list[Finding] = []
    if population is None:
        population = ratification_population(transport)[1]
    for ruling in population:
        if ruling.number in landed:
            continue
        if ruling.date is None:
            # An unknown date cannot excuse an unlanded ruling (exempt forever = forgotten).
            out.append(Finding(
                subject=f"R{ruling.number}",
                evidence=(f"{ruling.file} holds R{ruling.number}, which is not landed in "
                          f"{RULINGS_REL}, and the file has no computable date (a `date: YYYY-MM-DD` "
                          f"header or a dated file name), so its age cannot be shown to be within "
                          f"the grace period. Land it as an entry (`- **R{ruling.number} — "
                          f"<title>**`) with a `Carried by:` line, or date the file.")))
            continue
        passed = sum(1 for day in closed if day > ruling.date)
        if passed > grace:
            out.append(Finding(
                subject=f"R{ruling.number}",
                evidence=(f"{ruling.file} (dated {ruling.date.isoformat()}) holds "
                          f"R{ruling.number}, which is not landed in {RULINGS_REL}, and "
                          f"{passed} closed batch(es) have passed since -- {grace} is the "
                          f"grace period. Land it as an entry (`- **R{ruling.number} — "
                          f"<title>**`) with a `Carried by:` line.")))
    return out


@dataclass(frozen=True)
class RulingsReport:
    """Both legs. `unlanded is None` means NOT MEASURED -- the transport was unreadable."""
    uncarried: list[Finding]
    unlanded: list[Finding] | None
    counts: RegisterCounts
    unmeasured_reason: str = ""
    files_read: int = 0
    rulings_read: int = 0

    @property
    def refused(self) -> bool:
        return bool(self.uncarried or self.unlanded)

    @property
    def passed(self) -> bool:
        """True only when BOTH legs were measured and clean. `not refused` is not this: an
        unmeasured leg is not a refusal and it is not a pass, so a consumer asks `passed`."""
        return self.unlanded is not None and not self.refused

    def render(self) -> str:
        lines = []
        bad = list(self.uncarried) + list(self.unlanded or [])
        if bad:
            lines.append(f"decision-coverage rulings: REFUSED — {len(bad)} ruling(s)")
            for finding in bad:
                lines.append(f"  - {finding.subject}")
                lines.append(f"    {finding.evidence}")
        elif self.unlanded is None:
            # Never a bare OK: leg (a) was not read, so only leg (b) is a measured pass.
            lines.append("decision-coverage rulings: leg (b) OK; leg (a) NOT MEASURED")
        else:
            lines.append("decision-coverage rulings: OK")
        c = self.counts
        lines.append(f"  leg (b) carried: {c.carried} of {c.gated} gated ruling(s) (R"
                     f"{FIRST_GATED_RULING} on) carried; {c.grandfathered} older entr"
                     f"{'y' if c.grandfathered == 1 else 'ies'} counted, not refused")
        if self.unlanded is None:
            lines.append(f"  leg (a) landed within a batch: not measured -- {self.unmeasured_reason}")
        else:
            lines.append(f"  leg (a) landed within a batch: {len(self.unlanded)} unlanded past "
                         f"{GRACE_BATCHES} closed batch(es) -- read {self.rulings_read} ruling(s) in "
                         f"{self.files_read} non-superseded RATIFICATION file(s)")
        return "\n".join(lines)


def rulings_report(repo_root, *, transport=_UNSET, floor: int = FIRST_GATED_RULING) -> RulingsReport:
    """Both legs of the gate, in one place for the CLI, the audit finding and the tests.

    `transport=None` (or a transport with no `to-browser/`) leaves the unlanded leg NOT MEASURED;
    the carried leg needs only the repository and always runs.
    """
    root = Path(repo_root)
    uncarried = uncarried_rulings(root, floor=floor)
    counts = register_counts(root, floor=floor)
    if transport is _UNSET:
        transport = _transport_root()
    if transport is None:
        return RulingsReport(uncarried, None, counts, "the transport is unresolved "
                             "(CLAUDE_PROMPTS_DIR is unset or not a folder)")
    try:
        files, population = ratification_population(transport)
        unlanded = unlanded_rulings(root, transport, population=population)
    except TransportUnreadable as exc:
        return RulingsReport(uncarried, None, counts, str(exc))
    return RulingsReport(uncarried, unlanded, counts, files_read=len(files),
                         rulings_read=len(population))


# --------------------------------------------------------------------------------------- CLI


def _transport_root():
    """The live transport, or None. Isolated so a test can stand in for it."""
    try:
        import gen_handoff as gh  # noqa: PLC0415
        return gh.transport_root()
    except Exception as exc:      # noqa: BLE001 -- a surfacing organ never dies on a boundary
        logger.warning("transport unresolved: %r", exc)
        return None


def _open(args) -> gs.GraphStore:
    """The store, ALWAYS through the freshness check -- `graph_queries._open`'s contract, for
    the same reason: exists is not fresh, and a stale graph does not fail, it answers wrongly."""
    root = Path(args.repo_root).resolve()
    path = Path(args.db) if args.db else gs.store_path(root)
    return gs.ensure(root, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Every accepted decision carries a lifecycle state and an implementing row.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=".", help="repo to read (default: cwd)")
    common.add_argument("--db", default=None, help="store path (default: under the git dir)")
    common.add_argument("--no-transport", action="store_true",
                        help="measure the two in-repo classes only")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", parents=[common],
                           help="refuse on an accepted decision with no row and no disposition")
    check.add_argument("--staged", nargs="*", default=None,
                       help="paths to check (default: git diff --cached)")
    check.add_argument("--no-era", action="store_true",
                       help="leg 1 only -- the commit's own decision files")
    sub.add_parser("ledger", parents=[common], help="emit A9-2's decision ledger (writes nothing)")
    sub.add_parser("metrics", parents=[common], help="emit A9-3's four numbers")
    sub.add_parser("rulings", parents=[common],
                   help="refuse while a ratified ruling is unlanded past one batch, or landed "
                        "with neither a row nor a 'no implementation required' (R79.3, [#721])")

    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve()
    transport = None if args.no_transport else _transport_root()
    if args.command == "rulings":
        # The register leg reads files, not the graph store: no `_open` (a stale-store rebuild
        # would cost seconds a register read does not need), and its own transport judgement.
        try:
            report = rulings_report(root, transport=transport)
        except PopulationUnreadable as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
        print(report.render())
        if report.refused:
            return 1
        # 2 = leg (a) NOT MEASURED because the transport could not be read; `--no-transport` is the
        # operator's explicit choice to skip it, so that stays 0.
        return 2 if report.unlanded is None and not args.no_transport else 0
    try:
        store = _open(args)
    except gs.StoreUnreadable as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1

    try:
        if args.command == "check":
            findings = decision_coverage(root, store, staged=args.staged, transport=transport,
                                         era_leg=not args.no_era)
            stale = stale_dispositions(decisions(root, store, transport=transport))
            if stale:
                print("decision-coverage: NOTE — dispositions naming decisions that are gone: "
                      + ", ".join(stale))
            if not findings:
                print("decision-coverage: OK")
                return 0
            print(f"decision-coverage: REFUSED — {len(findings)} decision(s)")
            for finding in findings:
                print(f"  - {finding.subject}")
                print(f"    {finding.evidence}")
            return 1
        found = decisions(root, store, transport=transport)
        print(render_ledger(found) if args.command == "ledger" else metrics(found).render())
        return 0
    except PopulationUnreadable as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
