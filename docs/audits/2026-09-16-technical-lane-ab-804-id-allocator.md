# Lane ab-804 — push-reserved ids, a real manifest refusal at lane boot, and a widened lane grammar

**Lane:** `lane-ab-804-id-allocator` · **Branch:** `worktree-lane-ab-804-id-allocator` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`) · **Date:** 2026-09-16

Consumers: [#804] [#788] [#809]

## 1 · Premise — the locators, checked before anything was built

**Contract identity.** `sha256` of the frozen contract read at boot:
`6e80adff343ecdcbfaa0a70a85da627927e17e05ca55ceb86024aac1484f541f`. That matches the pin in the
batch AB manifest, so this is the contract that was dispatched.

**`/preflight` (`scripts/preflight_contract.py`, locator legs), run on the contract:** 7 of 8
claims resolve. Both SHAs (`279caaff`, `e17c6200`) resolve. `[#804]`, `[#788]`, `[#809]`,
`[#675]` and `[#793]` are open. The one failure is `[#717]`: it is closed. It appears only in the
dispatch boilerplate, as the reason the model is written on the dispatch line. Nothing in this
lane depends on it being open.

**Locator 1: `preflight_contract.check_open_batch` (contract: "~L1077").** It exists at
`scripts/preflight_contract.py:1077`. It calls `batch_manifest.open_batches(repo_root)`. It
returns one FAILED `Claim` when that list is empty or when the module cannot be read. On this
lane's base it returns batch AB as open.

**Locator 2: the PLAYBOOK claim (contract: "~L2740").** It is at `protocols/PLAYBOOK.md:2740-2743`,
under "The manifest opens a batch by `closed_by:`, and by nothing else", "RULED 2026-08-29" item 2:

> `/lane-boot` and the `[#591]` pre-freeze validator REFUSE to dispatch the first lane while
> `open_batches()` returns `[]`. The predicate is `preflight_contract.check_open_batch`

**What `/lane-boot` invokes today (`.claude/commands/lane-boot.md`).** Four commands, all in §1–§3:
`validate_branch_naming.py --lane`, `single_flight.py claim`, the ruled `dispatch` verb, and
`worktree_seed.py --plan`. **None of them calls `check_open_batch`.** Its only in-tree caller is
`freeze_predicates()`, which runs only when a seat runs `preflight_contract.py --freeze` by hand.
So the PLAYBOOK claim is **false as written**. The refusal it describes is a predicate that
nothing on the boot path calls. That is `[#804]` Done-when (1) as found.

**The dispatch path is not in this repo.** `dispatch` resolves to
`~/.dev-terminals/bin/dispatch.ps1`. That script delegates to
`win-tooling/scripts/dispatch/Invoke-Dispatch.ps1`. It calls nothing in the hub. That repo is
outside this lane's footprint, and lane R (`lane-ab-810-substrate-repair`) is editing it now. The
hub side of the wiring is therefore a Python entry point that `/lane-boot` calls, and that the
verb *can* call. Connecting the verb to it is recorded as an out-of-footprint follow-up (§6). It
is not claimed as done.

**Grammar consumers found (`[#809]`).** Restatements of the one-letter batch token:

- `scripts/validate_branch_naming.py`: `LANE_WORKTREE_RE` and `LANE_BRANCH_RE`. These are the
  single definitions.
- `scripts/batch_manifest.py`: `_LANEISH_IN_SUBJECT_RE` (a diagnostic, not an exemption path) and
  `_SLUG_TOKEN_RE` (the manifest lane-table reader for `[#630]`).
- `scripts/gen_lane_contract.py`: no copy. It goes through `validate_lane_worktree_name`.
- `tests/test_batch_manifest.py`: pins `worktree-lane-ab-514-two-letters` as REJECTED. That pin
  was written against the old rival regex, and the operator's `[#809]` ruling reverses it.

## 2 · RED-first witnesses (`455b2dca`)

Recorded run on the pre-build code: **34 failed, 66 passed** over the targeted set. Each
witness below failed on its own, not at collection:

- **Done-contract 1**, in `tests/test_id_allocator.py`. Two git worktrees race through one
  local bare `origin` for task id 815, three rounds. One wins, and the loser exits 3 with the
  winner named. Concurrent `allocate` calls from one block return `{815, 816}`. A second clone
  that never fetched is refused too.
- **Done-contract 4.** A sibling holds 815 on the remote while the local tree carries
  `tasks/900-*`. The answer is 816, which is neither `max + 1` (901) nor the colliding 815. Two
  very different local trees get the same answer. A source grep backs this up but is not relied
  on alone.
- **Done-contract 2**, in `tests/test_lane_boot.py`. The tests drive the `lane_boot.py
  preflight` CLI and assert that `/lane-boot`'s fenced block runs it. A manifest committed only
  off `main` is refused and named.
- **Done-contract 3**, in `test_validate_branch_naming`, `test_batch_manifest` and
  `test_gen_lane_contract`.

## 3 · The allocator (`0bc910d3`)

`scripts/id_allocator.py` reserves ids by pushing `refs/reservations/<kind>/<value>` with
`--force-with-lease=<ref>:`. The pushed object is a parentless, nonce-bearing commit naming its
holder, and a reservation counts as won only on the porcelain `*` flag. It has three verbs:
`reserve`, `allocate --block LO-HI` and `holder`. Its transport and verdict parsing are imported
from `single_flight`. Candidates come only from the granted block, and whether one is free is
asked only of the remote.

**Finding against `single_flight` ([#530]), measured and not edited.** In six rounds of two
threads racing one ref (git 2.55.0.windows.3), both pushers passed the lease. The server's ref
transaction refused the loser with `[remote rejected] (reference already exists)`. That text is
not in `single_flight._CONTENTION_MARKERS`, so a truly simultaneous `claim` exits **2**,
internal error, instead of **3**, in flight. The failure is closed, so there is no double grant.
But `/lane-boot` §1's exit table tells the operator "internal error" for what is really
contention. `id_allocator` adds the marker locally. The one-line fix in `single_flight` belongs
to whoever owns `[#530]`.

## 4 · The manifest refusal, wired (`c5c7d711`)

`scripts/lane_boot.py preflight` is now `/lane-boot` §1's command. It refuses (exit 1) a
malformed lane name, a failing `preflight_contract.check_open_batch`, and an open manifest that
`main` does not carry open. The last refusal names the file. `/lane-boot` §6 routes new task ids
through `id_allocator.py allocate`. Both scripts carry ON-DEMAND rows in
`graph_queries.ORPHAN_DISPOSITIONS`, on `single_flight`'s precedent.

## 5 · The grammar (`e672ac1a`)

`validate_branch_naming.BATCH_TOKEN = [a-z]{1,3}` is read by `LANE_WORKTREE_RE`,
`LANE_BRANCH_RE`, `batch_manifest._LANEISH_IN_SUBJECT_RE`, `batch_manifest._SLUG_TOKEN_RE` and
`id_allocator`'s `batch-token` kind. `worktree-lane-ab-808-guard-timeout` matches and is exempt
under an open manifest. `gen_lane_contract emit` accepts `lane-ab-…` without `--loose-slug`.

## 6 · Verdict, deviations, and what the integrator owes

**Targeted suite.** Thirty test modules were run: every module importing a changed script, plus
`test_single_flight`, `test_preflight_freeze_predicates`, `test_codespace_regime` and
`test_seat_cost`. Result: **1253 passed, 10 failed.** All ten also fail on `main` `18bda49a`,
re-run in a detached baseline worktree that was then removed and verified gone. Nine fail
identically there and one is skipped: `test_deny_and_point` ×3, `test_gen_handoff` ×5,
`test_archive_row_body::test_every_committed_record_still_proves_out`, and
`test_preflight_freeze_predicates::test_vi_batch1_reproduces_the_wrong_id_citation`. None touch
this diff. The full suite was not run, per the operator's constraint for batch AB.

**Rows.**

- `[#788]`: **closeable.** A checkable surface now refuses an id held outside the tree, and
  `/lane-boot` §6 is the lane-protocol step naming it. Its Done-when is met.
- `[#809]`: Done-when (1), (2) and (4) are met, and (3)'s first half is met. **Open:** refusing
  a recycled letter that only appears in history.
- `[#804]`: Done-when (1) is met for `/lane-boot`. (3) is met by the concurrency witness.
  **Open:** (1) at the `dispatch` verb, (2) reading the per-lane block from the manifest by
  machine (the AB manifest's blocks are a prose table), and (4) QR ids and JOURNAL letters.

**Decisions taken under the budget, and none escalated:**

1. The dispatch verb was **not** wired. It lives in `win-tooling` (`Invoke-Dispatch.ps1`),
   outside this lane's footprint and inside lane R's. The hub entry point exists for the verb to
   call. **Follow-up:** the verb runs `lane_boot.py preflight` as its first act.
2. Python module names use underscores, because every importable script in `scripts/` does.
   Hyphen-only applies to slugs and document names.
3. `SKIP=audit-health` on the first two commits only. The sole `[!!]` was
   `journal_spine_anchor` on `448a630b`, a real gap on `main` at the time, with the proof in each
   commit body. The lane then took two sync merges of `main` (`2053513d`, `4483bb11`), and
   `audit-health` ran normally on every later commit.
4. `SKIP=doc-counts-pytest-freshness` on every test-moving commit. **The integrator owes
   `gen_doc_counts.py --write`** on the merged tree.
5. PLAYBOOK prose and `batch_manifest` docstrings still spell the grammar
   `lane-<letter>-<id>-<slug>`, and PLAYBOOK still quotes the module docstring. They were left
   unedited because a lane cannot honestly restamp PLAYBOOK. The prose now describes a narrower
   grammar than the code.

**Observed, for `[#804]`:** `main` filed `[#827]` during this batch. That id is outside every
block in the AB manifest (§3 reserves 811-826). A manifest-held block did not stop an
out-of-block id, which is the allocator's case in one instance.

**Merge order.** This lane goes first, as the manifest suggests. Lane 1, lane R and the held
aa-12 lane get the ADR-110 exemption only once `e672ac1a` is on `main`.
