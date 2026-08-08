# Codex Review — batch-3-integrator-arc

**Date:** 2026-08-08
**Branch:** `docs/batch-3-close`
**HEAD:** `679ccbc0` (the arc's entire code impact)
**Diff range:** `bedcf3fe^1..bedcf3fe`, filtered to `*.py`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/0/0/2 <!-- Critical/High/Medium/Low, counted from the Findings section. Zero against the reviewed diff itself; the two LOWs are pre-existing stale locators in OTHER files, surfaced because the prompt's third question deliberately reached outside the diff. -->

**Review profile:** code
**Passes:** 1 (a 17-line diff; the loop had nothing to converge on)

## SUPERSEDES `docs/audits/2026-08-08-codex-batch-3-integrator-arc.md`

Same review, same codex output, **correct machine-readable shape**. The earlier file was authored
with a prose header (`# Codex review …` lowercase, and `**Branch:**` embedded in a bullet with
trailing content) and therefore matched **neither** `_REVIEW_TITLE_RE` (`^# Codex Review\b`) nor
`_REVIEW_BRANCH_RE` (which requires the field alone on its line). It was invisible to
`review_artifact_coverage` — a review that ran, reached a verdict, and satisfied no gate.

Superseding by a new file rather than editing in place, because `docs/audits/` is immutable
(CLAUDE.md §5 rule 3) and here the rule's **first** sanctioned option actually works: nothing
requires artifact uniqueness, and the earlier file — failing the title regex — is inert rather than
competing. That is the difference from this batch's manifest defect, where superseding was
impossible and the frontmatter had to be corrected in place as a reported deviation.

**The class of defect is the same one this batch keeps producing, and it is worth naming:** an
artifact that is *correct to a human reader* and *invisible to the machine*. The manifest's
`batch:` field granted a working exemption while failing its well-formedness test; this artifact
recorded a real review while satisfying no coverage leg. Both look done. Neither was.

## Why this artifact exists

Batch 2's manifest, condition 3: *"Condition 3 binds the integrator too… An integrator arc that
touches `scripts/` or `tests/` carries a review like any lane."* This arc touched `tests/`, so
`review_artifact_coverage` flagged the close merge — exactly as it flagged the batch-2 morning arc,
where the retroactive review then found two real defects. **The WARN was cleared by running the
review, not by dispositioning it.**

**Producer ≠ reviewer.** The diff's author did not grade it: the verdict is `codex exec` output,
invoked with three falsifiable questions rather than "look for problems".

## Scope reviewed

The arc's **entire** code impact — 2 changed lines in 1 file:

```
tests/test_reverse_dep_oracle.py | 4 ++--
```

Both are line pins re-pointed `327` → `344` after lane E's merge (`764f06c8`) inserted 17 lines
above `class Finding:` in `scripts/audit.py`. Everything else in the arc is markdown, `tasks/`
frontmatter, a `manifest.json` node removal, and generated files.

## Findings

**Against the reviewed diff: NONE.** All three questions answered affirmatively:

1. `class Finding:` **is** at `scripts/audit.py:344` — verified against the file, not the diff.
2. The second assertion **retains its meaning**: still `not in`, so the declaration site is still
   asserted not to be its own reverse-dependent. Only the line it names changed.
3. The zero-based companion pin at `tests/test_reverse_dep_oracle.py:84` is **already correct at
   343**, so the repin is complete and consistent.

### LOW — `tests/test_v6_frozen_contract.py:226`: stale `audit.py:1575` locator

A **comment**, not an assertion. The cited line no longer identifies `_select_active_bundle`'s
ambiguous-failure path, now around `scripts/audit.py:2046–2099`. Navigation rot only — nothing
asserts on it, so no test can catch it. Fix direction: cite the symbol, not the line.

### LOW — `tests/test_review_artifact_coverage.py:276`: stale `audit.py:3594` locator

Also a comment. The `[#483] R3` advisory posture it points at now begins around
`scripts/audit.py:3900`. Fix direction: cite `check_preflight_backlog_ids` by name.

**Both LOWs are PRE-EXISTING and CARRIED, not fixed** — this arc's contract forbids fixing carried
findings, and neither was introduced here.

## The finding worth more than the two LOWs

**Lane E repinned 1 of the 3 live pins and missed 2.** The comment above line 84 proves it knew
exactly what it was doing — *"Last re-pinned 2026-08-08 ([#396]: the gitenv import block landed
near the top of audit.py)"* — yet the two 1-based pins 136 lines below went untouched, and the lane
handed back without running its suite against them.

The standing lesson, sharpened: **re-grep the pin count, never recall it.** The lane recalled one
site; the integrator re-grepped and found three. A lane that repins "the" pin, singular, is the
shape of this defect.

## Honest limits

- Covers the arc's **code** impact only. The markdown — manifest, packet, amendments, JOURNAL
  entries — is unreviewed by codex and rests on the gates plus operator read.
- `codex exec` graded a 17-line diff. A clean verdict on a diff this small is strong evidence only
  about the two lines actually changed, not about the arc as a whole.
- The third question deliberately reached **outside** the diff, which is how the two LOWs surfaced.
  Absence of further findings outside the diff means the reviewer was not asked, not that nothing
  is there.
- Per the leg's own honest limit, this artifact proves a review **exists, is linked, and carries a
  parseable tally**. It cannot prove the review was competent or the tally truthful.
