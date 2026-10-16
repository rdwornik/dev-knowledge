# Archive copy of transport file DIGEST-HANDOVER-ANSWERS-2026-10-14.md

> Provenance: verbatim copy of `to-browser/DIGEST-HANDOVER-ANSWERS-2026-10-14.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] a5bee219e567a6d7. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-14
supersedes: none
summary: Tech-Architect-44's answers to the operator's 24 handover questions of 2026-10-14 (A decisions, B dispatch, C process, D where things are, E what is left, F what went wrong, G the handoff). The answers were first given in chat only; this file is that record, in English, updated with what was found later the same day: Conductor E ([#689], [#669]) was decided on 2026-09-09 and never built; TA-45's two sessions are running; the --dispatch-map generator exists only on the D5 branch. Repo facts are witnessed on main b46836c8 (git, 2026-10-14). Memory is marked UNVERIFIED, and "I don't know" is written where it applies.
by: Tech-Architect-44 (outgoing, 2026-10-08-dev-knowledge-architect, SEQ 1; Claude Code session aafe072f-4da2-5256-b29a-5c61187468a0, remote cse_014RFuLQH4gyfcjTpnbLRwAD)
to: Tech-Architect-45; the operator

# Handover answers — 24 questions (2026-10-14)

"STANDING" means the ruling is in `protocols/STANDING_RULINGS.md` on main.

## A. What was decided in my window

**1. Decisions.**

| Ruling | What it says | Where | Landed |
|---|---|---|---|
| R93 | B2-W3 GO under conditions; R73 set aside for B2-W3 only | RATIFICATION-2026-10-10 v3 | STANDING |
| R94 | Seat rotation by mechanism (Stop + SessionStart hooks), built by lane `seat-cycle` in B2-W4; D3 teardown rule | RATIFICATION-2026-10-10 v3 | STANDING; the mechanism was NOT built and `seat-cycle` never ran |
| R95 | Boot drift D1–D5: citations checked in code; the Project copy compared at boot | RATIFICATION-2026-10-10 v3 | STANDING; the code is on the unlanded D5 branch |
| R96 | Package D1–D15; Grok allowed (D13); D14 Codex and Copilot as producers; grimp | RATIFICATION-2026-10-11 | STANDING |
| R97 | CC runs B2-W4 with subagent lanes, one worktree each; replaces R96 D14; one land per wave | RATIFICATION-2026-10-12 v2 | STANDING |
| R98 | 58 known reds re-dated to 2026-10-31 | RATIFICATION-2026-10-12 v2, then 10-13 v2 | STANDING |
| R99 | CC orchestrates every vendor through `dispatch`; the browser reads ≤ 20 KB; a request until D1 lands | RATIFICATION-2026-10-12 v2 | STANDING; D1 not landed |
| R100 | Commit-attribution trailer design | RATIFICATION-2026-10-13 v2 | STANDING (my register F5 wrongly said it was not); D7 not built |
| R101 | Cost policy (a)–(i) | RATIFICATION-2026-10-13 v2 | Drive only |
| R102 | Handoff cut GO; `claude stop ac626cdc`; no back-dating | RATIFICATION-2026-10-14 | Drive only |
| R103 | A one-shot handoff | register §3 | a proposal, never ruled |

Not in any RATIFICATION file:
- "agy sign-in belongs to provisioning" (the operator; register v2 onward);
- "the backlog is the only lane entry; no arbitrary decisions" (the operator; my ANSWER to the plan review; TA-45 r4 took it);
- the GO for the branch deletion (the `branch-deletion-archive-tags` session; its exact file is UNVERIFIED);
- Q1–Q4 of the 2026-10-11 plan. Phase 0 ran; whether the operator answered "Q1–Q4 yes": I don't know.

The delegated decisions of 2026-10-14 are in DIGEST-OUTER-LOOP-RESEARCH v2 §3.

**2. Agreed to, and not done:**
- writing the 2026-10-11 plan to the transport (done only on 10-14, as register v3);
- the "harness process v2" ADR;
- the prose freeze (I broke it: 6 more orders and 1 AMEND);
- SEAT-LESSONS and an exam for the successor (R73);
- the reading contract (DIGEST-TOOLS-IN-USE D2);
- boot v2 landed before the handoff;
- `janitor --apply`;
- `seat-cycle` (R94 D2);
- D1 and D7;
- `cost_usd` per lane (R101f): BW had 0 `claude -p` launches;
- the bundle's FILL-INs;
- naming Conductor E ([#689], [#669]) as the open plan.

## B. How work actually runs

**3. How BW ran.**
- **10-12.** The operator pasted `BATCH-B2-W4-CC-FINISH-2026-10-12` plus `AMEND-…-R99` into one new CC session on the laptop, in the primary checkout. That was session 2d59e52d, Opus 5.5 high, orchestrator and integrator in one. The laptop lost power at about 17:17, mid-F0.
- **10-13, night.** `BATCH-BW-NIGHT-2026-10-13` went into a new CC session (Opus 5.5 high). It landed F0 `3db32c1a`, F1 `26bd4d93` and Wave C `d8619ab0`, then stopped on the 30-minute rule.
- **10-13, finish.** `BATCH-BW-FINISH-2026-10-13` v2 went into a new session: Sonnet 5.5 medium main thread, with at most 3 Opus architect-review calls. It landed Wave D `8e00b78d` and the close packet `2512b210`.
- **Each lane:**
  - the main thread ran `/lane-boot <batch> <id> <slug> <contract>` to provision a worktree, then an Agent-tool subagent worked in it;
  - review was `codex exec -s read-only`;
  - usage tests were `copilot -p … --allow-all-tools`;
  - D7 was produced by Codex.
- **Merge and close.** The same session merged the approved lanes of a wave into `worktree-integrate-bw`, then ran one `merge_path.py land --slug b2-w4-d`. The close receipt `0d3f7433` is still unlanded on that branch.
- **Afterwards.** Hygiene and `claude stop` ran in a separate session, on the operator's GO. The handoff was `/handoff` in architect mode, landed as `b46836c8`.
- The operator's paste was one line, "Read to-cc/<order> … execute it exactly; lint first". Its exact wording is UNVERIFIED.

**4. `/lane-boot` versus `dispatch.py launch`.**
- **`/lane-boot`** (`.claude/commands/lane-boot.md`) is an in-session prose procedure. It provisions the worktree, loads the contract and states the budget. It starts no process.
- **`dispatch.py launch CONTRACT`** (`scripts/dispatch.py:1803`) runs the pre-launch moment (occupancy, a live integrator, routing agreement), then spawns `claude --bg -n <slug>` or `codex exec`, and writes a launch receipt under `logs/receipts/`. It refuses with exit 5.
- **Which is official:** the repo says `dispatch.py launch` (MAP-DISPATCH: local = launch, PROVEN by `tests/test_dispatch_launch.py`).
- **Why BW used the other:** my R97 order said so, which is how dispatch got bypassed.
- **Contradiction:** Phase 0 lists `/lane-boot` as INERT, yet BW's order used it. Whether the session really invoked it: I don't know.
- **MAP-DISPATCH's provenance:** it was generated by `gen_handoff.py --dispatch-map`, which exists only on the D5 branch, not on main.
- **Under Conductor E,** both are replaced: [#689] §5 retires the dispatcher and integrator seats and "paste this to the integrator".

**5. Substrates.**
- **Local:** works. Start with `dispatch.py launch <contract>`, or in a session with `/lane-boot` plus a subagent. Limits: RAM (13 of 27.7 GB free in Phase 0) and 6 parallel lanes measured.
- **Codespace:** not end to end. The start verb is `dispatch.py codespace-exec`, PROVEN by a unit test only. It is blocked by credentials (Q6) and by the branch being far behind. TA-45's `BATCH-CODESPACE-FINISH` is running now.
- **Anthropic cloud:** DECLARED only. MAP-DISPATCH shows no start verb, so it is started by hand, with no receipt. Whether it was tested this window: I don't know.

**6. Codespace.**
- **What failed (commit `eea31c5d`, 2026-10-10).** `codespace-exec` refused twice at the credential-mirror step. The laptop Codex cache was 7.2 days old, in the dead band between the 7-day mirror limit and Codex's 8-day self-refresh. No Codespace was created.
- **What was tried:** two parity runs; Codex review rounds (FAIL, then fixed, `ff88c052`); `codex login` on 10-13. Whether the gate passes now is UNVERIFIED: there has been no run since.
- **agy:** its credential lives in Windows Credential Manager, so there is no file to mirror (`codespace_parity.py`, "BLOCKED-AUTH").
- **The one thing:** a fresh run with the Codex mirror, with agy signed in by device login at creation (D4). TA-45's order is doing exactly this, on branch `worktree-codespace-finish-2026-10-14` (`0d97edde`).

## C. The process

**7. The flow, step by step:**
- **ADR:** files; C5 flags are report-only; `/decide` is unused.
- **Backlog row:** code (`tasks/`, a generated BACKLOG, the close gate). But no lane is forced to own a row: 14 of 16 lanes owned none.
- **Distiller:** the code exists but sits off the entry path. It picks no vendor and enforces no tier.
- **Dispatch:** code, bypassed in BW.
- **Lane:** code (worktrees).
- **Gates:**
  - RED test: missing;
  - review: prose;
  - hooks: 17 armed, 18 manual;
  - CI: code;
  - commit-gate, ship-gate and phase-gate: `continue-on-error`;
  - ruleset: disabled.
- **Land:** code (`merge_path.py land`), not exclusive.
- **Evaluation:** prose. No merge telemetry since 10-10.
- **Git attribution:** missing (D7). Only `seat-ids.yaml` exists.
- **Map:** code (`system_map.py`, `/map`).
- **Handoff:** the generator is code, but the map diff never reaches the handoff and the boot is stale.
- **The transitions between all of these** are [#669], unbuilt.

**8. The distiller.**
- It takes `(kind, subject)`: kind is a BUILD-MODE delta (ARM, WIRE, REWRITE, MOVE, DELETE, BUILD) and subject is a row of `protocols/BUILD-LIST.md` (`gen_lane_contract.py` from about `:1687`; the error is at `:1746`). It was built for BUILD MODE, so it refuses a backlog row by design.
- The spine's stage 1 reads BUILD-LIST too (`harness.yaml:13`).
- The plan was SPINE-MAP gap G1 (repoint to `tasks/`) and `[#923]`/`[#617]` (vendor choice). Neither was built.
- Now: D3 (the vendor comes from the registry) and step 4 of the plan.

**9. Isolated agents.**
- **In code today:**
  - `offload_admission.py` denies a read route a verdict (INERT);
  - `read_gate` verifies quotes (INERT);
  - `conductor.py` phase gate, read-only and report-only;
  - the reviewer ≠ producer rule is prose (R101i).
- **Not in code:** one agent per stage with independent adversarial evaluators. It exists only in TA-45's pilot order (prose) and in [#669], unbuilt.
- **D1 lane-controller** (`b1db35ff`, 13 commits, +991 lines in `dispatch.py`, `merge_path.py`, `lane_digest.py`):
  - dispatch launches every producer kind (claude, codex, copilot) and records it;
  - land refuses an undispatched lane;
  - Windows spawn fixes and Copilot flag fixes.
- D1 does no stage isolation. Its 3 HIGH: land refuses the integrator's own merges; a fixture writes the live seat registry (Phase 0 E8: `test_seat_registry.py:317/482/519`, `CLAUDE_PID=os.getpid()`); the third: I don't know.

## D. Where everything is

**10. Read first, in order:**
1. `to-browser/LEDGER-dev-knowledge.md` v195 (TA-45's, with THE FLOW).
2. `to-browser/DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md` v2 (the plan).
3. `to-browser/DIGEST-PHASE0-2026-10-14.md`.
4. `to-browser/MAP-DISPATCH.md`.
5. `to-browser/DIGEST-TOOLS-IN-USE-2026-10-11.md`.
6. `tasks/689-conductor-e-is-decided-and-unbuilt.md` and `tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md`.
7. `to-cc/BATCH-BW-FINISH-2026-10-13.md` v2 (how a batch really ran).
8. `to-browser/DIGEST-SPINE-MAP-2026-10-10.md`.
9. RATIFICATION 10-12 v2, 10-13 v2, 10-14 v2.
10. `protocols/HANDOFF_BOOT.md` (stale since `f74d1c4c`).

**11. Maps:**
- **MAP-DISPATCH** (10-10): its verbs match `dispatch.py` on main, but its generator is unlanded (the D5 branch).
- **DIGEST-SPINE-MAP** (10-10): holds; G1–G10 are open, G7 partly.
- **System map:** main has record `47a6388c`; `88f1bc52` is on the unlanded `worktree-system-map-2026-10-14` (`c2953534`), which the green-main pilot's Part C lands.
- **DIGEST-HARNESS-CHECKLIST-2026-09-29** and **DIGEST-CAPABILITY-MAP 09-25 to 09-28:** stale (pre-B2; not re-checked by me).
- There is no map of maps.

**12. Drive simplification:** NOT done.
- On main (D8): `transport.py index`, `query`, `janitor`, `seat-ids`, and lint enforces the head fields on new files.
- Never applied: `index --write` was not run and `janitor --apply` was not run.
- Why: the janitor moves live Drive files, so it waited for seat approval. I put it in BW's scope and did not run it at the close.
- The INDEX at 345 KB is the legacy one. D5(a) of the plan does it.

## E. What is left

**13. Priorities:** DIGEST-OUTER-LOOP-RESEARCH v2 §4.
1. The two running sessions finish.
2. Turn on what is built: janitor and INDEX; boot v2; rulings; gates.
3. [#689] (phase field, phase table, blocking gate).
4. [#669] transitions, with spine stage 1 reading `tasks/`.
5. The steel thread.
6. Everything else as rows.
7. Prose removal.

Why this order: nothing lands on red; switching on built things is cheap and visible; [#689] and [#669] are the cause, not a symptom; everything else is cheaper once the loop exists.

**14. Unlanded branches (live origin, `git ls-remote`, 2026-10-14):**

| Branch | Tip | Ahead / behind | Contents | To land |
|---|---|---|---|---|
| `worktree-lane-bw-1374-lane-controller` | `b1db35ff` | 13 / 63 | D1, see Q9 | rebase; fix 3 HIGH; non-Anthropic review; a real row (not [#1374], which is the dispatch shim) |
| `worktree-lane-bw-1450-boot-teaching` | `f0d49169` | 19 / 63 | boot v2 (5 F4 pointers), R95 D1 citation check, `--dispatch-map` / `--reading-path` | fix the citation-check HIGH; rebase; `verify_handoff_probes`; re-write the Project copy |
| `worktree-b2w2-codespace-finish` | `eea31c5d` | 43 / 187 | Codespace parity, Codex credential mirror | superseded by the 10-14 rebase below |
| `worktree-codespace-finish-2026-10-14` | `0d97edde` | — | today's rebase, by TA-45's order (running) | its order |
| `worktree-integrate-bw` | `0d3f7433` | 1 / 4 | the BW close receipt | the next integration |
| `worktree-system-map-2026-10-14` | `c2953534` | — | map record 47a6388c → 88f1bc52 | green-main Part C |
| `automation/fleet-audit` | `d931ac47` | — | a scheduled routine | leave it |

Removed branches (D2 handoff-gen `10268435`, merge-clock, distill-kind-fix, integrate-b2-w4/-b/-c, verify-onboarding) are preserved by 39 archive tags on origin. The per-name mapping is UNVERIFIED.

**15. Commands and skills:**
- **Used:** `/handoff`, `/lane-integrate`, `/map`, `/lane-boot` (contested, see Q4).
- **Unused:** `/why`, `/spine`, `/decide`, `/boot-session`, `/changelog-review`, `/save`, `aj-scan`, `verify`, `check-against-spec`.
- **`/handoff-verify`** crashes on cp1252 and is not part of the boot (R30): fix it or remove it.
- No removal before the loop exists. The green-main pilot's Part A census gives KEEP/REMOVE; removal is the operator's act.

## F. What went wrong (did I know · why not handed over · the fix)

**16. The handoff broke main.**
- Did I know: partly. I knew seat-release failed on the filled bundle's manifest sha (LEDGER v187 BLOCKED BY 2). I did not know it fails tests on main.
- Why not handed over: I did not check CI after `b46836c8`, and I wrote "main green" from a relay.
- Fix: R103 item 4 (re-stamp the manifest after the fill); in progress as green-main defect X2.

**17. `ci_verdict` reads a retired step.**
- Did I know: no. I even advised "trust the bundle row" (the interview, Q4).
- Fix: `SUITE_GATE_STEP_NAME` (`ci_verdict.py:114`) reads the known_reds step; in progress as green-main defect X3.

**18. The provider registry.**
- Did I know: only that Grok and Gemini had no route. I never read `provider-registry.yaml` this window.
- Fix: D3, plus a model-currency check.

**19. The wrong row ids.**
- Did I know: no. My error: I took `[#1374]` and `[#1439]` from branch names, not from `tasks/`.
- Fix: rows filed through intake; under Conductor E a lane cannot exist without its row.

**20. The boot has not changed since 2026-10-04.**
- Did I know: yes, but only after the cut (register §7). I neither stopped the cut nor patched the boot.
- Fix: D5(b), then a boot-drift gate as a row.

**21. R48 print, the constraint registry, 13 INERT tools, prose gates, a disabled ruleset.**
- Did I know: the ruleset, the commit-gate, prose review and 5 INERT items, yes (LEDGER v187). The R48 absence and the full INERT list, no.
- Fix: D5(d), [#689] (required checks as gates), and R48 as a row.

**22. Preflight, Actions minutes, the map branch.**
- Did I know: I knew P11 at 145 OPEN files; not the QUESTION `disposition:` rule; not the 364 % Actions minutes. I wrote "not billed (public repo)" from memory, which is UNVERIFIED and most likely wrong. The map branch appeared after my work.
- Fix: janitor; `on.paths` in CI; the map refresh landing through the loop.

## G. The handoff

**23. Why it did not onboard TA-45.**
- The boot was 10 days stale.
- The FILL-INs were empty.
- There were no lessons and no exam.
- Dispatch knowledge lived in my orders and SESSION files.
- MAP-DISPATCH came from unlanded code.
- The LEDGER was wrong about CI.
- Conductor E ([#689], [#669]), the decided outer loop, was named nowhere.
- I then wrote the register after the cut, in pieces.

In his first five minutes he should have been told:
1. main is red; fix it first.
2. How a batch really runs (BW-FINISH v2); `dispatch.py launch` exists and BW bypassed it.
3. The outer loop is decided and unbuilt: [#689] and [#669]. Finish it; design nothing new.
4. The tools exist (DIGEST-TOOLS-IN-USE); read only the LEDGER, MAP-DISPATCH, TOOLS-IN-USE and Phase 0.
5. The open rulings and dates: 10-19 `manual_until`, 10-31 known reds.

**24. Reported as done or true, and not:**
- "main green apart from registered reds" (LEDGER v187);
- "nothing blocks the successor's boot";
- `[#1374]` and `[#1439]` as the owning rows;
- "62 hits manual_until" with "effect unknown" (Phase 0: 90 entries; nothing blocks);
- "Actions not billed";
- "Codespace unblocked except agy", which no run has shown;
- `--trial-cut :3526` (it is `:3528`);
- and in the other direction: R100 reported as unlanded (it is STANDING).
