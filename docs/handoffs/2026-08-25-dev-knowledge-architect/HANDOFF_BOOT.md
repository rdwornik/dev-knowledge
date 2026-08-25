# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-25-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-25-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Open **wave 1** against the batch ruling landed 2026-08-25 — `protocols/STANDING_RULINGS.md` **section U**, pointing at `docs/audits/2026-08-25-technical-register-ruling-packet.md` as the binding adjudication of all 37 candidate rows. The window that just closed landed the ruling and deliberately birthed **zero** rows, so this session's first act is the governance call in RESIDUAL **F1**: how ten ruled ADOPT arcs become rows without bypassing the ADR-111 funnel — decide that before filing anything. Serves **`[E4]` Decision management** (the ADR/intake funnel this question sits inside) and the ACCEPTED intake **`docs/intake/2026-08-05-func-simplification-distribution-wave.md`**, under which **ARC-G** (the doc diet) executes per the operator's documentation-splits-by-audience direction. Navigate from `BACKLOG.md` — themes `[E4]`, `[E5]` and `[E7]` carry the affected rows, and `[#549]`/`[#424]`/`[#359]` are the re-pegged items **F6** asks you to actually rule.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)` — this seat boots on the primary checkout<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->planning-surface writes only — `docs/intake/`, `docs/decisions/` (ADR drafts), `tasks/` + `gen_task_tree.py` regeneration if and only if **F1** is ruled in favour of direct births, and `JOURNAL.md` at wrap. **Never** hand-edit `BACKLOG.md` (generated since the ADR-107 §7.2 flip). **Never** edit a hub-single-sourced `CLAUDE.md` region without the lockstep `templates/claude-regions/*.md` act (**F2**). Immutable per CLAUDE.md §5: the landed 2026-08-25 audit artifacts and section U<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the next act **defines the way of working rather than advancing a named ticket** — it rules how a landed adjudication enters the backlog at all (**F1**), scopes the doc diet against a fleet-parity constraint (**F2**), and takes a supersede-plus-amend ADR decision (**F3**). Per ADR-108 §A these are **technical** questions the architect rules (revertable), not operator escalations; the operator-gated acts here are the push and the ARC-D substrate/cost fork (**F5**)<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-08-25-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

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
6. **Then the operator-context beat (§13d).** The supplement is **generated EMPTY**, so unless the operator fills it first the beat fires **FULL**: *"what off-repo context — intent, priorities, findings not in the repo, changed decisions?"*
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
