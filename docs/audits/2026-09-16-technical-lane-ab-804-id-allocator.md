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
