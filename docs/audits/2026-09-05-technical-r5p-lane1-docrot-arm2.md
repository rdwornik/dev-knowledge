# R5P lane 1 — `doc_rot` ARM 2 reports the CORPUS, not one WARN per row

**Consumers:** the R5P batch merge queue (this is lane 1 of 3, operator-declared at R5 B5);
`[#532]` is the closed arc that BUILT the two arms and whose §A9 posture this preserves;
`ADR-75` governs the disposition-register decoration this change triggers (§5 below).

**Lane:** `lane-r-000-docrot-arm2` · branch `worktree-lane-r-000-docrot-arm2` ·
contract `LANE-r-000-docrot-arm2.md` · no BACKLOG row (`000` is the no-row id; none filed).
**Owned files:** `scripts/validate_doc_rot.py` + `tests/test_validate_doc_rot.py`. Nothing
else was edited.

---

## 1. The before number, measured

Contract step 1 asked for the live per-row WARN count and forbade restating one from the
contract or a module comment. Measured by calling `validate_doc_rot.scan()` on this tree at
the branch point, 2026-09-05:

```
75  doc_rot findings total
70    backlog-row-length   <- ARM 2, ONE WARN PER ROW. The before number.
 3    backlog-accretion    (ARM 1)
 1    grooming-cadence
 1    section-history
```

Two numbers in the module's own `[#532]` memo were already stale by construction, which is
why the contract forbade restating them: it records **ARM 2 = 10 rows** and **ARM 1 firing
on ZERO**. Live today: 70 and 3. The memo is a dated measurement, not a claim about now, so
it was left alone — amending it is not this lane's file scope and would replace one stale
number with another.

## 2. The after number

```
 6  doc_rot findings total
 1    backlog-row-length   <- ONE corpus-level Finding
 3    backlog-accretion    (byte-identical)
 1    grooming-cadence     (byte-identical)
 1    section-history      (byte-identical)
```

The one Finding, verbatim from the live CLI:

```
backlog-row-length  BACKLOG#row-length  ->  70 of 224 rows over the declared ceiling 1320
chars (LONG, not rot: a row may be long for a ruled reason); longest 5315 chars; row-length
p50/p75/p90 over all 224 rows = 1259/1545/2214 chars; trend: +1 vs previous run (69 -> 70)
```

**The median backlog row is 1259 chars against a 1320 ceiling.** Seventy per-row WARNs
carried that fact and none of them stated it. That is the argument for the reshape in one
number: the ceiling is not a line a few outliers cross, it is a line the corpus is sitting
on, and no quantity of "this row is long" says so.

## 3. Done-contract, item by item

| # | Contract | Status | Evidence |
|---|---|---|---|
| 1 | ONE Finding carrying count / p50-p75-p90 / trend, with the before-count MEASURED | **MET** | §1 and §2 above; count measured, not restated |
| 2 | Every other arm byte-identical; PROVE it | **MET** | §4 — proved twice, live and in a pinned test |
| 3 | Seeded 3-row fixture yields 1 Finding naming 3 | **MET** | `test_arm2_emits_one_corpus_finding_naming_three_over_ceiling_rows`, asserting `3 of 4 rows over the declared ceiling 1320 chars` |
| 4 | `pytest` green on the targeted tests | **MET, with one pre-existing RED that is not this lane's** | §6 |

Also held: `_BACKLOG_ROW_CEILING` is still 1320 (reported against, never changed); ARM 1's
predicate, output and per-row locus are untouched; no new persistence store exists.

## 4. "Byte-identical" — proved twice, not asserted

**Live.** The five non-ARM-2 findings were captured from `scan()` before the module was
edited and compared string-for-string (`category|locus|detail`) after. Result: equal, 5/5.

**Pinned.** `test_every_other_arm_is_byte_identical_across_the_arm2_reshape` builds a
fixture repo that fires **all five** sub-detectors at once and asserts category, locus AND
detail of every non-ARM-2 finding, in order, against literals captured from the pre-reshape
module. It is deliberately GREEN on both sides of the change — a pin of "unchanged" that
went RED before the change would mean the pin was wrong, not that the change was right. It
is recorded here as such rather than counted among the RED-first witnesses.

The one thing that is NOT identical, stated precisely rather than glossed: ARM 2's finding
moved to the END of the BACKLOG block instead of interleaving with ARM 1 row by row. The
other arms' findings are unchanged in content and unchanged in their order relative to each
other; only ARM 2's position among them moved, which is unavoidable when N findings collapse
into one.

## 5. The locus moved — one consumer this lane may not edit

ARM 2's locus changed from `BACKLOG#<id>` to `BACKLOG#row-length`. Four entries in
`ecosystem/disposition-register.yaml` key on the per-row signature — `warn-row-length-546-*`,
`-547-*`, `-552-*`, `-533-*`, each matching `backlog-row-length BACKLOG#<id> (<n> chars`.
They now match nothing and will **decorate STALE**, which is `ADR-75` awareness output and
does not block. The single corpus WARN is undispositioned.

**Net effect on the #147 ship-gate is a reduction, not a regression:** before, 70 ARM-2 WARNs
of which 66 were undispositioned; after, 1. Naming its replacement disposition is a curated-
baseline act and the register is outside this lane's owned files, so it was not touched —
per the V-2 budget this is reported, not asked. The four stale entries carry real rulings
(`[#532]`/A9 acceptances) whose substance is unaffected; only their match key is dead.

