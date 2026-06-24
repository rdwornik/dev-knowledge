---
last_reviewed: 2026-06-19
status: active
owner: Rob
---

# DEFINITION OF DONE — session-close obligations
<!-- scope: meta -->

> **Single source of truth** for what "done" means at session close (ADR-85). The rules
> here are enforced *mechanically and deterministically* by the session-end Stop-hook
> (`scripts/session_end_backpressure.py`) — no LLM in the gate. This doc is the canon;
> the hook is the teeth; the `/override` command is the only escape. Injected into the
> orchestrator at session-start via `protocols/HANDOFF_BOOT.md`.

The point is **not** box-ticking. It is that the repo's value is its discipline — every
change traceable, no fabricated state — and the human should no longer be the manual
trigger that remembers to keep the record current. Scope is deliberately tiny: only the
two docs that both rot worst *and* legitimately change every working session.

## Gated per session

### JOURNAL — gated, **hard block** (un-gameable)
<!-- rule: seal-journal-anchor -->
Any session that produces commits **must** add a `JOURNAL.md` entry, and that entry
**must reference ≥1 commit SHA produced this session**. The SHA anchor is what makes this
un-gameable: a generic "did some work" line does not pass; the entry has to name a real
commit from this session's work.

**"This session" = the session boundary, not the push boundary (ADR-85 amendment 2026-06-19, C1).**
The arc gated is the trailing run of commits **since the last JOURNAL-citing ("journal-wrap")
commit** — *not* the push arc `base..HEAD` (`base` = `@{upstream}` else `main`). The push arc
spans **multiple sessions** under deferred-serial-push, where one *prior* session's citation
would vaccinate the whole arc (the leg passes on `any(SHA cited)`) and let a later un-journaled
session ride free — the C1 miss the amendment fixed. The boundary is found by walking
`base..HEAD` newest→oldest and stopping at the first commit that **wrote** a citation into
`JOURNAL.md` (a wrap cites its session's *work* commits, never its own unknowable hash);
the run of commits newer than that wrap is the current session, which is non-empty exactly
when this session shipped work it has not yet journaled. Per-commit detection uses `git show
--first-parent`, so a `--no-ff` merge that carries the branch's JOURNAL entry still anchors.

- **When it fires:** at a plausible wrap — a **clean tree** with unjournaled commits in this
  session's trailing run (work ahead of the last journal-wrap, with no session SHA in the
  `JOURNAL.md` additions for that run).
- **Effect:** the Stop-hook **blocks turn-end** (`decision: block`). The only exit is
  `/override [reason]`.
- **Supersedes** the older advisory journal-*presence* check — the SHA anchor strictly
  subsumes it (presence without a SHA no longer passes).

Implementation: `scripts/session_end_backpressure.py::check_journal_sha_anchor()` (the teeth);
the boundary-walk + `--first-parent` merge guard + verified-`origin/main` base live there.

### BACKLOG — gated, **advisory** (interim, v1)
Any session that lands commits **should** update `BACKLOG.md` with a structural-marker
change (a `[#NN]` issue-ID, a `status:` keyword, or a `[ ]`/`[x]` checkbox).

- **When it fires:** clean tree + commits ahead of `base` + no structural marker in the
  `BACKLOG.md` arc diff.
- **Effect:** **advisory nudge only** (folds into the hook's `additionalContext`) — it
  does **not** block turn-end in v1.
- **Why advisory, not a block (ADR-85 §3 / R1):** a hard gate is justified only for a
  check that is both un-gameable *and* always-warranted. The marker check is neither — it
  is gameable, and per the "done tasks leave the file" convention a session that *advances*
  but does not *finish* a tracked task legitimately warrants no backlog edit. Hard-gating
  it now would manufacture false-positives. It is **promoted to a hard block when the
  traceability-spine ADR lands** and gives it an airtight issue-ID↔commit anchor.

## NOT gated — "update when materially affected"
`ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `CONTRIBUTING.md` are **not** a per-session
obligation. Update them when the work materially affects them; otherwise leave them. Their
staleness is a later detection signal in the conformance dashboard (ADR-85 R2), **not** a
session gate and **not** human memory.

## Override
A blocked turn exits **only** via `/override [reason]` (`.claude/commands/override.md`):
- The reason is **required** — no reason, no override.
- It is **logged** (`logs/OVERRIDES.md`, gitignored ephemeral local audit).
- It is **HEAD-bound**: it allows the gate while HEAD is unchanged and **re-arms
  automatically when a new commit lands**. The Stop-hook only *reads* the token (it stays
  a read-only validator per the scripts-are-read-only invariant).
- **No auto-bypass-after-cap.** There is no retry-counter that eventually yields — that
  would train "persistence beats policy."

## Scope-freeze
**No docs are added to this gate for 4 weeks** from ADR-85 (i.e. until ~2026-07-14) —
gather reliability and override-rate data first. If overrides exceed ~10% of sessions, the
*rules* need tuning, not the human reinstated as trigger.

## Build/arc acceptance contracts — a different scope (pointer, NOT a gate here)
For a **deterministic build task**, "done" also requires that it met an **executable acceptance
contract the architect authored _before_ the build and froze** — immutable to the executor (CC may
strengthen, never weaken), with **closure declared on that contract (the hard metric), not on
"tests pass / merged."** That is **build/arc** scope: it lives in **PLAYBOOK Ch12.1 "Definition of
shipped"** + the **ADR-81 amendment (2026-06-24)** — **not** in this file and **not** in the
session-end Stop-gate. This doc governs only the *session-close record* (JOURNAL/BACKLOG above);
the three scopes — session-close / arc-shipped / organ-done — are kept distinct (PLAYBOOK Ch12.1).
Deterministic-scoped; the fuzzy band is deferred to its own arc.

---
See also: ESSENTIALS "Ending a Session" (the human-facing wrap habit this gate backstops);
`docs/decisions/ADR-85-session-lifecycle-enforcement.md` (the decision + rationale).
