# ADR-139: A task has one state file, an append-only event log written through one module, and a resume verb that validates against git before it projects

- **Status:** Proposed
- **Date:** 2026-11-01
- **Decision tier:** Path A -- a `/decide` proposal for operator ratification (R13, ADR-108 section A).
- **Related:** ADR-121 (event log, Proposed: D1 one file per event, D3 lane outbox, D4 envelope, D7 published state, D8 projection), ADR-122 (a task is a typed record), ADR-130 (conductor phases and receipts), ADR-134 (StageRecord, PhaseReceipt v2, logs/receipts/LANE-<slug>/); rows [#890], [#1613], [#884]; reserved rows 1830 (repair names a real refusal), 1822 (a lane's question reaches the dispatcher by code), 1828 and 1831 (DIGEST-E3-1-ID-GRANT-2026-11-01.md:16, :22, :24, :25).
- **Decommission:** the free-text repair prompt in `scripts/dispatch.py` (`RepairRequest.prompt`, scripts/dispatch.py:1945) is replaced by D5's rendered prompt.
- **Source:** the design evidence docs/audits/2026-11-01-technical-design-task-state.md (matrix, pre-mortem, M2 flips, evaluator responses); the scope is the operator's GO-E3.1 section 2 "AJ H7"; the inputs are DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md section 2 items 5, 6 and 8 and section 6, and DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md section 3 (flips agy:G-07, agy:G-23). Two evaluators (codex gpt-6-sol, served model unverified; Copilot gemini-4-argon) amended the first draft; their 22 findings are answered in the evidence file.

## Context

A paused, crashed or stopped lane has no record of its progress that a successor can trust. The repair verb's prompt says "read the refusal and the frozen contract ... fix only what the refusal names" (scripts/dispatch.py:1945) and passes no refusal: that is the night defect of reserved row 1830. A stopped job can be resumed by the daemon ([#1613]). The only code-written state file is per seat (scripts/seat_state.py), and it fills a missing timestamp with the current time (:203). No JSON reader in it rejects duplicate keys.

The operator ruled "one state file per task + resume verb, matching the night defects" (GO-E3.1 section 2). The AJ digest, amended by P8, says "a per-task state VIEW projected from ADR-121 events, plus a resume verb ... never a model-written task file" (DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:39). Flips agy:G-07 ("a per-task file contradicts pack :297") and agy:G-23 ("derive progress from ADR-121 events") went partly -> accepted (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:71, :73). The pack G-07 cites is in the AJ KB, outside the repo, and was not read; this ADR reads G-07 as the digest words it ("never a model-written task file") and asks the operator to confirm that reading. ADR-121 is Proposed. ADR-134 already fixes the per-lane receipt directory logs/receipts/LANE-<slug>/ (ADR-134:64; scripts/conductor.py:906).

## Decision

### AJ 6 -- task state and resume ([#890], [#1613], reserved row 1830)

- **D1 -- one file per task, holding events only.** Each task has exactly one state file, `logs/receipts/LANE-<slug>/TASK-STATE-<task-id>.jsonl`, under the receipts root that `dispatch.receipts_dir()` resolves (the primary checkout's gitignored logs/receipts, or `HARNESS_RECEIPTS_DIR`). The file is append-only, and each line is one event. It never stores a snapshot, a summary or a "current phase" field; the state is computed (D4). It is a per-task file, and the operator ruled for one. Against G-07 it holds that the file carries no model-written content and no stored state that can disagree with its events. It does **not** claim that no per-task file exists.
- **D2 -- one sanctioned writer, which is not a security boundary.** A new module, `scripts/task_state.py`, holds the only sanctioned writer, `append_event`. Only code calls it:
  - `dispatch.py`: launch, repair, refusal;
  - `land_lane.py`: landed, refused;
  - the conductor and `run_phase.py`: phase started, and phase finished with its receipt sha;
  - the stop path that records [#1613]'s `stopped-by-seat`.

  A lane records a phase boundary only by running `task_state.py record <kind> --lane <slug> --task <id> --phase <id> [--receipt <path>]`. Every argument is an enum value, an id, or a path the writer checks exists and hashes. No argument takes free text.

  **What this does not give:**
  - A lane runs with shell and filesystem access as the same OS user. It can call the verb at the wrong time, or append a line by hand. Nothing here prevents either.
  - The guarantee is detection, not prevention:
    - every line carries `prev_sha`, the sha256 of the line before it, so a reader detects an edit, a deletion or an insertion before the end;
    - D5 refuses any recorded phase whose commit or receipt sha git and the file system do not confirm, so a forged `phase-finished` with nothing behind it does not move a resume.

  Prevention needs OS-level isolation or ADR-121's integrator-only fold, and is not built here.
- **D3 -- ADR-121's D4 fields inside an extended record, not an ADR-121 event as is.** Each line is a JSON object with two parts.
  - **ADR-121 D4's six fields, by name:**
    - `event_id` (uuid4);
    - `entity` (`task:<id>`);
    - `expected_revision` (the line count read under the lock);
    - `writer` (module and function);
    - `schema_version` (`task-state/1`);
    - `causes` (event ids).
  - **Fields ADR-121 D4 does not name:** `seq` (1-based line number), `prev_sha`, `kind`, `lane`, `batch`, `ts`, `session_id` (ADR-134's field, or `UNVERIFIED`), and a `payload` whose keys are fixed per kind.

  `kind` is a closed enum: `launched`, `phase-started`, `phase-finished`, `phase-failed`, `refused`, `paused`, `stopped-by-seat`, `repair-launched`, `landed`, `abandoned`. A `refused` payload carries the refusal's id and its verbatim text, as the refusing organ printed it.

  The writer reads `ts` from the clock itself (`datetime.now(timezone.utc)`) and takes no ts argument. Order is `seq`, never `ts`.

  Each append:
  - takes a per-task lock (the LAUNCH-LOCK pattern);
  - writes one line and a newline;
  - fsyncs.

  A mismatched `expected_revision` is refused.
- **D4 -- strict read, state computed.** `task_state.read(path)` parses each line with an `object_pairs_hook` that refuses a duplicate key.
  - **It refuses:**
    - an unknown kind;
    - a missing field;
    - a `seq` gap;
    - a wrong `prev_sha`;
    - a missing or zero `ts`;
    - a writer not on the allowlist;
    - a torn last line.
  - **It does not refuse** a `ts` equal to or earlier than the line before. A clock step or two events in one tick is recorded as data, not refused.
  - A refusal names the line and the defect. No line is ever skipped.
  - **An absent file** projects to `no-record`, never to `never-started`.

  `task_state.project(events)` is a pure function.
  - **The state** is one of:
    - `never-started` (a `launched` event and nothing after it);
    - `running`;
    - `paused`;
    - `stopped`;
    - `failed-at <phase>`;
    - `blocked-at-gate <refusal id>`;
    - `landed`;
    - `abandoned`.
  - **It also returns** the completed phases with their commit and receipt shas, the last refusal, and the last commit.
- **D5 -- the resume verb validates against git before it renders.** `dispatch.py resume <slug> [--task <id>]` replaces the free-text repair prompt and keeps the repair mechanics: the lane's own worktree, and `kind: repair` in the launch receipt. `--task` is required only when `LANE-<slug>/` holds more than one state file.
  - **Validation, before anything renders:**
    - the worktree exists;
    - the branch exists;
    - every recorded commit is an ancestor of the branch head;
    - the frozen contract's sha equals the one in `launched`;
    - every recorded receipt file exists and its sha256 equals the recorded sha.

    Any mismatch refuses, names the mismatch, and spawns nothing.
  - **The verb also refuses:**
    - `landed` and `abandoned`;
    - `stopped-by-seat`, unless `--override-stop` is given, which is recorded as an event;
    - `no-record`. A lane that predates the file is resumed by hand, never by a guess.
  - **On success,** the prompt comes from a fixed template, pinned by hash, that holds only projected values: the phase to start at, the completed phases, and the last refusal's id and verbatim text. That refusal is what reserved row 1830 says the current prompt names but never passes.
  - **Not decided here:** the post-compaction re-injection hook (Maister item 3). It may later reuse this projection and template.
- **D6 -- the daemon path ([#1613]).** The `stopped-by-seat` event stays where [#1613] puts it: `seat_registry.py` records it (that module already appends events through `record_event`). The queue and daemon resume path refuses a job with that event, which is [#1613]'s RED test. D2's stop path also appends the same event to the task file, so D5's manual verb and the daemon refuse alike.
- **D7 -- when ADR-121 is ratified.** The storage and the authority change; the record's fields do not.
  - **The difference today:** ADR-121 D1 stores one JSON file per event on `harness-state`, under single-writer integrator authority. This file is one gitignored JSONL per task, in one checkout.
  - **The migration lane:**
    - replays each line as one outbox event on `refs/lanes/<lane>/events` (ADR-121 D3). It maps the six D4 fields one to one, carries the remaining fields into the event body or drops them as ADR-121's final schema says, and adds no field;
    - keeps the file read-only until the integrator's fold has every line;
    - asserts that the D8 projection and `task_state.project` agree;
    - retires the file.
  - **Until then,** the file is local to one checkout. A lost checkout loses it, and another machine cannot read it. ADR-121 D7's "published state" is not met before ratification. That limit is accepted: the file's purpose is a same-machine resume, and the git checks in D5 stay authoritative.

### AJ 5 -- research briefs with rejection criteria ([#884])

- **D8 -- a brief header, refused at launch when missing; a step past its deadline is abandoned with what it has.** Every subagent brief file in a `/decide` run opens with raw `key: value` lines, before any blank line. YAML is not used. The keys:
  - `question`: one sub-question;
  - `prior-art`: the digests or audits checked, or `none found` with the search used ([#884] item 4);
  - `agent-cap`: an integer;
  - `deadline`: minutes per agent, an integer;
  - `token-budget`: an integer;
  - `reject-if`: at least one criterion that makes a finding unusable;
  - `stop-when`: what counts as answered.

  A new subcommand, `decide_checks.py brief-schema <brief files>`, sits beside `subagent-exclusions`. It refuses a missing key or a non-integer cap, deadline or budget.

  **Refusal before launch, on every research dispatch (after the blind re-ruling of IIS7).** The header is enforced where the launch happens, not after it:
  - **Subagents (the Agent tool).** The existing Agent PreToolUse guard, `scripts/hooks/subagent_model_guard.py` (it already denies an Agent call on its model), gains a second deny: it refuses an Agent call whose `prompt` does not open with the seven keys, valid by the same parser `brief-schema` uses. A refusal spawns nothing. This covers `/decide` and every other seat that fans out subagents. The prompt is the brief, so the header travels with the call: a brief kept in a file must be pasted in, not pointed at.
  - **Lanes (`dispatch.py launch`).** A contract whose Dispatch block declares `kind: research` must carry `agent-cap`, `deadline` and `token-budget`. The pre-launch moment refuses one that lacks any of them, before anything spawns.
  - `decide_checks.py brief-schema` stays as the after-the-fact audit of the saved brief files, and decide.md step 2 names it.

  **A step past its deadline is abandoned and keeps what it has ([#884] items 2-3).**
  - **Lanes.** `dispatch.py govern` stays a monitor that never stops a lane. When the deadline passes it prints a `DEADLINE <slug>` line. A new verb, `dispatch.py abandon <slug>`, stops the job, keeps the worktree and the transcript, and appends `abandoned` to the task state file (D3) with the transcript path and the spend so far. The dispatcher seat runs it on that line. Nothing is deleted, so the partial result survives.
  - **Subagents.** The runtime cannot deliver a stop in the middle of a call. Under [#884] item 3, the per-agent `deadline` is the delivery: the producer launches each subagent in the background and stops it when the deadline passes, keeping its partial output. The evidence records, per brief, the stop time or the completion time. That this limit is enforced by the seat and not by code is recorded here, not implied away.

  The evidence file carries one `spend:` line per brief: tokens, tool calls and duration, copied from the Agent tool's completion record. `brief-schema --spend <evidence>` refuses a brief with no spend line ([#884] item 5).

  **Not built here:** a stop that reaches a session in the middle of a call without killing it. The runtime offers none.

### AJ 8 -- the clarification pass

- **D9 -- the distiller asks, the operator answers in a re-signed sign-off, then the contract freezes.** The pass has three steps.
  1. **The distiller asks.** `gen_lane_contract distill` emits a draft contract with a `## Clarifications` section. Each entry is `- CQ<n> [<rule>] <question> -- options: <a> | <b> ...`.

     Entries come only from deterministic rules, with no model judgment:
     - `locator`: a locator that preflight cannot resolve;
     - `done-when`: a Done-when clause with no checkable verb or file;
     - `scope`: a touches list that names a path outside the row's refs.
  2. **The operator answers.** The operator answers in a new revision of the sign-off, with one line per question, `CQ<n>: <chosen option or text>`, and signs it.
  3. **The distiller re-runs and freezes.** It refuses to freeze the contract unless every CQ id has an answer line in the signed sign-off, and it records that sign-off's sha in the contract header.

  No second launch path exists. The quick path stays a minimal contract under R12 (sol:S-08). A question a lane meets after freeze goes through reserved row 1822's question path, never back into the frozen contract.

### Not built here

Nothing is built by this ADR. It does not decide:
- the ADR-121 event log itself, its fold or its single writer;
- OS-level isolation of the state file;
- the compaction re-injection hook;
- a mid-call stop delivery, which the runtime does not offer ([#884] item 3 records the limit);
- reserved rows 1828 and 1831;
- a view of task state. ADR-133's view reads the file as one more source.

## Quality attributes

- **Quality attribute(s):** recoverability (a stopped lane resumes at the right phase), integrity (written through one module, stamped from the clock, parsed strictly, chained, and validated against git), evolvability (one field map at ADR-121 ratification).
- **Scenario:**
  - **Source:** a lane session that pauses, crashes or is stopped by a seat.
  - **Stimulus:** the dispatcher or the operator runs `dispatch.py resume <slug>`.
  - **Artifact:** the task state file, `task_state.py` and the resume verb.
  - **Environment:** one of these holds:
    - the worktree is intact;
    - its branch was reset;
    - a receipt changed;
    - the file has a torn last line, a duplicate key or a hand-inserted line;
    - no file exists.
  - **Response:** the verb projects the state and validates it against git and the receipts. Then it either renders a prompt naming the phase and the real last refusal, or refuses and names the mismatch. It never guesses.
- **Response measure:**
  - 100 percent of lines carry the six ADR-121 D4 fields, `seq`, `prev_sha` and a clock-read ts (checked by test).
  - These each fail `read`, with one fixture each:
    - a duplicate key;
    - a zero ts;
    - a seq gap;
    - an edited earlier line;
    - a torn line.
  - An equal or earlier ts passes `read` (fixture).
  - The projection tells apart `no-record`, `never-started`, `running`, `failed-at`, `blocked-at-gate` and `stopped` (one fixture each).
  - Resume refuses on each of these (one fixture each):
    - a reset branch;
    - a changed contract sha;
    - a receipt with a changed sha;
    - `no-record`.
  - The rendered prompt contains the recorded refusal text verbatim. This closes reserved row 1830.
  - Both the queue path and the resume verb refuse a `stopped-by-seat` job. This is [#1613]'s RED test.
  - Zero new dependencies.
  - `brief-schema` refuses a brief missing any of its seven keys.
  - The Agent guard denies an Agent call whose prompt lacks the header; the pre-launch moment refuses a research contract with no cap, deadline or budget; `abandon` leaves an `abandoned` event and keeps the transcript (one fixture each).
  - The distiller refuses to freeze while any CQ id has no answer.
- **Decision evidence:**
  - The matrix in the design evidence, after the evaluators: S3 3.00, then S1 2.80, S2 2.70, S5 2.70, S4 2.65, S6 1.95, S0 1.80.
  - The probes of its Subagent claims, among them:
    - the repair prompt (scripts/dispatch.py:1945);
    - the per-lane directory (ADR-134:64, scripts/conductor.py:906);
    - the timestamp fill in seat_state.py (:203);
    - ADR-121 D1 and D4 (ADR-121:63, :75).

## Flip-condition

- **Switch to S1** (a mutable snapshot written by code) if the build lane measures either of these:
  - `project` over a 10,000-line file takes more than one second on the operator's box;
  - more than 1 in 100 appends in a batch are refused on `expected_revision`.
- **Switch to S4** (a per-lane git ref now) if ADR-121 is ratified with D3 unchanged before the build lane starts. Then write the outbox ref directly and skip the file.
- **Revisit D3's field map** if ADR-121 is ratified with an envelope that differs from D4 as it reads today.
- **Revisit D2** if the operator wants prevention rather than detection. That means OS-level isolation or waiting for the integrator fold.
- **Revisit D9** if the operator rules that the dispatcher, not the operator, answers clarifications.

## Alternatives considered

- **S0, the status quo:** rejected (1.80). The repair prompt names a refusal it never receives (reserved row 1830), and nothing tells never-started from blocked.
- **S1, a mutable JSON snapshot per lane:** the nearest rival (2.80). It is rejected because a stored snapshot is what G-07 objects to, and its lead was lost on compat, not reuse. It is a flip target.
- **S2, wait for ADR-121's projection:** rejected for now (2.70). Reserved row 1830 is P1 wave 0, and ADR-121 has been Proposed since 2026-09-23.
- **S5, extend scripts/seat_state.py:** rejected (2.70). It is per seat, its evidence is a prose receipt line, and it fills a missing timestamp from the clock (:203).
- **S4, a per-lane git ref now:** rejected (2.65). It builds ADR-121 D3 before the single-writer and fold decisions are made. It is a flip target.
- **S6, intake 80's LANE-STATE.yml written by the lane:** rejected (1.95). The model writes it, which the AJ ruling excludes. Its fields survive as D3's kinds.
- **R0, brief rules as prose; R2, a separate brief organ:** both rejected in favour of D8's header, checked by the existing gate before fan-out.
- **K2, a clarification pass at lane boot:** rejected. It asks after the Done-contract is frozen, when the answer can no longer change it.
