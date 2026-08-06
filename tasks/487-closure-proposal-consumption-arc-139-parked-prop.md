---
id: "[#487]"
title: "Closure-proposal consumption arc — repair the pipeline first"
status: open
priority: P2
size: L
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#487] [P2][L] **Closure-proposal consumption arc — repair the pipeline first** — `propose_closures.py` writes `logs/PROPOSALS-*.md` each session; nothing consumes them, 149 parked. Precedent: 132 WEAK triaged, **0 closable** ([#277] at n=132) — the heuristic keys on churn in big files. **Re-scoped 2026-08-06, pipeline-repair-first** (adjudicating a broken pipeline's output re-parks it): (i) **write the checkbox** — the confirm convention is documented (`:310`) and validated (`validate_backlog.py:67`) but nothing emits `- [x]`; (ii) **unpin `since_commit`** — an unchecked-still-open id pins the baseline (`resolve_window`), so absent (i) one ancient WEAK id holds the window open; (i) unblocks (ii); (iii) **token detection**, twin-pinned (`:51` + the tier1-lifecycle copy): `fixes?` matches `fixe`/`fixes` not `fix`, so `fix [#N]` is missed → `fix(?:es)?`, folding [#432]; (iv) symbol-anchor over line numbers. Sheet + adjudication follow. · Done when: (i)-(iv) land twin-in-lockstep, a ranked sheet covers the set, verdict each, and a cadence prevents re-accumulation · refs scripts/propose_closures.py, #277, #271, #432 · kill-candidates: none — [#271] owns the LOOP, not consumption
