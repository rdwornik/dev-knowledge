---
batch: Y
seq: 1
status: open
closed_by: docs/audits/2026-09-14-technical-batch-y-close-packet.md
---

# Batch Y — manifest (dispatch half) · 2026-09-14

**Seat:** dispatcher · **Batch:** Y, wave 1 · **Ceiling:** ADR-110, six lanes
**Base at fire:** `main` after AY1-2's teardown — a single shared base for all lanes.
**Status:** **SIX CONTRACTS FROZEN. FOUR FIRED CONCURRENTLY, TWO SEQUENCED AS BACKFILL** — see
THE LANES and §3.

**Consumers:** `[#750]` `[#751]` `[#752]` `[#753]` `[#754]` `[#755]` — the reserved block below —
plus `[#675]`, `[#744]`, `[#612]`, `[#628]` and `[#667]` as the owners of individual clauses.
Every contract named below is copied in-tree into
`docs/audits/2026-09-14-technical-batch-y-launch-contracts/`.

---

## 1 · The GO, recorded

The authority for this batch is two operator files, both carried and both passing the `carried-by`
refusal (2 of 2 governed and carried):

- `to-cc/DECLARE-BATCH-Y-ROSTER-2026-09-13.md` — the six lanes.
- `to-cc/AMEND-BATCH-Y-ROSTER-001.md` — four rulings, three of which bind this freeze:

