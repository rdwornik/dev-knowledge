# Archive copy of transport file DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 479b452034cab09a. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
supersedes: none
summary: Read-only answer to the four-part order (token burn, handoff and seat cleanup inventory, archive inventory, two Conductor E facts). Tokens: ccusage works; 1.07 B of 1.13 B tokens since 10-12 are cache reads, so the burn is long contexts times many turns, not polling. Cleanup: /handoff-verify is still defined and wired in the repo, not in ~/.claude; BU lane L5 does not cover removing it and is not launched; NO dispatcher is running now. Archive: 148 transport files since 10-14, none has a same-named home on main. D: fallback B has no declared firing mechanism beyond a SessionStart hook in the #689 build list; Actions minutes are 11,805 gross, $0 billed.
by: dispatcher-bu (Claude Code claude-sonnet-5-5, seat 636ce8d7, unbound at the 15:50 cycle hand-over)

# TOKEN BURN, HANDOFF CLEANUP, ARCHIVE AND CONDUCTOR E FACTS (2026-10-15)

Read-only. Nothing was launched, stopped, deleted or changed; the only writes are this file and its ANNEX (`DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15-ANNEX.md`, which holds every table and raw finding verbatim). Parts B and C were gathered by two read-only subagents; the quotes below are theirs, and two of them (the `handoff-verify` hit list for `docs/handoffs/*` and the janitor dry-run numbers) I did not re-run myself. Plan of record read: `DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md` v2 section 3. I did not read `LEDGER-dev-knowledge.md` v210 end to end; the subagents quote it where it matters (line 15).

## First, one live fact

**No dispatcher is running.** I handed over at 15:50 and unbound; the successor has not been started (the `OPERATOR-ACTION: start successor` line is in `SESSION-dispatcher-bu-2026-10-15.md`). The `queue --watch` pass ended at its 3600 s deadline with `lane-bu-1536-routing` and `lane-bu-1450-boot-v2` (L5) still QUEUED, so **nothing will launch them** until a dispatcher re-runs the queue call after `lane-bu-1537` / `lane-bu-1539` merge. The four fired lanes (863, 1535, 1537, 1539) are working.

## PART A - token burn

**Source:** `npx ccusage@latest daily --since 20261012` and `session --since 20261014`, both exit 0 (the JSON has trailing npm notice text, so I parsed the first JSON value). Costs are ccusage's **API list-price estimate**, not plan quota: ccusage cannot see the weekly limit, so it cannot reproduce the operator's 54%. The harness's own `[cost]` line ($1,415.88 over 125 lanes, floor, one model unpriced) uses a different window and lane set and is not comparable to these numbers.

### A1. Per day, all agents (claude, codex, copilot, antigravity, grok)
```
day         input      output     cache-write   cache-read     USD
2026-10-12  112,803    174,136    2,277,538     34,318,578     23.03
2026-10-13  3,258,227  1,876,315  25,746,716    426,571,689    271.10
2026-10-14  1,903,533  1,417,181  9,946,254     276,428,881    110.28
2026-10-15  1,194,139  1,448,907  7,555,851     330,985,979    125.59   (so far)
total       6,468,702  4,916,539  45,526,359    1,068,305,127  529.99   (1,125,327,848 tokens)
```
**95% of all tokens are cache reads.** Output is 0.4%.

### A2. Per model, sessions active since 10-14 (127 sessions, $239.19)
```
claude-opus-5-5        in 4,888    out 1,592,161  cacheR 433,992,225  cacheW 6,203,537  $163.96
claude-sonnet-5-5      in 2,304    out   759,872  cacheR 120,809,634  cacheW 7,736,251  $ 40.92
claude-sonnet-5.5 (copilot) in 946 out   319,759  cacheR  30,074,270  cacheW 3,126,581  $ 14.03
gpt-5.6-terra          in 933,921  out    67,123  cacheR   5,989,430                    $  7.86
gpt-5.6-sol            in 423,848  out    27,446  cacheR   1,641,344                    $  5.80
others (gemini flash, grok x2, gpt-6 astra/luna, haiku, claude-sonnet-5)               $  6.6
```

