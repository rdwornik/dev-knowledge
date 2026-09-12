# LANE `lane-x-691-routing-half-a` — end-of-lane packet

> **X1-4 Half A: the routing mechanism, Claude-only.** Telemetry, registry, router and re-rank
> built and trip-tested with **no non-Claude provider ordered**.
>
> Contract: `docs/audits/2026-09-11-technical-batch-x-launch-contracts/LANE-x-691-routing-half-a.md`
> (landed on `main` mid-lane by the integrator — see *Findings* 1).
> Rows: `[#691]` (advanced, stays OPEN for Half B) · `[#694]` (one of four modules disposed).
> Branch: `worktree-lane-x-691-routing-half-a`. Commit-and-STOP; no merge, no push to `main`.

## 1. What changed

Five commits, in the order AX22-5 fixes and for the reason it fixes them — each step is the
next one's evidence.

| # | Commit | Step | Surface |
|---|---|---|---|
| 1 | `2c91d142` | GO carriage | `tasks/691-*.md`, `tasks/694-*.md` |
| 2 | `bffe8b7c` | 2 · telemetry | `scripts/cost_usage_telemetry.py`, `tests/test_routing_telemetry.py` |
| 3 | `b191ef78` | 3 · registry | `ecosystem/provider-registry.yaml`, `ecosystem/schema/provider_registry.py`, `scripts/provider_registry.py`, `deploy/manifest-v1.5.0.yaml`, 2 test modules |
| 4 | `ce10eec7` | 4 · router | `scripts/provider_router.py`, `scripts/graph_queries.py`, `tests/test_provider_router.py` |
| 5 | `09958f85` | 5 · re-rank | `scripts/provider_router.py`, `tests/test_provider_rerank.py` |

### The exists-before-build answer (AX9-4), which reshaped steps 2 and 3

Quoted rather than asserted, before anything was written:

```
uv run --locked python scripts/graph_queries.py process-list
  -> 161 processes; none routing-, ranking-, provider- or tally-shaped
grep -iE "rout|rank|provider|telemetr" ecosystem/organ-index.md
  -> 2 hits, both CHECKERS: `provider-registry-agreement` (pre-commit), `conformance-hub.js`
```

No **organ** answers the need, so the router is a genuinely new one. But AX5-1's telemetry
**already existed**: `scripts/cost_usage_telemetry.py` has emitted model, tokens and cost per
call since DM-2. Shipping a second emitter beside it would have been the exact failure AX9-4
exists to refuse, so step 2 became an **extension** — and what it extended was the missing
right-hand side of AX21-2's ratio, not the ratio itself.

Likewise `ecosystem/provider-registry.yaml` already existed and `scripts/routing_agreement.py`
is the router's nearest neighbour. Neither was folded into: the registry gained a **third**
collection (which `[#691]` is explicit is "a third thing, not a field rename"), and the
agreement checker was left alone, because asserting that two copies of one table agree and
choosing between candidates are different acts on different data.

### Step 2 — the tally records the work product, not only the call

`emit_genai_span` gains `role`, `outcome`, `reviewed_by`. AX21-2 names the input verbatim:
*"every call records model, tokens, cost **and outcome** (tests green? review HIGH-free?)"*.
The first three were already there; nothing recorded whether the work was any good, which role
the call served, or who reviewed it.

Three decisions worth carrying forward:

- **`unknown` is a first-class outcome.** An unjudged call must be *visible* as unjudged.
  Omitting the field instead makes it count as neither pass nor fail — which reads as a pass to
  any rate computed `passed / (passed + failed)` and silently inflates every provider's
  measured rate, defeating the "measured, not declared" clause itself.
- **The tokens are `passed/failed/unknown`, not `telemetry_emit`'s `pass/block/error`.** Those
  label a *gate fire*. Sharing the token `pass` would make two different facts
  indistinguishable in any join across the two stores.
- **The AX22-2 check falls back to `request_model`** when no response model was recorded —
  otherwise a caller who simply omits `response_model` buys an unchecked self-review, turning
  an optional field into a bypass.

### Step 3 — `[#691]`'s three legs, each absent for a different reason

| Leg | Where it landed |
|---|---|
| **(a) ORDER** | `roles:`, a third collection — six AX21-1 roles, each an ordered provider list |
| **(b) ADMISSION** | per-entry `admission:`, reusing `RoleAdmission` verbatim rather than forking a grammar |
| **(c) LICENCE** | per-provider `licence:` — the row measured this one as absent *entirely* |

