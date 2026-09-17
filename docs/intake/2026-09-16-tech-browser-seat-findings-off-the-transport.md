---
intake-id: 103
status: SEED
origin: browser-seat digests of 2026-09-15 and 2026-09-16, the window-close file of 2026-09-17, and the operator's browser chat of 2026-09-17 — all held only on the Drive transport (`to-browser/`) or in chat — ingested into the repo by a CC seat on 2026-09-17 so a handoff does not lose them
consumed-by:
note: an INGEST, not a decision. Every figure below is the source digest's measurement, attributed to its file; dedup against rows was re-done on 2026-09-17 against main 33246c0a, every local and origin branch, and origin's `refs/reservations/task-id/*`. No row was filed or closed by this doc.
---

<!--
  ADR-98 genre note. This doc is a SEED batch (precedent: 2026-07-30-tech-browser-architect-orientation.md,
  2026-07-07-arc5-pilot-followup-seeds.md): it carries findings off a transport that the repo cannot
  read, so the engine can triage them. It proposes nothing. Where a source digest wrote a
  "proposed Done when" or a recommended letter, it is quoted as the SOURCE's proposal, never
  adopted here. Intakes are cited BY PATH, never by bare number (the intake-id namespace has
  collided before).

  Row-citation convention used throughout:
    [#N]            an active row on main 33246c0a
    row N (branch)  a row that exists only on the named UNMERGED branch, not on main
    NO ROW          nothing found on main, on any branch, or as a reservation ref
-->

# The browser seat's findings of 2026-09-15/16 — off the transport and into the repo

## Problem / motivation

Between 2026-09-15 and 2026-09-16 the browser seat and the CC seats it commissioned measured the
harness end to end: where lane time goes, which rules refuse anything, which OS the harness is
bound to, which open rows are already satisfied, and what the next sessions should do first.
Every one of those findings lives in `$CLAUDE_PROMPTS_DIR/to-browser/`, a Google Drive folder the
repo cannot read, cannot diff and cannot gate. A handoff bundle cut today would carry none of it,
so the next architect would re-measure (the closure pass alone cost ~2.5 M tokens and four hours)
or, worse, act without it. This is the recoverability attribute the digests themselves say this
seat never raised: a decision file that lives only on the transport is not recoverable.

## Scenarios (+1 view)

- As a fresh architect booting from a handoff bundle, I open this one file and know the harness
  state per area, what is broken and measured, which rows already own each defect, what is
  unfiled, and in which order to act, without opening Drive.
- As the operator, I find the six contradicting rule pairs in one place with the source's
  recommended letter, and give one line back.
- As an integrator running a closure pass, I see which closures are already committed on an
  unmerged branch rather than re-deriving them.

## Functional requirements

- **Must:** every finding in the source digests listed under "Sources" is present here with its
  measurement or marked as not carried, with the reason.
- **Must:** every finding is marked with the row that owns it, or `NO ROW`.
- **Should:** the engine (ADR-111) triages each `NO ROW` item into exactly one funnel state.
- **Could:** the source digests are retired from the transport once this doc is merged.

## Acceptance criteria (ex-ante)

- A reader with no access to `to-browser/` or the browser chat can answer, from this file alone: the
  hook root cause and why a timeout cannot fix it; the guard and gate counters; the next window's
  acceptance test; the sixteen defects
  and each one's measurement; the five owed intakes; the ranked execution order with each item's
  measured cost of inaction; the six contradicting rule pairs with their locators; the browser
  seat's recorded failures.
- Each `NO ROW` item in section G has a funnel disposition (OWNED / DISCHARGED / CANDIDATE /
  REJECTED) recorded in a commit that cites this file's path.

## Non-goals

- Filing, closing, retiring or renumbering any row.
- Choosing between the options the digests present (portability, transport, CI arming, the rule
  pairs). Those are recorded as open questions.
- Re-measuring. Figures are the digests', dated to when they were taken.
- The contract-delivery question for Codespace lanes, which is a separate digest still in progress.

## Impact sketch (4+1 lite)

- **Logical:** no change; this records the state of the harness model, it does not alter it.
- **Process:** gives the triage funnel (ADR-111) an input it could not reach.
- **Development:** one new file under `docs/intake/` plus its two generated indices.
- **Physical:** none.

---

## Sources (all on the Drive transport, `to-browser/`, read 2026-09-17)

- `MAP-2026-09-16-harness-state-and-defects.md` — areas, 16 defects, rulings, operator owes
- `DIGEST-2026-09-16-pending-queue-v2.md` — blocker, measurements, five intakes, rows owed
- `PLAN-2026-09-16-execution-order.md` — waves ranked by cost of inaction, seat's own failures
- `DIGEST-2026-09-16-rules-enforcement-ladder.md` — 699 rule statements, 71 E-families, exit-code audit
- `QUESTION-contradicting-rules-2026-09-16.md` — the six pairs, one letter each, plus R1-R3
- `DIGEST-2026-09-16-closure-candidates.md` — 361 open rows verdicted, 25 closable, 5 retire
- `DIGEST-2026-09-16-os-coupling.md` — Windows coupling by line and organ, portable-port sizing
- `DIGEST-2026-09-15-why-lanes-are-slow.md` — wall-time split, top five sinks
- `DIGEST-2026-09-15-aj-and-benchmarks.md` — AJ M04 matrix, benchmark gaps
- `CLOSE-2026-09-17-window-close-and-successor-start.md` — the window close: diagnosis, what landed, closing sequence, the next window's test
- `DIGEST-2026-09-16-prose-as-source.md` — how far prose is the source of truth for execution (Q1 and Q5 of that digest never returned)
- The operator's browser chat of 2026-09-17, for the hook root cause and the guard counters in section 0 (no file carries them except, in summary, the CLOSE)
- No `DIGEST-2026-09-17-*` existed at read time.

## 0. TODAY — the window close of 2026-09-17 (read this section first)

These are the window's most valuable findings. Sources: the CLOSE file, the prose-as-source
digest, and the operator's browser chat.

### 0.1 The hook root cause — a spawn-level failure, not a hook defect

- **Hook processes were created SUSPENDED and never resumed.** Measured on the wedged sessions:
  **0 s CPU, no image path, one thread in Wait/Suspended.**
- **Our hook scripts never executed a line.** The failure is at process creation, below any code we
  own. **Rewriting the hooks would fix nothing.**
- **No timeout can fire on a process that never started.** A bound implemented inside or around the
  hook (the wrapper approach) cannot catch it; the CLOSE says the guard-timeout module may merge as a
  module only, NOT its settings wiring, because the wrapper cannot catch a suspended start and adds
  an interpreter per hook.
- **19-20 orphaned suspended processes accumulated from 2026-09-15 before anything wedged.** Killing
  them let **six of seven** wedged sessions recover.
- Consequence for the next session: the fix target is the spawn and the orphan population, not the
  hook bodies. Owners: row 863 (branch `worktree-file-hook-suspension-rows`, "hook processes are
  created suspended and never resumed"); [#808] was framed as a hang bound and does not by its title
  cover a process that never starts; emergency stop `33246c0a` disabled all PreToolUse hooks.

### 0.2 The guards enforced nothing — full cost, zero enforcement

Measured by lane ab-808:

- **The prompts guard timed out and PERMITTED 477 of 573 calls (83 %).**
- **`deny_and_point` timed out on all 182 of its calls and judged none.**
- Every one of those calls still paid the spawn (470-600 ms per matched call, section A ladder
  figures), so the cost was full and the enforcement zero, and nothing reported it because no
  counter existed.

### 0.3 The commit gate was never priced

- **34 hooks, ~244 s mean, worst leg 91-145 s (`decision-coverage`), `fail_fast` off, a single
  commit reaching 9+ minutes.**
- **No measurement of catches per cost has ever existed** for any hook.
- Since the CLOSE, main moved: `CLAUDE.md` §9 now reads "Since 2026-09-17 only the two
  index-freshness hooks run locally; the rest are `stages: [manual]`, run by conductor job
  `commit-gate`" — merge `6e9f0bb8` (`chore/commit-gate-priced`: "strip the local commit gate to
  data-loss protection, move 31 hooks to the conductor"), matching the CLOSE's closing-sequence
  step 2. A per-hook catch-per-cost measurement is not established by this ingest.

### 0.4 Prose as source of truth — how far the line is crossed

Source: `DIGEST-2026-09-16-prose-as-source.md`, read-only on main at the f8ca1d40 era.

- **115 citations of PLAYBOOK / STANDING_RULINGS as authority; 57 are the ONLY place the rule
  lives**, 33 point at an existing mechanism, 25 are reference.
- **47 PLAYBOOK rule families: 17 with no enforcement point, 21 partial, 9 gated.** The 17: F3
  serial integrator / GO per merge · F4 merge-is-atomic / push-before-delete · F5 launch test · F10
  frozen contract / decision budget · F11 refuse-to-finish / 2-touch / process-lane cap · F14
  JOURNAL authorship · F20 dispatch visibility · F24 night batch · F26 hub→consumer writes · F30
  commit-message standard · F33 output formatting · F36 architect discipline · F37 epic lanes · F38
  Council / ADR authorship · F43 lessons · F44 library-first · F46 scrum-master propagation.
  Gated: F2 F12 F13 F18 F28 F29 F32 F34 F40.
- **142 STANDING_RULINGS entries: ~10 enforcement-confirmed** by opening the mechanism; 103 name no
  script or hook (name-scan, weak evidence). The register has no field recording enforcement and no
  organ checks it (`decision_coverage.py` docstring: it does not see STANDING_RULINGS; [#721] open).
- **Two live contradictions:**
  1. **Who writes a lane's JOURNAL entry** — `.claude/commands/lane-boot.md:197` "Write the lane's
     JOURNAL entry on this branch, ahead of any merge" versus `scripts/gen_lane_contract.py:885`,
     emitted into EVERY generated contract: "No JOURNAL entry -- that is the integrator's surface".
     Measured cost: four lanes in one day each resolved it by judgment against the Stop hook. This
     is the same conflict as rule pair P1 (section E), now with an execution surface on each side.
     NO ROW.
  2. **`scripts/validate_branch_naming.py` is called "the checkable surface"** by CLAUDE.md,
     AGENTS.md and PLAYBOOK Ch3, while its own docstring says "READ-ONLY, AND WIRED INTO NO GATE".
     Same class as ADR-110's manifest check before [#804]: a mechanism nothing invokes. NO ROW.
- 18 classes of hand-written surface are parsed for meaning by a script (lower bound; the
  per-script census Q1 never returned). Ranked by an actual measured failure that converting prose
  to data would remove: (1) PLAYBOOK Ch8 dispatch fences read by `dispatch_drift.py:24,105` · (2)
  batch-manifest id blocks no parser read → id 827 filed outside every block ([#826]) · (3) JOURNAL
  authorship, above · (4) the contract `Substrate:` line is documentation, the verb is human choice
  → remote isolation silently fell back to local ([#803]) · (5) cloud token scope recorded only in an
  audit, not in `ecosystem/substrate-registry.yaml` · (6) CLAUDE.md §9 hook roster drift (4 live hooks
  omitted, a disabled guard described as live, at the digest's time) · (7) `ecosystem/north-star.md`
  claims GENERATED with its generator retired at `c9ea3b07`.
- Nothing in the repo DECIDES where a lane runs: a human chooses the verb; data plus
  `validate_substrate.py` only refuses some wrong choices. "Needs a consumer repo" is not encoded.
- Data registries hand-copied with no agreement check: `substrate-registry.yaml` vs PLAYBOOK Ch8
  Q1-Q4 vs `gen_lane_contract.SHAPE_ENUM` (the test pins the literal tuple).
- Library-first survey (capability → nearest tool): typed rule data → jsonschema / Pydantic;
  commit validation → check-jsonschema; rendering into marked regions → Cog (`cog --check` for
  drift); allow/deny policy with reasons → OPA/Rego, Cedar, zen-engine; agent tool-call gate →
  hand-rolled PreToolUse only; interim markdown-table parsing → markdown-it-py.

### 0.5 The one lesson

**A mechanism ships with a COUNTER — what it caught, what it cost, over what window. A gate with no
catch in its window is removed, not tuned.** Every ruling this window carried a refusal criterion
("it must refuse X") and none carried a cost criterion ("and this is how we learn it is not worth
it"). That asymmetry is why the harness became its own bottleneck. The CLOSE's count: ~15
mechanisms ruled in the window, 0 with a measured catch-rate or cost budget. NO ROW encodes the
counter requirement.

### 0.6 The next window's acceptance test — single and falsifiable

**One lane runs end to end, dispatch to merged, in under one hour, with nothing wedged and no human
decision in the middle. Until it passes, no new organ is built.**

The CLOSE's reading: the four cheap wirings already landed should make it reachable; what stands in
the way is the gate cost (0.3) and the suspended-spawn defect (0.1), both now measured. The window's
priority inverts: not "build more mechanisms" but "remove cost and prove throughput". NO ROW
carries this test.

### 0.7 The CLOSE's closing sequence for this window, and what landed

Closing sequence (source's order): 1. stop dispatching — every new session wedged at startup until
the hook disable was on main (now `33246c0a`) · 2. strip the commit gate to hooks with an evidenced
catch, move the rest to the Actions conductor, record commit time before and after (now reflected
in `CLAUDE.md` §9) · 3. merge what is finished: the hooks disable, conductor-reads-the-freeze,
substrate repair, cost telemetry, protocols heading gate, and the guard-timeout MODULE only · 4. land
the week's knowledge as ONE intake — this doc · 5. close batch AB, then the handoff bundle through
`.dev-knowledge` on the operator's explicit word.

Landed in the window (so the successor does not redo it): the id allocator (reserved by push) ·
`/lane-boot` refuses a batch with no committed manifest · the prompts guard fails closed ·
264,687 B and 15 files deleted with paired before/after suites · BACKLOG 99,961 → 75,143 B by
relocating narration to a dated audit · Actions proven for the suite (two identical runs on one
commit) · the Codespace container proven ours · rows 727, 684, 716-718, 692 closed with proving SHAs.

Also from the CLOSE: 43 of 51 Linux failures are fleet-shape assumptions, not OS; the operator owes a
word on whether the dispatch layer moves to Python (~9 lanes, os-coupling evidence).

## What moved since the digests were written (read at main 33246c0a, 2026-09-17)

- **All PreToolUse hooks and the billing-leak SessionStart sentinel are disabled**, by emergency
  merge `33246c0a` (`worktree-hooks-disable-emergency`). Every S2-tier enforcement proposal in the
  ladder digest now targets a tier that is switched off. Follow-ups are on branch
  `worktree-file-hook-suspension-rows`: row 863 (hook processes created suspended and never
  resumed), row 864 (decision-coverage gate is flaky), row 865 (user-level block-onedrive guard
  needs a hang ruling).
- **The conductor now judges pytest against the frozen baseline by node id**: merge `645ec4db`
  ([#802], row still open).
- **Task ids are reserved by push**: merge `af69c92e` (lane ab-804). Origin carries
  `refs/reservations/task-id/*`; ids 831 and 843 are reserved with no row file found on any ref.
- **The 25 closures are committed but NOT merged**: commit `0c120be2` on
  `worktree-lane-ab-828-closure-census` closes [#470] [#587] [#591] [#592] [#596] [#597] [#600]
  [#601] [#605] [#608] [#613] [#626] [#643] [#653] [#740] [#742] [#743] [#744] [#750] [#751] [#752]
  [#765] [#780] [#784] [#785], and files rows 828, 829, 830 carrying the digest's caveats.
- Live lane branches overlapping the execution order: `worktree-lane-ab-808-guard-timeout`,
  `-ab-810-substrate-repair`, `-ab-664-spine-witnessed`, `-ab-694-cost-telemetry`,
  `-ab-832-copilot-collections-comparison`, `-ab-833-seat-registry`, `-ab-834-protocols-heading-gate`.

## A. Harness state by area, with evidence

Source: MAP §Areas, with the 2026-09-17 column added by this ingest.

- **Task ids** — FIXED 2026-09-16: reserved by push before a lane writes; the loser of a race exits 3
  naming the holder; the local maximum is never read. Evidence: lane 804, 8 commits, merge
  `af69c92e`. Cost of not having it: 4 renumbers in one day. Rows: [#804] [#788] still open.
- **Batch manifest** — FIXED 2026-09-16 in `/lane-boot`: a batch whose manifest is not committed and
  open on main is refused, and a manifest on a side branch is refused by name. The dispatch VERB
  still boots without one: [#823].
- **Codespace** — proven live as a container: 11 positive markers, 0 recovery phrases, 11.97
  metered minutes. The heartbeat workflow failed on a uv mismatch (runner 0.12.15 vs pin
  `==0.11.19`), so the repo could not read that proof. Rows: [#810] (both defects), repair lane
  `worktree-lane-ab-810-substrate-repair`.
- **Guard hang** — wedged three sessions, ~14 h in the week. Rows: [#808]; lane
  `worktree-lane-ab-808-guard-timeout`; 2026-09-17 emergency disable `33246c0a`.
- **Events** — 33 hook events exist in claude-code 2.1.273; this repo wires 3 (PreToolUse, Stop,
  SessionStart) plus Notification at user level. **Exit 1 never blocks** on any event (binary's
  result classifier). Under `bypassPermissions` only deny rules and PreToolUse exit 2 refuse.
  Source: ladder §0-§1. Row: NO ROW (see G, R1 and owed intake 4).
- **Merge** — fast: median 17.6 min (n=4, range 12.4-67.9), `git merge` itself 0.7-1.1 min,
  **operator wait inside merges zero**; the seat then sat idle 10.6 h before the rulings.
  Source: batch AA receipts, pending-queue v2.
- **Seat** — does not exist as an entity; wedged / absent / starved are invisible. ~17 agent-hours
  lost. Row: row 833 (branch `worktree-lane-ab-833-seat-registry`).
- **Backlog** — 99,961 B of 100,000 B at 3d435d36 (39 B headroom); 75,143 B after a one-time 26 KB
  relocation at f746ddf9. Rows fill it, not narration: 25 closures free only ~4.7 KB. Filing to
  closing 8.8:1 in the window, 2.7:1 with the 25. Rows: [#589] [#754] [#807].
- **Decisions** — the engine works and refuses; `decision-coverage` costs 91-145 s per commit, the
  gate's worst leg. Row: row 864 (branch) for flakiness; cost NO ROW (see defect 13).
- **Tests** — impacted selection works; 62 failures frozen in the baseline (conductor run
  `35132508646`: 62 failed, 6265 passed). **Evals designed, never run**: [#661].
- **CI** — required-check ruleset `enforcement: disabled`
  (`deploy/conductor-required-checks.ruleset.json:4`); three red pushes to main landed.
  Merge-tier enforcement does not exist. Rows: [#689] adjacent, [#802] landed the freeze read;
  the ARM-or-report-only ruling is NO ROW (G, R2).
- **Actions** — proven for the suite, never for a lane; no runner credential. NO ROW (operator
  decision, section F).
- **Models** — USD 8,721.88 priced, **99.47 % Opus**, 0.53 % Sonnet, ~488 M tokens unpriced. First
  non-Opus lane 2026-09-16 (810 on Sonnet). Per-seat memory measured 646 MB. Rows: [#824]
  [#810] [#752] (closure on branch ab-828 with caveat row 828).
- **Telemetry** — instruments exist, nothing calls them (`cost_usage_telemetry.py` library-only).
  Row: [#694] adjacent, lane `worktree-lane-ab-694-cost-telemetry`.
- **Self-healing** — does not exist; waits on telemetry. NO ROW.
- **Docs** — ARCHITECTURE −22 %, ESSENTIALS gone; comprehending the repo is a process with no
  organ. Rows: [#755] [#760] [#781]; the comprehension question is owed intake 2.
- **Universalisation** — first consumer evidence is bad: the floor left `INSTALL.md` in
  win-tooling, a file that consumer's own gate forbids, red for two weeks. NO ROW found by this
  ingest; the source digest `DIGEST-2026-09-15-floor-consumer-defect.md` was not in the requested
  set and was not read.
- **Library-first** — regression: the deny-and-point hook (closed row 727) is disabled after wedging three
  sessions; organ-versus-raw-scan usage unmeasured. See why-lanes-slow below.
- **Benchmarks** — AJ M04 done, 7 rows [#766]-[#772]; the three-repo comparison ran on the wrong
  three repos. Per-task state carrier: NO ROW. Re-run: row 832 (branch).
- **Handoff** — impossible on 2026-09-16 (context exhausted, batch open). This doc exists so it is
  possible.

### Where lane time goes (why-lanes-slow, 2026-09-15)

Measured from transcripts (tool_use/tool_result timestamp pairs) on lanes aa-1, aa-2, z-4:

- Model time is the **smallest** category: 13-25 % of wall. 62-86 % is the box (shell, tests, gates).
- Top five sinks, ranked by measured cost:
  1. Wedged background agents aa-3 and aa-6: **~10.7 agent-hours, zero commits** — their host was
     inside one 34-hook `git commit` for ~1 h 48 m. Row: row 833 (branch) for the seat absence.
  2. Raw scans instead of organs: **132.1 min** across three lanes (z-4 alone 82.8 min, 7.6× its
     organ time). The deny-and-point escape is defeated by a pipe (`# raw-needed:` attaches only to
     the last pipeline segment). Row: NO ROW for the pipe escape.
  3. The 34-hook commit gate: **98.5 min** across three lanes; z-4 mean 244 s over 20 commits.
     decision-coverage 91-145 s, audit-health 51-61 s (733 MB), graph-rebuild 39-46 s, 1.5 s
     `uv run` spawn ×34, three OS processes per hook. One commit cost 447 s with
     `SKIP=audit-health` set. Row: NO ROW for cost (defect 13).
  4. Idle/blocked: **110.6 min**, including one contiguous 86.6 min stall in z-4.
  5. Tests: **80.6 min**, of which **20.4 min avoidable** (aa-2 ran the full suite twice against
     the once-at-integration rule). Row: NO ROW for "full suite once at integration" (ladder E01).
- Memory at the time: 1.44-1.53 GB free of 27.7 GB, 62 `claude.exe` at ~12.5 GB. A 7 KB contract
  read off `H:` took **96.4 s** (aa-1) and **83.9 s** (aa-2). Row: NO ROW.

### OS coupling (os-coupling, 2026-09-16)

- Cannot run outside Windows: **9,082 of 101,909 production lines (8.9 %)**; 7 of 74 organs (9.5 %),
  plus 4 mixed and 6 soft. Largest contributor: win-tooling `DispatchHelpers.psm1`, 3,964 lines,
  43.6 % of all Windows-bound lines.
- On ubuntu-latest the suite ran 51 failed / 5,999 passed; at most **8** failures are OS-specific.
- None of the three benchmark repos is a Python harness (premise corrected); none hand-rolls
  process management.
- No job objects and no tree kill exist today; a batch-X lane survived teardown 53.2 h.
- Three hooks invoke bare `python` (`block_immutable_edits.py`, the prompts guard, the plugin's
  `propose_closures.py`); on a host without `python-is-python3` the prompts guard refuses every
  matched call.
- Port estimate: about 9 lanes (8 if hygiene folds in); two gate on operator acts (new deps, the
  transport choice), two are capabilities that do not exist today.
- Lane contracts embed the PowerShell token `$env:CLAUDE_PROMPTS_DIR` (`gen_lane_contract.py`
  emits it), so a port changes a contract grammar, not only code.
- Rows: portability as an attribute NO ROW (owed intake 5); bare-`python` hooks NO ROW.

### Benchmarks and AJ (aj-and-benchmarks, 2026-09-15)

- AJ M04 (MCP): 82 items = 13 SHIPPED + 57 OWNED + 12 UNOWNED → rows [#766]-[#772]; locators 82/82
  resolved. M03 pillar score 1 of 3.
- M03 headline: four of five prior conclusions it was told to attack have **no source document in
  this repository** — the recoverability defect again.
- Not adopted, ranked by what it changes: per-task state carrier + GO/NO-GO artifact (NO ROW) ·
  secret scoping at dispatch [#772] · one refusal channel → three verdicts [#768] · evals never
  run [#661] · rubber-stamp detection (NO ROW) · model-agnosticism: logical aliases,
  provider-independent boundary (NO ROW; adjacent [#824]) · boot-payload budget [#766] · command
  declares the module it runs (`docs/intake/2026-09-15-tech-command-declares-the-module-it-runs.md`)
  · cost telemetry with call sites ([#694] adjacent) · corpus-wide locator resolution
  (`docs/intake/2026-09-15-tech-corpus-wide-locator-resolution.md`).
- Refused with reason, not to be re-opened (z-11 dispositions List B): installable consumer CLI,
  i18n, tasks→issue tracker, ten-rule skill validator, agent-persona roles, blanket TDD, a second
  docs site.

## B. The sixteen defects found in passing, each with its measurement

Source: MAP §Defects. "None of which existed as a row when found" was true on 2026-09-16; the
owner column is 2026-09-17.

1. **No launch verb for a non-Claude lane.** `dispatch` accepts only `claude` and the contract
   generator knows only Claude models, so every lane takes the Claude path. Measurement: 99.47 %
   of USD 8,721.88 priced spend on Opus. → **[#824]**
2. **`single_flight.py` misreports a real race** — a true simultaneous push loses with "reference
   already exists", which it does not recognise, so it exits 2 (internal error) instead of 3 (in
   flight). Nothing is granted twice; the operator is told the wrong thing. → **[#825]**
3. **A row was filed on main outside every manifest block** (id 827) — the prose id blocks stopped
   nothing. → **[#826]** (allocator context: [#788], [#804])
4. **`propose_row_closures` never reads a Done-when** — it compares branches, so its first run on
   main found zero by construction. Answering "which open rows did these merges satisfy" cost a
   model reading 361 rows: ~2.5 M fresh input tokens + ~10 M cache-read, ~four hours, and both
   readers still missed real closures (agy missed 629 and 742; Sonnet missed 587). → **[#730]**
   plus row 830 (branch `worktree-lane-ab-828-closure-census`, the `witness:` field)
5. **No age-or-abandonment census has ever run.** Closure candidates reach back only to id 470.
   → **[#506]** (its Done-when is a sheet with one row per open task and its last-touch date)
6. **The per-seat memory constant was wrong by ~7×** — 413 MB counted only processes named `claude`,
   missing each lane's uv, git and python children; measured 646 MB, with 2.8 GB observed at full
   lane start. → **[#827]**. **Discrepancy to resolve:** the MAP says admission *passed* work it
   could not run; [#827]'s title says it *refused* work it could run.
7. **`agy` in reader role wrote five scratch files into the repo root** and spawned sub-agents
   against its prompt before a quota error (closure digest: run 02 wrote the files, run 01 spawned
   sub-agents, run 03 returned SUCCESS with an empty response, run 04 errored on quota). A
   non-Claude reader needs no write access, not an instruction not to write. → **NO ROW**
   (adjacent: [#722] reader routing, [#753])
8. **Six mutually contradicting rules** — nothing on either side can be enforced until ruled.
   → section E. Owners: pair 5 [#823]; pair 6 [#806]; pair 4 adjacent [#685] [#414];
   **pairs 1, 2, 3 NO ROW**
9. **The ratchet cannot accept a ratified exception** — an operator ruling to raise a baseline is
   refused by the gate (silent-rule ratchet at 447/447), forcing a bypass or a reword; the
   integrator chose the reword. → **[#806]**
10. **A verb's reported success is not evidence of its effect** — four witnessed surfaces:
    `claude stop` returned success with the tree alive; Codespaces reported healthy while serving a
    recovery container; a cloud request reported "launched successfully" after falling back to
    local; our hooks exiting 1 report a pass while blocking nothing. → row 822 (branch
    `worktree-lane-ab-810-substrate-repair`, the rule) + **[#803]** (the cloud-fallback surface).
    The `claude stop` and hook-exit-1 surfaces have no row of their own.
11. **Seat lifecycle has no trigger** — a dispatcher exists because the browser pastes, an
    integrator because the browser remembers. Twice every lane finished and nothing merged.
    → row 833 (branch, seat registry) + row 820 (branch ab-810, a handback addressed to a seat that
    does not exist) + **[#805]** (integrator finishes unattended). A "dispatch without a
    receiving seat refuses" leg: not found in any of them by this ingest.
12. **A guard that hangs is worse than one that is absent**, because absence is visible; no hook
    carries a bounded execution time. Measured: ~14 h of wedges in a week. → **[#808]**; rows 863,
    865 (branch `worktree-file-hook-suspension-rows`). **Superseded in diagnosis by section 0.1:**
    the hooks did not hang, their processes were created suspended and never ran, so a bound on
    execution time cannot fire.
13. **The commit gate costs ~244 s across 34 hooks**, and `fail_fast` is off, so a refused commit
    runs every hook first. → **NO ROW** owning the cost. Adjacent: [#769] (no cancel for a
    long-running gate), row 864 (branch, decision-coverage flaky), and the READY intakes
    `docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md` and
    `docs/intake/2026-09-05-tech-batch-p-audit-gate-speed.md`
14. **The Codespace runner cannot pass a model at all**, so routing is impossible on the only
    off-box substrate. → **[#810]** (note: the deployed `DispatchHelpers.psm1` read 2026-09-17
    already emits `--model $Model` in the runner; the row's tracked-source leg is not verified here)
15. **A test double modelled a platform behaviour nobody verified** — five fakes returned a value the
    real tool never returns; 308 lines were built on it. → **[#787]**
16. **`safe_remove` returned SAFE on a module loaded by name** — the ADR-89 false-PASS class,
    observed live and reverted by the lane. → **NO ROW** (adjacent: row 489, safe_remove posture, status retired)

## C. The five intakes still owed

Source: pending-queue v2 §five intakes; PLAN §intakes. Each is to go THROUGH the decision engine
to an ADR. None exists as an intake doc on any ref at 2026-09-17.

1. **Per-task execution state.** Phase 1 must establish what [#664], `tasks/` frontmatter,
   `manifest.json`, FPG-1 and the organ index already hold, then compare against the benchmark
   carrier (maister-shaped `orchestrator-state.yml`: `completed_phases`, `failed_phases`,
   `auto_fix_attempts`, `task_context.risk_level`). Options the source names: extend what exists ·
   new frontmatter fields · a separate carrier (the source says refused structurally) · nothing.
   Adjacent intake: `docs/intake/2026-09-07-tech-per-lane-resumable-state-file.md` (per LANE,
   not per task). **No row.**
2. **How a seat comprehends this repo.** A generated map (process → trigger → organ → artifact →
   code location) versus hand-written prose versus query-on-demand. Adjacent rows: [#781]
   (management map), [#728], [#729]. **No intake.**
3. **A rule with no enforcement point is not a rule.** Classify every rule in PLAYBOOK, seat
   renders, CLAUDE.md and STANDING_RULINGS as enforceable in-session / at commit / at merge /
   advisory. Its read-only half is done: the enforcement-ladder digest (699 statements → 71
   enforceable families E01-E71 + 8 advisory classes A1-A8). Prior art the source names:
   `docs/audits/2026-07-19-census-silent-rule-ledger.md` (176 silent of 320), the silent-rule ratchet (closed row 436),
   `ecosystem/doc-code-edge.yaml`. Carried instance: ADR-110's manifest-before-dispatch (now [#804]
   landed at `/lane-boot`, [#823] open at the verb). **No intake doc** — the QUESTION digest
   records that intake 3's own text was never located.
4. **The event surface we never connected.** 33 events, ~3-4 wired; only exit 2 blocks. Map each
   measured failure to its existing event. The source's framing: four axes of one loop —
   domain-driven (where), spec-driven (what is authorised), test-driven (how we know),
   event-driven (when the next hop fires); today only the spec axis has teeth. The source's
   recommendation, recorded not adopted: orchestration for the sequence, choreography for the
   guards. **No intake, no row.**
5. **The attributes this seat never raised.** Security: every lane inherits the whole secret store
   ([#772]). Recoverability: decision files live only on the transport (this doc is one instance;
   no row). Portability: the harness assumes this Windows box while the floor deploys to consumers
   (os-coupling digest; no row). Testability: [#661] evals designed, never run. Usability: no
   finding recorded. **No intake.**

## D. Execution order, ranked by measured cost of inaction

Source: PLAN-2026-09-16. The PLAN's own change note: earlier versions ranked by size of the
problem, which is why the four cheapest fixes waited a week.

**Gating words first:** the six rule pairs (E) · the closure list · CI enforcement ON or documented
as report-only.

**Sequencing constraint (source's words, carried because inverting it bricks the repo):** turning
CI enforcement on while main carries 62 frozen failures blocks every merge. The conductor must
read the freeze first; only then does enforcement go on. The first half landed at `645ec4db`.

Wave 1 — cheap wiring, highest cost of inaction:

1. **Guard timeout + fail open** — cost: ~14 h of wedges in the week (integrator twice, ~6 h; a
   lane at 8 h), all at "running PreToolUse hooks". Owner: [#808], lane ab-808 live;
   2026-09-17 all PreToolUse hooks disabled (`33246c0a`) as the emergency stop.
2. **Task-id allocator + manifest wired to dispatch** — cost: 4 id reallocations in commit
   `279caaff` (787→800, 788→801, 790→802, 792→803), two renumbers in a day, ~2 h integrator
   untangling. Owner: allocator + `/lane-boot` refusal LANDED `af69c92e` ([#804] still open);
   verb leg [#823]; race exit code [#825]; machine-read id blocks [#826].
3. **Model routing enforced** — cost: USD 8,721 priced at 99.47 % Opus; USD 430+ per batch. Owner:
   [#752] (closure committed on branch ab-828 with caveat row 828), [#810], [#824].
4. **Conductor reads the freeze, THEN CI enforcement on** — cost: ruleset disabled, three red
   pushes landed. Owner: freeze read LANDED `645ec4db` ([#802] still open); arming: **NO ROW**
   (G, R2), adjacent [#689].

Wave 2 — the structural absences:

5. **Seat as a registered entity** — cost: ~17 agent-hours (6 h wedged integrator, 10.7 h starved
   subagents, a half-day with no integrator). Owner: row 833 (branch, lane live).
6. **Per-task execution state (the spine)** — cost: "how is the batch going" needs reading rows;
   all three benchmarks converge on it. Owner: **NO ROW** (owed intake 1).

Wave 3 — sustainability:

7. **Row closure + fix the closure detector** — cost: 10 rows filed and 0 closed in a day; row
   bytes nearly doubled since 2026-09-01 (32,383 → 61,436 B) while narration stayed flat. Owner:
   closures committed on branch ab-828 (`0c120be2`, unmerged); detector [#730] + row 830 (branch).
8. **Commit-gate cost** — cost: 34 hooks, ~244 s mean, `fail_fast` off. Owner: **NO ROW** (defect 13).

Then the ten build lanes that have waited, with their owners: BACKLOG one row format [#589] ·
one `protocols/` heading row 834 (branch, lane live) · ARCHITECTURE to target [#755] [#760] ·
prompt distiller [#617] (re-scoped, below) · path registry [#715] · cost telemetry wired [#694]
(lane live) · spine witnessed [#664] (lane live) · management map [#781] · copilot-collections
re-run row 832 (branch, lane live) · log review [#723] and charts [#705], both held on telemetry.

Constraints the PLAN places on every lane: no full suite on the workstation; locally only the
impacted set; a memory floor below which a local dispatch refuses; `-Model` explicit per lane and
reported ordered-vs-ran; no new commit-tier gate without a measured cost; Codespace as the default
off-box substrate; under `bypassPermissions` no enforcement may rest on allow or ask rules.

## E. The six contradicting rules awaiting an operator word

Source: QUESTION-contradicting-rules-2026-09-16.md (every locator re-opened by a CC seat at main
f746ddf9). The source's suggested one-line answer: `P1=C P2=A P3=B P4=C P5=A P6=B`. Nothing below
is ruled.

- **P1 · JOURNAL authorship.** A: `protocols/STANDING_RULINGS.md:1831` "A lane leaves `JOURNAL.md`
  alone…" · B: `protocols/PLAYBOOK.md:2107-2108` "written on that arc's own branch, ahead of the
  merge" + `STANDING_RULINGS.md:146`. Enforced today: neither preventively
  (`check_journal_day_letters` catches a duplicate after the fact). Cost measured: `279caaff`
  re-lettered colliding (n)/(o) to (t)/(u). Source recommends **C**: scope by branch (a batch lane
  follows A, any other branch follows B). **NO ROW.**
- **P2 · `--no-verify`.** A: `STANDING_RULINGS.md:2330-2331` banned without exception (and
  AGENTS.md "Gates") · B: `CLAUDE.md:191` names `git push --no-verify` as `block-unanchored-push`'s
  sole escape. Enforced today: neither (git cannot see a skipped hook). Keeping B disarms
  `block-ff-push` too. Source recommends **A**, with a `SKIP=block-unanchored-push` escape
  declared in the body — pre-commit `SKIP` on the pre-push stage is unmeasured. **NO ROW.**
- **P3 · CLAUDE.md size.** A: `PLAYBOOK.md:381`, `:555`, `:6145` "200 lines" · B: the CLAUDE.md
  header "bytes bind, ≤24,576 B … line count WARN-only". Measured at the time: 241 lines /
  24,291 B. Source recommends **B**. **NO ROW.**
- **P4 · Merge authorization.** A: `PLAYBOOK.md:855-856` per-act operator authorization · B:
  `.claude/settings.local.json:10` allows `Bash(git merge *)` (gitignored, machine-local). Source
  recommends **C**: project `permissions.ask` on the integration shape, drop the local allow.
  Adjacent rows: [#685], [#414].
- **P5 · ADR-110 manifest check locus.** A: `PLAYBOOK.md:2740-2742` says `/lane-boot` refuses · B:
  at the time `/lane-boot` never called `preflight_contract.check_open_batch`. Source recommends
  **A**, wired at the dispatch verb. Since then `/lane-boot` refuses (`af69c92e`); the verb leg is
  **[#823]**.
- **P6 · Register entries vs the silent-rule ratchet.** A: owed intake 3 asks every enforceable rule
  to gain a register entry · B: `ecosystem/derived-copies.yaml:55-59`, ratchet at 447/447. Source
  recommends **B**: register entries are keyword-free data that point at the rule. Owner of the
  underlying defect: **[#806]**.

## F. Operator decisions still open (not rule pairs)

From MAP §Still owed and pending-queue v2 §Operator decisions:

- The closure list — now committed on branch ab-828 for the 25; Table 2's **five RETIRE
  candidates** still need a word: [#303] (status deferred; seeder deleted), [#369] (`boundary_headers.py` deleted),
  [#383] (names the retired `desired_state_report.py`), [#604] (its validator deleted),
  [#617] (names the deleted dashboard). **Ruling already made for [#617] on 2026-09-16:
  RE-SCOPED, not retired** — its Done-when becomes "an intent resolves to the command, skill and
  hook for a named model without the browser composing it", with the `logs/prompts/` trace home as
  clause 1. Whether that ruling reached the row body is not verified by this ingest.
- CI enforcement ON, or CI documented as report-only.
- The Actions credential — on **security** grounds (a narrower blast radius than every local lane
  inheriting the whole `.env`), not on the CI claim, since there is no runner.
- BACKLOG headroom route: close rows, retire rows, or re-declare the [#589] ceiling.
- What a tagged manifest means: `docs/intake/2026-09-15-tech-floor-repin-reds-every-historical-manifest.md`.
- Deferred by the operator's own ruling until the waves are done: folder names, the v1.5.0 tag,
  the corp-monorepo deployment.

Closure-digest near-misses, each one act away (all still open): [#792] (`resource_lifecycle.py
admit` called by no hook or command) · [#690] (only the WARN-count clause unwitnessed) · [#629]
(`gen_lane_contract` has no reissue verb) · [#242] (met, but ordered not to close before [#362]) ·
[#746] (owes one `-b main` create datapoint).

## G. Findings with NO ROW anywhere (the triage list)

Checked 2026-09-17 against main `33246c0a`, all 20 local and origin branch refs, and origin's
`refs/reservations/task-id/*`. Each needs one ADR-111 funnel state.

- Defect 7 — a non-Claude reader runs with write access (agy wrote into the repo root).
- Defect 13 — commit-gate cost (~244 s, 34 hooks, `fail_fast` off) has no owning row; two READY
  intakes cover the theme.
- Defect 16 — `safe_remove` SAFE on a module loaded by name (ADR-89 false-PASS class).
- Defect 10's `claude stop` and hook-exit-1 surfaces (the rule itself is row 822 on a branch).
- Rule pairs P1, P2, P3.
- **R1** — under `bypassPermissions`, allow and ask rules are inert; only deny rules and PreToolUse
  exit 2 refuse (binary quote, claude-code 2.1.273; `PLAYBOOK.md:2956` says all three verbs run
  with bypass). Source's proposed Done-when: PLAYBOOK states the lane ladder with the binary quote
  as source, every lane-side refusal re-tiered to deny / verb / PreToolUse, and a RED-first
  fixture proving an ask rule does not refuse on a lane. Adjacent: [#752], [#769].
- **R2** — the CI required-check ruleset is `enforcement: disabled`; arm it or document report-only.
  Adjacent: [#689].
- **E01** — "the full suite runs once, at integration" is enforced nowhere
  (`merge_receipt.py:185` reads `suite` only under `--strict`, run by hand). Measured cost: 20.4 min
  of avoidable full-suite runs in one lane.
- The deny-and-point escape is defeated by a pipe (`# raw-needed:` binds to the last pipeline
  segment only); 132.1 min of raw scans in three lanes.
- A 7 KB read off the Drive transport took 83.9-96.4 s on a starved box.
- A "dispatch without a receiving seat refuses" leg (defect 11) — not found in row 833, 820 or [#805].
- Per-task execution state / GO-NO-GO artifact (owed intake 1; benchmark convergence).
- Rubber-stamp detection: nothing tests whether a gate or reviewer bites.
- Model-agnosticism: `MODEL_ENUM=("opus","sonnet","haiku")` hard-coded at three call sites in
  `gen_lane_contract.py`; the literal binary `claude` emitted.
- Portability of the harness (8.9 % of production lines Windows-bound; ~9 lanes to port).
- Three hooks invoke bare `python` rather than `uv run --locked python`.
- Ladder exit-code defects (ladder §2), none rowed: **A** `block_immutable_edits.py` has no
  existence test on its path, so an unset `CLAUDE_PROJECT_DIR` makes python exit 2 and PreToolUse
  blocks every Edit/Write · **B** an import-time crash there exits 1 and allows · **C** the Stop
  hook runs through `uv run --locked`, and uv exits 2 on an environment failure, turning an
  advisory hook into a turn-extender · **D** `block-onedrive.ps1` passes an unparseable payload
  (`catch { exit 0 }`) · **E** a terminating PowerShell error there exits 1 and passes. Cost:
  `block-onedrive.ps1` measured **5,226 ms median per call** on nearly every tool call. Row 865
  (branch) asks for a hang ruling on the same guard, not for these defects. The PreToolUse
  disable at `33246c0a` changes whether these are live.
- The universalisation defect (`INSTALL.md` left in win-tooling against its own gate) — no row
  found; its source digest was not in the requested set.
- Self-healing, and the Actions lane credential (operator decision, F).
- Section 0.2 — guards that time out PERMIT (prompts guard 477 of 573) or judge nothing
  (`deny_and_point` 0 of 182), with no counter reporting it.
- Section 0.3 / 0.5 — no mechanism carries a catch-per-cost counter; no rule removes a gate with no
  catch in its window.
- Section 0.4 — the JOURNAL-authorship contradiction between `lane-boot.md:197` and
  `gen_lane_contract.py:885`; `validate_branch_naming.py` named the checkable surface and wired into
  no gate; STANDING_RULINGS has no enforcement field and no organ reads it (adjacent [#721]).
- Section 0.6 — the next window's acceptance test (one lane, dispatch to merged, under one hour,
  nothing wedged, no human decision).
- Section 0.1 — the orphaned-suspended-process population (19-20 from 2026-09-15) has no census or
  reaper row of its own; row 863 (branch) names the suspension, not the accumulation.

## H. The browser seat's own recorded failures

Source: PLAN-2026-09-16 §"What this seat got wrong, so the successor inherits it". Verbatim in
substance:

1. Planned 13 lanes against a ceiling of 6.
2. Claimed a lane's work was committed when it had zero commits.
3. Reported an integrator as working while holding two identical transcript samples.
4. Omitted models from a dispatch, so a whole night would have run on Opus.
5. Wrote rules in pastes instead of registering them.
6. Ranked repairs by size of the problem instead of by cost of inaction, which is why the four
   cheapest fixes waited a week.

The CLOSE of 2026-09-17 restates them as six, sharper:

1. **Refusal without a counter** — ~15 mechanisms ruled, 0 with a measured catch-rate or cost budget.
2. **Instance, not class — three times** — disabled one hanging hook and declared the class closed;
   deferred the bounded-hook lane to third place on that belief; accepted a two-family disable when
   six families were armed. Each next wedge came from a family not touched.
3. **Ordered by size of problem, not cost of inaction — twice** — the four cheapest wirings waited a
   week behind a large structural lane.
4. **Asserted state from reports** — "the integrator is working" for hours on two identical
   transcript samples; the test (did the counter move) was available and unused.
5. **~40 decision files on the transport**, each arming `decision-coverage` against every concurrent
   session; four plan files once wedged every commit in the repo.
6. **Never proposed removing anything** until the system was unusable.

Recorded failures of the readers it commissioned, from the same window: agy wrote five files into
the repo root in a reader role and spawned sub-agents against its prompt (closure digest); agy
returned SUCCESS with an empty response (closure digest); the ladder digest's reader was an
unadmitted `read` provider (`verdict: unevaluated`) whose every locator had to be re-checked; the
z-11 comparison lane was frozen against the wrong three repositories because its contract never
named the operator's three; the os-coupling CC seat listed one directory under the OneDrive
exclusion path, reported by that seat as a slip and not repeated.

## Open questions

- Which funnel state does each section-G item take?
- Does the [#827] framing (refused work it could run) or the MAP's (passed work it could not run)
  describe the measured behaviour?
- With all PreToolUse hooks disabled at `33246c0a`, which of the ladder's S2-tier proposals remain
  meaningful, and does R1's re-tiering question change?
- Are reserved ids 831 and 843 rows in flight somewhere this ingest could not see, or abandoned
  reservations?
- Once this doc is merged, are the source digests retired from `to-browser/`, and who decides?

## Status

SEED — ingested 2026-09-17 from the Drive transport; awaiting triage of section G through the
decision engine. No rows filed or closed by this doc.
