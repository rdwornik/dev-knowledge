---
reconciled_with: handoff-process@7.1.0
---
<!-- scope: meta -->
<!--
  templates/dispatcher-order-template.md — the DISPATCHER seat's order (`protocols/HANDOFF_PROCESS.md`
  §1). The dispatcher launches lanes and continuation/repair sessions and writes receipts. It
  does not merge and does not build.

  DISTILLED (LANE-5A-9, 2026-09-24) from the dispatcher role and sequence of
  `BATCH-WAVE5A-2026-09-23` (v2). The shared rules are `templates/batch-common-rules-template.md`
  and are not restated. A batch's dated order fills this in: the batch name, its contracts in
  wave order, its dependencies. The operator's paste of the filled order into a NEW session is
  the batch GO.

  COMMANDS COME FROM CODE (ruling O-5). The launch line is `scripts/dispatch.py launch`; its
  options are whatever `uv run --locked python scripts/dispatch.py launch --help` prints today —
  read them there, not from a copy. No model name is typed here: `dispatch.py` reads each
  contract's Model table and Dispatch block, and routing is `ecosystem/provider-registry.yaml`.
  Replace every <angle-bracket> placeholder; delete this comment.
-->
carried-by: OPEN
lands-via: the lanes it dispatches, and its receipt in to-browser/
date: <YYYY-MM-DD>
from: <architect seat slug>
authorized-by: the operator's paste of this file into a NEW CC session. This paste IS the batch GO.
plan: <to-cc/PLAN-...md §n>

# BATCH <BATCH> — dispatcher order

The common rules — `to-cc/<BATCH-COMMON-...>.md`, filled from
`templates/batch-common-rules-template.md` — bind you. **Nobody waits for the operator.**

## Your role

You launch lanes and continuation or repair sessions, and write receipts. **You do not merge.**

- **Seat:** `uv run --locked python scripts/seat_registry.py bind --role dispatcher --batch <BATCH>`.
- **Receipt:** `to-browser/SESSION-dispatcher-<batch-slug>.md`.
- **Transport root:** the `CLAUDE_PROMPTS_DIR` environment variable.
- **Launcher:** `HARNESS_BATCH=<BATCH>`, then
  `uv run --locked python scripts/dispatch.py launch --batch <BATCH> <CONTRACT>.md`. Options:
  `--help`. On a refusal (exit 5) or failure, record the output verbatim; then use the contract's
  own `## Dispatch` line and record that you did.
- **Before each fire:**
  - `worktree_occupancy.py` — 0: fire · 1: record, do not fire · 2: wait 60 s and retry;
  - at least <N> GB free and at most <M> heavy lane sessions running.
- **Before each CODESPACE fire (W2, R7 — the one hard veto):**
  `uv run --locked python scripts/quota_watch.py check --projected-core-hours <n>` — exit 0
  (OK): fire · exit 1 (REFUSED): record the refusal verbatim, do not fire. `<n>` is that
  codespace's core count × its idle-timeout ceiling in hours (e.g. 4-core × the 240-min idle
  ceiling = 16 core-hours), multiplied by (codespaces of this batch already live + 1) when a
  slot is already occupied. Every other quota (Actions minutes, storage, Copilot credits) only
  warns via `QUOTA-WARN-<date>.md` (`quota_watch.py record`, run by the lane or the integrator)
  — not a launch refusal.

## Sequence

0. **Plan lint first.** `uv run --locked python scripts/plan_lint.py <every contract of the batch>`;
   paste its output into the receipt. An overlap a contract orders with
   `**Starts after `<lane>` is merged**` is sequenced, not a finding. For any other finding,
   record it and hold only the lanes it touches.
1. **Wave α,** <k> s apart: <lane slugs, in merge-priority order>.
2. **Wave β, as slots free, in this order:** <lane slugs>.
3. **Wave γ, when the dependency shows MERGED** in the integrator's receipt
   (`STATE <lane> MERGED ...` lines): <lane> after <lane>.
4. **Liveness, every <10> min.** A lane that is gone, or idle over <30> min without a HANDBACK line,
   and at least <10> min old, gets a continuation session `<lane>-resume-<n>` in its own
   worktree — at most <2>.
5. **Repairs.** Launch a repair only from a `to-browser/REFUSED-<slug>.md` that carries both
   `from: the INTEGRATOR` and `repair N of 2`. `HANDBACK-REFUSED-*` files are a lane's own
   self-refusals: do not repair from them.
6. **Close** when `to-browser/STATE-BATCH-<BATCH>.md` reads `CLOSED`:
   - write the summary — per lane: job, extra sessions, result, and the model that served;
   - confirm it on the transport;
   - stop every Monitor, poll and shell of yours; stop.
