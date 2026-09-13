# Batch X wave 3 — close packet · 2026-09-13

**Seat:** integrator · **Batch:** X, wave 3 · **Closes:** `docs/audits/2026-09-13-technical-batch-x3-manifest.md`
**Authority for every disposition below:** `to-browser/RATIFICATION-2026-09-13.md` (operator acts only, 2026-09-13).

> This packet is the `closed_by:` target the X3 manifest names. Landing it ENDS the
> ADR-110 declared-integration-arc exemption for batch X3 by construction: the exemption
> requires the closer ABSENT from the tree, and `docs/audits/` is immutable, so an expiry
> that depends on a mutable flag is no expiry at all. From this commit forward every merge
> pays its own anchor arc again until a new manifest declares a batch open.

---

## 1 · What this seat found on arrival, stated before anything else

**The four fired lanes, and the two backfill lanes with them, were ALREADY MERGED when this
seat booted.** This packet does not claim those merges. They were taken earlier the same night
by the integrator seat that ran waves 2 and 3; the spine below is read out of git, not
performed here.

What this seat did perform: the arrival survey, the origin sweep, the conductor read, the
ratification's item 5, the filings its items 3 and 4 order, this packet, and the four rows §6 files.

**Recorded because a close packet that reads as though one seat did all of it is exactly the
"close-out a reader can skim past and still declare done" that the refuse-to-finish checklist
exists to replace.**

---

## 2 · The merge spine — six lanes, every one merged

Read from `git log --first-parent`. Every lane merged `--no-ff`; no lane was abandoned.

```
slot  lane branch                              merge SHA  lane tip  merged (local)
1     worktree-lane-x-689-conductor-e-proof     959a00fc   605a20f5  2026-09-13 02:41
6     worktree-lane-x-000-docs-cut-manifest     ab7b84a9   6dcda4fd  2026-09-13 03:46
2     worktree-lane-x-000-trustworthy-suite     81c0a4c9   64230d8d  2026-09-13 04:08
3     worktree-lane-x-683-three-small-fixes     78823b05   b2702947  2026-09-13 04:30
4     worktree-lane-x-730-one-command-closure   83961dde   de578835  2026-09-13 05:39
5     worktree-lane-x-664-spine-armed           1d7bdddb   ff07de9a  2026-09-13 06:27
--    worktree-dispatch-x3-freeze               0c56a7c8   7f2012cb  2026-09-13 06:43
--    docs/batch-x3-close                       dbac84b8   22542c76  2026-09-13 06:59
```

**Each lane was on current `main` at its merge.** Five carry an explicit `Merge branch 'main'`
sync commit (`605a20f5`, `64230d8d`, `44c84024`, `26ed479d`, `858fe26e`). The sixth —
slot 6, docs-cut — needed none: it was dispatched on `95e162c8`, which `git merge-base
--is-ancestor` confirms was already the spine tip it merged into. **Verified rather than
assumed, because "no sync commit" and "not synced" look identical in a log.**

**Anchor cost: one arc per lane, five lane anchors plus the batch close anchor, despite the
exemption being live.** The X3 manifest §6 finding 8 predicted the exemption would spare wave 3
what wave 2 paid; the spine shows it did not. **An open discrepancy, not a closed one** —
triaged in §7 as F6 rather than smoothed away.

---

## 3 · Refuse-to-finish checklist (Ch8) — all five, mechanically

- **1 · every lane branch merged-or-explicitly-abandoned — PASS.** Six of six merged, §2.
  `git branch -r --no-merged origin/main` returns `origin/automation/fleet-audit` ALONE — the
  nightly routine's branch, not a batch-X lane. Swept on ORIGIN, not only locally, because a
  clean local tree is not evidence about the remote.
- **2 · full suite run once on the merged result — RAN, READ, AND RED.** Conductor run
  `34739225286` and its scheduled re-run `34750332267`, both at `dbac84b8`:
  **51 failed, 5999 passed, 21 skipped.** Read in full in §4.
