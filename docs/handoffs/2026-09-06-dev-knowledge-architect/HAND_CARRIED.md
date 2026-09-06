## Hand-carried section — the v7.1 deltas applied MANUALLY, this once

> **Why this section exists and what it is not.** Intake `#68` (the v7.1 amendment pack) is
> **DRAFT and unratified**. Nothing here is a version bump, and no seat may cite this section as
> evidence that v7.1 is live. It is the outgoing seat carrying, by hand, the four deltas whose
> absence was measurably paid for last window — deltas 1 (Done-when verbatim), 5 (live-session
> census), 7 (scorecard) and 11 (transport in the interface section). Ratifying them is agenda
> row 1 below, and this section is an argument for them, not a pre-emption of the ruling.
>
> **Counts live HERE, deliberately.** `gen_handoff`'s answer-free invariant bars counts, SHAs,
> verdicts and date-relations from `HANDOFF_BOOT.md`, `RESIDUAL.md` and `PROBES.md`, because the
> browser seat cannot verify them. `SUPPLEMENT.md` is the fill target and is not covered.

---

# 0 · READ FIRST — the agenda this seat was handed is NOT the newest operator direction

This bundle was commissioned against architect-inbox item **021**. Three later items —
**022, 023 and 024**, all written 2026-09-05 late — are sitting UNCONSUMED in `to-cc\`, and they
change the agenda rather than adding to it. They are deliberately **NOT archived** by this window's
retention pass (§7 of the brief), because they are the next window's input.

**022 · Next window = night research + the VISIBLE batch, and the day's ordering is REVERSED.**
*"it reverses the day's ordering — VISIBLE surfaces first, gates second."* It defines an overnight
file-by-file research arc over the Architekt Jutra corpus **and the operator's master's thesis**,
answering one strategic question — how Maister DEPLOYS to a project versus our carrier, and whether
each consumer repo runs its own CC sessions independently or work must route through the hub — as a
**decision memo with trade-offs measured on fleet-readiness §0**, not as opinion. It also names a
five-lane VISIBLE batch (V1 release commit · V2 `logs/` retention witness · V3 `ecosystem/`
migration · V4 archive bundles · V5 BACKLOG closure pass).

**022-B CONTAINS A RULING REVERSAL THAT LANDS DIRECTLY ON ROW 2 BELOW**, verbatim:

    V1 release commit v1.5.0: CLAUDE.md first-read ESSENTIALS line removed (hub region
    regeneration, fleet-coupled by construction) — architect ruling reversed: the tag waits
    on NC1 only.

**023 · Universalization is DEFINED by the operator, and it supersedes the architect's earlier
formulation.** *"Universalization = ONE pattern of SHAPE for every repo … Content stays each repo's
own; SHAPE is identical."* It states in its own words that the architect's earlier note *"floor
conformance, not sameness"* (in `ARCHITECT-INBOX-2026-09-05-009.md` and the fleet-readiness
contract) **is CORRECTED**: sameness of shape is the goal; sameness of content is not. The mechanism
is to universalize the EXISTING hub seal (`validate_hermetization` tree-seal, ADR-101), shipped to
consumers in REPORT mode first, then armed.

**023 also amends the H0 runbook quoted in Row 3:** *"H0 runbook (fleet-readiness §4) STARTS with
the seal report on corp-monorepo — before any region or hook lands — so the operator sees the root
list first."* The runbook as merged does not have that step.

**024 · Universalization scope + the packaging rule.** Enumerates what must be universal, then rules
the shape of it: *"At this scale NOTHING may be a per-repo act. Every element above is a COMPONENT
with a version in the deploy manifest, shipped by the carrier, with a drift check on both sides and
a per-consumer waiver."* It re-frames the derived-copies registry (candidate (c)) as *"not hygiene —
it is the inventory of components"*, and proposes a **floor staging for the operator's ruling**:
v1.5.0 = shape seal + regions + hooks + plugin + waivers + freshness registry (j) + roles table
(008), *"enough for H0 on corp-monorepo"*; v1.6 = Python stack, TRACE store, scorecard; v1.7 =
telemetry/dashboards, routing carried. Sending everything at once is *"refused on evidence (G3b: a
hub-shaped gate would have blocked every commit in three consumers)"*.

**Consequence for the sitting.** Row 1's ratification list (021-B) and Row 2's tag gate were written
before 022–024 existed. The operator should rule on which agenda governs BEFORE working the rows
below, because 022 reverses the ordering and 024 proposes putting the roles table (008) and the
freshness registry (j) *into* floor v1.5.0 — which are items 021-B lists as merely awaiting
ratification.

---

# 1 · AGENDA — in order, each row with its acceptance condition VERBATIM (delta 1)

**The rule this section obeys.** Delta 1 says the closure source is the row's own `Done when:`
text, never a defect narrative sitting next to it. Where a row HAS no `tasks/` entry, this section
says so in that many words rather than paraphrasing a summary into something that looks like an
acceptance condition. Three of the five rows below have no `tasks/` row, and that absence is
itself an agenda item.

## Row 1 · The ratification sitting (021-B) — eight items, and only five exist

**Acceptance condition: NONE EXISTS.** This is an operator sitting, not a backlog row; there is no
`tasks/` entry and therefore no `Done when:` to quote. The condition is the operator's word:
ACCEPT / DEFER / REJECT on each item.

**Read this before the sitting opens.** 021-B names eight items as "Intakes now DRAFT". Measured
against `docs/intake/` on `main`, **five are DRAFT intake files and three are not intakes at all**:

    #68  handoff-process v7.1 amendment pack ... DRAFT  docs/intake/2026-09-05-tech-handoff-process-v71-amendment-pack.md
    #69  boot_frontier prioritisation weights .. DRAFT  docs/intake/2026-09-05-tech-boot-frontier-prioritisation-weights.md
    #70  AJ second pass ....................... DRAFT  docs/intake/2026-09-05-tech-aj-second-pass.md
    #70  session roles with a carrier (008) .... DRAFT  docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md
    #71  batch P — audit-gate speed ............ DRAFT  docs/intake/2026-09-05-tech-batch-p-audit-gate-speed.md

    transport v2 (017) ...... NO INTAKE FILE. Its content is already LANDED in
                              protocols/OPERATOR-INTERFACE.md §1 ("Transport v2 — schema,
                              grammar, retention"), filed DONE at 81bc39f9 by FILINGS-1.
    rate-limit pause (019) .. NO INTAKE FILE. Exists only as to-cc\ARCHITECT-INBOX-2026-09-05-019.md.
    questions-as-files (020)  NO INTAKE FILE. Exists only as to-cc\ARCHITECT-INBOX-2026-09-05-020.md.

**Two consequences the sitting has to decide, not discover.** (i) 017 cannot be "accepted as an
intake" because there is none — the operator is either ratifying a protocol edit already on `main`
or filing it retroactively. (ii) 019 and 020 have no funnel object at all; ADR-111's only path to a
row is CANDIDATE to intake to ratification, so ruling ACCEPT on them today ratifies something with
no citable handle.

**`#70` IS A LIVE ID COLLISION, and its locus was itself mis-stated once.** Two source files each
declare `intake-id: 70` in frontmatter (`2026-09-05-tech-aj-second-pass.md` and
`2026-09-05-tech-session-roles-with-a-carrier.md`); max id is 71. ERRATUM 1 on the R5P close packet
placed the collision in `docs/intake/README.md` — that file is GENERATED
(`scripts/gen_intake_index.py`, hook `intake-index-freshness`) and was faithfully rendering two
sources, so repairing it would regenerate straight back. **ERRATUM 2 corrects this**; the fix must
land in one of the two files' frontmatter. Filed as CANDIDATE **R5P-C2**, deliberately UNREPAIRED —
renumbering a live citation handle is not an integrator's unilateral act at batch close.