**The reading that makes the Done-when coherent.** Taken flat it contradicts its own lane: it
says only admitted, licence-permitting providers "may appear", while the contract *requires*
`agy`, Grok 4.6, Copilot Enterprise and Codex terra to appear as NOT ADMITTED entries so the
router's refusals bite on real rows. Both hold once **LISTED** and **ELIGIBLE** are separated —
a provider is listable in any state; only admitted + licence-permitting + on-allowlist is
routable. So *"listing a non-admitted provider fails"* is enforced as *"**admitting** one
fails"*, which is the reading that leaves the clause with teeth.

**AX22-5's allowlist** is a new top-level `providers.allowed` in `deploy/manifest-v1.5.0.yaml`,
keyed by the nine ADR-104 fleet ids and asserted in both directions against
`ecosystem/parity-surfaces.yaml`. Inert to `deploy/tool.py` exactly as `components:` and
`doc_shapes:` are. `release_lint --version 1.5.0`: 0 FAIL, 7 pass, 1 pre-existing WARN.

### Step 4 — four refusals, three of them scoped narrower than "always"

| Refusal | Scope | Clause |
|---|---|---|
| `off-allowlist` | every role | AX22-5 (carries no role qualifier) |
| `not-admitted` | `implement`, **plus any entry that asks** | done-contract item 1 + AX22-2 |
| `licence` | every role | `[#691]` leg (c) gates *"the use"* |
| `reviewer-is-producer` | where the registry sets the flag | AX22-2 |

**The pair that reads like a contradiction and is not:** Codex terra is recorded NOT ADMITTED
and remains the routable reviewer. The done-contract scopes the admission refusal to
`implement` alone, so an unadmitted *reviewer* is refused by nothing — and current review
practice is untouched by Half A, which is the correct outcome. Widening that gate would have
been a behaviour change smuggled in under a mechanism commit.

**A RED test forced a real design change.** A role-level admission gate was the obvious
encoding until `test_refusal_4` went RED: AX22-2 says *"the reviewer is Grok (**after
admission**) or Sonnet"*, conditioning **one entry** on admission while leaving its role
ungated. Gating `review` would refuse Codex too; leaving it ungated routes to Grok before its
admission. Neither is the clause. So `RoleEntry` gained `requires_admission`, set on that one
entry, and the chain now lands on Sonnet by routing rather than by an edit.

**The router places no call** — no `subprocess`, no HTTP client, no provider SDK — and that is
asserted by walking the module's AST rather than grepping it. (The first draft grepped, and
went RED on the module's own docstring, which uses the word `subprocess` to say there is none:
the check was matching prose *about* the property while claiming to measure it.)

### Step 5 — the re-rank says when it measured nothing

The failure this is written against, from the contract: *"a router re-ranked on nothing measured
is a fixed list wearing a router's name."* A re-rank that quietly returns the declared order
looks identical to one that measured and confirmed it. So every result carries `measured` and
`basis`, and the three ways it can decline to reorder are three different sentences.

Metric decisions: `judged` excludes `unknown`; the sample floor is AX22-1's ten rather than a
second number invented here; **no recorded cost means no score, not a sentinel** (infinity
would make a subscription-metered provider unbeatable, zero would make it last — both
fabrications); unscored providers **hold** their declared position rather than being appended,
because "we learned nothing" is not the same claim as "measured worst".

## 2. The live state — what the mechanism says today

```
$ uv run --locked python scripts/provider_router.py report
Recorded admission state -- NOT a measurement (AX22-1's bar is Half B's).

  anthropic            admitted in [all six roles]    licence: permitted
  antigravity          NOT ADMITTED                   licence: permitted
  copilot-enterprise   NOT ADMITTED                   licence: unknown
  openai               NOT ADMITTED                   licence: permitted
  xai                  NOT ADMITTED                   licence: permitted

$ uv run --locked python scripts/provider_router.py rerank implement
  order   : ['anthropic']
  measured: False
  basis   : no measured calls for this role in the tally -- the declared order stands, and it
            is DECLARED rather than confirmed. Half A places no calls (AX23-2), so an empty
            tally is this arc's expected state

$ uv run --locked python scripts/provider_router.py route review --produced-by openai
  [0] openai      reviewer-is-producer:  (AX22-2: reviewer != producer, always)
  [1] xai         not-admitted:          (AX22-1: >= 8 of 10 green on first review)
  [2] anthropic   OK  eligible
```

Every non-Claude entry reads **NOT ADMITTED**, and **reporting that is not the same act as
measuring it** — the report says so in its own first line rather than leaving it to the reader.

## 3. Open items

### For the OPERATOR — one functional question, recorded and not answered

**May the BY-Product-Development enterprise Copilot seat be spent on this repository's work?**

