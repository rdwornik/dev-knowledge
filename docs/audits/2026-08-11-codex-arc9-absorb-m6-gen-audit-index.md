# Codex Review — ARC-9 absorb prep, the M6 fix to `gen_audit_index.py`

**Date:** 2026-08-11
**Branch:** `docs/arc9-absorb-prep`
**HEAD:** `d98c2d45` (the reviewed commit — the arc's only code impact)
**Diff range:** `--base main`, i.e. `d98c2d45` against `a7ad24e7`
**Model:** `gpt-5.6-terra`
**Mode:** `codex exec review --base main`
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. Terra emitted one finding at its own [P1] severity; mapped to High here, which is the closest band in this file's C/H/M/L scheme. Zero Critical, zero Medium, zero Low. -->

**Review profile:** code
**Passes:** 1

## Why this artifact exists

The operator's 2026-08-10 §8 ruling required the M6 fix to be **terra-reviewed pre-merge** because
it is code-impact. The review ran and its finding was adopted — but the review was not persisted,
so `audit.py::check_review_artifact_coverage` correctly flagged `e3016465` as a code-impact merge
with no linked review artifact. **Persistence is not machine-auditability** ([#480]): a review that
happened but left no parseable artifact is, to every later reader and to the gate, a review that
did not happen. This file is that artifact, authored **after** the merge and saying so.

Authored from the parser rather than from prose intent: `# Codex Review` title, a `**Branch:**`
line, a `**HEAD:**` line, and a `**Tally:** C/H/M/L` line, matching `_REVIEW_TITLE_RE`,
`_REVIEW_BRANCH_RE`, `_REVIEW_HEAD_RE` and `_REVIEW_TALLY_RE` in `scripts/audit.py`.

## What was reviewed

`scripts/gen_audit_index.py` — M6 from the conformance-digest content census. The generated
`docs/audits/README.md` header advertised audit retention as *"proposed separately (`[#212]`)"*.
`[#212]` closed 2026-07-06 (`b4c4b6e4`) into ADR-100, whose title reads *"folds and closes #212"*.
The string is hard-coded in the generator, so every regeneration re-emitted it — including the one
the absorb ×7 required, which is why the ruling sequenced this fix first.

## Findings

### [High — terra's P1] The fix advertised a navigation shape the generator does not emit — **ADOPTED**

> *"`render_index` still emits every audit into month sections, with no ~20-item fresh section or
> archive section, while this new generated text says the index is count-tiered. As a result, each
> regeneration preserves the unimplemented ADR-100 navigation behavior but presents it as completed;
> implement the count split/grouping (and update the generated output) before advertising the policy
> as such."*

**Verdict: correct, and it caught a real regression in the fix itself.** The first wording
(`d98c2d45`) said *"keep-all-accepted, count-tiered index"*. ADR-100 does rule both, but only
keep-all is **built**: `render_index` groups by month, and the count-tiered shape plus its freshness
hook are `[#269]` — verified open at `tasks/269-audit-index-count-tiered-shape-freshness-hook.md`.

So the fix as first written would have **replaced one false pointer with a second false claim**, and
the second is worse: the original said an answered question was still open; the replacement would
have said an unbuilt shape was built.

**Resolution — `cac0ed09`.** The header now states the ruling and names the unbuilt part explicitly:
retention is ruled keep-all-accepted (ADR-100); the count-tiered shape is `[#269]` and is NOT built;
this index groups by month. The `[#269]` pointer is live and correct, unlike the closed `[#212]`
pointer it replaces. Terra's remedy (implement the tiering) was **not** taken — that is `[#269]`'s
owned work and outside this arc's GO; the claim was corrected to match reality instead, which
resolves the finding without silently absorbing another row's scope.

## Honest limits of this review

- **One pass, one file.** The diff was two string sites in one module; there was nothing for a
  convergence loop to converge on.
- **Not re-run after the fix.** `cac0ed09` was verified by regeneration + `--check` exit 0 + ruff
  clean + reading the emitted header, not by a second terra pass.
- **Scope was the diff**, not `gen_audit_index.py` as a whole. Nothing here asserts the module is
  otherwise defect-free.
- **Authored post-merge.** The review preceded the merge; this record did not. The
  `review_artifact_coverage` WARN that prompted it was therefore accurate at the time it fired.
