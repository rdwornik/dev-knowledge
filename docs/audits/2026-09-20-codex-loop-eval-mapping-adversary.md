# Codex adversary pass over the loop-eval MAPPING (LANE-loop-eval, step 4)

> **Status:** record. Carrier row `[#929]`. Artifacts attacked: `2026-09-20-technical-loop-eval-mapping.md` (committed `0e32bd77`) and `2026-09-20-technical-loop-eval-live-probes.md` (committed `e06d3159`).
> **This is the Codex pass over the MAPPING the contract asks for (Done-contract 4):** the findings verbatim, then an accept / reject reason per finding.

## How it was run

```
codex exec -c model=gpt-5.6-sol --sandbox read-only --json --skip-git-repo-check -o adv-last.txt - < adv-prompt.txt > adv-events.jsonl 2> adv-err.txt
```

- **Requested model: `gpt-5.6-sol`.** The contract says "pinned to sol per the repo's routing". `ecosystem/routing-table.yaml` `roles.adversarial` is `cli: codex` with **no model pin** (its note says the row was rebound from `sol` on 2026-09-05 and to "restore `sol` here once it is installed"); `gpt-5.6-sol` is in `ecosystem/provider-registry.yaml` only as a provenance id. The CLI accepted the id (a `SOL_OK` probe returned exit 0), but `codex exec` reports no served model, so **"sol answered" is attested by the flag, not by the output**. Filed as `to-browser/QUESTION-lane-loop-eval.md` Q1; the pass ran on.
- **Mode:** read-only sandbox, stdin closed by a file redirect, no write mode. Exit 0, 90.6 s wall, 17 JSONL events.
- **Usage reported** (`turn.completed`): input 316,323 tokens (262,016 cached), output 4,629, reasoning 488. **No cost is reported** by `codex exec`; none is invented here.
- **Prompt:** an adversarial brief, not a diff review — it named the two records, asked "What breaks when dispatch and integration become spine stages? What does this mapping get wrong?", required a quoted claim, a repo path and line the critic opened, and a severity, and listed eight specific things to test. The full text is in the job's scratch dir; the questions are reproduced above.
- **Before accepting anything, the load-bearing citations were opened and checked** (lane-integrate.md :44-50, :108-136, :186-192, :346-351; PLAYBOOK :2385-2388, :2815-2823; graph_queries.py :410-420). Results are in the disposition column.

## The findings, verbatim

1. **HIGH — Stage ordering makes REVIEW and GATES post-merge in the live integrator protocol.**  
   **Claim attacked:** Mapping §1: “14 REVIEW … 15 GATES … 16 MERGE”; rows `scripts/review_packet.py` and `scripts/merge_receipt.py` assign them to stages 14 and 16.  
   **Counter-evidence:** `.claude/commands/lane-integrate.md:122` executes `git merge --no-ff` before assembling the review packet and racing review with the suite; `.claude/commands/lane-integrate.md:190,348-350` requires pushing the merge before its Actions verdict can be read.  
   **What breaks:** The proposed 13→14→15→16 sequence cannot preserve the existing integration protocol because its review, suite, and Actions gate operate on an already-created—and partly already-pushed—merge.  
   **Severity:** HIGH

2. **HIGH — Making `dodo.py` spawn stage 13 violates the explicit Layer-2 execution boundary.**  
   **Claim attacked:** Mapping §1 and `scripts/dodo.py` row: “under R1 it becomes the runner of 1-16.”  
   **Counter-evidence:** `CLAUDE.md:96` says “no script drives state in a child repo”; `scripts/dispatch.py:8-18` says this boundary is why the module “NEVER spawns a lane” and places spawning in the caller-side shim.  
   **What breaks:** A hub-side `dodo.py` RUN action collapses the ruled hub/caller split unless the runner is moved to the caller or stage 13 delegates across that boundary without spawning itself.  
   **Severity:** HIGH