- **3 · `git worktree list` == primary only — PASS.** One line, the primary. Every lane
  worktree torn down.
- **4 · manifest/packet archived, TWO halves — PASS on landing this file.** The manifest was
  committed at DISPATCH (`0c56a7c8`), its frontmatter parses, and `batch_manifest.open_batches()`
  returns X3 — called directly, not inferred from a gate. This packet is the second half.
- **5 · `git stash list` empty — PASS.** No entries. The item the other four structurally
  cannot cover, since `refs/stash` lives in the common git dir and is neither a branch nor a
  worktree.

`main` local == `origin/main` == `dbac84b8`, read with `git ls-remote` rather than from a
cached remote ref.

---

## 4 · Item 2 in full — the suite ran on the merged tree, and this seat READ it

The operator's standing instruction is that the full suite runs on the Actions conductor and
**not** on this box. It did. `[#675]`'s target 2 is explicit that a green run nobody reads is
not a gate, so what is recorded here is the reading, not the exit code.

**The merged tree is RED at 51 failures. The batch did not cause it.**

```
time   run          headSha   failed passed skipped  what landed
23:52  34726541930  ec18875e      55   6068      18  (previous day's last)
00:28  34728040263  35e42ccb      53   5937      22  batch-x2 closures [#727]
00:57  34729284770  95e162c8      53   5937      22  conductor-E anchor
02:21  34732844663  ea64a940      53   5944      22  first run AFTER the trustworthy-suite lane
02:44  34733771343  89a149ea      53   5952      22  683 anchor
03:48  34736402019  34daf06a      53   5970      22  730 anchor
05:00  34739225286  dbac84b8      51   5999      21  batch-x3 close
09:49  34750332267  dbac84b8      51   5999      21  scheduled re-run, same tree
```

- **Monotonically NON-INCREASING all day: 55 → 53 → 53 → 53 → 53 → 51.** Passing climbs 5937 → 5999.
- **Zero new failing node ids were introduced after 00:28.** The failure SET is byte-identical
  across `35e42ccb`, `95e162c8`, `ea64a940`, `89a149ea` and `34daf06a`, compared as sorted
  node-id lists. The batch-x3 close CLEARED two (`test_gen_audit_index.py`, both legs) and
  added none.
- **The trustworthy-suite lane specifically added zero failures and moved +7 passing.** Worth
  stating because a lane named "the suite stops lying" invites the suspicion that it made the
  number worse. It did not, and its scope was three named defects, never "the suite goes green"
  — its own evidence file says so and reports its final targeted run as 6 failed.

**Composition of the 51, classified rather than counted:**

- **21 are ENV-only.** They assert Windows path semantics, the operator's home tree, the fleet
  registry of sibling repos, armed local git hooks, or a persisted graph store that only a
  pre-commit hook builds — against `ubuntu-latest` on a fresh clone. **The conductor `pytest`
  job as currently written CANNOT go green.** A finding about the gate, not the tree (§7 F1).
- **28 are DATA drift** — hard-coded counts, curated baselines and generated views the repo has
  outgrown (the BACKLOG view at 89,338 B against a 72,000 B bar; a stale `north-star.md`).
- **2 look like genuine code defects** — an unbuilt `--repo-root`/`--cross-repo` CLI pair behind
  a frozen-contract requirement, and a dual-import identity assert.

**So item 2 holds in the sense the checklist can bear: the suite ran once on the merged result,
on the conductor, and was read.** It does NOT hold in the sense of green, and this packet does
not claim it does.

---

## 5 · Ratification dispositions — the three rows the operator ruled on

### `[#727]` — **CLOSED** · proving SHA `a8dee4ac`

Closed on wave 2, recorded here because this is batch X's close. Its amended clause
(*"`[#727]` does not close until that clause is green"*) is green: the three declared
allow-on-failure paths refuse, each naming cause and fix, each with a RED-first trip-test.

