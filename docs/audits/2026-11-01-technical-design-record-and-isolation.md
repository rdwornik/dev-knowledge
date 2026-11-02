# Design: the record and isolation (E3.1 /decide, run e31-i)

- **Run date:** 2026-11-01
- **Producer:** claude-opus-5-5 (this seat); research subagents claude-sonnet-5-5 (read-only, four in parallel)
- **Rows:** [#1047] (closed failure taxonomy), [#625] (standing eval set, read for overlap), row 1837 (`tasks/1837-decide-independent-adjudication-as-code.md:3`) (/decide independent adjudication, filed separately; not designed here)
- **Input:** the three transport digests, read in full: DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md (166 lines), DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md (119 lines), DIGEST-AJ-P9-REVIEW-2026-11-01.md (53 lines). Scope as ruled in GO-E3.1 section 2, "AJ H7" (AJ proposals 3, 7, 9 and 11 for this run); not reopened.
- **Output:** docs/decisions/ADR-138-the-record-is-revision-bound-and-isolation-is-measured.md at status Proposed. Nothing is built.

## Brief

Question: how should the harness (a) classify a failure in ONE closed taxonomy, (b) bind an approval verdict to the exact revision it judged and freeze a lane contract by hash, refusing a contract write after its freeze, (c) measure the rubber-stamp rate of approvals against an adjudicated key, and (d) measure the independence of two readers as a computed number with a threshold?

Known constraints (no answer pre-committed):
- ADR-134 (Accepted) already decides stage records, session_id, the judge-input builder and role overlap by (provider, session_id); ADR-121 (Proposed) decides verdict identity (D5) in an event log that does not exist; ADR-122 (Accepted) makes tasks typed records. Reuse first; say what each of (a)-(d) adds.
- The inputs, by line: proposal 3 is DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:36; proposal 7 is DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:40 (S-03 rejected there: the nonce proves the payload was read, not that the landed tree is the reviewed tree); proposal 9 is DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:42 (key first, then rate; 13/36 reversals are disagreement, not rubber-stamping); the independence lesson is DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:24 (agy not confined by --add-dir; quote-Jaccard caught a copy defect; census maximum 0.36) and DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:123 (target Jaccard 0.324, record Jaccard 0.0, threshold 0.5; M04 quote-Jaccard 0.106).
- No code is changed by this run; the build is a later lane after ratification.

Sub-questions fanned out: Q1 failure taxonomy; Q2 verdict identity and contract freeze; Q3 approval quality; Q4 measured independence.

## Subagent briefs

Each brief is copied verbatim from the file the subagent was sent (C:\Users\1028120\.claude\jobs\05d3b2bf\tmp\briefs-e31-i\brief-N.md); `decide_checks subagent-exclusions` over the four files: 0 defects.

### Brief 1

```text
CONTEXT: a design decision on how the .dev-knowledge harness should classify a FAILURE (a lane, gate or run failure) into ONE closed taxonomy. Nothing is being built.

SUB-QUESTION 1 (failure taxonomy): (a) find backlog row [#1047] under tasks/ (grep -l '1047' tasks/) and quote its title and its acceptance lines; (b) does any closed enum of failure classes already exist in scripts/, ecosystem/ or ecosystem/schema/ (grep -n for 'failure_class', 'FailureClass', 'failure_kind', 'Literal\[' near fail, 'verdict', 'known_reds', 'red_class')? For each hit give the enum members; (c) what fields does ecosystem/schema/phase_receipt.py carry for an outcome/failure (status, reason, verdict); (d) does docs/decisions/ADR-134-*.md define a stage record with an outcome/failure field (quote the line); (e) does docs/decisions/ADR-122-*.md (tasks are typed records) define a typed failure field?

EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit, pytest, or any writer.

OUTPUT: at most 450 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. The line cited must contain the thing claimed. A finding you cannot give a probe for (e.g. an absence) ends in {unverified} with your own count stated. Facts only, no recommendation, no design. Repo root = C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\e31-decide (a git worktree); cite repo-relative paths with forward slashes.
```

### Brief 2

```text
CONTEXT: a design decision on binding an approval verdict to the exact revision it judged, and freezing a lane contract by hash with a refusal to write a contract after its freeze. Nothing is being built.

SUB-QUESTION 2 (verdict identity and contract freeze): (a) quote decision D5 of docs/decisions/ADR-121-*.md (verdict identity) with line numbers and its status line; (b) read ecosystem/harness.yaml lines 170-200 and report what lines 178-180, 187 and 189 say (a challenger claimed "the base binding is partly present (harness.yaml:187, :178-180)"); (c) in scripts/subst_gate.py and scripts/conductor.py, find any sha/hash/digest of a contract, a reviewed revision (head sha, tree sha, base sha), a nonce, or a freeze (grep -n 'sha256\|hashlib\|nonce\|tree_sha\|head_sha\|frozen\|freeze'); (d) in ecosystem/schema/phase_receipt.py, which fields identify a revision or a contract hash; (e) does docs/decisions/ADR-134-*.md bind a stage record to a session_id and a revision (quote); (f) does any script refuse to write a contract file that already exists or is frozen (grep -rn 'frozen\|already frozen\|refuse' scripts/*contract* scripts/lane_contract* 2>/dev/null)?

EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit, pytest, or any writer.

OUTPUT: at most 450 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. The line cited must contain the thing claimed. A finding you cannot give a probe for (e.g. an absence) ends in {unverified} with your own count stated. Facts only, no recommendation, no design. Repo root = C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\e31-decide (a git worktree); cite repo-relative paths with forward slashes.
```

### Brief 3

```text
CONTEXT: a design decision on MEASURING the rubber-stamp rate of approvals (reviewer approvals / plan-review PASS verdicts) against an adjudicated key. Nothing is being built.

SUB-QUESTION 3 (approval quality): (a) find backlog row [#625] (standing eval set) under tasks/ and quote title and acceptance lines; (b) does any verdict ledger, approval log or reviewer-verdict record exist (grep -rln 'verdict' scripts/ ecosystem/ logs/*.jsonl | head; name files that APPEND verdicts and their fields); (c) does any script compute an approval rate, an agreement, a kappa, or a precision against a key (grep -rn 'kappa\|cohen\|agreement\|approval_rate\|rubber' scripts/)? (d) what does .claude/commands/decide.md and scripts/decide_checks.py record about evaluator findings and the Accepted/Rejected response table (which check, which function, line); (e) does ADR-134 (docs/decisions/ADR-134-*.md) define a judge-input builder or a judge record (quote lines)?

EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit, pytest, or any writer.

OUTPUT: at most 450 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. The line cited must contain the thing claimed. A finding you cannot give a probe for (e.g. an absence) ends in {unverified} with your own count stated. Facts only, no recommendation, no design. Repo root = C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\e31-decide (a git worktree); cite repo-relative paths with forward slashes.
```

### Brief 4

```text
CONTEXT: a design decision on MEASURING the independence of two readers (two model families reading the same sources) as a computed number with a threshold (quote-Jaccard over quoted spans, finding-Jaccard over finding targets). Nothing is being built.

SUB-QUESTION 4 (measured independence): (a) grep -rni 'jaccard' scripts/ tests/ ecosystem/ and list every hit with what it computes; (b) does docs/decisions/ADR-134-*.md define role overlap by (provider, session) or any independence check (quote lines); (c) does scripts/decide_checks.py check evaluator independence (excludes_producer) and how (function, line); (d) is there any recorded fact in the repo that agy (Gemini CLI) is not confined by --add-dir (grep -rn 'add-dir' scripts/ ecosystem/ docs/ .claude/ | head -20); (e) does ecosystem/provider-registry.yaml record a provider family per provider (quote a line)?

EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit, pytest, or any writer.

OUTPUT: at most 450 words. Each finding is ONE bullet ending in a probe the producer can re-run, in exactly one of these forms: {probe: <path>:<line>} or {probe: grep -c '<pattern>' <path>} or {probe: git check-ignore <path>}. The line cited must contain the thing claimed. A finding you cannot give a probe for (e.g. an absence) ends in {unverified} with your own count stated. Facts only, no recommendation, no design. Repo root = C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\e31-decide (a git worktree); cite repo-relative paths with forward slashes.
```

## Subagent claims

Each claim is one a subagent reported and the matrix or the pre-mortem relies on; the producer re-ran every probe (decide_checks subagent-claims) and read each cited line. An absence cannot be probed by a count of a present string, so it is recorded unverified with the count stated.

- Q1: row [#1047] proposes a closed 9-category root-cause enum beside severity in review_packet.py's verdict schema {probe: tasks/1047-aj-c-1-a-closed-root-cause-enum-9-category-agent-error.md:3}
- Q1: the row's done-when is the enum in review_packet.py's verdict schema, RED-first on a fixture verdict {probe: grep -c 'carries the 9-category enum beside' tasks/1047-aj-c-1-a-closed-root-cause-enum-9-category-agent-error.md}
- Q1: scripts/review_packet.py carries no severity token today; the producer's count is 0 {unverified}
- Q1: no enum named failure_class, FailureClass or failure_kind exists under scripts/ or ecosystem/; the subagent's count is 0 {unverified}
- Q1: phase_receipt.py has a closed Outcome enum (PASS, FAIL, ACCEPT, REFUSE, INPUT_REQUIRED) {probe: ecosystem/schema/phase_receipt.py:53}
- Q1: phase_receipt.py has a closed Severity enum, which grades a finding, not a cause {probe: ecosystem/schema/phase_receipt.py:54}
- Q1: PhasePayload carries outcome {probe: ecosystem/schema/phase_receipt.py:96}
- Q1: PhaseReceipt status is ok, COMPLETE, FAILED or KILLED, with no reason class {probe: ecosystem/schema/phase_receipt.py:178}
- Q1: lane_report has its own State enum including FAILED and REJECTED {probe: ecosystem/schema/lane_report.py:50}
- Q1: challenge_receipt has its own Verdict enum {probe: ecosystem/schema/challenge_receipt.py:43}
- Q1: known_reds classifies a red test into flag buckets, not a run failure {probe: scripts/known_reds.py:164}
- Q1: ADR-122's typed lifecycle fields are status, status_reason and closure, with no failure class {probe: docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md:66}
- Q2: ADR-121 D5 keys a verdict by candidate SHA, gate, baseline ID, comparison policy and execution context {probe: docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:79}
- Q2: ADR-121 is Proposed {probe: grep -c 'Status:\*\* Proposed' docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md}
- Q2: harness.yaml names the {base} placeholder and the per-spawn {payload} {nonce} {input_hash} {probe: ecosystem/harness.yaml:181}
- Q2: harness.yaml says the phase inputs are the files whose content is part of the input hash {probe: ecosystem/harness.yaml:180}
- Q2: the P5 qa row's inputs are the contract only {probe: ecosystem/harness.yaml:187}
- Q2: the P6b review prompt names the diff against {base} as a placeholder {probe: ecosystem/harness.yaml:189}
- Q2: PhaseReceipt carries input_hash {probe: ecosystem/schema/phase_receipt.py:181}
- Q2: each input carries its own sha256 (InputDigest) {probe: ecosystem/schema/phase_receipt.py:110}
- Q2: PhaseReceipt carries a nonce {probe: ecosystem/schema/phase_receipt.py:195}
- Q2: PhaseReceipt carries payload_sha256 {probe: ecosystem/schema/phase_receipt.py:197}
- Q2: PhaseReceipt has no base, head or tree sha field; the subagent's count is 0 {unverified}
- Q2: scripts/conductor.py computes no sha256, nonce or revision sha; the producer's grep count over those six names is 0 {unverified}
- Q2: conductor's only freeze is the suite-baseline freeze, keyed by a measured sha {probe: scripts/conductor.py:677}
- Q2: ADR-134's StageRecord carries stage, artifact sha, session_id, declared and served model, ts, and no revision of a judged tree {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:51}
- Q2: gen_lane_contract emit refuses an existing target unless forced {probe: scripts/gen_lane_contract.py:2367}
- Q2: gen_lane_contract distill refuses an existing target unless forced {probe: scripts/gen_lane_contract.py:2686}
- Q2: gen_lane_contract hashes the idea text, not the contract {probe: scripts/gen_lane_contract.py:2175}
- Q3: row [#625] is a rule-adherence eval corpus that must discriminate a weakened instruction set {probe: grep -c 'DISCRIMINATES' tasks/625-the-rule-adherence-eval-corpus-fresh.md}
- Q3: row [#625] mentions no adjudicated key; the producer's count of adjudicat in it is 0 {unverified}
- Q3: lane_report defines a Review verdict APPROVE or REQUEST-CHANGES {probe: ecosystem/schema/lane_report.py:118}
- Q3: read_gate appends a read-outcome ledger, not a reviewer verdict {probe: scripts/read_gate.py:320}
- Q3: merge_receipt appends the merge ledger {probe: scripts/merge_receipt.py:1216}
- Q3: no script computes kappa, an approval rate or a precision against a key; the only rubber hit is a comment {probe: scripts/fleet_health.py:106}
- Q3: decide_checks matches response rows Accepted or Rejected {probe: scripts/decide_checks.py:276}
- Q3: check_response_coverage checks coverage only and counts no accepted-to-rejected ratio {probe: scripts/decide_checks.py:279}
- Q3: decide_checks writes no ledger {unverified}
- Q3: ADR-134 lists the judge-input builder as owed work {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:79}
- Q4: the only Jaccard computations are file co-change coupling {probe: scripts/fleet_analytics.py:524}
- Q4: and BACKLOG near-duplicate titles at a 0.7 threshold {probe: scripts/validate_backlog.py:125}
- Q4: and gen_lane_contract.similarity over name tokens {probe: scripts/gen_lane_contract.py:2064}
- Q4: no code computes quote-Jaccard or finding-Jaccard between readers; the subagent's count is 0 of 11 hits {unverified}
- Q4: ADR-134 role overlap reads (provider, session_id) {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:54}
- Q4: ADR-134 records that session ids prove different sessions, not different context {probe: docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md:140}
- Q4: decide_checks' independence check is string equality of served and producer model {probe: scripts/decide_checks.py:265}
- Q4: the repo already records that --add-dir does not confine agy {probe: docs/audits/2026-08-29-technical-nb2-o-packet.md:233}
- Q4: a launch contract says to check what agy actually read {probe: docs/audits/2026-08-29-technical-batch2-wave2-launch-contracts/NB2-W2-LANE-O-A4-agy.md:52}
- Q4: the registry records that agy needs --add-dir for access, which is not confinement {probe: ecosystem/provider-registry.yaml:902}
- Q4: the registry records a model family per model {probe: ecosystem/provider-registry.yaml:1489}
- Q4: the registry already has a distinct-family rule for a role {probe: ecosystem/provider-registry.yaml:954}
- Row 1837 exists for /decide independent adjudication {probe: tasks/1837-decide-independent-adjudication-as-code.md:3}
- Evaluator round (IG2): run_phase builds every PhaseReceipt {probe: scripts/run_phase.py:240}
- Evaluator round (IG2): run_phase hashes each input file {probe: scripts/run_phase.py:435}
- Evaluator round (IG2): run_phase resolves {base} to the ref name origin/main, not a sha {probe: scripts/run_phase.py:294}
- Evaluator round (IG2): the conductor runs the doit round, it does not spawn phases itself {probe: scripts/conductor.py:902}
- Evaluator round (IG5): review_packet.py assembles context and judges nothing {probe: scripts/review_packet.py:41}
- Evaluator round (IG3): receipts are gitignored {probe: .gitignore:194}
- Evaluator round (IG3): land_lane works on origin/worktree-<slug> from an integration worktree {probe: scripts/land_lane.py:157}
- Evaluator round (IG4): the contract path is per slug, with no round {probe: scripts/gen_lane_contract.py:2366}
- Evaluator round (IG6): run_phase sets a reason on each failing run branch {probe: scripts/run_phase.py:205}
- Evaluator round (IG9): Finding has no target field {probe: ecosystem/schema/phase_receipt.py:76}
- Evaluator round (IG7): the registry has four families; the producer's count of family lines by value is anthropic 5, google 1, openai 1, xai 1 {unverified}

## Evidence and matrix

What exists, quoted from the probes above, and what each of (a)-(d) adds beyond ADR-134, ADR-121 and ADR-122:
- (a) Five closed enums already classify outcomes (Outcome, PhaseReceipt status, lane_report State, challenge Verdict, known_reds buckets); none names a cause. ADR-122 has status_reason (free text) and ADR-134's StageRecord has no outcome. Adds: one cause enum, carried by the records that already carry an outcome. [#1047]'s 9 agent-error categories are one half of it; mechanism causes (timeout, kill, quota, gate red) are the other.
- (b) ADR-121 D5 specifies the verdict key but lives in an event log that does not exist. Today a receipt binds its INPUT (input_hash over the contract file, the nonce) but not the REVISION judged: no base, head or tree sha. The contract writers refuse an existing file, but --force overrides and nothing records a frozen hash. Adds: D5's key as fields of the receipt and StageRecord now, and a freeze record a writer and the conductor check.
- (c) No ledger appends reviewer verdicts with a key; no script computes an approval rate or kappa. [#625] is a rule-adherence corpus, a different key. Adds: an adjudicated key and a false-approve rate with an interval.
- (d) ADR-134 separates sessions, not contexts (its own line 140). decide_checks compares model strings. Adds: quote-Jaccard and finding-Jaccard with a threshold, and a confinement witness for readers --add-dir does not confine.

Options. O0 status quo. O1 each of (a)-(d) as its own new organ. O2 extend the ADR-134 StageRecord and PhaseReceipt with revision-bound fields, one cause enum beside Severity, and one measure module for (c) and (d). O3 wait for ADR-121's event log. O4 one registry-driven check set (data) read by existing gates. O5 (research-added) [#1047] read literally: the enum only in review_packet.py, and (c)/(d) only as /decide checks.

Criteria. reuse: an existing organ or field over a new one. fidelity: the verdict provably judges the landed tree; the cause is one closed value. measurability: (c) and (d) yield a number with a threshold. footprint: new organs, files, gates (ADR-106, library-first). timeliness: usable before ADR-121 is ratified. modifiability: a new cause or reader pair is data.

Scores 1 to 5; a 4 or 5 needs a measured footnote on this repo this session, otherwise 3 caps.

Weights: reuse=20 fidelity=20 measurability=20 footprint=15 timeliness=15 modifiability=10

| Option | reuse | fidelity | measurability | footprint | timeliness | modifiability | Σ |
|---|---|---|---|---|---|---|---|
| O0 status quo | 3 | 1 | 1 | 4[^1] | 3 | 2 | 2.25 |
| O1 four new organs | 2 | 3 | 3 | 2 | 2 | 2 | 2.40 |
| O2 extend stage record and receipts, one measure module | 4[^2] | 3 | 3 | 3 | 3 | 3 | 3.20 |
| O3 wait for ADR-121 | 3 | 3 | 1 | 3 | 1 | 3 | 2.30 |
| O4 registry-driven check set | 3 | 2 | 2 | 3 | 2 | 3 | 2.45 |
| O5 [#1047] literal plus /decide-only checks | 2 | 2 | 2 | 3 | 3 | 2 | 2.30 |

[^1]: measured -- O0 adds nothing by construction: git status of this worktree at session start was clean and uv.lock is untouched by this run, so O0's footprint is zero new files, fields, gates or lock entries. (Revised after IG12: the first draft's footnote cited hash counts, which do not measure footprint.)
[^2]: measured -- the fields O2 extends exist today: input_hash and InputDigest.sha256 at `ecosystem/schema/phase_receipt.py:181` and `ecosystem/schema/phase_receipt.py:110`, the nonce at `ecosystem/schema/phase_receipt.py:195`, the Severity enum beside which the cause enum sits at `ecosystem/schema/phase_receipt.py:54`, the receipt builder in scripts/run_phase.py that already hashes inputs (`scripts/run_phase.py:435`) and builds every PhaseReceipt (`scripts/run_phase.py:240`), and the contract writers' existing refusal at `scripts/gen_lane_contract.py:2367` and `scripts/gen_lane_contract.py:2686`; ADR-134 D4 already owns the StageRecord shape. This measures that the extended fields and organs exist, which is what reuse scores; it does not measure integration effort (IS11).

Reading the matrix:
- After the evaluator round, O5's reuse fell to 2: review_packet.py, the module [#1047] names, has no verdict schema to extend (`scripts/review_packet.py:41`, IG5). O2 leads O4 by 0.75 and O5 by 0.90. Its only measured edge is reuse; every other O2 score is a judgment on an unbuilt design and caps at 3.
- O4 is not dropped wholesale: the cause enum's mapping table and the thresholds of (c) and (d) are data in O2 (ADR D1, D5), which takes O4's useful part.
- O3 loses on timeliness and measurability: an event log stores verdicts but measures nothing, and ADR-121 is Proposed. O2's fields are D5's key, so a later fold reads them unchanged.
- O5 meets [#1047]'s done-when but leaves PhaseReceipt and StageRecord without a cause and measures only /decide, so a lane failure stays unclassified.
- O1 multiplies organs to wire, the footprint the library-first rule weighs against.

Library-first check: stdlib statistics has no kappa and no Wilson interval; scikit-learn's cohen_kappa_score would be a new locked dependency (ADR-106) for about ten lines, so O2 hand-rolls kappa and Wilson in the measure module, recorded here so it is not relitigated. Jaccard is set arithmetic, already hand-rolled three times (claims Q4); the measure module reuses the formula and does not import those modules, which compute other things.

## M2 flips attached

- agy:G-17 on P6-7, rejected -> partly (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:64): "the base binding is partly present (harness.yaml:187, :178-180)". This run's probes confirm the partial: the input binding exists (input_hash and the nonce, `ecosystem/harness.yaml:181`, `ecosystem/schema/phase_receipt.py:181` and `ecosystem/schema/phase_receipt.py:195`) and {base} is a placeholder; the revision binding does not (no base, head or tree sha in PhaseReceipt; 0 hash calls in scripts/conductor.py). The ADR answers it in D2: it keeps the present binding and adds the missing one, so G-17 stands as a partial, not as "missing", matching DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:40 ("the binding is specified, not missing"). The harness.yaml lines have moved since the challenger's snapshot; the placeholders now sit at `ecosystem/harness.yaml:180` and `ecosystem/harness.yaml:181`.
- The /decide structure, P9 review section 3.3 (DIGEST-AJ-P9-REVIEW-2026-11-01.md:50-53): the producer answers challenges to its own work, the structure M2 measured as biased (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:83; 20 flips toward the challenger, DIGEST-AJ-P9-REVIEW-2026-11-01.md:27). The fix is row 1837 (`tasks/1837-decide-independent-adjudication-as-code.md:3`) and is not designed here. ADR-138 D6 says how its measures apply: the producer's Accepted/Rejected column is a verdict stream, measured against a blind key by D4, and the two evaluators' finding sets are a reader pair, measured by D5.
- No other M2 flip (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md:56-82) names P6-3, P6-7, P6-9 or the independence lesson; G-17 is the only one for this run.

## Pre-mortem

Assume ADR-138 was built as O2 and failed six months later. Likely causes, and what the design carries:
1. The cause enum fills with UNCLASSIFIED or a catch-all. Against: UNCLASSIFIED is written only by run_phase, after a fixed precedence (mechanism, payload, highest-severity finding) finds no source, so a receipt is always written; the UNCLASSIFIED share is a reported number, a WARN above its threshold. (Revised after IS8 and IG6.)
2. Two taxonomies drift: [#1047]'s review_packet enum and the receipt enum. Against: one Literal in ecosystem/schema/phase_receipt.py and no second copy; review_packet.py is not given one, because it judges nothing (IG5).
3. Revision binding refuses honest landings (a merge commit changes the commit sha). Against: bind the TREE sha of the reviewed tip as well as its commit; landing compares the lane tip's tree, which a --no-ff merge keeps on the second parent.
4. A re-freeze launders a contract change. Against: a re-freeze is a new StageRecord with a new round; every receipt whose contract_sha256 differs from the current freeze is stale and its stage incomplete.
5. The key is too small and a rate is quoted anyway. Against: below 30 adjudicated items the rate is NOT COMPUTED; every proportion carries a Wilson interval and kappa a seeded bootstrap interval (IS7).
6. The key inherits the bias it measures. Against: key adjudicators come from two families other than the producer's and the judged reviewer's, given only the contract and the diff (not ADR-134 D3's view, which shows the judged verdict, IG8); with four families known there is no third family for ties, so a disagreement leaves the item UNKEYED and counted, never ruled by the orchestrator (revised after IS4 and IG7; the P9 pattern at DIGEST-AJ-P9-REVIEW-2026-11-01.md:39-40 assumed three families).
7. Disagreement is misread as rubber-stamping again. Against: the rubber-stamp rate counts only approvals where the key finds a defect, never a disagreement with another reviewer (DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:42).
8. A high finding-Jaccard is read as copying when both readers found the same real defect. Against: quote-Jaccard (verbatim spans) is the copy signal; finding-Jaccard is reported beside it; both stay advisory until two batches of data confirm the threshold.
9. A reader reads outside its stage (agy). Against: a quote provenance check over the reader's inputs, the tree and the diff; a quote found only in the other reader's output is a copy defect. It cannot see unquoted reading, and says so (IS5, IG9).
10. D2's fields arrive beside ADR-134's PhaseReceipt v2 build and collide. Against: they ride the same schema bump as session_id, one version.

## Evaluator findings and responses

Evaluator records (header lines copied verbatim from each file; one em dash is written as -- to keep the file ASCII).

EVAL-i-sol.md: served-model: gpt-6-sol (UNVERIFIED, R9: the codex banner echoes the request; the model's own header line read gpt-6-astra) / attestation-source: codex exec header (model: gpt-6-sol, echo of the request) / session: 01a19857-e42a-72e0-8e41-3031790d79bd / VERDICT: DISAGREE -- the revision and freeze guarantees are not established by the specified checks, and the proposed measurements lack necessary operational definitions.

EVAL-i-argon.md: served-model: gemini-4-argon / attestation-source: copilot usage file currentModel (eval-i-argon/usage.json) / session: copilot-session-see-usage-file / VERDICT: DISAGREE -- The draft ADR contains multiple self-defeating mechanical defects verified against the worktree (the full verdict line is in the file; it names the baseline_id equality, the freeze deadlock, the gitignored receipts, the unpopulateable failure_class, the 5-family judge requirement and the false-positive confinement check).

Every finding was checked by the producer against the cited file and line before it was answered; the probes the answers rely on are in Subagent claims, "Evaluator round" bullets.

| id | objection (short) | response |
|---|---|---|
| IS1 | spawn-time tree does not prove the reviewer judged it | **Accepted** -- D2: head and tree stamped at harvest, the given diff is an input under input_hash, the payload echoes tree_sha; the ADR now says this binds what was given, not what was attended to |
| IS2 | "any" stage 5/6 receipt lets a missing review pass | **Accepted** -- D2: land_lane requires every receipt ADR-134 stages 5 and 6 require, present, complete and on the tip's tree |
| IS3 | a direct file write bypasses the freeze | **Accepted** -- D3: a write by other means cannot be prevented; it is detected at spawn (run_phase) and at land; the guarantee is restated as same-bytes, not unchangeable |
| IS4 | too few eligible families, no unkeyed rule | **Accepted** -- D4: UNKEYED (no families) and UNKEYED (disagreement), both counted |
| IS5 | quote checks cannot establish what agy read | **Accepted** (partly) -- renamed a quote provenance check with its limit stated; kept, because a copied or out-of-scope quote is a real detectable defect (AJ caught one, DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:24) |
| IS6 | finding-Jaccard empty set and line matching undefined | **Accepted** -- D5: both empty gives NOT COMPUTED, one empty 0; match = same path, lines within 3, same tree_sha; different tree shas not compared |
| IS7 | Wilson interval does not apply to kappa | **Accepted** -- D4: Wilson for proportions, a seeded bootstrap (1,000 resamples) for kappa |
| IS8 | no precedence rule for one cause | **Accepted** -- D1: mechanism, then payload top-level, then highest-severity finding (ties by id), then UNCLASSIFIED |
| IS9 | contract hash is not ADR-121's comparison policy | **Accepted** -- D2: a separate comparison_policy field (comparator id and version); contract_sha256 kept apart |
| IS10 | /decide rows lack stable ids and revision links | **Accepted** -- in full after the blind re-ruling (was partly): D6 now specifies adr-sha256/evidence-sha256 links, the key (run-id, evaluator file sha256, finding id), grouped rows UNKEYED, join only on equal hashes |
| IS11 | reuse 4 measures existence, not integration effort | **Accepted** (partly) -- footnote 2 now says it measures existence, which is what reuse scores; the score stays 4 because the fields and run_phase's hashing are measured present, and integration effort is not a criterion |
| IG1 | baseline_id equality refuses every merge | **Accepted** -- D2: baseline_id and comparison_policy compared only among receipts that carry one; absent rather than NONE |
| IG2 | run_phase, not the conductor, spawns and hashes; spawn-time stamp is wrong tree | **Accepted** -- verified `scripts/run_phase.py:240`, `scripts/run_phase.py:294`, `scripts/run_phase.py:435` and `scripts/conductor.py:902`; D2/D3 now name run_phase, stamp at harvest and resolve {base} to a sha; claims added |
| IG3 | gitignored receipts are not where land_lane reads | **Accepted** -- verified `.gitignore:194` and `scripts/land_lane.py:157`; D2 names the carrier, a read-only sibling read of the lane worktree's receipts (ADR-133 ruling, ADR-134's artifact), refuses when absent; flip to merge trailers |
| IG4 | round-less contract path deadlocks a re-freeze | **Accepted** -- verified `scripts/gen_lane_contract.py:2366`; D3: freeze keyed by (lane, round), a --refreeze flag writes round + 1 and stales old receipts |
| IG5 | review_packet.py has no verdict schema | **Accepted** -- verified `scripts/review_packet.py:41`; D1 leaves review_packet unchanged and asks the operator whether [#1047] is met in phase_receipt; O5 reuse 3 to 2, total 2.30 |
| IG6 | required failure_class has no deterministic source | **Accepted** -- D1: run_phase derives it by fixed precedence from its own run branches (`scripts/run_phase.py:205`) and writes UNCLASSIFIED itself; a payload top-level field added |
| IG7 | four families leave no tie-breaker | **Accepted** -- producer count anthropic 5, google 1, openai 1, xai 1; D4 drops the third-family tie-break for UNKEYED (disagreement); open question 3 restated |
| IG8 | D3 view leaks the judged verdict; lane_report and /decide lack a tree | **Accepted** -- D4: key view is contract + diff only; lane_report Review out of scope; /decide handled as a report in D6 with shas owed to row 1837 |
| IG9 | inputs list only the contract; Finding has no target; delimiters undefined | **Accepted** -- verified `ecosystem/schema/phase_receipt.py:76`; D5: legitimate sources include tree and diff, optional Finding.target, quotes = backtick or double-quote spans of 20+ chars, empty-set rule |
| IG10 | paths check extracted no file:line claims; row 1837 unbracketed | **Accepted** -- in full after the blind re-ruling (was partly): all repo file:line citations backticked and expanded; row 1837 cited by its task file so paths checks it |
| IG11 | digests and the M04 fixture are not in the repo | **Accepted** (partly) -- the response measure now uses synthetic fixtures and D7 bars KB content from the repo (DIGEST-AJ-FULL-ANALYSIS-2026-10-31.md:144); the digests stay cited by bare name, as operator rule P-1(1) requires for inputs |
| IG12 | footnote 1 stuffs "measured"; D6 vs advisory D5 contradict | **Accepted** -- footnote 1 rewritten to measure footprint (clean tree, no lock change); D6 now reports only, "not independent" is a report, not a disqualification |

PRODUCER IS1 accepted
PRODUCER IS2 accepted
PRODUCER IS3 accepted
PRODUCER IS4 accepted
PRODUCER IS5 partly
PRODUCER IS6 accepted
PRODUCER IS7 accepted
PRODUCER IS8 accepted
PRODUCER IS9 accepted
PRODUCER IS10 accepted
PRODUCER IS11 partly
PRODUCER IG1 accepted
PRODUCER IG2 accepted
PRODUCER IG3 accepted
PRODUCER IG4 accepted
PRODUCER IG5 accepted
PRODUCER IG6 accepted
PRODUCER IG7 accepted
PRODUCER IG8 accepted
PRODUCER IG9 accepted
PRODUCER IG10 accepted
PRODUCER IG11 partly
PRODUCER IG12 accepted

### Blind re-rulings

The RERULE lines, verbatim, in a text block (they cite the evaluators' scratch name DRAFT-ADR.md, which is not a repo path; one token, DRAFT-ADR.md:23, has its backticks written as single quotes because the paths check resolves a backticked file:line even inside a code block and reports this scratch name as a defect; every other character is as given):

```text
- RULING IS10 -- stands-in-full -- Checking `scripts/decide_checks.py:274-308` and `DRAFT-ADR.md:22-24, 33, 41` confirms that `_RESPONSE_ROW_RE` (`:276`) and `check_response_coverage` (`:279`) only verify in-memory coverage of `**Accepted`/`**Rejected` labels against local per-run finding IDs (even allowing slash-combined `id1 / id2` rows at `:276`) with no revision or artifact hash. Because D4 ('DRAFT-ADR.md:23') keys `logs/VERDICT-KEY.jsonl` by `tree_sha` and `contract_sha256` from lane receipts that `/decide` lacks, D6 must specify stable, ungrouped finding keys and artifact/revision links so key rulings can reliably join to the `/decide` response row and draft revision being rated.
- RULING IG10 -- stands-in-full -- `scripts/preflight_contract.py:84` requires backticks to extract file:line claims, and `scripts/decide_checks.py:108-124` delegates to that verifier. `EVIDENCE.md:15,127` and `DRAFT-ADR.md:6,8` use unbackticked citations and unbracketed row 1837, leaving those claims unchecked.
```

Producer answers (both overturns verified and accepted in full):
- IS10: verified at `scripts/decide_checks.py:276`, where the row pattern admits slash-combined ids and carries no hash. My Phase B answer handed revision links to row 1837 without specifying them, and that was the gap. D6 now specifies them: evaluator headers carry run-id plus adr-sha256 and evidence-sha256; the key is (run-id, evaluator file sha256, finding id); a grouped row is UNKEYED (grouped); a key ruling joins only on equal hashes, otherwise UNKEYED (revision mismatch). Building it is still row 1837's job, and decide_checks.py is unchanged.
- IG10: verified at `scripts/preflight_contract.py:84`, where the file:line pattern requires backticks. Every repo file:line citation in the ADR and in this file outside the verbatim briefs and transport quotes is now backticked, shorthand `:NNN` repo citations are expanded to full backticked paths, and row 1837 is cited by its task file `tasks/1837-decide-independent-adjudication-as-code.md:3`, which paths resolves. The bracket form is still not used: BACKLOG.md in this tree has 0 occurrences of 1837 (it is generated and not regenerated here), so a bracket would fail paths falsely. The citation is checked by its task file instead. Transport citations stay bare, as P-1(1) orders.

RERULE records for every finding the producer marked `partly` (all re-ruled blind by the other family in a new session; `verdict=upheld` means the re-ruler ruled the finding only partly valid and the producer disposition stands, `verdict=overturned` means it stands in full and was answered above; the re-rulers' full ruling lines for the upheld findings are in the lane receipt (the RERULE lines); copilot sessions have no id, their usage file stands in):

```text
RERULE IS5 producer=partly by=gemini-4-argon session=copilot-usage:rr/i-by-argon verdict=upheld
RERULE IS10 producer=partly by=gemini-4-argon session=copilot-usage:rr/i-by-argon verdict=overturned
RERULE IS11 producer=partly by=gemini-4-argon session=copilot-usage:rr/i-by-argon verdict=upheld
RERULE IG10 producer=partly by=gpt-6-sol session=01a198e7-b215-7df2-8a26-9742e262004d verdict=overturned
RERULE IG11 producer=partly by=gpt-6-sol session=01a198e7-b215-7df2-8a26-9742e262004d verdict=upheld
```
