# NB2 · LANE G — pre-freeze contract validator: [#591] extension, prior-seat R-Q4 — M

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge` (the hub)
**Branch:** `worktree-lane-g-591-preflight-predicates` · **Frozen by the architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N8.**

**Substrate:** local
**Worktree pairing:** slug `lane-g-591-preflight-predicates` -> branch `worktree-lane-g-591-preflight-predicates`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-g-591-preflight-predicates --permission-mode bypassPermissions "[dev-knowledge . #591 . pre-freeze predicates] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-G-591-preflight-predicates.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N8 — pre-freeze contract validator: [#591] extension, prior-seat R-Q4 — M
> Write-scope: the [#591] validator module (`scripts/validate_substrate.py` or its ruled sibling —
> extend the existing organ, LIBRARY-FIRST on our own organs, never a new rival) + its tests.
> Intent: the three architect premise errors of 2026-08-28 become mechanically impossible at
> freeze time, and the live `**Shape:**`→'one' mis-parse (finding C-F) is fixed in the same organ.
> Done: four predicates run on a contract FILE at freeze time, each with a failing-then-passing
> test: (i) every referenced off-repo input EXISTS at freeze; (ii) every "verified"/"measured"
> claim carries a witness (command or file:line); (iii) every cited [#id]/ADR/register id resolves
> live; (iv) the declared do-not-touch set is checked against detector scope roots. Plus: (v) the
> C-F defect fixed — `**Shape:**` prose no longer parses as a substrate declaration, regression
> test included; (vi) batch-1's frozen contract, run through the validator, reproduces exactly the
> three known defects (the validator's own acceptance evidence).
> Anti-patterns: a new standalone checker beside [#591] · predicates as prompt prose · weakening
> the substrate check to make C-F "pass".

## RESOLVED LOCATORS (verified at dispatch — open each before you act on it)

- **The [#591] organ is `scripts/validate_substrate.py`** (module docstring: *"the substrate
  validator, LAYER 2 (`[#591]`, intake #52 I4)"*), tests at `tests/test_validate_substrate.py`.
  Its registry is `ecosystem/substrate-registry.yaml`; it hard-codes no substrate name. **Extend
  it. Do not create a rival.** Note there is also `scripts/preflight_contract.py` and
  `scripts/gen_lane_contract.py` — establish which of the three is the right home for a
  *freeze-time* predicate before writing code, and **say which you chose and why** in the packet.
  The contract names [#591]; if the honest home turns out to be `preflight_contract.py`, that is
  a ruled-sibling reading the contract's own parenthetical permits — take it and justify it.
- **The C-F mis-parse** is visible in the docstring's own note: `gen_lane_contract` emits
  ``**Shape:** `local` `` while Ch8 and hand-authored contracts write `**Shape:**` followed by
  *prose*. Prose beginning "local mutation lanes = worktrees…" currently parses to the token
  `one`/`local`. Read the parse site, reproduce the mis-parse in a RED test first, then fix it.
  **Do not weaken the substrate check to make it pass** — the fix is a tighter declaration
  grammar (a declaration is a fenced/backticked token, prose is not a declaration), not a looser
  one.
- **The three architect premise errors** predicates (i)–(iii) must reproduce are recorded in
  `LESSONS.md` (appended 2026-08-28, commit `fef1e0a6`) and in
  `docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md`. In one line each:
  an **off-repo artifact assumed on disk**; **"verified"** asserted for a ratchet scope root that
  was not verified (`ecosystem/*.yaml` IS in ratchet scope); **[#587] cited for [#608]'s seam**.
- **Batch-1's frozen contract, for done-item (vi):**
  `docs/audits/2026-08-28-technical-batch1-launch-contracts/BATCH1-LANE-CONTRACTS-2026-08-28.md`
  (13,213 B, committed and immutable). That file is your acceptance fixture. Copy it into
  `tests/fixtures/` if the test needs a stable input — `tests/fixtures/**` is an allowlisted home.

## A FOURTH INSTANCE OF THE SAME CLASS, FOUND AT DISPATCH — use it

Lane F's contract restates batch-1's measurement of the AGENTS.md byte payload as
"9,161 B = 28.0%". Measured tonight: repo-root `AGENTS.md` is **5,539 B / 107 lines**, not
"5,270 B / 103 lines", and it has been 5,539 B **since its only content commit `43c18e9f`** —
so `CLAUDE.md` §2.68's figures were false when written. That is predicate (ii) exactly: a
**"measured" claim whose witness does not resolve**. If your predicate (ii) can flag it, it is
worth more as a fifth acceptance case than any synthetic fixture. Report whether it does.

## PREDICATE DESIGN NOTES (constraints, not a design — the design is yours)

- **(i) off-repo inputs.** The failure mode is a contract naming a file the executor cannot
  reach. An absolute operator-disk path and a bare filename resolving against the prompts dir are
  both "off-repo". Existence is checked **at freeze**, on the machine doing the freezing, and a
  MISS is a REFUSAL naming the path — not a warning.
- **(ii) witness-carrying claims.** The trigger words are the contract's own: `verified`,
  `measured`, and their inflections. A witness is a command line or a `file:line`. Beware false
  positives on quoted prose — the batch bundles quote their own lanes. State the precision/recall
  trade you chose; a detector this repo cannot trust is a detector it will disable.
- **(iii) live id resolution.** `[#id]` resolves against `tasks/` (the source of truth since
  [#589] — **not** `BACKLOG.md`, which is a one-line generated VIEW and would let the check pass
  on an empty set). ADR ids resolve against `docs/decisions/ADR-*.md`. Register ids resolve
  against `protocols/STANDING_RULINGS.md` headings.
- **(iv) do-not-touch vs detector scope roots.** The concrete instance: a contract declaring
  "ratchet untouched" while its write-scope lands inside `silent_rule_detector._SCOPE_RULES`.
  Read `_SCOPE_RULES` from the detector; do not restate it.
- **Exit codes:** follow the sibling gates in this repo — 0 clean, 1 violation, 2 internal error,
  and an internal error **BLOCKS** (Z-G4: a check that cannot compute its ground truth FAILS, it
  does not skip).
- **Wire it into no gate tonight.** The contract asks for predicates that *run on a contract
  FILE*; arming a new pre-commit hook is a separate act with its own roster and doc consequences
  (`ARCHITECTURE.md` Ch2, CLAUDE.md §9 — both outside your write-scope). Ship the organ + a CLI;
  report the arming as a candidate filing.

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
