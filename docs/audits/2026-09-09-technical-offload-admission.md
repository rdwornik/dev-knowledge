# The `offload` admission gate, and the Copilot route it REFUSES — end-of-lane artifact

Consumers: `[#627]` (the admission precedent this lane follows, and the row whose REFUSE-shape
this verdict copies) · intake #75 (the `offload` role, whose admission this measures).

> **Class:** technical · **Date:** 2026-09-09 · **Lane:** `lane-v-000-offload-admission`
> (batch V, V-8 by AMEND-BATCH-V-002 §2) · **Branch:** `worktree-lane-v-000-offload-admission`
> **Frozen contract:** `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-000-offload-admission.md`
> **Evidence bundle:** `docs/audits/2026-09-09-technical-offload-admission-artifacts/`
> — `MEASUREMENT.md` (step 2) · `DISPATCH-MODEL-WITNESS.md` (step 4) · `copilot-answer.json`
> and `copilot-usage.json` (the live run, re-adjudicated by the suite).

## 1 · Headline

**The gate exists and is measured. The Copilot route is REFUSED — on the mechanism, not on the
reading.**

- **Seeded-defect cases the admission REFUSES: 0 → 16.** Every one attributable to its own
  seed. A positive control is ADMITTED in the same run.
- **`-Model` reaches the dispatch line, and reaches the argv that actually runs.** Two legs,
  witnessed live on the deployed module.
- **The live Copilot run met the retrieval bar and was refused anyway.** 4/4 locators exact,
  all three planted defects found, no verdict returned — and REFUSED on two reproducibility
  legs that no amount of good reading repairs.

## 2 · The gate — where it lives, and why not where it does not

`scripts/offload_admission.py` (logic + a Click CLI), `tests/test_offload_admission.py`
(42 tests). The shape is `scripts/routing_agreement.py`'s, reused rather than reinvented: a
logic module that reads files and compares strings, Layer-2 clean — it runs no CLI, writes no
file the caller did not ask for, and touches no L0 surface.

**It is deliberately NOT a registered `audit.py` check**, and that is a decision with a reason
rather than an omission. The `ALL_CHECKS` count is pinned in more than one place, `audit.py`
and `tests/test_audit.py` are outside this lane's declared footprint, and registering a check
mid-batch would RED four peer lanes' trees for a property none of them touches. The gate is a
command a human or a later organ runs; promoting it to a commit-tier check is a separate act
with a separate owner, and it should be taken *after* a route has actually passed it.

## 3 · The seeded-defect suite — the specification, re-measured

`python scripts/offload_admission.py --seeded-defects` **re-measures** the number; it does not
print a constant. Output today:

```
seeded-defect cases REFUSED by the offload admission gate: 16/16
  [refused] role-mismatch                    a record produced for a different role
  [refused] unknown-provider                 a route the registry's closed vocabulary does not name
  [refused] cli-mismatch                     a binary named by the record, not by the registry
  [refused] unpinned-model                   MEASURED 2026-09-09: `--model` refuses every id
  [refused] missing-attestation              [#492]: no record of what actually answered
  [refused] attestation-is-a-selection-mode  MEASURED 2026-09-09: self-reported `auto`
  [refused] substituted-model                [#492] verbatim
  [refused] empty-run                        an admission that passes because nothing was found
  [refused] unranked-finding                 ranked retrieval with no ranks
  [refused] duplicate-rank                   two candidates sharing a place
  [refused] verdict-bearing                  intake #75: the seat rules, closes or disposes
  [refused] locator-malformed                a locator with no line
  [refused] locator-escapes-corpus           the [#627] flagship failure
  [refused] fabricated-file                  a locator naming a file that does not exist
  [refused] fabricated-line                  a line number past the file's end
  [refused] locator-drift                    the quote is not at the line it cites
  [control] admissible record -> ADMITTED
```

**Three properties make this a measurement rather than a tally:**

1. **Each seed is ONE mutation of an otherwise admissible record**, so the suite asserts
   `verdict.codes == (code,)` — not merely *that* the case was refused but that it was refused
   **for its own reason**. A right answer for a wrong reason is a RED here.
