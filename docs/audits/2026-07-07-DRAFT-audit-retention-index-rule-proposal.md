# DRAFT — Audit retention + index-currency rule proposal (pairs with #212)

> **STATUS: DRAFT — decision-reserved.** Overnight mission Block 4, unmerged branch. Proposes the
> ADR-class RULE that Block 3.3 deliberately deferred (the index artifact shipped; the policy did
> not). Pairs with **#212** (`docs/handoffs/**` retention/rollup) — both are the corpus's
> uncontrolled-growth vectors.

## 1. The two uncontrolled-growth vectors

| Vector | Count (2026-07-07) | Immutability | Current policy |
|---|---|---|---|
| `docs/audits/**` | 193 `.md` | immutable dated artifacts | **none** — unbounded; now has an index (Block 3.3) |
| `docs/handoffs/**` | ~416 bundles (#212) | immutable (ADR-82) | **none** — #212 open |

Both grow monotonically and immutably by design. The hub already condenses two OTHER accretion
vectors — doc section-history (ADR-49/65 → git pointer) and BACKLOG inline-history (`doc_rot`) —
but the two immutable dated-artifact trees have no deliberate call. #212 asks it for handoffs;
this asks it for audits; they should be decided together (same class, same mechanism candidates).

## 2. Two distinct questions

- **Q1 — Retention/roll-up:** should audits older than N be compacted/rolled-up (the ADR-49/65
  condense-to-git pattern applied to the audit tree), or is "keep all, unbounded" explicitly
  accepted with a recorded reason?
- **Q2 — Index currency:** the Block-3.3 `docs/audits/README.md` index has **no freshness gate**
  (deliberately deferred) — a new audit file silently staled it. Should it gain a
  `audit-index-freshness` pre-commit hook (mirroring `roster-freshness` / `claude-rosters-freshness`),
  or is a manual/periodic regen enough?

## 3. Options

**For Q1 (retention):**
- (1a) **Keep-all, accepted.** Record "unbounded audit growth is accepted; the index makes it
  navigable" as the deliberate call. Cheapest; the index is the mitigation. Pro: audits are the
  evidence spine — deleting/rolling them up loses grep-able history. Con: the tree grows forever.
- (1b) **Roll-up by year.** Audits older than the current year compact into a per-year digest
  (title + one-line + link to the git blob), the individual files moving to an archive path or
  staying but de-indexed. Pro: bounds the ACTIVE surface. Con: a compaction mechanism to build +
  the evidence-integrity question (an audit cited by an ADR must stay resolvable).
- (1c) **Age-tier the index only.** Keep every file; the index shows the last N months in full and
  older months collapsed to a count + link. Pro: navigability without touching the files. Con: none
  major — this is the low-risk middle.

**For Q2 (index currency):**
- (2a) **Add the freshness hook** — the fragment-gate pattern is proven (`roster-freshness`,
  `claude-rosters-freshness`); one more hook, +1 gate count. Catches drift on commit.
- (2b) **Manual/periodic regen** — regenerate at session wrap / handoff; no gate. Lighter, but the
  index rots between wraps.

## 4. Recommendation (draft — architect rules)

- **Q1 → (1a) keep-all-accepted + (1c) age-tier the index** as the mitigation. Audits are the
  evidence spine (ADRs, LESSONS, and this very ledger cite them by path) — rolling them up risks
  breaking those citations, and the storage cost is trivial. The honest call is "unbounded
  accepted, made navigable by an age-tiered index." Reconcile with **#212**: apply the SAME verdict
  to handoffs (keep-all-accepted + an index) unless the operator wants handoffs rolled up
  (they're heavier — 416 bundles — so #212 may legitimately diverge toward roll-up).
- **Q2 → (2a) add the freshness hook** once Q1's index shape is settled (an age-tiered index still
  regen-checks cleanly). Deferred from Block 3.3 precisely so this rule decides it.
- **This is ADR-class** (a retention policy over an immutable tree, sibling to ADR-49/65). File it
  as one ADR covering BOTH audits and handoffs (closing #212's policy question in the same
  decision), or two siblings. **Decision reserved.**
