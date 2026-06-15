# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-15-dev-knowledge-architect` |
| **Mode** | **architect** (v5 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff at the close of the **modularization arc** — not a carry-forward refresh. The 2026-06-13 architect theme ("finish the v5 handoff machinery deferred at the #149 flip") **largely landed since**: #163 teeth validator shipped, #156 durable task-graph shipped + ADR-66 ratified, Q9 resolved by ADR-84 (automation-writer isolation), PLAYBOOK Move 1 pointerized, collision graph encoded. The **two queued Council-bound design threads** are now the work: **(A) the hybrid handoff design** (handoff = CC repo-bundle *facts* + architect strategic brief *judgment* — demonstrated by today's `-session` bundle) and **(B) PLAYBOOK Move 2** (the structural split). The last machinery build item, **#164 (the v5 generator)**, is still open — every bundle, including this one, is hand-assembled. |
| **Generated at** | HEAD `ea9f190`, working tree clean, `main` **in sync** with `origin/main` (no ahead/behind — a change from both prior bundles; the 2026-06-15 push reconciled the gap). Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop /
> rationale lives **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read
> it for the walkthrough. This file carries only the **session header** (above) + the
> **paste-pointer** (below). v5 bundles carry **no per-bundle README** by design (the
> 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste the **full contents of `protocols/HANDOFF_BOOT.md`** — the ~3-line core **plus** the
   resident browser operating role (**both** the execution-mode default *and* the
   **architect-mode generative posture** travel in that one file). Never assume a CC-held file
   reaches the file-less browser, so that file is the thing you paste — not this one.
3. The browser replies with its on-load acknowledgment line (it names the Layer-1 actor); a
   partial or missing paste is then visible.
4. **This handoff is architect mode.** Tell the browser (or it reads it off `RESIDUAL.md`): use
   the **generative / decompositional** posture in `protocols/HANDOFF_BOOT.md` §"Architect mode"
   — orient first, **ask the operator for off-repo context**, drive decomposition, hold the
   whole-system view, surface design tensions — **not** the reactive-filter default.
5. **Orient before any mechanism.** Hand the browser `PROBES.md` **P1** (the orientation probe)
   first; it replies `run <command>`, CC reads live `VISION.md` / `ARCHITECTURE.md` Ch1 and
   substring-checks. The architect may not begin design until it holds both orienting lines.
6. **Then the operator-context beat (§13d).** After orienting, before design, the browser asks
   **one** targeted question for **off-repo** context — intent, priorities for this planning
   session, findings not in the repo, changed decisions. This is the channel the repo-derived
   residual structurally cannot carry (*off-repo only*, *architect mode only*). Answer it.
   (Note: exercising this beat in a real architect session is the only-remaining clause of **#159**
   — this session is the candidate.)
7. Hand `RESIDUAL.md` (drift-flags first — this time the headline is **clean**: `main` in sync,
   `audit.py health` OK, the lone WARN is the dispositioned `#77`) and run the rest of `PROBES.md`
   (P2–P9). Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `protocols/HANDOFF_BOOT.md` is the boot source and
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the
source wins — fix the pointer.
