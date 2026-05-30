---
description: Generate or complete a handoff per HANDOFF_PROCESS.md v4 — two-phase interview + consolidate
---

Invoked by Rob saying one of:
- `please create handoff for <repo>` — Phase 1 (interview)
- `complete handoff for <repo>` — Phase 2 (consolidate)

`<repo>` defaults to `.dev-knowledge` (self-handoff). A different repo name is a
cross-repo handoff (read-only on the target — ADR-36/41).

**Source of truth:** `protocols/HANDOFF_PROCESS.md` (v4). This skill is a dispatch
summary, not a substitute. Where they disagree, the spec wins — fix the divergence.

## Conventions

- `slug` = `YYYY-MM-DD-<repo>-<type>` (today's date; `type` defaults to `session`,
  or `onboarding` for a new-repo handoff). `<repo>` strips any path — e.g.
  `.dev-knowledge` → `dev-knowledge`.
- Interview (in-progress): `docs/handoffs/in-progress/<slug>/_handoff-interview.md`.
- Bundle: `docs/handoffs/<slug>/` (README + `01`–`07`); Phase 2 removes `in-progress/<slug>/`.
- One commit per phase on a feature branch. Validators must pass each commit.

## State machine (detect by CONTENT, not file existence)

| State | Detected by | Action |
|---|---|---|
| Fresh | no `in-progress/<slug>/_handoff-interview.md` | Phase 1 |
| Awaiting answers | interview exists, nothing below the PASTE marker | instruct operator (idempotent — do NOT regenerate) |
| Ready | interview exists **with** non-empty content below the marker | Phase 2 |
| Complete | `docs/handoffs/<slug>/` already exists | instruct operator on use |

The PASTE marker is the line `=== PASTE ANSWERS BELOW THIS LINE ===`. "Non-empty
answers" = substantive prose below it, not whitespace/placeholder. If state is
ambiguous (bundle exists and Rob says "create" again) → FLAG and ask, never
overwrite.

## Phase 1 — Interview

1. Pre-flight: confirm `<repo>` path exists and is a git repo; capture its state
   read-only — HEAD SHA (`git rev-parse HEAD`), branch (`git branch --show-current`),
   working tree (`git status --porcelain`).
