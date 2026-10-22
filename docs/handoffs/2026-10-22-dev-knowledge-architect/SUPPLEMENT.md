# Architect strategic supplement — 2026-10-22-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-22

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.
8. **Fixed slots (Part A minimum — REFUSED if the pasted answer omits one).** Restate the
   above as five short LABELED LINES, each non-empty (`"none"` is a valid non-empty value; a
   blank line after the label is not). This is the outgoing seat's judgement in a shape the
   next session can scan in five lines without reading the freeform answer above it; Part B
   (WAVE5B-N5 B1, the `seat-release` moment) is what eventually moves them into the boot card
   itself and makes the refusal a harness transaction rather than a re-render check
   (`gen_handoff.assert_supplement_fixed_slots`). The five labels, exactly:

   ```
   Headline: <one line>
   Open threads (with carriers): <thread — who/what carries it, or "none">
   Next authorized action: <the next act this window authorized, or "none">
   Contingencies: <what changes the plan if it happens, or "none">
   Do-not-repeat: <a mistake or dead end this window found, or "none">
   ```
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
<!-- the five Fixed-slot labeled lines (Q8) go anywhere in this region, each on its own line -->

# SUPPLEMENT ANSWERS — Tech-Architect-46 (window 2026-10-17 .. 2026-10-22)

