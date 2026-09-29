# Codex Review — lane-runtime-data-home-decision

**Date:** 2026-09-27
**Branch:** `worktree-lane-runtime-data-home`
**HEAD:** `4a968131`
**Diff range:** n/a — this reviews the R17 DECISION document (research/inventory/options/matrix
in `to-browser/SESSION-lane-runtime-data-home.md`), not a code diff; ad-hoc doc-lane invocation
per the established deviation (see Mode below).
**Codex version:** codex-cli 0.155.0
**Tally:** 0/1/5/1 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both prior lanes — [#469])
**Review profile:** doc (ad-hoc `codex exec -c model=gpt-5.6-terra --sandbox read-only`, not
the wrapper's diff-review path — this is a decision document, not a diff)

---

## Focus

- The R17 decision (LANE-5B4-15-runtime-data-home.md done-contract item 2): the `logs/`
  inventory with writer/reader per entry, five primary-source citations, all four
  contract-named options, and the five-criterion scoring matrix, all reproduced in full in
  the prompt fed to Codex (`C:\Users\1028120\.claude\jobs\d149f12a\tmp\r17-decision.md`).
- This is the SECOND repair-cycle review for this lane. Two prior rounds
  (`2026-09-27-codex-lane-runtime-data-home.md`, `-followup.md`) reviewed the redaction CODE;
  this round reviews the DECISION the integrator's first refusal named as incomplete.

---

## Findings

## High

### Decision document — inventory is incomplete and overstates "only ONE" private class

**What:** The gitignored inventory omitted several concrete entries (`FLEET-PARITY.md`,
`PARITY-EVENTS.jsonl`, `ENFORCEMENT-COVERAGE.md`, `LIVED-WORKFLOW.md`, `BOUNDARY-DRIFT.md`,
`FLEET-ANALYTICS.md`, `OVERRIDES.md`); `logs/prompts/` was not evidenced as safe.
**Why:** "Only ONE class" is the premise that earns option D a privacy score of 2, but the
census as first written did not establish it.

## Medium

### Decision document — writer/reader table is not complete

**What:** `logs/LANE-COSTS.jsonl` omitted `scripts/lane_cost.py` itself as a reader (it joins
the ledger against `MERGE-RECEIPTS.jsonl` for its own report render); the "regenerates from
live state on every run" claim was a blanket statement not checked against each writer.

### Decision document — FHS support is overstated

**What:** The FHS quote genuinely distinguishes `/var/cache`, `/var/lib`, `/var/log`,
`/var/spool` by kind, but the retention/backup-policy rationale attributed to it goes
beyond what the cited passage was verified to establish on this pass.

### Decision document — pip/npm analogy is weaker than represented

**What:** pip and npm's sources are genuine and accurately state per-user cache defaults,
but they concern disposable dependency caches, not persistent prompt-adjacent telemetry —
"identical problem/class of data" overstated the parallel.

### Decision document — option A is characterized inconsistently and option B is constrained to lose

**What:** Option A was called "flat" though the inventory itself lists `logs/2026-09/`,
`logs/receipts/`, `logs/prompts/`; option B was scored only under a full-relocation
assumption with no narrower variant considered.

### Decision document — matrix arithmetic is correct, but its decisive privacy score was unproven

**What:** Row totals (8, 6, 4, 9) were arithmetically correct and most cells followed the
stated prose, but D's `privacy_on_public_repo=2` rested on the then-uncited, incomplete
sensitivity census named in the High finding above.

## Low

### Decision document — primary-source research is otherwise sound

**What:** XDG, platformdirs, pip, npm and FHS are all genuine sources, correctly fetched
2026-09-27, and the core OS-placement rationale (XDG's state-directory semantic category +
`platformdirs.user_state_dir`) is credible independent of the narrower issues above.

---

## Answered (every finding, this repair)

1. **High — inventory completeness/"only ONE" premise.** Every currently-active ephemeral
   writer under `logs/` was enumerated from `.gitignore`'s `logs/` patterns and its owning
   script identified (`fleet_parity.py`, `enforcement_coverage.py`, `fleet_analytics.py`,
   `coherence_nudge.py`, `session_end_backpressure.py`, `bounded_hook.py`,
   `hooks/quota_daily.py`, and the receipts/prompts organs), then spot-checked
   (`git grep -n '"message"\|prompt\|free.text\|raw_text\|body'`) for arbitrary message/
   free-text serialization — none found; each writes structured counts, statuses or
   hook-bypass records, not prompt-adjacent content. **`logs/prompts/` is the one exception
   verified to matter:** its writer, `scripts/trace_writer.py`, was designed to hold the
   dispatch "contract AS SENT" (commit `413b9592`) — genuinely content-adjacent — but it was
   **retired and deleted** in commit `f7f04c41` (`[#664]`, 0 consumers, 0 outbound edges).
   `logs/prompts/` is therefore currently dead: no active writer populates it. Recorded
   honestly as `ROWS-OWED` below rather than asserted harmless, since a future revival of a
   prompts-writer would need the same privacy review this lane gave `GENAI-TELEMETRY.db`,
   not a silent re-use of the retired `.gitignore` entry.
2. **Medium — writer/reader completeness.** `scripts/lane_cost.py` added as a reader of its
   own `logs/LANE-COSTS.jsonl` (joins against `MERGE-RECEIPTS.jsonl` for its report render,
   `lane_cost.py:796`). The blanket "regenerates on every run" claim is now qualified per
   entry in the session file rather than stated once for the whole ephemeral class.
3. **Medium — FHS overstated.** The cited claim is narrowed to what `/var`'s text
   establishes directly: kind-based directory separation (`/var/log`, `/var/cache`,
   `/var/lib`, `/var/spool`). The retention/backup-policy rationale is kept as the fetched
   source's own gloss, attributed to the source rather than presented as this lane's
   independent finding.
4. **Medium — pip/npm analogy weaker than represented.** Reworded in the session file to
   "placement precedent only" (per-user, off-checkout tool-local state) rather than
   "identical problem/class of data"; the semantic-category argument rests on XDG +
   platformdirs alone, as Codex's Low finding recommends.
5. **Medium — option A/B fair characterization.** Option A's description now names the
   existing `logs/2026-09/`, `logs/receipts/`, `logs/prompts/` subfolders rather than calling
   the status quo "flat." Option B is now scored as two variants — full relocation (B) and a
   narrow variant that only applies the taxonomy to NEW paths, relocating nothing (B') — and
   B' is the fairer comparison: it ties option A on total score (8) precisely because it still
   scores 0 on privacy, the one criterion a public-repo in-tree folder cannot fix regardless
   of naming.
6. **Medium — matrix privacy score for D.** Substantiated by answer 1 above: after the
   completed census, no other CURRENTLY ACTIVE writer under `logs/` serializes free-text
   content, so D's privacy score reflects the ONE path (`GENAI-TELEMETRY.db`) this lane
   confirmed carries it, not an unverified blanket claim.
7. **Low — no change requested;** the five citations stand as fetched, with claims 3–4 above
   narrowed to match what each source supports.

**Re-scored matrix, both B variants, script re-run
(`C:\Users\1028120\.claude\jobs\d149f12a\tmp\score_options.py`):**
```
| Option | privacy_on_public_repo | os_agnostic | discoverability | what_agents_and_ci_read | migration_cost | TOTAL |
|---|---|---|---|---|---|---|
| A. keep logs/ (status quo) | 0 | 2 | 2 | 2 | 2 | 8 |
| B. domain-named in-repo folder per kind (full relocation) | 0 | 2 | 2 | 1 | 1 | 6 |
| B'. domain-named in-repo folder (narrow: new paths only, no relocation) | 0 | 2 | 2 | 2 | 2 | 8 |
| C. per-user OS state dir for everything | 2 | 2 | 0 | 0 | 0 | 4 |
| D. a mix (CHOSEN) | 2 | 2 | 1 | 2 | 2 | 9 |
```
Decision unchanged (D), now on a completed census: D wins even against the fairest possible
framing of its nearest in-repo competitor (B'), because privacy on a public repo — the one
property R17 exists to fix — is the one criterion no in-repo option can score above 0 on,
regardless of naming or relocation scope.

## ROWS-OWED (from this review)

- `ROWS-OWED: logs/prompts/ carries a retired writer (scripts/trace_writer.py, deleted
  f7f04c41) and an orphaned .gitignore entry; a future lane reviving prompt-tracing should
  re-run this lane's privacy classification against whatever it writes before assuming the
  existing ignore-and-forget treatment still applies.`
