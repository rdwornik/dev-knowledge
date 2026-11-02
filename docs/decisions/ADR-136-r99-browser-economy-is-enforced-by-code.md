# ADR-136: R99's browser economy is enforced by code — the LEDGER, one generated rollup and the map diff, at most 20 KB, regenerated after every main push

- **Status:** Accepted (ADR-94; ratified: to-cc/GO-E3.1.md (operator, 2026-11-01))
- **Date:** 2026-11-01
- **Origin:** /decide run E31-C, revision 3; challenged by CC (R41, 2026-11-01); ratified in `to-cc/GO-E3.1.md` (= `to-browser/RATIFICATION-2026-11-01.md`).
- **Numbering:** PROPOSAL-ADR-STAGE-PHASE = ADR-134, PROPOSAL-ADR-GIT-MEMORY = ADR-135, PROPOSAL-ADR-BROWSER-SURFACE = ADR-136, PROPOSAL-ADR-READ-FORMAT = ADR-137, ADR-124 stays ADR-124. Where the text below names a proposal, read its ADR number.
- **Decision tier:** Path A — operator ratification.
- **Implements:** R99 §3 "Browser economy" (`protocols/STANDING_RULINGS.md:6497-6499`). R99 is not amended.
- **Amends:**
  - the boot's reading path (HANDOFF_BOOT items 1-5, via the handoff update);
  - `scripts/handoff_state.py` READING_PATH (`:915-921`);
  - the cut's read set and its 40 KiB budget (`scripts/gen_handoff.py:4461`, `:4503-4538`).
- **Fits:** T1 light, "a bounded fix or extension inside an existing organ" (`protocols/STANDING_RULINGS.md:6939`).
- **Uses:** PROPOSAL-ADR-READ-FORMAT D2-D4 (the rollup until git-memory D6 exists; L11 builds them), PROPOSAL-ADR-GIT-MEMORY D6 (the rollup's later source, built in E3.2), [#1748] (the process view's design).

## Context

Measured 2026-10-31 on the transport and on main c6618dbb7.

**The rule already exists.**
- R99 §3: "Per review turn, the browser architect reads three things: the LEDGER, one generated rollup, and the map diff. The target is at most 20 KB in all. A longer surface is a defect of the tool that produced it."

**What the boot reads instead.**
- The reading path is five files:
  - INDEX.md, 22,461 B;
  - SEAT-LESSONS-2026-10-18, 5,929 B;
  - SEAT-EXAM-2026-10-18, 3,692 B;
  - DIGEST-DISPATCH-ONBOARDING-2026-10-09, 6,699 B, of which only one section is read;
  - MAP-DISPATCH, 1,629 B.
- That totals 40,410 B at most, twice R99's target.
- The LEDGER is not a reading-path item. HANDOFF_BOOT names it only under "Where things live" (`:35`).
- Every later turn starts with the inbox query, which reads headers only (`:46-47`).

**What the cut writes.**
- The cut's READING_PATH.md read set is INDEX + newest RATIFICATION + newest FINDING, with a 40 KiB budget.
- The cut regenerates the LEDGER (`scripts/gen_handoff.py:4579-4588`, `:4764`).
- No landing does. The live LEDGER reads "refreshed 2026-10-28", per a transport file the evaluators could not check.

**What gen_ledger gives.**
- Sections STATE, BLOCKED BY and NEXT (`scripts/gen_ledger.py:22`).
- No byte cap.
- BLOCKED BY covers `depends-on` only. A row held by "an unlanded ruling, an operator act or a vendor is invisible to this section, and that is most of what actually blocks this repo" (`:281-283`).

**The transport's index.**
- INDEX-ARCHIVE.md is 280,046 B: 1,576 rows, 627 of them UNATTRIBUTED.

**The browser's reading cost.**
- No transport file records a measured figure.

## Decision

