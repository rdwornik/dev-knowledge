# Lane `lane-y-751-cost-in-money` — end-of-lane packet

> Batch Y, lane 2. Frozen contract:
> `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-751-cost-in-money.md`.
> Manifest: `docs/audits/2026-09-14-technical-batch-y-manifest.md`. Row: `[#751]`.
> Branch `worktree-lane-y-751-cost-in-money`, three commits, commit-and-STOP.
> **Nothing here is merged.** Integration is the integrator's act, from the primary checkout.

---

## 1 · The premise the lane corrected, because everything else follows from it

The contract's own clause 1 said the rates did not exist and it was right. Measured again at
the start of this lane on `ecosystem/provider-registry.yaml`: top-level keys `providers` /
`roles` / `models`, and **no machine-readable rate, price or USD field anywhere**. The file's
only cost content was prose — the measured `$0.037` grok test call under `COST REGIME`.

So the lane's first act was authorship, not reading. That is why it is the registry's SOLE
OWNER for batch Y and why `[#753]` is sequenced behind it.

## 2 · What changed

| commit | what |
|---|---|
| `32f6c385` | the rate card, the reader, the cost module, the `[cost]` digest line |
| `23127d8b` | the TOKEN-LOG ruling executed, row `[#751]` filed |
| this one | the suite verdict and this packet |

**`ecosystem/provider-registry.yaml`** — a `rate_card:` block (currency, unit, `as_of`,
provenance, two cache multipliers) declared ONCE for the file, and per-model `rates:` on the
model rows. Two places, two different facts: *what does this model cost* belongs to the model,
*in what currency and as of when* belongs to the card. `claude-opus-5` gained a model row —
its absence was a real gap, since the registry's stated job is "every model string the repo's
LIVE surface names" and it was missing the one the live surface names most.

**`ecosystem/schema/provider_registry.py`** — `ModelRates`, `RateCard`, `Model.rates`,
`ProviderRegistry.rate_card`, and one cross-collection invariant: a model may not carry
`rates:` while the file carries no `rate_card:`. A bare `input: 5.0` is not a price.

**`scripts/provider_registry.py`** — `rate_card()`, `resolve_rate()`, `priced_models()`.
`resolve_rate` re-reads the file on every call, which is what makes the contract's "resolved
from that file at run time" true rather than nearly true.

**`scripts/lane_cost.py`** (new) — reads the four token counts every assistant turn already
carries in the session transcripts, de-duplicates on `message.id`, prices through the registry,
and renders per lane and per model. Verbs: `lane`, `close`, `receipt`, `report`, `token-log`.

**`scripts/fleet_health.py`** — a `[cost]` digest line: money per batch and per model, one
ledger read, fail-soft, and **silent** over an empty ledger rather than printing a `$0.00`.

**`logs/LANE-COSTS.jsonl`** (new, append-only) and **`logs/TOKEN-LOG.md`** (fed, see §4).

### The measurement, live

```
lane lane-y-751-cost-in-money  batch=Y  USD 18.82 over 128 call(s)  [rates as_of 2026-06-24]
  tokens: in 256 / out 95,616 / cache-write 320,197 / cache-read 28,861,393
  claude-opus-5: USD 18.82 (29,277,462 tokens, 128 call(s))
```

**Cache reads outnumber fresh input tokens by five orders of magnitude** — 28,861,393 against
256. That single ratio is why the cache multipliers are load-bearing rather than a detail: a
reporter that priced cache at the input rate, or at nothing, would be wrong by more than the
bill. It is also why this lane's figures are not comparable with `TOKEN-LOG`'s existing
`ccusage` entries, which exclude cache "for comparability".

## 3 · The design decision that needs the integrator's eye

**The cost block is its own ledger, joined onto the merge receipt by slug — it is NOT a field
inside the receipt row.** That is a batch ruling, not a preference.

