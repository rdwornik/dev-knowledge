# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-16-dev-knowledge-architect` |
| **Mode** | **architect** (v5.1 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff at an arc boundary. The 2026-06-15 headline design thread — **(A) the hybrid handoff** ("v5 has no formal slot for browser-authored judgment") — **substantially landed as HANDOFF_PROCESS v5.1** (the architect strategic supplement: the architect's *why* becomes a first-class advisory supplement via a structured 6-question interview). A **new** governance theme also shipped its v1: **ADR-85 session-lifecycle enforcement** (a deterministic, no-LLM Stop-gate — hard JOURNAL leg + advisory BACKLOG leg + HEAD-bound `/override`) plus the **Stop-hook loop fix** (#142). The consolidation pass filed **#170** (traceability-spine ADR → unblocks #168) and **#171** (conformance dashboard → unblocks #169), + **ADR-86**. The next session inherits: **dogfood the v5.1 supplement + §13(d) beat** (#159 — this handoff is the first to reach the supplement step), **finish #164** (the v5 generator, now also wiring the supplement emission), the two NEW build chains (#170→#168, #171→#169), and the standing Council-bound threads (**PLAYBOOK Move 2**, #162 vocab, #161 probe-core, #165 diagram rule). |
| **Generated at** | HEAD `0752efa`, working tree clean, `main` **ahead 9** of `origin/main` (unpushed — a change from the 2026-06-15 in-sync state; the ADR-85/v5.1/Stop-hook arc landed locally, not pushed). This handoff's own commits increment the ahead-count. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop /
> rationale lives **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read
> it for the walkthrough. This file carries only the **session header** (above) + the
> **paste-pointer** (below). v5 bundles carry **no per-bundle README** by design (the
> 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste **`PASTE_THIS.md`** (in this bundle directory) — it contains the browser role file,
   residual, and probes assembled in order. One paste; the browser receives everything it needs.
   Never assume a CC-held file reaches the file-less browser, so `PASTE_THIS.md` is the thing you
   paste — not individual bundle files and not `protocols/HANDOFF_BOOT.md` directly.
   *(No `SUPPLEMENT.md` is bundled this session — this handoff was generated after a `/clear`, so
   there was no outgoing architect-browser to interview; `assemble_paste.py` `[warn]`s it absent,
   which is expected, not a defect. See `RESIDUAL.md` §2 "The supplement-interview finding".)*
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
   (Exercising this beat **and** the v5.1 supplement interview in a real architect session is the
   only-remaining clause of **#159** — this session is the candidate.)
7. Hand `RESIDUAL.md` (**drift-flags first — the headline is NOT clean this time**: the actionable
   `ARCHITECTURE.md` `pytest_collected` 511→530 drift + `main` ahead 9 unpushed; the lone WARN is
   the dispositioned `#77`) and run the rest of `PROBES.md` (P2–P9). Any probe FAIL blocks
   onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `PASTE_THIS.md` is the assembled boot source (generated
by `scripts/assemble_paste.py`, never hand-edited) and `docs/handoffs/README.md` is the operator
runbook. If a pointer and its source disagree, the source wins — fix the pointer or regenerate
`PASTE_THIS.md`.
