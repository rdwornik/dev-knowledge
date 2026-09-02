---
batch: G
seq: 1
shape: ADR-110 — DERIVE -> architect's cut -> FREEZE -> DISPATCH; 9 committing lanes (1 codespace parity witness + 8 local). G0 ran serial on the primary before any lane booted; G3b was cut mid-batch by ruling R-G-G3b.
dispatched: 2026-09-02
status: open
closed_by: docs/audits/2026-09-02-technical-batch-g-close-packet.md
substrate: LOCAL (8) + CODESPACE (1, the G5 parity witness) — the flip is recorded below
---

# BATCH G — THE ROUTING CARRIER, THE SUBSTRATE DECISION AND THE DEBT LANES · THE MANIFEST

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves an open batch as
the conjunction of four facts: the manifest is TRACKED, `status: open`, `closed_by:` names a shape
that CAN resolve, and that path is ABSENT from the tree. All four hold at the time of writing.

**FILED LATE, AND THAT IS RECORDED RATHER THAN TIDIED.** Batch G was frozen and dispatched without
this file. It was created by the integrator at the head of the merge queue, when the missing
ADR-110 exemption surfaced. A manifest written after dispatch cannot pretend to have governed it,
so `dispatched:` carries the real date and this paragraph carries the defect. The lane roster below
is the roster that actually ran, read off the branches, not a plan.

## THE LANES — 9 committing

Contracts: `docs/audits/2026-09-02-technical-batchg-launch-contracts/`.

```
G0  (no lane branch — serial on the PRIMARY, merged alone)   local   opus    [#613] routing carrier
G5  lane-g-632-parity                        codespace  sonnet  [#632] THE HINGE, merges first
G1  lane-g-630-lane-contract-predicate       local      sonnet  [#630] + [#629]
G2  lane-g-276-deploy-waiver                 local      sonnet  [#276]
G3  lane-g-621-freshness-absent              local      sonnet  [#621] partial — item 3 only
G4  lane-g-626-executing-copies              local      sonnet  [#626]
G6  lane-g-628-essentials-debless            local      sonnet  [#628]
G8  lane-g-614-hygiene                       local      sonnet  NC6 hygiene + one CANDIDATE
G7  lane-g-611-bundle-thinning               local      opusplan [#611] PLAN mode
G3b lane-g-621-c7                            local      sonnet  [#621] completion + C7 re-shape
```

**Every branch is `worktree-<slug>` and matches `LANE_BRANCH_RE`** (`^worktree-lane-[a-z]-\d+-...$`),
G5 included: a codespace lane commits and pushes like a local lane, merely elsewhere, so the cloud
transport's `claude/` would name a branch nothing creates (R-ENUM leg 3).

**Two slugs deviate from the batch prompt's shorthand, because the grammar refused it.**
`g5-632-parity` and `lane-g-621b-c7` are both rejected by `validate_lane_worktree_name` — the
`<id>` segment is numeric and the `<letter>` is one letter — so the lanes are `lane-g-632-parity`
and `lane-g-621-c7`. The gate is the authority over the prompt's shorthand.

## SUBSTRATE — the flip is MEASURED, not assumed

G5 ran the hub suite on both substrates against the byte-identical tree at `b5753f52`:

```
local      13 failed, 4863 passed,  4 skipped, 1 xfailed   897.22 s
codespace  16 failed, 4852 passed, 12 skipped, 1 xfailed   311.24 s
container-only: 5 nodeids beyond the two named receipt.json exceptions  ->  R2 FIRES
```

**VERDICT: FLIP.** G1–G4, G6–G8 and G3b dispatch LOCAL. The flip changed the VERB the operator
types and nothing else — no contract was rewritten for it (rulings V1/V3). Evidence:
`docs/audits/2026-09-02-verification-parity-b5753f52.md`.

## MERGE ORDER (ruled)

`G5 -> G1 -> G2 -> G3 -> G4 -> G6 -> G8 -> G7 -> G3b`. G5 first: its verdict line may flip the
rest. G3 before G6: they collide on `conformance-hub.js:133`, and G6's grep-to-zero is only
verifiable after G3 lands. G3b last: it is the completion of what G3 escalated.

**Delta A2 is the INTEGRATOR's, once per merge, serial** (ruling R-G-A2) — lanes run targeted
tests only. Base set: `docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`.
Rulings of record: `protocols/STANDING_RULINGS.md` section AC.