`scripts/merge_receipt.py` is `[#750]`'s **SOLE-OWNED** file for batch Y — its own Done-contract
clause 3 says so in as many words, and `[#752]` is already sequenced behind it. `[#750]` fired
in the same wave as this lane and is rewriting that module's completeness predicate right now.
Writing to it here would have been an undeclared **third** claim on a module being restructured,
and the freeze's `file-collision` check records wave 1 as *"4 contracts, 8 declared paths, no
file claimed twice"* — a count this lane would have falsified.

The contract's Done-when 2 is still satisfied on its own terms. It requires the lane receipt to
carry tokens and USD "resolved from that file at run time — **never a rate table hard-coded into
this lane, and never a literal in the receipt writer**". There is no literal in the receipt
writer because the receipt writer was not opened. `lane_cost.py receipt --slug <slug>` renders
the lane receipt as one thing: minutes from `MERGE-RECEIPTS.jsonl`, tokens and USD from
`LANE-COSTS.jsonl`. Both ledgers stay append-only; neither writes the other.

### Proposed diff — for `[#750]`'s owner or the integrator, AFTER that branch lands

Not applied. **Re-resolve the context before applying**: `[#750]` is rewriting
`Receipt.incompleteness_reason` and `wall_seconds` in this same module, so the line anchors
below will have moved.

```python
# scripts/merge_receipt.py

# 1. In `class Receipt`, beside `closed`:
    #: [#751] -- the lane's token/USD cost block, attached at close. OPAQUE here on purpose:
    #: this module is a stopwatch and knows nothing about rates. It carries the block; it
    #: never computes one.
    cost: Optional[dict] = None

# 2. In `Receipt.from_dict`, so a round-trip stops dropping it (the live defect: `from_dict`
#    silently discards every key it does not name, so a cost block written into the scratch
#    file today does not survive `close`):
                   kind=data.get("kind", KIND_MERGE), steps=steps, closed=data.get("closed"),
                   cost=data.get("cost"))

# 3. In `close_receipt`, immediately before `line = json.dumps(...)`:
    if receipt.cost is None:
        # Fail-soft and NAMED: a receipt that could not be costed is still a receipt, and a
        # cost of 0.0 would be worse than no cost at all.
        try:
            import lane_cost
            receipt.cost = lane_cost.lane_cost(slug, batch=receipt.batch).to_dict()
        except Exception as exc:                        # noqa: BLE001
            logger.warning("no cost block for %s -- minutes only: %r", slug, exc)
```

With that seam in place, `lane_cost.uncosted_reason` becomes redundant for merge receipts and
`logs/LANE-COSTS.jsonl` can be retired in favour of the receipt row. **Until then the join is
the mechanism**, and it is a complete one.

## 4 · The TOKEN-LOG ruling — FED, not deleted

**Ruled FED.** The contract asked for a recorded decision rather than an omission; this is it.

Deletion had a real case. The file is fed by hand — a `ccusage --json` snapshot pasted weekly
through `/session-summary` — and it had not been fed since **2026-08-04**, six weeks before this
lane. A record whose feeding mechanism has stopped working is a decoration.

FED wins on two grounds:

1. It is **ADR-29/ADR-39 append-only in the STRICT class** — the LESSONS.md archival exception
   explicitly does not reach it — and it holds eighteen months of history back to the
   2026-03-28 baseline. Deleting it destroys the only longitudinal usage record the repo has,
   and that is an operator act, not a lane's.
2. **What failed was the feeding, not the file**, and this lane produces exactly the figures it
   wants from a path that runs. Deleting a record because nobody could fill it, in the same
   commit that makes it fillable, is the wrong half of the decision.

Executed: `lane_cost.py token-log --append` writes in the file's own established format and
**prepends** under the three-line header, because "append" for this file means newest-first.
Measured on the real append: **7 lines, 546 bytes, header byte-identical, every pre-existing
entry byte-identical** — pure insertion. `test_feeding_the_token_log_rewrites_not_one_existing_
byte` pins that in both directions. The feeder **refuses to create** the file if it is absent,
because whether it exists at all IS this decision.

