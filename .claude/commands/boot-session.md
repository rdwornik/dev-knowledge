---
name: boot-session
description: Assemble the v7 BOOT-INVERSION paste — OPERATOR ASKS first, then FUNNEL HEALTH, north-star arcs, the rot/orphan list, open browser asks, PROPOSED NEXT BATCH, and one hand-written RESIDUAL — from live state, in one pass.
---

# /boot-session — the generated-from-live-state boot (v7 BOOT-INVERSION)

**Source of truth:** `protocols/HANDOFF_PROCESS.md` §17. This file is a dispatch summary, not
a substitute — where they disagree, the spec wins.

**This command NARRATES; it does NOT compute.** Every number below comes from a command
this file names — `scripts/funnel_lifecycle.py`, `scripts/boot_frontier.py`,
`scripts/fleet_health.py`, `BACKLOG.md`/`tasks/` — never from memory, and never re-derived by
prose. If a step's command fails or is unavailable, report that fact in its section rather than
guessing a number.

Emit **one** fenced block for the operator to paste — the fence is not decoration: bare
markdown tables paint as box-drawing glyphs at ~3× the token cost in browser chat (§ "Output
formatting" convention, `CLAUDE.md`).

## 1. OPERATOR ASKS — render FIRST, above everything

Read `protocols/HANDOFF_PROCESS.md` §17.1's registry (the fenced block under the bolded
**Seed entries** line). For each row: `asked`, `visible-fix` or `blocker`, `owner`, `re-asked`.
Apply the rule verbatim: **`re-asked >= 2` with no visible-fix AND no named blocker renders
RED**, as a status, never as prose. *"Tracked in `[#N]`"* alone does not discharge it.

Cross-check the live digest line rather than re-deriving the verdict by eye:

```
uv run --locked python -c "import sys; sys.path.insert(0,'scripts'); import fleet_health as fh; print(fh.operator_asks_line(open('protocols/HANDOFF_PROCESS.md', encoding='utf-8').read()))"
```

Render every row as a table; a RED row is marked `RED`, not merely listed.

## 2. FUNNEL HEALTH

Print the live one-line digest (the same line SessionStart already surfaces, extended, never
duplicated — `scripts/fleet_health.py` §17.2b):

```
uv run --locked python scripts/fleet_health.py
```

Quote its `[fleet]`, `[load]`, `[asks]` and `[funnel]` lines verbatim.

## 3. North-star arcs, with priorities

Read `BACKLOG.md`'s `[E#]` theme headings live, and count each theme's open rows by
`[P1..P3]` band. This is a plain read over the committed source — no new tool. One row per
theme: `[E#] <name> — N open (P1 x / P2 y / P3 z)`.

## 4. The rot/orphan list

`scripts/funnel_lifecycle.py` is READ ONLY (never written — this lane's write-scope note; it
already exposes `measure()`/`findings()`, and this section quotes them rather than re-detecting
anything):

```
uv run --locked python scripts/funnel_lifecycle.py --report
```

List every FAIL/WARN finding verbatim. rot = legs a1/a2/b (terminal objects not archived);
orphan = leg c (row provenance unresolved) — `scripts/fleet_health.py::funnel_health_line`
already computes these two counts; quote its `[funnel]` line from step 2 rather than
re-counting by hand.

## 5. Open asks for the browser

Pull forward every OPERATOR ASKS row from step 1 that carries **no** `visible-fix` — the
browser (Layer 1, no file access) needs to see what is still outstanding without re-reading the
whole registry. A row already GREEN (visible-fix present) is omitted here; it stays in step 1.

## 6. PROPOSED NEXT BATCH

Run the frontier/scoring/batch library — this is the hard, tested part, never composed by hand.
Scoring + batch selection is the DEFAULT action (no flag needed — `--frontier` switches to the
raw unscored list instead, which this step does not want):

```
uv run --locked python scripts/boot_frontier.py
```

Render its output verbatim, including the `held back (serialize-group disjointness)` and
`more unblocked work exists beyond the ledger bound` lines when present. **State explicitly,
every time:** this is a PROPOSAL, never a dispatch. AUT-R1's self-planning axis (Phase 4):
*"adjudication stays a human act... nothing merges unattended."* Nothing in this command, or in
`boot_frontier.py`, dispatches a lane — the batch requires an explicit operator **GO** before
any `dispatch <contract-path>` line is composed (`.claude/commands/lane-boot.md` §2).

## 7. RESIDUAL — the one hand-written section

Everything above is generated. This is the exception: **ONE small paragraph** carrying the
judgment a generator cannot have — rejections, tensions, and why. Write it fresh each run; do
not copy a prior session's RESIDUAL forward (the same discipline HANDOFF_PROCESS §2 already
states for the CC-authored residual: re-narration drifts from its source).

## Emit

Prepend the ROLE PIN (the same mechanism §4 uses, extended — no separate refusal path):

```
uv run --locked python scripts/assemble_paste.py --pin-only
```

Then the seven sections above, each under its own `=== SECTION ===` header (the `assemble_paste`
convention), and a terminal sentinel line `=== END OF PASTE — N sections · B bytes ===` — `N`
counts sections actually rendered (RESIDUAL is one; a step reporting "unavailable" is still a
rendered section, not a dropped one), `B` measures the body before the sentinel.

**The naming convention is filed, not applied.** `boot-session` / `boot-lane` / `boot-batch` is
a coherent prefix-first pattern this command participates in without being ruled on it. It is
filed as an **ADR-111 CANDIDATE** to the commands+skills census — not a row birth, and
`/lane-boot` is **not** renamed by this filing (`protocols/HANDOFF_PROCESS.md` §17.3). This
lane's write-scope carries no census document, so state the candidate text in the end-of-lane
artifact for the integrator to carry forward, rather than filing it here.
