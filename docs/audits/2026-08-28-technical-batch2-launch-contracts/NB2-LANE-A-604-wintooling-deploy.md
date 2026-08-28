# NB2 · LANE A — [#604] remainder + [#606] win-tooling first slice — L — **TWO REPOS**

**Batch:** night-batch-2 · **Dispatched from:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Hub branch:** `worktree-lane-a-604-wintooling-deploy`
**Consumer branch (you create it):** `worktree-lane-a-604-wintooling-consumer` in
`C:\Users\1028120\Documents\Dev\win-tooling`
**Frozen by the Layer-1 architect, 2026-08-28. Architect's lane id in the frozen bundle: N1.**

**Substrate:** local
**Worktree pairing:** slug `lane-a-604-wintooling-deploy` -> branch `worktree-lane-a-604-wintooling-deploy`


## Dispatch

```
claude --bg --model opus --effort high --worktree lane-a-604-wintooling-deploy --permission-mode bypassPermissions "[dev-knowledge . #604 #606 . win-tooling deploy] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-LANE-A-604-wintooling-deploy.md"
```

## LANE CONTRACT (verbatim from the frozen bundle)

> ### N1 — [#604] remainder + [#606] win-tooling first slice — L
> Write-scope: HUB `ecosystem/{deployed-versions,satellite-onboarding-rulings,parity-surfaces}.yaml`
> + `ecosystem/win-tooling/history/` · CONSUMER win-tooling `.claude/` (CLAUDE-FLOOR.md,
> settings.json) + `.pre-commit-config.yaml`. RULING-W throughout: the authorizing amendment lands
> BEFORE the consumer write.
> Intent: win-tooling goes from zero enforcing organs to floor + pre-commit set + session gate +
> /ship at engine v1.4.0, parity flips pre-deploy→consumer, and the repo stops being one disk
> failure from loss. The operator's deployment mandate, landing.
> Done: (1) **re-measure first** — every hub-side claim about win-tooling re-derived on the live
> consumer (the hub picture is a PLAN: 51 baseline commits are local-only; treat X1 as the one
> verified discharge — v1.4.0 resolves local AND origin, so [#606]'s blocking precondition is
> DISCHARGED); (2) **P5 check** — establish whether the deploy path requires an ANNOTATED tag; if
> yes, STOP that step, report for the morning; (3) deploy: floor present, pre-commit set armed,
> session gate + /ship live, verified by `audit repo win-tooling` reporting so, with a FRESH
> baseline in `ecosystem/win-tooling/history/`; (4) parity `role: pre-deploy → consumer` flipped
> AFTER the proof, never before; (5) [#604] fold: terminal-setup carries a null-valued
> deployed-versions key + a rulings entry naming full|floor-only with ruled_by and date; (6)
> workspace_settings recorded hand-fixed or accepted-debt — the editor-config carrier is
> declaration-only and CANNOT close it; (7) **branch backup:** 11/11 win-tooling branches carry
> upstreams (`git push -u origin <branch>` each; backup only, zero merging, zero cleanup —
> `git branch -vv` recorded); (8) commit-and-STOP on both sides.
> Anti-patterns: writing into win-tooling outside RULING-W · touching DispatchHelpers (N2 owns it) ·
> retroactive amendment · trusting the stale hub baseline · improvising a tag rewrite at night.

## P5 — THE TAG CHECK IS YOUR FIRST ACT (frozen ruling, carried)

> **P5 (tag):** v1.4.0 is a LIGHTWEIGHT tag; siblings are annotated and manifest-v1.0.0's
> comment says "annotated + resolvable". N1's first act includes the annotation-requirement
> check; if annotation is required, that step STOPS and reports (morning operator fix —
> re-tagging is a history-adjacent act, never improvised at night).

Re-tagging is **forbidden tonight**, in both repos, under any reading. If the deploy path
requires an annotated tag, that single step stops; **everything else in this contract still runs**
and the packet says exactly which step stopped and why.

## THE TWO-REPO SHAPE — mechanically

You booted into a **hub** worktree. The consumer half needs its own worktree because a sibling
lane (lane B, the architect's N2) is committing in win-tooling at the same time — one checkout is
one committing session:

```
git -C C:\Users\1028120\Documents\Dev\win-tooling worktree add ^
    C:\Users\1028120\Documents\Dev\win-tooling\.claude\worktrees\lane-a-604-wintooling-consumer ^
    -b worktree-lane-a-604-wintooling-consumer
```

(Use the PowerShell/`git -C` form that actually works in your shell — the point is the path and
the branch name, not the line continuation.) **RULING-W, verbatim from `ESSENTIALS.md`:** *the hub
MAY and SHOULD write into a consumer for methodology/cleanup, and the only sanctioned shape is
**consumer worktree/branch → report** — never a direct push into a live consumer checkout;
re-witness the consumer live first.* **Mechanism before act:** the hub-side authorizing amendment
(the `ecosystem/*.yaml` rows) is **committed on the hub branch BEFORE** the corresponding consumer
write. A permission cannot be earned retroactively.

**Do not touch `config/dispatch-helpers/DispatchHelpers.psm1` or `tests/test_dispatch_helpers_*`**
— lane B owns them and is running concurrently.

## MEASURED AT DISPATCH (hub-side facts, so you re-measure the consumer, not these)

- win-tooling primary is on `main` at `53a1d02`, working tree **clean**.
- **11 local branches**, and **exactly one (`main`) carries an upstream.** That is done-item (7)'s
  before-state: `chore/root-artifact-dispose-and-guard`, `feat/cloud-models`,
  `feat/codespace-remote-exit-code`, `feat/dispatch-codespace`, `fix/check-advisory-unowned-path`,
  `fix/cloud-models-fail-fast`, `fix/codespace-bypass-permissions`,
  `fix/credential-scope-default-shell`, `fix/dispatch-three-column-table`,
  `fix/sanitise-external-text`, `main`. Remote: `https://github.com/rdwornik/win-tooling.git`
  (private, per STANDING_RULINGS G3). Record `git branch -vv` before and after.
- **Four worktrees already exist** in win-tooling (`cloud-fail-fast`, `cloud-models`,
  `external-text`, `fix+check-advisory-unowned-path`). They are the morning's X3 item.
  **Do not remove them** — cleanup is explicitly out of scope for done-item (7) and removing a
  worktree is a destructive act nobody authorized tonight.
- Hub parity today: `ecosystem/parity-surfaces.yaml` line ~135 carries
  `win-tooling: {role: pre-deploy, …}`. Item (4) flips it **after** the proof.

## GATE HAZARDS YOU WILL HIT (both repos)

- Committing in the hub with a consumer-repo edit staged is not possible — they are separate
  repos. Commit each side in its own worktree.
- `audit-health` runs `audit.py health` at hub pre-commit; `fleet_audit_replication` FAIL wedges
  every hub commit. Prove ownership before reaching for `SKIP=`; a declared, reasoned
  `SKIP=<hook>` in the commit body is the sanctioned escape, `--no-verify` is not.
- A commit-context `fleet_parity` run can mis-resolve a consumer; if that is what fires, the
  recorded lever is `SKIP=audit-health` **with the reason stated in the commit body**.
- Arming pre-commit in win-tooling means `pre-commit install --hook-type pre-commit
  --hook-type commit-msg --hook-type pre-push`. A relic `core.hooksPath` silently disarms
  everything — check `git -C <repo> config --get core.hooksPath` and report what you found.
- `git push -u origin <branch>` × 10 is an **outward-facing act that the operator pre-authorized
  in this contract** (backup only). Push nothing else, merge nothing, delete nothing.

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