**Proved beyond its own tests, twice, on this seat.** `deny_and_point` refused two of this
session's own `Bash` calls — a raw search over `scripts/actions_verdict.py` and another over
the module named in ratification item 5 — and in both cases named the organ to run instead
(`file_purpose_graph.py why`, `graph_queries.py process-list`, `impacted_tests.py select`).
**A guard that fires on the seat closing its own batch is the strongest available evidence
that it is not a paper gate.**

**Caveat recorded, not buried:** the two CI tests named
`test_a_CRASH_MID_EVALUATION_fails_CLOSED` and `test_an_UNRECOGNISED_VERDICT_fails_CLOSED`
are RED on the conductor. The cause is a **test** defect, not a fail-open guard — a fresh
clone has no persisted graph store, so `deny_and_point.py:701` short-circuits on an empty
process list and the monkeypatched `decide` is never reached. The mechanism is sound; it
fired live on this seat. Triaged as F2.

### `[#675]` — **HELD OPEN** (operator: NO-GO)

Its Done-when is *"six things, all six and not a pick-list"*. Three carry verified false-pass
holes, each **resolved in the code by this seat before filing** rather than carried on the
review's word:

- **Target 2** — `scripts/actions_verdict.py:205-213`. A failed `gh run view --json jobs` is
  swallowed into an empty job list on every path (non-zero exit, `OSError`,
  `SubprocessError`, `JSONDecodeError`). `verdict_for` then computes an empty failing set and
  returns `STATE_PASS`. **An unreadable run reports PASS** — and the same function's FIRST `gh`
  call already raises `ActionsUnavailable`, so the module knows how to say "I could not read
  this" and the second call simply does not use it.
- **Target 4** — `scripts/seat_refusals.py:304-306`. The directory group in `_CONTRACT_PATH_RE`
  is `+`-quantified, so a path needs at least one slash to be seen at all, and `_WRITE_ROOTS`
  is eleven slash-terminated prefixes. **Every root-level tracked file is invisible to the
  collision extractor** — `ARCHITECTURE.md`, `CLAUDE.md`, `JOURNAL.md`, `.pre-commit-config.yaml`,
  `pyproject.toml`. Live right now: the same ratification's item 7 GO'd a cut to `ARCHITECTURE.md`.
- **Target 6** — `scripts/merge_receipt.py:448-457`. `median_report` filters on `kind` and
  nothing else; `Receipt.closed` is `Optional[str] = None`, so an abandoned merge is a valid
  receipt with fewer steps, a shorter wall time, and a vote in the median — **pulling it toward
  the under-30 target precisely when the process fails.**

**Filed as `[#742]`, `[#743]`, `[#744]`** (§6). The wave-2 verdict sheet recommended routing
them to intake as CANDIDATEs; **the operator's ratification is the ratifying act (ADR-111), and
it says they become rows**, so they are rows.

### `[#734]` — **HELD OPEN** (operator: NO-GO)

Done-when clause 2 is undischarged: *"the 16 UNKNOWN are resolved to a live/non-live verdict by
a second pass rather than carried forward."* The stage-2 evidence file (730 lines) **does not
contain the string `UNKNOWN` at all**, and stage 1 recorded the position explicitly. The row
predicted its own failure mode — clause 2 is *"the clause most likely to be quietly dropped,
because an UNKNOWN is the one bucket that costs work to empty and looks harmless full."* It was.

KEPT items keep their reasons (8 in `deploy/lived_sandbox/`, 7 on positive evidence).
**Filed as `[#745]`** (§6).

---

## 6 · Rows filed by this packet

