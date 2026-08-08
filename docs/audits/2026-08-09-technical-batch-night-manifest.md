---
batch: 0
status: open
closed_by: docs/audits/2026-08-09-technical-batch-night-packet.md
---

# Night batch, 2026-08-09 — manifest, committed at DISPATCH

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** batch-night-manifest
- **Protocol:** ADR-110 + PLAYBOOK Ch8 "The batch protocol". Width **5**, one wave, read-mostly.
- **Authority:** operator ruling 2026-08-08 evening — dispatched with this file, not after it.
- **Predecessor:** batch 3, manifest `docs/audits/2026-08-08-technical-batch-3-manifest.md`,
  packet `docs/audits/2026-08-08-technical-batch-3-packet.md` (committed, so batch 3 is CLOSED
  and no exemption was live when this file landed).

## Why this file exists — the lesson from batch 3, applied rather than restated

Batch 3 was dispatched with no manifest. The cost was measured, not hypothetical: a **2h12m**
integrator run that reached the precondition gate and correctly **STOPPED before merge #1**
rather than reach for `SKIP=audit-health` or `--no-verify`
(`docs/audits/2026-08-08-technical-batch-3-consolidation-report.md`). Without a committed
manifest there is no ADR-110 declared-integration-arc exemption, and without that exemption the
merge queue is mechanically unrunnable — each lane merge lands an unanchored first-parent spine
entry and `audit-health` (`always_run: true`) evaluates PER-COMMIT, so the batch's own JOURNAL
entry (which can only name the merge SHAs *after* the merges) cannot discharge them mid-queue.

This file is committed **at dispatch**, in the present tense, which is what Ch8 required all
along and what batch 2 met. Nothing here is back-dated.

**Expiry is automatic and needs no edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3), so
openness is deliberately not a mutable flag anyone flips: the exemption dies the moment
`docs/audits/2026-08-09-technical-batch-night-packet.md` exists in the committed tree.

## TWO FIELDS DERIVED LIVE, because the dispatch contract's content did not carry them

Recorded here rather than absorbed silently, because a machine-read surface authored from prose
intent instead of from its parser is the exact class that cost this repo two artifacts on
2026-08-08 (JOURNAL entries (h) and (l): a manifest that granted a working exemption while
failing its own well-formedness pin, and a review artifact that recorded a real review while
satisfying no coverage leg — both read as done, neither was).

**1. The filename is `...-technical-batch-night-manifest.md`, not `...-technical-night-batch-manifest.md`.**
The dispatch contract named the latter. `batch_manifest.MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match`, and the contract's name
does **not** match it — after the only `-batch-` there is no further `-manifest.md` to consume,
so the glob fails. Verified before writing, both spellings:

```
False  2026-08-09-technical-night-batch-manifest.md
True   2026-08-09-technical-batch-night-manifest.md
```

A manifest the reader cannot enumerate declares nothing: `open_batches` would return `[]`, the
exemption would not exist, and this file would have reproduced batch 3's failure while looking
like its repair. Two tokens were swapped — the smallest edit that makes the parser see it. The
alternative, widening the glob in `batch_manifest.py`, is a code change to a gate path and was
out of scope for a manifest commit. The name still satisfies `validate_hermetization` Rule B:
class token `technical` from the closed ADR-101 enum, slug `batch-night-manifest` lowercase-kebab.

**2. `batch: 0` — a sentinel, because this batch has no number and the field must be a digit.**
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against **every** live open manifest, so a value like `night` would leave the
suite RED for as long as the batch is open. The content genuinely lacks a number: the closure
contract below names "the batch-4 planning GO" as a *future* decision this batch feeds, so this
batch is not batch 4, and numbering it 4 would make the file contradict itself in two paragraphs.
`0` is chosen because it is the one digit that cannot collide with any batch number past or
future. **It means "unnumbered night batch, outside the 1/2/3 execution sequence"; the next
execution batch is 4, exactly as the closure contract says.** The field is reporting-only —
`batch_manifest` reads it with `fm.get("batch", "?")` and gates openness on `status:` and
`closed_by:` alone — so the choice affects what the gate *prints*, not what it *decides*. Gate
evidence will read "while batch 0 is open (`docs/audits/2026-08-09-technical-batch-night-manifest.md`)";
the path is the disambiguator.