### A3. Claude sessions active since 2026-10-14 (every one over $1; full 127-row table in the ANNEX)
Tokens are the sum over models: output / cache-read / cache-write in thousands (input is under 2,000 tokens each, so omitted). Wall = first to last transcript timestamp, not active time.
```
session   name / order it ran                         wall    out k   cacheR k   cacheW k   USD
ab339d52  batch-green-main-pilot dispatch (10-14)     7.4 h   357     95,536     3,055      32.40
7b6e040e  codespace-batch-finish (10-14)              5.8 h   284     73,353     2,070      26.32
3b89474e  batch-build1-prep-amend (10-15)             0.9 h   230     47,910       947      17.62
28cc9f14  lane-bu-1535-outer-loop (live)              2.1 h   206     48,274       755      16.38
18d1781a  lane-bu-863-prompts-guard (live)            2.1 h   170     46,907       639      14.45
b85d73fc  batch-test-graph-data-2026-10-15 (S1)       1.3 h   160     31,376       714      13.86
db75a3c3  lane-bu-1539-transport (live)               2.1 h   113     30,645     1,551      13.78
43f6418c  lane-bu-1537-codespace-finish (live)        2.1 h   183     39,573       683      12.91
3cdb5b69  integrator-bu-2026-10-15 (live)             3.5 h    79     26,300       313       8.98
3090b73b  batch-design-outer-loop (10-14)             0.6 h   109     18,359       326       8.47
cae209ca  batch-define-outcomes-2026-10-15            0.8 h    90     19,737       267       7.89
4a74c271  branch-deletion-archive-tags (10-13..14)    17.4 h*  57     14,486       441       7.56
2cbf27b3  (unnamed, 10-14)                            0.2 h   115      9,962       804       4.55
d3b53ee5  (unnamed, 10-14)                            0.3 h    52      6,949       179       3.86
4e51a080  NV integrator/dispatcher (10-14)            0.8 h    27      7,337       112       2.90
636ce8d7  dispatcher-bu-2026-10-15 (me)               2.2 h    21      4,901       239       1.49
the six nv-929/689 lanes (Sonnet 5.5)                 0.4-12 h  18-34  3-8 M      113-232    1.26-1.67 each
```
`*` 17.4 h is the first-to-last span of a session that was idle most of it.

### A4. Integrator and dispatcher: wakes that found nothing
Counted from the transcripts: a notification message followed by an assistant turn that made no tool call.
```
seat                         notifications   wakes with no tool call   est. cost of those wakes
integrator-bu (3cdb5b69)          3                  1                   under $0.1
dispatcher-bu (636ce8d7, me)     13                  8                   about $0.1-0.2 (51k tokens of context per turn)
codespace-batch-finish 7b6e040e  49                 33                   about $1.7 (6% of its $26.32)
green-main-pilot dispatch ab339d52 27               10                   about $0.7 (2% of its $32.40)
```
The empty-wake cost is small because each one re-reads the context once (about $0.01-0.05). **Polling is not where the tokens go.** My own 10-minute heartbeat Monitor produced 8 empty wakes at roughly 51k context each; that is the dispatcher's whole polling cost, under $0.2.

### A5. Top 3 consumers, split by turn type
Method: each assistant turn (deduplicated by message id) is classed by its tool calls. Polling = Monitor, ScheduleWakeup, TaskStop or sleep. Reading = any other tool (Read, Grep, Bash and so on). Producing = a Write or Edit, or a turn with no tool call (this includes the empty wakes above). USD is my estimate from the token mix scaled by the ratio that fits ccusage's own number; treat as approximate.
```
consumer (USD per ccusage)                    polling      reading       producing
1. ab339d52 green-main-pilot dispatch $32.40  4 turns 2%  63 turns 25%  178 turns 74%  (113,964 output tokens)
2. 7b6e040e codespace-batch-finish    $26.32  10 turns 4% 40 turns 16%  193 turns 80%  (87,607 output tokens)
3. 3b89474e batch-build1-prep-amend   $17.62  0 turns     37 turns 16%  139 turns 84%  (164,083 output tokens)
```
**Reading the result:** the cost is the context carried on every turn. Each session ran 250 to 530 turns at 200-250k tokens of cache read per turn, so cache reads are 75-80% of every bill. Producing is largest because 'producing' includes long Write turns and the output-heavy build1-prep (164k output tokens in 0.9 h). Seats that live for hours (ab339d52 7.4 h, 7b6e040e 5.8 h) pay the context bill on every one of their 500 turns; the cycle hand-over (about 2 h) is the right lever, and neither of the two biggest sessions had one.