Second-order, worth naming because it is quiet: `gen_trend_dashboard.collect_doc_rot` plots
the COUNT of doc_rot findings per dated snapshot. Its series will step from ~75 to ~6 at the
first snapshot after this lands. That is a units change in the panel, not a drain — nothing
was fixed, one number was collapsed into one Finding. `parse_doc_rot_count` needs no code
change; a reader of the panel needs the warning, which is why it is here.

## 6. Tests

Targeted run (`tests/test_validate_doc_rot.py`, `test_canonical_docs.py`,
`test_archive_row_body.py`, `test_gen_trend_dashboard.py`, `test_trend_dashboard.py`):
**252 passed, 1 failed.**

The failure is `test_live_corpus_has_no_accretion_arm_findings_only_length_findings`, and it
is **not this lane's**. It was captured RED at the branch tip BEFORE any edit here — baseline
at `ac2c6a15`: 1 failed, 46 passed, same test, same three loci (`BACKLOG#267`, `#297`, `#82`).
ARM 1 now fires on three live rows whose inline date spans crossed the 30-day arm with the
calendar; the assertion pins a live-corpus zero that the calendar retired. ARM 1 is
untouched by this lane, and fixing that assertion is an ARM-1 act the contract forbids here.

RED-first witness for step 2, recorded before any module edit: **17 failed, 44 passed**.

`ruff check` clean on both files.

## 7. Decisions taken under the frozen defaults (reported, not asked)

* **Percentiles over the WHOLE corpus, not the flagged rows.** Over the flagged rows all
  three sit above the ceiling by construction and are uninformative by construction.
* **Nearest rank, never interpolated** — every reported percentile is a real row length that
  exists in the corpus and can be looked up. An interpolated p90 belongs to no row.
* **The Finding is CONDITIONAL on at least one row being over.** An unconditional corpus
  Finding would mean `scan()` never returns empty and `doc_rot` never emits `pass`. Clean
  stays clean; "exactly one Finding" means at most one, never a mandatory one.
* **Severity unchanged** — the adapter still emits WARN, as it did for each of the 70.
* **The trend reads an existing surface: `ecosystem/.dev-knowledge/state.yaml`**, the
  previous run's own findings, the same hub-relative literal
  `gen_trend_dashboard.collect_doc_rot` already hardcodes (so a worktree resolves it exactly
  as the primary does). **No new store was created.** It reads BOTH prior shapes — the legacy
  one-entry-per-row form and the new corpus form — so the trend was live on the first run
  (`+1 vs previous run (69 -> 70)`) instead of spending a cycle at `n/a`. Absent,
  unparseable, or a state file with no `doc_rot` finding at all yields
  `n/a (no prior run recorded)`, never a fabricated zero; that last distinction is inherited
  from `gen_trend_dashboard.parse_doc_rot_count`, which had to rule on it for this same
  check. Fail-soft in full — nothing this surface can do degrades the detector.
  **Caveat, stated because it bounds the term's value:** `state.yaml` is gitignored, so on a
  fresh clone or in CI the trend reads `n/a` until a full `audit run` has written one. The
  frozen default anticipated exactly this and it needed no escalation.
* **The Finding detail is ASCII-only.** Its first live run rendered an em-dash as `?` on a
  cp1252 console, and this string lands in machine-read evidence — `state.yaml`, the trend
  dashboard, and any disposition `match:` an operator writes against it.

## 8. Open items for the integrator

1. **A replacement disposition for the single corpus WARN**, if the ship-gate should stay
   quiet on it. Suggested key: the stable prefix `backlog-row-length BACKLOG#row-length`
   WITHOUT the count, since the count now moves every run and a count-bearing match would
   go stale immediately. The four dead per-row entries can be retired in the same act.
2. **`docs/audits/README.md` is left stale on purpose** — `[#590]` narrowed
   `audit-index-freshness` so lanes stop colliding on it. The integrator regenerates once on
   the merged result (`gen_audit_index.py --write`, `git add` first).
3. **`ecosystem/doc-counts.md` is stale** — this lane adds tests and the contract forbids
   index regeneration. Owed at integration.
4. **No JOURNAL entry was written** — the integrator owns the anchor. SHAs in §9.
5. **No R5P batch manifest is committed on this tree.** Searched `docs/audits/`, `tasks/`
   and `protocols/` for `R5P`: nothing. Flagged because a batch with no committed manifest
   is not integrable through the normal merge queue, and because an audit linked from a
   committed manifest counts as CITED — this artifact therefore declares its consumers
   explicitly at the top instead.
6. **The pre-existing ARM-1 RED (§6) still needs an owner.** It is a calendar-driven
   assertion failure on `main`, not a regression, and it will not clear on its own.

## 9. SHAs

```
2b9582e7  test(doc_rot): RED first -- ARM 2 owes ONE corpus Finding, not one WARN per row
3752728d  fix(doc_rot): ARM 2 reports the CORPUS -- 70 per-row WARNs become 1 Finding
```

Both sit on `worktree-lane-r-000-docrot-arm2` above `78daf400`. The lane was
`--ff-only` synced from `ac2c6a15` to `78daf400` before its first commit:
`audit-health`'s `journal_spine_anchor` was RED on four spine entries, and the two-tree
diagnostic showed the gap in this tree only and empty against main's own `JOURNAL.md` —
pure lane tree-lag, not a real unanchored merge. Re-run after the sync: empty in both.
**No bypass was used anywhere in this lane** — no `SKIP=`, no `--no-verify`.
