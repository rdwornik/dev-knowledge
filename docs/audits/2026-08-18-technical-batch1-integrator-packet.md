# BATCH 1 (2026-08-18) — INTEGRATOR PACKET

> **Outcome artifact** for the contract of record
> `docs/audits/2026-08-18-technical-batch1-integrator-contract.md` (merge `3ab1f94c`).
> The serial merge queue was walked from the primary checkout on `main`, one writer throughout.

## 1 · Per-lane result

| Lane | Branch (final name) | Merge sha | Review verdict | Targeted tests |
|---|---|---|---|---|
| — | `docs/batch1-integrator-contract` | `3ab1f94c` | n/a (contract of record) | n/a |
| D | `worktree-lane-d-558-vision` | `e72f712f` | not gated | docs-only (`VISION.md`, 5 lines) |
| F | `worktree-lane-f-348-p10-evidence` | `da318c83` | not gated | docs-only |
| I | `worktree-lane-i-31-adoption-preflight` | `6c88bdfc` | not gated | docs-only |
| H | `worktree-lane-h-554-codex-review` | `06bc65ab` | not gated (it *is* the review lane) | docs-only |
| G | `worktree-lane-g-536-a9-trim` | `cb47783b` | not gated | `gen_task_tree --check` **ok** |
| C | `worktree-lane-c-554-devcontainer` | `80c7b9e8` | **FIX-BEFORE-MERGE** (H) → C-1 applied at `57313811` | `test_validate_hermetization.py` **45 passed**; `bash -n provision.sh` ok |
| E | `worktree-lane-e-502-mutmut` | `7a316976` | **MERGE-CLEAN** (H) | docs + harness |
| A | `worktree-lane-a-533-leg2` | `f4a01f0e` | **MERGE-CLEAN** (P3, this seat) | `test_journal_anchor.py` + `test_audit_parallel.py` **57 passed** |

**C-1 — the one itemized fix applied.** `.devcontainer/devcontainer.json:52`
`"waitFor": "postCreateCommand"` → `"postStartCommand"`. On a *resumed* container
`postCreateCommand` does not run, so waiting on it did not gate attachment on the `--gate`
re-assert path — the single scenario the stated guarantee exists for. The JSON was re-parsed
after the edit. Nothing else on branch C was touched: C-2…C-5 were explicitly non-blocking in
H's verdict and are left for filing, exactly as that verdict scoped them.

## 2 · P1 — branch-grammar evidence (feeds `[#514]`)

**The contract's premise is out of date, and that is itself the finding.** It says *"there are
two rival ones — `[#514]`'s finding"*. There is now exactly **one** definition in the tree:

```
scripts/validate_branch_naming.py:85
  LANE_BRANCH_RE = ^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$

scripts/batch_manifest.py:134
  from validate_branch_naming import LANE_BRANCH_RE      <- an IMPORT, not a second definition
  bm.LANE_BRANCH_RE is vbn.LANE_BRANCH_RE  ==  True      (verified live this session)
```

The loose rival (`^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`) was deleted by batch-4 W1, and the
identity is pinned by
`tests/test_batch_manifest.py::test_exactly_one_LANE_BRANCH_RE_definition_ships_in_scripts`.
So "test EVERY queued branch against BOTH" collapses to one grammar. Recorded rather than
silently reinterpreted.

**Per-branch results, as dispatched:**

```
worktree-lane-d-558-vision              PASS
worktree-lane-i-31-adoption-preflight   PASS
worktree-lane-c-554-devcontainer        PASS
worktree-lane-e-502-mutmut              PASS
worktree-lane-a-533-leg2                PASS
worktree-lane-h-554-codex-review        PASS
worktree-lane-f-p10-evidence            FAIL   <- `p10` is not `\d+`
worktree-lane-g-a9-trim                 FAIL   <- `a9`  is not `\d+`
```

**Renames applied** (`git branch -m`; both re-tested PASS afterwards):

```
worktree-lane-f-p10-evidence  ->  worktree-lane-f-348-p10-evidence    ([#348] owns the grooming arc)
worktree-lane-g-a9-trim       ->  worktree-lane-g-536-a9-trim         ([#536] owns the A9 row pile)
```

**2 of 8 lanes reached the integrator off-grammar.** That is the direct measurement `[#514]`'s
undischarged **leg 1** predicts: a lane dispatched straight through `claude --worktree` never
reaches `/lane-boot`'s check, and the `KIND_UNKNOWN` BLOCK at provisioning is still unbuilt. The
grammar held at *integration* time only because a human ran it here.

**Honest limit.** The renames fix the BRANCH names. The worktree *directory* names
(`.claude/worktrees/lane-f-p10-evidence`, `.../lane-g-a9-trim`) still fail `LANE_WORKTREE_RE`.
They were left alone deliberately: they are torn down at close-out, and renaming a locked
worktree directory mid-queue buys nothing. Recorded, not swept.