2. **The positive control is load-bearing, not decoration.** A gate that refused everything
   would score 16/16 as well. `test_the_admissible_record_is_ADMITTED` is what separates the
   two, and its absence is how a seeded-defect suite quietly becomes worthless.
3. **Every seed is a recorded scar** — `[#492]`, the `[#627]` flagship failure, the 2026-09-05
   Gemini 6/6 locator bar and its "locator-exactness is not claim-correctness" caveat, intake
   #75's "never a verdict", the registry's own poisoned-name and `cursor` rows. Two of the
   sixteen were seeded from *this lane's own live run* (§5), not from theory.

## 4 · `-Model` reaches the dispatch line — the seam test

Full transcript: `…-artifacts/DISPATCH-MODEL-WITNESS.md`. Summary of why it has two legs:
`Start-DispatchLane` builds the argv array **and** separately interpolates the `DRY RUN --
would run:` string. They are written independently and can therefore agree in the printed line
while disagreeing in the executed one — the same declared-but-unbacked class as the
`gen_lane_contract` → `dispatch` seam AMEND-BATCH-V-002 §1 rules on. So:

- **Leg A** — three `-DryRun` runs: default → `--model opus`; `-Model sonnet` → `--model
  sonnet`; `-Model claude-opus-5` → `--model claude-opus-5`. The default plus two overrides
  show the printed value is the value passed, not a constant that happens to match.
- **Leg B** — `claude` shadowed by an argv-recording stub, run **without** `-DryRun`, so
  `& claude @claudeArgs` itself is exercised. Recorded: `--bg --model gpt-5.6-terra --effort
  xhigh --permission-mode bypassPermissions --worktree probe-model-live-d "<prompt>"`.

Witnessed against the **deployed** module (`~/.dispatch-helpers/…/DispatchHelpers.psm1`,
v1.6.0, sha256 `EA8B1A07…`), not the `win-tooling` source. No lane launched, no branch created,
tree and stash clean afterwards.

## 5 · The live Copilot run — the verdict, and the shape of it

The Copilot CLI was run non-interactively over the committed probe corpus (`PROBE_CORPUS` in
`scripts/offload_admission.py`, three planted defects — a contradiction, an unenforced rule, a
clause duplicated across two files). The corpus lives in the module, not as loose files, so the
instrument is reproducible: `--probe-corpus DIR` rebuilds it byte-for-byte.

### 5.1 · The reading half — it MET the bar

| property | result |
|---|---|
| planted defects found | **3 of 3** (both halves of the contradiction, the unenforced rule, the duplication) |
| findings returned | 4, ranked 1–4, no repeats |
| locators re-opened on disk | **4 of 4 EXACT — zero fabrications** |
| verdicts returned | **none** — candidates and locators only, as the role requires |

That is the `[#627]`/Gemini bar, met. Recorded explicitly so a re-run on a seat where the
mechanism works starts from a measured reading rather than from scratch, and so the refusal
below is not mistaken for a judgement about the model's competence.

### 5.2 · Why it is REFUSED anyway — two mechanism legs

```
ADMITTED: False
findings_seen: 4   locators_verified: 4
  - unpinned-model                   the record declares no `requested_model`
  - attestation-is-a-selection-mode  `served_model` is 'auto'
```

**Leg 1 — the model cannot be pinned on this seat.** `--model` refused **every** id tried,
including all three the CLI's own `copilot help config` documents:

```
claude-sonnet-5    -> Error: Model "claude-sonnet-5" from --model flag is not available.
claude-fable-5.1   -> Error: Model "claude-fable-5.1" from --model flag is not available.
claude-fable-5     -> Error: Model "claude-fable-5" from --model flag is not available.
(also refused: sonnet-5, claude-sonnet-4.5, claude-sonnet-4, gpt-5, gpt-5-mini,
 gpt-5.1, claude-opus-5, opus-5, gpt-4.1, claude-haiku-4.5)
```