3. **HIGH — Stage 13 also contradicts the standing operator-dispatch rule, not merely a historical implementation detail.**  
   **Claim attacked:** Mapping PLAYBOOK row “AM-5 operator dispatches” is stage 13/KEEP while the mapping simultaneously proposes stage-13 agent execution.  
   **Counter-evidence:** `protocols/PLAYBOOK.md:2815-2823` requires the operator to dispatch from a terminal and says lanes are “never spawned from the primary session or any other session”; `protocols/PLAYBOOK.md:2874` classifies the surrounding workflow as local and interactive.  
   **What breaks:** An agent-driven spine invocation would become the forbidden nested/session-side dispatcher unless AM-5 is explicitly superseded; marking it KEEP conceals the contradiction.  
   **Severity:** HIGH

4. **HIGH — `check_go_artifact` does not prove operator GO.**  
   **Claim attacked:** Mapping §2/§6: `lane_boot.py` includes “a GO artifact” and “The GO artifact already exists on the boot side.”  
   **Counter-evidence:** `scripts/lane_boot.py:154-168` selects the last table row containing the lane name; `scripts/lane_boot.py:170-193` accepts any such row whose text does not contain `HELD`; the docstring explicitly excludes the operator’s `RATIFICATION-<date>.md`.  
   **What breaks:** A planned or mechanically generated non-HELD manifest row is treated as operator authorization, so the supposed boot-side GO predicate proves roster state, not consent.  
   **Severity:** HIGH

5. **HIGH — The proposed merge-side GO reader cannot be “the same predicate applied to a merge.”**  
   **Claim attacked:** Mapping §2: “the reader for it is the same predicate applied to a merge.”  
   **Counter-evidence:** `scripts/lane_boot.py:170-193` recognizes lane names plus `HELD` state only, whereas `.claude/commands/lane-integrate.md:47-50` authorizes the whole batch with one GO and `protocols/PLAYBOOK.md:2387` requires “operator GO each” merge.  
   **What breaks:** Boot authorization, batch authorization, and per-merge authorization have different subjects and cardinalities, so reusing this predicate would either authorize too much or reject the ruled batch-wide ceremony.  
   **Severity:** HIGH

6. **HIGH — The “whole loop” runner still declares itself contract preparation only.**  
   **Claim attacked:** Mapping row `scripts/dodo.py`: stage `1-12`, verdict KEEP, “under R1 it becomes the runner of 1-16.”  
   **Counter-evidence:** `scripts/dodo.py:7-12` says “this PREPARES A CONTRACT” and rejects moving rows through dispatched/merged phases; `ecosystem/harness.yaml:5-6` repeats that the spine prepares a contract and moves no row through a phase.  
   **What breaks:** Extending this unchanged organ to RUN and MERGE directly contradicts both authoritative docstrings, so KEEP is the wrong verdict; the runner’s contract must be superseded or a different orchestration layer introduced.  
   **Severity:** HIGH

7. **HIGH — The mapping assigns the review packet to pre-merge stage 14 although its own consumer creates it after merge.**  
   **Claim attacked:** Mapping organ row `scripts/review_packet.py`: stage 14, “BECOMES-STAGE-14.”  
   **Counter-evidence:** `.claude/commands/lane-integrate.md:122-130` merges first and only then invokes `review_packet.py --range main..worktree-$L`; after the merge, that range may be empty because `main` contains the lane tip.  
   **What breaks:** Preserving the current command order can produce a packet with no branch diff, while moving it before merge changes the protocol the mapping claims merely to absorb.  
   **Severity:** HIGH

8. **MED — `MERGE-INTO-dispatch.py` contradicts `dispatch.py`’s explicit retained surface.**  
   **Claim attacked:** Mapping external-organ row `Invoke-Dispatch.ps1`: verdict “MERGE-INTO-`scripts/dispatch.py`.”  
   **Counter-evidence:** `scripts/dispatch.py:35-48` lists only selected ports under “WHAT MOVED,” while `scripts/dispatch.py:56-59` says cloud dispatch, harvest, `Start-DispatchAfter`, deep-code, and derived-line fallback “DID NOT MOVE” and remain in win-tooling.  
   **What breaks:** Retiring or merging the external organ into `dispatch.py` would drop live capabilities that the target module expressly does not contain.  
   **Severity:** MED

