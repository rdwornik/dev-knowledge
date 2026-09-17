# LANE lane-ac-694-cloud-census — Read-only cloud census - organ calls versus raw scans, row age and abandonment, landed versus claimed, live ARCHITECTURE bytes

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `gen_task_tree` over `tasks/` -- the row set and its ages (FROM THE ORGANS FIRST; git only for what they cannot answer)
- `file_purpose_graph.py` (FPG-1) + `graph_queries.py` -- relationships and stats
- `ecosystem/organ-index.md` -- the organ roster the call/scan ratio is measured against

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#694]` PRIMARY -- **AX9-5 is owned by THIS row**, whose body carries the metric clause verbatim. The night order cites "AX9-5 (`[#685]`)"; that citation is WRONG and the correction is binding here.
- `[#747]` -- consumes AX9-5's counter (the rolling 30-day invocation window per organ); ONE counter, not a second telemetry path
- `[#685]` -- the operator-GO artifact row. **PAIRED WITH `[#694]` IN ONE LANE BUT A DIFFERENT ROW** -- `[#694]`'s own body says so. Do not merge them.

**Library ladder** for anything genuinely new: stdlib > established dependency > proven project > industry pattern; hand-roll only on a MEASURED divergence, recorded so it is not relitigated.

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

**Kind:** `text` — text-only, deletion, or read-only digest — prose, rows, rulings and removals; no executable code changes hands.

The kind is DECLARED, not inferred, and it is what the routing default keys on
(`[#885]` clause 2). A text-only, deletion or read-only-digest lane never starts on
Opus; a review lane is not dispatched from a lane contract at all, because
`ecosystem/routing-table.yaml` is the authority for which CLI runs that role; a code lane
plans on Opus and implements on Sonnet **as two sessions with a file between them**,
never as one session changing tier mid-flight. The prompt cache is keyed PER MODEL,
so a mid-session switch re-writes the whole context: at this repo's measured mean of
232,875 tokens per call, one switch costs USD 1.46 into Opus or USD 0.58 into Sonnet
against USD 0.0812 saved per turn moved — about 25 consecutive cheap turns to repay
one round trip. Anything shaped like plan-then-execute is TWO SESSIONS.

```
Dispatch-CloudV2 LANE-ac-694-cloud-census.md -Title 'lane-ac-694-cloud-census'
```

The operator runs the line above verbatim. The **whole file is the brief** — it
travels in a JSON body, so one file is one lane and never a multi-lane bundle —
and the dispatch binds Revision `main`. `Dispatch-CloudV2` carries no `-Effort`
parameter, so this lane's tier is on the record in the routing table above
(`sonnet` / `high`) rather than on the command line. Permission
mode is `bypassPermissions`, as it is for an on-machine lane.
A cloud session clones from `origin`, so every input this contract names is
pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `lane-ac-694-cloud-census` -> branch `claude/lane-ac-694-cloud-census` -> contract `LANE-ac-694-cloud-census.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created
by the cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<the session's first assistant text, echoed back>`

A dispatch missing either half is treated as not having started, and is
re-dispatched. The lane also branches fresh off `origin/main` and leaves files it
did not author and this contract does not name exactly as found (Q4).

## Done-contract (immutable)

1. **BOUNDS, STATED UP FRONT AND BINDING: agent cap 4 concurrent · per-agent deadline 20 minutes HARD · token budget 150k total.** A step exceeding its deadline is **ABANDONED with what it has, never waited on.** Model: Haiku for enumeration fan-out, Sonnet to synthesise.
2. **READ-ONLY. NO WORKTREE. THIS LANE CANNOT COMMIT.** Its output is a report handed back, not a tree change.
3. **C1a** -- ORGAN CALLS vs RAW SCANS per session across the last two weeks of transcripts, and ORGANS UNCALLED IN 30 DAYS enumerated by name. An ORGAN CALL is an invocation of an organ in the order's §4 or in the organ index; a RAW SCAN is `grep`/`rg`/`find`/`Select-String`/`git log`/`git grep` used where a listed organ would have answered. If no telemetry emitter exists, v1 COUNTS FROM TRANSCRIPTS BY COMMAND STRING; deriving the transcript location is part of the lane, and **if no transcript store exists THAT IS THE FINDING**. Building an emitter is OUT OF SCOPE -- it would be a new organ. **Note explicitly that the BROWSER SEAT carries no telemetry and is therefore absent from the count.**
4. **C1b** -- ROW AGE AND ABANDONMENT CENSUS. Per row: filing date · last commit touching the task file · last commit citing the id · whether anything still references it. Bucket by age, oldest-untouched first. Disposition per bucket: still wanted / superseded / never happening. **PROPOSE ONLY -- closing rows is the operator's act.** `tasks/` mirrors the backlog, so one census answers both.
5. **C1c** -- Landed-vs-claimed for `[#665]` `[#666]` `[#667]` `[#668]` `[#669]` `[#670]` `[#760]` `[#755]` `[#628]`. **Quote each row's live state.** Resolve the two-owner contradiction on the `ESSENTIALS.md` deletion (RESIDUAL §2 says `[#755]`; the P11 advisory says `[#628]`).
6. **C1d** -- The LIVE `ARCHITECTURE.md` byte count. The "down 22%" figure is UNSOURCED and must not be carried; produce the number.
7. **C1e** -- Read `copilot-collections` FIRST-HAND. The previous comparison used the wrong three repos (spec-kit, BMAD, superpowers).
8. **C1f** -- Phase 1 of the execution-state intake: establish what `[#664]`, `tasks/` frontmatter, `manifest.json`, FPG-1 and the organ index ALREADY hold. **Read-only. No build.** This is the input to `[#890]`.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Fan out C1a, C1b, C1c enumeration on Haiku under the 4-agent cap and the 20-minute hard deadline.
2. Run C1d, C1e, C1f.
3. Synthesise on Sonnet into ONE report; abandon any step over its deadline with what it has and say which. **Hand the report back. Do NOT commit.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
