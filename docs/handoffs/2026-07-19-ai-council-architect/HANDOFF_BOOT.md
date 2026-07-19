# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-19-ai-council-architect` |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-19-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Target repo** | **`ai-council`** — cross-repo (ADR-36/41). This bundle is *hosted* in the hub and derived **READ-ONLY** from the ai-council checkout. **Run every `PROBES.md` command in ai-council, not the hub.** |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Shape the **fix-and-unblock** window that follows ai-council's just-closed verification-and-debt window. Four threads need an architect's call, not an executor's: the two P2 silent-failure defects (#69/#71 — shared-helper vs local patch), whether the silent-failure trio (#62/#63/#65, plus #35) is one uniform fail-loud output-routing contract rather than four S-sized patches, a decide/drop ruling on the two proposed guards (#67/#68), and how to sequence around **#27**, whose Phase-3 operator scoring is the single highest-leverage unblock in the repo and is gated on a human action. Navigate from ai-council **`BACKLOG.md`** (the seven-theme story-map); `RESIDUAL.md` §4 carries the tension in each thread.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/ai-council-architect-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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
   `run <command>`, CC reads live **ai-council** `VISION.md` / `ARCHITECTURE.md` Ch1 and substring-checks.
   The architect may not begin design until it holds both orienting lines (P1's grep is a *tool* that
   confirms the frame — the **backlog navigates**, §13c). **Then P4**, which anchors this window's ready
   slack (#69/#71) in the live story-map.
6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless the operator fills it first the beat fires **FULL**: *"what off-repo context — intent, priorities, findings not in the repo, changed decisions?"*
7. Hand `RESIDUAL.md` — **drift-flags first** (the §1 headline: the falsified date-gate premise, and that
   #44 closed on "or fixes filed" rather than clean) — then the **next-frontier decisions** (§4) + the
   **shipped-this-window** map (§2), then run the rest of `PROBES.md` (P2/P3/P5/P6/P7). Any probe FAIL
   blocks onboarding (the escalation ladder). **Re-derive every value live — the bundle states none;
   P6 (gate green) and P7 (whole-open-BACKLOG grooming) are the load-bearing ones.**

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