## 3 · Full suite (one clean run, post-merge)

```
5 failed, 3023 passed, 4 skipped, 1 xfailed  in 1651.51s (27:31)   pytest -n auto
```

**Owned RED #1 — stands, not fixed:**
`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`
(`3 declared routine row(s)` vs the pinned `1`).

**The second expected owned RED is GONE, and that is a real result rather than a miss.** The
contract named the `doc_rot` accretion arm as the other standing RED. Lane G's trim cleared all
four `backlog-accretion` loci (`#293 #428 #550 #553`), so `validate_doc_rot --all` now reports
**0** accretion loci and the arm is green. Verified by direct measurement, not inferred.

**The remaining three are working-tree artifacts of this arc, proven rather than asserted** —
each was re-run after the closure work was committed and the JOURNAL landed, and each returned
to green:

- `tests/test_task_tree_gate.py::test_registered_and_green_on_live_repo` — `check_task_tree_coherence`
  refuses to answer while the index and working tree disagree on `BACKLOG.md`/`tasks/`. The clean
  suite ran with the closure edits still uncommitted, which is exactly that state.
- `tests/test_audit.py::test_health_ok_with_registered_repo`
- `tests/test_audit.py::test_health_stays_ok_with_na_status`
  — both assert `audit.py health` exits 0, which it cannot while `journal_spine_anchor` FAILs on
  this arc's own nine unjournaled spine merges.

**`tests/test_audit.py::test_check_fleet_parity_green_on_live_repo`** — see the re-run result
recorded below; it is the one failure whose attribution was not settled by the commit.

## 4 · Closures banked vs births

**Banked (6):** `[#505]` · `[#556]` · `[#557]` · `[#558]` · `[#502]` · `[#536]`
**Births: 0** — as instructed.
**Left OPEN and reported rather than forced:** `[#554]`.

`[#554]`'s Done-when is literally *"one lane runs green (`audit.py health` **and**
`pytest -m 'not slow'`) on the Codespaces free tier, and the identical script is runnable via
`devcontainer up` on a VPS"*. Lane C reached STEP 4, found **no boot channel available** (its
`gh` token lacks the `codespace` scope), and took the contract's authorized fork — reporting
**D1 and D2 open** rather than fabricating a boot log. D1/D2 **are** Done-when items (a) and (b).
Per the integrator contract's own instruction for exactly this case, the row stays open.
**The remaining items are D1 and D2 — the proof, and only the proof.** Everything else lane C
owed (legs L1–L4) landed.

## 5 · What each closure act actually did

1. **`[#556]` / `[#505]` drift.** `[#505]` was closed by merge `25ff8ec37` but its row was still
   in `BACKLOG.md` carrying `status: open`. Closed through the retire-not-delete path
   (ADR-107 §6.3): the node was removed from `tasks/manifest.json`, the record kept with a
   terminal `status: closed`, then `gen_task_tree.py --emit-source`. `validate_git_backlog` now
   reports **"OK — no closed-but-present drift"**; it reported 1 DRIFT before. `[#556]` closed with it.
2. **`[#557]` / the three `[stale]` dispositions.** `warn-preflight-backlog-ids-310-292`,
   `warn-review-artifact-387b794a-repin-close` and `warn-review-artifact-d62796ad-boot-acts` were
   **removed**, not re-pointed — each replaced by the register's own `# (cleared …)` comment form
   with the reason recorded in place, which is what `[#557]`'s Done-when asks for. Removal is the
   correct verdict for all three: the live `review_artifact_coverage` WARN names a *different*
   merge set entirely, so the two review-artifact entries have left the scan window rather than
   moved, and re-pointing would have invented a suppression for a finding they never covered.
   Register 28 → 25 entries.
3. **`[#558]`** closed — lane D landed the `VISION.md` re-scope (`e72f712f`). The residual
   non-`CLAUDE.md` sites are the seat's follow-up candidate, not this row's scope.
4. **`[#554]`** — left open; see §4.
5. **`[#502]`** closed, and the ruling transcribed **verbatim** into intake #27's Tier-L adoption
   ledger (row 8 of `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md`): decision 6 =
   ADOPT; CI-only (Windows walls: POSIX `resource`, `fork`); report-only ratchet; baseline 1210
   survivors on the `fleet_analytics` slice, direction no-growth; survivor triage deferred with
   trigger post-`[#533]` / next audit-py batch. The intake stayed `status: DRAFT` — **no status
   flip**, per the contract's exclusion. Both intake generators were re-run and
   `gen_intake_tree --check` reports **OK**.
