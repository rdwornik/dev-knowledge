---
paths: "**/*"
---
## Git Discipline for .dev-knowledge

This is a git-tracked knowledge base. Every edit must be committed.

### Rules
- After editing ANY file: stage and commit immediately
- Commit message format: `docs: [what changed]` for living files, `lessons: [topic]` for LESSONS.md appends
- NEVER leave uncommitted changes at end of session
- verify: run `git status` — must show clean working tree before session ends

### MERGE IS ATOMIC (standing operator rule, established after three repeats)

> **MERGE IS ATOMIC:** merge `--no-ff` + push + delete the source branch are ONE
> operation. A branch merged into main and pushed is deleted in the same step, without
> separate operator authorization. Exceptions exist only by EXPLICIT PROTECTION
> (currently `claude/conformance-*`); silence is not protection. A merged branch left
> alive is a defect, not a pending decision.

Do not ask whether to delete a branch you just merged and pushed — deleting it is part of
the merge you were already authorized to perform. `--merged` still gets verified first and
nothing is ever force-deleted; the rule removes the *authorization* round-trip, not the
safety check.

**`automation/*` is EXPLICITLY PROTECTED** (operator ruling 2026-08-10, seat-27 checklist
3c-3; register `.dev-knowledge/protocols/STANDING_RULINGS.md` I-D). It joins
`claude/conformance-*` on the protection list. Reason: an `automation/<slug>` lane is an
organ-produced replication branch (the fourth machine-produced lane prefix, B5) whose
*whole purpose* is to live outside `main` — `automation/fleet-audit` is the live instance,
and `audit.py::check_fleet_audit_replication` asserts it stays replicated to origin. It is
therefore never "a merged branch left alive", and deleting it breaks the organ rather than
tidying after it.

**`claude/conformance-*` protection is scoped to the UNABSORBED** (operator ruling
2026-08-10, Fork 3; register `.dev-knowledge/protocols/STANDING_RULINGS.md` I-F3). A digest
branch is protected **until it is absorbed**, and an **absorbed** branch deletes at its own
merge under MERGE IS ATOMIC — no separate authorization, no per-instance
`operator-authorized` subject line.

Why the narrowing was needed, recorded so it is not re-litigated: the protection existed
because *nothing absorbed*, so the branches were the only copy. Once absorb is an act the
repo performs, "keep it after absorbing" preserves nothing and merely converts an
unmerged-and-kept branch into a merged-and-kept one — reinstating the ~319–365 branches/yr
accumulation the ruling exists to end. The pre-absorb guarantee is untouched: an unabsorbed
digest is still never deleted. **The two protected globs now have opposite lifecycles on
purpose** — `automation/*` is protected permanently (it lives outside `main` by design),
`claude/conformance-*` only until absorbed.

- verify: `git branch --merged main` lists nothing but `main`, `automation/*`, and any
  `claude/conformance-*` not yet absorbed.

### THE HANDOFF MERGE IS ATOMIC WITH TEARDOWN (operator ruling 2026-08-28, B1)

MERGE IS ATOMIC above governs *which* branches delete at their merge. This leg states *where*
the deletion has to reach and *what proves it is safe*, because the 2026-08-28 handoff merge
satisfied MERGE IS ATOMIC's intent and still left a branch alive in two places.

**Both places, or the merge is unfinished.** A merged handoff branch is deleted **locally AND on
origin** in the same act as the merge and push. A local-only delete is not a completed teardown —
it is the same defect at half the radius, and it is the half that survives review because
`git branch` looks clean. `docs/handoff-2026-08-28` is the witness: alive locally and on origin
after its merge, with the seat asking whether to delete rather than deleting.

**The ancestor proof is the safety check, and it is what makes the round-trip removable.**
`git merge-base --is-ancestor <branch> main` exiting 0 is the evidence the branch is contained.
Exit non-zero: stop, report, delete nothing. `-d` is the deletion verb and is never escalated to
`-D` under this rule — the rule removes the *authorization* round-trip, not the safety check.

The mechanism lives in `.claude/commands/handoff.md`, section *"The merge step — ATOMIC WITH
TEARDOWN"*, as an ordered command block rather than a sentence: an instruction is a request, a
mechanism is a guarantee. Explicit protection still outranks it (`automation/*` permanently,
`claude/conformance-*` until absorbed).

- verify: after a handoff merge, `git branch --merged main` lists no handoff branch AND
  `git ls-remote --heads origin <branch>` returns empty.

### WORKTREE TEARDOWN IS TWO BRANCHES, NOT ONE

Teardown = `git worktree remove` + `git worktree prune` + delete the **work** branch **AND** the
`worktree-<name>` **provisioning** branch. A leftover provisioning branch is a defect, not a
pending decision — it is the half of teardown that gets forgotten because the work branch is the
one you were thinking about. Deletion is still gated on operator word wherever the branch is
explicitly protected; the rule fixes *what teardown covers*, not who authorizes it.

- verify: after any teardown, `git worktree list` shows no stale entry AND `git branch -a` lists
  no `worktree-*` branch for the removed tree.

**Scope refinement (2026-09-19): the rule above covers a MERGED lane only.** As first written it
was too narrow — it assumed every removed worktree's branch was merged. A branch KEPT, unmerged,
as the only carrier of unfinished work is a different case: removing its worktree removes a
checkout, and deleting its branch would delete the work. A carrier branch is exempt from the
branch-deletion leg only while it is listed below, pushed to origin, with an expiry and a named
close condition. When the close condition fires, the branch is merged or abandoned by ruling, and
this rule then applies to it normally. At the expiry the entry is dead: the branch is flagged
again with no edit required, and keeping it longer needs a new dated entry.

| carrier branch | tip | closes when | expires |
|---|---|---|---|
| `worktree-wave2-dispatch` (L3) | `c00f9c10` | the caller-side dispatch shim lands (BUILD-LIST Decision 2026-09-19, dispatch) | 2026-11-18 |

- verify: every `worktree-*` branch with no registered worktree is either merged and deleted,
  or listed in the carrier table above, before its expiry, with `git ls-remote --heads origin
  <branch>` non-empty.

### Commit message examples
- `docs: update PLAYBOOK S5 council debate format`
- `docs: update ENVIRONMENT with new skills architecture`
- `lessons: append 4 entries from universalization session`
- `docs: remove JOURNAL.md, update file references`