No third field was invented, and no field the schema does not read was added.

## Class, and the standing rule for tonight

**Class:** read-mostly research and review. **No lane merges to `main` overnight.** Every lane
commits its report on its own branch and pushes; the operator integrates in the morning.

## Runtime — CLOUD sessions, and the three consequences that follow

The operator's machine is **off**. Every lane runs as a cloud session, and three consequences are
recorded here so a lane does not rediscover them one at a time:

1. **No local-only artifact is reachable.** Anything gitignored does not exist in a fresh clone —
   notably `logs/PROPOSALS-*.md`. A lane whose analysis wants one must say so in its report and
   proceed without it, never infer its contents.
2. **No operator interaction is possible.** Every lane batches its questions into a
   `## Needs a ruling` section of its own report. A lane never blocks waiting for an answer and
   never rules on the operator's behalf.
3. **No lane tears anything down.** Teardown is the morning integrator's, under F1
   verify-before-destroy.

## Width — 5 lanes, read-mostly, file-disjoint

One report each under `docs/audits/`, so the lanes share no file and cannot conflict.

| Lane | Subject | Report path |
|---|---|---|
| N1 | Position vs North Star — backlog shape, priorities, deferred set, the road to hub v1.0 | `docs/audits/2026-08-09-technical-n1-position-northstar.md` |
| N2 | Architect-defect → mechanism map; handoff & onboarding gaps | `docs/audits/2026-08-09-technical-n2-mechanism-map.md` |
| N3 | Performance, bottlenecks, and the measure-first instrumentation design | `docs/audits/2026-08-09-technical-n3-performance.md` |
| N4 | Code review of the hub's hot spots (reviewer-lane backed) | `docs/audits/2026-08-09-technical-n4-code-review.md` |
| N5 | Library-first sweep of hand-rolled machinery | `docs/audits/2026-08-09-technical-n5-library-first.md` |

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-09-technical-batch-night-packet.md` is the single act that discharges the
last of them and expires the ADR-110 exemption:

1. all five reports are merged;
2. their `## Needs a ruling` sections are adjudicated by the architect;
3. the end-of-batch packet reports **opened / closed / net / open-total** plus the
   **dispatched-vs-close width delta**.

`closed_by:` is filled at close — the packet is a distinct artifact authored then, which is also
what `/lane-integrate` §4 and its checklist item 4 require independently. Naming an
already-committed file would close this batch on arrival and grant no exemption at all, since
`batch_manifest.open_batches` requires the `closed_by` path to be **absent** from the committed
tree.

## Births — ZERO tonight

Every proposal in every report is a **candidate** for the batch-4 planning GO, ruled against
demonstrated close capacity. No lane files a BACKLOG row, and no lane closes one.

## Baseline at manifest commit

- `main` @ `dd0cb148`, pushed, working tree clean at branch time.
- `python scripts/audit.py health` → **`health: OK`** before this file was written.
- `batch_manifest.open_batches(.)` → `[]` — batch 3 is closed by its committed packet, so this
  manifest opens the only live batch and inherits no stale exemption.
- No `2026-08-09` JOURNAL entries existed; this arc's is `(a)`.

## One standing consequence of an open batch, stated so it is not discovered at 6am

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH; `docs/handoffs/` is immutable, so a bundle sealed mid-batch is wrong forever).
`/handoff` will therefore refuse until the closing packet lands. That is correct behaviour, not a
fault, and the remedy is to land the packet — never to bypass the refusal.

## What this manifest deliberately does NOT do

- It does not enumerate lane **branch** names, because the lanes are cloud sessions whose branch
  names are assigned at launch. The ADR-110 exemption is not scoped to enumerated lanes anyway —
  any `worktree-lane-*` `--no-ff` merge qualifies while a batch is open, which is
  `batch_manifest`'s second stated honest limit, unchanged and not narrowed here.
- It does not pre-authorize any merge to `main`. Overnight lanes push branches; the morning
  integrator merges.