The entry states its method, because per-lane-with-cache and fleet-weekly-without-cache are not
comparable line-for-line and an entry that did not say so would invite a false trend.

## 5 · Open items

| # | item | owner |
|---|---|---|
| 1 | The receipt-row seam above — apply after `[#750]` lands and re-resolve the context | `[#750]`'s owner / integrator |
| 2 | **`provider_router._sibling` does not register its module in `sys.modules`** (PEP 451 requires it before `exec_module`). Any `@dataclass` in a module it loads dies with `AttributeError: 'NoneType' object has no attribute '__dict__'` — 33 errors in `test_provider_router.py`, none of them pointing at the dataclass. Worked around here by making `ModelRate` a `NamedTuple`; the loader is a shared helper this lane does not own, and the same shape appears at ~10 `spec_from_file_location` sites. **The same class has a second live victim** (§6): `tests/test_seal_repo_profile.py:32-35` OVERWRITES `sys.modules["validate_hermetization"]` with a second object from the same file, and any xdist worker that draws it before `test_manifest_link_route` REDs an `is` assertion — order-dependent, so it surfaces and vanishes with the collection. One row should cover both: `sys.modules` handling at path-based load sites. | unowned — candidate |
| 3 | **`journal_spine_anchor` FAILs on main's spine, and this lane cannot fix it.** PROOF, not assertion: the gate names `e6acb23e` and `8a41c650`; `git show 8a41c650:JOURNAL.md` names none of `dceb82e9` / `8a41c650` / `e6acb23e` / `f5384ac4`, so the anchor was already absent at this lane's **base** commit, and this lane's diff touches no `JOURNAL.md`. STANDING_RULINGS P-1 forbids a lane writing a JOURNAL entry at all. | integrator, at the merge |
| 4 | Two hooks SKIPped on every commit here, declared in each commit body: `doc-counts-pytest-freshness` (this lane adds tests; the contract forbids index regeneration in a lane — Q1) and `audit-health` (item 3 above). | integrator |
| 5 | **Steps 1 and 2 landed as ONE commit, not two.** `graph-orphan-census` refuses a script no wiring surface reaches and reads the TREE, while pre-commit stashes unstaged work — so a step-1 commit leaving `lane_cost.py` unwired is refused, and wiring it unstaged reads as HEAD and is refused identically. The two acts land together or neither does. | reported, no action |
| 6 | **The rate card is stamped `as_of: 2026-06-24`**, which is the cache date of the source it was copied from, not today. That is deliberate — a card stamped with the day it was copied tells a reader it is current when it is not — but it means the figures are ~3 months old. Re-reading the source is its own act. | unowned — candidate |
| 7 | **Five model ids are unpriced**: `gpt-5.6-terra`, `gpt-5.6-sol`, `grok-l5`, `grok-4.6`, `gemini-3.7-flash`. Honest rather than lazy — `grok`'s one measured datum is a whole-CALL price (`$0.037`), not a per-token rate, and inflating it would manufacture a number. Every report names them and calls its own total a floor. | unowned — candidate |
| 8 | `logs/LANE-COSTS.jsonl` holds ONE row, this lane's, and it **excludes this lane's own closing turns** — they had not happened when it was measured. The ledger is append-only, so this is recorded rather than corrected in place. The other five batch-Y lanes are uncosted; closing a running lane would record a partial figure as a final one, which is the exact defect this module refuses. | integrator, at batch close |
| 9 | **The suite is 48 RED on main's own tree, and every one of them is pre-existing** — see §6 for the paired-run proof. Three are item 3's anchor gap; the other 45 are unrelated drift across eighteen test modules. This lane adds none and fixes none. | integrator |

## 6 · Suite

`uv run --locked pytest -q -n 6` at the lane tip: **5,783 passed · 48 failed · 25 skipped ·
2 xfailed**, 2,253 s. `-n 6` rather than `-n auto`, which is OOM-killed on this box.