The route answers perfectly well with no `--model` at all — so the server chooses, and the
choice is not the caller's. **This is the `cursor` precedent already recorded in
`ecosystem/provider-registry.yaml`**, reached by a different road: *"an undisclosed model is an
UNREPRODUCIBLE RESULT, and a lane whose result cannot be reproduced is not evidence."*

**One credit where it is due, and it is a real difference from `cursor`:** the CLI **refuses**
an unknown id rather than silently substituting one. That is the failure mode that cost a
window in `[#492]` and the one `gemini` exhibits, and Copilot does not have it.

**Leg 2 — the seat's self-report is not an attestation.** Asked what served it, the run
answered `"auto"`. The CLI's own `--usage-output-file`, written by the same call, says:

```json
"currentModel": "mai-code-1.1-flash",
"modelMetrics": { "mai-code-1.1-flash": { "requests": { "count": 1, "cost": 1 } } }
```

So the model is disclosed **post-hoc, by the CLI** — which is genuinely better than nothing and
better than `agy`'s envelope `status` field — but the seat itself does not know what served it,
and `auto` names how a model was *chosen*, not which one answered. A record whose attestation
is a selection mode is unattributable, and the gate says so.

### 5.3 · The verdict is a regression, not a paragraph

`copilot-answer.json` and `copilot-usage.json` are committed, and
`test_the_live_copilot_run_is_REFUSED_on_the_two_reproducibility_legs` re-adjudicates the
committed answer against a freshly-materialised corpus on every run. If a later change softens
either leg, or repoints `copilot-enterprise` in the registry, the suite turns RED.

## 6 · What this lane did NOT do, and why each is correct rather than incomplete

- **No `offload` row in `ecosystem/routing-table.yaml`.** The declaration that moved this lane
  into batch V asks for the routing row **on PASS** and a REFUSE verdict on FAIL. The verdict
  is REFUSE, so the row is not warranted — and this is the same separation `[#627]` records:
  a verdict discharges the *measurement*, never the two births (the role row, and routing a CLI
  to it). Independently, the row is outside this lane's declared footprint, and adding it would
  immediately FAIL `check_routing_agreement` against the L0 derived copy — which this lane is
  pinned out of repairing. Three reasons, any one sufficient.
- **No L0 edit.** `~/.claude/ROUTING.md` and the whole L0 surface are untouched.
- **No Copilot billing probing.** Ruled closed 2026-08-29. The `--usage-output-file` capture is
  a per-call statistic the CLI writes locally about this lane's own call; it reads no billing
  page and queries no account.
- **No field added to `provider-registry.yaml`.** Its schema is `extra="forbid"` and the row is
  a thin identity surface. The lane READ it and pinned the read with a test.
- **No `role_admission:` block written on a model row.** A REFUSE verdict *could* be recorded
  there, and deliberately was not: the schema requires a verdict to name a MODEL row, and the
  model that actually served (`mai-code-1.1-flash`) is not a row in `models:` today. Writing one
  would be registering a model id on the strength of a route the same document refuses — and
  creating a model row is a registry act outside this lane's footprint. Named as owed rather
  than done; §8 carries it.
- **No JOURNAL entry, no BACKLOG write, no index regeneration.** The integrator's surfaces.
- **`ecosystem/doc-counts.md` WAS regenerated in-lane** — a declared deviation, §7.

## 7 · Deviations, declared

1. **`ecosystem/doc-counts.md` is not in this lane's footprint and was edited anyway.**
   `doc-counts-pytest-freshness` is a **blocking** pre-commit gate on any commit that moves the
   collected-test count, and it cannot be deferred to the integrator — deferring yields zero
   commits. The delta is `5390 → 5432`, exactly the 42 tests this round adds, so ownership is
   arithmetic rather than assertion. Precedent for the shape: the SHEET-506 ruling that a gate
   outranks a contract's file list, and that the deviation is reported rather than absorbed.
   **The integrator should expect a conflict here** — every test-adding lane in the batch
   touches this one file.
