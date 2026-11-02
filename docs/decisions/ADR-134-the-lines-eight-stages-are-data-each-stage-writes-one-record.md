# ADR-134: The line's eight stages are data — four are contract phases, four are moments, and each stage writes one record a landing check reads

- **Status:** Accepted (ADR-94; ratified: to-cc/GO-E3.1.md (operator, 2026-11-01))
- **Date:** 2026-11-01
- **Origin:** /decide run E31-D, revision 3; challenged by CC (R41, 2026-11-01); ratified in `to-cc/GO-E3.1.md` (= `to-browser/RATIFICATION-2026-11-01.md`).
- **Numbering:** PROPOSAL-ADR-STAGE-PHASE = ADR-134, PROPOSAL-ADR-GIT-MEMORY = ADR-135, PROPOSAL-ADR-BROWSER-SURFACE = ADR-136, PROPOSAL-ADR-READ-FORMAT = ADR-137, ADR-124 stays ADR-124. Where the text below names a proposal, read its ADR number.
- **Decision tier:** Path A — operator ratification.
- **Amends:** ADR-130 D1 (where the phase table comes from, and its models). **Disposes:** ADR-130 D6, which GO-E3.0 R1 sent to E3.1.
- **Depends on:** nothing open. GO-E3.0 R11 is in `ecosystem/provider-registry.yaml` since e30-bootstrap (7993b70a9): the judge order starts with gpt-6-sol (`:1075`).
- **Uses:** [#1689] (phases from the contract), [#1687] (served model in every receipt), GO-E3.0 R9 (the UNVERIFIED class).
- **Source:** plan r3 §3 (transport `to-cc/PLAN-NEXT-2026-10-30.md:40-51`); `ecosystem/harness.yaml@689a537e5:181-189`; `scripts/subst_gate.py:109-117`; `ecosystem/schema/phase_receipt.py:162-196`; `scripts/conductor.py:791,1043`; research brief D.

## Context

The plan names eight stages; the conductor runs seven phase rows (P6 has two). Measured on main c6618dbb7 (revision 2), re-measured on main 13023da42 (revision 3):
- Stages 1 (sign-off), 7 (land) and 8 (used) have no phase. `sign-?off` has 0 matches in harness.yaml.
- Stage 2's distiller is not a phase. P1 `spec` writes a second spec from an already-frozen contract. C-SCOPE refuses a lane without a P1 payload (`scripts/conductor.py:791`).
- Stage 3 RED is P2 on `claude`/`claude-sonnet-5-5`. R11 says Copilot T1 on `gpt-6-luna`.
- Stage 6's judge is P7 on `claude-opus-5-5`. P7 reads "every receipt and payload in {round_dir}". The registry's `judge` order is gpt-6-sol first since e30-bootstrap (`:1075`); its `description:` still names R104's Opus (`:1070`).
- P3 implement and P5 qa run Copilot `claude-sonnet-5.5` (`harness.yaml:186`, `:188`). R11: Sonnet implements through `claude`; T2 runs `gpt-6-luna`.
- `harness.yaml:12` already holds a `stages:` key: the spine's eight contract-preparation stages (kind-subject to provider-model-version). A second block cannot share the name.
- A Copilot `--usage-output-file` carries no session id; the id is the `~/.copilot/session-state/` folder created at the file's start time.
- P6b `review-grok` has `model: null`, so declared == served cannot be evaluated.
- P4 constraints is mandatory (ADR-130 D4) and has no plan stage.
- subst_gate's `_PHASE_RULES` maps role words. Of the harness phase names, 5 of 8 (spec, constraints, qa, review-grok, judge) map to no rule and are refused at `:289`.
- `PhaseReceipt` v1 has 24 fields, with no session id. It embeds its payload, `detail` included (`:195`).
- No record type exists for a moment stage.
- [#1689] has landed (13023da42): `contract_phases()` reads a contract's `## Phases` (`scripts/conductor.py:1148`).

## Decision

**D1. Stages are a data block.** `ecosystem/harness.yaml` gains `line_stages:` (not `stages:`, the spine's key at `:12`), one row per plan stage: `{stage, name, kind: phase|moment, carrier, phases, record, complete_when}`.

| stage | kind | carrier | model | complete when |
|---|---|---|---|---|
| 1 sign-off | moment, pre-launch | sign-off generator + `go_reader` at pre-launch | Opus writes, operator signs | GO file present for the batch |
| 2 spec + prompt evaluation | moment, pre-launch | `gen_lane_contract.py distill` | Opus | contract frozen + distiller verdict READY |
| 3 RED | phase P2 | Copilot T1, own session | `gpt-6-luna` | P2 receipt + RED sha + CI run on it concluded failure |
| 4 implement | phases P3 then P4 | CC; deterministic constraints | `claude-sonnet-5-5`; none | P3 receipt AND a separate P4 PASS receipt |
| 5 two reviews | phases P6a, P6b | Codex; Copilot | `gpt-5.6-terra`; `gemini-4-argon` (a family other than the implementer's and review 1's; fallback `gpt-6-luna`; last resort per H-Q2; Grok only per case) | both receipts on the final tip |
| 6 isolated evaluation | phases P5 then P7 | T2 Copilot run on CI at the exact SHA; judge | `gpt-6-luna`; `gpt-6-sol` (UNVERIFIED, R9) | P5 success AND P7 ACCEPT |
| 7 land | moment, merge | `land_lane.py` via the integrator | Sonnet integrator | merge receipt |
| 8 used | moment, post-merge | the consumer named in the sign-off | code | usage witness recorded |

**D2. The contract carries the phases** ([#1689], landed 13023da42). The harness `phases:` block is the default only for a contract that declares none. P1 leaves a distilled contract only after C-SCOPE (`conductor.py:791`) and the P2/P3 prompts read the frozen contract instead of the P1 payload (Q-D1). Phase models come from the registry roles, where R11 now stands.

**D3. Stage 6 has a defined input view (Q-D2).** One input builder gives P7: the contract, `git diff <base>..<tip>` (the diff only, no commit messages), the P5 (T2) receipt, and the P6 reviewer receipts reduced to `outcome` + `findings`. It never gives a payload's `detail`, the P3 payload, a HANDBACK, LANE-END or SESSION text, or a transcript: nothing the producer wrote about its own work. Every adjudication of a reviewer finding, inside P7 or outside it, is built by the same builder (E3.0 night defect 9: an adjudication carried the lane's description of its code instead of the diff). A test pins the redaction. P7's (provider, session) differs from those of stages 3-5.

**D4. One record per stage, with sessions.**
- `PhaseReceipt` gains `session_id` (v2), read from the CLI's own record where one exists, otherwise `UNVERIFIED`.
- A moment stage writes a `StageRecord`: stage, artifact sha, session_id, declared model, served model or `UNVERIFIED`, ts.
- A two-phase stage (4, 5, 6) is complete when its `complete_when` holds over its phase receipts. Its StageRecord lists their shas.
- `land_lane` refuses a merge whose stages 1-6 are incomplete (E3.1 build). Stage 8's record makes the row DONE.
- The role-overlap check reads `(provider, session_id)`. Two different providers are separate by construction; within one provider both session ids must be verified and differ, and `UNVERIFIED` there is a refusal. Copilot's id is its session-state folder.

**D5. ADR-130 D6 is ratified as written:** "dynamic workflows stay audit-only". No stage of the line runs inside a dynamic workflow. No exception is claimed.

## Quality attributes

- **Quality attribute(s):** traceability (code can count a record for every stage), isolation (stage 6 provably separate, both by session and by input view), conformance (the routed models in force as data, not prose).
- **Scenario:**
  - **Source:** the conductor and land_lane on the E3.2 pilot.
  - **Stimulus:** a lane reaches the integrator for landing.
  - **Artifact:** the PhaseReceipts (v2) and StageRecords under `logs/receipts/LANE-<slug>/`.
  - **Environment:** E3.1 built; E3.0's L1 ([#1689], landed) and L2 ([#1687]) landed.
  - **Response:** land_lane evaluates each stage's `complete_when` from data, refuses on an incomplete stage 1-6, and the role-overlap check passes on session ids.
  - **Response measure:** on the pilot:
    - 8 of 8 stages are complete by their rule (baseline: 0 StageRecords);
    - P7's (provider, session_id) differs from those of P2, P3, P6a and P6b;
    - the judge-input test shows no `detail` key;
    - every phase record's declared model equals its served model or reads UNVERIFIED.
- **Decision evidence:** the Context measurements; the matrix; codex gpt-6-sol and grok-4.7 records (17 findings, all accepted).

## Consequences

E3.1 builds:
- the `stages:` block;
- `PhaseReceipt` v2 with `session_id`, and `StageRecord`;
- the judge-input builder and its test;
- the stage-completion check in land_lane;
- the role-overlap check;
- C-SCOPE and the P2/P3 prompts re-pointed to the frozen contract;
- the harness P2, P3, P5, P6b and P7 defaults changed to the routed models (P6b becomes `review-copilot` on `gemini-4-argon`);
- the registry: a copilot-enterprise `gemini-4-argon` review entry admitted on served evidence (R82; served once, `DIGEST-E3-0-GROK-SPEND-2026-11-01.md` section 4), and the judge `description:` re-pointed to R11.

`subst_gate._PHASE_RULES` gains role rules, not names: `spec` → plan/orchestrate, `qa` → test, `judge` → judge; `review-copilot` already maps (`scripts/subst_gate.py:111`). `constraints` is exempt as deterministic.

M1 becomes a count of complete stages.

The `## Phases` schema [#1689] landed is reused unchanged.

## Flip-condition

- If on the pilot the judge, given the redacted view, issues a verdict that a later evaluation with the full payloads overturns (witnessed, recorded), D3's input view is reopened.
- ADR-130's own flip applies unchanged to the phase chain (`docs/decisions/ADR-130-the-outer-loop-runs-in-code.md:50`). This ADR adds none for it.
- If Claude Code dynamic workflows gain cross-session resume and per-agent receipts, D5 is reopened.
- If [#669]'s row machine lands before E3.1's build (R109 D-2 lets it proceed without [#664]), the moment stages move into it.

## Alternatives considered

- **S0, status quo** (harness P1-P7, stages as prose). Rejected:
  - 3 stages have no phase;
  - P2, P3, P5 and P7 contradict R11;
  - moments have no record;
  - isolation cannot be checked.
- **S1, eight conductor phases.** Rejected:
  - the conductor runs inside the lane worktree;
  - land is the integrator's (GO-E3.0 C2);
  - `used` happens after the merge.
- **S2, mapping in the ADR only; contract phases, no `stages:` block.** Ties S3 in the matrix. Not recommended: stages 1, 2, 7 and 8 get no record, so M1 cannot be counted by code for them.
- **S4, wait for [#669]'s row state machine.** Rejected: [#669] has not started. Its depends-on still names [#664] (`tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md:9`), although R109 D-2 lifts the wait (`protocols/STANDING_RULINGS.md:6707`). Waiting is unbounded either way.

---

## Evidence

Weights: fidelity=25 isolation=20 buildability=20 observability=20 modifiability=15
| Option | fidelity | isolation | buildability | observability | modifiability | Σ |
|---|---|---|---|---|---|---|
| S0 status quo | 1 | 1 | 3 | 2 | 2 | 1.75 |
| S1 eight phases | 3 | 2 | 1 | 3 | 2 | 2.25 |
| S2 mapping prose | 3 | 3 | 4[^1] | 2 | 3 | 3.00 |
| S3 stages as data | 3 | 3 | 3 | 3 | 3 | 3.00 |
| S4 wait for 669 | 2 | 2 | 1 | 3 | 3 | 2.15 |

[^1]: measured -- `git grep -c -E 'Phases|--contract' c9cec3f28 -- scripts/conductor.py` = 22 on the lane branch, 0 on main c6618dbb7.

Scoring notes:
- fidelity: how many of the 8 stages keep their routed model and gate;
- isolation: stage 6 separation enforceable by code;
- buildability: E3.1 effort, given what exists;
- observability: M1 computable from records;
- modifiability: a stage change is a data edit.

Revision 1 scored S3 observability 4 on a proposed table; both evaluators refused that as unmeasured (SPC5, SPG2), so it is 3 here.

### Pre-mortem

- The `stages:` block could drift from a contract's `## Phases`. Mitigation: the check reads phase ids from the contract and only moment rows and completion rules from harness.yaml.
- Session ids prove different sessions, not different context. D3's view limits the inputs; Q-D2 asks about `findings`.
- R9 accepts UNVERIFIED for Codex, so a served == declared check passes vacuously on every Codex record.
- Q-D3 is ruled and already data; the stale judge `description:` is the only residue (Consequences).
- The stage-5 Copilot review model is not yet admitted for review in the registry; until that row lands, review 2 runs as a recorded hand step.

## Subagent claims

- harness.yaml already holds the spine's stages key {probe: ecosystem/harness.yaml:12}
- P3 implement runs copilot {probe: ecosystem/harness.yaml:186}
- P5 qa runs copilot {probe: ecosystem/harness.yaml:188}
- contract_phases reads a contract's Phases section on main {probe: scripts/conductor.py:1148}
- a copilot review phase rule exists {probe: scripts/subst_gate.py:111}
- the judge description still names R104 {probe: ecosystem/provider-registry.yaml:1070}
- ADR-130 is Proposed {probe: docs/decisions/ADR-130-the-outer-loop-runs-in-code.md:3}
- D6 reads "dynamic workflows stay audit-only" {probe: grep -c 'dynamic workflows stay audit-only' docs/decisions/ADR-130-the-outer-loop-runs-in-code.md}
- P7 judge reads every receipt and payload (true at 689a537e5; the P7 row was rewritten on main since) {unverified}
- P6b grok has model null (true at 689a537e5:189; the P6 rows were rewritten on main since) {unverified}
- the subst_gate phase grammar ends at 117 {probe: scripts/subst_gate.py:117}
- a phase row the gate cannot judge is refused {probe: scripts/subst_gate.py:300}
- PhaseReceipt embeds the payload at 195 {probe: ecosystem/schema/phase_receipt.py:195}
- C-SCOPE reads the P1 payload {probe: scripts/conductor.py:791}
- run_round is the round runner {probe: grep -c 'def run_round' scripts/conductor.py}
- the registry judge order starts with gpt-6-sol, R11 {probe: ecosystem/provider-registry.yaml:1075}
- [#1689]'s Done-when reads phases from the contract {probe: tasks/1689-conductor-phase-table-disagrees-with-the-lane-contract-p5.md:12}
- [#669] still names #664 {probe: grep -c '664' tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md}
- R109 D-2 lets [#669] proceed without waiting {probe: protocols/STANDING_RULINGS.md:6707}
- Workflow resume is same-session only (this session's Workflow tool schema, `resumeFromRunId`) {unverified}

## Evaluator records

Unchanged and verbatim in revision 2, `to-browser/PROPOSAL-ADR-STAGE-PHASE-2026-11-01.md` (sessions, nonces, served models, every finding id). Revision 3 was not re-sent to the evaluators: its changes come from CC's R41 challenge and the operator's rulings of 2026-11-01, listed in the Revision 3 section below.

## Response table

| id | objection (short) | response |
|---|---|---|
| SPC1 | dropping P1 breaks C-SCOPE and P2/P3 | **Accepted** -- D2: P1 leaves only after C-SCOPE and the P2/P3 prompts read the frozen contract; Q-D1 |
| SPC2 | no session field in PhaseReceipt v1 | **Accepted** -- D4: PhaseReceipt v2 gains session_id; the overlap check reads it |
| SPC3 | receipts embed payload.detail | **Accepted** -- D3: a judge-input builder with a redaction test |
| SPC4 | registry judge is Opus | **Accepted** -- Q-D3 and "Depends on" line; D1's judge cell conditional on the ruling |
| SPC5 | S3 observability 4 unmeasured | **Accepted** -- lowered to 3; the matrix now ties S2/S3 at 3.00, recorded |
| SPC6 | two-phase stages underspecified | **Accepted** -- D1 `complete_when` column, D4 aggregation rule |
| SPC7 | flip 1 does not test soundness | **Accepted** -- flip 1 now needs a witnessed overturned verdict |
| SPG1 | judge role is Opus in repo | **Accepted** -- same change as SPC4; no registry rewrite claimed from the transport |
| SPG2 | footnote 2 not a measurement | **Accepted** -- footnote removed, score 3 |
| SPG3 | name the session field | **Accepted** -- `session_id` on PhaseReceipt v2 and StageRecord |
| SPG4 | D5 exception is an amendment | **Accepted** -- exception removed; D6 ratified as written |
| SPG5 | which text binds for #669 | **Accepted** -- S4 cites both; R109 D-2 binds, and the wait is unbounded either way |
| SPG6 | P4 hidden inside implement | **Accepted** -- stage 4 completes only with a separate P4 PASS receipt |
| SPG7 | subst_gate needs role rules | **Accepted** -- Consequences now names the role rules |
| SPG8 | flip 2 unobservable | **Accepted** -- replaced by a pointer to ADR-130:50 |
| SPG9 | plan claims unverifiable here | **Accepted** -- plan citations marked as transport; the sign-off count is noted as true |
| SPG10 | footnote 1 half unverifiable | **Accepted** -- re-measured on the local branch ref c9cec3f28: 22 vs 0 |

## Revision 3 - CC's R41 challenge (2026-11-01, on main 13023da42) and what changed

Every revision-2 finding was accepted (17/17); R41 looked hardest where nothing was defended.
- SP-R1 (stale base): the judge order is already gpt-6-sol first (`ecosystem/provider-registry.yaml:1075`, e30-bootstrap). "Depends on" closed; Q-D3 recorded as ruled; the stale `description:` (`:1070`) moved to Consequences.
- SP-R2 (name collision, undefended): `harness.yaml:12` already holds `stages:` (the spine's eight stages). Neither evaluator saw it. D1's block is `line_stages:`.
- SP-R3 (incomplete): P3 and P5 run Copilot `claude-sonnet-5.5` (`harness.yaml:186`, `:188`), which also contradicts R11; revision 2 named only P2, P6b, P7. Consequences and S0 now list all five.
- SP-R4 (stale): [#1689] landed at 13023da42 (`scripts/conductor.py:1148`); the "main has 0" bullet is replaced.
- SP-R5 (vacuous check): a Copilot usage file has no session id, so a session-only overlap check reads every Copilot RED as UNVERIFIED. D4 judges (provider, session).
- SP-R6 (operator ruling Q-D2): the judge input is diff + reviewer findings + T2 results; no producer prose, no commit messages; adjudications use the same builder (night defect 9). This matches the registry's own judge text (`:1070-1071`, "never the implementer's report").
- SP-R7 (operator review routing, 2026-11-01): stage 5 = Codex terra + Copilot gemini-4-argon (Google; in Copilot's CAPI catalog by the 2026-11-01 probe; served once). Fallback gpt-6-luna. The ruled last resort "Sonnet in a new isolated session" is held: `scripts/provider_router.py:283` refuses a reviewer of the producer's provider (`excludes_producer: true`, `ecosystem/provider-registry.yaml:824`). See H-Q2 in `to-browser/DIGEST-E3-1-SIGNOFF-2026-11-01.md`.
- Matrix unchanged: none of the above moves a score; the S2/S3 tie and its reason stand.

## Amendment 2026-11-02 (architect ruling Q-L0-2)

The decision text above is unchanged; only this block was added. The ruling is `to-browser/DIGEST-RULINGS-MORNING-2026-11-02.md` (row Q-L0-2, S-2), taken on the lane question in `to-browser/QUESTION-E3.1-2026-11-01-e31-decide-v3-text-defects.md`.

- **Consequences' `stages:` means D1's `line_stages:`.** D1 governs: `ecosystem/harness.yaml:12` already holds the spine's `stages:` key, and the new block is `line_stages:`. A build lane cites `line_stages:`.
- **D1's table, with its `model` column, is the field authority.** The D1 prose that lists the row fields without `model` is read against that table.
- The `Numbering:` header line stays as written. It is a header, not decision text.
- **Locators re-pointed (architect ruling Q-L0-4 = A', `to-browser/DIGEST-RULING-Q-L0-4-STALE-LOCATOR-2026-11-02.md`).** Main moved `scripts/conductor.py` and `ecosystem/harness.yaml` after this ADR was drafted, so its `path:line` locators were re-pointed to the same lines and two claims about rewritten rows were marked `{unverified}` with the sha they were true at. No decision text changed.
- This marker touches a ratified ADR by marker only, so it is reported to the operator in the next ratification package.