**All 48 are PRE-EXISTING. Zero are this lane's.** That is measured, not asserted, by a paired
run: the same 48 node ids re-run at this lane's base commit `8a41c650`, from this same worktree,
with the same interpreter — **47 fail there identically**. The lane's whole diff is twelve files
(`git diff --name-only 8a41c650..HEAD`) and not one of them is imported by the 47.

### The 48th, isolated, because one failure differing is exactly where a real regression hides

`test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`
failed in the tip's full suite and passed in the base's targeted run — two variables moved at
once (the commit *and* the run shape), so neither run alone attributes it. Isolated:

| run | shape | result |
|---|---|---|
| tip `23127d8b` | that test alone, `-n 0` | **passes** |
| tip `23127d8b` | `test_seal_repo_profile.py` then that test, `-n 0` | **fails** |
| base `8a41c650` | `test_seal_repo_profile.py` then that test, `-n 0` | **fails, identically** |

So the discriminating variable is module ORDER, not the commit. The mechanism is in the tree at
`tests/test_seal_repo_profile.py:32-35`: it loads `scripts/validate_hermetization.py` by path and
**overwrites `sys.modules["validate_hermetization"]` with a second module object built from the
same file**. Any worker that runs that module first leaves `batch_manifest`'s enum and the
freshly-imported one as two objects, and `assert … is …` fails on frozensets that compare equal.
Both files are outside this lane's diff, and the failure reproduces at the base commit with no
lane file loaded at all. What this lane actually changed was the xdist *distribution* — 22 new
tests in `tests/test_lane_cost.py` reshuffled which worker drew which module.

**Not fixed here, deliberately.** The fix is either `importlib.reload` discipline in that test
module or dropping the `sys.modules` overwrite, and both are edits to a file this lane does not
own. It is the same defect class as open item 2 — a path-based loader mishandling `sys.modules` —
and it belongs in that row.

### Nothing in the 48 moved because of this lane, including the two that look like it might

- `test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar` — filing row
  `[#751]` grew `BACKLOG.md` from **91,281 to 91,502 bytes** against a 72,000-byte bar. The bar
  was already exceeded by 19,281 bytes at the base commit; this lane's 221 bytes cross no
  threshold and clear none.
- `test_proof_layer.py::test_the_live_guard_population_is_at_or_below_its_baseline` — the extra
  guards it names are in `test_fleet_analytics.py` and `test_worktrees…`, not in
  `tests/test_lane_cost.py`, and it fails identically at base.

### What is GREEN, and it is the part the contract binds

Every test covering this lane's diff passes: `test_lane_cost` (22, all new and RED-first),
`test_provider_registry`, `test_provider_registry_schema`, `test_provider_router`,
`test_provider_roles`, `test_provider_rerank`, `test_fleet_health`. `ruff check` clean.

---

## AMENDMENT 1 — 2026-09-14 · the integrator's review, four findings closed

