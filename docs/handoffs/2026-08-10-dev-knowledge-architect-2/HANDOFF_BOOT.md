# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-10-dev-knowledge-architect-2` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-10-dev-knowledge-architect-2 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->**Adjudicate.** The ruling debt is still the only thing that moves the number, and it is untouched: `docs/audits/2026-08-09-technical-decision-sheet.md` §7 carries fifteen UNADJUDICATED items and ADR-111 §4 its OPERATOR-owed departure — both owed to this seat. **The overnight cloud lanes are no longer in flight**; ARC-5 archived them (manifest `737dd479` → merge `19aca464` → packet `fd464967`), so what was integration work is now *reading* work: three reports under `docs/audits/2026-08-10-technical-*`, plus this arc's own `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`. Two decisions are queued and are the operator's, not this seat's to assume: whether to absorb the six unmerged `claude/conformance-*` digests (a BROKEN step, named — it is a recurrence of open `[#419]`), and every lane's `## Needs a ruling` section. The strategic frame is unchanged: measured close capacity **3 per arc** against **170 open**, so "under 100" needs 71 closes ≈ 24 arcs — **births are the lever, not throughput**. Task state: `BACKLOG.md`, but read per-row status from `tasks/*.md` frontmatter, never from the generated file.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->The primary checkout on `main`, as the adjudication seat. It may record rulings in `protocols/STANDING_RULINGS.md`, ratify or amend ADRs (ADR-111 first), write intake status and `decided-by` fields, and birth or re-peg BACKLOG rows through `tasks/`. **The batch manifest the overnight lanes needed is already authored and already closed by its packet** — ARC-5 did that, so this seat inherits no open batch and no unmerged lane branch. Any conformance-digest absorption it chooses to run is a fresh operator-authorized act, not a carried obligation. It does NOT author inside a lane's branch, does not edit any immutable class in place (ADRs beyond a status line, transcripts, handoffs, audits), and does not push into a live consumer checkout.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect: the next session rules, it does not advance a named row. Its output is adjudications — fifteen carried §7 items, ADR-111's §4 departure from the ARC-2 clause on ADR-98 §3 grounds, and the `[#511]` fork about the SHAPE of the handoff load rather than its seconds — plus the birth decisions those rulings unblock. ARC-4 is the evidence for choosing this mode over execution: it ran four kill proposals to completion and closed nothing, because all four rested on premises no one had checked. The bottleneck is adjudication quality, not throughput. Mode follows HANDOFF_PROCESS §13 ("define-or-reshape-the-way-of-working → architect"), and the seat boots opus per the amended Ch8 routing matrix.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/arc5-night-batch-archive`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The `Destination` row is declared ex-ante — a lane inherits none of it from a prior prompt.**
> Only its **branch** field has a mechanical counterpart: `PROBES.md` **P3** compares it against
> live `git branch --show-current`, and a mismatch is a FAIL. Worktree, write-scope and MODE-basis
> stay **prose** and deliberately carry no probe leg — a leg with no mechanical counterpart cannot
> fail honestly, and one that cannot fail honestly discredits the whole block (R3).

> **Anti-bluff in effect.** The contract, what the withholding buys, and where generation-time
> hints go instead are stated **once** in this bundle's own `PROBES.md` header (spec:
> `HANDOFF_PROCESS.md` §5) — one hop inside the same paste, rather than a second copy free to
> disagree with the first.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

> **Dispatch prep is not copied here either.** A seat taking the architect role finds how a dispatch
> prompt is made, how model + effort are routed, how a batch runs, and how completion is managed at
> **`protocols/PLAYBOOK.md` Ch8 "Handoff prep for the next architect"** — itself an index of pointers,
> so this is one hop to the index and one more to each home. Standing rulings applied without asking:
> `protocols/STANDING_RULINGS.md`. Same pointer-not-copy rule as the runbook above.

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

## Operator-facing forms (resident by design)

The three sections above hand doctrine to a **pointer**, because doctrine is read once and lives
in the repo. **Forms are the other case: they are typed, not read**, and a form a seat has to go
fetch is a form the seat composes from memory instead. So the four commands an operator or an
incoming seat actually types are resident here — in the bundle, in the paste — rather than one hop
away. Rationale and mechanics for each stay at the homes named beside it; only the *form* is copied.

**1 — Dispatch a contract.** The whole surface is one typed line, run from the repo:

```
dispatch <CONTRACT-FILE>.md
```

The contract's own `## Dispatch` block carries the line; the helper runs it verbatim, resolving the
literal `$env:CLAUDE_PROMPTS_DIR` token and a bare filename against the prompts directory
(`$env:CLAUDE_PROMPTS_DIR`, else `~/Downloads`). Add `-DryRun` to print the resolved line and stop.
Home: `protocols/PLAYBOOK.md` Ch8 "The dispatch surface is `dispatch <file>`";
`templates/prompt-template.md` is the block's point-of-use form.

**2 — Take a lane into its own tree.** Either form provisions the isolated checkout:

```
claude --worktree <name>          # a fresh session, in a new worktree
```

or, from inside a running session, the native `EnterWorktree` tool — which also restores cwd on the
way out, the step the raw path leaves to you. `/lane-boot <letter> <id> <slug> <contract-path>` wraps
this for a batch lane and seeds the tree. Home: `protocols/PLAYBOOK.md` Ch8 "Parallel sessions &
worktree discipline".

**3 — Integrate a batch.** From the **primary checkout, on `main`** — not from inside a worktree:

```
/lane-integrate
```

It walks the merge queue serially, then runs the five-item refuse-to-finish checklist. Home:
`protocols/PLAYBOOK.md` Ch8 "The batch protocol — ONE plan → N lanes → ONE integrator";
`.claude/commands/lane-integrate.md` is the mechanical close-out.

**4 — Tear a worktree down. Four steps, and the fourth is the one that gets forgotten:**

```
git -C <repo> worktree remove .claude/worktrees/<name>    # --force if seeds make it dirty
git -C <repo> worktree prune                              # recovery path for an interrupted remove
git -C <repo> branch -d worktree-<name>                   # the PROVISIONING branch
git -C <repo> branch -d <work-branch>                     # the WORK branch
```

Teardown covers **two** branches, not one — the work branch is the one you were thinking about, so
the `worktree-<name>` provisioning branch is the half that survives. `cd` out of the worktree first;
your own shell locks the directory otherwise. Then verify, because `git worktree remove` no-ops
silently when the directory is busy: `git worktree list` shows only the primary, the
`.claude/worktrees/<name>` directory is gone, `git status` is clean. Home: `CLAUDE.md` §5 rule 9
(no leftovers), `.claude/rules/git-discipline.md` "WORKTREE TEARDOWN IS TWO BRANCHES, NOT ONE",
`protocols/PLAYBOOK.md` Ch8 §4.

## Why a pointer, not a copy

The methodology, the browser role, and the operator runbook all live in the repo and are referenced by
**pointer**; CC (which holds the repo) serves any part the file-less browser needs just-in-time.
**The forms section directly above is the declared exception, not a lapse:** a pointer works for prose
a seat reads once, and fails for a command a seat types — which is why each form above still points at
its doctrine home while carrying the line itself.
`PASTE_THIS.md` is the assembled boot source (generated by `scripts/assemble_paste.py`, never hand-edited);
`docs/handoffs/README.md` is the operator runbook. If a pointer and its source disagree, the source wins —
fix the pointer or regenerate `PASTE_THIS.md`.
