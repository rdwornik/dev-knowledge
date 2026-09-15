---
intake-id: 96
status: DRAFT
origin: lane `lane-z-11-three-repo-comparison`, 2026-09-15 — measured against bmad-code-org/BMAD-METHOD `tools/validate_file_refs.py`; see `docs/audits/2026-09-15-technical-lane-z-11-comparison-matrix.md` row G-1
consumed-by:
---

# Nothing checks that the locators in our own living documents still resolve

## Problem / motivation

`CLAUDE.md` §4 names locator resolution as *"the most-recorded executor failure in the
2026-08-21 governance-drift audit"* and binds it: *"a `file:line`, heading, SHA, branch or
`[#id]` you have not opened is a claim, not evidence."*

The rule is enforced **on inputs** — a contract or prompt handed to `/preflight`. It is not
enforced **on this corpus**. A `file:line` written into a living protocol document is never
re-checked after the file it cites moves, and `check_doc_code_edge` does not cover the case:
its scope is an include-list of four declaration docs and a single `<!-- rule: ID -->`
annotation form, fail-soft by declaration.

A comparable project runs the corpus-wide version. `bmad-code-org/BMAD-METHOD` ships
`tools/validate_file_refs.py`, which resolves cross-file references across all source files
and refuses absolute-path leaks — warning-only by default, *"so adoption is
non-disruptive"*, the same posture this repo already chose for `preflight_contract.py`.

**The yield here is low, and this intake is filed at that strength rather than louder.**
Measured in this lane, read-only, over 127 committed files: exactly **one** live broken
locator.

```
protocols/STANDING_RULINGS.md:4074  ->  templates/handoff/v5/PROBES.md.tmpl:96
live:  templates/handoff/v5/PROBES.md.tmpl is 77 lines
```

(The same citation appears at `JOURNAL.md:6171`, which is append-only and was true when
written — historical, not a defect.)

One finding across 127 files is not an emergency. What makes it worth filing anyway is
where it sits: in a **living governing document** that sessions are instructed to obey,
defending the failure class the repo names as its most-recorded. A session that resolves
that locator to decide what a ruling says finds nothing at line 96.

## Scenarios (+1 view)

- As a **session** reading `STANDING_RULINGS.md` for a ruling's basis, I follow the cited
  locator and it does not resolve. I cannot tell whether the ruling moved, the template was
  cut down, or the citation was always wrong — and the rule tells me an unopened locator is
  not evidence, so I am blocked on a governing document.
- As the **operator**, I want a doc whose citations rot to say so at commit time, in the
  same act that already regenerates the indices, rather than at the moment a session needs
  the citation.
- As an **auditor**, I want the corpus's citation health to be a number I can read rather
  than a spot-check, so "we follow the locator rule" stops being a claim about intent.

## Functional requirements

- **Must:** the citations in living documents are checked mechanically, on a cadence, and
  the result is reportable.
- **Must:** the check is calibrated for a **corpus**, not for a contract at freeze time.
  Three miscalibrations were measured this lane and any of them alone would sink adoption:
  - a `[#id]` predicate asking *"currently OPEN"* — right for a contract, wrong for an
    immutable ADR citing a long-closed row (282 of 499 flagged on this basis);
  - a `file:line` leg that reads any bare `name.ext:NN` in prose as a locator — it flagged
    `huggingface.co:443`, a host and port (37 of 39 flagged this way);
  - a `sha` leg that cannot survive a shallow clone (intake `#95`).
- **Should:** posture is warning-only at adoption. The measured yield does not justify a
  blocking gate, and both this repo and BMAD independently reached the non-disruptive
  default for this organ.
- **Could:** the append-only files (`JOURNAL.md`, `LESSONS.md`, `logs/TOKEN-LOG.md`) are
  scoped out or reported separately — a historical entry that was true when written is not
  rot, and treating it as such would make the report unreadable.

## Acceptance criteria (ex-ante)

1. A run over the living corpus reports the `STANDING_RULINGS.md` finding above.
2. The same run reports **zero** of the 37 prose false positives measured this lane —
   `huggingface.co:443` among them — and zero of the 282 closed-`[#id]` citations.
3. The run's output is a count plus a list, so corpus citation health is a number.
4. The check is re-runnable by the operator on demand and does not write to the tree.

## Non-goals

- Fixing the one finding. That is a one-line edit to a living doc and belongs to whoever
  holds that surface, not to the mechanism.
- Blocking a commit. Warning-only is the requested posture; promotion is a later ruling.
- Checking whether a locator points at the **right** line. `preflight_contract.py` already
  states plainly that it cannot, and that limit is inherited, not solved here.
- Building a second predicate library. The predicates exist; the gap is scope and
  calibration.

## Impact sketch (4+1 lite)

- **Logical:** a checker's subject widens from one input artifact to the committed corpus.
- **Process:** citation rot becomes visible on a cadence instead of at point of need.
- **Development:** one module (likely a mode on an existing one) plus tests.
- **Physical:** none — read-only, Layer-2 (ADR-28/36).

## Open questions

- Which files are in scope? "Living documents" is the intent; the enumerated set is a
  technical-architect question, and `canonical_docs.py::FRESHNESS_FILES` may already be the
  right surface to reuse rather than a new list.
- Does this belong as a mode on `preflight_contract.py` or as a sibling module? Technical.
- Is one finding per 127 files enough to justify the organ at all? A genuine functional
  question for the operator, recorded rather than assumed — this intake argues yes on the
  strength of *where* the finding sits, not on volume.

## Status

DRAFT — filed by lane `lane-z-11-three-repo-comparison`, 2026-09-15. Not triaged.
