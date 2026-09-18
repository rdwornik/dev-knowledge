# Lane ac-694 (insurance leg) — the live ARCHITECTURE.md byte count

**Lane:** `lane-ac-694-insurance-census` · **Branch:** `worktree-lane-ac-694-insurance-census` ·
**Batch:** AC · **Date:** 2026-09-18 · **Scope:** read-only measurement, no edits

## 1 · The number

`ARCHITECTURE.md`, measured directly (`wc -c`) at repo root, worktree HEAD: **110,357 bytes**
(107.8 KiB). Target per `[#755]`/`[#760]`: ≤ 15 KB. **Currently ~7.3× the target.**

## 2 · Sourcing the "down 22%" claim

The unsourced "down 22%" figure traces to
`docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-755-docs-cut-finish.md:63`:

> "`ARCHITECTURE.md` continues toward its <= 15 KB target through `[#667]`'s render-from-source,
> with bytes reported BEFORE and AFTER (**100,800 B at freeze, already down 22% from 129,213 B**)."

The arithmetic checks out for that snapshot: (129,213 − 100,800) / 129,213 = 22.0%. A separate
figure from that same lane's own close-packet (per this batch's `[#755]`/`[#628]` verification,
`docs/audits/2026-09-18-verification-lane-ac-694-landed-vs-claimed.md` §2) puts the post-cut
figure at 95,288 B — a second, lower snapshot from the same event, not independently re-verified
here.

## 3 · The number has since moved backward

The live file (110,357 B) is **larger than both cited post-cut snapshots**:

| Snapshot | Bytes | vs. live (110,357 B) |
|---|---|---|
| Original baseline (pre-cut) | 129,213 B | live is **−14.6%** from this, not −22% |
| "At freeze" (cited 22%-down point) | 100,800 B | live is **+9,557 B / +9.5%** above this |
| Lane-y-755 close-packet's own post-cut figure | 95,288 B | live is **+15,069 B / +15.8%** above this |

**Headline: the "down 22%" claim is stale.** Whatever cut landed, the file has grown back since —
live is only ~14.6% below the original baseline, not 22%, and has regained roughly 10–15 KB since
whichever post-cut snapshot the 22% figure or its close-packet sibling was measured against. The
≤ 15 KB target (`[#755]`/`[#760]`) remains unmet by a wide margin regardless of which snapshot is
used as the comparison point.

## 4 · Caveats

- Byte count measured on this worktree's checked-out `HEAD`; if `main` has diverged since this
  worktree was provisioned, re-measure before citing this number as current.
- The three cited historical figures (129,213 / 100,800 / 95,288 B) are taken from prior audit
  prose, not re-derived from the git blob at those commits in this lane — if a precise growth
  timeline is needed, `git show <sha>:ARCHITECTURE.md | wc -c` at each cited commit would confirm
  them directly.
