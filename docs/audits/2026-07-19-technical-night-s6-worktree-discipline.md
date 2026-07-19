# Night-audit cycle-close — S6 worktree / parallel-session discipline

Night-audit cycle-close · Stream S6 · ADR-101 class `technical`; read-only

## 1. Current mechanism (incident ledger + existing organs)

**Incident ledger (witnessed, chronological, all "recovered non-destructively" — none prevented):**

- `LESSONS.md:167` (2026-06-01) — worktree-sprawl consolidation: one repo, 5 concurrent worktrees, an unmerged branch + orphan dirs + a stray file.
- `LESSONS.md:163` (2026-06-02) — no-leftovers cleanup: two empty orphan sibling dirs (`.dev-knowledge-cadence`, `.dev-knowledge-night-adr`) survived a silently-no-op'd `git worktree remove`. Led to `check_no_sibling_orphans` (below).
- `LESSONS.md:135` (2026-06-05) — "#81 pilot contamination": a parallel session committed onto the audit's own checked-out branch while 27 verifiers were reading the tree (single shared `.git/HEAD`).
- `LESSONS.md:114` (2026-06-07) — parallel-session HEAD/index collision: a second session's commit swept the first session's staged file into its own commit and stranded a closeout on the wrong branch.
- `LESSONS.md:110` (2026-06-10) — "worktree transmission gap": a documented worktree-mechanics section existed but didn't transmit the decision layer (when to parallelize) to a fresh session — existence ≠ codification.
- `LESSONS.md:66` (2026-06-19) — neither raw `git worktree add` nor native `claude --worktree` reliably seeds gitignored `ecosystem/*/state.yaml`; `audit-health` blocks post-hoc only, after the fact.
- `LESSONS.md:60` (2026-06-25) — "#184 session-close (shared-checkout race, n+1)": a "read-only" audit session still commits its report, so it raced a shared checkout exactly like any committing session — HEAD switched to `main` mid-audit, landing a report commit direct-on-`main`.
- `JOURNAL.md:162` (2026-07-17) — **Concurrent-session incident (recovered non-destructively)**: a parallel `ai-council-P6-handoff` session sharing the checkout switched branches out from under the active session (`docs/339` → `main` → its own branch → `--no-ff` merge, pushed), so the active session's reconciliation commit landed DIRECT on `main` (core-invariant #5 violation). Recovered via `checkout -B` + `branch -f` (no `reset --hard`).
- `JOURNAL.md:92` (2026-07-18) — "on a quiet primary the day after a concurrent session had briefly hijacked the shared checkout (fully recovered, no work lost)".
- `JOURNAL.md:54` + `JOURNAL.md:36/38` (2026-07-18) — **corp-E5 stray-bundle**: an untracked `docs/handoffs/2026-07-18-corp-monorepo-e5-registry-developer/` bundle "(NOT this session's, not mine) appeared in the tree mid-session; left untouched, flagged to operator", later committed verbatim on its own unmerged quarantine branch by explicit operator ruling (`3b6b3f18`).
- `JOURNAL.md:24/32` (2026-07-19) — the corp-E5 incident directly produced the filing of **#353** ("session-boot contract hardening") as Step 4 of the ARC-4 leg-1 close-out.

**Existing organs that touch this surface (all post-hoc detection or session-END checks — none prevents the incidents above):**

- `docs/decisions/ADR-61-git-worktree-parallel-sessions.md` — the DECISION (same-repo concurrency requires separate worktrees). Pure governance prose; carries no script/hook enforcement itself.
- `scripts/audit.py:827-874` `check_no_sibling_orphans` (registered in `ALL_CHECKS` at `scripts/audit.py:2194`, run via the `audit-health` pre-commit hook, `.pre-commit-config.yaml:109-117`) — flags an unregistered `<repo>-*` sibling dir that looks like a torn-down worktree remnant (empty, or a `.git` gitlink). Scope: orphan **directories** only. It does not detect HEAD movement, does not detect stray content appearing **inside** a live tree, and only runs at commit time (not at boot, not mid-session).
- `scripts/session_end_backpressure.py` (Stop-hook, wired in `.claude/settings.json`) — 1 HARD check (`check_journal_sha_anchor`) + 3 ADVISORY checks (`check_backlog_marker`, `check_dirty_tree` at L340-350, `check_canonical_freshness`). `check_dirty_tree` flags uncommitted changes at **Stop** but has zero notion of provenance — a stray externally-appeared bundle and the session's own edits look identical to it. All four checks fire only at session-END; none fires at boot or mid-session, and none is scoped to "is this a worktree, and does this order declare one."
- `scripts/hooks/block_immutable_edits.py` (PreToolUse, ADR-77) — the only PreToolUse **write**-guard resident in this repo. Proves the available shape (fail-closed inside a zone / fail-open outside, JSON stdin → `{"decision":"block"}` on stdout, `_ZONE_SEGMENT` substring match at L83) but its zone is `docs/decisions/transcripts/**` only — zero worktree/HEAD relevance.
- `~/.claude/hooks/block-onedrive.ps1` (cited via `core-invariants.md:16`) — the PreToolUse-guard precedent #344 Ask 2 explicitly wants copied ("the `block-onedrive` shape").
- `plugins/tier1-lifecycle/commands/ship.md:12-21` — `/ship`'s "refuse inside a linked worktree" check. This IS a concrete, named git-command detection (`git rev-parse --path-format=absolute --git-common-dir` vs `--git-dir`) — but it lives in a **command markdown file**, i.e. it is agent-instruction-level (the executing Claude reads and obeys it), not a PreToolUse/pre-commit/Stop **hook**. Nothing mechanically blocks a skipped or misread check.
- `.pre-commit-config.yaml` — zero hooks reference worktree state, live-HEAD safety, or stray-content provenance; `audit-health` (L109-117) is the closest, and it only carries `check_no_sibling_orphans`'s narrow orphan-dir scope.
- `~/.claude/rules/core-invariants.md` — rule #4 "git status must be clean before starting new tasks" (L41-45) has **no `verify:` line** and no mechanism (contrast rule #5 `--no-ff`, L47-52, which has both a `verify:` line AND a real prevent-hook, `scripts/block_ff_push.py`, wired pre-push).