**Read first (transport to-browser/ unless noted):**
- RATIFICATION-2026-10-22.md (K1-K15: this window's last rulings), RATIFICATION-2026-10-18/-19/-20 (R129-R179);
- DIGEST-PRE-HANDOFF-INVENTORY-2026-10-22 (witnessed end state; preflight output in §7);
- DIGEST-HARNESS-MAP-2026-10-20 (+ANNEX) and DIGEST-HARNESS-STATE-2026-10-22 (the process as coded);
- DIGEST-INTEGRATION-THROUGHPUT-2026-10-22; DIGEST-CODESPACE-TELEMETRY-2026-10-21; DIGEST-GIT-AS-AGENT-MEMORY-2026-10-21; DIGEST-TEST-EXECUTION-EVAL-2026-10-20; DIGEST-AGENT-FILE-CHALLENGE-2026-10-20;
- DIGEST-E2-0-CLOSE-2026-10-20 (UPDATE 2026-10-22); HANDOVER-adr-131-accept-inflight-2026-10-22; CARRY-LEDGER-E2.0-MERGE-RECEIPTS-2026-10-22;
- PROPOSAL-ADR-SEAT-MODEL / -PROCESS-MODEL / -SUBSTRATE-2026-10-18 (ratified as R130 / R131 / R132).
- The hand-written LEDGER v285-v307 is history only. It violated the registry (K12); regenerate the LEDGER with scripts/gen_ledger.py.

## 1. Strategic intent

**Make the harness run its own loop in code, end to end.** The organs exist; the process between them is not a model in code.
- No step declares its contract (inputs, outputs, owner, model, effort, exit condition). So every new level the window reached — tests, dispatch, landing, transport — exposed an undefined seam, and a seat patched it in prose. That is why "the devil is in the details" keeps recurring.
- The direction is already ratified: **R131 (ADR-beta = B, python-statemachine, P1 first)**, R130 (dispatch triggered by the harness; the integrator only integrates), R132 (one Substrate protocol; cloud read-only), and the operator's 2026-10-18 principle (process model in code, diagram generated, one responsible module per step, library-first; code defines prose).
- Executing R131 means collapsing the **four competing process carriers** (DIGEST-HARNESS-MAP disagreement 1) into one and wiring the transitions through it. It is not a new decision.

**Operator focus areas (K15):**
1. dispatching and the feedback loop;
2. the three substrates — local, Codespace, and the Anthropic cloud, which is not working or used and must be evaluated;
3. how sessions write to Google Drive (key).

**Measurable aims:**
- main green with push-time verification;
- median landing <= 25 min with 0 model calls on a clean landing (baseline 43.9 min, ~62 Opus calls per row);
- no seat older than the R179 threshold;
- the start-up context back to ~47k tokens (today 96.4k on a dirty tree, §8.4).

## 2. Tensions weighed

- **Speed vs integrity.** "Tested merge = landed merge" is KEPT. Speed comes from script plus batching (ADR-131 D1/D5), not from relaxing CI or letting main go red.
- **Vendor platform vs own code.** The GitHub merge queue and org move are REJECTED (K2). The git-native, bors-style path wins.
- **Gates vs flow.** Permanently red advisory gates taught everyone to ignore red. R169 removed the ship-gate job. The commit-gate was KEPT (restored in ci-dedupe repair 1) because it is the only CI leg running graph task-coverage — and it is red on main now.
- **Parallelism vs closure.** More boxes do not help while landing is serial and seat-run. Opening lanes during a close costs the most time (C5, K9).
- **Prose vs mechanism.** Every seat error of this window came from acting on prose or memory where code already defined the answer (§8.6).

## 3. Considered and rejected (do not relitigate)

- GitHub merge queue + org move; Mergify; TAP last-green as the primary gate.
- The one-time model waiver W1 (withdrawn: repair, not waive).
- Raising the BACKLOG view budget (only closing open rows frees bytes).
- `--batch ""` to land a non-model change: it fails at `merge_path.py:187-191` and is a flag hack. The answer is an operator-act landing class (K1).
- Git notes for agent memory; the `history` verb; auto-close of rows from trailers; a `CI-Run:` trailer.
- Paying for more Codespace capacity before landing is fixed.
- "Declared exceptions" to git hygiene (K5).
- Updating HANDOFF_BOOT during this close (K13: route B instead).

## 4. Open questions (for the operator)

- **Carrier collapse under R131:** which of the four existing carriers fold into the python-statemachine model, and in what order. The spike at tag `archive/e21-p1-spike` (P1 dispatch TO-BE) is input. The seat made no call (K11).
- **Phase-table ruling** (map transition 5) to bind the isolated test chain (K6).
- **GPT-6 tier mapping:** the catalog has gpt-6-astra / gpt-6-sol / gpt-6-luna and no terra. Where review belongs; the open proposal is the review role -> gpt-6-sol (E2-0-CLOSE UPDATE decision 3).
- **Codespace:** per-box login link vs mirrored credential (R140); the `user` scope for the quota meter (QUOTA-DAILY-CLAIM fails without it).
- **Anthropic cloud substrate:** keep, fix or drop. R132/R171 say read-only and no tests there; nothing uses it today; no evaluation exists (K15).
- **Landing trailers** (`Rows:` `Decided-by:` `Models:` `Suite:`): an ADR amending ADR-85 (DIGEST-GIT-AS-AGENT-MEMORY).
- Further operator decisions from E2-0-CLOSE: arm `ecosystem/test-flow-ceilings.yaml`; tag v1.5.0 (unblocks the seat-cycle consumer parity run); the AGENTS.md review stamp; file the READY-TO-FILE rows R1-R22; the devcontainer bubblewrap carrier lane.
- R180-R184: sources needed (cited, never ratified).
- Lazygit tracked config path (needs a GO for a new path).

## 5. Decomposition (next-window order; do NOT redo or re-decide)

0. **Boot truth (K13, K14).** Rewrite protocols/HANDOFF_BOOT.md so its facts are generated from code (gen_handoff already derives the rows). Add a truth check beside `boot_citations`. Design the handoff update process: what the handoff verifies mechanically, what the browser seat must know, what it need not know. §8.3 lists the stale claims. The Project copy must be re-uploaded by the operator after it lands.
1. **Main green before 2026-10-31.** The 40 known-reds registry members all expire 2026-10-31; after that every landing reads red. Today: 38 main-state reds, commit-gate red, and `tests/test_routing_agreement.py::test_the_live_table_is_well_formed` red with no owner. Restore push-time verification of main (e2-ci-dedupe removed the main push run; ADR-131 D1's post-landing re-read and the nightly are the backstops).
2. **Operator-act landing class**, then the ADR-131 flip from its tag (K1). The first merge appends the line in CARRY-LEDGER-E2.0-MERGE-RECEIPTS-2026-10-22.md (sha256 7578da64...df28b74). The final JOURNAL (i) text and the F2 per-test list sit in the laptop job dir `jobs/6e369dfa/tmp/` (ji-final.md; cycle-10 receipt). Claude Code preserves jobs/, but carry them into the CARRY-LEDGER at the start.
3. **Execute R131:** one process carrier. Every step declares owner, model, effort and exit condition. Today no file declares effort.
4. **Wire the transitions, integration first (K8):**
   - `scripts/land_lane.py` becomes the only landing path (it has no caller; landing is seat-run via `.claude/commands/lane-integrate.md`), then batching (ADR-131 D5);
   - handback -> integrator wake (#1661);
   - dispatch and the feedback loop (K15): queue -> substrate, refusal -> repair, landed -> row_close (#1637);
   - box lifecycle (#1662 #1657 #1658): fix `_box_size_and_hash` (scripts/dispatch.py ~:4074 passes `sh -c` and its command as separate argv, so delivery fails closed and the box SESSION file is copied by hand); land the devcontainer bubblewrap/runArgs carrier (commits 23ea91c9, 74a48ceb, not on main);
   - evaluate the Anthropic cloud substrate (K15).
5. **Transport writes in code (K12, K15):**
   - seats write through `transport.py`;
   - the LEDGER comes from `gen_ledger.py`;
   - a sweep runs at wake (#1435 #1577);
   - triage the 318 historical hard lint findings (279 lane-contract-no-r59-proof, 21 no-by, 15 wrong-folder — including the previous seat's SUPPLEMENT-ANSWERS-TA45-2026-10-17 in to-browser — and 3 unknown-kind).
6. **Tests:**
   - `scripts/test_run.py` (R167 L3, not on main);
   - the isolated test chain (K6, transition 5);
   - the test lifecycle;
   - the suite currently runs ~5 times per landing (range 2-9).
7. **Backlog as a process stage:** 758 open rows; BACKLOG.md 159,887 / 160,000 B. Close-or-kill; file the READY-TO-FILE set.
8. **Agent file (R173/R176):** delete the 49 DUPLICATE/HISTORY lines; add `ecosystem/hand-rules.yaml`; persist the six Drive-only rules (R153 R156 R158 R159 R166 G29). CLAUDE.md on main is 20,647 B.

**Do NOT re-decide:**
- landing direction e+b (ADR-131 ratified);
- no org move;
- R130-R132;
- R167-R179;
- the model rule (K3);
- H1 (no new rows until backlog cleanup);
- K1-K15.

## 6. Off-repo context (changed intent only)

- The operator's tolerance for prose patches, repeated diagnoses and seat self-made lists is exhausted. Start from the plan of record and the code, not from rediscovery.
- Every recommendation needs CC research first and code evidence. A known problem is not a discovery.
- The integrator must not take this long, and tokens must be watched: the operator exhausted the weekly allowance fast last week, and there is no instrument for it (R154).
- The operator is dissatisfied with how hard handoffs are (K14).
- Codespace is a wanted parallel substrate once landing is fixed (K8).

## 7. Ratified register

Everything ratified this window is in a RATIFICATION file:
- R129-R147 in -2026-10-18;
- R148-R159 in -2026-10-19;
- R160-R175 in -2026-10-20;
- R176-R179 in STANDING_RULINGS §AY;
- K1-K15 in -2026-10-22.

Code carriers on main (witnessed 2026-10-22): routing-table, seat_cycle.py, subst_gate.py, handback.py, test_os_split_gate, test_flow_metrics.py, land_lane.py, view_budget.yaml. The R167 L3 carrier, the R160 batch grammar (BATCH_TOKEN is still `[a-z]{1,3}` at validate_branch_naming.py:92), ADR-131 Accepted, and the one-line CLAUDE.md are NOT on main.

## 8. Onboarding pack for the next architect

### 8.1 What runs automatically vs what a seat does by hand

DIGEST-HARNESS-MAP: 22 transitions, of which 13 are USED/WIRED, 4 BUILT-unused and 5 DECIDED-only. **Only 3 fire without a seat.**

- **WIRED in code:** dispatch, pre-launch, lane-end; the transport write gate (for callers that use it); the gen_handoff preflight (12 rows).
- **BUILT but no caller:**
  - the phase chain red/implement/qa/review/judge via `run_phase.py` / `conductor.py run_round`;
  - `handback.py` as a trigger;
  - the distiller (gen_lane_contract distill);
  - the queue;
  - seat self-launch;
  - `land_lane.py`.
- **Seat by hand:** integrate, land, teardown, batch-close, handoff and plan-lint; Codespace handback delivery. TODAY-GLUE lists 27 hand steps (G1-G27).
- **Prose only:** intake filing, seat release.
- **Nightly routine `dev-knowledge: nightly-conformance`** (scheduled task, model claude-sonnet-5): reports SUCCEEDED in ~90 s every night, but its last digest in docs/audits/ is 2026-08-10. It is green without output — fix it or retire it.

### 8.2 Works / does not work, by topic

- **Landing:**
  - Measured: median 43.9 min (11.6 pre-push, 17.9 CI wait, 0.8 after).
  - `merge_path.land` polls 900 s, shorter than CI.
  - 5 of 22 landings pushed twice.
  - `land_lane.py` is on main and unused. The ADR-131 flip is held (K1).
- **Model routing:** WORKS (routing table + catalog probe; gpt-6 in the table). The MODELS gate refused Copilot implement phases because Copilot Auto served gpt-6-luna instead of the pin, so always pin `--model`.
- **Codespace:**
  - fix landed (08ec7be68);
  - Codex in the box works on path (i), bwrap + user namespaces, gpt-6-sol;
  - delivery breaks (`_box_size_and_hash`);
  - max 2 concurrent boxes;
  - 79.49 / 180 core-hours used.
- **OS split:** on main. Linux by default; WINDOWS_ONLY_TESTS has 25 entries (30 tests).
- **TDD:** Copilot writes RED tests (R177). There is no test runner off the laptop (R167 L3 missing). Main is never green.
- **Distillation:** landed, unused. In real use it produced 4 candidate rows. Defects: the conductor's phase table differs from the lane contract; `--json-schema` rejects the schema; served_model is always null; stdin is DEVNULL; #1669 clause 2 is not done.
- **Agent-file challenge:** C1-C7 PASS on CLI 2.1.304. A CLAUDE.md in the cwd or an ancestor silently disables the AGENTS.md fallback. The merged file (~33.9 KB) exceeds Codex's 32,768 B cap. Nothing adopted.
- **ci-dedupe:** no unconditional duplicate CI on a main push. Commit-gate red on main.
- **Seat-cycle (R179):** BOUND witnessed. The self-driven stop path is unproven; the R94 Stop-hook trigger is not built.
- **Git-as-memory:** research done (landing trailers); nothing built; needs the ADR-85 amendment.
- **Drive transport:** registry, write gate and lint exist. Sessions writing through a Drive connector bypass every gate (lint docstring: "bypasses every hook"). This is how this window's seat coined two prefixes, misfiled SUPPLEMENT ANSWERS and hand-wrote the LEDGER.

### 8.3 HANDOFF_BOOT corrections (K13)

protocols/HANDOFF_BOOT.md on main (last_reviewed 2026-10-15, boot_version 2, last commit bb644d35f 2026-10-16) is identical in its claims to the Project copy and is stale:

- "**Conductor E** ... code decides what runs next: conductor.py lane --round runs the phase chain". In fact the phase chain is BUILT with no caller; a seat decides and runs (8.1).
- "**Models** (R104) — Opus plans and judges, Copilot produces code, Sonnet writes the RED tests; the routing table ... is pending [#1536]". In fact R104 is superseded by R134 (roles as tasks, models as data); the routing table is on main; R153/R177/R178 govern; the model rule is K3.
- Not mentioned at all:
  - `land_lane.py` (ADR-131);
  - `seat_cycle.py` (R179);
  - the gen_handoff 12-row preflight as THE pre-handoff checklist;
  - `gen_ledger.py` as the LEDGER writer;
  - K12;
  - the known-reds expiry;
  - R148-R179.
- "the browser has no file access": in this Project the seat reads and writes the Drive transport through a connector. That is exactly the ungated write path of 8.2. K12 bounds it.
- `boot_citations` PASS (66/66) proves only that citations resolve, not that claims are true.

### 8.4 Token and integrator diagnosis (operator priority)

- **Start-up doubling:** each session start on a dirty tree costs +45,078 tokens. The Stop hook `scripts/session_end_backpressure.py:470 check_dirty_tree` continues the turn, which is a second model call: 44,707 clean vs 89,785 dirty, identical on CLI 2.1.302-2.1.304 (SESSION-e2-startup-bisect). The proposed fix row is not filed. This is the cheapest large saving.
- **Integrator on Opus:** session 7cce2581 used 500 calls, 108,899,707 cache-read tokens and 227,931 output tokens for 8 receipt rows. Wiring land_lane.py (0 model calls on a clean path) fixes time and tokens together. R178 bars Opus for the orchestrator; the integrator was still claude-opus-5-5 at cycle 10.
- **No instrument for the weekly allowance (R154)** and no per-session spend visibility. The night-map seat could not confirm its USD stop.
- **Boot bytes:** CLAUDE.md 20,647 B plus AGENTS.md load every session.
- **Spend that is metered:** Copilot 8,784 / 20,000 credits; Codespaces 79.49 / 180 core-hours.

### 8.5 Claude Code runtime facts (agent view / supervisor)

Sources: code.claude.com/docs/en/agent-view.md, cli-usage.md, claude-directory.md, read 2026-10-22.

- **Read state, not status text.** `claude agents --json` gives working / blocked / done / failed / stopped; done means "ready for your next prompt, whether or not its process is still alive". An external report (#77804, unverified) says a session parked on AskUserQuestion shows working, not blocked — another reason for K4.
- **Idle sessions stop on their own:** the supervisor stops a finished, unattached session after about an hour; pin it with Ctrl+T to keep it.
- **Retention:** rows stay until `claude rm` (never without the operator's GO). Transcripts are removed after cleanupPeriodDays (default 30). `jobs/` and `daemon/` are preserved state.
- **Auto-update:** idle sessions move to the new version; working ones are not interrupted.
- **Recovery when the background service is stuck** (the 2.1.308 double-start of this window): `claude daemon stop --any --keep-workers`, then `claude agents`, then `claude respawn <id>`.
- **End state of this window:** 87 sessions (78 done, 8 stopped, 1 working = the inventory itself); none waiting on input; no seat bound; no claim markers; no harness cron.

### 8.6 The window's biggest errors (seat-caused; learn, do not repeat)

**Common cause:** the seat acted on prose, memory or a compaction summary where code already defined the answer, then patched the result with more prose — a repair spiral.

Instances:
- recommended the org move before research;
- used gpt-5.6 out of habit;
- launched e2-ci-dedupe without checking R168 (5 h hold);
- wrong #83705 hypothesis;
- the spike flip-flop;
- presented known problems as discoveries;
- added `--disallowedTools AskUserQuestion` without checking the variadic parse;
- recommended `--batch ""` without reading merge_path;
- left "declared exceptions";
- coined two transport prefixes;
- put SUPPLEMENT ANSWERS in the wrong folder;
- hand-wrote the LEDGER against `writers: [gen_ledger]`;
- composed its own pre-handoff lists while `gen_handoff.py --preflight-only` existed;
- gave three contradictory verdicts in three replies.

**Rules for the next seat:**
- read the code contract first;
- the pre-handoff list IS the preflight;
- write only SUPPLEMENT ANSWERS and RATIFICATION (K12);
- one verdict after a full witness, not a verdict per partial read.

=== END OF SUPPLEMENT ANSWERS ===
