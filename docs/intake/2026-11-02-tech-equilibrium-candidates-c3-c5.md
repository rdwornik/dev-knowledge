---
intake-id: 123
status: SEED
origin: "operator order 2026-11-02 (RATIFICATION-2026-11-02-GROK-AND-TOKEN-D0.md, decision 4: route CANDIDATEs C-3, C-4, C-5 through the ADR-111 funnel); candidates from DIGEST-EQUILIBRIUM-RESULTS-2026-11-02.md (orchestrator-e3-0-cycle-2)"
consumed-by:
---

# SEED batch — equilibrium-digest CANDIDATEs C-3, C-4, C-5 (one batched doc per the feed pattern)

Three findings of the 2026-11-02 equilibrium night were triaged **CANDIDATE** under ADR-111 §2(c): each needs a decision before it can become work. The operator ordered them routed through the funnel (CANDIDATE -> intake -> ratification). This doc is the intake step. It proposes; it decomposes nothing and files no backlog row (a row comes only after ratification, ADR-111). No ADR is drafted here.

Source of all three: `DIGEST-EQUILIBRIUM-RESULTS-2026-11-02.md` (operator's `to-browser/`, off-repo), candidate list near lines 171-173. Routing record: `RATIFICATION-2026-11-02-GROK-AND-TOKEN-D0.md`, decision 4. Context: `DIGEST-TOKEN-AND-GROK-REVIEW-2026-11-02.md`.

## C-3 — The handoff boundary check also refuses on branch leftovers

**Disposition (ADR-111): CANDIDATE.** Verbatim:

> **C-3 The handoff boundary check also refuses on branch leftovers:** a merged branch other than main/automation/*, or a `worktree-*` branch with no registered worktree that is not in the carrier table (git-discipline.md's verify lines, enforced at the cut by gen_handoff.assert_boundary_hygiene).

Evidence in the digest (H-6): the mechanism check was ABSENT. `assert_boundary_hygiene` (scripts/gen_handoff.py:584-608) refuses on linked worktrees and stash entries only; it never checks a merged branch or a `worktree-*` branch with no worktree, which is what `.claude/rules/git-discipline.md`'s verify lines name. `audit.py check_stale_worktrees` (:1898) is WARN-tier and covers worktrees only. Locators are the digest's and unverified here (run `/preflight` before acting).

Open question for the architect: does the cut refuse (blocking) or only report, given ADR-129 (the cut is gated by handoff-relevant checks only)?

## C-4 — The boot's "check BACKLOG.md" line

**Disposition (ADR-111): CANDIDATE.** Verbatim:

> **C-4 The boot's "check BACKLOG.md" line:** decide the line's fate (BACKLOG.md is generated; the funnel view is `boot-session`) together with ADR-135 D6's JOURNAL freeze, which retires "read the last 5 JOURNAL entries".

Evidence in the digest (G-M1): ADR-135 exists, Accepted, but only on `worktree-e31-decide` (main stops at ADR-133); it does not decide the two instruction lines. D6 runs a generated read journal in parallel with JOURNAL.md for one batch (E3.2) and freezes JOURNAL.md only if its measures hold, so "read the last 5 JOURNAL entries" cannot retire before that freeze (ADR-85's pre-push gate still reads JOURNAL.md). "Check BACKLOG.md" is decided by no ADR. The two lines are in CLAUDE.md (§1 item 3 and §6 item 4), not AGENTS.md.

Open question: ordering against ADR-135 D6 (the digest couples the two decisions).

## C-5 — Grok launch argv gets `--trust`, plus one capped obedience call

**Disposition (ADR-111): CANDIDATE.** Verbatim:

> **C-5 Grok launch argv gets `--trust`, plus one capped obedience call,** before any CLAUDE.md deletion (section 3).

Evidence in the digest (section 3): headless Grok loads AGENTS.md only with a trusted folder; `grok --trust inspect --json` listed the project AGENTS.md (`projectTrusted: true`), without `--trust` only global files. Discovery only, 0 model calls; obedience unproven. The registry note of 2026-08-26 ("grok picks CLAUDE.md over AGENTS.md") is stale until re-measured.

**Constraint (operator ruling R-a, 2026-11-02):** Grok leaves the backup chain and runs only with the operator's **per-case approval**, under token-economy D0's per-run per-provider cap. The "one capped obedience call" is therefore a Grok call that needs the operator's explicit approval each time it is made; ratifying C-5 does not pre-approve it.

## Status

SEED (feed pattern). Awaiting technical-architect triage and ratification per ADR-111; no backlog row until then.
