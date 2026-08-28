# NB2 · LANE E — [#605] de-hardcode consumer-root resolution — M

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge` (the hub)
**Branch:** `worktree-lane-e-605-consumer-root` · **Frozen by the Layer-1 architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N6.**

**Substrate:** local
**Worktree pairing:** slug `lane-e-605-consumer-root` -> branch `worktree-lane-e-605-consumer-root`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-e-605-consumer-root --permission-mode bypassPermissions "[dev-knowledge . #605 . consumer root] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-E-605-consumer-root.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N6 — [#605] de-hardcode consumer-root resolution — M
> Write-scope: `deploy/tool.py` · `scripts/audit.py` · one new test file.
> Intent: the hub stops assuming every consumer is a filesystem sibling under Dev/ — the premise
> any off-laptop substrate needs.
> Done: (1) consumer-root resolution EXPLICIT in both modules with the sibling default as
> fallback; (2) a non-sibling layout resolves in both, PROVEN BY A TEST; (3) `audit repo <name>`
> runs from a checkout with no sibling tree; (4) deploy/tool.py's docstring tells the truth.
> MERGE ORDER: after N1 (D4). Anti-patterns: changing preflight refusal semantics · touching
> manifest files · widening into the profile-ruling read (separate row).

## WHAT THE MERGE ORDER MEANS FOR YOU

Nothing you must do — it is the integrator's constraint. **D4** puts lane A (the architect's N1,
the win-tooling deploy lane) ahead of you in the hub queue because lane A *exercises* the tool
you rewire: your files and lane A's are disjoint, the **behaviour** is not. Do not coordinate
with lane A, do not read its branch, do not wait for it. Write the seam so that a caller passing
nothing behaves exactly as today.

## THE TRAP THIS LANE EXISTS INSIDE — `audit.py` is the pre-commit gate

`scripts/audit.py` is not an ordinary module here: `audit-health` runs `audit.py health` as a
**pre-commit hook**, so a regression in it blocks **every commit in every lane**, including your
own commit of the fix. Two consequences, both mechanical:

- **Run `uv run --locked python scripts/audit.py health` before each commit**, and read the
  FAIL/WARN split. A FAIL blocks; a WARN informs.
- `ALL_CHECKS` count pins live in **six** places. If your change adds or renames a check (it
  should not — this row is a resolution seam, not a new check), the pins and the oracle test move
  with it. If you find yourself editing a count pin, stop: that is a sign the change grew past
  its contract.
- Tests that stub `audit` can shadow it — `gen_handoff`'s stub makes `ALL_CHECKS` read `[]`; use
  `CHECK_ORDER` when you need the roster in a test.

## RESOLVE THESE BEFORE YOU EDIT (do not take the contract's word — it is a plan, not evidence)

1. Find the actual sibling assumption in both modules. Grep for the literal parenting
   (`parent.parent`, `"Dev"`, `..`, `resolve()`-then-sibling) rather than assuming a single
   constant exists. Report what you found, with `file:line`, in the packet — the row's premise
   that it is "hardcoded" in **both** modules is itself a claim to verify.
2. Establish the precedence you are landing and write it into the docstring (done-item 4):
   explicit argument -> environment variable -> registry/config entry -> sibling default. Pick
   the shape that matches what already exists in the repo (`ecosystem/*.yaml` is the registry
   home) rather than inventing a new configuration surface — **library-first on our own organs**.
3. Done-item 3 asks that `audit repo <name>` runs **from a checkout with no sibling tree**. Prove
   it in a test with `tmp_path`, not by moving anything on disk. `GIT_DIR` overrides both cwd and
   `-C` in a subprocess — if your test shells out to git, scrub the environment
   (`git rev-parse --local-env-vars`) or the test will silently read the wrong repo.

## HONEST NOTE FROM THE DISPATCHER

The contract's anti-pattern list forbids "widening into the profile-ruling read (separate row)"
and "touching manifest files". `deploy/manifest-v*.yaml` and `.claude/methodology-roster.md` are
manifest files; `roster-freshness` gates the latter against the former. If your seam makes a
manifest read differently, that is the signal you have widened — stop and report it as a
candidate filing.

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
