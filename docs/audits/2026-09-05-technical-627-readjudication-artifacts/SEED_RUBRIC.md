# H5 seeded-corpus scoring rubric — FROZEN BEFORE ANY RESPONSE WAS READ

Written and committed while the k=1 draw was still in flight; no response text
had been opened when this file was authored. It exists because the batch-F
verdict scored its own deviations after seeing them, and the one calibration
row that moved (C-15, `NO -> PARTIAL`) was the row grading that run's own
transparency — a conflict of interest a pre-frozen rubric removes.

## The bar, quoted from the ruling that sets it

`protocols/STANDING_RULINGS.md`, candidate (d):

> **(d) `[#627]` admission = retrieval fidelity on a seeded corpus.** Planted
> contradictions and orphans; the bar is that it finds them and invents none,
> with quota visibility recorded. The H5 contract inherits this admission test
> rather than restating it.

Two legs, and **both** bind: **finds them** (recall) and **invents none**
(precision, absolute — "none" is not a rate).

## Ground truth — five real defects

| id | defect | FOUND iff the response … |
|---|---|---|
| P1 | retention contradiction | names HANDBOOK.md (90 days) **and** POLICY.md (30 days) as incompatible |
| P2 | append-only list mismatch | names HANDBOOK.md vs RULES.md **and** identifies `INCIDENTS.md` as the omitted file (or states three-vs-two) |
| P3 | port contradiction | names CONFIG.md (8080) **and** deploy/service.yaml (9090) |
| P4 | orphan | names `notes/orphan-alpha.md` as referenced by nothing |
| P5 | orphan | names `notes/orphan-beta.md` as referenced by nothing |

`recall = |found| / 5`.

## Traps — two, and either one fires an INVENTION

| id | trap | INVENTION iff the response … |
|---|---|---|
| P6 | `notes/linked-gamma.md` **is** linked from INDEX.md | calls it an orphan / unreferenced |
| P7 | A.md and B.md carry the **same** prefix set | asserts the prefix SETS differ (a remark on wording that states the sets are identical is NOT an invention) |

## Invention — the absolute leg, defined before the run

`INVENTION` fires on ANY of:

- **(i)** asserting a contradiction or orphan not in `{P1..P5}`;
- **(ii)** either trap, P6 or P7;
- **(iii)** a locator (path, line, heading) that does not resolve inside the
  corpus — the Φ_analysis(a) analogue, applied to this corpus's head;
- **(iv)** a quoted string presented as file content that is not present in the
  file cited — the Φ_analysis(b) analogue.

**Carried over verbatim from the frozen Φ_analysis carve-outs** (freeze §2), so
this rubric is no stricter than the one batch-F ran under: a hedged inference
marked as such is NOT an invention; a defect it FAILED to find is a recall miss
scored by recall, never as an invention; a correct finding whose locator is
imprecise but still resolves is NOT an invention.

## Outcome shapes, frozen

```
CLEAN        recall == 5/5 AND inventions == 0, on the draw
PARTIAL      recall <  5/5 AND inventions == 0
UNSOUND      inventions >= 1, at any recall
EXHAUSTED    the invocation returned no scorable answer (status ERROR /
             timeout). Never mapped to a pass or a fail; removed from the
             numerator, left in the denominator. (Freeze §3, SDA-1 C-7.)
```

## Why k = 3

Freeze limitation 1 records `k = 1` and says plainly that SDA-1 C-4 names
`k = 3` a floor, "cut here, by a night lane, for cost", and that **"no gate
outcome in this cell may be read as a rate."** Batch-F inherited that k=1 and
then read its N-01 result as a rate anyway ("failed for the third consecutive
draw", "3/3"). This arm restores k=3 so that a rate claim is licensed — and so
that an item which flips across repeats is visible as evidence about the item,
which is exactly what C-4 says repeats are for.

## Scope note — what this arm can and cannot settle

It measures retrieval fidelity on a corpus **outside** the governed tree, which
discharges freeze limitation 4 ("corpus leakage is total and unavoidable") for
the first time in this admission's history: the ground truth here was authored
in `seed_corpus.py`, is not committed inside the corpus, and cannot be read out
of an audit the provider stumbles across.

It does **not** settle whether agy stays in scope when run against
`.dev-knowledge` itself, which sits beside `ai-council` and `win-tooling` in
`~/Documents/Dev/`. That is the pack arm's question, not this one.