## 2. Designed/intended shape (invariants that SHOULD hold)

1. Every concurrent same-repo session runs in its own worktree — ADR-61 Decision.
2. A session must never commit in a checkout it does not exclusively hold; "read-only parallel" means literally zero commits (`LESSONS.md:114`, `LESSONS.md:60`).
3. A hub session must **refuse** to act on a mid-session externally-authored order (injected work) unless it (a) names a worktree for its side effects, OR (b) the tree is clean — **#353**'s exact language, `BACKLOG.md:42`. Confirmed **OPEN** — no `closes`/DONE marker in the BACKLOG line, and the 2026-07-19 JOURNAL "Next (operator)" line (`JOURNAL.md:32`) lists only the merge-GO and consumer freshness debt, not a #353 build.
4. Session-close discipline (test-then-close) must travel via a boot/gate mechanism, never operator restatement — **#349**, `BACKLOG.md:41`, explicitly OPEN and explicitly overlapping #344 Ask 1 pending a scope ruling.
5. A consumer-side PreToolUse guard (the `block-onedrive` shape) should BLOCK Write/Edit/NotebookEdit resolving into a hub/global path (`.dev-knowledge/`, `~/.claude/`) from a consumer session — **#344 Ask 2**, `BACKLOG.md:23`, confirmed OPEN / NEEDS-RULING.
6. Worktree teardown must leave no orphan (PLAYBOOK G5 "no-leftovers") — mechanized ONLY for the empty/gitlink-remnant case (`check_no_sibling_orphans`); a torn-down worktree that leaves populated-but-unregistered content is not caught (`_looks_like_worktree_remnant`, `scripts/audit.py:791-824`, deliberately narrows to avoid false-positiving live sibling repos — a documented trade-off, not a bug).
7. `ecosystem/*/state.yaml` must be seeded per fresh worktree (`LESSONS.md:66`) — prose-only; the only downstream signal is `audit-health` failing generically ("repos registered (none)") after the fact.

## 3. Gap (invariants with NO mechanism)

