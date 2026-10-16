# Batch BU (BUILD-1) — close packet · 2026-10-16

> The `closed_by` artifact named in `docs/audits/2026-10-15-technical-batch-bu-manifest.md`.
> Written by the integrator seat INTEGRATOR-BU cycle-4 (Claude Code, claude-opus-5-5, session
> `0c555c63`) under `to-cc/INTEGRATOR-BU-2026-10-15.md`, plan `PLAN-HARNESS-2026-10-14.md` r6 BUILD-1.
> Every figure names its instrument; a figure with no instrument is marked UNMEASURED. The full
> per-event record is the receipt `to-browser/SESSION-integrator-bu-2026-10-15.md`.

## 1. Landed on main (first-parent spine, batch base `50013d6f`)

Instrument: the `STATE` and `LAND` lines of the receipt, each from `merge_path.py land` output.
Pickup-to-push is the receipt's own minutes figure.

| Lane | Main merge | Refusals | Land verdict | CI run | Pickup-to-push |
|---|---|---|---|---|---|
| freeze `build1-prep` | `b6161972` | 0 | LANDED PRE-EXISTING | 38725590391 | — |
| `lane-bu-1539-transport` | `4ccb89c5` | 0 | LANDED PRE-EXISTING | 38775124621 | 50 min |
| `lane-bu-1535-outer-loop` | `97bcd374` | 1 (repair 1) | LANDED PRE-EXISTING | 38783484469 | 273 min |
| `lane-bu-863-prompts-guard` | `a3d0ae31` | 0 | LANDED PRE-EXISTING | 38818573365 | 50 min |
| `lane-bu-1537-codespace-finish` | `c949ffd6` | 2 (repairs 1, 2) | LANDED PRE-EXISTING | 38830068303 | 425 min |
| `lane-bu-1450-boot-v2` | `d73c56c5` | 2 (repairs 1, 2) | LANDED PRE-EXISTING | 38844207423 | 50 min |
| `lane-bu-1536-routing` | `52b9a90b` | 0 | LANDED PRE-EXISTING | 38869248123 | 49 min |

Six of six lanes MERGED; none FAILED; no STOP-THE-LINE. Every land FLAGGED one red on both
sides, never a refusal: `tests/test_archive_row_body.py::test_every_committed_record_still_proves_out`
(`[stale-registry-signature]`, ubuntu + windows). The five refusals are
`REFUSED-lane-bu-1535-outer-loop.md`, `REFUSED-lane-bu-1537-codespace-finish.md` and
`REFUSED-lane-bu-1450-boot-v2.md` on the transport (each overwritten by its later repair).

## 2. Not landed

Nothing of the batch's six lanes. The steel thread `[#1430]` was never in this batch: it is
BUILD-2 slot 1, started now that `lane-bu-1535-outer-loop` has landed.

## 3. Rows filed vs closed

Instrument: `status:` in `tasks/<id>-*.md` on main `52b9a90b`.

- **Closed (3):** `[#1535]` (carried by the 863 merge), `[#1450]` and `[#1538]` (`row_close.py`
  with CI run 38844207423, carried by the 1536 merge).
- **Held open, with evidence on the receipt (ROWS-OWED):**
  - `[#1539]`, `[#1454]`, `[#1332]` — `row_close.py` closes a contract's rows all or none;
    `[#1539]` (4)/(6) and `[#1454]` (3) wait on the operator's janitor `--apply`.
  - `[#863]`, `[#912]`, `[#1540]` — `[#1540]` needs the next conductor schedule run on main and
    its concurrent push run's legs uncancelled; `[#912]` dispositions expire 2026-10-31.
  - `[#1537]` — PARTIAL on Done-contract clause 8 (the agy nonce probe GAP: no sign-in URL).
  - `[#1536]` — DONE by its lane, but the contract's closes clause also names `[#1452]`, whose
    Done-when (1)-(2) reach `scripts/dispatch.py`, `scripts/plan_lint.py` and the S9/S10/S17 pins
    outside the lane's footprint (PREMISE-FAILED); close `[#1536]` once that remainder is ruled.
- `[#689]` is never closed by this batch (order).

## 4. BACKLOG size

Instrument: `gen_task_tree.py --emit-source` on `52b9a90b`: 661 tasks.

## 5. Hygiene (no leftovers)

- Every lane: `no_leftovers.py verify --lane <slug>` CLEAN 12/12 at its teardown (receipt).
- Lane worktrees, branches and claim markers of all six lanes: removed (receipt `TEARDOWN` lines).
- Left by operator decision: `chore/bu-1535-row-close` (local + origin; its four files are on main
  byte-identical, but it is not an ancestor, so `-d` refuses and `-D` is barred).
- The integration worktree `.claude/worktrees/integrate-bu` and this packet's branch are removed
  after this packet lands; the batch-close trial cut's only FAIL (`worktree_owners`) is that
  worktree.

## 6. Cost

- Lane cost, instrument `lane_cost.py lane --slug <slug>` (rates as_of 2026-06-24):
  1537 USD 31.17 · 863 USD 38.02 · 1539 USD 26.41 · 1535 USD 23.30 · 1450 USD 22.02 ·
  1536 USD 21.35 — **USD 162.27** for six lanes. Integrator and dispatcher seats are not in it
  (UNMEASURED here).
- Quota, instrument `quota_watch.py line` (2026-10-16): Codespaces 53.98/180 core-hours;
  Actions 12926/3000 min (public repo: not billed); Copilot 7755/20000 credits (38.8%); cloud
  sessions UNMEASURED.

## 7. Batch-close moment

`moment:batch-close` with `HARNESS_BATCH=BU` on `52b9a90b` (before this packet): the trial cut
passed every row (`ship_gate`, `boot_citations` 66/66, `journal_anchored`, `question_disposition`,
`p11_carriage`, `living_docs_stamped`, `status_byte_budget`) except `worktree_owners`, the
integration worktree that carries this packet. Re-run after its removal: recorded in the receipt.