- **`[#742]` · P1/S** — `actions_verdict` reports PASS when job details cannot be read. Parent: `[#675]` target 2.
- **`[#743]` · P1/S** — the step-0 collision extractor is blind to root-level files. Parent: `[#675]` target 4.
- **`[#744]` · P1/S** — `median_report` counts incomplete receipts. Parent: `[#675]` target 6.
- **`[#745]` · P1/M** — the census's 16 UNKNOWN resolved by a second pass. Parent: `[#734]` clause 2.

Every one carries a RED-first acceptance clause per ADR-108 §B. None carries a kill-candidate:
both parents stay OPEN by the operator's own act, so closing either would orphan the remainder
— which is exactly what the two NO-GOs refused.

---

## 7 · Findings — triaged per ADR-111, one bucket each, none left untriaged

**F1 · The conductor `pytest` job cannot go green as written — 21 of 51 failures are ENV-only.**
It runs `ubuntu-latest` on a fresh clone, and the suite contains tests asserting Windows path
semantics, `~/.claude/`, the sibling-repo fleet registry, armed local hooks and a graph store
built only by a pre-commit hook. **A gate whose green state is unreachable is not a gate**, and
the operator's instruction to run the suite there rather than on his box makes this load-bearing
rather than cosmetic. → **CANDIDATE.**

**F2 · The two `deny_and_point` fail-closed tests are red for a test-fixture reason, and the
distinction matters.** A reader scanning CI sees `[#727]`'s fail-closed guarantee failing. The
guard is fine — it fired twice on this seat. The tests do not seed a graph store, so
`deny_and_point.py:701` returns allow before the monkeypatched `decide` runs. **A red test named
`fails_CLOSED` against a guard that does fail closed is worse than no test**, because it trains
the reader to discount it. → **CANDIDATE.**

**F3 · One invalid YAML value REDs six tests.** `docs/intake/2026-09-11-tech-batch-x-roster.md`'s
frontmatter has an unquoted `origin:` whose value contains a bare `mechanism: evidenced bulk
closure`; `yaml.safe_load` raises at line 4 col 697, frontmatter parses to empty, and every
downstream funnel field renders "unavailable". **Quoting one value clears 6 of the 51** — the
highest-leverage single fix on the board. Not executed here: no ratified GO covers it and it is
outside this packet's scope. → **CANDIDATE.**

**F4 · `offload_admission.py`'s swap detection is defeated by inode reuse on Linux.** The Z-G4
guarantee captures `(st_dev, st_ino)` and re-reads it; an `rmdir()`+`mkdir()` on Linux commonly
reuses the freed inode, so identity is unchanged and detection never fires. **The docstring's
guarantee does not hold on the platform the conductor runs.** → **CANDIDATE.**

**F5 · The trustworthy-suite lane's `skipif` markers enlarged the `test_proof_layer` guard
population above its curated baseline.** A known ratchet class: adding a skipped test trips the
proof-layer count. The baseline needs updating; the lane is not at fault for the mechanism.
→ **CANDIDATE.**

**F6 · The ADR-110 exemption was live for wave 3 and an anchor arc was paid per lane anyway.**
The X3 manifest §6 finding 8 established that batch X and X2's manifests carry no frontmatter,
so `open_batches()` returned empty and wave 2 paid an anchor per merge. X3's manifest fixed
that — `open_batches()` now returns X3, confirmed by calling it directly. **Yet the spine shows
an anchor arc per lane anyway.** Either the exemption does not reach the case it was written
for, or the merging seat did not take it. **AX28-3 names integration throughput as the night's
real constraint, so this is the finding with the largest standing cost.** → **CANDIDATE.**

**F7 · No Codex review artifact landed in-tree for waves 2 or 3.** `docs/audits/` holds no
`*codex*` file dated after 2026-09-07, and the transport holds none for 09-12 or 09-13. The
reviews demonstrably RAN — they produced the three verified `[#675]` holes — but their only
durable record is `to-browser/CLOSURE-VERDICTS-2026-09-13.md`, outside the repo. The X3
manifest §7 noted an uncommitted stub (`2026-09-13-codex-x727-fail-closed.md`, tally `TBD`); it
is in neither the tree nor the working copy. **A review whose findings survive only as someone's
summary is a review that cannot be re-read against the code.** → **CANDIDATE.**