The registry already recorded (before this lane) that `copilot-enterprise` consumption is
metered to that **employer** org seat. Whether that licence permits this use is a *functional*
question, so under ADR-108 §A it is the operator's, not this seat's. It is recorded
`licence: unknown` — a first-class verdict, neither a soft refusal nor a soft permission — and
the schema refuses to admit anything under it.

The consequence, stated so the entry is actionable: `copilot-enterprise` is ineligible **twice
over**, and the two blocks are **independent**. An admission measurement would not clear the
licence; a licence ruling would not admit it. AX21-1 places it *first* on bounded implement
work, so this question gates a position the role table already wants filled.

### Proposed diffs — named, not made

1. **A gate asserting every role resolves to at least one eligible provider.** The router makes
   it a five-line check, and it would catch a registry edit that strands a role. Not made here:
   a NEW pre-commit hook is an **AX4-1 floor-declaration event** requiring an
   `ecosystem/parity-surfaces.yaml` registration, and that surface is not this lane's to write.
   It is also what would let `scripts/provider_router.py` drop off `ORPHAN_DISPOSITIONS` by
   being *wired* rather than dispositioned.
2. **Retire the stale `scripts/worktree_seed.py` disposition row** — one deletion. See
   *Findings* 3.
3. **Fix or re-rule `tests/test_routing_agreement.py`'s `sol` assertion** — see *Findings* 2.

### Inherited by Half B, so it is not rediscovered

- The **two first acts** the full-scope contract opened with, both Grok-specific and both
  deliberately not run here: read the grok account's usage-limit cause (AX21-4), and verify
  grok's token-ceiling flag (AX21-3 / R1-4(b) / A7-5 — *a CLI that cannot enforce a token
  ceiling by flag is not ordered*).
- `record_routing_call()` is the seam to call after each trial task. It **re-checks the route
  and refuses to record an ineligible one** — which closes the one path by which an unadmitted
  provider could earn a position without ever being admitted, since the re-rank treats that
  table as evidence.
- Admission is lifted by **measurement, not by editing the registry**. The schema refuses an
  `admitted` verdict without provenance, under a non-permitting licence, or against a model row
  recording the same role refused.

## 4. Findings and deviations

1. **A measurement of mine went stale mid-arc, and the record was replaced rather than
   appended to.** Before step 0's re-sync, AX23-1 and AX23-2 resolved **nowhere** in-repo, and
   the GO-carriage commit was first written claiming exactly that. The integrator then advanced
   `main` `b71acdf8 → f1711e3d`, landing this lane's own contract, and both clauses now resolve
   in two files. True when measured, false afterwards. The carriage stands on the reason that
   survives the correction — a row should carry what binds it — and the stale claim is gone
   from both the commit and the row.

2. **Pre-existing RED on `main`, reported not absorbed.**
   `tests/test_routing_agreement.py::test_the_live_table_is_well_formed` asserts
   `adversarial == ['sol']`; the table says `['codex']`. Commit `5be038ff` rebound that role off
   an absent CLI on 2026-09-05 and did not update the test. **Not fixed here**: the table's own
   comment says *"Restore `sol` here once it is installed"*, so which of the two is the defect
   is a judgement belonging to whoever owns the rebind.

