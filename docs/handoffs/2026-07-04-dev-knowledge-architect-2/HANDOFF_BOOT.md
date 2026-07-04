# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-04-dev-knowledge-architect-2` |
| **Mode** | **architect** (v5.3 §13 — planning / way-of-working scope) |
| **Purpose** | **Second architect handoff of 2026-07-04 — the delta since the `-architect` bundle (`c185c09`), which is: the operator's re-sequenced program moved into execution.** The prior (filled) supplement re-ordered everything around **deployment · sandbox · tests** and ruled **P5/P6 WAIT**: Phase 0 (safety + self-honesty) → Phase 1 (build the lived-workflow **sandbox** as the retroactive acceptance instrument for [#244] P1–P4) → Phase 2 (fleet re-gated). This window executed into that: **(1) ARCHITECTURE 2026-07-04 currency re-read** (coherence-spine self-blindness cleared — `undeclared_edges` now verified live in `ALL_CHECKS`, `roster-freshness` gate added, honest re-stamp); **(2) RF-2 hub self-arm + `hooks_armed` check** (the sandbox's own precondition; delete-a-hook→`health DEGRADED` demonstrated); **(3) the handoff-generator lane** — `gen_handoff.py` + the anti-bluff RF-1 answer-hint rung made **STRUCTURAL, not hand-discipline** ([#164]/[#161]/[#163], NOT closed); **(4) lived-workflow sandbox Slice A** ([#252]) — isolated `claude -p` **spawn + isolation PROVEN + Codex-hardened** (2 CRIT + 2 HIGH fixed), then **STOP at the Slice A gate for architect review**. **The next session's PRIMARY job is that review:** adjudicate the spawn+isolation foundation → on approval, build **Slice B** (OUTER deterministic observer + `engages:`-spec oracle + six-hook arc + seeded-EXPECTED-BUT-SILENT closure). Secondary, all still open: (a) **integrate the handoff-generator's deferred spec arc** (HANDOFF_PROCESS §5/§13 → option b + `5.3→5.4` bump + 5 `reconciled_with` re-stamps — decoupled to the architect because it collides with sandbox-owned `ARCHITECTURE.md`); (b) **route the four carried Fable reviews** (RF-1 now *structurally* half-fixed — the spec re-ratify + first bluff-dogfood-rerun still owed); (c) hold **P5/P6** per the operator rule; (d) clear the LIVE debts — **ai-council `CLAUDE.md` A2-stale** (the deployed freshness gate will block its next commit) and a **flagged `ANTHROPIC_API_KEY` leak** into this session's local transcript (rotation recommended). |
| **Generated at** | Bundle cut on branch `docs/2026-07-04-architect-handoff-2` **off `main` (`a523fca`)**, working tree **clean**, `main` **in sync with `origin/main`** at generation. **All window work is on `main`** — no parallel feature branch open (the sandbox `feat/lived-sandbox-slice-a` and `feat/handoff-generator` lanes already merged `--no-ff`; only `automation/fleet-audit`, a routine baseline branch, remains unmerged — separate concern, leave). This bundle's own commit + the later `/ship` `--no-ff` merge move HEAD and push `main` ahead of `origin` until pushed. **Re-derive HEAD / sync at read-time** (`PROBES.md` P3) — do not trust this line. |

> **`SUPPLEMENT.md` is generated EMPTY.** The bundle is assembled by CC from committed repo state; the
> operator may fill the supplement from the outgoing architect chat (`supplement filled`) so its ANSWERS
> fold into `PASTE_THIS.md`, or leave it empty for a cold handoff (the defined §13 disposition). **Until
> filled, the incoming §13(d) operator-context beat fires FULL** (a full off-repo ask), not the narrowed
> *"anything changed since?"*.

> **RF-1 corrective in effect — now the RATIFIED, STRUCTURAL contract (read `PROBES.md` header).** The
> Fable handoff-adoption review found every recent bundle printed its probe answers as `expected:` hints,
> inverting the §5 anti-bluff contract; the operator **re-ratified** withholding ("treat every `expected:`
> as SUSPECT") and this window made the fix **structural** — `verify_handoff_probes._classify` now FAILs a
> probe that ships an answer hint, so the erosion cannot silently return. This bundle **deliberately
> withholds the probe answer values** (no counts, SHAs, dates, verdicts, or orienting lines). The
> withholding IS the teeth; run the commands.

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
7. Hand `RESIDUAL.md` — **drift-flags first** (the headline: the standing dispositioned set only, no new
   regression this window — re-derive the verdict + count live via `PROBES.md` P7) — then the
   **next-frontier decisions** (§4: **the Slice A review gate is the primary**; then the deferred
   handoff-spec arc, the carried Fable-review routing, P5/P6 hold, and the two live debts) + the
   **shipped-this-window** map (§2: ARCHITECTURE currency + RF-2 hub-arm + handoff-generator + sandbox
   Slice A) + run the rest of `PROBES.md` (P2–P9). Any probe FAIL blocks onboarding (the escalation ladder).

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
