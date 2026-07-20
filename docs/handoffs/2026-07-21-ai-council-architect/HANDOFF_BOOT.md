# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-07-21-ai-council-architect` |
| **Chat title** | `[ai-council] Technical Architect — 2026-07-21-ai-council-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Target repo** | **`ai-council`** — CROSS-REPO handoff (ADR-36/41). The bundle lives in the `.dev-knowledge` hub; the **subject** is the sibling repo `ai-council`, and every probe binds to **its** files, resolved from **its** root. The hub is read-only w.r.t. the target. |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**CROSS-REPO — the target is `ai-council`, not the hub.** Rule on the design forks the 2026-07-20 window deliberately left open rather than patched: **`[#80]`/`[#81]`** (where `RESIDUAL.md` §4 item 1 shows the operator-ruled doctrine and `[#81]`'s own done-when **contradict each other**, so no implementation can close it as written), the **buy-vs-build** question the markdown-it-py spike deferred on one unanswered empirical premise, and the twice-deferred **Contract-Version 1.1** bundle (`[#34]` + `[#76]`). **Time-critical:** §1's headline flag is that the spike's *evidence* — the empirical basis for the first two rulings — is currently in an **unreachable git object awaiting `gc`**; `PROBES.md` **P11 re-derives whether it still exists and should be run EARLY**. Navigate from `ai-council/BACKLOG.md` (theme backbone `[E1]`–`[E7]`; `[E1]` carries most of the above) — and note **`RESIDUAL.md` §4 is the payload here, not §2**.<!-- FILL-IN:purpose END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/ai-council-architect-handoff-0721`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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
   (§4) + the **shipped-this-window** map (§2), then run the rest of `PROBES.md` (P2–P12). Any probe FAIL
   blocks onboarding (the escalation ladder). **Re-derive the drift-flag values live (P4/P6/P7/P9/P11/P12)
   — the bundle states none.**
8. **Run `PROBES.md` P11 EARLY — it is the only probe whose window can close on its own.** It re-derives
   whether the deleted spike branch's evidence still exists as an unreachable git object or has already
   been collected by `git gc`. Every other probe is answerable at any later time; this one is not, and
   §4's first two rulings rest on what it finds. **Every probe is read-only — do not mutate the target
   to rescue the object (ADR-36/41); surfacing it is this handoff's job, recovering it is the target
   session's call.**

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
