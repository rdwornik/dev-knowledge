# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-01-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-01-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Open the window after the **[E9] Fleet Desired-State System (North Star)** epic's first build arc actually landed: [#382] is CLOSED and ADR-109 (*Fleet desired-state contract v1*) is Accepted on `main`, so the fleet now has a typed contract, a loader over the live registry sources, and a divergence report — where a week ago it had four hand-divergent registries and no single answer. The first job is to rule, not to build: **[#383] wave 1 carries the generalization discharge** ADR-109 §4 deliberately left open, and the further decisions queued in `RESIDUAL.md` §4 — the conformance branches were RESOLVED (merged + deleted) and `automation/fleet-audit` deep-reviewed in the 2026-07-31 night resolution, so the queue now leads with [#460]'s recorded recommendation and the wave-1 surface choice. Navigate from `BACKLOG.md` — themes `[E9] Fleet Desired-State System (North Star)` and `[E7] Tooling & evaluation` — not from this header.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` <!-- AMENDMENT 2026-07-31 (operator-authorized): this field read `docs/2026-08-01-handoff-skeleton` as generated — the bundle's own GENERATION branch, which the finalize merge deleted under MERGE IS ATOMIC. Corrected to `main` per HANDOFF_PROCESS §13(c″) (v6.0.1): the field is the BOOT DESTINATION — where the seat LANDS at boot, not where its work is committed — and `main` is legal for a primary-tree architect seat. The row's own write-scope prose already said this seat boots on `main`. Original value preserved here and in git history; no other bundle file altered by this amendment. Generator defect fixed in the same arc (gen_handoff `BOOT_DESTINATION` token, RED-first). --> · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->**read-anything / write-nothing until a branch exists.** This seat boots on `main` to orient and decide; per core-invariant #5 every change — including a one-line doc edit — branches first (`feat/ fix/ docs/ chore/`) and returns via `--no-ff`, with the operator as the serial gate. In-scope to *plan*: `BACKLOG.md`/`tasks/`, `docs/`, `protocols/`, `ecosystem/schema/` and the `scripts/desired_state_*` pair. Explicitly OUT of scope without a fresh operator ruling: `automation/fleet-audit` (report-only pending the [#460] ruling; the `claude/conformance-*` branches no longer exist — resolved 2026-07-31 night, `RESIDUAL.md` §4 item 1), and any `~/.claude/` global infra (core-invariant #6).<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->**architect** because every item at the front of the queue is a ruling, not a task-graph. [#383]'s wave-1 surface choice decides whether ADR-109's generality claim gets discharged cheaply or stays open indefinitely; [#460] is now a recorded recommendation whose acceptance (or amendment) *gates* the reconcile-loop work behind it — a ruling, not a build, either way. An execution seat would have to invent those decisions before it could act — the reactive-filter failure ADR-87 names.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/2026-08-01-handoff-skeleton`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The `Destination` row is declared ex-ante — a lane inherits none of it from a prior prompt.**
> Only its **branch** field has a mechanical counterpart: `PROBES.md` **P3** compares it against
> live `git branch --show-current`, and a mismatch is a FAIL. Worktree, write-scope and MODE-basis
> stay **prose** and deliberately carry no probe leg — a leg with no mechanical counterpart cannot
> fail honestly, and one that cannot fail honestly discredits the whole block (R3).

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
5. **Ask CC for `/handoff-verify`, then paste its ONE evidence block.** CC runs the *whole* gate —
   every `PROBES.md` row, the orientation reads, the inherited claims — against live state at
   check-time, and emits a single table. You paste it **once**. The browser reads the table; it does
   not dictate commands one at a time (HANDOFF_PROCESS §5, the v6 one-round-trip boot).
6. **Then the operator-context beat (§13d).** The supplement is **FILLED**; its ANSWERS are in the paste, so the beat **NARROWS** to *"anything changed since the supplement was written?"*.
7. Hand `RESIDUAL.md` — **drift-flags first** (the §1 headline) — then the **next-frontier decisions**
   (§4) + the **shipped-this-window** map (§2). The probe answers are already in the evidence block
   from step 5. **Any FAIL there blocks onboarding** (the escalation ladder); a missing required row
   is not a pass. **The bundle states no drift-flag value — the block carries them, re-derived live.**

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
