# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-17-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one arc-boundary past 2026-06-16. The 2026-06-16 bundle's first-dogfood finding — *a cold/`/clear`ed handoff produced **no** supplement file at all (missing-deliverable look, zero git tracking, operator un-led)* — **landed its fix as HANDOFF_PROCESS v5.2**: the architect strategic supplement is now an **always-generated, committed, self-documenting fillable file** (`SUPPLEMENT.md`), with a **defined cold-handoff disposition** (empty ANSWERS = committed N/A, not a defect) and an **ANSWERS-only, fold-if-non-empty** assembler rule (was: whole-file fold + warn-if-absent). The next session inherits: **the real #159 dogfood is STILL owed** (v5.2 *defined + hardened* the mechanism — it did **not** exercise a supplement filled with *real answers* end-to-end), **finish #164** (the v5 generator must now emit the always-file form), and the standing threads — **PLAYBOOK Move 2** (#39, Council-bound), **#162** vocab, **#161** probe-core, **#165** diagram rule, the two ADR-85 build chains **#170→#168** / **#171→#169**, and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `ef62dd8`, working tree clean, `main` **in sync** with `origin/main` (a change from the 2026-06-16 `ahead 9` — the v5.2 arc was pushed and the merged stragglers `-d`'d). This handoff's own commits put `main` **ahead** of origin until pushed. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

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
   *(A `SUPPLEMENT.md` **is** bundled this session — v5.2 always-generates it — but its ANSWERS are
   **empty**: this handoff was generated cold (a fresh CC session, no outgoing architect-browser in
   context to interview), so `assemble_paste.py` prints `ANSWERS empty … not folded` and folds
   nothing. The empty file is committed by design — the defined cold-handoff disposition, **not** a
   missing deliverable. To capture this session's strategic **why**, route the QUESTIONS in
   `SUPPLEMENT.md` to a chat that holds the v5.2 deliberation and say `supplement filled`; otherwise
   the incoming §13(d) beat below fires **full**.)*
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
   residual structurally cannot carry (*off-repo only*, *architect mode only*). Because the
   supplement ANSWERS are **empty** this session, the beat fires **full** — there is nothing to
   narrow against (§13(d) cold-handoff path). Answer it. (Exercising this beat **and** a *filled*
   supplement in a real architect session is the only-remaining clause of **#159**.)
7. Hand `RESIDUAL.md` (**drift-flags first** — the headline is *mostly* clean this time: `main`
   back in sync + stragglers cleaned, but the **actionable `ARCHITECTURE.md` `pytest_collected`
   511→534 drift carries**; the lone WARN is the dispositioned `#77`) and run the rest of
   `PROBES.md` (P2–P9). Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `PASTE_THIS.md` is the assembled boot source (generated
by `scripts/assemble_paste.py`, never hand-edited) and `docs/handoffs/README.md` is the operator
runbook. If a pointer and its source disagree, the source wins — fix the pointer or regenerate
`PASTE_THIS.md`.