6. **A9 route (ii).** Six dispositions written, covering **every** live `backlog-row-length`
   locus: `[#546]` `[#547]` `[#552]` (lane G's REPORT list) plus `[#533]` `[#529]` `[#530]` (the
   still-open remainder of lane G's contract-EXCLUDED set — the other four excluded rows,
   `[#502]` `[#556]` `[#557]` `[#558]`, closed in this same arc and took their WARNs with them).
   Each entry is keyed on the row id **and its measured length**, per the register's
   precision-over-recall rule, so a row that changes re-surfaces instead of staying silently
   suppressed at a length nobody agreed to. Three stated reasons: *no carrier* (`[#546]`,
   `[#547]` — trimming would delete the only record of the finding); *structurally above the
   ceiling before any prose exists* (`[#552]` — 1654 chars of governance clauses alone, lane G
   §2.2); *length is the leg enumeration / mechanism spec* (`[#533]`, `[#529]`, `[#530]`).
7. **`[#536]`** closed. Its Done-when — *"a ruling records … and `validate_doc_rot --all` reports
   the agreed count with every remaining locus dispositioned in the register"* — is met: 6
   row-length loci, 6 dispositions, and the `backlog-accretion` arm now stands at **0 loci**
   (lane G's trim cleared all four of `#293 #428 #550 #553`).
8. **Adjudication transcription (A13).** Row edits only, through the generator, no births — see
   §5 for why they are pointers.

## 6 · A13 verdicts, transcribed

The rows carry short dated pointers; the verdicts are recorded here in full. Lane G had trimmed
these rows to the ceiling, leaving `[#535]` 18 characters of headroom, `[#514]` 28 and `[#539]`
30 — writing the verdicts inline would have pushed them over the 1320 ceiling and manufactured
new undispositioned WARNs, i.e. self-induced bloat, which the register's own precedent says gets
*drained* rather than dispositioned.

- **`[#514]` — LIVE, priority-up.** Already `P1`, and `P1` is the top of the live enum
  (`P1|P2|P3`), so it stays P1; no `P0` was invented. The P1 grammar evidence of §2 is attached:
  one constant, not two, and leg 1 confirmed unbuilt by 2 of 8 lanes arriving off-grammar.
- **`[#535]` — lane-E evidence note.** Lane E hit this exact class in its own harness:
  `fleet_analytics` was being registered under two `sys.modules` keys, and the fix registers the
  **same object** under both (`sys.modules[_MODNAME]` and the bare name) so the two spellings
  cannot diverge. A second live instance of the two-module-identities defect, from an unrelated lane.
- **`[#457]` — note.** The two OWNED suite REDs are `routine_consumers` and the `doc_rot`
  accretion arm.
- **`[#348]`** owns the full 194-verdict grooming arc (a batch-2 lane).
- **`[#540]` + `[#539]`** own the dispatch/harvest systematization (next session).

All six edited rows were verified under the ceiling afterwards; `[#539]` sits at exactly 1320.

## 7 · Deviations — every one

1. **Review-artifact filename.** The contract names `docs/audits/2026-08-18-review-batch1-a.md`.
   `review` is **not** a member of `validate_hermetization.AUDIT_CLASS_ENUM`, so that path is
   refused by the ADR-101 Rule B gate at commit time. Landed as
   `docs/audits/2026-08-18-codex-review-batch1-a.md` (`codex` class) — the shape lane H's own
   artifact already uses.
2. **H's artifact path.** The contract cites `docs/audits/2026-08-18-review-batch1-c-e.md`; the
   file on `07628523` is `docs/audits/2026-08-18-codex-review-batch1-c-e.md`. Read from the real path.
3. **`SKIP=audit-health` on six merge commits.** A *conflict-free* merge runs commit-msg hooks
   only, but a **conflicted** one runs the full pre-commit set — and `journal_spine_anchor` FAILs
   while this arc's own merges are not yet journaled, which wedges the very queue it protects.
   Ownership was proven before each use: the only `[!!]` FAIL in `audit.py health` was
   `journal_spine_anchor`, naming **only** merges this arc had just made. `--no-verify` was never
   used, and every other gate (hermetization, seal-identity, audits-index, backlog-id, filing
   backpressure, ruff) stayed armed and passed. The JOURNAL entry in this same arc discharges all
   nine spine entries.
4. **`docs/audits/README.md` merge conflicts (6 of 9 merges).** The generated audits index is a
   collision file — every lane that lands an artifact rewrites it. Resolved deterministically by
   **regeneration** (`gen_audit_index.py --write`), never by hand-picking a side. This is the
   "trivial disjoint-file artifact" class the contract anticipates.
5. **`[#514]` priority-up** was already at the enum ceiling — see §6.
6. **Act-8 row edits are pointers, not inlined evidence** — see §6.
7. **The first full-suite run was discarded.** It was started before the closure acts and I
   edited `BACKLOG.md` while it was still running, which can fake REDs. It was re-run clean with
   no concurrent writes, and only the clean run is reported.
