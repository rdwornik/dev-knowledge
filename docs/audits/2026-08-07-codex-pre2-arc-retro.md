# Codex Review — pre2-arc-retro

**Date:** 2026-08-07
**Branch:** `feat/pre2-batch2-preconditions`
**HEAD:** `945598f9`
**Diff range:** `4ad76bc5..945598f9`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/5/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- RETROACTIVE review of the merged PRE-2 arc (batch-2 preconditions).
- scripts/batch_manifest.py (NEW): the ADR-110 declared-integration-arc exemption. Check the fail-toward-no-exemption posture, the None-vs-empty distinction, the frontmatter parse, the closed_by absence probe, and whether any input could make open_batches() report an open batch it should not.
- scripts/audit.py check_journal_spine_anchor: the exemption wiring. Can an exempted entry ever be silently dropped without appearing in the pass evidence?
- scripts/audit.py _stash_findings / _git_stash_entries: the git_known_good resolution.
- .github/workflows/report-only-wall.yml: the new changes job and the mutation-pilot if gate. Shell-injection risk in the changed-files step; correctness of the before-sha guards.
- Ignore prose/markdown paths entirely.

---

## Findings
## Critical

(none)

## High

### `scripts/batch_manifest.py:116` — Uncommitted manifests grant the exemption

**What:** `open_batches()` reads manifests directly from the working tree, despite the rule requiring a committed manifest.  
**Why:** An untracked `status: open` manifest can make the audit backstop pass locally without any committed declaration.  
**Fix direction:** Resolve manifests and their closure state from `HEAD` (or otherwise require tracked, committed content).

### `scripts/batch_manifest.py:127` — `closed_by` can create a non-expiring exemption

**What:** `closed_by` is accepted as any path; absolute/escaping paths and YAML inline-comment suffixes are treated as absent filesystem paths.  
**Why:** For example, `closed_by: /never-created` or `packet.md # closes batch` leaves a manifest open even after the intended packet lands.  
**Fix direction:** Enforce a strict repo-relative closure-path grammar and parse/reject unsupported frontmatter syntax before probing the path.

### `scripts/audit.py:3875` — Mixed results hide applied exemptions

**What:** When non-exempt gaps remain, the function returns the FAIL finding before emitting any evidence for `exempted`; the added test explicitly expects the lane SHA to be absent.  
**Why:** An exemption can be silently dropped from the audit record whenever another unanchored merge also exists, undermining the stated traceability requirement.  
**Fix direction:** Include exempted SHAs and their manifest/closure provenance in both PASS and FAIL evidence.

### `.github/workflows/report-only-wall.yml:54` — Non-fast-forward pushes can spuriously run the mutation pilot

**What:** The changed-files guard verifies that `before` exists but not that it is an ancestor of `github.sha`.  
**Why:** If an old main tip remains reachable through another ref after a force-push, `git diff` compares unrelated histories and can mark the pilot subject changed.  
**Fix direction:** Require `before` to be an ancestor before using it as the pilot’s change range; otherwise emit `pilot_subject=false`.

### `.github/workflows/report-only-wall.yml:158` — Anchor recorder invokes the hook with an unresolved old SHA

**What:** Unlike the `changes` job, the anchor step only checks empty/all-zero `before` values and never confirms the old commit is present.  
**Why:** After a force-push whose previous tip is unavailable in the checkout, the report records a hook internal error rather than the documented `n/a` range skip.  
**Fix direction:** Add a `git cat-file -e "$before^{commit}"` guard before invoking `block_unanchored_push.py`.

## Medium

(none)

## Low

(none)
---

## Disposition — 2026-08-07 (PRE-2 self-review)

**Tally 0/5/0/0 — ALL FIVE ACCEPTED, all five FIXED.** This is the integrator reviewing its own
arc, which the batch-2 manifest's condition 3 requires of the integrator exactly as of a lane.
The [#480] leg flagged `945598f9` for the same gap it flagged lanes A and B, and it was right
again: five real defects, three of them in the R-1 exemption **that batch 2 is about to run
under**.

### H1 · An UNCOMMITTED manifest granted the exemption — FIXED

`open_batches()` globbed the working tree and checked only that a FILE EXISTED, while the ADR
says a **committed** manifest. An untracked file dropped into `docs/audits/` would have quieted
the gate with nothing appearing in any diff a reviewer reads. **Fixed** with a
`git ls-files --error-unmatch` tracked-ness probe (unknown reads as not-tracked, the safe
direction), pinned by `test_an_UNCOMMITTED_manifest_grants_nothing`, which asserts the same file
opens nothing untracked and opens the batch once committed.

### H2 · `closed_by` could name a path that never resolves — FIXED

Any string was accepted. An absolute path, a drive-lettered one, one escaping via `..`, one
outside `docs/audits/`, or one carrying a YAML inline comment would never resolve on disk — and
a closer that never resolves is a **permanent exemption wearing well-formed clothes**, the exact
hole the ADR's own honest-limit warns about. **Fixed** by `_valid_closer()` shape validation plus
inline-comment stripping in the frontmatter reader; six rejected shapes are parametrized, and
`test_the_live_repos_own_manifest_is_well_formed` checks the batch-2 manifest that is armed right
now rather than assuming it.

### H3 · The mixed case hid the exemptions it had applied — FIXED

When any non-exempt gap remained, the FAIL branch returned **before mentioning `exempted` at
all**. So a FAIL naming one unanchored merge silently omitted the lane merges just skipped —
directly contradicting this amendment's own *"reported, never applied silently"* clause, in the
one case where a reader is most likely to be counting. **My own test pinned the hole**: it
asserted only that the lane SHA was absent, which a FAIL that never mentioned the exemption
satisfies perfectly. **Fixed** in the evidence, and the test now also asserts the disclosure.

That is the third time today my code contradicted a rule written in its own docstring (the
stash-leg silence, the "detector that cannot see" line, and now this). The pattern is worth
naming: prose stating a principle is not evidence the branch implements it, and a test written
by the same author in the same sitting inherits the same blind spot. A second reader is what
caught all three.

### H4 · The pilot filter compared possibly-unrelated histories — FIXED

The `changes` job verified `before` EXISTS but not that it is an ANCESTOR of `github.sha`. After
a force-push the old tip can remain reachable through another ref, and `git diff` across
unrelated histories reports every file as changed — marking the pilot subject touched on a push
that never went near it. **Fixed** with a `git merge-base --is-ancestor` guard, still failing
toward not-running.

### H5 · The anchor leg handed the hook an unresolvable SHA — FIXED

The anchor step guarded only empty and all-zero `before` values, never existence, so after a
force-push whose previous tip is absent from the checkout the record captured a hook INTERNAL
ERROR instead of the documented `n/a` range skip. **Fixed** with a `git cat-file -e` guard —
the shape the `changes` job already had and this older step did not. Pre-existing from lane A
rather than introduced by this arc, and fixed here because it is one line and sits in the file
this arc was already editing.

### What this says about the gate that caught it

`review_artifact_coverage` fired on the integrator's own merge, and the review found three
defects in the exemption mechanism before batch 2 ran under it. The condition-3 clause that
binds the integrator is not ceremony.
