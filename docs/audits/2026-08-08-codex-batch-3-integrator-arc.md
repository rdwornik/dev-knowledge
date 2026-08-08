# Codex review — batch-3 integrator arc code impact

- **Class:** codex (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** batch-3-integrator-arc
- **Branch:** `docs/batch-3-close` · **Merge:** `bedcf3fe` · **Reviewed commit:** `679ccbc0`
- **Reviewer:** `codex exec` (codex-cli 0.145.0), independent of the author.

**Tally:** 0/0/0/2 <!-- Critical/High/Medium/Low. Counted from the Findings section below. Zero findings against the reviewed diff itself; the two LOWs are pre-existing stale locators in OTHER files, surfaced by the review's third question and carried per the arc's contract. -->

## Why this artifact exists

Batch 2's manifest, condition 3: *"Condition 3 binds the integrator too… An integrator arc that
touches `scripts/` or `tests/` carries a review like any lane."* This arc touched `tests/`, so
`review_artifact_coverage` flagged the close merge exactly as it flagged the batch-2 morning arc —
where the retroactive review then found two real defects. The WARN was **not** dispositioned around;
the review was run.

**Producer ≠ reviewer.** The diff's author did not grade it: the verdict below is `codex exec`
output, invoked with the diff and three falsifiable questions rather than "look for problems".

## Scope reviewed

The arc's **entire** code impact — 2 changed lines in 1 file:

```
tests/test_reverse_dep_oracle.py | 4 ++--
```

Both are line pins re-pointed from `327` to `344` after an unrelated merge (lane E, `764f06c8`)
inserted 17 lines above `class Finding:` in `scripts/audit.py`. Everything else in the arc is
markdown, `tasks/` frontmatter, `manifest.json` node removal, and generated files.

## Findings

**Against the reviewed diff: NONE.** All three questions answered affirmatively:

1. `class Finding:` **is** at `scripts/audit.py:344` — verified against the file, not the diff.
2. The second assertion **retains its meaning** — it still uses `not in`, so the declaration site
   is still asserted not to be its own reverse-dependent. Only the line it names changed.
3. The zero-based companion pin at `tests/test_reverse_dep_oracle.py:84` is **already correct at
   343**, so the repin is complete and consistent.

### LOW — `tests/test_v6_frozen_contract.py:226`: stale `audit.py:1575` locator

A **comment**, not an assertion. The cited line no longer identifies `_select_active_bundle`'s
ambiguous-failure path, which now sits around `scripts/audit.py:2046–2099`. Navigation rot only —
nothing asserts on it, so no test can catch it. Fix direction: cite the symbol, not the line.

### LOW — `tests/test_review_artifact_coverage.py:276`: stale `audit.py:3594` locator

Also a comment. The `[#483] R3` advisory posture it points at now begins around
`scripts/audit.py:3900`. Fix direction: cite `check_preflight_backlog_ids` by name.

**Both LOWs are PRE-EXISTING and are CARRIED, not fixed** — this arc's contract forbids fixing
carried findings, and neither was introduced here. Filed for whoever takes the F3/F4 locator work.

## The finding the review made possible, worth more than the two LOWs

**Lane E repinned 1 of the 3 live pins and missed 2.** The comment above line 84 proves it knew
exactly what it was doing — *"Last re-pinned 2026-08-08 ([#396]: the gitenv import block landed
near the top of audit.py)"* — yet the two 1-based pins 136 lines below went untouched, and the lane
handed back with its own suite unrun against them.

This is the standing lesson in sharper form: **the pin count must be re-grepped, never recalled.**
The lane recalled one site. The integrator re-grepped and found three. A lane that repins "the"
pin, singular, is the shape of this defect.

## Honest limits

- The review covers the arc's **code** impact only. The markdown — this batch's manifest, packet,
  amendments and JOURNAL entries — is unreviewed by codex and rests on the gates plus operator read.
- `codex exec` graded a 17-line diff. A clean verdict on a diff this small is weak evidence about
  the arc as a whole; it is strong evidence only about the two lines actually changed.
- The third question deliberately reached **outside** the diff (other stale pins), which is how the
  two LOWs surfaced. That widening was the author's prompt, so absence of further findings outside
  the diff means the reviewer was not asked, not that nothing is there.
