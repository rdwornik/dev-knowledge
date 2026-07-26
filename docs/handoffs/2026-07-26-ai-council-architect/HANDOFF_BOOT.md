# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-26-ai-council-architect` |
| **Target repo** | `ai-council` — **CROSS-REPO** (ADR-36/41). The bundle is hosted in the `.dev-knowledge` hub; the **subject** is `ai-council`. Every `#id`, path, and `BACKLOG.md` reference is **ai-council's** unless marked hub. Every probe runs in the **target** root — see the run-in-root table at the top of `PROBES.md`. |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-26-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**A great deal landed, and all three mission axes moved zero. Break that pattern, then rule the class of defect that made the green lights untrustworthy.** Everything shipped this window was record and quality-control scaffolding — worth having, but the standing axes (CLI parity, now in its **seventh** un-run window; the boost/protocol Contract-Version arc; non-cognitive debate) are exactly where they were. Two of the three are gated on **decisions, not work** — an operator sit-down and an ADR-11 interactivity ruling that resolves its dependent in **either** direction. Meanwhile the window surfaced one recurring defect **five times**, twice inside the checker built to catch it: **a green published without the predicate that produced it** — a rule reporting pass while reading a fraction of the surfaces it claims (**P11**), and validators whose exit zero is silence rather than a verdict (**P7**). The instance repairs are filed; **whether that class gets a durable home is the open design question**. Spec: `ai-council/BACKLOG.md`, themes `[E1]`–`[E7]`; read the grooming log's 2026-07-26 entries before re-deciding anything. **The supplement is EMPTY — run the §13(d) operator-context beat in FULL before accepting the residual's ordering.**<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-07-26-ai-council`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

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
6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless the operator fills it first the beat fires **FULL**: *"what off-repo context — intent, priorities, findings not in the repo, changed decisions?"*
7. Hand `RESIDUAL.md` — **drift-flags first** (the §1 headline) — then the **next-frontier decisions**
   (§4) + the **shipped-this-window** map (§2), then run the rest of `PROBES.md` (P2–P10). Any probe FAIL
   blocks onboarding (the escalation ladder). **Re-derive the drift-flag values live (P4/P6/P7/P9) — the
   bundle states none.**

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