## Row 2 · Tag gate v1.5.0 — the agenda names THREE conditions; the checklist carries FIVE

**Acceptance condition, VERBATIM from `docs/audits/2026-09-05-technical-v150-tag-checklist.md`**
(the container inbox item 012-C specifies, and the only place the gate is enumerated):

    | # | Gate                                                                                    | State |
    | 1 | ship-gate reports 0 hard-fail and 0 undispositioned at `main`                           | OPEN  |
    | 2 | `CLAUDE.md` first-read ESSENTIALS line removed in the release commit (`[#628]` closure) | OPEN — deferral recorded |
    | 3 | doc-counts in sync via the commit-gate derivation (R5P L2)                              | OPEN  |
    | 4 | fleet-readiness §4 runbook merged with the local amendment                              | OPEN  |
    | 5 | the release commit is the ONLY commit touching hub regions and the manifest version together | OPEN — one nearby act cleared |

Its own status banner, verbatim: **"Status: NOT EXECUTED. This file is the checklist, not the tag.
It is created empty-by-design and filled as each witness lands. The operator declares the tag on
this checklist — no seat flips it, and a gate is not satisfied because the work behind it looks
done."**

**The discrepancy, stated as a mapping rather than as a complaint.** The agenda handed to this seat
names the gate as "NC1 + NC3 + NC6". By TEXT those map exactly onto gates **1, 2 and 3**:

    "NC1 ship-gate 0 hard-fail + 0 undispositioned"           == gate 1
    "NC3 CLAUDE.md first-read ESSENTIALS line ... ([#628])"   == gate 2
    "NC6 doc-counts"                                          == gate 3

