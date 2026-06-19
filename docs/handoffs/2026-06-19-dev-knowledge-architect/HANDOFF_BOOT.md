# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-19-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one workday past `2026-06-18-dev-knowledge-architect`, capturing the 2026-06-19 window (scope-matrix **Case 2** — clean tree, commits since the `496016a` `…-architect` bundle, today's slug absent). The window landed the **enforcement seal**: **(1)** the **Phase-1 "seal" integration** — three worktree tracks merged `--no-ff` to `main` (seal-hooks: **#188** hook-completeness audit [OPEN] + the **C1** per-session JOURNAL SHA-anchor fix in `session_end_backpressure.py` + an ADR-85 amendment; seal-dedup: **#187** dedup-on-entry WARN + **#186** floor-sync of the #156 task-graph checks into the plugin floor; grooming: **#140** `doc_rot` grooming-gate, `ALL_CHECKS` 20→**21**), closing **#187 / #186 / #140**; **(2)** **ADR-88** *file-oriented dependency management* **authored** (`7e6f996`, **Proposed**) — the capstone the 2026-06-18 supplement directed, now existing-but-unratified; **(3)** the **consolidation doc-currency seal** — `DEFINITION_OF_DONE` C1-boundary rewrite (push→session), **ESSENTIALS** brought under the freshness gate (check #10), a sealed state report; **(4)** a **PLAYBOOK/ESSENTIALS currency groom** (purged the archived `/boot`,`/evolve`; fixed coherence) and a **session-wrap** (pushed `main`, deleted 9 merged branches + 3 seal worktrees, archived 2 deep-research transcripts). The next architect inherits the still-open strategic spine — **unify + encapsulate the methodology into ONE self-enforcing, deployable whole, with #131 (ai-council onboarding) as the first deployment test** (the 2026-06-18 filled supplement's directive) — now with the **capstone ADR-88 authored but unratified**, plus **#184** (demonstrate ADR-87, rides #131), the **§7 graduated review-command reconcile** (still not landed), **#181** coherence-v2 (data-gated on `logs/coherence-nudge.log`), **#164** (the v5 generator), the standing threads (**#162** vocab, **#161** probe-core, the **#170→#168** / **#171→#169** ADR-85 chains), and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `3a894ee`, working tree clean, `main` **in sync** with `origin/main` (0 ahead / 0 behind at generation). This handoff's own commits put `main` **ahead** of origin until pushed. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **⚠ This bundle is COLD.** Generated in a fresh `/clear`ed CC session, reconstructed from
> JOURNAL + live git (not witnessed-live). `SUPPLEMENT.md` is committed with **empty ANSWERS** —
> there is no outgoing 2026-06-19 architect chat in context to interview. Consequence: the
> assembler folds **no** supplement section into `PASTE_THIS.md`, and the incoming architect's
> **§13(d) operator-context beat fires FULL** (there is nothing to narrow against). If an outgoing
> chat *does* exist, the operator may `supplement filled` it later — then re-run
> `scripts/assemble_paste.py` and the beat narrows. The most recent transmissible strategic *why*
> is the **2026-06-18 filled supplement** (`docs/handoffs/2026-06-18-dev-knowledge-architect/SUPPLEMENT.md`)
> — read it as carried context (pointer in `RESIDUAL.md` §2/§3).

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
   *(A `SUPPLEMENT.md` **is** bundled this session — v5.2 always-generates it — but it is **COLD**
   (empty ANSWERS), so `assemble_paste.py` folds **no** supplement section. Consequence for step 6:
   the §13(d) beat **fires FULL**, it does not narrow.)*
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
   residual structurally cannot carry (*off-repo only*, *architect mode only*). Because this
   bundle's supplement is **COLD** (empty ANSWERS), the beat **fires FULL** — read the
   *2026-06-18* filled supplement first for the most recent strategic *why*, then ask the full
   off-repo question.
7. Hand `RESIDUAL.md` (**drift-flags first** — the headline this time is an **undispositioned
   process slip**: `audit.py ship-gate` is **RED** because two 2026-06-19 wrap commits
   (`3a894ee` journal-wrap, `d0f9ead` transcript-archive) landed **direct on `main`** (FF/direct,
   violating core-invariant #5); they are **already pushed**, so they cannot be un-FF'd without a
   history rewrite — the resolution is a disposition-register entry **or** operator acceptance,
   **a next-session decision, not fixed in this handoff** (§1); the lone other flag is the
   dispositioned `#77` `[~~]`, and `pytest_collected` is now **clean** 667/667 — the prior bundle's
   587-vs-614 re-drift was fixed in the consolidation) and run the rest of `PROBES.md` (P2–P9).
   Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `PASTE_THIS.md` is the assembled boot source (generated
by `scripts/assemble_paste.py`, never hand-edited) and `docs/handoffs/README.md` is the operator
runbook. If a pointer and its source disagree, the source wins — fix the pointer or regenerate
`PASTE_THIS.md`.