**What I cannot say:** why the weekly limit stands at 54%. That figure is plan quota on the operator's side; ccusage prices tokens at API list price, and the `/usage` number depends on plan weights I cannot see. I also did not see the 10-13 sessions' transcripts beyond the daily total ($271.10 on 10-13, the largest day).

## PART B - handoff and seat cleanup inventory (list only)

### B1. Where `/handoff-verify` is still asked for or mentioned
- **~/.claude (commands, skills, agents, settings*.json, plugins): zero hits.** `git grep -i handoff-verify -- templates`: zero hits.
- **Live definition and wiring (repo):** `.claude/commands/handoff-verify.md:2: name: handoff-verify` (6 hits); `.claude/commands/handoff.md:23,27,167,260`; `.claude/generated/commands-repo.md:13`; `.methodology.yaml:75: - component: command-handoff-verify`; `ecosystem/parity-surfaces.yaml:978,981,1086`; `ecosystem/transport-registry.yaml:906-907: prefix: "HANDOFF-VERIFY-"`; `ecosystem/seat-ids.yaml:667-668`; `scripts/verify_handoff_probes.py:886,893,930,993`; tests `test_gen_handoff.py` (5), `test_seat_release_moment.py` (3), `test_v6_frozen_contract.py` (4), `test_verify_handoff_probes.py` (4), `test_assemble_paste.py:717`, `test_transport.py`; `.github/workflows/conductor.yml:724`; `CONTRIBUTING.md:263`; ADR-82 and ADR-128.
- **Boot prose that still teaches it as the gate:** `protocols/HANDOFF_PROCESS.md:297: v6, **one CC-side command** (\`/handoff-verify\`, R1) runs every verification against live state` (9 hits: 297, 312, 316, 692, 1327, 1426, 1433, 1586, 1606); `protocols/OPERATOR-INTERFACE.md:130`; `docs/handoffs/README.md:132-133,172,239,259`. **Correct (negations):** `protocols/HANDOFF_BOOT.md:29` and `docs/handoffs/2026-10-14-dev-knowledge-architect/SUPPLEMENT.md:175` say no `/handoff-verify`; `STANDING_RULINGS.md:5060` is R30, "the browser seat boots without `/handoff-verify`".
- **Stale transport copies that still ask:** `to-browser/PASTE_THIS.md:224`, `to-browser/PASTE_THIS-2026-09-19-dev-knowledge-architect.md:213`, `to-browser/HANDOFF_BOOT-2026-09-06-architect.md:73` ("5. **Ask CC for `/handoff-verify`, then paste its ONE evidence block.**"), plus `BROWSER-SEAT-FLOOR-DRAFT-2026-09-06.md:37`, `PIN-2026-09-08.md:23`, `DIGEST-2026-09-08.md:12`, and the two evidence blocks `HANDOFF-VERIFY-2026-09-08-architect-2.md` / `-09-10-architect.md`. About 351 further hits in the transport are history.
- **Status of the retirement:** `to-cc/BATCH-AUDIT-SPINE-AND-TOOLS-2026-10-04.md:49: /handoff-verify was approved for retirement (R30, R66 A2), yet it still exists.` `to-cc/ANSWER-SEAT-CHECKLIST-2026-10-10.md:1102: ... /handoff-verify (R30 retired it for the browser boot only; lane 11 kept it).`