2. **Two refusal codes were added to the gate AFTER the live run**, from what the run measured
   (`unpinned-model`, `attestation-is-a-selection-mode`). Declared because the seeded set is
   the gate's specification, and growing a specification from evidence discovered mid-lane is
   worth stating out loud rather than presenting as if it had been designed that way.
3. **`docs/audits/README.md` is left stale**, per `[#590]` — a lane landing an audit does not
   regenerate the index, and the hook is narrowed so it will not fire. The integrator
   regenerates once on the merged result. Stated so the owed regen is not invisible.

## 8 · What is owed after this lane

- **`intake #75` ratification** (Sitting 1, already scheduled). This lane measured the
  admission the intake describes; nothing here ratifies the role definition.
- **A `models:` row for whatever Copilot actually serves**, if and when a routing decision
  needs one. `mai-code-1.1-flash` is what served on 2026-09-09; it is in no registry row today.
- **The re-run condition, stated so it is checkable rather than aspirational:** this route
  becomes admissible when `copilot --model <id>` accepts an id **and** the seat's own
  `served_model` matches it. Both legs are mechanical; neither needs a judgement call. The
  reading half is already measured and does not need repeating.
- **`tokens saved` as a scorecard row** (intake #75 §1, `scripts/window_metrics.py`) is
  explicitly *not* started here: the intake makes it a number that follows admission, and
  admission was refused.

## 9 · Honest limits on this artifact

- **n = 1.** One live run, one corpus, one day, one seat. It is enough to establish the two
  mechanism legs — those are deterministic properties of the CLI, re-probed thirteen times for
  leg 1 — and it is **not** enough to characterise the route's retrieval quality. The 3-of-3
  reading result is an encouraging single draw, nothing more, and `[#627]`'s own history (a
  flagship item failing three consecutive draws) is the reason that distinction is drawn here.
- **The `-Model` witness proves argv, not behaviour.** It establishes that `claude` is invoked
  with the value passed. Whether `claude` honours it is a claim about a different program.
- **The gate adjudicates records; it does not produce them.** A record can be honest about a
  dishonest run. Nothing here detects a candidate that read the corpus, then wrote plausible
  findings from a locator scrape — only that whatever it returned holds on disk.

## 10 - Owed, APPENDED after landing (addendum to section 8)

> **Why this is a new section rather than a bullet inside section 8.** An audit is immutable
> and this lane's instruction is append-only: the owed item below belongs to section 8 by
> subject, and it is written here because inserting it there would edit landed text. Read
> section 8 and this section as one list.

- **`ecosystem/provider-registry.yaml` gains a `reviewer` ROLE ENTRY carrying an ORDERED
  fallback list.** For the integrator to file as a row; not started here.

  - **Admission is the entry condition.** Only a provider that has PASSED the seeded-defect
    bar may appear on the list. That is the same bar this lane built and ran, so the row
    inherits a mechanism rather than proposing one -- and it is what keeps the fallback list
    from becoming a list of whatever happened to be reachable.
  - **A quota hit on the current reviewer routes to the next ADMITTED provider automatically.**
    Automatically is the operative word: the fallback is worth having only if it fires without
    a seat noticing and re-dispatching by hand.
  - **The tally line records WHICH MODEL ACTUALLY REVIEWED.** A review tally that does not name
    its reviewer is the same instrument-layer defect this lane spent eleven passes removing
    from its own headline: a number that certifies something it never measured. If the run can
    silently change reviewers, the tally must say which one it got.
  - **Candidate fallbacks to run through the bar:** `grok`, `gemini`, `deepseek`. Candidates,
    not admissions -- each is a provider to MEASURE, and this lane's verdict on Copilot is the
    precedent for what a candidate failing the bar looks like.

  **Today: terra only, no fallback.** Witnessed in this lane rather than predicted: the pass-12
  review returned `You've hit your usage limit ... try again at 6:26 PM`, and the loop stalled
  ~50 minutes with no second reviewer to route to. The stopping rule -- loop until a pass
  returns nothing -- makes reviewer availability a dependency of lane CLOSURE, not merely of
  lane speed, which is what turns a stall into a blocked gate.
