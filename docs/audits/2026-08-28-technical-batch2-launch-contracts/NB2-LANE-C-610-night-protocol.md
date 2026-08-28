# NB2 · LANE C — [#610] doc half: the night-batch protocol chapter — M — **RATCHET LANE**

**Batch:** night-batch-2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge` (the hub)
**Branch:** `worktree-lane-c-610-night-protocol` · **Frozen by the Layer-1 architect, 2026-08-28.**
**Architect's lane id in the frozen bundle: N3.** This file is the contract of record; the bundle
it was cut from is `docs/audits/2026-08-28-technical-batch2-launch-contracts/NIGHT-BATCH2-CONTRACTS-2026-08-28.md`.

**Substrate:** local
**Worktree pairing:** slug `lane-c-610-night-protocol` -> branch `worktree-lane-c-610-night-protocol`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-c-610-night-protocol --permission-mode bypassPermissions "[dev-knowledge . #610 . night protocol] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-C-610-night-protocol.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N3 — [#610] doc half: the night-batch protocol chapter — M — RATCHET LANE
> Write-scope: `protocols/PLAYBOOK.md` + `protocols/HANDOFF_PROCESS.md` (forms-card delta ONLY) —
> the batch's single ratchet authorization covers both; no other protocols/ file.
> Intent: the night protocol stops being operator habit; and the two rules this window proved can
> die in a seat's head become bundle-carried doctrine.
> Done: (1) a named PLAYBOOK section enumerating all five phases — dispatch, manifest, night run,
> morning adjudication, ledger — each with inputs, outputs, refusal conditions; (2) manifest shape
> specified so two seats produce identical sections; the 2026-08-27 landed manifest validates as
> the reference instance; (3) byte-identical-or-state-the-deviation rule, citing the two C-reports
> that opened with prose; (4) report-selection rule names the Stop-hook-noise trap; (5) ledger is a
> REQUIRED output; (6) intake-#60 constraints travel here: ~5 proposals/night cap, 7-day
> auto-expire, no autonomous semantic refactoring at night, proposals land as docs/intake/ SEEDs;
> (7) **prior-seat R-Q1/R-Q2 land as doctrine:** the session-boundary rule (five-pillar close;
> architect never initiates the bundle; operator declares closure) + the substrate-routing answer
> (local/cloud/Codespace, incl. the measured uv-provisioning nuance — "unrunnable by default,
> runnable after `pip install --target` provisioning", per the Ch8 Q1 amendment candidate) +
> HANDOFF_PROCESS forms-card carries both, so every future bundle boots them; (8) ratchet old→new
> reported.
> Anti-patterns: naming N2's verbs as though they already resolve · touching Ch8's dispatch table ·
> any protocols/ file beyond the two named.

## RATCHET — this lane's single authorization (operator, carried in the GO)

**D2: the ratchet move is authorized for THIS LANE ONLY**, bounded to the night-protocol section
plus the `HANDOFF_PROCESS.md` forms-card delta. **old → new must be reported** in your packet.

Measured at dispatch, on `main`, `2026-08-28 23:37 local`:

```
detector: silent-rule-v5
files:    61
count:    443
```

The baseline has **zero headroom** — `443` live == `443` baseline. Run the detector before your
first commit and after your last, and report both numbers. `validate_transition` refuses a
baseline *raise* in code regardless of authorization, so if your text needs headroom the
authorized move is the ruled `--accept` path for the bounded delta, and the delta you report must
be the one you actually caused. If you can author the section **token-free** (batch-1 lane L1 did
exactly this and spent ZERO of a granted allowance), that is the better outcome — say so.

## RESOLVED LOCATORS (verified at dispatch — do not re-derive, but do re-open before editing)

- The reference manifest instance: `docs/audits/2026-08-27-technical-night-harvest-manifest.md`
  (3,695 B). Its **Verification** section is the one that carries the byte-identity deviation
  record for C1/C3 — that is the "two C-reports that opened with prose" your item (3) cites.
- The ledger the protocol must require as an output:
  `docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md`.
- Ch8's dispatch table is at `protocols/PLAYBOOK.md`, heading
  `#### The dispatch table — the SOLE literal-command site`. **Do not touch it** (anti-pattern).
  Your new section is a sibling under Ch8 or a new chapter — your call, stated in the packet.
- The PLAYBOOK TOC is gated (`toc-freshness-playbook`). Adding a section means regenerating the
  TOC with the repo's own `scripts/toc/` tool — that regen is **inside** your lane, not the
  integrator's, because the gate blocks your own commit otherwise.

## HONEST NOTE FROM THE DISPATCHER (recorded, not an instruction)

Item (7) asks you to land the substrate-routing answer including the measured uv nuance. The
Ch8 Q1 row already carries that measurement as an **amendment candidate, routing unchanged
pending a ruling**. Landing it as doctrine in your new section while Q1 still says "pending a
ruling" would put two live readings in one chapter. If you judge that a conflict, the section
states the routing answer **and cites Q1's pending status**, rather than resolving it — and you
report the tension as a candidate filing. Do not edit the Q1 row.

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
