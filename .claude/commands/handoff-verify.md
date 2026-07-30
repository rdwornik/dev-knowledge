---
name: handoff-verify
description: Run the whole live probe gate for a handoff bundle in ONE pass and emit exactly ONE evidence block — the v6 one-round-trip boot (HANDOFF_PROCESS §5)
---

Run the **entire** live comprehension gate for a **v6** handoff bundle in one pass and emit
**exactly one evidence block** for the operator to paste. This is the CC side of the v6
one-round-trip boot: one command → one evidence block → one operator paste.

**Pre-v6 bundles are EXEMPT, not failed.** A bundle cut before the v6 cut carries no `Destination`
row and no P0 legs, and its probes were written for the per-probe ferry. Bundles are immutable and
are judged by the era they were cut in (`docs/handoffs/README.md`, "The run loop"). So when the
bundle predates v6, run it as a **legacy diagnostic**: report those rows as
`n/a — pre-v6 bundle, row not required` and say so in the RESULT line. Their absence is **never**
a FAIL and **never** blocks onboarding — that would block a deliberately exempt handoff. Detect
the era structurally, not by date: a bundle whose `HANDOFF_BOOT.md` has no `Destination` row and
whose `PROBES.md` has no `P0a` row is pre-v6.

**Source of truth:** `protocols/HANDOFF_PROCESS.md` §5 — "Who runs it — the one-round-trip
boot" carries both the transport contract and the teeth. (§2 is the residual; §13 covers mode
behaviour and the P0/Destination rows.)
This file is a dispatch summary, not a substitute. Where they disagree, the spec wins.

## Why this is a separate command (R1)

`/handoff` **generates**, and its output is **answer-free by construction**: the bundle ships
questions + source-locators + exact verification commands, and never an answer. `/handoff-verify`
**checks**, and its output is **answer-producing**: live command output, re-derived now.

Those are opposite contracts and they stay in opposite commands. A `--verify` flag on `/handoff`
would recouple the ferry and the proof in one surface — exactly the boundary the §5 anti-bluff
contract exists to protect. `/handoff` must never grow a verify flag, and `/boot` stays archived.

## What it replaces

Before v6, the browser answered `run <command>` for each probe and the operator ferried each
command and its output back, one round trip per probe. The proof boundary is unchanged — the
browser has no file access, so the teeth still bite at the **CC ↔ primary-source** boundary.
What changes is the **transport count**, never the proof threshold:

> force the receiver to open the primary source → **force CC to re-derive every load-bearing
> fact from the live primary source at check-time, and block onboarding on any mismatch.**

## Usage

```
/handoff-verify                          # the active bundle (newest by git add date)
/handoff-verify <bundle-dir>             # an explicit bundle
```

## Procedure

1. **Resolve the bundle.** Default to the ACTIVE bundle under `docs/handoffs/` — an uncommitted
   bundle (the one being generated now) outranks every tracked one; otherwise the newest by
   **git add date**, never slug order. Two uncommitted candidates is **ambiguous → STOP and ask**;
   never silently pick one. (Same selection rule as `audit.py::_select_active_bundle`.)
2. **Structural pre-check.** Run `python scripts/verify_handoff_probes.py <bundle-dir>`. This is
   resolve-only — it proves each row *binds* to live state; it does **not** execute the probes.
   A FAIL here means the manifest itself is broken: report it and stop, rather than running a
   gate whose rows are known-toothless.
3. **Run every row's command against live state, now.** Every row in the bundle's `PROBES.md` —
   P0a/P0b/P0c, P1a/P1b, and P2 onward — plus the orientation reads and any inherited claim the
   residual or a folded supplement asserts. Re-derive; never answer from the bundle, from a
   compaction summary, or from memory.
4. **Emit ONE evidence block** (below). One block, one table, one paste.

## The evidence block

Emit **one** fenced block. The fence is not decoration: the terminal paints bare markdown tables
with box-drawing glyphs that cost ~3× the tokens when copied into browser chat, so anything the
operator copies out is fenced and flat.

Every row reports: the probe id, its source locator, the check performed, **PASS/FAIL**, and the
live evidence the browser needs. Required rows, per HANDOFF_PROCESS §5:

| Required row | Live source / locator |
|---|---|
| Live check count | `ALL_CHECKS` in `scripts/audit.py` — count + last name |
| Exact-line quote | the named `PLAYBOOK` / `ESSENTIALS` / spec section |
| Live HEAD / tree | live git — check-time SHA and tree state |
| Ship-gate read-back | `audit.py ship-gate` ∩ `ecosystem/disposition-register.yaml` — GREEN/RED, dispositioned-WARN count, any `[stale]` line |
| Pointer round-trip | the live `PLAYBOOK` section a pointer names |
| Orientation: vision | `VISION.md` `## Vision` opening sentence, substring-checked |
| Orientation: architecture | `ARCHITECTURE.md` Ch1 opening line, substring-checked |
| Inherited claims | every inherited claim that asserts a **repo-verifiable fact** (count / sha / file state / "X landed"), verified CC-side. A supplement's *why* — intent, tensions, rejected options, off-repo context — has no live source by construction: it is advisory and is **never** failed for being unverifiable. |
| P0a / P0b / P0c | the standing-topic legs (epic-theme preambles + `gen_task_tree --check` currency; ACCEPTED intakes; Purpose-vs-authority). **v6 bundles only** — `n/a` on a pre-v6 bundle. |
| P3 destination | live `git branch --show-current` vs the boot header's `Destination` row branch field. **v6 bundles only** — `n/a` on a pre-v6 bundle. |

Shape:

````
```
HANDOFF-VERIFY — <bundle-slug> — <YYYY-MM-DD HH:MM>
id    | source locator            | check                        | verdict | live evidence
P0a   | BACKLOG.md [E#] preambles | quoted live + tree currency  | PASS    | <quote>; gen_task_tree --check ok
...
RESULT: <n> PASS / <n> FAIL / <n> degraded [/ <n> n/a pre-v6] — ONBOARDING <CLEARED|BLOCKED>
```
````

## Hard rules

- **Any FAIL blocks onboarding.** Route through the escalation ladder: re-read the named primary
  source → re-derive → abort if still unmet.
- **A missing required row is not a pass.** If a row could not be run, it is reported as such and
  the block says so; silence is never a pass. The ONE exception is the declared pre-v6 exemption
  above: a v6-only row is reported `n/a — pre-v6 bundle`, which is neither a pass nor a failure,
  and is stated in the RESULT line so the exemption is visible rather than assumed.
- **Degraded coverage is reported, never counted as a pass** — a tool absent from PATH, a git
  probe that errored, an anchor that moved. Degrade loudly.
- **One block.** No required row may be deferred to a second block or another ferry turn — the
  whole point is that the operator pastes once.
- **Answers live here, never in the bundle.** This command's output is check-time evidence. It is
  never written back into a browser-visible bundle file: a bundle that carries an answer is
  bluffable by construction, and `verify_handoff_probes.py` FAILs any row bearing an `expected:`
  value.
- **The block is CC's own work, not a relay.** Every value is one this session re-derived from
  the live source. Never transcribe a value from the residual, the supplement, or a prior block.
