# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-04-dev-knowledge-architect` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **The [#244] essence-spec lifecycle epic is BUILT: P1→P4 all SHIPPED this window (the prior handoff resumed at P2 — this window ran P2→P3→P4 to completion, n=1 proven throughout).** The deploy engine gained a **remove leg** (ADR-96) and pruned a real component from ai-council (verified ABSENT, locally-modified REFUSED); the **methodology roster is now machine-generated** (CLAUDE.md §9 `@import`, Fable R3 closed); the **Informant gained a Tier-3 drift classifier + fleet drift line** (seb inject→DRIFT→rejected-non-waivable proven). Deployed methodology **v1.2.0 to ai-council** (tag `v1.2.0`). Only **P5 (hub self-prune #130) + P6 (fleet roll n=2+ #221)** remain of the epic. **Separately — and this is the real work of the next session — four Fable read-only reviews LANDED** (analysis-only, all merged, nothing acted on): **handoff-adoption** (headline **RF-1: the anti-bluff probe contract is INVERTED — every architect bundle including THIS one prints probe answers as `expected:` hints; the bluff-dogfood never re-ran**), **coherence-spine** (inverted investment + demonstrated self-blindness + the RF-5 FAIL-trap), the **rot-algorithm design** (build-it-small; the home for the operator's continuous-conformance vision), and the **Fable-5 architecture review**. **The next session is an ADJUDICATION session, not a build one:** (1) route the four Fable reviews' findings (RF-1 is meta-urgent — it indicts this very handoff mechanism); (2) sequence the epic tail P5→P6 (P6 gated on #225, and on NOT onboarding a consumer through a soon-to-change corpus); (3) decide build-vs-defer on the rot-algorithm / continuous-conformance vision; (4) clear the LIVE standing debt — ai-council's `CLAUDE.md` is A2-stale and the now-deployed freshness gate WILL block its next commit (a real re-review, never a faked stamp). |
| **Generated at** | Bundle cut on branch `docs/2026-07-04-architect-handoff` **off `main` (`25b104e`)**, working tree **clean**, `main` **in sync with `origin/main`** at generation. **All epic work is on `main`** — no parallel feature branch this window (contrast the prior `feat/essence-spec-p1`). This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **`SUPPLEMENT.md` is generated EMPTY.** The bundle is assembled by CC from committed repo state; the
> operator may fill the supplement from the outgoing architect chat (`supplement filled`) so its ANSWERS
> fold into `PASTE_THIS.md`, or leave it empty for a cold handoff (the defined §13 disposition). **Until
> filled, the incoming §13(d) operator-context beat fires FULL** (a full off-repo ask), not the narrowed
> *"anything changed since?"*.

> **RF-1 corrective in effect (read `PROBES.md` header).** Because the Fable handoff-adoption review
> found that every recent bundle prints its probe answers as `expected:` hints — inverting the §5
> anti-bluff contract — this bundle **deliberately withholds the probe answer values** (no counts, SHAs,
> dates, verdicts, or orienting lines). Whether the drift-reference hints should return is itself an open
> §4 decision (RF-1). The withholding IS the teeth; run the commands.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (the 2026-06-12 canonical-runbook collapse — `HANDOFF_PROCESS.md` §13).

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste **`PASTE_THIS.md`** (in this bundle directory) — the browser role file + residual + probes (+ the
   supplement ANSWERS **only if filled**), assembled in order by `scripts/assemble_paste.py`. One paste;
   never hand-feed individual files to the file-less browser.
3. The browser replies with its on-load acknowledgment line (it names the Layer-1 actor); a partial or
   missing paste is then visible.
4. **Architect mode** — the browser uses the **generative / decompositional** posture
   (`protocols/HANDOFF_BOOT.md` §"Architect mode"): orient first, ask the operator for off-repo context,
   drive decomposition, hold the whole-system view, surface design tensions — **not** the reactive-filter
   default.
5. **Orient before any mechanism** — hand the browser `PROBES.md` **P1** (orientation) first; it replies
   `run <command>`, CC reads live `VISION.md` / `ARCHITECTURE.md` Ch1 and substring-checks. The architect
   may not begin design until it holds both orienting lines. (P1's grep is a *tool* that confirms the
   frame — the **backlog navigates**, v5.3 §13c.)
6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless the operator
   fills it first the beat fires **FULL**: *"what off-repo context for this planning session — intent,
   priorities, findings not in the repo, changed decisions?"* (If the operator runs `supplement filled`,
   its ANSWERS are in the paste and the beat narrows to *"anything changed since?"*.)
7. Hand `RESIDUAL.md` — **drift-flags first** (the headline: `ship-gate` is **GREEN** and clean — **10
   WARN dispositioned**, **NO `[stale]`**) — then the **next-frontier decisions** (§4: adjudicate the four
   Fable reviews — RF-1 first — then sequence P5→P6, the rot-algorithm build call, and the ai-council
   re-stamp debt) + the **shipped-this-window** map (§2: the [#244] P1→P4 close + the four Fable landings)
   + run the rest of `PROBES.md` (P2–P9). Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