| Invariant | Mechanism? | Evidence of absence |
|---|---|---|
| 1. worktree-per-concurrent-session | **NONE** | No SessionStart/PreToolUse organ checks "is another session live on this checkout" before a commit; enforcement is entirely LESSONS-entry-after-the-fact (5 recovery episodes 2026-06-05 → 2026-07-18) |
| 2. never commit in a non-exclusively-held tree | **NONE** | Same — git itself gives Claude no signal that a concurrent session is active; `check_dirty_tree` only fires at this session's own Stop, blind to a sibling session's activity |
| 3. #353 boot-contract refusal | **NONE — OPEN** | `BACKLOG.md:42`; no `refs` line points to a built script, only `scripts/session_end_backpressure.py` (a Stop-hook, wrong lifecycle phase — #353 needs boot/mid-session, not close) |
| 4. #349 close-discipline inheritance | **NONE — OPEN** | `BACKLOG.md:41`; explicitly unresolved vs #344 Ask 1 |
| 5. #344 Ask 2 consumer hub-write guard | **NONE — OPEN/NEEDS-RULING** | `BACKLOG.md:23`; operator-owed ruling, no script exists under any name matching "hub-write-guard" in `scripts/` or `scripts/hooks/` |
| 6. worktree teardown verified | **PARTIAL** | `check_no_sibling_orphans` covers only empty/gitlink remnants — a populated abandoned worktree dir is invisible to it by design |
| 7. state.yaml seeding | **NONE (indirect only)** | prose gotcha only; `audit-health` fails generically post-seed-miss, not a seeding gate itself |
| Stop-hook loop risk on a stray/foreign bundle | **Partially addressed, but not for this case** | The general Stop-hook block-cap loop defect WAS fixed (fire-once + structural floor, `scripts/session_end_backpressure.py:36-46`, JOURNAL 2026-06-16 `JOURNAL.md:3886`) — but that fix addresses the JOURNAL-anchor HARD-block loop generically; it has no special handling for "the unanchored commit/content is not this session's own work" (e.g. an accidentally-committed stray bundle would still demand a JOURNAL citation from the session that didn't create it) |
| /ship worktree-refusal | **Instruction-level, not hook-level** | `plugins/tier1-lifecycle/commands/ship.md:12-21` is agent-obeyed markdown, not a PreToolUse/pre-commit gate — nothing mechanically enforces it if the executing agent skips the pre-flight step |

## 4. Proposed MECHANISM

**(a) #353 — session-boot contract, two paired organs (mirrors the existing `/override` token precedent at `scripts/session_end_backpressure.py:120-122`):**
   - A **SessionStart** hook (new script, e.g. `scripts/session_boot_snapshot.py`, added to the `.claude/settings.json` SessionStart roster alongside `fleet_health.py`/`arm_hooks.py` per `CLAUDE.md` §9) writes a gitignored boot-state marker: `git status --porcelain` snapshot + `git worktree list` + timestamp, under `logs/.session-boot-state` (same directory convention as the override token).
   - A **PreToolUse** guard (new script under `scripts/hooks/`, same shape as `scripts/hooks/block_immutable_edits.py:138-188` — fail-open outside the trigger condition, fail-closed once triggered) that, on a mutating tool call, refuses when: the tree was dirty (or carried untracked paths) at boot per the snapshot, the target path was **not** present in that boot snapshot (i.e. new/foreign content), AND the session has not declared a worktree for this order. This directly operationalizes #353's own Done-when clause (`BACKLOG.md:42`).

**(b) #344 Ask 2 — consumer hub-write guard**, same file-shape as `scripts/hooks/block_immutable_edits.py` but inverted target: block `Edit`/`Write`/`NotebookEdit`/`MultiEdit` whose resolved `file_path` lands under `.dev-knowledge/` or `~/.claude/` when the session's own repo root is a consumer (not the hub) — modeled explicitly on `~/.claude/hooks/block-onedrive.ps1` per the BACKLOG text itself (`BACKLOG.md:23`) and per core-invariant #6's exception-with-ruling posture (`core-invariants.md:54-58`).

**(c) Concurrent-HEAD-movement advisory** (harder problem — git offers no cross-session lock Claude can rely on): a lightweight lockfile (`.claude/.session-lock`: pid + HEAD sha + timestamp, written at SessionStart, cleared at a clean Stop) checked by the same PreToolUse guard as (a) before any commit-shaped Bash/PowerShell call — if live HEAD no longer matches the lock's recorded HEAD, refuse/warn before the commit lands, rather than recovering non-destructively afterward as in the 2026-06-05/06-07/06-25/07-17/07-18 incidents.

**(d) #349 — fold into the existing Stop-hook's helpers rather than duplicate**: `session_end_backpressure.py` already has `_is_clean()`/`_session_shas()` (L128-172); reuse them in a **SessionStart**-side echo (surfaced via the same additionalContext channel already used by other SessionStart hooks, CLAUDE.md §9) so a fresh/resumed session is told the test-then-close contract at boot, not only refused at Stop.

## 5. BACKLOG seed

No id (this is build material for three already-filed tasks, not a new invariant).

kill-candidates: none — #353 (boot-time refusal), #344 Ask 2 (consumer hub-write guard), and #349 (close-time inheritance) are three distinct organs per their own BACKLOG text (`BACKLOG.md:42`, `BACKLOG.md:23`, `BACKLOG.md:41`); this seed proposes concrete build shapes for each, it does not merge or replace any of them.

Done when: (1) a SessionStart boot-snapshot + PreToolUse refusal organ exists and demonstrably blocks a seeded mid-session externally-authored order that touches a new/foreign path while the tree is dirty with no worktree declared (#353's own Done-when, `BACKLOG.md:42`), with a test; (2) a consumer-repo PreToolUse guard blocks a seeded Write/Edit/NotebookEdit resolving into `.dev-knowledge/` or `~/.claude/` from a consumer session, with a test (#344 Ask 2); (3) a fresh/resumed session demonstrably inherits the test-then-close discipline from a boot-injected mechanism with no operator reminder (#349's own Done-when) — OR each leg is instead recorded permanent-defer-with-reason.
