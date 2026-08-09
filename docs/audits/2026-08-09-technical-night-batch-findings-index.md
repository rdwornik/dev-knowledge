# Night batch 2026-08-09 — findings index across all five lane reports

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** night-batch-findings-index
- **Batch:** the 2026-08-09 night batch, manifest `docs/audits/2026-08-09-technical-batch-night-manifest.md` (`batch: 0`, open at authoring)
- **Author:** the morning integrator (hub primary checkout, local gate mesh live)
- **Purpose:** the next architect's single entry point. Without it, adjudicating this batch means
  reading five long reports (3,487 lines) to locate one item.

**This file INDEXES; it does not restate.** Every row is one line plus a locator. The reasoning,
the evidence and the measurement live in the source report named in each row, and this index is
deliberately not a substitute for reading the one report a decision actually turns on.

**Nothing here is adjudicated.** Zero rows born, zero closed, zero re-pegged by this arc. Every
`ARCHITECT` disposition below is a decision *owed*, not a decision *taken*.

## How to read the columns

- **Sev/Class** — the source report's own severity where it assigned one (N4 uses Critical/High/
  Medium/Low); otherwise a class token: `MEASURE` (a number, no action implied), `DEFECT`,
  `PROPOSAL` (a mechanism offered), `DO-NOT-BUILD` (a proposal the lane argues against building),
  `VERDICT` (a keep/replace/adopt ruling from the library sweep), `PEG` (a deferred row's peg).
- **Owning row** — resolved **live** against `tasks/*.md` frontmatter by this arc, not copied from
  the reports. `UNOWNED` means no open or deferred row covers it. Where a row is adjacent but its
  Done-when does not cover the finding, that is stated rather than rounded to "owned".
- **Disposition** — who the item is waiting on:
  - `ARCHITECT` — needs adjudication (every `## Needs a ruling` item, every kill/re-peg proposal).
  - `OPERATOR` — needs an act only the operator's machine or authority can perform (local reflog,
    a global-infra edit, an external fact).
  - `BUILD-CAND` — a mechanism proposal; a candidate for the batch-4 planning GO, not a decision.
  - `SETTLED` — the lane reached a verdict that closes the question (including every
    `DO-NOT-BUILD`); recorded so it is not re-litigated, per the do-not-relitigate discipline.
  - `INFO` — a measurement or a health finding with no action owed.

---

## 0. Read this first — what more than one lane found independently

Convergence across independently-dispatched lanes is the strongest signal in the batch, because no
lane could see another's work. Five convergences, and the first two are the ones that change what
batch 4 should do.

**C-1 · A cloud container cannot run this repo's gate mesh, and an open row already says so.**
Four of five lanes (N1 §0.3, N3 §0, N4 §1, N5 §8.1) independently re-derived the same three gaps:
the clone arrives **shallow**; `uv` is 0.8.17 against the ADR-106 `==0.11.19` pin so **every**
`uv run --locked` hook entry refuses before doing any work; and `audit.py health` cannot return
`OK` because `repos registered` counts sibling repos that do not exist in a single-repo clone.
**`[#453]` (OPEN, P2/M) already records all three, with these exact workarounds, from the
2026-07-31 cloud batch.** The batch spent four lanes' attention re-measuring an open row. That is
a consumption failure, not a discovery — and it is the sharpest argument in the batch for reading
the open set before dispatch. N1 §0.3.4 and N4 §1 add the part `[#453]` does not yet carry: the
gate mesh is not merely degraded in that container, it is **entirely absent**, so an unattended
cloud session's commits are ungated by construction.

**C-2 · The ADR-110 exemption granted this batch nothing, and no lane could have seen it.**
Integrator finding, verified live before merge #1 (§6, I-1). `batch_manifest.exempt()` requires
**both** an open manifest **and** a merge whose branch matches
`LANE_BRANCH_RE = ^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`. Cloud lanes are `claude/<slug>`
branches, assigned at launch by the runtime. The manifest was correct, committed, and enumerable —
and the exemption it exists to grant was inert for every one of tonight's five merges. It is the
complement of `[#510]` (OPEN, P2/M), which is scoped to the exemption being *too loose*; this is
the same predicate being *unreachable*. See §6.

