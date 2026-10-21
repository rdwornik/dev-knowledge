# BOOT-REFERENCE — relocated session-boot detail

> **On-demand reference, never a boot read.** Everything here was moved *verbatim* out of the always-loaded surfaces (`CLAUDE.md`, `.claude/rules/git-discipline.md`) by rows [#1616] / [#1618] (BATCH-TOKEN-CUTS-2026-10-16) because those surfaces are paid on every turn of every session (DIGEST-NIGHT-CLOSEOUT-2026-10-15 §5: ~25 k tokens). Each section names the line that points here. Sanctioned home: `.claude` (an admitted home in `ecosystem/fleet-shape-spec.yaml` `home_grammar`), linked from `CLAUDE.md` (`CLAUDE.md` §5 rule 5 navigation trigger: the boot file's measured per-turn cost).

## Conventions, §3, §4, §8 and header text moved out of CLAUDE.md

### Header blurb (budget / universal-rules note)

> **Session boot contract for Claude Code in this repo** — auto-read at session start (ADR-53, as re-pointed by ADR-115). **Genre:** a rule lives here only if a session needs it *before it can act*; rationale, history and per-organ detail live at the home each line cites.

### Conventions (section 4 bullets)

- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal, not enforced (ADR-27/ADR-48)
- **File lifecycle:** append-only `LESSONS.md` + `logs/TOKEN-LOG.md`; newest-first-prepend `JOURNAL.md`; immutable ADRs / transcripts / handoffs / audits; living `README.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md` — rules and exceptions at §5. **`BACKLOG.md` is generated:** edit `tasks/`, then `gen_task_tree.py --emit-source`
- **Freshness cadence:** the stamped set is **computed, not restated here** — `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`. A `last_reviewed` stamp means *re-read end-to-end and confirmed accurate, or drift filed*, never merely "touched"
- **TDD — a build-arc standard, not a blanket mandate.** ADR-108 §B binds every build arc: RED-first witnesses, failing tests before build code, frozen after freeze; the architect freezes the pass/fail criterion *before* it, and CC may strengthen but **never weaken** it (ADR-81 amend. 2026-06-24). A blanket mandate is **not** live — Council rejected "Mandatory TDD". Say partial when it is partial
- **Spec-driven development (ADR-108 §B)** — spec before build, acceptance contract ex-ante. Live: the `check-against-spec` skill, `coherence-nudge` over `_SPEC_REGISTRY`, the `reconciled_versions` check, this file's `reconciled_with:` stamp

### §9 Hooks active (roster, session hooks, rules)

## 9. Hooks active
<!-- scope: runtime -->
> **[REPO - local]** region `hooks-repo-roster` - this repo owns these lines.
<!-- methodology:start id=hooks-repo-roster owner=repo -->

> **A roster, not a manual.** Per-hook rationale, exit codes and **honest limits** live in each module's docstring under `scripts/`; **failure posture** in `ARCHITECTURE.md` Ch2 and its "Validators and enforcement" chapter; the full organ inventory in the generated `ecosystem/organ-index.md`. Read those, never a copy here.

<!-- Machine-read: validate_doc_claims.extract_claimed_hooks takes the leading backtick id of every bullet from this header to the first non-bullet line. Keep it complete and contiguous. -->

**Arm the two pre-push hooks once per clone:** `pre-commit install --hook-type pre-push` — `default_install_hook_types` wires them only on a fresh install; `SessionStart`'s `arm_hooks.py` then does it idempotently.

Session hooks (`.claude/settings.json`, `disableAllHooks: false`): **1 SessionStart**, `scripts/hooks/session_start.py` via the shared launcher ([#1001]): 9 readers in one interpreter (`arm_hooks`, `surface_triage`, `changelog_sentinel`, `conductor` session-start, `resource_lifecycle` session-start, `codespace_regime` session-start, `billing_leak_sentinel`, `fleet_health`, `quota_daily`), output byte-capped **+ 2 Stop** (`session_end_backpressure`, advisory; `lane_end_guard`). **PreToolUse** `scripts/hooks/scope_guard.py` IS wired, at `.claude/settings.json:89` (L2, every tool call). Separately, PreToolUse `[#727]` deny-and-point stays UNWIRED 2026-09-18 (B2 lane4 rule-8; script kept, see audit above). Off since 2026-09-17, expiry 2026-10-08 pending wave 5b ([#863]): the prompts guard, the ADR-77 transcript guard, `logs_retention.py`. `propose_closures` (plugin Stop) still runs, KNOWN-UNGOVERNABLE.

Rules (`.claude/rules/`): `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end.


### §2 Portable layer

- **Portable layer:** root `AGENTS.md` carries the build/test/landing facts every provider reads (ADR-115, superseding ADR-53 Decision 2); this file keeps the Claude-runtime remainder and imports it below. No fact is duplicated across the two — the importer preserves ADR-53's substance

### §3 Where to jump

- **Where to jump:** **Ch2** organ map — which organ fires when, and how it fails · **Ch3** automation axes — cloud/nightly Routine, spec-orchestration, model routing · **Ch4** distribution — carriers, child floor, browser bundle · **Ch6** verification mesh — the nightly outcome loop.

### §3 Daily working mode

- **The daily working mode is NOT in ARCHITECTURE.** Parallel worktree lanes, lane dispatch and the ADR-110 batch protocol are `protocols/PLAYBOOK.md` **Ch8 "Session boundaries"**.

### §4 Naming

- **Naming:** UPPERCASE for top-level living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated artifacts, `docs/audits/` names also carrying a closed-enum class (`validate_hermetization.AUDIT_CLASS_ENUM`); `logs/` artifacts UPPERCASE-KEBAB, extension honest to the format ([#395]); kebab-case otherwise

### §4 Decision funnel

- **Decision funnel (ADR-111):** every audit finding is triaged into **exactly one** of OWNED / DISCHARGED / CANDIDATE / REJECTED — no finding becomes a backlog row without triage, and the only path is CANDIDATE → intake (ADR-98) → ratification. Question routing is ADR-108 §A: the operator rules **functional** questions, the architect **technical** ones

### §8 user skills

User-level (`~/.claude/skills/`): `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls). `verify` is **not** user-level; the live copy is hub-local, below. `boot` / `session-summary` / `handoff` / `save` are **commands** (§7), not skills, however the picker surfaces them.

### §8 repo skills

Repo-level skills live in `.claude/skills/<name>/SKILL.md` — list that directory when a skill-shaped task arises; run `verify` after `pytest`. Repo-specific empirical patterns live in `LESSONS.md` — append-only; read it before structural changes. Plugin `tier1-lifecycle@dev-knowledge-methodology` is enabled (its `Stop` hook runs `propose_closures.py`; it ships `/review-closures` + `/ship`).

### §4 Out of scope

**Out of scope:** code-level implementation → child repos · runtime config → `~/.claude/`. The in-hub Council transcript archive was **deleted 2026-07-22** by operator ruling — do not recreate it; the ADR-77 guard is OFF since 2026-09-17 (expiry 2026-10-08, [#863]; §9).

## git-discipline.md — full text (the rule file now carries a summary plus every `verify:` line)

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
`claude/conformance-*` on the protection list. Reason: STANDING_RULINGS B5.

**`claude/conformance-*` protection is scoped to the UNABSORBED** (operator ruling
2026-08-10, Fork 3; register `.dev-knowledge/protocols/STANDING_RULINGS.md` I-F3). A digest
branch is protected **until it is absorbed**, and an **absorbed** branch deletes at its own
merge under MERGE IS ATOMIC — no separate authorization, no per-instance
`operator-authorized` subject line.

**The two protected globs have opposite lifecycles on purpose** — `automation/*` permanently,
`claude/conformance-*` until absorbed. Why: STANDING_RULINGS I-F3.

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
| `worktree-d0-rows` | `dbce4c89` + the D0 close commit | the operator ratifies the D0/D1 rows `[#1625]`-`[#1642]` and the integrator lands the branch | 2026-11-01 |

- verify: every `worktree-*` branch with no registered worktree is either merged and deleted,
  or listed in the carrier table above, before its expiry, with `git ls-remote --heads origin
  <branch>` non-empty.

### Commit message examples
- `docs: update PLAYBOOK S5 council debate format`
- `docs: update ENVIRONMENT with new skills architecture`
- `lessons: append 4 entries from universalization session`
- `docs: remove JOURNAL.md, update file references`

