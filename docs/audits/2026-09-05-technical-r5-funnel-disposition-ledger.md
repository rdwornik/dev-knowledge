# R5 funnel-coverage disposition ledger — the 13 that survived the manifest-link hotfix

- **Class:** technical · **Date:** 2026-09-05 · **Arc:** `[#552]` · **Window:** R5 dispositioning
- **Author:** CC (Opus 5, FILINGS-3 seat) · **Ruling:** ARCHITECT-INBOX-2026-09-05-007 bundles **B3 + B4**, declared by the operator in `to-cc/R5-DECLARED.md`
- **Consumed by:** `[#552]` (window-close disposition routine — *"one window closes with every new audit dispositioned"*), and the R5 window's close

> **THE SELF-DISCHARGE RULE (architect ruling, R5/B3, 2026-09-05).** *A disposition ledger
> self-discharges by construction: it carries a row naming itself, so using the mechanism can
> never mint the very debt it exists to clear.* Without that row every ledger would land as a
> new undispositioned artifact and the mechanism would be strictly net-neutral at best — the
> recursion the R5 disposition sheet flagged. The same rule is now stated at the point of
> enforcement, in `scripts/funnel_coverage.py`'s module docstring.

## 1 · Why this file exists, and why it is a NEW file

The R5 disposition sheet (`docs/audits/2026-09-05-technical-r5-disposition-sheet.md`, measured
at `main` @ `6de676fb`) grouped 32 `funnel_coverage` rows into bundles B3 (10 net-new batch-G
artifacts) and B4 (22 inherited). Both were ruled **fix-now**, one artifact, same act.

**Re-measured at `main` @ `ac2c6a15` before acting, as item 007 requires** — and the count moved
far more than the sheet's "a row or two". The B1 manifest-link hotfix (`ac2c6a15`, *"an audit
linked from a batch manifest counts as CITED and DISPOSITIONED"*) cleared **19 of the 32**:
`funnel_coverage` 32 → 13, and its sibling `consumer_at_landing` 16 → 6. The 13 below are what
a manifest link does not reach. The B3/B4 shape held exactly; only the population shrank.

**A new file rather than an append** because the existing ledger,
`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`, is an audit artifact and audits
are immutable (CLAUDE.md §5 rule 3). `funnel_coverage` admits **any** artifact carrying a
correctly-shaped table, so a new dated ledger is the compliant route rather than a workaround.

## 2 · The ruled vocabulary

Architect standing ruling of 2026-08-17, quoted verbatim at the head of the 2026-08-17 ledger
and in `scripts/funnel_coverage.py`:

> Every audit artifact carries exactly one disposition: ACTIONED (conclusion already live —
> cite the commit), FILED (a row owns it — cite the id), REJECTED (a ruling declined it —
> cite it), SUPERSEDED (a later artifact replaced it — cite it). An undisposed audit is a
> defect, not a document.

PENDING is admitted for the undecidable case, **with the exact question it needs** — *"a wrong
ACTIONED is worse than an honest PENDING"*. One row below is PENDING, and it is marked as the
one place in this ledger where the disposition is not yet a decision.

## 3 · The ledger

| file | disposition | evidence locator |
|---|---|---|
| 2026-09-01-technical-629-630-lane-g-packet.md | FILED | `[#629]` + `[#630]` — the packet's own title names both rows; lane-g-7 end-of-lane packet |
| 2026-09-01-technical-agy-admission-verdict.md | FILED | `[#627]` — agy analysis-role admission, measured and REFUSED; sibling ref `[#578]` |
| 2026-09-01-technical-article-harness-substrate-brief.md | REJECTED | R5 window bundle **B2**, ruled 2026-09-05: an operator-commissioned external research brief, landed verbatim with a §0 provenance record. It has **no governance consumer by design** — it feeds an article outside the hub, so it is genuinely unconsumed rather than mis-measured. |
| 2026-09-01-technical-atlas-r1-layer-graph.md | FILED | `[#615]` — ATLAS-R1 sidecar to the landed HTML artifact |
| 2026-09-01-technical-batchf-derivation.md | FILED | `[#614]` — batch-F derived state, cut for the architect |
| 2026-09-01-technical-boot-r1-prioritization-scheduling.md | FILED | `[#611]` — BOOT-R1 prioritization/scheduling for a task graph |
| 2026-09-01-technical-v7-history-delta-equilibrium-map.md | FILED | `[#614]` — declared Arc in the artifact's own header line |
| 2026-09-01-verification-atlas-r1-harvest-attempt.md | FILED | `[#614]` — declared Arc; consumed-by `[#614]` per its header |
| 2026-09-01-verification-batchf-integration-suite.md | FILED | `[#614]` — declared Arc `[#614]`/`[#632]`/`[#528]`; supersedes the batch-F close packet §9 second bullet |
| 2026-09-01-verification-codespace-admission-report.md | FILED | `[#632]` — independent codespace-admission witness, named in its own title |
| 2026-09-01-verification-model-routing-witness.md | FILED | `[#614]` — declared Arc; consumed-by `[#614]`, `[#615]` per its header |
| 2026-09-02-technical-lane-g-626-terra-tally.md | FILED | `[#626]` — G4 terra pre-merge tally and the blocked release act |
| 2026-09-05-technical-corpus-coherence-gemini.md | PENDING | Q: candidate (g) — does the Gemini whole-corpus reader's finding set become a backlog row, or stay a Z-C register candidate owned by the STANDING_RULINGS writer? The artifact carries no `[#id]` because none has been allocated yet; FILINGS-1 holds the Z-C register for this inbox, so naming an owner here would be this seat deciding another seat's allocation. |
| 2026-09-05-technical-r5-funnel-disposition-ledger.md | FILED | `[#552]` — **the self-discharging row.** This ledger is owned by the window-close disposition routine whose Done-when is *"one window closes with every new audit dispositioned"*; see the self-discharge rule at the head of this file. |