**Gates 4 and 5 appear on no version of the agenda.** All five are OPEN. If the sitting rules "tag
when NC1/NC3/NC6 are green", it green-lights a tag with two of its own declared conditions
unexamined.

**THERE ARE THREE LIVE ENUMERATIONS OF THIS ONE GATE, and they do not agree.** Listed oldest to
newest, because the newest is a reversal and reversals are exactly what a summary loses:

    (i)   the CHECKLIST     five gates, all OPEN     docs/audits/2026-09-05-technical-v150-tag-checklist.md
    (ii)  the AGENDA        NC1 + NC3 + NC6          021 / browser-seat notes §5
    (iii) item 022-B        "the tag waits on NC1 only — architect ruling reversed"

If (iii) governs, gate 2 (`[#628]`, the ESSENTIALS line) moves OUT of the tag's preconditions and
INTO the release commit itself as lane V1 — which is what 022-B actually describes. That is a
different act from "close `[#628]` before tagging", and only the operator can say which is meant.

**This seat does not rule which enumeration governs — that is the operator's.** What it will say
plainly: the three lists are not the same list; the checklist is the one with a recorded
owner-instruction behind it; and 022-B is the newest and is explicitly a reversal. **Ruling on the
tag from the agenda alone would rule from the middle version of three.**

