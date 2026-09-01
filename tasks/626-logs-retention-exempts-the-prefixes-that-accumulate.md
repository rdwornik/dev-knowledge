---
id: "[#626]"
title: "`logs/` does not thin — the retention rule exempts the two prefixes that actually accumulate"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#626] [P2][M] **`logs/` does not thin — the retention rule exempts the two prefixes that actually accumulate** — HY-2 (`[#614]` batch E, merged `1c92024f`) built the retention MECHANISM and it is correct: dated files relocate into `logs/YYYY-MM/` byte-identically, month buckets rather than day buckets so a single file does not mint a folder (Z-G5). **But its dry run against this repo is a NO-OP, and that is the row.** `logs/TOKEN-LOG.md` is excluded absolutely and rightly (ADR-29/39 strict append-only, and the 2026-07-17 archival carve-out is LESSONS.md-only in as many words). `PROPOSALS-*.md` and `DETECTOR-ERROR-*.md` are excluded **by prefix**, and those are exactly the files that accumulate — because two live callers glob them FLAT: `propose_closures.resolve_window` / `find_last_proposals_head`, and `review_closures.latest_proposals`. **So the organ is ahead of the next producer and behind none of them, and the operator's complaint that `logs/` never visibly thins stands until the exemption is retired rather than documented.** · Done when: both callers resolve a bucketed path (`logs/YYYY-MM/PROPOSALS-*.md`) as well as a flat one, with a test per caller proving a bucketed file is found; the two prefix exemptions are REMOVED from `logs_retention` with its fire-test updated; a live run relocates the accumulated files; and `git status` is clean afterwards, since the closure detector's pending-window baseline is what a wrong move corrupts · **Sequencing is the risk, not the code:** re-point the callers FIRST and prove them green, then retire the exemption — the reverse order breaks the closure loop between two commits · refs `scripts/logs_retention.py`, `scripts/propose_closures.py`, `scripts/review_closures.py`, `docs/audits/2026-09-01-verification-batche-post-merge-terra-round.md` (the round that also found this organ had no bound on its target directory) · kill-candidates: none — no open row owns `logs/` retention; `[#614]`'s HY-2 built the mechanism and closed with the exemption named as owed · source: operator addendum (b), 2026-09-01