## 4 · Honest limits

- **This ledger clears `funnel_coverage`, not `consumer_at_landing`.** They are different
  questions over the same corpus — *was it dispositioned* versus *does anything consume it* —
  and `consumer_at_landing.POOL_DIRS` is `tasks/`, `docs/decisions/`, `docs/intake/`,
  `protocols/`. `docs/audits/` is excluded from that pool except for batch-manifest files and
  their `closed_by:` targets, so a row here is invisible to it **by construction**. Six
  `consumer_at_landing` rows therefore survive this act; only one of them (the article brief)
  is ruled, as B2.
- **FILED is verified for SHAPE, not for truth.** `funnel_coverage.locator_resolves` checks that
  a FILED locator matches `\[#\d+\]`; it does not check that the row exists, is open, or agrees.
  Each id above was read out of the artifact's own header rather than inferred, but the check
  would have accepted a wrong one.
- **One row is PENDING and is not coverage in the ordinary sense.** It is counted as *known*
  rather than *absent* — the mechanism's deliberate middle state, recorded so the distinction
  between "looked at, question open" and "never looked at" survives.

## 5 · R5 residue — the pre-batch unlinked artifacts (architect ruling 3, 2026-09-05 evening)

**What was ruled.** The residue this window surfaced but no 007 bundle owned — reported by me as
unowned at hand-off — is *"pre-batch unlinked artifacts, so they belong to R5 B3/B4's single
ledger"*. B3/B4 is mine, so the residue is filed here rather than left for whoever merged next.

**Measured, not relayed.** The hand-off shorthand was "25 + 17", which reads as 42. It is not:
`consumer_at_landing` reports **25** beyond its arm-time baseline and
`funnel_coverage`'s ratchet reports **17**, and **12** artifacts
appear in BOTH — so the true residue is **30 distinct artifacts**, of which
**6** already carried a row in §3 and **24** are added below.

**THIS IS A CLASS ROUTING, NOT 24 INDIVIDUAL ADJUDICATIONS, and the difference matters.**
Each row below files its artifact to `[#552]`, the window-close disposition routine whose
Done-when is *"one window closes with every new audit dispositioned"* — that row genuinely owns
the sweep. What no row below claims is that this seat opened each artifact and decided its
substantive owner. If any one of them deserves a different id, it takes precedence over the class
filing and this ledger is the place to record it.

**HONEST LIMIT — this section clears the funnel_coverage half and CANNOT clear the
consumer_at_landing half.** The two organs read different surfaces. `funnel_coverage` reads the
disposition ledger, so a row here disposes the artifact. `consumer_at_landing` asks whether a
GOVERNANCE POOL file cites the artifact, and its pool is `tasks/`, `docs/decisions/`,
`docs/intake/`, `protocols/` plus six root files — `docs/audits/` is **not** a citer, so a ledger
row is invisible to it by construction.

That is not a prediction; it is already visible in §3 above. Of the artifacts dispositioned there,
6 STILL appear in `consumer_at_landing`'s unconsumed set — dispositioned and
unconsumed at the same time, because the two organs were never asking the same question. Clearing
the consumer half needs a POOL-SIDE citer naming each artifact, which is the route `[#552]` used
for this ledger itself. That is a separate act on a separate surface and is NOT performed here;
recording the gap so no one reads a green funnel leg as both.

| file | disposition | evidence locator |
|---|---|---|
| 2026-08-29-technical-claude-md-regenre.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing. |
| 2026-09-05-technical-627-readjudication.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-aj-second-pass-lane-contract.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: funnel_coverage. |
| 2026-09-05-technical-batch-h0-manifest.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-batch-r5p-manifest.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-browser-prose-rule-census.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-browser-seat-notes.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: funnel_coverage. |
| 2026-09-05-technical-claude-md-section-history-ledger.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: funnel_coverage. |
| 2026-09-05-technical-fleet-readiness.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-funnel-groom-lane-contract.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-funnel-groom-sheet.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-lane-h0-trace-close.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-r5-disposition-sheet.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-r5p-lane1-docrot-arm2.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-technical-research-architekt-jutra-gap-analysis.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: funnel_coverage. |
| 2026-09-05-technical-research-python-quality-speed.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: funnel_coverage. |
| 2026-09-05-technical-v150-tag-checklist.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| 2026-09-05-verification-lane-h0-suite-speed.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening) onto this ledger as B3/B4's single disposition surface. Surfaced by: consumer_at_landing + funnel_coverage. |
| ARM3_NOTE.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-627-readjudication.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
| LANE-r-000-bundle-gitlog.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-batch-r5p-manifest.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
| LANE-r-000-docrot-arm2.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-batch-r5p-manifest.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
| LANE-r-000-zc-candidates.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-batch-r5p-manifest.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
| SEED_RUBRIC.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-627-readjudication.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
| VERDICT_RULE.md | FILED | `[#552]` — pre-batch unlinked artifact, routed by architect ruling 3 (2026-09-05 evening). COMPANION FILE of `2026-09-05-technical-627-readjudication.md`, which carries its own row in this same section; it is not an independent audit and inherits that parent's ownership. Surfaced by: consumer_at_landing. |
