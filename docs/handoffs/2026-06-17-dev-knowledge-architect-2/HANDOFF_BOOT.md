# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-17-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one arc-boundary past `2026-06-17-dev-knowledge-architect` (this is bundle **#2** of 2026-06-17). Two linked things landed since that bundle: **(1)** its `SUPPLEMENT.md` was **filled** with real architect answers — the **first end-to-end #159 fill→fold dogfood** — surfacing the operator's strategic reframe, **"file-oriented dependency management"** (Markdown files = objects, the AI = runtime; the systemic fix for the coherence-by-memory failure class); and **(2)** the **coherence spine v1** shipped whole (**#172** "Done when" met → ready for `/review-closures`; **#171** dashboard now buildable against the locked `Finding` format) — *the first concrete v1 of that very reframe*: a deterministic reconciliation checker (the **20th** `ALL_CHECKS` entry) + forgotten-bump nudge + an over-extracting enumerator + the `check-against-spec` LLM-verdict skill + an e2e closure gate. The next session inherits: **elaborate the "file-oriented dependency management" paradigm + run coherence v2** (firing-rate-gated on `logs/coherence-nudge.log` — the candidate top thread), **finish #164** (the v5 generator, always-file `SUPPLEMENT.md`), the **incoming §13(d) beat** (#159's last clause), and the standing threads — **PLAYBOOK Move 2** (#39, Council-bound), **#162** vocab, **#161** probe-core, **#165** diagram rule, the two ADR-85 chains **#170→#168** / **#171→#169**, and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `adf0cbe`, working tree clean, `main` **in sync** with `origin/main`. This handoff's own commits put `main` **ahead** of origin until pushed; **two merged stragglers** (`docs/handoff-2026-06-17-architect`, `…-supplement-filled`) await operator `-d`. Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

> **⚠ UPDATE — supplement FILLED (warm).** Generated cold, but the operator then `supplement filled`
> real architect answers (the **second #159 fill→fold dogfood**), now folded into `PASTE_THIS.md`
> (answers-only). Read the folded `SUPPLEMENT.md` answers as the authoritative strategic *why* (name
> the paradigm as an ADR; the enumerator is load-bearing; the §16 do-not-build list; next failure
> classes in priority order). **First backlog action for the next architect: extract `#172`'s
> v2-deferred items into their own IDs before `#172` is closed, or the roadmap orphans.** The §13(d)
> beat **narrows** to "changed since the supplement?" (not full).

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
   *(A `SUPPLEMENT.md` **is** bundled this session — v5.2 always-generates it — and it was **FILLED**
   post-generation: the bundle was generated cold (fresh CC session), but the operator then obtained
   real architect answers and `supplement filled` them, so `assemble_paste.py` **folds the ANSWERS
   region into `PASTE_THIS.md`** (answers-only — no QUESTIONS leakage). This is the **second real #159
   fill→fold dogfood**. Consequence for step 6: the §13(d) beat **narrows**, it does not fire full.)*
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
   bundle's supplement was **FILLED** post-generation (UPDATE note in step 2), the beat **narrows** to
   "anything changed since the supplement was written?" — its answers already carried the off-repo
   context (Q6 + addenda). Read the folded answers first, then ask only what changed since.
7. Hand `RESIDUAL.md` (**drift-flags first** — the headline is **clean on doc-claims** this time:
   the prior bundle's `pytest_collected` carry was **resolved** (587/587) and `main` is back in
   sync; the lone WARN is the dispositioned `#77`, plus two merged stragglers to `-d`) and run the
   rest of `PROBES.md` (P2–P9). Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `PASTE_THIS.md` is the assembled boot source (generated
by `scripts/assemble_paste.py`, never hand-edited) and `docs/handoffs/README.md` is the operator
runbook. If a pointer and its source disagree, the source wins — fix the pointer or regenerate
`PASTE_THIS.md`.