2. If `in-progress/<slug>/_handoff-interview.md` already exists → you are NOT fresh;
   report the detected state and stop (don't clobber).
3. Create `docs/handoffs/in-progress/<slug>/` if absent. Write `_handoff-interview.md`
   with the **sage→apprentice** content below — verbatim, matching HANDOFF_PROCESS
   §3.1 (the apprentice reads the books independently; the sage transmits only this
   project's lived implementation this session, NOT methodology curriculum):
   - A header table: repo, slug, date, type, captured HEAD/branch/working-tree, and
     a `Process` row. Substitute the captured values.
   - The **Role frame** preamble (elder sage handing wisdom to a tired apprentice;
     books = theory, sage = lived implementation) and the **four-tag** claim
     discipline (v4.2 Amendment A — supersedes the three-tag §3.1 body; carry these
     definitions verbatim into the preamble) + skip-if-N/A instruction:
     - **witnessed** = I just verified this OR saw it happen recently AND have no reason to think it changed since
     - **recall** = I remember this from earlier in the session — state may have changed; prefer verifying via CC inline if the claim is load-bearing
     - **inferred** = reasoning from evidence (not direct knowledge)
     - **unknown** = I don't know — say so explicitly
   - A **single cluster of 5 questions**: `1. Past — what shipped`, `2. Present —
     where things stand`, `3. Future — natural next step`, `4. Wisdom — key
     decisions`, `5. Warnings — landmines`. Question wording matches §3.1 verbatim.
   - The marker line `=== PASTE ANSWERS BELOW THIS LINE ===` with empty space below.
4. Append a JOURNAL marker entry (newest-first): handoff Phase 1 interview generated
   for `<slug>`; HEAD captured; awaiting operator answers.
5. Run validators (`pre-commit run --all-files` or pytest/ruff/audit). Commit on the
   feature branch.
6. Report: interview written; next step — paste the question block into the sender
   chat, paste answers below the marker, save, then say `complete handoff for <repo>`.

## Phase 2 — Consolidate

1. Read `in-progress/<slug>/_handoff-interview.md`. If no non-empty answers below the
   marker → report "awaiting answers" and stop (idempotent).
2. Re-capture current repo state. **Cross-check** the browser answers against actual
   repo state (git log/branch/status, BACKLOG, file existence). Surface any drift to
   the operator — both the claim and the repo fact — and let the bundle reflect
   verified state.
3. Read `templates/handoff/` (README + `01`–`07`). For each, resolve markers from
   source at handoff time:
   - `{{PULL: <source>#<section>}}` — condense the named section of the live source
     (PLAYBOOK / ESSENTIALS / VISION / CLAUDE / BACKLOG, or `git branch -v`). For
     cross-repo, pull project files from the **target** repo when present.
   - `{{SYNTHESIZE: <source>}}` — write narrative prose (JOURNAL arc, interview
     answers folded inline, claims cross-check, dynamic comprehension questions).
   - `{{CONTEXT: <var>}}` — substitute captured values (slug, repo, type, date,
     branch, head_sha, working_tree_state, degradation_notes, drift_notes, version,
     status). `version` = `4.3`; `status` = `beta` (promote to `stable` after one
     fresh-eyes review with <2 critical findings — v4.3 item E, which supersedes the
     v4.2 three-runs heuristic).
   - `04_RECENT.md`: synthesize from JOURNAL last N entries (N=20 OR last 7 days,
     whichever smaller) as NARRATIVE prose, fold in the interview answers, and inline
     the load-bearing-claims cross-check (v4 home of the old `11_CLAIMS.md`).
3a. **Always-emit rules** (v4.2 items B/C/D + v4.3 item B — emit whether or not drift was found):
   - `04_RECENT.md` carries the **Four-tag discipline (canonical)** standalone section
     (v4.3 item B) between the narrative arc and the Load-bearing facts table —
     verbatim from the template, so the apprentice applies the discipline from the
     bundle alone without reading the spec.
   - `04_RECENT.md` Load-bearing facts table is a **required section**, columns fixed
     `Claim from sender | Repo fact | Phase-2 verdict | Verification command`. No drift → the
     single row `| (all sender claims) | matches repo state | ✅ no drift detected |
     (verified at Phase 2) |`. Drift → one row per claim with the EXACT detection
     command in the Verification command column.
   - `README.md` carries the **Drift cross-check** section right after the paste
     sequence + escalation ladder, before the bundle contents table. No drift →
     `**No drift detected** — all sender claims verified against repo state at Phase 2.`
   - `README.md` header carries the stamp `Generated by HANDOFF_PROCESS v4.3 (status: beta)`.
4. Respect line budgets: 01≤100, 02≤200, 03≤150, 04≤250, 05≤100, 06≤80, 07≤50.
5. Write the bundle to `docs/handoffs/<slug>/` (8 files, flat, markdown only — NO
   JSON manifest, NO gate-probe file, NO separate claims file).
6. **Graceful degradation:** missing source file → build from fallbacks, omit the
   section, and note it in `README.md` degradation notes — never fabricate.
   Unresolvable marker (section renamed/removed) → stop on that file, report the
   marker + its target source, ask the operator. Never ship a literal marker.
7. Remove the `in-progress/<slug>/` folder (interview content is folded into `04_RECENT`).
8. Append a JOURNAL marker entry: handoff Phase 2 complete for `<slug>`; bundle at
   `docs/handoffs/<slug>/`.
9. Run validators. Commit on the feature branch.
10. Report: bundle generated; any drift found; any degradation noted; next step —
    use the bundle per its `README.md` escalation ladder (paste 01–05, then 06,
    Tier 1/2/3 on failure, then 07).

## Hard constraints (violation is a process failure)

- **Two phases only.** No Stage vocabulary, no placeholder-file dance, no separate
  scratch files per artifact — one interview file, one bundle.
- **Eight files, flat, markdown only.** README + `01`–`07`. No JSON manifest, no
  `10_GATE_PROBE`, no `11_CLAIMS`, no `12_OPERATIONAL_*`.
- **Generate from source, never hand-maintain.** Every bundle is as current as the
  repo at handoff time. Resolve all markers; degrade loudly, never fabricate.
- **Cross-repo is read-only (ADR-36/41).** Never write to or direct work on another
  repo. Bundle always lives in `.dev-knowledge/docs/handoffs/`.
- **Operator-triggered only.** CC never proposes a handoff unprompted.
- **No ADR authored here.** The v4 architecture decision goes through AI Council, not
  this skill.
