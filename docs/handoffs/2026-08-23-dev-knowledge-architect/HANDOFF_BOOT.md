# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-23-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-23-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Close the model-acceptance question this window opened and could not finish. `[E7] Tooling & evaluation` is the authority: the guarded A/B ran, both candidates were REFUSED on the G1 floor, and the verdict earned exactly ONE mitigated rerun whose instrument is now itself in question. The session's job is to rule the two open dispositions that gate everything downstream — intake 41 (does a scored item depend on the guard's refusal surface, and is that fixed in the item set or the guard?) and `[#171]` leg 1 (implement the ADR-80 writer policy, or rule that human-committed satisfies "committed" and amend ADR-86) — then decide what the rerun slot is spent on. Task-state: `BACKLOG.md`, `[E7]`, rows `[#578]` / `[#171]` / `[#492]`.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->the two rulings' carriers and nothing else — `docs/intake/2026-08-23-tech-nopack-guard-refusal-surface.md` (status transition), `tasks/` + the regenerated `BACKLOG.md`, and an ADR only if a disposition meets ADR-98 §3's fork test. NOT `scripts/nopack_sandbox.py`: changing the instrument is what the intake exists to rule on first<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect per ADR-87 item 5 — both open items are dispositions a reasonable person could decide either way (the (a)/(b) on `[#171]`; item-set-vs-guard on intake 41), so the work is pricing and ruling, not executing. An execution bundle would carry a lane that has nothing lawful to build until these are ruled<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-08-23-architect`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

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

## Amendments

> **AMENDMENT A1 (operator, 2026-08-23).** The Destination write-scope is widened for the
> mandate batch. This lane and its children may write: `ecosystem/provider-registry.yaml`
> and provider-consuming seams; `scripts/` (new check modules, `gen_dashboard.py`, the
> status-grammar validator) and their tests; `docs/adr/` for the rulings named in the
> batch; `docs/intake/` status transitions; `docs/audits/` lane artifacts;
> `CLAUDE.md` / `protocols/` / essentials for the claim-truth sweep; `tasks/` and the
> regenerated `BACKLOG.md`. `scripts/nopack_sandbox.py` remains OUT of scope — intake 41
> rules on the instrument before the instrument is touched. Any path not derivable from a
> quoted governance source is PROPOSED, never created.