> **AY1-1 · Y-1 amended: completeness is judged on the suite step's VERDICT STATE, not its exit
> code.** `PASS` or `PRE-EXISTING` → COMPLETE with the state recorded by name; `REGRESSED`, or a
> verdict that cannot be read → INCOMPLETE and the merge is refused. Forcing the step to exit 0 is
> ruled out by name (`[#744]`'s false pass).

> **AY1-2 · Ceiling: the two work-carrying trees land, all five are torn down.** … Batch Y opens
> at 0 + 6.

> **AY1-3 · Y-5's premise corrected:** `archive_row_body.py` has no wiring consumer on `main` …
> Y-5 therefore sequences after AY1-2's merges, and its first act verifies the trigger is live on
> `main` before touching a single row.

**Scope bound:** the GO covers these six lanes and no lane outside them fires on it. The DECLARE's
own "not in this batch" list — the prompt distiller, the management map, charts, folder names,
corp-monorepo deployment — is explicitly out.

## THE LANES — six, frozen 2026-09-14

> **The heading is deliberately UNNUMBERED.** `batch_manifest.py` finds this table with
> `^ {0,3}#{1,6}\s*THE LANES\b` (line 648), so a section number between the `##` and the words
> makes the manifest declare **zero** lane slugs, and the `[#630]` agreement check then refuses
> every contract while reporting no manifest-side excess. Batch X4 hit exactly this and recorded
> it as an amendment; the integrator seat re-flagged it before this freeze, and it was verified
> against the regex rather than taken on trust.

```
slot  row     slug                             model  effort  shape        wave
1     #750    lane-y-750-merge-receipts        opus   xhigh   local        1 -- concurrent
2     #751    lane-y-751-cost-in-money         opus   high    local        1 -- concurrent
3     #754    lane-y-754-backlog-to-bar        opus   high    local        1 -- concurrent
4     #755    lane-y-755-docs-cut-finish       opus   high    local        1 -- concurrent
5     #752    lane-y-752-declared-model-runs   opus   xhigh   local        2 -- backfill after #750
6     #753    lane-y-753-non-claude-trial      opus   high    interactive  2 -- ATTENDED, after #751
```

**Every lane is `opus`, explicitly, and `opusplan` appears nowhere.** This is not a default
inherited from the routing matrix — it is rendered onto each dispatch line, because `opusplan` is a
measured no-op under `--bg` (`lane-x-689` ordered opusplan and ran sonnet-5, making every routing
decision in that window advisory). Closing that hole is `[#752]`'s own subject, so this batch must
not reproduce it at its own freeze.

**Concurrency 4, with rolling backfill.** Slots 1–4 fire together. Slots 5 and 6 are held and
released by a landing, not by a timer:

- **`#752` releases when `#750` lands.** Both write `scripts/merge_receipt.py`.
- **`#753` releases when `#751` lands.** Both write `ecosystem/provider-registry.yaml`.

**Serialisation groups — two, and both are REAL collisions rather than checker artifacts:**

| file | owner (first) | sequenced (second) | why it is substantive |
|---|---|---|---|
| `scripts/merge_receipt.py` | `#750` | `#752` | `#750` rewrites the completeness predicate; `#752` adds the ordered-not-equal-ran refusal to the same module |
| `ecosystem/provider-registry.yaml` | `#751` | `#753` | the registry carries **no** machine-readable rate field (top-level keys are `providers` / `roles` / `models`; cost appears only as prose), so `#751` must AUTHOR the rates — it is a write, not a read |

**`#753` is ATTENDED and is frozen at `shape: interactive`, not `local`.** Its own contract says it
"runs in the daytime and reports per task, never unattended", and a `--bg` lane can neither ask a
question nor report between tasks. Dispatching it `--bg` would contradict the lane's own frozen
text, so it is not in the fired set at all; it is launched by the operator when he is present.

**Reserved task-id block: `#750`–`#755`, allocated AT FREEZE.** The high-water mark was measured at
**749** across three refs — `main`, the batch-X4 freeze branch and the x-664 deletion branch — so
the block sits above the reach of everything then in flight. (Those two branch names are given in
prose rather than spelled as slugs deliberately: see the phantom-row note below.) Each contract names its OWN id, and no lane calls "next free id" at all. This is the fix
batch X4's AMENDMENT 3 asked for in its own words — *"allocate from above the lanes' reach, or
reserve the block at freeze"* — after that seat took `#746`, lane 2 filed `#746` forty minutes
later, and the row had to be renumbered to `#747` across five surfaces. `next_task_id` reads a
working tree, and a sibling lane's rows are not in it, so a duplicate id is invisible on both sides
until integration.

## 3 · STEP 0 refusals

> **PHANTOM-ROW NOTE — a defect caught in THIS manifest, at freeze, by running the predicate over
> its own draft, and the reason this note lives HERE rather than one section up.**
> `manifest_lane_slugs` scans the whole `THE LANES` section for slug-shaped tokens, so ANY prose
> mention of a `lane-*` name inside it becomes a declared row. The draft cited the provenance of
> the id high-water using the full x-664 worktree name, and `freeze_manifest_contract_agreement`
> REFUSED: *"the manifest names ['lane-x-664-delete-list-execution'] with no matching contract"* —
> a phantom seventh lane, in a batch of six, from one prose citation. The first fix FAILED because
> this very note quoted the refusal verbatim while still sitting inside `THE LANES`, which
> re-declared the phantom it was documenting. It is the same class as the extractor's own recorded
> limit — a filename quoted inside a Done-contract reads as a declaration — and the general rule is
> that these parsers cannot tell a citation from a declaration and do not guess. **Keep every
> `lane-*` literal out of `THE LANES` unless it IS a row.** Verified after the move: 6 manifest
> slugs, 6 contract slugs, sets equal both ways.

| check | result |
|---|---|
| `lane-ceiling --check-worktrees` | **REFUSED at first run, then PASS.** The first run named five provisioned batch-X worktrees — the ceiling working exactly as designed, refusing *before* the first worktree existed rather than reporting a decorative number afterwards. Two of the five carried 15 commits that existed nowhere on `main`. That refusal is what produced ruling AY1-2; the batch opened only once the live list read **0**. |
| `carried-by` | **PASS — 2 of 2** over the DECLARE and the AMEND. The one standing refusal on the transport, `DECLARE-BATCH-V-CLOSE-2026-09-09.md` (`carried-by: BACKLOG.md`, prose rather than a locator), is another seat's frozen declaration and is neither this batch's to edit nor caused by it. |
| `file-collision` | **REFUSED on the full six, by design — and the refusal is RECORDED rather than worked around.** Two files are claimed twice (table above). Both are resolved by sequencing, so the concurrent set never holds either file twice: over wave 1 (`#750` `#751` `#754` `#755`) the check returns **PASS — 4 contracts, 8 declared paths, no file claimed twice**. |
| `file-collision` — **a hole closed at this freeze** | The first run reported *"2 contract(s) declared NO repo path and were invisible to this check"* — `#750` and `#752`, the two that collide on `scripts/merge_receipt.py`. The extractor reads **only the `## Done-contract` section** (`seat_refusals.py:397`), so a footprint declared under `## Steps` is invisible. Both contracts now declare their paths inside the Done-contract, and the collision the check could not see became visible. **Without this, wave 1 would have fired two lanes at the same module on a PASS that was vacuous.** |
| `graph-task-coverage` | **REFUSED once, on ONE file, and the refusal exposed that the other five passes were INCIDENTAL.** `[#664]` clause 2 refuses a staged file no OPEN row claims. Five of the six contracts cite `[#675]` and `[#717]` — and they do so only because the `local` shape's Dispatch boilerplate mentions them (`[#675]` clause 1 / AX25-2 for the `claude` head token; `[#717]` for the model being on the line). Both are open rows, so five files were claimed by citations never intended as claims. The `interactive` shape carries neither, so the sixth was the only one where the gate actually bit. Fixed honestly rather than by citation: no existing open row covers a supervised non-Claude producer trial — `[#578]` (the earned mitigated rerun, scoped to the 14-item pack plus `C1-N3`), `[#568]` (config as code via junctions) and `[#492]` (deferred, review-lane acceptance) were each checked and rejected — so **row `[#753]` is filed in THIS commit**, and its lane AMENDS it rather than filing it. The reserved block is otherwise unchanged: the remaining five lanes file their own rows in their own first commits. |
| `sleeping-poll` | Declared waits are the two backfill releases, and both are written as a predicate on a ref surface — *"`#752` opens `scripts/merge_receipt.py` only after `#750` has landed on `main`, and verifies it"* — not as an intention to check later. |
| `dryrun-step0` | Recorded in §4 at fire. |

## 4 · Receipts

Filled at fire. Each lane is confirmed up by its BRANCH appearing in `git branch`, not by the
dispatch command returning.