### B2. Non-live handoff and boot artifacts
Canonical: `protocols/HANDOFF_PROCESS.md` (v7, stamp 7.1.0), `protocols/HANDOFF_BOOT.md`, active bundle `docs/handoffs/2026-10-14-dev-knowledge-architect`. Table (path, superseded by, referenced, janitor) is in the ANNEX section B; summary:
- **130 older bundles under `docs/handoffs/`** are immutable (CLAUDE.md rule 3); janitor does not touch repo files.
- **Stale transport copies (janitor: NO, no "superseded" in the name):** `HANDOFF_BOOT-2026-09-06-architect.md` (referenced by `INDEX.md:642`, `seat-ids.yaml:669`, `tests/test_transport.py:194`), `PASTE_THIS.md`, `PASTE_THIS-2026-09-19-...md`, `PASTE_THIS-2026-10-08-...md`, `PIN-2026-09-07.md`, `PIN-2026-09-08.md`, the two `HANDOFF-VERIFY-*` evidence blocks.
- **`to-browser/LEDGER-dev-knowledge-v204..v209-superseded-2026-10-15.md`:** each superseded by the next, the head by `LEDGER-dev-knowledge.md` (v210); **janitor handles all six** (they appear in its dry run).
- **`to-cc/PLAN-HARNESS-2026-10-15-withdrawn.md`:** the live plan is `to-cc/PLAN-HARNESS-2026-10-14.md`; the ledger marks this one withdrawn (r8). Referenced only at `LEDGER-dev-knowledge.md:15`. **Janitor does NOT handle it**: `scripts/transport.py:538 _SUPERSEDED_RE` and `:1084 if not _SUPERSEDED_RE.search(path.name)` match only the word "superseded", never "withdrawn". Two other `-withdrawn` files share this.
- **Janitor dry run** (flag-less, `scripts/transport.py:35-36`, nothing moved): `live: 2298  archive: 279  moves: 305  skipped: 7  untouched: 1986`, manifest `ca2319dcb869062b0541ce6cd6a71751abca1588737c319221f85fcdc27aca4b`. It also moves `to-cc/AMEND-HANDOFF-BOOT-DISPATCH-SECTION-2026-09-20-SUPERSEDED-wrong-command.md`, which `STANDING_RULINGS.md:4575`, `seat-ids.yaml:1737` and others cite by the old path; the registry readers glob `archive/*/` (`scripts/transport.py:1029`), but the name-keyed lookups in `tests/test_transport.py` were not checked. Its 7 skips are UNATTRIBUTED or unregistered files.

### B3. Seat hygiene
- `no_leftovers.py verify` (no args, read-only husk scan): `FAIL husk directory (unregistered with git): ...\.claude\worktrees\integrate-bu [0 top-level entries]` / `NOT CLEAN (1 leftover(s))`. Branch `worktree-integrate-bu`, its origin copy and `chore/bu-merge-receipts` still exist.
- **Worktrees:** `define-outcomes-2026-10-15` (job cae209ca, state done) and `test-strategy-rows-2026-10-15` (job b85d73fc, state done) are still **locked** with pushed branches. A temp `fleet-health-producer-8sgbcg4e/wt` detached worktree is a fleet_health artifact. No worktree exists for L5 (`lane-bu-1450-boot-v2`) or `lane-bu-1536-routing`.
- **Stale claims in `to-cc/` (no live job):** `LANE-1423-b2w2-codespace-finish.CLAIMED-fed25fc7`, `...-resume-1.CLAIMED-d56342c0`, `LANE-1439-b2w2-transport-index.CLAIMED-3e770e56`, `LANE-1443-b2w2-boot-teaching.CLAIMED-244a8e74`, `LANE-1444-b2w2-merge-clock.CLAIMED-d8d63b99`, `...-resume-1.CLAIMED-80dbac44`. The five live claims match working jobs (`INTEGRATOR-BU`, `LANE-bu-1535/1537/1539/863`).
- **Seat registry:** 9 to 16 session ids are bound to each BU lane slug (many `wedged`, SessionStart but no Stop), but each lane has exactly one job; **no session id appears twice**. The NV batch rows are all `absent`. `b85d73fc` is `live unbound` and `cae209ca` `wedged unbound` though both jobs are done; `c81e7015` is working but `wedged` in the registry. The registry, not the job record, is the one that disagrees.
- **Live background sessions -> order:** `18d1781a` lane-bu-863-prompts-guard -> `LANE-bu-863-prompts-guard.md`; `28cc9f14` -> `LANE-bu-1535-outer-loop.md`; `43f6418c` -> `LANE-bu-1537-codespace-finish.md`; `db75a3c3` -> `LANE-bu-1539-transport.md`; `3cdb5b69` integrator-bu (state blocked: "start the successor integrator with the `claude --bg ...` command from the receipt's OPERATOR-ACTION line") -> `INTEGRATOR-BU-2026-10-15.md`; `636ce8d7` dispatcher-bu (state blocked, no longer bound) -> `DISPATCHER-BU-2026-10-15.md`; `c81e7015` **graph-data-test-batch-run** -> `to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md` (census leg S2).
- **Commit 496b0951:** `docs(tasks): file rows [#1560]-[#1568] and intake 115 for the R119/R120 test strategy decision`, tip of `worktree-test-strategy-rows-2026-10-15`. It was made by job `b85d73fc`, whose **name** is `batch-test-graph-data-2026-10-15`; it ran `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md`. `graph-data-test-batch-run` is a **different job** (`c81e7015`) running the sibling `BATCH-TEST-GRAPH-DATA-2026-10-15.md`. The session name follows the batch family umbrella; the branch follows the content. No shared id, no session in two records; the "naming anomaly" in `LEDGER-dev-knowledge-v208-superseded-2026-10-15.md:25` is resolved.