**`NC` IS A CROSS-NAMESPACE COLLISION, live tonight.** A bare `NC3` resolves into two unrelated
lists: this tag gate, AND the AJ second-pass lane contract's own NC1–NC6 non-negotiables
(`docs/audits/2026-09-05-technical-aj-second-pass-lane-contract.md`, where NC3 is "the seeded task
is identical text for both legs"). This is the same class ERRATUM 2 isolated for `E-NN` vs `#NN`,
and it wants the same remedy: **qualify the citation with its path.** ERRATUM 2's own evidence for
this is worth copying — AMENDMENT 9 survived the `#70` collision only because it cited number *and*
path.

**Ownership.** Gates 1, 3, 4 and 5 are UNOWNED. The checklist says so in its own words: *"Creating
the container is not claiming the item — gates (1), (3), (4) and (5) are unowned and need an
operator word."*

**`[#628]` is gate 2's row and it DOES have a `Done when:`. Verbatim from
`tasks/628-dc2-recut-essentials-dissolution-is-a-release-act.md`:**

    Done when: a frozen contract exists whose write-scope covers all ten consumers plus the floor
    sidecar and every pinned manifest; the ADR-88 register entry's justification is re-based or the
    entry re-pointed; `canonical_docs.py`'s five memberships move together with
    `canonical_freshness_gate.py:49`'s consumer-standalone fallback list; and the three tolerant
    readers (`canonical_freshness_gate:124`, `validate_doc_structure:319`, `validate_doc_rot:397`,
    all verified to skip on absence) are confirmed still tolerant after the move

Note what that condition is NOT: it is not "delete the line". The row is **DE-BLESSED** — the
mechanical dissolution is all that remains — but its Done-when still requires a frozen contract
covering ten consumers, the floor sidecar and three pinned manifests, because a floor edit is a
release act by construction (`deploy/release_lint.py` C5 asserts a three-way hash equality).

## Row 3 · H0 — corp-monorepo attended

**Acceptance condition: no `tasks/` row exists.** The runnable condition is the runbook's own
closing sentence, verbatim from `docs/audits/2026-09-05-technical-fleet-readiness.md` §4:

    **corp-monorepo will still read FAIL** — CM-4 (14 ADR-grammar defects) and CM-5 (substrate
    registry) are untouched by this runbook and are separate arcs. H0 is complete when those three
    rows clear, not when the repo turns PASS.

("those three rows" = CM-6 freshness re-stamp, CM-7 malformed `reconciled_with`, CM-8 dead worktree
prune.) Seven steps, each ending in an exact command and the witness that proves it landed.

**Three facts that change how this row is planned, all verbatim from §4:**

- **"Target is `v1.4.0`, not v1.5.0."** v1.5.0 is an untagged release candidate and
  `deploy/tool.py`'s preflight requires the tag to resolve before `--execute`. **So H0 does not
  depend on the tag** — which is what makes the agenda's tag-before-H0 ordering safe, and it is
  worth stating because gate 4 above points the other way round.
- **"Substrate: LOCAL."** None of this runs in the cloud (wall B1.2).
- **Step 0 is a RULING, not a command:** *"ADR-102 / #336 ruled corp-monorepo stays at v1.2.0 …
  This step is an operator ruling, not a command. If the answer is 'hold at v1.2.0', steps 3–5 drop
  and steps 1, 2, 6, 7 still stand on their own."* The sitting needs to answer Step 0 before H0 is
  dispatchable at all.

Amendments 1–3 to that audit are landed and renumbered by supersession, not by edit.

**AND A FOURTH STEP THAT IS NOT IN THE MERGED RUNBOOK.** Item 023 adds a new first step, verbatim:
*"H0 runbook (fleet-readiness §4) STARTS with the seal report on corp-monorepo — before any region
or hook lands — so the operator sees the root list first."* The runbook on `main` begins at Step 0
(the v1.2.0-hold ruling) and has no seal-report step. Whoever dispatches H0 must reconcile the two
BEFORE freezing a contract, or the lane will execute a runbook the operator has already amended in
`to-cc\`. This is the same failure class as ruling the tag from the middle of three enumerations.

## Row 4 · AJ second pass (`#70`) — the result, read BEFORE any AJ candidate is ratified

**Acceptance condition: no `tasks/` row.** The deliverable is the artifact, and it is **MERGED TO
`main` during this session** at `8f5bcda2` (lane commits `5f02a502`, `0e56457f`), resolving at
`docs/audits/2026-09-05-technical-research-aj-second-pass.md`, and delivered to `to-browser\`.
The lane was pre-anchored before the merge, per the standing order to anchor BEFORE and never
after.

**The headline, verbatim: "6.4× the wall-clock and 16.2× the cost, for the same verdict on the same
task."** Leg M (Maister) 7809 s / 2 h 10 m 09 s plus ~732 s of `/maister:init`; Leg D (our lane
contract) 1225 s / 20 m 25 s. Neither leg regressed the suite (M +8, D +4, same five pre-existing
failures).

**021-D says the Maister outcome must be read before any AJ candidate is ratified. It has been, and
the decision table's own verdicts are the reason:** most rows come back **ALREADY-RUNNING** — often
with ours the stronger leg (clarifications: *"theirs records answers; ours **fails** when the repo
contradicts one"*). Only **two** rows are ADOPT-INTO-HUB, both narrow: **C-1** cost-per-command as
an architecture signal, and **C-3** a "where is this task now" run-state view. One row is **REJECT
as framed** (per-loop trace inspection — *"Maister does not have it either"*).

The finding that should shape the routing ruling in §5.2 below: leg M *"ran **entirely on
`claude-opus-5`**: 123 turns, 14 subagents, one model class, no cheap tier"* — *"an unrouted harness
billed $48.53 doing an S row on the most expensive model."*

## Row 5 · Batch P (`#71`) — audit-gate speed

**Acceptance condition: no `tasks/` row.** Intake `#71` is DRAFT
(`docs/intake/2026-09-05-tech-batch-p-audit-gate-speed.md`), filed by FILINGS-3 as inbox item
004-A.2, and it *"open[s] with a RECONCILE-BEFORE-BIRTH table against intake #54"*. It is a batch
proposal awaiting ratification, so its condition is the sitting's word, not a measurement.

Governing datum, from the R5P close packet: `audit.py health` runs **35.2 s ± 0.15 (n=3)** — and
that number is **hand-counted, not organ-computed**: the command prints no timing at all.

---

# 2 · LIVE-SESSION CENSUS (delta 5) — as of this cut

**Why delta 5 exists, in the outgoing seat's own words:** *"The bundle tells me which session holds
the primary checkout and which worktrees are live and whose. I do not allow six concurrent writers
into one checkout until a TOCTOU puts a commit on main under a passing gate."*

**The primary checkout is INTEGRATOR-ONLY.** That is a standing notice from INTEGRATOR-2, and it
held tonight: this seat needed the primary to cut and **asked for it rather than switching HEAD**.

**Registered worktrees at this cut: the primary only.** `aj-second-pass` was the last one and was
released during this session (below). Directory husks remain — they are inert, carry no `.git`, and
do **not** block a handoff cut; only *registered* worktrees do.

**Status boards in `to-browser\` at this cut** — the read surface, per 017-E:

    STATUS.md ............. FILINGS-1. "Every item I own is DONE. The branch is RELEASED."
    STATUS-FILINGS-3.md ... FILINGS-3. Branch MERGED at 128c660b; working tree clean.
    STATUS-INTEGRATOR.md .. INTEGRATOR-2. Batch R5P CLOSED; erratum branch landed.

**`SESSION-*.md` files: NONE EXIST.** 021-C's census delta asks for `STATUS*.md` **and**
`SESSION-*.md`. The `SESSION-<name>.md` mechanism is item **020-A** — a proposal for the Stop hook
to write one per session — and it is **unratified and unbuilt**. Their absence is not an omission
by this seat; it is the state of a mechanism the sitting is being asked to rule on.

**Two live inter-seat facts recorded because no organ computes them:**

- `worktree-aj-second-pass` was **released on its seat's word during this session**, at this seat's
  request, after the cut refused over it. The seat exited the worktree FIRST, then deregistered —
  and left **no husk**. Branch preserved, unmerged, for the integrator.
- Both of that branch's commits carry a **declared `SKIP=audit-health` bypass**, stated in each
  commit body, because at its branch point `main` carried 18 unanchored first-parent merges. The
  integrator has accepted that defect as **its own backlog, not the lane's** — a lane cannot write
  JOURNAL entries (STANDING_RULINGS P-1), so the lane had no remedy available.

---

# 3 · INTERFACE — the constants a seat acts on

**Transport (OPERATOR-INTERFACE §1; delta 11).** The pointer, not a copy — the browser's memory
entry is a CACHE of §1, never its source.

    prompts dir  : $env:CLAUDE_PROMPTS_DIR (User scope). THE VARIABLE IS THE SOURCE. A seat that
                   hardcodes a path has substituted a fact it cannot keep current for one it can
                   resolve. Currently a Drive-for-Desktop folder the browser reads via the connector.
    to-cc\       : browser -> CC. Contracts, pastes, ARCHITECT-INBOX-<date>-<NNN>.md
    to-browser\  : CC -> browser. Delivered artifacts + inbox copies with a DONE <sha> line per
                   item — the browser's ONLY witness that an item ran
    read rule    : prompts dir FIRST; if absent there, ~\Downloads and its to-cc\ / to-browser\
                   (fallback per FILE, not per variable)
    copy header  : every to-browser\ copy opens with
                   <!-- COPY OF <repo path>@<sha> - generated, never edited; the repo is the source -->
    session start: every CC session RESOLVES the prompts dir from User scope and prints it on boot,
                   overriding a differing process value

**The variable genuinely has two live values, and it bit tonight.** User scope resolves to the Drive
channel; a session started earlier inherits `C:\Users\1028120\Downloads`. A seat that reads the
inherited value finds `to-cc\` present but EMPTY and reads that as "nothing filed" rather than as a
misresolved variable — *the fallback directory EXISTING is what makes the failure silent.*

**§7 — copy-ready blocks.** *"Every step that requires the operator's action ends with a copy-ready
block — the exact shell command(s) or the exact CC paste — never a description of what will happen.
A description where a block belongs is an interface defect."*

**RATE-LIMIT PAUSE (019) — the copy-ready block itself:**

    FREEZE UNTIL RESET. Run ONE background command and do nothing else until it completes:
    powershell -NoProfile -Command "$r=Get-Date '<HH:MM>'; if((Get-Date) -gt $r){$r=$r.AddDays(1)};
    while((Get-Date) -lt $r){Start-Sleep -Seconds 60}; 'RESET REACHED'"
    When it completes, continue EXACTLY where you stopped, without re-planning.

`<HH:MM>` = reset time **+ 2 min**, on the clock of the machine the session runs on (cloud: container
clock, UTC). Paste to the integrator FIRST; stagger by ~30 s so wake-ups do not burst. **A sleeping
tool call spends no usage, and extra-usage credits are not consumed while frozen.** Witnessed
2026-09-05: six sessions frozen, all resumed where they stopped.

**Inbox grammar (017).** Every item carries frontmatter — `repo:` · `owner-role:
filings|dispatcher|integrator` · `files: [footprint]` · `gate: <none | DECLARE-<item>>` ·
`depends: [items]`. **Ownership and gates live in the FILE, never in a chat paste** — a chat paste
is not addressable, so two sessions handed overlapping work cannot detect the overlap and the first
evidence is a merge conflict or a doubled filing. Names: `INBOX-<repo>-<YYYY-MM-DD>-<NNN>.md` ·
`DECLARE-<item>.md` · `STATUS-<repo>.md`. **`STATUS-<repo>.md` is the read surface; the DONE copies
are the audit trail; there is no third ledger.**

**FILINGS standing-session paste** — the shape a FILINGS seat boots with: it owns only the items
whose frontmatter names its role, edits only its own section of `STATUS-<repo>.md`, writes a
`DONE <sha>` copy into `to-browser\` per item (without which, from the browser's side, the item did
not run), and routes a candidate belonging to another lane to that lane rather than filing it.

---

# 4 · POINTERS — read at the source, not restated here

    browser-seat notes + amendments . docs/audits/2026-09-05-technical-browser-seat-notes.md
                                      (ERROR REGISTER E-01..E-25 at §1; six amendments, one of
                                      which WITHDRAWS an earlier defence)
    batch-G close packet ............ docs/audits/2026-09-02-technical-batch-g-close-packet.md
                                      (§11 = the proposed H order; see §5.1 below)
    batch-R5P close packet .......... docs/audits/2026-09-05-technical-batch-r5p-close-packet.md
                                      (+ ERRATUM 1 and ERRATUM 2, both APPENDED, not edited)
    R5 sheet + R5-DECLARED .......... docs/audits/2026-09-05-technical-r5-disposition-sheet.md
                                      docs/audits/2026-09-05-technical-r5-funnel-disposition-ledger.md
    fleet-readiness + 3 amendments .. docs/audits/2026-09-05-technical-fleet-readiness.md
    AJ gap analysis ................. docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md
    AJ second pass (the RESULT) ..... docs/audits/2026-09-05-technical-research-aj-second-pass.md
    Python quality/speed research ... docs/audits/2026-09-05-technical-research-python-quality-speed.md
    corpus-coherence audit (Gemini) . docs/audits/2026-09-05-technical-corpus-coherence-gemini.md
    #627 verdict .................... docs/audits/2026-09-05-technical-627-readjudication.md
    v1.5.0 tag checklist ............ docs/audits/2026-09-05-technical-v150-tag-checklist.md
    batch-H0-PREP close packet ...... docs/audits/2026-09-05-technical-batch-h0-close-packet.md
                                      (written during THIS window — see §5.6)

## 5.6 · H0-PREP was closed tonight, without an operator instruction — read this deliberately

**What happened, and why it is flagged rather than buried.** The handoff cut refused a second time,
on `OpenBatchError`: `gen_handoff` will not cut ANY bundle while a batch is open, and H0-PREP was
open. Its three committing lanes were all merged (`c710ece0` L5, `62ec945c` L4, `b3326083` L3) —
verified independently by two seats — so **only its close packet was unwritten**. An unwritten
packet was therefore blocking every handoff in the repository.

The handoff seat wrote it and INTEGRATOR-2 reviewed and merged it, on the joint judgment that the
packet was **owed work rather than a formality manufactured to open a gate**. The test both seats
applied first: had any lane been unmerged, the handoff would have been reported as owed instead.
**This is recorded for the operator to revisit, not presented as settled.**

**Its hard metric contradicts what both seats initially expected: ROWS CLOSED = 0.** Measured per
id, not inferred from a merged lane — `[#528]` open (its lane calls itself "one narrow leg … not a
closure of it"), `[#634]` open (re-scoped), and `[#66]` **is not a backlog row at all** but an
intake id carried in `[#id]` bracket notation.

**Four CANDIDATES were carried, none filed as rows:**

    H0-C1  an unwritten close packet silently blocks EVERY handoff in the repo, and the
           refusal names the batch rather than the missing act
    H0-C2  a handoff cut cannot be taken from a worktree, so "never the primary" is
           unsatisfiable for that one act
    H0-C3  [#66] — an intake id in backlog-row notation. Distinct from R5P-C2's allocation
           race: that needs an allocator, this needs QUALIFIED CITATIONS (number AND path)
    H0-C4  [#634]'s title asserts a defect narrower than the row's re-scoped content, so a
           reader who resolves only the title misreads a live P1

## 5.7 · FOUR REVIEW FINDINGS ON THE AJ SECOND-PASS AUDIT — merged unacted-on, deliberately

INTEGRATOR-2 raised four findings in pre-merge review of lane-s's audit and **merged without acting
on them**, because the lane had exited and rewriting another seat's audit is producing, not
integrating. That reasoning is carried here with the findings, because it is the reason they are
still open:

    HIGH  the "live head-to-head" is ASSERTED, NOT AUDITABLE. Task, run artifacts, metrics and
          teardown evidence are cited only as bare filenames or placeholders (SEEDED-TASK.txt,
          FR2-*, DEVIATIONS.md, TEARDOWN.md, "the arc's scratch") and NONE is in the commit
          tree. The 6.4x / 16.2x conclusion has no resolvable evidence after teardown.
    MED   several proposals read ADOPT-INTO-HUB while calling themselves candidates — a
          candidate recommends; it cannot decide adoption before intake
    MED   the header's `Intake: #70` is not resolvable — independently corroborating R5P-C2
    LOW   a bare "73 committed SUPPLEMENT.md" count with no computing surface

**This lands directly on Row 4 of the agenda.** The AJ result is the input 021-D says must be read
before any AJ candidate is ratified — and its headline number is, per the integrator's HIGH finding,
**unverifiable from the tree**. The lane's scratch evidence (64 files) survives OUTSIDE the repo at
`Downloads\aj-scratch\second-pass-evidence\`, so the claim is checkable by a seat with disk access
and not by the browser. **Whether an erratum is owed on that audit is the architect's call, not a
seat's** — it is put to the sitting rather than ruled here.

---

# 5 · OPEN JUDGMENTS THE NEXT SEAT INHERITS (021-D) — explicitly, and one premise corrected

## 5.1 · The H order — operator has NOT ruled

Verbatim from the batch-G close packet §11, *"THE ARCHITECT'S PROPOSED H ORDER — for the operator's
ruling"* (note: **batch-G's** packet, not R5P's):

    The architect proposes, and this packet does not decide: **(g) the Gemini/agy whole-corpus
    doctrine-coherence audit first**, because it is retrieval-only and its output re-prices
    everything after it; **then H0 with the monorepo attended**; **then the TRACE layer**, which is
    the declared precondition for the prompt-distiller and dashboard asks both (a trace has nowhere
    to land until `logs/prompts/` exists); **then the derived-copies registry** (candidate (c)) …
    **then the rest**. Candidates (a) README front door, (g) corpus audit and (j) per-consumer
    freshness registry are each flagged **H0 PRECONDITION**.

## 5.2 · agy / Gemini role after `#627` — THE INHERITED PREMISE IS WRONG

**021-D says "#627 FLIP-TO-ADMIT". The artifact says the opposite.** Verbatim from
`docs/audits/2026-09-05-technical-627-readjudication.md`:

    ## VERDICT
    **RATIFY REFUSE — and reclassify what is being refused.**
    … Correcting every defect moved the verdict **further from ADMIT, not closer**.

**What actually flipped is the CLAIM, not the outcome** — and the distinction is the whole routing
decision:

    So: refused, but as *not admissible under the harness as issued* — not as a liar.

Batch-F refused agy as an untrustworthy analyst (fabrication, both absolute honesty gates). *"That
characterisation is wrong on the evidence. agy fabricated almost nothing: the quotes it was failed
for are byte-accurate text from real files it named out loud. The defect is **scope binding**, it is
**deterministic**, it has a **named location on disk**."* A deterministic, localised harness defect
is fixable; a fabricating model is not — so the routing-table question is live, but it is *"is the
harness defect fixed?"*, **not** *"was agy admitted?"*. `[#627]` stays OPEN.

**Do not collapse "agy" and "Gemini" into one row.** Item 022-C carries them forward separately and
as settled, verbatim: *"Gemini: admitted as reader with mandatory verification (2026-09-05). Grok:
not admitted (needs seeded-defect admission)."* So the provider question the next seat inherits is
narrower than 021-D's phrasing suggests: Gemini's reader role is **decided**; what is open is agy's
harness defect and the routing-table row that depends on it.

## 5.3 · Maister outcome — READ, and it is in Row 4 above

Two narrow ADOPT-INTO-HUB candidates (C-1 cost-per-command, C-3 run-state view); the rest
ALREADY-RUNNING or REJECT-as-framed. No AJ candidate should be ratified without Row 4's cost datum.

## 5.4 · The two pre-existing REDs + the spine-predicate lane (after the tag)

From the R5P close packet, **attributed, not totalled**: the 7 `governance_health` failures are
pre-existing (files untouched, last changed `28bb3002`); `test_batch_manifest` fails on **H0-PREP's**
name, not R5P's. From FILINGS-3: `test_consumer_at_landing` and `test_funnel_coverage` are both
FOREIGN to its lane, and `ecosystem/audit-consumer-baseline.json` was **deliberately not
regenerated** — that would rebase the ratchet and silently absorb 25 artifacts.

## 5.5 · Still needing an operator word, carried from the boards

1. **015-C** — the integrator DECLINED the route, correctly (it is declining the route, not the
   ruling). *"One word from you executes it."*
2. **`consumer_at_landing` cannot be closed from a ledger row** — a mechanism fact, not incomplete
   work: `funnel_coverage` reads the disposition ledger, but `consumer_at_landing` asks whether a
   governance POOL file cites the artifact, and `docs/audits/` is not in `POOL_DIRS`. Clearing it
   needs a POOL-SIDE citer. Wants its own ruling.
3. **UNOWNED items** — `007`, `004-A.2`'s successor scope, `012-C` gates 1/3/4/5, and inbox `014`
   (board-assigned, no brief; **no owner was invented**).
4. **Candidate (l)** is cited twice and has never been filed.

---

# 6 · SCORECARD (delta 7) — ten numbers, each marked for provenance

Carried from the R5P close packet §6, **which marks every number for how it was obtained**. Session
span `3200757d..HEAD` at the R5P close. Reproduced rather than re-measured, and *not* re-stamped to
this cut — several have moved since (more worktrees torn down; fewer husks).

    rows closed                       0      organ-computed  window_metrics.py
    net backlog delta                 0      organ-computed  window_metrics.py (224 -> 224)
    paste / boot bytes vs budget  17364      organ-computed  window_metrics.py (96% of 18000)
    audit checks                     54      organ-computed  gen_doc_counts.py --check
    pre-commit hooks                 23      organ-computed  gen_doc_counts.py --check
    pytest collected               4992      organ-computed  gen_doc_counts.py --check
    suite result           21F / 4967P       organ-computed  pytest -q, 1310.50 s, idle tree
    audits corpus                   897      organ-computed  gen_audit_index.py
    spine merges landed              43      hand-counted    git log --first-parent 3200757d..HEAD
    audit.py health wall-clock    35.2 s     hand-counted    3 timed runs; the command prints no
                                                             timing, so the mean and the +/- 0.15
                                                             are the integrator's

**Read the `window_metrics.py` zeros correctly.** They are CORRECT for the range the organ declares
(`origin/main..HEAD`), which was empty because every merge of the day had already been pushed. *"The
reason is the measurement conditions, not a standing property."* That correction is ERRATUM 1's, and
the erratum is explicit that the 21/4967 aggregate is **NOT** re-measured on the landed tree.

---

# 7 · WHAT THIS BUNDLE CORRECTS, so the next seat does not re-derive it

1. **`#627` did not flip to ADMIT.** It RATIFIED REFUSE and re-classified the reason (§5.2).
2. **The tag gate has five conditions, not three** (§1 Row 2), and `NC` is a cross-namespace
   citation hazard.
3. **Three of the eight ratification items are not intakes** (§1 Row 1), and `#70` names two files.
4. **`SESSION-*.md` does not exist** because the mechanism that would write it is unratified (§2).
5. **A handoff cut cannot be taken from a worktree.** `gen_handoff.assert_boundary_hygiene` refuses
   over ANY linked worktree and has no override flag, so a brief instructing a seat to "work in your
   own worktree, never the primary" is **unsatisfiable for a handoff cut** — provisioning the
   worktree blocks the gate the cut needs. Witnessed and worked around tonight by asking the holding
   seat to release and the integrator to hand over the primary. **CANDIDATE-shaped; not filed as a
   row.**
6. **`ExitWorktree` with `action: "remove"` deletes the worktree AND its branch**, with no way to
   keep one without the other — on an unmerged branch it silently drops the commits. Use
   `action: "keep"` and deregister by hand. This is also why the safe teardown leaves a husk.
7. **The commissioned agenda is one revision behind the operator** (§0). Items 022–024 postdate it,
   reverse its ordering, reverse the tag ruling, define universalization and amend the H0 runbook.
   They are LIVE in `to-cc\` and were deliberately left out of the retention sweep.

---

## Retention performed at this wrap (017-D), stated so the next seat can trust the directory

**Archived** to `to-browser\archive\2026-09-05\`: consumed inbox items (through 021) and the
delivered artifact copies whose arcs closed this window.

**Deliberately LEFT at the top level**, each for a stated reason:

    STATUS.md · STATUS-FILINGS-3.md · STATUS-INTEGRATOR.md .. the read surface (017-E)
    PASTE_THIS.md · HANDOFF_BOOT-<slug>.md ................. this bundle's boot
    2026-09-05-technical-research-aj-second-pass.md ......... the AJ deliverable, per the brief
    ARCHITECT-INBOX-2026-09-05-022/023/024 ................. UNCONSUMED — next window's input

A retention pass that swept 022–024 would have archived the operator's newest direction on the
night it was written. That is the failure this note exists to prevent.
