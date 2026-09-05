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
