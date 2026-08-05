---
id: "[#487]"
title: "Closure-proposal consumption arc — 139 parked proposals + 2 fleet issues have no consumption path"
status: open
priority: P2
size: L
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#487] [P2][L] **Closure-proposal consumption arc — 139 parked proposals + 2 fleet issues have no consumption path** — `propose_closures.py` has written `logs/PROPOSALS-*.md` every session since the Tier-1 loop went live and nothing consumes them: detect-and-propose with no adjudication step, so the parked set only grows. Measured precedent: the cloud triage below classified 132 WEAK proposals and found **0 plausibly-closable** — reproducing [#277]'s near-zero-precision diagnosis at n=132 instead of n=49, because the WEAK heuristic keys on churn in large canonical files. So the arc is NOT "work the backlog": fan-out builds the ranked sheet (retrieval), the **architect adjudicates** (judgment). · Done when: a ranked sheet exists for the full parked set, every proposal carries an architect verdict, and the loop has a stated consumption cadence so the set cannot re-accumulate · refs scripts/propose_closures.py, docs/audits/2026-07-30-technical-proposals-2026-07-29-triage.md, #277, #271 · kill-candidates: none — [#271] owns the nightly proposal LOOP, not the consumption of what it parks
