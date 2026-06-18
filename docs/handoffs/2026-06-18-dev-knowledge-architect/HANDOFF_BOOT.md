# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-06-18-dev-knowledge-architect` |
| **Mode** | **architect** (v5.2 §13 — planning / way-of-working scope) |
| **Purpose** | A **fresh** architect handoff one workday past `2026-06-17-dev-knowledge-architect-2`. The 2026-06-18 window landed four linked things: **(1)** **ADR-87** — the architect/CC **equilibrium contract** (the prompt division of labor: architect emits intent + closure + anti-patterns + mode + a thin governance-pointer; CC owns code-impact context, gotchas, the skeleton, model/effort) — codified across PLAYBOOK §2, the prompt template, ESSENTIALS, HANDOFF_BOOT; empirical close = **#184** (OPEN), GAP-2 residue = **#185** (filed, not built); **(2)** the **coherence-spine consolidation** — #172's v2 roadmap **extracted** into **#179–#183** (a NEW `coherence` serialize-group; the prior bundle's load-bearing "extract before close" first-action) and **#172 closed**; **(3)** a **backlog groom** — closed #138, condensed the giants (ADR-65), filed #187–#189 (net 83 tasks); **(4)** the **worktree / parallel-arc lifecycle** codified in PLAYBOOK (native auto-seed verified). The next session inherits the candidate top thread — **name "file-oriented dependency management" as an ADR** (the prior supplement's explicit directive; the durable #179–#183 graph now lacks its capstone doctrine) — plus **coherence v2** (#181 data-gated on `logs/coherence-nudge.log`), the **§7 review-command graduated-rule reconcile** (not landed), **ADR-87 demonstration** (#184), **#164** (the v5 generator), the standing threads (#162 vocab, #161 probe-core, the **#170→#168** / **#171→#169** ADR-85 chains, **#186** plugin-floor sync), and the **ADR-85 override-rate watch** (scope-freeze to ~2026-07-14). |
| **Generated at** | HEAD `62763d7`, working tree clean, `main` **in sync** with `origin/main`. This handoff's own commits put `main` **ahead** of origin until pushed; **no merged stragglers** (the prior bundle's two were `-d`'d). Re-derive HEAD/sync at read-time (`PROBES.md` P3). |

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
   *(A `SUPPLEMENT.md` **is** bundled this session — v5.2 always-generates it — but this bundle is
   **cold** (fresh CC session, no outgoing architect chat holds this window's deliberation), so its
   ANSWERS region is **empty** and `assemble_paste.py` folds **nothing** from it. If you have an
   outgoing chat that drove the 2026-06-18 work, you may still fill it: paste its QUESTIONS to that
   chat, paste answers below the divider, and tell CC `supplement filled` — then the answers fold in.
   Otherwise leave it empty: the §13(d) beat captures off-repo context live.)*
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
   residual structurally cannot carry (*off-repo only*, *architect mode only*). Because this bundle
   is **cold** (empty ANSWERS — UPDATE note in step 2), the beat **fires FULL** — read the *prior*
   bundles' filled supplements first for the most recent strategic *why*, then ask the live question.
7. Hand `RESIDUAL.md` (**drift-flags first** — the headline this time is an **actionable re-drift**:
   `pytest_collected@ARCHITECTURE.md` says 587 but live pytest collects 614 — a next-session fix owed,
   *not* fixed in this handoff (§1); the lone other flag is the dispositioned `#77` `[~~]`, and `main`
   is in sync with no stragglers) and run the rest of `PROBES.md` (P2–P9). Any probe FAIL blocks
   onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are
referenced by **pointer**; CC (which holds the repo) serves any part the file-less browser
needs, just-in-time. This file points; `PASTE_THIS.md` is the assembled boot source (generated
by `scripts/assemble_paste.py`, never hand-edited) and `docs/handoffs/README.md` is the operator
runbook. If a pointer and its source disagree, the source wins — fix the pointer or regenerate
`PASTE_THIS.md`.