**C-3 · "Authored from prose intent rather than from its parser" is now at nine instances.**
N2 §1.7c documents three (manifest filename vs `MANIFEST_GLOB`, a lowercase codex-review title vs
`_REVIEW_TITLE_RE`, a non-digit `batch:` vs the suite's pin). N3 §4 independently names the same
three as one sink. **This batch added three more** — N2, N3 and N5 each landed their report at a
path the manifest's lane table does not declare (§5) — and N4 caught its own instance and repaired
it by rename before pushing. Nine instances in three days, of which exactly two cost nothing
because someone chose to run the parser first. N2 §1.7e's Rule C is the proposed refusal.

**C-4 · Three lanes examined `scripts/audit.py` from three angles and converge on one answer.**
N3 §2 measured the whole 41-check mesh at **11.66 s** and refutes the standing suspicion that the
check count is a cost centre. N5 §5.1 measured **0 of 41** checks as generic lint, so no library
replaces any of it. N4 §4 found it doing four jobs and recommends extracting **only** the
230-line fleet-automation write path. **Combined verdict, which no single lane states: keep the
checks, adopt no library, do not split the mesh, extract job 3.** That is a much smaller and much
better-evidenced action than "decompose `audit.py`".

**C-5 · "A ruled adoption that landed at some sites and not others" is now at n=3, not n=2.**
N5 R4 asks whether propagation-completeness deserves an enforcement leg, citing two instances
(`markdown_it` at 2 of 4 fence sites; `yaml.safe_load` at 1 of 2 frontmatter readers). **N3's
cheap-win #2 is a third**: the 2026-07-27 terra ruling that a corpus is defined by what git
*tracks* is implemented in `silent_rule_detector.py` and was never propagated to
`tests/test_toc.py` or `tests/test_normalize_headers.py` — which is the defect N3 measured at
15.13× suite inflation. Three instances, three different rulings, one shape. N5 R4 should be
adjudicated on n=3.

---

## 1. N1 — Position vs North Star

Source: `docs/audits/2026-08-09-technical-n1-position-northstar.md` (646 lines).

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| N1-01 | MEASURE | Open set confirmed exactly: **161 `status: open` · 33 deferred · 194 rendered**; both readings live, differing by exactly the deferred set | — | INFO |
| N1-02 | MEASURE | `audit-py` serialize-group is **43 rows, 27% of the open set**, all mutually serializing — the largest structural constraint on any parallel close plan | — | INFO |
| N1-03 | MEASURE | Backlog is fast, not old: **73% of open rows born in the last 30 days**, zero older than 90 days; live-row curve 80 → 202 in 30 days, first sustained fall on 08-08 | — | INFO |
| N1-04 | MEASURE | **Birth rate, not close capacity, is the binding constraint on v1.0**: 62 closes needed for criterion (3) ≈ **37 batches at the measured net rate** vs **~11 at the close rate with births held at zero** | — | ARCHITECT |
| N1-05 | PEG | **15 of 33 deferred pegs have EXPIRED** — each an owed decision, listed individually at §1.3 in five classes | — | ARCHITECT |
| N1-06 | PEG | Class A (7 rows) — pegged on Wave-1, which closed **the day before the pegs were written**: `[#82]` `[#145]` `[#171]` `[#239]` `[#293]` `[#297]` `[#310]`; all seven verified deferred today | the seven rows | ARCHITECT |
| N1-07 | PEG | `[#171]` alone holds a three-row chain — `[#169]` has `depends-on: #171` *and* pegs on it; `[#322]` names it as a data source | `[#171]` `[#169]` `[#322]` | ARCHITECT |
| N1-08 | PEG | Class B (3 rows) — pegged on a referent that no longer exists: `[#308]` `[#325]` (the P6 carrier step, closed with no successor), `[#294]` (a `mesh-portability` epic that appears nowhere but inside `[#294]`) | the three rows | ARCHITECT |
| N1-09 | PEG | Class C (1 row) — `[#102]`'s peg text states in its own words that its condition will never occur | `[#102]` | ARCHITECT |
| N1-10 | PEG | Class D (1 row) — `[#492]`'s calendar leg (≥ 2026-08-07) has passed; the Grok 4.6 release leg is external and unverifiable from the repo | `[#492]` | OPERATOR |
| N1-11 | PEG | Class E (1 row) — `[#298]`: the handoff-group pass it pegs on demonstrably ran and skipped it; it also blocks `[#301]`, a **deferred-on-deferred** chain stalled at both ends | `[#298]` `[#301]` | ARCHITECT |
| N1-12 | DEFECT | `[#322]`'s peg referent (C4 visualization research) **exists and was ruled against** — "visualization deferred wholesale", 2026-07-11. A row waiting on research already answered negatively is waiting on nothing | `[#322]` | ARCHITECT |
| N1-13 | MEASURE | The 18 non-expired pegs are itemised with their class (event-witnessed / id-pegged / condition-pegged) — no adjudication owed on them today | — | INFO |
| N1-14 | DEFECT | **Intake #28 §B is `DRAFT`** — the whole North Star scoreboard is scored against an unratified finish line (verified live: intake #28 status `DRAFT`) | — | ARCHITECT |
| N1-15 | MEASURE | Scoreboard: **0 of 8 criteria met, 1 partial, 7 open** | — | ARCHITECT |
| N1-16 | MEASURE | Criterion (1) W-wave: intake #25 is `DRAFT`, expects 6–8 births, **zero exist**. Closing it makes criterion (3) worse — the two collide by construction | — | ARCHITECT |
| N1-17 | **ACTION** | Criterion (2) closure-harvest: **1 of 2 windows**. Exactly one artifact in the repo carries the required opened/closed/net line (batch-3's packet). **This batch's own packet closes the criterion if the night's net is ≤ 0** — the cheapest of the eight by a wide margin | — | INFO (discharged §7) |
| N1-18 | MEASURE | Criterion (3) open backlog < 100: distance **62** (`status: open`) or **95** (rendered) | — | ARCHITECT |
| N1-19 | DEFECT | Criterion (4) "one command from the template" names **a template that does not exist** — it is intake #25's W-1 (copier), zero births; three deferred rows sit on the same surface, all Class A/B expired | `[#293]` `[#294]` `[#305]`; `[#215]` open + diff-verified closeable | ARCHITECT |
| N1-20 | DEFECT | Criterion (5) handoff cut: the mechanized cost is **~4.5 s — 0.25% of the 30-minute wall clock**. **No engineering closes this**; it needs one operator ruling on which load is cut | `[#511]` OPEN P2/M | ARCHITECT |
| N1-21 | DEFECT | Criterion (6) provider-swap: codex is live as a **reviewer, never a producer**; the enabling row is open and idle 23 days | `[#341]` OPEN P2/S | BUILD-CAND |
| N1-22 | DEFECT | Criterion (7) zero standing REDs: **exactly 1 RED, owner named** — but "dispositioned owner" is undefined; `[#426]` is named in the failing test's docstring, not in `ecosystem/disposition-register.yaml` | `[#426]` OPEN P2/M | ARCHITECT |
| N1-23 | PROPOSAL | Criterion (8) weekly so-what packet: no such artifact exists; **cheapest build of the seven open criteria** — declare an ADR-105 routine over the already-shipped `window_metrics.py` | `[#461]` closed (tool shipped); `[#419]` OPEN P2/M (routines nobody consumes) | BUILD-CAND |
| N1-24 | PROPOSAL | Four-batch critical path to v1.0 (batch 4 adjudication → 5 cheap builds → 6 W-wave → 7+ the number); **honest total ~14–15 batches**, contingent on holding birth rate near zero | — | ARCHITECT |
| N1-25 | DEFECT | **16 of 86 open P1/P2 rows have not moved in >30 days**; 10 of the 16 were last touched by a *bulk grooming pass*, so their real "considered on merits" date is older than the table shows | the 16 rows | ARCHITECT |
| N1-26 | DEFECT | **`[#270]` is the standout**: one of only three open P1s, idle 32 days, and a prerequisite — `[#271]` and `[#348]` carry `depends-on: #270` and `[#117]` pegs on it (all verified live) | `[#270]` OPEN P1/M | ARCHITECT |
| N1-27 | DEFECT | `[#213]` is idle 32 days **and already diff-verified closeable** — a consumption failure, not a work failure | `[#213]` OPEN P2/L | ARCHITECT |
| N1-28 | DEFECT | Three confirmed P3-blocks-P1/P2 edges: `[#23]`→`[#112]` (3-deep), `[#170]`→`[#139]`, `[#298]`→`[#301]` | those rows | ARCHITECT |
| N1-29 | DEFECT | **8 rows carry P1/P2 priority *and* `deferred` status**, two of them P1 (`[#218]`, `[#300]`) — a row simultaneously urgent and parked carries a priority it cannot act on | those 8 rows | ARCHITECT |
| N1-30 | PROPOSAL | **K-1 · kill `[#102]`** — the peg's own text says the condition will never occur; no superseding id; the verify-first clause was never discharged | `[#102]` | ARCHITECT |
| N1-31 | PROPOSAL | **K-2 · kill or re-peg `[#308]`** — its own `kill-candidates:` line says the referent closed "with no successor"; the underlying decision is still real, so re-peg may be the correct disposition | `[#308]` | ARCHITECT |
| N1-32 | PROPOSAL | **K-3 · fold `[#325]`** — same dead peg; `[#294]` is the nearest live carrier row, so a fold is likelier correct than a kill | `[#325]` `[#294]` | ARCHITECT |
| N1-33 | PROPOSAL | **K-4 · kill `[#310]`** — cheapest in the set: the live audit's `preflight_backlog_ids` WARN already points at it every run, and `#292` (its escape clause's precondition) is verified closed | `[#310]` | ARCHITECT |
| N1-34 | SETTLED | Considered and **not** proposed for death: `[#239]`/`[#240]` (a titling defect, not duplication) and `[#153]`/`[#188]`/`[#166]` (thematic overlap, distinct mechanisms — a `[#506]` grooming call) | `[#506]` OPEN P2/M | SETTLED |
| N1-35 | DEFECT | `[#499]`'s peg cannot fire regardless of code quality if the false-positive count is not *being reported at each seal*; the live audit shows `review_artifact_coverage` WARN today | `[#499]` deferred P3/M | ARCHITECT |
| N1-36 | INFO | 153 open ids carry a pending closure-proposal that **could not be examined** — the store is gitignored and does not exist in a cloud clone | `[#487]` OPEN P2/L | OPERATOR |
| N1-37 | DEFECT | The suite's verdict **inverts with the container**: `test_reverse_dep_oracle.py` fails when a language server IS present (it asserts absence); 17 `test_fleet_analytics.py` failures are pandas-in-an-optional-group; the `-n auto` whole-suite invocation **hung** in the cloud container | `[#453]` OPEN P2/M | ARCHITECT |
| N1-38 | INFO | Method note: the lane **declined the contract's prescribed haiku fan-out** for frontmatter/last-touch extraction, on the ground that both quantities are exactly computable and a retrieval subagent could only add transcription error. Flagged, not done silently | — | INFO |

**N1 rulings requested:** R-1 … R-16 → §7.

---

## 2. N2 — Architect-defect → mechanism map

Source: `docs/audits/2026-08-09-technical-night-n2-mechanism-map.md` (920 lines).

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| N2-01 | DEFECT | **D1 · Batch 3 dispatched with no committed manifest** — measured cost **2h12m**, an integrator run that reached the precondition gate and correctly STOPPED before merge #1. The asymmetry is the finding: `batch_manifest` is a **reader**; nothing anywhere *demands* a manifest at dispatch | `[#505]` OPEN P1/M | — |
| N2-02 | PROPOSAL | Fix for D1: `scripts/batch_open.py --check` reusing `open_batches()` verbatim + a first-step refusal in `/lane-boot` §1. **~30 lines.** The stronger "make the prompt unemittable" form is unreachable from Layer 2 — take the reachable version | `[#505]`; `[#509]` OPEN P3/S (the dispatch wrapper) | BUILD-CAND |
| N2-03 | DEFECT | **D2 · A frozen contract asserted repo state that was false at dispatch** (`journal_spine_anchor` "hard-RED"; live predicate returned `[]`). Cheapest of the six by measured cost — corrected in-flight by the receiving lane | — | — |
| N2-04 | DO-NOT-BUILD | **Do not build `contract-lint`** — it cannot discriminate a state claim from prose without NLP; the batch-3 contract *already carried a SHA*, so a stamping rule would have passed the very artifact it exists to catch; and the contract is not a repo artifact. The repo has a named precedent for refusing this heuristic class (`_REVIEW_TITLE_RE`'s docstring) | — | SETTLED |
| N2-05 | PROPOSAL | Build instead: **one sentence in `templates/prompt-template.md`** making `/preflight` a mandatory opening beat that reports each §Premises claim CONFIRMED/REFUTED with live output. Zero code | `[#483]` closed (preflight adopted, ungated) | BUILD-CAND |
| N2-06 | DEFECT | **D3 · Nine of ten hub lane branches violated the ratified enum**, and **two rival `LANE_BRANCH_RE` definitions ship in one repo** (`validate_branch_naming` strict, `batch_manifest` loose). Every satellite lane the same day conformed — a hub-side dispatch-discipline gap, not a broken validator | `[#508]` covers **prose-vs-code cardinality only**; the code-vs-code split is **UNOWNED** (`[#510]`'s own text says so) | ARCHITECT |
| N2-07 | PROPOSAL | D3 fix, **and the sequence is the whole point**: (1) enforce at provisioning first — a pre-commit leg classifying `git branch --show-current`, BLOCK on `KIND_UNKNOWN` under the `worktree-lane-` prefix, ~15 lines against a tested classifier; (2) *then*, after one clean batch, delete the loose regex and import the strict one. **Step 2 before step 1 is a merge-queue outage** (9 of 10 historical merges become non-exempt) | `[#508]` `[#510]` | BUILD-CAND |
| N2-08 | DEFECT | **D4 · Worktree provisioning hand-written instead of `/lane-boot`** — folds into D3; it is D3's delivery vehicle. Also corrects a live premise: `worktree_seed --plan` prints *two* halves, not one | `[#429]` closed | SETTLED |
| N2-09 | DEFECT | **D5 · Integration hand-written instead of `/lane-integrate`** — cost masked by D1's stop; **no figure invented** | `[#505]` | — |
| N2-10 | PROPOSAL | D5 fix: not a checker, a **surfacer** — an open batch whose manifest is older than the newest commit by >1 day WARNs. ~12 lines against `audit.py`'s existing open-batch reporting; converts "the batch never formally closed" from invisible to a daily nag | `[#505]` | BUILD-CAND |
| N2-11 | DEFECT | **D6 · Acceptance criteria froze "exactly N files"** — unsatisfiable by construction, because six hooks mandate regenerated companions. Confirmed live tonight: N5 shipped one file and left `docs/audits/README.md` stale (§5) | — | ARCHITECT |
| N2-12 | DEFECT | **D6(b) · The contract froze `pythonpath = ["."]`**, a spelling under which **67 of 99 test files fail to collect**; a full three-arm measurement lane was spent measuring a spelling the architect had frozen as the answer | `[#502]` OPEN P3/M | ARCHITECT |
| N2-13 | DO-NOT-BUILD | For D6 there **should be no organ** — a contract freezing a wrong literal is a reasoning error, and the tool that catches it is the lane. Two contract-prose rules instead: acceptance names a **property, never a file count**; a frozen literal is stated as a **hypothesis** | — | SETTLED |
| N2-14 | DO-NOT-BUILD | Rejected: a "companion-file predictor" computing the true N from `.pre-commit-config.yaml` (~80 lines to serve one prose sentence, and it institutionalises the file-count habit) | — | SETTLED |
| N2-15 | **HIGHEST-RATIO** | **D7 · A manifest filename invisible to the parser that consumes it.** The dispatch contract's spelling does not match `MANIFEST_GLOB`; had it shipped, `open_batches()` returns `[]` and the night reproduces batch 3's 2h12m **while looking like its repair**. Cost this time ~zero — because of individual diligence, not a mechanism | `[#505]` adjacent; the refusal itself UNOWNED | ARCHITECT |
| N2-16 | DEFECT | The gap named precisely: **`validate_hermetization` Rule B validates that a filename is well-formed for the TREE and never that it is well-formed for its READER.** Both spellings pass Rule A+B. Two grammars govern one name; one is gated, one is not | UNOWNED | ARCHITECT |
| N2-17 | DEFECT | Recovery cost is asymmetric: `docs/audits/` is immutable, so this class costs **either a superseding artifact or a knowing violation of rule 3** — instance C could not be superseded (two manifests would both match the glob) and was repaired by editing an immutable file in place | — | INFO |
| N2-18 | DO-NOT-BUILD | **"Name it through the generator" does NOT subsume the class** — no generator writes any new file under `docs/audits/` today, and the repo holds a **measured negative result**: `PLAYBOOK.md:3476` already carries the correct `# Codex Review — {topic}` template and instance B was hand-authored around it anyway. The refusal is the enforcing half; the generator is the ergonomic half and catches nothing | — | SETTLED |
| N2-19 | PROPOSAL | **Rule C — consumer-glob round-trip**, ~45 lines extending a live pre-commit hook: an added `docs/audits/*.md` whose name *announces* a class (`manifest`) its consumer cannot enumerate is refused. Predicate **imported, never restated**. Ranked #1 in the report | UNOWNED | BUILD-CAND |
| N2-20 | INFO | Rule C's honest limits, stated by the lane: it catches **announced classes only** (an *omission* is not refusable); it fixes the filename leg only; and `_CONSUMER_CONTRACTS` is a growth surface that must ship with closure discipline — "a Rule C with six speculative rows is worse than no Rule C" | — | ARCHITECT |
| N2-21 | PROPOSAL | Two cheaper legs to ride along: shape-check `batch:` in `open_batches()` (~6 lines, converts instance C from "working exemption, RED suite" to a loud refusal); and BLOCK an added `docs/audits/*-codex-*.md` whose body fails `_REVIEW_TITLE_RE` (~15 lines) | `[#480]` closed (the coverage leg) | BUILD-CAND |
| N2-22 | VERDICT | Library-first on Rule C: stdlib wins (the predicate is already a repo constant); **`pydantic` is the right tool in the wrong place** — it must not enter a gate path, and outside it duplicates a 6-line check; `jsonschema`/`python-frontmatter`/`PyYAML` all NO. Rule C is the **fourth instance of a shape this repo has already ratified three times** | — | SETTLED |
| N2-23 | DEFECT | **D8 · Lane contracts are not recoverable from the repo — `[#505]` leg 1, missed by two consecutive batches.** Batch 3 removed the manifest as well, so a fresh seat inheriting it finds **neither** the contracts nor the plan. Every contract lived in `~/Downloads`; `$env:CLAUDE_PROMPTS_DIR` did not expand at dispatch | `[#505]` OPEN P1/M leg 1; `[#509]` OPEN P3/S | ARCHITECT |
| N2-24 | PROPOSAL | D8 fix, **~10 lines against existing helpers**: a `contracts:` frontmatter field, and a manifest whose `contracts:` path is absent from the committed tree **opens nothing** — the same discipline `_valid_closer` already applies. It works because it inverts the incentive: the batch cannot obtain its exemption until the contracts are in the tree | `[#505]` | BUILD-CAND |
| N2-25 | DEFECT | D8's blocker: **`docs/batch/` is not a sanctioned `SANCTIONED_GENRES` value**, so it needs an ADR-101 amendment; nesting contracts under `docs/audits/` avoids the amendment but misclassifies a contract as an audit | `[#345]` OPEN P2/M (externalize the ADR-101 frozensets) | ARCHITECT |
| N2-26 | INFO | Scope honesty from the lane: this delivers `[#505]` **leg 1 only**. Do not read leg 1 landing as the row closing | `[#505]` | INFO |
| N2-27 | DEFECT | **D9 · n=5 unattributed HEAD swaps is UNVERIFIED** — relayed from the dispatch contract, checked nowhere in the tree, and the reflog needed to verify it is gitignored. Two *prior* instances are fully documented in `JOURNAL.md`, so the pattern is real even though n is not | UNOWNED | OPERATOR |
| N2-28 | DO-NOT-BUILD | **Do not build a HEAD-swap detection organ.** `block-ff-push` already refuses the push a HEAD swap produces and has failed CLOSED since 2026-08-03; the residual harm is that *repair is unsafe while a sibling session is live*, and the mechanism for that is **not sharing the primary checkout** — which D3's provisioning refusal delivers anyway | — | SETTLED |
| N2-29 | PROPOSAL | Handoff amendment 1 — `HANDOFF_PROCESS` §2: **session-scoped retrieval is RESIDENT, not pointered.** The pointer rule protects against drift, and drift needs more than one reader; a candidate pool cut for one session has exactly one reader. Test: *stale in a week → pointer it; meaningless in a week → carry it* | `[#511]` OPEN P2/M | BUILD-CAND |
| N2-30 | PROPOSAL | Handoff amendment 2 — §5: **a required evidence row must be able to FAIL.** Of the required rows only P3 can genuinely fail in the ordinary case; a manifest of rows that pass by construction reads as ceremony and discounts the rows that can fail. Proposes three-seal pruning | `[#511]` | ARCHITECT |
| N2-31 | PROPOSAL | Handoff amendment 3 — §4 BOOT DRILL: **the sample dispatch line's lane name is *checked*, not looked at** (`validate_branch_naming.py --lane`). Evidence: on 2026-08-08 the drill either did not run or ran without the enum check — nine of ten emitted lanes were off-enum, and an off-enum name is not visible to a look | `[#511]`; `[#359]` OPEN P1/M (phantom enforcement) | BUILD-CAND |
| N2-32 | MEASURE | Ranking by prevented-cost ÷ build-size, prevented cost **measured, not projected**. **Build first: Rule C (§1.7e), lane-enum at provisioning (§1.3), dispatch-time open-batch refusal (§1.1)** — together under 100 lines, zero dependencies, each converting a documented 2026-08-08 failure into a refusal | — | ARCHITECT |

**N2 rulings requested:** R1 … R7 → §7.

---

## 3. N3 — Performance, bottlenecks, instrumentation design

Source: `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md` (862 lines).

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| N3-01 | DEFECT | **The record's ÷3.5 suite claim is confounded** — the cited pair changes *two* variables (worktree count **and** test population: 2555 vs 2721 collected). The clean pair was already in the record and unused | — | INFO |
| N3-02 | MEASURE | The defensible measurement, at constant test population: **532.28 s → 1903.85 s, ×3.58 — 22m51s of pure overhead.** Stronger evidence than the claim it replaces | — | INFO |
| N3-03 | DEFECT | **Mechanism proven in code:** `tests/test_toc.py:262` and `tests/test_normalize_headers.py:222` define a `_SKIP_PARTS` set that omits `.claude`, and `rglob` does not honour `norecursedirs` — so **five tests read and CommonMark-parse every markdown file in every registered worktree**. Four collection-scope hypotheses were REFUTED first | **UNOWNED** (no open row matches) | BUILD-CAND |
| N3-04 | DEFECT | **The standard already exists in-repo and predates the incident.** Three production scanners exclude worktrees (`validate_reconciliation.py`, `enforcement_coverage.py`, `silent_rule_detector.py` — the last structurally, via `git ls-files`, ruled terra HIGH **2026-07-27**). The two test files are the outlier — see C-5 | UNOWNED | ARCHITECT |
| N3-05 | MEASURE | Controlled sweep in an isolated sandbox (the real repo was **never** given a worktree): **15.13× wall at 14.00× corpus** — slightly superlinear, traced to `sorted(root.rglob(...))` | — | INFO |
| N3-06 | **CORRECTION** | **The lane corrects its own first reading:** on 16 cores the five tests are independent units under `--dist load`, so the contribution to *wall* clock is the critical path, not the serial sum. **The tree walk explains ≈24% (~5m23s) of the observed 22m51s. ~17 min remains unexplained by it** | — | INFO |
| N3-07 | DEFECT | Named candidate for the remainder, **UNMEASURED**: 8 of the worktrees were `locked` — i.e. up to **8 live lane sessions** — while a 16-worker suite ran on a 16-core box. The two causes are **confounded and multiplicative**, and no experiment in the record separates them | UNOWNED | ARCHITECT |
| N3-08 | **REFUTED** | **The 41-check gate mesh costs 11.66 s total — ~0.2% of an integration arc.** The suspicion that the check count is a cost centre is refuted by measurement; three checks are 83.5% of it. **No cheap win lives here** | — | SETTLED |
| N3-09 | MEASURE | No superlinear check found; worktree amplification **does not reach the gate mesh** — by construction, because `check_doc_code_edge` passes an explicit include-list and `repo_path/"scripts"`. The mesh is already built to the standard the two test files miss | — | INFO |
| N3-10 | PROPOSAL | `validate_doc_code_edge` walks `scripts/*.py` **twice** (lines 161 and 189). Merging them saves **~3 s per gate run** — "real, correct, and worth ~3 seconds, which is precisely why it should not be prioritised" | UNOWNED | BUILD-CAND (low) |
| N3-11 | MEASURE | **The suite is wait-bound, not CPU-bound: 14.6% CPU utilisation** (269.7 s CPU against 462.8 s wall on 4 cores) — average parallelism 0.58 of a core | `[#317]` OPEN P2/M (default-parallel invocation) | ARCHITECT |
| N3-12 | DEFECT | **Language-server timeouts are ~83 s of pure sleep per suite run** (4 tests sitting on `DEFAULT_WARM_TIMEOUT = 20.0` when no server is present) | UNOWNED; `[#317]`'s `slow` marker tier is the existing mechanism | BUILD-CAND |
| N3-13 | DEFECT | **Instrument defect:** because tests load modules via `spec_from_file_location` and mutate a shared worker's `sys.path`, `--durations` attributes a first import's entire cost to whichever test triggered it. Per-test durations are **worker-history-dependent**; `-n 0` is the only trustworthy instrument for per-test attribution | `[#502]` OPEN P3/M | INFO |
| N3-14 | MEASURE | Batch-3 integration cost **~3h40m across both attempts**, of which **~2h12m produced nothing mergeable**. Attempt 2's merge queue was 33m02s for 10 merges (3m18s average) **including every generated-file conflict** | — | INFO |
| N3-15 | **REFUTED** | **Conflict resolution on generated files was not the sink**, and regeneration-by-default is already the practice and already cheap. The measured win from regeneration is a **correctness** win, not a time win — both doc-counts sides were wrong; hand-picking either would have committed a number nobody counted. **Do not book it as a saving** | — | SETTLED |
| N3-16 | PROPOSAL | `/lane-integrate` §2 as literally written (a full suite after every merge) would have cost **10 × 8m59s ≈ 1h30m**. The integrator correctly ran one suite on the merged result. **The text is what is now wrong** — worth ~1h21m per 10-lane batch | `[#505]` | ARCHITECT |
| N3-17 | DEFECT | Contract figures **"2h43m" and "~9 minutes" are unlocated anywhere in the tracked record** — `grep` returns nothing for any spelling. Per the lane's own discipline: a reported figure it could not verify is a finding, not a fact | — | OPERATOR |
| N3-18 | DEFECT | **The 8m23s / 8m59s divergence**: the consolidation report's prose says one figure, the packet and JOURNAL say the other. Both are real runs (pre- and post-repin) | — | ARCHITECT |
| N3-19 | MEASURE | Reviewer-loop economics (lane 290): **1h44m40s, 24 findings, 21 accepted.** All 7 Criticals landed by pass 6; passes 7–14 cost **41% of the loop and returned zero Critical**. Every accepted finding across 14 passes was **one shape** — 21 instances of one defect class at ~5 min each | — | INFO |
| N3-20 | PROPOSAL | Verdict: the loop was worth running *given the code it was reviewing*; the code should not have needed it. Proposed standing trigger: **when three consecutive passes return findings of the same shape, stop fixing instances and replace the mechanism** — it would have fired at pass 3 and plausibly saved most of an hour. Offered as a question (n=1), not a proposal | UNOWNED | ARCHITECT |
| N3-21 | **DESIGN** | S3a instrumentation: **the correct organ is a READER, not a RECORDER.** Claude Code already writes a complete timestamped per-message, per-model, token-attributed JSONL for every session, including `gitBranch` (free lane attribution), `effort`, and `subagents/agent-*.jsonl` side-files that satisfy S2's split criterion at no extra cost. **Verified live** against the lane's own transcript | `[#419]` adjacent; the design itself UNOWNED. Its requirement lives in intake **#29, `DRAFT`** | BUILD-CAND |
| N3-22 | DO-NOT-BUILD | **Anti-goal, stated plainly: do not add a `PostToolUse` hook.** It fires on every tool call, sits on the operator's latency path, and re-records data already on disk. One `SessionEnd` hook, fail-soft, never blocking — **not `Stop`**, per the ADR-85 "an organ that can be exhausted cannot carry teeth" finding | — | SETTLED |
| N3-23 | PROPOSAL | Shape: one JSONL line per session to `logs/ARC-METRICS.jsonl` (gitignored, §9 naming rule, `PARITY-EVENTS.jsonl` precedent); per-batch one packet line; per-window **extend `window_metrics.py` (~40 lines) rather than add a seventh reporter**. ~120 LOC, no new dependency. Phase derivation is a heuristic and the `basis` key says so; operator idle is reported as a **named gap**, not a number | `[#461]` closed (the tool to extend) | BUILD-CAND |
| N3-24 | **FALSIFIABLE** | Recorded in advance so it cannot be retrofitted: **if two windows confirm `retrieval` < 20% of arc wall, S3b/S3c (the distillation engine) should be descoped** — tonight's single-arc reconstruction suggests verification and review dominate, not context assembly | intake #29 `DRAFT` | ARCHITECT |
| N3-25 | **CHEAP-WIN #0** | **Do not run the integration suite while lane worktrees are locked** — **~23 min per suite run observed**, of which ~17 min is the un-isolated contention share. **Zero code**: a sequencing rule. Largest number in the report, and it **rests on inference, not measurement** (the lane flags this against itself) | UNOWNED | ARCHITECT |
| N3-26 | **CHEAP-WIN #1/#2** | Switch both test corpora to `git ls-files` (the already-ruled standard) rather than patching `_SKIP_PARTS`: **≈5m23s critical path** whenever worktrees are registered, **plus 3.9× faster enumeration** (58.4 ms → 15.1 ms), platform-stable, O(1) in worktree count, and it cannot rot the way a hand-maintained skip list does. **Provably identical file set on the current tree (set-difference 0)** | UNOWNED | BUILD-CAND |
| N3-27 | INFO | How #0 and #1/#2 relate: teardown removes both causes, so on an arc that can wait for its lanes the code fix adds nothing. **Its value is precisely the case where teardown is not available** — a mid-batch suite run, which is the normal condition during exactly the batches that hurt | — | INFO |
| N3-28 | INFO | **No line of the cheap-wins table should be read as "the suite gets 35% faster."** The honest floor is the critical-path saving: ~21 s + ~23 s if both classes vanish in a worktree-free tree | — | INFO |
| N3-29 | DEFECT | **`check_stale_worktrees` cannot see the cost, by design** — its docstring rules mid-batch a PASS deliberately, and the cost was 13 *fresh, legitimate* worktrees. The lane explicitly does **not** propose changing it. Separately: the doctrine says "mechanized weekly prune stays" but **no scheduled task runs it** | `[#505]` (WARN-tier scope) | INFO |
| N3-30 | UNMEASURED | **The single highest-value measurement not taken tonight:** `-n 4` vs `-n 8` vs `-n 16` on a fixed tree. The 14.6% utilisation is measured; the inference that `-n` should exceed `os.cpu_count()` for wait-bound work is **not**. Costs two suite runs, and should precede any `addopts` change | `[#317]` OPEN P2/M | OPERATOR |

**N3 rulings requested:** 1 … 6 → §7.

---

## 4. N4 — Structural code review of the hub's hot spots

Source: `docs/audits/2026-08-09-technical-n4-code-review.md` (561 lines). **Tally: 0 Critical / 3 High / 5 Medium / 4 Low.**
The artifact is deliberately **not** titled `# Codex Review` and states why — no reviewer lane was
reachable in the container, and claiming the title would manufacture exactly the unfalsifiable
evidence `check_review_artifact_coverage` exists to prevent. It is a **first-party** tally.

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| N4-F1 | **HIGH** | `scripts/audit.py:2998-3004` — `_git` runs **unscrubbed** (`cwd=` but no `env=`) while the same file imports `gitenv` at module level. **Reproduced:** `GIT_DIR` makes it read repo A while labelling the answer with B. Six call sites; the worst feeds `check_silent_rule_ratchet`'s **baseline** read, so a *confidently wrong* baseline reads as `valid` and sails through the lattice designed to block indeterminacy. Lane worktrees export `GIT_DIR` absolutely, so this fires in every lane commit | **UNOWNED** (`[#396]`, `[#512]` both closed and neither covered this helper) | BUILD-CAND |
| N4-F2 | **HIGH** | **Two `LANE_BRANCH_RE` constants, same name, different grammar — measured to disagree on 8 of 11 real merged lane branches.** The loose one grants the ADR-85 anchoring exemption to branches the naming validator deliberately classifies `unknown`. **Both organs cannot be enforced.** Needs a ruling *before* code moves | **UNOWNED** for the code-vs-code split (`[#508]` covers prose cardinality; `[#510]` covers roster scoping) | ARCHITECT |
| N4-F3 | **HIGH** | `deploy/carrier_globalconfig.py:179-195` — **the only carrier that writes outside a repo is the one with no path containment.** `target_filename` is joined to `~/.codex` with no `_safe_rel`/`_contained`/`.resolve()`; `../../.bashrc` writes hub bytes into the user's home tree. The `try/except ValueError` at `:80` **looks like a guard and is not** — it falls through to reading the out-of-tree path anyway. Rated HIGH on **blast radius**, not likelihood (the manifest is hub-authored) | UNOWNED; `[#485]` OPEN P3/S is the natural landing seam | BUILD-CAND |
| N4-F4 | MED | The 2026-08-08 containment fix is **correct and well-tested** (symlinks resolved on both legs, re-checked after `mkdir`, Win32 trailing-dot refused, adversarial tests) — **but local to one carrier.** Three sibling carriers take manifest paths with **no guard and zero containment tests**. Nothing anywhere in `deploy/` checks Windows reserved device names | `[#485]` OPEN P3/S | BUILD-CAND |
| N4-F5 | MED | `scripts/gen_handoff.py:186-224` is a **fifth, independent copy of the git-env scrub** that `[#396]` did not consolidate — in the very module whose open-batch refusal `gitenv.py`'s docstring cites as the motivating live failure. Latent drift edge, not a live wrong answer | UNOWNED (`[#396]` closed) | BUILD-CAND |
| N4-F6 | MED | `scripts/audit.py:3001` — `text=True` with no `encoding=`/`errors=`; **`UnicodeDecodeError` is a `ValueError` and escapes the function's own handler**. **Reproduced** under `core.quotePath=false`: the blocking `audit-health` gate dies with a traceback instead of returning a verdict. Every *other* git call in the file already carries `errors="replace"` — ratified terra HIGH 2026-08-07. **Same one-line call site as F1** | UNOWNED | BUILD-CAND |
| N4-F7 | MED | **Two freshness hooks do not watch their own generator** (`roster-freshness`, `claude-rosters-freshness`), so a commit changing only rendering logic never triggers that generator's regen-and-diff gate. The two sibling hooks include theirs — an inconsistency, not a design choice. **Fix is two regex fragments** | UNOWNED | BUILD-CAND |
| N4-F8 | MED | The general case behind the intake finding, worst-first: **`ecosystem/index.yaml` is fully unguarded** — generated wholesale, `click.Choice(["update"])` so there is **no `--check` mode to hook**, no `ALL_CHECKS` leg, no dedicated test. `templates/child-methodology-floor.sha256` unguarded on the hub; `ecosystem/doc-counts.md` WARN-only. `docs/intake/manifest.json` is the *mildest* case and **is** blocking-guarded | PARTIAL — `[#369]` OPEN P3/S is the same class; `[#132]`/`[#269]` adjacent; **`ecosystem/index.yaml` itself UNOWNED** | BUILD-CAND |
| N4-F9 | LOW | `scripts/audit.py:2977` splits newline-separated git output on **whitespace**, shredding filenames containing spaces. The verdict survives; **the evidence it prints names files that do not exist**, which is what a human then acts on. Fix: `.splitlines()` | UNOWNED | BUILD-CAND |
| N4-F10 | LOW | `scripts/validate_onboarding_rulings.py` is reachable by **no gate and no command** — deliberate per its own docstring, recorded because *an inert validator is indistinguishable from a passing one until someone checks* | UNOWNED | INFO |
| N4-F11 | LOW | The validator family has **no shared module**: 8 byte-identical repo-root discoveries, 6 `format_findings` implementations, and **3 date-shape regexes that disagree on the same input**. Inside `audit.py`, `_run` is duplicated and four near-identical YAML loaders sit within 70 lines | PARTIAL — `[#397]` OPEN P3/M | ARCHITECT |
| N4-F12 | LOW | `scripts/gitenv.py:87-90` — the consolidated scrub has **no `timeout=`**, while every other git call in the fleet carries one, including the F5 copy proposed for deletion. Not a regression, but consolidating onto it would **lose** the timeout. Fix both together | UNOWNED | BUILD-CAND |
| N4-13 | DEFECT | `audit.py` is doing **four jobs**, and job 3 — a fleet-automation **WRITE path** that stages, commits and pushes — sits oddly against CLAUDE.md §5 rule 4 / ADR-28 / ADR-36 ("Layer 2 never executes"). It may well be sanctioned, **but the sanction is not visible at the invariant** | `[#397]` OPEN P3/M | ARCHITECT |
| N4-14 | PROPOSAL | **Do not split the check mesh.** Coupling is real and measured (30 test files `import audit`; 17 dual-mode import pairs; reflective `ALL_CHECKS` reads; source-text assertions). **Extract job 3 only** — ~230 contiguous lines, the only part that mutates state, with **zero `ALL_CHECKS` coupling** | `[#397]` | BUILD-CAND |
| N4-15 | INFO | Per-check coverage is genuinely complete (41 registered = 41 defined, zero orphans either way, zero untested). **No smoke-only test in the entire 12-validator family.** Two weak spots named: a zero-assert test and an exit-code-only test | — | INFO |
| N4-16 | DEFECT | **Where the unmeasured-assertion-quality gap matters most:** mutation testing is unavailable, and the three fail-CLOSED organs (`block_ff_push`, `block_unanchored_push`, the shared `journal_anchor` predicate) are the only organs with teeth. **If mutation testing is ever affordable for exactly one module, it should be `scripts/journal_anchor.py`** — two organs import its predicate and a silent weakening disarms both at once | `[#502]` OPEN P3/M | ARCHITECT |
| N4-17 | INFO | **No dead code found** anywhere in `scripts/`. Drift found: `gitenv.py:10-12` misdescribes its own history (one named copy *delegated* rather than being hand-copied, and it omits the `gen_handoff.py` copy) — doc-vs-code drift inside the module written to end drift | UNOWNED | BUILD-CAND (low) |
| N4-18 | DEFECT | **The contract's own locators were stale** — `_git` cited at `:3004` (measured `:2998`), callers off by 6–17 lines, and "7 of 21 `subprocess.run` with `env=`" measures as **6 of 19**. This is the `/preflight` class the repo already has a command for (see N2-05) | `[#483]` closed | INFO |
| N4-19 | INFO | Locator correction: **`scripts/validate_audit_casing.py` does not exist in the hub** — it is the *consumer-side* name, recorded as a declared d1 divergence at `.methodology.yaml:20-25`. Hub-side is `validate_hermetization` Rule B | — | INFO |
| N4-20 | INFO | **What the lane found healthy, listed as part of the finding:** `ALL_CHECKS` integrity; the `check_mermaid_theme_directive` retirement (asserted un-un-retirable); `carrier_docs`' containment guard; `gitenv`'s by-path loading (proved adversarially with decoy modules on `PYTHONPATH`); `journal_anchor`'s posture; `_rmtree_guarded` reused by import; CI's uv-pin self-check | — | INFO |

**N4 rulings requested:** 1 … 4 → §7.

---

## 5. N5 — Library-first sweep

Source: `docs/audits/2026-08-09-technical-night-n5-library-first-sweep.md` (498 lines).

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| N5-01 | **REFUTED** | **The premise that `audit.py` is full of generic linting is FALSE, and the inverse is true.** 0 of 41 checks is generic lint — every one encodes ADR-cited policy with a repo-specific constant. A subagent's "14 of 41 are generic" label meant *portable across the fleet*, not *off-the-shelf-replaceable*; the lane corrected it rather than passing it through | — | SETTLED |
| N5-02 | **DEFECT** | **The generic hygiene layer a maintained tool does provide is absent entirely.** `.pre-commit-config.yaml` has exactly one remote repo (ruff); grep for the standard set returns **0**. **There is no secret scanning of any kind — bespoke or delegated.** The gap is not "we rebuilt a tool", it is "we never installed the tool and built policy instead" | UNOWNED | ARCHITECT |
| N5-03 | **SWAP 1** | Propagate the **already-ruled** `markdown_it` fence ADOPT (2026-08-03) to the two sites never examined: `audit.py:2714` `_strip_code_regions` diverges from CommonMark on **32 / 1,633** files (it anchors at column 0, so legal 1–3-space-indented fences leak into the `@import` scan `check_import_edges` gates on); `validate_doc_structure.py:113` on **8 / 1,633** (blind to `~~~`, inverts on 4-backtick inner runs). ~10 lines per site, **no new dependency** | UNOWNED | BUILD-CAND |
| N5-04 | INFO | Swap-1 caveat carried from the repo's own record: the 2026-08-03 codex review raised a HIGH against gating on `heading_open` tokens (it excludes headings inside HTML blocks and silently drops TOC entries). **Both swaps must use `markdown_it` to locate fenced *ranges*, never to token-gate** | — | INFO |
| N5-05 | **SWAP 2** | Land the `yaml.safe_load` ADOPT **ruled 2026-08-03 and still unimplemented** in `gen_claude_rosters.py:61-73`, whose regex key class `[a-z0-9-]+` **cannot match any underscore-bearing key**. Its twin `gen_intake_index.py` **was** migrated. ~12 lines, one file, in a generator feeding two `@`-imported CLAUDE.md fragments read at every session boot | UNOWNED | BUILD-CAND |
| N5-06 | **SWAP 3** | Adopt the standard `pre-commit-hooks` 6.0.0 set — **read-only members only**: `detect-private-key`, `check-added-large-files` (with a `JOURNAL.md` exclude), `check-merge-conflict`, `check-yaml`, `check-json`. 6 config lines, no code, prospective-only (which pre-commit does natively and this repo already has precedent for). Measured: 143 files carry trailing whitespace, 51 lack a final newline | UNOWNED | ARCHITECT (R1) |
| N5-07 | INFO | The 143/51 numbers are **not** an argument for a bulk rewrite — most sit in immutable audits that policy forbids editing. `trailing-whitespace` and `end-of-file-fixer` are deliberately **held back**: a rewriting hook collides with the append-only and immutability invariants | — | ARCHITECT (R1) |
| N5-08 | VERDICT | `check-jsonschema` 0.37.4 remains an **ADOPT-candidate** for `deploy/manifest-v*.yaml`; unchanged by tonight's evidence | `[#345]` OPEN P2/M adjacent | ARCHITECT |
| N5-09 | VERDICT | **WRAP** the 8 hand-rolled `sys.argv` CLIs in `argparse` — but 6 of the 8 are hook entry points taking zero or one argument, where `sys.argv[1]` is arguably honest. **Realistic saving ~40–60 lines. Worth doing opportunistically; not worth a lane** | `[#397]` adjacent | SETTLED |
| N5-10 | VERDICT | **WRAP (internal, not a library question)**: `_git()` is defined in **16 production files with three incompatible signatures**. GitPython/pygit2/dulwich are already REJECTED — GitPython shells out to git and inherits the same env problem. **Sequence with N4-F1/F6: the one-line fix first, the wrap after** | UNOWNED; `[#397]` adjacent | ARCHITECT |
| N5-11 | VERDICT | **WRAP (internal, low)**: repo-root discovery re-derived in 60+ files across 5 idioms. Consistency only; **no defect class demonstrated** | `[#397]` | INFO |
| N5-12 | **DEFECT** | **The closure-proposal store writes to gitignored `logs/`, so the evidence base for every closure decision is invisible to exactly the cloud sessions being asked to do the work.** `review_closures` also silently picks the newest file by filename sort, so a stale run and a fresh run are indistinguishable | `[#487]` OPEN P2/L; `[#454]` OPEN P2/S; `[#277]` OPEN P2/M | ARCHITECT (R2) |
| N5-13 | PROPOSAL | Durable shape (design only, nothing built): keep the store **derived**, make the **decision** durable — a tracked append-only `logs/CLOSURE-DECISIONS.jsonl`; add `--since <sha>` so any session can reproduce a window byte-for-byte; and make `review_closures` **refuse** a proposals file whose `head_commit` is not current HEAD | `[#487]` | ARCHITECT (R2) |
| N5-14 | **NARROWS** | **`lychee` KEEP — do not adopt.** The raw scan looks damning (157 broken local links, 24.4%) and **inverts when split by editability**: living docs carry 29 local + 233 anchor links with **0 real breaks**; all 153 breaks live in artifacts ADR-101 and CLAUDE.md §4 forbid editing. A link checker would emit 153 findings policy prohibits fixing and 0 it permits. **Both "0 real" figures survived adversarial checking** (4 were the lane's own extractor false-positiving on citation prose; 4 were GitHub duplicate-heading suffixes, each confirmed) | — | SETTLED (narrows the 2026-08-06 open candidate) |
| N5-15 | **DECISIVE** | **There is no corpus-wide schema surface for a validator to bind to**: `tasks/` 248/249 with frontmatter (and already schema-gated by `validate_backlog` + `task_tree_coherence`), `docs/audits/` **57 of 442 (12.9%, and all 57 are batch manifests)**, ADRs **1 of 83** (they use a bullet-list header). Adding a schema library governs `tasks/` only — duplicating a working gate — or requires *inventing* frontmatter for 385 audits and 82 ADRs, which is a doctrine change, not a library adoption | — | SETTLED |
| N5-16 | VERDICT | **KEEP** handoff templating: `gen_handoff` splices FILL-IN regions **byte-for-byte** from the prior bundle so hand-written architect content is never clobbered. **Jinja2 renders forward; it does not preserve a human's edits in the output it overwrites.** Probes are deliberately *not executed* — so "generic templating plus a test runner" does not describe the engine | — | SETTLED |
| N5-17 | VERDICT | **KEEP** batch/lane orchestration — **it does not reimplement git.** `worktree_seed.py` never calls `git worktree add`; teardown leaves removal to the caller; `/lane-integrate` is a documented serial walk plus a checklist. The git-native primitives are **already delegated; what remains is policy** | — | SETTLED |
| N5-18 | VERDICT | **KEEP, unjustified** — `.worktreeinclude` is a 3-line bespoke manifest where git sparse-checkout exists. Named per the contract's instruction to flag accidental bespoke **even when replacing is not worth it** | — | INFO |
| N5-19 | VERDICT | **REJECT `mkdocs`** — the eight generators emit marker-delimited blocks into existing living files, not a site; there is nothing to build. `mkdocs` is also two years stale by release date | — | SETTLED |
| N5-20 | DEFECT | **Two generators are unguarded**: `generate_floor.py` is operator-only and hash-guarded downstream, but **`gen_doc_counts.py` has a `--check` mode at `:136-150` and no hook calling it** — a 6-line config addition, not a library question | UNOWNED | BUILD-CAND |
| N5-21 | VERDICT | **KEEP** `propose_closures.py`'s fence/quote stripper — it handles `~~~` *and* equal-length inline pairing and operates on **commit messages, not markdown**. Reclassified from "unjustified" to "justified" by the lane on inspection | — | SETTLED |
| N5-22 | MEASURE | Whole surface: **98 Python modules, 36,806 LOC production, 38,317 LOC tests, 2,441 test functions** — tests outweigh production 1.04:1. `audit.py` is the centre of gravity by every measure (**43% of its lifetime commits landed in the last 30 days**) | — | INFO |
| N5-23 | DEFECT | **The clone arrives shallow and a lane that does not `--unshallow` first will silently report a floor as a measurement** (310 commits vs 4,723). Worth adding to the cloud-lane preamble | `[#453]` OPEN P2/M | BUILD-CAND |
| N5-24 | DEFECT | **Second witnessed instance of the uv-pin class** (first: 2026-08-08 item 8c, verdict left open). *"Two instances in six days is the shape that usually earns a ruling."* Tonight it is **four** — see C-1 | `[#453]`; ADR-106 governs the pin | ARCHITECT (R3) |
| N5-25 | INFO | **Method honesty:** where a measurement needed a library this container lacked, the lane did **not** install it — it wrote a stdlib CommonMark oracle from the spec and replicated the repo's own `_slugify`. Consequently the §4 divergence counts **should be re-measured against `markdown-it-py` itself before the swap lands**; the lane expects them to hold or grow and marks that expectation UNVERIFIED | — | INFO |
| N5-26 | INFO | GitHub API is 403 through the proxy, so **every maintenance-health, star and commit-activity claim is UNVERIFIED** and tagged. PyPI versions and release dates **were** verified | — | INFO |

**N5 rulings requested:** 1 … 5 → §7.

---

## 6. Integrator findings — this arc, not the lanes'

These arose during integration and belong to no lane report. They are indexed here because the
architect reads this file, not the packet's process log.

| # | Sev/Class | Finding | Owning row | Disp. |
|---|---|---|---|---|
| I-1 | **HIGH** | **The ADR-110 declared-integration-arc exemption granted this batch nothing.** `batch_manifest.exempt()` needs both an open manifest **and** `LANE_BRANCH_RE = ^worktree-lane-…$`; cloud lanes are `claude/<slug>`. Verified live before merge #1: all five branch names return `False`. The manifest was correct and enumerable — **the batch it declared simply could not use the exemption it was written to obtain.** Consequence: `check_journal_spine_anchor` (a FAIL, gating `audit-health` at pre-commit) treats every lane merge as unanchored, so the merge queue wedges at the first *conflicted* merge exactly as batch 3 did | **`[#510]` OPEN P2/M is adjacent but does not cover it** — that row is scoped to the exemption being too *loose* (self-grantable by rename); this is the same predicate being *unreachable*. Its proposed fix (resolve against a manifest-declared lane roster) **would** cover this case | ARCHITECT |
| I-2 | DEFECT | **The manifest itself records the assumption that failed** — "any `worktree-lane-*` `--no-ff` merge qualifies while a batch is open" is quoted accurately from `batch_manifest`'s honest limits, and is simply not reachable by a cloud batch. The manifest also *declines to enumerate lane branch names* on the ground that cloud branch names are assigned at launch — which is precisely the input `[#510]`'s fix needs | `[#510]` | ARCHITECT |
| I-3 | **PROCESS** | Worked around **without any bypass**: the JOURNAL entry anchoring the queue was written and merged **before** the merge queue ran, naming each lane branch's tip SHA. This is the ADR-85 §A7 predicate used exactly as specified (a merge is anchored by a SHA it *introduced*), not a loophole — but it means **the batch's own JOURNAL is split across two entries**, and that is a divergence from the contract's "JOURNAL entry as the LAST commit" (see §8) | — | INFO |
| I-4 | **DEFECT** | **Three of five reports landed at a path the manifest's lane table does not declare** (N2, N3, N5 — §5 of the packet). The manifest states the table is load-bearing twice: it is the file-disjointness guarantee *and* closure condition 1. N4 caught its own instance and repaired it by rename before pushing; the other three did not. Merged on their merits — content is unambiguous in all three — with the divergence named | `[#505]` (batch protocol); the class is N2-15/C-3 | ARCHITECT |
| I-5 | DEFECT | **N5 did not regenerate `docs/audits/README.md`**, which the batch mandated and which `audit-index-freshness` gates. It could not have been caught in the container: `.git/hooks/` held only samples and every `uv run --locked` entry refused. Regenerated by the integrator at merge time | `[#453]` | INFO |
| I-6 | DEFECT | **N4's report carries leaked tool-call markup at EOF** — a literal `</content>` and `</invoke>` after its last section. Merged **as authored**: `docs/audits/` is immutable and the branch commit predates the merge, so silently editing a lane's artifact is the wrong repair. Cosmetic (it trips no gate), but it is in a file that is now permanent | — | INFO |
| I-7 | INFO | **The suite baseline is ~9 minutes, not ~32.** Measured on bare `main` before any merge: `1 failed, 2716 passed, 3 skipped, 1 xfailed in 526.76s (8m46s)`, zero worktrees registered. This independently corroborates N3 §1a — the 31m43s figure in the record is the *inflated* one, and any planning that budgets ~32 min per suite run is budgeting the defect, not the suite | N3-25/N3-26 | INFO |

---

## 7. Every `Needs a ruling` item, in one place

**38 items across five lanes.** Full text lives in each report's final section; this is the roll
call so none is lost. Counts per lane are the closing packet's `Needs a ruling` figures.

**N1 (16)** — R-1 is intake #28 §B binding? · R-2 `[#511]`: which handoff load is cut? · R-3
`[#499]`: is the FP count actually reported at each seal? · R-4 `[#301]`→`[#298]` deferred-on-
deferred, which end opens? · R-5 `[#492]`: has Grok 4.6 released? *(OPERATOR — external fact)* ·
R-6 `[#181]` unadjudicable from a cloud clone · R-7 `[#240]`: does "mesh baseline n=2" count as met?
· R-8 `[#322]`: the C4 research exists and was ruled against · R-9 which filter does "open backlog
< 100" mean — 161 or 194? · R-10 what counts as a "dispositioned owner"? · R-11 `[#218]` (P1)
rides a re-scoped `[#487]` · R-12 should a deferred row keep an action priority? · R-13 the 15
expired pegs are decisions owed today · R-14 the 153 unexamined closure proposals *(OPERATOR)* ·
R-15 should `uv sync --group analytics` be the documented suite invocation? · **R-16 the
`audit-health` gate cannot pass in a cloud clone and tonight dispatched five of them** *(see C-1;
`[#453]` owns it)*.

**N2 (7)** — R1 Rule C's scope: accept announced-class-only with the omission gap documented, or
mandate a template name for manifests? · R2 the `batch:` field's failure direction (the exemption's
safe direction is `gen_handoff`'s unsafe one) · R3 `docs/batch/` and ADR-101 — amend, misclassify,
or a third home? · R4 are committed lane contracts immutable? · R5 the probe-manifest three-seal
pruning rule · R6 n=5 is unverified *(OPERATOR — local reflog)* · **R7 confirm the two-step
`LANE_BRANCH_RE` sequence** — provisioning-enforcement *before* tightening, or nine of ten
historical lane shapes become non-exempt.

**N3 (6)** — 1 take cheap-win #2 (git-tracked corpus) in the two test files? · **2 rule the bigger
lever that has no number on it** — "an integration suite does not run while lane worktrees are
locked" · 3 the 8m23s/8m59s divergence — amendment marker or below the bar? · 4 the contract's
`2h43m` / `~9 minutes` figures are unlocated *(OPERATOR — name the surface)* · 5 amend
`/lane-integrate` §2 to one suite on the merged result? · 6 is "three passes, same shape → replace
the mechanism" worth a standing ruling at n=1?

**N4 (4)** — 1 **which `LANE_BRANCH_RE` is canonical?** (until ruled, no code change is safe) ·
2 is `audit.py`'s fleet-automation write path compatible with Layer-2 invariant #4? · 3 is `_git`'s
missing scrub a defect or an undocumented exemption? · 4 cloud-runtime gate coverage — if nightly
Routines run in this container class, that is a standing hole *(C-1)*.

**N5 (5)** — 1 do rewriting pre-commit hooks get in, or the read-only set only? · 2 does the
closure-decision ledger get born, and as what? · 3 is the uv-pin class ready for a decision?
*(C-1 — now four witnessed instances)* · 4 **who owns propagating a ruled adoption?** *(C-5 — now
n=3)* · 5 `docs/audits/` frontmatter is 12.9% *(informational; no action requested)*.

**Three rulings are asked twice by different lanes and should be adjudicated once:**
`LANE_BRANCH_RE` canonicality (N2 R7 + N4 R1, plus I-1/I-2); cloud-runtime gate coverage (N1 R-16 +
N4 R4 + N5 R3); and the uv pin (N5 R3 + N1 R-15's sibling).

---

## 8. What this index does not do

- **It adjudicates nothing.** No row born, closed, killed or re-pegged; no peg re-dated; no
  `Needs a ruling` item answered. Every proposal above is a candidate for the batch-4 planning GO.
- **It implements nothing.** Not one mechanism, swap or fix from any report was built.
- **It does not re-verify every claim.** The **ownership** column was re-resolved live against
  `tasks/*.md` and the corrections are folded in; the reports' internal measurements were not
  re-run, except where §6 says otherwise (I-1 and I-7 were measured by this arc).
- **It does not resolve the contradiction it surfaces.** N3-25 (the largest measured saving) rests
  on inference, and the lane says so against its own recommendation. That tension is the
  architect's to resolve, not the index's to smooth over.
