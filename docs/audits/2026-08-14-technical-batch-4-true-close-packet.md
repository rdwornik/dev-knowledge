---
title: "Batch 4 — TRUE close packet (packet-close window-tail)"
date: 2026-08-14
class: technical
---

# Batch 4 — TRUE close packet

**What this is:** the corrected, current-state close report for batch 4, superseding the
counts in `docs/audits/2026-08-11-technical-batch-4-packet.md` (written against the
FLAG-1-uncorrected marker) with the ruled disposition (FLAG-1 / M-3 / `N1-FLAG-1`) plus one
further discharge that happened after that packet landed. Read-only reporting — no births,
no closes, no re-litigation of the M-3 ruling.

## 1. Closure state per FLAG-1 / M-3

Ruled 2026-08-12 (operator `OK` en bloc; register `protocols/STANDING_RULINGS.md` M-3 /
`N1-FLAG-1`): **the batch closes on the three that closed in-window, with the rest carried
recorded as carried** — rather than holding the batch open until all five of the closure
contract's named rows land.

- **CLOSED in the window (3):** `[#270]` · `[#132]` · `[#521]`.
- **CARRIED at batch close (3, per the FLAG-1 correction):** `[#514]` · `[#510]` · `[#513]`.

**Update as of this packet (2026-08-14, packet-close window-tail): `[#513]` is now
DISCHARGED.** Its closing commit `387b794a` (itself a product of the 2026-08-13 git-surgery
re-land, §3 below) is confirmed an ancestor of current main HEAD `62f42dad`
(`git merge-base --is-ancestor 387b794a HEAD` — true), landing before this window's own
`d581c60f`/`62f42dad` merges. `[#513]`'s own row carries the closing evidence.

**Corrected total, this packet:**
- **CLOSED (4):** `[#270]` · `[#132]` · `[#521]` · `[#513]` (sha `387b794a`).
- **CARRIED to the next window (2):** `[#514]` · `[#510]`.

Neither `[#514]` nor `[#510]` closes here — this packet reports state, it does not discharge
either row. Both remain open with their own rows as owners, per M-3's explicit terms.

## 2. CODEX-524 state

**Complete.** All four `[#524]` legs landed via the standing R5 fallback (Codex/terra
produces a text-only DESIGN against the four clauses quoted verbatim, CC implements the
code, terra reviews pre-merge) — `JOURNAL.md` 2026-08-14 (c). Provenance: Codex-specified
(zero files touched by Codex, confirmed via `git status` post-dispatch), CC-implemented
(`scripts/audit.py`, `scripts/validate_backlog.py`, `scripts/journal_anchor.py` + tests, all
CC commits). Landed at `789a86a5`, merged to main at `62f42dad`
(`worktree-lane-l-524-check-extensions`). Leg (d) required no code — `check_hooks_armed`
already discharged it.

## 3. W4 wave-1 conversion arithmetic

Four lanes, dispatched against the 2026-08-13 partition print (69 assigned ids total, the
census's ready P1/P2 conversion drafts applied verbatim-with-adaptation):

| Lane | Contract | Assigned | Converted | Skipped | Merge sha |
|---|---|---|---|---|---|
| h | W4a (group A) | 17 | 6 | 11 | `a4fc652d` |
| i | W4b (group B) | 18 | 13 | 5 | `8a091278` |
| j | W4c (group C) | 18 | 9 | 9 | `5eb1269f` |
| k | W4d (group D) | 16 | 11 | 5 | `781bd4ff` |
| **Total** | | **69** | **39** | **30** | |

Every skip carries a one-line reason in its lane's own JOURNAL entry (no census draft, or a
stale draft against the live row) — no skip is silent. Full W4 wave-1 roster + lane-l
(`[#524]`, §2 above) closed this window: h `a4fc652d`, i `8a091278`, j `5eb1269f`, k
`781bd4ff`, l `62f42dad`.

## 4. Git-surgery incident summary

**2026-08-13:** three commits landed direct-to-main (`e15c97f6` / `b0f5eda5` / `3d97d5c5`),
caught by `block-ff-push` at **push** time — after the commits already existed locally and
after local recovery required rewriting history rather than a simple prevention. Cleared via
a `commit-tree` git-surgery re-land, replacing the three with six: `387b794a` / `a4fc652d` /
`8a091278` / `5eb1269f` / `781bd4ff` / `7f5d2105`. Full incident detail:
`CONSOLIDATION-REPORT-2026-08-13.md` §1 (operator's Downloads, not repo-tracked).

**The gap this incident exposed — `block-ff-push` is real but late.** It fires at push,
after a bad commit already exists on `main` locally. A commit-time local hook closes the gap
before the commit exists to unwind. This packet's own step 3(c) files that gap as
`[#527]` — **Anti-direct-to-main mechanism — a commit-time local hook, not vigilance** (P2/S,
`tasks/527-anti-direct-to-main-mechanism.md`), citing this incident's six shas directly and
naming `[#153]` (server-side/push-time teeth) and `[#514]`/`[#510]` (ADR-110 exemption
grammar) as the neighboring rows that do not cover this scope.

## 5. Night-branch set for the next window

Five `claude/*` branches remain on `origin`, unexamined-not-clean, per the deferred
satellite-branch census (`N1-D24` / STANDING_RULINGS 3c-5: "DEFERRED with an owner, W-wave
scope — satellites are recorded as unexamined-not-clean"):

- `claude/nc-lessons-mechanisms-jw5dda`
- `claude/nd-governance-promotion-prune-77qc6b`
- `claude/night-nb-handoff-prep`
- `claude/night-ne-northstar-value`
- `claude/window-truth-audit-yr83j2`

**No merges performed here** — this packet reports the set so the next W-wave inherits an
accurate list rather than re-deriving it; disposition (absorb, prune, or carry again) is that
wave's own decision under `N1-D24`.

---

**Net for this packet:** 0 births, 0 closes performed by this act. It reports one row's
discharge that already happened in the tree (`[#513]`, evidenced elsewhere) and states the
current carried/closed split, the CODEX-524 landing, the W4 arithmetic, the git-surgery
mechanism gap's new owner (`[#527]`), and the next window's night-branch inheritance.