9. **MED — `RETIRE-CANDIDATE = 0` suppresses an expressly unresolved retirement candidate.**  
   **Claim attacked:** Mapping §1: “`RETIRE-CANDIDATE` is 0, on purpose,” and `scripts/gen_ledger.py` row: KEEP.  
   **Counter-evidence:** `scripts/graph_queries.py:413-418` records `gen_ledger.py` as a new orphan owned by the “V+1 retirement-or-wiring list”; the mapping row itself says “no live trigger.”  
   **What breaks:** An organ with no trigger and an explicit retirement-or-wiring owner meets the mapping’s candidate purpose even if deletion has not yet been adjudicated; KEEP converts unresolved disposition into presumed retention.  
   **Severity:** MED

10. **MED — The B3 diagnosis misses that `dep_file` introduces shared mutable state and concurrency risk.**  
    **Claim attacked:** Live-probes B3: “doit’s state db … records task results, but no stage consults it.”  
    **Counter-evidence:** `scripts/dodo.py:29-38` creates one temp database keyed only by checkout path and configures it as `dep_file`; its docstring promises only that different worktrees do not share state, not that concurrent runs in the same checkout are isolated.  
    **What breaks:** Two spine invocations in one checkout contend on the same external database even though caching is disabled, so the state file is operationally relevant and can become a lock/corruption/failure surface.  
    **Severity:** MED

11. **MED — “No resume, by design at `dodo.py:75`” overstates what the code establishes.**  
    **Claim attacked:** Live-probes B3 verdict: re-execution is “by design” because every task has `uptodate: [False]`.  
    **Counter-evidence:** `scripts/dodo.py:66-76` forces re-execution, but neither that function nor its docstring states an interrupted-run policy; `scripts/dodo.py:29-38` still provisions persistent doit state.  
    **What breaks:** The probe proves current no-resume behavior, but not a deliberate resume design; treating it as settled avoids the required policy decision for expensive agent, review, and merge stages.  
    **Severity:** MED

12. **MED — B1 proves one SDK path, not that “the Agent SDK works as an adapter.”**  
    **Claim attacked:** Mapping §2 and live-probes B1 verdict: “the Agent SDK works as an adapter.”  
    **Counter-evidence:** The inline probe in `docs/audits/2026-09-20-technical-loop-eval-live-probes.md:43-99` exercises only `query()` with `Read|Bash`, one hook, one process, and a budget; `scripts/dispatch.py:151-171` requires stop confirmation and distinguishes an ungoverned surviving lane.  
    **What breaks:** The probe does not establish process-tree teardown, cancellation, crash recovery, durable identity, or cap enforcement after adapter death—the properties RUN needs to avoid leaving a writing agent alive.  
    **Severity:** MED

13. **MED — B4 disproves AM-5’s observation but does not validate unattended stage-13 completion.**  
    **Claim attacked:** Mapping §2: “B4 — a `--bg` spawn from inside a session gets its own row and record,” used as positive stage-13 evidence.  
    **Counter-evidence:** Live-probes B4 records that the job returned to `working` and began reading `JOURNAL.md` after reporting `DONE`; `protocols/PLAYBOOK.md:2815-2823` still forbids session-side spawning.  
    **What breaks:** The mechanism supplies identity but not terminality or policy compliance, so a stage can falsely regard an answer as completion while the spawned agent continues acting.  
    **Severity:** MED

