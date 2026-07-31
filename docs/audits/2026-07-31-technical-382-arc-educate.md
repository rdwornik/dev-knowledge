# [#382] arc educate report — desired-state contract v1, W1–W4 (the so-whats)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** 382-arc-educate
- **What this is:** the arc-closure educate record the [#382] execution brief owes — one
  so-what paragraph per merged wave, plus the §C/§H verdicts and the cross-model review
  result. Written for the operator's two-minute read; every claim is anchored in the wave
  merges (`7ef40567` W1 · `d163680a` W2 · `ee176854` W3 · W4 merge pending at write time).

## W1 — ADR-109 (so what)

The fleet now has ONE ruled answer to "what are the four registries and what happens to
them" — a question the North Star asserted for ten days without anyone being able to name
the four. The answer came out of the intake's own mapping table (deployed-versions.yaml is
the STATE file, so the four are the OTHER four), which means the enumeration is derived
from ruled inputs, not invented. The operator's §E paragraph is transcribed verbatim as the
chain's functional requirement, so every later arc closes against operator intent instead
of only technical Done-whens. The independent-derivation rule ran for real: sol derived the
schema blind, nine divergences were adjudicated one by one, and three of sol's structures
(the desired/observed root split, the lossless lifecycle assertions, the component layer)
beat CC's first draft and shipped.

## W2 — schema v1 (so what)

Every cross-registry contradiction the prep dossier catalogued (C1–C8) is now either a
typed field or a computable derivation — a contradiction between registries stopped being
an error and became data. The honesty constraints are structural, not aspirational: the
allocation type CANNOT claim concurrent-allocation prevention (the Literal admits only
"not-provided"), a source-of-truth manifest CANNOT also claim to be derived, and a
gate-rev-ahead declaration CANNOT waive. The review loop earned its cost in one pass:
terra caught the under-built root, and grok caught two load-breaking defects terra missed
— `RefKind` lacking the live `audit` provenance kind, and four Surface fields whose
on-disk shape is a dict where the schema held scalars. Both would have detonated in W3 on
first contact with the real yaml. They didn't, because the shadow lane ran.

## W3 — loader (so what)

The live fleet loads end-to-end into one validated model: 8-repo union, 5 resolved members
(the deployed-versions anchor), the corp gate sanctioned-divergence as a typed declaration,
the 20-day-stale audit rollup surfaced as data instead of read as current. The
witnessed-behavior discipline cut both ways: terra's "backticked paths" finding was
disk-verified TRUE (the fixture under-reproduced the live table), its H3 finding exposed
CC violating its own D2 adjudication (synthesizing lifecycle from role), and grok's earlier
"81/81" overcount was disk-refuted — reviewer claims got the same verify-first treatment as
CC's own.

## W4 — divergence report (so what)

The operator's two-minute read exists. The live render: **185 conform · 3 diverge · 3
declared · 219 n/a** — and the 3 diverges are precisely the real, previously-invisible
gaps (ai-council deployed 1.3.1 against the declared 1.4.0 target — the G11 gap that had
no field anywhere; corp-ops and corp-sca ruled `full` with nothing deployed — the C3 gap
between a ruling and a state file that never referenced each other). corp-monorepo's
sanctioned gap renders **declared**, not red — the report distinguishes "diverged" from
"diverged with a ruling behind it", which is the entire point of the declaration layer.
The review loop moved these numbers before merge: terra's W4 pass (6 High, all accepted)
caught 11 FALSE-declared cells (repo tier rows equal to their role baseline are not
departures), made the gate-ahead declaration self-invalidate once its tag is reached, and
narrowed the C3 verdict to ruled-full repos only. "Conform" is defined in the report's own
limits block as *no divergence DECLARED* — the declaration layer, never a probe result;
observational joins await the G9 crosswalk (#383); fleet_parity keeps the probes.

## §C verdict — grok shadow vs terra (one artifact: 2026-07-31-technical-382-w2-grok-shadow-ab.md)

Complementary, not redundant: grok verified against live disk state and caught the two
load-breakers; terra reasoned against the spec and caught the architectural under-build.
One grok factual overstatement (81/81 → 1) was corrected on disk-verify. Cost leg honestly
inconclusive — neither CLI exposes token pricing; wall-clock comparable (~5 min each).
Recommendation on record: keep the grok shadow for foundational diffs; the operator's
"cheaper-and-possibly-better" hypothesis is *better-in-part witnessed, cheaper unproven*.

## §H verdict — portability

Witnessed: the process ran multi-provider end-to-end with no model owning it — sol (OpenAI)
derived, terra (OpenAI) and grok (xAI) reviewed with accepted Criticals from each, CC
(Anthropic) built, the operator stayed the serial gate. NOT witnessed: a non-Claude
BUILDER. Three debt items on record in the §C/§H artifact: the builder-role probe itself,
a repeatable grok wrapper, and the harness-specific review plumbing.

## Carried out of the arc

[#457] the two inherited test failures (test-vs-organ mismatch) · [#458] the
gates-never-race-commits PLAYBOOK note · ADR-109 §4 generality-pending (owner [#383]
wave 1: the §6.2 second-surface proof) · §H builder-probe debt (natural slot: an [E9]
wave with grok/Codex as builder).
