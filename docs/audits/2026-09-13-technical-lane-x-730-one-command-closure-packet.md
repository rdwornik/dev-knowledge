# LANE `lane-x-730-one-command-closure` — end-of-lane packet

> **One-command row closure.** `close_row <id> --evidence <sha>` performs the three coupled
> edits atomically; closed-iff-absent-from-the-manifest is armed as a commit-tier check
> carrying a RED-first trip-test; a first run emits the closure list to the operator's
> transport.
>
> Contract: `H:\My Drive\CLAUDE PROMPT DIR\LANE-x-730-one-command-closure.md`.
> Row: `[#730]` (this lane is a narrower, single-lane instance of its larger
> evidenced-bulk-closure vision — AX16-2 and AX27-5 are the two clauses this lane discharges).
> Branch: `worktree-lane-x-730-one-command-closure`. Commit-and-STOP; no merge, no push to
> `main`.

## 1. What changed

Four commits, RED-first, one per contract step:

| # | Commit | Step | Surface |
|---|---|---|---|
| 1 | `99a6c1a0` | 1 · RED-first | `tests/test_gen_task_tree.py` (8 new tests, all failing against no implementation) |
| 2 | `132b273b` | 2 · `close_row` | `scripts/gen_task_tree.py` (`close_row_plan`, `_cmd_close_row`, `--close-row`/`--evidence` CLI, `status_override` derivation exception) |
| 3 | `6907c9ea` | 3 · commit-tier invariant | `scripts/gen_task_tree.py` (`_scan_source`'s `identity` list gains the terminal-status-while-referenced refusal, wired at `TIER_COMMIT` via the existing `check_task_tree_coherence` registration — zero new wiring) |
| 4 | `8211e0cf` | 4 · witness scan | `scripts/propose_row_closures.py` (new), `tests/test_propose_row_closures.py` (new, 10 tests), `scripts/graph_queries.py` (`ORPHAN_DISPOSITIONS` +1 entry) |

Between steps, three sync-merges (`dc0a4e53`, `fb4abfb2`, `26ed479d`) absorbed a fast-moving
`main` — see *Findings* 4.

## 2. The live state — what the mechanism says today

**`close_row`, the three coupled edits, verified on a throwaway fixture** (never run against
this repo's real `tasks/` — see §4's *Closure is proposed, never performed* clause):

```
$ pytest tests/test_gen_task_tree.py -k close_row -q
10 passed
```

covering: the three-edit atomicity, malformed-evidence refusal, id-not-open refusal,
double-close refusal, `--evidence`/`--close-row` CLI pairing, a torn-write rollback (both
files byte-identical to before on a simulated mid-write `OSError`), and survival of a
subsequent `--emit-source` frontmatter refresh.

**The commit-tier invariant, live:**

```
$ uv run --locked python scripts/gen_task_tree.py --check
```

refuses (identity-tier, blocking `--emit-source`) any manifest-referenced task file carrying
`status: closed|retired|superseded` — the closed-iff-absent direction ADR-107 §6.3 had not
previously enforced.

**The witness scan, run for real against this repo:**

```
$ uv run --locked python scripts/propose_row_closures.py
propose_row_closures: 0 row(s) witnessed against `main` -> H:\My Drive\CLAUDE PROMPT DIR\to-browser\CLOSURE-LIST-2026-09-13.md
```

Zero rows witnessed is the honest-empty case, not a false negative: no row this branch shows
open has yet been removed from `main`'s `BACKLOG.md` history since the merge-base — expected,
since this lane's own manifest is unchanged from `main`'s.

## 3. Open items

### Proposed diffs — named, not made

1. **Whether a command file should invoke `scripts/propose_row_closures.py`** is a successor
   decision. `ORPHAN_DISPOSITIONS` carries it as arrived-after-the-census, same class as
   `gen_ledger.py` (§4 finding 3) — not resolved here, because this lane's declared footprint
   is `scripts/` and `tests/`, and a new command file or wiring-surface decision is out of it.
2. **Relocating `ORPHAN_DISPOSITIONS` to `ecosystem/disposition-register.yaml`** — an owed
   follow-up the register's own module docstring already names (predates this lane); this
   lane's one added row inherits that debt rather than creating it.
3. **`[#730]`'s larger evidenced-bulk-closure vision stays open.** This lane discharges AX16-2
   (the atomic three-edit closure primitive and its commit-tier invariant) and a single-lane,
   mechanical instance of AX27-5 (a witness scan comparing this branch against one
   `compare_ref`). The full vision — a per-BATCH close packet citing which gate or test proved
   each Done-when — is not attempted; `propose_row_closures.py`'s own docstring and rendered
   output both say so explicitly rather than overclaiming.

## 4. Findings and deviations

1. **The output path is the operator transport, not this git tree — caught by the gate
   built to catch exactly this.** The first implementation of step 4 wrote to
   `<repo_root>/to-browser/CLOSURE-LIST-2026-09-13.md`. `validate-hermetization` correctly
   refused it as an unsanctioned new top-level directory (ADR-101). The refusal was right; the
   target was wrong. `scripts/gen_ledger.py` and `scripts/gen_handoff.py` already resolve
   `to-browser/` under `gen_handoff.transport_root()` (`CLAUDE_PROMPTS_DIR`, falling back to
   `~/Downloads`) — outside the repo by design. `propose_row_closures.py` now reuses that same
   resolution (library-first) instead of inventing a second convention. No ADR-101 amendment
   was needed or sought.

2. **`ORPHAN_DISPOSITIONS` gained one entry, decided per contract default rather than
   escalated.** Adding a disposition row for a newly-landed, on-demand-by-CLI report generator
   is this register's own routine extension path (its docstring invites it), not a
   curated-baseline act in the V-2 escalation sense — confirmed against precedent: prior
   lanes (`[#675]`, `[#691]`) added and removed rows in their own feature commits without
   escalating. The row mirrors `scripts/gen_ledger.py`'s own class (arrived-after-the-census,
   operator-transport generator, on-demand-by-CLI).