**D1. Per turn, the browser reads R99's three things:**
- the LEDGER;
- one generated rollup: the journal window from PROPOSAL-ADR-GIT-MEMORY D6 once it is built; until then the TSV projection of `logs/MERGE-RECEIPTS.jsonl` by `lane_digest.py project` (PROPOSAL-ADR-READ-FORMAT D2-D4; Q-R1);
- the map diff: the diff of the generated process view, the browser's big picture (operator, 2026-11-01). It is Mermaid from python-statemachine 3.2.2's `MermaidGraphMachine` beside `scripts/system_map.py`, per [#1748]'s ratified design; no new dependency (the Graphviz path is not used). Until that view exists, the change in `ecosystem/system-map-record.json` since the last LEDGER. The whole view is read on demand; only its diff is per turn, so it does not become a fourth per-turn read.

The inbox query's headers count toward the same budget. INDEX.md is a lookup the browser opens only when the LEDGER names a file. The browser never reads INDEX-ARCHIVE.md.

**D2. gen_ledger carries STATE.** One organ, extended (T1 light). It gains three sections:
- OPERATOR ASKS, from HANDOFF_PROCESS §17.1's table;
- HELD BY, rows waiting on an unlanded ruling, an operator act or a vendor, sourced from the rows' frontmatter and the open RATIFICATION asks;
- the active batch's lane stages.

A `previous:` line carries the prior LEDGER's sha.

**D3. The 20 KB is measured by code.**
- A new check renders the R99 set (LEDGER + rollup + map diff + an inbox sample) and records its bytes in the regeneration receipt.
- Over 20,480 B, it sheds the rollup's oldest rows first.
- If the set is still over after shedding, the write is refused and named. This refusal is new behaviour: today gen_ledger has no cap.

**D4. Freshness after every push.**
- gen_ledger runs after land_lane's push of the land merge and of the receipt merge (`scripts/land_lane.py:459-463`), and at the batch-close tag.
- The LEDGER's first line names the origin/main sha it read, never the primary's working tree (nothing advances the primary after a landing: E3.0 night defect 16). A reader compares that sha with the head CC reports.

**D5. Reading path and cut agree.**
- `handoff_state.READING_PATH` and the cut's read set both become the R99 set.
- The cut's budget becomes 20 KB.
- SEAT-LESSONS, the seat exam, the dispatch exam and MAP-DISPATCH stay boot-time exams pulled on demand (R73). They are not per-turn reads.
- Q-C1 (ruled directly): the browser opens the three files on Drive itself; the boot's "via CC" wording changes for them.

## Quality attributes

- **Quality attribute(s):**
  - reading cost: bytes per browser turn;
  - freshness: lag from a main push to the LEDGER;
  - completeness: from the set, the browser can say what is running, what is blocked and by whom, and what is asked of the operator.
- **Scenario:**
  - **Source:** a browser seat in the middle of a batch.
  - **Stimulus:** a status turn.
  - **Artifact:** the R99 set as rendered by the last regeneration.
  - **Environment:** E3.1 lane L11 built; Q-C1 ruled directly.
  - **Response:** the browser answers the three status questions from the set, without INDEX.
  - **Response measure:**
    - the recorded R99-set bytes are <= 20,480 at every regeneration in the first batch (baseline: reading path 40,410 B);
    - the LEDGER's head sha equals main's head after each landing;
    - the batch digest records 0 hand steps of cause `ledger-missing` (status relays the LEDGER could not answer).
- **Decision evidence:** the Context measurements; R99's text; the matrix; codex gpt-6-sol and grok-4.7 (15 findings, all accepted).

## Consequences

**E3.1 builds:**
- the gen_ledger sections and the post-push trigger;
- the R99-set byte check and its refusal;
- the READING_PATH and cut read-set change;
- the boot's reading-path text (handoff update, edit E13);
- read-format's `project` and `record` verbs, moved into this lane;
- the process-view diff slot.

**What stays:**
- INDEX and INDEX-ARCHIVE stay as generated. Their 627 UNATTRIBUTED rows remain a janitor topic.
- The `STATE-*.json` sidecars stay with the seats.

**One cost:**
- Every main push now also writes to Drive.

## Flip-condition

- If the rendered R99 set is refused by D3 at two consecutive regenerations after shedding, the content split is reopened. The cause is recorded in the regeneration receipt.
- If a batch digest records 2 or more `ledger-missing` hand steps, D2's sections are reopened.
- If the LEDGER head sha lags main by more than one landing twice in a batch, D4's trigger is reopened.

## Alternatives considered

- **B0, status quo** (five-item reading path; LEDGER refreshed at the cut). Rejected:
  - 40,410 B against R99's 20 KB;
  - the LEDGER is fresh only at cuts.
- **B1, the browser's proposal as written** (a new STATE generator capped at 12 KB, plus LEDGER, journal and RATIFICATION). Rejected:
  - a second organ beside gen_ledger, whose STATE section already exists;
  - four standing files instead of R99's three.
- **B2, gen_ledger alone at 12 KB, plus the newest RATIFICATION** (revision 1's choice). Rejected:
  - it drops R99's rollup and map diff;
  - its BLOCKED BY misses operator acts.
- **B3, slim INDEX.** Rejected: still a file list, not state.
- **B4, CC-mediated only.** Rejected: every status question becomes an operator relay (M8).

---

## Evidence

Weights: readcost=30 conformance=20 reuse=20 completeness=15 enforce=15
| Option | readcost | conformance | reuse | completeness | enforce | Σ |
|---|---|---|---|---|---|---|
| B0 status quo | 1 | 1 | 3 | 3 | 1 | 1.70 |
| B1 STATE generator | 3 | 2 | 2 | 3 | 3 | 2.60 |
| B2 gen_ledger 12 KB | 3 | 2 | 3 | 2 | 3 | 2.65 |
| B3 slim INDEX | 2 | 1 | 3 | 2 | 2 | 2.00 |
| B4 CC-mediated | 3 | 2 | 3 | 2 | 1 | 2.35 |
| B5 R99 enforced | 3 | 4[^1] | 3 | 3 | 3 | 3.20 |

[^1]: measured -- R99 §3 names exactly three files and a 20 KB target (protocols/STANDING_RULINGS.md:6498); B5's set is those three files plus the inbox headers, by construction; B0's reading path measured 40,410 B (Get-Item lengths, 2026-10-31).

**Scoring notes:**
- `readcost` is capped at 3 for every unbuilt option, because a projected cap is not a measurement (BSC6, BSG7).
- `conformance` scores fit with the standing rulings (R99, T1 light).
- `enforce` scores whether a cap or trigger lives in code.

### Pre-mortem

- **Bytes are not tokens.** The read-format ADR measures the token side.
- **Shedding can hide what the browser needed.** D3 sheds rollup history first, and the flip-condition watches refusals.
- **A Drive sync lag can show an older LEDGER than main.** D4's sha line makes this visible but does not prevent it.
- **`ledger-missing` depends on honest hand-step recording.** The cause tag comes from the seat that relays.
- **The process view could crowd the budget.** Only its diff is per turn, and D3's byte check covers the diff.

## Subagent claims

- python-statemachine is locked at 3.2.2 {probe: grep -c 'python-statemachine==3.2.2' pyproject.toml}
- python-statemachine 3.2.2 ships MermaidGraphMachine (.venv statemachine/contrib/diagram/__init__.py:70, read by CC 2026-11-01) {unverified}
- R99 §3 browser economy: three things, at most 20 KB {probe: protocols/STANDING_RULINGS.md:6498}
- T1 light is an extension inside an existing organ {probe: protocols/STANDING_RULINGS.md:6939}
- the boot names the ledger under where-things-live, not the reading path {probe: protocols/HANDOFF_BOOT.md:35}
- the boot says everything else is pulled via CC {probe: protocols/HANDOFF_BOOT.md:11}
- the reading path's five items are data in handoff_state {probe: scripts/handoff_state.py:916}
- the cut's read-set budget is 40 KiB {probe: scripts/gen_handoff.py:4461}
- the cut regenerates the LEDGER {probe: scripts/gen_handoff.py:4585}
- gen_ledger declares STATE / BLOCKED BY / NEXT {probe: scripts/gen_ledger.py:22}
- BLOCKED BY is blind to rulings, operator acts and vendors {probe: scripts/gen_ledger.py:282}
- gen_ledger writes through the transport {probe: scripts/gen_ledger.py:355}
- the browser reads/writes via the Drive {probe: protocols/OPERATOR-INTERFACE.md:47}
- INDEX-ARCHIVE is 280,046 B with 1,576 rows, 627 UNATTRIBUTED (to-browser/INDEX-ARCHIVE.md) {unverified}
- the five reading-path files total 40,410 B (Get-Item, 2026-10-31) {unverified}

## Evaluator records

Unchanged and verbatim in revision 2, `to-browser/PROPOSAL-ADR-BROWSER-SURFACE-2026-11-01.md` (sessions, nonces, served models, every finding id). Revision 3 was not re-sent to the evaluators: its changes come from CC's R41 challenge and the operator's rulings of 2026-11-01, listed in the Revision 3 section below.

## Response table

| id | objection (short) | response |
|---|---|---|
| BSC1 | direct Drive reads vs pull via CC | **Accepted** -- Q-C1 is the only open question; the ADR works either way; the boot line changes only on "directly" |
| BSC2 | the cut read set and budget not updated | **Accepted** -- D5: READING_PATH and the cut read set both become the R99 set at 20 KB |
| BSC3 | static LEDGER stale after push | **Accepted** -- D4: regenerated after every main push; head-sha line |
| BSC4 | BLOCKED BY misses operator acts | **Accepted** -- D2 adds HELD BY and OPERATOR ASKS with named sources |
| BSC5 | flip contradicts D3 | **Accepted** -- flip 1 now fires on refused writes after shedding |
| BSC6 | readcost 4 projected | **Accepted** -- readcost capped at 3 for every unbuilt option |
| BSG1 | R99 already rules 20 KB | **Accepted** -- B5 implements R99 §3; Q-C2 withdrawn |
| BSG2 | R99 set missing as an option | **Accepted** -- B5 added and recommended |
| BSG3 | wrong ruling cited | **Accepted** -- cites T1 light (:6939); R14 removed |
| BSG4 | inbox query not counted | **Accepted** -- D1 and D3 count the inbox headers in the 20 KB |
| BSG5 | the cut already regenerates the LEDGER | **Accepted** -- Context states it; D4 adds landing-time freshness |
| BSG6 | flip unobservable | **Accepted** -- replaced by refusals in the regeneration receipt and `ledger-missing` hand steps |
| BSG7 | B1 readcost 4 unsupported | **Accepted** -- 3 |
| BSG8 | LEDGER is not a reading-path item | **Accepted** -- Context corrected |
| BSG9 | refusal cap is new behaviour | **Accepted** -- D3 says so |

## Revision 3 - CC's R41 challenge (2026-11-01, on main 13023da42) and what changed

Every revision-2 finding was accepted (15/15); R41 looked hardest where nothing was defended.
- BS-R1 (missing source): D1's rollup came from PROPOSAL-ADR-GIT-MEMORY D6, whose build moves to E3.2 under the scope cut. Without a fallback, L11 would ship a two-thing set. The rollup is read-format's TSV projection of MERGE-RECEIPTS until D6 exists (Q-R1), and L11 absorbs read-format D2-D4.
- BS-R2 (operator addition vs R99): a process view added as a fourth per-turn read breaks R99's three-thing, 20 KB set. It fills the "map diff" slot instead: its diff per turn, the whole view on demand. Mermaid output needs no new dependency (`MermaidGraphMachine` in the locked python-statemachine 3.2.2; pydot is not in `uv.lock`).
- BS-R3 (freshness premise): D4's head-sha line must read origin/main. The primary is not advanced after a landing (E3.0 night defect 16, HAND-STEP 38); a LEDGER read from it would name a stale sha.
- BS-R4 (ruling): Q-C1 directly, so the boot's "via CC" line (HANDOFF_BOOT.md:11) changes in the handoff lane, not here.
- Matrix unchanged.
