# NB2 · LANE F — CANDIDATE C-A: the [#577] byte-cap test — S

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge` (the hub)
**Branch:** `worktree-lane-f-577-byte-cap` · **Frozen by the Layer-1 architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N7.**

**Substrate:** local
**Worktree pairing:** slug `lane-f-577-byte-cap` -> branch `worktree-lane-f-577-byte-cap`


## Dispatch

```
claude --bg --model opus --effort medium --worktree lane-f-577-byte-cap --permission-mode bypassPermissions "[dev-knowledge . #577 . byte cap test] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-F-577-byte-cap.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N7 — CANDIDATE C-A: the [#577] byte-cap test — S
> Write-scope: `tests/` — one new file (reads AGENTS.md + CLAUDE.md, edits neither).
> Intent: batch-1 measured the combined global+root payload at 9,161 B = 28.0% of Codex's 32 KiB
> project_doc_max_bytes cap and reported it UNGUARDED. The figures exist; the gate does not.
> Done: (1) a test asserts the combined payload IN BYTES against the cap; (2) fails on a planted
> oversize fixture; (3) [#577]'s done-when fully discharged — said so in the packet.
> Anti-patterns: editing AGENTS.md/CLAUDE.md · asserting lines (this corpus averages ~117 B/line) ·
> regenerating doc-counts (integrator, once).

## CONTRACT DEFECT FOUND AT DISPATCH — recorded, not silently repaired (D-F1)

**The 9,161 B figure the contract's Intent restates is FALSE against the landed tree.** Measured
at dispatch, 2026-08-28 23:40 local:

| surface | measured | batch-1's claim (`CLAUDE.md` §2.68) |
|---|---|---|
| `~/.codex/AGENTS.md` (Codex global) | **3,891 B** | 3,891 B (implied) |
| repo-root `AGENTS.md` | **5,539 B**, 107 lines | "**103 lines**, **5,270 B**" |
| combined payload | **9,430 B = 28.78 %** of 32,768 | "9,161 B = 28.0 %" |

`AGENTS.md` has been 5,539 B **since birth** — `git cat-file -s 43c18e9f:AGENTS.md` == 5539, and
`43c18e9f` is its only content commit. So §2.68's line/byte figures were wrong when written, not
stale by drift. This is a **fourth** instance of the premise class lane G is being built to
refuse at freeze time, and it is reported to the integrator as such.

**What this changes for you: nothing about the deliverable, everything about the assertion.**
Your test asserts the payload **against the cap**, never against a remembered constant. Re-measure
in the test itself. Report the measured live figure in your packet; the morning packet will report
it against the ex-ante statement "byte-cap test green at 9,161 B payload" and name the delta.

**Candidate filing (do NOT file it — report it):** `CLAUDE.md` §2.68's byte/line figures are
false; correcting them is a `CLAUDE.md` write, outside your frozen scope, and `CLAUDE.md` is at
196/200 of its file budget.

## THE HARD PART: what "the payload" is, and why a naive test is machine-dependent

Codex composes `project_doc_max_bytes` from a **global** doc plus the **repo-root** doc.
The global one lives **off-repo** at `~/.codex/AGENTS.md`. A test that reads an off-repo,
per-machine file will pass here and fail (or vacuously skip) anywhere else — including in any
future CI. Decide this explicitly and **write the decision into the test's own docstring**:

- read the repo-root `AGENTS.md` from the tree, always; **and**
- for the global half, either (a) read the in-repo `codex/AGENTS.md` — measured at dispatch as
  **3,891 B, byte-identical in length to `~/.codex/AGENTS.md`** — as the tracked stand-in, or
  (b) read the real off-repo file when present and fall back to (a) when absent, or (c) assert
  only the repo-root half against a repo-root budget derived from the cap.

(a) or (b) keep the assertion honest about what Codex actually reads; (c) is weaker but fully
hermetic. **Whichever you choose, state the trade in the docstring and in the packet** — the
anti-pattern this repo keeps re-learning is a gate that looks armed and measures the wrong thing.
Verify the byte-identity claim yourself before relying on it; do not take this contract's word.

## THE PLANTED-OVERSIZE HALF (done-item 2) — RED first

A gate that never fired is not proven. Build the oversize fixture as a **fixture**, not by
touching the real files: parametrise the size-source so the test can be pointed at a `tmp_path`
pair, prove it FAILS at cap+1, and prove it PASSES at the live figures. Two tests, one helper.
`xdist` is on by default here — if a monkeypatch of a stdlib module through an alias kills a
worker, run that one test with `-n 0` and say so.

## DONE-ITEM 3: "[#577]'s done-when fully discharged"

Open `tasks/577-adopt-agents-md-as-the-portable-instruction-layer.md` and answer its done-when
**clause by clause** in the packet, MET / NOT-MET / PARTIAL with a witness each. The row is still
**open** on `main` as of dispatch (so is `[#584]`) even though batch-1 landed the work; whether
either closes is `/review-closures`' call, not yours. Report the closure candidacy; do not file it.

---

## BOOT (mechanical — do this before touching a file)

You were launched by `dispatch` into your own worktree. `/lane-boot` steps 1–2 are already
done for you (name validated, single-flight claimed, worktree provisioned). Run steps 3–7:

```
Get-Location                                              # confirm you are in the worktree
uv run --locked python scripts/worktree_seed.py --plan .  # prints the seed plan; RUN what it prints
```

Seeding matters: without `ecosystem/*/state.yaml` copied from the primary, `audit-health`
reports `repos registered (none)` -> `health: DEGRADED` and **every commit is blocked**.
Then `uv sync --locked` (the hub's environment) and, once, the import proof:
`uv run --locked python scripts/worktree_import_proof.py --repo .`  (the hub answers
NOT-APPLICABLE / exit 3 — that is expected and is not a PASS).

Every test invocation is `uv run --locked pytest …`. A bare `pytest` inherits `VIRTUAL_ENV`
from the primary tree and reports green about the primary's source (STANDING_RULINGS D4).

## SHARED CLAUSES — every local lane of night-batch-2 (frozen, verbatim)

> A5: generated surfaces (BACKLOG.md, doc-counts.md, doc-code-edge.yaml, indices, ALL_CHECKS
> registrations) resolved by REGENERATION at integration, ONCE on the merged result. N4 is the
> batch's EXCLUSIVE tasks/ writer; every other lane REPORTS candidate filings for the integrator.
> RATCHET: only N3 may move 443; every other lane's protocols/+templates/ delta must be 0,
> verified pre-commit. Decision budget: standing rulings silently; ask only curated-baseline /
> rule-vs-ruling / no-ruling fork / out-of-scope path (P1); everything else per defaults, ONE
> lane packet: per-item MET/NOT-MET, commits, terra tally, candidate filings, budget decisions.

**Ratchet verification is mechanical, not a promise.** Unless you are lane C, run
`uv run --locked python scripts/silent_rule_detector.py` before your first commit and again
before your last. The dispatch-time measurement is **count: 443, files: 61, detector
silent-rule-v5**. A non-zero delta from a lane other than C is a STOP-and-report, not a
baseline bump.

## THE FOUR THINGS THIS LANE DOES NOT DO

1. **No JOURNAL.md entry.** A batch lane never journals — the integrator writes one anchor for
   the whole queue after every lane has STOPped. The session-end Stop hook will demand a JOURNAL
   entry naming your SHAs: **decline it explicitly and say why** (ADR-85 amendment 2026-08-03
   §A5 made that hook advisory in full; the hard leg is `block-unanchored-push` at pre-push, and
   a lane does not push). Do not silently ignore it and do not "fix" it.
2. **No self-merge, and no suggesting one.** Commit-and-STOP. Your branch enters an integrator
   queue whose order is frozen; naming a merge command invites it to happen out of order.
   A hand-back packet ends at `branch + SHAs + gate state + findings`.
3. **No row closures and no `tasks/` writes** (lane D is the batch's exclusive `tasks/` writer).
   Findings are **REPORTED as candidate filings**, never filed. `/review-closures` owns closure.
4. **No generated-surface regeneration** — `BACKLOG.md`, `docs/audits/README.md`,
   `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, `.claude/generated/*`. The integrator
   regenerates ONCE on the merged result. If a pre-commit gate forces one to keep your own commit
   legal, do it, keep it in its own commit, and **name that commit in your packet**.

## TESTS

Targeted only — the files covering your own diff ([#528]; PLAYBOOK Ch5). The **full suite runs
once, at integration**, and takes ~9–13 min here. Known pre-existing REDs that are **not yours**:
the anchor-gate probe test has been RED on main since 2026-08-22 (`tmp_path` fixture), and a lane
worktree structurally REDs `test_stale_worktrees`. Report a RED you did not cause as inherited,
with the evidence that it is inherited; do not "fix" it inside this lane.

## REVIEWER

Terra pre-merge is required on every LOCAL lane, **tally-in-body**. Run
`codex exec` over your own diff (NOT `/codex-review` — a mixed doc/code diff kills that lane) and
put the tally in your packet. If codex is unreachable, say so in one line with the error and move
on; an unreachable reviewer is a recorded deviation, not a lane failure.

## YOUR PACKET (the last thing you write, in-tree)

Land it at `docs/audits/2026-08-28-technical-nb2-<lane-letter>-packet.md` — never at the repo
root (`validate-hermetization` Rule A refuses a new top-level file class). It carries, in this
order: (1) per-done-item **MET / NOT-MET / PARTIAL** against the contract above, each with a
witness (command output or `file:line`); (2) the commit SHAs on this branch, in order;
(3) the terra tally; (4) candidate filings for the integrator (never filed here); (5) every
decision taken under the budget; (6) deviations, each with an owner. A claim with no witness
is not a claim — this batch's whole point is that the packet is checkable.

Then **STOP**.
