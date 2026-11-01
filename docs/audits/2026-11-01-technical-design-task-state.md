# Design: task state and the resume verb (E3.1 /decide, run e31-ii)

- **Run date:** 2026-11-01
- **Producer:** claude-opus-5-5 (seat e31-decide, run e31-ii); research subagents claude-sonnet-5-5 (read-only, three, one per sub-question)
- **Rows:** [#890] (tasks/890-per-task-execution-state-carrier.md), [#1613] (tasks/1613-the-daemon-does-not-resume-a-lane-that-was-stopped.md), [#884] (tasks/884-a-research-dispatch-states-its-bounds-before-launch.md); row 1830 (reserved) is reserved, not filed (DIGEST-E3-1-ID-GRANT-2026-11-01.md:24). All rows stay open: the build follows the operator's ratification.
- **Scope ruling:** GO-E3.1 section 2, "AJ H7": "/decide in L0 over AJ proposals 1, 3, 5, 6 (priority: one state file per task + resume verb, matching the night defects), 7, 8, 9 and 11" (to-cc GO-E3.1.md:38). Not re-opened here.
- **Inputs (read in full):** DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md (166 lines), DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md (119 lines), DIGEST-AJ-P9-REVIEW-2026-11-01.md (53 lines); also DIGEST-E3-1-ID-GRANT-2026-11-01.md (37 lines).
- **Output:** docs/decisions/ADR-139-a-task-has-one-state-file-and-a-resume-verb.md at status Proposed. Nothing is built.

## Brief

Question, in the operator's order:
1. AJ 6 ([#890], [#1613]): how does a paused, crashed or stopped lane keep and resume its progress? What is the state file, where does it live, who writes it, how does the resume verb read it, and what happens when ADR-121 is ratified?
2. AJ 5 ([#884]): what is the research-brief schema with rejection criteria, and where does /decide enforce it?
3. AJ 8: what does the contract's clarification pass ask, when, and who answers, under R12 (sign-off plus contract)?

Known constraints (no answer is pre-committed):
- The operator ruled "one state file per task + resume verb, matching the night defects" (GO-E3.1.md:38).
- The AJ digest, as amended by P8, says: "A per-task state VIEW projected from ADR-121 events, plus a resume verb (G-07, S-04, S-05). It is never a model-written task file." (DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:39).
- Two M2 flips point the same way: agy:G-07 "a per-task file contradicts pack :297" and agy:G-23 "derive progress from ADR-121 events", both partly -> accepted (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:71, :73).
- Maister adopt items: 3 post-compaction re-injection, 4 strict parse with duplicate keys rejected, 5 clock-read timestamps ("refuse zero-fill and guesses; 14/14 AJ state files were zero-filled"), 6 ADR-121 vocabulary plus a projection in place of orchestrator-state.yml (DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:96-98); position "resume validates artifacts" (:105). Item 8 is "gate ordering" (:100).
- ADR-121 is Proposed. ADR-122, ADR-130 (in part) and ADR-134 are Accepted.
- The night defects: the repair prompt reads a refusal that does not exist (row 1830 (reserved), DIGEST-E3-1-ID-GRANT-2026-11-01.md:24); nothing advances the primary after a landing (row 1828 (reserved), :22); TaskStop leaves a bash loop (row 1831 (reserved), :25).

Sub-questions fanned out: Q1 what resume and state exist today; Q2 the event and record shapes already decided; Q3 briefs, the contract template and the question path.

## Subagent briefs

The sub-question of each brief is quoted below. Brief 1 is verbatim; briefs 2 and 3 are abridged (file paths shortened, the shared CONTEXT line and the common exclusion and output paragraph omitted). The full texts are the files the subagents were sent (C:\Users\1028120\.claude\jobs\05d3b2bf\tmp\briefs-e31-ii\). The three files passed `decide_checks subagent-exclusions` with 0 defects.

### Brief 1 (q1-repair-and-resume.md)

```text
CONTEXT: a /decide run on how a paused, crashed or stopped lane keeps and resumes its progress (rows tasks/890-per-task-execution-state-carrier.md, tasks/1613-the-daemon-does-not-resume-a-lane-that-was-stopped.md). Nothing is being built.

SUB-QUESTION 1 (what exists for resume today): (a) scripts/dispatch.py's repair subcommand: what does its prompt tell the resumed session, which refusal text does it name, and does that refusal exist anywhere in scripts/ (grep for the exact phrase); (b) what a launch receipt contains and where it lives (logs/receipts/ layout, LANE-<slug> dirs, file names, fields); (c) scripts/seat_cycle.py and ecosystem/seat-cycle.yaml: what state the R179 handover records and who writes it; (d) any existing per-lane or per-task state/progress/status file written by code (grep scripts/ for 'state.json', 'progress', 'resume', 'PAUSED'); (e) whether any writer uses atomic write (os.replace) and whether any JSON reader rejects duplicate keys (object_pairs_hook).

EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". [... the common exclusion, output and probe-form paragraph, identical in all three briefs ...]
```

### Brief 2 (q2-event-shape.md)

```text
SUB-QUESTION 2 (the event and record shapes already decided): read ADR-121, ADR-122, ADR-130 and ADR-134. Report: (a) each ADR's status line; (b) ADR-121's event envelope fields, the writer, where events live (ref name), the projection rule, and D5 verdict identity; (c) ADR-134's StageRecord and PhaseReceipt v2 fields (session_id) and where the code defining them lives in scripts/; (d) ADR-130's phase list and receipt location; (e) whether scripts/conductor.py or scripts/land_lane.py already write a per-lane record with timestamps, and how the timestamp is obtained.
```

### Brief 3 (q3-briefs-and-clarification.md)

```text
SUB-QUESTION 3: (a) quote row 884's body; (b) what scripts/decide_checks.py checks today and .claude/commands/decide.md step 1-2; (c) any existing brief template or schema; (d) the lane contract template and its sections; (e) where R12 (sign-off + contract) is stated in protocols/STANDING_RULINGS.md; (f) whether any mechanism carries a lane question to the operator or dispatcher today.
```

## Subagent claims

Every claim below was re-run by the producer this session (decide_checks subagent-claims). Where a subagent's line probe did not quote the line it named, the producer replaced it with a probe it checked by reading the line.

- Q1: the repair prompt says "read the refusal and the frozen contract" and names no refusal text {probe: scripts/dispatch.py:1945}
- Q1: the phrase "read the refusal" occurs once in dispatch.py, in that prompt {probe: grep -c 'read the refusal' scripts/dispatch.py}
- Q1: a repair refuses when the lane's own worktree is missing {probe: grep -c 'no existing worktree' scripts/dispatch.py}
- Q1: the slug launch receipt is logs/receipts/LAUNCH-<SLUG>.json {probe: scripts/dispatch.py:815}
- Q1: logs/receipts is gitignored {probe: git check-ignore logs/receipts/x}
- Q1: sibling receipts include a per-slug lock file {probe: grep -c 'LAUNCH-LOCK-' scripts/dispatch.py}
- Q1: a repair receipt keeps earlier launches in a launches list {probe: grep -c 'launches' scripts/dispatch.py}
- Q1: the launch receipt is written with a plain write_text, not atomically {probe: scripts/dispatch.py:828}
- Q1: the R179 handover is a markdown file written with a plain write_text {probe: scripts/seat_cycle.py:184}
- Q1: the successor binds by a BOUND line {probe: grep -c 'BOUND seat=' scripts/seat_cycle.py}
- Q1: seat-cycle.yaml holds thresholds, not lane state {probe: grep -c 'context_tokens' ecosystem/seat-cycle.yaml}
- Q1: seat_cycle.py reads the harness job's state.json, which no repo code writes {probe: scripts/seat_cycle.py:333}
- Q1: scripts/seat_state.py is a per-SEAT state file with its own schema id {probe: grep -c 'dev-knowledge-seat-state/1' scripts/seat_state.py}
- Q1: seat_state.py writes atomically with os.replace {probe: scripts/seat_state.py:322}
- Q1 (producer): seat_state.py fills a missing row timestamp with the current time, the guess Maister item 5 refuses {probe: scripts/seat_state.py:203}
- Q1: no JSON reader in the state organs rejects duplicate keys; object_pairs_hook is absent; the producer's count in scripts/seat_state.py is 0 {unverified}
- Q1: the word PAUSED does not occur in dispatch.py; the producer's count is 0 {unverified}
- Q2: ADR-121 is Proposed {probe: docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:3}
- Q2: ADR-121 D4 names the envelope fields event_id, entity, expected_revision, writer, schema_version and causal links, with no timestamp {probe: docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:75}
- Q2: ADR-121 D3 gives each lane its own outbox ref {probe: grep -c 'refs/lanes/<lane>/events' docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md}
- Q2: ADR-121 D5 keys a verdict by candidate SHA, gate, baseline ID, policy and context {probe: docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:79}
- Q2: ADR-121 D8 says a stale projection is rebuilt or fails closed {probe: grep -c 'fails closed' docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md}
- Q2: ADR-134 defines the StageRecord fields stage, artifact sha, session_id, declared and served model, ts {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:51}
- Q2: ADR-134 puts PhaseReceipts and StageRecords under logs/receipts/LANE-<slug>/ {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:64}
- Q2: the conductor resolves the same directory, per round {probe: scripts/conductor.py:906}
- Q2: PhaseReceipt v1 is a pydantic model in ecosystem/schema {probe: ecosystem/schema/phase_receipt.py:165}
- Q2: run_phase.py stamps UTC wall-clock seconds {probe: scripts/run_phase.py:72}
- Q2: conductor.py states the repo records no clock against operator time {probe: scripts/conductor.py:392}
- Q2: StageRecord is not yet implemented in the conductor; the producer's count in scripts/conductor.py is 0 {unverified}
- Q3: row 884 asks for an agent cap, a per-agent deadline and a token budget, refused when missing {probe: tasks/884-a-research-dispatch-states-its-bounds-before-launch.md:12}
- Q3: decide.md step 1 says questions only, no pre-committed answer {probe: .claude/commands/decide.md:30}
- Q3: the only brief check today tests that the excluded root is named {probe: scripts/decide_checks.py:390}
- Q3: no brief template or rejection-criteria schema exists under templates/ or .claude/; the subagent's counts were 0 {unverified}
- Q3: the lane contract template's last section is the immutable Done-contract {probe: templates/lane-contract-template.md:94}
- Q3: the lane contract template has no QUESTION section; the producer's count is 0 {unverified}
- Q3: R12 is "No launch without (a) a sign-off the operator signed and (b) a lane contract produced by the distiller" {probe: protocols/STANDING_RULINGS.md:7680}
- Q3: the transport already has a QUESTION request kind {probe: scripts/transport.py:88}
- Q3: gen_handoff requires every QUESTION file in to_browser to be answered or carried {probe: scripts/gen_handoff.py:1491}
- Q3: no script carries a lane's question to the dispatcher; the subagent did not read dispatch.py for it {unverified}

## Evidence and matrix (AJ 6)

### What exists, quoted

- **Repair today.** `RepairRequest.prompt` is "Repair for {slug} (attempt {n}): read the refusal and the frozen contract at {contract}; fix only what the refusal names; hand back per the common rules." (scripts/dispatch.py:1945). No refusal is passed in: the night defect row 1830 (reserved) is that the prompt points at a document that does not exist. The repair runs in the lane's own worktree and rewrites the slug receipt with `kind: repair` (scripts/dispatch.py:1428).
- **Receipts.** One JSON per slug, LAUNCH-<SLUG>.json (scripts/dispatch.py:815), in gitignored logs/receipts, written non-atomically (:828). ADR-134 already fixes the per-lane directory logs/receipts/LANE-<slug>/ for PhaseReceipts v2 and StageRecords (ADR-134:64), and the conductor uses it (scripts/conductor.py:906).
- **A code-written state file already exists, per seat.** scripts/seat_state.py ("the per-lane state an orchestrator seat hands to its own successor") writes atomically (:322), refuses torn and stale files, and requires evidence on every row. Two gaps measured against the Maister items: it fills a missing ts with the current time (:203), which is a guess; and no reader rejects duplicate keys (object_pairs_hook count 0).
- **Intake 80** (docs/intake/2026-09-07-tech-per-lane-resumable-state-file.md, DRAFT) proposed a lane-written LANE-STATE.yml in the worktree, at phase boundaries, with phase, completed, failed, last_commit. Its own open question is "Gitignored or committed?". The AJ ruling "never a model-written task file" rules out its writer, not its fields.
- **ADR-121** gives the target shape: lanes write only their own outbox `refs/lanes/<lane>/events` (D3); every event carries event_id, entity, expected_revision, writer, schema_version and causal links (D4); a projection is rebuilt or fails closed (D8). D4 names no timestamp.
- **[#1613]** already names the event a stop must leave: "a test asserts seat_registry.py records a stopped-by-seat event for a stopped job and that the queue/resume path refuses a job with that event" (tasks/1613-the-daemon-does-not-resume-a-lane-that-was-stopped.md:12).

### Reconciling the operator's ruling with the flips

The operator ruled one state FILE per task. The AJ digest and flips G-07 and G-23 rule out a model-written file and ask for progress derived from ADR-121 events. Both hold when **the one file is an append-only event log in the ADR-121 envelope, written only by code, and "state" is a pure function of it computed by the reader.** No second, mutable snapshot exists that could drift from the events (G-07's objection to a per-task file); progress is derived from events (G-23); and there is exactly one file per task (the operator). When ADR-121 is ratified, the file's lines are the lane's outbox events (D3) with no reshaping, and the reader becomes a D8 projection.

### Options

S0 status quo (repair re-reads the transcript and the contract). S1 a code-written mutable JSON snapshot per lane plus a resume verb. S2 a pure projection of ADR-121 events, wait for ratification. S3 an append-only code-written event file per task in the ADR-121 envelope, under logs/receipts/LANE-<slug>/, plus a resume verb that projects it (projection-compatible). S4 a git ref per lane now (ADR-121 D3's outbox ref, early). S5 extend scripts/seat_state.py's per-seat file with per-task rows (found by research). S6 intake 80's lane-written LANE-STATE.yml in the worktree (found by research).

Criteria. resume: the verb can tell never-started, stopped mid-phase, failed and blocked apart, and names the real last refusal. integrity: code-written, clock-read, strict parse, artifacts validated. compat: no reshaping when ADR-121 lands. reuse: existing organs and directories. footprint: new code, gates and leftovers. now: usable before ADR-121 is ratified, at E3.2 wave 0 (row 1830 (reserved) is P1 wave 0).

Scores are 1 to 5. A 4 or 5 needs a footnote that says measured; every other score is a judgment on an unbuilt design and caps at 3.

Weights: resume=25 integrity=20 compat=20 reuse=15 footprint=10 now=10

| Option | resume | integrity | compat | reuse | footprint | now | Σ |
|---|---|---|---|---|---|---|---|
| S0 status quo | 1 | 1 | 1 | 3 | 4[^1] | 3 | 1.80 |
| S1 mutable JSON snapshot + resume verb | 3 | 3 | 2 | 3 | 3 | 3 | 2.80 |
| S2 wait for ADR-121 projection | 3 | 3 | 3 | 3 | 2 | 1 | 2.70 |
| S3 append-only event file in the ADR-121 envelope + resume verb | 3 | 3 | 3 | 4[^2] | 3 | 3 | 3.15 |
| S4 per-lane git ref now | 3 | 3 | 3 | 2 | 2 | 2 | 2.65 |
| S5 extend seat_state.py per-seat file | 2 | 3 | 2 | 4[^3] | 3 | 3 | 2.70 |
| S6 lane-written LANE-STATE.yml (intake 80) | 2 | 1 | 1 | 3 | 3 | 3 | 1.95 |

[^1]: measured -- S0 changes nothing, so it adds no code, gate or file; this session's reading of scripts/dispatch.py:1945 shows the cost it keeps, a prompt naming no refusal.
[^2]: measured -- the directory S3 writes into is already fixed by ADR-134:64 and resolved by scripts/conductor.py:906, the receipts root by scripts/dispatch.py:815, and the atomic-write pattern exists at scripts/seat_state.py:322; all read this session.
[^3]: measured -- scripts/seat_state.py exists with a schema id, atomic write (:322) and torn/stale refusal, read this session.

Reading the matrix:
- S3 leads S1 by 0.35. The lead is compat (+0.20) and reuse (+0.15): S3's lines are ADR-121 outbox events, so ratification changes the transport, not the record. S1 keeps a mutable snapshot, the very artifact G-07 objects to.
- S2 and S5 tie at 2.70. S2 loses on now: row 1830 (reserved) is wave 0 and ADR-121 has been Proposed since 2026-09-23. S5 loses on resume and compat: seat_state.py is per seat, keyed by lane state enum with prose-receipt evidence, not per task, and its timestamp fill (:203) breaks Maister item 5.
- S4 is ADR-121 D3 built before ADR-121 is ratified: it pre-empts the single-writer and fold decisions (D2, D7) that are still open.
- S6 fails integrity by construction: the model writes the file, which the AJ ruling and G-07 exclude.
- Every non-S0 score is a judgment except the reuse 4s. The margin S3 over S1 is moderate; the flip-condition names S1.

## AJ 5 -- research briefs with rejection criteria ([#884])

What exists: decide.md step 1 says "state the question and its known constraints; nothing more" (.claude/commands/decide.md:30); the only brief check is the excluded-root substring (scripts/decide_checks.py:390); no brief template exists (claim above, unverified count 0). Row 884 asks for an agent cap, a per-agent deadline and a token budget before launch, refusal when missing, and a prior-art check (tasks/884-...:12). The M1 judge read the research-brief theme as hub /decide work (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:45), which confirms that its home is /decide, not a consumer carrier.

Options: R0 prose in decide.md; R1 a header block in every brief file, checked by a new decide_checks subcommand `brief-schema` beside subagent-exclusions; R2 a separate brief organ with its own CLI. R1 reuses the existing gate and the brief files the run already saves; R2 adds an organ for one block of fields. Decision: R1. The fields are fixed in the ADR (D7).

## AJ 8 -- the clarification pass in the contract

What exists: the lane contract has Read first, Dispatch, Worktree pairing, Value, Done-contract (immutable), Do not (templates/lane-contract-template.md); no QUESTION section; R12 makes the distiller's contract and a signed sign-off the only launch path (protocols/STANDING_RULINGS.md:7680); the transport has a QUESTION kind (scripts/transport.py:88) and the handoff generator refuses an unanswered QUESTION file (scripts/gen_handoff.py:1491); a lane question reaching the dispatcher by code is row row 1822 (reserved) (DIGEST-E3-1-ID-GRANT-2026-11-01.md:16). sol:S-08 (quick path = a minimal contract under R12) flipped to accepted (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:76), so the clarification pass must not become a second launch path.

Options: K0 none; K1 a pass inside the distiller, before the contract freezes: the distiller lists unresolved points, the operator answers them in the sign-off; K2 a pass at lane boot, the lane asks; K3 both. K1 keeps the question before freeze, where R12 already places the operator's signature, and adds no lane-to-operator round trip mid-run. K2 asks after freeze, when the Done-contract is immutable and the answer cannot change it. Decision: K1, with a lane-side residual question carried by row 1822 (reserved), not by this ADR.

## M2 flips attached

Flips of this run's items, with how the ADR answers them:

| flip | item | file:line | how the ADR answers |
|---|---|---|---|
| agy:G-07 partly -> accepted | P6-6 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:71 | no mutable per-task file exists; the one file is an append-only event log, state is computed (D1, D3) |
| agy:G-23 partly -> accepted | P6-6 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:73 | progress is derived from events in the ADR-121 envelope; on ratification the lines are outbox events (D1, D6) |

All other M2 flips of section 3 (agy:G-17 is run (i)'s and is omitted):

| flip | item | file:line | note |
|---|---|---|---|
| agy:G-14 rejected -> accepted | mm:reality-assessor | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:58 | concerns mm:reality-assessor; not an item of this run |
| agy:G-19 rejected -> accepted | theme:M08-T02 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:59 | concerns theme:M08-T02; not an item of this run |
| agy:G-02 rejected -> partly | B4 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:61 | concerns B4; not an item of this run |
| agy:G-10 rejected -> partly | C2 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:62 | concerns C2; not an item of this run |
| agy:G-12 rejected -> partly | B2 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:63 | concerns B2; not an item of this run (B2's "research goal" field is the consumer intake's, not the /decide brief of D7) |
| agy:G-21 rejected -> partly | mm:code-quality-pragmatist | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:65 | concerns mm:code-quality-pragmatist; not an item of this run |
| agy:G-27 rejected -> partly | C4 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:66 | concerns C4; not an item of this run |
| agy:G-30 rejected -> partly | mm:artifact reconciliation | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:67 | concerns mm:artifact reconciliation; not an item of this run (D5's artifact check at resume reuses no reconciliation organ) |
| agy:G-01 partly -> accepted | P6-2 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:69 | concerns P6-2; not an item of this run |
| agy:G-04 partly -> accepted | B3 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:70 | concerns B3; not an item of this run |
| agy:G-16 partly -> accepted | tool:jqwik | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:72 | concerns tool:jqwik; not an item of this run |
| agy:G-28 partly -> accepted | P6-10 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:74 | concerns P6-10; not an item of this run |
| sol:S-01 partly -> accepted | P6-2 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:75 | concerns P6-2; not an item of this run |
| sol:S-08 partly -> accepted | mm:quick commands | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:76 | concerns mm:quick commands; not an item of this run (read as a constraint on D8: no second launch path) |
| sol:S-11 partly -> accepted | C4 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:77 | concerns C4; not an item of this run |
| sol:S-15 partly -> accepted | mm:product-design workflows | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:78 | concerns mm:product-design workflows; not an item of this run |
| sol:S-18 partly -> accepted | tool:Jinja | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:79 | concerns tool:Jinja; not an item of this run |
| agy:G-20 partly -> rejected | C7 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:81 | concerns C7; not an item of this run |
| sol:S-07 partly -> rejected | B3 | DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:82 | concerns B3; not an item of this run |

Section 3 lists 22 flips (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:13): 2 above, 19 here, and agy:G-17 in run (i). The "pack :297" that G-07 cites is in the AJ KB, outside the repo, and was not read; the flip is taken as the digest states it.

## Pre-mortem

Assume S3 was built and failed six months later. Likely causes, and what the design carries against each:
1. **The model writes the file anyway**, through a shell redirect or an Edit. Against: the writer is one module; a reader refuses a line whose writer is not on the module's allowlist of code writers; a test asserts no lane prompt or contract template names the file path.
2. **Timestamps are guessed or zero-filled** (14/14 AJ state files were, DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:97). Against: the writer reads the clock itself and takes no ts argument; the reader refuses a missing, zero or non-monotonic ts. seat_state.py's fill (:203) is not copied.
3. **A duplicate key or a torn line passes.** Against: strict parse with object_pairs_hook rejecting duplicates; a torn final line is refused, not skipped; append with a lock (the LAUNCH-LOCK pattern) and fsync.
4. **The resume verb trusts a stale record.** The file says phase 3 done, but the branch was reset. Against: resume validates artifacts before it renders a prompt: worktree present, branch present, every recorded commit an ancestor of the branch head, the contract's sha unchanged, the recorded receipt files present. Any mismatch refuses with the mismatch named.
5. **ADR-121 lands with a different envelope**, for example no ts, or entity named differently. Against: the record carries ADR-121 D4's six fields by name, and ts as an extra field; the flip-condition names this; a one-shot migration is a line-by-line map, not a reshaping, because every line is already one event.
6. **The file outlives its lane or is lost with it.** Against: it lives in the primary's gitignored logs/receipts/LANE-<slug>/ (not in the worktree), so teardown does not delete it and no leftovers are created in the tree; logs retention governs its age.
7. **Two writers race** (dispatch stop and a phase write). Against: one lock per slug, expected_revision is the line count read under the lock, and a mismatched expected_revision is refused (ADR-121 D4 in miniature).
8. **The resume prompt grows prose again.** Against: the prompt is rendered from the projection by a fixed template with only enum values, ids, shas and the recorded refusal text; a test pins the template.
9. **Per task vs per lane drift.** A lane runs one task by contract today. Against: the file is keyed by task id and lane slug both; a second task in one lane is a second file.

## Open for the operator

1. Confirm that "one state file" may be an append-only event file whose state is computed (D1), not a mutable snapshot.
2. Confirm the location: the primary's gitignored logs/receipts/LANE-<slug>/, not the worktree and not git.
3. Should a lane's own phase boundary be recorded by a CLI verb the lane runs (code writes, the model only invokes with enum arguments), or only by the conductor and dispatch? D2 proposes both.
4. AJ 8: confirm that the operator answers clarification questions in the sign-off (K1).
