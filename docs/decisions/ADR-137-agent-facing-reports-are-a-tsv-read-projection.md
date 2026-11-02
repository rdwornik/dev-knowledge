# ADR-137: Agent-facing reports are a TSV read projection over records kept as stored, chosen by measured tokens and lookups

- **Status:** Accepted (ADR-94; ratified: to-cc/GO-E3.1.md (operator, 2026-11-01))
- **Date:** 2026-11-01
- **Origin:** /decide run E31-B, revision 3; challenged by CC (R41, 2026-11-01); ratified in `to-cc/GO-E3.1.md` (= `to-browser/RATIFICATION-2026-11-01.md`).
- **Numbering:** PROPOSAL-ADR-STAGE-PHASE = ADR-134, PROPOSAL-ADR-GIT-MEMORY = ADR-135, PROPOSAL-ADR-BROWSER-SURFACE = ADR-136, PROPOSAL-ADR-READ-FORMAT = ADR-137, ADR-124 stays ADR-124. Where the text below names a proposal, read its ADR number.
- **Decision tier:** Path A — operator ratification.
- **Implements:** plan r3 §5 R-e, "JSONL source + a compact read projection chosen by measurement". The plan file is on the transport.
- **Fits:** T1 light, "a bounded fix or extension inside an existing organ" (`protocols/STANDING_RULINGS.md:6939`). The renderer extends `scripts/lane_digest.py`, the receipts-to-digest organ (`:1`, `:25`).
- **Used by:**
  - PROPOSAL-ADR-GIT-MEMORY D6 (the generated journal's read form);
  - PROPOSAL-ADR-BROWSER-SURFACE D1's rollup (Q-R1, ruled).

## Context

**What exists today** (the night seat's worktree commit c6618dbb7, branched from main's tip at session start):
- `logs/MERGE-RECEIPTS.jsonl` is the integrator's append-only ledger (`scripts/merge_receipt.py:45`, `:153`).
  - It holds 235 records, written as spaced JSON.
  - Twelve scripts read it, by grok's count (RFG2); `gen_handoff.py` only cites its name.
  - `lane_digest.py` renders it for the operator (`scripts/lane_digest.py:25`).
- Launch receipts:
  - `scripts/dispatch.py:815` writes one `LAUNCH-<SLUG>.json` per slug, rewritten on repair;
  - `:819` writes `LAUNCH-JOB-<job_id>.json` sidecars;
  - 449 `LAUNCH-*` files in the primary, 235 of them sidecars.
- No agent-facing projection exists.

**Keys, checked over the whole ledger:**
- `slug` alone repeats 11 times.
- `slug + merge_sha` repeats twice, and `merge_sha` is missing on 67 records (it is optional, RFG5).
- `slug + opened` has 0 duplicates and 0 missing.
- For launches, the receipt's file stem is unique by construction. `job_id` can be `pending` or `unresolved` (`scripts/dispatch.py:145`, `:1193`; re-pointed on main 13023da42).

**Corpora:**
- the last 20 lines of `logs/MERGE-RECEIPTS.jsonl`;
- the 20 newest `LAUNCH-<SLUG>.json` (sidecars excluded).

**Forms measured:**
- Every field kept:
  - the bytes as stored on disk;
  - compact JSONL;
  - jsonl-lean (empty and null fields dropped);
  - kv-blocks.
- Projections:
  - declared columns, key columns first;
  - a nested value shown as `<n>`;
  - a column empty in every row dropped;
  - one leading `# source: ... full record: ...` line;
  - rendered as TSV, as kv-blocks, or as JSONL.

**Instrument:**
- **How a figure is computed:** `claude -p --model claude-haiku-5-5 --output-format json --max-turns 1 --tools ""` from a scratch directory outside the repo. Content tokens = (`input_tokens` + `cache_creation_input_tokens` + `cache_read_input_tokens`) minus a one-word baseline from the same repetition. Each figure is the median of 3 repetitions.
- **Why this instrument:** the API `count_tokens` endpoint refused the call (credit balance).
- **Its noise** (RFG6):
  - baselines drifted between repetitions (22,442; 22,125; 25,519);
  - a repetition whose baseline drifted inside it gives a wrong value (negative, or about 3,400 high);
  - the observed step between agreeing repetitions is 317;
  - no bound is claimed, only medians and ratios.
- **Comprehension check:**
  - per corpus, 10 lookup questions generated with a fixed seed from the projected scalar columns, each naming its record by the key;
  - asked once per form, all 10 in one call, of claude-haiku-5-5;
  - scored by exact match against the source value.

| corpus / form | bytes | content tokens (median of 3) | vs stored | lookups correct |
|---|---|---|---|---|
| merge, as stored | 38,243 | 19,738 | 1.00 | 10/10 |
| merge, compact jsonl | 35,771 | 18,793 | 0.95 | - |
| merge, jsonl-lean | 31,102 | 16,594 | 0.84 | 10/10 |
| merge, kv-blocks (all fields) | 30,321 | 16,418 | 0.83 | - |
| merge, projection tsv | 5,506 | 3,634 | 0.18 | 10/10 |
| merge, projection kv | 9,988 | 5,774 | 0.29 | 10/10 |
| merge, projection jsonl | 10,889 | 6,010 | 0.30 | 10/10 |
| launch, as stored | 32,582 | 16,185 | 1.00 | 10/10 |
| launch, compact jsonl | 28,102 | 13,903 | 0.86 | - |
| launch, jsonl-lean | 26,151 | 13,052 | 0.81 | 10/10 |
| launch, kv-blocks (all fields) | 24,831 | 12,467 | 0.77 | - |
| launch, projection tsv | 9,252 | 5,336 | 0.33 | 10/10 |
| launch, projection kv | 13,138 | 6,881 | 0.43 | 7/10 |
| launch, projection jsonl | 14,508 | 7,509 | 0.46 | 5/10 |

**Revision 1's run also measured YAML and a markdown table** (corpus not yet corrected; baseline compact JSONL):
- YAML: +3% / +2%;
- markdown table: -12% / -13%.

**Reading the table:**
- The forms that keep every field save at most 23% against the stored bytes.
- The large gain is from projecting.
- After projecting, TSV costs the fewest tokens and made no lookup errors.
- The kv and JSONL projections cost 59% and 65% more tokens (merge), and they missed lookups on the wider launch corpus. That is one run of 10 questions, so it is weak evidence of an order. It is not evidence of a rate.

**Evidence files** (scratch, outside the repo): `C:\Users\1028120\.claude\jobs\1bc3df49\tmp\decide\readfmt\evidence\`
- `tokens-v2.json`: per-repetition tokens, baselines, questions, scores and the column lists;
- `count_v2.py`: the renderers and the instrument;
- revision 1's files.

## Decision

**D1. Records stay as stored.**
- The merge ledger stays JSONL.
- Launch receipts stay one JSON file per slug.
- Nothing is migrated.

**D2. An agent-facing report rendered from records is a TSV projection:**
- one `#` metadata line, then one header row, then one row per record;
- the columns are a declared list per record kind, kept as data in the renderer's registry, with the key columns first;
- a nested value is shown as `<n>`, its item count;
- a column empty in every row is dropped;
- cells are written by `csv.writer(delimiter="\t")`.
- **Parser rule (RFC6):** a reader skips exactly one leading line that starts with `#`. `project` round-trips its own output in a test.

**D3. Unique keys, and a fetch of the stored record.**
- **Keys:**
  - merges: `slug + opened` (unique and present on all 235 records);
  - launches: `receipt`, the file stem `LAUNCH-<SLUG>`.
- **Fetch:** `lane_digest.py record --kind <k> --key <key>` prints the record exactly as stored, byte for byte (RFC4):
  - for a merge, the ledger line;
  - for a launch, the receipt file, which is its latest attempt.
- **Sidecars:** `LAUNCH-JOB-*` are not records of this kind.

**D4. One renderer, in the existing organ.**
- `lane_digest.py` gains `project` and `record`.
- The browser rollup calls it (Q-R1). The journal generator (git-memory D6, built in E3.2) calls it too.

**D5. The choice stays measured.**
- The build lane commits the two 20-record fixtures and asserts:
  - (a) the projection's bytes are at most 20% (merge) and 35% (launch) of the stored bytes (measured: 14% and 28%);
  - (b) `record` returns the stored bytes;
  - (c) the keys are unique over the committed ledger.
- **Bytes are a regression bound, not the claim (RFG4).** The claim is the token cut, which is re-measured when a flip-condition fires. A test cannot call a model.

## Quality attributes

- **Quality attribute(s):**
  - reading cost: tokens per N records;
  - comprehension: correct lookups;
  - fidelity: every stored byte reachable by a unique key.
- **Scenario:**
  - **Source:** CC or a lane seat.
  - **Stimulus:** needs the last 20 landings or launches.
  - **Artifact:** the projection plus `record`.
  - **Environment:** E3.1 built.
  - **Response:** the agent reads the projection and fetches by key only what it needs.
  - **Response measure:**
    - the D5 tests pass;
    - before HANDBACK, the build lane reruns the comprehension check (20 lookups per kind, claude-haiku-5-5) and records it in the lane receipt; landing calls no model (ADR-131). The projection scores no fewer than jsonl-lean (tonight: 20/20 vs 20/20).
- **Decision evidence:** the Context table; the matrix; 15 evaluator findings, all accepted.

## Consequences

**E3.1 builds:**
- `project` and `record`;
- the column registry;
- the fixtures and the D5 tests;
- the build-lane comprehension rerun (before HANDBACK, never inside `land_lane.py`).

**Costs:**
- A reader that needs `steps` or `argv` makes a second call.
- TSV is less pleasant for a person than markdown; Q-R1 ruled it for the browser rollup, whose reader is an agent seat.

**Out of scope:**
- No dependency is added. A third-party token-oriented notation was not measured and would need the operator's approval as a new dependency.

## Flip-condition

- If the build-lane comprehension check scores the TSV projection below jsonl-lean, the default read becomes jsonl-lean (F4, 20/20 tonight). It does not become a kv projection, which was measured worse (RFC7). The switch is recorded in the lane receipt.
- **The cross-vendor check (RFG3)**, recorded once by the build lane:
  - pipe each fixture form to `codex exec` and read the `tokens used` line of its log, minus a one-word baseline exec;
  - if the merge projection is above 50% of the stored form by that count, the choice is reopened for Codex readers.
- If test (a) fails after a column is added, the column registry is reviewed before the bound is raised.

## Alternatives considered

- **F0, read as stored.** Rejected: 19,738 / 16,185 tokens against 3,634 / 5,336.
- **F1, YAML.** Rejected: more than compact JSONL (revision 1, +3% / +2%).
- **F2, markdown table of every field.** Rejected:
  - -12% / -13% (revision 1);
  - nested JSON needs escaping in cells;
  - not parseable back.
- **F3, kv-blocks of every field.** Rejected: -17% / -23%, and not parseable back.
- **F4, jsonl-lean as the read.** Rejected as the default (-16% / -19%). Kept as the flip target.
- **F6, the projection as JSONL.** Rejected: +65% / +41% tokens over F5, and 5/10 on launch lookups.
- **F7, the projection as kv-blocks** (revision 1's fallback). Rejected: +59% / +29% tokens over F5, and 7/10 on launch lookups.

---

## Evidence

Weights: tokens=35 fidelity=20 machine=15 reuse=15 comprehension=15
| Option | tokens | fidelity | machine | reuse | comprehension | Σ |
|---|---|---|---|---|---|---|
| F0 as stored | 1 | 3 | 3 | 3 | 4[^3] | 2.45 |
| F1 yaml | 1 | 3 | 3 | 2 | 3 | 2.15 |
| F2 md-table | 3 | 2 | 2 | 2 | 3 | 2.50 |
| F3 kv-blocks all fields | 3 | 2 | 2 | 2 | 3 | 2.50 |
| F4 jsonl-lean | 3 | 3 | 3 | 3 | 4[^3] | 3.15 |
| F5 tsv projection + stored fetch | 5[^1] | 3 | 3 | 3 | 4[^3] | 3.85 |
| F6 jsonl projection + stored fetch | 4[^2] | 3 | 3 | 3 | 2 | 3.20 |
| F7 kv projection + stored fetch | 4[^2] | 2 | 2 | 3 | 3 | 3.00 |

[^1]: measured -- median of 3 claude -p usage readings (claude-haiku-5-5) minus a same-repetition baseline, against the bytes as stored: merge 3,634 vs 19,738 (-82%), launch 5,336 vs 16,185 (-67%); tokens-v2.json.
[^2]: measured -- same instrument: F6 merge 6,010 (-70%), launch 7,509 (-54%); F7 merge 5,774 (-71%), launch 6,881 (-57%).
[^3]: measured -- 10 seeded lookups per corpus, one run each, exact match: 20/20 for as-stored, jsonl-lean and the TSV projection (kv projection 17/20, jsonl projection 15/20); capped at 4 because n is 20 and the run is single.

**Scoring notes:**
- `fidelity`: every stored byte is reachable by a unique key. The projections reach it through `record`, a second call. kv forms do not parse back.
- `machine`: the read parses with the standard library under the stated rule.
- `reuse`: fit with an existing organ.
- `comprehension`: 2 or 3 where lookups were missed (F6, F7) or not run (F1-F3).

### Pre-mortem

- **One tokenizer.** Claude's tokenizer only; the cross-vendor flip line watches this.
- **Wide TSV can be misread by column position.** On the 24-column launch corpus TSV made no errors in 10 lookups, but the build-lane rerun is the real watch.
- **The projection hides nested data**, e.g. `steps` (per-step minutes). The metadata line names the fetch. That mitigates; it does not prevent.
- **A declared column list can go stale.** D5 (a) forces a review.
- **The instrument is a fallback with drift.** Only medians and ratios are claimed.
- **The lookups were generated by the producer seat.** The questions are in `tokens-v2.json` for anyone to rerun.

## Subagent claims

- landing is a script that calls a model only on conflict, red CI or BASE-MOVED {probe: grep -c 'Landing is a script' docs/decisions/ADR-131-landing-is-a-script-a-model-only-on-conflict-red-or-base-moved.md}
- the merge ledger path is a declared constant {probe: scripts/merge_receipt.py:153}
- merge receipts are committed, append-only records of cost {probe: scripts/merge_receipt.py:45}
- lane_digest renders the integrator's ledger for the operator {probe: scripts/lane_digest.py:25}
- lane_digest is the operator-facing digest organ {probe: scripts/lane_digest.py:1}
- a launch receipt is one file per slug {probe: scripts/dispatch.py:815}
- job sidecars are a separate file per job id {probe: scripts/dispatch.py:819}
- job_id can be pending {probe: scripts/dispatch.py:145}
- job_id can be unresolved {probe: scripts/dispatch.py:1217}
- T1 light is an extension inside an existing organ {probe: protocols/STANDING_RULINGS.md:6939}
- plan r3 R-e asks for a JSONL source and a measured projection (to-cc/PLAN-NEXT-2026-10-30.md:76) {unverified}
- the token, byte and lookup figures (evidence directory, scratch) {unverified}

## Evaluator records

Unchanged and verbatim in revision 2, `to-browser/PROPOSAL-ADR-READ-FORMAT-2026-11-01.md` (sessions, nonces, served models, every finding id). Revision 3 was not re-sent to the evaluators: its changes come from CC's R41 challenge and the operator's rulings of 2026-11-01, listed in the Revision 3 section below.

## Response table

| id | objection (short) | response |
|---|---|---|
| RFC1 | launch corpus mixed sidecars; not write-once | **Accepted** -- corpus re-cut to the 20 newest LAUNCH-<SLUG>.json; Context says rewritten on repair |
| RFC2 | measured renderer was not the specified one | **Accepted** -- re-measured with key columns first and the metadata line: merge 3,634, launch 5,336 |
| RFC3 | baseline reserialized | **Accepted** -- the baseline is now the bytes as stored (38,243 B / 32,582 B) |
| RFC4 | lean fetch is not the full record | **Accepted** -- D3: `record` returns the stored bytes; test (b) |
| RFC5 | job_id not a unique key | **Accepted** -- launch key is the receipt stem; merge key slug + opened, checked unique over 235 |
| RFC6 | footer row breaks TSV parsing | **Accepted** -- D2: one leading `#` line with an explicit parser rule and a round-trip test |
| RFC7 | kv fallback unmeasured | **Accepted** -- measured: 7/10 on launch, +59% tokens; the flip target is now jsonl-lean |
| RFG1 | launch key | **Accepted** -- same as RFC5 |
| RFG2 | reader count | **Accepted** -- twelve; gen_handoff only cites the name |
| RFG3 | vendor flip not observable | **Accepted** -- uses the `tokens used` line of `codex exec`'s log, minus a baseline exec, recorded by the build lane |
| RFG4 | bytes are not the claim | **Accepted** -- D5 says so |
| RFG5 | merge key not unique | **Accepted** -- slug + opened: 0 duplicates, 0 missing |
| RFG6 | noise overstated as a bound | **Accepted** -- Context states the drift and claims medians only |
| RFG7 | main vs worktree commit | **Accepted** -- relabelled |
| RFG8 | F5 right on the measured tokens | **Accepted** -- kept; margin widened under the corrected baseline |

## Revision 3 - CC's R41 challenge (2026-11-01, on main 13023da42) and what changed

Every revision-2 finding was accepted (15/15); R41 looked hardest where nothing was defended.
- RF-R1 (contradiction, undefended): the response measure and flip 1 put a 20-lookup Haiku call "at landing". ADR-131 makes landing a script that calls a model only on conflict, red CI or BASE-MOVED. The rerun moves to the build lane before HANDBACK, and its result travels in the lane receipt.
- RF-R2 (stale locators): e30-bootstrap moved `dispatch.py`; the receipt writers are now at `:815` / `:819`, and `pending` / `unresolved` at `:145` / `:1193`. The claims are re-pointed; no figure changes.
- RF-R3 (ruling): Q-R1 yes, so E3.1 lane L11 builds D2-D4 with the browser surface. The git-memory generator, which also calls `project`, is built in E3.2.
- Not changed, stated again: one tokenizer (Claude's), a producer-written question set, one run per form; the cross-vendor flip stays the watch.
- Matrix unchanged.