3. **A pre-existing, cross-lane test failure, reported not absorbed.**
   `tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
   fails on `scripts/worktree_seed.py` both before and after this lane's `ORPHAN_DISPOSITIONS`
   edit (verified by stashing the edit and re-running the test in isolation). Same root cause
   `lane-x-691`'s own packet already recorded (finding 3 there): the register's disposition
   row for `worktree_seed.py` predates `[#716]` wiring it as a live trigger, and the row has
   not yet been deleted. Not fixed here — it belongs to `[#664]`'s arc, per the register's own
   convention ("drops off this list by being wired rather than by being dispositioned").

4. **Three sync-merges were needed mid-lane against an actively-landing `main`.** Between
   steps 3 and 4, and again while finishing step 4, `local main` advanced repeatedly (multiple
   concurrent lanes' `--no-ff` merges landing in quick succession, each briefly leaving its own
   merge-tip unanchored in `JOURNAL.md` until a follow-up anchor commit landed — the documented
   `journal_spine_anchor` tree-lag/chase-pattern). Each occurrence was diagnosed with the
   hook's own prescribed discriminator (`journal_anchor.introduced` / `is_anchored` against
   this tree vs. `main`) before acting: two resolved as tree-lag (fixed by `git merge main`),
   one resolved on its own once the concurrent seat pushed its anchor commit while this lane
   was mid-retry. No JOURNAL entry was written by this lane (P-1); `--no-verify` was not used
   at any point.

5. **Pre-existing, out-of-footprint test failures, neither touched:**
   - `tests/test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar`
     (asserts `BACKLOG.md < 72_000` bytes; measured 89,338+ — repo-wide drift from other
     lanes' filing activity, confirmed via `git status` to be untouched by this lane's diff).
   - The graph-spine disposition test in finding 3 above.

6. **No index regeneration performed** (BACKLOG.md, `ecosystem/organ-index.md`, audits index)
   beyond `ecosystem/doc-counts.md`, which the `doc-counts-pytest-freshness` commit-tier gate
   requires on every commit that moves the collected-test count — regenerated via
   `uv run --locked python scripts/gen_doc_counts.py --write` before each commit, per that
   gate's own instruction rather than a lane-scope exception.

## 5. Verification

- **Targeted: 117 passed, 1 deselected** (the pre-existing byte-bar failure, finding 5) across
  `tests/test_gen_task_tree.py` and `tests/test_propose_row_closures.py` — this lane's full
  diff footprint (`scripts/gen_task_tree.py`, `scripts/graph_queries.py`,
  `scripts/propose_row_closures.py`).
- **RED-first on every code step:** step 1 landed 8 failing tests against no implementation;
  step 2 turned them green; step 3 added a 9th (`test_check_reds_when_a_referenced_task_file_carries_a_terminal_status`)
  RED-first against the un-armed check, then green once the `identity` refusal landed; step 4
  landed 9 new tests for `propose_row_closures.py` against no module, then green (10 total —
  the CLI import test came free with `pytest.main`'s collection).
- `ruff check` clean on every file this lane touched (`scripts/gen_task_tree.py`,
  `scripts/graph_queries.py`, `scripts/propose_row_closures.py`,
  `tests/test_gen_task_tree.py`, `tests/test_propose_row_closures.py`).
- **Full suite not run** — the contract's own default (Q1/[#528]): the full suite runs once,
  at integration, not per lane. This lane's targeted set is its full declared footprint, so no
  additional module was in scope to widen it against.
</content>