### B4. Does BU lane L5 (`LANE-bu-1450-boot-v2.md`, rows [#1450] [#1538]) cover removing B1 and B2? **No.**
- **Owned files (l.90):** `protocols/HANDOFF_BOOT.md`, `protocols/STANDING_RULINGS.md` (a NEW section after §AT only), `tests/test_standing_rulings_sources.py`, the boot tests, and the files of the carried branch `worktree-lane-bw-1450-boot-teaching`, rebased on `origin/main`.
- **Done-when [#1450]:** "(1) `protocols/HANDOFF_BOOT.md` states the R80 order ... and names `to-browser/INDEX.md` as the first read, its version bumped, and a test over the file finds both; (2) the file stays within its byte budget (`scripts/assemble_paste.py` caps it at 18,000 B); (3) RED-first: that test fails on `03d21ff8` and passes after the change". **[#1538]:** "RED first: (1) a new section in the §AT shape lands every existing heading R100-R102 and R104-R115 ... (3) `uv run --locked python scripts/decision_coverage.py rulings` reports 0 unlanded among them". Done-contract item 5: "... HANDOFF-GAPS items 1, 2, 4 and 5 read as given; **v5/v6 leftovers** and the HANDOFF-GAPS Q3 contradictions are gone." That covers leftovers **inside `HANDOFF_BOOT.md` only**, whose line 29 is already correct.
- **Not covered:** the command file, the four registries, `HANDOFF_PROCESS.md`, `docs/handoffs/README.md`, `OPERATOR-INTERFACE.md`, `verify_handoff_probes.py`, and every transport file in B1/B2. The contract bars creating any path it does not name, and `scripts/transport.py` is barred for lane 1539. Removal needs its own row.
- **Launched? No.** Last queue line: `[queue] watch ended after 50 poll(s): fired 4, held-failed 0, routed-codespace 0, of 6; DEADLINE -- still pending: lane-bu-1536-routing, lane-bu-1450-boot-v2`. State QUEUED; no worktree, branch, claim or job. Its gate is "Starts after `lane-bu-1539-transport` is merged"; the 1539 tip `a5ff5843` is not merged and its job is still working.

## PART C - nothing wasted

### C1. Files changed since 2026-10-14 00:00 (full table in the ANNEX section C)
**148 files**: about 105 in `to-browser/`, about 43 in `to-cc/`; includes many `-vN-superseded` copies, 25 LEDGER versions, 9 RATIFICATION versions and 5 `.CLAIMED-*` markers. **None of the 148 has a same-named tracked file on origin/main or on any unmerged branch.** About 30 are cited by name from tracked files, e.g. `DIGEST-BUILD1-READY-2026-10-15.md` from `JOURNAL.md` and `docs/audits/2026-10-15-technical-batch-bu-manifest.md`, `DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md` from `tasks/1535-...` and `tasks/1538-...`. A citation is not a home. Two DIGESTs are cited only from rows on unmerged branches: `DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md` (branch `worktree-define-outcomes-2026-10-15`) and `DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md` (branch `worktree-test-strategy-rows-2026-10-15`).

### C2. Proposed homes for decision and analysis records (rules quoted; none inferred)
- **The rule that exists:** `protocols/STANDING_RULINGS.md:3664`: "Everything written to `to-browser/` is a GENERATED copy: the repo stays the single source". DIGEST files have no repo source, so they got the reverse; **I found no rule that says what to do in that case.**
- **The only governing rule for a repo home:** `docs/decisions/ADR-101-hermetization.md:64` (Rule B) requires `docs/audits/<date>-<class>-<slug>.md` with the class from the closed list in `ecosystem/fleet-shape-spec.yaml:374-385`; Rule A (`:63`) bars a new `docs/` folder. "digest" is not a class. Proposal: `docs/audits/2026-10-15-technical-<slug>.md` for a DIGEST the operator wants kept. **No rule requires copying DIGEST-* files in.**
- **RATIFICATION decisions** land in `protocols/STANDING_RULINGS.md` ("Landed by `lane-...`" precedent); row `tasks/1538` on main is the open vehicle. **LEDGER, SESSION, STATE and LANE-END** files are transport-only per `OPERATOR-INTERFACE.md:114-125`. **To-cc contracts** (BATCH, AMEND, PLAN): no rule found for a repo copy.

### C3. Pushed branches not on main carrying records from this window
- `worktree-define-outcomes-2026-10-15` @ 69ab3bc9: 1 ahead, 0 behind, 10 files. Has `kill-candidates: none`, **no JOURNAL change** (so no anchor). Needs a `--no-ff` merge.
- `worktree-test-strategy-rows-2026-10-15` @ 496b0951: 1 ahead, 0 behind, 14 files. Has `kill-candidates: [#1383]`, no JOURNAL change. **Both rows branches edit `tasks/manifest.json` and `docs/intake/manifest.json`, so the second merge will probably conflict** (not test-merged).
- `worktree-codespace-sample-2026-10-14` and `worktree-lane-bu-1537-codespace-finish`: 51 ahead, 0 behind, 25 and 23 files; only the sample branch carries a JOURNAL change. `worktree-codespace-finish-2026-10-14`: 43 ahead, 30 behind, JOURNAL says "REFUSE after round 2"; 1537 carries it forward at `f7cc1ef6`.
- `chore/bu-merge-receipts` adds one receipt line. The two bw lane branches and `integrate-bw` date from 10-13, `b2w2-codespace-finish` from 10-10, `automation/fleet-audit` has no merge base with main.

## PART D - two facts about the decided Conductor E (no design)

### D1. In fallback B (local), what fires the [#669] transitions and the doit spine runner?
**No document I read names a firing mechanism for B.** What is stated:
- `DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md` D2: "B is 'same task files, same graph, same phase table, run locally'." Nothing says what starts it.
- The `[#689]` row (`tasks/689-conductor-e-is-decided-and-unbuilt.md`) lists its build: "**1. `conductor.yml` + ruleset. 2. `phase:` field + validator. 3. SessionStart hook.**" That is the only trigger named for the local leg, and it is in the build list, not described.
- `DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md` section 2 table gives the **trigger per [#669] transition**, as data conditions, not as an actor: T1 intake `ACCEPTED` with no carrier row (action: propose, "operator files it"); T2 frozen contract, plan_lint 0, preflight 0 (action: dispatch launch); T3 "the lane's merge_receipt record on main (logs/MERGE-RECEIPTS.jsonl)" (action: `gen_task_tree --emit-source`, telemetry consumer, `propose_closures`); T4 "operator closure approval" (action: `archive_row_body.py`). Its ordering note: "B6 last (without B5, T3 runs by hand)" and "Q2 ... Without the waiver, B5 drops and T3 runs by hand."
- So today a transition fires **by a seat** (the dispatcher, the integrator or the operator), not by a hook or timer. The dispatch queue (`dispatch.py queue`) launches lanes (T2) but it is a verb a seat runs; this session's `queue --watch` ended at its deadline and did not resume.

**[#669] Done-when:** "each of the four transitions fires from a declared trigger with a trip-test proving it fires and a test proving it does NOT fire on the state before it; the operator's five decisions remain the only manual transitions and are named in the machine rather than implied; `archive_row_body` runs from its trigger rather than by hand; and emitted telemetry has a named consumer that reads it on the merge leg".
**[#689] Done-when:** "the four numbers of `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` section 6 move ... 1. Phase transitions without operator action / all transitions - today ~0%, target > 80% (Actions logs). 2. Operator hours per feature landed in corp-monorepo ... 3. Operator pastes per week - today dozens, target < 5. 4. Organs deleted from the section 5 list - target >= 10. If 1 and 3 do not fall, revert to B."
**What BU L1 (`LANE-bu-1535-outer-loop`) builds toward it:** per its Done-when (2), "the HY `phases:` table drives P1-P7 as one doit run per round through `conductor.py lane --round r` (at most 2 rounds)", with `run_phase(argv, timeout_s)` that kills the process tree, PhaseReceipt v1, constraints as data, `distill`, CHALLENGE, and `doit -f scripts/dodo.py spine` stage 1 passing on a `tasks/` row. **It builds no trigger for any [#669] transition**: its contract says `[#669]` is "related, not closed by this lane" and "Do not add python-statemachine ... the psm leg is `[#669]`'s, after its spike (CHALLENGE M4)". Its `conductor.py lane` subcommand is something a seat invokes.

### D2. GitHub Actions minutes: 364% or free?
**Both numbers are real, they measure different things, and neither means anything is being charged.**
- `uv run --locked python scripts/quota_watch.py report` (read-only; `check` is the Codespaces-core-hours veto and needs `--projected-core-hours`): `actions_minutes: 11,805.00/3,000.00 minutes (393.5%), burn 843.214/day, exhaustion 2026-10-15` / `billed: none this cycle`. The v2 digest's "364% (10,921 of 3,000)" is an **earlier reading of the same counter**; it has since grown.
- The raw call quota_watch uses, `gh api users/rdwornik/settings/billing/usage/summary` (billing month 2026-10): `actions_linux grossQuantity 11805.0, discountQuantity 11818.0, netQuantity 0.0, grossAmount 70.83, discountAmount 70.908, netAmount 0.0`; `actions_windows grossQuantity 10033.0, discountQuantity 10033.0, netAmount 0.0`.
- `gh api repos/rdwornik/dev-knowledge` -> `{"private":false,"visibility":"public"}`. `ecosystem/quotas.yaml:56-60`: "The hub has been PUBLIC since ~2026-09-15, so its GitHub-hosted Actions minutes are free regardless of this declared quota (RATIFICATION-2026-09-25 R9 correction) -- this row still tracks USAGE against the historical private-repo allowance; `first_billed_dollar` is the figure that actually says whether anything is being charged."
- **Which is current:** the 11,805 gross and the 100% discount (net $0) are current; the 3,000 quota is the historical private-repo allowance. The R116 CHALLENGE ("CI on the public repo is free") is the correct reading. The v2 sentence "Actions minutes are at 364% of the included amount" is a quota counter against a limit that no longer applies; as a reason to prefer fallback B it rests on a stale premise. The row [#689] already recorded this: "**One fact neither section 7 nor the amendment anticipated ... the repo is PUBLIC.** ... Three surfaces assert a visibility the API contradicts." Windows minutes (10,033 gross) are free for the same reason.

## What I could not verify
- Why the weekly plan limit is at 54% (plan weights are not visible to ccusage).
- The 10-13 sessions (the largest day, $271) beyond the daily total.
- The `handoff-verify` hits inside `docs/handoffs/*` bundles and the 351 transport history hits: counted by the subagent, not re-run.
- Whether `tests/test_transport.py` name maps break if the janitor moves the cited files.
- Whether the second rows branch merge conflicts (not test-merged).