14. **MED — Stage 15’s stated gate set is not the current integration gate set.**  
    **Claim attacked:** Mapping §2: stage 15 consists of “audit / ship-gate / ruff / impacted tests.”  
    **Counter-evidence:** `.claude/commands/lane-integrate.md:126-135` runs the full pytest suite and review concurrently after merge; `.claude/commands/lane-integrate.md:190,348-350` additionally requires a pushed-merge Actions verdict; `ecosystem/harness.yaml:14-17` only selects impacted tests at stage 10 and has no stages 13-16.  
    **What breaks:** Implementing the mapped list would omit the current full-suite and Actions predicates or duplicate them at incompatible times.  
    **Severity:** MED

15. **LOW — The ARMED/INERT hook counts are correct but “ARMED” overstates execution coverage.**  
    **Claim attacked:** Mapping §1/§2: “36 pre-commit hooks — 17 ARMED, 19 INERT.”  
    **Counter-evidence:** `.pre-commit-config.yaml` contains exactly 36 hook IDs, 19 with `stages: [manual]`, leaving 17 non-manual entries; however `.pre-commit-config.yaml:814-829` includes pre-push hooks, so the 17 are not all pre-commit-time gates.  
    **What breaks:** The arithmetic is correct, but treating all 17 as one armed stage-15 population conflates commit and push triggers and obscures when each predicate can block.  
    **Severity:** LOW

16. **LOW — The mapping omits `templates/dispatch-shim.ps1` as an organ row despite making it the only sanctioned spawner.**  
    **Claim attacked:** Mapping §2 says the shim is “the caller-side spawn,” while the enumerated surface totals and tables provide no dedicated shim organ row.  
    **Counter-evidence:** `scripts/dispatch.py:8-18` assigns spawning to `templates/dispatch-shim.ps1`; the mapping only mentions it inside prose and `scripts/dispatch.py` grounding (`mapping.md:41,170`).  
    **What breaks:** The component that actually crosses from plan to a live agent has no independent stage, trigger, verdict, or failure analysis, leaving stage 13’s most stateful organ unmapped.  
    **Severity:** LOW

TALLY HIGH:7 MED:7 LOW:2

## Disposition — accept / reject, with the reason and what changed

