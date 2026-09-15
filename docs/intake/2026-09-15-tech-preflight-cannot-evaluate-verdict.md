---
intake-id: 95
status: DRAFT
origin: lane `lane-z-11-three-repo-comparison`, 2026-09-15 — measured while comparing this repo against github/spec-kit, bmad-code-org/BMAD-METHOD and obra/superpowers; see `docs/audits/2026-09-15-technical-lane-z-11-comparison-matrix.md` row G-7
consumed-by:
---

# A locator predicate that cannot look must say so, not report a refusal

## Problem / motivation

`scripts/preflight_contract.py` verifies the locators a contract cites. One of its four
legs resolves a short SHA against this repo's object store, and renders a miss as
`not present in this repo's object store`.

In a full clone that verdict is correct. In a **shallow clone it is a false refusal**, and
a shallow clone is what every cloud lane runs on. Measured in this lane's own cloud
session, against a checkout carrying `.git/shallow` and 275 commits: **3,774 of 3,894** SHA
citations across 127 committed files rendered as unresolved, none of them because the
citation was wrong.

The verdict the reader receives is indistinguishable from "this SHA is wrong". So the organ
this repo points sessions at for locator discipline — `CLAUDE.md` §4, *"Resolve a locator
before you act on it … run `/preflight` first"* — produces a wall of false refusals in the
substrate an increasing share of lanes run in, and a reader who learns to discount them has
learned to discount the whole report.

Nothing is broken today: the organ is read-only and, as its own frontmatter says, *"wired
into no gate"*. The cost is entirely on the promotion path, and that path is live — ADR-119
and the `[#664]` census are actively deciding which operator-invoked organs deserve wiring.
Promoting this one unchanged would gate cloud lanes on a predicate that fails closed for a
reason that has nothing to do with the contract being verified.

**This repo already holds the answer and has not applied it here.** The same module keeps
exit 2 distinct from exit 1 precisely so that *"I could not look" stays distinguishable
from "I looked and it is wrong"*. `.claude/settings.json` argues the same distinction at
length for the prompts guard, and the `[#727]` guard is fail-OPEN by design for the mirror
reason. The `sha` leg simply does not extend the distinction it already owns to the case
where the object store is legitimately incomplete.

## Scenarios (+1 view)

- As a **cloud lane**, I run `/preflight` on my frozen contract. Every SHA the contract
  cites reports unresolved. I cannot tell which — if any — are real, so the report tells me
  nothing and I proceed unverified, which is the exact failure `/preflight` exists to stop.
- As the **architect** deciding whether `/preflight` becomes a gate (ADR-119 / `[#664]`), I
  need to know the predicate behaves the same way in every substrate before I can wire it.
  Today it does not, and that is a blocker on a live decision.
- As a **reader of a preflight report**, I see a refusal and cannot distinguish a wrong
  citation from an incomplete checkout. A verdict I must contextualise by hand is not a
  mechanism.

## Functional requirements

- **Must:** a locator verdict distinguishes *unverifiable in this checkout* from *verified
  wrong*. The distinction is visible in the rendered report, not only in an exit code.
- **Must:** the exit posture on an unverifiable claim is decided deliberately and recorded —
  a lane must not be able to read "could not check" as "checked and clean".
- **Should:** the report states, once, why a leg was unverifiable, so the reader learns the
  cause rather than the count.
- **Could:** the other three legs are reviewed for the same class of miss.

## Acceptance criteria (ex-ante)

1. Run the verifier on a contract citing a SHA that is real but outside a shallow clone's
   depth. The report does **not** present it as a failed citation.
2. Run the same verifier on a contract citing a genuinely non-existent SHA. The report
   **does** present it as a failed citation, distinctly from (1).
3. The two renderings are textually distinguishable by a reader with no other context.
4. A run in a full clone is unchanged from today's behaviour.

## Non-goals

- Deciding whether `/preflight` becomes a gate. That is ADR-119 / `[#664]` and is not
  settled here; this intake makes the organ *fit* to be gated, nothing more.
- Fetching history to deepen a clone so the leg can answer. Whether that is acceptable is
  an open question below, not an assumption.
- Any change to the heading, file-line or backlog-id legs' semantics.

## Impact sketch (4+1 lite)

- **Logical:** a verdict domain gains a third member alongside pass and fail.
- **Process:** a cloud lane's preflight report becomes readable, which is the precondition
  for the ADR-119 wiring decision.
- **Development:** one module and its two test files.
- **Physical:** none — read-only, Layer-2 (ADR-28/36).

## Open questions

- Is "unverifiable" a pass, a fail, or a third exit code? This repo's posture doctrine cuts
  both ways and the choice is a technical-architect question, not one to guess here.
- Should the verifier detect the shallow clone itself, or be told by its caller? Technical.
- Does the same miss exist in the freeze-time predicates (`--freeze`)? Unmeasured.

## Status

DRAFT — filed by lane `lane-z-11-three-repo-comparison`, 2026-09-15. Not triaged.