3. **A cross-lane collision neither lane could have seen.**
   `tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
   fails on `scripts/worktree_seed.py`: the orphan register holds a disposition row for it while
   `.claude/settings.json` now *triggers* it. Two wave-1 lanes did this between them —
   `eccb5814` (`[#716]`) wired it, `11c7c8b1` (`[#664]`) built the register carrying the row.
   The register's own convention names the remedy ("drops off this list by being wired rather
   than by being dispositioned"), so the fix is deleting one row. **Not done here** — the row
   belongs to `[#664]`'s arc.

4. **The silent-rule ratchet fired, and the drain was the remedy rather than a dodge.**
   Step 3 first landed +6 normative keywords in `ecosystem/provider-registry.yaml` (in scope for
   `silent-rule-v5`). Drained by **moving each statement to the module that enforces it** — the
   two verbatim AX21-1 quotes now live on `Role.rerankable` and `Role.excludes_producer` and are
   cited from the YAML. A rule stated in a YAML comment is silent by construction; the same rule
   on the validator that refuses violations of it is mechanized. Back to baseline 447. No ruling
   sought, no baseline raised.

5. **Declared single-hook bypass on four commits:** `SKIP=doc-counts-pytest-freshness`. The new
   tests move the `pytest_collected` claim in the **generated** `ecosystem/doc-counts.md`; the
   contract makes the integrator gate-of-record for it (Q1). One named hook, named in each body.
   `--no-verify` was not used anywhere in this lane.

6. **The lane's branch was provisioned off a sibling lane's branch, not off `main`** — it
   carried six unmerged commits from `worktree-dispatch-x14-freeze` at boot. Resolved on its own
   when the integrator merged that branch; recorded because `[#716]` (`worktree.baseRef` unset)
   is the row that owns it and this is one more instance.

7. **`[#691]`'s Done-when cites an admission bar that does not resolve to a live one.** Intake
   #75 is `status: DRAFT` and awaiting ratification. **AX22-1's ≥ 8-of-10** is the
   operator-ratified instantiation and is what the registry encodes. Recorded in the row rather
   than substituted silently.

## 5. Verification

- **Targeted: 222 passed** across `test_provider_rerank`, `test_provider_router`,
  `test_provider_roles`, `test_routing_telemetry`, `test_provider_registry`,
  `test_provider_registry_schema`, `test_cost_usage_telemetry`, `test_telemetry_emit`.
- **RED-first on every step**, as the contract requires: step 2 → 14 failed on
  `TypeError: unexpected keyword argument 'role'`; step 3 → the registry's own data was wrong
  (Codex terra marked admitted) and the test caught it; step 4 → 19 collection errors, then 7
  failures of which **six were my test expectations rather than the code**; step 5 → 14 failed.
- `ruff check` clean on every file this lane touched.
- Full-suite state at close: **§6 below** — 59 failures, **measured** identical at the
  pre-code baseline and at the tip, so zero of them are this lane's.

## 6. Full-suite result

**The suite is NOT green, and none of it is this lane's.** That second clause is a measurement,
not a claim — the distinction is the whole reason this section is a paired experiment rather
than a sentence.

### The measurement

Two whole-suite runs, one at each end of this lane's code:

```
ref                                        failed  passed  skipped  wall
f1c51be1  baseline (main + clause carriage)    59    5994       11  1369.91s
09958f85  lane tip (all four code commits)     59    6071       11   997.42s
```

`f1c51be1` is the merge commit carrying `main` plus **only** the clause-carriage commit
`2c91d142` — that is, this lane's rows but none of its code. The four code commits under test
are `bffe8b7c` (step 2), `b191ef78` (step 3), `ce10eec7` (step 4) and `09958f85` (step 5).

Comparing the two `short test summary info` blocks node-for-node:

```
PRE-EXISTING (fails at baseline AND at tip)  : 59
NEW AT TIP   (passes at baseline, fails at tip):  0
FIXED BY TIP (fails at baseline, passes at tip):  0
```

The failure set is **identical**, not merely the same size. The pass count rises by
**exactly 77**, and `pytest --collect-only` over this lane's four new test modules
(`test_routing_telemetry`, `test_provider_roles`, `test_provider_router`,
`test_provider_rerank`) collects **exactly 77**. So the whole delta between the two runs is
"77 new tests, all passing" — no existing test changed outcome in either direction.

### A second, independent pass at the same question

Before the paired whole-suite runs, the 31 modules that carry the 59 failures were run at both
refs in five identical batches. That produced **49 failures at baseline and the same 49 at
tip** — again 0 new, 0 fixed. Ten of the 59 do not reproduce in batches at all (they need
whole-suite population), which is exactly why the batched pass was not treated as sufficient
and the whole-suite pair was run.

### What is honestly unresolved

- **The worker counts differed.** Baseline ran `-n 6`; the tip run ran the default `-n auto`
  (16 on this box). Not a choice — the first baseline attempt at `-n auto` was **killed by the
  OS for memory pressure** partway through, so the retry halved the workers. The sets came out
  identical across *different* distributions, which makes the failure set worker-invariant and
  strengthens the conclusion rather than weakening it; but the two runs are not byte-identical
  invocations and this section does not pretend they were.
- **Why 59 fail on `main` is not this lane's question and is not answered here.** They span 31
  modules — `test_fleet_analytics` (17), `test_gen_handoff` (5), `test_normalize_headers` (4),
  `test_funnel_lifecycle` (4), `test_cloud_provisioning` (2), `test_canonical_docs` (2), and 25
  modules with one each. Two were separately traced to provenance during this lane and are
  findings 2 and 3 above. The remaining 57 are an integrator-surface fact: the suite was
  **already 59-RED on `main` before this lane wrote a line of code**.

### The contract's own words, applied to this section

Step 6 asks for `pytest` green. It is not green, and this lane cannot make it green without
editing 31 modules outside its declared footprint — which the prohibitions forbid. The honest
discharge available to a lane in that position is the one taken here: **measure** which
failures are attributable to it, report the number, and leave the 59 where they live. Asserting
"none of them are mine" from the fact that the targeted tests pass would have been the same
move the re-rank step is forbidden to make — reporting something in place of measuring it.