```
#   sev   verdict          reason (evidence opened)                                                          change made
1   HIGH  ACCEPT           lane-integrate.md:122 `git merge --no-ff` runs FIRST, then the review packet      MAPPING §4 stage 15: the live
                           (:124-130), then suite || review (:131-135), then push (:186-192), then Actions   order stated; §6 finding 9. The ADR
                           verdict (:346-351). Verified. Review and gates sit between a LOCAL merge and      must place 14 and 15 around the
                           the push; "MERGE" is two acts.                                                    local merge and the push.
2   HIGH  ACCEPT IN PART   Layer-2 boundary (CLAUDE.md :96; dispatch.py :8-18) is real; the mapping already  dodo.py row now names the scope
                           named it (§4 stage 13 item 3, §6 finding 2). What the critic is right about is    text that must be superseded.
                           that the `dodo.py` row said "becomes the runner of 1-16" without saying that
                           dodo.py's own docstring (:7-12) forbids it.
3   HIGH  ACCEPT           PLAYBOOK :2815-2823 (AM-5) verified verbatim. B4 re-witnessed its premise false;   MAPPING §4 stage 13 states AM-5
                           DECLARE R7 says that re-rules nothing. The AM-5 row is KEEP and stays KEEP, but   still binds; §6 finding 10.
                           a session-side stage 13 is barred until AM-5 is re-ruled.
4   HIGH  ACCEPT IN PART   lane_boot.py :154-193 reads a manifest row naming the lane and accepts anything   Wording: "GO artifact" now says
                           not HELD; its docstring records the operator's RATIFICATION file as a documented  it is the seat's roster state, not
                           gap. So it is roster state, not proof of consent. It is still the ruled [#685]    the operator's own file.
                           artifact and the only boot-side GO reader; "does not prove consent" is the fair
                           limit, and it is now stated.
5   HIGH  ACCEPT           "the same predicate applied to a merge" was an overclaim: boot is per lane;       Reworded to "same style, not the
                           lane-integrate.md :44-46 says ONE GO for the batch; PLAYBOOK :2387 says          same predicate"; QUESTION Q3
                           "operator GO each". Verified: the two prose texts DISAGREE. That is a functional  written for the operator.
                           question (ADR-108 §A), so it is escalated, not decided.
6   HIGH  ACCEPT IN PART   Same evidence as 2 (dodo.py :7-12; harness.yaml :5-6). KEEP stands — the organ    dodo.py row + ADR name both texts
                           stays and R1 extends it — but the critic is right that KEEP with no qualifier     as text to supersede.
                           hides that the scope text must change.
7   HIGH  ACCEPT           lane-integrate.md :122-130: `--range main..worktree-$L` is evaluated after the    MAPPING §4 stage 15 records it "as
                           merge into main, where main already holds the lane tip -- an empty range by git   written". Not filed as a row (the
                           semantics. As written this is a documentation defect in a live command.           seat files rows); listed in the DIGEST.
8   MED   ACCEPT           dispatch.py :56-59 lists what did NOT move. The row's MERGE-INTO overclaimed;     Verdict now "MERGE-INTO-dispatch.py
                           the merge is of the ported functions, not the file.                               (PARTIAL: the ported functions only)".
9   MED   ACCEPT           graph_queries.py :413-418 (and the register's other entries): owner "V+1          RETIRE-CANDIDATE 0 -> 3 (gen_ledger.py,
                           retirement-or-wiring list" for gen_ledger.py, offload_admission.py,              changelog-review.md, save.md — those
                           propose_row_closures.py and five .claude entries. "0, on purpose" was wrong.     with no loop role); the wiring
                                                                                                             branch proposed for the other five.
10  MED   REJECT           UNVERIFIED speculation: the critic did not run two concurrent spine runs; doit's  Recorded as "not probed" in B3 so
                           behaviour on a shared db file is not measured, and the probe's question was       it is not lost.
                           resume, not concurrency.
11  MED   ACCEPT           dodo.py :75 records no reason. "Deliberate choice" was my inference.               B3 wording corrected in the
                                                                                                             probes record.
12  MED   ACCEPT           B1 shows one process, two tools, one hook, one budget. Teardown, cancellation,    B1 verdict now lists what it did
                           crash recovery and run identity were not probed.                                  not test; MAPPING §4 reworded.
13  MED   REJECT           Duplicate of what the records already say: B4 records the job resuming work after  none
                           `DONE`, MAPPING §6 finding 7 says a quiet spawn is not proven, and AM-5 is
                           stated as still binding. B4 is not used as completion evidence anywhere.
14  MED   ACCEPT           The integrator's gate set today includes the full pytest suite on the merged      MAPPING §4 stage 15: the current
                           result and the pushed-merge Actions verdict (lane-integrate.md :346-351); R1's    gate set is stated next to R1's list.
                           four-name list is narrower.
15  LOW   ACCEPT (wording) 17 / 19 arithmetic is right (the critic confirmed it against the file); the 17    MAPPING §4 breaks the 17 into 12
                           armed hooks are not all pre-commit-time gates.                                    commit + 3 commit-msg + 2 push.
16  LOW   ACCEPT           templates/dispatch-shim.ps1 is the only sanctioned spawner and had no row.        Row added (external / other organs).
```

**Tally of dispositions:** 16 findings — 10 ACCEPT, 3 ACCEPT IN PART (2, 4, 6), 2 REJECT (10, 13), and finding 15 accepted as wording. Every HIGH was verified against the file it cites before it was accepted.

## What the adversary did not do

- It raised nothing against **B2** or the **stage 14** analysis, although the prompt named "B1/B2 overclaim" as a check; silence is not a clean bill for those two.
- It did not run anything: read-only, no suite, no probe re-run. Every finding is a code read.
- **Independence caveat:** the requested model is `gpt-5.6-sol` and the served model is not attestable (above); the pass is a different vendor from the records' author, which is the property the adversarial role needs, and no more than that is claimed.