**F8 · The docs cuts are ratified GO and UNEXECUTED, so this batch removed no bytes.** Item 7
GO'd three: ARCHITECTURE's prologue cut to the reader-routing guide (30,122 B → ~1 KB),
ESSENTIALS retired under `[#628]` (16,461 B), PLAYBOOK's review-pass blockquotes cut (within a
7,836 B prologue). The wave-3 docs-cut lane was **proposal-only by its own contract** — its
closing commit reads *"confirm nothing cut"*. **Roughly 53 KB is approved for removal and none
of it has been removed.** → **OWNED** by the GO itself, needing an execution lane, which is the
operator's dispatch rather than this seat's act.

**F9 · Ratification items 2 and 6 are likewise ratified and unexecuted.** Item 2 (6 DELETE,
2 TRIGGER, 28 KEEP, with `cost_usage_telemetry.py`'s stale disposition text corrected) and item
6 (remove the dead callers — `.devcontainer/provision.sh`'s six call sites of the retired
`cloud_provisioning.py` at 349/350/367/368/585/587, and `tests/test_e2e_consumer_lifecycle.py:94`'s
importlib load of the retired `boundary_report.py` — *without* restoring the modules, plus one
row for what provisioning's history/ecosystem repair actually needs). → **OWNED** by the GO,
awaiting an execution lane.

**F10 · `#369` is moot and still open** — the boundary-headers generator's pre-commit wiring,
now that `boundary_headers.py` is retired. Flagged by the x-734 lane, which correctly declined
to disposition another row itself. → **CANDIDATE** for retirement at the next grooming.

**F11 · Ratification item 1 is routed, not ruled.** Command files DO count as a `[#664]` wiring
surface — YES, with ADOPTION-BY-INVOCATION attached: an organ no command has actually called in
30 days returns to the register, the same counter as AX9-5. The operator was explicit that this
goes **through the decision engine (`[#692]`, on `main` at `a77e3302`), not ruled in chat**:
intake → alternatives → response measure → flip condition → ADR, with the ratification as its
input. → **OWNED** by `[#692]`. Recorded here only so the routing is not lost between packets.

**Discharged by this packet:** ratification item 5 — the `ORPHAN_DISPOSITIONS` entry for the
lane-seed module is deleted (it is reachable over `TRIGGER_KINDS` via `gen_lane_contract.py`).
This was ALSO the trustworthy-suite lane's open handback item 2 to the integrator, and it was
RED on the conductor. `tests/test_graph_spine.py` — **37 passed**; the full impacted-test set
for the changed module — **green**. → **DISCHARGED.**

---

## 8 · What this seat did NOT do

- **No lane was merged by this seat.** All six were already on the spine (§1).
- **No full suite was run on this box.** Operator instruction; the conductor is the surface, and
  §4 is the reading rather than a re-run. Targeted tests only.
- **No ratified-but-unscoped GO was executed.** Items 2, 6 and 7 are GO and are left for an
  execution lane, named in F8/F9 with their byte figures so the next dispatch can size them.
  Item 5 WAS executed: one line, handed to the integrator by a lane in this batch, and red in CI.
- **`[#675]` and `[#734]` were not closed.** The operator ruled NO-GO on both; their remainders
  are `[#742]`–`[#745]`.
- **No row was reopened.** `[#683]` is closed and the X3 manifest §6 finding 9 records that
  slot 3's contract cites it as live work. Reopening is the operator's act.

---

## 9 · Batch X3 — CLOSED

Five checklist items verified in §3, item 2 with the explicit qualification of §4. Six lanes
merged, zero abandoned, zero leftovers, four rows filed for the two held remainders, eleven
findings triaged, one ratification item discharged.

**The exemption ends with this file.**
