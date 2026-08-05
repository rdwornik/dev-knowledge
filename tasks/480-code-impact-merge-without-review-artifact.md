---
id: "[#480]"
title: "A code-impact merge with no codex-review artifact is mechanically invisible — make the absence surface"
status: closed
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#480] [P3][M] **A code-impact merge with no codex-review artifact is mechanically invisible — make the absence surface** — the 2026-08-02 W2 report recorded “terra review: zero findings on both arcs” while NO artifact existed anywhere. The claim was never refuted; it was UNFALSIFIABLE, and nothing in the repo could tell the two apart. All 88 prior codex reviews left a `docs/audits/<date>-codex-<slug>.md`, so the convention is strong enough to check against. Cured retroactively for W2, but the MECHANISM gap remains: a review claim is trusted prose. Needs a ruling FIRST on whether an artifact is REQUIRED for a code-impact merge and what counts as code-impact — the check is cheap, the policy is not. · Done when: the ruling is recorded AND, if required, a code-impact merge lacking its review artifact is surfaced by a named organ with a test · refs docs/audits/2026-08-03-technical-night-la-w2-verification.md, ADR-70, #431, #469 · kill-candidates: none — no row owns review-artifact presence; [#431]/[#469] own the wrapper's routing and model pin, not whether a review happened · evidence n=6: docs/audits/*codex-arc[23]-[tvm]*.md; JOURNAL (i)(k) · serialize-group: audit-py

**CLOSED 2026-08-05 — the ruling plus its advisory leg IS this row's deliverable.**

**The ruling (P3, architect, 2026-08-05): LAYERED.** An artifact is required for a code-impact merge, surfaced by an ADVISORY WARN-tier audit leg NOW; the HARD pre-push leg is DEFERRED behind an evidence bar of **0 false positives over two consecutive windows, reported at each seal**. The hard flip is filed as **[#499]** carrying that bar as its peg — a deferral that is tracked, not a disclaimer (ADR-81 (d)).

**Shape (b), forward-only.** One canonical machine-parseable header: a `**Tally:** <C>/<H>/<M>/<L>` line plus Branch, HEAD and Model fields. Measured before it was ruled — across all 108 codex artifacts `Branch` appears 99x, `HEAD` 97x, and a tally line **zero** times — so the grammar codifies what already exists and adds exactly one line. It applies FORWARD-ONLY from the ruling date: the 9/16 legacy artifacts matching no recognised shape are immutable records and are never retro-edited, which the leg's date filter makes mechanically true rather than merely promised.

**Delivered:** `audit.check_review_artifact_coverage` (WARN-tier, registered in `ALL_CHECKS`, structurally incapable of the hard verdict — asserted at the source via `inspect.getsource`, not merely observed), 19 tests in `tests/test_review_artifact_coverage.py`, and this arc's own review artifacts written in the canonical shape (dogfooded). The code-impact predicate is suffix `.py`/`.ps1` + prefix `scripts/`/`deploy/`/`tests/`/`plugins/` + the EXACT paths `.pre-commit-hooks.yaml` and `.pre-commit-config.yaml` (operator amendment 2026-08-05 — the two files where this window's own enforcement defects lived); further paths arrive by ruling, never by sweep.

**Honest limit, carried in the check's docstring:** it verifies an artifact EXISTS, is LINKED, and carries a PARSEABLE tally. It cannot verify the review happened, was competent, or that the tally is truthful — a fabricated header passes. It converts an unfalsifiable claim into a checkable one; it does not make it a true one.

**One defect found and fixed pre-merge, recorded because the cost was measured rather than estimated:** the first implementation ran `git log -1 --format=%cs <sha>` per first-parent spine entry — 1317 entries, **236 seconds** — inside `audit-health`, which is a PRE-COMMIT gate, so it would have added roughly four minutes to every commit in this repo. Batched to a single whole-spine `--format=%H %cs` walk: **2.9s**, identical verdict. Pinned by `test_spine_date_lookup_stays_batched`, asserted on the SOURCE rather than by wall-clock (a timing assertion is flaky under load and gets muted first) and not by call-counting (the dual-import idiom means a monkeypatched `journal_anchor._git` can silently read zero).
