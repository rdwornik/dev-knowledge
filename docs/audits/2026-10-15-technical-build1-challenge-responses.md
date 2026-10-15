# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-RESPONSES-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-RESPONSES-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] 3d0504065740d84a. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: the producer's response to every finding of the two BUILD-1 CHALLENGE evaluators (EVAL1 Codex gpt-5.6-sol, 54 ids; EVAL2 Grok grok-4.20-0309-non-reasoning, 23 ids), one row each, plus the research subagents' claims with their probes.

# RESPONSES - BUILD-1 CHALLENGE

Evaluator records: `to-browser/DIGEST-BUILD1-CHALLENGE-EVAL1-2026-10-15.md`, `...-EVAL2-...`. Matrices: `...-M2-R113-...`, `...-M3-R114-...`, `...-M4-RUNNER-...`, `...-M5-L6-...`. Verdicts land in `to-browser/DIGEST-BUILD1-READY-2026-10-15.md` `## CHALLENGE`.

## EVAL1 - Codex sol

| id | topic | response |
|---|---|---|
| X-I1-1 | concurrency already live | **Accepted** -- `conductor.yml:87-89`; L3 builds no concurrency, only the group-key fix `[#1540]` (schedule run cancels main's push verdict). |
| X-I1-2 | nightly Windows drops the per-change gate | **Accepted** -- R111 Linux-first: DISAGREE/INPUT_REQUIRED; no row filed. |
| X-I1-3 | `pytest (windows-latest)` is a required context | **Accepted** -- ADR-127 D3; a change needs a ruleset migration and a ruling. |
| X-I1-4 | savings claim unsupported | **Accepted** -- repo is PUBLIC, standard runners free; last 7 d linux 3,579 min / windows 3,986 min at $0; Windows leg 26.5 min < ADR-127 40-min flip. |
| X-I2-1 | no duplicate ruff hook | **Accepted** -- one hook, `.pre-commit-config.yaml:824`; List A item dropped. |
| X-I2-2 | plugin validate_backlog is a carrier twin | **Accepted** -- kept; used by propose_closures/review_closures + parity test. |
| X-I2-3 | hub validator declares the twin | **Accepted** -- same disposition as X-I2-2. |
| X-I2-4 | aider/llm/amp are negative probes | **Accepted** -- kept; `tests/test_provider_bench.py:433-438`. |
| X-I2-5 | terra job is a deliberate report-only signal | **Accepted** -- kept; pinned by `tests/test_conductor.py:709-719`. |
| X-I3-1 | bypass unnecessary for the measured case | **Accepted** -- reads declare the workspace with an absolute path plus `--add-dir` (common rules §8). |
| X-I3-2 | read_gate already passes bypass | **Accepted** -- `read_gate.py:375-381`; L2 adds no agy route. |
| X-I3-3 | bypassed agy wandered before | **Accepted** -- confinement is INPUT_REQUIRED to the operator. |
| X-I3-4 | read-only tasks is no mitigation | **Accepted** -- same INPUT_REQUIRED; agy never pointed at a writable tree. |
| X-I3-5 | F2 does not establish confinement | **Accepted** -- recorded in M2; `--sandbox` unprobed. |
| X-I4-1 | distiller duplicates map/reuse stages | **Accepted** -- `distill` extends `gen_lane_contract`, reuse candidates come from `file_purpose_graph.py why` and organ-index. |
| X-I4-2 | payload-only contradicts dodo's exit-0 receipt | **Rejected** -- dodo's receipt governs doit stages; a vendor point task may never exit (`copilot.exe`, codespace LANE-END G2), so exit is recorded, not required. |
| X-I4-3 | stale or prewritten payload | **Accepted** -- completion needs a FRESH payload: schema-valid, spawn nonce, input hash, mtime after spawn (`[#1535]` (1)). |
| X-I4-4 | recreates doit lifecycle | **Accepted** -- phases run as doit tasks via `conductor.py lane`; PhaseReceipt keeps the ten dodo keys. |
| X-I5-1 | import-linter retrial vs ADR-124 trigger | **Accepted** -- the BUILD-3 trial must test ADR-124's flip condition; nothing built in BUILD-1. |
| X-I5-2 | BUILD-3 catalogue is not one row | **Accepted** -- no row filed now; one row per tool at BUILD-3 filing. |
| X-I5-3 | consumer first | **Rejected** -- the operator's standing order sequences trials before the consumer; recorded as the evaluator's objection. |
| X-I6-1 | python-statemachine is a second authority | **Accepted** -- BUILD-1 freezes option a (conductor + doit + pydantic); psm stays behind the `[#669]` spike. |
| X-I6-2 | pydantic is no differentiator | **Accepted** -- M4 re-scored. |
| X-I6-3 | doit already chosen | **Accepted** -- M4 option a is the incumbent. |
| X-I6-4 | e recommended before V9 | **Accepted** -- V9 shows doit gates natively; a wins 3.55 vs 3.35. |
| X-I7-1 | L1 not disjoint | **Rejected** -- one owner of the loop; footprint 16 paths, no collision; a split would serialize on `dodo.py`/`conductor.py`. |
| X-I7-2 | L3 mixes surfaces | **Accepted** -- trimmed: List A, terra and Linux-first out; `[#863]` `[#912]` `[#1540]` share conductor.yml and known-reds. |
| X-I7-3 | L2 after L4 settles the route late | **Rejected** -- the agy result is already measured (F1/F2); L4 owns `dispatch.py`, L2 does not; the order stands. |
| X-I7-4 | L5 needs L6 first | **Accepted** -- L5 starts after `lane-bu-1539-transport` MERGED. |
| X-I7-5 | steel thread out of BUILD-1 | **Rejected** -- AMEND v5 moves `[#1430]` to BUILD-2 slot 1, started once L1 lands. |
| X-I8-1 | NEW-JUSTIFIED is new vocabulary | **Rejected** -- AMEND v5 L1 names it; the gate reads candidates from existing organs and refuses only NEW-where-a-candidate-exists. |
| X-I8-2 | ChallengeReceipt duplicates the ADR-111 funnel | **Rejected** -- the funnel triages audit findings; the receipt is a per-idea verdict that halts a row at INPUT_REQUIRED before any build. |
| X-I8-3 | mandatory other vendor adds availability risk | **Rejected** -- R59 independence; no reachable reviewer = INPUT_REQUIRED, never a pass. |
| X-I8-4 | discards exit status | **Accepted** -- exit is recorded in the receipt; only its requirement is dropped (X-I4-2). |
| X-I9-1 | agy-first default | **Accepted** -- no new route in L2; agy confinement goes to the operator. |
| X-I9-2 | bypass broader than needed | **Accepted** -- absolute path plus `--add-dir`. |
| X-I9-3 | declared-workspace contract | **Accepted** -- carried into common rules §8. |
| X-I10-1 | concurrency present | **Accepted** -- as X-I1-1. |
| X-I10-2 | List A false candidates | **Accepted** -- List A STOP, INPUT_REQUIRED. |
| X-I10-3 | Linux-first row premature | **Accepted** -- not filed. |
| X-I11-1 | fake-agy cannot prove the auth flow | **Accepted** -- official docs read: CLI prints a URL, the browser shows a code, the operator pastes it back; L4 needs a return channel. |
| X-I11-2 | protocol before code | **Accepted** -- protocol taken from antigravity.google/docs/cli/install, 2026-10-15. |
| X-I11-3 | synchronous wait in an unattended lane | **Accepted** -- bounded file-observed wait, at most 10 min. |
| X-I11-4 | cleanup not proven | **Accepted** -- L4 Done-contract 4 kills the auth tree on timeout. |
| X-I12-1 | no R103 | **Accepted** -- `[#1538]` lands by id; R103 recorded absent. |
| X-I12-2 | register says no R100 | **Accepted** -- R100 exists at RATIFICATION-2026-10-13:42; L5 corrects the register line. |
| X-I12-3 | superseded-only sources | **Accepted** -- each id cites its own source file. |
| X-I12-4 | boot claims ahead of code | **Accepted** -- boot teaches only mechanisms on main; others "pending [#id]". |
| X-I13-1 | L6 mostly built | **Accepted** -- L6 extends `transport.py`; M5. |
| X-I13-2 | inbox duplicates `query` | **Accepted** -- `query` gains `--since`; no new command. |
| X-I13-3 | in-place status edits break immutability | **Accepted** -- status derived from answer records. |
| X-I13-4 | janitor --apply on Drive | **Accepted** -- only with an operator-reviewed `--expect-manifest`. |
| X-I13-5 | INDEX trigger fails open | **Accepted** -- writers bypass it; INDEX measured 375,536 B stale; L6 owns the fix. |
| X-I13-6 | L6 conflates acts | **Rejected** -- AMEND v5 defines L6 as one lane; 7 disjoint paths; the destructive act stays operator-gated. |

## EVAL2 - Grok

| id | topic | response |
|---|---|---|
| G-I1-1 | Linux-first worse | **Accepted** -- conclusion only; its premise "path-filtered Windows" is false: the matrix runs windows-latest per change (`conductor.yml:100-107`). |
| G-I1-2 | terra removal redundant | **Accepted** -- terra kept. |
| G-I2-1 | no duplicate ruff | **Accepted** -- as X-I2-1. |
| G-I2-2 | no plugin copy exists | **Rejected** -- `plugins/tier1-lifecycle/scripts/validate_backlog.py` exists (probe below). |
| G-I2-3 | census already in the registry | **Rejected** -- they are asserted negative probes, not registry duplicates. |
| G-I2-4 | terra dead | **Rejected** -- report-only by design and test-pinned, not dead. |
| G-I3-1 | --add-dir suffices | **Accepted** -- as X-I3-1. |
| G-I3-2 | routing already Copilot-first for reads | **Rejected** -- the registry reads agy -> Copilot -> Sonnet (`provider-registry.yaml:776-804`). |
| G-I4-1 | distiller redundant | **Accepted** -- extend `gen_lane_contract distill`; `learning_distiller.py` distils refusals and is not reused for this. |
| G-I4-2 | payload completion already built | **Rejected** -- `conductor.py` has no psutil or tree kill (probe: 0 matches); the kill lives in `bounded_hook.py`. |
| G-I5-1 | R115 already in STANDING_RULINGS | **Rejected** -- 0 matches for R115 there; line 4868 is about another lane. |
| G-I5-2 | R100/R103 contradictions | **Accepted** -- as X-I12-1/X-I12-2. |
| G-I6-1 | e already chosen, psm locked | **Rejected** -- psm is not in `uv.lock`; M4 picks a. |
| G-I6-2 | pydantic already used | **Accepted** -- as X-I6-2. |
| G-I7-1 | lane split contradicts the AMEND | **Rejected** -- the six lanes are the AMEND's own, with the dependency fixes above. |
| G-I7-2 | L6 duplicates transport | **Accepted** -- L6 extends existing transport code. |
| G-I8-1 | DistillReceipt etc. already exist | **Rejected** -- `learning_distiller.py` has no DistillReceipt (0 matches); composition of existing organs is kept. |
| G-I9-1 | bypass route vs Copilot-first | **Rejected** -- premise false (G-I3-2); L2 adds no route either way. |
| G-I10-1 | L3 additions redundant | **Accepted** -- as X-I10-1/X-I10-2. |
| G-I11-1 | L4 duplicates R110 code | **Rejected** -- no code returns the sign-in code to a remote prompt today; L4 builds it. |
| G-I12-1 | L5 duplicates [#1450] | **Rejected** -- L5 is the carrier of `[#1450]` and `[#1538]`; not a duplicate. |
| G-I13-1 | L6 redundant | **Accepted** -- in part: built on existing transport; the gaps of M5 remain. |
| G-I13-2 | janitor/index partly built | **Accepted** -- same as X-I13-1. |

## Subagent claims

- concurrency with cancel-in-progress exists in conductor.yml {probe: grep -c 'cancel-in-progress' .github/workflows/conductor.yml}
- pytest runs on ubuntu-latest and windows-latest per change {probe: grep -c 'windows-latest' .github/workflows/conductor.yml}
- ADR-127 states standard runners are free for a public repo {probe: docs/decisions/ADR-127-ci-os-verification.md:14}
- the repo is PUBLIC (gh repo view, 2026-10-15) {unverified}
- one ruff hook only {probe: grep -c '- id: ruff\s' .pre-commit-config.yaml}
- the plugin validate_backlog twin exists {probe: grep -c 'def ' plugins/tier1-lifecycle/scripts/validate_backlog.py}
- aider/llm/amp are asserted absent by a test {probe: grep -c 'aider' tests/test_provider_bench.py}
- read_gate passes the agy bypass flag {probe: grep -c 'dangerously-skip-permissions' scripts/read_gate.py}
- registry read route is agy then Copilot then Sonnet {probe: grep -c 'read / scan -> agy -> Copilot' ecosystem/provider-registry.yaml}
- agy wrote outside its workspace in 2026-09 {probe: docs/audits/2026-09-05-technical-627-readjudication.md:300}
- transport write trigger exists and fails open {probe: scripts/transport.py:982}
- dodo stage subprocess has no timeout today {probe: scripts/dodo.py:302}
- doit halts on a failed dependency via task_dep {probe: grep -c 'task_dep' scripts/dodo.py}
- agy sign-in pastes a browser code back into the remote prompt (antigravity.google/docs/cli/install) {unverified}
- R100 heading in RATIFICATION-2026-10-13.md:42; no R103 heading anywhere (transport files) {unverified}
