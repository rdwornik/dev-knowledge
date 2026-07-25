# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-25-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. Every probe runs in the **target** root — see the run-in-root table at the top of `PROBES.md`. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-25-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**The checker got built — and it shipped with a hole its own green test suite structurally could not see. Rule that class, then shape the arc.** The last window's biggest gap (no automated doc-vs-reality organ) is now partly closed: a read-only, non-blocking claim-vs-reality checker landed, alongside the allowed-edge-set ruling (recorded as **TARGET**, re-derivation triggered by the refactor ticket) and the largest filing batch in the recent record. But its rule registry is **incomplete and undisclosed** (**P11**), for the second instance of one recurring shape — a validator checked against its own artifact. Rule the standalone repair, rule whether that shape gets a durable home, then rule the checker's gate posture and the zero-findings follow-up whose target moves on its own (**P12**). **Keep the blind-scoring lane unblocked and out of the ordering — it is operator-only and shares no surface with any of this.** Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; the grooming log's 2026-07-25 entries are this window's ruling record — read them before re-deciding anything.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-25-ai-council`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **Anti-bluff in effect (read `PROBES.md` header).** This bundle **withholds every probe answer
> value** by construction — no counts, SHAs, dates, verdicts, or orienting lines. The withholding IS
> the teeth; run the commands. Generation-time drift hints live in the JOURNAL generation-entry, which
> the browser never sees — never in this bundle.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

## What the operator does (paste-pointer)

1. Open a fresh Claude.ai chat.
2. Paste **`PASTE_THIS.md`** (in this bundle directory) — the browser role file + residual + probes (+ the
   supplement ANSWERS **only if filled**), assembled in order by `scripts/assemble_paste.py`. One paste;
   never hand-feed individual files to the file-less browser.
3. The browser replies with its on-load acknowledgment line (it names the Layer-1 actor); a partial or
   missing paste is then visible.
4. **architect mode** — the browser adopts the mode posture from `protocols/HANDOFF_BOOT.md` (§"architect
   mode"): orient first, ask the operator for off-repo context, drive decomposition, hold the whole-system view, surface design tensions — not the reactive-filter default.
5. **Orient before any mechanism** — hand the browser `PROBES.md` **P1** (orientation) first; it replies
   `run <command>`, CC reads live `VISION.md` / `ARCHITECTURE.md` Ch1 and substring-checks. The architect
   may not begin design until it holds both orienting lines (P1's grep is a *tool* that confirms the frame
   — the **backlog navigates**, §13c).
6. **Then the operator-context beat (§13d).** The supplement is **FILLED**; its ANSWERS are in the paste, so the beat **NARROWS** to *"anything changed since the supplement was written?"*.
7. Hand `RESIDUAL.md` — **drift-flags first** (the §1 headline) — then the **next-frontier decisions**
   (§4) + the **shipped-this-window** map (§2), then run the rest of `PROBES.md` (**P2–P16** — this
   cross-repo set is re-bound to `ai-council` surfaces and larger than the generator's default). Any
   probe FAIL blocks onboarding (the escalation ladder). **Re-derive the drift-flag values live
   (P7/P4/P9/P11/P12) — the bundle states none.** Three are order-sensitive: **P11 before any checker
   build work**, **P12 before touching the zero-findings follow-up**, **P14 before any allowed-set or
   codemap edit**.

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