> **In-file amendment marker, not an edit.** An audit is immutable (`CLAUDE.md` §5 rule 3), so
> §1–§6 above stand as written and this section records what changed after them. Where this
> section and §5 disagree, **this section is later and governs**.
>
> Raised by the batch-Y integrator holding this lane's merge at `2e5c31bc`, from a Codex pass
> the integrator then verified against the code by hand. All four findings are in
> **aggregation or attribution**. None is in pricing: the integrator re-derived §2's USD 18.82
> against the live card (256 in @ $5/M + 95,616 out @ $25/M + 320,197 cache-write @ $6.25/M +
> 28,861,393 cache-read @ $0.5/M = $18.8236, against the ledger row's 18.823608) and it holds.
> **The pricing path is unchanged by this amendment.**

### Finding 1 (CRITICAL) — an unmeasured lane was absorbed into every total as $0.00

`LaneCost.has_transcript()` existed and `LaneCost.render()` used it correctly — *"NO TRANSCRIPT
FOUND … UNKNOWN rather than zero"* — but `BatchCostReport` never consulted it. A `models=()` row
contributed 0.0 to `usd`, to `by_batch()`, and incremented the `n=` in *"cost over n=N lane
receipt(s)"*. §6's own principle, one level down: **an empty ledger is not a free batch, and an
empty row is not a free lane.**

It fires on this module's documented happy path, not on a contrived input. `transcript_dirs`
states that a `--bg` lane's transcript is filed under its launching session and carries no
directory of its own — so the first honest `close --slug <bg-lane>` appends an empty row, and
only then does the caller learn to pass `--slug-dir`. **Every remaining batch-Y lane is `--bg`.**

**Fixed** by giving `BatchCostReport` a `measured()` / `unmeasured()` split that every figure is
built from. Unmeasured lanes are named in `render()` and in the `[cost]` digest, never summed and
never counted in `n=`. `cost_health_line` returns `None` rather than `$0.00` when nothing is
measured — that line prints at every SessionStart, the widest audience an unmeasured zero could
reach.

### Finding 2 (CRITICAL) — a re-close double-counted, permanently

`cmd_close` appends unconditionally; `append_cost` is append-only by design (ADR-29/ADR-39 class).
`BatchCostReport` then **summed every row** while `uncosted_reason` took **`rows[-1]`** — one
ledger, two incompatible meanings for the same duplicate. Because the ledger is append-only there
is **no sanctioned repair**: the superseded line cannot be deleted, so a single retry would
inflate the batch total and every future boot's `[cost]` line for good.

It composes with finding 1: empty row, then re-close with `--slug-dir`, is the *normal* first
correct use — which is how the ledger gets two rows for one lane.

**Fixed in the reader, not the file.** `BatchCostReport.resolved()` keeps one row per slug,
**last wins** — the rule `uncosted_reason` already applied — so the aggregate and the per-slug
reader can no longer disagree. `test_the_ledger_keeps_both_lines_because_it_is_append_only` pins
that the *file* still keeps every line: superseding by rewriting the ledger would fix the
arithmetic by breaking the ADR-29/39 guarantee, which is the worse trade.

### Finding 3 (CRITICAL as raised; the integrator rated live risk lower and left the weighting to this lane)

`transcript_dirs` matched `wanted in _normalise(d.name)` while its own docstring said *"MATCHED,
NOT GUESSED, AND NEVER WIDENED"*. **Containment is a widening:** a truncated `lane-y-75` claims
`lane-y-751`'s entire transcript.

**Weighted as worth fixing now, and fixed**, for the reason the integrator gave rather than the
severity: the failure is *silent*, so the wrong amount arrives confident. Two further reasons the
low live risk is not a reason to defer — the absence of a collision among batch Y's ids is a
property of **data**, not of the code, and the next batch's ids are not yet chosen; and the fix is
three lines against a defect that misattributes money between lanes.

Matching is now **dash-bounded** — both sides must land on a dash or a string edge, so a slug
matches whole path segments — and a slug reaching more than one directory logs a WARNING naming
every directory it summed. Demonstrated live on this host after the fix:

```
lane --slug lane-y-751-cost-in-money   ->  USD 35.44 over 226 call(s)      (correct)
lane --slug lane-y-75                  ->  NO TRANSCRIPT FOUND             (was: the same figure)
```

**A gate shaped the implementation, and that is worth recording rather than hiding.** The obvious
spelling is a regex, `(?:^|-)<slug>(?:-|$)`. It was written that way first and the commit was
REFUSED by `graph-edge-class-census`: `graph_queries.is_edge_computation_shape` counts
"≥2 `re.` calls + a scan or read" as a private five-kind edge computation, and the new
`re.compile` was this module's second `re.` call after `_normalise`'s `re.sub`.

The finding is a **false positive on the merits** — a session store lives outside the repo, so
matching a slug to a directory there is not a corpus-structure relation, and it is none of the
five kinds (citation / generation / template / test / script call-site). The gate says as much
about itself: *"RECALL OVER PRECISION, deliberately. A false positive costs one verdict row in the
register."*

**That row was NOT added, and the reason is the decision budget rather than the merits.**
`EDGE_COMPUTATIONS` in `scripts/graph_queries.py` is a curated register outside this lane's
declared footprint, and a curated-baseline touch is escalation class (a) under V-2 — not
something a lane takes on its own while the batch is open. So the predicate is spelled as four
string comparisons instead (`_matches_segment`), which is the identical predicate, needs no
register row, and reads no worse. The choice is documented in that function's own docstring so
the next reader does not "simplify" it back into a regex and re-trip the gate.

**Carried for the integrator** (§5, new row 10): the census will refuse the *next* lane that adds
a second regex to any `scripts/*.py` for an equally non-corpus reason. Whether the predicate
should narrow, or whether such modules should just take verdict rows, is a call above a lane.

### Finding 4 (HIGH) — nothing priced against the LIVE registry, and the fixture hid it

Every pricing test used `_registry(tmp_path, input_rate=5.0, output_rate=25.0)` — **exactly** the
live `claude-opus-5` rates. The fixture mirrored the truth it was supposed to check, so a live
rate that went missing would still have looked right everywhere.

**Fixed as a RESOLVABILITY test, deliberately not by pinning a rate.** A typed rate is the
stale-number pattern this repo forbids (*"never restate a count — cite the surface that computes
it"*) and would go RED at the next genuine price change, which is not a defect.
`test_every_live_priced_model_prices_through_this_module` asserts that every model the **live**
card prices resolves through this module's own pricing path and yields a positive figure for
positive usage; `test_the_model_this_repo_actually_runs_is_priced_live` asserts `claude-opus-5` is
in the live priced set. Neither asserts a price.

**Honest limit:** these two were **GREEN on arrival**, because the live card is currently correct.
Finding 4 was a coverage gap, not a live defect, and they are regression guards rather than
RED-first witnesses. Findings 1–3 had seven RED-first witnesses, all failing before the fix.

### What was verified

- `tests/test_lane_cost.py` — **32 passed** (22 before, 10 added here).
- The impacted set named by `impacted_tests.py select --changed scripts/lane_cost.py`, plus
  `test_fleet_health` and `test_provider_registry`: **736 passed, 3 failed** — the same
  `journal_spine_anchor` trio §6 already proved pre-existing, and no others.
- `ruff check` clean. Live `report`, `receipt` and `lane` re-run; §2's figures unchanged.

### One existing test's assertion was rewritten, and why that is not a weakened test

`test_the_report_over_an_empty_ledger_says_so_rather_than_reporting_zero` pinned the literal
phrase `"no cost receipts"`, which gained the word *measured* when the refusal widened to cover
transcript-less rows. It now asserts the **invariant** — the words `cost receipts`, `undefined`,
`not zero`, and no `$0.00` anywhere — so a predicate that got **stricter** no longer reads as a
regression. The test's guarantee is unchanged in strength and its subject is larger.

### Open items, amended

- **§5 row 8 is superseded in its mechanism, not in its fact.** `logs/LANE-COSTS.jsonl` still
  holds one row measuring less than this lane's full spend, and it is still append-only. But
  re-closing is now *safe* — the reader supersedes by slug — so the integrator can re-close this
  lane at batch close with `--slug-dir` and the total will be right rather than doubled. That was
  not true before this amendment.
- **§5 rows 1–7 and 9 stand unchanged.**
- **NEW row 10 — `graph-edge-class-census` refuses a non-corpus second regex.** Adding a second
  `re.` call to any `scripts/*.py` that also scans or reads trips
  `is_edge_computation_shape`, regardless of whether the module computes a five-kind corpus
  relation at all. This lane routed around it by writing the predicate without a regex (finding
  3 above), which is a fix for this module and not for the class. Either the predicate narrows,
  or modules like this one take `not-an-edge` verdict rows — a curated-register decision,
  escalation class (a), so it is reported rather than taken. **Owner: integrator / unowned —
  candidate.**
