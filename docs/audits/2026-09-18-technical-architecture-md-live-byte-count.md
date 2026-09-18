# ARCHITECTURE.md — live byte count, and where the "down 22%" figure comes from

**Measured:** 2026-09-18 · **Method:** `wc -c` on the live tree, plus a repo-wide grep for the
figure's every occurrence and a `git log --follow` read of the file's own commit history.

## The live number

```
PS/sh> wc -c ARCHITECTURE.md
110357 ARCHITECTURE.md
```

**110,357 bytes today** (1,179 lines). `ARCHITECTURE.md` carries no stated size-budget entry of its
own — `[[architecture-md-has-no-size-budget-entry-the-15kb-is-a-target]]` — the ≤15 KB figure cited
below is a target named elsewhere, not a gate this file enforces on itself.

## Where "down 22%" comes from

Repo-wide grep for the figure found exactly one place it is COMPUTED and one place it is
RESTATED as an established fact:

- **Computed, at freeze:** `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-755-
  docs-cut-finish.md:63` — *"`ARCHITECTURE.md` continues toward its <= 15 KB target through
  `[#667]`'s render-from-source, with bytes reported BEFORE and AFTER (100,800 B at freeze, already
  down 22% from 129,213 B)."* `(129213 - 100800) / 129213 = 21.99%` — the arithmetic behind "22%"
  checks out against those two numbers, both stated as the lane's OWN before/after at its freeze
  point (2026-09-14), not as a standing claim about the file today.
- **Restated as fact, later, with no percentage recomputed:** `docs/intake/2026-09-16-tech-browser-
  seat-findings-off-the-transport.md:289` — *"Docs — ARCHITECTURE −22 %, ESSENTIALS gone..."* — carries
  the figure forward two days later with no fresh byte count behind it.

## The live number does not match either historical figure

```
git log --oneline --follow -- ARCHITECTURE.md   (relevant span)
530dbecf docs(755): relocate ARCHITECTURE prose to the docstrings that own it -- 107,266 B -> 95,288 B
```

Three numbers, three different moments, none matching today:

| Point | Bytes | Source |
|---|---|---|
| Baseline the 22% was computed against | 129,213 B | LANE-y-755 contract, "at freeze" |
| LANE-y-755's own reported AFTER | 100,800 B | same line — `-22%` from baseline |
| A LATER commit's own before/after (`530dbecf`) | 107,266 B -> 95,288 B | commit subject line, `[#755]` |
| **LIVE, measured today** | **110,357 B** | `wc -c`, this measurement |

**The file grew back after both cuts.** 110,357 B is *higher* than every post-cut figure on record
(100,800 B and 95,288 B) and is only **14.6% below** the original 129,213 B baseline
(`(129213 - 110357) / 129213 = 0.1459`), not 22%. Something added roughly 15,000-19,000 bytes back
into the file after whichever cut the 22% figure describes, and no later commit subject in the
file's own `--follow` history recomputes or corrects the percentage — the intake doc two days after
the cut restates "−22%" as if it were still current, and nothing since has re-measured it against
the live tree.

**Disposition:** the 22% figure is **sourced but STALE** — correct arithmetic against the two
numbers it cited at the time, silently carried forward as fact through at least one later doc
without being re-measured, and false against the file's live state today (14.6%, not 22%).
