---
batch: H0-PREP
seq: 1
shape: DISPATCHER-CUT — four lanes ruled, one (L2) RETIRED before dispatch on evidence; 3 committing lanes, all codespace, dispatched in parallel against a 2-running account cap.
dispatched: 2026-09-05
status: open
closed_by: docs/audits/2026-09-05-technical-batch-h0-close-packet.md
substrate: CODESPACE (3) — Dispatch-Codespace, PLAYBOOK.md Ch8 row 4, quoted at dispatch
---

# BATCH H0-PREP — THE ADMISSION GATE THAT WAS ALREADY FIXED, AND THE THREE LANES BEHIND IT · THE MANIFEST

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves an open batch as
the conjunction of four facts: the manifest is TRACKED, `status: open`, `closed_by:` names a shape
that CAN resolve, and that path is ABSENT from the tree. All four hold at the time of writing.

## L2 WAS RETIRED BEFORE DISPATCH, AND THAT IS THE BATCH'S MAIN FINDING

The batch was cut as four lanes. L2 (`lane-h0-admission-gate`, `[#634]` P1) was to make the
dispatch admission gate stop accepting `GITHUB_TOKEN` as its Anthropic-token check. It was
**retired by operator ruling 2026-09-05 (OPTION 2 amended)** before any machine was provisioned,
on two facts the dispatcher established first:

1. **The target is cross-repo.** `dispatch-run.sh` is not a source file in this repo at all — it is
   ignored at this repo's root (`.gitignore`), absent from disk and from history across the whole
   `Dev/` tree, and **generated per run** by
   `win-tooling/config/dispatch-helpers/DispatchHelpers.psm1`, which copies it into the container.
   The L2 contract's own escape clause ("cross-repo → STOP and report") fired.
2. **The defect was already fixed.** `win-tooling@d6cbd92` (2026-09-01 21:36, merged `49cb75e`)
   split `adm_tok_anthropic` from `adm_tok_github`, so a GitHub credential can no longer satisfy an
   Anthropic check. `[#634]` was ruled from AMENDMENT 2 of
   `docs/audits/2026-09-01-verification-codespace-longrun-proof.md`, which **pre-dates** that fix:
   the premise was stale on arrival, by four days.

The contracted closure — *"only `GITHUB_TOKEN` set → REFUSED naming the variable"* — was **not**
built, and deliberately so: it would be fail-CLOSED on a path measured working. In
`lane-632-longrun-a-w95qprj5wq4cg67g`, `CLAUDE_CODE_OAUTH_TOKEN` was UNSET and `claude auth status`
reported `loggedIn: false`, yet the dispatched session ran **338 events** authenticated over
`CLAUDE_CODE_MESSAGING_SOCKET`. Both local probes false-negative. `[#634]` was therefore re-scoped
rather than closed (branch `docs/rescope-634`), the residual being (a) a probe that can SEE the
socket path and (b) **Done-clause 0** — a dispatched lane's correctness gate is a commit on its own
branch, never the receipt. The standing hold on codespace dispatch was LIFTED in that ruling, which
is what permitted this batch to dispatch at all.

## THE LANES — 3 committing, all codespace

Contracts are per-run artifacts (`/LANE-*.md`, ignored at root) and are therefore NOT committed;
each was emitted by `scripts/gen_lane_contract.py emit --shape codespace --loose-slug` and passed
`gen_lane_contract.py check` before dispatch.

```
L5  lane-h0-suite-speed   codespace  opus  [#528]  suite must not pay for live worktrees   MERGES FIRST
L4  lane-h0-trace         codespace  opus  [#66]   dispatch trace under logs/prompts/
L3  lane-h0-readme        codespace  opus  --      README as the front door                MERGES LAST
```

**Merge order is L5 → L4 → L3**, serial, from the primary checkout. Every lane branch was created
at `origin/main` = `3200757d` and pushed before dispatch, because the container clones from
`origin` and a codespace lane can only see what is already there.

**Every lane carries Done-clause 0**, added to the frozen contracts from the operator's ruling: a
lane is done when its branch carries a commit. A receipt reports TRANSPORT — `Ok` and
`RemoteExitCode` read separately still say nothing about whether the lane committed — so the
integrator must not merge a lane on the strength of its receipt.

## `--loose-slug` IS A DECLARED DEVIATION, NOT AN OVERSIGHT

The batch-lane grammar is `lane-<letter>-<id>-<slug>` and refused all three operator-given names.
The names were kept and the grammar relaxed with `--loose-slug`, because the operator named these
lanes in the ruling and a silent rename would have made the merge queue unreadable against the
instruction that produced it. Contracts are never committed, so `lane-contract-check` — which fires
on staged files — is not bypassed by this; the branch names still satisfy `validate_branch_naming`
via the `worktree-` prefix.

## ONE CONTRACT DEFECT WAS CAUGHT BEFORE FREEZE

L5's first draft told the lane to "measure the baseline with the 2 existing worktrees". The floor of
2 is real — the operator's PRIMARY checkout carries `corpus-coherence-gemini` and
`r5-disposition-sheet`, so 0 is not a state the suite is ever actually run in — but
`.claude/worktrees/` is untracked, so a **fresh codespace clone has none**. The contract was
corrected before dispatch to PROVISION the floor of 2 rather than find it. Frozen as sent, the lane
would have STOPped on a refuted premise at step 1.

## HONEST LIMITS

- **The account caps concurrent codespaces at 2.** L5 and L4 provisioned; L3's create was refused
  `HTTP 400: You have too many codespaces running`. Nothing was provisioned for L3 and nothing was
  billed for it; it is dispatched into the first slot that frees. "Three lanes in parallel" was the
  instruction and it is **not** what physically happened — two ran, one queued.
- **This manifest was written after dispatch, not before it.** `dispatched:` carries the real date
  and this line carries the defect; a manifest written after the fact cannot pretend to have
  governed the dispatch.
- **No lane outcome is recorded here.** At the time of writing the two live lanes were
  `Provisioning`. What each lane actually did belongs in the close packet named by `closed_by:`,
  read off the branches rather than off the receipts.
